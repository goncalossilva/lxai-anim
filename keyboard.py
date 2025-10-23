import sys
import termios
import tty
import select
from typing import Any


class KeyboardHandler:
    """Handles non-blocking keyboard input for interactive controls."""

    def __init__(self) -> None:
        """Initialize the keyboard handler."""
        self.old_settings: list[Any] | None = None

    def setup(self) -> None:
        """Setup terminal for non-blocking input."""
        if sys.stdin.isatty():
            self.old_settings = termios.tcgetattr(sys.stdin)
            tty.setcbreak(sys.stdin.fileno())

    def cleanup(self) -> None:
        """Restore terminal settings."""
        if self.old_settings is not None:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)

    def get_key(self) -> str | None:
        """
        Get a key press without blocking.

        Returns:
            str: The pressed key, or None if no key was pressed
        """
        if select.select([sys.stdin], [], [], 0)[0]:
            return sys.stdin.read(1)
        return None
