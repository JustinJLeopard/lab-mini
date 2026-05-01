from __future__ import annotations

from lab_mini import Claim, render_html, render_markdown, write_html, write_markdown


def _claims() -> list[Claim]:
    return [Claim("Mean value is 2.000", 2.0, 1.0, 3.0, "bootstrap mean", 3, 0.95)]


def test_render_markdown_structure() -> None:
    markdown = render_markdown(_claims(), title="Demo")
    assert markdown.startswith("# Demo")
    assert "| Statement | Estimate | CI | Method | n | Confidence |" in markdown


def test_render_markdown_includes_claim() -> None:
    assert "Mean value is 2.000" in render_markdown(_claims())


def test_render_markdown_empty_claims() -> None:
    markdown = render_markdown([])
    assert markdown.count("\n") >= 3


def test_render_html_structure() -> None:
    html = render_html(_claims(), title="Demo")
    assert "<!doctype html>" in html
    assert "<table>" in html


def test_render_html_escapes_text() -> None:
    html = render_html([Claim("<x>", 1.0, 0.0, 2.0, "<m>", 2, 0.9)])
    assert "&lt;x&gt;" in html
    assert "&lt;m&gt;" in html


def test_render_html_empty_claims() -> None:
    assert "<tbody>" in render_html([])


def test_write_markdown(tmp_path) -> None:
    path = write_markdown(_claims(), tmp_path / "report.md")
    assert path.read_text(encoding="utf-8").startswith("# Lab Mini Report")


def test_write_html(tmp_path) -> None:
    path = write_html(_claims(), tmp_path / "report.html")
    assert "<html" in path.read_text(encoding="utf-8")
