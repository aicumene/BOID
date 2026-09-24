from __future__ import annotations

import numpy as np
from scipy.signal import periodogram


def lz76_phrase_count(binary: np.ndarray) -> int:
    s = "".join("1" if int(v) else "0" for v in np.asarray(binary).ravel())
    n = len(s)
    if n == 0:
        return 0

    i, l, k, k_max, c = 0, 1, 1, 1, 1
    while True:
        if i + k >= n or l + k >= n:
            c += 1
            break
        if s[i + k - 1] == s[l + k - 1]:
            k += 1
            if l + k > n:
                c += 1
                break
        else:
            if k > k_max:
                k_max = k
            i += 1
            if i == l:
                c += 1
                l += k_max
                if l + 1 > n:
                    break
                i, k, k_max = 0, 1, 1
            else:
                k = 1
    return c


def normalized_lz76(x: np.ndarray) -> float:
    """Median-binarized normalized LZ76.

    The normalization c(n) log2(n) / n is an explicit implementation choice.
    """
    x = np.asarray(x, dtype=float).ravel()
    if x.size < 2:
        return float("nan")
    b = x > np.median(x)
    c = lz76_phrase_count(b)
    return float(c * np.log2(x.size) / x.size)


def spectral_entropy(
    x: np.ndarray,
    fs: float,
    fmin: float = 0.5,
    fmax: float = 40.0,
    normalize: bool = True,
) -> float:
    x = np.asarray(x, dtype=float)
    if x.ndim == 1:
        x = x[None, :]

    values = []
    for channel in x:
        f, pxx = periodogram(channel, fs=fs, detrend="constant")
        mask = (f >= fmin) & (f <= fmax)
        p = pxx[mask]
        if p.size == 0 or np.sum(p) <= 0:
            continue
        p = p / np.sum(p)
        p = p[p > 0]
        h = -np.sum(p * np.log(p))
        if normalize and p.size > 1:
            h /= np.log(p.size)
        values.append(h)

    return float(np.mean(values)) if values else float("nan")
