# src/metahan/cli.py
from __future__ import annotations

import argparse

from metahan.io.config_loader import load_layout_config
from metahan.io.gds_writer import write_layout_gds


def main() -> None:
    parser = argparse.ArgumentParser(description="Build GDS from YAML config.")
    parser.add_argument("--config", required=True, help="Path to YAML config.")
    parser.add_argument("--output", default=None, help="Optional output GDS path.")
    args = parser.parse_args()

    cfg = load_layout_config(args.config)
    out = write_layout_gds(cfg, output_file=args.output)
    print(f"Wrote: {out}")


if __name__ == "__main__":
    main()
