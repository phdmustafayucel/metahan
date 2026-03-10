"""
Ellipse unit cell implementation.
"""
from __future__ import annotations

import gdstk

from metahan.unit_cells.base import UnitCell


class EllipseCell(UnitCell):
    """An ellipse unit cell centered at the origin."""

    def __init__(
        self,
        radius_x_um: float,
        radius_y_um: float,
        layer: int = 1,
        datatype: int = 0,
        tolerance_um: float = 1e-3,
    ):
        super().__init__(layer=layer, datatype=datatype)
        if radius_x_um <= 0:
            raise ValueError("radius_x_um must be > 0")
        if radius_y_um <= 0:
            raise ValueError("radius_y_um must be > 0")
        if tolerance_um <= 0:
            raise ValueError("tolerance_um must be > 0")
        self.radius_x_um: float = float(radius_x_um)
        self.radius_y_um: float = float(radius_y_um)
        self.tolerance_um: float = float(tolerance_um)

    def build_polygons(self) -> list[gdstk.Polygon]:
        return [gdstk.ellipse(
            center=(0, 0),
            radius=(self.radius_x_um, self.radius_y_um),
            tolerance=self.tolerance_um,
            layer=self.layer,
            datatype=self.datatype,
        )]
