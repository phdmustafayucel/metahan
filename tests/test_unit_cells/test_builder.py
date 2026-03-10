# Here we test the MetasurfaceBuilder with a simple supercell consisting of two circles. The test checks if the builder can create a metasurface with the given supercell and lattice, and if the resulting GDS file is generated without errors.
from metahan.apertures.rectangle import RectangleAperture
from metahan.unit_cells.circle import CircleCell
from metahan.unit_cells.supercell import SuperCell
from metahan.core.lattice import Lattice
from metahan.core.builder import MetasurfaceBuilder
import gdstk

lattice = Lattice(pitch=1.0)
cell = CircleCell(radius_um=0.5)
position = (0.0, 0.0)
unit_cell = SuperCell([(cell, position)])
aperture = RectangleAperture(width=100, height=100)

builder = MetasurfaceBuilder(
    unit_cell=unit_cell,
    lattice=lattice,
    aperture=aperture,
    center=(0.0, 0.0)
)
built_polygons = builder.build()
cell = gdstk.Cell("TEST_BUILDER")


cell.add(*built_polygons)
lib = gdstk.Library()
lib.add(cell)
lib.write_gds("test_builder.gds")
