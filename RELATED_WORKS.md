# Related methodological work

## Primary BOID work

Alexandra Bernadotte, Ivan Menshikov.  
**Brain Oscillator Intrinsic Dimension marks consciousness, recovery mode, and failed downshifting in coma.**  
AiCumene. Preprint. 2026.  
https://research.aicumene.com/papers/boid-coma/  
DOI: 10.13140/RG.2.2.31610.25288

## Theoretical foundation of BOID

Alexandra Bernadotte.  
**Topology-driven classification of time series.**  
bioRxiv, 2026.  
DOI: 10.64898/2026.04.25.720787  
https://doi.org/10.64898/2026.04.25.720787

**Theorem 1 and Eqs. (24)–(26)** provide the theoretical dimensionality law
underlying BOID. For a structured time series

$$g(t)=\sum_{i=1}^{k_1} a_i e^{\alpha_i t}+\sum_{j=1}^{k_2} b_j\sin(\omega_j t+\phi_j)+\sum_{\ell=1}^{k_3} c_\ell e^{\lambda_\ell t}\sin(\nu_\ell t+\psi_\ell)$$

the associated delay-embedding trajectory satisfies $K_{g(t)}\subset L$ and

$$\dim L\le k_1+2k_2+2k_3$$

Under generic non-degeneracy conditions, equality holds. Thus real exponential
components contribute one dimension, while harmonic and exponentially modulated
oscillatory components contribute two-dimensional invariant planes. This
component-to-dimension relation is the theoretical basis for recovering
oscillator dimensionality from a Hankel signal subspace.

For BOID, this law is used as a theoretical foundation rather than as the
empirical estimator itself: measured-data BOID is defined by retained
positive-frequency TLS-ESPRIT poles within the selected analysis band.

## MSSA mathematical layer

Alexandra Bernadotte, Ivan Menshikov.  
**Multichannel Singular Spectrum Analysis.**  
AiCumene. Preprint. 2026.  
https://research.aicumene.com/papers/MSSA/

## Foundational precursor

Alexandra Bernadotte, Victor Buchstaber.  
**Method for evaluating the number of signal sources and application to non-invasive brain-computer interface.**  
arXiv:2410.11844 (2024).  
DOI: 10.48550/arXiv.2410.11844

This work develops the Hankel-embedding/source-counting line that precedes the BOID formulation.

## Applied / engineering continuation

Alexandra Bernadotte.  
**Estimating the Number of Sources in EEG with Hankel Embedding for Brain-Computer Interface.**  
ICARA 2026.  
DOI: 10.1109/ICARA69401.2026.11480398

Ivan Menshikov, Nikolai Elfimov, Alexandra Bernadotte.  
**A Lightweight Hankel-Embedded Pipeline for Real-Time EEG Filtering and Classification.**  
ICARA 2026.  
DOI: 10.1109/ICARA69401.2026.11480292

## Foundational methods

Nina Golyandina, Vladimir Nekrutkin, Anatoly Zhigljavsky.  
**Analysis of Time Series Structure: SSA and Related Techniques.**  
Chapman & Hall/CRC, 2001.

Nina Golyandina, Anatoly Zhigljavsky.  
**Singular Spectrum Analysis for Time Series.**  
Springer Briefs in Statistics, 2013 (2nd ed. 2020).

Victor M. Buchstaber.  
**Time series analysis and Grassmannians.**  
Amer. Math. Soc. Transl. 162, 1–17 (1994).

Richard Roy, Thomas Kailath.  
**ESPRIT — estimation of signal parameters via rotational invariance techniques.**  
IEEE Trans. Acoust. Speech Signal Process. 37, 984–995 (1989).  
DOI: 10.1109/29.32276
