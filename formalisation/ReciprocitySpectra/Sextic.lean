import Mathlib

/-!
# Sextic residue exponents at split primes of `ℤ[ω]` (CAND-002 inventory E0–E3, E5, E6)

Modelling convention (documented, not derived from a Mathlib `ℤ[ω]`): a primary prime `ρ = a + bω` of
`ℤ[ω]` with `N ρ = p ≡ 1 (mod 6)` is handled through its residue field, identified with `ZMod p` by
`ω ↦ r`, where `r = -a/b` satisfies `r² + r + 1 = 0`. Elements `c + dω` are pairs `(c, d)`.
`ζ = 1 + r` is the image of `ζ₆ = 1 + ω`. The sextic exponent of `x ≠ 0` is the `k : Fin 6` with
`x ^ ((p - 1) / 6) = ζ ^ k` (Euler's criterion), exactly as in `reciprocity_spectra/arith.py` and the
numerical engines.
-/

namespace ReciprocitySpectra

/-- `c + d ω` in `ℤ[ω]`, with `ω² = -1 - ω`. -/
structure Eis where
  c : ℤ
  d : ℤ
  deriving DecidableEq, Repr

namespace Eis

/-- Multiplication in `ℤ[ω]` (`arith._mul_w`). -/
instance : Mul Eis := ⟨fun x y => ⟨x.c * y.c - x.d * y.d, x.c * y.d + x.d * y.c - x.d * y.d⟩⟩

@[simp] lemma mul_c (x y : Eis) : (x * y).c = x.c * y.c - x.d * y.d := rfl
@[simp] lemma mul_d (x y : Eis) : (x * y).d = x.c * y.d + x.d * y.c - x.d * y.d := rfl

/-- `ζ₆ = 1 + ω`. -/
def zeta6 : Eis := ⟨1, 1⟩

end Eis

variable {p : ℕ}

/-- Reduction `ℤ[ω] → ZMod p`, `c + dω ↦ c + d r`. -/
def res (r : ZMod p) (x : Eis) : ZMod p := x.c + x.d * r

/-- E3 (ring part): reduction is multiplicative when `r² + r + 1 = 0`. -/
theorem res_mul {r : ZMod p} (hr : r ^ 2 + r + 1 = 0) (x y : Eis) :
    res r (x * y) = res r x * res r y := by
  simp only [res, Eis.mul_c, Eis.mul_d]
  push_cast
  linear_combination (-(x.d : ZMod p) * y.d) * hr

/-- The image of `ζ₆`. -/
def zeta (r : ZMod p) : ZMod p := 1 + r

theorem res_zeta6 (r : ZMod p) : res r Eis.zeta6 = zeta r := by
  simp [res, Eis.zeta6, zeta]

/-- The sextic exponent (Euler's criterion), `none` when the residue is `0`. Computable. -/
def sexticExp (r x : ZMod p) : Option (Fin 6) :=
  if x = 0 then none
  else (List.finRange 6 : List (Fin 6)).find? (fun k : Fin 6 => x ^ ((p - 1) / 6) = zeta r ^ k.val)

/-- The symbol exponent of an element `α ∈ ℤ[ω]` at the split prime given by `r`. -/
def symExp (r : ZMod p) (α : Eis) : Option (Fin 6) := sexticExp r (res r α)

section Field

variable [Fact p.Prime]

lemma zeta_cube {r : ZMod p} (hr : r ^ 2 + r + 1 = 0) : zeta r ^ 3 = -1 := by
  unfold zeta
  linear_combination (r + 2) * hr

lemma zeta_sq {r : ZMod p} (hr : r ^ 2 + r + 1 = 0) : zeta r ^ 2 = r := by
  unfold zeta
  linear_combination hr

/-- `ζ = 1 + r` is a primitive sixth root of unity when `p ≠ 2, 3`. -/
theorem zeta_primitive {r : ZMod p} (hr : r ^ 2 + r + 1 = 0) (h2 : (2 : ZMod p) ≠ 0)
    (h3 : (3 : ZMod p) ≠ 0) : IsPrimitiveRoot (zeta r) 6 := by
  have hc := zeta_cube hr
  have hs := zeta_sq hr
  refine IsPrimitiveRoot.mk_of_lt (zeta r) (by norm_num) ?_ ?_
  · calc zeta r ^ 6 = (zeta r ^ 3) ^ 2 := by ring
      _ = 1 := by rw [hc]; ring
  · intro l hl0 hl6 h1
    interval_cases l
    · -- ζ = 1 forces r = 0, then 1 = 0
      have : r = 0 := by unfold zeta at h1; linear_combination h1
      rw [this] at hr
      norm_num at hr
    · -- ζ² = r = 1 forces 3 = 0
      rw [hs] at h1
      rw [h1] at hr
      exact h3 (by linear_combination hr)
    · -- ζ³ = -1 = 1 forces 2 = 0
      rw [hc] at h1
      exact h2 (by linear_combination -h1)
    · -- ζ⁴ = -ζ = 1 forces r = -2, then 3 = 0
      have h4 : zeta r ^ 4 = -zeta r := by
        calc zeta r ^ 4 = zeta r ^ 3 * zeta r := by ring
          _ = -zeta r := by rw [hc]; ring
      rw [h4] at h1
      have : r = -2 := by unfold zeta at h1; linear_combination -h1
      rw [this] at hr
      exact h3 (by linear_combination hr)
    · -- ζ⁵ = -ζ² = -r = 1 forces r = -1, then 1 = 0
      have h5 : zeta r ^ 5 = -r := by
        calc zeta r ^ 5 = zeta r ^ 3 * zeta r ^ 2 := by ring
          _ = -r := by rw [hc, hs]; ring
      rw [h5] at h1
      have : r = -1 := by linear_combination -h1
      rw [this] at hr
      norm_num at hr

/-- E0: for `x ≠ 0` and `6 ∣ p - 1`, `x ^ ((p - 1) / 6)` is a power of `ζ`. -/
theorem exists_exp {r : ZMod p} (hr : r ^ 2 + r + 1 = 0) (h2 : (2 : ZMod p) ≠ 0)
    (h3 : (3 : ZMod p) ≠ 0) (h6 : 6 ∣ p - 1) {x : ZMod p} (hx : x ≠ 0) :
    ∃ k : Fin 6, x ^ ((p - 1) / 6) = zeta r ^ (k : ℕ) := by
  have hprim := zeta_primitive hr h2 h3
  have hpow : (x ^ ((p - 1) / 6)) ^ 6 = 1 := by
    rw [← pow_mul, Nat.div_mul_cancel h6]
    exact ZMod.pow_card_sub_one_eq_one hx
  obtain ⟨i, hi, hzi⟩ := hprim.eq_pow_of_pow_eq_one hpow
  exact ⟨⟨i, hi⟩, hzi.symm⟩

/-- E0: the exponent is unique. -/
theorem exp_unique {r : ZMod p} (hr : r ^ 2 + r + 1 = 0) (h2 : (2 : ZMod p) ≠ 0)
    (h3 : (3 : ZMod p) ≠ 0) {k l : Fin 6} (h : zeta r ^ (k : ℕ) = zeta r ^ (l : ℕ)) : k = l :=
  Fin.ext ((zeta_primitive hr h2 h3).pow_inj k.isLt l.isLt h)

/-- Characterisation of `sexticExp` from its definition (`List.find?` over `Fin 6`). -/
theorem sexticExp_some {r x : ZMod p} {k : Fin 6} (h : sexticExp r x = some k) :
    x ≠ 0 ∧ x ^ ((p - 1) / 6) = zeta r ^ (k : ℕ) := by
  unfold sexticExp at h
  split_ifs at h with hx
  refine ⟨hx, ?_⟩
  simpa using List.find?_some h

/-- Conversely, any valid exponent is the computed one (uses uniqueness, E0). -/
theorem sexticExp_eq_some {r : ZMod p} (hr : r ^ 2 + r + 1 = 0) (h2 : (2 : ZMod p) ≠ 0)
    (h3 : (3 : ZMod p) ≠ 0) {x : ZMod p} {k : Fin 6} (hx : x ≠ 0)
    (hk : x ^ ((p - 1) / 6) = zeta r ^ (k : ℕ)) : sexticExp r x = some k := by
  have hs : ((List.finRange 6 : List (Fin 6)).find?
      (fun j : Fin 6 => x ^ ((p - 1) / 6) = zeta r ^ j.val)).isSome := by
    rw [List.find?_isSome]
    exact ⟨k, List.mem_finRange k, by simpa using hk⟩
  obtain ⟨j, hj⟩ := Option.isSome_iff_exists.mp hs
  have hj' : x ^ ((p - 1) / 6) = zeta r ^ (j : ℕ) := by simpa using List.find?_some hj
  have : j = k := exp_unique hr h2 h3 (hj'.symm.trans hk)
  unfold sexticExp
  rw [if_neg hx, hj, this]

lemma zeta_pow_mod {r : ZMod p} (hr : r ^ 2 + r + 1 = 0) (n : ℕ) : zeta r ^ n = zeta r ^ (n % 6) := by
  have h6 : zeta r ^ 6 = 1 := by
    calc zeta r ^ 6 = (zeta r ^ 3) ^ 2 := by ring
      _ = 1 := by rw [zeta_cube hr]; ring
  conv_lhs => rw [← Nat.div_add_mod n 6, pow_add, pow_mul, h6, one_pow, one_mul]

/-- E3: sextic exponents add under multiplication. -/
theorem sexticExp_mul {r : ZMod p} (hr : r ^ 2 + r + 1 = 0) (h2 : (2 : ZMod p) ≠ 0)
    (h3 : (3 : ZMod p) ≠ 0) {x y : ZMod p} {k l : Fin 6} (hx : sexticExp r x = some k)
    (hy : sexticExp r y = some l) : sexticExp r (x * y) = some (k + l) := by
  obtain ⟨hx0, hxk⟩ := sexticExp_some hx
  obtain ⟨hy0, hyl⟩ := sexticExp_some hy
  apply sexticExp_eq_some hr h2 h3 (mul_ne_zero hx0 hy0)
  rw [mul_pow, hxk, hyl, ← pow_add, zeta_pow_mod hr, Fin.val_add]

/-- E3 for elements of `ℤ[ω]`. -/
theorem symExp_mul {r : ZMod p} (hr : r ^ 2 + r + 1 = 0) (h2 : (2 : ZMod p) ≠ 0)
    (h3 : (3 : ZMod p) ≠ 0) {α β : Eis} {k l : Fin 6} (hα : symExp r α = some k)
    (hβ : symExp r β = some l) : symExp r (α * β) = some (k + l) := by
  unfold symExp at *
  rw [res_mul hr]
  exact sexticExp_mul hr h2 h3 hα hβ

/-- E1: multiplying by a sixth power coprime to the prime leaves the exponent unchanged. -/
theorem sexticExp_mul_sixth_pow {r : ZMod p} (h6 : 6 ∣ p - 1) {x y : ZMod p} (hy : y ≠ 0) :
    sexticExp r (x * y ^ 6) = sexticExp r x := by
  have hy6 : (y ^ 6) ^ ((p - 1) / 6) = 1 := by
    rw [← pow_mul, Nat.mul_div_cancel' h6]
    exact ZMod.pow_card_sub_one_eq_one hy
  unfold sexticExp
  by_cases hx : x = 0
  · simp [hx]
  · rw [if_neg (mul_ne_zero hx (pow_ne_zero 6 hy)), if_neg hx, mul_pow, hy6, mul_one]

lemma five_mul_mod (k : Fin 6) : (k : ℕ) * 5 % 6 = ((-k : Fin 6) : ℕ) % 6 := by
  fin_cases k <;> rfl

/-- E2: the fifth power gives the negated (conjugate) exponent. -/
theorem sexticExp_pow_five {r : ZMod p} (hr : r ^ 2 + r + 1 = 0) (h2 : (2 : ZMod p) ≠ 0)
    (h3 : (3 : ZMod p) ≠ 0) {x : ZMod p} {k : Fin 6} (hx : sexticExp r x = some k) :
    sexticExp r (x ^ 5) = some (-k) := by
  obtain ⟨hx0, hxk⟩ := sexticExp_some hx
  apply sexticExp_eq_some hr h2 h3 (pow_ne_zero 5 hx0)
  rw [← pow_mul, mul_comm, pow_mul, hxk, ← pow_mul, zeta_pow_mod hr, zeta_pow_mod hr ((-k : Fin 6) : ℕ),
    five_mul_mod]

/-- E5: the exponent of `ζ₆` at a split prime is `((p - 1) / 6) mod 6`. -/
theorem sexticExp_zeta {r : ZMod p} (hr : r ^ 2 + r + 1 = 0) (h2 : (2 : ZMod p) ≠ 0)
    (h3 : (3 : ZMod p) ≠ 0) :
    sexticExp r (zeta r) = some ⟨(p - 1) / 6 % 6, Nat.mod_lt _ (by norm_num)⟩ := by
  have hz : zeta r ≠ 0 := by
    intro h0
    have := zeta_cube hr
    rw [h0] at this
    exact h2 (by linear_combination 2 * this)
  exact sexticExp_eq_some hr h2 h3 hz (zeta_pow_mod hr _)

/-- E5 (norm arithmetic): `(N - 1)/6 mod 6` is additive on norms `≡ 1 (mod 6)`. -/
theorem unit_exponent_additive (m n : ℕ) :
    ((6 * m + 1) * (6 * n + 1) - 1) / 6 % 6 = (m + n) % 6 := by
  have h : (6 * m + 1) * (6 * n + 1) - 1 = 6 * (6 * (m * n) + (m + n)) := by
    have : (6 * m + 1) * (6 * n + 1) = 6 * (6 * (m * n) + (m + n)) + 1 := by ring
    omega
  rw [h, Nat.mul_div_cancel_left _ (by norm_num), Nat.mul_add_mod]

/-- E6: with `b r = -a`, `2a - b ≡ -b (1 + 2r)`, i.e. `Tr ρ ≡ -b √-3` modulo `ρ`. -/
theorem trace_residue {r : ZMod p} {a b : ℤ} (hb : (b : ZMod p) * r = -(a : ZMod p)) :
    ((2 * a - b : ℤ) : ZMod p) = -(b : ZMod p) * (1 + 2 * r) := by
  push_cast
  linear_combination (2 : ZMod p) * hb

end Field

end ReciprocitySpectra
