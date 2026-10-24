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

## RS-6: bulk universality for n = 3, 4 after removing outliers (PILOT)

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
by this finite test. The pre-registered X = 160000 run continues without changed tolerances,
character normalization, or control.
