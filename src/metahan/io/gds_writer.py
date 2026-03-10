# src/metahan/io/gds_writer.py
from __future__ import annotations

from pathlib import Path
from typing import Optional

import gdstk

from metahan.core.builder import MetasurfaceBuilder
from metahan.io.config_loader import LayoutConfig


def write_layout_gds(config: LayoutConfig, output_file: Optional[str] = None) -> Path:
    lib = gdstk.Library()
    used_names = set()

    def unique(name: str) -> str:
        if name not in used_names:
            used_names.add(name)
            return name
        i = 2
        while f"{name}_{i}" in used_names:
            i += 1
        final = f"{name}_{i}"
        used_names.add(final)
        return final

    def as_group_name(name: str) -> str:
        return name if name.startswith("GROUP_") else f"GROUP_{name}"

    def apply_group_tag(polygons: list[gdstk.Polygon], layer: int, datatype: int) -> None:
        for poly in polygons:
            poly.layer = layer
            poly.datatype = datatype

    top_root = gdstk.Cell(unique("TOP"))
    lib.add(top_root)

    for top in config.top_cells:
        group_cell = gdstk.Cell(unique(as_group_name(top.name)))
        lib.add(group_cell)
        top_root.add(gdstk.Reference(group_cell))

        for item in top.metasurfaces:
            ms_cell_name = unique(item.cell_name)
            ms_cell = gdstk.Cell(ms_cell_name)
            polys = MetasurfaceBuilder([item.spec]).build()
            if polys:
                apply_group_tag(polys, top.layer, top.datatype)
                ms_cell.add(*polys)
            lib.add(ms_cell)
            group_cell.add(gdstk.Reference(ms_cell, origin=item.origin))

    target = Path(output_file or config.output_file)
    lib.write_gds(str(target))
    return target
