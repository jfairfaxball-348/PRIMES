# E019 D1-57 / SQ-021 — immutable complete D19 run command

**Checkpoint purpose:** exact D19 discovery invocation pinned after actual source and synthetic/poison test commit `ff95798e52d9288714b5b9549da1c51ada88218d`. This document is a separate pre-generator Git commit. It does not authorize H19, A19, guards, historical ranges, calibration or any other scan.

**Run directory:** repository root. The command below is the **entire** pinned command line, run exactly twice, unchanged, on the same output pathname:

```bash
PYTHONPATH=.:src python experiments/E019_two_row_ladder_spanning_forest_boundary_shapes.py --band D19 --code-commit ff95798e52d9288714b5b9549da1c51ada88218d --output /tmp/e019-d19.json
```

**Complete ordered positive generator plan inside the pinned evaluator, per invocation (prevalidated before either generator):**
1. `(base_sieve_support, 0, 10000, whole_prefix)`, exact `isqrt(99_999_999)=9999` and exclusive endpoint 10000.
2. `(segmented_target, 99_000_000, 100_000_000, direct_segmented)` — only D19.

The implementation independently checks all **89** distinct historical named intervals, six E005 calibration maxima and **30** nested E005 ranges, all five frozen E019 roles and exact positive-plan equality. High whole-prefix, shifted, split, extra, reordered, off-phase, indirect-helper, guard, reserve and malformed plans fail before low/high generation.

**Reproducibility order:** complete first run; preserve first output as uninterpreted raw bytes and its SHA-256; run precisely the same command a second time writing the exact same `/tmp/e019-d19.json`; compare complete raw bytes and both whole-file SHA-256 digests before any descriptive field inspection. Only then validate the strict narrow ten-key canonical typed payload, zero counters and frozen B1 singleton promotion gate. No per-anchor serialization.

**No execution or observational result is contained in this pre-generator command checkpoint.**
