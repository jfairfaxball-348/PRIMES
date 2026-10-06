# PRIMES Programme Status

Status date: 2026-10-06

## Current stage

**DISCOVERY-1 — E001 candidate-synthesis triage complete; no candidate promoted; three replicated observations retained; A0 untouched**

## Gates

| Gate | Status | Requirement to open |
|---|---|---|
| Exact data pipeline | OPEN / VALIDATED | Core implementation, lint, tests, E000 smoke |
| Pattern discovery | OPEN / H0 REPLICATED | Frozen E001 discovery grammar and partition |
| Observation promotion | OPEN / 3 REPLICATED, 1 REFUTED | Exact reproducible observation |
| Candidate conjecture | OPEN / ELIGIBLE, NONE PROMOTED | Holdout survival satisfied by OBS-001 through OBS-003; D1-02 found no exact non-arbitrary candidate statement justified by current evidence |
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
- E001 implementation and boundary/determinism tests committed at `beab213501dab318075199c3fcac6d5501d0b9d3`;
- E001 D0 executed twice with byte-identical 24,923,621-byte artifacts, SHA-256 `822431d664d5a35949abdf230a1b8abb41afa1f97511b7c129e5d18779f2e284`;
- four exact D0 observations promoted with H0 criteria frozen before holdout generation;
- E001 H0 executed twice with byte-identical 25,557,012-byte artifacts, SHA-256 `80c8c49f1845e941764b31471404a8e674fa794394687cb6502dbd2eca980254`;
- H0 frozen-criterion outcomes: `OBS-001`, `OBS-002`, and `OBS-003` REPLICATED; `OBS-004` REFUTED by the empty anchored block `[1_671_800, 1_671_900)`;
- D1-02 candidate-synthesis triage considered only OBS-001 through OBS-003 and created no candidate: OBS-001/002 remain range-local modal-rank facts whose natural generalizations introduce unsupported scale/banding quantifiers, while OBS-003's finite frozen-modulus coverage does not justify an all-moduli or infinite-occurrence extrapolation;
- reserved A0 remains untouched; no mechanism work or prior-art search has yet been performed;
- authoritative discovery/novelty/calibration protocols: committed;
- observation, conjecture, failure, search-queue, autonomous-session records: committed.

Validated CI head: `e47b272b6e3867fb10d0eefc199b1231557659da`.

E000 preflight evidence: `experiments/E000_PREFLIGHT_2026-10-06.md`.

E001 frozen specification: `experiments/E001_REPRESENTATION_GRID.md`.

E001 D0 execution evidence: `experiments/E001_D0_DISCOVERY_2026-10-06.md`.

Local-session limitations: detached runner network/Ruff availability and current-head CI observability are incomplete; recorded as `FAIL-001` and `FAIL-002`. Local E001 pytest passed 14/14, compilation succeeded, and an independent SymPy prime list exactly matched the repository sieve on D0.

## E001 frozen partition

- Discovery D0: `[0, 1_000_000)`
- Untouched holdout H0: `[1_000_000, 2_000_000)`
- Reserved adversarial A0: `[10_000_000, 11_000_000)`

D0 has been generated and used for discovery. H0 has now been generated twice byte-identically and inspected only against the four frozen replication criteria. `OBS-001` through `OBS-003` replicated; `OBS-004` was refuted. A0 remains untouched.

## Session control

- Autonomous closeout protocol: **ACTIVE**
- Owner decision blocker: **NONE**
- Live next-session prompt: **ACTIVE — `NEXT_SESSION_PROMPT.md`**
- Closeout rule: automatically emit the next runnable prompt unless an owner decision blocks continuation.

## Active task

**D1-03 / SQ-002:** cross-scale persistence preflight for replicated `OBS-001` through `OBS-003`. Freeze a new E002 scale-persistence design and fresh disjoint numerical bands before execution. Preserve the E001 definitions, keep A0 reserved and untouched, and do not create a candidate or perform prior-art/mechanism work in the preflight unit.

## Research inventory

- Active observations: 3
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

DISCOVERY-1 is active. H0 replication is complete: three observations survived and one was refuted. D1-02 candidate-synthesis triage created no `CAND-###`: the current two-band evidence is sufficient for replication but not for a mathematically non-arbitrary extrapolation. The next natural checkpoint is D1-03 / SQ-002 cross-scale persistence preflight, which must freeze a new design and fresh disjoint ranges before any new execution. A0 remains reserved and untouched.
