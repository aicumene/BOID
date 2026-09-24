from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd
import mne

from ..preprocessing import preprocess_eeg, iter_nonoverlapping_windows
from ..estimator import estimate_boid
from ..descriptors import (
    hankel_participation_ratio,
    hankel_entropy_rank,
    stable_rank,
    weighted_frequency_summary,
)

STAGE_MAP = {
    "Sleep stage W": "W",
    "Sleep stage 1": "N1",
    "Sleep stage 2": "N2",
    "Sleep stage 3": "N3",
    "Sleep stage 4": "N3",
    "Sleep stage R": "REM",
    "Sleep stage ?": "?",
    "Movement time": "?",
    "W": "W",
    "N1": "N1",
    "N2": "N2",
    "N3": "N3",
    "REM": "REM",
}


def read_eeg_edf(path: str | Path):
    raw = mne.io.read_raw_edf(str(path), preload=True, verbose="ERROR")

    explicit = [
        i for i, name in enumerate(raw.ch_names)
        if "EEG" in name.upper()
    ]
    picks = np.asarray(explicit, dtype=int)

    if len(picks) == 0:
        picks = mne.pick_types(raw.info, eeg=True, exclude=[])

    if len(picks) == 0:
        raise ValueError("No EEG channels identified.")

    x = raw.get_data(picks=picks)
    names = [raw.ch_names[i] for i in picks]
    return x, float(raw.info["sfreq"]), names


def read_sleep_annotations(path: str | Path) -> pd.DataFrame:
    ann = mne.read_annotations(str(path), verbose="ERROR")
    rows = []
    for onset, duration, desc in zip(ann.onset, ann.duration, ann.description):
        stage = STAGE_MAP.get(str(desc).strip(), "?")
        dur = float(duration) if float(duration) > 0 else 30.0
        rows.append({
            "onset_s": float(onset),
            "duration_s": dur,
            "sleep_stage": stage,
        })
    return pd.DataFrame(rows)


def stage_at_time(annotations: pd.DataFrame, time_s: float) -> str:
    hit = annotations[
        (annotations["onset_s"] <= time_s)
        & (time_s < annotations["onset_s"] + annotations["duration_s"])
    ]
    if hit.empty:
        return "?"
    return str(hit.iloc[-1]["sleep_stage"])


def compute_sleep_boid(
    psg_path: str | Path,
    hypnogram_path: str | Path,
    record_id: str,
    embedding_lag: int,
    finite_sample_correction: float,
    target_fs: float = 100.0,
    window_seconds: float = 4.0,
    delay_samples: int = 1,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    x, fs, _ = read_eeg_edf(psg_path)
    x, fs, _ = preprocess_eeg(x, fs=fs, target_fs=target_fs)
    ann = read_sleep_annotations(hypnogram_path)

    rows = []
    for start, w in iter_nonoverlapping_windows(
        x,
        fs=fs,
        window_seconds=window_seconds,
    ):
        midpoint_s = (start + w.shape[1]/2.0) / fs
        stage = stage_at_time(ann, midpoint_s)
        if stage == "?":
            continue

        result = estimate_boid(
            w,
            fs=fs,
            embedding_lag=embedding_lag,
            finite_sample_correction=finite_sample_correction,
            delay_samples=delay_samples,
            fmin=1.0,
            fmax=40.0,
        )
        summary = weighted_frequency_summary(
            result.frequencies_hz,
            result.mode_power,
        )

        rows.append({
            "record_id": record_id,
            "window_start_s": start/fs,
            "window_mid_s": midpoint_s,
            "sleep_stage": stage,
            "boid": result.boid,
            "signal_rank": result.rank,
            "hankel_participation_ratio": hankel_participation_ratio(
                result.singular_values
            ),
            "hankel_entropy_rank": hankel_entropy_rank(
                result.singular_values
            ),
            "stable_rank": stable_rank(result.singular_values),
            **summary,
        })

    windows = pd.DataFrame(rows)

    if windows.empty:
        return windows, pd.DataFrame()

    # Explicit reconciliation convention for display/scoring epochs:
    # 4-s BOID windows are assigned by midpoint to a 30-s sleep epoch;
    # numeric values are summarized by median within that epoch.
    windows["sleep_epoch_start_s"] = (
        np.floor(windows["window_mid_s"] / 30.0) * 30.0
    )

    numeric = [
        c for c in windows.columns
        if c not in {
            "record_id",
            "sleep_stage",
            "window_start_s",
            "window_mid_s",
            "sleep_epoch_start_s",
        }
    ]

    epochs = (
        windows.groupby(
            ["record_id", "sleep_epoch_start_s", "sleep_stage"],
            as_index=False,
        )[numeric]
        .median()
    )

    return windows, epochs
