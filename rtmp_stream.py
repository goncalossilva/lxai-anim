"""RTMP stream capture and ASCII conversion using ffmpeg."""

from __future__ import annotations

import shutil
import subprocess
import sys
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from renderer import TerminalRenderer


class RTMPStream:
    """Captures RTMP stream via ffmpeg and converts to ASCII."""

    def __init__(self, rtmp_url: str, target_fps: int = 10) -> None:
        """Initialize RTMP stream capture.

        Args:
            rtmp_url: The RTMP stream URL to capture
            target_fps: Target frames per second for capture (default: 10)
        """
        self.rtmp_url = rtmp_url
        self.target_fps = target_fps
        self.process: subprocess.Popen[bytes] | None = None
        self.current_frame: bytes | None = None
        self.frame_width = 0
        self.frame_height = 0
        self.is_running = False
        self.last_frame_time = 0.0
        self.consecutive_failures = 0

    @staticmethod
    def is_ffmpeg_available() -> bool:
        """Check if ffmpeg is installed and available.

        Returns:
            True if ffmpeg is found in PATH, False otherwise
        """
        return shutil.which("ffmpeg") is not None

    @staticmethod
    def probe_stream(rtmp_url: str, timeout: float = 3.0) -> bool:
        """Probe if an RTMP stream is available without fully connecting.

        Args:
            rtmp_url: The RTMP stream URL to probe
            timeout: Maximum time to wait for probe in seconds

        Returns:
            True if stream is available, False otherwise
        """
        if not RTMPStream.is_ffmpeg_available():
            return False

        try:
            # Use ffprobe (part of ffmpeg) to quickly check stream availability
            result = subprocess.run(  # noqa: S603
                [  # noqa: S607
                    "ffprobe",
                    "-v",
                    "quiet",
                    "-rtsp_transport",
                    "tcp",
                    "-timeout",
                    str(int(timeout * 1_000_000)),  # ffprobe expects microseconds
                    "-i",
                    rtmp_url,
                ],
                capture_output=True,
                timeout=timeout + 1,  # Add buffer to subprocess timeout
                check=False,
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            return False

    def start(self, width: int, height: int) -> bool:
        """Start capturing the RTMP stream.

        Args:
            width: Target width for frames
            height: Target height for frames

        Returns:
            True if stream started successfully, False otherwise
        """
        if not self.is_ffmpeg_available():
            print("Error: ffmpeg is not installed", file=sys.stderr)
            return False

        if self.is_running:
            return True

        self.frame_width = width
        self.frame_height = height

        try:
            # Start ffmpeg process to capture stream
            # -i: input URL
            # -f rawvideo: output raw video frames
            # -pix_fmt gray: grayscale pixel format (1 byte per pixel)
            # -s: output size
            # -r: frame rate
            # pipe:1: output to stdout
            self.process = subprocess.Popen(  # noqa: S603
                [  # noqa: S607
                    "ffmpeg",
                    "-loglevel",
                    "error",  # Only show errors
                    "-i",
                    self.rtmp_url,
                    "-f",
                    "rawvideo",
                    "-pix_fmt",
                    "gray",
                    "-s",
                    f"{width}x{height}",
                    "-r",
                    str(self.target_fps),
                    "pipe:1",
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                bufsize=width * height * 2,  # Buffer 2 frames
            )
            self.is_running = True
            self.consecutive_failures = 0
            return True
        except (FileNotFoundError, OSError) as e:
            print(f"Error starting ffmpeg: {e}", file=sys.stderr)
            return False

    def stop(self) -> None:
        """Stop capturing the RTMP stream."""
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.process.kill()
            finally:
                self.process = None
        self.is_running = False
        self.current_frame = None

    def update(self, time_delta: float) -> None:
        """Update by reading the next frame from ffmpeg if available.

        Args:
            time_delta: Time elapsed since last frame in seconds
        """
        if not self.is_running or not self.process or not self.process.stdout:
            return

        # Calculate if we should try to read a new frame
        current_time = time.time()
        if current_time - self.last_frame_time < (1.0 / self.target_fps):
            return

        # Calculate expected frame size (1 byte per pixel for grayscale)
        frame_size = self.frame_width * self.frame_height

        try:
            # Try to read a frame (non-blocking via buffer check)
            frame_data = self.process.stdout.read(frame_size)

            if len(frame_data) == frame_size:
                self.current_frame = frame_data
                self.last_frame_time = current_time
                self.consecutive_failures = 0
            elif len(frame_data) == 0:
                # Stream ended or disconnected
                self.consecutive_failures += 1
                if self.consecutive_failures > 3:
                    self.stop()
            else:
                # Partial frame, likely a problem
                self.consecutive_failures += 1

        except (OSError, ValueError):
            self.consecutive_failures += 1
            if self.consecutive_failures > 3:
                self.stop()

    def render(self, renderer: TerminalRenderer) -> None:
        """Render the current frame to the terminal renderer.

        Args:
            renderer: The terminal renderer to draw to
        """
        if not self.current_frame or not self.is_running:
            return

        # Convert grayscale bytes to density values and render
        for y in range(min(self.frame_height, renderer.height)):
            for x in range(min(self.frame_width, renderer.width)):
                pixel_index = y * self.frame_width + x
                if pixel_index < len(self.current_frame):
                    # Convert byte value (0-255) to density (0.0-1.0)
                    density = self.current_frame[pixel_index] / 255.0
                    renderer.set_pixel(x, y, density)

    def is_available(self) -> bool:
        """Check if the stream is currently available and running.

        Returns:
            True if stream is active, False otherwise
        """
        if not self.is_running or not self.process:
            return False

        # Check if process is still alive
        return self.process.poll() is None

    def cleanup(self) -> None:
        """Clean up resources."""
        self.stop()
