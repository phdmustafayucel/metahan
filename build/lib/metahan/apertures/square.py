from metahan.apertures.base import Aperture


class SquareAperture(Aperture):
    def __init__(self, side: float):
        if side <= 0:
            raise ValueError("side must be > 0")
        self.side = float(side)

    def contains(self, x: float, y: float) -> bool:
        half = self.side / 2.0
        return -half <= x <= half and -half <= y <= half
