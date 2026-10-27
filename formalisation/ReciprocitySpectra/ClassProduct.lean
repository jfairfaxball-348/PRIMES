import ReciprocitySpectra.RowSum
import ReciprocitySpectra.ShiftConvention

/-!
# RS-S032: a true Eisenstein representative of every finite twist class

The previous finite matrix identity uses `rowShift` in a model residue field.
Here we construct a finite Eisenstein product, prove its reduction for all
columns (including factors that vanish), and reconcile the full row identity
to the frozen Conjecture.shiftedGauss without changing its definition.
-/

namespace ReciprocitySpectra

/-- Multiplication of Eisenstein coordinate pairs is a commutative monoid.
This is the original multiplication from Sextic.lean, with a genuine identity. -/
instance : CommMonoid Eis where
  one := ⟨1, 0⟩
  mul := fun x y =>
    ⟨x.c * y.c - x.d * y.d,
     x.c * y.d + x.d * y.c - x.d * y.d⟩
  one_mul := by
    intro x
    rcases x with ⟨a, b⟩
    congr 1 <;> simp <;> ring
  mul_one := by
    intro x
    rcases x with ⟨a, b⟩
    congr 1 <;> simp <;> ring
  mul_assoc := by
    intro x y z
    rcases x with ⟨a, b⟩
    rcases y with ⟨c, d⟩
    rcases z with ⟨e, f⟩
    congr 1 <;> simp <;> ring
  mul_comm := by
    intro x y
    rcases x with ⟨a, b⟩
    rcases y with ⟨c, d⟩
    congr 1 <;> simp <;> ring

/-- A fixed sixth-power-free class has a genuine finite product in
Eisenstein coordinates; no arbitrary infinite product is assumed. -/
noncomputable def classEisRepresentative (κ : TwistClass) : Eis :=
  κ.support.prod (fun π => π ^ (κ π).val)

/-- Column-independent numerator whose reduction is the model's rowShift. -/
noncomputable def rowEisShift (κ : TwistClass) (ρ : Eis) : Eis :=
  ρ * classEisRepresentative κ

/-- The residue of the actual finite Eisenstein class product agrees with
the Finsupp classResidue, including zeros and all six-power exponents. -/
theorem classEisRepresentative_res (σ : Eis) (κ : TwistClass)
    (hr : residueRoot σ ^ 2 + residueRoot σ + 1 = 0) :
    res (residueRoot σ) (classEisRepresentative κ) = classResidue κ σ := by
  classical
  let r := residueRoot σ
  have hone : res r (1 : Eis) = 1 := by
    change (1 : ZMod (eisNorm σ).toNat) + 0 * r = 1
    ring
  have hpow (π : Eis) (n : ℕ) :
      res r (π ^ n) = res r π ^ n := by
    induction n with
    | zero => simpa only [pow_zero] using hone
    | succ n ih =>
      rw [pow_succ, res_mul hr, ih, pow_succ]
  have hprod (s : Finset Eis) :
      res r (s.prod (fun π => π ^ (κ π).val)) =
        s.prod (fun π => res r π ^ (κ π).val) := by
    induction s using Finset.induction_on with
    | empty => simpa only [Finset.prod_empty] using hone
    | @insert π s hs ih =>
      rw [Finset.prod_insert hs, Finset.prod_insert hs, res_mul hr,
          hpow π (κ π).val, ih]
  simpa only [classEisRepresentative, classResidue] using hprod κ.support

/-- An actual Eisenstein product, not merely a formal residue class,
produces precisely the shift used by the finite matrix. -/
theorem rowShift_eq_res_eis (σ ρ : Eis) (κ : TwistClass)
    (hr : residueRoot σ ^ 2 + residueRoot σ + 1 = 0) :
    rowShift κ ρ σ = res (residueRoot σ) (rowEisShift κ ρ) := by
  unfold rowShift rowEisShift
  rw [res_mul hr, classEisRepresentative_res σ κ hr]

/-- The actual finite residue matrix is the conjugate shifted Gauss-sum
row using a true Eisenstein shift. Every column's hypotheses follow from
index membership; the frozen Conjecture.shiftedGauss is unchanged. -/
theorem residueMatVec_frozen_shift (X : ℕ) (κ : TwistClass) (ρ : Eis) :
    residueMatVec X κ ρ =
      ∑ σ ∈ primarySplitPrimes X,
        star (shiftedGauss (rowEisShift κ ρ) σ /
          (Real.sqrt ((eisNorm σ).toNat : ℝ) : ℂ)) := by
  rw [residueMatVec_orientation]
  apply Finset.sum_congr rfl
  intro σ hσ
  obtain ⟨hb, hr, h2, h3, h6⟩ := primarySplitPrimes_model hσ
  haveI : NeZero (eisNorm σ).toNat :=
    ⟨(primarySplitPrimes_prime hσ).ne_zero⟩
  rw [rowShift_eq_res_eis σ ρ κ hr,
      ← shiftedGauss_frozen_eq_direct (rowEisShift κ ρ) σ]

end ReciprocitySpectra
