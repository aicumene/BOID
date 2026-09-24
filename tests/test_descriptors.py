import numpy as np

from boid.descriptors import (
    hankel_participation_ratio,
    hankel_entropy_rank,
    stable_rank,
)


def test_singular_spectrum_descriptors():
    s = np.array([4.0, 2.0, 1.0])
    assert hankel_participation_ratio(s) > 1.0
    assert hankel_entropy_rank(s) > 1.0
    assert stable_rank(s) > 1.0
