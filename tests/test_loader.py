from __future__ import annotations

import pandas as pd
import pytest

from lab_mini import apply_schema, load_csv, load_json, load_table, require_columns


def test_load_csv_reads_fixture(sample_path) -> None:
    frame = load_csv(sample_path)
    assert list(frame.columns) == ["date", "group", "value", "score", "label"]


def test_load_table_dispatches_csv(sample_path) -> None:
    assert len(load_table(sample_path)) == 5


def test_load_json_reads_records(tmp_path) -> None:
    path = tmp_path / "data.json"
    pd.DataFrame({"a": [1], "b": ["x"]}).to_json(path, orient="records")
    assert load_json(path).to_dict("records") == [{"a": 1, "b": "x"}]


def test_require_columns_accepts_present_columns(sample_frame) -> None:
    schema = require_columns(["value", "group"])
    assert schema(sample_frame).equals(sample_frame)


def test_require_columns_rejects_missing_columns(sample_frame) -> None:
    with pytest.raises(ValueError, match="missing required columns"):
        require_columns(["missing"])(sample_frame)


def test_apply_schema_allows_none_schema(sample_frame) -> None:
    assert apply_schema(sample_frame) is sample_frame


def test_apply_schema_allows_mutating_validator(sample_frame) -> None:
    def schema(frame: pd.DataFrame) -> pd.DataFrame:
        return frame.assign(extra=1)

    assert "extra" in apply_schema(sample_frame, schema)


def test_apply_schema_accepts_validator_returning_none(sample_frame) -> None:
    def schema(frame: pd.DataFrame) -> None:
        assert "value" in frame

    assert apply_schema(sample_frame, schema) is sample_frame


def test_load_table_rejects_unknown_extension(tmp_path) -> None:
    with pytest.raises(ValueError, match="unsupported table format"):
        load_table(tmp_path / "data.txt")


def test_load_csv_with_schema(sample_path) -> None:
    frame = load_csv(sample_path, schema=require_columns(["value"]))
    assert "value" in frame
