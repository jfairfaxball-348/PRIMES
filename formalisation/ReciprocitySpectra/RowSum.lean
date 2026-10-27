module

public import ReciprocitySpectra.RowBridge

@[expose] public section

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

/-- A prime norm cannot divide both Eisenstein coordinates: if p divided
both, p² would divide the norm p, contradicting p ≥ 2. -/
theorem primeNorm_d_ne_zero (σ : Eis)
    (hp : (eisNorm σ).toNat.Prime) :
    (σ.d : ZMod (eisNorm σ).toNat) ≠ 0 := by
  let p := (eisNorm σ).toNat
  letI : Fact p.Prime := ⟨hp⟩
  have hpos : 0 ≤ eisNorm σ := by
    dsimp [eisNorm]
    nlinarith [sq_nonneg (2 * σ.c - σ.d), sq_nonneg σ.d]
  have heq : eisNorm σ = (p : ℤ) := (Int.toNat_of_nonneg hpos).symm
  intro hd0
  have hnormzero :
      (σ.c : ZMod p) ^ 2 - (σ.c : ZMod p) * (σ.d : ZMod p) +
        (σ.d : ZMod p) ^ 2 = 0 := by
    have hz : (eisNorm σ : ZMod p) = 0 := by
      rw [heq]
      simpa only [Int.cast_natCast] using (ZMod.natCast_self p)
    change ((σ.c * σ.c - σ.c * σ.d + σ.d * σ.d : ℤ) : ZMod p) = 0 at hz
    push_cast at hz
    simpa only [pow_two] using hz
  have hc2 : (σ.c : ZMod p) ^ 2 = 0 := by simpa [hd0] using hnormzero
  have hc0 : (σ.c : ZMod p) = 0 := by
    rcases mul_eq_zero.mp (by simpa only [pow_two] using hc2) with h | h
    · exact h
    · exact h
  obtain ⟨u, hu⟩ := (ZMod.intCast_zmod_eq_zero_iff_dvd σ.c p).mp hc0
  obtain ⟨v, hv⟩ := (ZMod.intCast_zmod_eq_zero_iff_dvd σ.d p).mp hd0
  let m : ℤ := u * u - u * v + v * v
  have hmnorm : (p : ℤ) = (p : ℤ) * ((p : ℤ) * m) := by
    calc
      (p : ℤ) = eisNorm σ := heq.symm
      _ = (p : ℤ) * ((p : ℤ) * m) := by
        dsimp [eisNorm, m]
        rw [hu, hv]
        ring
  have hpneq : (p : ℤ) ≠ 0 := by exact_mod_cast hp.ne_zero
  have hone : (1 : ℤ) = (p : ℤ) * m := by
    apply mul_left_cancel₀ hpneq
    simpa only [mul_one] using hmnorm
  have hpge : (2 : ℤ) ≤ p := by exact_mod_cast hp.two_le
  by_cases hm : m ≤ 0
  · have hmul : (p : ℤ) * m ≤ (p : ℤ) * 0 :=
      mul_le_mul_of_nonneg_left hm (by omega)
    omega
  · have hm1 : 1 ≤ m := by omega
    have hmul : (p : ℤ) * 1 ≤ (p : ℤ) * m :=
      mul_le_mul_of_nonneg_left hm1 (by omega)
    omega

/-- Every indexed column automatically satisfies the complete sextic
character assumptions, without assuming them as an axiom or argument. -/
theorem primarySplitPrimes_model {X : ℕ} {σ : Eis}
    (hσ : σ ∈ primarySplitPrimes X) :
    (σ.d : ZMod (eisNorm σ).toNat) ≠ 0 ∧
    residueRoot σ ^ 2 + residueRoot σ + 1 = 0 ∧
    (2 : ZMod (eisNorm σ).toNat) ≠ 0 ∧
    (3 : ZMod (eisNorm σ).toNat) ≠ 0 ∧
    6 ∣ (eisNorm σ).toNat - 1 := by
  let p := (eisNorm σ).toNat
  have hc : σ.c % 3 = 2 := (Finset.mem_filter.mp hσ).2.1
  have hd : σ.d % 3 = 0 := (Finset.mem_filter.mp hσ).2.2.1
  have hp : p.Prime := primarySplitPrimes_prime hσ
  letI : Fact p.Prime := ⟨hp⟩
  have hn_pos : 0 ≤ eisNorm σ := by
    dsimp [eisNorm]
    nlinarith [sq_nonneg (2 * σ.c - σ.d), sq_nonneg σ.d]
  have hn_int : eisNorm σ = (p : ℤ) := (Int.toNat_of_nonneg hn_pos).symm
  have hp3 : p % 3 = 1 := by
    have hm : (p : ℤ) % 3 = 1 := by
      rw [← hn_int]
      exact primary_norm_mod_three σ hc hd
    exact_mod_cast hm
  have hpne2 : p ≠ 2 := by omega
  have hpne3 : p ≠ 3 := by omega
  have hp5 : 5 ≤ p := hp.five_le_of_ne_two_of_ne_three hpne2 hpne3
  have h2 : (2 : ZMod p) ≠ 0 := by
    intro hz
    have hdvd : p ∣ 2 := (ZMod.natCast_eq_zero_iff 2 p).mp hz
    have hle : p ≤ 2 := Nat.le_of_dvd (by omega) hdvd
    omega
  have h3 : (3 : ZMod p) ≠ 0 := by
    intro hz
    have hdvd : p ∣ 3 := (ZMod.natCast_eq_zero_iff 3 p).mp hz
    have hle : p ≤ 3 := Nat.le_of_dvd (by omega) hdvd
    omega
  have hpodd : p % 2 = 1 := (hp.mod_two_eq_one_iff_ne_two).mpr hpne2
  have h6 : 6 ∣ p - 1 := by omega
  have hb : (σ.d : ZMod p) ≠ 0 := primeNorm_d_ne_zero σ hp
  exact ⟨hb, residueRoot_poly σ hb, h2, h3, h6⟩

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

/-- Actual finite matrix identity, with ALL column hypotheses derived from
membership in the frozen primary split-prime index. -/
theorem residueMatVec_orientation (X : ℕ) (κ : TwistClass) (ρ : Eis) :
    residueMatVec X κ ρ =
      ∑ σ ∈ primarySplitPrimes X,
        star (directShiftedGauss σ (rowShift κ ρ σ) /
          (Real.sqrt ((eisNorm σ).toNat : ℝ) : ℂ)) := by
  apply residueMatVec_orientation_of
  intro σ hσ
  obtain ⟨hb, hr, h2, h3, h6⟩ := primarySplitPrimes_model hσ
  exact ⟨hb, h2, h3, h6⟩


end ReciprocitySpectra
