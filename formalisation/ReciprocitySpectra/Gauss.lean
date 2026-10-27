module

public import ReciprocitySpectra.Sextic

@[expose] public section

/-!
# Gauss-sum identities: analytic part of E4 and E7

Theorems in this file are proved for any multiplicative character of a finite field.
The identification of the Euler-criterion sextic exponent with a particular
`MulChar (ZMod p) ℂ` is a separate, unproved bridge. In particular, a theorem
with a hypothesis `χ ≠ 1` is *not* an unconditional sextic-character theorem.

The primitive additive character required for the computational sextic Gauss
sum is the canonical additive character `t ↦ exp(2 π i t/p)`. Its identification
with a Mathlib `AddChar` is likewise an explicit remaining obligation.
-/

namespace ReciprocitySpectra

section GaussIdentities

variable {F : Type*} [Field F] [Fintype F]

/-- E7 (character-level): squared Gauss modulus, expressed as `g * conj g`,
for a nontrivial multiplicative character and a primitive additive character.
This is precisely the Mathlib product theorem and conjugation identity. -/
theorem gauss_modulus_sq (χ : MulChar F ℂ) (ψ : AddChar F ℂ)
    (hχ : χ ≠ 1) (hψ : ψ.IsPrimitive) :
    gaussSum χ ψ * star (gaussSum χ ψ) = (Fintype.card F : ℂ) := by
  rw [star_gaussSum_eq]
  exact gaussSum_mul_gaussSum_eq_card hχ hψ

/-- E4 (character-level): shifting the additive character by a unit multiplies
the Gauss sum by the inverse multiplicative character. -/
theorem gauss_shift (χ : MulChar F ℂ) (ψ : AddChar F ℂ) (a : Fˣ) :
    gaussSum χ (ψ.mulShift (a : F)) = χ⁻¹ (a : F) * gaussSum χ ψ :=
  gaussSum_mulShift_eq χ ψ a

/-- E4 (finite orientation): the sum of shifted Gauss sums equals the
corresponding matrix-weighted sum, with no convergence assumptions. -/
theorem finite_gauss_orientation {ι : Type*} (S : Finset ι)
    (χ : ι → MulChar F ℂ) (ψ : ι → AddChar F ℂ)
    (shift : ι → Fˣ) :
    (∑ j ∈ S, gaussSum (χ j) ((ψ j).mulShift (shift j : F))) =
      ∑ j ∈ S, (χ j)⁻¹ (shift j : F) * gaussSum (χ j) (ψ j) := by
  classical
  apply Finset.sum_congr rfl
  intro j hj
  exact gauss_shift (χ j) (ψ j) (shift j)

/-- The zero additive shift vanishes for a nontrivial multiplicative character.
This closes the zero-shift branch of the generic E4 identity without assuming
that the shift is a unit. -/
theorem gauss_zero_shift (χ : MulChar F ℂ) (ψ : AddChar F ℂ)
    (hχ : χ ≠ 1) :
    gaussSum χ (ψ.mulShift (0 : F)) = 0 := by
  simpa [gaussSum, AddChar.mulShift_apply] using
    (MulChar.sum_eq_zero_of_ne_one hχ)

/-- Shift a Gauss sum by any field element, including zero. This is an
unconditional finite-character identity *given* a nontrivial χ; the sextic
character and its nontriviality still need constructing. -/
theorem gauss_shift_all [DecidableEq F] (χ : MulChar F ℂ) (ψ : AddChar F ℂ)
    (hχ : χ ≠ 1) (a : F) :
    gaussSum χ (ψ.mulShift a) =
      if a = 0 then 0 else χ⁻¹ a * gaussSum χ ψ := by
  by_cases ha : a = 0
  · subst a
    simpa using gauss_zero_shift χ ψ hχ
  · simp only [if_neg ha]
    let u : Fˣ := Units.mk0 a ha
    have hu : (u : F) = a := rfl
    calc
      gaussSum χ (ψ.mulShift a) =
          gaussSum χ (ψ.mulShift (u : F)) := by rw [hu]
      _ = χ⁻¹ (u : F) * gaussSum χ ψ := gauss_shift χ ψ u
      _ = χ⁻¹ a * gaussSum χ ψ := by rw [hu]

end GaussIdentities

end ReciprocitySpectra
