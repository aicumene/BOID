import numpy as np

from boid.research.subspace_classifier import BernadotteSubspaceClassifier


def make_signal(freq, phase, fs=100.0, n=400):
    t = np.arange(n) / fs
    return np.vstack([
        np.sin(2*np.pi*freq*t + phase),
        0.8*np.sin(2*np.pi*freq*t + phase + 0.3),
    ])


def test_subspace_classifier_runs():
    rec = []
    y = []

    for i in range(6):
        rec.append(make_signal(8.0, i*0.1))
        y.append(0)
        rec.append(make_signal(18.0, i*0.1))
        y.append(1)

    clf = BernadotteSubspaceClassifier(
        rank=2,
        k=2,
        embedding_lag=12,
    )
    clf.fit(rec, np.asarray(y))
    scores = clf.decision_function(rec)

    assert scores.shape == (12,)
    assert np.all(np.isfinite(scores))
