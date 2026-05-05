"""
Diagnostic script: check polygon count, vertex count, and overlaps in a GDS file.
Usage: python scripts/diagnose_gds.py output/gds/metasurface_dose_test.gds
"""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

import gdstk


def main() -> None:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("output/gds/metasurface_dose_test.gds")
    if not path.exists():
        print(f"File not found: {path}")
        sys.exit(1)

    lib = gdstk.read_gds(str(path))
    print(f"GDS unit: {lib.unit} m  |  precision: {lib.precision} m")
    print(f"Cells: {[c.name for c in lib.cells]}\n")

    all_polys: list[gdstk.Polygon] = []
    for cell in lib.cells:
        flat = cell.get_polygons()
        all_polys.extend(flat)

    if not all_polys:
        print("No polygons found (may all be in references — flattening each cell).")
        return

    vertex_counts = [len(p.points) for p in all_polys]
    print(f"Total polygons : {len(all_polys)}")
    print(f"Max vertices   : {max(vertex_counts)}")
    print(f"Min vertices   : {min(vertex_counts)}")
    print(f"Avg vertices   : {sum(vertex_counts)/len(vertex_counts):.1f}")

    dist = Counter(vertex_counts)
    print("\nVertex count distribution (top 10):")
    for v, n in sorted(dist.items(), key=lambda x: -x[1])[:10]:
        print(f"  {v:4d} vertices : {n} polygons")

    # Overlap check: look for polygons with identical bounding boxes (same position)
    from collections import defaultdict
    bbox_map: dict[tuple, list[int]] = defaultdict(list)
    for i, p in enumerate(all_polys):
        bb = p.bounding_box()
        if bb is not None:
            key = (round(bb[0][0], 4), round(bb[0][1], 4), round(bb[1][0], 4), round(bb[1][1], 4))
            bbox_map[key].append(i)

    overlaps = {k: v for k, v in bbox_map.items() if len(v) > 1}
    if overlaps:
        print(f"\nWARNING: {len(overlaps)} bounding boxes shared by multiple polygons (possible duplicates/overlaps)")
        for bb, idxs in list(overlaps.items())[:5]:
            print(f"  bbox {bb}: polygon indices {idxs}")
    else:
        print("\nNo duplicate bounding boxes detected.")


if __name__ == "__main__":
    main()
