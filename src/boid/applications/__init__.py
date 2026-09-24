"""Application-specific BOID workflows."""

from .neuroscience import estimate_eeg_boid
from .sleep import compute_sleep_boid

__all__ = ["estimate_eeg_boid", "compute_sleep_boid"]
