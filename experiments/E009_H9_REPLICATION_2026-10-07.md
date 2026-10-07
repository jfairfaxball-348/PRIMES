# E009 H9 Replication — 2026-10-07

**Stage:** replication  
**Queue item:** SQ-009  
**Related task:** D1-27 / SQ-009  
**Frozen specification:** `experiments/E009_UNIT_ACTION_COVER_SHAPES.md`  
**Frozen discovery evidence:** `experiments/E009_D9_DISCOVERY_2026-10-07.md` and `research/evidence/E009_D9_discovery.json`  
**Status:** COMPLETE — OBS-012 AND OBS-013 REPLICATED; A9 UNTOUCHED

This record documents the one-shot H9 replication of the two frozen E009 observations only. D9 remains frozen historical discovery evidence. C1 was not reconsidered, C3 remained duplicate-suppressed, no H9 pattern was promoted, and no calibration object or historical-unblinding mechanism was used to interpret or retune E009.

## Frozen implementation integrity

The final D1-26 E009 evaluator/runtime and focused-test bytes were verified before H9 generation against checkpoint `52f295f46ce8225f195f9e772dd7462a0dd873a1`.

- evaluator: `experiments/E009_unit_action_cover_shapes.py`
- evaluator Git blob: `b377d352569519b7c1c55fe1eaa46d3412ddf82b`
- runtime: `experiments/E009_unit_action_cover_shapes_runtime.py`
- runtime Git blob: `860c906baa5ece6583400ae6f5d9568dd6b07cd3`
- focused tests: `tests/test_e009.py`
- focused-test Git blob: `a05a3d9ab9a2e1ff070388dbb08c10c4c94170e4`
- runtime tests: `tests/test_e009_runtime.py`
- runtime-test Git blob: `1f5ebba2eb5ea08594b7ef740d9e1ab1a9d10e5d`
- unchanged core Git blob: `ee600508452e1036f52d00fb9c0b22844c646601`

Q=210, ordered basis A=(2,3,5,7), exact factorization/Lambda/order semantics, canonical subset ordering, cover/minimal-antichain semantics, C1-C4 definitions, controls, floors, enrichment rule, duplicate suppression, descriptive allowlist, serialization, and both frozen H9 targets were unchanged.

## Validation before H9 generation

Validation on exact reconstructed committed bytes:

```text
PYTHONPATH=.:src pytest -q tests/test_e009.py tests/test_e009_runtime.py
22 passed

python -m compileall -q src experiments tests
success
```

Before any H9 prime generator call, the complete canonical plan was constructed and validated:

```json
[
  {"purpose":"base_sieve_support","strategy":"whole_prefix","start":0,"stop":7550},
  {"purpose":"segmented_target","strategy":"segmented","start":56000000,"stop":57000000}
]
```

The low prefix is exactly `[0,7550)`, sufficient through `floor(sqrt(56,999,999)) = 7,549`; the only high-value generation interval is H9=`[56_000_000,57_000_000)`. Fifty-three deliberate invalid plans were rejected before the prime generator was called. These covered short/expanded/shifted low support, high whole-prefix generation, partial/expanded/shifted/split H9, D9, G9-pre/G9-mid, A9, H8/A8, A1/H3/H4/G6-mid/A3/A4/A6/G7-pre/G7-mid/A7/G8-pre/G8-mid, every E003/E004 guard, every historical generated novelty band, all six E005 maximum calibration segments, and an arbitrary other non-target high interval.

## Deterministic H9 artifact

Exact command:

```bash
PYTHONPATH=.:src python experiments/E009_unit_action_cover_shapes_runtime.py --band H9 --code-commit 52f295f46ce8225f195f9e772dd7462a0dd873a1 --output /mnt/data/e009-h9.json
```

The identical complete command was executed twice with the same arguments and output path before any replication criterion was inspected. The outputs were byte-identical.

- bytes: 85,386
- SHA-256: `9fccccd71c49983870e226f6f03ab80bff60820874edc2fe09cfbc6fdd361126`
- H9 Q-admissible anchors: 228,571
- H9 prime anchors `N_P`: 56,105
- H9 composite controls `N_C`: 172,466
- first H9 prime: 56,000,003
- last H9 prime: 56,999,989
- all eight frozen runtime validation-failure aggregates: zero
- compact criterion evidence: `research/evidence/E009_H9_replication.json`

After byte determinism was established, inspection was restricted to the two precommitted target signatures, their target counts, highest competing prime-frequency counts, target composite counts, and exact enrichment numerators. No competing signature value, per-anchor factorization, Lambda value, order vector, subset-lcm table, cover table, modular-power witness, non-mode enrichment scan, or new H9 target was inspected or promoted.

## Frozen criterion results

| Observation | Family | Frozen target | H9 target prime count | Highest competing prime count | H9 target composite count | Exact enrichment numerator | Result |
|---|---|---|---:|---:|---:|---:|---|
| OBS-012 | C2 | `[2,0,0,0]` | 13,900 | 11,411 | 35,726 | 392,870,170 | REPLICATED |
| OBS-013 | C4 | `[]` | 3,869 | 3,089 | 5,075 | 382,538,079 | REPLICATED |

For both observations, `N_P>=1000`, `N_C>=1000`, target count is at least 32, the target has strictly greater H9 prime frequency than every competitor, and the exact enrichment numerator is strictly positive. Both therefore satisfy their unchanged one-shot H9 criteria exactly.

No fallback, retargeting, target mutation, new observation allocation, or H9 discovery mining occurred.

## Preserved ranges and stop rule

This unit generated no high-value primes outside H9. D9 remains discovery-consumed historical evidence. G9-pre=`[53_000_000,54_000_000)` and G9-mid=`[55_000_000,56_000_000)` remain ungenerated non-target guards. A9=`[108_000_000,109_000_000)` remains frozen, untouched, uninspected, and unexecuted. H8/A8 and every historical reserve/holdout/guard retain their prior protected roles.

D1-27 stops at this replication checkpoint. No candidate synthesis, candidate creation, mechanism/proof/adversarial work, prior-art/collision search, literature search, novelty claim, calibration-object transfer, or protected-range inspection occurred.

The next bounded unit is D1-28 / SQ-009 synthesis-only candidate triage over replicated OBS-012 and OBS-013, using only committed D9+H9 evidence and no new prime generation. A9 remains untouched during that triage.
