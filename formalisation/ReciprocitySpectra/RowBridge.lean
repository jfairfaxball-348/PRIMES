import ReciprocitySpectra.ShiftedGauss

/-!
# RS-S031: finite class residues and exact row/column orientation

The class product is reduced separately modulo each column prime. It is a
modelling convention, not a theorem asserting an Eisenstein quotient equivalence.
The theorems retain the explicit split-prime hypotheses.
-/

namespace ReciprocitySpectra

/-- Reduce the finite twist-class product into the column residue field. -/
noncomputable def classResidue (κ : TwistClass) (σ : Eis) :
    ZMod (eisNorm σ).toNat :=
  κ.support.prod (fun π => res (residueRoot σ) π ^ (κ π).val)

/-- Multiplicativity identifies the class residue with the original
    complex symbol product, even when one factor reduces to zero. -/
theorem sexticCharacter_class (σ : Eis) (κ : TwistClass)
    [Fact (eisNorm σ).toNat.Prime]
    (hr : residueRoot σ ^ 2 + residueRoot σ + 1 = 0)
    (h2 : (2 : ZMod (eisNorm σ).toNat) ≠ 0)
    (h3 : (3 : ZMod (eisNorm σ).toNat) ≠ 0)
    (h6 : 6 ∣ (eisNorm σ).toNat - 1) :
    sexticCharacter (residueRoot σ) hr h2 h3 h6
      (classResidue κ σ) = classSymbol κ σ := by
  classical
  let χ := sexticCharacter (residueRoot σ) hr h2 h3 h6
  have hprod (s : Finset Eis) :
      χ (s.prod (fun π => res (residueRoot σ) π ^ (κ π).val)) =
        s.prod (fun π => complexSymbol π σ ^ (κ π).val) := by
    induction s using Finset.induction_on with
    | empty => simp
    | @insert π s hπ ih =>
      rw [Finset.prod_insert hπ, Finset.prod_insert hπ, map_mul, map_pow, ih]
      rw [show χ (res (residueRoot σ) π) = complexSymbol π σ from
        sexticCharacter_eis σ π hr h2 h3 h6]
  simpa only [classResidue, classSymbol] using hprod κ.support

/-- The row numerator reduced mod the current column, multiplied by the
    finite class product in the same residue field. -/
noncomputable def rowShift (κ : TwistClass) (ρ σ : Eis) :
    ZMod (eisNorm σ).toNat :=
  res (residueRoot σ) ρ * classResidue κ σ

theorem rowShift_symbol (σ ρ : Eis) (κ : TwistClass)
    [Fact (eisNorm σ).toNat.Prime]
    (hr : residueRoot σ ^ 2 + residueRoot σ + 1 = 0)
    (h2 : (2 : ZMod (eisNorm σ).toNat) ≠ 0)
    (h3 : (3 : ZMod (eisNorm σ).toNat) ≠ 0)
    (h6 : 6 ∣ (eisNorm σ).toNat - 1) :
    sexticCharacter (residueRoot σ) hr h2 h3 h6 (rowShift κ ρ σ) =
      complexSymbol ρ σ * classSymbol κ σ := by
  unfold rowShift
  rw [map_mul, sexticCharacter_eis σ ρ hr h2 h3 h6,
      sexticCharacter_class σ κ hr h2 h3 h6]

/-- Per-column matrix orientation: row numerator ρ, column denominator σ,
    including zero symbols and normalized conjugation. -/
theorem residueColumn_orientation (σ ρ : Eis) (κ : TwistClass)
    [Fact (eisNorm σ).toNat.Prime]
    (hr : residueRoot σ ^ 2 + residueRoot σ + 1 = 0)
    (h2 : (2 : ZMod (eisNorm σ).toNat) ≠ 0)
    (h3 : (3 : ZMod (eisNorm σ).toNat) ≠ 0)
    (h6 : 6 ∣ (eisNorm σ).toNat - 1) :
    residueMatrix ρ σ * classVector κ σ =
      star (directShiftedGauss σ (rowShift κ ρ σ) /
        (Real.sqrt ((eisNorm σ).toNat : ℝ) : ℂ)) := by
  have hshift := shiftedGauss_e4 σ hr h2 h3 h6 (rowShift κ ρ σ)
  have hrow := rowShift_symbol σ ρ κ hr h2 h3 h6
  have hd : star ((Real.sqrt ((eisNorm σ).toNat : ℝ) : ℂ)) =
      ((Real.sqrt ((eisNorm σ).toNat : ℝ) : ℂ)) := by simp
  unfold residueMatrix classVector normalizedGauss
  rw [hshift, hrow]
  simp only [star_div₀, star_mul, star_star, hd]
  ring

end ReciprocitySpectra
