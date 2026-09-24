"""Theoretical dimensionality relations underlying BOID.

The functions in this module encode Theorem 1 and Eqs. (24)-(26) of:

    Alexandra Bernadotte, "Topology-driven classification of time series",
    bioRxiv (2026), DOI: 10.64898/2026.04.25.720787.

For a structured signal containing k1 real exponential components, k2 harmonic
components, and k3 exponentially modulated oscillatory components, the Hankel
trajectory lies in a subspace L with

    dim(L) <= k1 + 2*k2 + 2*k3.

Under generic non-degeneracy conditions equality holds. This law is a
THEORETICAL foundation of BOID; empirical BOID is not defined as rank/2.
"""

from __future__ import annotations


def _nonnegative_int(value: int, name: str) -> int:
    value = int(value)
    if value < 0:
        raise ValueError(f"{name} must be non-negative.")
    return value


def bernadotte_dimension_bound(
    n_real_exponentials: int,
    n_harmonic: int,
    n_exponentially_modulated: int,
) -> int:
    """Upper bound from the Bernadotte geometric-invariance theorem.

    Returns k1 + 2*k2 + 2*k3.
    """
    k1 = _nonnegative_int(n_real_exponentials, "n_real_exponentials")
    k2 = _nonnegative_int(n_harmonic, "n_harmonic")
    k3 = _nonnegative_int(
        n_exponentially_modulated, "n_exponentially_modulated"
    )
    return k1 + 2 * k2 + 2 * k3


def bernadotte_dimension_generic(
    n_real_exponentials: int,
    n_harmonic: int,
    n_exponentially_modulated: int,
) -> int:
    """Generic ideal dimension when all theorem directions are independent.

    Under the non-degeneracy conditions of the theorem, the upper bound is
    attained, so this equals the corresponding ideal Hankel-subspace dimension.
    """
    return bernadotte_dimension_bound(
        n_real_exponentials,
        n_harmonic,
        n_exponentially_modulated,
    )


def oscillator_count_from_ideal_dimension(
    dimension: int,
    n_real_exponentials: int = 0,
) -> int:
    """Recover ideal oscillator count from the generic dimension law.

    This helper applies only to the ideal finite-component model:

        dimension = k1 + 2*m_osc.

    It is deliberately NOT used by :func:`boid.estimate_boid`, which counts
    retained positive-frequency TLS-ESPRIT poles directly.
    """
    dim = _nonnegative_int(dimension, "dimension")
    k1 = _nonnegative_int(n_real_exponentials, "n_real_exponentials")
    residual = dim - k1
    if residual < 0:
        raise ValueError("dimension cannot be smaller than n_real_exponentials.")
    if residual % 2:
        raise ValueError(
            "dimension - n_real_exponentials must be even under the ideal law."
        )
    return residual // 2
