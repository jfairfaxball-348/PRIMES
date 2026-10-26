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
* Statement (3) is a conditional statement, not a proved logical implication
  from statements (1) and (2). In particular the large-t premise of (2)
  does not yield a fixed-prime X→∞ limit.
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

noncomputable def shiftedFirstMoment (X : ℕ) (u : Eis) : ℂ :=
  ∑ σ ∈ primarySplitPrimes X, shiftedGauss u σ

/-- The deliberately abstract sextic Patterson-type hypothesis, uniform in
all positive-norm shifts with N(u) ≤ B X. It asserts the existence of c(u)
without identifying c(u) with τ₆ or any known theta coefficient. -/
noncomputable def AbstractPrimeMomentHP : Prop :=
  ∃ c : Eis → ℂ,
    ∀ B : ℝ, 0 < B →
      ∀ ε : ℝ, 0 < ε → ∃ X₀ : ℕ,
        ∀ X : ℕ, X₀ ≤ X → 2 ≤ X →
          ∀ u : Eis, 0 < eisNorm u →
            (eisNorm u : ℝ) ≤ B * (X : ℝ) →
              ‖shiftedFirstMoment X u -
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

/-- CAND-002 (3): the separate conditional fixed-class corollary.
This is *not* a theorem derived from (1) and (2). -/
noncomputable def CAND002_Conditional : Prop :=
  AbstractPrimeMomentHP →
    ((∀ κ : TwistClass, admissibleFixedClass κ → fixedClassEnhanced κ) ∧
      (∀ π : Eis, admissibleAtom π → fixedFifthNotEnhanced π))

/-- The complete formal-conjecture package. No proof of this Prop is claimed. -/
noncomputable def CAND002 : Prop :=
  CAND002_Crossover ∧ CAND002_Fifth ∧ CAND002_Conditional

end ReciprocitySpectra
