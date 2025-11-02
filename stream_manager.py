"""Stream manager for handling fallback between RTMP and cloud animation."""

from __future__ import annotations

import threading
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from renderer import TerminalRenderer
    from rtmp_stream import RTMPStream
    from stream_source import StreamSource


class StreamManager:
    """Manages switching between RTMP stream and fallback cloud animation."""

    def __init__(
        self,
        rtmp_stream: RTMPStream | None,
        fallback_source: StreamSource,
        probe_interval: float = 5.0,
    ) -> None:
        """Initialize stream manager.

        Args:
            rtmp_stream: RTMP stream (primary source)
            fallback_source: Fallback animation source (e.g., CloudStream)
            probe_interval: How often to probe for stream availability in seconds
        """
        self.rtmp_stream = rtmp_stream
        self.fallback_source = fallback_source
        self.probe_interval = probe_interval
        self.current_source: StreamSource = fallback_source
        self.using_rtmp = False
        self.last_probe_time = 0.0
        self.stream_started = False
        self.terminal_size: tuple[int, int] | None = None

        # Background probing state
        self.probe_thread: threading.Thread | None = None
        self.probe_result: bool = False
        self.probe_lock = threading.Lock()

    def start(self, width: int, height: int) -> None:
        """Start the stream manager with given terminal dimensions.

        Args:
            width: Terminal width
            height: Terminal height
        """
        self.terminal_size = (width, height)

        # Try to start RTMP stream if configured
        if self.rtmp_stream and not self.stream_started:
            if self.rtmp_stream.start(width, height):
                self.current_source = self.rtmp_stream
                self.using_rtmp = True
                self.stream_started = True
            else:
                self.current_source = self.fallback_source
                self.using_rtmp = False

    def _probe_stream_background(self) -> None:
        """Background thread function to probe stream availability."""
        if self.rtmp_stream:
            result = self.rtmp_stream.probe_stream(self.rtmp_stream.rtmp_url)
            with self.probe_lock:
                self.probe_result = result

    def update(self, time_delta: float) -> None:
        """Update the current active source.

        Args:
            time_delta: Time elapsed since last frame in seconds
        """
        current_time = time.time()

        # If using RTMP, check if it's still available
        if self.using_rtmp and self.rtmp_stream:
            self.rtmp_stream.update(time_delta)

            if not self.rtmp_stream.is_available():
                # RTMP stream disconnected, properly stop it and switch to fallback
                self.rtmp_stream.stop()
                self.current_source = self.fallback_source
                self.using_rtmp = False
                self.stream_started = False

        # If using fallback, manage probing and reconnection
        elif not self.using_rtmp and self.rtmp_stream:
            # Start a new probe every probe_interval seconds
            if current_time - self.last_probe_time >= self.probe_interval:
                self.last_probe_time = current_time

                # Start background probe if not already running
                if self.probe_thread is None or not self.probe_thread.is_alive():
                    self.probe_thread = threading.Thread(
                        target=self._probe_stream_background, daemon=True
                    )
                    self.probe_thread.start()

            # Check probe result every frame (not just when starting new probe)
            with self.probe_lock:
                if self.probe_result and self.terminal_size:
                    # Stream is available, try to reconnect
                    width, height = self.terminal_size
                    if self.rtmp_stream.start(width, height):
                        self.current_source = self.rtmp_stream
                        self.using_rtmp = True
                        self.stream_started = True
                    self.probe_result = False  # Reset for next probe

        # Update the current active source
        self.current_source.update(time_delta)

    def render(self, renderer: TerminalRenderer) -> None:
        """Render the current active source.

        Args:
            renderer: The terminal renderer to draw to
        """
        self.current_source.render(renderer)

    def resize(self, width: int, height: int) -> None:
        """Handle terminal resize.

        Args:
            width: New terminal width
            height: New terminal height
        """
        self.terminal_size = (width, height)

        # Resize fallback source (CloudStream)
        if hasattr(self.fallback_source, "resize"):
            self.fallback_source.resize(width, height)

        # If using RTMP, restart with new dimensions
        if self.using_rtmp and self.rtmp_stream:
            self.rtmp_stream.stop()
            if self.rtmp_stream.start(width, height):
                self.stream_started = True
            else:
                self.current_source = self.fallback_source
                self.using_rtmp = False
                self.stream_started = False

    def is_available(self) -> bool:
        """Check if any source is available.

        Returns:
            Always True (fallback ensures availability)
        """
        return True

    def is_using_rtmp(self) -> bool:
        """Check if currently using RTMP stream (vs fallback).

        Returns:
            True if using RTMP stream, False if using fallback
        """
        return self.using_rtmp

    def next_logo_style(self) -> None:
        """Cycle logo style on the fallback source (CloudStream)."""
        if hasattr(self.fallback_source, "next_logo_style"):
            self.fallback_source.next_logo_style()

    def cleanup(self) -> None:
        """Clean up all resources."""
        # Wait for probe thread to complete if running
        if self.probe_thread and self.probe_thread.is_alive():
            self.probe_thread.join(timeout=1.0)

        if self.rtmp_stream:
            self.rtmp_stream.cleanup()
        self.fallback_source.cleanup()

    def get_status(self) -> str:
        """Get current status string.

        Returns:
            Status string indicating active source
        """
        if self.using_rtmp:
            return "RTMP Stream"
        return "Cloud Animation"
