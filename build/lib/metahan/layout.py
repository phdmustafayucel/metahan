from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Literal

import matplotlib.pyplot as plt

from metahan.core.builder import MetasurfaceBuilder
from metahan.io.config_loader import LayoutConfig, load_layout_config
from metahan.io.gds_writer import build_layout_library

PlotMode = Literal["points"]


class LayoutResult:
    def __init__(self, config: LayoutConfig):
        self.config = config
        self.library, self.top_cell_name = build_layout_library(config)

    def write_gds(self, output_file: str | Path | None = None) -> Path:
        target = Path(output_file or self.config.output_file)
        self.library.write_gds(str(target))
        return target

    def plot(self, mode: PlotMode = "points", show: bool = True):
        if mode != "points":
            raise ValueError(f"Unsupported plot mode '{mode}'. Expected 'points'.")

        fig, ax = plt.subplots(figsize=(8, 8))
        seen: set[tuple[int, int]] = set()

        for group in self.config.top_cells:
            xs: list[float] = []
            ys: list[float] = []
            for item in group.metasurfaces:
                builder = MetasurfaceBuilder([item.spec])
                positions = builder._resolve_positions(item.spec)
                positions = builder._filter_aperture(positions, item.spec)
                positions = builder._rotate_positions(positions, item.spec.rotation_deg)
                positions = builder._translate_positions(positions, item.spec.center)
                ox, oy = item.origin
                for x, y in positions:
                    xs.append(x + ox)
                    ys.append(y + oy)

            if not xs:
                continue

            key = (group.layer, group.datatype)
            label = None
            if key not in seen:
                label = f"Layer {group.layer} / Datatype {group.datatype}"
                seen.add(key)

            ax.scatter(
                xs,
                ys,
                s=2,
                c=f"C{(group.layer - 1) % 10}",
                alpha=0.8,
                linewidths=0,
                label=label,
            )

        ax.autoscale()
        ax.set_aspect("equal", adjustable="box")
        ax.set_xlabel("x (um)")
        ax.set_ylabel("y (um)")
        ax.set_title(f"{self.top_cell_name} preview")
        handles, labels = ax.get_legend_handles_labels()
        if labels:
            ax.legend(loc="best")

        if show:
            plt.show()
        return fig, ax

    def show(self, app: str | None = None, output_file: str | Path | None = None) -> Path:
        target = Path(output_file) if output_file is not None else Path(tempfile.mkdtemp(prefix="metahan_")) / "layout.gds"
        written = self.write_gds(target)

        if app is not None:
            subprocess.Popen([app, str(written)])
            return written

        if sys.platform.startswith("win"):
            os.startfile(str(written))
            return written

        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.Popen([opener, str(written)])
        return written


def build_layout(config: str | Path | LayoutConfig) -> LayoutResult:
    if isinstance(config, LayoutConfig):
        resolved = config
    else:
        resolved = load_layout_config(config)
    return LayoutResult(resolved)
