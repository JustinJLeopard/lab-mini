# lab-mini

[![CI](https://github.com/JustinJLeopard/lab-mini/actions/workflows/ci.yml/badge.svg)](https://github.com/JustinJLeopard/lab-mini/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Minimal reference for repeatable data-science labbing: load, profile, analyze, claim, report.

## Install

```bash
pip install git+https://github.com/JustinJLeopard/lab-mini.git
```

For local development:

```bash
pip install -e '.[dev]'
```

## 30-second example

```python
from lab_mini import claim_mean, load_csv, profile, render_markdown

frame = load_csv("tests/_fixtures/sample_lab.csv")
dataset_profile = profile(frame)
claim = claim_mean(frame, "value", seed=42)

print(dataset_profile.row_count)
print(render_markdown([claim]))
```

See [docs/USAGE.md](docs/USAGE.md) for the full loop.

