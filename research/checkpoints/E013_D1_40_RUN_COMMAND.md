# E013 D1-40 immutable H13 pre-generation command

Frozen authority: `experiments/E013_MODULAR_QUADRATIC_ORBIT_SHAPES.md`; frozen observations OBS-018/O1=3 and OBS-019/O2=2 in `research/OBSERVATION_LEDGER.md`. D13 remains closed and unchanged.

Exact final H13 source/test checkpoint: `153c2bc814b847b195237a80608f29911daa8bd0`.

Verified byte-identical against locally tested files: `experiments/E013_h13_replication.py` Git blob `bb77515e90bec124a94f17c75f6cfa614cf9c689`; `tests/test_e013_h13.py` Git blob `4ff8d7116c5b3400e197ea52b9411bd65cd655e3`.

Pre-generation validation on the exact files: 5/5 focused pytest tests passed, Python compilation passed, 305 interval metadata comparisons checked; targeted Ruff unavailable locally under existing FAIL-001/FAIL-002 tooling limitation. Poison-generator negatives rejected before generator entry; no generator was reached by a negative plan. No H13 generator was run before this exact checkpoint and command commit.

From the repository root, execute this **identical complete command twice**, same source/test checkpoint and same output path; record first-run bytes separately, then compare complete bytes and SHA-256 **before viewing any H13 criterion field**:

```bash
PYTHONPATH=.:src python experiments/E013_h13_replication.py --phase H13 --code-commit 153c2bc814b847b195237a80608f29911daa8bd0 --output /tmp/e013-h13.json
```

The complete exact ordered prime generation plan, authorized before either generator, is whole-prefix low support `[0,8661)` followed only by directly segmented `H13=[74_000_000,75_000_000)`. All other high intervals and helper primality calls are forbidden, including A13, both G13 guards, D13 and historical protected/calibration bands. Output may contain only frozen population, validation, target-specific two-family gate aggregates and exact mechanical statuses. Never generate or inspect A13.
