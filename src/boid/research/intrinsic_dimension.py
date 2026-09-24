from __future__ import annotations

import numpy as np
from scipy.spatial import distance
from scipy.sparse.csgraph import minimum_spanning_tree
from sklearn.neighbors import NearestNeighbors


def levina_bickel_mle(points: np.ndarray, k: int = 10) -> float:
    X = np.asarray(points, dtype=float)
    if X.ndim != 2 or X.shape[0] <= k:
        return float("nan")
    nn = NearestNeighbors(n_neighbors=k + 1).fit(X)
    d, _ = nn.kneighbors(X)
    d = d[:, 1:]
    Tk = np.maximum(d[:, -1], np.finfo(float).tiny)
    ratios = np.log(Tk[:, None] / np.maximum(d[:, :-1], np.finfo(float).tiny))
    local = np.mean(ratios, axis=1) ** -1
    local = local[np.isfinite(local) & (local > 0)]
    return float(np.mean(local)) if local.size else float("nan")


def twonn(points: np.ndarray) -> float:
    X = np.asarray(points, dtype=float)
    if X.ndim != 2 or X.shape[0] < 5:
        return float("nan")
    nn = NearestNeighbors(n_neighbors=3).fit(X)
    d, _ = nn.kneighbors(X)
    r1 = np.maximum(d[:, 1], np.finfo(float).tiny)
    r2 = np.maximum(d[:, 2], r1)
    mu = np.sort(r2 / r1)
    n = len(mu)
    F = (np.arange(1, n + 1) - 0.5) / n
    x = np.log(mu)
    y = -np.log(1.0 - F)
    ok = np.isfinite(x) & np.isfinite(y) & (x > 0)
    if np.sum(ok) < 3:
        return float("nan")
    return float(np.dot(x[ok], y[ok]) / np.dot(x[ok], x[ok]))


def correlation_dimension(points: np.ndarray, max_points: int = 1500) -> float:
    X = np.asarray(points, dtype=float)
    if X.ndim != 2 or X.shape[0] < 20:
        return float("nan")
    if X.shape[0] > max_points:
        idx = np.linspace(0, X.shape[0] - 1, max_points).astype(int)
        X = X[idx]
    d = distance.pdist(X)
    d = d[np.isfinite(d) & (d > 0)]
    if d.size < 20:
        return float("nan")
    lo, hi = np.quantile(d, [0.10, 0.50])
    eps = np.geomspace(lo, hi, 12)
    C = np.array([np.mean(d < e) for e in eps])
    ok = (C > 0) & (C < 1)
    if np.sum(ok) < 3:
        return float("nan")
    slope, _ = np.polyfit(np.log(eps[ok]), np.log(C[ok]), 1)
    return float(slope)


def mst_length(points: np.ndarray, max_points: int = 1000) -> float:
    X = np.asarray(points, dtype=float)
    if X.ndim != 2 or X.shape[0] < 2:
        return float("nan")
    if X.shape[0] > max_points:
        idx = np.linspace(0, X.shape[0] - 1, max_points).astype(int)
        X = X[idx]
    D = distance.squareform(distance.pdist(X))
    tree = minimum_spanning_tree(D)
    return float(tree.sum())


def higuchi_fd_1d(x: np.ndarray, kmax: int = 10) -> float:
    x = np.asarray(x, dtype=float).ravel()
    n = len(x)
    if n < 2*kmax + 1:
        return float("nan")
    L = []
    ks = np.arange(1, kmax + 1)
    for k in ks:
        vals = []
        for m in range(k):
            idx = np.arange(m, n, k)
            if len(idx) < 2:
                continue
            length = np.sum(np.abs(np.diff(x[idx])))
            norm = (n - 1) / ((len(idx) - 1) * k)
            vals.append(length * norm / k)
        L.append(np.mean(vals) if vals else np.nan)
    L = np.asarray(L)
    ok = np.isfinite(L) & (L > 0)
    if np.sum(ok) < 3:
        return float("nan")
    slope, _ = np.polyfit(np.log(1.0/ks[ok]), np.log(L[ok]), 1)
    return float(slope)


def higuchi_fd(x: np.ndarray, kmax: int = 10) -> float:
    x = np.asarray(x, dtype=float)
    if x.ndim == 1:
        return higuchi_fd_1d(x, kmax)
    values = np.asarray([higuchi_fd_1d(ch, kmax) for ch in x], dtype=float)
    return float(np.nanmean(values))
