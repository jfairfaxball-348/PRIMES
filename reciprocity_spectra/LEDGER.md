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
