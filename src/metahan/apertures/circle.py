from metahan.apertures.base import Aperture


class CircleAperture(Aperture):

    def __init__(self, radius: float, center=(0.0, 0.0)):
        self.radius = radius
        self.cx, self.cy = center


    def contains(self, x: float, y: float) -> bool:

        dx = x - self.cx
        dy = y - self.cy

        return dx*dx + dy*dy <= self.radius*self.radius