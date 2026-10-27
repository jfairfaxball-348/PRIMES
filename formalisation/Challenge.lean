module

public import Mathlib

/-!
# Finite sextic arithmetic — independently auditable Challenge

These are exact elementary field and character identities in the proven
Reciprocity Spectra library, NOT any asymptotic CAND-002 conjecture.

The comparator also selects the actual specialised sextic Gauss E7 and E4,
finite Eisenstein numerator reduction and full frozen matrix-row identity.
Its definitions repeat the proof library's definitions, rather than importing
that library, as Palomar requires for an independent Challenge.
-/

@[expose] public section
namespace ReciprocitySpectra

/-- Coordinates of c+dω, where ω²+ω+1=0. -/
structure Eis where
  c : ℤ
  d : ℤ
  deriving DecidableEq, Repr

namespace Eis
/-- Multiplication in the Eisenstein coordinate model. -/
instance : Mul Eis := ⟨fun x y =>
  ⟨x.c * y.c - x.d * y.d, x.c * y.d + x.d * y.c - x.d * y.d⟩⟩

/-- The Eisenstein sixth root 1+ω. -/
@[simp] lemma mul_c (x y : Eis) : (x * y).c = x.c * y.c - x.d * y.d := rfl
@[simp] lemma mul_d (x y : Eis) : (x * y).d = x.c * y.d + x.d * y.c - x.d * y.d := rfl

def zeta6 : Eis := ⟨1, 1⟩
end Eis

variable {p : ℕ}

/-- Reduction c+dω ↦ c+dr into the explicitly modelled residue field. -/
def res (r : ZMod p) (x : Eis) : ZMod p := x.c + x.d * r

/-- A sixth root 1+r in the model field. -/
def zeta (r : ZMod p) : ZMod p := 1 + r

/-- The computable sextic exponent of a nonzero field residue; none at zero. -/
def sexticExp (r x : ZMod p) : Option (Fin 6) :=
  if x = 0 then none
  else (List.finRange 6 : List (Fin 6)).find?
    (fun k : Fin 6 => x ^ ((p - 1) / 6) = zeta r ^ k.val)

/-- Sextic exponent of an Eisenstein coordinate pair. -/
def symExp (r : ZMod p) (α : Eis) : Option (Fin 6) :=
  sexticExp r (res r α)

/-- E3: reduction preserves multiplication under the Eisenstein root equation. -/
theorem res_mul {r : ZMod p} (hr : r ^ 2 + r + 1 = 0) (x y : Eis) :
    res r (x * y) = res r x * res r y := by sorry

section Field
variable [Fact p.Prime]


/-- E0: 1+r is a primitive sixth root in the split-prime model. -/
theorem zeta_primitive {r : ZMod p} (hr : r ^ 2 + r + 1 = 0)
    (h2 : (2 : ZMod p) ≠ 0) (h3 : (3 : ZMod p) ≠ 0) :
    IsPrimitiveRoot (zeta r) 6 := by sorry

/-- E0: Euler's sixth-power character takes values among six roots. -/
theorem exists_exp {r : ZMod p} (hr : r ^ 2 + r + 1 = 0)
    (h2 : (2 : ZMod p) ≠ 0) (h3 : (3 : ZMod p) ≠ 0)
    (h6 : 6 ∣ p - 1) {x : ZMod p} (hx : x ≠ 0) :
    ∃ k : Fin 6, x ^ ((p - 1) / 6) = zeta r ^ (k : ℕ) := by sorry

/-- E0: uniqueness of the primitive-root exponent. -/
theorem exp_unique {r : ZMod p} (hr : r ^ 2 + r + 1 = 0)
    (h2 : (2 : ZMod p) ≠ 0) (h3 : (3 : ZMod p) ≠ 0)
    {k l : Fin 6} (h : zeta r ^ (k : ℕ) = zeta r ^ (l : ℕ)) :
    k = l := by sorry

/-- E3: sextic exponents are additive modulo six. -/
theorem sexticExp_mul {r : ZMod p} (hr : r ^ 2 + r + 1 = 0)
    (h2 : (2 : ZMod p) ≠ 0) (h3 : (3 : ZMod p) ≠ 0)
    {x y : ZMod p} {k l : Fin 6} (hx : sexticExp r x = some k)
    (hy : sexticExp r y = some l) :
    sexticExp r (x * y) = some (k + l) := by sorry

/-- E3: Eisenstein representatives inherit exponent additivity. -/
theorem symExp_mul {r : ZMod p} (hr : r ^ 2 + r + 1 = 0)
    (h2 : (2 : ZMod p) ≠ 0) (h3 : (3 : ZMod p) ≠ 0)
    {α β : Eis} {k l : Fin 6} (hα : symExp r α = some k)
    (hβ : symExp r β = some l) :
    symExp r (α * β) = some (k + l) := by sorry

/-- E1: multiplying by a nonzero sixth power leaves the symbol invariant. -/
theorem sexticExp_mul_sixth_pow {r : ZMod p} (h6 : 6 ∣ p - 1)
    {x y : ZMod p} (hy : y ≠ 0) :
    sexticExp r (x * y ^ 6) = sexticExp r x := by sorry

/-- E2: the fifth power negates the sextic exponent. -/
theorem sexticExp_pow_five {r : ZMod p} (hr : r ^ 2 + r + 1 = 0)
    (h2 : (2 : ZMod p) ≠ 0) (h3 : (3 : ZMod p) ≠ 0)
    {x : ZMod p} {k : Fin 6} (hx : sexticExp r x = some k) :
    sexticExp r (x ^ 5) = some (-k) := by sorry

/-- E5: sixth-root unit exponent at a split prime. -/
theorem sexticExp_zeta {r : ZMod p} (hr : r ^ 2 + r + 1 = 0)
    (h2 : (2 : ZMod p) ≠ 0) (h3 : (3 : ZMod p) ≠ 0) :
    sexticExp r (zeta r) =
      some ⟨(p - 1) / 6 % 6, Nat.mod_lt _ (by norm_num)⟩ := by sorry

/-- E5: norm unit exponents add under multiplication. -/
theorem unit_exponent_additive (m n : ℕ) :
    ((6 * m + 1) * (6 * n + 1) - 1) / 6 % 6 = (m + n) % 6 := by sorry

/-- E6: the trace-normalisation residue identity. -/
theorem trace_residue {r : ZMod p} {a b : ℤ}
    (hb : (b : ZMod p) * r = -(a : ZMod p)) :
    ((2 * a - b : ℤ) : ZMod p) = -(b : ZMod p) * (1 + 2 * r) := by sorry
end Field

section GaussIdentities
variable {F : Type*} [Field F] [Fintype F]

/-- Generic E7: squared modulus for a nontrivial multiplicative character
and primitive additive character, NOT yet the specialised sextic sum. -/
theorem gauss_modulus_sq (χ : MulChar F ℂ) (ψ : AddChar F ℂ)
    (hχ : χ ≠ 1) (hψ : ψ.IsPrimitive) :
    gaussSum χ ψ * star (gaussSum χ ψ) = (Fintype.card F : ℂ) := by sorry

/-- Generic E4: multiplicative twist by a unit. -/
theorem gauss_shift (χ : MulChar F ℂ) (ψ : AddChar F ℂ) (a : Fˣ) :
    gaussSum χ (ψ.mulShift (a : F)) = χ⁻¹ (a : F) * gaussSum χ ψ := by sorry

/-- A zero additive shift has zero Gauss sum for a nontrivial character. -/
theorem gauss_zero_shift (χ : MulChar F ℂ) (ψ : AddChar F ℂ)
    (hχ : χ ≠ 1) :
    gaussSum χ (ψ.mulShift (0 : F)) = 0 := by sorry

/-- Generic E4 at all shifts, including zero. -/
theorem gauss_shift_all [DecidableEq F] (χ : MulChar F ℂ)
    (ψ : AddChar F ℂ) (hχ : χ ≠ 1) (a : F) :
    gaussSum χ (ψ.mulShift a) =
      if a = 0 then 0 else χ⁻¹ a * gaussSum χ ψ := by sorry
end GaussIdentities


/-! ## RS-S035: exact specialised finite claims

These independently restated definitions use explicit Eisenstein coordinate-pair
arithmetic and the original finite sums, not an unconstructed quotient ring.
The advertised theorems are statements here and have proofs in Solution.
-/

/-- Quadratic Eisenstein norm c²-cd+d²; no positivity assumption is built into the definition. -/
def eisNorm (x : Eis) : ℤ := x.c * x.c - x.c * x.d + x.d * x.d


/-- Finite square-box enumeration of primary Eisenstein pairs with prime norm at most X. -/
def primarySplitPrimes (X : ℕ) : Finset Eis :=
  (((Finset.Icc (-(2 * (X : ℤ))) (2 * (X : ℤ))).product
      (Finset.Icc (-(2 * (X : ℤ))) (2 * (X : ℤ)))).image
    (fun ab : ℤ × ℤ => Eis.mk ab.1 ab.2)).filter
      (fun x => x.c % 3 = 2 ∧ x.d % 3 = 0 ∧
        (eisNorm x).toNat.Prime ∧ (eisNorm x).toNat ≤ X)


/-- Image of ω in the residue-field model: -c/d modulo the norm. -/
def residueRoot (σ : Eis) : ZMod (eisNorm σ).toNat :=
  -(σ.c : ZMod (eisNorm σ).toNat) *
    (σ.d : ZMod (eisNorm σ).toNat)⁻¹


/-- Complex sixth root exp(πi/3), fixing the positive sextic phase convention. -/
noncomputable def complexZeta6 : ℂ :=
  Complex.exp (Complex.I * ((Real.pi : ℂ) / 3))


/-- Complex sextic residue symbol from the computable exponent; zero when the residue vanishes. -/
noncomputable def complexSymbol (num den : Eis) : ℂ :=
  match symExp (residueRoot den) num with
  | none => 0
  | some k => complexZeta6 ^ k.val


/-- Actual positive-sign rational Gauss sum on representatives t from 0 to Nσ-1. -/
noncomputable def rawGauss (σ : Eis) : ℂ :=
  ∑ t ∈ Finset.range (eisNorm σ).toNat,
    complexSymbol ⟨(t : ℤ), 0⟩ σ *
      Complex.exp (2 * (Real.pi : ℂ) * Complex.I * (t : ℂ) /
        ((eisNorm σ).toNat : ℂ))


/-- Direct rational Gauss sum divided by the positive real square root of Nσ. -/
noncomputable def normalizedGauss (σ : Eis) : ℂ :=
  rawGauss σ / (Real.sqrt ((eisNorm σ).toNat : ℝ) : ℂ)


/-- A finitely supported Eisenstein-pair map to the six exponent classes ZMod 6. -/
abbrev TwistClass := Eis →₀ ZMod 6


/-- Product of complex symbols over the finite class support, preserving zero factors. -/
noncomputable def classSymbol (κ : TwistClass) (σ : Eis) : ℂ :=
  κ.support.prod (fun π => complexSymbol π σ ^ (κ π).val)


/-- Conjugate-normalised sextic Gauss vector multiplied by the class symbol. -/
noncomputable def classVector (κ : TwistClass) (σ : Eis) : ℂ :=
  star (normalizedGauss σ) * classSymbol κ σ


/-- Original finite matrix entry with row numerator ρ and column denominator σ. -/
noncomputable def residueMatrix (ρ σ : Eis) : ℂ :=
  complexSymbol ρ σ


/-- Full finite matrix-vector product over the chosen primary norm-bounded prime set. -/
noncomputable def residueMatVec (X : ℕ) (κ : TwistClass) (ρ : Eis) : ℂ :=
  ∑ σ ∈ primarySplitPrimes X, residueMatrix ρ σ * classVector κ σ


/-- Explicit witness for Lean's internal numeral elaboration at the frozen
shifted Gauss sum. This is the same trivial typeclass fact that the source
compiler generates under this exact name in Conjecture.lean. Keeping it
separate prevents the Challenge compiler from reusing rawGauss._proof_1.
The numeral's value is unchanged. -/
theorem shiftedGauss._proof_1 : Nat.AtLeastTwo (nat_lit 2) := ⟨by decide⟩

/-- Frozen positive-sign exponential sum with unreduced shift product modulo the norm. -/
noncomputable def shiftedGauss (u σ : Eis) : ℂ :=
  ∑ t ∈ Finset.range (eisNorm σ).toNat,
    complexSymbol ⟨(t : ℤ), 0⟩ σ *
      Complex.exp ((@OfNat.ofNat ℂ (nat_lit 2) (@instOfNatAtLeastTwo ℂ (nat_lit 2) Complex.instNatCast shiftedGauss._proof_1)) * (Real.pi : ℂ) * Complex.I *
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
