"""Neuroscience application helpers for BOID.

The BOID method itself is domain-general. This module contains the application
conventions used by the accompanying neuroscience work.
"""

from __future__ import annotations

import numpy as np

from ..estimator import BOIDResult, estimate_boid
from ..preprocessing import preprocess_eeg


def estimate_eeg_boid(
    x: np.ndarray,
    fs: float,
    *,
    embedding_lag: int,
    finite_sample_correction: float,
    delay_samples: int = 1,
    target_fs: float = 100.0,
    preprocessing_band: tuple[float, float] = (0.5, 40.0),
    boid_band: tuple[float, float] = (1.0, 40.0),
) -> BOIDResult:
    """Apply the neuroscience BOID convention to one EEG analysis window.

    The 1–40 Hz BOID band is application-specific; it is not part of the
    general definition of Bernadotte Oscillator Intrinsic Dimension.
    """
    x_pre, fs_out, _ = preprocess_eeg(
        x,
        fs=fs,
        target_fs=target_fs,
        band=preprocessing_band,
    )
    return estimate_boid(
        x_pre,
        fs=fs_out,
        embedding_lag=embedding_lag,
        finite_sample_correction=finite_sample_correction,
        delay_samples=delay_samples,
        fmin=boid_band[0],
        fmax=boid_band[1],
    )
