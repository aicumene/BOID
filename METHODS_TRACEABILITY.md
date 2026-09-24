# Methods traceability

This document separates manuscript-specified analysis choices from numerical or implementation details that are not yet fixed explicitly in the current manuscript.

## Explicitly specified

### Preprocessing

- EEG channels only.
- Band-pass: **0.5–40 Hz**.
- Resample to **100 Hz** where needed.
- Mouse recordings remain at the supplied **128 Hz**.
- Non-overlapping windows.
- **4 s** windows for oscillator/frequency analyses.
- **30 s** windows for sleep singular-spectrum descriptors.
- Flat or non-finite channels are excluded.
- Non-finite / near-zero-variance windows are skipped.
- Window-level descriptors are aggregated to recording-, subject-, or patient-level medians.

### BOID

- multichannel block-Hankel embedding;
- MSSA signal-subspace estimation;
- self-calibrated MP/Bai–Yin ε-rank threshold;
- TLS-ESPRIT pole extraction;
- BOID = number of recovered **positive-frequency poles in 1–40 Hz**.

### Synthetic construct-validity experiment

- oscillator count `m ∈ {3, 12}`;
- random frequencies in **2–40 Hz**;
- random amplitudes and phases;
- additive white noise `σ ∈ {0.3, 1.5}` relative to a unit-variance signal;
- **40 realizations per cell**;
- comparison with normalized LZ76 and spectral entropy.

### Discriminative-subspace classifier

- classifier embedding lag is explicitly **L = 12**;
- rank `r` and discriminant dimension `k` are tuned;
- class mean projectors are compared through a signed projector difference.

## Not numerically specified in the current manuscript

The repository does not silently invent the following final-paper parameters:

1. general BOID embedding lag `L`;
2. finite-sample correction `c_n` in the MP/Bai–Yin threshold;
3. exact filter family/order and edge handling;
4. exact definition of “near-zero variance”;
5. exact mode-amplitude fitting routine;
6. exact LZ76 normalization convention;
7. exact synthetic amplitude/spatial-weight distributions and random seed.

These choices are exposed in code/configuration.

## 4-s versus 30-s sleep representation

The Methods specify 4-s windows for oscillator analyses, whereas the sleep figure description refers to BOID values on a 30-s sleep-stage grid.

The current sleep pipeline therefore:

1. computes BOID on non-overlapping 4-s windows;
2. assigns each 4-s window to the concurrent sleep stage;
3. reports an optional 30-s display/scoring table as the median of 4-s BOID values assigned to each 30-s epoch.

This convention should remain documented in the final paper/code release.

## MSSA ownership

Block-Hankel construction, MSSA decomposition and generic rank estimation are implemented in the separate canonical repository:

https://github.com/aicumene/MSSA

This BOID repository should not duplicate those modules.
