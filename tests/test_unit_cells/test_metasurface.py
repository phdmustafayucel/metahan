from metahan.unit_cells.circle import CircleCell
from metahan.unit_cells.supercell import SuperCell
from metahan.core.lattice import Lattice
from metahan.core.builder import MetasurfaceBuilder
import gdstk


circle1 = CircleCell(radius_um=0.2)
circle2 = CircleCell(radius_um=0.1)

supercell = SuperCell(cells=[(circle1, (0, 0)), (circle2, (0.5, 0.5))])

lattice = Lattice(pitch=1.0)

builder = MetasurfaceBuilder(
    unit_cell=supercell, 
    lattice=lattice, 
    center=(0, 0)
    )

polygons = builder.build()

cell = gdstk.Cell("METASURFACE")
cell.add(*polygons)

lib = gdstk.Library()
lib.add(cell)

lib.write_gds("metasurface_test.gds")