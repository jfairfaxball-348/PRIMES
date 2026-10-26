# RS-S014: sixth-power-class audit of the sextic strength law

**Date:** 2026-10-26.

**Stages:** falsification and certification. This is an audit of existing evidence; no new
large-scale matrices were built.

**Execution.** The run was in the cloud session on `ccr-c363c6bb-0zejeu`, at the owner's request
("run s014"), after main was fast-forwarded to RS-S013 (`db46d65`). The RS-S013 handoff assumed a
local Windows run. The scope is unchanged:

- no fresh-scale matrices;
- no new CAND;
- no proof-route fallback.

**Machine record.** `results/rs_s014_invariance_2026-10-26.json`. Regenerate it with
`scripts/audit_invariance.py`, and verify it with `--check`.

## 1. Exact identities

These are tested in `test_sextic_twist_classes_sixth_powers_and_inversion`. Fix u and v in ℤ[ω],
both coprime to 3, and let ρ be an indexed (primary, split) prime.

1. **Sixth powers.** (u v⁶/ρ)₆ = (u/ρ)₆ if ρ ∤ v, and = 0 if ρ | v. So w_{uv⁶} = w_u · 1_{ρ∤v}.
2. **Fifth powers are conjugate twists.** (u⁵/ρ)₆ = conj((u/ρ)₆), because the symbol values are
   sixth roots of unity. So w_{u⁵} is exactly the conjugate ("−") twist of u, including the rows
   with ρ | u (zero on both sides).
3. **Units.** Twisting by (−1/ρ)₆ leaves r unchanged exactly (RS-S006). Together with
   r_u = r_{−ū} (RS-S009), this gives r_u = r_{−u} = r_ū = r_{−ū}.
4. **Classes.** For ±primary u, r_u depends only on the **twist class**: the exponent vector
   (e_π mod 6) of u over primary primes (`arith.sextic_twist_class`). It is exactly independent of
   the representative when no indexed prime divides the sixth-power part. In general it is
   independent in the limit (§2).
5. **The exact factorization** `arith.eisenstein_factorization` reconstructs u. Its unit index uses
   ζ₆ = 1 + ω. The sixth-power-free norm is N₆(u) = Π N(π)^{e_π mod 6}.

**Example.** 32 = 2⁵ is ±primary and coprime to 3, and 2 divides no indexed prime. So
**r₃₂(X) = r₂⁽⁻⁾(X) exactly**. The stored values are 0.938, 0.948, 0.967, 0.976, 0.970 and 0.966 at
X = 2·10⁴, …, 6.4·10⁵.

## 2. Lemma: limit invariance under u → u v⁶

**Setting.** Let k be the number of indexed primes dividing v but not u (k ≤ ω(v)). Let
d = w_u − w_{uv⁶}, so ‖d‖² = k and ‖w_{uv⁶}‖² = D_u − k.

**Bound.** By the triangle inequality, |‖C w_{uv⁶}‖ − ‖C w_u‖| ≤ σ₁(C)·√k. Hence

```
| r_{uv⁶} − r_u·sqrt(D_u/(D_u − k)) | ≤ σ₁(C)·sqrt(k) / sqrt(D (D_u − k)).
```

The n-th order large sieve of Blomer–Goldmakher–Louvel (Thm 1.3; n = 6, K = ℚ(ω); see
`RS_S013_LITERATURE.md` §1) gives σ₁(C)² ≪_ε X^{4/3+ε}. Our element conventions differ from their
ideal family only by unimodular diagonal and finite ray-class factors, which do not change
singular values. **This matching is still to be written out in full; it is a caveat on the
lemma.** With D ≍ X/log X:

- the right-hand side is ≪ X^{−1/3+ε};
- r ≤ σ₁/√D ≪ X^{1/6+ε}.

So r_{uv⁶}² − r_u² ≪ X^{−1/6+2ε} → 0.

**Conclusion.** For fixed u and v, any limit of ε_u = (r_u² − 1)/(r₁² − 1) is unchanged by u → u v⁶,
whenever r₁² − 1 stays bounded away from 0. The trivial class u = 1 is enhanced in every
computation (r₁ = 1.32 → 1.43). **Any valid strength law is therefore a function of the twist
class.** In particular, the frozen RS-S012 law in N(u) is impossible (RS-S013, u = 64).

## 3. Stored evidence by twist class

Source: the phase1e twist runs (X = 2·10⁴ … 6.4·10⁵) and the phase1j sextic run (X = 10⁶). The
statistic is the mean of ε·N(π)^{k/6} for single-prime classes π^k. The sixth-power-free-norm
law predicts +1 for every k.

| X | k = 1 | k = 2 | k = 3 | k = 4 | k = 5 |
|---:|---:|---:|---:|---:|---:|
| 2·10⁴ | 0.954 | 0.914 | 0.887 | 0.534 | −1.18 |
| 4·10⁴ | 0.886 | 0.845 | 0.866 | 0.367 | −1.18 |
| 8·10⁴ | 0.907 | 0.887 | 0.885 | 0.653 | −0.95 |
| 1.6·10⁵ | 0.894 | 0.890 | 0.896 | 0.554 | −1.03 |
| 3.2·10⁵ | 0.927 | 0.916 | 0.914 | 0.815 | −1.00 |
| 6.4·10⁵ | 0.943 | 0.940 | 0.940 | 0.827 | −0.97 |
| 10⁶ | 0.947 | 0.945 | 0.941 | — | — |

The counts per X are in the JSON: k = 1 has 48–120 classes, k = 5 has 48–120, and k = 2, 3, 4 have
2–10. Spreads are also in the JSON; for k = 5 the spread is 0.28–1.26, dominated by small N(π).

**By norm, for k = 5:**

- N(π) ≥ 19: ε·N^{5/6} = −1.02 to −1.11 in every norm band at X = 1.6·10⁵ and 6.4·10⁵.
- N = 4 (inert 2): −0.17 to −0.21.
- N = 7, 13: −0.65 to −0.87.

**Raw r by exponent pattern** (stored ±primary twists; multi-prime patterns are from N(u) ≤ 300):

| pattern | r (min–max across scales) | behaviour |
|---|---|---|
| (1), (2), (3), (1,1), (1,2), (1,1,1) | 1.12–1.34 | enhanced, increasing with X |
| (4) | 0.997–1.15 | enhanced at all X ≥ 8·10⁴; one value 0.997 at X = 4·10⁴ |
| (5), (5,5), (4,5) | 0.90–1.03 | **not enhanced**; group means 0.96–1.00 |
| (5,5,5) | 1.017–1.023 | two twists only |

## 4. Obstructions

**O1: statement 1 of CAND-001 in its universal form ("every ±primary u is enhanced").**

- By identity 2, the statement includes every class π⁵ (for example u = 32 = 2⁵ or u = π⁵), and
  every class with exponent 5.
- Those twists stay at or below the random level at every one of six scales: max r ≤ 1.014 over
  48–120 classes, mean 0.97–0.985, and r₃₂ ≈ 0.97.
- A lim inf claim cannot be strictly refuted by finite data. But the statement has no support on
  these classes, and data at every scale contradict it.
- The registered tests of statement 1 (RS-S006) covered only "+" twists with N(u) ≤ 100, so they
  did not include these classes.
- **Disposition: the universal form is withdrawn** and replaced by the class form of §5. This is
  an audit finding, recorded against CAND-001 without allocating an ID.

**O2: the sixth-power-free-norm repair of statement 3 alone.**

- The repaired law ε → N₆(u)^{−1/6} predicts a positive excess for every class.
- Classes with exponent 5 have a **negative** excess at every scale (mean ε·N₆^{1/6} < 0; see the
  k = 5 column).
- The repair is right for exponents 1, 2 and 3, uncertain for 4, and wrong in sign for 5.

## 5. Provisional statement (PROV-RS14). Not a CAND; not frozen.

**Definitions.**

- Let κ = (e_π) be a finitely supported exponent vector mod 6 on primary primes coprime to 3, with
  units dropped.
- w_κ = conj(g̃₆)·Π_π (π/·)₆^{e_π}.
- ε_κ = (r_κ² − 1)/(r₁² − 1).
- N₆(κ) = Π N(π)^{e_π}, with e_π ∈ {1, …, 5}.

**Statements.**

- **(A)** If every e_π ∈ {1, 2, 3}, then ε_κ·N₆(κ)^{1/6} → 1. Observed 0.94–0.95 at
  X = 6.4·10⁵ and 10⁶, rising from about 0.89.
- **(B)** If κ = π⁵ with N(π) large, then ε_κ < 0 and ε_κ·N(π)^{5/6} → −1. Observed −1.02 to
  −1.11 for N(π) ≥ 19. Small-prime behaviour (N = 4, 7, 13) is open.
- **(C)** For κ = π⁴, ε_κ·N(π)^{4/6} is positive. Whether it tends to 1 or to a constant below 1
  is open (0.53 → 0.83).
- **(D) Class dichotomy.** Classes with every exponent in {1, 2, 3, 4} are enhanced
  (lim inf r > 1). Classes containing an exponent 5 are not (lim sup r ≤ 1). Mixed patterns such as
  (1,5), (2,5), (3,5) and (4,4) are **untested**.

**Theory analogy, not a derivation.** Patterson's cubic coefficients vanish at τ₃(π²), which is
exponent n − 1 = 2 for n = 3. They also carry the cube periodicity τ(cd³) ∝ |d|τ(c). Statement (B)
is the sextic counterpart at exponent n − 1 = 5. The negative sign there, rather than a zero, is
unexplained. Bröker–Hoffstein study τ₆ at π, π² and π⁴, so k = 2 and k = 4 are where published
coefficient data could be compared.

**Statement 2 of CAND-001** (prime-level unit-class bias) concerns u-independent unit classes. It
is unaffected by this audit.

## 6. Falsification plan, for the next session to register before data

**Design.** Build w_κ directly as products of prime symbol vectors. No large u is needed, so every
class is accessible.

- **Scale:** X = 10⁶ (D = 78462). Exponents 4, 5 and mixed classes are fresh there.
- **Single-prime classes:** π^k for k = 1, …, 5 over the 20 smallest primary primes (N ≤ about
  100), giving 100 classes.
- **Pair classes:** (e₁, e₂) ∈ {1, …, 5}² over the 6 smallest prime pairs, giving 150 classes.
- **Controls:** 10 random-phase vectors and 10 conj(g̃₆)·(random sixth roots).
- **Cost:** forward products only. The cost is measured, not projected: the RS-S012 run at this X
  took 950 s for about 85 products plus the build. This plan needs about 270 products, so it should
  be split into two jobs of 45 minutes or less.

**Power.** At D = 78462, random-vector r has spread about 0.003 (max 1.0054 over 20 at
D = 52008), so σ_ε ≈ 2σ_r/(r₁² − 1) ≈ 0.006. Signals:

- (A): ε ≥ N₆^{−1/6} ≥ 0.21 for N₆ ≤ 10⁴, which is ≥ 30σ.
- (B): |ε| ≈ N^{−5/6} = 0.086 to 0.021 for N = 19 to 100, which is 3.5σ to 14σ.
- Per-class (B) tests are therefore restricted to N ≤ 61, which is ≥ 6σ. Larger N enter only
  through group means.

**Draft criteria (to be registered verbatim before running):**

- **P1 (A):** over single-prime k ∈ {1, 2, 3} and pair classes with exponents in {1, 2, 3},
  mean ε·N₆^{1/6} ∈ [0.90, 1.00] and sd ≤ 0.05.
- **P2 (B):** every single-prime k = 5 class with 19 ≤ N(π) ≤ 61 has r < 1, and over N ≥ 19 the
  mean ε·N^{5/6} ∈ [−1.30, −0.80].
- **P3 (D):** every class containing an exponent 5, including (1,5), (2,5), (3,5) and (4,5), has
  r < 1.02. Every class with exponents in {1, 2, 3} has r > 1.05.
- **P4 (C), exploratory:** report ε·N₆^{1/6} for k = 4 and for pairs containing 4.

A failure of P1 or P3 refutes PROV-RS14 as stated. Only after P1–P3 pass would a replacement
candidate (CAND-002) be justified.
