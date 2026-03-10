# src/metahan/unit_cells/supercell.py
"""
SuperCell implementation for composite unit cells.

This module provides the SuperCell class, which combines multiple unit cells
at different positions to create a composite structure. SuperCells allow for
the creation of more complex metasurface patterns by grouping and positioning
multiple unit cells together.
"""
from __future__ import annotations
import gdstk

from metahan.unit_cells.base import UnitCell


class SuperCell(UnitCell):
    """
    A composite unit cell made of multiple positioned unit cells.

    SuperCell represents a collection of unit cells that are positioned at
    specific locations. This allows for creating complex patterns by combining
    simpler unit cell types. All contained cells are translated relative to
    the origin (0, 0).

    Attributes:
        cells (list[tuple[UnitCell, tuple[float, float]]]): A list of tuples,
            each containing a UnitCell instance and its (x, y) position offset
            in micrometers.
        layer (int): The GDS layer number for the supercell.
        datatype (int): The GDS datatype number for the supercell.
    """

    def __init__(self,
                 cells: list[tuple[UnitCell, tuple[float, float]]],
                 layer: int = 1,
                 datatype: int = 0):
        """
        Initialize a supercell with multiple positioned unit cells.

        Args:
            cells (list[tuple[UnitCell, tuple[float, float]]]): List of tuples,
                where each tuple contains:
                - A UnitCell instance
                - A (x, y) tuple with the position offset in micrometers
            layer (int): The GDS layer number. Defaults to 1.
            datatype (int): The GDS datatype number. Defaults to 0.
        """
        super().__init__(layer=layer, datatype=datatype)
        self.cells = cells

    def build_polygons(self) -> list[gdstk.Polygon]:
        """
        Build and return the polygons for all unit cells in the supercell.

        Each unit cell is built and then translated to its specified position.
        All polygons maintain their original layer and datatype information.

        Returns:
            list[gdstk.Polygon]: A list of polygons, one for each unit cell in
                the supercell, positioned at their respective offsets.
        """
        polygons = []
        for cell, (x, y) in self.cells:
            for polygon in cell.build_polygons():
                # Translate the polygon to its specified position
                p = polygon.copy()  # Create a copy to avoid modifying the original 
                p.translate(x, y)
                polygons.append(p)
        return polygons