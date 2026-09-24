from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from scipy.stats import pearsonr


def corr(df, a, b):
    r, p = pearsonr(df[a], df[b])
    return float(r), float(p)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("csv", type=Path)
    args = p.parse_args()

    df = pd.read_csv(args.csv)

    for label, cols in {
        "BOID vs true oscillator count": ("boid", "true_m"),
        "LZ76 vs noise sigma": ("lz76_normalized", "noise_sigma"),
        "LZ76 vs true oscillator count": ("lz76_normalized", "true_m"),
        "spectral entropy vs true oscillator count": (
            "spectral_entropy", "true_m"
        ),
    }.items():
        r, pval = corr(df, *cols)
        print(f"{label}: r={r:.3f}, p={pval:.3g}")


if __name__ == "__main__":
    main()
