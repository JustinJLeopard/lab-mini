from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

import numpy as np
import pandas as pd

from lab_mini.analyzer import finite_values, mean_difference
from lab_mini.types import JsonDict


@dataclass(frozen=True)
class Claim:
    statement: str
    point_estimate: float
    ci_low: float
    ci_high: float
    method: str
    n: int
    confidence: float

    def to_dict(self) -> JsonDict:
        return asdict(self)

    @classmethod
    def from_dict(cls, payload: JsonDict) -> Claim:
        return cls(
            statement=str(payload["statement"]),
            point_estimate=float(payload["point_estimate"]),
            ci_low=float(payload["ci_low"]),
            ci_high=float(payload["ci_high"]),
            method=str(payload["method"]),
            n=int(payload["n"]),
            confidence=float(payload["confidence"]),
        )


def confidence_interval(values: np.ndarray, confidence: float) -> tuple[float, float]:
    if values.size == 0:
        raise ValueError("cannot build a confidence interval from no values")
    if not 0.0 < confidence < 1.0:
        raise ValueError("confidence must be between 0 and 1")
    alpha = 1.0 - confidence
    low, high = np.quantile(values, [alpha / 2.0, 1.0 - alpha / 2.0])
    return float(low), float(high)


def bootstrap_statistic(
    values: np.ndarray,
    *,
    statistic: str = "mean",
    n_resamples: int = 1_000,
    seed: int | None = None,
) -> np.ndarray:
    clean = values[np.isfinite(values)]
    if clean.size == 0:
        raise ValueError("cannot bootstrap an empty sample")
    if n_resamples < 1:
        raise ValueError("n_resamples must be >= 1")
    rng = np.random.default_rng(seed)
    samples = rng.choice(clean, size=(n_resamples, clean.size), replace=True)
    if statistic == "mean":
        return samples.mean(axis=1)
    if statistic == "median":
        return np.median(samples, axis=1)
    raise ValueError("statistic must be 'mean' or 'median'")


def claim_mean(
    frame: pd.DataFrame,
    column: str,
    *,
    confidence: float = 0.95,
    n_resamples: int = 1_000,
    seed: int | None = None,
) -> Claim:
    values = finite_values(frame, column)
    if values.size == 0:
        raise ValueError(f"{column} has no finite numeric observations")
    bootstrap = bootstrap_statistic(values, n_resamples=n_resamples, seed=seed)
    ci_low, ci_high = confidence_interval(bootstrap, confidence)
    point = float(values.mean())
    return Claim(
        statement=f"Mean {column} is {point:.3f}",
        point_estimate=point,
        ci_low=ci_low,
        ci_high=ci_high,
        method="bootstrap mean",
        n=int(values.size),
        confidence=confidence,
    )


def claim_median(
    frame: pd.DataFrame,
    column: str,
    *,
    confidence: float = 0.95,
    n_resamples: int = 1_000,
    seed: int | None = None,
) -> Claim:
    values = finite_values(frame, column)
    if values.size == 0:
        raise ValueError(f"{column} has no finite numeric observations")
    bootstrap = bootstrap_statistic(values, statistic="median", n_resamples=n_resamples, seed=seed)
    ci_low, ci_high = confidence_interval(bootstrap, confidence)
    point = float(np.median(values))
    return Claim(
        statement=f"Median {column} is {point:.3f}",
        point_estimate=point,
        ci_low=ci_low,
        ci_high=ci_high,
        method="bootstrap median",
        n=int(values.size),
        confidence=confidence,
    )


def claim_group_difference(
    frame: pd.DataFrame,
    value: str,
    group: str,
    *,
    baseline: Any,
    confidence: float = 0.95,
    n_resamples: int = 1_000,
    seed: int | None = None,
) -> Claim:
    point = mean_difference(frame, value, group, baseline=baseline)
    values = pd.to_numeric(frame[value], errors="coerce")
    groups = frame[group]
    baseline_values = values[groups == baseline].dropna().to_numpy(dtype=float)
    comparison_values = values[groups != baseline].dropna().to_numpy(dtype=float)
    if baseline_values.size == 0 or comparison_values.size == 0:
        raise ValueError("both baseline and comparison groups need numeric observations")
    rng = np.random.default_rng(seed)
    estimates = np.empty(n_resamples, dtype=float)
    for index in range(n_resamples):
        baseline_sample = rng.choice(baseline_values, size=baseline_values.size, replace=True)
        comparison_sample = rng.choice(comparison_values, size=comparison_values.size, replace=True)
        estimates[index] = comparison_sample.mean() - baseline_sample.mean()
    ci_low, ci_high = confidence_interval(estimates, confidence)
    return Claim(
        statement=f"Mean {value} differs by {point:.3f} versus {baseline}",
        point_estimate=point,
        ci_low=ci_low,
        ci_high=ci_high,
        method="bootstrap mean difference",
        n=int(baseline_values.size + comparison_values.size),
        confidence=confidence,
    )
