import ReciprocitySpectra.GaussBridge

/-!
# RS-S031: positive-sign shifted sextic Gauss sums

All shifts are residues in the explicitly modelled field ZMod (N σ).
The direct exponential is evaluated at the canonical representative of
the *product* a*t, so it has the same positive Fourier sign as the engine.
Zero shifts are included, and no Eisenstein quotient is asserted.
-/

namespace ReciprocitySpectra

/-- The direct positive-sign rational sextic Gauss sum with additive shift a.
    Unlike an abstract GaussSum, this displays the finite rational
    representatives and the exponential sign explicitly. -/
noncomputable def shiftedGauss (σ : Eis)
    (a : ZMod (eisNorm σ).toNat) : ℂ :=
  ∑ t ∈ Finset.range (eisNorm σ).toNat,
    complexSymbol ⟨(t : ℤ), 0⟩ σ *
      Complex.exp (2 * (Real.pi : ℂ) * Complex.I *
        ((a * (t : ZMod (eisNorm σ).toNat)).val : ℂ) /
        ((eisNorm σ).toNat : ℂ))

/-- An exact finite reindexing to Mathlib's shifted Gauss sum. -/
theorem shiftedGauss_eq_gaussSum (σ : Eis)
    [Fact (eisNorm σ).toNat.Prime]
    (hr : residueRoot σ ^ 2 + residueRoot σ + 1 = 0)
    (h2 : (2 : ZMod (eisNorm σ).toNat) ≠ 0)
    (h3 : (3 : ZMod (eisNorm σ).toNat) ≠ 0)
    (h6 : 6 ∣ (eisNorm σ).toNat - 1)
    (a : ZMod (eisNorm σ).toNat) :
    shiftedGauss σ a =
      gaussSum (sexticCharacter (residueRoot σ) hr h2 h3 h6)
        ((rationalAddChar (eisNorm σ).toNat).mulShift a) := by
  let p := (eisNorm σ).toNat
  haveI : NeZero p := ⟨(Fact.out : p.Prime).ne_zero⟩
  rw [gaussSum, zmod_sum_eq_range]
  unfold shiftedGauss
  apply Finset.sum_congr rfl
  intro t ht
  have hχ :
      sexticCharacter (residueRoot σ) hr h2 h3 h6
        (t : ZMod (eisNorm σ).toNat) =
        complexSymbol ⟨(t : ℤ), 0⟩ σ := by
    simpa only [Int.cast_natCast] using
      (sexticCharacter_rational σ hr h2 h3 h6 (t : ℤ))
  have hψ :
      rationalAddChar p (a * (t : ZMod p)) =
        Complex.exp (2 * (Real.pi : ℂ) * Complex.I *
          ((a * (t : ZMod p)).val : ℂ) / (p : ℂ)) := by
    simpa only [ZMod.natCast_zmod_val] using
      (rationalAddChar_nat p (a * (t : ZMod p)).val
        (ZMod.val_lt (a * (t : ZMod p))))
  simpa only [AddChar.mulShift_apply] using
    (congrArg₂ (· * ·) hχ hψ).symm

/-- Specialized sextic E4, including a = 0. The right side uses complex
    conjugation, not character inversion at zero. -/
theorem shiftedGauss_e4 (σ : Eis)
    [Fact (eisNorm σ).toNat.Prime]
    (hr : residueRoot σ ^ 2 + residueRoot σ + 1 = 0)
    (h2 : (2 : ZMod (eisNorm σ).toNat) ≠ 0)
    (h3 : (3 : ZMod (eisNorm σ).toNat) ≠ 0)
    (h6 : 6 ∣ (eisNorm σ).toNat - 1)
    (a : ZMod (eisNorm σ).toNat) :
    shiftedGauss σ a =
      star (sexticCharacter (residueRoot σ) hr h2 h3 h6 a) *
        rawGauss σ := by
  let p := (eisNorm σ).toNat
  haveI : NeZero p := ⟨(Fact.out : p.Prime).ne_zero⟩
  let χ := sexticCharacter (residueRoot σ) hr h2 h3 h6
  let ψ := rationalAddChar p
  calc
    shiftedGauss σ a = gaussSum χ (ψ.mulShift a) :=
      shiftedGauss_eq_gaussSum σ hr h2 h3 h6 a
    _ = (if a = 0 then 0 else χ⁻¹ a * gaussSum χ ψ) :=
      gauss_shift_all χ ψ
        (sexticCharacter_ne_one (residueRoot σ) hr h2 h3 h6) a
    _ = star (χ a) * rawGauss σ := by
      rw [gaussSum_sextic_eq_raw σ hr h2 h3 h6]
      by_cases ha : a = 0
      · subst a
        have hz : χ (0 : ZMod p) = 0 := by
          change sexticValue (residueRoot σ) 0 = 0
          exact sexticValue_zero (residueRoot σ)
        simp [hz]
      · simpa only [if_neg ha, MulChar.star_apply']

/-- The sextic character equals the exponent-based symbol at the reduction
    of every Eisenstein coordinate pair, including the zero residue. -/
theorem sexticCharacter_eis (σ α : Eis)
    [Fact (eisNorm σ).toNat.Prime]
    (hr : residueRoot σ ^ 2 + residueRoot σ + 1 = 0)
    (h2 : (2 : ZMod (eisNorm σ).toNat) ≠ 0)
    (h3 : (3 : ZMod (eisNorm σ).toNat) ≠ 0)
    (h6 : 6 ∣ (eisNorm σ).toNat - 1) :
    sexticCharacter (residueRoot σ) hr h2 h3 h6
      (res (residueRoot σ) α) = complexSymbol α σ := by
  rw [sexticCharacter_apply]
  rfl

end ReciprocitySpectra
