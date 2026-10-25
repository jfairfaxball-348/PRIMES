# Working conjectures

Status vocabulary:

- **PILOT**: supported by the 2026-10-24 pilot only.
- **STRESSED**: survived a pre-registered prediction at a larger scale.
- **REFUTED**
- **PROVED**

None of these is a theorem.

Notation:

- `D` is the dimension of the matrix.
- `edge = 2√D` is the bulk edge for unimodular random matrices.
- `g̃(π) = g(π)/√N(π)`, with `g(π) = Σ_{t=1}^{p-1} (t/π)_n e(t/p)`. The code checks that
  `g³ = pπ` for n = 3 and `g⁴ = pπ²` for n = 4.
- BBP inversion: an observed top singular value `σ₁` defines the spike strength `θ` through
  `σ₁ = θ + D/θ`, valid when `θ > √D`. The BBP-predicted overlap of the top right singular vector
  with the spike direction is `√(1 − D/θ²)`.

---

## RS-1: cubic spike law (STRESSED)

For `C_X = ((π/ρ)₃)` over primary degree-one primes of `Z[ω]` with `N ≤ X`:

```
σ₁(C_X) = θ_X + D/θ_X + o(√D),     θ_X ~ κ₃ · X^{2/3} / log X,     κ₃ ≈ 1.42,
|⟨v₁, conj(g̃)⟩| / ‖g̃‖ = √(1 − D/θ_X²) + o(1)  →  1.
```

**Evidence:**

|      X |     D | σ₁/edge | κ₃ estimate | overlap | BBP prediction |
|-------:|------:|--------:|------------:|--------:|---------------:|
|  5,000 |   660 |   1.212 |       1.419 |   0.896 |          0.850 |
| 10,000 |  1222 |   1.275 |       1.434 |   0.895 |          0.875 |
| 20,000 |  2248 |   1.341 |       1.425 |   0.910 |          0.894 |
| 40,000 |  4178 |   1.416 |       1.416 |   0.924 |          0.910 |
| 80,000 |  7796 |   1.514 |       1.424 |   0.931 |          0.926 |
| 160,000 | 14640 |  1.621 |       1.425 |   0.936 |          0.939 |

A random matrix with the same symmetry gives `σ₁/edge = 0.999–1.000`.

**Mechanism hypothesis:**

- twisted multiplicativity of cubic Gauss sums;
- the Patterson bias `Σ g̃(π) ~ c X^{5/6}/log X` (Dunn–Radziwiłł);
- the Fourier coefficients of the Kubota–Patterson theta function, which decay like `N(ρ)^{-1/6}`.

These give a spike of size `X^{2/3}/log X` (heuristic in `ROADMAP.md`, Phase 2).

**Pre-registered falsifier for the next scale (X = 6.4·10⁵):** the conjecture is in trouble if
either of these happens:

- κ₃ leaves `[1.38, 1.47]`;
- the overlap differs from the BBP prediction by more than 0.03.

**Open subproblem:** derive κ₃ in closed form, for example from Patterson's constant
`(2π)^{2/3}/(3Γ(2/3))` and a Rankin–Selberg sum of theta coefficients.

## RS-2: the outlier family is the cubic theta function (PILOT)

The singular values above the bulk edge are labelled by small cube-free `u ∈ Z[ω]`:

- `u = 1`;
- `u = 2` (inert);
- the primes of norm 7, 13, 19, 31, …;
- the ramified prime `1 − ω`.

The corresponding singular vectors are close to `conj(g̃)·(u/·)₃^{±1}`. Their strengths decrease
with `N(u)`. Conjecture: `θ_u/θ_1 → |τ(u)/τ(1)|`, where the `τ` are Fourier coefficients of the
cubic theta function. The outliers would then be a *spectral realization of the theta function*.

**Evidence (X = 40,000, top 24 singular vectors).** Projection norm of the twisted Gauss-sum vector
onto the top-24 singular subspace:

| u | projection norm | dominant σ/edge |
|---|---:|---:|
| 1 | 0.924 | 1.416 |
| 2 | 0.875 | 1.199 |
| N = 7 | 0.840 | 1.138 |
| 1−ω (conjugate twist) | 0.831 | 1.104 |
| N = 13 | 0.784 | 1.078 |
| N = 19 | 0.729 | 1.055 |
| N = 31 | 0.638 | 1.018 |
| N = 37 | 0.483 | 1.022 |
| N = 43 | 0.436 | 0.992 |

Untwisted controls (`u = ω`, wrong twist sign) give 0.05.

**Test:** compare the measured `θ_u` ratios with Patterson's closed formulas for `τ(u)`.

## RS-3: the quartic regime is log-critical, and its outliers are not Gauss sums (STRESSED)

For `Q_X = ((π/ρ)₄)` over primary degree-one primes of `Z[i]`:

- The outliers exist: `σ₁/edge` is 1.073, 1.105, 1.141, 1.181 at X = 2, 4, 8, 16·10⁴. The
  symmetry-matched random control gives 0.997.
- The BBP strength `θ_n = θ/√D` is 1.461, 1.574, 1.690, 1.810, growing by about 0.116 per
  doubling of X, so `θ_n ≈ 0.166·log X − 0.18`.
- The top singular vectors are *not* Gauss-sum vectors. The best twisted candidate projects
  only about 0.5 onto the top-16 subspace. The Rayleigh quotient of `conj(g̃)` is enhanced to
  about 1.5·√D but does not dominate.

**Conjecture:** in the BBP sense, the outlier vectors converge to the vector of Fourier coefficients
of the quartic theta function at primes. Those coefficients are *not known in closed form*
(David–Dunn–Hamieh–Lin 2023/2026; Eckhardt–Patterson 1992).

**Tests:**

- derive the `log X` growth from the X^{3/4} bias conjecture;
- compare the outlier vectors with any available numerics for the quartic theta coefficients.

## RS-4: compression of the quadratic Legendre matrix (STRESSED)

For `L_D = ((p_i/p_j))` over the first `D` odd primes:

```
singular values of L_D/√D  →  quarter-circle law on [0, 2], with an arithmetic correction:
m₄(D) = 2 − c₄/log D + o(1/log D),   c₄ ≈ 1.2
σ₁(L_D)/√D = 2 − c_e/log D + o(1/log D),   c_e ≈ 1.15
```

There are no outliers.

**Evidence:**

| D | m₄ | (2 − m₄)·log D | σ₁/edge | (1 − σ₁/edge)·log D |
|---:|---:|---:|---:|---:|
| 668 | 1.8081 | 1.248 | 0.9082 | 0.597 |
| 1228 | 1.8273 | 1.229 | 0.9206 | 0.565 |
| 2261 | 1.8430 | 1.212 | 0.9231 | 0.594 |
| 4202 | 1.8549 | 1.211 | 0.9310 | 0.576 |
| 7836 | 1.8663 | 1.199 | 0.9369 | 0.565 |
| 14682 | 1.8753 | 1.196 | 0.9397 | 0.579 |

A random matrix with the same reciprocity structure gives `m₄ = 1.997–1.998` and
`σ₁/edge ≈ 0.998`.

**Mechanism hypothesis.** By symmetry,

```
m₄ − 2 = (average over pairs p ≠ p' of |Σ_q (q/pp')|²)/D − 1,
```

where q runs over the primes in the index set. So RS-4 states that the mean square of real
character sums over primes, taken over the family of conductors `pp'`, is `π(X)·(1 − c/log)`.
That is a secondary term of Montgomery–Hooley / Barban–Davenport–Halberstam type.

**Contrast:** the cubic bulk shows no such deficit (`m₄ = 1.993` at D = 2248). A candidate reason
is that `χ² = 1` only for real characters.

## RS-5: no outliers for n ≥ 6 (REFUTED: registered finite-scale form)

**Heuristic:** an n-th order theta function with prime coefficients of size `N^{-(1/2 - 1/n)}`
gives a spike of order `X^{2/n}` against a bulk of `√X`:

- supercritical for n = 3;
- critical for n = 4;
- subcritical for n ≥ 5.

For n = 2 the theta function is supported on squares, so there is no spike at primes.

**Test:** sextic residue matrices over `Z[ω]`, and quintic over `Z[ζ₅]`.

## RS-6: bulk universality for n = 3, 4 after removing outliers (PILOT bulk; finite local extension REFUTED)

After deflating `O(1)` outliers, the singular-value distribution tends to the quarter circle with
no `1/log D` correction. Local statistics remain to be tested: spacings, and Tracy–Widom
fluctuations of the first non-outlier singular value.


## RS-S002: Phase-1a outcomes at X = 320000

Predictions remain exactly as committed at `0b77769`. Results and validation are in
`results/phase1_2026-10-24.json`; no asymptotic assertion is proved by this computation.

### RS-1: STRESSED

- **PASS** — `kappa3 in [1.38, 1.47]`. Measured 1.422127145.
- **PASS** — `cubic top-singular-vector overlap with conj(g~) within 0.03 of sqrt(1 - D/theta^2)`.
  Measured overlap 0.941510961, BBP prediction 0.948673890.

Both committed Phase-1 predictions pass at this scale, accompanied by the seed-0 matched control.
The X = 640000 predictions remain untested; the final budget decision is recorded below.

### RS-3: STRESSED

- **PASS** — `quartic theta_n = 0.166*ln X - 0.18 +- 0.05`.
  Measured theta/sqrt(D) = 1.922239066; formula = 1.924228662.

The committed Phase-1 growth prediction passes with its matched control at X = 320000.
This unit does not validate the proposed interpretation of the outlier vectors.

### RS-4: STRESSED

- **PASS** — `quadratic (2 - m4)*ln D in [1.0, 1.4]`.
  Measured correction 1.230641123, standard error
  0.021399855. The m4 estimate is 1.879653606
  with standard error 0.002092727, from 128 probes (seed 1).

The registered band contains the estimate and its two-standard-error interval.
Sigma1/(2 sqrt(D)) = 0.944136181; the matched control is recorded at the same D.

RS-1, RS-3 and RS-4 are STRESSED at X = 320000 for their committed Phase-1 predictions.
RS-2 and RS-6 remain PILOT; RS-5 remains UNTESTED.

### Larger-scale limit of this session

X = 640000 was **SKIPPED**, not passed or failed. Required-job runtime projections are
54.11 minutes (cubic), 48.89 (quartic), and
87.86 (quadratic), exceeding the 45-minute limit on this two-CPU-quota container.
These are planning estimates, not spectral measurements. The original predictions are unchanged.
All STRESSED labels above refer to X = 320000 only.


## RS-S003: pre-registered Phase-1b predictions (before test data)

The owner requested continuation here from the committed RS-S002 handover. Main remains
`9a038fa`; RS-S003 is based on `52d0854` on a separate branch, without merging main.
The machine-readable registration is `results/phase1b_2026-10-24.json`.

**RS-5, sextic at X = 40000 and 160000, both criteria at both scales:**

- `sextic sigma1/(2 sqrt(D)) <= 1.02`.
- `sextic (sigma1 - control_sigma1)/(2 sqrt(D)) <= 0.02`.

Use the same primary Eisenstein indices as cubic. Define zeta6 = 1 + omega, and the sextic
character by direct Euler exponentiation in the residue field: its square is the cubic character
and its cube the field-quadratic character. The seed-0 control has independent uniform
upper sextic exponents and the exact full pairwise reciprocity signs, with zero diagonal.
These signs need not have the simpler rank-one parity form used for quadratic/quartic matrices.

**RS-6, cubic and quartic at X = 20000 and 40000, all four comparisons:**

- `abs(mean_bulk_gap_ratio - control_mean_bulk_gap_ratio) <= 0.03`.

Deflate every singular value strictly above 2 sqrt(D), separately for arithmetic and seed-0
matched control. Sort the remaining m singular values ascending; take the half-open slice
[ceil(0.2 m), floor(0.8 m)). For consecutive gaps in that slice, average
min(delta_i, delta_(i+1))/max(delta_i, delta_(i+1)); a zero denominator contributes zero.
There is no unfolding, dropped tie, adjusted window, fitted cutoff or change after seeing data.

The tolerances are fixed finite-scale discrimination allowances, not calibrated confidence
levels. Every applicable prediction must pass before promotion. RS-5 promotion covers only
its tested sextic case; RS-6 promotion covers only this registered local statistic. Other
universality claims are not certified. Any failure is retained and prevents promotion.
No old Phase-1a prediction changes. No sextic spectrum or local statistic has been measured
before this registration is committed and pushed.


## RS-S003 incremental outcomes

### RS-5: registered finite-scale sextic formulation REFUTED

At X = 40000, D = 4178: sigma1/(2 sqrt(D)) = 1.029470034,
control = 0.996124577, normalized excess = 0.033345457.

- **FAIL** — `sextic sigma1/(2 sqrt(D)) <= 1.02`.
- **FAIL** — `sextic (sigma1 - control_sigma1)/(2 sqrt(D)) <= 0.02`.

The first registered scale fails both criteria, preventing STRESSED promotion. REFUTED here
refers to the explicit finite-scale formulation; an eventual asymptotic claim is not disproved
by this finite test. At that checkpoint the pre-registered X = 160000 run continued without changed tolerances,
character normalization, or control; its completed outcome follows below.

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

### RS-S003 disposition and scope

All eight finite comparisons FAIL. No STRESSED promotion follows from RS-S003. The REFUTED
labels refer to the registered finite-scale sextic formulation and local-statistic extension;
finite data do not disprove eventual asymptotic limits. The original RS-6 bulk claim remains
PILOT, and RS-1, RS-2, RS-3 and RS-4 retain their RS-S002 statuses. No prediction was revised.
Additional exact identities in a null ensemble require separate certification and fresh-scale
predictions; they must not retroactively change these outcomes.


## RS-S004: conjugation-matched null and pre-registered Phase-1c predictions (before test data)

**Certified identities** (exact tests in `tests/test_reciprocity_spectra.py`; machine record in
`results/phase1c_2026-10-25.json`): for n = 3, 4, 6, `(conj x/conj y)_n = conj((x/y)_n)`, and
the reciprocity mask is conjugation-invariant. Reciprocity plus conjugation force
`x = (π/conj π)_n` to satisfy `x = s·conj(x)`: `x = 1` (cubic), `x ∈ {±1}` or `{±i}` by
`p mod 8` (quartic), `s = +1` and `x = ±1` (sextic). For n = 3, `H = C·P` (P the conjugation
permutation) is exactly Hermitian and real in a real basis, so the cubic singular values are
the moduli of the eigenvalues of a real symmetric matrix. No further identity was found;
completeness is not claimed. The quadratic null (n = 2, no conjugation) is unchanged.

**Control:** `rs_random_conj` (seed 0), drawing one uniform exponent per {transpose,
conjugation} orbit and copying the (π, conj π) entries.

**Predictions (new IDs; RS-S003 outcomes are not changed):**

- **RS-S004-P6C-cubic / -quartic (X = 80000):**
  `abs(mean_bulk_gap_ratio - control_mean_bulk_gap_ratio) <= 0.03`, using the RS-S003 window,
  deflation and tie rules.
- **RS-S004-P1C (cubic, X = 80000):** `σ₁/edge − control σ₁/edge ≥ 0.40`.
- **RS-S004-P3C (quartic, X = 80000):** `σ₁/edge − control σ₁/edge ≥ 0.10`.
  For P1C/P3C the arithmetic σ₁ at this X is already known from the pilot; these test the
  corrected control.
- **RS-S004-P5C (sextic, X = 320000):** `0.035 ≤ σ₁/edge − control σ₁/edge ≤ 0.065`.
  This predicts that the sextic outlier persists above the corrected null.

The basis is the EXPLORATORY rows in the JSON: gap-ratio differences ≤ 0.02 at X = 20000 and
40000 over control seeds 0–2, and sextic excess 0.0325 and 0.0421 at X = 40000 and 160000.


## RS-S004 outcomes (scored verbatim against `ed4961d`)

| ID | mode | X | D | arithmetic | seed-0 conjugation control | value | outcome |
|---|---|---:|---:|---:|---:|---:|---|
| RS-S004-P6C-cubic | cubic | 80000 | 7796 | gap 0.424229725 | gap 0.417128495 | 0.007101230 | **PASS** |
| RS-S004-P1C | cubic | 80000 | 7796 | σ₁/edge 1.514342308 | 1.000965311 | 0.513376997 | **PASS** |
| RS-S004-P6C-quartic | quartic | 80000 | 7806 | gap 0.527786408 | gap 0.525672180 | 0.002114228 | **PASS** |
| RS-S004-P3C | quartic | 80000 | 7806 | σ₁/edge 1.140784463 | 0.999855787 | 0.140928676 | **PASS** |
| RS-S004-P5C | sextic | 320000 | 27554 | σ₁/edge 1.050189908 | 0.999755252 | 0.050434656 | **PASS** |

Status consequences (scope limited to the tests performed; finite data prove nothing):

- **RS-1, RS-3:** remain STRESSED. Their outliers stay far above the corrected null.
- **RS-4:** unchanged. The quadratic null needs no conjugation matching.
- **RS-5:** its registered finite form remains REFUTED.
- **RS-6:** its RS-S003 finite local extension remains REFUTED, and its original bulk claim
  remains PILOT. The qualified statement is registered as **RS-6C**.
- **RS-7:** new. It records the sextic outlier persisting above the corrected null.

## RS-6C: bulk gap ratio matches the conjugation-matched null (STRESSED at X = 80000)

For the cubic and quartic matrices, the mean bulk gap ratio (RS-S003 window rules) agrees within
0.03 with the conjugation-matched control at the same D. Evidence:

- EXPLORATORY: X = 20000 and 40000, seeds 0–2.
- Registered PASS: X = 80000.

Mechanism (exact for the symmetry class, heuristic for the statistics): in the cubic case the
singular values are the moduli of the eigenvalues of a real symmetric matrix. They therefore
interleave two eigenvalue sequences, which is consistent with the low ratio of about 0.42. The
quartic matrix is real in a real basis, and its ratio is about 0.53. Neither value has been
compared with a theoretical ensemble constant. The RS-S003 failure was caused by a null with
the wrong symmetry class; it was not an arithmetic deviation.

## RS-7: sextic outliers above the corrected null (STRESSED at X = 320000)

The sextic matrix over `Z[ω]` has `σ₁/edge` exceeding the conjugation-matched control by:

| X | excess | status |
|---:|---:|---|
| 40000 | 0.0325 | EXPLORATORY |
| 160000 | 0.0421 | EXPLORATORY |
| 320000 | 0.0504 | registered PASS |

This contradicts the RS-5 heuristic of no outliers for n ≥ 5 at these scales. At X = 320000 the
top three singular values are nearly degenerate: 348.650, 347.581 and 346.681 against a control
σ₁ of 331.907. This suggests a cluster of outliers rather than a single spike. The outlier
vectors and their mechanism are unidentified.


## RS-S005: pre-registered Phase-1d predictions for RS-7 (before X = 320000 data)

The exploratory basis is in `results/phase1d_2026-10-25.json`.

**Multiplicity.** The number of sextic singular values above the largest of three corrected
controls is:

- 7 at X = 40000 (D = 4178);
- 22 at X = 160000 (D = 14640).

**Delocalization.** The cluster vectors are delocalized: IPR·D ≈ 2.0–2.6.

**Gauss-sum candidates.** No single Gauss-sum candidate dominates. The best is conj(g̃6),
which projects 0.26 and 0.24 onto the top-24 subspace.

**Family span.** The span of conj(g̃6)·(u/π)₆ over N(u) ≤ 60 (210 vectors) is enriched over a
random span of equal dimension: by 1.55× at X = 40000 and by 2.35× at X = 160000.

**Working picture (hypothesis).** The cluster is many weak twisted-Gauss-sum spikes, which
cross the BBP threshold as X grows.

- **RS-S005-P7M (X = 320000):** the number of singular values (top 48) strictly above the seed-0
  conjugation-matched control σ₁ is ≥ 28. A count of 48 is censored and counts as ≥ 48.
- **RS-S005-P7F (X = 320000):** the conj(g̃6) twisted-family enrichment ratio, averaged over the
  top 8 right singular vectors, is ≥ 2.0.

The solver is Lanczos with tol 1e-11 and seed 2. The random-span seed is 5.


## RS-S005 outcomes (scored verbatim against `f3a1b75`)

| ID | X | D | value | registered criterion | outcome |
|---|---:|---:|---:|---|---|
| RS-S005-P7M | 320000 | 27554 | 34 (not censored, k = 48) | ≥ 28 | **PASS** |
| RS-S005-P7F | 320000 | 27554 | 2.962 | ≥ 2.0 | **PASS** |

The seed-0 control σ₁/edge is 0.999755, which reproduces RS-S004. The family projections of the
top 8 vectors are 0.17–0.36, against a random-span baseline of 0.084–0.092.

## RS-7a: the sextic cluster is a growing family of weak twisted-Gauss-sum spikes (STRESSED at X = 320000)

**Statement.**

- The number of sextic singular values above the conjugation-matched null grows with X:
  7, then 22, then 34 at X = 40000, 160000 and 320000.
- The top singular vectors are delocalized.
- The top singular vectors are increasingly enriched in the span of conj(g̃6)·(u/π)₆ over small
  u: enrichment is 1.55, 2.35 and 2.96 at the same scales.
- No single vector dominates: conj(g̃6) alone projects only about 0.24 onto the top-24
  subspace.

**Diagnostic at X = 40000.** The bulk m4 matches the controls (1.9994 against 1.9976–1.9992),
while the upper tail is stretched: the 0.99 quantile is 1.926 against 1.915–1.917.

**Status of the identification.** It is partial. The family span captures only part of each
vector, and the per-u spike strengths have not been measured. The mechanism is unknown, and the
cluster contradicts the subcritical RS-5 heuristic at these scales.


## RS-S006: pre-registered twist-dichotomy predictions (before X = 320000 / 640000 Rayleigh data)

**Set-up.** Let `w_u = conj(g̃6)·(u/π)₆`, normalized, and `r_u = ‖C w_u‖/√D`. In the
spiked model, `r_u² − 1 = θ_u²/D`, and a twist is individually supercritical iff `r_u > √2`.

**EXPLORATORY findings** (`results/phase1e_2026-10-25.json`, X = 20000–160000):

- **No twist is individually supercritical.** The maximum is r₁ = 1.379 at X = 160000.
  - So "count the supercritical twists" predicts 0 outliers where 7–22 are observed. That model
    FAILS.
  - A synthetic model (control plus subcritical spikes with random left directions) gives about 16
    small outliers at X = 40000, against 7 larger ones observed. That model also FAILS.
- **Dichotomy (exact at every tested scale).** Among "+" twists by u coprime to 3, every
  ±primary u (d ≡ 0 mod 3, the normalization of the index primes) has r ≥ 1.117. Every other
  associate has r ≤ 0.980, below the random level of about 1.0.
- **Ramified twist.** The ramified u = 1 − ω is strong with the conjugate sign, as in the cubic
  RS-2 family.
- **Strength profile.** Strength decays slowly with N(u) and grows with X.
- **Exact symmetry.** Twisting by (−1/π)₆ leaves r unchanged. Conjugation sends g6(π) to
  (−1/π)₆·conj(g6(π̄)), which forces `Re⟨C w₊, C w₋⟩ = 0`. The null already shares this.

**Mechanism hypothesis (unproved).** For ±primary u, sextic reciprocity turns (u/π)₆ into a
character of π modulo u. The family is then twisted Gauss sums, as in RS-2. A non-primary
associate adds a unit supplementary factor, which destroys the alignment.

**Predictions (N(u) ≤ 100, 246 elements u coprime to 3):**

- **RS-S006-P7S-320000 and RS-S006-P7S-640000.** Both conditions must hold:
  - min r over ±primary u ≥ 1.10;
  - max r over the other associates ≤ 1.02.
- **RS-S006-P7U-320000.** r₁ ∈ [1.370, 1.420].
- **RS-S006-P7U-640000.** r₁ ∈ [1.375, 1.435].


## RS-S006 outcomes (scored verbatim against `feca6a1`)

| ID | X | D | value | criterion | outcome |
|---|---:|---:|---|---|---|
| RS-S006-P7S-320000 | 320000 | 27554 | min ±primary 1.1745; max other 0.9802 | ≥ 1.10 and ≤ 1.02 | **PASS** |
| RS-S006-P7U-320000 | 320000 | 27554 | r₁ = 1.3963 | [1.370, 1.420] | **PASS** |
| RS-S006-P7S-640000 | 640000 | 52008 | min ±primary 1.1907; max other 0.9824 | ≥ 1.10 and ≤ 1.02 | **PASS** |
| RS-S006-P7U-640000 | 640000 | 52008 | r₁ = 1.4183 | [1.375, 1.435] | **PASS** |

These are the first sextic computations at X = 640000. Random-phase vectors give r ≤ 1.0054
there. r₁ = 1.4183 exceeds √2 = 1.4142, so in the spiked-model reading the u = 1 twist has just
become individually supercritical (θ₁/√D ≈ 1.006). That reading is model-dependent: no spectrum
was computed at X = 640000.

## RS-7b: primary-class twist dichotomy (STRESSED at X = 640000)

**Definitions.**

- `w_u = conj(g̃6)·(u/π)₆`, with u coprime to 3 and the index primes π primary.
- `r_u = ‖C w_u‖/(√D ‖w_u‖)`.

**Statement.** Two properties hold:

- If u is ±primary (u ≡ ±1 or ±2 mod 3, i.e. d ≡ 0 mod 3), then `r_u` is bounded away above 1.
  The observed minimum is 1.117–1.191, rising with X.
- If u is any other associate, `r_u` lies below the random level of 1.
  The observed maximum is 0.945–0.982.

**Scale dependence.** Strengths decay slowly with N(u) and increase with X. r₁ was 1.322, 1.354,
1.362, 1.379, 1.396 and 1.418 for X from 2·10⁴ to 6.4·10⁵.

**Tested range.**

- N(u) ≤ 100 at X = 20000, 80000, 320000 and 640000.
- N(u) ≤ 300 at X = 40000 and 160000.

**Status.** This is a finite-range observation. The mechanism is an unproved hypothesis: sextic
reciprocity makes `(u/π)₆` a character of π modulo u exactly when u is in the index
normalization.

**How it explains RS-7a.** The cluster comes from a large family of near-critical twisted spikes.
No single twist is individually supercritical below X ≈ 6·10⁵. Two simple quantitative models of
the cluster multiplicity fail (records in the JSON).


## RS-S007: mechanism stage for RS-7b

Data are in `results/phase1f_2026-10-25.json`.

### Exact results

These are tested in `test_sextic_unit_symbols_are_characters_of_the_norm`.

- `(ζ₆ʲ/π)₆ = ζ₆^{j(p−1)/6}`. This is a Dirichlet character of p = N(π) modulo 36. For an
  associate u′ = ζ₆ʲu, it gives `(u′/π)₆ = ζ₆^{j(p−1)/6}·(u/π)₆`.
- The extra factor depends only on p mod 4, as `(−1/p)`, exactly for j ∈ {0, 3}, i.e. u′ = ±u.
  For every other j it depends on p mod 9 or p mod 18, so it is ramified at 3.
- RS-7b therefore says: **a twist of conj(g̃6) is enhanced exactly when its unit-class factor is
  unramified at 3.** Ramification at 3 is necessary for suppression in every case checked. That
  it is also sufficient is an observation.
- Associate sum rule (exact). Orthogonality of the six unit characters gives
  `Σ_j ‖C D_j w‖² = 6 Σ_{c mod 36} ‖C w|_{p≡c}‖²`. This holds to a relative error of 2.3e-16
  (X = 20000, u = 2).

### Measured, not explained

| X | mean Σ(r²−1) over associates | ±primary mean r²−1 | other mean r²−1 |
|---:|---:|---:|---:|
| 40000 | 0.04 ± 0.11 | 0.339 | −0.159 |
| 640000 | 0.75 ± 0.29 | 0.528 | −0.077 |

So the compensation among associates is approximate, and it drifts with X.

- **Strength profile:** `θ_u²/D ∝ N(u)^α` with α = −0.17 to −0.21, stable for X from 2·10⁴ to
  6.4·10⁵. The naive theta-coefficient heuristic, `|τ(u)|² ∝ N(u)^{−2/3}`, **FAILS**.
- **Bias:** the plain twisted Gauss-sum mean, `|Σ conj(g̃6) ζ₆^{j(p−1)/6}|/√D`, is largest in
  the unramified classes j = 0 and 3 at every X ≥ 40000. It reaches 2.62 at X = 640000, against
  ≤ 0.76 for the ramified classes. That is only marginally above the random range of 1.7–2.2,
  so it is suggestive and not decisive.

**Mechanism status:** UNEXPLAINED. The ramification criterion is exact as algebra but empirical as
an equivalence. The cause of the strength and its N(u) profile is open.


## RS-S009: registration of Astra's cubic-calibration prediction (before data)

The source is `ASTRA_RESPONSE_2026-10-25.md`, check 2. It was written without access to these
measurements.

- **RS-S009-A2-exponent (X = 40000).** Take cubic twists `conj(g̃3)·(u/π)₃` over ±primary u
  coprime to 3, with 1 < N(u) ≤ 200. The fitted slope of `log(r_u² − 1)` against `log N(u)` lies
  in [−0.433, −0.233], i.e. −1/3 ± 0.1. If any twist has r ≤ 1, the fit is undefined and the
  outcome is FAIL.
- **RS-S009-A2-count (X = 40000).** At least 24 cubic singular values exceed the seed-0
  conjugation-matched control σ₁.

### RS-S009 outcomes at X = 40000 and new registration for X = 160000

**Registered outcomes at X = 40000.**

- **RS-S009-A2-exponent: FAIL.** The fit is undefined: 18 ±primary cubic twists have r ≤ 1.
- **RS-S009-A2-count: FAIL.** 19 singular values exceed the control σ₁, fewer than 24.

These outcomes stand.

**EXPLORATORY diagnostics (after scoring).**

- The weak twists are exactly the u whose cube-free part is not squarefree: 2², π₇², 4π₇, π₁₃²,
  4π₇². They have r = 0.90–0.93.
- Over squarefree u the slope is −0.377, consistent with Astra's −1/3.
- r₁ = 2.64 (θ₁²/D = 5.99, matching Astra's 5.9).
- 98 ±primary twists have r > √2.
- The other associates have max r = 0.931, so the cubic case has the same associate dichotomy.
- In the sextic case, the same square u are enhanced (r ≈ 1.15–1.23 at X = 160000). This is
  consistent with the Chinta–Friedberg–Hoffstein expectation that sextic coefficients at squares
  are nonzero.

**Registered for X = 160000 (cubic twist strengths not yet computed there).**

- **RS-S009-C1-slope.** Over squarefree ±primary u with 1 < N(u) ≤ 200, the slope lies in
  [−0.433, −0.233].
- **RS-S009-C2-squarefree.** min r over the squarefree ±primary u > 1.05, and max r over the
  non-squarefree ±primary u < 1.0.
- **RS-S009-C3-associates.** max r over the non-±primary associates < 1.0.

### RS-S009 outcomes at X = 160000 (scored verbatim against `98118bf`)

| ID | value | outcome |
|---|---|---|
| RS-S009-C1-slope | −0.3634 | **PASS** |
| RS-S009-C2-squarefree | min squarefree r 1.511; max non-squarefree r 0.934 | **PASS** |
| RS-S009-C3-associates | max other-associate r 0.929 | **PASS** |

At this scale r₁ = 3.057.

## RS-8: cubic twist law (STRESSED at X = 160000)

**Definitions.** w_u = conj(g̃3)·(u/π)₃, with u coprime to 3. The squarefree condition refers
to the cube-free part of u.

**Statement.**

1. If u is ±primary and squarefree, the twist is enhanced, with r_u² − 1 ∝ N(u)^{≈−1/3}.
2. If u is ±primary but not squarefree, r_u < 1.
3. For every other associate, r_u < 1.

**Interpretation.** This matches Patterson's cubic theta coefficients: they are unimodular at
squarefree arguments, and the size of the residue gives −1/3 (Astra's derivation). Many of these
twists are individually supercritical. The cubic outliers (RS-2) are this family.

**Calibration value.** This is the cubic analogue of RS-7b, where the theory is known. The sextic
exponent −0.19 is near Astra's predicted −1/6. In the sextic case squares stay enhanced,
consistent with Chinta–Friedberg–Hoffstein.


## RS-S010: registration of Astra's Q5 test and corrected versions (before X = 1.28·10⁶ data)

**Exploratory results** (to X = 3.2·10⁵; `results/phase1h_2026-10-25.json`), in the trace form
with n a product of primary primes:

| class | \|T\| / √count | local slope |
|---|---:|---:|
| j = 1, 2 | 2.84 | ≈ 0.71 |
| j = 4, 5 | 2.2 | ≈ 0.59 |
| j = 0, 3 | 0.34 | — |

This is the opposite of Astra's prediction. At the prime level, the matrix normalization
(factor (ρ̄/ρ)₆) moves the strong classes to j = 0 and 3 (2.05 random-walk units against
≤ 0.53). Astra's check 3 said this factor cannot create a 3-adic effect; the data contradict that.

**Registered for X = 1.28·10⁶:**

- **RS-S010-ASTRA-Q5.** Astra's prediction, as stated: the slope of |T₀| lies in 2/3 ± 0.1 and
  the slope of |T₁| is ≤ 0.6.
- **RS-S010-K1-trace.** The slope of |T₁| lies in [0.55, 0.85]; |T₁|/√count ≥ 3.0; and
  |T₀|/√count ≤ 2.0.
- **RS-S010-K2-primes-matrix-norm.** In the matrix normalization at primes, class 0 is ≥ 2.0
  random-walk units, and classes 1, 2, 4 and 5 are each ≤ 1.5.

Slopes are fitted on the dyadic grid for X ≥ 128000.

### RS-S010 outcomes at X = 1.28·10⁶ (scored verbatim against `e745eaa`)

The run had D = 98512 split primes and 361287 squarefree n.

| ID | value | outcome |
|---|---|---|
| RS-S010-ASTRA-Q5 | slope of \|T₀\| 0.614; slope of \|T₁\| 0.602 (> 0.6) | **FAIL** |
| RS-S010-K1-trace | slope of \|T₁\| 0.602; \|T₁\|/√count 3.27; \|T₀\|/√count 0.74 | **PASS** |
| RS-S010-K2-primes-matrix-norm | classes 0, 3: 2.63; classes 1, 2: 0.61; classes 4, 5: 0.90 | **PASS** |

A design lesson: slope fits are uninformative for classes with no main term. T₀ fluctuated (183,
607, 443 on the last grid points) and landed inside the band by chance. The magnitude ratios are
the reliable statistic.

**Correction (exact, after the run).** (ρ̄/ρ)₆ = ±1 is determined by (a, b) mod 4, and is +1
for p ≡ 3 (mod 4). This is tested to 2·10⁴ and checked to 2·10⁵. Astra's check 3 ("2-adic
only") is therefore **correct**. The registration text above, which said the data contradict it,
is withdrawn; it stays visible for the record.

## RS-9: unit-class selection of the Gauss-sum main term (STRESSED at X = 1.28·10⁶)

**Statement.** For sextic Gauss sums:

- In the trace form (Heath-Brown–Patterson normalization, n a product of primary primes), the
  Kubota sums over squarefree n carry growing main terms in the ω-rotated unit classes j = 1, 2
  (and 4, 5). They carry none in j = 0, 3.
- Over primes, the matrix normalization differs from the trace form only by the 2-adic sign
  (ρ̄/ρ)₆. There the bias sits in j = 0, 3, and the ω-rotated classes are at or below random.

**Interpretation.** RS-7b (the matrix dichotomy) is the matrix shadow of the second statement.

**Open.** Why a purely 2-adic sign moves the main term between classes that differ at 3. A
plausible route is the 2-adic cubic factor (2/ρ)₃ in the Hasse–Davenport factorization, but this
is not derived.
