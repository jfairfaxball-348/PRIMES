# Search Queue

This queue contains bounded discovery work, not claims.

## SQ-001 — Baseline representation sweep

Stage: discovery

Run exact scans over:

- gap words of widths 2 through 6;
- finite differences through order 4;
- residue transitions for a small declared modulus family;
- block occupancies at logarithmically separated widths;
- record-gap local neighbourhoods.

Goal: produce descriptive summaries and artifact checks only.

Promotion cap: 10 observations.

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
