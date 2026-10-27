# RS-S026 — Prime-moment to fixed-class bridge: mathematics-first checkpoint

> **Erratum (2026-10-27).** The H_P used here applied the X^(2/3)/log X scale to raw Gauss sums. The correct scale is normalised X^(2/3)/log X (raw X^(7/6)/log X). See `RS_HP_SCALE_ERRATUM.md` for which statements are unaffected and which rates change.

**Date:** 2026-10-27. **Status:** exact finite identities and a fixed-shift Abelian lemma PROVED on paper; CAND-002(3) **NOT PROVED**. **Scope:** hard prime-level / matrix-level problem only. No new computation at a discovery scale, novelty audit, Lean edits or Palomar work.

## 0. Authority and distinctions

The frozen text of CAND-002 in `research/CONJECTURE_REGISTER.md` is unchanged. We use its rational-normalised sextic Gauss sums, primary degree-one split-prime matrix, twist classes and statistics. We also use the **distinct** abstract hypothesis `AbstractPrimeMomentHP` in `formalisation/ReciprocitySpectra/Conjecture.lean` (lines 84–96), as a stated, unproved hypothesis rather than as a theorem. The pre-existing `RS_CAND002_LOGICAL_BRIDGE_AUDIT.md` already proves the scalar nonimplication (1)+(2)+baseline => (3) *without* H_P. This session does **not** upgrade that countermodel into one satisfying H_P or into a sextic-matrix counterexample.

Let `P_X` be the primary split primes of norm at most X, `D=|P_X|`, and `χ_σ(u)=(u/σ)_6`. Write

```text
G_σ = g_σ(1) / sqrt(Nσ),
g_σ(u) = Σ_{a mod σ} χ_σ(a) exp(2πi res_σ(ua)/Nσ).
w_κ(σ) = conjugate(G_σ) χ_σ(κ).
U_κ(X) = {σ in P_X : χ_σ(κ) != 0},  D_κ = |U_κ(X)|.
```

For split prime σ, χ_σ is a nontrivial multiplicative character extended by zero at zero, and the additive character displayed above is primitive. The usual finite-field Gauss modulus identity gives `|G_σ|=1`; this is an elementary **paper** identity, **not** a new Lean specialization. Note that D_κ can be less than D even when κ is a fixed class. We only use statistics where D and D_κ are nonzero. For fixed κ and sufficiently large X, D_κ = D - O_κ(1), since the finite set of split prime divisors of κ is fixed.

## 1. Exact finite row identity (proved)

**Proposition 1.** For every row prime ρ, every admissible class κ and every X for which the sums are defined,

```text
(R_X w_κ)_ρ = conjugate( Σ_{σ in P_X} g_σ(ρκ) / sqrt(Nσ) ).
```

**Proof.** If σ does not divide `ρκ`, substitute `a ↦ (ρκ)^{-1} a` into the finite Gauss sum:
`g_σ(ρκ)=conjugate(χ_σ(ρκ)) g_σ(1)`. Complex conjugation and multiplicativity yield
`conjugate(g_σ(ρκ)/sqrt(Nσ))=χ_σ(ρ) χ_σ(κ) conjugate(G_σ)`, exactly the σ summand of `R_X w_κ`. If σ divides ρκ, then `g_σ(ρκ)=Σ_a χ_σ(a)=0` by nontriviality, and the right-hand matrix summand is also zero (including the σ=ρ diagonal). Summing proves the formula. QED.

This is the rational additive character and numerator-row/denominator-column convention of the frozen candidate, **not** the trace-normalised composite-modulus convention.

## 2. Exact signed two-point dispersion (proved)

Define `q_κ(σ)=conjugate(G_σ)χ_σ(κ)` and the prime-correlation kernel

```text
K_X(σ,τ) = Σ_{ρ in P_X} χ_σ(ρ) conjugate(χ_τ(ρ)).
O_κ(X) = Σ_{σ,τ in U_κ(X), σ!=τ}
             q_κ(σ) conjugate(q_κ(τ)) K_X(σ,τ).
```

Though individual summands are complex, `O_κ(X)` is real by conjugate-pair symmetry.

**Proposition 2.** With the exact finite definitions above,

```text
||R_X w_κ||² = D_κ (D-1) + O_κ(X),
r_κ(X)²       = 1 - 1/D + O_κ(X)/(D D_κ),
r_κ(X)² - 1   = [O_κ(X)/D_κ - 1]/D.                    (★)
```

**Proof.** Expand `||R_X w_κ||² = Σ_ρ |Σ_σ χ_σ(ρ)q_κ(σ)|²` and interchange finite sums. The off-diagonal sum is precisely O_κ. For every σ in U_κ, the σ=τ contribution is `|q_κ(σ)|² Σ_ρ |χ_σ(ρ)|²=1·(D−1)`: χ_σ vanishes exactly at the row ρ=σ among P_X. There are D_κ such σ. Divide by `D||w_κ||²=D D_κ`. QED.

As long as `r_1²−1 !=0`, write `O_1` for the untwisted off-diagonal and `n=N_6(κ)`. Equation (★) gives the **exact**, support-corrected identity

```text
ε_κ(X) = [O_κ(X)/D_κ − 1] / [O_1(X)/D − 1],
s_κ(X) = n^(1/6) · [O_κ(X)/D_κ − 1] / [O_1(X)/D − 1].
```

Thus both sides of the fixed-class dichotomy require **signed two-point prime correlations**. One-point asymptotics alone cannot simply be squared to discard cross terms or the diagonal. The constant `−1` in (★) is not an irrelevant finite-dimensional decoration: it comes from the zero diagonal and remains needed for exact identities. For the fifth class, non-enhancement requires control of the *positive* off-diagonal excess, not merely absence of a positive residue.

The identities were independently checked using arbitrary zero-diagonal unit-modulus complex matrices and every one-column deletion at D=3,5,8. These are synthetic algebra checks, **not** arithmetic evidence or proof of asymptotics. The proof above supplies the mathematical justification.

## 3. What the committed H_P really implies after normalisation

The Lean hypothesis has the form, uniformly for `0<N(u)≤B Y` with *each B fixed* and arbitrary positive ε,

```text
A_u(Y) := Σ_{Nσ≤Y} g_σ(u)
       = c(u) Y^(2/3)/log Y + E_u(Y),
|E_u(Y)| ≤ ε Y^(2/3)/log Y  for all Y sufficiently large,
```

where `c : Eis → ℂ` is existential and otherwise unconstrained. The hypothesis is for the **raw (unnormalised)** Gauss sums; matrix rows use `g_σ(u)/sqrt(Nσ)`.

**Proposition 3 (fixed-shift Abelian lemma).** For **each fixed nonzero shift u**, H_P implies

```text
M_u(X) := Σ_{Nσ≤X} g_σ(u)/sqrt(Nσ)
        = 4 c(u) X^(1/6)/log X + o_u(X^(1/6)/log X).   (†)
```

**Proof.** For fixed u, choose B=1 in H_P; `N(u)≤Y` eventually, giving the displayed asymptotic as `Y→∞`. Abel summation, valid for complex coefficients, says exactly

```text
M_u(X) = A_u(X)/sqrt(X)
       + (1/2) ∫_{Y0}^X A_u(y) y^(-3/2) dy + C_u,
```

for a fixed lower starting cutoff and fixed finite boundary correction C_u. Substitute the main term. Since
`∫^X y^(-5/6)/log y dy ~ 6 X^(1/6)/log X`, the endpoint contributes `c(u)` and the integral contributes `3c(u)` times `X^(1/6)/log X`: total `4c(u)`. For the error, given η>0 choose Y_η such that `|E_u(y)|≤η y^(2/3)/log y` for y≥Y_η. Split the integral at Y_η: the finite initial piece is O_u,η(1), and the tail is at most `3η(1+o(1))X^(1/6)/log X`. The endpoint error is at most `η X^(1/6)/log X`. Let η→0. QED.

**Important:** (†) is genuine mathematical progress for *fixed shifts* under the assumed H_P, but it **cannot** be substituted into Proposition 1 for the moving row shifts `u=ρκ` without a new uniform argument.

### Precisely where H_P falls short of the row range

Fix κ. Rows with Nρ comparable to X have `N(ρκ)≈Nκ·X`. For any fixed B chosen in H_P, its bound for a partial sum `A_{ρκ}(y)` is available only where `N(ρκ)≤By`. For those rows, this restricts Abel's integration variable to `y≥N(ρκ)/B≈(Nκ/B)X`: an interval starting at a *positive fraction of X*, not at a fixed lower bound. The omitted prefix of the *normalised* character sum can be as large as O(X) under trivial termwise bounds `|g_σ(u)/sqrt(Nσ)|≤1` (even O(X/log X) with a prime-counting bound); neither is o(`X^(1/6)/log X`). Quantification over every **fixed** B does not permit a diagonal selection `B=B(X)→∞` with a controlled threshold X₀(B,ε).

Consequently the uniform `o(Y^(2/3)/log Y)` error in raw H_P is **not** a demonstrated uniform asymptotic for matrix rows. And the fixed-u coefficient `c(u)` is complex and unconstrained: H_P asserts no nonvanishing, sign, size, correlation, or averaged-square estimate for `c(ρκ)` as ρ varies. There is no positivity theorem for `O_κ` in it as written. The missing step is substantive, not a Lean elaboration issue.

This shows a failed proposed *inference*. It is **not** a model-theoretic proof that CAND-002(1)+(2)+H_P cannot imply (3) for the particular arithmetic objects: no H_P-satisfying counterexample is constructed.

## 4. Separate the two fixed-class conclusions

### A. Fixed κ with no exponent five

By frozen (1), `F(t)` has a positive lower bound for sufficiently small *positive* t. But `t=n/X→0` for a fixed class and compact-aspect uniformity is only for `a≤t≤b` with a>0. Hence one **additional** boundary estimate sufficient for this fixed κ is

```text
s_κ(X) = F(n/X) + o_κ(1)   as X→∞.                   (A-boundary)
```

This is a separate hypothesis, **not proved** by (1) or H_P. If the baseline `r_1²−1≥η>0` eventually, the small-t profile `F≥a>0` gives eventually `s_κ≥a/2`. By definition,
`r_κ²≥1+η a/(2 n^(1/6))`; hence
`liminf r_κ≥sqrt(1+η a/(2n^(1/6)))>1`.
For the unit class the baseline alone suffices. The derivation proves this conditional implication, but supplies no arithmetic proof of (A-boundary).

### B. Fixed π, class π⁵

Frozen (2) instead takes `Nπ→∞` with `Nπ⁵/X` large. For fixed π that ratio tends to zero and Nπ may not even exceed N₀(δ). Thus (2) is silent at the required limit. A separate sufficient small-aspect condition is

```text
[(r_1(X)²−1) · (s_{π⁵}(X))_+] → 0,                 (B-small)
```

where `z_+=max(z,0)` and the normalization denominator is eventually positive. Indeed
`(r_{π⁵}²−1)_+ = [(r_1²−1)(s_{π⁵})_+]/Nπ^(5/6)→0`; since strengths are nonnegative, `limsup r_{π⁵}≤1`. A stronger possible arithmetic target is `s_{π⁵}(X)≤0` eventually. Merely assuming `(s_{π⁵})_+→0` is **not enough without** an upper bound on `r_1²−1`: the baseline gap is only a *lower* bound. Neither (B-small) nor eventual nonpositivity follows from (2) or H_P as written.

## 5. Separate proposed *prime-level* repair, NOT a result for the sextic matrices

Proposition 2 reduces the hard version to a precise analytic task that does not mention F or the normalised conjectural statistic.

**Two-point correlation hypothesis T2P(κ):** For every fixed admissible non-five class κ, there is an `a_κ>0` such that, as X→∞,

```text
O_κ(X) / (D D_κ) ≥ a_κ + o_κ(1);
```

for every fixed π with κ=π⁵,

```text
O_{π⁵}(X) / (D D_{π⁵}) ≤ o_π(1).
```

The little-o in inequalities means a real error tending to zero; no positive main term is assumed in the fifth case.

**Conditional theorem (proved by (★)).** T2P entails both fixed-class claims of CAND-002(3) unconditionally, without invoking raw H_P or (1),(2).

**Proof.** First clause: `r_κ²≥1−1/D+a_κ+o(1)`; for large X, `r_κ≥sqrt(1+a_κ/2)>1`. Fifth clause: `r_{π⁵}²≤1−1/D+o(1)`, so `limsup r_{π⁵}≤1`. QED.

**Epistemic warning.** T2P is **UNPROVED**; as a signed two-point bound, it largely **re-expresses the hard matrix-strength target**. It is not a free consequence of single shifted first moments, a literature theorem, or a meaningful simplification of the analytic difficulty. Its value is to identify the exact zero-diagonal correction and the signed prime-correlation object that any non-circular arithmetic proof must estimate. A genuinely non-circular advance would derive these inequalities from explicit reciprocity/character-sum transformations and arithmetic coefficient estimates. The old unrestricted operator-norm route cannot do this (PROOF_ROUTE §7).

## 6. Hard-route research dependencies and failure modes

1. **Moving-shift Abel transport.** Establish a *two-parameter* raw first-moment estimate with initial-segment information at all cutoffs `y≤X` for shifts `u=ρκ` (or bypass Abel via a directly weighted prime sum), including a quantitative error whose **row-averaged square** is small relative to `D²`. Fixed-B H_P alone does not provide this.
2. **Signed covariance/dispersion.** Control `K_X(σ,τ)` in the specific phases `q_κ(σ) conjugate(q_κ(τ))`; no arbitrary-coefficient norm bound can preserve the required sign. Derive local factors for exponents 1–4 versus π⁵, not by an unjustified positive squared-main-term ansatz.
3. **Row-varying coefficient arithmetic.** Identify `c(ρκ)` (or its correct normalised analogue) and prove nonvanishing and averaged-square bounds for non-five classes and suppression for π⁵. A claimed τ₆(π⁵)=0 at one modulus does not automatically give the signed *row average*.
4. **Endpoint control.** Obtain a genuine estimate down to `N₆(κ)/X→0` for fixed κ; frozen compact-`t` (1) and large-`t` (2) do not reach this boundary.
5. **Baseline.** Establish/retain `r_1²−1≥η>0` where using normalized profiles, and do not assume an upper bound on it without proof.
6. **Actual hard route first.** The generic large-sieve obstruction and missing sextic arithmetic coefficients are documented in PROOF_ROUTE §7. No new squarefree, GRH-conditional or function-field theorem is asserted here.

## 7. Validation and disposition

- Proofs are finite character manipulation, a diagonal/off-diagonal Gram expansion, Abel summation plus a regular-variation integral, and elementary inequalities. None invokes an unproved sextic asymptotic as if it were known.
- Independent complex-number sanity check: three matrix sizes D=3,5,8 with every one-column deletion; verifies the exact Gram and baseline correction to numerical tolerance. This checks *algebra only*, not the arithmetic, asymptotics or H_P.
- No project numerical scale run; no new prediction, holdout or result JSON. Historical evidence and frozen registration untouched.
- No Lean file, toolchain, CI, comparator, Palomar metadata or paper modified.
- **Outcome:** Prime-to-matrix finite identities and the coefficient **4** in the fixed-u normalized Abelian leading term are proved on paper. The joint moving-u uniformity, sign of off-diagonal energy, coefficient support, fifth suppression and both endpoint claims remain **OPEN**. CAND-002(3) remains conditional, not a derived theorem.
- **Next:** RS-S027 must attack the arithmetic of the *two-point* kernel and moving-shift weighted prime sums rather than resume Lean. See the single root `NEXT_SESSION_PROMPT.md`.
