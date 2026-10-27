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

**Second registered sextic result: X = 160000, D = 14640.**

Sigma1/(2 sqrt(D)) = 1.041519910; matched control =
0.998855152; normalized excess = 0.042664758.
Completed arithmetic plus resumed control took 258.876 seconds.

- **FAIL** — `sextic sigma1/(2 sqrt(D)) <= 1.02`.
- **FAIL** — `sextic (sigma1 - control_sigma1)/(2 sqrt(D)) <= 0.02`.

Both criteria fail at both registered scales. The first registered failing scale is X = 40000;
no assertion about the globally smallest failing X is made. The original character definition,
normalization, control and tolerances were not changed after seeing either result.

**Registered local-statistics results:**

| mode | X | D | arithmetic mean ratio | control mean ratio | absolute difference | outcome |
|---|---:|---:|---:|---:|---:|---|
| cubic | 20000 | 2248 | 0.422538122 | 0.528322607 | 0.105784485 | FAIL |
| cubic | 40000 | 4178 | 0.410355005 | 0.533655860 | 0.123300854 | FAIL |
| quartic | 20000 | 2250 | 0.538972970 | 0.601537355 | 0.062564385 | FAIL |
| quartic | 40000 | 4170 | 0.532925836 | 0.605604066 | 0.072678229 | FAIL |

- **FAIL** (cubic, X = 20000) — `abs(mean_bulk_gap_ratio - control_mean_bulk_gap_ratio) <= 0.03`.
- **FAIL** (cubic, X = 40000) — `abs(mean_bulk_gap_ratio - control_mean_bulk_gap_ratio) <= 0.03`.
- **FAIL** (quartic, X = 20000) — `abs(mean_bulk_gap_ratio - control_mean_bulk_gap_ratio) <= 0.03`.
- **FAIL** (quartic, X = 40000) — `abs(mean_bulk_gap_ratio - control_mean_bulk_gap_ratio) <= 0.03`.

The RS-6 finite local-statistic extension is REFUTED; the original bulk quarter-circle and
no-secondary-term claim remains PILOT. This scalar local test does not settle those bulk
claims, eventual asymptotic limits, or Tracy-Widom fluctuations. Raw full singular spectra,
window bounds, deflation and ratio counts, seeds, commands and code commits are in the JSON.

**Certification, execution incident and limitations:**

- Exact sextic normalization (square = cubic, cube = field quadratic), multiplicativity, and
  pairwise reciprocity were tested in pure Python; native entries, signs and complex adjoints
  agree. At X = 2000 the sextic matrix and full sign mask agree exactly with the independent
  Python calculation, and top-eight singular values agree with SciPy within 1e-8 relative.
- The quad/cubic/quartic overlap gate was rerun: matrices byte-identical at X = 20000, top-eight
  singular values agree with SciPy at X = 40000, and stochastic m4 is within two standard
  errors of its dense reference. The largest legacy relative discrepancy is 5.107e-15; sextic
  discrepancy is 5.773e-15. The full-SVD top-eight checks also pass on both X = 40000 local jobs.
- The registered window, strict deflation and tie conventions were checked on known arrays.
  The recorded full spectra independently reproduce every saved gap-ratio statistic.
- Targeted Ruff and strict native compiler checks pass; pytest passes 345 tests.
- A documentation push overlapped the X = 160000 arithmetic checkpoint push and GitHub rejected
  one ref update. The committed arithmetic result was pushed serially; only the missing
  control was resumed. Push retry/resume handling and the incident are retained. No numerical
  method, seed or prediction changed. All required jobs remained below 45 minutes.
- The null matches the registered reciprocity constraints. Whether other exact identities
  also need matching was not certified; no explanation of the failures is claimed.
- No mechanism derivations, quintic computation, paused D1 work or main merge was performed.
  RS-S002 evidence and all earlier predictions are unchanged; matrices remain uncommitted.

**Commits:** `4ae9c7a` (registration, pushed before data), `a0c6e2c` (engine/tests/runner),
`10dfba6` (validation), `31f2647`/`07ed9c2` (first sextic), `c693bad`/`80e2d66`
(second sextic), `ce669a0` (checkpoint incident/resume), and local-statistics checkpoints through
`bea27ab`. Final closeout follows on `rs-s003-phase1b`.

**Outgoing state (supersedes earlier snapshots):** Phase 1b complete; eight finite comparisons
FAIL, zero PASS. RS-5 registered finite-scale form REFUTED; its eventual asymptotic version
remains unresolved. RS-6 finite local extension REFUTED, original bulk claim PILOT. RS-1,
RS-3 and RS-4 remain STRESSED from RS-S002; RS-2 remains PILOT. X = 640000 is still untested.

**Next dependency and justification:** before assigning a mechanism to these failures, certify
the null ensemble against all exact matrix identities, then test a qualified model at fresh
scales. That is one RS-S004 / Phase 1c unit, with a single prompt in NEXT_SESSION_PROMPT.md.
No owner-decision blocker is active.

### Owner-session note (2026-10-25): null-model defect behind the RS-6 FAIL (EXPLORATORY)

Not a numbered session and not a status driver; RS-S003's eight registered FAIL outcomes are
immutable. The cubic and quartic matrices satisfy `(conj π/conj ρ)_n = conj((π/ρ)_n)` exactly,
`(π/conj π)₃ = 1` for every cubic index, and the quartic `(π/conj π)₄` entries are forced. The
RS-S003 controls matched reciprocity only. A control imposing the conjugation identity and copying
the forced entries gives, at X = 20000, bulk gap ratios 0.430/0.435 against arithmetic 0.422
(cubic) and 0.535/0.542 against 0.539 (quartic): inside the old 0.03 tolerance. Corrected control
`σ₁/edge` is 1.011–1.013 (cubic) and 0.991–1.001 (quartic), so the cubic outlier (1.341 at this X)
is unaffected; quartic and sextic margins need re-measurement. Code:
`scripts/conjugation_null_diagnostic.py`; data: `results/conjugation_null_diagnostic_2026-10-25.json`.
`NEXT_SESSION_PROMPT.md` (RS-S004) now names this identity as the hypothesis to certify.

### RS-S004 (2026-10-25): Phase 1c, certified conjugation-matched null and fresh-scale tests

**Stage:** certification and falsification. **Branch:** `ccr-c363c6bb-0zejeu`, based on main
`965a392`, which already contains RS-S003. Main was not merged.

**Identity audit (exact):**

- Galois equivariance gives `(conj x/conj y)_n = conj((x/y)_n)` for n = 3, 4 and 6. For n = 6,
  conjugation also inverts `ζ₆ = 1 + ω`.
- Primary primes map to primary primes of the same norm.
- The reciprocity mask is conjugation-invariant.
- The two identities force `(π/conj π)_n` to satisfy `x = s·conj(x)`:
  - cubic: `x = 1`;
  - quartic: `x ∈ {±1}` or `{±i}`, by `p mod 8`;
  - sextic: `s = +1` and `x = ±1`.
- For the cubic matrix, `H = C·P` is exactly Hermitian and real in a real basis.
- The sextic mask is a function of (a, b) mod 4 classes. It is not of parity form.
- Conjugation is the only nontrivial Galois automorphism, and units do not act on the primary
  index set. No further identity was found; completeness is not claimed.
- The quadratic null is unchanged.

These checks are three new pure-Python or native tests (`tests/test_reciprocity_spectra.py`),
including a byte-level pure-Python SplitMix reference for the new native control
`rs_random_conj`. That control draws one exponent per {transpose, conjugation} orbit and copies
the (π, conj π) entries.

**Validation:** `phase1c.py validate` at X = 20000 for cubic, quartic and sextic:

- zero identity violations in both the arithmetic and control matrices;
- cubic and quartic matrices sha256-identical to RS-S002;
- top-8 Lanczos values agree with SciPy `svds` within 8.0e-15 relative;
- control complex matvec and adjoint products agree with dense products within 1e-12;
- the control's `C·P` is Hermitian.

Targeted Ruff and a strict `-Wall -Wextra -Werror` compile both pass, and pytest passes 348 tests.

**EXPLORATORY (results JSON, not status drivers):**

| mode | X | arithmetic gap ratio | control gap ratio (seeds 0–2) |
|---|---:|---:|---|
| cubic | 20000 | 0.4225 | 0.416, 0.426, 0.412 |
| cubic | 40000 | 0.4104 | 0.430, 0.412, 0.435 |
| quartic | 20000 | 0.5390 | 0.534, 0.528, 0.534 |
| quartic | 40000 | 0.5329 | 0.546, 0.541, 0.520 |

- Cubic and quartic corrected-control `σ₁/edge` is 0.997–1.008.
- Sextic excess over the corrected control is 0.0325 at X = 40000 and 0.0421 at X = 160000. The
  RS-5 failure is therefore not a null artefact.
- The owner diagnostic is reproduced qualitatively, with independent code and a different RNG.

**Pre-registration:** `ed4961d`, pushed before any X = 80000 or 320000 data. The predictions
are in `CONJECTURES.md` and in the JSON.

**Registered outcomes:** all five PASS (table in `CONJECTURES.md`).

| job | value | runtime |
|---|---|---:|
| cubic, X = 80000 | gap difference 0.0071; outlier excess 0.513 | 342 s |
| quartic, X = 80000 | gap difference 0.0021; outlier excess 0.141 | 346 s |
| sextic, X = 320000 | excess 0.0504; Gram residuals ≤ 2.2e-12 | 1281 s |

**Status:**

- RS-6C (new): STRESSED at X = 80000.
- RS-7 (new): STRESSED at X = 320000.
- RS-1 and RS-3: STRESSED, with corrected-null margins confirmed.
- RS-4: STRESSED, unchanged.
- RS-2: PILOT.
- RS-5 finite form and the RS-6 local extension: REFUTED, unchanged.
- X = 640000: untested.

**Commits:** `e486a07` (control, tests, runner), `0ca553b` (validation), `49c6102`–`5d9aa8a`
(exploratory), `ed4961d`/`fb2b681` (registration), `6df598b`, `468a075`, `c934b55`
(registered outcomes), then the closeout.

**Limitations:**

- Each registered comparison uses one control seed.
- The gap-ratio statistic has a seed spread of about 0.01–0.025 at D ≈ 4000.
- The ensemble constants and the sextic mechanism are not derived.
- Matrices are not committed. No D1 records were touched.

**Next dependency:** identify the sextic outlier cluster (RS-7): its multiplicity above the
corrected null, and its singular vectors against sextic and cubic Gauss-sum candidates. This
is one RS-S005 / Phase 1d unit.

### RS-S005 (2026-10-25): Phase 1d, sextic outlier cluster (RS-7)

**Stage:** discovery, then falsification. **Branch:** `ccr-c363c6bb-0zejeu`, continuing directly
from RS-S004 at the owner's request ("keep going"). Main was not merged.

**Exact work:**

- Added `sextic_gauss_sum` and `sextic_jacobi_sum` to `arith.py`.
- New tests check `|g6|² = p` and `g6² = J(χ6,χ6)·g3`, and that native `sexticg` output matches
  Python at X = 400.
- Noted from existing exact tests: the sextic matrix equals conj(cubic matrix) ∘ (field-quadratic
  symbol matrix), entrywise.

**EXPLORATORY** (`scripts/phase1d.py`, `results/phase1d_2026-10-25.json`):

| | X = 40000 | X = 160000 |
|---|---:|---:|
| values above the largest of seeds 0–2 controls | 7 | 22 |
| IPR·D of the cluster vectors | 1.96–2.13 | 2.19–2.58 |
| conj(g̃6) projection onto the top-24 subspace | 0.258 | 0.238 |
| conj(g̃6) Rayleigh quotient / edge | 0.677 | 0.689 |
| family enrichment, conj(g̃6) twists, N(u) ≤ 60 | 1.55 | 2.35 |

- The cluster vectors are delocalized, with no concentration on small primes or residue classes.
- conj(g̃6) is the best single candidate, but its Rayleigh quotient is well below the cluster's
  σ/edge of about 1.03.
- The g6, g3, conj g3 and constant twist families sit at the random level.
- At X = 40000 the bulk m4 equals the control's, and the upper tail is stretched.
- The first X = 40000 pass ran before the diagnostics were added. It is retained as
  `superseded_exploratory`.

**Pre-registration:** `f3a1b75`, pushed before any X = 320000 data.

**Registered outcomes (X = 320000, D = 27554):**

| prediction | value | outcome |
|---|---:|---|
| P7M multiplicity | 34 | **PASS** |
| P7F enrichment | 2.962 | **PASS** |

- The arithmetic job (top 48) took 1419 s, and the control job took 484 s.
- The maximum Gram residual is 3.4e-14.

**Status:**

- RS-7a (new): STRESSED at X = 320000. The identification is partial.
- All other statuses are unchanged.

**Validation:** targeted Ruff passes, the strict compile passes, and pytest passes 350 tests.

**Commits:** `a562069`, `754330c`, `0dc8836`, `35545ce`, `0cc7e53`, `f3a1b75`/`9822ae3`
(registration), `511a8e2`, `a1235b8`, then the closeout.

**Limitations:**

- Multiplicity at the registered scale uses one control seed.
- The family uses N(u) ≤ 60 only.
- The enrichment ratio depends on the family dimension.
- No mechanism is derived.

**Next dependency:** measure the per-twist strengths, i.e. the Rayleigh quotients of
conj(g̃6)·(u/π)₆ as a function of N(u). Then test whether the number above threshold predicts
the cluster multiplicity. This is one RS-S006 unit.

### RS-S006 (2026-10-25): per-twist sextic spike strengths and the primary-class dichotomy

**Stage:** discovery, then falsification. **Branch:** `ccr-c363c6bb-0zejeu`. At the start of the
session, and on the owner's instruction, RS-S004/S005 were merged to main as `10153fd`.

**EXPLORATORY** (`scripts/phase1e.py`, `results/phase1e_2026-10-25.json`): the Rayleigh quotient
`r_u = ‖C conj(g̃6)(u/π)₆‖/√D` was computed for every twist.

| X | N(u) ≤ | twists |
|---:|---:|---:|
| 40000 | 300 | 2094 |
| 160000 | 300 | 2094 |
| 20000 | 100 | 492 |
| 80000 | 100 | 492 |

At X = 40000 and 160000 the runs also included family capture, a compressed Gram matrix and a
cluster count.

**Findings:**

1. **No twist is individually supercritical.** The maximum is r₁ = 1.379 at X = 160000, against
   the threshold √2. The individual twist-count model predicts 0 outliers, against 7 and 22
   observed: **FAIL**.
2. **The collective random-left-direction model is wrong.** It gives 15–17 outliers at
   σ₁/edge ≈ 1.017, against 7 observed with σ₁/edge 1.0295
   (`phase1e_model_diagnostic.py`): **FAIL**. The left images of the strongest twists are partly
   aligned: maximum |corr| 0.37, against 0.048 for the control.
3. **Exact symmetry.** Twisting by (−1/π)₆ leaves r unchanged. This follows from
   g6(conj π) = (−1/π)₆·conj(g6(π)) and the conjugation identity; the null already shares it.
4. **Dichotomy.**
   - Every "+" twist by a ±primary u has r ≥ 1.117.
   - Every other associate coprime to 3 has r ≤ 0.980.
   - Ramified 1 − ω is strong with the conjugate sign.
   - The "−" twists stay near the random level, except for a few by ramified-divisible u.

**Pre-registration:** `feca6a1`, pushed before any Rayleigh data at X = 320000 or 640000.

**Registered outcomes:** all four PASS (table in `CONJECTURES.md`).

| X | runtime |
|---:|---:|
| 320000 | 356 s |
| 640000 (D = 52008) | 1172 s |

These are the first sextic data at X = 640000. There, r₁ = 1.4183 > √2.

**Status:**

- RS-7b (new): STRESSED at X = 640000.
- RS-7a: STRESSED. Its quantitative multiplicity model is still open.
- All other statuses are unchanged.

**Validation:**

- Targeted Ruff passes, and pytest passes 350 tests.
- No new exact functions were added; the twist symbols reuse the tested `sextic_symbol`
  convention.
- Matrices are not committed.

**Commits:** `15b53f0`–`8aae078` (exploratory), `4def9cf`, `0d38368`, `4183876`, then
`feca6a1`/`3cfeb05` (registration), `d6f96eb`, `cc07a91` (registered outcomes), `128d3de`
(model diagnostic), then the closeout.

**Limitations:**

- The dichotomy and strengths are finite-range observations.
- The mechanism has not been checked exactly.
- The cluster-multiplicity model is unresolved.
- No expert review has taken place.

**Next dependency (mechanism stage):**

- Verify exactly that, for ±primary u, `(u/π)₆ = ε(u, π)·(π/u)₆`, where ε is a simple sign
  determined by sextic reciprocity.
- Derive the associate sum rule implied by the depletion of non-primary associates.
- Compare the profile of `r_u² − 1` against N(u) with a twisted-Gauss-sum heuristic.

This is one RS-S007 unit.

### RS-S007 (2026-10-25): mechanism stage for RS-7b

**Stage:** mechanism. **Branch:** `ccr-c363c6bb-0zejeu`. At the start of the session, on the
owner's instruction, main was fast-forwarded to RS-S006 (`1971fea`).

**Exact work:**

- Added `test_sextic_unit_symbols_are_characters_of_the_norm`. It proves that the
  associate-class factor `ζ₆^{j(p−1)/6}` is a character of p mod 36, and that it is unramified at
  3 exactly for u′ = ±u.
- Verified the associate sum-rule identity to a relative error of 2.3e-16.

**Reformulation of RS-7b.** A twist is enhanced exactly when its unit-class factor is unramified
at 3, in every case checked.

**Diagnostics** (`scripts/phase1f.py`, X = 2·10⁴ to 6.4·10⁵, no new matrices beyond X = 20000):

- the associate excess drifts from 0.04 to 0.75;
- the strength exponent in N(u) is about −0.19, so the naive theta heuristic, which predicts
  −2/3, FAILS;
- the unramified-class Gauss-sum bias is the largest at every X ≥ 40000 but is only marginal.

No fresh-scale prediction emerged, so none was registered.

**Validation:** pytest passes 351 tests, and targeted Ruff passes.

**Commits:** `7bb8406` and its parent, then the closeout.

**Status:**

- RS-7b: STRESSED, with its mechanism UNEXPLAINED. The algebraic reformulation is exact.
- All other statuses are unchanged.

**Assessment.** The empirical findings are now sharp and pre-registered. They are:

- the certified null;
- RS-6C;
- the sextic cluster (RS-7, RS-7a);
- the primary-class dichotomy (RS-7b), tested to X = 6.4·10⁵.

The remaining questions are theoretical: why unramified twists are enhanced, the N(u)^−0.19
profile, and how a cluster forms from subcritical spikes. These are what an expert in
metaplectic forms should be asked.

**Next dependency:** draft the external expert-review note and refresh the collision audit. This
is one RS-S008 unit.

### RS-S008 (2026-10-25): collision-audit refresh, expert-review note, Astra prompt

**Stage:** collision audit, then write-up. **Branch:** `ccr-c363c6bb-0zejeu`. At the start of the
session, on the owner's instruction, main was fast-forwarded to RS-S007 (`90e85e7`).

**Owner direction.** The external expert is OpenAI's Astra agent. The questions are to be built
into the prompt. Following PROTOCOL and the RS-S008 prompt, this session contacts no one: the
prompt is prepared for the owner to send.

**Work:**

- **`PRIOR_ART.md` refresh.** Added the sextic theta-function literature:
  - Chinta–Friedberg–Hoffstein 2011;
  - Bröker–Hoffstein, Math. Comp. 2015;
  - Friedberg–Ginzburg, arXiv 1403.3930;
  - arXiv 2301.05329 on sextic Gauss-sum equidistribution.

  Per-finding statuses: RS-7b is POSSIBLE_OVERLAP / NOVELTY_REQUIRES_EXPERT_REVIEW; RS-6C and
  RS-7/7a are SEARCHED_NO_COLLISION_FOUND; the exact null identities are KNOWN_IMPLIED.
- **`NOTE_DRAFT.md`.** Covers the setup, the certified null, six tables, the sextic findings with
  all failures, the open questions, prior art and reproducibility.
  - Every table is generated by `scripts/note_tables.py` from the results JSONs.
  - The new test `test_note_tables_match_results` enforces this in CI.
- **`ASTRA_PROMPT.md`.** A self-contained, ready-to-paste referee prompt for Astra, with
  findings F1–F6 and questions Q1–Q5:
  - Q1: mechanism of the unramified-at-3 dichotomy;
  - Q2: strength law;
  - Q3: cluster model;
  - Q4: prior art;
  - Q5: the sharpest falsifying test.

  It asks for known / derivable / conjectural answers to be separated, with citations and
  falsifiable predictions.

**Validation:** pytest passes 352 tests; targeted Ruff passes; `note_tables.py --check` passes.
No new computation was run and no statuses changed.

**Owner-decision blocker (type: external input).**

- Continuation needs Astra's reply. Sending it is the owner's decision and action.
- To unblock: send `reciprocity_spectra/ASTRA_PROMPT.md` (optionally attaching
  `NOTE_DRAFT.md`), then commit the reply verbatim as
  `reciprocity_spectra/ASTRA_RESPONSE_<date>.md`.
- RS-S009 would then evaluate the reply under the evidence and novelty rules, and pre-register
  the falsification test it proposes.
- `NEXT_SESSION_PROMPT.md` is suppressed until then.

### RS-S009 (2026-10-25): evaluating the Astra referee response

**Stage:** falsification and mechanism. **Branch:** `ccr-c363c6bb-0zejeu`. Main was already at
RS-S008 (`c295f9c`). The owner sent a trimmed version of the Astra prompt; the response is
committed verbatim as `ASTRA_RESPONSE_2026-10-25.md`.

**A prompt error, recorded.** The trimmed prompt said the cubic case has "one" outlier. RS-2
already records several. Astra's check 2 caught the inconsistency.

**Claims checked:**

- **Exact symmetry r_u = r_{−ū}.** It holds to 1.2e-15 on every existing twist run, with up to
  2090 pairs per scale. It also confirms that our 1−ω data were consistent; there was no bug.
- **Hasse–Davenport factorization.** g̃6(ρ) = conj((2/ρ)₃)·(ρ/|ρ|)·g̃₂·conj(g̃₃(ρ)) holds to
  4.6e-15 for every prime up to 3000. It is now `test_sextic_gauss_sum_hasse_davenport_factorization`.
- **Its consequence.** A unit twist ζ₆ʲ rotates the cubic frequency by a character ramified at 3,
  unless j ∈ {0, 3}. This gives a derivable explanation of the structure of RS-7b.
- **Sextic scaling.** The prediction N(u)^{−1/6} with X^{1/6}/log X agrees with the measured
  exponent of −0.19 and with the flat ratio for r₁. This is already in the existing data; there
  was no new test.
- **Astra's cubic calibration.**
  - Registered at `81aa006`/`9165700`, before the data.
  - RS-S009-A2-exponent: FAIL (fit undefined).
  - RS-S009-A2-count: FAIL (19 < 24).
  - Diagnosis: non-squarefree u are suppressed.
- **Corrected predictions.** Registered at `98118bf`, before the X = 160000 data; all three PASS
  (RS-8).

**Validation:** pytest passes 353 tests, and targeted Ruff passes.
`scripts/phase1g.py` records its classifier, commands and commits in
`results/phase1g_2026-10-25.json`.

**Status:**

- RS-8 (new): STRESSED at X = 160000.
- RS-7b: STRESSED. Its structure is now partly derivable through the Hasse–Davenport
  factorization, and its mechanism is no longer purely empirical. Astra's claim that non-cube
  rotations kill the residue is still a conjecture.
- All other statuses are unchanged.

**Next dependency.** Astra's decisive test (Q5): Kubota partial sums T_j(X) over squarefree n
coprime to 6, in the Heath-Brown–Patterson normalization. The prediction is a slope of 2/3 for
j ∈ {0, 3} and 1/2 otherwise. Q3, the excess spectrum of a compressed twist basis against the
cluster sizes 7/22/34, follows if time allows. This is one RS-S010 unit.

### RS-S010 (2026-10-25): Astra's decisive test (Q5)

**Stage:** falsification and mechanism. **Branch:** `ccr-c363c6bb-0zejeu`. At the start of the
session, on the owner's instruction, main was fast-forwarded to RS-S009 (`e10dec3`).

**Exact work:**

- Trace-form sextic Gauss sums `kubota_g6_prime`, including inert primes.
- Tests:
  - |g|² = N(π);
  - g_ours = (π̄/π)₆·g_HBP, Astra's check 3;
  - unit-frequency rotation;
  - twisted multiplicativity, by direct summation for split × split, π × π̄ and split × inert
    moduli.
- `test_conjugate_ratio_symbol_is_two_adic`.
- Engine `RS_NO_MATRIX` mode. Its Gauss sums and metadata are byte-identical to a full build, and
  the full-build hash is unchanged.

**EXPLORATORY** (to X = 3.2·10⁵; `scripts/phase1h.py`, `results/phase1h_2026-10-25.json`):

- In the trace form the main terms sit in j = 1, 2 and 4, 5, not in 0, 3. This is opposite to
  Astra's prediction.
- At primes, the matrix normalization puts the bias in j = 0, 3.
- The multiplicative extension ψ(n) = Π(π̄ᵢ/πᵢ)₆ over composites gives no clean main term.

**Registered:** `e745eaa`, before the X = 1.28·10⁶ data. The run took 649 s, with D = 98512.

| prediction | outcome |
|---|---|
| Astra's Q5 as stated | **FAIL** |
| K1-trace | **PASS** |
| K2-primes-matrix-norm | **PASS** |

**Correction recorded.** Astra's check 3 was right that the factor is purely 2-adic. My earlier
claim to the contrary is withdrawn.

**Status:**

- RS-9 (new): STRESSED at X = 1.28·10⁶.
- RS-7b: STRESSED. It is now tied to a prime-level Gauss-sum bias confirmed at a fresh scale.
- Astra's literal Q5 explanation: FAIL as stated.
- The 2-adic/3-adic interplay: open.

**Validation:** pytest passes 355 tests; targeted Ruff passes; the strict C compile passes.

**Next dependency.** Map the full selection rule. Over primes and over squarefree n, measure the
main term for every pair (unit class j, character χ of (ℤ[ω]/4)^× or the relevant 2-adic group).
Identify exactly which pairs carry a main term, register the table, and test it at a fresh scale.
This is one RS-S011 unit. It will yield the crisp statement to send back to Astra and to human
experts.

### Owner decisions (2026-10-25, recorded before RS-S011)

- RS-S010 was merged to main (`18bb011`).
- The owner set two rules, now recorded as PROTOCOL §9:
  - proof work targets the hard, prime-level and matrix-level version first;
  - no external human reviewer is required to proceed; a deep novelty audit is required before
    any publication or formal submission.
- RS-S011 is amended so that it ends by freezing CAND-001 and drafting the hard-version proof
  route.

### RS-S011 (2026-10-25): selection table, CAND-001 frozen, hard-version proof route

**Stage:** falsification, then the start of the proof stage. **Branch:** `ccr-c363c6bb-0zejeu`.
Main is at `18bb011` plus the owner-decision commit `4a19e31`.

**Exact work.**

- `arith.mod4_class_coordinates` and `mod4_character`: (ℤ[ω]/4)^× = ⟨ω⟩ × ⟨−1⟩ × ⟨1+2ω⟩.
- New tests:
  - (2/ρ)₃ = χ(1,0,0);
  - (−1/p) = χ(0,0,1);
  - (ρ̄/ρ)₆ is a class function mod 4 but not a character. Exactly,
    ψ = ½(χ₀₀₀ − χ₀₀₁ − χ₀₁₀ − χ₀₁₁).
- Engine option `RS_GAUSS_MIN`, for disjoint norm windows. It was verified to give identical
  Gauss sums above the cut.

**EXPLORATORY.** The 6 × 12 table of (unit class, character) biases out to 1.28·10⁶ suggested
main terms only for characters with trivial cubic part, and within those for s1 = 1.

**Registered.**

| test | window | outcome | detail |
|---|---|---|---|
| RS-S011-SEL (`e8821be`) | 1.28·10⁶ < p ≤ 1.92·10⁶ | **FAIL** | the even, trivial-cubic group averaged 2.05 |
| RS-S011-M0 (`6bbb11b`) | 1.92·10⁶ < p ≤ 2.56·10⁶ | **FAIL** | the trivial-cubic group averaged 1.35 |

A power calculation done after the fact shows that the window statistics are underpowered.

**CAND-001 frozen** in `research/CONJECTURE_REGISTER.md`. It is the first CAND in PRIMES, and
contains only what passed registered fresh tests:

- statement 1, the matrix dichotomy (RS-7b);
- statement 2, the prime-level unit-class bias (RS-S010-K2).

**`PROOF_ROUTE.md`** follows PROTOCOL §9 (hard version first):

- reduction of statement 1 to a twisted sextic dispersion estimate, the analogue of
  Dunn–Radziwiłł;
- a Heath-Brown decomposition into Type I (Kubota residues, T1) and Type II (bilinear sextic sums,
  T2; the expected crux, with X^{1/6} of room);
- a table of inputs marked known, conditional or open;
- next steps.

**Validation:** pytest passes 356 tests; targeted Ruff passes; the strict compile passes.

**Commits:** `a9c0634`, `e8821be`, `c0a552b`, `6bbb11b`, `874e5e4`, `dc17534`, then the closeout.

**Next dependency (hard route, step 1).** Verify exactly that

```
‖C w_u‖² = D(D − 1) + off-diagonal = Σ_π |S(πu)|²,
```

and measure how much of the off-diagonal term the S(πu) main terms carry. Then start T1, the
local theory at 2 and 3, by reproducing the cubic RS-8 from Patterson's explicit coefficients.
This is RS-S012.

### RS-S012 (2026-10-25): exact reduction, cubic calibration, sextic strength law

**Stage:** proof (hard route), mechanism calibration. **Branch:** `ccr-c363c6bb-0zejeu`. At the
start of the session, on the owner's instruction, main was fast-forwarded to RS-S011 (`357e734`).

**Exact.** `test_twist_norm_equals_sum_of_twisted_prime_gauss_sums` verifies the dispersion
reduction (PROOF_ROUTE step 1) for five twists, including non-primary ones.

**Literature input.** The statement of Patterson's cubic theta coefficients is taken from
Dunn–Radziwiłł, arXiv 2109.07463v3, (5.7)–(5.8) and (5.17), fetched in this session.

**EXPLORATORY.**

- The cubic Patterson ratio is constant to 2–4% and converges toward 1.
- The sextic ratio with exponent 1/6 is constant to about 3%, with no squarefree condition: squares
  follow the same law. The earlier fitted exponent −0.19 was finite-size bias.

**Registered** at `0971270`, before the fresh-scale data:

| test | scale | outcome |
|---|---|---|
| RS-S012-PAT-CUBIC | X = 320000 | **PASS** |
| RS-S012-LAW-SEXTIC | X = 10⁶, D = 78462 | **PASS** |

**Changes:** CAND-001 gains statement 3. `PROOF_ROUTE.md` §6 records progress.

**Validation:** pytest passes 357 tests, and targeted Ruff passes.

**Next dependency:** T2, the hard-route crux. Measure the bilinear sextic sums, extract the exact
large-sieve exponents, and state the gap. This is RS-S013.

### RS-S013 (2026-10-26): Type II audit, exact obstruction, local closeout

**Stages:** mechanism, certification, EXPLORATORY measurement, falsification.
**Branch:** codex/rs-s013-type-ii. **Execution:** local Windows, as requested.
Local main and fetched origin/main were both 68d19bd, already containing
RS-S012; the handoff's unmerged-branch note was stale. No cloud compute or
merge was started; checkpoint commits use [skip ci].

**Mathematical result.** The reciprocal sextic-symbol product is a cubic
kernel with an explicit mod-4 sign. Unimodular Gauss factors do not change
its singular values. The generic large-sieve envelope is X^(5/6+epsilon),
above the sextic target by X^(1/6), apart from logs. An arbitrary bounded
coefficient estimate at X^(2/3)/log X is impossible: random column phases
and row alignment give balanced prime-band values of order
X^(3/4)/(log X)^(3/2). Actual arithmetic coefficients remain a separate
unresolved problem. Source statements and hypotheses are in
RS_S013_LITERATURE.md; full interpretation is PROOF_ROUTE.md section 7.

**Measurements.** The implementation/design checkpoint b6556f7 was pushed
before execution. Eight squarefree-ideal supports completed locally,
including inert factors and both split conjugates; c=1, coprime pairs only.
Matched controls use seeds 0,1,2; random coefficients use seed 23.
At dimensions 139 x 139 the norm is 22.4568 and the L2 extremal form is
4.1926 times the numerical target. Results are EXPLORATORY, with no
asymptotic or conjecture promotion: results/type_ii_2026-10-26.json.

**Exact refutation.** The frozen CAND-001 conjunction is REFUTED: u=64=2^6
gives w_64=w_1 and r_64=r_1 exactly, but statement 3 predicts excess ratio
1/4. Statement 1 makes the denominator eventually positive. Statements
1 and 2 themselves are not refuted. Original statements and evidence remain.

**Finite correction.** The RS-S012 scorer wrongly excluded +/-8 in sextic
mode using a cubic-only rule. Rescoring all 80 originally registered stored
rows gives mean 0.9426270886, population sd 0.02148995984; all original
conditions still PASS. The current script is fixed; frozen JSON is unchanged.
The reproducible audit is scripts/audit_strength.py --check; its JSON preserves
original/corrected summaries and historical source provenance.

**Dispersion correction.** The exact diagonal is (D-1)D_u. The old positive
squared-main-term ansatz cannot imply nonprimary suppression; that claimed
full equivalence is withdrawn. The exact sum identity survives.

**Validation.** Targeted Ruff and the audit pass. With PYTHONUTF8=1, the
Windows-compatible suite has 319 passed, 3 skipped. Full pytest was attempted
but three frozen D1 modules fail collection on Unix-only fcntl:
test_e010.py, test_e010_runtime.py, test_e011.py. They were explicitly excluded
from the compatible-suite run. Three native-C tests skip without GCC.
D1 source files were not edited. Independent review rebuilt all eight exponent
hashes and all control norms; Gram eigenvalues agree with SVD norms within
3.2e-14. See results/rs_s013_validation_2026-10-26.json.

**Commits:** implementation/design/source audit b6556f7; result/authority
closeout commit follows this entry on the same branch. Checkpoints are pushed
serially. Main remains at the entry authority until an explicitly requested merge.

**Current state / next dependency:** the generic operator route is exhausted,
not every hard-route method. No all-n/function-field fallback or theorem
graduation is started. RS-S014 is an invariant-formulation audit using exact
sixth-power classes and existing evidence before any fresh registration.
No owner blocker. Exactly one continuation is in NEXT_SESSION_PROMPT.md;
RS-S014 is not executed here.

### RS-S014 (2026-10-26): sixth-power-class audit of the strength law

**Stages:** falsification and certification. This audited stored evidence only; no new matrices
were built.

**Branch and execution.** Branch `ccr-c363c6bb-0zejeu`, in the cloud session. At the owner's
request, main was first fast-forwarded to RS-S013 (`db46d65`), and RS-S014 was then run here. The
handoff had assumed a local Windows run; the scope was kept: no fresh-scale matrices, no new CAND,
no merge of RS-S014, no fallback.

**Exact work.**

- New functions:
  - `arith.eisenstein_factorization`, which factors via the rational norm;
  - `sixth_power_free_norm`;
  - `sextic_twist_class`.
- New test `test_sextic_twist_classes_sixth_powers_and_inversion` covers:
  - (uv⁶/ρ)₆ = (u/ρ)₆ away from ρ | v, and 0 at ρ | v;
  - (u⁵/ρ)₆ = conj((u/ρ)₆);
  - exact reconstruction of the factorization;
  - invariance of N₆ and of the twist class.
- **Lemma (`RS_S014_INVARIANCE_AUDIT.md` §2).** Any limit of (r_u² − 1)/(r₁² − 1) is invariant
  under u → uv⁶, with explicit error ≪ X^{−1/6+ε}. The proof uses the BGL large sieve; the matching
  of conventions is still a caveat.

**Audit of stored evidence.** `scripts/audit_invariance.py` produces
`results/rs_s014_invariance_2026-10-26.json`, verified with `--check`. The single-prime class
statistic ε·N^{k/6} is:

| X | k = 1 | k = 2 | k = 3 | k = 4 | k = 5 |
|---:|---:|---:|---:|---:|---:|
| 6.4·10⁵ | 0.943 | 0.940 | 0.940 | 0.827 | −0.97 |
| 10⁶ | 0.947 | 0.945 | 0.941 | — | — |

For k = 5 the value is −1.02 to −1.11 when N(π) ≥ 19, and less negative for N = 4, 7, 13. The
patterns (5), (5,5) and (4,5) are never enhanced.

**Obstructions.**

- **O1.** CAND-001 statement 1's universal form is withdrawn. Its ±primary u include the classes
  π⁵, which are the conjugate twists (r₃₂ = r₂⁽⁻⁾ exactly, ≈ 0.97). Its registered tests had
  covered "+" twists with N(u) ≤ 100 only.
- **O2.** The N₆^{−1/6} repair has the wrong sign at exponent 5.

**PROV-RS14** (provisional, class-based; statements (A)–(D)) and a powered falsification plan
(P1–P3) are recorded. No CAND was allocated.

**Maintenance.** The RS-S013 checker `audit_strength.py --check` failed on Linux. The cause: the
record stored the hash of a Windows CRLF checkout. The checker now accepts the line-ending-normalized
content, and the record gains a `sha256_lf` field; its original fields are unchanged. It now
passes.

**Validation:** full pytest passes 363 tests on Linux (no exclusions); targeted Ruff passes; `audit_strength.py --check` and `audit_invariance.py --check` both pass.

**Next dependency.** RS-S015: register P1–P3 verbatim, then run the class tests at X = 10⁶.

### RS-S015 (2026-10-26): registered sixth-power-class tests of PROV-RS14 at X = 10⁶. Prediction block

**Stage:** falsification. **Branch:** `rs-s015-class-tests`. **Execution:** local Windows, as the owner
requested.

**Engine port (before any data).** This machine has MSVC only. `native/residue_engine.c` gains an
`_MSC_VER` path, and the GCC path is unchanged in behaviour:

- 64-bit residue products (X < 2³¹ is enforced);
- the three complex kernels written in explicit real arithmetic, with the same blocking and
  summation order;
- OpenMP loop variables declared outside the loop.

`phase1.compile_engine` builds with `cl /openmp:llvm` on win32. Validation is in
`results/rs_s015_class_tests_2026-10-26.json` (`engine_validation`):

- the sextic matrices at X = 3.2·10⁵ and 6.4·10⁵ are **byte-identical** to the stored Linux
  SHA-256 hashes;
- 42 stored r values at X = 3.2·10⁵ (40 twists and 2 random-phase draws) agree to 5.9·10⁻¹⁶
  relative.

**Exact test.** `test_sextic_class_exponents_match_direct_symbols` checks that the product of
prime-symbol exponents equals (u/ρ)₆ for u = Π π^e. It covers inert 2 and 5, conjugate pairs,
exponents 1–5 and ρ | u.

**Registered before data (verbatim from `RS_S014_INVARIANCE_AUDIT.md` §6).** The setting is X = 10⁶,
w_κ = conj(g̃₆)·Π(π/·)₆^e, and s = ε·N₆^{1/6}.

**Classes.** There are 250:

- singles π^k, k = 1–5, over the 20 smallest primary primes. These include inert (2) and (5); the
  norms run from 4 to 73.
- pairs: all 6 pairs among the 4 smallest primary primes, with (e₁, e₂) ∈ {1..5}².

**Controls.** Ten random-phase vectors and ten conj(g̃₆)·(random sixth roots), with seed 15.

**Predictions.**

- **P1:** over the {1,2,3}-classes, mean s ∈ [0.90, 1.00] and sd ≤ 0.05.
- **P2:** every k = 5 single with 19 ≤ N ≤ 61 has r < 1, and the mean s over N ≥ 19 lies in
  [−1.30, −0.80].
- **P3:** every class containing an exponent 5 has r < 1.02, and every {1,2,3}-class has r > 1.05.
- **P4:** exploratory report on the classes containing exponent 4.

**Pre-data margin note.** Under (A), with r₁ = 1.4342, the smallest expected r is 1.0513, for
(3,3) on N = 7·13. The P3 threshold therefore has a thin margin.

**Decision rule.** Freeze CAND-002 only if P1, P2 and P3 all PASS. A failure of P1 or P3 refutes
PROV-RS14 as stated. The prediction commit hash is recorded in the JSON (`prediction_commit`).

### RS-S015 outcomes (scored verbatim against `552f5b7`; prediction_commit in the JSON)

The record is `results/rs_s015_class_tests_2026-10-26.json` (`runs`, `score`). Runs:

- singles (101 products and 20 controls): 664 s;
- pairs: run separately.

r₁ = 1.4342110940043258 in both parts. This is identical to the stored Linux X = 10⁶ value
(RS-S012). The controls are:

- random-phase: max 1.0043, sd 0.0022;
- conj(g̃₆)·roots: max 1.0022.

| Prediction | Outcome | Numbers |
|---|---|---|
| P1 | **FAIL** | mean s = 0.791, sd = 0.215 over 114 {1,2,3}-classes |
| P2 | **PASS** | max r = 0.982 over 11 k = 5 singles with 19 ≤ N ≤ 61; mean s = −1.050 for N ≥ 19 |
| P3 | **FAIL** | exponent-5 clause PASS (max r = 0.992 over 74 classes); {1,2,3} clause FAIL on 16 classes |
| P4 | exploratory | see the table below |

**The smallest failing class** by N₆ is π₇³·π₁₃², with (a, b) = (−1, −3)³ and (−4, −3)²,
N₆ = 57967 and r = 1.049. Clear failures:

- π₇₃³: r = 1.009;
- (3,3) on π₇·π₁₃: r = 0.998, at the random level.

**Mean s by exponent pattern** (s = ε·N₆^{1/6}; (A) predicts about 0.95):

| pattern | s | pattern | s | pattern | s |
|---|---:|---|---:|---|---:|
| (1) | 0.952 | (1,1) | 0.938 | (4) | 0.190 |
| (2) | 0.863 | (1,2) | 0.866 | (4,4) | −0.072 |
| (3) | 0.577 | (2,2) | 0.844 | (5) | −0.913 |
| (1,3) | 0.859 | (2,3) | 0.717 | (5,5) | −0.844 |
| (3,3) | 0.386 | (1,4) | 0.701 | (4,5) | −1.057 |

**Single-prime trend.** For k = 3, s falls from 0.94 at N = 4 to 0.14 at N = 73. For k = 4, r ≤ 1
when N ≥ 31. The RS-S014 k = 3 and k = 4 evidence came from N ≤ 13 only, where the decay is not yet
visible.

**Disposition.**

- **PROV-RS14 is REFUTED as stated.** (A) fails at exponent 3. (D) fails: classes with every
  exponent in {1, …, 4}, such as (4), (4,4), (3,3) and (3,4), are not enhanced at large N₆.
- (B) survives as a registered PASS (P2).
- Every class containing an exponent 5 has r < 1, which is consistent with the second half of (D).
- Per the decision rule, **no CAND-002 is frozen.** CAND-001 remains REFUTED.

**Validation.**

- Targeted Ruff passes.
- `audit_strength.py --check` and `audit_invariance.py --check` pass. The invariance checker now
  writes POSIX source paths, which fixes a Windows-only mismatch; the record is unchanged.
- Local pytest (`PYTHONUTF8=1`): 321 passed, 3 skipped.
- Windows exclusions: `tests/test_e010.py`, `test_e010_runtime.py` and `test_e011.py`, because the
  frozen D1 experiments import POSIX `fcntl`.
- Without `PYTHONUTF8`, `test_note_tables_match_results` fails on cp1252 decoding; this is a
  Windows locale issue only.

**Commits.**

- `552f5b7`: engine port, runner, test and registration;
- `c953114`: prediction commit;
- `32b88fb`: singles run;
- the pairs run and the closeout commits that follow it.

**Next dependency.** RS-S016 (exploratory): decide whether the exponent-3 and exponent-4 decay is a
finite-X effect or a different class law.

### RS-S016 (2026-10-26): X-dependence of the class excess (EXPLORATORY)

**Stage:** discovery and falsification, exploratory; no registration and no CAND. **Branch:**
`rs-s016-x-dependence`. **Execution:** local Windows, MSVC engine. **Owner direction (this
session):** if the exponent-3/4 decay is a finite-X effect, register a corrected class law;
otherwise pivot to CAND-001 statement 2 plus law (B) and a prior-art audit.

**Work.** `scripts/phase1l.py` reran the RS-S015 single-prime classes at X = 1.6·10⁵, 3.2·10⁵ and
6.4·10⁵ (20 + 20 controls in total per X, seed 16). The decision rule was committed in `4cf7c60`,
before the runs. The record is `results/rs_s016_x_dependence_2026-10-26.json`, and the write-up is
`RS_S016_CROSSOVER.md`.

**Result.**

- T (k = 3, N ≥ 37) = 0.022, 0.129, 0.250 and 0.342 at the four X. This is monotone, with a gain
  of 0.32, so the **verdict is finite-X**.
- The excess collapses in t = N₆/X, with best exponent a = 1.0 for exponents {2,3,4} pooled. The
  curve has a plateau of about 0.85, falls to about 0 near t ≈ 1, and is about −0.1 for t ≫ 1.
- Exponent 5 has the opposite profile: about −1.1 for t ≫ 1, and about −0.2 at small t.
- RS-S015's P1 and P3 failures are crossover effects. Its P2 / law (B) is the large-t regime.

**PROV-RS16** is recorded in §4 of `RS_S016_CROSSOVER.md`:

- (A″): a crossover law with a fixed-class limit c ∈ [0.80, 1.00];
- (B″): the exponent-5 law;
- the dichotomy restated in fixed-class form;
- a falsification plan, Q1–Q4, on fresh classes at X = 10⁶ and 6.4·10⁵.

**Validation.**

- Targeted Ruff passes.
- PYTHONUTF8=1 pytest: 321 passed and 3 skipped, with the fcntl exclusions as in RS-S015.
- Both audit checkers pass.
- No matrices are committed; `data/*.bin` were deleted.

**Next dependency.** RS-S017: register Q1–Q4 verbatim, then run them.

### RS-S017 (2026-10-26): registered fresh-class tests of PROV-RS16. Prediction block

**Stage:** falsification. **Branch:** `rs-s017-fresh-classes`. **Execution:** local Windows, MSVC
engine. X = 1.28·10⁶ is skipped because there is 6.2 GB of free RAM, against a 9.7 GB matrix.

**Fresh classes.** These use only primary primes with 79 ≤ N ≤ 400; none was used in RS-S015 or
RS-S016. That is 58 primes, including inert 11 and 17. There are 440 classes:

- singles π^k, k = 1–5, over all 58 primes;
- pairs (e₁, e₂) ∈ {1..5}² over the 6 pairs of the 4 smallest.

**Scales:** X = 6.4·10⁵ and 10⁶. **Controls:** 10 + 10 per X, seed 17.

**Frozen inputs.** F is the RS-S016 k234 bin table, linearly interpolated in log₁₀ t. Per-class
predictions are in `results/rs_s017_fresh_classes_2026-10-26.json`. A class is "powered" if
σ_s = 0.004·N₆^{1/6} ≤ 0.05; 149 of the 328 no-5 classes are powered.

**Predictions (verbatim from `RS_S016_CROSSOVER.md` §5; "fresh no-5" means powered).**

- **Q1:** every fresh no-5 class with t ≤ 10⁻² has s ∈ [0.70, 1.00], at each X.
- **Q2:** every half-decade bin with at least 4 fresh no-5 classes has |mean s − mean F| ≤ 0.12.
- **Q3:** every fresh class containing a 5 has r < 1, and the π⁵ singles with t ≥ 3 have mean s
  ∈ [−1.25, −0.85], at each X.
- **Q4:** at least 80% of fresh no-5 classes with 10^{−1.5} ≤ t(10⁶) ≤ 10 have s(10⁶) > s(6.4·10⁵).

**Pre-data power.** Q4 covers 66 classes. Its expected fraction under PROV-RS16 is 0.904, giving
P(pass) ≈ 0.999.

**Decision rule.**

- A failure of Q1, Q2 or Q4 refutes (A″). A failure of Q3 refutes (B″).
- If all four pass, draft (do not freeze) a replacement candidate.
- Otherwise, record the smallest failing class and begin the fallback.

### RS-S017 outcomes (scored verbatim against `df8f889`)

The record is `results/rs_s017_fresh_classes_2026-10-26.json` (`runs`, `score`, `observed`,
`post_data_note`).

| X | r₁ | Run time | Random-phase max | conj(g̃₆)·roots max |
|---|---:|---:|---:|---:|
| 6.4·10⁵ | 1.41831 | 503 s | 1.0026 | 1.0059 |
| 10⁶ | 1.43421 | 1148 s | 1.0025 | 1.0019 |

Both r₁ values are identical to the earlier stored values.

| ID | Outcome | Numbers |
|---|---|---|
| Q1 | **PASS** | 129 class-scale points with t ≤ 10⁻²; s ∈ [0.797, 0.936] |
| Q2 | **PASS** | all 10 bins within 0.12 of frozen F; largest gap +0.081 at log t ∈ [0.5, 1) |
| Q3 | **FAIL** | mean clause passes (−0.966 at 6.4·10⁵, −1.051 at 10⁶); per-class r < 1 fails on 30 of 224 points |
| Q4 | **PASS** | 61 of 66 classes increase (0.924) |

**Q3 failure.**

- **Smallest failing class:** the π⁵ single on N = 307, π = (−1, −18), with r = 1.0002 at 6.4·10⁵.
- All the failures lie inside control noise. The expected r under (B) is 0.996–0.9997, so the
  per-class clause had no power at large N₆, and it was not power-filtered at registration. This
  is a design defect, recorded as such and not re-scored.
- One class is near z ≈ 3 at both X: π₇₉⁴·π₉₇⁵, with r = 1.0059 and 1.0053.

**Disposition (decision rule).**

- **(A″) survives** its registered fresh-class test: Q1, Q2 and Q4 all pass. F transferred to 149
  unseen powered classes, including exponent 1, and to pairs.
- **(B″) is refuted as stated** by Q3. Its mean form (s ≈ −1.05 at t ≫ 1) passes again.
- Not all four Q passed, so **no replacement candidate is drafted**, and the owner-agreed fallback
  begins.

**Fallback scope.** The audit covers CAND-001 statement 2 and the mean form of law (B). It also
covers (A″), now that (A″) has passed a registered test. This scope extension is stated openly here.

**Validation.**

- Targeted Ruff passes.
- PYTHONUTF8=1 pytest: 321 passed and 3 skipped (fcntl exclusions).
- Both audit checkers pass.
- No matrices are committed.

**Next dependency.** RS-S018: a collision-audit (prior-art and novelty) of the surviving core.

### RS-S018 (2026-10-26): collision audit of the surviving core

**Stage:** collision-audit. **Branch:** `rs-s018-collision-audit`. No new matrices were built.
**Records:**

- `RS_S018_COLLISION_AUDIT.md`;
- the `PRIOR_ART.md` RS-S018 section;
- `results/rs_s018_collision_checks_2026-10-26.json`, from `scripts/audit_collision.py`.

**Sources read.**

- Bröker–Hoffstein, arXiv 1312.0568: the sextic theta Hecke relations, including τ₆(p⁵) = 0.
- David–Dunn–Hamieh–Lin, arXiv 2306.11875: the general-n first-moment heuristic.
- Xu–Sang, arXiv 2610.17675v2 (Oct 2026): the sextic large sieve is sharp via Gauss vectors.
- Dunn–Radziwiłł, for context.

**Findings.**

- (i), statement 2: its main term is theory-implied (conjecturally). The exact unit-class selection
  rule needs expert review.
- (ii): non-enhancement of π⁵ is consistent with τ₆(p⁵) = 0. The negative constant −1.05 has no
  collision.
- (iii), the crossover law: no collision.
- A stored-data check shows the excess is uniform across Bröker–Hoffstein's τ₆(π²)-vanishing
  condition (0.848 versus 0.843). So the matrix quantity is not a naive τ₆ readout.
- RS-7/RS-7a are upgraded to POSSIBLE_OVERLAP at the norm level (Xu–Sang).

**Decision.** A candidate is drafted for RS-S019, not frozen and with no ID: the *sextic
twist-class crossover law*, in `RS_S018_COLLISION_AUDIT.md` §5. Its status is
NOVELTY_REQUIRES_EXPERT_REVIEW.

**Validation.**

- Targeted Ruff passes.
- PYTHONUTF8=1 pytest: 321 passed and 3 skipped (fcntl exclusions).
- Both audit checkers pass.

**Next dependency.** RS-S019: freeze the candidate as CAND-002, with full candidate-record fields.

### Owner action (2026-10-26): external expert review requested

After RS-S018, the owner sent an external expert a review request. The request covers:

- the twist-class setup;
- observations (1) the crossover law, (2) the π⁵ deficit and (3) the unit-class rule;
- the τ₆(π²) contrast check;
- five questions: whether it is known, the theta-side correspondence, the π⁵ constant, the
  unit-class rule, and possible triviality.

The expert is not named here without their consent.

**Status:** awaiting a reply. Under PROTOCOL §9.2 this does not block RS-S019. A reply is evidence
to evaluate, not authority. When it arrives, record its substance (with the expert's permission
before naming them), and update the novelty statuses in `RS_S018_COLLISION_AUDIT.md` and
`PRIOR_ART.md`.

### External review received (2026-10-26, anonymous)

The reply is recorded, paraphrased, in `EXTERNAL_REVIEW_2026-10-26.md`. **The reviewer asked to
remain anonymous and uncited: never name them.**

**Main points.**

- Each coordinate of R₆w_κ is a prime-modulus first moment of shifted sextic Gauss sums with
  u = ρκ. The universal profile could be a ρ-averaged shift-aspect crossover of the Kubota series
  ψ₆(u, s). This would explain why N₆(κ), rather than N(rad κ), sets the scale.
- No known result gives the profile.
- Limiting claims must be conjectural, conditional on a sextic Patterson-type prime asymptotic.
- The τ₆(π²) contrast may be a squaring and ρ-averaging effect. Test: split the rows by (ρ/π)₆.
- The π⁵ deficit may be a prime-sieve term. Decisive test: prime versus unrestricted moduli.
- The unit-class rule needs an exact normalization-factor calculation, (c_ρ/ρ)₆.
- Fit a 1/log X correction to the plateau drift.

**Our checks.**

- Orientation: (R₆w)_ρ = Σ_σ (ρ/σ)₆·w(σ), so the shift is u = ρκ directly, with no reciprocity
  factor.
- The twisting prime is excluded, and the generators are primary.
- No Lean formalizations exist. The "Palomar register" is the Palomar registry, identified by the
  owner and now a release gate (see below).
- We also corrected our own RS-S018 typo: the exponent is 1/2 + 1/n, giving X^{2/3} for n = 6.

**Decision.** Freezing CAND-002 is deferred. The candidate will be reformulated, as a ρ-averaged
crossover with conditional limiting claims, after the decisive tests.

**Next.** RS-S019 runs pre-registered tests: prime versus unrestricted moduli, and a log-correction
fit.

### Owner decision (2026-10-26): Lean formalization and Palomar registration before any release

The reviewer's question 7 referred to the Palomar registry of Lean-verified mathematics
(https://palomar-registry.org/). The owner agrees: exact results must be formalized and registered
before anything is released.

The new stage is PROTOCOL §10, with §9 item 5 and an `AGENTS.md` graduation-rule note. It runs:

1. exact-identity inventory;
2. Lean 4 + Mathlib formalization, in a separate public repository;
3. Palomar registration, with the IDs recorded;
4. only then a draft, which labels every claim as registered, paper-proved or conjectural.

**Facts from Palomar's own pages.**

- Lean 4 Challenge/Solution modules from a fixed public GitHub commit.
- The Lean FRO comparator, with no `sorry` or custom axioms.
- `formalization.yaml` metadata.
- Registration is not a journal green light.
- Only proved statements are registered. Conjectures cannot be.

**Status.** No formalization exists yet. Lean 4.35 is installed locally. Research sessions continue;
the gate blocks release only.

### Owner decisions (2026-10-26): route to publication; formalize the conjectures too

- The route to arXiv and journals is recorded in `ROADMAP.md`. It has six phases, from settling
  the science to journal submission, with the owner decisions marked.
- Conjecture statements will be formalized in Lean as `Prop`s, alongside the proved lemmas
  (PROTOCOL §10.2b), with a computable faithfulness check against the engine (§10.2c).
- Palomar registers proved results only, so the formal conjectures live in the public Lean
  repository, possibly also in a conjecture collection after checking its criteria.
- Known limits: theta-coefficient conditional hypotheses can only be stated abstractly;
  reciprocity-dependent lemmas need reciprocity laws that Mathlib likely lacks.

### RS-S019 (2026-10-26): prime versus unrestricted moduli. Prediction block

**Stage:** falsification. It runs the anonymous reviewer's decisive test. **Branch:**
`rs-s019-moduli`. **Execution:** local Windows.

**Design.**

- Rows are the primary degree-one primes ρ, N ≤ X.
- **prime** columns are the split primes σ.
- **unrestricted** columns are every squarefree primary c coprime to 6, with split and inert
  factors and N(c) ≤ X.
- Entries are (ρ/c)₆ = Π_{p|c} (ρ/p)₆.
- Column weights are conj(G(c))·(κ/c)₆·(ζ₆ʲ/c)₆ with j = 0. G is **trace-normalized**:
  g(1, c) = Σ_{x mod c} (x/c)₆·e(Tr(x/c)), assembled by twisted multiplicativity.

Trace normalization is used on both sides because twisted multiplicativity, and hence the Kubota
object, needs a trace character. Our earlier rational e(t/p) prime weights have no natural
composite extension.

**Exact and validation work (before data).**

- New `arith.trace_gauss_sum` (brute force over ℤ[ω]/(c)) and `arith.twisted_gauss_product`.
- New test `test_trace_gauss_sums_twisted_multiplicativity`. It checks |g|² = N(c), the twisted
  multiplicativity including inert 5 and 11, conjugate pairs and three factors, and
  g_trace(σ) = conj(((2a−b)/σ)₆)·g_rational(σ).
- The new rectangular code path (`scripts/phase1n.py`), in rational/prime mode, reproduces all 101
  stored RS-S016 r values at X = 1.6·10⁵ to 4.6·10⁻¹⁵ relative.

**Exploratory, X = 5·10⁴ (not scored).**

| Setting | j ∈ {0, 3} | j ∈ {1, 2, 4, 5} |
|---|---:|---:|
| trace / prime | r₁ = 1.286 | 1.088–1.089 |
| trace / unrestricted | 1.245 | 1.263–1.264 |

The unit-class selection largely disappears with unrestricted moduli. j = 0 was fixed from this
scan.

**Registered predictions** (`results/rs_s019_moduli_2026-10-26.json`). The run is at X = 2·10⁵ on
the RS-S015 singles, with seed 19 and 10 + 10 controls per setting.

- **P:** let B be the mean s over π⁵ singles with t ≥ 3 (prime setting), and U the same in the
  unrestricted setting.
  - BASELINE_ABSENT if B > −0.6;
  - otherwise SIEVE_SUPPORTED if U − B ≥ 0.5 or U > 0;
  - INTRINSIC if |U − B| ≤ 0.25;
  - UNDECIDED in between.

  The sieve hypothesis predicts SIEVE_SUPPORTED.
- **Q:** in each setting, let Pl be the plateau mean (k ≤ 4, t ≤ 10⁻²) and C the crossover mean
  (k ≤ 4, 10^{−0.5} ≤ t ≤ 10^{0.5}). PROFILE_PRESENT iff Pl ∈ [0.5, 1.3] and C ≤ Pl − 0.3.
  Predicted PRESENT in both settings.

**Power.** P uses 15 classes; Q uses 38 plateau and 11 crossover classes. The SE of B and of U is
about 0.05.

### RS-S019 outcomes (scored verbatim against `d915b4d`)

The run is at X = 2·10⁵ with D = 17976 rows. It has 17976 prime columns and 56433 unrestricted
squarefree moduli, and took 100 s.

| | r₁ | Random-phase max (sd) | conj(G)·roots max |
|---|---:|---|---:|
| prime (trace) | 1.3064 | 1.0053 (0.0031) | 1.0092 |
| unrestricted | 1.2972 | 1.0067 (0.0025) | 1.0066 |

| ID | Outcome | Numbers |
|---|---|---|
| RS-S019-P | **INTRINSIC** | B = −1.081 (prime), U = −1.222 (unrestricted), U − B = −0.141 (15 π⁵ classes each) |
| RS-S019-Q | **PROFILE_PRESENT in both; prediction met** | prime: plateau 0.863 (n = 38), crossover −0.042 (n = 11); unrestricted: 0.899 and −0.132 |

**Reading.**

- The π⁵ deficit is **not** a prime-sieve effect. It persists, and slightly deepens, over all
  squarefree moduli. It also survives the change to trace normalization. So the reviewer's
  sieve hypothesis is not supported.
- The crossover profile is a property of the shifted Gauss-sum first moment (the Kubota object),
  not of the prime restriction. This is consistent with the reviewer's ρ-averaged shift-aspect
  mechanism.

**Exploratory, `phase1n.py fits`; record `exploratory_fits`.**

- **The π⁵ coefficient tends to −1.** By norm band (174 class-scale points):

  | N(π) | 19–43 | 61–73 | 79–150 | 151–250 | 251–400 |
  |---|---:|---:|---:|---:|---:|
  | mean s | −1.081 | −1.035 | −1.021 | −1.011 | −1.001 |
  | SE | 0.018 | 0.034 | 0.041 | 0.044 | 0.064 |

  The fit is s = −0.995 − 2.6/N. This answers the reviewer's Q3a: the coefficient approaches −1.
- **The plateau is not a single 1/log X correction.**
  - k = 1 with t ≤ 10^{−3.5} rises with X (0.932 → 0.952).
  - k = 2/3 with 10^{−3.5} < t ≤ 10^{−2} falls slightly (0.857 → 0.843).
  - Their 1/log X extrapolations disagree (1.10 and 0.75).
  - The smallest-t classes (k = 1, N ≤ 13) sit at 0.97–0.99.
  - Hypothesis, not a finding: F keeps rising as t → 0, possibly to F(0⁺) = 1, mirroring the π⁵
    limit −1.
- **Unit classes (the explore scan at X = 5·10⁴).** The j ∈ {0, 3} versus j ∈ {1, 2, 4, 5}
  selection is strong with prime moduli (1.286 versus 1.089) and nearly absent with unrestricted
  moduli (1.245 versus 1.263). Statement 2's selection rule therefore looks like a prime-modulus
  effect.

**Validation.**

- New exact test: composite trace Gauss sums.
- The new code path reproduces 101 stored r values to 4.6·10⁻¹⁵.
- Targeted Ruff passes.
- PYTHONUTF8=1 pytest: 322 passed and 3 skipped (fcntl exclusions).
- Both audit checkers pass.
- No matrices are committed.

**Next dependency.** RS-S020 runs the reviewer's ρ-partition test (does the τ₆(π²) vanishing
reappear when the rows are split by (ρ/π)₆?) and the exact unit-normalization factor, which now
must explain why the selection vanishes for unrestricted moduli. It then registers the ±1
hypotheses for a later scale.

### RS-S020 (2026-10-26): ρ-partition, normalization lemmas, H− registration. Prediction block

**Stage:** mechanism and falsification. **Branch:** `rs-s020`. **Execution:** local Windows.

**Exact lemmas** (test `test_trace_normalization_factor_and_unit_twist_by_norm`, over every prime
up to 3000):

- ((2a−b)/ρ)₆ = (−1/ρ)₆·(√−3/ρ)₆·(3/ρ)₆·(b′/ρ)₆ = (ρ̄/ρ)₆. This is the rational-to-trace factor.
  The residual (b′/ρ)₆ is not a character of ρ.
- (ζ₆/c)₆ = ζ₆^{(N(c)−1)/6} for squarefree products of split primes, and ζ₆^{(q²−1)/6} at inert
  q. So unit twists are characters of N(c) mod 36.

**Exploratory: the reviewer's ρ-partition test** (`scripts/phase1o.py`, X = 3.2·10⁵, prime moduli,
classes π^k for k = 1, 2, 4 with N ≤ 200; `results/rs_s020_rho_partition_2026-10-26.json`).

- For k = 2 and N ≡ 1 mod 12, the excess lives on rows ρ that are quadratic residues mod π.
  - Parts j = (ρ/π)₆ even: s ≈ +1.75.
  - Parts j odd: s ≈ −0.37 (rational normalization, both (π/π̄)₆ groups).
  - This is consistent with BH's Hecke relation τ₆(mp²) = G₃(m, p)·τ₆(mp²): a coefficient at ρπ²
    can be nonzero only for one quadratic class of ρ. So **ρ-averaging hides the vanishing
    condition**, as the reviewer suggested.
- In trace normalization, the (π/π̄)₆ ≠ 1 group shows a weaker contrast (+0.84 / +0.16 against
  +1.55 / −0.57). So BH's Lemma 5.3 condition is visible there.
- N ≡ 7 mod 12, k = 1 and k = 4 are uniform across parts. The N ≡ 7 case is unexplained.

**Registered before data:** RS-S020-H− (`results/rs_s020_h_minus_2026-10-26.json`).

- **Classes:** 88 fresh π⁵ singles, 400 < N ≤ 1000, including inert 23 and 29, all with t ≫ 1, at
  X = 10⁶ with prime moduli and rational normalization.
- **Prediction:** mean s ∈ [−1.15, −0.85]. The SE is about 0.076.
- **Dropped before data:** a fitted-intercept clause, which was underpowered (SE about 0.31). It is
  reported as exploratory only.
- **H+ (F(0⁺) = 1):** needs X ≥ 4·10⁶. It is deferred to a large-RAM or cloud session, which is an
  owner compute decision.

### RS-S020 outcome (scored verbatim against `0efc29b`)

The run is at X = 10⁶ (D = 78462; r₁ = 1.4342110940043258, identical to the earlier stored value)
and took 686 s. Random-phase max 1.0027, sd 0.0015.

| ID | Outcome | Numbers |
|---|---|---|
| RS-S020-H− | **PASS** | mean s = −0.919 ± 0.083 over 88 fresh π⁵ classes (400 < N ≤ 1000); band [−1.15, −0.85]; max r = 1.0029 |

**Exploratory.**

- The fitted intercept is c₅ = −0.43 with b = −320. As stated before the data, it is too noisy to
  interpret.
- The fresh π¹ classes give mean s = 0.859 at t ≈ 4·10⁻⁴ to 10⁻³.

**Reading.**

- The π⁵ law, s → −1 in the large-t regime, now has:
  - three registered passes: RS-S015-P2, RS-S017-Q3 (mean clause), and RS-S020-H− (on fresh primes
    up to N = 1000);
  - the exploratory norm-band trend toward −1.00;
  - persistence over all squarefree moduli (RS-S019).
- H+ (F(0⁺) = 1) is deferred, because it needs X ≥ 4·10⁶.

**Validation.**

- Two new exact lemmas, tested.
- Targeted Ruff passes.
- PYTHONUTF8=1 pytest: 323 passed and 3 skipped (fcntl exclusions).
- Both audit checkers pass.
- No matrices are committed.

**Next dependency.** RS-S021: reformulate and freeze CAND-002. The large-X holdout and H+ need an
owner compute decision; they are not blockers for freezing.

### RS-S021 (2026-10-26): matrix-free engine and larger-X evidence. Prediction block

**Stage:** certification (the new engine) and falsification. **Branch:** `rs-s021-large-x`.
**Execution:** local Windows, 16 threads. The owner chose local larger-X runs; the machine runs
continuously.

**New engine: `native/residue_free.c`.**

- It computes Y = R·W without storing R. Each symbol is Euler's criterion x^{(p−1)/6} mod p,
  matched against the powers of the image of ζ₆ = 1 + ω, using a double-assisted mulmod for
  p < 2²².
- Threads own row blocks, and each row accumulates in a fixed order, so the results are
  thread-independent.
- `residue_engine.c` gains `RS_THREADS`, which sets the thread count for the build and Gauss sums.
  Results do not depend on it.
- Memory is O(D·V) rather than D² (about 1 GB at X = 4·10⁶ instead of about 80 GB).

**Validation (PROTOCOL §6), before use.** The record is `results/rs_s021_large_x_2026-10-26.json`
(`validation`).

- At X = 3.2·10⁵, all 101 stored r values agree to 5.3·10⁻¹⁵ relative.
- At X = 10⁶, r₁ = 1.434211094004326, against the stored 1.4342110940043258 (relative 2.2·10⁻¹⁶).

**Registered before data:** fresh scales X = 2·10⁶ and 4·10⁶, on the RS-S015 singles, with seed 21
and 10 random-phase controls.

- **H+:** let K1 be the mean s over the k = 1 singles with N ≤ 43. The stored values are 0.932,
  0.953, 0.963 and 0.961 for X = 1.6·10⁵ … 10⁶.
  - RISING if K1(4e6) > 0.9712, K1(4e6) > K1(2e6) and K1(4e6) ≤ 1.05;
  - LEVEL if |K1(4e6) − 0.9612| ≤ 0.01;
  - otherwise UNDECIDED.
- **A (new-scale holdout of the crossover law):** every half-decade bin with ≥ 4 singles (k ≤ 4)
  has |mean s − frozen F| ≤ 0.12.
- **B:** π⁵ singles with t ≥ 3 have mean s ∈ [−1.15, −0.85] at each X.
- **Power:** the SE of K1 is about 0.001. The π⁵ classes have σ_s about 0.03–0.07 each.

### RS-S021 outcomes (scored verbatim against `2717a13`)

| X | D | r₁ | Gauss build | products (V = 111) | Random-phase sd (max) |
|---|---:|---:|---:|---:|---|
| 2·10⁶ | 148824 | 1.45405 | 446 s | 723 s | 0.00117 (1.0025) |
| 4·10⁶ | 282896 | 1.47899 | 1724 s | 2697 s | 0.00083 (1.0013) |

| ID | Outcome | Numbers |
|---|---|---|
| RS-S021-H+ | **RISING** | K1 = 0.9612 (10⁶, stored) → 0.9701 (2·10⁶) → 0.9747 (4·10⁶) |
| RS-S021-A (new-scale holdout of frozen F) | **PASS** | 12 of 12 bins within 0.05 of F (tolerance 0.12), log₁₀ t from −5 to 1.5 |
| RS-S021-B (π⁵) | **PASS** | −1.058 (2·10⁶), −1.047 (4·10⁶) |

**Reading.**

- **The crossover law transfers to new scales**, up to 4× beyond any earlier computation, with the
  frozen F. The largest bin gap is 0.049.
- **The plateau keeps rising toward 1.** This favours F(0⁺) = 1 over a level near 0.96. Finite data
  cannot establish the limit.
- **The π⁵ law holds at the new scales.**
- These are the largest computations in the programme, made possible by the matrix-free engine.

**Validation.**

- Engine: 5.3·10⁻¹⁵ against stored results.
- Targeted Ruff passes.
- PYTHONUTF8=1 pytest: 323 passed and 3 skipped (fcntl exclusions).
- Both audit checkers pass.
- No large files are committed.

**Next dependency.** RS-S022: freeze CAND-002, now including the new-scale holdouts.

### RS-S022 (2026-10-26): CAND-002 frozen

**Stage:** candidate freezing. **Branch:** `rs-s022-cand002`. No new matrices were built.

**Allocated: CAND-002**, the shift-aspect crossover law for twisted sextic Gauss-sum vectors, plus
the exponent-five deficit (`research/CONJECTURE_REGISTER.md`; RS-10 in `CONJECTURES.md`).

- Lifecycle status: CANDIDATE.
- Novelty status: NOVELTY_REQUIRES_EXPERT_REVIEW.
- Limits are conditional on a sextic Patterson-type hypothesis H_P, as the external review advised.
- F(0⁺) = 1 and three other items stay open sub-questions.

**Triviality check** (`scripts/audit_cand002.py`; `results/rs_s022_cand002_audit_2026-10-26.json`;
600 points over six scales):

| Normalization | Collapse roughness (k = 2–4) | Across-X spread of bin means | π⁵ mean |
|---|---:|---:|---:|
| frozen | 0.0037 | 0.022 | −1.059 |
| control-referenced | 0.0037 | 0.021 | −1.056 |
| raw | 0.0082 | 0.067 | −1.089 |

So F is not an artefact of the baseline, and normalizing by r₁ (the untwisted strength) is what
makes the scales coincide.

**Recorded in the candidate.**

- Proof targets under §9: the hard versions need H_P with shift uniformity, which is open.
- The exact-identity inventory E1–E9 (formalizable), plus the paper-proved and conjectural
  groups. This is the input to §10 stage 1.

**Validation.**

- Targeted Ruff passes.
- PYTHONUTF8=1 pytest: 323 passed and 3 skipped (fcntl exclusions).
- Both audit checkers pass.

**Next dependency.** RS-S023, release-gate stage 1: precise inventory statements, a Lean repository
scaffold, and a Mathlib gap assessment.

### RS-S023 (2026-10-26): owner decisions; release gate stage 1; Lean formalisation started

**Owner decisions (2026-10-26).**

- The Lean formalisation lives in `formalisation/` inside this repository, matching the owner's
  other repositories. This is recorded in PROTOCOL §10 and AGENTS.md.
- Novelty assessment and external review are done independently by the owner. They are **not
  gates** (PROTOCOL §9.2 and §10.5 are revised).
- The roadmap is now: formalise in Lean → Palomar registration → write the paper → arXiv preprint →
  journal submission (`ROADMAP.md`).

**Work.**

- `RELEASE_INVENTORY.md` gives precise statements of E0–E9, L1–L2 and C1–C2, with tests, Lean
  formulations and an effort rating.
- **Mathlib assessment:** `gaussSum`, `gaussSum_mulShift`, `gaussSum_sq`, `MulChar` and Fermat are
  available. There is no power-residue symbol and no Eisenstein-integer API. The route is therefore
  `ZMod p` via ω ↦ r, as a documented modelling convention.
- **The `formalisation/` Lean project.** It pins Lean v4.35.0 and Mathlib `56a005855ea1`, the
  owner's Palomar-ready pin. The built packages were copied locally and are git-ignored.
  - Proved: E0, E1, E2, E3, E5 and E6, with no `sorry` and standard axioms only.
  - Faithfulness: all 1764 entries of the engine's X = 200 exponent matrix match the Lean
    definition.

**Validation.**

- `lake build ReciprocitySpectra` and `lake build Checks` succeed.
- PYTHONUTF8=1 pytest: 323 passed and 3 skipped.
- Both audit checkers pass.

**Next dependency.** RS-S024: E7 and E4 via `MulChar`/`gaussSum`; the matrix and vector
definitions; CAND-002 as a Lean `Prop`.

### Owner note (2026-10-26): RS-S024 runs in the cloud

The next session runs as a cloud session, not locally. Its prompt carries CLOUD EXECUTION NOTES,
using the same method as the owner's Almost-Stacked-Proof `formal/`.

**New `formalisation/cloud_setup.sh`.** It installs elan, takes the pinned toolchain from
`lean-toolchain`, runs `lake exe cache get` for the pinned Mathlib commit, then builds the library
and the checks.

**Baseline the cloud session must reproduce.**

- Standard axioms only.
- Faithfulness 1764/1764.

**Also in the notes.**

- The container is ephemeral, so push often.
- The engine compiles with gcc on Linux, and full pytest runs on Linux.
- Palomar readiness:
  - convert every file to the module system;
  - Challenge/Solution, `comparator.json` and `formalization.yaml`, as in Almost-Stacked;
  - an orphan `palomar/submission` snapshot;
  - the owner uploads.

### RS-S024 (2026-10-26): cloud Lean checkpoint — generic Gauss identities and formal CAND-002

**Execution:** GitHub-hosted Linux cloud runner (not owner's local machine);
branch `rs-s024-cloud`. The work was broken into smaller, pushed checkpoints.

**Kernel-checked, standard axioms only:**

- `formalisation/ReciprocitySpectra/Gauss.lean`: character-level E7,
  `gauss_modulus_sq`, establishes `g · conj(g) = |F|` assuming the
  multiplicative character is nontrivial and the additive character primitive.
- Character-level E4: `gauss_shift` for nonzero shifts, and
  `finite_gauss_orientation` by finite-sum congruence.
- Existing E0–E3, E5–E6 remain unchanged and proved.

**Definitions and statements (NOT proofs of the conjecture):**

- `Model.lean` defines a norm-bounded primary split-prime index, the sextic
  exponent-based complex matrix, twist classes, vectors, finite matrix-vector
  product and the exact statistics `r`, `epsilon`, `s`, `t`.
- `Conjecture.lean` states CAND-002 (1), (2), and the conditional (3) as
  Lean `Prop`s, including a positive untwisted denominator gap, compact
  uniformity, support bounds, and an abstract prime-moment H_P.
  No conjecture is asserted as an axiom or proven.
- The finite-index and symbol-exponent data are computable; analytic complex
  exponentials are noncomputable in Lean. The new *numerical* Gauss comparison
  is C against independent Python, not Lean `#eval`.

**Numerical faithfulness at X=200:** 42 complex128 normalized sextic Gauss
sums exported by `native/residue_engine.c` into
`formalisation/fixtures/sextic_gauss_200.json`; independent comparison
with `arith.sextic_gauss_sum`. Maximum complex absolute difference
1.4983512726234129e-15 (tolerance 2e-12). The existing 1764/1764 Lean
exponent matrix comparison remains intact.

**Validation:** Cloud run 40401497506
(`https://github.com/jfairfaxball-348/PRIMES/actions/runs/40401497506`)
passed: `lake build ReciprocitySpectra`, `lake build Checks`;
all printed theorem axioms confined to `propext`, `Classical.choice`,
`Quot.sound`; matrix fidelity 1764/1764; 366 passed in Linux pytest;
Ruff on scripts; strength audit; read-only CAND-002 audit.
A later cloud run additionally checks the committed Gauss fixture.

**Not completed in this bounded session:**

- No `MulChar (ZMod p) ℂ` was constructed from `sexticExp`;
  sextic nontriviality/order 6 and compatibility with the primitive additive
  character are *not* yet established. E7/E4 therefore hold only at the
  generic character level, not yet for the project's instantiated sextic symbol.
  The zero-shift case in the sextic orientation formula also needs proof.
- CAND-002 (3) has a quantifier/implication gap: frozen (2) concerns
  `N(pi)^5/X` large, while fixing `pi` and letting `X→∞` makes
  that quantity tend to zero. Thus (3) does not follow from (2)
  as written, even under H_P without additional information.
  The frozen candidate text is not silently changed.
- No Palomar Challenge/Solution packaging, module-system migration, or
  submission was attempted. The release gate remains closed.

**Next dependency:** RS-S025, one focused Lean unit: construct the actual
sextic `MulChar`, prove its nontriviality and the primitive additive
character bridge, then instantiate E7/E4; document any remaining gap.
Do not treat incomplete mathematical bridges as completed because generic
character results compiled.

### RS-S025 (2026-10-26): cloud kernel-checked additive-character bridge — bounded partial checkpoint

**Execution:** GitHub-hosted cloud on `rs-s025-cloud`, PR #4. The session began at committed main and preserved the frozen D1 programme and CAND-002.

**New proved declarations** in `formalisation/ReciprocitySpectra/CharacterBridge.lean`:

- `rationalAddChar p : AddChar (ZMod p) ℂ`, the canonical character using `exp(2πi/p)` with the **positive** numerical sign convention (assuming `NeZero p`).
- `rationalAddChar_primitive`: its primitivity, discharged with Mathlib's `AddChar.zmodChar_primitive_of_primitive_root`.
- `rationalAddChar_apply`: the exact formula as the `t.val`-th power of the positive primitive exponential root.

These two theorems are **kernel checked with standard axioms only**. The first CI attempt failed on a missing explicit modulus argument to the Mathlib primitivity theorem; the correction is preserved in branch history and passed a new run. No `sorry` or new axioms were introduced.

**Independent cloud validation:** GitHub Actions run
https://github.com/jfairfaxball-348/PRIMES/actions/runs/40405177673
**PASS**, including `lake build ReciprocitySpectra`, `lake build Checks`; the axiom printout for both new theorems lists only `propext`, `Classical.choice`, `Quot.sound`; the engine-to-Lean exponent fixture remains **1764/1764**; **366** Python tests passed; `ruff check reciprocity_spectra/scripts` passed; native/Python Gauss X=200 **42** values agree to ~1.5e-15; both frozen strength and CAND-002 audit checkers passed. The legacy repo-wide Ruff CI still fails on hundreds of frozen D1 files and is outside this programme's targeted lint scope.

**Exact outstanding mathematical bridges:**

1. Construct `chi_rho : MulChar (ZMod p) ℂ` from `sexticExp r x`, including zero at zero, full multiplicativity, an exact complex sixth-root compatibility, order six, and `chi_rho ≠ 1` with all hypotheses on p, r and the split-prime model.
2. Prove pointwise equality of `chi_rho` and the existing `complexSymbol` on rational residues, including the zero branch; prove `rationalAddChar` agrees with the exponential factor of `rawGauss` and then `gaussSum chi_rho (rationalAddChar p) = rawGauss σ`.
3. Only then specialize E7 (`|g|²=p`, `|gtilde|=1`) and E4 (matrix row-numerator / column-denominator orientation, zero shifts, primes dividing rho·kappa). Generic Gauss theorems remain proved, but **E7/E4 are not proved for the actual sextic matrix**.

**Frozen CAND-002 logic remains an open owner decision.** Statement (2) controls `N(π)^5/X` bounded below by a large threshold, whereas fixed π and X→∞ sends the ratio to zero. Also statement (1) has crossover uniformity only on compact subsets of `(0,∞)`; fixed-class `t=N₆(κ)/X→0` lies outside them. Neither fixed-class conclusion of (3) is a formal logical consequence of those respective regimes as written; further hypotheses/arguments would be needed. No claim is refuted merely by these implication gaps; the frozen record was not altered.

**Release gate:** still closed. No Palomar packaging, paper, external review or novelty audit in this session. The next unit is RS-S026, **complete the actual sextic multiplicative-character bridge** before any packaging.


### RS-S026 (2026-10-27): mathematics-first prime moment / dispersion checkpoint

**Stage:** proof-obligation audit, hard prime-level and matrix-level route. **Branch:** `rs-s026-mathematics-first`. No Lean formalisation or paper/Palomar packaging; frozen CAND-002 and historical data unchanged.

**Proof record:** `reciprocity_spectra/RS_S026_PRIME_MOMENT_BRIDGE.md`.

**Proved mathematically (not newly kernel checked):**

1. For rational-normalised sextic sums and the original matrix orientation, `(R_X w_κ)_ρ = conjugate(Σ_σ g_σ(ρκ)/sqrt(Nσ))`, including prime-divisor zeros.
2. If `D_κ` is the number of columns not dividing κ, and `O_κ` is the signed off-diagonal correlation against the prime Gram kernel, then exactly `r_κ² = 1−1/D+O_κ/(D D_κ)` and `s_κ = N₆(κ)^(1/6) (O_κ/D_κ−1)/(O_1/D−1)` whenever the denominator is nonzero. Crucial zero-diagonal correction included.
3. The committed abstract unnormalised H_P implies for **each fixed shift u** `Σ_{Nσ≤X} g_σ(u)/sqrt(Nσ) = 4c(u) X^(1/6)/log X + o_u(X^(1/6)/log X)`, via Abel summation. It does not furnish uniformity for moving shifts `u=ρκ` of norm comparable to X.
4. A conditional two-point prime-correlation criterion would imply fixed-class enhancement and fifth suppression by the exact matrix identity; it is **unproved** and substantially restates the difficult signed dispersion task, rather than establishing an arithmetic mechanism.

**Blocker:** H_P gives only raw one-point moments with arbitrary complex `c(u)`, and for moving shifts only cutoffs `y≥N(u)/B` with B fixed. It does not control Abel's missing initial segment, signed off-diagonal correlations or averaged squares. Frozen (1) is uniform only for t bounded away from 0; (2) addresses the opposite, large-t regime. No theorem yet bridges to fixed-class t→0; separate sufficient conditions and their limitations are proved in the record.

**Validation:** Independent arbitrary zero-diagonal unit-complex-matrix algebra checks at D=3,5,8, with every one-column deletion, pass for the exact norm and dispersion identity. These are consistency checks, not sextic number-theory evidence. All analytic claims are proved step by step in the record. No new conjecture testing, results JSON, Lean edits or frozen D1 changes.

**Disposition:** CAND-002 (1)–(3) remain CANDIDATE/OPEN as appropriate; no status promotion, no Palomar registration. Next RS-S027 remains **MATHEMATICS-FIRST**, targeting signed two-point prime correlations and uniform moving-shift weighted moments before any formalisation.


### RS-S027 (2026-10-27): reciprocal kernel and uniform moving-shift upper-tail lemma

**Stage:** mathematics-first hard prime-level / matrix-level proof obligation.
**Session branch:** \`rs-s027-signed-kernel\`. **Record:**
\`reciprocity_spectra/RS_S027_SIGNED_KERNEL_TAIL.md\`.

**Proved on paper:**
- Exact sextic reciprocity transfer of the off-diagonal prime kernel:
  \(K_X(\sigma,\tau)=\sum_{\rho\in P_X}h_{\sigma,\tau}(\rho)(\sigma\tau^5/\rho)_6\)
  with an explicit mod-4 quadratic sign, including all zero terms.
- The character \(z\mapsto(z/\sigma)_6\overline{(z/\tau)_6}\) is primitive at
  both distinct primes, has complete-residue orthogonality, and extends
  with a necessary \(\pm1\) normalization to a nonprincipal Hecke ideal
  character of conductor dividing \((3\sigma\tau)\). Invoking the classical
  fixed-conductor Hecke prime-ideal theorem gives
  \(K_X(\sigma,\tau)=o_{\sigma,\tau}(D)\), **not** uniform in moving pairs.
- From the *unproved* raw H_P, a genuine **uniform upper-slice** weighted
  Abel lemma for every fixed \(\lambda>0,B>0\), uniformly in
  \(0<N(u)\le B\lambda X\), with its exact deterministic \(H_\lambda(X)\).
  The coefficient c(u) remains unconstrained, and the missing lower slice
  cannot be controlled from the same H_P quantifiers.

**Hard-route obstruction:** reciprocity produces moving shift
\(N(\sigma\tau^5)\asymp X^6\) for bulk index pairs, outside
H_P's fixed-B scale \(N(u)\le BX\), and the \(\bmod4\) factor requires
a local twist. Fixed-pair PNT and generic operator estimates do not
give the sign-sensitive averaged energy needed for the fixed endpoints.
No fifth-class negative limit or non-five positive limit is proved.

**Validation:** independent Euler-symbol and mod-4 computations on 32
split primary primes: 992 ordered reciprocity pairs and 31,744
kernel triples passed, including prime-divisor zeros. Mathematical
proofs and quantifier review as in the note; no discovery-scale run.
No Lean, formalization, registration, publication or frozen evidence edit.

**Disposition:** CAND-002 and its fixed-class logical bridge remain OPEN;
status unchanged. The generic large-sieve route is exhausted as in RS-S013,
not the hard arithmetic-coefficient route. **Next:** RS-S028, make a
non-circular arithmetic coefficient/model and Type II obligation explicit
or prove its obstruction. No owner-decision blocker.


### RS-S028 (2026-10-27): prime projection, ideal Vaughan blocks and residue-transfer obstruction

**Stage:** mathematics-first proof-obligation audit on the hard prime/matrix route.
**Session branch:** \`rs-s028-prime-projection-vaughan\`. **Proof record:**
\`reciprocity_spectra/RS_S028_PRIME_PROJECTION_VAUGHAN.md\`.
Frozen CAND-002 and historical predictions were not changed. No Lean or
Palomar work was resumed.

**New rigorously derived paper-level results (not new Lean proofs):**

1. **Exact ideal prime projection.** Extend rational-normalized split-prime
   Gauss weights to a squarefree, 6-coprime *ideal* trace-Gauss weight
   \(b_u(\mathfrak a)\), multiplying by an explicitly defined
   rational/trace correction at each degree-one prime. The formula
   \(\sum_{\sigma\in P_X}g^{rat}_\sigma(u)/\sqrt{N\sigma}
      =\sum_{N\mathfrak a\le X}(\Lambda_K(\mathfrak a)/
      \log N\mathfrak a)b_u(\mathfrak a)-E_u^{inert}(X)\)
   is exact; \(|E_u^{inert}(X)|\le\sqrt X\). Prime powers of
   degree \(\ge2\) vanish by squarefree support; ramified 3
   and inert 2 are excluded explicitly. The rational normalization
   correction is **not** identified with a fixed Hecke character.
2. **Exact ideal Vaughan decomposition.** Ideal convolution identities
   give four explicit pieces I1-I2+I0+II. The actual Type II
   coefficients are Möbius divisor sums \(\alpha_U(\mathfrak m)\)
   and \(\Lambda_K(\mathfrak n)\), independent of any eigenvector
   or fitted statistic. With U=V=X^(1/3+δ) on the top dyadic
   shell, all nonzero Type II factors have norms strictly above
   X^(1/3+δ) and at most X^(2/3−δ), for 0<δ<1/6.
   Its surviving \(\mathfrak n\) is prime (prime powers
   are excluded); coprime composite trace Gauss sums bring the
   signed cubic reciprocal kernel with mod-4 and primary-generator
   corrections. This is an exact decomposition **not** a
   Type II cancellation theorem.
3. **Analytic transfer counterexample.** Two explicitly constructed
   nonnegative Dirichlet coefficient sequences share a simple
   pole and residue at \(s=2/3\), yet their rational-prime
   partial sums differ by
   \(\sim(3/2)X^{2/3}/\log X\).
   This rigorously rules out the *general logical inference*
   "all-moduli pole residue determines the prime coefficient,"
   not an arithmetic-specific Kubota theorem or CAND-002.
4. **Error bookkeeping.** A row-averaged \(\ell^2\) log budget for
   dyadic blocks is recorded, **explicitly unproved**. The
   required positive no-five signed energy and nonpositive fifth
   energy remain separate. No identified analytic \(B_6\)
   model, uniform moving-shift bound, arithmetic main term or
   sign theorem was produced.

**Independent proof checks:** ideal convolution proved algebraically;
the matching integer-monoid Vaughan identity independently checked
for n=2..299 at U=11,V=13; the distinct-composite pairing in the
Dirichlet-series counterexample checked on 167 odd primes below
1000 and established by parity. These finite checks are **not**
number-theoretic asymptotic evidence. Sources and assumptions
are distinguished in the proof record. No project discovery-scale
run or evidence JSON; no .lean, workflow, comparator or historical
data edits.

**Disposition:** CAND-002(3) remains OPEN, both endpoints unproved.
The generic operator-norm route is still ruled out as in RS-S013;
the arithmetic-coefficient hard route has **not** been exhausted.
No status promotion and no owner blocker. **Next:** RS-S029,
an exact arithmetic coefficient/local-factor and signed Type II
obligation using the defined ideal Vaughan blocks, before any
attempt to equate a Kubota residue with a prime main term.

### H_P scale erratum and RS-S028 merge (2026-10-27; owner-requested review)

**Review.** The owner asked for a check of RS-S024 to RS-S028.

- The logical-bridge audit is **correct**: CAND-002(3) does not follow from (1) and (2). This was an
  error in the RS-S022 freezing text.
- The exact identities of RS-S026, RS-S027 and RS-S028 check out.
- The Lean build and checks pass locally.

**Erratum.** `AbstractPrimeMomentHP` applied X^{2/3}/log X to **raw** Gauss sums, which are expected
to be about X^{7/6}/log X. That made the conditional statement vacuous.

- **Fix:** the hypothesis is now stated for the normalised first moment. The owner authorised this
  Lean edit; it overrides the §9.6 Lean pause for this correction only.
- **Impact** (`RS_HP_SCALE_ERRATUM.md`):
  - RS-S026 Props 1–2 and RS-S027 Prop 1, (7) and (8) are unaffected.
  - The specific rates in RS-S026 Prop 3 (coefficient 4) and RS-S027 Prop 2 belong to the old
    scale.
  - New, stronger obstruction: H_P's uniform error exceeds the √D row scale, so H_P alone cannot
    constrain r_κ.
- Erratum pointers were added to RS-S026, RS-S027 and the bridge audit. A clarification was added
  to the CAND-002 record; the frozen text is unchanged.

**Merged:** `rs-s028-prime-projection-vaughan`, including its RS-S029 handoff, which is now
amended. Stale branches were deleted after archive tags.

**Validation.**

- `lake build ReciprocitySpectra Checks` succeeds.
- Standard axioms only.
- Faithfulness 1764/1764.

### Owner decision (2026-10-27): proof work out of the pipeline; formalise what is exact

- Proving CAND-002 is removed from the release pipeline and parked as optional research
  (PROTOCOL §9.6 revised). The 2026-10-26 Lean pause is lifted.
- CAND-002(3) is restated as a standalone fixed-class conjecture (register entry), formalised as
  `CAND002_FixedClass`. `CAND002` is now (1) ∧ (2) ∧ (3). The H_P-conditional form is kept
  outside the package for the record.
- The Lean build succeeds, and faithfulness is 1764/1764.
- `RELEASE_INVENTORY.md` has a plan of record that classifies every claim:
  - (A) Lean-proved;
  - (A′) formalisable, to do;
  - (B) paper-proved;
  - (C) conjectural or numerical.
- **Next:** RS-S029, the cloud Lean sextic character bridge. Then RS-S030, Palomar packaging.

### RS-S029 (2026-10-27): sextic MulChar bridge — verified partial completion

**Authority:** the owner's plan of record from commit `daaaa681`;
the proof of CAND-002 is parked. **Branch:** `rs-s029-sextic-character-bridge`.
**Pull request:** #8.

**Exact Lean results, no `sorry`:** new `SexticCharacter.lean`
constructs the exponent-based `MulChar` with E3 multiplicativity,
zero at zero, nontriviality via the cyclic unit group, agreement
with `complexSymbol` for rational residues and the split-prime
residue-root quadratic equation under the explicit nonzero
coefficient assumption. Generic E4 now has a certified zero-shift
branch (`gauss_zero_shift`, `gauss_shift_all`). Every theorem
is included in `Checks/Axioms.lean`.

**Validation:** pinned Lean 4.35.0/Mathlib full cloud run
`40485959252` SUCCESS for both library and Checks; standard
axioms only; 1764/1764 matching exponents; complete pytest,
Gauss fixture, touched-Python Ruff and both frozen-evidence
audit checkers PASS. No new numerical claim and no change to
conjecture status.

**Precise remainder:** `rawGauss` is still a `Finset.range`
direct sum, with no Lean equation to `gaussSum sexticCharacter
rationalAddChar`. Consequently no E7 specialized raw modulus,
no E4 specialized shifted identity and no finite matrix
row-orientation identity have been proved. These are not
implied merely by the generic Gauss lemmas. E8/E9, Gram identity,
CAND-002 proof and Palomar remain outside this checkpoint.

**Next:** RS-S030, prove the raw/direct sum equivalence, specialize
E7/E4 including the zero shift, and attempt the exact row identity.
No owner-decision blocker.

### RS-S030 (2026-10-27): exact direct sextic Gauss bridge and E7

**Stage:** Lean formalization; **branch:** `rs-s030-exact-gauss-bridge`; **PR:** #9. The committed owner plan (PROTOCOL §9.6) governs: CAND-002 proof is parked as optional; release only exact formalized claims.

**Kernel-checked (not numerical assumptions):** `GaussBridge.lean` proves bijective `ZMod p` / `Finset.range p` reindexing; the exact positive-sign additive exponential on canonical representatives; `gaussSum_sextic_eq_raw` equating the direct rational `rawGauss` sum to the proven exponent-based sextic character's Mathlib Gauss sum; and `rawGauss_modulus_sq` proving specialized E7, `Gσ·conj(Gσ)=Nσ`. The split-prime/model assumptions are explicit. All four theorems are audited in `Checks/Axioms.lean`, no sorry/new axiom.

**Validation:** first build found a redundant final `rfl` after the equality had already been proved; removed. Pinned GitHub Actions run **40489442361 SUCCESS**: both Lean targets, standard axioms, 1764/1764 exponent faithfulness, 366 full pytest checks, Ruff, 42 Gauss fixture comparisons and evidence audits. No new asymptotic computation or status promotion.

**Remainder:** direct positive-sign shifted Gauss sum, specialized E4 for zero/nonzero shifts and exact `residueMatVec` row orientation (including class products and conjugation). Generic E4 is known but NOT yet specialized to the matrix. Optional Gram identity is pending. CAND-002 and all asymptotic limits remain OPEN. No Palomar submission or paper work. **Next RS-S031** takes E4 + matrix orientation; Palomar only afterwards.


### RS-S031 (2026-10-27): specialized shifted sextic E4 and per-column orientation

**Bounded unit:** Lean formalisation only, on `rs-s031-shifted-e4-bridge`, PR #10. Started from committed latest main. No D1, novelty audit, CAND-002 proof, Palomar packaging or release work.

**Kernel-compiled library theorems:** `ShiftedGauss.lean` constructs a direct positive-sign rational shifted sum for all `a : ZMod p`, including zero, and proves exact `gaussSum` identification, specialized sextic E4 and pointwise Eisenstein residue-symbol agreement. `RowBridge.lean` proves multiplicativity over a finite class support, row-shift symbol factorization, and per-column orientation `residueMatrix ρ σ * classVector κ σ = star (directShiftedGauss σ (rowShift κ ρ σ) / sqrt(Nσ))` with the correct numerator/denominator, zero cases and normalization. All hypotheses are explicit; no placeholder, axiom or conjectural arithmetic is admitted as a theorem. The Lean library target compiled after the direct function was renamed to avoid conflicting with the separate frozen `Conjecture.shiftedGauss`.

**Validated on final RS-S031 closeout code+docs commit `735374e`:** GitHub Actions [40493962451](https://github.com/jfairfaxball-348/PRIMES/actions/runs/40493962451) **SUCCESS**. Both `lake build ReciprocitySpectra` and `lake build Checks` passed using pinned Lean 4.35/Mathlib 56a005855ea1; `Checks/Axioms.lean` prints only `propext`, `Classical.choice`, `Quot.sound` for all new theorems; fixture exponent matches **1764/1764**; **366/366** pytest; targeted Ruff; native/Python Gauss **42** values (max ≈1.5e-15); both historical evidence audits PASS. The first cloud build identified a missing explicit `Option` split in `sexticCharacter_eis` (fixed), and another build identified an import collision with the pre-existing conjecture shifted sum (fixed without editing `Conjecture.lean`). After both fixes, the pinned cloud `lake build ReciprocitySpectra` passed. The first audit run could not resolve the new theorem names because `Checks/Axioms.lean` still imported the older GaussBridge; this import was corrected to RowBridge. Record final full Checks/faithfulness/Python/audit workflow status from the run on the closeout commit. Earlier baseline RS-S030 was independently fully validated (40489442361).

**Exact gap to full matrix orientation:** For every member of `primarySplitPrimes X`, derive the model prime/root and 2/3/6 split assumptions, then sum the per-column theorem to prove a literal `residueMatVec` equality. Also reconcile the existing `Conjecture.shiftedGauss (u σ : Eis)`, whose exponential uses a nonreduced representative product, with the new reduced-residue direct shift; finite exponential periodicity is needed. The present per-column identity uses `rowShift`, not a proved Eisenstein `ρκ` object. This work is not treated as automatic or complete.

**Disposition:** (A′) specialized E4 and per-column orientation progressed; full (A′) item 3 remains OPEN until its actual finite sum and frozen-model bridge pass. (B) and (C) untouched. CAND-002(1),(2),(3) still OPEN, no conjectural promotion. Optional Gram work deferred. **Next RS-S032**: full finite sum/membership/shift-convention bridge; Palomar only after validation.


### RS-S032 (2026-10-27): full reduced-model finite row identity verified

**Scope:** bounded cloud Lean session, branch `rs-s032-finite-matrix-bridge`, PR [#11](https://github.com/jfairfaxball-348/PRIMES/pull/11). No D1 access, asymptotic proof, novelty, Palomar or paper work. Frozen `Conjecture.lean` unchanged.

**Exactly proved in the pinned Lean library:** `primarySplitPrimes_prime` extracts prime norm from membership; `primary_norm_mod_three` computes norm ≡1 (mod 3) from primary coordinates; `primeNorm_d_ne_zero` excludes both coordinates vanishing modulo their prime norm; `primarySplitPrimes_model` derives the polynomial residue root, 2/3 nonzero and 6∣p−1. The genuine `residueMatVec_orientation` equates the full sum over `primarySplitPrimes X` to conjugated direct shifted sextic Gauss sums divided by √(norm), with no unproved membership hypotheses and including zero factors. `positiveExp_mod` proves exact exponential periodicity, and `shiftedGauss_frozen_eq_direct` equates the untouched frozen `shiftedGauss(u,σ)` and direct shifted sum for any actual Eisenstein integer u including zero (assuming p≠0). All are in the standard-axiom audit; no `sorry`, admitted axiom or changed conjecture.

**Successful pinned validation checkpoint:** run [40505888940](https://github.com/jfairfaxball-348/PRIMES/actions/runs/40505888940), library and Checks SUCCESS (standard axioms only); faithfulness 1764/1764; full pytest 366; 42 Gauss comparisons, targeted Ruff and both audits PASS. A final run of the documentation closeout commit is still required for merge. Repository-wide historical `ci` failures on paused D1 are unchanged.

**One remaining identification:** the `rowShift` used in the proved finite sum is defined as a residue-field class product. It is **not yet proved** to be the reduction of one true Eisenstein `ρκ` for arbitrary `TwistClass`. An attempted finite Eisenstein `CommMonoid`/product bridge failed Lean elaboration and was removed from the branch; its errors were never promoted to a theorem. Accordingly the full reduced-model row identity and frozen shift-convention equality are both proved **separately**, but a single frozen-class `Conjecture.shiftedGauss(ρκ,σ)` row identity remains open. No Gram identity, no Palomar package, no CAND-002(1),(2),(3) proof. RS-S033 tackles precisely the missing finite Eisenstein class product; Palomar only after its theorem and complete pinned validation.
