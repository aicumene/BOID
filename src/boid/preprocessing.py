from __future__ import annotations

from fractions import Fraction
import numpy as np
from scipy.signal import butter, sosfiltfilt, resample_poly


def as_channels_by_samples(x: np.ndarray) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    if x.ndim == 1:
        x = x[None, :]
    if x.ndim != 2:
        raise ValueError("Expected a 1D or 2D array.")
    return x


def drop_invalid_channels(
    x: np.ndarray,
    variance_epsilon: float = 1e-12,
) -> tuple[np.ndarray, np.ndarray]:
    x = as_channels_by_samples(x)
    finite = np.all(np.isfinite(x), axis=1)
    variance = np.var(x, axis=1)
    keep = finite & (variance > float(variance_epsilon))
    return x[keep], keep


def bandpass_filter(
    x: np.ndarray,
    fs: float,
    low_hz: float = 0.5,
    high_hz: float = 40.0,
    order: int = 4,
) -> np.ndarray:
    x = as_channels_by_samples(x)
    nyq = fs / 2.0
    if not (0 < low_hz < high_hz < nyq):
        raise ValueError(
            f"Require 0 < low < high < Nyquist; got {low_hz}, {high_hz}, fs={fs}."
        )
    sos = butter(
        order,
        [low_hz / nyq, high_hz / nyq],
        btype="bandpass",
        output="sos",
    )
    return sosfiltfilt(sos, x, axis=-1)


def resample_signal(
    x: np.ndarray,
    fs: float,
    target_fs: float,
    max_denominator: int = 1000,
) -> tuple[np.ndarray, float]:
    x = as_channels_by_samples(x)
    if np.isclose(fs, target_fs):
        return x.copy(), float(fs)
    ratio = Fraction(float(target_fs) / float(fs)).limit_denominator(max_denominator)
    y = resample_poly(x, ratio.numerator, ratio.denominator, axis=-1)
    return y, float(target_fs)


def preprocess_eeg(
    x: np.ndarray,
    fs: float,
    target_fs: float = 100.0,
    band: tuple[float, float] = (0.5, 40.0),
    variance_epsilon: float = 1e-12,
    filter_order: int = 4,
) -> tuple[np.ndarray, float, np.ndarray]:
    """Light preprocessing used by the article-level BOID pipelines."""
    x, keep = drop_invalid_channels(x, variance_epsilon=variance_epsilon)
    if x.shape[0] == 0:
        raise ValueError("No usable EEG channels remain.")
    x = bandpass_filter(
        x,
        fs=fs,
        low_hz=band[0],
        high_hz=band[1],
        order=filter_order,
    )
    x, fs_out = resample_signal(x, fs=fs, target_fs=target_fs)
    return x, fs_out, keep


def iter_nonoverlapping_windows(
    x: np.ndarray,
    fs: float,
    window_seconds: float = 4.0,
    variance_epsilon: float = 1e-12,
):
    x = as_channels_by_samples(x)
    n = int(round(window_seconds * fs))
    if n <= 1:
        raise ValueError("Window length must contain at least two samples.")
    for start in range(0, x.shape[1] - n + 1, n):
        w = x[:, start:start + n]
        if not np.all(np.isfinite(w)):
            continue
        if np.var(w) <= variance_epsilon:
            continue
        yield start, w
