from __future__ import annotations

from dataclasses import dataclass
import numpy as np
from aicumene_mssa import MSSA


def signal_subspace(
    x: np.ndarray,
    rank: int,
    embedding_lag: int,
    delay_samples: int = 1,
) -> np.ndarray:
    model = MSSA(
        window_length=embedding_lag,
        delay_samples=delay_samples,
    ).fit(x)
    return model.signal_subspace(rank)


def projector(U: np.ndarray) -> np.ndarray:
    U = np.asarray(U)
    return U @ U.T.conj()


@dataclass
class BernadotteSubspaceClassifier:
    """Binary discriminative-subspace classifier used in the BOID manuscript.

    The manuscript evaluates this classifier with embedding_lag=12; the value
    remains explicit at construction time in user code when a different
    application is intended.
    """
    rank: int
    k: int
    embedding_lag: int = 12
    delay_samples: int = 1

    class_a_: object | None = None
    class_b_: object | None = None
    delta_k_: np.ndarray | None = None

    def fit(self, recordings: list[np.ndarray], labels: np.ndarray):
        labels = np.asarray(labels)
        classes = np.unique(labels)
        if len(classes) != 2:
            raise ValueError("Classifier requires exactly two classes.")

        self.class_a_, self.class_b_ = classes[0], classes[1]

        subspaces = [
            signal_subspace(
                x,
                rank=self.rank,
                embedding_lag=self.embedding_lag,
                delay_samples=self.delay_samples,
            )
            for x in recordings
        ]
        proj = [projector(U) for U in subspaces]

        Pa = np.mean([P for P, y in zip(proj, labels) if y == self.class_a_], axis=0)
        Pb = np.mean([P for P, y in zip(proj, labels) if y == self.class_b_], axis=0)
        delta = Pa - Pb

        evals, evecs = np.linalg.eigh(delta)
        order = np.argsort(np.abs(evals))[::-1][:self.k]
        W = evecs[:, order]
        lam = evals[order]
        self.delta_k_ = (W * lam) @ W.T.conj()
        return self

    def decision_function(self, recordings: list[np.ndarray]) -> np.ndarray:
        if self.delta_k_ is None:
            raise RuntimeError("fit must be called first.")

        scores = []
        for x in recordings:
            U = signal_subspace(
                x,
                rank=self.rank,
                embedding_lag=self.embedding_lag,
                delay_samples=self.delay_samples,
            )
            scores.append(np.trace(U.T.conj() @ self.delta_k_ @ U).real)
        return np.asarray(scores)

    def predict(self, recordings: list[np.ndarray]) -> np.ndarray:
        scores = self.decision_function(recordings)
        return np.where(scores >= 0, self.class_a_, self.class_b_)
