# Reciprocity Spectra: programme ledger

This ledger is append-only. Session IDs are `RS-S###`.

## Current state

- **Phase:** 1 (scaling with pre-registered predictions). Not started.
- **Conjectures:** RS-1, RS-2, RS-3, RS-4 and RS-6 are PILOT. RS-5 is UNTESTED.
- **Committed predictions:** written in `CONJECTURES.md` and `ROADMAP.md` at commit `0b77769`.
  That is before any run at X > 1.6·10⁵. For X = 3.2·10⁵ and 6.4·10⁵:
  - κ₃ ∈ [1.38, 1.47];
  - cubic overlap within 0.03 of `√(1 − D/θ²)`;
  - quartic `θ_n = 0.166·ln X − 0.18 ± 0.05`, which is 1.924 at 3.2·10⁵ and 2.039 at 6.4·10⁵;
  - quadratic `(2 − m₄)·ln D ∈ [1.0, 1.4]`.
- **Owner decision blocker:** none.
- **Next unit:** RS-S002, Phase 1a (see `NEXT_SESSION_PROMPT.md`).

---

### RS-S001 (2026-10-24): area triage, pilot, and opening of the programme

**Stage:** area selection, collision audit, and pilot computation.

**Bounded task:** find an unsaturated, genuinely interesting research area in primes, given the
failure modes of PRIMES D0–D1 and Pointed Order Zeta. Pilot it, and set up a programme.

**What was done:**

- Read both repositories and diagnosed their failure modes (`LESSONS.md`).
- Checked eight candidate areas against the literature (`AREA_TRIAGE.md`).
- Killed one candidate computationally: there is no consecutive-prime bias in the non-abelian part
  of an S3 Frobenius, to 10⁹ (`scripts/consecutive_frobenius_s3.c`).
- Chose spectra of power-residue matrices.
- Recorded the collision audit (`PRIOR_ART.md`). The closest prior art is at operator-norm level
  only: Dunn–Radziwiłł (2024) and de Faveri–Dunn–Hoffstein (July 2026). The matrices themselves come
  from Dummit–Dummit–Kisilevsky (2016).

**Results (pilot, D ≤ 14,682):**

- **RS-1.** The cubic spike law holds with κ₃ = 1.419–1.434 for X from 5·10³ to 1.6·10⁵. The
  overlap with conjugate Gauss sums is 0.936, against a BBP prediction of 0.939.
- **RS-2.** The cubic outlier family is identified with twisted Gauss sums for u = 2, 1−ω, and the
  primes of norm 7, 13, 19, 31, 37, 43.
- **RS-3.** Quartic outliers have θ_n = 1.461, 1.574, 1.690, 1.810, and their vectors are not
  Gauss sums.
- **RS-4.** The quadratic compression gives `(2 − m₄)·ln D` = 1.248 down to 1.196 for D from 668 to
  14,682.
- Symmetry-matched random controls give `σ₁/edge = 0.997–1.000` and `m₄ ≈ 1.997`.

**Validation:**

- 6 new exact tests: reciprocity laws for n = 2, 3, 4; `g³ = pπ`; `g⁴ = pπ²`; `−χ(−1)J = π`;
  multiplicativity.
- The full pytest suite passes.
- `ruff check` is clean on all new files.
- The C builder is byte-identical to the pilot builds.
- `scripts/run_pilot.sh 10000` reproduces the recorded numbers.

**Commits:**

- PRIMES `0b77769`: programme opened.
- pointed-order-zeta `b7dd2b8`: successor pointer.
- Follow-up commit: this ledger, `PROTOCOL.md`, and the switch of the active programme.

**Owner decision (recorded from the 2026-10-24 conversation):**

- Merge the work.
- Start investigating under a new authoritative next-session prompt.
- Implemented as follows. Reciprocity Spectra is the active PRIMES programme. The DISCOVERY-1 chain
  is **paused** at D1-72/S074, with 16 REPLICATED / 0 OBSERVED / 9 REFUTED and zero candidates.
  SQ-037 is deferred, not started. The previous D1-73 prompt is preserved in git history at
  `8bbaeee:NEXT_SESSION_PROMPT.md`.

**Failures and limitations:**

- Novelty status is search-based only. The area is adjacent to an active group (Dunn, de Faveri,
  Hoffstein, David), and expert review is needed before any claim.
- Mechanisms are hypotheses. κ₃ and c₄ are not derived.
- The repository-wide ruff step was already failing on frozen D1 files. That is unchanged.

**Outgoing state:** Phase 1 ready. One prompt has been written (RS-S002).


### RS-S002 (2026-10-24): Phase 1a, scalable engine and registered scaling tests

**Stage:** certification and falsification.

**Bounded task:** build and validate a four-thread byte engine, then test the predictions committed
at `0b77769` at X = 320000. No mechanism derivations or additional families.

**Engine and validation:**

- Added `native/residue_engine.c` and `scripts/phase1.py`: OpenMP character-table construction and
  normalized Gauss sums, blocked complex forward/adjoint products, matrix-free Lanczos, and
  seeded Hutchinson fourth moments. The pilot builder remains unchanged.
- All three matrix files at X = 20000 are byte-identical to the pilot builder.
- All top-eight singular values at X = 40000 agree with SciPy `svds` within 1e-8 relative.
  The optimized engine's maximum discrepancy is 4.663e-15.
- Quadratic m4 at X = 40000 passes the two-standard-error comparison with the dense Gram trace;
  individual probe values and standard errors are retained in the results JSON.
- Cubic Gauss sums at X = 20000 are byte-identical to the serial builder. Complex products,
  adjoints and matched-control reciprocity signs are checked independently.
- Ruff passes on touched Python files; the full pytest suite passes (343 tests).
- The initial transpose adjoint was slow. Its unfinished control was stopped without reporting
  a control value. A contiguous-row adjoint using the existing reciprocity signs was separately
  validated before further scaling computation. The attempt and both validation records are
  preserved; this is an implementation identity, not a mechanism derivation.

**Incremental cubic result (completed; other families still running at this checkpoint):**

X = 320000, D = 27554; sigma1 = 577.368785377, theta = 524.872196315,
kappa3 = 1.422127145. Overlap = 0.941510961;
BBP prediction = 0.948673890. Seed-0 matched-control sigma1 =
331.928018816. All top-twelve values and residuals appear in
`results/phase1_2026-10-24.json`. Completed arithmetic and control components took
911.343 seconds, excluding the abandoned control attempt.

- **PASS** — `kappa3 in [1.38, 1.47]`.
- **PASS** — `cubic top-singular-vector overlap with conj(g~) within 0.03 of sqrt(1 - D/theta^2)`.

RS-1 becomes **STRESSED at X = 320000**: both of its committed Phase-1 predictions pass.
The pre-registered X = 640000 test has not been run.

**Quartic result (completed, with matched control):**

X = 320000, D = 27542; sigma1 = 405.346301128, theta = 319.010616411,
theta/sqrt(D) = 1.922239066, against the committed formula's
1.924228662. Seed-0 matched-control sigma1 =
331.545164828; all top-twelve singular values and residuals are in the JSON.
Arithmetic plus control took 821.456 seconds.

- **PASS** — `quartic theta_n = 0.166*ln X - 0.18 +- 0.05`.

RS-3 becomes **STRESSED at X = 320000** for its committed Phase-1 growth prediction.
The interpretation of its singular vectors remains unverified by this unit.

**Quadratic result (completed, with matched control):**

X = 320000, D = 27607; sigma1 = 313.743144015, sigma1/(2 sqrt(D)) =
0.944136181. A real supercritical BBP strength is undefined below the bulk edge
(`theta: null` in JSON). With 128 real Rademacher probes and seed 1,
m4 estimate = 1.879653606, standard error = 0.002092727.
The registered correction is 1.230641123, with standard error
0.021399855. Seed-0 matched-control sigma1 =
332.095659511. All top-twelve spectra and probe values are in the JSON.
The required arithmetic-plus-control job took 1481.641 seconds.

- **PASS** — `quadratic (2 - m4)*ln D in [1.0, 1.4]`.

RS-4 becomes **STRESSED at X = 320000**. All four committed Phase-1a comparisons now pass.
RS-2 and RS-6 remain PILOT; RS-5 remains UNTESTED.

**Additional null diagnostic (EXPLORATORY, not a status driver):**

The same quadratic seed-0 control has m4 estimate 2.002133525, standard error
0.002261309, with 128 probes and probe seed 1. The command and code commit are
recorded with the control probe values in JSON. This separate diagnostic took
147.194 seconds.

**X = 640000 skipped:**

Steps 1–4 were complete, and all required X = 320000 family/control jobs finished below the
45-minute cap. This container enforces two CPU-equivalents and 8 GiB RAM, despite four OpenMP
threads being configured. Planning-only prime counts give dimensions 52008 (cubic),
52046 (quartic), and 52073 (quadratic) at X = 640000. Scaling each measured required job by
(D640000/D320000)^2 with the iteration count held fixed projects 54.11,
48.89, and 87.86 minutes, respectively. These are forecasts,
not measured larger-scale runtimes, and exclude the extra control-moment diagnostic. Every
projection exceeds 45 minutes. RAM would fit byte storage; runtime is the deciding limit.
No matrix or spectrum at X = 640000 was computed. Its committed predictions remain unchanged
and untested. The exact dimension counts, projection formula and runtimes are in JSON.

**Closeout and outgoing state (supersedes the opening current-state snapshot):**

- Phase 1a is complete at its required X = 320000 target. All four registered comparisons PASS.
- RS-1, RS-3 and RS-4: STRESSED at this scale. RS-2 and RS-6: PILOT. RS-5: UNTESTED.
- No theorem or mechanism was established; no sextic or quintic computation was performed.
- The paused DISCOVERY-1 records were not changed. Matrices remain uncommitted in ignored data/.
- Engine, validation, arithmetic results, controls and prediction comparisons were committed and
  pushed incrementally. Key checkpoints: `14782d3` (initial engine), `598dc22` (initial gate),
  `2a9043d` (contiguous adjoint), `5f62af6` (replacement gate), `274c633`/`26c3971` (cubic),
  `7ab6b47`/`d4020e5` (quartic), `44a6600`/`23d7e1a` (quadratic), `a876cde` (all comparisons),
  and `bb6560c` (control m4). Final closeout commits follow these on `rs-s002-phase1a`.
- Validation: byte equality, SciPy comparison, complex adjoints, dense-moment comparison,
  strict C compiler checks, targeted Ruff, and 343 passing pytest tests. Repository-wide
  frozen D1 Ruff findings were not repaired.
- No owner-decision blocker. Main was not merged.
- Next dependency: Phase 1b, test the untested sextic boundary (RS-5) and one pre-registered
  local-spacing prediction (RS-6). These are the remaining empirical Phase-1 dependencies.
  Exactly one RS-S003 prompt is in `NEXT_SESSION_PROMPT.md`.


### RS-S003 (2026-10-24): Phase 1b, sextic boundary and local gap ratios

**Stage:** certification and falsification.

**Bounded task:** the owner requested "Continue next session here" after RS-S002. Continue from
committed handover `52d0854` on `rs-s003-phase1b`; authoritative main is still `9a038fa` and is not
merged. Test the untested sextic case of RS-5 and one local gap-ratio prediction of RS-6.

**Pre-registration:** before any sextic spectral computation or local statistic, the exact
criteria, indices, character normalization, null model, deflation/window/tie rules, scales,
solver parameters and seeds were written to CONJECTURES.md and
`results/phase1b_2026-10-24.json` and committed/pushed. RS-5 has two criteria at each of
X = 40000 and 160000; RS-6 has one criterion for each of cubic/quartic at X = 20000 and 40000.
All applicable predictions must pass for promotion, with scope limited to the tests performed.
No mechanism derivations, quintic family, or paused D1 work are included.

**First registered sextic result: X = 40000, D = 4178.**

Sigma1/(2 sqrt(D)) = 1.029470034; matched control =
0.996124577; normalized excess = 0.033345457.
The required job took 24.554 seconds. All top-twelve singular values,
residuals, code commits, commands, seeds and file hashes are in the RS-S003 JSON.

- **FAIL** — `sextic sigma1/(2 sqrt(D)) <= 1.02`.
- **FAIL** — `sextic (sigma1 - control_sigma1)/(2 sqrt(D)) <= 0.02`.

This is the first failing registered scale checked; no smaller registered sextic scale
exists in this unit. RS-5 cannot be promoted. The registered finite-scale formulation is
REFUTED; these finite calculations do not disprove an eventual asymptotic limit.
The X = 160000 run remains scheduled unchanged, and no prediction or normalization is revised.
