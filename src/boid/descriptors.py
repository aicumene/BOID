from __future__ import annotations

import numpy as np
from aicumene_mssa import participation_ratio, entropy_rank, stable_rank as _stable_rank


def hankel_participation_ratio(singular_values: np.ndarray) -> float:
    return participation_ratio(singular_values)


def hankel_entropy_rank(singular_values: np.ndarray) -> float:
    return entropy_rank(singular_values)


def stable_rank(singular_values: np.ndarray) -> float:
    return _stable_rank(singular_values)


def shannon_entropy(probabilities: np.ndarray, normalize: bool = False) -> float:
    p = np.asarray(probabilities, dtype=float)
    p = p[np.isfinite(p) & (p > 0)]
    if p.size == 0:
        return float("nan")
    p = p / np.sum(p)
    h = -np.sum(p * np.log(p))
    if normalize and p.size > 1:
        h /= np.log(p.size)
    return float(h)


def weighted_frequency_summary(
    frequencies_hz: np.ndarray,
    powers: np.ndarray,
) -> dict[str, float]:
    f = np.asarray(frequencies_hz, dtype=float)
    w = np.asarray(powers, dtype=float)
    ok = np.isfinite(f) & np.isfinite(w) & (w >= 0)
    f, w = f[ok], w[ok]

    if f.size == 0:
        return {
            "mean_frequency_hz": float("nan"),
            "median_frequency_hz": float("nan"),
            "mode_frequency_entropy": float("nan"),
            "delta_fraction": float("nan"),
            "theta_fraction": float("nan"),
            "alpha_fraction": float("nan"),
            "beta_fraction": float("nan"),
            "hf_gt20_fraction": float("nan"),
        }

    if np.sum(w) <= 0:
        w = np.ones_like(f)
    w = w / np.sum(w)

    idx = np.argsort(f)
    fs = f[idx]
    ws = w[idx]
    median_f = float(fs[np.searchsorted(np.cumsum(ws), 0.5)])

    def frac(lo, hi):
        mask = (f >= lo) & (f < hi)
        return float(np.sum(w[mask]))

    return {
        "mean_frequency_hz": float(np.sum(w * f)),
        "median_frequency_hz": median_f,
        "mode_frequency_entropy": shannon_entropy(w, normalize=True),
        "delta_fraction": frac(1.0, 4.0),
        "theta_fraction": frac(4.0, 8.0),
        "alpha_fraction": frac(8.0, 13.0),
        "beta_fraction": frac(13.0, 30.0),
        "hf_gt20_fraction": float(np.sum(w[f > 20.0])),
    }
