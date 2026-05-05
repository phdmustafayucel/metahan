# src/metahan/unit_cells/ring.py
"""
Ring unit cell implementation.

This module provides the RingCell class, which represents a ring (annulus) unit cell
for metasurface generation. The ring is centered at the origin and consists of a circle
with a circular hole in the center.
"""
from __future__ import annotations
import gdstk
from metahan.unit_cells.base import UnitCell


class RingCell(UnitCell):
    """
    A ring (annulus) unit cell for metasurface generation.

    This class creates a ring centered at (0, 0) with a specified outer radius and
    inner radius. The ring is approximated using ellipses with equal x and y radii.
    The tolerance parameter controls the approximation accuracy.

    Attributes:
        outer_radius_um (float): The outer radius of the ring in micrometers.
        inner_radius_um (float): The inner radius of the ring (hole) in micrometers.
        layer (int): The GDS layer number.
        datatype (int): The GDS datatype number.
        tolerance_um (float): The tolerance for polygon approximation in micrometers.
    """

    def __init__(
        self,
        outer_radius_um: float,
        inner_radius_um: float,
        layer: int = 1,
        datatype: int = 0,
        tolerance_um: float = 1e-9,
    ):
        """
        Initialize a ring unit cell.

        Args:
            outer_radius_um (float): The outer radius of the ring in micrometers. Must be > 0.
            inner_radius_um (float): The inner radius of the ring in micrometers. Must be > 0.
            layer (int): The GDS layer number. Defaults to 1.
            datatype (int): The GDS datatype number. Defaults to 0.
            tolerance_um (float): The tolerance for polygon approximation in micrometers.
                Defaults to 1e-3.

        Raises:
            ValueError: If outer_radius_um is not greater than 0.
            ValueError: If inner_radius_um is not greater than 0.
            ValueError: If inner_radius_um is not less than outer_radius_um.
            ValueError: If tolerance_um is not greater than 0.
        """
        super().__init__(layer=layer, datatype=datatype)
        if outer_radius_um <= 0:
            raise ValueError("outer_radius_um must be > 0")
        if inner_radius_um <= 0:
            raise ValueError("inner_radius_um must be > 0")
        if inner_radius_um >= outer_radius_um:
            raise ValueError("inner_radius_um must be < outer_radius_um")
        if tolerance_um <= 0:
            raise ValueError("tolerance_um must be > 0")
        self.outer_radius_um: float = float(outer_radius_um)
        self.inner_radius_um: float = float(inner_radius_um)
        self.tolerance_um: float = float(tolerance_um)

    def build_polygons(self) -> list[gdstk.Polygon]:
        """
        Build and return the ring polygon geometry.

        Creates a ring (annulus) centered at (0, 0) using gdstk's native ellipse 
        function with inner_radius parameter. This is optimized and avoids the 
        discontinuities from boolean operations.

        Returns:
            list[gdstk.Polygon]: A list containing the ring polygon representing the unit cell.
        """
        ring = gdstk.ellipse(
            center=(0, 0),
            radius=self.outer_radius_um,
            inner_radius=self.inner_radius_um,
            tolerance=self.tolerance_um,
            layer=self.layer,
            datatype=self.datatype,
        )
        
        return [ring]
