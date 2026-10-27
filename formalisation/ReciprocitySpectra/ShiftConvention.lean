import ReciprocitySpectra.Conjecture
import ReciprocitySpectra.ShiftedGauss

/-!
# RS-S032: positive-sign exponential periodicity

The frozen conjecture's shift multiplies *unreduced* natural representatives,
whereas the direct shifted Gauss sum reduces the product before exponentiating.
The two conventions are exactly equal for every shift (including zero).
No modification is made to the frozen Conjecture.shiftedGauss definition.
-/

namespace ReciprocitySpectra

/-- The positive-sign additive exponential is periodic on integer arguments
modulo p. This is an exact complex identity, not floating-point evidence. -/
theorem positiveExp_mod (p : ℕ) [NeZero p] (n : ℕ) :
    Complex.exp (2 * (Real.pi : ℂ) * Complex.I * (n : ℂ) / (p : ℂ)) =
      Complex.exp (2 * (Real.pi : ℂ) * Complex.I *
        ((n % p : ℕ) : ℂ) / (p : ℂ)) := by
  let ζ : ℂ := Complex.exp (2 * (Real.pi : ℂ) * Complex.I / (p : ℂ))
  have hζ : ζ ^ p = 1 :=
    (Complex.isPrimitiveRoot_exp p (NeZero.out)).pow_eq_one
  have hmod (m : ℕ) : ζ ^ m = ζ ^ (m % p) := by
    conv_lhs => rw [← Nat.div_add_mod m p, pow_add, pow_mul, hζ, one_pow, one_mul]
  have hexp (m : ℕ) :
      Complex.exp (2 * (Real.pi : ℂ) * Complex.I * (m : ℂ) / (p : ℂ)) =
        ζ ^ m := by
    dsimp [ζ]
    rw [← Complex.exp_nat_mul]
    congr 1
    push_cast
    ring
  rw [hexp n, hexp (n % p)]
  exact hmod n

/-- Exact equality of the two **unchanged** direct finite sums for every
Eisenstein shift, with no prime/character hypotheses beyond nonzero modulus. -/
theorem shiftedGauss_frozen_eq_direct (u σ : Eis)
    [NeZero (eisNorm σ).toNat] :
    shiftedGauss u σ =
      directShiftedGauss σ (res (residueRoot σ) u) := by
  let p := (eisNorm σ).toNat
  let a : ZMod p := res (residueRoot σ) u
  have hval (t : ℕ) :
      (a * (t : ZMod p)).val = (a.val * t) % p := by
    have hcast : a * (t : ZMod p) = ((a.val * t : ℕ) : ZMod p) := by
      simpa only [Nat.cast_mul, ZMod.natCast_zmod_val]
    rw [hcast, ZMod.val_natCast]
  unfold shiftedGauss directShiftedGauss
  apply Finset.sum_congr rfl
  intro t ht
  congr 1
  change
    Complex.exp (2 * (Real.pi : ℂ) * Complex.I * (a.val : ℂ) *
        (t : ℂ) / (p : ℂ)) =
      Complex.exp (2 * (Real.pi : ℂ) * Complex.I *
        ((a * (t : ZMod p)).val : ℂ) / (p : ℂ))
  calc
    Complex.exp (2 * (Real.pi : ℂ) * Complex.I * (a.val : ℂ) *
        (t : ℂ) / (p : ℂ)) =
      Complex.exp (2 * (Real.pi : ℂ) * Complex.I *
        ((a.val * t : ℕ) : ℂ) / (p : ℂ)) := by
          congr 1
          push_cast
          ring
    _ = Complex.exp (2 * (Real.pi : ℂ) * Complex.I *
        (((a.val * t) % p : ℕ) : ℂ) / (p : ℂ)) :=
      positiveExp_mod p (a.val * t)
    _ = Complex.exp (2 * (Real.pi : ℂ) * Complex.I *
        ((a * (t : ZMod p)).val : ℂ) / (p : ℂ)) := by rw [hval]

end ReciprocitySpectra
