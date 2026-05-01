from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
from typing import Any

import pandas as pd

from lab_mini.types import SchemaValidator


def require_columns(columns: Sequence[str]) -> SchemaValidator:
    expected = tuple(columns)

    def validate(frame: pd.DataFrame) -> pd.DataFrame:
        missing = [column for column in expected if column not in frame.columns]
        if missing:
            raise ValueError(f"missing required columns: {', '.join(missing)}")
        return frame

    return validate


def apply_schema(frame: pd.DataFrame, schema: SchemaValidator | None = None) -> pd.DataFrame:
    if schema is None:
        return frame
    validated = schema(frame)
    return frame if validated is None else validated


def load_csv(
    path: str | Path, schema: SchemaValidator | None = None, **kwargs: Any
) -> pd.DataFrame:
    return apply_schema(pd.read_csv(path, **kwargs), schema)


def load_parquet(
    path: str | Path, schema: SchemaValidator | None = None, **kwargs: Any
) -> pd.DataFrame:
    return apply_schema(pd.read_parquet(path, **kwargs), schema)


def load_json(
    path: str | Path, schema: SchemaValidator | None = None, **kwargs: Any
) -> pd.DataFrame:
    return apply_schema(pd.read_json(path, **kwargs), schema)


def load_table(
    path: str | Path, schema: SchemaValidator | None = None, **kwargs: Any
) -> pd.DataFrame:
    source = Path(path)
    suffix = source.suffix.lower()
    if suffix == ".csv":
        return load_csv(source, schema=schema, **kwargs)
    if suffix in {".parquet", ".pq"}:
        return load_parquet(source, schema=schema, **kwargs)
    if suffix in {".json", ".jsonl", ".ndjson"}:
        return load_json(source, schema=schema, **kwargs)
    raise ValueError(f"unsupported table format: {suffix or '<none>'}")
