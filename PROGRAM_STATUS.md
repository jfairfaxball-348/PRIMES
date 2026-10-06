# PRIMES Programme Status

Status date: 2026-10-06

## Current stage

**DISCOVERY-0 — E001 grid frozen; first structured discovery sweep pending**

## Gates

| Gate | Status | Requirement to open |
|---|---|---|
| Exact data pipeline | OPEN / VALIDATED | Core implementation, lint, tests, E000 smoke |
| Pattern discovery | OPEN / READY | Frozen E001 discovery grammar and partition |
| Observation promotion | OPEN | Exact reproducible observation |
| Candidate conjecture | CLOSED | Holdout survival + exact statement |
| Prior-art collision audit | CLOSED | Candidate status reached |
| Proof programme | CLOSED | Candidate survives collision/falsification |
| Publication | CLOSED | Separate theorem project reaches proof maturity |

## Bootstrap and preflight verification

- package installation: passed in GitHub Actions;
- Ruff: passed in GitHub Actions;
- pytest: passed in GitHub Actions and reproduced locally (9/9);
- E000 baseline smoke run: passed in GitHub Actions;
- E000 repeated at limits 10,000 and 100,000 with byte-identical summaries on repeat execution;
- repository sieve independently matched a trial-division generator at both E000 limits;
- E001 representation grid and numerical partition: **FROZEN BEFORE RESULT INSPECTION**;
- authoritative discovery/novelty/calibration protocols: committed;
- observation, conjecture, failure, search-queue, autonomous-session records: committed.

Validated CI head: `e47b272b6e3867fb10d0eefc199b1231557659da`.

E000 preflight evidence: `experiments/E000_PREFLIGHT_2026-10-06.md`.

E001 frozen specification: `experiments/E001_REPRESENTATION_GRID.md`.

Local-session limitation: detached runner network access and Ruff availability were incomplete; recorded as `FAIL-001`. No E000 data-quality failure was found.

## E001 frozen partition

- Discovery D0: `[0, 1_000_000)`
- Untouched holdout H0: `[1_000_000, 2_000_000)`
- Reserved adversarial A0: `[10_000_000, 11_000_000)`

No E001 result has yet been generated or inspected. H0 and A0 remain untouched.

## Session control

- Autonomous closeout protocol: **ACTIVE**
- Owner decision blocker: **NONE**
- Live next-session prompt: **ACTIVE — `NEXT_SESSION_PROMPT.md`**
- Closeout rule: automatically emit the next runnable prompt unless an owner decision blocks continuation.

## Active task

**D0-03 / SQ-001:** implement the frozen E001 representation grid, validate deterministic serialization/boundary semantics, and execute/inspect the discovery range D0 only. Do not generate or inspect H0.

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
7. E001 H0 cannot be used to tune any feature; proposed observations must be frozen exactly before one-shot holdout replication.
8. No candidate conjecture may be created unless an exact observation has survived an untouched holdout.

## Next stage

DISCOVERY-1 begins when the first structured observation sweep has been recorded and its promoted observations have untouched holdout ranges reserved.
