# Reciprocity Spectra: session protocol

This protocol governs every session that works on `reciprocity_spectra/`. It keeps PRIMES's
epistemic core and session mechanics. It replaces the DISCOVERY-1 blind-discovery machinery, which
`LESSONS.md` identifies as the cause of zero candidates in 72 sessions. The D1 chain is paused, not
deleted. Its records and rules stay in force for D1 work only.

## 1. Enter from committed authority

The repository on `main` is authoritative. Conversation history is not.

Read, in order:

1. `reciprocity_spectra/PROTOCOL.md` (this file);
2. `reciprocity_spectra/LEDGER.md`: programme ledger and latest state;
3. `reciprocity_spectra/CONJECTURES.md`: statuses and committed predictions;
4. `reciprocity_spectra/ROADMAP.md`: the current phase;
5. `NEXT_SESSION_PROMPT.md`;
6. when relevant: `README.md`, `LESSONS.md`, `PRIOR_ART.md`, `AREA_TRIAGE.md` in this directory.

You do **not** need to read or reconstruct the D1 records:

- `research/OBSERVATION_LEDGER.md`;
- interval roles;
- guard bands;
- E005 calibration objects.

Do not modify them.

## 2. Inherited from PRIMES (binding)

- **Hard epistemic rules** (`PROJECT_CHARTER.md`, rules 1–10):
  - finite computation refutes but never proves;
  - a negative literature search is not novelty;
  - a visual pattern is not a conjecture;
  - a fitted curve is not a mechanism;
  - failures stay in the record;
  - approximate numerics are never silently substituted for exact arithmetic.
- **Evidence rules** (`AGENTS.md`):
  - prefer exact arithmetic;
  - record seeds;
  - commit machine-readable outputs;
  - state exactly what was checked.
- **Novelty vocabulary** (`docs/NOVELTY_PROTOCOL.md`): UNAUDITED, SEARCHED_NO_COLLISION_FOUND,
  POSSIBLE_OVERLAP, KNOWN_EQUIVALENT, KNOWN_IMPLIED, NOVELTY_REQUIRES_EXPERT_REVIEW. Never write
  "new", "novel" or "first" from memory.
- **Session mechanics** (`docs/SESSION_PROTOCOL.md` §2–§10):
  - one bounded unit per session;
  - stop at a natural checkpoint;
  - classify blockers;
  - meet the closeout obligations;
  - write exactly one next prompt, or stop for an owner decision;
  - validate before closing.

## 3. Replaced (does not apply to Reciprocity Spectra)

| D1 rule | Replacement |
|---|---|
| Blind-discovery firewall; no literature during discovery | **Model first.** Literature and theory are used from the start. Every external fact is cited with its source. |
| Discovery, holdout and adversarial band partitions; one-shot holdouts; interval-role audits; guard bands; generator preflights; AST guards; one-shot workflows | **Pre-registration** (§4) and the **null-model rule** (§5) |
| OBS/CAND numbering | RS-n conjecture IDs with statuses PILOT, STRESSED, REFUTED, PROVED, KNOWN (`CONJECTURES.md`). A statement that becomes a theorem candidate may also be registered as a `CAND-###` in `research/CONJECTURE_REGISTER.md` for graduation. |
| Calibration lane (E005) | not used |

## 4. Pre-registration: the holdout discipline of this programme

Before any computation that tests a conjecture at a new scale, or on a new family:

1. Write the predicted values and their pass/fail tolerances into `CONJECTURES.md`, or into the
   session's prediction block in `LEDGER.md`.
2. Commit and push that change.
3. Only then run the computation.
4. Record the outcome against the committed prediction, verbatim. Never edit a prediction after
   seeing data. A revised prediction is a new prediction for a new scale.

Computations without a committed prediction are allowed. They must be labelled EXPLORATORY in
`results/`, and they cannot change a conjecture's status on their own.

## 5. Null-model rule

Every reported spectral deviation is accompanied by the symmetry-matched random control at the same
dimension D (`scripts/spectra.py`, `structured_random`), with the seed recorded.

## 6. Results and code

- Every number quoted in a document appears in a results JSON under `results/`. The JSON records
  the date, the code commit, the command, the parameters, X, D and seeds.
- Matrices are deterministic and are not committed. Rebuild them into the git-ignored `data/`.
- New exact functions get pure-Python tests in `tests/test_reciprocity_spectra.py`, which CI runs.
- A new numerical engine is validated against the previous one at overlapping sizes before it is
  used at a new scale:
  - matrices byte-identical;
  - singular values agree to 1e-8 relative.
- Run `ruff check` on the touched Python files and `pytest` before closeout. The repository-wide
  `ruff check .` currently fails on frozen D1 experiment files. Do not edit those files to fix it.

## 7. Closeout

Update:

- `LEDGER.md`: a session entry with the bounded task, the result, validation, commits, and the
  next dependency;
- `CONJECTURES.md`: status changes, recorded against the predictions;
- `results/`;
- `ROADMAP.md`, if the phase changes;
- the current-stage line of `PROGRAM_STATUS.md`, if the programme state changes materially;
- `NEXT_SESSION_PROMPT.md`: exactly one prompt, or suppressed if an owner decision is required
  (`docs/SESSION_PROTOCOL.md` §7).

Commit and push to the session's designated branch. Work becomes authoritative when it is merged to
`main`. Merge only with the owner's explicit instruction in that session.

## 8. Compute budget for cloud sessions

Observed resources on 2026-10-24: 4 cores, about 15 GB RAM, about 29 GB disk, and an ephemeral
container.

- Keep any single run to about 45 minutes of wall-clock time or less. Write results to JSON as you
  go, and commit them as they arrive. Anything not pushed is lost when the container is reclaimed.
- Dense complex128 matrices held in RAM: up to D ≈ 15,000 (3.4 GB).
- uint8 exponent storage with blockwise matrix–vector products: up to D ≈ 60,000–80,000
  (3.6–6.4 GB). That covers Phase 1, X ≤ 6.4·10⁵.
- Beyond D ≈ 100,000 (X ≳ 1.3·10⁶): use 2-bit packing, compute blocks on the fly, or move to a
  machine with ≥ 64 GB RAM.
