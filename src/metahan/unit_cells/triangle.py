"""
Triangle unit cell implementation.
"""
from __future__ import annotations

import math

import gdstk

from metahan.unit_cells.base import UnitCell


class TriangleCell(UnitCell):
    """An equilateral triangle unit cell centered at the origin."""

    def __init__(self, side_um: float, layer: int = 1, datatype: int = 0):
        super().__init__(layer=layer, datatype=datatype)
        if side_um <= 0:
            raise ValueError("side_um must be > 0")
        self.side_um: float = float(side_um)

    def build_polygons(self) -> list[gdstk.Polygon]:
        height = math.sqrt(3.0) * self.side_um / 2.0
        points = [
            (0.0, 2.0 * height / 3.0),
            (-self.side_um / 2.0, -height / 3.0),
            (self.side_um / 2.0, -height / 3.0),
        ]
        return [gdstk.Polygon(points, layer=self.layer, datatype=self.datatype)]
