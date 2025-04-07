import asyncio
import json
import signal
import ssl
import sys
from datetime import datetime
from urllib.parse import urlparse

import typer
import websockets
from loguru import logger

from trainwave_cli.api import Api, JobStatus
from trainwave_cli.config.config import config


def format_timestamp(ts: str | None) -> str:
    """
    Convert a nanosecond timestamp to a human-readable datetime string.

    Args:
    ----
        ts: Timestamp in nanoseconds as a string, or None

    Returns:
    -------
        Formatted datetime string in YYYY-MM-DD HH:MM:SS.ffffff format, or empty string if ts is None

    """
    if ts is None:
        return ""
    timestamp = int(ts) / 1e9
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime("%Y-%m-%d %H:%M:%S.%f")


def setup_logger():
    """
    Configure the logger with appropriate formatting for the logs command.

    Removes any existing handlers and adds a new handler that outputs to stdout
    with colorized timestamps and messages.
    """
    logger.remove()
    logger.add(
        sys.stdout,
        format="<green>{extra[log_time]}</green> | <white>{message}</white>",
        colorize=True,
        serialize=False,
        level="DEBUG",
        enqueue=True,
        catch=True,
    )


def build_websocket_uri(job_id: str) -> str:
    """
    Construct the WebSocket URI for connecting to job logs.

    Args:
    ----
        job_id: The ID of the job to connect to

    Returns:
    -------
        Complete WebSocket URI including protocol, host, port, path, and API key

    """
    parsed = urlparse(config.endpoint)
    scheme = "wss" if parsed.scheme == "https" else "ws"
    port = f":{parsed.port}" if parsed.port else ""
    return (
        f"{scheme}://{parsed.hostname}{port}/ws/logs/{job_id}/?api_key={config.api_key}"
    )


def get_ssl_context(uri: str) -> ssl.SSLContext | None:
    """
    Create an SSL context for secure WebSocket connections.

    Args:
    ----
        uri: The WebSocket URI to check

    Returns:
    -------
        SSL context with certificate verification disabled for trainwave.dev domains,
        or None if no SSL context is needed

    """
    if "trainwave.dev" in uri:
        ssl_context = ssl.SSLContext()
        ssl_context.verify_mode = ssl.CERT_NONE
        return ssl_context
    return None


class LogsConnection:
    """
    Manages a WebSocket connection for streaming job logs.

    This class handles the lifecycle of a WebSocket connection, including:
    - Setting up signal handlers for graceful shutdown
    - Establishing and maintaining the connection
    - Processing incoming log messages
    - Cleaning up resources when the connection is terminated
    """

    def __init__(self, job_id: str):
        """
        Initialize a new logs connection.

        Args:
        ----
            job_id: The ID of the job to connect to

        """
        self.job_id = job_id
        self.shutdown_event = asyncio.Event()
        self.websocket = None
        self.original_sigint = None
        self.original_sigterm = None

    def setup_signal_handlers(self):
        """
        Register signal handlers for graceful shutdown.

        Saves the original handlers and sets up new handlers for SIGINT and SIGTERM
        that will trigger the shutdown event when received.
        """

        def handle_sigint(sig, frame):
            self.shutdown_event.set()

        def handle_sigterm(sig, frame):
            self.shutdown_event.set()

        self.original_sigint = signal.getsignal(signal.SIGINT)
        self.original_sigterm = signal.getsignal(signal.SIGTERM)
        signal.signal(signal.SIGINT, handle_sigint)
        signal.signal(signal.SIGTERM, handle_sigterm)

    def restore_signal_handlers(self):
        """
        Restore the original signal handlers.

        Called during cleanup to ensure the application's signal handling
        returns to its original state.
        """
        if self.original_sigint:
            signal.signal(signal.SIGINT, self.original_sigint)
        if self.original_sigterm:
            signal.signal(signal.SIGTERM, self.original_sigterm)

    async def close_websocket(self):
        """
        Safely close the WebSocket connection.

        Attempts to close the connection if it exists and is not already closed,
        catching and ignoring any exceptions that might occur during closure.
        """
        if self.websocket and not self.websocket.closed:
            try:
                await self.websocket.close()
            except Exception:
                pass

    async def process_message(self, message: str):
        """
        Process and display a log message.

        Parses the JSON message, extracts the log content and timestamp,
        and outputs it to the logger with appropriate formatting.

        Args:
        ----
            message: The raw JSON message received from the WebSocket

        """
        data = json.loads(message)
        logger.info(data["message"], log_time=format_timestamp(data.get("ts")))

    async def connect_and_listen(self):
        """
        Establish a WebSocket connection and listen for log messages.

        Connects to the job logs endpoint, sets up a message processing loop,
        and handles various connection states and errors. The loop continues
        until the shutdown event is set or the connection is closed by the server.
        """
        uri = build_websocket_uri(self.job_id)
        ssl_context = get_ssl_context(uri)
        opts = {"ssl": ssl_context} if ssl_context else {}

        try:
            async with websockets.connect(uri, **opts) as ws:
                self.websocket = ws
                typer.echo(f"Connected to logs for job {self.job_id}")

                while not self.shutdown_event.is_set():
                    try:
                        # Use a timeout to periodically check if we should shut down
                        response = await asyncio.wait_for(ws.recv(), timeout=1.0)
                        await self.process_message(response)
                    except asyncio.TimeoutError:
                        # This is expected, just continue to check shutdown_event
                        continue
                    except websockets.exceptions.ConnectionClosed:
                        typer.echo("Connection closed by server.")
                        break
        except Exception as e:
            typer.echo(f"Error in logs connection: {e}")
        finally:
            await self.close_websocket()
            typer.echo("Logs connection terminated.")


async def check_job_status(job_id: str) -> bool:
    """
    Verify if a job is in a state that allows log streaming.

    Queries the API to get the current state of the job and checks if
    it has progressed beyond the initial setup phases.

    Args:
    ----
        job_id: The ID of the job to check

    Returns:
    -------
        True if the job is ready for logs, False otherwise

    """
    api_client = Api(config.api_key, config.endpoint)
    job = await api_client.get_job(job_id)

    if job.state in (JobStatus.SUBMIT_CODE, JobStatus.LAUNCHING):
        typer.echo(f"Job {job_id} has not started yet.")
        return False

    return True


async def stream_logs(job_id: str):
    """
    Stream logs for a specified job.

    Orchestrates the entire logs streaming process:
    1. Verifies the job is in a state that allows log streaming
    2. Sets up the logger with appropriate formatting
    3. Creates and manages a WebSocket connection
    4. Handles graceful shutdown when interrupted

    Args:
    ----
        job_id: The ID of the job to stream logs for

    """
    if not await check_job_status(job_id):
        typer.Exit(1)

    setup_logger()

    logs_connection = LogsConnection(job_id)
    logs_connection.setup_signal_handlers()

    try:
        await logs_connection.connect_and_listen()
    finally:
        logs_connection.restore_signal_handlers()
