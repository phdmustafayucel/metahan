# Project Structure Guide

This document explains the purpose of each folder and file in the repository scaffold for **MetaHan** (metasurface layout and GDS generation toolkit).

## Repository Overview

This project is organized to separate:

* **Core logic** (geometry, placement, generation)
* **Shape definitions** (unit cells and apertures)
* **I/O** (config loading, GDS export, preview)
* **Configs** (YAML examples and defaults)
* **Examples** (demo scripts)
* **Tests** (unit/integration validation)
* **Documentation** (architecture and supported features)

---

## Root Directory Files

### `.gitignore`

Defines files/folders Git should ignore (e.g., generated GDS files, virtual environment, cache folders, Python bytecode).

### `.pre-commit-config.yaml`

Optional pre-commit hooks configuration (formatting, linting, basic checks before commit).

### `LICENSE`

Project license (e.g., MIT, BSD, GPL). Defines how others can use and distribute the code.

### `README.md`

Main project entry page for GitHub. Should contain:

* project description
* installation instructions
* quick start examples
* roadmap

### `pyproject.toml`

Modern Python project configuration file (dependencies, packaging metadata, tool config such as `pytest`, `ruff`, `black`, etc.).

### `requirements.txt`

Simpler dependency list for quick installation (useful for beginners or quick setups).

### `Makefile`

Convenience commands (e.g., `make test`, `make lint`, `make run`) for Linux/macOS users.

---

## GitHub CI

### `.github/workflows/ci.yml`

GitHub Actions workflow file for Continuous Integration (CI).
Typically runs:

* tests
* linting
* formatting checks

This helps ensure code quality on every push / pull request.

---

## Documentation Folder

### `docs/architecture.md`

Explains the software architecture:

* module responsibilities
* data flow (config -> builder -> geometry -> GDS)
* extension strategy (new shapes, new mappings)

### `docs/unit_cells.md`

Documentation for supported **unit cell** geometries (circle, ellipse, square, cross, triangle, etc.), including parameters.

### `docs/metasurface_shapes.md`

Documentation for supported **global metasurface/aperture** shapes (rectangle, square, circle, half-circle, etc.).

---

## Example Scripts

These are runnable examples demonstrating common use cases.

### `examples/example_circle_aperture.py`

Creates a metasurface with a **circular aperture** using one selected unit cell type.

### `examples/example_rectangle_aperture.py`

Creates a metasurface with a **rectangular aperture**.

### `examples/example_half_disk_aperture.py`

Creates a metasurface with a **half-circle / half-disk aperture**.

### `examples/example_param_sweep.py`

Runs a parameter sweep (e.g., pitch, cell size, aperture size) to generate multiple layouts.

---

## Configuration Files (`configs/`)

This folder contains YAML presets and demo configurations.

### `configs/unit_cells/`

Default parameter templates for each unit cell type.

* `circle.yaml` — default parameters for circular unit cells
* `ellipse.yaml` — default parameters for elliptical unit cells
* `rectangle.yaml` — default parameters for rectangular unit cells
* `square.yaml` — default parameters for square unit cells
* `cross.yaml` — default parameters for cross-shaped unit cells
* `triangle.yaml` — default parameters for triangular unit cells

### `configs/apertures/`

Default parameter templates for global metasurface shapes (apertures).

* `square.yaml` — square aperture parameters
* `rectangle.yaml` — rectangular aperture parameters
* `circle.yaml` — circular aperture parameters
* `half_circle.yaml` — half-circle aperture parameters

### `configs/examples/`

Complete example configs combining unit cells + aperture + lattice parameters.

* `demo_square_on_circle.yaml` — square unit cells inside a circular aperture
* `demo_cross_on_rectangle.yaml` — cross unit cells inside a rectangular aperture

---

## Output Folder (`output/`)

Stores generated files. Usually **ignored by Git**.

### `output/gds/`

Generated **GDSII** files (layout output).

### `output/previews/`

Generated previews (PNG/SVG/PDF snapshots) for quick visual inspection.

---

## Utility Scripts (`scripts/`)

Command-line helper scripts used during development and batch generation.

### `scripts/run_from_config.py`

Loads a YAML/JSON config and runs one metasurface generation job.

### `scripts/batch_generate.py`

Runs multiple generations (batch mode), typically from a folder of configs or a parameter list.

---

## Source Code (`src/metasurface_gds/`)

This is the main Python package (core implementation).

> Note: If the project branding is **MetaHan**, you may later rename this package to `src/metahan/`.

### `src/metasurface_gds/__init__.py`

Marks the folder as a Python package and may expose version info and top-level imports.

### `src/metasurface_gds/cli.py`

Command-line interface entry point (future command like `metahan build config.yaml`).

### `src/metasurface_gds/constants.py`

Stores constants such as:

* GDS layer numbers
* unit conversion constants
* tolerances / default values

### `src/metasurface_gds/exceptions.py`

Custom exception classes for cleaner error handling (config errors, invalid geometry, unsupported type, etc.).

---

## Core Generation Logic (`core/`)

This is the orchestration layer that connects config, geometry, placement, and export.

### `src/metasurface_gds/core/__init__.py`

Package marker.

### `src/metasurface_gds/core/builder.py`

Main orchestrator:

* loads validated parameters
* creates aperture and unit cell objects
* generates lattice points
* places geometries
* sends output to GDS writer

### `src/metasurface_gds/core/lattice.py`

Defines lattice/grid generation:

* pitch
* origin
* rectangular/hexagonal grids (future)
* point coordinates

### `src/metasurface_gds/core/placement.py`

Placement logic:

* checks whether points lie inside aperture
* region-based assignment (future)
* clipping / filtering / transforms before writing polygons

### `src/metasurface_gds/core/params.py`

Dataclasses or typed parameter models used internally after config parsing.

### `src/metasurface_gds/core/validation.py`

Validates user inputs:

* positive dimensions
* valid type names
* feature size constraints
* parameter compatibility

---

## Geometry Utilities (`geometry/`)

Low-level geometric operations used by both apertures and unit cells.

### `src/metasurface_gds/geometry/__init__.py`

Package marker.

### `src/metasurface_gds/geometry/primitives.py`

Creates base shapes and points/polygons (circles approximated by polygons, rectangles, triangles, etc.).

### `src/metasurface_gds/geometry/transforms.py`

Geometric transforms:

* translation
* rotation
* scaling
* mirroring

### `src/metasurface_gds/geometry/utils.py`

Shared geometry helpers:

* bounding boxes
* point-in-shape checks
* coordinate helpers

---

## Unit Cells (`unit_cells/`)

Defines the **meta-atom / unit cell** shapes.

### `src/metasurface_gds/unit_cells/__init__.py`

Package marker.

### `src/metasurface_gds/unit_cells/base.py`

Abstract base class/interface for all unit cells (common API like `build()` or `to_polygon()`).

### `src/metasurface_gds/unit_cells/registry.py`

Maps string names to classes, e.g.:

* `"circle"` -> `CircleCell`
* `"square"` -> `SquareCell`

This allows config-driven creation from YAML.

### `src/metasurface_gds/unit_cells/circle.py`

Implementation of circular unit cell geometry.

### `src/metasurface_gds/unit_cells/ellipse.py`

Implementation of elliptical unit cell geometry.

### `src/metasurface_gds/unit_cells/rectangle.py`

Implementation of rectangular unit cell geometry.

### `src/metasurface_gds/unit_cells/square.py`

Implementation of square unit cell geometry (often a rectangle specialization).

### `src/metasurface_gds/unit_cells/cross.py`

Implementation of cross-shaped unit cell geometry.

### `src/metasurface_gds/unit_cells/triangle.py`

Implementation of triangular unit cell geometry.

---

## Apertures (`apertures/`)

Defines the **global metasurface boundary** (where cells are allowed to be placed).

### `src/metasurface_gds/apertures/__init__.py`

Package marker.

### `src/metasurface_gds/apertures/base.py`

Abstract base class/interface for aperture shapes (common API like `contains(point)` and bounds).

### `src/metasurface_gds/apertures/registry.py`

Maps aperture names to classes, e.g.:

* `"circle"` -> `CircleAperture`
* `"half_circle"` -> `HalfCircleAperture`

### `src/metasurface_gds/apertures/square.py`

Square aperture implementation.

### `src/metasurface_gds/apertures/rectangle.py`

Rectangular aperture implementation.

### `src/metasurface_gds/apertures/circle.py`

Circular aperture implementation.

### `src/metasurface_gds/apertures/half_circle.py`

Half-circle aperture implementation.

---

## Mapping Layer (`mapping/`) — Optional / Advanced

Used when layout geometry depends on optical design targets (phase/amplitude maps, LUTs).

### `src/metasurface_gds/mapping/__init__.py`

Package marker.

### `src/metasurface_gds/mapping/phase_map.py`

Loads or computes a phase map (e.g., target phase at each position).

### `src/metasurface_gds/mapping/lookup_table.py`

Maps optical response targets to unit cell geometry parameters using a LUT.

### `src/metasurface_gds/mapping/strategies.py`

Strategies for assigning geometry across the metasurface:

* nearest LUT match
* interpolation
* region-based rules
* custom distributions

---

## Input / Output (`io/`)

Responsible for reading configs and writing outputs.

### `src/metasurface_gds/io/__init__.py`

Package marker.

### `src/metasurface_gds/io/config_loader.py`

Loads YAML/JSON configuration files and converts them into Python dictionaries or typed parameter objects.

### `src/metasurface_gds/io/gds_writer.py`

Exports geometry to **GDSII** (using `gdstk` or `gdspy`).

### `src/metasurface_gds/io/preview.py`

Creates quick visual previews (e.g., matplotlib or SVG), useful for debugging before exporting GDS.

### `src/metasurface_gds/io/naming.py`

Centralizes filename conventions (consistent naming for outputs based on config parameters).

---

## General Utilities (`utils/`)

Shared helper code that does not belong to one specific module.

### `src/metasurface_gds/utils/__init__.py`

Package marker.

### `src/metasurface_gds/utils/logging.py`

Logging helpers (structured logs, formatting, verbosity control).

### `src/metasurface_gds/utils/units.py`

Unit conversion helpers (nm / um / mm), ensuring consistent internal units.

---

## Tests (`tests/`)

Contains automated tests to validate behavior and prevent regressions.

### `tests/__init__.py`

Package marker for tests.

### `tests/conftest.py`

Shared pytest fixtures and test setup utilities.

---

### Unit Cell Tests (`tests/test_unit_cells/`)

Tests for unit cell geometry implementations.

* `test_circle.py` — validates circle cell geometry generation
* `test_ellipse.py` — validates ellipse cell geometry generation
* `test_rectangle.py` — validates rectangle cell geometry generation
* `test_cross.py` — validates cross cell geometry generation
* `test_triangle.py` — validates triangle cell geometry generation

---

### Aperture Tests (`tests/test_apertures/`)

Tests for aperture containment and bounds.

* `test_circle_aperture.py` — circle aperture behavior
* `test_rectangle_aperture.py` — rectangle aperture behavior
* `test_half_circle_aperture.py` — half-circle aperture behavior

---

### Core Logic Tests (`tests/test_core/`)

Tests for orchestration and placement logic.

* `test_lattice.py` — lattice/grid generation
* `test_placement.py` — point filtering / placement rules
* `test_builder.py` — end-to-end builder behavior

---

### I/O Tests (`tests/test_io/`)

Tests for configuration parsing and output writing.

* `test_config_loader.py` — YAML/JSON loading and validation behavior
* `test_gds_writer.py` — GDS export function behavior (basic checks)

---

## Suggested Development Order (Recommended)

If starting from scratch, implement files in this order:

1. `io/config_loader.py`
2. `unit_cells/base.py` + one shape (`square.py`)
3. `apertures/base.py` + one shape (`rectangle.py`)
4. `core/lattice.py`
5. `core/placement.py`
6. `io/gds_writer.py`
7. `core/builder.py`
8. examples + tests
9. additional shapes / advanced mapping

---

## Notes

* Many files are initially placeholders (empty files) and are meant to be implemented progressively.
* This structure is intentionally modular so new unit cells, apertures, and mapping strategies can be added without rewriting the whole project.
* YAML configs are used to keep **parameters separate from code**, making experiments reproducible and easier to version in Git.

---
