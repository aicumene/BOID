from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import kruskal, mannwhitneyu, wilcoxon, friedmanchisquare
from sklearn.metrics import roc_auc_score


def subject_level_median(
    table: pd.DataFrame,
    group_cols: list[str],
    value_cols: list[str],
) -> pd.DataFrame:
    return (
        table.groupby(group_cols, dropna=False)[value_cols]
        .median()
        .reset_index()
    )


def zscore_within_group(
    table: pd.DataFrame,
    group_col: str,
    columns: list[str],
) -> pd.DataFrame:
    out = table.copy()
    for col in columns:
        out[col + "_z"] = out.groupby(group_col)[col].transform(
            lambda s: (s-s.mean())/s.std(ddof=0) if s.std(ddof=0) > 0 else 0.0
        )
    return out


def pmpi(
    table: pd.DataFrame,
    timepoint_col: str,
    mode_count_col: str,
    hf_fraction_col: str,
    burst_col: str,
    mode_entropy_col: str,
) -> pd.Series:
    cols = [mode_count_col, hf_fraction_col, burst_col, mode_entropy_col]
    z = zscore_within_group(table, timepoint_col, cols)
    return sum(z[c + "_z"] for c in cols)


def auc_for_poor_outcome(y_poor, score) -> float:
    return float(roc_auc_score(np.asarray(y_poor).astype(int), np.asarray(score)))


def kruskal_by_group(values, groups):
    frame = pd.DataFrame({"value": values, "group": groups}).dropna()
    arrays = [g["value"].to_numpy() for _, g in frame.groupby("group")]
    return kruskal(*arrays)


def mann_whitney(a, b, alternative="two-sided"):
    return mannwhitneyu(a, b, alternative=alternative)


def paired_wilcoxon(a, b, alternative="two-sided"):
    return wilcoxon(a, b, alternative=alternative)


def friedman_repeated(*arrays):
    return friedmanchisquare(*arrays)
