# src/metahan/cli.py
from __future__ import annotations

import argparse

from metahan.layout import build_layout


def main() -> None:
    parser = argparse.ArgumentParser(description="Build GDS from YAML config.")
    parser.add_argument("--config", required=True, help="Path to YAML config.")
    parser.add_argument("--output", default=None, help="Optional output GDS path.")
    args = parser.parse_args()

    layout = build_layout(args.config)
    out = layout.write_gds(args.output)
    print(f"Wrote: {out}")


if __name__ == "__main__":
    main()
