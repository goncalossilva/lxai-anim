import sys
import os


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

    def __init__(self, width=None, height=None, style="dots"):
        """
        Initialize the renderer.

        Args:
            width: Terminal width (auto-detected if None)
            height: Terminal height (auto-detected if None)
            style: Character set style - 'dots', 'stipple', 'fine', 'blocks', or 'density'
        """
        self.width, self.height = self._get_terminal_size()
        if width:
            self.width = min(width, self.width)
        if height:
            self.height = min(height, self.height)

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

    def render(self):
        """Render the buffer to the terminal."""
        # Move cursor to top-left and clear screen
        sys.stdout.write("\033[H\033[2J")

        # Render each line
        for row in self.buffer:
            sys.stdout.write("".join(row) + "\n")

        sys.stdout.flush()

    def hide_cursor(self):
        """Hide the terminal cursor."""
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()

    def show_cursor(self):
        """Show the terminal cursor."""
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()

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
