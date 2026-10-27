module

public import ReciprocitySpectra.CharacterBridge

@[expose] public section

/-!
# RS-S029: the sextic exponent as a multiplicative character

This bridge uses the existing exponent defined over `ZMod p`. It does not
identify the residue field with an Eisenstein-integer quotient (the modelling
convention in `Sextic.lean`).
-/

namespace ReciprocitySpectra

variable {p : ℕ} [Fact p.Prime]

/-- The complex sextic root uses the same positive orientation as Mathlib's
canonical primitive root. -/
theorem complexZeta6_eq_exp :
    complexZeta6 = Complex.exp (2 * (Real.pi : ℂ) * Complex.I / 6) := by
  unfold complexZeta6
  congr 1
  ring

theorem complexZeta6_primitive : IsPrimitiveRoot complexZeta6 6 := by
  rw [complexZeta6_eq_exp]
  exact Complex.isPrimitiveRoot_exp 6 (by norm_num)

theorem complexZeta6_pow_mod (n : ℕ) :
    complexZeta6 ^ n = complexZeta6 ^ (n % 6) := by
  have h6 : complexZeta6 ^ 6 = 1 := complexZeta6_primitive.pow_eq_one
  conv_lhs => rw [← Nat.div_add_mod n 6, pow_add, pow_mul, h6, one_pow, one_mul]

/-- Complex value of the exponent, extended by zero. -/
noncomputable def sexticValue (r x : ZMod p) : ℂ :=
  (sexticExp r x).elim 0 (fun k => complexZeta6 ^ k.val)

@[simp] theorem sexticValue_zero (r : ZMod p) : sexticValue r 0 = 0 := by
  simp [sexticValue, sexticExp]

theorem sexticValue_of_some {r x : ZMod p} {k : Fin 6}
    (h : sexticExp r x = some k) :
    sexticValue r x = complexZeta6 ^ k.val := by
  simp [sexticValue, h]

theorem sexticValue_one {r : ZMod p}
    (hr : r ^ 2 + r + 1 = 0) (h2 : (2 : ZMod p) ≠ 0)
    (h3 : (3 : ZMod p) ≠ 0) :
    sexticValue r 1 = 1 := by
  have h1 : sexticExp r 1 = some (0 : Fin 6) :=
    sexticExp_eq_some hr h2 h3 (one_ne_zero) (by simp)
  simpa using sexticValue_of_some h1

theorem sexticValue_mul {r : ZMod p}
    (hr : r ^ 2 + r + 1 = 0) (h2 : (2 : ZMod p) ≠ 0)
    (h3 : (3 : ZMod p) ≠ 0) (h6 : 6 ∣ p - 1)
    (x y : ZMod p) :
    sexticValue r (x * y) = sexticValue r x * sexticValue r y := by
  by_cases hx : x = 0
  · subst x
    simp
  by_cases hy : y = 0
  · subst y
    simp
  obtain ⟨k, hk⟩ := exists_exp hr h2 h3 h6 hx
  obtain ⟨l, hl⟩ := exists_exp hr h2 h3 h6 hy
  have sx : sexticExp r x = some k :=
    sexticExp_eq_some hr h2 h3 hx hk
  have sy : sexticExp r y = some l :=
    sexticExp_eq_some hr h2 h3 hy hl
  have sxy : sexticExp r (x * y) = some (k + l) :=
    sexticExp_mul hr h2 h3 sx sy
  rw [sexticValue_of_some sx, sexticValue_of_some sy,
    sexticValue_of_some sxy]
  rw [Fin.val_add, ← complexZeta6_pow_mod (k.val + l.val), pow_add]

/-- A split-prime residue root satisfies its Eisenstein quadratic equation.
The prime-norm hypothesis supplies the field; nonvanishing of the second
coordinate in that field is explicit. Primarity is not needed for this
algebraic identity. -/
theorem residueRoot_poly (σ : Eis)
    [Fact (eisNorm σ).toNat.Prime]
    (hb : (σ.d : ZMod (eisNorm σ).toNat) ≠ 0) :
    residueRoot σ ^ 2 + residueRoot σ + 1 = 0 := by
  have hn_pos : 0 ≤ eisNorm σ := by
    dsimp [eisNorm]
    nlinarith [sq_nonneg (2 * σ.c - σ.d), sq_nonneg σ.d]
  have hn_int : eisNorm σ = ((eisNorm σ).toNat : ℤ) :=
    (Int.toNat_of_nonneg hn_pos).symm
  have hcast : (eisNorm σ : ZMod (eisNorm σ).toNat) = 0 := by
    calc
      (eisNorm σ : ZMod (eisNorm σ).toNat) =
          (((eisNorm σ).toNat : ℤ) : ZMod (eisNorm σ).toNat) :=
            congrArg (fun z : ℤ => (z : ZMod (eisNorm σ).toNat)) hn_int
      _ = 0 := by simpa only [Int.cast_natCast] using
        (ZMod.natCast_self (eisNorm σ).toNat)
  have hn : (σ.c : ZMod (eisNorm σ).toNat) ^ 2 -
      (σ.c : ZMod (eisNorm σ).toNat) * (σ.d : ZMod (eisNorm σ).toNat) +
      (σ.d : ZMod (eisNorm σ).toNat) ^ 2 = 0 := by
    change ((σ.c * σ.c - σ.c * σ.d + σ.d * σ.d : ℤ) :
      ZMod (eisNorm σ).toNat) = 0 at hcast
    push_cast at hcast
    simpa only [pow_two] using hcast
  have hbr : (σ.d : ZMod (eisNorm σ).toNat) * residueRoot σ =
      -(σ.c : ZMod (eisNorm σ).toNat) := by
    dsimp [residueRoot]
    calc
      (σ.d : ZMod (eisNorm σ).toNat) *
          (-(σ.c : ZMod (eisNorm σ).toNat) *
            (σ.d : ZMod (eisNorm σ).toNat)⁻¹) =
        -(σ.c : ZMod (eisNorm σ).toNat) *
          ((σ.d : ZMod (eisNorm σ).toNat) *
            (σ.d : ZMod (eisNorm σ).toNat)⁻¹) := by ring
      _ = -(σ.c : ZMod (eisNorm σ).toNat) := by
        rw [mul_inv_cancel₀ hb, mul_one]
  have hz : (σ.d : ZMod (eisNorm σ).toNat) ^ 2 *
      (residueRoot σ ^ 2 + residueRoot σ + 1) = 0 := by
    calc
      _ = ((σ.d : ZMod (eisNorm σ).toNat) * residueRoot σ) ^ 2 +
          (σ.d : ZMod (eisNorm σ).toNat) *
            ((σ.d : ZMod (eisNorm σ).toNat) * residueRoot σ) +
          (σ.d : ZMod (eisNorm σ).toNat) ^ 2 := by ring
      _ = (σ.c : ZMod (eisNorm σ).toNat) ^ 2 -
          (σ.c : ZMod (eisNorm σ).toNat) * (σ.d : ZMod (eisNorm σ).toNat) +
          (σ.d : ZMod (eisNorm σ).toNat) ^ 2 := by rw [hbr]; ring
      _ = 0 := hn
  exact (mul_eq_zero.mp hz).resolve_left (pow_ne_zero 2 hb)

/-- The sextic `MulChar`, constructed without any additional axioms.
The root and split-prime constraints are explicit parameters. -/
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

/-- The actual character agrees with the previously checked exponent
definition at *every* residue, including zero. -/
theorem sexticCharacter_apply (r : ZMod p)
    (hr : r ^ 2 + r + 1 = 0) (h2 : (2 : ZMod p) ≠ 0)
    (h3 : (3 : ZMod p) ≠ 0) (h6 : 6 ∣ p - 1)
    (x : ZMod p) :
    sexticCharacter r hr h2 h3 h6 x = sexticValue r x := rfl

/-- Nontriviality follows from cyclicity of the split-prime field's
multiplicative group. The Euler-criterion power cannot be identically one
because its exponent is strictly smaller than the group's order. -/
theorem sexticCharacter_ne_one (r : ZMod p)
    (hr : r ^ 2 + r + 1 = 0) (h2 : (2 : ZMod p) ≠ 0)
    (h3 : (3 : ZMod p) ≠ 0) (h6 : 6 ∣ p - 1) :
    sexticCharacter r hr h2 h3 h6 ≠ 1 := by
  classical
  have hp : 1 < p := (Fact.out : p.Prime).one_lt
  have hge : 6 ≤ p - 1 := Nat.le_of_dvd (by omega) h6
  obtain ⟨g, hg⟩ := (inferInstance : IsCyclic (ZMod p)ˣ).exists_generator
  have hgo : orderOf g = p - 1 := by
    simpa [Nat.card_eq_fintype_card, Fintype.card_units] using
      (orderOf_eq_card_of_forall_mem_zpowers hg)
  have hpowUnits : g ^ ((p - 1) / 6) ≠ 1 :=
    pow_ne_one_of_lt_orderOf (by omega) (by rw [hgo]; omega)
  have hpow : ((g : ZMod p) ^ ((p - 1) / 6)) ≠ 1 := by
    intro heq
    apply hpowUnits
    apply Units.val_injective
    simpa using heq
  obtain ⟨k, hk⟩ := exists_exp hr h2 h3 h6 g.ne_zero
  have hs : sexticExp r (g : ZMod p) = some k :=
    sexticExp_eq_some hr h2 h3 g.ne_zero hk
  intro htriv
  have hv : sexticCharacter r hr h2 h3 h6 (g : ZMod p) = 1 := by
    rw [htriv]
    exact MulChar.one_apply_coe g
  have hroot : complexZeta6 ^ k.val = 1 := by
    calc
      complexZeta6 ^ k.val = sexticCharacter r hr h2 h3 h6 (g : ZMod p) :=
        (sexticValue_of_some hs).symm.trans (sexticCharacter_apply r hr h2 h3 h6 _).symm
      _ = 1 := hv
  have hdvd : 6 ∣ k.val :=
    (complexZeta6_primitive.pow_eq_one_iff_dvd _).mp hroot
  have hkzero : k.val = 0 := by omega
  apply hpow
  rw [hk]
  simp [hkzero]

/-- Identification with the complex symbol for embedded rational integers,
including the zero residue. -/
theorem sexticCharacter_rational (σ : Eis)
    [Fact (eisNorm σ).toNat.Prime]
    (hr : residueRoot σ ^ 2 + residueRoot σ + 1 = 0)
    (h2 : (2 : ZMod (eisNorm σ).toNat) ≠ 0)
    (h3 : (3 : ZMod (eisNorm σ).toNat) ≠ 0)
    (h6 : 6 ∣ (eisNorm σ).toNat - 1) (n : ℤ) :
    sexticCharacter (residueRoot σ) hr h2 h3 h6
      (n : ZMod (eisNorm σ).toNat) = complexSymbol ⟨n, 0⟩ σ := by
  rw [sexticCharacter_apply]
  simp only [sexticValue, complexSymbol, symExp, res, Eis.c, Eis.d,
    Int.cast_zero, zero_mul, add_zero]
  cases h : sexticExp (residueRoot σ) (n : ZMod (eisNorm σ).toNat) <;> simp [h]

end ReciprocitySpectra
