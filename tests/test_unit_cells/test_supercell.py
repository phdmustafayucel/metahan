import gdstk
from metahan.apertures.circle import CircleAperture
from metahan.unit_cells.circle import CircleCell
from metahan.unit_cells.supercell import SuperCell
from metahan.unit_cells.base import UnitCell
from metahan.core.lattice import Lattice
from metahan.core.builder import MetasurfaceBuilder
import matplotlib.pyplot as plt
from metahan.apertures.rectangle import RectangleAperture

if __name__ == "__main__":


    circle1 = CircleCell(radius_um=0.15)
    circle2 = CircleCell(radius_um=0.1)
    
    supercell = SuperCell(cells=[(circle1, (0, 0)), (circle2, (0.5, 0.5))])
    lattice = Lattice(pitch=1)
    positions = lattice.square(nx=200, ny=200)
    aperture = RectangleAperture(width=100, height=100)

    aperture_positions = [
        (x, y) for (x, y) in positions
        if aperture.contains(x, y)
    ]

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.scatter(*zip(*aperture_positions), s=1)
    ax.set_aspect("equal")
    plt.show()
    # Now build the gds geometry without using MetasurfaceBuilder, to test the SuperCell directly

    cell = gdstk.Cell("SUPER_CELL_TEST")
    for x, y in aperture_positions:
        for poly in supercell.build_polygons():
            p = poly.copy()
            p.translate(x, y)
            cell.add(p)
    
    lib = gdstk.Library()
    lib.add(cell)
    lib.write_gds("supercell_test.gds")