"""Grassmannian geometry helpers for BOID signal subspaces."""

from __future__ import annotations

import numpy as np


def _orthonormal_columns(U: np.ndarray) -> np.ndarray:
    U = np.asarray(U)
    if U.ndim != 2 or U.shape[1] == 0:
        raise ValueError("U must be a non-empty 2D basis matrix.")
    Q, _ = np.linalg.qr(U)
    return Q[:, : U.shape[1]]


def principal_angles(U: np.ndarray, V: np.ndarray) -> np.ndarray:
    """Principal angles between equal-dimensional subspaces in radians."""
    Uq = _orthonormal_columns(U)
    Vq = _orthonormal_columns(V)
    if Uq.shape[0] != Vq.shape[0]:
        raise ValueError("Subspaces must share the same ambient dimension.")
    if Uq.shape[1] != Vq.shape[1]:
        raise ValueError("Subspaces must have the same intrinsic dimension.")
    s = np.linalg.svd(Uq.conj().T @ Vq, compute_uv=False)
    s = np.clip(np.real(s), 0.0, 1.0)
    return np.arccos(s)


def grassmann_geodesic_distance(U: np.ndarray, V: np.ndarray) -> float:
    """Geodesic Grassmann distance: sqrt(sum(theta_i^2))."""
    theta = principal_angles(U, V)
    return float(np.linalg.norm(theta))


def grassmann_projection_distance(U: np.ndarray, V: np.ndarray) -> float:
    """Projection Grassmann distance: sqrt(sum(sin(theta_i)^2))."""
    theta = principal_angles(U, V)
    return float(np.linalg.norm(np.sin(theta)))
