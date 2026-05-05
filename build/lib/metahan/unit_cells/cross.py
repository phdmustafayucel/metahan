"""
Cross unit cell implementation.
"""
from __future__ import annotations

import gdstk

from metahan.unit_cells.base import UnitCell


class CrossCell(UnitCell):
    """A cross-shaped unit cell centered at the origin."""

    def __init__(
        self,
        arm_length_um: float,
        arm_width_um: float,
        layer: int = 1,
        datatype: int = 0,
    ):
        super().__init__(layer=layer, datatype=datatype)
        if arm_length_um <= 0:
            raise ValueError("arm_length_um must be > 0")
        if arm_width_um <= 0:
            raise ValueError("arm_width_um must be > 0")
        if arm_width_um > arm_length_um:
            raise ValueError("arm_width_um must be <= arm_length_um")
        self.arm_length_um: float = float(arm_length_um)
        self.arm_width_um: float = float(arm_width_um)

    def build_polygons(self) -> list[gdstk.Polygon]:
        half_len = self.arm_length_um / 2.0
        half_w = self.arm_width_um / 2.0
        horizontal = gdstk.rectangle(
            (-half_len, -half_w),
            (half_len, half_w),
            layer=self.layer,
            datatype=self.datatype,
        )
        vertical = gdstk.rectangle(
            (-half_w, -half_len),
            (half_w, half_len),
            layer=self.layer,
            datatype=self.datatype,
        )
        # Fuse both arms into a single cross region to avoid overlap artifacts.
        merged = gdstk.boolean(
            [horizontal],
            [vertical],
            "or",
            layer=self.layer,
            datatype=self.datatype,
        )
        return merged or []
