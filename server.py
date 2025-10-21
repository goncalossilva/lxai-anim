#!/usr/bin/env python3
import argparse
import asyncio
import os
import stat
import time
from pathlib import Path

import asyncssh

from clouds import CloudSystem
from renderer import TerminalRenderer
from typography import LXAITypography

HOST_KEY_FILENAME = "ssh_host_key"
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 2222


def ensure_host_key(path: Path) -> asyncssh.SSHKey:
    """
    Load an existing host key or generate a new one.

    Args:
        path: Destination path for the key file.

    Returns:
        asyncssh.SSHKey: Loaded or newly generated host key.
    """
    if path.exists():
        return asyncssh.read_private_key(path)

    key = asyncssh.generate_private_key("ssh-ed25519")
    path.write_bytes(key.export_private_key())
    try:
        os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)
    except PermissionError:
        # On non-POSIX systems chmod may fail; ignore quietly.
        pass
    return key


class SSHAnimationSession:
    """Run the LisbonAI animation inside an SSH channel."""

    def __init__(self, channel, width, height, fps, logo_style, render_style):
        self.channel = channel
        self.fps = fps
        self.frame_time = 1.0 / fps
        self.renderer = TerminalRenderer(
            width=width, height=height, style=render_style, output=channel
        )
        self.clouds = CloudSystem(self.renderer.width, self.renderer.height)
        self.typography = LXAITypography(style=logo_style)

        self.running = True
        self.auto_cycle_enabled = True
        self.auto_cycle_interval = 30.0
        self.last_style_change = 0.0

        self.start_time = None
        self.elapsed_time = 0.0
        self.key_queue = asyncio.Queue(maxsize=256)

    def queue_keys(self, data: str):
        """Enqueue incoming characters for later processing."""
        for char in data:
            if char:
                try:
                    self.key_queue.put_nowait(char)
                except asyncio.QueueFull:
                    # Drop excess input to keep animation responsive.
                    break

    def stop(self):
        """Request the animation loop to stop."""
        self.running = False

    async def run(self):
        """Run the animation loop until stopped or the channel closes."""
        self.start_time = time.monotonic()
        last_time = self.start_time

        self.channel.write("\033[?1049h\033[2J\033[H")
        await self._drain_channel()
        self.renderer.hide_cursor()
        await self._drain_channel()

        try:
            while self.running:
                now = time.monotonic()
                delta_time = now - last_time
                last_time = now

                await self._handle_input()
                self._update(delta_time)
                await self._render_frame()

                frame_end = time.monotonic()
                sleep_time = self.frame_time - (frame_end - now)
                if sleep_time > 0:
                    await asyncio.sleep(sleep_time)
        finally:
            await self._cleanup()

    async def _handle_input(self):
        """Process any pending keyboard input."""
        while True:
            try:
                key = self.key_queue.get_nowait()
            except asyncio.QueueEmpty:
                break

            if key == "n":
                self.auto_cycle_enabled = False
                self.renderer.next_style()
            elif key == "m":
                self.typography.next_style()
            elif key == "q":
                self.running = False
            elif key in ("\x03", "\x04"):  # Ctrl+C / Ctrl+D
                self.running = False

    def _update(self, delta_time: float):
        """Update animation state based on elapsed time."""
        self.elapsed_time = time.monotonic() - self.start_time
        self.clouds.update(delta_time)

        if self.auto_cycle_enabled:
            if self.elapsed_time - self.last_style_change >= self.auto_cycle_interval:
                self.renderer.next_style()
                self.last_style_change = self.elapsed_time

    async def _render_frame(self):
        """Render a single frame to the SSH channel."""
        self.renderer.clear_buffer()
        self.clouds.render(self.renderer)
        self.typography.render_bottom_right(
            self.renderer, margin_x=10, margin_y=2, opacity=1.0
        )

        frame_data = self.renderer.render_to_string()
        try:
            self.channel.write(frame_data)
            await self._drain_channel()
        except (asyncssh.Error, OSError):
            self.running = False

    async def _cleanup(self):
        """Restore terminal state and clear the screen."""
        try:
            self.renderer.show_cursor()
            self.channel.write("\033[?1049l")
            await self._drain_channel()
            self.channel.close()
        except (asyncssh.Error, OSError):
            pass

    async def _drain_channel(self):
        """Flush pending output if the writer supports draining."""
        drain = getattr(self.channel, "drain", None)
        if callable(drain):
            await drain()

    def resize(self, width: int, height: int):
        """Handle terminal resizes from the client."""
        self.renderer.resize(width, height)
        self.clouds.resize(width, height)


class LXAIAnimationSession(asyncssh.SSHServerSession):
    """AsyncSSH session wrapper for the animation."""

    def __init__(self, config):
        self.config = config
        self.channel = None
        self.animation = None
        self.animation_task = None
        self.pending_size = None

    def connection_made(self, chan):
        self.channel = chan

    def pty_requested(self, term_type, term_size, term_modes):
        width = height = 0
        if term_size:
            width, height, _, _ = term_size
        cols = width or 80
        rows = height or 24
        self.pending_size = (cols, rows)
        return True

    def shell_requested(self):
        return True

    def session_started(self):
        cols, rows = self._get_initial_size()
        self.animation = SSHAnimationSession(
            channel=self.channel,
            width=cols,
            height=rows,
            fps=self.config["fps"],
            logo_style=self.config["logo_style"],
            render_style=self.config["render_style"],
        )
        loop = asyncio.get_running_loop()
        self.animation_task = loop.create_task(self.animation.run())

    def data_received(self, data, datatype):
        if self.animation:
            self.animation.queue_keys(data)

    def terminal_size_changed(self, width, height, pixwidth, pixheight):
        if self.animation:
            self.animation.resize(width, height)

    def eof_received(self):
        if self.animation:
            self.animation.stop()
        return True

    def connection_lost(self, exc):
        if self.animation:
            self.animation.stop()
        if self.animation_task:
            self.animation_task.cancel()

    def _get_initial_size(self):
        """Fallback-aware terminal size detection."""
        if self.pending_size:
            return self.pending_size
        try:
            cols, rows = self.channel.get_terminal_size()
            return cols or 80, rows or 24
        except Exception:
            return 80, 24

    def signal_received(self, signal):
        if self.animation:
            self.animation.stop()
        return True


class LXAIAnimationServer(asyncssh.SSHServer):
    """SSH server which skips authentication and serves animation sessions."""

    def __init__(self, config):
        super().__init__()
        self.config = config

    def begin_auth(self, username):
        """Allow clients to connect without authentication."""
        return False

    def session_requested(self):
        return LXAIAnimationSession(self.config)


async def run_server(host, port, config):
    """Start the AsyncSSH server and serve forever."""
    host_key_path = Path(__file__).with_name(HOST_KEY_FILENAME)
    host_key = ensure_host_key(host_key_path)

    async with asyncssh.create_server(
        lambda: LXAIAnimationServer(config),
        host,
        port,
        server_host_keys=[host_key],
        line_editor=False,
        line_echo=False,
    ) as server:
        await server.wait_closed()


def parse_args():
    parser = argparse.ArgumentParser(
        description="Serve the LisbonAI animation over SSH."
    )
    parser.add_argument("--host", default=DEFAULT_HOST, help="Host/IP to bind to.")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="Port to bind.")
    parser.add_argument("--fps", type=int, default=10, help="Target frames per second.")
    parser.add_argument(
        "--style",
        default="bold",
        help="Typography style for the LisbonAI logo (see typography.py).",
    )
    parser.add_argument(
        "--render-style",
        default="dots",
        choices=["dots", "stipple", "fine", "blocks", "density"],
        help="Character set used for cloud rendering.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    config = {
        "fps": args.fps,
        "logo_style": args.style,
        "render_style": args.render_style,
    }

    try:
        asyncio.run(run_server(args.host, args.port, config))
    except (OSError, asyncssh.Error) as exc:
        raise SystemExit(f"Failed to start SSH server: {exc}") from exc
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
