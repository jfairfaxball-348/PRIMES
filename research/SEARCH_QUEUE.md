# Search Queue

This queue contains bounded discovery work, not claims.

## SQ-001 — Baseline representation sweep

Stage: discovery

Status: **D0 EXECUTED — FOUR OBSERVATIONS FROZEN; H0/A0 UNTOUCHED**

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

D0 result: deterministic discovery artifact SHA-256 `822431d664d5a35949abdf230a1b8abb41afa1f97511b7c129e5d18779f2e284`; four promoted observations (`OBS-001` through `OBS-004`) now have exact one-shot H0 replication criteria frozen in `research/OBSERVATION_LEDGER.md`.

Next bounded action: execute E001 on untouched **H0 only** using the unchanged implementation semantics and evaluate only the four frozen replication criteria. Do not mine H0 for new observations, do not generate A0, and do not create a candidate in the same bounded unit.

## SQ-002 — Cross-scale persistence

Stage: replication/discovery

Take only definitions frozen by SQ-001 and compare their rankings/extrema across disjoint magnitude bands.

Goal: identify features whose *definition* survives scale rather than features tuned to one band.

Promotion cap: 5 observations.

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
