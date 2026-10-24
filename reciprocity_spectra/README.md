# Reciprocity Spectra

**A new PRIMES research programme, opened 2026-10-24.**

**Status: PILOT POSITIVE.** Live, model-discriminating structure has been found and the open
questions are identified. Nothing is proved. No novelty claim is made beyond the search scope
recorded in `PRIOR_ART.md`.

## The idea in one paragraph

Put the law of reciprocity into a matrix. Take every prime of norm `≤ X` in a ring where n-th power
reciprocity holds:

- odd rational primes, for n = 2;
- primary Eisenstein primes in `Z[ω]`, for n = 3;
- primary Gaussian primes in `Z[i]`, for n = 4.

Form the matrix `R_n(X) = ((π/ρ)_n)` of power-residue symbols between them. Reciprocity fixes the
matrix's symmetry type. Otherwise its entries look like independent n-th roots of unity. So
random-matrix theory gives a sharp, parameter-free null model, and **every deviation from it is
arithmetic**. A pilot computation, with matrices of dimension up to 14,682, found three distinct
regimes.

| n | What the spectrum does | Mechanism (hypothesis) |
|---|---|---|
| 3 | **Supercritical outliers.** The top singular value leaves the random bulk exactly like a spiked random matrix with spike strength `θ ≈ 1.42·X^{2/3}/log X`; the constant holds to ±0.01 over a 32-fold range of X. The singular vector is the vector of normalized cubic Gauss sums, with overlap 0.936 against a predicted 0.939. A whole *family* of further outliers matches Gauss sums twisted by `(u/π)₃` for u = 2, 1−ω and primes of norm 7, 13, 19, …. | Kubota–Patterson cubic theta function; the outlier spectrum appears to realize its Fourier coefficients. |
| 4 | **Slowly growing outliers.** `σ₁/edge` = 1.07 → 1.18 as X goes from 2·10⁴ to 1.6·10⁵, with spike strength growing like `log X`. The singular vectors are *not* Gauss-sum vectors. | Quartic theta function, whose Fourier coefficients at primes are not known in closed form. The outliers may give a numerical window onto them. |
| 2 | **No outliers, but a compressed spectrum.** The singular values of the Legendre matrix of the first D primes approach the quarter-circle law with an arithmetic correction: `(2 − m₄)·log D ≈ 1.20` and edge `≈ 2√D·(1 − 0.58/log D)`, steady for D = 668 to 14,682. | Montgomery–Hooley-type secondary term in mean squares of real character sums over primes. |

A uniformly random matrix with *exactly the same reciprocity symmetry* shows none of these effects:
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

## Immediate next step

Phase 1 of `ROADMAP.md`. Store matrices as uint8 exponents with blockwise matrix–vector products to
reach X = 6.4·10⁵. Before running, pre-register the predictions: κ₃ ∈ [1.38, 1.47]; cubic overlap
within 0.03 of the BBP value; quartic `θ_n ≈ 0.166·log X − 0.18`; quadratic `(2 − m₄)·log D` in
[1.0, 1.4]. Then run the n = 6 test of RS-5.
