from collections.abc import Sequence
from typing import Optional, Tuple, Union
import math 
import gdstk

from metahan.apertures.base import Aperture
from metahan.core.lattice import Lattice
from metahan.core.metasurface import MetasurfaceSpec
from metahan.unit_cells.base import UnitCell

Position = Tuple[float, float]

class MetasurfaceBuilder:
    def __init__(
        self,
        surfaces: Optional[Union[Sequence[MetasurfaceSpec], MetasurfaceSpec]] = None,
        *,
        unit_cell: Optional[UnitCell] = None,
        lattice: Optional[Lattice] = None,
        positions: Optional[Sequence[Position]] = None,
        center: Position = (0.0, 0.0),
        rotation_deg: float = 0.0,
        aperture: Optional[Aperture] = None,
        nx: Optional[int] = None,
        ny: Optional[int] = None,
        lattice_kind: str = "square",
        name: Optional[str] = None,
    ):
        if surfaces is not None and unit_cell is not None:
            raise TypeError("Use either 'surfaces' or legacy args, not both.")

        if surfaces is not None:
            if isinstance(surfaces, MetasurfaceSpec):
                self.surfaces = [surfaces]
            else:
                self.surfaces = list(surfaces)
        else:
            if unit_cell is None:
                raise TypeError("Provide 'surfaces' or legacy args including 'unit_cell'.")

            resolved_nx, resolved_ny = self._resolve_grid_size(nx, ny, lattice, aperture)
            self.surfaces = [
                MetasurfaceSpec(
                    unit_cell=unit_cell,
                    lattice=lattice,
                    positions=positions,
                    center=center,
                    rotation_deg=rotation_deg,
                    aperture=aperture,
                    nx=resolved_nx,
                    ny=resolved_ny,
                    lattice_kind=lattice_kind,
                    name=name,
                )
            ]

        if not self.surfaces:
            raise ValueError("'surfaces' cannot be empty.")

    @staticmethod
    def _resolve_grid_size(
        nx: Optional[int],
        ny: Optional[int],
        lattice: Optional[Lattice],
        aperture: Optional[Aperture],
    ) -> tuple[Optional[int], Optional[int]]:
        if lattice is None:
            return nx, ny

        if nx is not None and ny is not None:
            return nx, ny

        pitch = getattr(lattice, "pitch", None)
        if pitch is None or pitch <= 0:
            return nx or 1, ny or 1

        if aperture is not None and hasattr(aperture, "width") and hasattr(aperture, "height"):
            width = float(getattr(aperture, "width"))
            height = float(getattr(aperture, "height"))
            inferred_nx = max(1, int(math.ceil(width / pitch)))
            inferred_ny = max(1, int(math.ceil(height / pitch)))
            return nx or inferred_nx, ny or inferred_ny

        if aperture is not None and hasattr(aperture, "radius"):
            diameter = 2.0 * float(getattr(aperture, "radius"))
            inferred_n = max(1, int(math.ceil(diameter / pitch)))
            return nx or inferred_n, ny or inferred_n

        return nx or 1, ny or 1

    def _resolve_positions(self, spec: MetasurfaceSpec) -> list[Position]:
        if spec.positions is not None:
            return list(spec.positions)

        if spec.lattice is None or spec.nx is None or spec.ny is None:
            raise ValueError("Missing lattice grid parameters for metasurface generation.")

        if spec.lattice_kind == "square":
            return spec.lattice.square(nx=spec.nx, ny=spec.ny)
        if spec.lattice_kind == "hexagonal":
            return spec.lattice.hexagonal(nx=spec.nx, ny=spec.ny)
        raise ValueError(f"Unsupported lattice_kind '{spec.lattice_kind}'")

    def _filter_aperture(
            self, positions: list[Position], spec: MetasurfaceSpec
    ) -> list[Position]:
        if spec.aperture is None:
            return positions
        return [(x, y) for (x, y) in positions if spec.aperture.contains(x, y)]

    def _rotate_positions(
            self, positions: list[Position], angle_deg: float
    ) -> list[Position]:
        if angle_deg == 0.0:
            return positions

        angle_rad = math.radians(angle_deg)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        return [(x * cos_a - y * sin_a, x * sin_a + y * cos_a) for (x, y) in positions]

    def _translate_positions(
            self, positions: list[Position], center: Position
    ) -> list[Position]:
        if center == (0.0, 0.0):
            return positions

        cx, cy = center
        return [(x + cx, y + cy) for (x, y) in positions]

    def _build_one(self, spec: MetasurfaceSpec) -> list[gdstk.Polygon]:
        resolved_positions = self._resolve_positions(spec)
        aperture_positions = self._filter_aperture(resolved_positions, spec)
        rotated_positions = self._rotate_positions(aperture_positions, spec.rotation_deg)
        translated_positions = self._translate_positions(rotated_positions, spec.center)

        base_polygons = spec.unit_cell.build_polygons()
        polygons: list[gdstk.Polygon] = []

        for x, y in translated_positions:
            for poly in base_polygons:
                p = poly.copy()
                if spec.rotation_deg != 0.0:
                    p.rotate(math.radians(spec.rotation_deg))
                p.translate(x, y)
                polygons.append(p)

        return polygons

    def build(self) -> list[gdstk.Polygon]:
        polygons: list[gdstk.Polygon] = []
        for spec in self.surfaces:
            polygons.extend(self._build_one(spec))
        return polygons
