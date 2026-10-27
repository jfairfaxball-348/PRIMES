import ReciprocitySpectra.Model

/-!
# CAND-002: formal **statements**, no proofs

The definitions below state the frozen experimental claims as Lean propositions.
None is an axiom or a theorem. All finite statistics refer to `Model.lean`.

Interpretive choices made explicit:
* X is a natural cutoff, tending to infinity along all sufficiently large X.
* Classes are finite maps of primary split or inert prime atoms to ZMod 6.
* The crossover family excludes exponent 5 and bounds the support cardinality.
* Uniformity holds simultaneously over classes in every compact [a,b] ⊂ (0,∞).
* r₁² - 1 is eventually bounded below by a positive real constant.
* H_P is an ABSTRACT prime-first-moment asymptotic with a coefficient c(u);
  it is not an identification with a Kubota coefficient or τ₆.
* Statement (3) is a standalone fixed-class conjecture (owner decision
  2026-10-27), not a consequence of (1) and (2): (1) is compact-aspect and
  (2) is large-aspect, and neither reaches the fixed-class limit.
-/

namespace ReciprocitySpectra

/-- Eventual nonvanishing of the normalization denominator, with a positive
gap, prevents a silent use of 0/0 in the finite statistics. -/
noncomputable def normalizationGap : Prop :=
  ∃ η : ℝ, 0 < η ∧ ∃ X₀ : ℕ,
    ∀ X : ℕ, X₀ ≤ X → η ≤ strength X unitClass ^ 2 - 1

/-- The positive small-t behaviour required of the universal profile. -/
def profileAtZero (F : ℝ → ℝ) : Prop :=
  ∃ η δ : ℝ, 0 < η ∧ 0 < δ ∧
    ∀ t : ℝ, 0 < t → t < δ → η ≤ F t

/-- Monotonicity on the frozen interval 10⁻² ≤ t ≤ 1. -/
def profileDecreasing (F : ℝ → ℝ) : Prop :=
  ∀ s t : ℝ, (1 : ℝ) / 100 ≤ s → s ≤ t → t ≤ 1 → F t ≤ F s

/-- Limsup at +∞ is at most zero, written in ε–T form. -/
def profileAtInfinity (F : ℝ → ℝ) : Prop :=
  ∀ ε : ℝ, 0 < ε → ∃ T : ℝ, 0 < T ∧
    ∀ t : ℝ, T ≤ t → F t ≤ ε

/-- Compact-uniform crossover, with a uniform finite bound on the number of
prime factors. The compact set is represented by arbitrary 0 < a ≤ b. -/
noncomputable def uniformCrossover (F : ℝ → ℝ) : Prop :=
  ∀ B : ℕ, ∀ a b : ℝ, 0 < a → a ≤ b →
    ∀ ε : ℝ, 0 < ε → ∃ X₀ : ℕ,
      ∀ X : ℕ, X₀ ≤ X →
        ∀ κ : TwistClass, admissibleSmallClass B κ →
          a ≤ aspect X κ → aspect X κ ≤ b →
            |scaledExcess X κ - F (aspect X κ)| < ε

/-- CAND-002 (1), including the explicit denominator-gap assumption. -/
noncomputable def CAND002_Crossover : Prop :=
  normalizationGap ∧ ∃ F : ℝ → ℝ,
    uniformCrossover F ∧ profileAtZero F ∧
      profileDecreasing F ∧ profileAtInfinity F

/-- CAND-002 (2), exactly in its variable-prime, large-t regime. The phrase
"X large" is interpreted as an additional threshold X₀. -/
noncomputable def CAND002_Fifth : Prop :=
  ∀ δ : ℝ, 0 < δ →
    ∃ N₀ X₀ : ℕ, ∃ T : ℝ, 0 < T ∧
      ∀ X : ℕ, X₀ ≤ X →
        ∀ π : Eis, admissibleAtom π →
          N₀ ≤ (eisNorm π).toNat →
            T ≤ aspect X (fifthClass π) →
              |scaledExcess X (fifthClass π) + 1| < δ

/-- The first moment of Gauss sums shifted by the *residue* of u, rather than
by its coordinate a or by its norm. This is a finite expression, not a
Kubota-series coefficient. -/
noncomputable def shiftedGauss (u σ : Eis) : ℂ :=
  ∑ t ∈ Finset.range (eisNorm σ).toNat,
    complexSymbol ⟨(t : ℤ), 0⟩ σ *
      Complex.exp (2 * (Real.pi : ℂ) * Complex.I *
        (((res (residueRoot σ) u).val : ℕ) : ℂ) * (t : ℂ) /
        ((eisNorm σ).toNat : ℂ))

/-- Raw (unnormalised) prime first moment: each summand has modulus √(N σ). -/
noncomputable def shiftedFirstMoment (X : ℕ) (u : Eis) : ℂ :=
  ∑ σ ∈ primarySplitPrimes X, shiftedGauss u σ

/-- Normalised prime first moment Σ g_σ(u)/√(N σ), the quantity in the matrix
orientation identity (each summand has modulus at most 1). -/
noncomputable def normalizedShiftedFirstMoment (X : ℕ) (u : Eis) : ℂ :=
  ∑ σ ∈ primarySplitPrimes X,
    shiftedGauss u σ / (Real.sqrt ((eisNorm σ).toNat : ℝ) : ℂ)

/-- The deliberately abstract sextic Patterson-type hypothesis, uniform in
all positive-norm shifts with N(u) ≤ B X. It asserts the existence of c(u)
without identifying c(u) with τ₆ or any known theta coefficient.

Scale (corrected 2026-10-27): the Patterson-type main term X^(1/2 + 1/n)/log X
(n = 3: X^(5/6); n = 4: X^(3/4); n = 6: X^(2/3)) is for **normalised** Gauss
sums, so the hypothesis is stated for `normalizedShiftedFirstMoment`. The
earlier version applied X^(2/3)/log X to the raw sums, whose expected size is
X^(7/6)/log X; it was therefore expected to be false for the actual Gauss sums,
which made `CAND002_Conditional` vacuous. See RS_HP_SCALE_ERRATUM.md. -/
noncomputable def AbstractPrimeMomentHP : Prop :=
  ∃ c : Eis → ℂ,
    ∀ B : ℝ, 0 < B →
      ∀ ε : ℝ, 0 < ε → ∃ X₀ : ℕ,
        ∀ X : ℕ, X₀ ≤ X → 2 ≤ X →
          ∀ u : Eis, 0 < eisNorm u →
            (eisNorm u : ℝ) ≤ B * (X : ℝ) →
              ‖normalizedShiftedFirstMoment X u -
                c u * ((((X : ℝ) ^ ((2 : ℝ) / 3)) / Real.log X : ℝ) : ℂ)‖ ≤
                ε * (((X : ℝ) ^ ((2 : ℝ) / 3)) / Real.log X)

/-- Admissible fixed twist classes without exponent five (including 1). -/
def admissibleFixedClass (κ : TwistClass) : Prop :=
  ∀ a ∈ κ.support, admissibleAtom a ∧
    (κ a).val ≠ 5

/-- Fixed-class r eventually exceeds 1 by a positive gap. -/
noncomputable def fixedClassEnhanced (κ : TwistClass) : Prop :=
  ∃ δ : ℝ, 0 < δ ∧ ∃ X₀ : ℕ,
    ∀ X : ℕ, X₀ ≤ X → 1 + δ ≤ strength X κ

/-- For a *fixed* prime π, limsup_X r_{π⁵}(X) ≤ 1. -/
noncomputable def fixedFifthNotEnhanced (π : Eis) : Prop :=
  ∀ ε : ℝ, 0 < ε → ∃ X₀ : ℕ,
    ∀ X : ℕ, X₀ ≤ X → strength X (fifthClass π) ≤ 1 + ε

/-- CAND-002 (3), restated (owner decision 2026-10-27) as a **standalone**
fixed-class conjecture with no analytic hypothesis: every fixed admissible class
without exponent five is eventually enhanced, and every fixed fifth class is not.
It is not derived from (1) and (2), which do not reach the fixed-class boundary
(`RS_CAND002_LOGICAL_BRIDGE_AUDIT.md`). -/
noncomputable def CAND002_FixedClass : Prop :=
  (∀ κ : TwistClass, admissibleFixedClass κ → fixedClassEnhanced κ) ∧
    (∀ π : Eis, admissibleAtom π → fixedFifthNotEnhanced π)

/-- Historical H_P-conditional form of (3), retained for the record only and NOT
part of the CAND-002 package: H_P (even at the corrected normalised scale) is too
weak at row scale to bear on it (`RS_HP_SCALE_ERRATUM.md` §3). -/
noncomputable def CAND002_Conditional : Prop :=
  AbstractPrimeMomentHP →
    ((∀ κ : TwistClass, admissibleFixedClass κ → fixedClassEnhanced κ) ∧
      (∀ π : Eis, admissibleAtom π → fixedFifthNotEnhanced π))

/-- The complete formal-conjecture package: (1), (2) and standalone (3).
No proof of this Prop is claimed. -/
noncomputable def CAND002 : Prop :=
  CAND002_Crossover ∧ CAND002_Fifth ∧ CAND002_FixedClass

end ReciprocitySpectra
