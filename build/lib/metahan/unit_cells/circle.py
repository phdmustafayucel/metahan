# src/metahan/unit_cells/circle.py
"""
Circle unit cell implementation.

This module provides the CircleCell class, which represents a circular unit cell
for metasurface generation. The circle is centered at the origin and can be used
as a building block in lattice structures.
"""
from __future__ import annotations
import gdstk
from metahan.unit_cells.base import UnitCell


class CircleCell(UnitCell):
    """
    A circular unit cell for metasurface generation.

    This class creates a circular polygon centered at (0, 0) with a specified radius.
    The circle is approximated using an ellipse with equal x and y radii. The
    tolerance parameter controls the approximation accuracy.

    Attributes:
        radius_um (float): The radius of the circle in micrometers.
        layer (int): The GDS layer number.
        datatype (int): The GDS datatype number.
        tolerance_um (float): The tolerance for polygon approximation in micrometers.
    """

    def __init__(
        self,
        radius_um: float,
        layer: int = 1,
        datatype: int = 0,
        tolerance_um: float = 1e-3,
    ):
        """
        Initialize a circular unit cell.

        Args:
            radius_um (float): The radius of the circle in micrometers. Must be > 0.
            layer (int): The GDS layer number. Defaults to 1.
            datatype (int): The GDS datatype number. Defaults to 0.
            tolerance_um (float): The tolerance for polygon approximation in micrometers.
                Defaults to 1e-3.

        Raises:
            ValueError: If radius_um is not greater than 0.
        """
        super().__init__(layer=layer, datatype=datatype)
        if radius_um <= 0:
            raise ValueError("radius_um must be > 0")
        if tolerance_um <= 0:
            raise ValueError("tolerance_um must be > 0")
        self.radius_um: float = float(radius_um)
        self.tolerance_um: float = float(tolerance_um)

    def build_polygons(self) -> list[gdstk.Polygon]:
        """
        Build and return the circular polygon geometry.

        Creates a circle centered at (0, 0) using gdstk's ellipse function with
        equal x and y radii. The polygon is placed on the specified layer and datatype.

        Returns:
            list[gdstk.Polygon]: A list containing the circular polygon representing the unit cell.
        """
        return [gdstk.ellipse(
            center=(0, 0),
            radius=self.radius_um,
            tolerance=self.tolerance_um,
            layer=self.layer,
            datatype=self.datatype,
        )]