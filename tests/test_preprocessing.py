import numpy as np

from boid.preprocessing import iter_nonoverlapping_windows


def test_nonoverlapping_windows():
    x = np.vstack([
        np.linspace(0, 1, 1000),
        np.linspace(1, 2, 1000),
    ])
    windows = list(iter_nonoverlapping_windows(x, fs=100.0, window_seconds=4.0))
    assert len(windows) == 2
    assert windows[0][1].shape == (2, 400)
    assert windows[1][0] == 400
