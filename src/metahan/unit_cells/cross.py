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
        serif: bool = False,
        serif_size_um: float = 0.020,
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
        self.serif: bool = serif
        self.serif_size_um: float = float(serif_size_um)

    def _serif_rect(self, cx: float, cy: float) -> gdstk.Polygon:
        h = self.serif_size_um / 2.0
        return gdstk.rectangle(
            (cx - h, cy - h), (cx + h, cy + h),
            layer=self.layer, datatype=self.datatype,
        )

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
        merged = gdstk.boolean(
            [horizontal], [vertical], "or",
            layer=self.layer, datatype=self.datatype,
        )

        if not self.serif:
            return merged or []

        # 8 outer convex corners — arm tips
        outer_corners = [
            (-half_w,  half_len), ( half_w,  half_len),   # top arm
            (-half_w, -half_len), ( half_w, -half_len),   # bottom arm
            ( half_len,  half_w), ( half_len, -half_w),   # right arm
            (-half_len,  half_w), (-half_len, -half_w),   # left arm
        ]
        # 4 inner concave corners — arm junctions
        inner_corners = [
            ( half_w,  half_w), (-half_w,  half_w),
            ( half_w, -half_w), (-half_w, -half_w),
        ]

        outer_serifs = [self._serif_rect(cx, cy) for cx, cy in outer_corners]
        inner_serifs = [self._serif_rect(cx, cy) for cx, cy in inner_corners]

        # Add outer serifs (convex corner compensation)
        merged = gdstk.boolean(
            merged, outer_serifs, "or",
            layer=self.layer, datatype=self.datatype,
        )
        # Subtract inner serifs (concave corner compensation)
        merged = gdstk.boolean(
            merged, inner_serifs, "not",
            layer=self.layer, datatype=self.datatype,
        )

        return merged or []
