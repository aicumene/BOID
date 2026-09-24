# BOID repository architecture

## AiCumene MSSA — generic numerical layer

Canonical repository (to be published separately):

https://github.com/aicumene/MSSA

MSSA owns the generic numerical operations shared across applications:

- block-Hankel embedding;
- lagged-scatter / MSSA decomposition;
- MP / Bai–Yin signal-rank estimation;
- signal-subspace extraction;
- grouped reconstruction and singular-spectrum diagnostics.

BOID imports those operations as a dependency. It does **not** maintain a second
copy of `hankel.py`, `mssa.py`, or `rank.py`.

## BOID — oscillator-dimensionality layer

This repository owns:

- TLS-ESPRIT shift-operator estimation;
- conversion of poles to frequency and damping;
- positive-frequency pole selection inside an application-specific band;
- Bernadotte Oscillator Intrinsic Dimension (BOID);
- oscillator-family descriptors;
- theoretical dimensionality-law helpers;
- Grassmannian signal-subspace geometry;
- discriminative-subspace classifier;
- synthetic validation and neuroscience application workflows.

The dependency boundary is intentional:

```text
aicumene/MSSA
    block-Hankel -> MSSA -> MP/Bai-Yin rank -> signal subspace
                         |
                         v
aicumene/BOID
    TLS-ESPRIT -> positive-frequency poles -> BOID
                         |
                         +-> organization descriptors / geometry / applications
```

## Dataset

The AiCumene EEG-BCI Sleep-Wake Dataset is a separate research object on Zenodo:

DOI: 10.5281/zenodo.22923070

Data archives should not duplicate the MSSA or BOID implementations.


## Python package layout

```text
src/boid/
├── esprit.py
├── poles.py
├── estimator.py
├── descriptors.py
├── regulation.py
├── theory.py
├── geometry.py
├── preprocessing.py
├── applications/
│   ├── neuroscience.py
│   └── sleep.py
└── research/
    ├── complexity.py
    ├── intrinsic_dimension.py
    ├── topology.py
    ├── subspace_classifier.py
    ├── statistics.py
    └── synthetic.py
```

Only the first layer is the general BOID method. `applications/` contains
domain-specific conventions, while `research/` contains manuscript-analysis
utilities that are not part of the minimal estimator contract.

## Dataset boundary

The BOID core is dataset-agnostic. The **AiCumene EEG-BCI Sleep–Wake Dataset**
(DOI: `10.5281/zenodo.22923070`) is connected only through the neuroscience/sleep
application layer.

The dataset is organized into two components: a public synthetic-data component,
and recordings acquired with AiCumene neurointerface devices that are available
to qualified researchers upon request. The companion dataset repository is
`https://github.com/aicumene/aicumene-eeg-bci-sleep-wake-dataset`.

```text
dataset
  ├── synthetic validation data
  └── AiCumene-device recordings (upon request)
          ↓
boid.applications.neuroscience / boid.applications.sleep
          ↓
aicumene/MSSA
          ↓
BOID core
```

