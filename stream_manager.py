"""Stream manager for handling fallback between RTMP and cloud animation."""

from __future__ import annotations

import sys
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from renderer import TerminalRenderer
    from rtmp_stream import RTMPStreamCapture
    from stream_source import StreamSource


class StreamManager:
    """Manages switching between RTMP stream and fallback cloud animation."""

    def __init__(
        self,
        rtmp_stream: RTMPStreamCapture | None,
        fallback_source: StreamSource,
        probe_interval: float = 5.0,
    ) -> None:
        """Initialize stream manager.

        Args:
            rtmp_stream: RTMP stream capture (primary source)
            fallback_source: Fallback animation source (e.g., CloudSystem)
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
                print("RTMP stream connected", file=sys.stderr)
            else:
                print(
                    "Failed to connect to RTMP stream, using fallback animation",
                    file=sys.stderr,
                )
                self.current_source = self.fallback_source
                self.using_rtmp = False

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
                # RTMP stream disconnected, switch to fallback
                print(
                    "RTMP stream disconnected, switching to fallback animation",
                    file=sys.stderr,
                )
                self.current_source = self.fallback_source
                self.using_rtmp = False
                self.stream_started = False

        # If using fallback, periodically probe for RTMP availability
        elif (
            not self.using_rtmp
            and self.rtmp_stream
            and current_time - self.last_probe_time >= self.probe_interval
        ):
            self.last_probe_time = current_time

            # Probe stream availability
            if self.rtmp_stream.probe_stream(self.rtmp_stream.rtmp_url) and self.terminal_size:
                # Stream is available, try to reconnect
                width, height = self.terminal_size
                if self.rtmp_stream.start(width, height):
                    print(
                        "RTMP stream reconnected, switching from fallback",
                        file=sys.stderr,
                    )
                    self.current_source = self.rtmp_stream
                    self.using_rtmp = True
                    self.stream_started = True

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

        # If using RTMP, restart with new dimensions
        if self.using_rtmp and self.rtmp_stream:
            self.rtmp_stream.stop()
            if self.rtmp_stream.start(width, height):
                self.stream_started = True
            else:
                print(
                    "Failed to restart RTMP stream after resize",
                    file=sys.stderr,
                )
                self.current_source = self.fallback_source
                self.using_rtmp = False
                self.stream_started = False

    def is_available(self) -> bool:
        """Check if any source is available.

        Returns:
            Always True (fallback ensures availability)
        """
        return True

    def cleanup(self) -> None:
        """Clean up all resources."""
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
