# src/metahan/io/config_loader.py
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml

from metahan.apertures.circle import CircleAperture
from metahan.apertures.rectangle import RectangleAperture
from metahan.apertures.square import SquareAperture
from metahan.core.lattice import Lattice
from metahan.core.metasurface import MetasurfaceSpec
from metahan.unit_cells.circle import CircleCell
from metahan.unit_cells.cross import CrossCell
from metahan.unit_cells.ellipse import EllipseCell
from metahan.unit_cells.rectangle import RectangleCell
from metahan.unit_cells.square import SquareCell
from metahan.unit_cells.supercell import SuperCell
from metahan.unit_cells.triangle import TriangleCell


@dataclass
class PlacedMetasurface:
    cell_name: str
    spec: MetasurfaceSpec
    origin: Tuple[float, float] = (0.0, 0.0)


@dataclass
class TopCellConfig:
    name: str
    metasurfaces: List[PlacedMetasurface]
    layer: int = 1
    datatype: int = 0


@dataclass
class LayoutConfig:
    output_file: str
    top_cells: List[TopCellConfig]


def _to_xy(value: Any, field: str) -> Tuple[float, float]:
    if not isinstance(value, (list, tuple)) or len(value) != 2:
        raise ValueError(f"'{field}' must be [x, y].")
    return float(value[0]), float(value[1])


def _build_unit_cell(cfg: Dict[str, Any]):
    t = cfg.get("type")
    if t == "circle":
        return CircleCell(radius_um=float(cfg["radius_um"]))
    if t == "square":
        return SquareCell(side_um=float(cfg["side_um"]))
    if t == "rectangle":
        return RectangleCell(width_um=float(cfg["width_um"]), height_um=float(cfg["height_um"]))
    if t == "ellipse":
        return EllipseCell(radius_x_um=float(cfg["radius_x_um"]), radius_y_um=float(cfg["radius_y_um"]))
    if t == "triangle":
        return TriangleCell(side_um=float(cfg["side_um"]))
    if t == "cross":
        return CrossCell(arm_length_um=float(cfg["arm_length_um"]), arm_width_um=float(cfg["arm_width_um"]))
    if t == "supercell":
        cells = []
        for item in cfg.get("cells", []):
            child = _build_unit_cell(item)
            offset = _to_xy(item.get("offset", [0.0, 0.0]), "offset")
            cells.append((child, offset))
        return SuperCell(cells=cells)
    raise ValueError(f"Unsupported unit_cell.type: {t}")


def _build_aperture(cfg: Optional[Dict[str, Any]]):
    if cfg is None:
        return None
    t = cfg.get("type")
    if t == "rectangle":
        return RectangleAperture(width=float(cfg["width"]), height=float(cfg["height"]))
    if t == "circle":
        return CircleAperture(radius=float(cfg["radius"]))
    if t == "square":
        return SquareAperture(side=float(cfg["side"]))
    raise ValueError(f"Unsupported aperture.type: {t}")


def _build_spec(cfg: Dict[str, Any]) -> MetasurfaceSpec:
    unit_cell = _build_unit_cell(cfg["unit_cell"])
    aperture = _build_aperture(cfg.get("aperture"))
    center = _to_xy(cfg.get("center", [0.0, 0.0]), "center")

    positions = cfg.get("positions")
    if positions is not None:
        parsed_positions = [(_to_xy(p, "positions[]")) for p in positions]
        return MetasurfaceSpec(
            name=cfg.get("name"),
            unit_cell=unit_cell,
            positions=parsed_positions,
            center=center,
            rotation_deg=float(cfg.get("rotation_deg", 0.0)),
            aperture=aperture,
        )

    lattice_cfg = cfg.get("lattice", {})
    lattice = Lattice(pitch=float(lattice_cfg["pitch"]))
    return MetasurfaceSpec(
        name=cfg.get("name"),
        unit_cell=unit_cell,
        lattice=lattice,
        nx=int(lattice_cfg["nx"]),
        ny=int(lattice_cfg["ny"]),
        lattice_kind=str(lattice_cfg.get("kind", "square")),
        center=center,
        rotation_deg=float(cfg.get("rotation_deg", 0.0)),
        aperture=aperture,
    )


def load_layout_config(path: str | Path) -> LayoutConfig:
    path = Path(path)
    with path.open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    output = raw.get("output", {})
    output_file = output.get("file", "layout.gds")

    top_cells: List[TopCellConfig] = []
    for top in raw.get("top_cells", []):
        metas = []
        for m in top.get("metasurfaces", []):
            spec = _build_spec(m)
            cell_name = m.get("name") or "METASURFACE"
            origin = _to_xy(m.get("origin", [0.0, 0.0]), "origin")
            metas.append(PlacedMetasurface(cell_name=cell_name, spec=spec, origin=origin))
        top_cells.append(
            TopCellConfig(
                name=top["name"],
                metasurfaces=metas,
                layer=int(top.get("layer", 1)),
                datatype=int(top.get("datatype", 0)),
            )
        )

    return LayoutConfig(output_file=output_file, top_cells=top_cells)
