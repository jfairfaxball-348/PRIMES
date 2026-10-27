module

public import ChallengePrefix

@[expose] public section

/-!
# Independent Palomar Challenge: frozen shifted sum and specialised identities

ChallengePrefix is a Mathlib-only source copy, not an import of the proof
library. The module boundary reproduces the original Model/Conjecture
boundary, preventing Lean from recycling rawGauss's generated numeral proof
constant inside the frozen shiftedGauss definition.
-/

namespace ReciprocitySpectra

/-- Frozen positive-sign exponential sum with unreduced shift product modulo the norm. -/
noncomputable def shiftedGauss (u σ : Eis) : ℂ :=
  ∑ t ∈ Finset.range (eisNorm σ).toNat,
    complexSymbol ⟨(t : ℤ), 0⟩ σ *
      Complex.exp (2 * (Real.pi : ℂ) * Complex.I *
        (((res (residueRoot σ) u).val : ℕ) : ℂ) * (t : ℂ) /
        ((eisNorm σ).toNat : ℂ))


namespace Eis

/-- Coordinatewise extensionality for the explicit Eisenstein pair. -/
theorem ext {x y : Eis} (hc : x.c = y.c) (hd : x.d = y.d) :
    x = y := by
  cases x
  cases y
  cases hc
  cases hd
  rfl

/-- Multiplicative identity in the concrete coordinate-pair model of Z[ω]. -/
instance : CommMonoid Eis where
  one := ⟨1, 0⟩
  mul := (· * ·)
  one_mul := by
    intro x
    apply Eis.ext
    · change (1 * x.c - 0 * x.d : ℤ) = x.c
      ring
    · change (1 * x.d + 0 * x.c - 0 * x.d : ℤ) = x.d
      ring
  mul_one := by
    intro x
    apply Eis.ext
    · change (x.c * 1 - x.d * 0 : ℤ) = x.c
      ring
    · change (x.c * 0 + x.d * 1 - x.d * 0 : ℤ) = x.d
      ring
  mul_assoc := by
    intro x y z
    apply Eis.ext
    · simp only [Eis.mul_c, Eis.mul_d]
      ring
    · simp only [Eis.mul_c, Eis.mul_d]
      ring
  mul_comm := by
    intro x y
    apply Eis.ext
    · simp only [Eis.mul_c]
      ring
    · simp only [Eis.mul_d]
      ring

end Eis


/-- One column-independent Eisenstein product of all class atoms with their exponents. -/
noncomputable def classNumerator (κ : TwistClass) : Eis :=
  ∏ a ∈ κ.support, a ^ (κ a).val


/-- Reduction of the finite twist product into the residue field of column σ. -/
noncomputable def classResidue (κ : TwistClass) (σ : Eis) :
    ZMod (eisNorm σ).toNat :=
  κ.support.prod (fun π => res (residueRoot σ) π ^ (κ π).val)


/-- Residue of row ρ times the reduced finite-class numerator. -/
noncomputable def rowShift (κ : TwistClass) (ρ σ : Eis) :
    ZMod (eisNorm σ).toNat :=
  res (residueRoot σ) ρ * classResidue κ σ


/-- Direct finite sextic Gauss sum using the reduced product a·t in the positive exponential. -/
noncomputable def directShiftedGauss (σ : Eis)
    (a : ZMod (eisNorm σ).toNat) : ℂ :=
  ∑ t ∈ Finset.range (eisNorm σ).toNat,
    complexSymbol ⟨(t : ℤ), 0⟩ σ *
      Complex.exp (2 * (Real.pi : ℂ) * Complex.I *
        ((a * (t : ZMod (eisNorm σ).toNat)).val : ℂ) /
        ((eisNorm σ).toNat : ℂ))


/-- Complex sixth root raised to the chosen nonzero residue exponent; zero at zero. -/
noncomputable def sexticValue (r x : ZMod p) : ℂ :=
  (sexticExp r x).elim 0 (fun k => complexZeta6 ^ k.val)


/-- Canonical positive-sign additive character of the finite prime residue field. -/
noncomputable def rationalAddChar (p : ℕ) [NeZero p] : AddChar (ZMod p) ℂ :=
  AddChar.zmodChar p (Complex.isPrimitiveRoot_exp p (NeZero.out)).pow_eq_one


section Specialised
variable [Fact p.Prime]

/-- The original sextic multiplicative character, determined by sexticValue
    at every residue. The laws are proved in the Solution. -/
@[simp] theorem sexticValue_zero (r : ZMod p) : sexticValue r 0 = 0 := by
  simp [sexticValue, sexticExp]

theorem sexticValue_one {r : ZMod p}
    (hr : r ^ 2 + r + 1 = 0) (h2 : (2 : ZMod p) ≠ 0)
    (h3 : (3 : ZMod p) ≠ 0) :
    sexticValue r 1 = 1 := by sorry

theorem sexticValue_mul {r : ZMod p}
    (hr : r ^ 2 + r + 1 = 0) (h2 : (2 : ZMod p) ≠ 0)
    (h3 : (3 : ZMod p) ≠ 0) (h6 : 6 ∣ p - 1)
    (x y : ZMod p) :
    sexticValue r (x * y) = sexticValue r x * sexticValue r y := by sorry

noncomputable def sexticCharacter (r : ZMod p)
    (hr : r ^ 2 + r + 1 = 0) (h2 : (2 : ZMod p) ≠ 0)
    (h3 : (3 : ZMod p) ≠ 0) (h6 : 6 ∣ p - 1) :
    MulChar (ZMod p) ℂ where
  toFun := sexticValue r
  map_one' := sexticValue_one hr h2 h3
  map_mul' := sexticValue_mul hr h2 h3 h6
  map_nonunit' := by
    intro x hnot
    have hx : x = 0 := by
      by_contra h
      exact hnot (isUnit_iff_ne_zero.mpr h)
    simp [hx]

/-- Exact library theorem; all original hypotheses and quantifiers retained. -/
theorem sexticCharacter_apply (r : ZMod p)
    (hr : r ^ 2 + r + 1 = 0) (h2 : (2 : ZMod p) ≠ 0)
    (h3 : (3 : ZMod p) ≠ 0) (h6 : 6 ∣ p - 1)
    (x : ZMod p) :
    sexticCharacter r hr h2 h3 h6 x = sexticValue r x := by sorry


/-- Exact library theorem; all original hypotheses and quantifiers retained. -/
theorem sexticCharacter_ne_one (r : ZMod p)
    (hr : r ^ 2 + r + 1 = 0) (h2 : (2 : ZMod p) ≠ 0)
    (h3 : (3 : ZMod p) ≠ 0) (h6 : 6 ∣ p - 1) :
    sexticCharacter r hr h2 h3 h6 ≠ 1 := by sorry


/-- Exact library theorem; all original hypotheses and quantifiers retained. -/
theorem gaussSum_sextic_eq_raw (σ : Eis)
    [Fact (eisNorm σ).toNat.Prime]
    (hr : residueRoot σ ^ 2 + residueRoot σ + 1 = 0)
    (h2 : (2 : ZMod (eisNorm σ).toNat) ≠ 0)
    (h3 : (3 : ZMod (eisNorm σ).toNat) ≠ 0)
    (h6 : 6 ∣ (eisNorm σ).toNat - 1) :
    gaussSum (sexticCharacter (residueRoot σ) hr h2 h3 h6)
      (rationalAddChar (eisNorm σ).toNat) = rawGauss σ := by sorry


/-- Exact library theorem; all original hypotheses and quantifiers retained. -/
theorem rawGauss_modulus_sq (σ : Eis)
    [Fact (eisNorm σ).toNat.Prime]
    (hr : residueRoot σ ^ 2 + residueRoot σ + 1 = 0)
    (h2 : (2 : ZMod (eisNorm σ).toNat) ≠ 0)
    (h3 : (3 : ZMod (eisNorm σ).toNat) ≠ 0)
    (h6 : 6 ∣ (eisNorm σ).toNat - 1) :
    rawGauss σ * star (rawGauss σ) = ((eisNorm σ).toNat : ℂ) := by sorry


/-- Exact library theorem; all original hypotheses and quantifiers retained. -/
theorem shiftedGauss_eq_gaussSum (σ : Eis)
    [Fact (eisNorm σ).toNat.Prime]
    (hr : residueRoot σ ^ 2 + residueRoot σ + 1 = 0)
    (h2 : (2 : ZMod (eisNorm σ).toNat) ≠ 0)
    (h3 : (3 : ZMod (eisNorm σ).toNat) ≠ 0)
    (h6 : 6 ∣ (eisNorm σ).toNat - 1)
    (a : ZMod (eisNorm σ).toNat) :
    directShiftedGauss σ a =
      gaussSum (sexticCharacter (residueRoot σ) hr h2 h3 h6)
        ((rationalAddChar (eisNorm σ).toNat).mulShift a) := by sorry


/-- Exact library theorem; all original hypotheses and quantifiers retained. -/
theorem shiftedGauss_e4 (σ : Eis)
    [Fact (eisNorm σ).toNat.Prime]
    (hr : residueRoot σ ^ 2 + residueRoot σ + 1 = 0)
    (h2 : (2 : ZMod (eisNorm σ).toNat) ≠ 0)
    (h3 : (3 : ZMod (eisNorm σ).toNat) ≠ 0)
    (h6 : 6 ∣ (eisNorm σ).toNat - 1)
    (a : ZMod (eisNorm σ).toNat) :
    directShiftedGauss σ a =
      star (sexticCharacter (residueRoot σ) hr h2 h3 h6 a) *
        rawGauss σ := by sorry


/-- Exact library theorem; all original hypotheses and quantifiers retained. -/
theorem classNumerator_reduction (κ : TwistClass) (σ : Eis)
    (hr : residueRoot σ ^ 2 + residueRoot σ + 1 = 0) :
    res (residueRoot σ) (classNumerator κ) = classResidue κ σ := by sorry


/-- Exact library theorem; all original hypotheses and quantifiers retained. -/
theorem rowShift_eisenstein (κ : TwistClass) (ρ σ : Eis)
    (hr : residueRoot σ ^ 2 + residueRoot σ + 1 = 0) :
    rowShift κ ρ σ =
      res (residueRoot σ) (ρ * classNumerator κ) := by sorry


/-- Exact library theorem; all original hypotheses and quantifiers retained. -/
theorem residueMatVec_frozen_orientation (X : ℕ) (κ : TwistClass) (ρ : Eis) :
    residueMatVec X κ ρ =
      ∑ σ ∈ primarySplitPrimes X,
        star (shiftedGauss (ρ * classNumerator κ) σ /
          (Real.sqrt ((eisNorm σ).toNat : ℝ) : ℂ)) := by sorry


end Specialised

end ReciprocitySpectra
