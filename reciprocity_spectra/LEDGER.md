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
