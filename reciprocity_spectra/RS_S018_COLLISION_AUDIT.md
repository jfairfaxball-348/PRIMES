# RS-S018: collision audit of the surviving core

**Date:** 2026-10-26. **Stage:** collision-audit. No new matrices were built.

**Tools.**

- Parallel web search and fetch; the queries are in §6.
- One stored-data consistency check, `scripts/audit_collision.py`, which writes
  `results/rs_s018_collision_checks_2026-10-26.json`.

A negative search is not novelty. Statuses use the PROTOCOL vocabulary. Every external fact below
is cited.

## 1. The three statements audited

Notation:

- R₆(X) is the sextic residue matrix on primary degree-one primes of ℤ[ω] with N ≤ X, of
  dimension D;
- g̃₆ is the normalized sextic Gauss sum;
- w_κ = conj(g̃₆)·Π_π (π/·)₆^{e_π};
- r_κ = ‖R₆ w_κ‖/(‖w_κ‖√D);
- ε_κ = (r_κ² − 1)/(r₁² − 1);
- s_κ = ε_κ·N₆(κ)^{1/6};
- t = N₆(κ)/X.

**(i) CAND-001 statement 2 (RS-9).** In the matrix normalization, consider the unit-class sums
|Σ_{Nρ≤X} g̃₆(ρ)·conj((ζ₆ʲ/ρ)₆)|.

- For j ∈ {0, 3}, they grow faster than √π(X).
- For j ∈ {1, 2, 4, 5}, they are O(√(X/log X)·X^{o(1)}).

In the trace normalization of Heath-Brown and Patterson, the main terms move to j = 1, 2, 4, 5
instead. Registered PASS at X = 1.28·10⁶ (RS-S010-K2).

**(ii) Mean form of law (B).** For κ = π⁵ and t → ∞, s_κ → −c₅, with c₅ ≈ 1.05. This is registered
PASS twice: RS-S015-P2 (−1.050) and the mean clause of RS-S017-Q3 (−0.966 at 6.4·10⁵ and −1.051 at
10⁶).

**(iii) (A″), the crossover law.** For κ with every exponent in {1, …, 4},
s_κ(X) = F(N₆(κ)/X) + o(1), where:

- F is a single decreasing function, independent of the exponent pattern;
- F(0⁺) = c ∈ [0.80, 1.00];
- F(t) ≈ 0 near t ≈ 1.

This is registered PASS on 440 fresh classes (RS-S017 Q1, Q2 and Q4).

## 2. Theory relevant to all three

**Twisted Gauss sums and theta coefficients.**

- Twisting by a symbol is a shifted Gauss sum: g_n(r, c) = conj((r/c)_n)·g_n(1, c) for (r, c) = 1.
  Source: Bröker–Hoffstein, arXiv 1312.0568, Lemma 3.2.
- The Dirichlet series Σ_c g_n(r, c)·N(c)^{−s} has its principal residue proportional to the
  Fourier coefficient τ_n(r) of the n-fold-cover theta function (same source, §1). Patterson and
  Kazhdan–Patterson are the origin of this theory.
- Hence the prime sum Σ_ρ g̃₆(ρ)·conj((u/ρ)₆) is the prime-restricted first moment of g̃₆(u, ·).
  Its expected main term is governed by τ₆(u).

**Size.** For general n, Patterson's heuristic gives a first moment of order X^{1/2+1/(2n)} over
primes:

- n = 3 gives X^{5/6} (proved under GRH; Dunn–Radziwiłł, Ann. of Math. 200 (2024), arXiv
  2109.07463);
- n = 4 gives X^{3/4} (conjectured; David–Dunn–Hamieh–Lin, arXiv 2306.11875, Conj. 1.2);
- n = 6 gives X^{2/3}.

DDHL note that even an X^{5/6+ε} upper bound is hard for n ≥ 5.

**Hecke relations and periodicity for n = 6.** Bröker–Hoffstein §1, from Kazhdan–Patterson:

- τ₆(p⁵) = 0;
- τ₆(p⁴) = G₁(1, p), which has modulus 1;
- τ₆(p) = G₂(1, p)·τ₆(p³);
- τ₆(m·p⁶) = τ₆(m)·N(p)^{1/2}.

Bröker–Hoffstein's Lemma 5.3 adds: for |π| ≡ 1 mod 12, τ₆(π²) ≠ 0 forces (π/π̄)₆ = 1.

**Norm level.**

- The sextic large sieve is sharp: Ξ₆(Q, Q) ≫ Q^{7/6−ε}, via Gauss-sum vectors, on squarefree
  ideals. Source: Xu–Sang, arXiv 2610.17675v2 (14 Oct 2026), Thm 1.1, matching de Faveri's upper
  bound.
- The same paper bounds second moments of prime sums of sextic characters, Σ_u |Σ_π ψ_u(π)|², below
  the general norm (Thm 1.2). Its coefficients are unweighted characters over primes, not
  Gauss-sum vectors.
- Earlier, cubic and quartic non-orthogonality was established unconditionally by de Faveri–Dunn–
  Hoffstein, arXiv 2607.07911.

## 3. Stored-data check of the theta-coefficient reading

If the twist excess were a direct readout s ∝ |τ₆(u)/τ₆(1)|², then Lemma 5.3 would force π² classes
with N ≡ 1 mod 12 and (π/π̄)₆ ≠ 1 to lose their enhancement.

The check uses stored singles (RS-S015 to RS-S017) with t < 10⁻²:

| class group | n | mean s | sd |
|---|---:|---:|---:|
| k = 2, N ≡ 1 (12), (π/π̄)₆ ≠ 1 (τ₆(π²) = 0 by BH 5.3) | 14 | 0.848 | 0.021 |
| k = 2, N ≡ 1 (12), (π/π̄)₆ = 1 | 12 | 0.843 | 0.011 |
| k = 2, N ≡ 7 (12) | 38 | 0.868 | 0.038 |
| k = 1, all groups | 184 | 0.894–0.903 | ≤ 0.040 |
| k = 3, both groups | 16 | 0.844–0.846 | ≤ 0.016 |
| k = 4, N ≡ 7 (12) | 6 | 0.832 | 0.016 |

**Reading.** The enhancement is uniform across the BH vanishing condition. So the matrix excess is
**not** the naive |τ₆(u)|² in BH's normalization. One of two things is true:

- the correspondence passes through an averaging over the coset/normalization choices V, or over the
  row primes σ, through τ₆(σu), and that averaging is not identified here;
- or the matrix quantity is a different object.

This is a finite-data observation about our mapping, not a statement about BH's coefficients.

## 4. Status by statement

| Statement | Status | Specific overlap |
|---|---|---|
| (i) Existence of a growing unit-class main term in sextic Gauss sums over primes | **KNOWN_IMPLIED (conjectural)**: it follows from the Patterson–Kubota residue heuristic (X^{2/3} for n = 6); no proof is known for n ≥ 5 (DDHL) | Patterson 1987; Kazhdan–Patterson 1984; DDHL 2023–26 |
| (i) The exact unit-class selection rule (j ∈ {0, 3} in matrix normalization, moved by the 2-adic sign) | **NOVELTY_REQUIRES_EXPERT_REVIEW**: it should be determined by the unit-support of τ₆ under the chosen V; no explicit statement found | BH §2 (V-dependence of τ(r, V)); Xu–Sang (one unit class carries ≥ 1/6 of the energy; no selection rule) |
| (ii) Non-enhancement of π⁵ classes | **KNOWN_IMPLIED (heuristic)**: consistent with τ₆(p⁵) = 0 | BH §1, Kazhdan–Patterson |
| (ii) The negative constant: s → −1.05 for t ≫ 1, and a weak deficit (about −0.2) at small t | **SEARCHED_NO_COLLISION_FOUND** | none |
| (iii) Crossover s = F(N₆/X), universal across exponent patterns, positive fixed-class limit | **SEARCHED_NO_COLLISION_FOUND**. The scale N₆ ≍ X is the expected conductor-versus-length transition (level-aspect Voronoi: DR24 §5), so the existence of a transition is POSSIBLE_OVERLAP; the universal profile is not found, and §3 shows it is not the naive τ₆ readout | DR24 §5 (level-aspect Voronoi); BH Lemma 5.3 (contrast) |
| RS-7/RS-7a: sextic outliers above the null | Upgraded from SEARCHED_NO_COLLISION_FOUND to **POSSIBLE_OVERLAP / partly KNOWN at norm level**: Gauss-sum vectors give sharp Rayleigh quotients for the sextic character matrix | Xu–Sang 2610.17675 Thm 1.1 |

## 5. Decision

(ii)'s negative constant and (iii) remain SEARCHED_NO_COLLISION_FOUND, and both have registered
evidence. (iii) is the stronger:

- it passed on 440 unseen classes, at two scales;
- the §3 check shows it is not a direct readout of known or conjectured theta coefficients.

(i) is mostly theory-implied, apart from its selection rule.

**Candidate draft for RS-S019 (not frozen; no ID allocated).** *Sextic twist-class crossover law*
(matrix form), in the notation of §1.

1. For each class κ with every exponent in {1, …, 4}, s_κ(X) − F(N₆(κ)/X) → 0 as X → ∞, uniformly
   in κ with N₆(κ)/X bounded. F is one decreasing function, independent of κ, with
   F(0⁺) = c > 0. In particular, lim_{X→∞} r_κ(X) > 1 for every such fixed κ.
2. For κ = π⁵, s_κ(X) → −c₅ < 0 as N(π)⁵/X → ∞, and lim sup_X r_κ(X) ≤ 1 for every fixed κ
   containing an exponent 5.

**Evidence.**

- Discovery: RS-S015/16, 400 single-class points.
- Holdout: RS-S017, 440 fresh classes, PASS for statement 1; statement 2 passes in mean form.
- The finite estimates c ∈ [0.83, 0.95] and c₅ ∈ [0.97, 1.11] are evidence, not part of the
  statement.

**Novelty.** NOVELTY_REQUIRES_EXPERT_REVIEW. The sextic theta-coefficient and Gauss-sum community
is the natural reviewer: Hoffstein, Dunn, de Faveri, Bröker; for the norm-level framing, Xu–Sang.

**Known caveats.**

- The fixed-class limit in statement 1 is an extrapolation: the plateau drifts from 0.85 at
  t ≈ 10⁻³ to 0.94 at t ≈ 10⁻⁴·⁵.
- Statement 2's fixed-class limit at small t is open: about −0.2 at π = 2.
- The mapping to τ₆ is unresolved (§3).

## 6. Queries (Parallel search, 2026-10-26)

- Patterson distribution of general Gauss sums at prime arguments
- Patterson conjecture n-th order Gauss sums primes main term theta
- sextic Gauss sums prime arguments bias
- Bröker Hoffstein Fourier coefficients sextic theta series
- Chinta Friedberg Hoffstein sextic theta conjecture coefficients
- Kazhdan Patterson theta coefficients prime powers vanish
- twisted cubic Gauss sums sum over primes residue symbol twist
- cubic Gauss sums twisted by character uniformity conductor
- Dunn Radziwill bias cubic Gauss sums twisted
- Kazhdan Patterson metaplectic forms theta Fourier coefficients units
- residue Dirichlet series Gauss sums g_n(r,c) theta coefficient tau(r)
- Patterson 1987 general Gauss sums prime arguments
- singular values matrix power residue symbols primes
- random matrix Legendre symbol matrix primes spectrum outliers
- sextic residue symbol matrix eigenvalues Gauss sums
- sextic Gauss sums over primes 2025
- sixth order Gauss sums bias primes theta
- non-orthogonality sextic large sieve

**Fetched:** arXiv 2306.11875v4 (DDHL), arXiv 1312.0568 (BH), arXiv 2610.17675v2 (Xu–Sang).
