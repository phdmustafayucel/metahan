from dataclasses import dataclass
from typing import Optional, Sequence
from metahan.unit_cells.base import UnitCell
from metahan.core.lattice import Lattice
from metahan.apertures.base import Aperture

@dataclass
class MetasurfaceSpec:
    unit_cell: UnitCell
    lattice: Optional[Lattice] = None
    positions: Optional[Sequence[tuple[float, float]]] = None
    center: tuple[float, float] = (0.0, 0.0)
    rotation_deg: float = 0.0
    aperture: Optional[Aperture] = None
    nx: Optional[int] = None
    ny: Optional[int] = None
    lattice_kind: str = "square"
    name: Optional[str] = None

    def __post_init__(self) -> None:
        allowed_kinds = {"square", "hexagonal"}
        if self.lattice_kind not in allowed_kinds:
            raise ValueError(
                f"Unsupported lattice_kind '{self.lattice_kind}'. "
                f"Expected one of {sorted(allowed_kinds)}."
            )

        has_positions = self.positions is not None
        has_lattice_grid = self.lattice is not None

        if has_positions and has_lattice_grid:
            raise ValueError(
                "Provide either 'positions' or ('lattice' with 'nx' and 'ny'), not both."
            )

        if not has_positions and not has_lattice_grid:
            raise ValueError(
                "You must provide either 'positions' or ('lattice' with 'nx' and 'ny')."
            )

        if has_lattice_grid:
            if self.nx is None or self.ny is None:
                raise ValueError(
                    "When 'lattice' is provided, both 'nx' and 'ny' must be set."
                )
            if self.nx <= 0 or self.ny <= 0:
                raise ValueError("'nx' and 'ny' must be positive integers.")
        else:
            if self.nx is not None or self.ny is not None:
                raise ValueError(
                    "'nx' and 'ny' can only be set when 'lattice' is provided."
                )
