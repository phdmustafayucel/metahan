# src/metahan/unit_cells/base.py
"""
Base classes for unit cell implementations.

This module defines the abstract base class for all unit cells used in metasurface
generation. Unit cells represent the fundamental geometric shapes that are repeated
in a lattice structure to create metasurfaces.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
import gdstk


class UnitCell(ABC):
    """
    Abstract base class for all unit cell types.

    This class provides the interface that all unit cell implementations must follow.
    Each unit cell represents a geometric shape that can be placed in a lattice
    to form a metasurface. The unit cell is responsible for generating its own
    polygon geometry centered at the origin.

    Attributes:
        layer (int): The GDS layer number for the unit cell geometry.
        datatype (int): The GDS datatype number for the unit cell geometry.
    """

    def __init__(self, layer: int = 1, datatype: int = 0):
        """
        Initialize a unit cell with layer and datatype information.

        Args:
            layer (int): The GDS layer number. Defaults to 1.
            datatype (int): The GDS datatype number. Defaults to 0.
        """
        self.layer = layer
        self.datatype = datatype

    @abstractmethod
    def build_polygons(self) -> list[gdstk.Polygon]:
        """
        Build and return the polygon geometry for this unit cell.

        This method must be implemented by all concrete unit cell classes.
        The returned polygon should be centered at (0, 0) and represent the
        complete geometry of the unit cell.

        Returns:
            list[gdstk.Polygon]: A list of polygons representing the unit cell geometry.
        """
        raise NotImplementedError