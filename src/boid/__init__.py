"""Bernadotte Oscillator Intrinsic Dimension (BOID).

BOID estimates the number of resolved positive-frequency oscillatory modes
inside a statistically significant MSSA signal subspace. Generic block-Hankel,
MSSA, reconstruction, and rank-estimation routines are provided by the separate
AiCumene MSSA package: https://github.com/aicumene/MSSA
"""

from .estimator import BOIDResult, estimate_boid
from .esprit import tls_esprit
from .poles import (
    pole_frequency_hz,
    pole_damping_per_second,
    select_positive_frequency_poles,
)
from .descriptors import weighted_frequency_summary
from .regulation import StateBOIDSummary, summarize_boid_by_state, median_boid_shift
from .theory import (
    bernadotte_dimension_bound,
    bernadotte_dimension_generic,
    oscillator_count_from_ideal_dimension,
)
from .geometry import grassmann_geodesic_distance, grassmann_projection_distance

__all__ = [
    "BOIDResult",
    "estimate_boid",
    "tls_esprit",
    "pole_frequency_hz",
    "pole_damping_per_second",
    "select_positive_frequency_poles",
    "weighted_frequency_summary",
    "StateBOIDSummary",
    "summarize_boid_by_state",
    "median_boid_shift",
    "bernadotte_dimension_bound",
    "bernadotte_dimension_generic",
    "oscillator_count_from_ideal_dimension",
    "grassmann_geodesic_distance",
    "grassmann_projection_distance",
]

__version__ = "0.3.0"
