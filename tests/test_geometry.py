import numpy as np

from boid.geometry import (
    grassmann_geodesic_distance,
    grassmann_projection_distance,
)


def test_identical_subspaces_have_zero_distance():
    U = np.eye(4)[:, :2]
    assert grassmann_geodesic_distance(U, U) < 1e-12
    assert grassmann_projection_distance(U, U) < 1e-12


def test_orthogonal_lines_have_pi_over_two_geodesic_distance():
    U = np.array([[1.0], [0.0]])
    V = np.array([[0.0], [1.0]])
    assert np.isclose(grassmann_geodesic_distance(U, V), np.pi / 2)
    assert np.isclose(grassmann_projection_distance(U, V), 1.0)
