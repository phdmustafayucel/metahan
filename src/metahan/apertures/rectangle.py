# rectangle aperture class
from metahan.apertures.base import Aperture

class RectangleAperture(Aperture):

    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def contains(self, x: float, y: float) -> bool:
        half_width = self.width / 2
        half_height = self.height / 2
        return -half_width <= x <= half_width and -half_height <= y <= half_height