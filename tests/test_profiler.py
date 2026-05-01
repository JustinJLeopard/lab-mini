from __future__ import annotations

import pandas as pd

from lab_mini import column_distribution, dtype_inventory, null_rates, profile, profile_column


def test_profile_counts_shape(sample_frame) -> None:
    result = profile(sample_frame)
    assert (result.row_count, result.column_count) == (5, 5)


def test_profile_detects_duplicates(sample_frame) -> None:
    frame = pd.concat([sample_frame, sample_frame.iloc[[0]]], ignore_index=True)
    assert profile(frame).duplicate_rows == 1


def test_profile_empty_frame() -> None:
    result = profile(pd.DataFrame())
    assert result.row_count == 0
    assert result.columns == []


def test_profile_all_null_column() -> None:
    result = profile(pd.DataFrame({"x": [None, None]}))
    assert result.columns[0].null_rate == 1.0
    assert result.columns[0].stats["mean"] is None


def test_profile_mixed_dtypes(sample_frame) -> None:
    result = profile(sample_frame)
    assert {column.name for column in result.columns} == {
        "date",
        "group",
        "value",
        "score",
        "label",
    }


def test_profile_column_numeric_stats(sample_frame) -> None:
    result = profile_column(sample_frame, "value")
    assert result.stats["min"] == 10.0
    assert result.stats["max"] == 21.0


def test_column_distribution_numeric_p95(sample_frame) -> None:
    assert column_distribution(sample_frame["value"])["p95"] > 20.0


def test_column_distribution_datetime() -> None:
    stats = column_distribution(pd.Series(pd.date_range("2026-01-01", periods=3)))
    assert stats["min"] == "2026-01-01 00:00:00"


def test_column_distribution_text_returns_empty_stats() -> None:
    assert column_distribution(pd.Series(["a", "b"]))["mean"] is None


def test_null_rates_empty_with_columns() -> None:
    assert null_rates(pd.DataFrame(columns=["x"])) == {"x": 0.0}


def test_null_rates_regular_frame() -> None:
    assert null_rates(pd.DataFrame({"x": [1, None]})) == {"x": 0.5}


def test_dtype_inventory(sample_frame) -> None:
    assert dtype_inventory(sample_frame)["value"] == "float64"
