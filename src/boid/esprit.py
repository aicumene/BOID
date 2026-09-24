"""TLS-ESPRIT pole extraction used by BOID."""

from __future__ import annotations

import numpy as np


def tls_esprit(signal_subspace: np.ndarray, n_channels: int) -> np.ndarray:
    """Recover ESPRIT poles from a block-Hankel MSSA signal subspace.

    Parameters
    ----------
    signal_subspace
        Leading left-singular/eigenvector basis of the block-Hankel trajectory,
        with shape ``(n_channels * embedding_length, rank)``.
    n_channels
        Number of channels in the original multichannel signal.

    Returns
    -------
    numpy.ndarray
        Complex eigenvalues of the estimated shift operator.
    """
    U = np.asarray(signal_subspace)
    if U.ndim != 2:
        raise ValueError("signal_subspace must be 2D.")

    c = int(n_channels)
    r = U.shape[1]
    if c <= 0:
        raise ValueError("n_channels must be positive.")
    if U.shape[0] <= c:
        raise ValueError("At least two lag blocks are required for ESPRIT.")
    if r == 0:
        return np.array([], dtype=complex)

    # With MSSA rows stacked by lag-block, dropping one channel block at each
    # end gives the two shift-related subspaces.
    U_first = U[:-c, :]
    U_second = U[c:, :]

    if U_first.shape[0] < r:
        raise ValueError(
            f"ESPRIT is underdetermined: shifted row count {U_first.shape[0]} "
            f"is smaller than rank {r}. Increase the embedding length."
        )

    # TLS solution of U_second ≈ U_first Phi.
    Z = np.hstack([U_first, U_second])
    _, _, Vh = np.linalg.svd(Z, full_matrices=False)
    V = Vh.conj().T
    V_small = V[:, -r:]
    V12 = V_small[:r, :]
    V22 = V_small[r:, :]
    Phi = -V12 @ np.linalg.pinv(V22)
    return np.linalg.eigvals(Phi)
