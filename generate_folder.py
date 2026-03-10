from pathlib import Path

# Nom du dossier racine du repo (change-le si tu veux)
ROOT = Path("metasurface-gds")

DIRS = [
    ".github/workflows",
    "docs",
    "examples",
    "configs/unit_cells",
    "configs/apertures",
    "configs/examples",
    "output/gds",
    "output/previews",
    "scripts",
    "src/metasurface_gds",
    "src/metasurface_gds/core",
    "src/metasurface_gds/geometry",
    "src/metasurface_gds/unit_cells",
    "src/metasurface_gds/apertures",
    "src/metasurface_gds/mapping",
    "src/metasurface_gds/io",
    "src/metasurface_gds/utils",
    "tests",
    "tests/test_unit_cells",
    "tests/test_apertures",
    "tests/test_core",
    "tests/test_io",
]

FILES = [
    ".github/workflows/ci.yml",

    "docs/architecture.md",
    "docs/unit_cells.md",
    "docs/metasurface_shapes.md",

    "examples/example_circle_aperture.py",
    "examples/example_rectangle_aperture.py",
    "examples/example_half_disk_aperture.py",
    "examples/example_param_sweep.py",

    "configs/unit_cells/circle.yaml",
    "configs/unit_cells/ellipse.yaml",
    "configs/unit_cells/rectangle.yaml",
    "configs/unit_cells/square.yaml",
    "configs/unit_cells/cross.yaml",
    "configs/unit_cells/triangle.yaml",

    "configs/apertures/square.yaml",
    "configs/apertures/rectangle.yaml",
    "configs/apertures/circle.yaml",
    "configs/apertures/half_circle.yaml",

    "configs/examples/demo_square_on_circle.yaml",
    "configs/examples/demo_cross_on_rectangle.yaml",

    "scripts/run_from_config.py",
    "scripts/batch_generate.py",

    "src/metasurface_gds/__init__.py",
    "src/metasurface_gds/cli.py",
    "src/metasurface_gds/constants.py",
    "src/metasurface_gds/exceptions.py",

    "src/metasurface_gds/core/__init__.py",
    "src/metasurface_gds/core/builder.py",
    "src/metasurface_gds/core/lattice.py",
    "src/metasurface_gds/core/placement.py",
    "src/metasurface_gds/core/params.py",
    "src/metasurface_gds/core/validation.py",

    "src/metasurface_gds/geometry/__init__.py",
    "src/metasurface_gds/geometry/primitives.py",
    "src/metasurface_gds/geometry/transforms.py",
    "src/metasurface_gds/geometry/utils.py",

    "src/metasurface_gds/unit_cells/__init__.py",
    "src/metasurface_gds/unit_cells/base.py",
    "src/metasurface_gds/unit_cells/registry.py",
    "src/metasurface_gds/unit_cells/circle.py",
    "src/metasurface_gds/unit_cells/ellipse.py",
    "src/metasurface_gds/unit_cells/rectangle.py",
    "src/metasurface_gds/unit_cells/square.py",
    "src/metasurface_gds/unit_cells/cross.py",
    "src/metasurface_gds/unit_cells/triangle.py",

    "src/metasurface_gds/apertures/__init__.py",
    "src/metasurface_gds/apertures/base.py",
    "src/metasurface_gds/apertures/registry.py",
    "src/metasurface_gds/apertures/square.py",
    "src/metasurface_gds/apertures/rectangle.py",
    "src/metasurface_gds/apertures/circle.py",
    "src/metasurface_gds/apertures/half_circle.py",

    "src/metasurface_gds/mapping/__init__.py",
    "src/metasurface_gds/mapping/phase_map.py",
    "src/metasurface_gds/mapping/lookup_table.py",
    "src/metasurface_gds/mapping/strategies.py",

    "src/metasurface_gds/io/__init__.py",
    "src/metasurface_gds/io/config_loader.py",
    "src/metasurface_gds/io/gds_writer.py",
    "src/metasurface_gds/io/preview.py",
    "src/metasurface_gds/io/naming.py",

    "src/metasurface_gds/utils/__init__.py",
    "src/metasurface_gds/utils/logging.py",
    "src/metasurface_gds/utils/units.py",

    "tests/__init__.py",
    "tests/conftest.py",

    "tests/test_unit_cells/test_circle.py",
    "tests/test_unit_cells/test_ellipse.py",
    "tests/test_unit_cells/test_rectangle.py",
    "tests/test_unit_cells/test_cross.py",
    "tests/test_unit_cells/test_triangle.py",

    "tests/test_apertures/test_circle_aperture.py",
    "tests/test_apertures/test_rectangle_aperture.py",
    "tests/test_apertures/test_half_circle_aperture.py",

    "tests/test_core/test_lattice.py",
    "tests/test_core/test_placement.py",
    "tests/test_core/test_builder.py",

    "tests/test_io/test_config_loader.py",
    "tests/test_io/test_gds_writer.py",

    ".gitignore",
    ".pre-commit-config.yaml",
    "LICENSE",
    "README.md",
    "pyproject.toml",
    "requirements.txt",
    "Makefile",
]

DEFAULT_CONTENT = {
    ".gitignore": """__pycache__/
*.pyc
.venv/
.env
.pytest_cache/
.mypy_cache/
coverage.xml
htmlcov/

output/gds/*
!output/gds/.gitkeep
output/previews/*
!output/previews/.gitkeep

*.gds
*.oas
""",
    "README.md": """# MetaHan

**Hub for Advanced Nanodesign**

Python toolkit for metasurface layout and GDS generation.
""",
    "src/metasurface_gds/__init__.py": '__version__ = "0.1.0"\n',
}

def main():
    # Create directories
    for d in DIRS:
        (ROOT / d).mkdir(parents=True, exist_ok=True)

    # Create files
    for rel_path in FILES:
        path = ROOT / rel_path
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            content = DEFAULT_CONTENT.get(rel_path, "")
            path.write_text(content, encoding="utf-8")

    # Keep empty output directories tracked by git
    for keep in ["output/gds/.gitkeep", "output/previews/.gitkeep"]:
        kp = ROOT / keep
        kp.parent.mkdir(parents=True, exist_ok=True)
        if not kp.exists():
            kp.write_text("", encoding="utf-8")

    print(f"✅ Structure créée dans : {ROOT.resolve()}")

if __name__ == "__main__":
    main()