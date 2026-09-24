"""Command-line entry points for BOID."""

from __future__ import annotations

import argparse
from pathlib import Path
import numpy as np


def synthetic_main() -> None:
    from .research.synthetic import generate_exposinusoidal_signal
    from .estimator import estimate_boid

    p = argparse.ArgumentParser(description="Run a small synthetic BOID example.")
    p.add_argument("--embedding-lag", type=int, required=True)
    p.add_argument("--c-n", type=float, required=True)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--oscillators", type=int, default=3)
    args = p.parse_args()

    x, truth = generate_exposinusoidal_signal(
        args.oscillators,
        noise_sigma=0.3,
        rng=np.random.default_rng(args.seed),
    )
    result = estimate_boid(
        x,
        fs=100.0,
        embedding_lag=args.embedding_lag,
        finite_sample_correction=args.c_n,
    )
    print("true oscillators:", len(truth))
    print("BOID:", result.boid)
    print("estimated rank:", result.rank)
    print("frequencies_hz:", np.round(result.frequencies_hz, 4))


def sleep_main() -> None:
    # Lazy import keeps core BOID usable without optional MNE/pandas extras.
    from .applications.sleep import compute_sleep_boid

    p = argparse.ArgumentParser(description="Compute BOID from PSG + hypnogram EDF.")
    p.add_argument("--psg", required=True)
    p.add_argument("--hypnogram", required=True)
    p.add_argument("--record-id", required=True)
    p.add_argument("--embedding-lag", type=int, required=True)
    p.add_argument("--c-n", type=float, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()

    windows, epochs = compute_sleep_boid(
        args.psg,
        args.hypnogram,
        record_id=args.record_id,
        embedding_lag=args.embedding_lag,
        finite_sample_correction=args.c_n,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    windows.to_csv(args.output, index=False)
    epoch_path = args.output.with_name(args.output.stem + "_30s.csv")
    epochs.to_csv(epoch_path, index=False)
    print(args.output)
    print(epoch_path)
