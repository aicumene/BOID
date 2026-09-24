import pytest

from boid.theory import (
    bernadotte_dimension_bound,
    bernadotte_dimension_generic,
    oscillator_count_from_ideal_dimension,
)


def test_bernadotte_dimension_law():
    assert bernadotte_dimension_bound(3, 2, 4) == 15
    assert bernadotte_dimension_generic(3, 2, 4) == 15
    assert oscillator_count_from_ideal_dimension(15, n_real_exponentials=3) == 6


def test_ideal_inverse_rejects_incompatible_dimension():
    with pytest.raises(ValueError):
        oscillator_count_from_ideal_dimension(10, n_real_exponentials=1)
