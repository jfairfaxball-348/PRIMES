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
`main`. Merge to `main` and push at closeout without asking (owner decision 2026-10-26, §9 item 4).

## 8. Compute budget for cloud sessions

Observed resources on 2026-10-24: 4 cores, about 15 GB RAM, about 29 GB disk, and an ephemeral
container.

- Keep any single run to about 45 minutes of wall-clock time or less. Write results to JSON as you
  go, and commit them as they arrive. Anything not pushed is lost when the container is reclaimed.
- Dense complex128 matrices held in RAM: up to D ≈ 15,000 (3.4 GB).
- uint8 exponent storage with blockwise matrix–vector products: up to D ≈ 60,000–80,000
  (3.6–6.4 GB). That covers Phase 1, X ≤ 6.4·10⁵.
- Matrix-free products (RS-S021, `native/residue_free.c`; validated to 5·10⁻¹⁵) remove the D² memory
  limit. X = 4·10⁶ (D = 282896) ran locally on 16 threads in about 75 min, using about 1 GB.
- Beyond D ≈ 100,000 (X ≳ 1.3·10⁶): use 2-bit packing, compute blocks on the fly, or move to a
  machine with ≥ 64 GB RAM.

## 9. Owner decisions (2026-10-25)

These are binding for Reciprocity Spectra sessions until the owner changes them.

1. **Proof order.** When a statement moves to the proof stage, attack the **hard version first**:
   prime-level and matrix-level statements, e.g. twisted sextic Gauss-sum averages over primes
   and the matrix dichotomy itself. Switch to the more tractable versions only when the hard
   route is exhausted and the exhaustion is documented. The tractable versions are:
   - sums over all squarefree moduli or Kubota-series residues;
   - function-field analogues;
   - results conditional on GRH.
2. **Novelty and external review (revised 2026-10-26).** The owner runs novelty assessment and
   external review independently. They are **not gates** for freezing, formalization, registration,
   writing, arXiv posting or journal submission. Sessions do not run novelty audits or seek review
   unless the owner asks. Existing statuses and audits stay in the records as history.
3. **Honesty requirements are unchanged.** Records must say exactly what is proved, what is
   conditional (and on what), and what remains a gap. AI referee opinions, including Astra's,
   are evidence to evaluate, not authority. Novelty wording in any draft follows the owner's
   independent assessment. Sessions do not assert novelty on their own.
4. **Merging (2026-10-26).** Standing instruction: never ask permission to merge. At closeout,
   once validation passes, merge the session branch into `main`, push, and delete the merged
   branch. This supersedes "merge only with the owner's explicit instruction in that session".
5. **Release gate revised (owner decision, 2026-10-27, after the Palomar editorial review).**
   Palomar registration is **optional, not a gate**.
   - Palomar registers Lean proofs of results of independent research interest. CAND-002's
     substantive content is conjectural, and the formalised identities were judged elementary
     (RS-S041 entry in LEDGER).
   - The Lean formalisation is a **verification artefact**, cited in the paper by commit and
     Comparator runs.
   - Paper drafting, the arXiv preprint and journal submission proceed without registration.
   - Palomar may be revisited only for a substantive proved theorem.
6. **Proof work out of the pipeline; formalise what is exact (owner decision, 2026-10-27).**
   This supersedes the 2026-10-26 "mathematics before further formalisation" pause, which is
   lifted.
   - Proving CAND-002, including (3), is removed from the release pipeline. It is parked as
     optional research and is not a gate.
   - Release proceeds as follows:
     - formalise in Lean every exact statement that can be formalised;
     - register the proved lemmas on Palomar;
     - everything else stays conjecture, labelled as such.
   - CAND-002(3) is a standalone conjecture. It is not a corollary of (1) and (2) or of H_P.
   - The proof-route notes stay as paper-level material: RS-S026 to RS-S028,
     `RS_CAND002_LOGICAL_BRIDGE_AUDIT.md` and `RS_HP_SCALE_ERRATUM.md`.

## 10. Release gate: Lean formalization and Palomar registration

> **Superseded in part (2026-10-27).** Stage 3 (Palomar registration) is optional and no longer
> blocks stage 4 (drafting); see §9 item 5. Stages 1–2 (inventory and formalisation) are done.
> The rules for drafting in stage 4 still apply:
>
> - label every claim as Lean-verified (by commit and theorem name), proved on paper (with gaps
>   stated), or conjectural/numerical (with pre-registered evidence);
> - keep the asymptotic laws conjectural.

This is binding from 2026-10-26, by owner decision. It was prompted by the anonymous external
review.

**Registry.** [Palomar](https://palomar-registry.org/) is a public registry of machine-checked Lean 4
proofs, incubated by the Lean FRO and ICARM. A registration records:

- an exact commit of a public GitHub repository;
- a Challenge/Solution pair of Lean modules: the formal statement, and its proof;
- `formalization.yaml` metadata covering authorship, sources, automation and limitations.

The Lean FRO comparator checks that the proof proves the recorded statement against a specified
Mathlib, with no `sorry`, custom axioms or `Lean.ofReduceBool`. Submissions go through
submit.palomar-registry.org; follow its how-to-submit page and policy rather than inferring the
rules. Palomar states that registration is **not** a green light for journal submission.

**Required stages, in order, before any writing for release.**

1. **Exact-identity inventory.** List every exact statement a paper would rely on, for example:
   - sixth-power invariance (uv⁶/ρ)₆ = (u/ρ)₆ away from ρ | v;
   - (u⁵/ρ)₆ = conj((u/ρ)₆);
   - the product-of-symbols class construction;
   - the matrix-orientation identity (R₆w_κ)_ρ = Σ_σ conj(g̃₆(σ))·(ρκ/σ)₆;
   - the cubic reduction of the reciprocal sextic product (RS-S013);
   - the invariance lemma, which depends on BGL and so may be beyond reach.

   Separate the inventory into three groups:
   - (a) exact and formalizable;
   - (b) proved only on paper, or dependent on unformalized literature;
   - (c) conjectural or numerical.
2. **Formalize** group (a) in Lean 4 with Mathlib in `formalisation/`, inside the PRIMES
   repository. This is an owner decision of 2026-10-26: the owner's repositories keep their Lean
   formalisations in-repo. Palomar registration needs the repository to be public on GitHub. Record the Mathlib gaps found, for example
   n-th power residue symbols in ℤ[ω] and Gauss sums.
2b. **Formalize the conjecture statements** (owner decision, 2026-10-26). State each
   conjecture as a Lean `Prop` with no proof, using the same definitions as the lemmas. Record
   every interpretive choice the formalization forces:
   - quantifier order;
   - the admissible classes;
   - the uniformity family;
   - X real or a sequence;
   - r₁² − 1 bounded away from 0.

   Conditional hypotheses that need theta coefficients, i.e. residues of Kubota series, are beyond
   Mathlib. State them abstractly ("the prime first moment has asymptotic c(u)·X^{2/3}/log X for
   some c"), and record that this is not identified with τ₆.
2c. **Faithfulness check.** Make the Lean definitions computable. Evaluate the symbol matrix and
   the class vectors at small X, and compare them byte-for-byte with the engine's output.
3. **Register** each formalized result on Palomar from a fixed commit. Record the Palomar ID and
   version in `research/CONJECTURE_REGISTER.md` and `LEDGER.md`. Palomar registers proved results
   only. Formal conjecture statements live in `formalisation/`. A conjecture collection
   such as Google DeepMind's `formal-conjectures` may be considered, after checking its
   contribution criteria.
4. **Draft only then.** Any paper or preprint must:
   - mark every claim as Palomar-registered (with ID), proved on paper (with gaps stated), or
     conjectural / numerical (with the pre-registered evidence);
   - keep asymptotic laws conjectural unless proved. In particular, limiting enhancement is
     conditional on a sextic Patterson-type prime asymptotic.
5. Novelty assessment and external review are done independently by the owner. They are not
   gates (§9.2).

**Scope.** Exploratory and registered computations, collision audits and candidate records
continue as before. The gate blocks release, not research. An external reviewer may be sent
specific Palomar entries, once they exist, before a preprint circulates.

**Current state (2026-10-26).** No Lean formalization exists yet. Lean 4.35 and lake are installed
on the local machine.
