from __future__ import annotations

import math
from typing import Any

import pandas as pd

from lab_mini.types import ColumnProfile, DatasetProfile


def _clean_float(value: Any) -> float | str | None:
    if pd.isna(value):
        return None
    if hasattr(value, "isoformat"):
        return str(value)
    try:
        result = float(value)
    except (TypeError, ValueError):
        return str(value)
    return None if math.isnan(result) else result


def column_distribution(series: pd.Series) -> dict[str, float | str | None]:
    clean = series.dropna()
    if clean.empty:
        return {"min": None, "p50": None, "p95": None, "max": None, "mean": None, "std": None}
    if pd.api.types.is_numeric_dtype(clean):
        quantiles = clean.quantile([0.5, 0.95])
        return {
            "min": _clean_float(clean.min()),
            "p50": _clean_float(quantiles.loc[0.5]),
            "p95": _clean_float(quantiles.loc[0.95]),
            "max": _clean_float(clean.max()),
            "mean": _clean_float(clean.mean()),
            "std": _clean_float(clean.std(ddof=1)),
        }
    if pd.api.types.is_datetime64_any_dtype(clean):
        ordered = clean.sort_values()
        return {
            "min": _clean_float(ordered.iloc[0]),
            "p50": _clean_float(ordered.quantile(0.5)),
            "p95": _clean_float(ordered.quantile(0.95)),
            "max": _clean_float(ordered.iloc[-1]),
            "mean": None,
            "std": None,
        }
    return {"min": None, "p50": None, "p95": None, "max": None, "mean": None, "std": None}


def profile_column(frame: pd.DataFrame, column: str) -> ColumnProfile:
    series = frame[column]
    row_count = len(series)
    null_count = int(series.isna().sum())
    null_rate = 0.0 if row_count == 0 else null_count / row_count
    return ColumnProfile(
        name=column,
        dtype=str(series.dtype),
        null_rate=null_rate,
        non_null_count=row_count - null_count,
        unique_count=int(series.nunique(dropna=True)),
        stats=column_distribution(series),
    )


def profile(frame: pd.DataFrame) -> DatasetProfile:
    return DatasetProfile(
        row_count=len(frame),
        column_count=len(frame.columns),
        duplicate_rows=int(frame.duplicated().sum()) if len(frame.columns) else 0,
        columns=[profile_column(frame, str(column)) for column in frame.columns],
    )


def null_rates(frame: pd.DataFrame) -> dict[str, float]:
    if frame.empty:
        return {str(column): 0.0 for column in frame.columns}
    return {str(column): float(rate) for column, rate in frame.isna().mean().items()}


def dtype_inventory(frame: pd.DataFrame) -> dict[str, str]:
    return {str(column): str(dtype) for column, dtype in frame.dtypes.items()}
