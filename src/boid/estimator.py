"""Core Bernadotte Oscillator Intrinsic Dimension estimator."""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from aicumene_mssa import MSSA, estimate_rank_bai_yin
from aicumene_mssa.rank import RankEstimate

from .esprit import tls_esprit
from .poles import pole_frequency_hz, pole_damping_per_second, select_positive_frequency_poles


@dataclass(frozen=True)
class BOIDResult:
    """Result of one-window BOID estimation."""

    boid: int
    rank: int
    poles: np.ndarray
    frequencies_hz: np.ndarray
    damping_per_second: np.ndarray
    mode_power: np.ndarray
    singular_values: np.ndarray
    rank_estimate: RankEstimate
    fmin_hz: float
    fmax_hz: float
    embedding_lag: int
    delay_samples: int


def _as_channels_samples(x: np.ndarray) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    if x.ndim == 1:
        x = x[None, :]
    if x.ndim != 2:
        raise ValueError("x must have shape (channels, samples).")
    if not np.all(np.isfinite(x)):
        raise ValueError("BOID input contains non-finite samples.")
    if x.shape[1] < 4:
        raise ValueError("BOID input is too short.")
    if np.var(x) <= 1e-15:
        raise ValueError("BOID input has near-zero variance.")
    return x


def _validate_band(fs: float, fmin: float, fmax: float) -> None:
    if fs <= 0:
        raise ValueError("fs must be positive.")
    if not (0.0 <= fmin < fmax <= fs / 2.0):
        raise ValueError(
            f"Require 0 <= fmin < fmax <= Nyquist; got "
            f"fmin={fmin}, fmax={fmax}, fs={fs}."
        )


def _estimate_positive_mode_power(
    x: np.ndarray,
    poles_positive: np.ndarray,
) -> np.ndarray:
    """Estimate aggregate per-mode power from complex least-squares amplitudes.

    The manuscript specifies per-channel complex amplitudes but not one unique
    numerical fitting routine. The least-squares convention is therefore kept
    isolated here as an explicit implementation choice.
    """
    if poles_positive.size == 0:
        return np.array([], dtype=float)

    n = x.shape[1]
    t = np.arange(n, dtype=float)
    all_poles = np.concatenate([poles_positive, np.conj(poles_positive)])

    with np.errstate(over="ignore", invalid="ignore"):
        V = np.column_stack([z ** t for z in all_poles])

    if not np.all(np.isfinite(V)):
        return np.full(len(poles_positive), np.nan)

    powers = np.zeros(len(poles_positive), dtype=float)
    for channel in x:
        coeff, *_ = np.linalg.lstsq(V, channel, rcond=None)
        powers += np.abs(coeff[: len(poles_positive)]) ** 2
    return powers


def estimate_boid(
    x: np.ndarray,
    fs: float,
    embedding_lag: int,
    finite_sample_correction: float,
    delay_samples: int = 1,
    fmin: float = 1.0,
    fmax: float = 40.0,
) -> BOIDResult:
    """Estimate Bernadotte Oscillator Intrinsic Dimension for one analysis window.

    BOID is defined operationally as the number of resolved positive-frequency
    TLS-ESPRIT poles in ``[fmin, fmax]`` after the signal subspace has been
    selected by the MSSA MP/Bai-Yin rank estimator.

    Notes
    -----
    The ideal relation ``rank = 2 * BOID`` applies only to an ideal purely
    oscillatory finite-component model. It is not used here as the empirical
    definition of BOID.
    """
    if embedding_lag is None:
        raise ValueError("embedding_lag must be supplied explicitly.")
    if finite_sample_correction is None:
        raise ValueError("finite_sample_correction (c_n) must be supplied explicitly.")

    L = int(embedding_lag)
    tau = int(delay_samples)
    if L < 2:
        raise ValueError("embedding_lag must be >= 2.")
    if tau < 1:
        raise ValueError("delay_samples must be >= 1.")

    _validate_band(float(fs), float(fmin), float(fmax))
    x = _as_channels_samples(x)

    mssa = MSSA(window_length=L, delay_samples=tau).fit(x)

    n_rows, n_columns = mssa.hankel_.shape
    if n_rows >= n_columns:
        raise ValueError(
            "MP/Bai-Yin rank estimation requires block-Hankel rows < columns; "
            f"got {n_rows} rows and {n_columns} columns. Reduce embedding_lag "
            "or delay_samples, increase window length, or reduce channels."
        )

    rank_est = estimate_rank_bai_yin(
        mssa.hankel_,
        finite_sample_correction=float(finite_sample_correction),
    )
    r = int(rank_est.rank)

    empty = dict(
        fmin_hz=float(fmin),
        fmax_hz=float(fmax),
        embedding_lag=L,
        delay_samples=tau,
    )

    if r == 0:
        return BOIDResult(
            boid=0,
            rank=0,
            poles=np.array([], dtype=complex),
            frequencies_hz=np.array([], dtype=float),
            damping_per_second=np.array([], dtype=float),
            mode_power=np.array([], dtype=float),
            singular_values=mssa.singular_values_,
            rank_estimate=rank_est,
            **empty,
        )

    U = mssa.signal_subspace(r)
    shifted_rows = U.shape[0] - x.shape[0]
    if r > shifted_rows:
        raise ValueError(
            f"Estimated signal rank r={r} exceeds the ESPRIT shift dimension "
            f"{shifted_rows}. Increase embedding_lag or use a longer window."
        )

    poles_all = tls_esprit(U, n_channels=x.shape[0])
    freq_all = pole_frequency_hz(poles_all, fs=float(fs), delay_samples=tau)
    damping_all = pole_damping_per_second(
        poles_all,
        fs=float(fs),
        delay_samples=tau,
    )

    poles, freq, damping = select_positive_frequency_poles(
        poles_all,
        freq_all,
        damping_all,
        fmin=float(fmin),
        fmax=float(fmax),
    )

    power = _estimate_positive_mode_power(x, poles)

    return BOIDResult(
        boid=int(len(poles)),
        rank=r,
        poles=poles,
        frequencies_hz=freq,
        damping_per_second=damping,
        mode_power=power,
        singular_values=mssa.singular_values_,
        rank_estimate=rank_est,
        **empty,
    )
