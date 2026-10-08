# E019 D1-58 / SQ-022 — immutable complete H19 one-shot command

**Purpose:** fixed already-observed OBS-024 B1 integer target 2 only. This is the separately committed and remote-verified complete actual H19 command. No new target, no D19 replay, no guards, A19, earlier bands or calibration access. Execute only after full remote source/test verification and independent synthetic/poison validation.

**Pre-generator complete source/test commit:** `3f0b8c0ec83a28aed426ace73298bdb19ddc5c2e`; the full source and test Git blobs were individually remotely fetched and independently Git-SHA1 checked.

**Working directory:** repository root.

**Entire pinned invocation, identical both times on the same output pathname:**

```bash
PYTHONPATH=.:src python experiments/E019_H19_fixed_two_row_ladder_spanning_forest.py --band H19 --code-commit 3f0b8c0ec83a28aed426ace73298bdb19ddc5c2e --output /tmp/e019-h19.json
```

**Exact prevalidated ordered positive generator calls EACH invocation:**
1. `(base_sieve_support, 0, 10100, whole_prefix)` where `isqrt(101_999_999)=10099`.
2. `(segmented_target, 101_000_000, 102_000_000, direct_segmented)` exactly once.

Preflight must reject every 89 historical named and 30 nested calibration intervals, all five E019 role collisions (including consumed D19), guard, A19, D18/H18, unauthorized off-phase, whole-high-prefix, split, extra, reordered, altered low support/target, per-anchor/indirect helper plan BEFORE either generator.

After first complete invocation save complete output as uninterpreted raw bytes and its SHA-256, execute the identical complete command again, and establish complete raw-file byte cmp plus SHA-256 match before inspecting descriptive aggregate. Then independently validate exact canonical typed ten-key schema, mandatory ten zero validators, frozen target 2 strict unique four-state prime mode and ALL originally frozen floors, signed controls, mixed classes and singleton-support/cap. One failed gate REFUTES with no repair. The pinned command is not executed by writing this file.
