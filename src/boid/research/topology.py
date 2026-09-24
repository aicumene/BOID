from __future__ import annotations

import numpy as np


def persistence_summary(points: np.ndarray, maxdim: int = 1) -> dict[str, float]:
    """Vietoris–Rips persistence summaries. Requires optional `ripser`."""
    try:
        from ripser import ripser
    except ImportError as exc:
        raise ImportError(
            "Persistent homology requires: pip install -e '.[topology]'"
        ) from exc

    X = np.asarray(points, dtype=float)
    dgms = ripser(X, maxdim=maxdim)["dgms"]
    out = {}

    for q, dgm in enumerate(dgms):
        finite = dgm[np.isfinite(dgm[:, 1])]
        lifetimes = finite[:, 1] - finite[:, 0] if len(finite) else np.array([])
        if lifetimes.size and np.sum(lifetimes) > 0:
            p = lifetimes / np.sum(lifetimes)
            entropy = -np.sum(p*np.log(p))
            long_count = int(np.sum(lifetimes > np.quantile(lifetimes, 0.75)))
            max_life = float(np.max(lifetimes))
        else:
            entropy = float("nan")
            long_count = 0
            max_life = 0.0

        out[f"H{q}_persistence_entropy"] = float(entropy)
        out[f"H{q}_long_lived_count"] = float(long_count)
        out[f"H{q}_max_lifetime"] = max_life

    return out
