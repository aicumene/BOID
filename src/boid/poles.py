"""ESPRIT pole conversion and filtering utilities used by BOID."""

from __future__ import annotations

import numpy as np


def pole_frequency_hz(
    poles: np.ndarray,
    fs: float,
    delay_samples: int = 1,
) -> np.ndarray:
    """Convert discrete ESPRIT pole angles to signed frequencies in hertz."""
    if fs <= 0:
        raise ValueError("fs must be positive.")
    if int(delay_samples) < 1:
        raise ValueError("delay_samples must be >= 1.")
    poles = np.asarray(poles, dtype=complex)
    return np.angle(poles) * float(fs) / (2.0 * np.pi * int(delay_samples))


def pole_damping_per_second(
    poles: np.ndarray,
    fs: float,
    delay_samples: int = 1,
) -> np.ndarray:
    """Convert pole magnitudes to exponential damping/growth rates per second."""
    if fs <= 0:
        raise ValueError("fs must be positive.")
    if int(delay_samples) < 1:
        raise ValueError("delay_samples must be >= 1.")
    poles = np.asarray(poles, dtype=complex)
    mag = np.maximum(np.abs(poles), np.finfo(float).tiny)
    return np.log(mag) * float(fs) / int(delay_samples)


def select_positive_frequency_poles(
    poles: np.ndarray,
    frequencies_hz: np.ndarray,
    damping_per_second: np.ndarray,
    *,
    fmin: float,
    fmax: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Retain finite positive-frequency poles inside an application band.

    BOID is defined by the number of poles retained by this operation after
    MSSA signal-subspace estimation and TLS-ESPRIT recovery.
    """
    poles = np.asarray(poles, dtype=complex)
    frequencies_hz = np.asarray(frequencies_hz, dtype=float)
    damping_per_second = np.asarray(damping_per_second, dtype=float)

    if not (poles.shape == frequencies_hz.shape == damping_per_second.shape):
        raise ValueError("poles, frequencies_hz and damping_per_second must have matching shapes.")
    if not (0.0 <= float(fmin) < float(fmax)):
        raise ValueError("Require 0 <= fmin < fmax.")

    keep = (
        np.isfinite(frequencies_hz)
        & np.isfinite(damping_per_second)
        & (frequencies_hz >= float(fmin))
        & (frequencies_hz <= float(fmax))
    )
    p = poles[keep]
    f = frequencies_hz[keep]
    d = damping_per_second[keep]

    order = np.argsort(f)
    return p[order], f[order], d[order]
