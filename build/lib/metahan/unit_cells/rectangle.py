"""
Rectangle unit cell implementation.
"""
from __future__ import annotations

import gdstk

from metahan.unit_cells.base import UnitCell


class RectangleCell(UnitCell):
    """A rectangle unit cell centered at the origin."""

    def __init__(
        self,
        width_um: float,
        height_um: float,
        layer: int = 1,
        datatype: int = 0,
    ):
        super().__init__(layer=layer, datatype=datatype)
        if width_um <= 0:
            raise ValueError("width_um must be > 0")
        if height_um <= 0:
            raise ValueError("height_um must be > 0")
        self.width_um: float = float(width_um)
        self.height_um: float = float(height_um)

    def build_polygons(self) -> list[gdstk.Polygon]:
        half_w = self.width_um / 2.0
        half_h = self.height_um / 2.0
        return [gdstk.rectangle(
            (-half_w, -half_h),
            (half_w, half_h),
            layer=self.layer,
            datatype=self.datatype,
        )]
