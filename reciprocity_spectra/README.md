# Reciprocity Spectra

**A new PRIMES research programme, opened 2026-10-24.**

**Status: PHASE 1c COMPLETE.** The certified-null local revision is STRESSED for its registered
finite statistic; the qualified sextic positive-excess revision is REFUTED. Cubic/quartic
outliers and quadratic compression survive the corrected controls. All old FAIL outcomes
remain unchanged; eventual asymptotic limits and the original RS-6 bulk claim are unsettled.
Nothing is proved. No novelty claim is made beyond the search scope
recorded in `PRIOR_ART.md`.

## The idea in one paragraph

Put the law of reciprocity into a matrix. Take every prime of norm `≤ X` in a ring where n-th power
reciprocity holds:

- odd rational primes, for n = 2;
- primary Eisenstein primes in `Z[ω]`, for n = 3 or 6 with the declared character normalization;
- primary Gaussian primes in `Z[i]`, for n = 4.

Form the matrix `R_n(X) = ((π/ρ)_n)` of power-residue symbols between them. Reciprocity and
simultaneous conjugation impose structural relations, with further fixed values between conjugate
prime generators. The certified conditional null draws uniformly on the remaining symmetry orbits.
A deviation from that stated benchmark identifies correlations beyond its conditions; it does not
by itself identify a mechanism. A pilot computation, with matrices of dimension up to 14,682,
found three distinct regimes.

| n | What the spectrum does | Mechanism (hypothesis) |
|---|---|---|
| 3 | **Supercritical outliers.** The top singular value leaves the random bulk exactly like a spiked random matrix with spike strength `θ ≈ 1.42·X^{2/3}/log X`; the constant holds to ±0.01 over a 32-fold range of X. The singular vector is the vector of normalized cubic Gauss sums, with overlap 0.936 against a predicted 0.939. A whole *family* of further outliers matches Gauss sums twisted by `(u/π)₃` for u = 2, 1−ω and primes of norm 7, 13, 19, …. | Kubota–Patterson cubic theta function; the outlier spectrum appears to realize its Fourier coefficients. |
| 4 | **Slowly growing outliers.** `σ₁/edge` = 1.07 → 1.18 as X goes from 2·10⁴ to 1.6·10⁵, with spike strength growing like `log X`. The singular vectors are *not* Gauss-sum vectors. | Quartic theta function, whose Fourier coefficients at primes are not known in closed form. The outliers may give a numerical window onto them. |
| 2 | **No outliers, but a compressed spectrum.** The singular values of the Legendre matrix of the first D primes approach the quarter-circle law with an arithmetic correction: `(2 − m₄)·log D ≈ 1.20` and edge `≈ 2√D·(1 − 0.58/log D)`, steady for D = 668 to 14,682. | Montgomery–Hooley-type secondary term in mean squares of real character sums over primes. |

The pilot reciprocity-only random control showed none of these effects (the corrected structural
ensemble and its limitations are described in the RS-S004 section below):
`σ₁/edge = 0.997–1.000` and `m₄ = 1.997`.

## Why this is a good research area

- **New questions on classical objects.**
  - Dummit–Dummit–Kisilevsky define these "residue matrices" but only classify which ±1 or
    root-of-unity patterns occur.
  - The large-sieve literature (Heath-Brown; Dunn–Radziwiłł; de Faveri–Dunn–Hoffstein, July 2026)
    bounds only their operator norms.
  - Spectra, outlier families, spike laws and bulk corrections appear unstudied. See
    `PRIOR_ART.md` for what is known and what is not claimed.
- **Natural quantifiers and an exact null model.** Every conjecture is a limit law as X → ∞ with a
  measurable constant (κ₃, c₄, the quartic growth rate). This avoids the quantifier-selection
  trap that stopped PRIMES (see `LESSONS.md`).
- **Deep mechanisms, reachable computationally.**
  - metaplectic theta functions (n = 3, 4);
  - the variance of primes in progressions (n = 2);
  - random-matrix spiked models (BBP).

  A four-core machine reaches decisive sizes in minutes.
- **A connection to Pointed Order Zeta.** That project studied one row of the residue table (fixed
  base a, varying p) and collapsed into Artin/Chebotarev theory. The whole matrix is where new
  structure appears.

## Document map

| File | Contents |
|---|---|
| `PROTOCOL.md` | **Session rules for this programme**: what is inherited from PRIMES, what is replaced, the pre-registration rule, and the compute budget for cloud sessions |
| `LEDGER.md` | Append-only programme ledger with the current state and committed predictions |
| `LESSONS.md` | Why PRIMES (0 candidates in 72 sessions) and Pointed Order Zeta (PILOT_KILL) failed, and the design rules this programme adopts |
| `AREA_TRIAGE.md` | Eight candidate areas checked on 2026-10-24, with verdicts and sources, including one computed kill |
| `PRIOR_ART.md` | Collision audit for this area: known, possible overlap, or no collision found |
| `CONJECTURES.md` | Working conjectures RS-1 … RS-6 with evidence tables and pre-registered falsifiers |
| `ROADMAP.md` | Phases 1–5: scaling with predictions, mechanisms, quartic theta coefficients, theorems in reach, expert review |
| `results/pilot_2026-10-24.json` | Every pilot number in machine-readable form |
| `arith.py` | Exact pure-Python core (primary primes, residue symbols, Gauss and Jacobi sums), tested in CI by `tests/test_reciprocity_spectra.py` |
| `native/residue_matrix.c` | Fast matrix and Gauss-sum builder |
| `scripts/spectra.py` | Spectral analysis: summary, spike law, outlier family, bulk moments (numpy and scipy) |
| `scripts/run_pilot.sh` | One-command reproduction (`scripts/run_pilot.sh 160000` reproduces the full pilot) |
| `scripts/consecutive_frobenius_s3.c` | Recorded kill: no consecutive-prime bias in the non-abelian part of an S3 Frobenius |

## Reproduce

```bash
python -m pip install numpy scipy        # only for the numerical scripts
pytest tests/test_reciprocity_spectra.py # exact arithmetic checks (no numpy needed)
reciprocity_spectra/scripts/run_pilot.sh 40000   # about 2 minutes; 160000 takes about 30 minutes, 4 GB RAM
```

The exact core checks these identities on small cases:

- the reciprocity laws for n = 2, 3, 4;
- `g(π)³ = pπ` for cubic and `g(π)⁴ = pπ²` for quartic Gauss sums;
- `−χ(−1)·J(χ,χ) = π` for quartic Jacobi sums.

The C builder reproduces the pilot matrices byte for byte.

## Original scaling plan (RS-S001)

Phase 1 of `ROADMAP.md`. Store matrices as uint8 exponents with blockwise matrix–vector products to
reach X = 6.4·10⁵. Before running, pre-register the predictions: κ₃ ∈ [1.38, 1.47]; cubic overlap
within 0.03 of the BBP value; quartic `θ_n ≈ 0.166·log X − 0.18`; quadratic `(2 − m₄)·log D` in
[1.0, 1.4]. Then run the n = 6 test of RS-5.

## Scalable byte engine (RS-S002)

`native/residue_engine.c` builds the same byte format as the pilot builder, using four OpenMP
threads for character tables, matrix construction, and normalized Gauss sums. Its ctypes ABI
provides blocked complex forward and adjoint products directly from the bytes. The solver uses
Lanczos on `C*C`; it never materializes a dense floating matrix at the scaling sizes.

The quadratic fourth moment uses independent real Rademacher Hutchinson probes of `(C*C)^2`,
with the individual estimates, probe count, seed and sample standard error retained in JSON.
The matched controls use uniform upper-triangle exponents and the pilot reciprocity signs.
Their seeded SplitMix64 counter stream differs from numpy's PCG64 stream; the distribution is
matched, not the individual realization. Matrices and controls stay in ignored `data/`.

From the repository root:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=4 python reciprocity_spectra/scripts/phase1.py validate
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=4 python reciprocity_spectra/scripts/phase1.py run --x 320000
```

The validation command checks byte identity against the unchanged pilot C builder, singular
values against dense SciPy `svds`, forward and adjoint products, Gauss sums, control symmetry,
and the stochastic fourth moment against a dense Gram trace. The run command requires a passed
validation record, limits each family and its control to about 45 minutes, and checkpoints and
pushes arithmetic results and matched controls separately to the RS-S002 session branch.
Do not reuse that branch or results filename for a later session without updating the runner's
session-specific provenance and checkpoint destinations.

The RS-S002 required scaling target is now complete; see `results/phase1_2026-10-24.json`
and the ledger for every comparison, both engine validation records, the abandoned slow-control
attempt, and the X = 640000 runtime-budget skip. STRESSED is finite numerical evidence, not proof.
The subsequent RS-S003 results and current handover are described below.

The adjoint uses the existing reciprocity signs to read contiguous byte rows; the generic
transpose kernel remains available and is checked independently. To reproduce the additional
exploratory quadratic matched-control moment after completing its spectra:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=4 python reciprocity_spectra/scripts/phase1.py control-m4 --x 320000 --mode quad
```


## Phase 1b: sextic and local-statistics tests (RS-S003)

`arith.py` now defines the sextic character explicitly with zeta6 = 1 + omega on the existing
Eisenstein indices. Metadata coefficients stay in the omega basis. The native engine supports
`sextic` and a full pairwise reciprocity mask for blocked adjoints and seed-0 controls. The
simpler parity-mask kernel remains unchanged for the previous families.

`results/phase1b_2026-10-24.json` contains the registration committed before data, exact/numerical
validation, both sextic top-twelve spectra and controls, all full local-statistics spectra,
fixed-window summaries, eight FAIL outcomes, and the checkpoint incident. These finite failures
do not disprove eventual limits. Only the registered gap-ratio extension was tested locally.

```bash
OPENBLAS_NUM_THREADS=2 OMP_NUM_THREADS=4 python reciprocity_spectra/scripts/phase1b.py validate
OPENBLAS_NUM_THREADS=2 OMP_NUM_THREADS=4 python reciprocity_spectra/scripts/phase1b.py sextic
OPENBLAS_NUM_THREADS=2 OMP_NUM_THREADS=4 python reciprocity_spectra/scripts/phase1b.py local
```

The runner is specific to RS-S003; preserve its evidence when starting another session. The subsequent structural-null certification and fresh-scale results are recorded below.
No explanation of the sextic excess is claimed here.


## Certified structural null (RS-S004)

`NULL_CERTIFICATION.md` derives the exact conjugation, primary/unit/Galois, boundary and
conditional orbit constraints, with their scope. `null_model.py` is the pure-Python exact BFS
reference; the native engine supplies the independent four-position orbit sampler. Fixed
conjugate-pair phases come from one-prime trace formulas, not copied arithmetic entries.

`results/phase1c_2026-10-25.json` contains the committed registration, validation, all-entry
audits, full cubic/quartic spectra at X = 80000, sextic top-twelve spectra at X = 320000, two
fixed controls per comparison, quadratic Monte Carlo probes/errors, and every outcome. Four
qualified local tests and six retention diagnostics PASS; both qualified sextic tests FAIL.
These do not retroactively change any RS-S003 result. The two counter seeds are fixed
benchmarks, not independent-replication p-values; see the certification document.

```bash
OPENBLAS_NUM_THREADS=2 OMP_NUM_THREADS=4 python reciprocity_spectra/scripts/phase1c.py validate
OPENBLAS_NUM_THREADS=2 OMP_NUM_THREADS=4 python reciprocity_spectra/scripts/phase1c.py run
```

The session-specific runner resumes incomplete components and preserves completed ones. Do
not overwrite its evidence for a later session. The next unit, RS-S005 / Phase 2a, investigates
one exact Gauss-sum mechanism for the remaining sextic excess with a bounded collision check.
Its single prompt is in the root `NEXT_SESSION_PROMPT.md`.
