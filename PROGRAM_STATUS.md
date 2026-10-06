# PRIMES Programme Status

Status date: 2026-10-06

## Current stage

**DISCOVERY-0 — validated bootstrap; first structured observation sweep pending**

## Gates

| Gate | Status | Requirement to open |
|---|---|---|
| Exact data pipeline | OPEN / VALIDATED | Core implementation, lint, tests, E000 smoke |
| Pattern discovery | OPEN | E000 baseline available |
| Observation promotion | OPEN | Exact reproducible observation |
| Candidate conjecture | CLOSED | Holdout survival + exact statement |
| Prior-art collision audit | CLOSED | Candidate status reached |
| Proof programme | CLOSED | Candidate survives collision/falsification |
| Publication | CLOSED | Separate theorem project reaches proof maturity |

## Bootstrap verification

- package installation: passed in GitHub Actions;
- Ruff: passed;
- pytest: passed;
- E000 baseline smoke run: passed;
- authoritative discovery/novelty/calibration protocols: committed;
- observation, conjecture, failure, and search-queue records: committed.

Validated CI head: `e47b272b6e3867fb10d0eefc199b1231557659da`.

## Active task

**D0-02 / D0-03:** run E000 at declared research scales, freeze the E001 representation grid, and begin SQ-001 without using holdout data for feature tuning.

## Research inventory

- Active observations: 0
- Active candidates: 0
- Refuted candidates: 0
- Prior-art collisions: 0
- Graduated theorem projects: 0

## Current methodological commitments

1. Discovery and prior-art search are separate stages.
2. Numerical ranges are partitioned before candidate evaluation.
3. Exact statements outrank visual/statistical impressions.
4. Failed directions remain part of the project.
5. White-space claims require explicit collision audits and, ultimately, expert scrutiny.
6. Historical rediscovery is a quarantined calibration lane and cannot generate novelty claims.

## Next stage

DISCOVERY-1 begins when the first structured observation sweep has been recorded and its promoted observations have untouched holdout ranges reserved.
