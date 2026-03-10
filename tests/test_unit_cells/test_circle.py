import gdstk
from metahan.unit_cells.circle import CircleCell

def test_circle_cell(tmp_path):
    # Create unit cell
    cell = CircleCell(radius_um=0.5)

    # Build polygon
    polygon = cell.build_polygons()

    # Creat GDS cell
    gds_cell = gdstk.Cell("CIRCLE_TEST_CELL")
    gds_cell.add(*polygon) # Unfold the list of polygons into individual arguments
    # Create library
    lib = gdstk.Library()
    lib.add(gds_cell)

    # Write to GDS file
    gds_file = tmp_path / "circle_cell_test.gds"
    lib.write_gds(str(gds_file))

    assert gds_file.exists(), "GDS file was not created"

if __name__ == "__main__":
    from pathlib import Path
    test_circle_cell(tmp_path=Path("."))