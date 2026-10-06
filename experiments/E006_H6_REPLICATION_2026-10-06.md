# E006 H6 Replication — 2026-10-06

**Stage:** replication  
**Queue item:** SQ-006  
**Related task:** D1-17 / SQ-006  
**Frozen specification:** experiments/E006_TRANSLATION_OVERLAP_SPECTRUM.md  
**Frozen discovery evidence:** experiments/E006_D6_DISCOVERY_2026-10-06.md and research/evidence/E006_D6_discovery.json  
**Status:** COMPLETE — OBS-008 REPLICATED; OBS-005/006/007/009 REFUTED; A6 UNTOUCHED

This record documents the one-shot H6 replication of the five frozen E006 observations only. D6 remains frozen historical discovery evidence. E001/E002/E003/E004 were not rerun or mined, SQ-005 remained quarantined, and no calibration object or historical-unblinding mechanism was used to interpret H6.

## Frozen implementation integrity

The exact E006 evaluator and focused-test bytes were checked before H6 generation against implementation/test checkpoint `8bfcc27d96dc1b0858c514cf2bfab81790ab71b0`.

- evaluator: `experiments/E006_translation_overlap_spectrum.py`
- evaluator Git blob: `4f79c435c8213c49859da351c7393a692be34b0c`
- focused tests: `tests/test_e006.py`
- focused-test Git blob: `2102f44af67497cf293bf95b5a3a8afcb21a8b31`
- unchanged core Git blob: `ee600508452e1036f52d00fb9c0b22844c646601`

Current bytes matched the frozen checkpoint exactly. H=1000, shifts {2,4,...,1000}, the common anchor, all-pairs overlap definition, odd-radical classes, frozen targets, occurrence floor, tie rule, ordering, serialization, and generation guard were unchanged.

## H6 generation-plan validation

Before prime generation, the complete H6 plan was validated:

~~~json
[
  {"purpose":"base_sieve_support","start":0,"stop":6709,"strategy":"whole_prefix"},
  {"purpose":"segmented_target","start":44000000,"stop":45000000,"strategy":"segmented"}
]
~~~

The low prefix is exactly `[0,6709)`, sufficient through `floor(sqrt(44,999,999)) = 6708`, and remains inside historically safe support below 100,000. The only high-value interval is H6=`[44_000_000,45_000_000)`.

Guard validation deliberately attempted high whole-prefix generation, partial-H6 generation, D6, G6-mid, A1, all frozen E003/E004 targets and guards, H3, H4, A3, A4, and A6. Every invalid plan failed before the prime generator was called.

## Validation before H6 generation

Validation on the exact committed bytes:

~~~text
PYTHONPATH=src pytest -q tests/test_e006.py
14 passed

python -m compileall -q src experiments tests
success

ruff --version
command not found
~~~

Ruff absence is the existing FAIL-001/FAIL-002 detached-runner limitation, not a new repository defect. Combined-status and PR-triggered workflow-run collections were empty for both checkpoint `8bfcc27d96dc1b0858c514cf2bfab81790ab71b0` and the D1-16 head `d8f2ce9a1f8f87a1320407d3334613dd6b2041af`; this is the existing FAIL-002 observability limitation only.

## Deterministic H6 artifact

Exact command:

~~~bash
PYTHONPATH=src python experiments/E006_translation_overlap_spectrum.py --band H6 --code-commit 8bfcc27d96dc1b0858c514cf2bfab81790ab71b0 --output /tmp/e006-h6.json
~~~

The identical complete command was executed twice with the same arguments and output path before any criterion result was inspected. The outputs were byte-identical.

- bytes: 111,561
- SHA-256: `be1694f488777be97202d9ccb047d56ba97a2d8fe087bab968090837dfc6ca3e`
- compact criterion evidence: `research/evidence/E006_H6_replication.json`

No descriptive H6 scan was performed after generation. Only the five predeclared replication criteria were read.

## Frozen criterion results

| Observation | rho | target h | H6 target count | highest same-class competitor | strict margin | Result |
|---|---:|---:|---:|---|---:|---|
| OBS-005 | 15 | 900 | 11,397 | h=90: 11,456 | -59 | REFUTED |
| OBS-006 | 35 | 280 | 6,776 | h=560: 6,855 | -79 | REFUTED |
| OBS-007 | 7 | 56 | 5,047 | h=28: 5,179 | -132 | REFUTED |
| OBS-008 | 21 | 294 | 10,305 | h=126: 10,301 | +4 | REPLICATED |
| OBS-009 | 3 | 324 | 8,527 | h=216: 8,667 | -140 | REFUTED |

Every target count exceeds the frozen occurrence floor of 8. There are no target ties in these five criterion checks. OBS-005, OBS-006, OBS-007, and OBS-009 fail only because a frozen same-radical competitor has higher H6 count. OBS-008 succeeds because shift 294 retains strict superiority over every other frozen rho=21 member, with highest competitor shift 126 at 10,301.

No failed observation was retargeted, no unselected radical class was inspected for a new phenomenon, and no H6 observation was promoted.

## Preserved ranges and stop rule

This unit generated no high-value primes outside H6. D6 remains frozen historical discovery evidence. A1=`[33_000_000,34_000_000)`, H3=`[37_000_000,38_000_000)`, H4=`[41_000_000,42_000_000)`, G6-mid=`[43_000_000,44_000_000)`, A3=`[70_000_000,71_000_000)`, A4=`[78_000_000,79_000_000)`, A6=`[84_000_000,85_000_000)`, and all frozen E003/E004 guards were not generated in D1-17 and retain their frozen roles.

D1-17 stops at this replication checkpoint. No candidate synthesis, candidate creation, mechanism/proof work, prior-art/collision search, A6 generation, protected-range inspection, or H6 pattern mining occurred.

The next bounded unit is D1-18 / SQ-006 candidate-synthesis triage over the sole E006 holdout survivor, OBS-008, using only committed D6+H6 evidence and no new prime generation.
