from __future__ import annotations

from html import escape
from pathlib import Path

from lab_mini.claim import Claim


def render_markdown(claims: list[Claim], *, title: str = "Lab Mini Report") -> str:
    lines = [
        f"# {title}",
        "",
        "| Statement | Estimate | CI | Method | n | Confidence |",
        "| --- | ---: | ---: | --- | ---: | ---: |",
    ]
    for claim in claims:
        lines.append(
            "| "
            f"{claim.statement} | "
            f"{claim.point_estimate:.6g} | "
            f"[{claim.ci_low:.6g}, {claim.ci_high:.6g}] | "
            f"{claim.method} | "
            f"{claim.n} | "
            f"{claim.confidence:.1%} |"
        )
    lines.append("")
    return "\n".join(lines)


def render_html(claims: list[Claim], *, title: str = "Lab Mini Report") -> str:
    rows = "\n".join(
        "<tr>"
        f"<td>{escape(claim.statement)}</td>"
        f"<td>{claim.point_estimate:.6g}</td>"
        f"<td>[{claim.ci_low:.6g}, {claim.ci_high:.6g}]</td>"
        f"<td>{escape(claim.method)}</td>"
        f"<td>{claim.n}</td>"
        f"<td>{claim.confidence:.1%}</td>"
        "</tr>"
        for claim in claims
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{escape(title)}</title>
  <style>
    body {{ font-family: system-ui, sans-serif; margin: 2rem; line-height: 1.4; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ border: 1px solid #ddd; padding: 0.5rem; text-align: left; }}
    th {{ background: #f5f5f5; }}
  </style>
</head>
<body>
  <h1>{escape(title)}</h1>
  <table>
    <thead>
      <tr><th>Statement</th><th>Estimate</th><th>CI</th><th>Method</th><th>n</th><th>Confidence</th></tr>
    </thead>
    <tbody>
{rows}
    </tbody>
  </table>
</body>
</html>
"""


def write_markdown(
    claims: list[Claim], path: str | Path, *, title: str = "Lab Mini Report"
) -> Path:
    destination = Path(path)
    destination.write_text(render_markdown(claims, title=title), encoding="utf-8")
    return destination


def write_html(claims: list[Claim], path: str | Path, *, title: str = "Lab Mini Report") -> Path:
    destination = Path(path)
    destination.write_text(render_html(claims, title=title), encoding="utf-8")
    return destination
