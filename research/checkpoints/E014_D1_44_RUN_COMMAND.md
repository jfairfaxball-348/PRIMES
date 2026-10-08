# E014 D1-44 — exact OBS-020 I2=1 H14 one-shot replication command

**Purpose:** Freeze only the previously committed identical OBS-020 I2=1 H14 criterion and two-call guard before any H14 prime query; never reopen D14 or authorize A14.

**Exact pre-generation implementation/test Git commit:** `6d5bd2d374d98fb0751b69b15bcb2a005b7f0dea`.

**Independently byte-verified Git blobs before generation:**
- Frozen D14 mathematical primitives, unchanged `experiments/E014_primitive_three_cube_incidence_shapes.py`: `736789b92043b96366815c9a4ed24c882ca5718d`.
- H14 target-specific evaluator/guard `experiments/E014_h14_primitive_three_cube_replication.py`: `dc3b87291e314a738d67979cfa1b23e613623158`.
- H14 synthetic/poison tests `tests/test_e014_h14.py`: `46b7e56488a588a344f249b6838e38e7a5fdb1b7`.

**Exact complete runnable command** (run from repo root twice, identical source and same output path):

```bash
PYTHONPATH=src:. python experiments/E014_h14_primitive_three_cube_replication.py --implementation-commit 6d5bd2d374d98fb0751b69b15bcb2a005b7f0dea --output research/evidence/E014_H14_replication.json
```

Only two ordered generator calls per run: whole-prefix low `[0,8945)` then directly segmented H14 `[79_000_000,80_000_000)`. The full positive allowlist is checked before any generator entry and again at boundaries. There is no other high prefix, phase, auxiliary sieve, primality, guard, historical range, E005 calibration, A13, A14, D14, D13 or H13 generation. All source/test bytes, pinned Git hash, exact output path and complete command remain fixed on both runs. Seal first raw artifact; repeat complete command and compare all bytes and SHA-256 prior to inspecting a single target field. Invalid narrow target-only canonical JSON or any of nine nonzero validation counters fails closed. Then apply OBS-020's already committed I2=1 criterion once, with no fallback or mining.

**Pre-generation validation:** metadata 330/330 disjoint; focused H14 tests 5/5 passed using only fabricated labels and poison generators; Python compilation passed; Ruff unavailable locally (not claimed passed). Exact source/test and frozen dependency independently remote-byte-verified prior to this command checkpoint. The command checkpoint itself must be separately Git-committed and remotely byte-verified before execution.
