import pytest
import gdstk
from metahan.unit_cells.ring import RingCell


def test_ring_cell_creation():
    """Test basic ring cell creation with valid parameters."""
    cell = RingCell(outer_radius_um=1.0, inner_radius_um=0.5)
    assert cell.outer_radius_um == 1.0
    assert cell.inner_radius_um == 0.5
    assert cell.layer == 1
    assert cell.datatype == 0


def test_ring_cell_custom_layer_datatype():
    """Test ring cell creation with custom layer and datatype."""
    cell = RingCell(
        outer_radius_um=1.0,
        inner_radius_um=0.5,
        layer=5,
        datatype=2
    )
    assert cell.layer == 5
    assert cell.datatype == 2


def test_ring_cell_invalid_outer_radius():
    """Test that invalid outer radius raises ValueError."""
    with pytest.raises(ValueError, match="outer_radius_um must be > 0"):
        RingCell(outer_radius_um=0, inner_radius_um=0.5)
    
    with pytest.raises(ValueError, match="outer_radius_um must be > 0"):
        RingCell(outer_radius_um=-1.0, inner_radius_um=0.5)


def test_ring_cell_invalid_inner_radius():
    """Test that invalid inner radius raises ValueError."""
    with pytest.raises(ValueError, match="inner_radius_um must be > 0"):
        RingCell(outer_radius_um=1.0, inner_radius_um=0)
    
    with pytest.raises(ValueError, match="inner_radius_um must be > 0"):
        RingCell(outer_radius_um=1.0, inner_radius_um=-0.5)


def test_ring_cell_inner_radius_exceeds_outer():
    """Test that inner radius >= outer radius raises ValueError."""
    with pytest.raises(ValueError, match="inner_radius_um must be < outer_radius_um"):
        RingCell(outer_radius_um=1.0, inner_radius_um=1.0)
    
    with pytest.raises(ValueError, match="inner_radius_um must be < outer_radius_um"):
        RingCell(outer_radius_um=1.0, inner_radius_um=1.5)


def test_ring_cell_invalid_tolerance():
    """Test that invalid tolerance raises ValueError."""
    with pytest.raises(ValueError, match="tolerance_um must be > 0"):
        RingCell(outer_radius_um=1.0, inner_radius_um=0.5, tolerance_um=0)
    
    with pytest.raises(ValueError, match="tolerance_um must be > 0"):
        RingCell(outer_radius_um=1.0, inner_radius_um=0.5, tolerance_um=-1e-3)


def test_ring_cell_build_polygons():
    """Test that build_polygons returns a list of polygons."""
    cell = RingCell(outer_radius_um=1.0, inner_radius_um=0.5)
    polygons = cell.build_polygons()
    
    assert isinstance(polygons, list)
    assert len(polygons) > 0
    assert all(isinstance(p, gdstk.Polygon) for p in polygons)


def test_ring_cell_gds_export(tmp_path):
    """Test that ring cell can be exported to GDS format."""
    cell = RingCell(outer_radius_um=1.0, inner_radius_um=0.5)
    polygons = cell.build_polygons()
    
    # Create GDS cell
    gds_cell = gdstk.Cell("RING_TEST_CELL")
    gds_cell.add(*polygons)
    
    # Create library
    lib = gdstk.Library()
    lib.add(gds_cell)
    
    # Write to GDS file
    gds_file = tmp_path / "ring_cell_test.gds"
    lib.write_gds(str(gds_file))
    
    assert gds_file.exists(), "GDS file was not created"


def test_ring_cell_various_sizes():
    """Test ring cell with various size combinations."""
    test_cases = [
        (0.5, 0.1),
        (2.0, 1.0),
        (10.0, 5.0),
        (1.5, 0.75),
    ]
    
    for outer, inner in test_cases:
        cell = RingCell(outer_radius_um=outer, inner_radius_um=inner)
        polygons = cell.build_polygons()
        assert len(polygons) > 0, f"Failed to build polygons for outer={outer}, inner={inner}"


if __name__ == "__main__":
    from pathlib import Path
    
    # Basic test
    cell = RingCell(outer_radius_um=2.0, inner_radius_um=1.0)
    polygons = cell.build_polygons()
    
    gds_cell = gdstk.Cell("RING_TEST_CELL")
    gds_cell.add(*polygons)
    
    lib = gdstk.Library()
    lib.add(gds_cell)
    
    lib.write_gds("ring_cell_test.gds")
    print("GDS file created: ring_cell_test.gds")
