"""Utilities for state-dependent regulation of oscillator dimensionality.

BOID does not assume that a larger or smaller dimensionality is universally
better. These helpers summarize how BOID changes across labelled dynamical
states without imposing a direction of desirability.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class StateBOIDSummary:
    state: object
    n: int
    median_boid: float
    q25_boid: float
    q75_boid: float


def summarize_boid_by_state(
    boid_values,
    states,
) -> list[StateBOIDSummary]:
    """Return robust BOID summaries for each observed state label."""
    values = np.asarray(boid_values, dtype=float)
    labels = np.asarray(states, dtype=object)
    if values.ndim != 1 or labels.ndim != 1 or values.size != labels.size:
        raise ValueError("boid_values and states must be 1D arrays of equal length.")

    out: list[StateBOIDSummary] = []
    for state in dict.fromkeys(labels.tolist()):
        mask = labels == state
        x = values[mask]
        x = x[np.isfinite(x)]
        if x.size == 0:
            continue
        q25, med, q75 = np.quantile(x, [0.25, 0.50, 0.75])
        out.append(
            StateBOIDSummary(
                state=state,
                n=int(x.size),
                median_boid=float(med),
                q25_boid=float(q25),
                q75_boid=float(q75),
            )
        )
    return out


def median_boid_shift(before, after) -> float:
    """Median BOID(after) minus median BOID(before), with no value judgement."""
    a = np.asarray(before, dtype=float)
    b = np.asarray(after, dtype=float)
    a = a[np.isfinite(a)]
    b = b[np.isfinite(b)]
    if a.size == 0 or b.size == 0:
        return float("nan")
    return float(np.median(b) - np.median(a))
