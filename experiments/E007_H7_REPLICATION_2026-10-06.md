# E007 H7 Replication — 2026-10-06

**Stage:** replication  
**Queue item:** SQ-007  
**Related task:** D1-21 / SQ-007  
**Frozen specification:** `experiments/E007_NEIGHBOUR_FACTORIZATION_COUPLING.md`  
**Frozen discovery evidence:** `experiments/E007_D7_DISCOVERY_2026-10-06.md` and `research/evidence/E007_D7_discovery.json`  
**Status:** COMPLETE — OBS-010 AND OBS-011 REPLICATED; A7 UNTOUCHED

This record documents the one-shot H7 replication of the two frozen E007 observations only. D7 remains frozen historical discovery evidence. E001/E002/E003/E004/E006 were not rerun or mined, SQ-005 remained quarantined, and no calibration object or historical-unblinding mechanism was used to interpret H7.

## Frozen implementation integrity

Before H7 generation, the current evaluator and focused-test bytes were checked against implementation/test checkpoint `ad09ec3d72dc291d4930f13d9954a5a155590574`.

- evaluator: `experiments/E007_neighbour_factorization_coupling.py`
- evaluator Git blob: `e81601ac9d557c94273b21885b675cf8a502cc60`
- focused tests: `tests/test_e007.py`
- focused-test Git blob: `657aabd557d8cd2434907f03ded2d07b4b1ecd1a`
- core Git blob: `ee600508452e1036f52d00fb9c0b22844c646601`
- project-config Git blob: `dc4f15f98caf407eaaddd1506e1c323c5c2efbff`

The current bytes matched the frozen checkpoint exactly. The common-anchor semantics, thin/thick normalization, exact odd factorization, F1-F4 definitions, exact enrichment arithmetic, support floors, duplicate rule, deterministic ordering/serialization, and fail-closed generation guard were unchanged.

## H7 generation-plan validation

Before any H7 prime generation, the complete plan was validated:

~~~json
[
  {"purpose":"base_sieve_support","start":0,"stop":7000,"strategy":"whole_prefix"},
  {"purpose":"segmented_target","start":48000000,"stop":49000000,"strategy":"segmented"}
]
~~~

The low prefix is exactly `[0,7000)`, sufficient through `floor(sqrt(48,999,999)) = 6,999`, and lies inside historically safe generated support below 100,000. The only high-value generation interval is H7=`[48_000_000,49_000_000)`.

Thirty deliberate invalid plans were rejected before any prime-generator call. They covered high whole-prefix generation, short/long low support, partial and expanded H7, G7-pre, D7, G7-mid, A7, A1, H3, H4, G6-mid, A3, A4, A6, every E003/E004 guard/target, historical novelty bands, and another non-target high interval.

## Validation before H7 generation

Validation on the exact frozen bytes completed before the first H7 run:

~~~text
PYTHONPATH=src pytest -q tests/test_e007.py
22 passed

python -m compileall -q src experiments tests
success

ruff --version
command not found
~~~

Ruff absence and detached-runner GitHub DNS failure are recurrences of the existing FAIL-001/FAIL-002 environment limitations, not new repository failures. GitHub combined-status and PR-triggered workflow-run collections were empty for both checkpoint `ad09ec3d72dc291d4930f13d9954a5a155590574` and the D1-20 head `3a0e07d55f1272ed052797368fd78160296db9b7`; this reuses FAIL-002 and is not treated as CI pass/fail evidence.

## Deterministic H7 artifact

Exact command:

~~~bash
PYTHONPATH=src python experiments/E007_neighbour_factorization_coupling.py --band H7 --code-commit ad09ec3d72dc291d4930f13d9954a5a155590574 --output /tmp/e007-h7.json
~~~

The identical complete command was executed twice, with the same output path, before any criterion result was inspected. The outputs were byte-identical.

- bytes: 450,687
- SHA-256: `6a25381c7430a6e720e619fb27696ec75e8696514d72a8f7a26398f616d85ced`
- compact criterion evidence: `research/evidence/E007_H7_replication.json`

No descriptive H7 scan was performed after generation. Only the required anchor populations and the two predeclared F2/F3 same-target replication criteria were inspected. F1/F4 H7 results were not inspected for promotion, no per-anchor prime/factor catalog was exposed, and no new H7 signature was sought.

## Frozen criterion results

H7 contains 56,387 prime anchors and 443,612 odd-composite control anchors, so both frozen population floors pass.

| Observation | Family | Frozen target | H7 target prime count | Highest competitor | H7 target composite count | Exact enrichment numerator | Result |
|---|---|---|---:|---|---:|---:|---|
| OBS-010 | F2 | `[3,3]` | 7,917 | `[3,2]`: 6,404 | 52,339 | 560,837,011 | REPLICATED |
| OBS-011 | F3 | `[3,3]` | 5,106 | `[3,2]`: 3,977 | 38,940 | 69,373,092 | REPLICATED |

For OBS-010, exact F2 target `[3,3]` remains the strict unique H7 prime-anchor mode, its count is above 32, and

`7,917*443,612 - 52,339*56,387 = 560,837,011 > 0`.

For OBS-011, exact F3 target `[3,3]` remains the strict unique H7 prime-anchor mode, its count is above 32, and

`5,106*443,612 - 38,940*56,387 = 69,373,092 > 0`.

Both frozen criteria therefore succeed without tuning. No fallback target, threshold change, alternative family, normalization, factorization rule, or ranking change was used.

## Preserved ranges and stop rule

This unit generated no high-value primes outside H7. G7-pre=`[45_000_000,46_000_000)`, G7-mid=`[47_000_000,48_000_000)`, and A7=`[92_000_000,93_000_000)` were not generated in D1-21. A1, H3, H4, G6-mid, A3, A4, A6, every E003/E004 guard, and all historical novelty bands retained their frozen historical roles and were not generated or inspected in this unit.

D1-21 stops at this replication checkpoint. No candidate was created, no candidate synthesis or mechanism/proof/adversarial work was performed, and no prior-art/collision/literature search or H7 pattern mining occurred.

Because OBS-010 and OBS-011 both survived the untouched holdout, the next bounded unit is D1-22 / SQ-007 candidate-synthesis triage over these two replicated observations only, using committed D7+H7 evidence and no new prime generation or A7 execution.
