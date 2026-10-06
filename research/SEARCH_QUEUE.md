# Search Queue

This queue contains bounded discovery work, not claims.

## SQ-001 — Baseline representation sweep

Stage: discovery

Status: **CANDIDATE TRIAGE COMPLETE — NO CANDIDATE CREATED; THREE REPLICATED OBSERVATIONS RETAINED; A0 UNTOUCHED**

Frozen specification: `experiments/E001_REPRESENTATION_GRID.md`

Predeclared value ranges:

- discovery D0: `[0, 1_000_000)`;
- untouched holdout H0: `[1_000_000, 2_000_000)`;
- reserved adversarial A0: `[10_000_000, 11_000_000)`.

Run exact scans over:

- gap words of widths 2 through 6;
- finite differences through order 4;
- residue transitions for the frozen modulus family `6, 10, 12, 30, 60`;
- globally anchored block occupancies at widths `100, 1_000, 10_000, 100_000`;
- strict global record-gap neighbourhoods at gap radii `2, 4, 8`.

Goal: produce descriptive summaries and artifact checks only.

Promotion cap: 10 observations.

D0 result: deterministic discovery artifact SHA-256 `822431d664d5a35949abdf230a1b8abb41afa1f97511b7c129e5d18779f2e284`; four observations were frozen before holdout.

H0 result: deterministic holdout artifact SHA-256 `80c8c49f1845e941764b31471404a8e674fa794394687cb6502dbd2eca980254`. `OBS-001`, `OBS-002`, and `OBS-003` replicated under their frozen criteria. `OBS-004` was refuted by the empty anchored block `[1_671_800, 1_671_900)`. A0 remains untouched.

Candidate-synthesis result: D1-02 considered `OBS-001` through `OBS-003` only and allocated no `CAND-###`. OBS-001 and OBS-002 remain exact replicated modal-rank facts but do not yet support a non-arbitrary scale/band quantifier. OBS-003 remains exact replicated finite-grid coverage but does not yet justify an all-moduli or infinite-occurrence extrapolation. OBS-004 remains REFUTED and excluded.

Next bounded action: D1-03 / SQ-002 cross-scale persistence preflight. Freeze a new E002 design and fresh disjoint ranges before execution, using the E001 definitions unchanged and excluding reserved A0. Do not generate new results, create a candidate, perform mechanism work, or run prior-art search in that preflight unit.

## SQ-002 — Cross-scale persistence

Stage: replication

Status: **FROZEN — E002 READY FOR EXECUTION; NO E002 RESULTS GENERATED**

Frozen specification: `experiments/E002_CROSS_SCALE_PERSISTENCE.md`

Scope: `OBS-001`, `OBS-002`, and `OBS-003` only. `OBS-004` remains REFUTED and excluded.

Fresh fixed-width scale ladder:

- S1: `[2_000_000, 3_000_000)`;
- S2: `[4_000_000, 5_000_000)`;
- S3: `[8_000_000, 9_000_000)`;
- S4: `[16_000_000, 17_000_000)`;
- S5: `[32_000_000, 33_000_000)`.

All five bands are mutually disjoint and exclude E001 D0, H0, and reserved A0 = `[10_000_000, 11_000_000)`. A0 remains untouched.

Frozen persistence tests preserve the exact E001 definitions:

- OBS-001: third forward difference `0` must be the strict unique mode in every E002 band;
- OBS-002: width-2 gap motif `[6, 6]` must be the strict unique mode in every E002 band;
- OBS-003: directed reduced-residue transition support must be complete for every modulus in the unchanged family `{6,10,12,30,60}` in every E002 band.

A tie fails the applicable modal-rank criterion; any missing allowed transition fails OBS-003. Overall E002 persistence requires passing all five bands. The full predeclared ladder is evaluated even after an earlier failure; no replacement/additional bands or post-result thresholds are allowed.

Goal: test definition-preserving persistence with increasing value magnitude while holding the one-million band width fixed.

Promotion cap: no new observations or candidates in the E002 execution unit; it records persistence outcomes for the existing replicated observations only.

Next bounded action: D1-04 / SQ-002 — implement and execute the frozen E002 criterion-only test, validate determinism, evaluate only the predeclared criteria, keep A0 untouched, and do not mine new phenomena or perform candidate/mechanism/prior-art work.

## SQ-003 — Event-centred neighbourhoods

Stage: discovery

Define prime-dense, prime-sparse, and record-gap events using frozen thresholds. Encode fixed-radius neighbourhoods around those events.

Goal: search for repeated exact local configurations and before/after asymmetries.

Promotion cap: 5 observations.

## SQ-004 — Residue-transition factorization

Stage: discovery

Compare transition fingerprints across related moduli and ask whether one fingerprint can be exactly derived from another by a simple projection/refinement rule.

Goal: exact inter-modulus identities or forbidden transition patterns.

Promotion cap: 5 observations.

## SQ-005 — Historical rediscovery calibration

Stage: calibration

Run the method in the quarantined calibration lane described in docs/CALIBRATION_PROTOCOL.md.

Goal: learn which discovery operations are capable of producing genuinely explanatory objects.

Nothing from this queue item can be promoted as novel.
