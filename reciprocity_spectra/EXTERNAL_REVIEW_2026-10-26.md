# External review (anonymous), received 2026-10-26

**Context.** After RS-S018, the owner asked an external expert for an opinion. The request covered:

- the twist-class setup;
- the crossover law, the π⁵ deficit and the unit-class rule;
- the τ₆(π²) contrast check.

**Anonymity.** The reviewer asked to remain anonymous, and not to be cited or named as a referee at
this stage. **Do not name the reviewer in any record, draft or preprint.** Their content is
paraphrased below. Under PROTOCOL §9.3 it is evidence to evaluate, not authority.

## 1. Summary of the reviewer's points (paraphrased)

**Structural interpretation.** Each coordinate of R₆w_κ is a first moment of shifted sextic Gauss
sums over prime moduli, with shift u = ρκ, and N(ρ) can be as large as X.

- The untwisted vector already sits near the transition range of the approximate functional
  equation of the Kubota series ψ₆(u, s). This could explain the slow growth of r₁.
- Twisting moves the effective shift to N(ρ)·N(κ). Averaging a common crossover F(N(ρ)N(κ)/X) over
  the row primes would give a profile in t = N(κ)/X, with local weights at the primes dividing κ.
- The reviewer reads the observed control by N₆(κ), the norm of the shift, rather than by
  N(rad κ), the conductor scale, as suggestive of this mechanism.
- Rigour would need uniform shift-aspect estimates.

**Q1: is the crossover known?**

- The reviewer knows of no result giving this profile.
- The mechanism (the functional equation of ψ_n(u, s) with a varying shift) is familiar. The
  uniformity is not standard when N(u) is comparable to or larger than the modulus range, and the
  moduli are restricted to primes.
- The limiting claim "every fixed class is enhanced" presupposes a sextic Patterson-type
  prime-modulus asymptotic, which is unproved even for n = 3 without GRH. It must therefore be
  stated conjecturally.
- Keep the evidence for a common profile separate from any claimed limiting law.

**Q2: why does τ₆(π²) = 0 not show?**

- The statistic is a squared norm, Σ_ρ |c(ρκ)|². Here c is a prime-modulus first-moment
  coefficient, not τ₆ itself.
- Prime sieving (Möbius or Vaughan) changes the local factors. Twisted multiplicativity makes the
  π²-contribution depend on (ρ/π)₆, so averaging over ρ can hide a vanishing condition that is
  visible at m = 1.
- **Suggested test:** split the row primes by (ρ/π)₆ for exponent-2 classes, and look for
  concentration that correlates with (π/π̄)₆.

**Q3: the exponent-5 deficit.**

- Exponent n − 1 = 5 is where the local theta coefficient vanishes. Removing the principal local
  term could leave an opposite-sign contribution created by the prime sieve, of local size about
  N(π)^{−5/6}, with a coefficient near −1.
- Factors like (1 ± N(π)^{−1})^{±1} could explain why the small primes (π above 2) differ.
- This is a proposed mechanism, not a derivation.
- **Suggested tests:**
  - (a) does the normalized coefficient tend to −1 as N(π) grows?
  - (b) **prime versus unrestricted moduli:** repeat with all admissible moduli. A sieve effect
    should disappear or change substantially. The reviewer finds this the most compelling test.

**Q4: unit classes.**

- Reconcile the normalizations first. A Gauss sum built with e(t/p) differs from the
  trace-normalized one by a sextic factor (c_ρ/ρ)₆, where c_ρ = 2a − b or −b. That factor involves
  (−1/ρ)₆, (−3/ρ)₆ (which is sensitive to b mod 9), and a residual (b′/ρ)₆, where b = 3b′.
- The residual is not a fixed character, so a change of normalization need not permute j.
- Compute this factor exactly before interpreting the selection rule.

**Q5: consistency checks.** The reviewer listed four:

- (a) matrix orientation and reciprocity;
- (b) fit an explicit 1/log X correction, since the 0.85 → 0.94 plateau drift may be logarithmic
  rather than two regimes;
- (c) exclude the twisting prime from the σ-sum;
- (d) the choice of primary generator and unit ambiguity, especially at exponent 5.

**Direction.**

- Formulate the profile as a ρ-averaged shift-aspect crossover for sextic Gauss-sum first moments.
- Identify the local weights, and how prime restriction modifies the theta coefficients.
- Use exponent 5 to isolate a hidden local contribution.
- The reviewer would not yet claim a universal limiting law, but judges the phenomenon worth
  pursuing.
- Suggested presentation: (1) the ρ-averaged crossover identification; (2) the prime-versus-all-
  moduli comparison at exponent 5.
- Separate exactly verifiable identities from conjectural asymptotics.
- The reviewer asked whether any identities are formalized in Lean or recorded in "the Palomar
  register". The reviewer offered to read a draft with precise definitions, tables and the
  prime-versus-all-moduli comparison.

## 2. Programme response (RS-side assessment)

**Point 5a (orientation): checked.**

- Our engine computes (R₆w)_ρ = Σ_σ (ρ/σ)₆·w(σ): `native/residue_engine.c` stores
  E[i][j] = (π_i/π_j)₆, and `rs_apply` computes y_i = Σ_j ζ^{E[i][j]}·x_j.
- Hence (R₆w_κ)_ρ = Σ_σ conj(g̃₆(σ))·(ρκ/σ)₆ exactly. This is the shifted first moment with
  u = ρκ, and no reciprocity factor is involved.

**Point 5c (exclusion of the twisting prime): satisfied by construction.**

- w_κ(σ) = 0 when σ divides κ (`phase1k`/`phase1m`: rows with a None exponent are zeroed).
- The diagonal of R₆ is zero.

**Point 5d (primary generators).**

- Classes use primary generators (a ≡ 2 mod 3, b ≡ 0 mod 3; inert q as (q, 0)).
- (u⁵/ρ)₆ = conj((u/ρ)₆) is exact and tested.
- Unit twists by −1 leave r unchanged exactly (RS-S006).
- The reviewer's concern about unit ambiguity at exponent 5 is therefore addressed for ±primary
  generators. Non-±1 unit choices were not used.

**Exponent bookkeeping (our correction).** `RS_S018_COLLISION_AUDIT.md` §2 wrongly wrote the
general-n heuristic exponent as 1/2 + 1/(2n). The listed values follow 1/2 + 1/n, giving X^{2/3}
for n = 6. The reviewer's "X^{5/6} type" is read as a reference to the cubic analogue.

**Open (to be done).**

- Q2: the ρ-partition test.
- Q3a: the trend of the π⁵ coefficient.
- Q3b: prime versus unrestricted moduli. This needs a new engine variant, with rows the primes and
  columns all admissible c ≤ X with g̃₆(c).
- Q4: the exact normalization factor.
- Q5b: a 1/log X fit.

**Lean and Palomar.** The programme has **no** Lean formalizations yet. "Palomar" is the Palomar
registry of Lean-verified mathematics (https://palomar-registry.org/), as the owner identified. By
owner decision, formalization and registration of the exact results is now a mandatory stage
before any release (PROTOCOL §10). The exact identities are checked by pure-Python tests in
`tests/test_reciprocity_spectra.py`.

**Results of the reviewer's tests (RS-S019, registered).**

- **Prime versus unrestricted moduli:** the π⁵ deficit is **INTRINSIC** (−1.08 prime against
  −1.22 over all squarefree moduli). The sieve explanation is not supported.
- **The crossover profile persists** with unrestricted moduli, consistent with the proposed
  ρ-averaged shift-aspect mechanism.
- **Q3a:** the π⁵ coefficient approaches −1 as N(π) grows (exploratory).
- **The 0.85 → 0.94 drift** does not fit a single 1/log X correction. It looks like continued
  t-dependence of F.
- **The unit-class selection** disappears with unrestricted moduli (exploratory).

**Effect on the candidate.** Freezing CAND-002 in the RS-S018 §5 form is **deferred**. The
reviewer's interpretation implies the statement should be reformulated:

- as a ρ-averaged shift-aspect crossover;
- with any limiting enhancement stated conditionally on a sextic Patterson-type prime-modulus
  asymptotic.

The decisive tests come first. This is a programme decision taken in response to the review. It
is not a refutation.
