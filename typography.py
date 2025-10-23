from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from renderer import TerminalRenderer


class LXAITypography:
    """Handles LisbonAI logo rendering with multiple styles."""

    # Large block-style LisbonAI logo
    LOGO_LARGE: list[str] = [
        "██╗     ██╗███████╗██████╗  ██████╗ ███╗   ██╗ █████╗ ██╗",
        "██║     ██║██╔════╝██╔══██╗██╔═══██╗████╗  ██║██╔══██╗██║",
        "██║     ██║███████╗██████╔╝██║   ██║██╔██╗ ██║███████║██║",
        "██║     ██║╚════██║██╔══██╗██║   ██║██║╚██╗██║██╔══██║██║",
        "███████╗██║███████║██████╔╝╚██████╔╝██║ ╚████║██║  ██║██║",
        "╚══════╝╚═╝╚══════╝╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝",
    ]

    # Medium block-style
    LOGO_MEDIUM: list[str] = [
        "██╗     ██╗███████╗██████╗  ██████╗ ███╗   ██╗ █████╗ ██╗",
        "██║     ██║██╔════╝██╔══██╗██╔═══██╗████╗  ██║██╔══██╗██║",
        "██║     ██║███████╗██████╔╝██║   ██║██╔██╗ ██║███████║██║",
        "███████╗██║███████║██████╔╝╚██████╔╝██║ ╚████║██║  ██║██║",
        "╚══════╝╚═╝╚══════╝╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝",
    ]

    # Sleek minimal style
    LOGO_MINIMAL: list[str] = [
        "╦  ╦╔═╗╔╗ ╔═╗╔╗╔  ╔═╗╦",
        "║  ║╚═╗╠╩╗║ ║║║║  ╠═╣║",
        "╩═╝╩╚═╝╚═╝╚═╝╝╚╝  ╩ ╩╩",
    ]

    # ASCII art style
    LOGO_ASCII: list[str] = [
        " _     ___ ____  ____   ___  _   _    _    ___ ",
        "| |   |_ _/ ___|| __ ) / _ \\| \\ | |  / \\  |_ _|",
        "| |    | |\\___ \\|  _ \\| | | |  \\| | / _ \\  | | ",
        "| |___ | | ___) | |_) | |_| | |\\  |/ ___ \\ | | ",
        "|_____|___|____/|____/ \\___/|_| \\_/_/   \\_\\___|",
    ]

    # Slant style
    LOGO_SLANT: list[str] = [
        "   ____        __             ___   ____",
        "  / / /____   / /_  ___  ___ / _ | /  _/",
        " / / /(_-<  / _ \\/ _ \\/ _ / __ |_/ /  ",
        "/_/_//___/ /_.__/\\___/_//_/_/ |_/___/  ",
    ]

    # Simple compact style
    LOGO_SIMPLE: list[str] = [
        "LisbonAI",
    ]

    # Stipple/dot styles - using heavier dot characters for visibility
    LOGO_DOTS: list[str] = [
        "●●   ●● ●●●●● ●●●●   ●●●●  ●●●  ●●  ●  ●●●  ●●",
        "●●   ●● ●●    ●●  ●● ●●  ●● ●● ●● ●● ●● ●● ●● ●●",
        "●●   ●● ●●●●● ●●●●   ●●  ●● ●● ●● ●●●●● ●●●●● ●●",
        "●●   ●●    ●● ●●  ●● ●●  ●● ●● ●● ●● ●● ●● ●● ●●",
        "●●●●●●● ●●●●● ●●●●    ●●●●   ●●●  ●● ●  ●● ●● ●●",
    ]

    LOGO_CIRCLES: list[str] = [
        "○○   ○○ ○○○○○ ○○○○   ○○○○  ○○○  ○○  ○  ○○○  ○○",
        "○○   ○○ ○○    ○○  ○○ ○○  ○○ ○○ ○○ ○○ ○○ ○○ ○○ ○○",
        "○○   ○○ ○○○○○ ○○○○   ○○  ○○ ○○ ○○ ○○○○○ ○○○○○ ○○",
        "○○   ○○    ○○ ○○  ○○ ○○  ○○ ○○ ○○ ○○ ○○ ○○ ○○ ○○",
        "○○○○○○○ ○○○○○ ○○○○    ○○○○   ○○○  ○○ ○  ○○ ○○ ○○",
    ]

    LOGO_MIXED_DOTS: list[str] = [
        "●●   ●● ●●●●● ●●●●   ●●●●  ●●●  ●●  ●  ●●●  ●●",
        "●●   ●● ●●    ●●  ●● ●●  ●● ●● ●● ●● ●● ●● ●● ●●",
        "●●   ●● ●●●●● ●●●●   ●●  ●● ○○ ○○ ○○○○○ ○○○○○ ●●",
        "●●   ●●    ●● ●●  ●● ●●  ●● ●● ●● ●● ●● ●● ●● ●●",
        "●●●●●●● ●●●●● ●●●●    ●●●●   ●●●  ●● ●  ●● ●● ●●",
    ]

    LOGO_STIPPLE: list[str] = [
        "∙∙   ∙∙ ∙∙∙∙∙ ∙∙∙∙   ∙∙∙∙  ∙∙∙  ∙∙  ∙  ∙∙∙  ∙∙",
        "∙∙   ∙∙ ∙∙    ∙∙  ∙∙ ∙∙  ∙∙ ∙∙ ∙∙ ∙∙ ∙∙ ∙∙ ∙∙ ∙∙",
        "∙∙   ∙∙ ∙∙∙∙∙ ∙∙∙∙   ∙∙  ∙∙ ∙∙ ∙∙ ∙∙∙∙∙ ∙∙∙∙∙ ∙∙",
        "∙∙   ∙∙    ∙∙ ∙∙  ∙∙ ∙∙  ∙∙ ∙∙ ∙∙ ∙∙ ∙∙ ∙∙ ∙∙ ∙∙",
        "∙∙∙∙∙∙∙ ∙∙∙∙∙ ∙∙∙∙    ∙∙∙∙   ∙∙∙  ∙∙ ∙  ∙∙ ∙∙ ∙∙",
    ]

    # Extra large bold block style - highly visible
    LOGO_HUGE: list[str] = [
        "██╗     ██╗███████╗██████╗  ██████╗ ███╗   ██╗ █████╗ ██╗",
        "██║     ██║██╔════╝██╔══██╗██╔═══██╗████╗  ██║██╔══██╗██║",
        "██║     ██║███████╗██████╔╝██║   ██║██╔██╗ ██║███████║██║",
        "██║     ██║╚════██║██╔══██╗██║   ██║██║╚██╗██║██╔══██║██║",
        "███████╗██║███████║██████╔╝╚██████╔╝██║ ╚████║██║  ██║██║",
        "╚══════╝╚═╝╚══════╝╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝",
        "",
    ]

    # Double-height block characters for maximum visibility
    LOGO_DOUBLE: list[str] = [
        "██╗     ██╗███████╗██████╗  ██████╗ ███╗   ██╗ █████╗ ██╗",
        "██║     ██║██╔════╝██╔══██╗██╔═══██╗████╗  ██║██╔══██╗██║",
        "██║     ██║███████╗██████╔╝██║   ██║██╔██╗ ██║███████║██║",
        "██║     ██║███████║██████╔╝██║   ██║██╔██╗ ██║███████║██║",
        "██║     ██║╚════██║██╔══██╗██║   ██║██║╚██╗██║██╔══██║██║",
        "███████╗██║███████║██████╔╝╚██████╔╝██║ ╚████║██║  ██║██║",
        "███████╗██║███████║██████╔╝╚██████╔╝██║ ╚████║██║  ██║██║",
        "╚══════╝╚═╝╚══════╝╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝",
    ]

    # Bold dots - extra thick for visibility
    LOGO_BOLD_DOTS: list[str] = [
        "⬤⬤⬤   ⬤⬤⬤ ⬤⬤⬤⬤⬤⬤⬤ ⬤⬤⬤⬤⬤   ⬤⬤⬤⬤⬤⬤  ⬤⬤⬤⬤  ⬤⬤⬤  ⬤⬤   ⬤⬤⬤⬤  ⬤⬤⬤",
        "⬤⬤⬤   ⬤⬤⬤ ⬤⬤⬤      ⬤⬤⬤  ⬤⬤⬤ ⬤⬤⬤  ⬤⬤⬤ ⬤⬤⬤ ⬤⬤⬤ ⬤⬤⬤ ⬤⬤⬤ ⬤⬤⬤ ⬤⬤⬤ ⬤⬤⬤",
        "⬤⬤⬤   ⬤⬤⬤ ⬤⬤⬤⬤⬤⬤⬤ ⬤⬤⬤⬤⬤⬤   ⬤⬤⬤  ⬤⬤⬤ ⬤⬤⬤ ⬤⬤⬤ ⬤⬤⬤⬤⬤⬤⬤ ⬤⬤⬤⬤⬤⬤⬤ ⬤⬤⬤",
        "⬤⬤⬤   ⬤⬤⬤      ⬤⬤⬤ ⬤⬤⬤  ⬤⬤⬤ ⬤⬤⬤  ⬤⬤⬤ ⬤⬤⬤ ⬤⬤⬤ ⬤⬤⬤ ⬤⬤⬤ ⬤⬤⬤ ⬤⬤⬤ ⬤⬤⬤",
        "⬤⬤⬤⬤⬤⬤⬤ ⬤⬤⬤⬤⬤⬤⬤ ⬤⬤⬤⬤⬤⬤    ⬤⬤⬤⬤⬤⬤  ⬤⬤⬤⬤  ⬤⬤⬤ ⬤⬤   ⬤⬤⬤ ⬤⬤⬤ ⬤⬤⬤",
    ]

    # Clean bold ASCII - very readable
    LOGO_BOLD_ASCII: list[str] = [
        "██      ██ ███████ ██████   ██████  ███  ██  ████  ██",
        "██      ██ ██      ██   ██ ██    ██ ████ ██ ██  ██ ██",
        "██      ██ ███████ ██████  ██    ██ ██ ████ ██████ ██",
        "██      ██      ██ ██   ██ ██    ██ ██  ███ ██  ██ ██",
        "███████ ██ ███████ ██████   ██████  ██   ██ ██  ██ ██",
    ]

    def __init__(self, style: str = "bold") -> None:
        """
        Initialize typography with a specific style.

        Args:
            style: Logo style - 'bold', 'huge', 'double', 'bold_dots', 'bold_ascii',
                   'large', 'medium', 'minimal', 'ascii', 'slant', 'simple',
                   'dots', 'circles', 'mixed', 'stipple'
        """
        self.styles: dict[str, list[str]] = {
            "bold": self.LOGO_BOLD_ASCII,
            "bold_dots": self.LOGO_BOLD_DOTS,
            "huge": self.LOGO_HUGE,
            "double": self.LOGO_DOUBLE,
            "large": self.LOGO_LARGE,
            "medium": self.LOGO_MEDIUM,
            "minimal": self.LOGO_MINIMAL,
            "dots": self.LOGO_DOTS,
            "circles": self.LOGO_CIRCLES,
            "stipple": self.LOGO_STIPPLE,
            "ascii": self.LOGO_ASCII,
            "slant": self.LOGO_SLANT,
            "simple": self.LOGO_SIMPLE,
            "mixed": self.LOGO_MIXED_DOTS,
        }
        self.style_names: list[str] = list(self.styles.keys())
        self.current_style: str = style if style in self.styles else "bold"
        self.logo: list[str] = self.styles[self.current_style]
        self.width: int = max(len(line) for line in self.logo)
        self.height: int = len(self.logo)

    def render_centered(
        self, renderer: TerminalRenderer, y_offset: int = 0, opacity: float = 1.0
    ) -> None:
        """
        Render the logo centered in the renderer.

        Args:
            renderer: TerminalRenderer instance
            y_offset: Vertical offset from center
            opacity: Opacity from 0.0 to 1.0
        """
        # Calculate center position
        x_start = (renderer.width - self.width) // 2
        y_start = (renderer.height - self.height) // 2 + y_offset

        # Render each line
        for i, line in enumerate(self.logo):
            y = y_start + i
            if 0 <= y < renderer.height:
                for j, char in enumerate(line):
                    x = x_start + j
                    if 0 <= x < renderer.width:
                        if char != " ":
                            # Apply opacity by blending with background
                            if opacity >= 1.0:
                                renderer.buffer[y][x] = char
                            else:
                                # For partial opacity, use lighter characters
                                if opacity > 0.7:
                                    renderer.buffer[y][x] = char
                                elif opacity > 0.4:
                                    renderer.buffer[y][x] = "░"
                                elif opacity > 0.2:
                                    renderer.buffer[y][x] = "·"

    def render_at(
        self, renderer: TerminalRenderer, x: int, y: int, opacity: float = 1.0
    ) -> None:
        """
        Render the logo at specific coordinates.

        Args:
            renderer: TerminalRenderer instance
            x: X coordinate (left edge)
            y: Y coordinate (top edge)
            opacity: Opacity from 0.0 to 1.0
        """
        for i, line in enumerate(self.logo):
            row = y + i
            if 0 <= row < renderer.height:
                for j, char in enumerate(line):
                    col = x + j
                    if 0 <= col < renderer.width:
                        if char != " ":
                            if opacity >= 1.0:
                                renderer.buffer[row][col] = char
                            else:
                                if opacity > 0.7:
                                    renderer.buffer[row][col] = char
                                elif opacity > 0.4:
                                    renderer.buffer[row][col] = "░"
                                elif opacity > 0.2:
                                    renderer.buffer[row][col] = "·"

    def render_bottom_right(
        self,
        renderer: TerminalRenderer,
        margin_x: int = 10,
        margin_y: int = 10,
        opacity: float = 1.0,
        with_background: bool = False,
    ) -> None:
        """
        Render the logo at bottom-right corner.

        Args:
            renderer: TerminalRenderer instance
            margin_x: Distance from right edge
            margin_y: Distance from bottom edge
            opacity: Opacity from 0.0 to 1.0
            with_background: If True, render a background behind the text
        """
        x = renderer.width - self.width - margin_x
        y = renderer.height - self.height - margin_y

        # Optionally render background
        if with_background:
            self._render_background(renderer, x, y)

        self.render_at(renderer, x, y, opacity)

    def _render_background(
        self, renderer: TerminalRenderer, x: int, y: int, padding: int = 1
    ) -> None:
        """
        Render a background box behind the logo.

        Args:
            renderer: TerminalRenderer instance
            x: X coordinate of logo
            y: Y coordinate of logo
            padding: Padding around the text
        """
        # Draw background using a darker character
        bg_char = "▓"

        for row in range(y - padding, y + self.height + padding):
            for col in range(x - padding, x + self.width + padding):
                if 0 <= row < renderer.height and 0 <= col < renderer.width:
                    renderer.buffer[row][col] = bg_char

    def set_style(self, style: str) -> None:
        """
        Change the logo style.

        Args:
            style: New style name
        """
        if style in self.styles:
            self.current_style = style
            self.logo = self.styles[style]
            self.width = max(len(line) for line in self.logo)
            self.height = len(self.logo)

    def next_style(self) -> str:
        """Cycle to the next logo style."""
        current_index = self.style_names.index(self.current_style)
        next_index = (current_index + 1) % len(self.style_names)
        self.set_style(self.style_names[next_index])
        return self.current_style
