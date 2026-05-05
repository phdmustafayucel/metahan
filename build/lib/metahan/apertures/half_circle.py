from __future__ import annotations

from metahan.apertures.base import Aperture


class HalfCircleAperture(Aperture):
    def __init__(self, radius: float, center=(0.0, 0.0), orientation: str = "up"):
        if radius <= 0:
            raise ValueError("radius must be > 0")
        self.radius = float(radius)
        self.cx, self.cy = float(center[0]), float(center[1])
        self.orientation = str(orientation).lower()
        if self.orientation not in {"up", "down", "left", "right"}:
            raise ValueError("orientation must be one of: up, down, left, right")

    def contains(self, x: float, y: float) -> bool:
        dx = x - self.cx
        dy = y - self.cy
        if dx * dx + dy * dy > self.radius * self.radius:
            return False
        if self.orientation == "up":
            return dy >= 0
        if self.orientation == "down":
            return dy <= 0
        if self.orientation == "left":
            return dx <= 0
        return dx >= 0
