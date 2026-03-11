from metahan.apertures.half_circle import HalfCircleAperture


def test_half_circle_contains_points_in_selected_half():
    aperture = HalfCircleAperture(radius=5.0, orientation="up")

    assert aperture.contains(0.0, 2.0)
    assert aperture.contains(0.0, 0.0)
    assert not aperture.contains(0.0, -0.1)
    assert not aperture.contains(6.0, 0.0)


def test_half_circle_supports_horizontal_orientations():
    aperture = HalfCircleAperture(radius=5.0, orientation="left")

    assert aperture.contains(-1.0, 0.0)
    assert not aperture.contains(1.0, 0.0)
