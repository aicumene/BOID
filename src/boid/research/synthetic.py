from __future__ import annotations

import numpy as np


def generate_exposinusoidal_signal(
    n_oscillators: int,
    fs: float = 100.0,
    duration_seconds: float = 4.0,
    n_channels: int = 2,
    fmin: float = 2.0,
    fmax: float = 40.0,
    noise_sigma: float = 0.3,
    rng: np.random.Generator | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """Generate a finite multichannel oscillator mixture.

    Exact amplitude/spatial-weight distributions are implementation choices;
    the article specifies random frequencies, amplitudes and phases.
    """
    rng = rng or np.random.default_rng()
    n = int(round(fs * duration_seconds))
    t = np.arange(n) / fs

    frequencies = np.sort(rng.uniform(fmin, fmax, size=n_oscillators))
    phases = rng.uniform(0, 2*np.pi, size=n_oscillators)
    amplitudes = rng.uniform(0.5, 1.5, size=(n_channels, n_oscillators))

    clean = np.zeros((n_channels, n), dtype=float)
    for j, (f, phase) in enumerate(zip(frequencies, phases)):
        base = np.sin(2*np.pi*f*t + phase)
        clean += amplitudes[:, [j]] * base[None, :]

    clean = clean / np.std(clean)
    noisy = clean + rng.normal(0.0, noise_sigma, size=clean.shape)
    return noisy, frequencies
