import os
import sys


class TerminalRenderer:
    """Handles terminal rendering with double buffering."""

    # ASCII density characters for dithering (light to dark)
    DENSITY_CHARS = " ·:-=+*#%@"

    # Block characters for smoother gradients
    BLOCK_CHARS = " ░▒▓█"

    # Dot-based stipple characters (light to dark)
    DOT_CHARS = " .·⋅∙•∘○●◉⬤"

    # Alternative stipple patterns
    STIPPLE_CHARS = " .·:∴∵⁘⁙∷≈≋"

    # Fine dot gradient
    FINE_DOTS = " .·˙∙⋅∘○◌●◉⦿"

    def __init__(self, width=None, height=None, style="dots", output=None):
        """
        Initialize the renderer.

        Args:
            width: Terminal width (auto-detected if None)
            height: Terminal height (auto-detected if None)
            style: Character set style - 'dots', 'stipple', 'fine', 'blocks', or 'density'
            output: Output stream (default: sys.stdout)
        """
        term_width, term_height = self._get_terminal_size()
        self.width = width if width and width > 0 else term_width
        self.height = height if height and height > 0 else term_height

        self.output = output or sys.stdout

        # Select character set based on style
        self.styles = {
            "dots": self.DOT_CHARS,
            "stipple": self.STIPPLE_CHARS,
            "fine": self.FINE_DOTS,
            "blocks": self.BLOCK_CHARS,
            "density": self.DENSITY_CHARS,
        }
        self.style_names = list(self.styles.keys())
        self.current_style = style if style in self.styles else "dots"
        self.chars = self.styles[self.current_style]
        self.buffer = [[" " for _ in range(self.width)] for _ in range(self.height)]

    def _get_terminal_size(self):
        """Get terminal dimensions."""
        try:
            size = os.get_terminal_size()
            return size.columns, size.lines - 1  # Reserve one line
        except OSError:
            return 80, 24

    def clear_buffer(self):
        """Clear the rendering buffer."""
        self.buffer = [[" " for _ in range(self.width)] for _ in range(self.height)]

    def set_pixel(self, x, y, density):
        """Set a pixel with a density value (0.0 to 1.0)."""
        if 0 <= x < self.width and 0 <= y < self.height:
            index = int(density * (len(self.chars) - 1))
            index = max(0, min(index, len(self.chars) - 1))
            self.buffer[y][x] = self.chars[index]

    def draw_text(self, x, y, text, char="█"):
        """Draw text at position."""
        for i, ch in enumerate(text):
            if 0 <= x + i < self.width and 0 <= y < self.height:
                if ch != " ":
                    self.buffer[y][x + i] = char

    def blend_pixel(self, x, y, density):
        """Blend a new density value with existing pixel."""
        if 0 <= x < self.width and 0 <= y < self.height:
            current_char = self.buffer[y][x]
            current_density = (
                self.chars.index(current_char) / (len(self.chars) - 1)
                if current_char in self.chars
                else 0
            )
            new_density = max(current_density, density)
            self.set_pixel(x, y, new_density)

    def render(self, output=None):
        """Render the buffer to the terminal or provided stream."""
        data = "\r\n".join("".join(row) for row in self.buffer)
        data = f"\033[2J\033[H{data}\r"
        target = output or self.output
        target.write(data)
        if hasattr(target, "flush"):
            target.flush()

    def hide_cursor(self):
        """Hide the terminal cursor."""
        self.output.write("\033[?25l")
        if hasattr(self.output, "flush"):
            self.output.flush()

    def show_cursor(self):
        """Show the terminal cursor."""
        self.output.write("\033[?25h")
        if hasattr(self.output, "flush"):
            self.output.flush()

    def set_style(self, style):
        """
        Change the rendering style.

        Args:
            style: New style name ('dots', 'stipple', 'fine', 'blocks', 'density')
        """
        if style in self.styles:
            self.current_style = style
            self.chars = self.styles[style]

    def next_style(self):
        """Cycle to the next rendering style."""
        current_index = self.style_names.index(self.current_style)
        next_index = (current_index + 1) % len(self.style_names)
        self.set_style(self.style_names[next_index])
        return self.current_style

    def resize(self, width, height):
        """
        Resize the renderer to new dimensions.

        Args:
            width: New width in characters
            height: New height in characters
        """
        self.width = width
        self.height = height
        self.clear_buffer()
