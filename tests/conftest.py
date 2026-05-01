from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest


@pytest.fixture
def sample_path() -> Path:
    return Path(__file__).parent / "_fixtures" / "sample_lab.csv"


@pytest.fixture
def sample_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "date": pd.date_range("2026-01-01", periods=5, freq="D"),
            "group": ["A", "A", "B", "B", "B"],
            "value": [10.0, 12.0, 19.0, 21.0, 20.0],
            "score": [0.2, 0.3, 0.55, 0.6, 0.65],
            "label": ["baseline", "baseline", "treatment", "treatment", "treatment"],
        }
    )
