import numpy as np

from aicumene_mssa import MSSA
from boid.esprit import tls_esprit
from boid.poles import pole_frequency_hz


def test_esprit_recovers_single_frequency_with_known_rank():
    fs = 100.0
    f0 = 12.0
    t = np.arange(400) / fs
    x = np.sin(2*np.pi*f0*t)[None, :]

    model = MSSA(window_length=40).fit(x)
    poles = tls_esprit(model.signal_subspace(2), n_channels=1)
    f = pole_frequency_hz(poles, fs)
    positive = f[f > 0]

    assert len(positive) == 1
    assert abs(positive[0] - f0) < 0.1
