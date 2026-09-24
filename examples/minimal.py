"""Minimal BOID example on a synthetic two-channel oscillator mixture."""

import numpy as np
from boid import estimate_boid

fs = 100.0
t = np.arange(400) / fs
x = np.vstack([
    np.sin(2 * np.pi * 8.0 * t) + 0.7 * np.sin(2 * np.pi * 17.0 * t + 0.2),
    0.8 * np.sin(2 * np.pi * 8.0 * t + 0.4) + np.sin(2 * np.pi * 17.0 * t),
])

result = estimate_boid(
    x,
    fs=fs,
    embedding_lag=40,
    finite_sample_correction=0.0,
    fmin=1.0,
    fmax=40.0,
)

print("BOID:", result.boid)
print("frequencies_hz:", result.frequencies_hz)
