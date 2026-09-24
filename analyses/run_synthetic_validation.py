from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from boid.research.synthetic import generate_exposinusoidal_signal
from boid.estimator import estimate_boid
from boid.research.complexity import normalized_lz76, spectral_entropy


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--embedding-lag", type=int, required=True)
    p.add_argument("--c-n", type=float, required=True)
    p.add_argument("--seed", type=int, default=2026)
    p.add_argument("--channels", type=int, default=2)
    p.add_argument("--output", type=Path, default=Path("synthetic_results.csv"))
    args = p.parse_args()

    rng = np.random.default_rng(args.seed)
    rows = []

    for m in [3, 12]:
        for sigma in [0.3, 1.5]:
            for rep in range(40):
                x, _ = generate_exposinusoidal_signal(
                    n_oscillators=m,
                    fs=100.0,
                    duration_seconds=4.0,
                    n_channels=args.channels,
                    fmin=2.0,
                    fmax=40.0,
                    noise_sigma=sigma,
                    rng=rng,
                )
                result = estimate_boid(
                    x,
                    fs=100.0,
                    embedding_lag=args.embedding_lag,
                    finite_sample_correction=args.c_n,
                    fmin=1.0,
                    fmax=40.0,
                )
                rows.append({
                    "true_m": m,
                    "noise_sigma": sigma,
                    "replicate": rep,
                    "boid": result.boid,
                    "estimated_rank": result.rank,
                    "lz76_normalized": float(np.mean([
                        normalized_lz76(ch) for ch in x
                    ])),
                    "spectral_entropy": spectral_entropy(x, fs=100.0),
                })

    df = pd.DataFrame(rows)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.output, index=False)

    print(df.groupby(["true_m", "noise_sigma"])[
        ["boid", "lz76_normalized", "spectral_entropy"]
    ].median())
    print("\nSaved:", args.output)


if __name__ == "__main__":
    main()
