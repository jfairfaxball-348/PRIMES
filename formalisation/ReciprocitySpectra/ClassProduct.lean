import ReciprocitySpectra.RowSum
import ReciprocitySpectra.ShiftConvention

/-!
# RS-S033: an actual Eisenstein numerator for finite sextic twist classes

The element below lives in the same coordinate-pair Eisenstein model as the
frozen conjecture, and is independent of the denominator prime. We prove that
its reduction equals the already-verified finite class residue, including
vanishing factors and every exponent in ZMod 6.
-/

namespace ReciprocitySpectra

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

variable {p : ℕ}

/-- Reduction preserves the actual Eisenstein identity. -/
@[simp] theorem res_one (r : ZMod p) : res r (1 : Eis) = 1 := by
  change (1 : ZMod p) + 0 * r = 1
  simp

/-- Reduction commutes with arbitrary natural powers, including the zeroth
power, so it also handles all six exponent classes. -/
theorem res_pow_eis (r : ZMod p) (hr : r ^ 2 + r + 1 = 0)
    (a : Eis) (n : ℕ) : res r (a ^ n) = (res r a) ^ n := by
  induction n with
  | zero => simp
  | succ n ih =>
      rw [pow_succ, res_mul hr, ih, pow_succ]

/-- Reduction of a finite product, with no assumption that factors are units. -/
theorem res_prod_eis (r : ZMod p) (hr : r ^ 2 + r + 1 = 0)
    (s : Finset Eis) (f : Eis → Eis) :
    res r (∏ a ∈ s, f a) = ∏ a ∈ s, res r (f a) := by
  classical
  induction s using Finset.induction_on with
  | empty => simp
  | @insert a s ha ih =>
      simp only [Finset.prod_insert ha]
      rw [res_mul hr, ih]

/-- Column-independent Eisenstein representative of a frozen twist class. -/
noncomputable def classNumerator (κ : TwistClass) : Eis :=
  ∏ a ∈ κ.support, a ^ (κ a).val

/-- Actual reduction of the numerator equals the pre-existing columnwise
classResidue; zero residues and exponents 0 through 5 are retained. -/
theorem classNumerator_reduction (κ : TwistClass) (σ : Eis)
    (hr : residueRoot σ ^ 2 + residueRoot σ + 1 = 0) :
    res (residueRoot σ) (classNumerator κ) = classResidue κ σ := by
  classical
  unfold classNumerator classResidue
  rw [res_prod_eis (residueRoot σ) hr]
  apply Finset.prod_congr rfl
  intro a ha
  exact res_pow_eis (residueRoot σ) hr a (κ a).val

/-- The reduced rowShift is the residue of one actual Eisenstein integer,
for every column at once, not a column-dependent representative. -/
theorem rowShift_eisenstein (κ : TwistClass) (ρ σ : Eis)
    (hr : residueRoot σ ^ 2 + residueRoot σ + 1 = 0) :
    rowShift κ ρ σ =
      res (residueRoot σ) (ρ * classNumerator κ) := by
  rw [res_mul hr, classNumerator_reduction κ σ hr]
  rfl

/-- Exact frozen-definition row identity for the genuine Eisenstein product.
There are no prime-level hypotheses beyond membership in the frozen index,
and no admitted asymptotic statement. -/
theorem residueMatVec_frozen_orientation (X : ℕ) (κ : TwistClass) (ρ : Eis) :
    residueMatVec X κ ρ =
      ∑ σ ∈ primarySplitPrimes X,
        star (shiftedGauss (ρ * classNumerator κ) σ /
          (Real.sqrt ((eisNorm σ).toNat : ℝ) : ℂ)) := by
  rw [residueMatVec_orientation]
  apply Finset.sum_congr rfl
  intro σ hσ
  letI : Fact (eisNorm σ).toNat.Prime :=
    ⟨primarySplitPrimes_prime hσ⟩
  letI : NeZero (eisNorm σ).toNat :=
    ⟨(primarySplitPrimes_prime hσ).ne_zero⟩
  have hr := (primarySplitPrimes_model hσ).2.1
  rw [shiftedGauss_frozen_eq_direct]
  rw [← rowShift_eisenstein κ ρ σ hr]

end ReciprocitySpectra
