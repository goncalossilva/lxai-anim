import noise
import random


class CloudLayer:
    """A single parallax cloud layer using Perlin noise."""

    def __init__(
        self,
        width,
        height,
        speed=1.0,
        scale=0.1,
        octaves=3,
        persistence=0.5,
        lacunarity=2.0,
        seed=None,
    ):
        """
        Initialize a cloud layer.

        Args:
            width: Width of the rendering area
            height: Height of the rendering area
            speed: Horizontal movement speed (parallax factor)
            scale: Noise scale (smaller = more zoomed in)
            octaves: Number of noise octaves (more = more detail)
            persistence: Amplitude multiplier per octave
            lacunarity: Frequency multiplier per octave
            seed: Random seed for reproducible noise
        """
        self.width = width
        self.height = height
        self.speed = speed
        self.scale = scale
        self.octaves = octaves
        self.persistence = persistence
        self.lacunarity = lacunarity
        self.seed = seed if seed is not None else random.randint(0, 1000)
        self.offset_x = 0.0
        self.offset_y = 0.0

    def update(self, delta_time):
        """Update the cloud layer position."""
        self.offset_x += self.speed * delta_time

    def get_density(self, x, y):
        """
        Get cloud density at position (x, y).

        Returns:
            float: Density value from 0.0 to 1.0
        """
        # Calculate noise coordinates
        nx = (x + self.offset_x) * self.scale
        ny = (y + self.offset_y) * self.scale

        # Generate Perlin noise
        value = noise.pnoise2(
            nx,
            ny,
            octaves=self.octaves,
            persistence=self.persistence,
            lacunarity=self.lacunarity,
            repeatx=1024,
            repeaty=1024,
            base=self.seed,
        )

        # Normalize from [-1, 1] to [0, 1]
        density = (value + 1.0) / 2.0

        # Apply contrast curve to make clouds more distinct and show dithering better
        density = self._apply_contrast(density, power=2.5)

        return density

    def _apply_contrast(self, value, power=2.5):
        """Apply contrast curve to make clouds more distinct and enhance dithering."""
        # Use a power curve to increase contrast
        if value < 0.5:
            return 0.5 * pow(2 * value, power)
        else:
            return 1.0 - 0.5 * pow(2 * (1 - value), power)


class CloudSystem:
    """Manages multiple parallax cloud layers."""

    def __init__(self, width, height):
        """Initialize the cloud system with multiple layers."""
        self.width = width
        self.height = height
        self.layers = []

        # Create multiple cloud layers with different parameters
        # Background layer - slow, large features, subtle
        self.layers.append(
            CloudLayer(
                width,
                height,
                speed=0.3,
                scale=0.03,
                octaves=3,
                persistence=0.6,
                seed=42,
            )
        )

        # Mid-ground layer - medium speed, medium features
        self.layers.append(
            CloudLayer(
                width,
                height,
                speed=0.6,
                scale=0.06,
                octaves=4,
                persistence=0.55,
                seed=123,
            )
        )

        # Foreground layer - fast, smaller features with more detail
        self.layers.append(
            CloudLayer(
                width,
                height,
                speed=1.0,
                scale=0.1,
                octaves=5,
                persistence=0.5,
                seed=456,
            )
        )

    def update(self, delta_time):
        """Update all cloud layers."""
        for layer in self.layers:
            layer.update(delta_time)

    def get_combined_density(self, x, y):
        """
        Get combined density from all layers at position (x, y).

        Returns:
            float: Combined density value from 0.0 to 1.0
        """
        # Combine layers using weighted average
        total_density = 0.0
        weights = [0.25, 0.35, 0.4]  # Weight each layer (foreground gets more)

        for layer, weight in zip(self.layers, weights):
            density = layer.get_density(x, y)
            total_density += density * weight

        # Apply final gamma correction to enhance mid-tones and show dithering better
        total_density = pow(total_density, 0.8)

        # Clamp to [0, 1]
        return max(0.0, min(1.0, total_density))

    def render(self, renderer):
        """Render all cloud layers to the renderer."""
        for y in range(renderer.height):
            for x in range(renderer.width):
                density = self.get_combined_density(x, y)
                renderer.set_pixel(x, y, density)

    def resize(self, width, height):
        """
        Resize all cloud layers to match a new viewport.

        Args:
            width: New width in characters
            height: New height in characters
        """
        self.width = width
        self.height = height
        for layer in self.layers:
            layer.width = width
            layer.height = height
