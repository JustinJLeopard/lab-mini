from __future__ import annotations

import lab_mini


def test_public_api_exports_claim() -> None:
    assert "Claim" in lab_mini.__all__


def test_public_api_exports_pipeline_functions() -> None:
    for name in ["load_csv", "profile", "descriptive_stats", "claim_mean", "render_markdown"]:
        assert name in lab_mini.__all__
