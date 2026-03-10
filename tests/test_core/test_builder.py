from metahan.apertures.rectangle import RectangleAperture
from metahan.core.builder import MetasurfaceBuilder
from metahan.core.lattice import Lattice
from metahan.core.metasurface import MetasurfaceSpec
from metahan.unit_cells.circle import CircleCell
from metahan.unit_cells.supercell import SuperCell
from metahan.unit_cells.cross import CrossCell
import gdstk

if __name__ == "__main__":

    supercell1 = SuperCell(cells=[(CircleCell(radius_um=0.25), (0, 0)), (CircleCell(radius_um=0.1), (0.5, 0.5))])
    supercell2 = SuperCell(cells=[(CrossCell(arm_length_um=0.5, arm_width_um=0.1), (0, 0))])
    metasurface1 = MetasurfaceSpec(
        unit_cell=supercell1,
        lattice=Lattice(pitch=1.5),
        center=(100, 100),
        rotation_deg=45.0,
        nx=200,
        ny=200,
        aperture=RectangleAperture(width=100, height=100),
        name="METASURFACE_1",
    )

    metasurface2 = MetasurfaceSpec(
        unit_cell=supercell2,
        lattice=Lattice(pitch=1.5),
        center=(0, 0),
        rotation_deg=0.0,
        nx=200,
        ny=200,
        aperture=RectangleAperture(width=100, height=100),
        name="METASURFACE_2",
    )

    lib = gdstk.Library()

    # Build each metasurface in its own cell
    ms1_cell = gdstk.Cell(metasurface1.name)
    ms1_polygons = MetasurfaceBuilder(surfaces=[metasurface1]).build()
    ms1_cell.add(*ms1_polygons)
    lib.add(ms1_cell)

    ms2_cell = gdstk.Cell(metasurface2.name)
    ms2_polygons = MetasurfaceBuilder(surfaces=[metasurface2]).build()
    ms2_cell.add(*ms2_polygons)
    lib.add(ms2_cell)

    # Parent group cell
    measurable_cell = gdstk.Cell("METASURFACE_MEASURABLE")
    measurable_cell.add(gdstk.Reference(ms1_cell, origin=(0, 0)))
    measurable_cell.add(gdstk.Reference(ms2_cell, origin=(400, 0)))
    lib.add(measurable_cell)

    lib.write_gds("builder_test.gds")
