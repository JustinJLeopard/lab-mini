from __future__ import annotations

import numpy as np
import pandas as pd


def numeric_frame(frame: pd.DataFrame) -> pd.DataFrame:
    return frame.select_dtypes(include=["number"])


def descriptive_stats(frame: pd.DataFrame) -> pd.DataFrame:
    numeric = numeric_frame(frame)
    if numeric.empty:
        return pd.DataFrame()
    return numeric.describe().transpose()


def rolling_trend(
    frame: pd.DataFrame,
    column: str,
    *,
    window: int = 3,
    method: str = "mean",
) -> pd.Series:
    if window < 1:
        raise ValueError("window must be >= 1")
    series = pd.to_numeric(frame[column], errors="coerce")
    rolling = series.rolling(window=window, min_periods=1)
    if method == "mean":
        return rolling.mean()
    if method == "median":
        return rolling.median()
    raise ValueError("method must be 'mean' or 'median'")


def iqr_outliers(frame: pd.DataFrame, column: str, *, multiplier: float = 1.5) -> pd.Series:
    series = pd.to_numeric(frame[column], errors="coerce")
    clean = series.dropna()
    if clean.empty:
        return pd.Series(False, index=frame.index, dtype=bool)
    q1 = float(clean.quantile(0.25))
    q3 = float(clean.quantile(0.75))
    iqr = q3 - q1
    lower = q1 - multiplier * iqr
    upper = q3 + multiplier * iqr
    return ((series < lower) | (series > upper)).fillna(False)


def zscore_outliers(frame: pd.DataFrame, column: str, *, threshold: float = 3.0) -> pd.Series:
    series = pd.to_numeric(frame[column], errors="coerce")
    mean = series.mean(skipna=True)
    std = series.std(skipna=True, ddof=0)
    if pd.isna(std) or float(std) == 0.0:
        return pd.Series(False, index=frame.index, dtype=bool)
    zscores = (series - mean) / std
    return (zscores.abs() > threshold).fillna(False)


def outlier_flags(
    frame: pd.DataFrame,
    column: str,
    *,
    z_threshold: float = 3.0,
    iqr_multiplier: float = 1.5,
) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "iqr": iqr_outliers(frame, column, multiplier=iqr_multiplier),
            "z_score": zscore_outliers(frame, column, threshold=z_threshold),
        },
        index=frame.index,
    )


def correlation_matrix(frame: pd.DataFrame, *, method: str = "pearson") -> pd.DataFrame:
    numeric = numeric_frame(frame)
    if numeric.empty:
        return pd.DataFrame()
    return numeric.corr(method=method)


def mean_difference(frame: pd.DataFrame, value: str, group: str, *, baseline: object) -> float:
    values = pd.to_numeric(frame[value], errors="coerce")
    groups = frame[group]
    baseline_values = values[groups == baseline].dropna()
    comparison_values = values[groups != baseline].dropna()
    if baseline_values.empty or comparison_values.empty:
        raise ValueError("both baseline and comparison groups need numeric observations")
    return float(comparison_values.mean() - baseline_values.mean())


def finite_values(frame: pd.DataFrame, column: str) -> np.ndarray:
    values = pd.to_numeric(frame[column], errors="coerce").to_numpy(dtype=float)
    return values[np.isfinite(values)]
