# Usage

This example uses the bundled CSV fixture at `tests/_fixtures/sample_lab.csv`.

## Load

```python
from pathlib import Path

from lab_mini import load_csv, require_columns

path = Path("tests/_fixtures/sample_lab.csv")
frame = load_csv(path, schema=require_columns(["date", "group", "value", "score"]))
```

## Profile

```python
from lab_mini import profile

dataset_profile = profile(frame)
print(dataset_profile.row_count)
print(dataset_profile.columns[0])
```

## Analyze

```python
from lab_mini import correlation_matrix, outlier_flags, rolling_trend

trend = rolling_trend(frame, "value", window=3)
outliers = outlier_flags(frame, "value")
correlations = correlation_matrix(frame)
```

## Claim

```python
from lab_mini import claim_group_difference, claim_mean

claims = [
    claim_mean(frame, "value", n_resamples=500, seed=42),
    claim_group_difference(frame, "value", "group", baseline="A", n_resamples=500, seed=42),
]
```

## Report

```python
from lab_mini import write_html, write_markdown

write_markdown(claims, "/tmp/lab_mini_demo_report.md")
write_html(claims, "/tmp/lab_mini_demo_report.html")
```

Run the same flow from the command line:

```bash
python examples/demo.py
```

