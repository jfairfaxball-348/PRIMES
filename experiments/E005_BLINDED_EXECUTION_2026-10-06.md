# E005 Blinded Calibration Execution — 2026-10-06

**Lane:** historical rediscovery calibration (permanently quarantined from novelty)  
**Queue item:** SQ-005  
**Related task:** D1-12 / SQ-005  
**Frozen specification:** `experiments/E005_PRIME_COUNT_SCALE_CALIBRATION.md`  
**Status:** COMPLETE — PARTIAL_PASS / HISTORICAL THEORY STILL BLINDED

This record documents the exact two-phase execution of the frozen E005 prime-count scale calibration benchmark. No historical mathematical source or mature theory was consulted during this unit. No E001/E002/E003/E004 experiment was rerun or mined, no novelty candidate or observation was created, and A1/H3/A3/H4/A4 remained untouched/uninspected.

## Frozen implementation checkpoint and validation

Evaluator:

- `experiments/E005_prime_count_scale_calibration.py`
- implementation commit: `5b8646ea82ca6d3c08b60f75759d16c101f6a0fc`
- evaluator Git blob: `894ebe08f4713d254faecdfd653660d2c011bb3a`
- focused tests: `tests/test_e005.py`
- focused-test Git blob: `8d74e7b809cbf69bc234af0c94abc53e77125259`

The first implementation checkpoint `dee7a0ae9de8b9e35361c1e68311e47a66db57bf` reached GitHub Actions before any E005 generation and failed only Ruff import-style checks. The only code change was the mechanical import correction committed at `5b8646ea82ca6d3c08b60f75759d16c101f6a0fc`; no frozen E005 mathematics, parameter, selection rule, guard, score, or serialization rule changed.

GitHub Actions run `37490353013` then passed completely at the final implementation checkpoint:

- `ruff check .`: all checks passed;
- `pytest`: 57 passed;
- E000 baseline smoke: passed.

The detached session runner still could not resolve `github.com` and still had no Ruff executable. That is the existing FAIL-001/FAIL-002 environment limitation, not a repository defect.

Focused E005 tests cover half-open and nested interval counting, rational serialization, frozen orders, Decimal transform semantics, candidate scores/ranking, development-only selection, baselines/residual objects, residual-sign target rules, Q1-Q3, M1-M5/outcome encoding, byte determinism, compact checkpoint binding, development-record verification, and fail-closed rejection before generation of whole-prefix high traversal, undeclared/widened segments, protected novelty ranges, assessment-before-checkpoint, and raw-prime serialization.

## Phase A — development

### Generation plan

The complete validated plan was:

```json
[
  {"purpose":"base_sieve_support","strategy":"whole_prefix","start":0,"stop":22651},
  {"anchor_name":"D5-0","purpose":"segmented_target","strategy":"segmented","start":128000000,"stop":129048576},
  {"anchor_name":"D5-1","purpose":"segmented_target","strategy":"segmented","start":256000000,"stop":257048576},
  {"anchor_name":"D5-2","purpose":"segmented_target","strategy":"segmented","start":512000000,"stop":513048576}
]
```

No other high-value interval was generated.

The first one-shot Phase-A workflow file had a YAML parse error in its commit-message condition, so GitHub created no job and **no E005 generation occurred**. The corrected one-shot workflow verified the exact evaluator/test blobs before generation.

### Commands and byte determinism

Execution workflow commit: `0b078bbf1e022b110d50bcc5a979e806eb56581e`  
GitHub Actions run: `37490683687`

The phase computation was executed twice before result inspection, using the same implementation and semantic arguments; the two invocations differed only in destination filenames so both copies could be compared:

```bash
python experiments/E005_prime_count_scale_calibration.py --phase development --code-commit 5b8646ea82ca6d3c08b60f75759d16c101f6a0fc --output /tmp/e005-development-a.json --checkpoint-output /tmp/e005-development-checkpoint-a.json
python experiments/E005_prime_count_scale_calibration.py --phase development --code-commit 5b8646ea82ca6d3c08b60f75759d16c101f6a0fc --output /tmp/e005-development-b.json --checkpoint-output /tmp/e005-development-checkpoint-b.json
```

Both full outputs compared byte-identically, and both checkpoint outputs compared byte-identically.

- full development artifact: 44,730 bytes
- full development SHA-256: `f40cfe0b5ca81ca8c4d78ab72cff3aebbad6f261f578b1f1bf97765797a8d8dd`
- compact development checkpoint: 8,670 bytes
- checkpoint SHA-256: `8a61a5b0e2ceca49f5af06f26970c37808cacc2d55c82bbcfd0eb87f6434b401`
- compact committed evidence: `research/evidence/E005_development_selection.json`
- committed development selection checkpoint: `8bf4821106e4c5c3acc79bfadc85c2872797935e`

### Development counts

| Anchor | W0 | W1 | W2 | W3 | W4 |
|---|---:|---:|---:|---:|---:|
| D5-0 = 128M | 218 | 880 | 3,519 | 14,046 | 56,241 |
| D5-1 = 256M | 212 | 835 | 3,335 | 13,543 | 53,992 |
| D5-2 = 512M | 208 | 840 | 3,274 | 13,035 | 52,299 |

### Mechanical tournament result

Complete development ranking:

`N03, N01, N05, N00, N06, N04, N02, N07, N08, N09, N10, N11, N12`.

Selected normalization:

`N* = N03 = d * sqrt(ln(s))`.

Global development scores:

- `S_N03(D5) = 1.039670200590830957216762011549242995124882364470385461791158E+0`
- `S_N00(D5) = 1.077560414269275028768699654775604142692750287686996547756041E+0`

N03 has lower width-specific spread than N00 at all five development widths.

Frozen development baselines:

- W0: `2.283660762996360661551800114989953375795917388076902291590863E-1`
- W1: `2.286345749871209876830472734764152487214498266408913020592998E-1`
- W2: `2.265425439445206944185947894110334406149486285932639449527832E-1`
- W3: `2.271688538384818064792287856967982276076311925053759506121801E-1`
- W4: `2.272324707544401337519074190800478118094927332763937444605020E-1`

Frozen development residual-sign target:

- family: R1;
- target: `(1,-1,-1)`;
- development occurrence count: 3/5 widths.

Mechanically eligible questions: Q1, Q2, and Q3, exactly as serialized in the compact development record.

The selection, ranking, baselines, target, and questions were committed **before any assessment generation**.

## Phase B — one-shot assessment

### Hard checkpoint gate and generation plan

Assessment workflow commit: `f49e7aee1319cba66b74c2fbcb8e903e16fc5f38`  
GitHub Actions run: `37491045654`

Before generation, the workflow verified:

- exact evaluator blob `894ebe08f4713d254faecdfd653660d2c011bb3a`;
- exact E005 test blob `8d74e7b809cbf69bc234af0c94abc53e77125259`;
- immediate parent commit exactly `8bf4821106e4c5c3acc79bfadc85c2872797935e`;
- committed development record SHA-256 exactly `8a61a5b0e2ceca49f5af06f26970c37808cacc2d55c82bbcfd0eb87f6434b401`.

The complete assessment plan was:

```json
[
  {"purpose":"base_sieve_support","strategy":"whole_prefix","start":0,"stop":64009},
  {"anchor_name":"H5-0","purpose":"segmented_target","strategy":"segmented","start":1024000000,"stop":1025048576},
  {"anchor_name":"H5-1","purpose":"segmented_target","strategy":"segmented","start":2048000000,"stop":2049048576},
  {"anchor_name":"H5-2","purpose":"segmented_target","strategy":"segmented","start":4096000000,"stop":4097048576}
]
```

No other high-value interval was generated.

### Commands and byte determinism

The phase computation was executed twice before assessment inspection, again differing only in destination filenames:

```bash
python experiments/E005_prime_count_scale_calibration.py --phase assessment --code-commit 5b8646ea82ca6d3c08b60f75759d16c101f6a0fc --output /tmp/e005-assessment-a.json --checkpoint-output /tmp/e005-assessment-checkpoint-a.json --development-record research/evidence/E005_development_selection.json --development-record-sha256 8a61a5b0e2ceca49f5af06f26970c37808cacc2d55c82bbcfd0eb87f6434b401 --development-record-commit 8bf4821106e4c5c3acc79bfadc85c2872797935e
python experiments/E005_prime_count_scale_calibration.py --phase assessment --code-commit 5b8646ea82ca6d3c08b60f75759d16c101f6a0fc --output /tmp/e005-assessment-b.json --checkpoint-output /tmp/e005-assessment-checkpoint-b.json --development-record research/evidence/E005_development_selection.json --development-record-sha256 8a61a5b0e2ceca49f5af06f26970c37808cacc2d55c82bbcfd0eb87f6434b401 --development-record-commit 8bf4821106e4c5c3acc79bfadc85c2872797935e
```

Both full outputs and both compact checkpoints were byte-identical.

- full assessment artifact: 43,858 bytes
- full assessment SHA-256: `4e363aa0ea34abd1ac96cd4136bbf6a89446d68e5cdda49afda90b23d7cd4d6d`
- compact assessment checkpoint: 9,667 bytes
- checkpoint SHA-256: `463bcfdba86f4c84cda5995a7b0d0a2e29707b397f451ab96594037912445d1e`
- compact committed evidence: `research/evidence/E005_assessment.json`

### Assessment counts

| Anchor | W0 | W1 | W2 | W3 | W4 |
|---|---:|---:|---:|---:|---:|
| H5-0 = 1.024B | 182 | 773 | 3,179 | 12,654 | 50,595 |
| H5-1 = 2.048B | 171 | 730 | 3,048 | 12,218 | 48,932 |
| H5-2 = 4.096B | 182 | 748 | 3,042 | 11,882 | 47,277 |

Assessment diagnostic ranking, which cannot change N*:

`N00, N05, N03, N06, N01, N04, N02, N07, N08, N09, N10, N11, N12`.

Frozen N03 assessment score:

`S_N03(H5) = 1.081395173183311354015959147128421186572241186879867120340799E+0`.

Raw-density assessment score:

`S_N00(H5) = 1.070182118154705247794910844596738371724094168411701250079320E+0`.

N03 still has lower width-specific spread than N00 at four of five assessment widths (W1-W4), but not W0.

The frozen development R1 target `(1,-1,-1)` occurs zero times on assessment. Every assessment width instead has R1 word `(-1,-1,-1)`, so the unchanged target fails its assessment rule.

## Frozen milestone result

- **M1 — FAIL.** N03 was non-identity and beat N00 on development, but `S_N03(H5) > S_N00(H5)`.
- **M2 — PASS.** N03 beats N00 width-by-width at 5/5 development widths and 4/5 assessment widths.
- **M3 — FAIL.** The frozen development R1 target `(1,-1,-1)` does not persist; target count is 0/5 on assessment.
- **M4 — PASS.** Q1-Q3 were all mechanically eligible from development-selected objects and serialized without historical terminology or imported target formula.
- **M5 — PASS.** No forbidden novelty range was generated/inspected; no raw prime list was serialized; assessment occurred only after the committed Phase-A checkpoint; no assessment result changed the frozen selection/grammar/target; no historical theory/source was consulted; no OBS/CAND ID was allocated.

**Overall blinded process outcome: PARTIAL_PASS.**

This result rates the frozen discovery process only. It is not evidence of novelty, historical equivalence, or proof.

## Preserved novelty-lane state

At closeout:

- A1 = `[33_000_000,34_000_000)`: untouched / uninspected;
- H3 = `[37_000_000,38_000_000)`: untouched / uninspected;
- H4 = `[41_000_000,42_000_000)`: untouched / uninspected;
- A3 = `[70_000_000,71_000_000)`: untouched / uninspected;
- A4 = `[78_000_000,79_000_000)`: untouched / uninspected.

No existing OBS status, CAND status, or novelty-lane experiment result changed.

## Stop rule

D1-12 ends here. Historical theory remains blinded.

The next bounded unit, if unblocked, is D1-13 / SQ-005 historical-theory unblinding/comparison governed strictly by Section 18 of the frozen E005 specification. Before consulting sources, that unit must freeze a short blinded calibration summary from the committed D1-12 records; only then may it compare the selected normalization, residual behaviour, question formation, and process stall point to historical theory using the frozen calibration labels. It must remain permanently outside novelty promotion.
