from __future__ import annotations

import pandas as pd
import pytest

from lab_mini import (
    correlation_matrix,
    descriptive_stats,
    finite_values,
    iqr_outliers,
    mean_difference,
    numeric_frame,
    outlier_flags,
    rolling_trend,
    zscore_outliers,
)


def test_numeric_frame_selects_numbers(sample_frame) -> None:
    assert list(numeric_frame(sample_frame).columns) == ["value", "score"]


def test_descriptive_stats_has_mean(sample_frame) -> None:
    assert descriptive_stats(sample_frame).loc["value", "mean"] == pytest.approx(16.4)


def test_descriptive_stats_no_numeric_returns_empty() -> None:
    assert descriptive_stats(pd.DataFrame({"x": ["a"]})).empty


def test_rolling_trend_mean(sample_frame) -> None:
    assert rolling_trend(sample_frame, "value", window=2).iloc[-1] == 20.5


def test_rolling_trend_median(sample_frame) -> None:
    assert rolling_trend(sample_frame, "value", window=2, method="median").iloc[-1] == 20.5


def test_rolling_trend_rejects_bad_window(sample_frame) -> None:
    with pytest.raises(ValueError, match="window"):
        rolling_trend(sample_frame, "value", window=0)


def test_rolling_trend_rejects_bad_method(sample_frame) -> None:
    with pytest.raises(ValueError, match="method"):
        rolling_trend(sample_frame, "value", method="sum")


def test_iqr_outliers_flags_extreme_value() -> None:
    frame = pd.DataFrame({"x": [1, 2, 3, 100]})
    assert bool(iqr_outliers(frame, "x").iloc[-1])


def test_iqr_outliers_empty_numeric() -> None:
    assert not iqr_outliers(pd.DataFrame({"x": [None]}), "x").any()


def test_zscore_outliers_flags_extreme_value() -> None:
    frame = pd.DataFrame({"x": [1, 1, 1, 1, 10]})
    assert bool(zscore_outliers(frame, "x", threshold=1.5).iloc[-1])


def test_zscore_outliers_constant_series() -> None:
    assert not zscore_outliers(pd.DataFrame({"x": [2, 2, 2]}), "x").any()


def test_outlier_flags_has_both_methods() -> None:
    result = outlier_flags(pd.DataFrame({"x": [1, 2, 100]}), "x", z_threshold=1.0)
    assert list(result.columns) == ["iqr", "z_score"]


def test_correlation_matrix(sample_frame) -> None:
    result = correlation_matrix(sample_frame)
    assert result.loc["value", "score"] > 0.9


def test_correlation_matrix_without_numeric() -> None:
    assert correlation_matrix(pd.DataFrame({"x": ["a"]})).empty


def test_mean_difference(sample_frame) -> None:
    assert mean_difference(sample_frame, "value", "group", baseline="A") == pytest.approx(9.0)


def test_mean_difference_requires_both_groups() -> None:
    with pytest.raises(ValueError, match="both baseline"):
        mean_difference(
            pd.DataFrame({"value": [1], "group": ["A"]}), "value", "group", baseline="A"
        )


def test_finite_values_drops_nan_and_inf() -> None:
    result = finite_values(pd.DataFrame({"x": [1, None, float("inf"), "bad"]}), "x")
    assert result.tolist() == [1.0]
