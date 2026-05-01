from __future__ import annotations

from pathlib import Path

from lab_mini import claim_group_difference, claim_mean, load_csv, profile, render_html, render_markdown


def main() -> None:
    fixture = Path(__file__).resolve().parents[1] / "tests" / "_fixtures" / "sample_lab.csv"
    frame = load_csv(fixture)
    dataset_profile = profile(frame)
    claims = [
        claim_mean(frame, "value", n_resamples=500, seed=42),
        claim_group_difference(frame, "value", "group", baseline="A", n_resamples=500, seed=42),
    ]

    markdown = render_markdown(claims, title=f"Lab Mini Demo ({dataset_profile.row_count} rows)")
    html = render_html(claims, title="Lab Mini Demo")
    Path("/tmp/lab_mini_demo_report.md").write_text(markdown, encoding="utf-8")
    Path("/tmp/lab_mini_demo_report.html").write_text(html, encoding="utf-8")


if __name__ == "__main__":
    main()

