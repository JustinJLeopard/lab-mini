from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from typing import Any, Protocol, TypeAlias

import pandas as pd

DataFrame: TypeAlias = pd.DataFrame
Series: TypeAlias = pd.Series
SchemaValidator: TypeAlias = Callable[[pd.DataFrame], pd.DataFrame | None]


class SupportsFrame(Protocol):
    def to_pandas(self) -> pd.DataFrame: ...


@dataclass(frozen=True)
class ColumnProfile:
    name: str
    dtype: str
    null_rate: float
    non_null_count: int
    unique_count: int
    stats: Mapping[str, float | str | None]


@dataclass(frozen=True)
class DatasetProfile:
    row_count: int
    column_count: int
    duplicate_rows: int
    columns: Sequence[ColumnProfile]


JsonDict: TypeAlias = dict[str, Any]
