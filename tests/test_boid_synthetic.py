import numpy as np

from boid.research.synthetic import generate_exposinusoidal_signal
from boid.estimator import estimate_boid


def test_boid_returns_modes_on_low_noise_signal():
    rng = np.random.default_rng(7)
    x, _ = generate_exposinusoidal_signal(
        n_oscillators=3,
        fs=100.0,
        duration_seconds=4.0,
        n_channels=2,
        noise_sigma=0.05,
        rng=rng,
    )

    out = estimate_boid(
        x,
        fs=100.0,
        embedding_lag=40,
        finite_sample_correction=0.0,
        fmin=1.0,
        fmax=40.0,
    )

    assert out.boid >= 1
    assert np.all((out.frequencies_hz >= 1.0) & (out.frequencies_hz <= 40.0))
