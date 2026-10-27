# Erratum: the scale of the abstract hypothesis H_P (2026-10-27)

**Found in** the owner-requested review of RS-S024 to RS-S028. **Fixed in**
`formalisation/ReciprocitySpectra/Conjecture.lean` (`AbstractPrimeMomentHP`). Historical text in
RS-S026 and RS-S027 is preserved; this note records the impact.

## 1. The error

- The Patterson-type first moment over primes has main term X^{1/2+1/n}/log X for **normalised**
  Gauss sums g̃ = g/√p, with |g̃| = 1:
  - n = 3: X^{5/6} (Dunn–Radziwiłł, under GRH);
  - n = 4: X^{3/4} (DDHL conjecture);
  - n = 6: X^{2/3}.
- The **raw** sextic sums, with |g| = √p, are therefore expected to be about X^{7/6}/log X.
- The previous Lean `AbstractPrimeMomentHP` applied c(u)·X^{2/3}/log X to the **raw** first moment
  `shiftedFirstMoment`. For the actual Gauss sums that statement was expected to be false, so
  `CAND002_Conditional` (H_P → …) was vacuously true.
- **Origin:** the informal wording "prime first moment ~ c(u)·X^{2/3}/log X" (PROTOCOL §10.2b and the
  CAND-002 record) did not say "normalised". The formaliser read it as raw. The fault is in the
  informal statement, not the formalisation.

## 2. The fix

- `AbstractPrimeMomentHP` is now stated for `normalizedShiftedFirstMoment X u = Σ_{σ∈P_X}
  g_σ(u)/√Nσ` at scale X^{2/3}/log X. This is the quantity in the matrix orientation identity.
- The raw `shiftedFirstMoment` is kept as a definition.
- An equivalent raw-scale formulation would use X^{7/6}/log X.
- The Lean build succeeds, and faithfulness is unchanged at 1764/1764.

## 3. Impact on RS-S026

- **Propositions 1 and 2** (the row identity and the zero-diagonal Gram identity): exact and
  **unaffected**.
- **Proposition 3** (the fixed-shift Abel lemma, M_u(X) ~ 4c(u)X^{1/6}/log X) is correct for the
  old raw-scale hypothesis. That hypothesis was the wrong one.
  - Under the corrected H_P, the normalised asymptotic M_u(X) = c(u)X^{2/3}/log X + o(·) is the
    hypothesis itself, so no Abel step is needed.
  - Under a correct **raw** formulation, A_u(Y) ~ c′(u)Y^{7/6}/log Y, the same Abel argument gives
    M_u(X) ~ (7/4)c′(u)X^{2/3}/log X: endpoint 1, integral (1/2)·(3/2) = 3/4.
- **§3, "where H_P falls short of the row range".** The prefix obstruction concerned Abel
  summation of the raw hypothesis below N(ρκ)/B. It is moot for the corrected hypothesis, which
  applies directly at cutoff X to every row of a fixed class once B ≥ N(κ), because
  N(ρκ) ≤ N(κ)·X.
  - **A stronger obstruction replaces it.** By the exact Gram identity, Σ_ρ |(R w_κ)_ρ|² =
    D·D_κ·r_κ², so a typical row has modulus about √D ≍ (X/log X)^{1/2}. H_P's uniform error
    o(X^{2/3}/log X) is larger than an entire row.
  - Any family of rows with sup |M_u(X)| = o(X^{2/3}/log X) satisfies H_P with c ≡ 0. So H_P alone
    places **no constraint** on r_κ, and cannot imply CAND-002(3) without strictly finer input.
- **Conclusion:** RS-S026's disposition stands, with a stronger reason. CAND-002(3) is not derivable
  from H_P.

## 4. Impact on RS-S027

- **Proposition 1** (the reciprocity transform of the kernel), the primitive-conductor lemma, the
  fixed-pair Hecke consequence, the conductor-aspect remark and the signed contraction (7): exact
  or classical, and **unaffected**.
- **Proposition 2** (the upper-slice Abel lemma) is correct as a deduction from the old raw-scale
  hypothesis. Its specific rates are artefacts of that scale:
  - H_λ(X) ~ 4(1 − λ^{1/6})X^{1/6}/log X;
  - |c(u)| ≪ X^{5/6};
  - the comparison of (6) with X^{1/6}/log X.
- **Under the corrected hypothesis:**
  - M_u(λX, X) = c(u)(f(X) − f(λX)) + o(f(X)), with f = X^{2/3}/log X, uniformly for
    N(u) ≤ BλX;
  - the trivial normalised bound gives |c(u)| ≪ X^{1/3};
  - the prefix discussion in (6) becomes unnecessary.
- **§4, target (8)** (a row-averaged mean-square error ≪ D²(log X)^{−A} for an independently
  defined model B₆): **unaffected**. It is precisely the precision the §3 analysis shows is needed,
  per-row error well below √D. It remains the correct hard-route target.

## 5. Impact on RS-S028 and the logical-bridge audit

- **RS-S028:** exact identities (prime sieve, ideal Vaughan, trace-Gauss sign rule (9),
  residue-transfer counterexample) **unaffected**. Its remark that raw and normalised scales are
  not interchangeable is consistent with this erratum.
- **`RS_CAND002_LOGICAL_BRIDGE_AUDIT.md`:** the countermodel to (1) + (2) ⇒ (3) is **unaffected**;
  it does not use H_P. Its §4 obligation 1 (passage from raw to normalised) is discharged by the
  restatement. Obligation 2 is sharpened by §3 above.

## 6. Status

- CAND-002(1) and (2): unchanged.
- CAND-002(3): OPEN, with the logical bridge open. The corrected H_P is still too weak to bridge
  it. Any proof needs row-level precision of the kind in RS-S027 (8).
