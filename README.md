# lab-mini

[![CI](https://github.com/JustinJLeopard/lab-mini/actions/workflows/ci.yml/badge.svg)](https://github.com/JustinJLeopard/lab-mini/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Minimal reference for repeatable data-science labbing: load, profile, analyze, claim, report.

`lab-mini` is the small research loop behind the bigger agent-infrastructure
work: make the dataset shape explicit, make claims reproducible, and render the
result as a report that another session can inspect.

## What It Proves

- A lab run should produce a claim artifact, not just notebook state.
- Profiling comes before analysis so downstream claims know their data shape.
- Deterministic seeds and fixture-backed tests keep the loop repeatable.
- The same pattern works as a lightweight evaluation harness for agent behavior.

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

## Related

- [JustAi](https://github.com/JustinJLeopard/JustAi) — orchestration control plane.
- [safe-mini](https://github.com/JustinJLeopard/safe-mini) — safe local execution substrate.
- [memory-mini](https://github.com/JustinJLeopard/memory-mini) — durable agent memory reference.
