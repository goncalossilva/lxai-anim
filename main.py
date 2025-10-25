#!/usr/bin/env python3
from __future__ import annotations

import signal
import sys
import time
from typing import TYPE_CHECKING

from clouds import CloudSystem
from keyboard import KeyboardHandler
from renderer import TerminalRenderer
from rtmp_stream import RTMPStreamCapture
from stream_manager import StreamManager
from typography import LXAITypography

if TYPE_CHECKING:
    from types import FrameType

    from stream_source import StreamSource


class Animation:
    """Main animation controller."""

    def __init__(
        self,
        fps: int = 30,
        logo_style: str = "bold",
        render_style: str = "dots",
        rtmp_url: str | None = None,
    ) -> None:
        """
        Initialize the animation.

        Args:
            fps: Target frames per second
            logo_style: Style for the LisbonAI logo
            render_style: Rendering style for dithering
            rtmp_url: Optional RTMP stream URL to render
        """
        self.fps: int = fps
        self.frame_time: float = 1.0 / fps
        self.running: bool = False
        self.start_time: float = 0.0
        self.elapsed_time: float = 0.0

        # Initialize components
        self.renderer: TerminalRenderer = TerminalRenderer(style=render_style)
        self.typography: LXAITypography = LXAITypography(style=logo_style)
        self.keyboard: KeyboardHandler = KeyboardHandler()

        # Initialize stream source (either RTMP with cloud fallback, or just clouds)
        clouds = CloudSystem(self.renderer.width, self.renderer.height)
        if rtmp_url:
            # Check if ffmpeg is available before attempting to use RTMP
            if not RTMPStreamCapture.is_ffmpeg_available():
                print(
                    "Warning: ffmpeg not found. Install ffmpeg to use RTMP streaming.",
                    file=sys.stderr,
                )
                print("Falling back to cloud animation only.", file=sys.stderr)
                self.stream_source: StreamSource = clouds
            else:
                rtmp_stream = RTMPStreamCapture(rtmp_url, target_fps=fps)
                manager = StreamManager(rtmp_stream, clouds, probe_interval=5.0)
                manager.start(self.renderer.width, self.renderer.height)
                self.stream_source = manager
        else:
            self.stream_source = clouds

        # Animation parameters
        self.logo_fade_duration: float = 3.0
        self.logo_float_amplitude: float = 3.0
        self.logo_float_frequency: float = 0.3

        # Auto-cycling parameters
        self.auto_cycle_enabled: bool = True
        self.auto_cycle_interval: float = 30.0  # in seconds
        self.last_style_change: float = 0.0

    def setup(self) -> None:
        """Setup the animation."""
        self.renderer.hide_cursor()
        self.keyboard.setup()
        self.start_time = time.time()
        self.running = True

    def cleanup(self) -> None:
        """Cleanup and restore terminal."""
        self.stream_source.cleanup()
        self.keyboard.cleanup()
        self.renderer.show_cursor()
        self.renderer.clear_buffer()
        self.renderer.render()

    def handle_input(self) -> None:
        """Handle keyboard input."""
        key = self.keyboard.get_key()
        if key:
            if key == "n":
                # Cycle to next rendering style and disable auto-cycling
                self.auto_cycle_enabled = False
                self.renderer.next_style()
            elif key == "m":
                # Cycle to next text/logo style
                self.typography.next_style()
            elif key == "q":
                # Quit the animation
                self.running = False

    def update(self, delta_time: float) -> None:
        """Update animation state."""
        self.elapsed_time = time.time() - self.start_time
        self.stream_source.update(delta_time)

        # Auto-cycle rendering styles every 30 seconds if enabled
        if (
            self.auto_cycle_enabled
            and self.elapsed_time - self.last_style_change >= self.auto_cycle_interval
        ):
            self.renderer.next_style()
            self.last_style_change = self.elapsed_time

    def render(self) -> None:
        """Render the current frame."""
        # Clear buffer
        self.renderer.clear_buffer()

        # Render stream source (RTMP or clouds)
        self.stream_source.render(self.renderer)

        # Render LisbonAI typography at bottom-right, fixed position
        self.typography.render_bottom_right(
            self.renderer,
            margin_x=10,
            margin_y=2,
            opacity=1.0,
        )

        # Display to terminal
        self.renderer.render()

    def run(self) -> None:
        """Main animation loop."""
        self.setup()

        try:
            last_time = time.time()

            while self.running:
                current_time = time.time()
                delta_time = current_time - last_time
                last_time = current_time

                # Handle input
                self.handle_input()

                # Update and render
                self.update(delta_time)
                self.render()

                # Frame timing
                frame_end = time.time()
                sleep_time = self.frame_time - (frame_end - current_time)
                if sleep_time > 0:
                    time.sleep(sleep_time)

        except KeyboardInterrupt:
            pass
        finally:
            self.cleanup()


def signal_handler(sig: int, frame: FrameType | None) -> None:
    """Handle Ctrl+C gracefully."""
    sys.exit(0)


def main() -> None:
    """Entry point for the LisbonAI animation."""
    # Setup signal handler
    signal.signal(signal.SIGINT, signal_handler)

    # Parse arguments (simple version)
    fps = 30
    style = "bold"
    render_style = "dots"
    rtmp_url = None

    if len(sys.argv) > 1:
        if "--fps" in sys.argv:
            idx = sys.argv.index("--fps")
            if idx + 1 < len(sys.argv):
                fps = int(sys.argv[idx + 1])

        if "--style" in sys.argv:
            idx = sys.argv.index("--style")
            if idx + 1 < len(sys.argv):
                style = sys.argv[idx + 1]

        if "--render-style" in sys.argv:
            idx = sys.argv.index("--render-style")
            if idx + 1 < len(sys.argv):
                render_style = sys.argv[idx + 1]

        if "--rtmp-url" in sys.argv:
            idx = sys.argv.index("--rtmp-url")
            if idx + 1 < len(sys.argv):
                rtmp_url = sys.argv[idx + 1]

    # Run animation
    animation = Animation(
        fps=fps,
        logo_style=style,
        render_style=render_style,
        rtmp_url=rtmp_url,
    )
    animation.run()


if __name__ == "__main__":
    main()
