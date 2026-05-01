from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from lab_mini import (
    Claim,
    bootstrap_statistic,
    claim_group_difference,
    claim_mean,
    claim_median,
    confidence_interval,
)


def test_claim_serialization_round_trip() -> None:
    claim = Claim("x", 1.0, 0.5, 1.5, "method", 10, 0.95)
    assert Claim.from_dict(claim.to_dict()) == claim


def test_confidence_interval_rejects_empty() -> None:
    with pytest.raises(ValueError, match="no values"):
        confidence_interval(np.array([]), 0.95)


def test_confidence_interval_rejects_bad_confidence() -> None:
    with pytest.raises(ValueError, match="between"):
        confidence_interval(np.array([1.0]), 1.0)


def test_confidence_interval_quantiles() -> None:
    assert confidence_interval(np.array([0.0, 10.0]), 0.8) == pytest.approx((1.0, 9.0))


def test_bootstrap_statistic_seeded_is_deterministic() -> None:
    values = np.array([1.0, 2.0, 3.0])
    first = bootstrap_statistic(values, n_resamples=5, seed=7)
    second = bootstrap_statistic(values, n_resamples=5, seed=7)
    assert first.tolist() == second.tolist()


def test_bootstrap_statistic_median() -> None:
    result = bootstrap_statistic(np.array([1.0, 5.0]), statistic="median", n_resamples=3, seed=1)
    assert result.shape == (3,)


def test_bootstrap_statistic_rejects_empty() -> None:
    with pytest.raises(ValueError, match="empty"):
        bootstrap_statistic(np.array([float("nan")]))


def test_bootstrap_statistic_rejects_bad_resamples() -> None:
    with pytest.raises(ValueError, match="n_resamples"):
        bootstrap_statistic(np.array([1.0]), n_resamples=0)


def test_bootstrap_statistic_rejects_bad_statistic() -> None:
    with pytest.raises(ValueError, match="statistic"):
        bootstrap_statistic(np.array([1.0]), statistic="sum")


def test_claim_mean(sample_frame) -> None:
    claim = claim_mean(sample_frame, "value", n_resamples=100, seed=3)
    assert claim.n == 5
    assert claim.ci_low <= claim.point_estimate <= claim.ci_high


def test_claim_mean_rejects_no_numeric() -> None:
    with pytest.raises(ValueError, match="no finite"):
        claim_mean(pd.DataFrame({"x": ["bad"]}), "x")


def test_claim_median(sample_frame) -> None:
    claim = claim_median(sample_frame, "value", n_resamples=100, seed=3)
    assert claim.point_estimate == 19.0


def test_claim_median_rejects_no_numeric() -> None:
    with pytest.raises(ValueError, match="no finite"):
        claim_median(pd.DataFrame({"x": [None]}), "x")


def test_claim_group_difference(sample_frame) -> None:
    claim = claim_group_difference(
        sample_frame, "value", "group", baseline="A", n_resamples=100, seed=3
    )
    assert claim.point_estimate == pytest.approx(9.0)


def test_claim_group_difference_rejects_missing_group() -> None:
    with pytest.raises(ValueError, match="both baseline"):
        claim_group_difference(
            pd.DataFrame({"value": [1], "group": ["A"]}), "value", "group", baseline="A"
        )
