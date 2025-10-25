"""Stream source protocol for animation sources."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from renderer import TerminalRenderer


class StreamSource(Protocol):
    """Protocol for animation sources (clouds, RTMP streams, etc)."""

    def update(self, time_delta: float) -> None:
        """Update the animation state.

        Args:
            time_delta: Time elapsed since last frame in seconds
        """
        ...

    def render(self, renderer: TerminalRenderer) -> None:
        """Render the current frame to the terminal renderer.

        Args:
            renderer: The terminal renderer to draw to
        """
        ...

    def is_available(self) -> bool:
        """Check if this stream source is currently available.

        Returns:
            True if the source is ready to render, False otherwise
        """
        ...

    def cleanup(self) -> None:
        """Clean up resources when the source is no longer needed."""
        ...
