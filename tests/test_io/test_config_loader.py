from metahan.io.config_loader import load_layout_config


def test_load_layout_config_supports_half_circle_aperture(tmp_path):
    path = tmp_path / "layout.yaml"
    path.write_text(
        "\n".join(
            [
                "output: { file: output/gds/test.gds }",
                "top_cells:",
                "  - name: TEST",
                "    metasurfaces:",
                "      - name: MS",
                "        origin: [0, 0]",
                "        unit_cell: { type: circle, radius_um: 0.15 }",
                "        lattice: { kind: square, pitch: 0.6, nx: 10, ny: 10 }",
                "        aperture:",
                "          type: half_circle",
                "          radius: 5",
                "          center: [0.0, 0.0]",
                "          orientation: up",
            ]
        ),
        encoding="utf-8",
    )

    cfg = load_layout_config(path)

    assert cfg.output_file == "output/gds/test.gds"
    assert len(cfg.top_cells) == 1
