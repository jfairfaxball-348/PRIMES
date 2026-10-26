import ReciprocitySpectra.Model

/-!
# RS-S025: the rational additive-character bridge

The character uses the positive exponential sign: psi(t) = exp(2*pi*i*t/p).
The root of unity is fixed independently of the sextic multiplicative character.
The latter is still an outstanding proof obligation.
-/

namespace ReciprocitySpectra

/-- The rational additive character with the *positive* Fourier sign. -/
noncomputable def rationalAddChar (p : ℕ) [NeZero p] : AddChar (ZMod p) ℂ :=
  AddChar.zmodChar p (Complex.isPrimitiveRoot_exp p (NeZero.out)).pow_eq_one

/-- No primitivity assumption is left as an unproved hypothesis. -/
theorem rationalAddChar_primitive (p : ℕ) [NeZero p] :
    (rationalAddChar p).IsPrimitive := by
  unfold rationalAddChar
  exact AddChar.zmodChar_primitive_of_primitive_root
    (Complex.isPrimitiveRoot_exp p (NeZero.out))

/-- Exact character values at the canonical representatives 0,...,p-1. -/
theorem rationalAddChar_apply (p : ℕ) [NeZero p] (t : ZMod p) :
    rationalAddChar p t =
      Complex.exp (2 * (Real.pi : ℂ) * Complex.I / (p : ℂ)) ^ t.val := by
  exact AddChar.zmodChar_apply
    (Complex.isPrimitiveRoot_exp p (NeZero.out)).pow_eq_one t

end ReciprocitySpectra
