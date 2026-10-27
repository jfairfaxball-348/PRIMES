import ReciprocitySpectra.SexticCharacter

/-!
# RS-S030: the direct rational Gauss sum and the finite-field Gauss sum

This module identifies the *actual* direct sum used in Model.rawGauss with
Mathlib's gaussSum. The positive-sign additive character and the rational
representatives 0,...,p-1 are matched explicitly.
-/

namespace ReciprocitySpectra

/-- Every residue is represented exactly once by a natural number below p. -/
theorem zmod_sum_eq_range (p : ℕ) [NeZero p] (f : ZMod p → ℂ) :
    (∑ x : ZMod p, f x) = ∑ t ∈ Finset.range p, f (t : ZMod p) := by
  classical
  calc
    (∑ x : ZMod p, f x) = ∑ j : Fin p, f (ZMod.finEquiv p j) := by
      simpa using ((ZMod.finEquiv p).sum_comp f).symm
    _ = ∑ j : Fin p, f (j.val : ZMod p) := by
      apply Finset.sum_congr rfl
      intro j _
      congr 1
      apply ZMod.val_injective
      rw [ZMod.val_natCast, Nat.mod_eq_of_lt j.isLt]
      cases p with
      | zero => exact (NeZero.ne 0 rfl).elim
      | succ n => rfl
    _ = ∑ t ∈ Finset.range p, f (t : ZMod p) :=
      Fin.sum_univ_eq_sum_range (fun t : ℕ => f (t : ZMod p)) p

/-- The canonical additive character has the same positive exponential
sign as the direct rational sum, on its full range of representatives. -/
theorem rationalAddChar_nat (p : ℕ) [NeZero p] (t : ℕ) (ht : t < p) :
    rationalAddChar p (t : ZMod p) =
      Complex.exp (2 * (Real.pi : ℂ) * Complex.I * (t : ℂ) / (p : ℂ)) := by
  rw [rationalAddChar_apply, ZMod.val_natCast_of_lt ht, ← Complex.exp_nat_mul]
  congr 1
  ring

/-- The direct sextic rational Gauss sum equals the Mathlib finite-field
Gauss sum. All split-prime-model assumptions are explicit; no equality is
postulated as a hypothesis. -/
theorem gaussSum_sextic_eq_raw (σ : Eis)
    [Fact (eisNorm σ).toNat.Prime]
    (hr : residueRoot σ ^ 2 + residueRoot σ + 1 = 0)
    (h2 : (2 : ZMod (eisNorm σ).toNat) ≠ 0)
    (h3 : (3 : ZMod (eisNorm σ).toNat) ≠ 0)
    (h6 : 6 ∣ (eisNorm σ).toNat - 1) :
    gaussSum (sexticCharacter (residueRoot σ) hr h2 h3 h6)
      (rationalAddChar (eisNorm σ).toNat) = rawGauss σ := by
  let p := (eisNorm σ).toNat
  haveI : NeZero p := ⟨(Fact.out : p.Prime).ne_zero⟩
  rw [gaussSum, zmod_sum_eq_range]
  unfold rawGauss
  apply Finset.sum_congr rfl
  intro t ht
  have hχ :
      sexticCharacter (residueRoot σ) hr h2 h3 h6
        (t : ZMod (eisNorm σ).toNat) =
        complexSymbol ⟨(t : ℤ), 0⟩ σ := by
    simpa only [Int.cast_natCast] using
      (sexticCharacter_rational σ hr h2 h3 h6 (t : ℤ))
  rw [hχ, rationalAddChar_nat p t (Finset.mem_range.mp ht)]
  rfl

/-- E7 for the actual rational sextic Gauss sum, not merely an abstract
character: squared modulus is the norm p of the split prime. -/
theorem rawGauss_modulus_sq (σ : Eis)
    [Fact (eisNorm σ).toNat.Prime]
    (hr : residueRoot σ ^ 2 + residueRoot σ + 1 = 0)
    (h2 : (2 : ZMod (eisNorm σ).toNat) ≠ 0)
    (h3 : (3 : ZMod (eisNorm σ).toNat) ≠ 0)
    (h6 : 6 ∣ (eisNorm σ).toNat - 1) :
    rawGauss σ * star (rawGauss σ) = ((eisNorm σ).toNat : ℂ) := by
  let p := (eisNorm σ).toNat
  haveI : NeZero p := ⟨(Fact.out : p.Prime).ne_zero⟩
  rw [← gaussSum_sextic_eq_raw σ hr h2 h3 h6]
  simpa only [ZMod.card] using
    (gauss_modulus_sq
      (sexticCharacter (residueRoot σ) hr h2 h3 h6)
      (rationalAddChar p)
      (sexticCharacter_ne_one (residueRoot σ) hr h2 h3 h6)
      (rationalAddChar_primitive p))

end ReciprocitySpectra
