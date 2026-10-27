import ReciprocitySpectra.RowBridge

/-!
# RS-S032: sum the exact sextic row orientation over genuine prime columns

The finite index supplies primality, not a new assumed field. The remaining
arithmetic conditions are explicitly listed until they can be derived from
membership. The theorem is conditional and is not the final release identity.
-/

namespace ReciprocitySpectra

/-- Every element of the finite column index has prime norm. -/
theorem primarySplitPrimes_prime {X : ℕ} {σ : Eis}
    (hσ : σ ∈ primarySplitPrimes X) : (eisNorm σ).toNat.Prime := by
  exact (Finset.mem_filter.mp hσ).2.2.2.1

/-- Primarity forces the integer norm to be one modulo three. -/
theorem primary_norm_mod_three (σ : Eis)
    (hc : σ.c % 3 = 2) (hd : σ.d % 3 = 0) :
    eisNorm σ % 3 = 1 := by
  let a := σ.c / 3
  let b := σ.d / 3
  have ha : σ.c = 3 * a + 2 := by dsimp [a]; omega
  have hb : σ.d = 3 * b := by dsimp [b]; omega
  have hn : eisNorm σ =
      3 * (3 * a ^ 2 + 4 * a - 3 * a * b - 2 * b + 3 * b ^ 2 + 1) + 1 := by
    dsimp [eisNorm]
    rw [ha, hb]
    ring
  omega

/-- Sum the already-proved per-column theorem without altering a single
matrix or class-vector definition. Root and characteristic conditions are
tracked as genuinely outstanding proof obligations rather than axioms. -/
theorem residueMatVec_orientation_of (X : ℕ) (κ : TwistClass) (ρ : Eis)
    (hcolumns : ∀ σ ∈ primarySplitPrimes X,
      (σ.d : ZMod (eisNorm σ).toNat) ≠ 0 ∧
      (2 : ZMod (eisNorm σ).toNat) ≠ 0 ∧
      (3 : ZMod (eisNorm σ).toNat) ≠ 0 ∧
      6 ∣ (eisNorm σ).toNat - 1) :
    residueMatVec X κ ρ =
      ∑ σ ∈ primarySplitPrimes X,
        star (directShiftedGauss σ (rowShift κ ρ σ) /
          (Real.sqrt ((eisNorm σ).toNat : ℝ) : ℂ)) := by
  unfold residueMatVec
  apply Finset.sum_congr rfl
  intro σ hσ
  obtain ⟨hb, h2, h3, h6⟩ := hcolumns σ hσ
  letI : Fact (eisNorm σ).toNat.Prime := ⟨primarySplitPrimes_prime hσ⟩
  exact residueColumn_orientation σ ρ κ (residueRoot_poly σ hb) h2 h3 h6

end ReciprocitySpectra
