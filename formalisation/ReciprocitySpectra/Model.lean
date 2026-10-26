import ReciprocitySpectra.Gauss

/-!
# Computable finite-data semantics for CAND-002

All index sets, sextic exponent lookups, matrix entries, twist vectors and
finite statistics are specified by finite operations. This is a *definition*,
not a proof of any conjectural asymptotic.

For every primary split prime σ = a + b ω, the quotient field is modelled
by ZMod (N σ), with ω ↦ -a/b. We use the root exp(π i/3) to turn the
previously verified exponents into complex symbols.
-/

namespace ReciprocitySpectra

/-- Eisenstein norm of a coordinate pair. -/
def eisNorm (x : Eis) : ℤ := x.c * x.c - x.c * x.d + x.d * x.d

/-- An atom in the frozen class family: either a primary degree-one prime or
an inert rational prime q ≡ 2 (mod 3), represented as (q,0). -/
def admissibleAtom (x : Eis) : Prop :=
  (x.c % 3 = 2 ∧ x.d % 3 = 0 ∧ (eisNorm x).toNat.Prime) ∨
  (x.d = 0 ∧ x.c > 0 ∧ x.c % 3 = 2 ∧ x.c.toNat.Prime)

/-- Deterministic norm-bounded split-prime index. The square box of radius
2X contains all points of norm at most X (a geometric inequality); the filter
enforces primarity and prime norm. -/
def primarySplitPrimes (X : ℕ) : Finset Eis :=
  (((Finset.Icc (-(2 * (X : ℤ))) (2 * (X : ℤ))).product
      (Finset.Icc (-(2 * (X : ℤ))) (2 * (X : ℤ)))).image
    (fun ab : ℤ × ℤ => Eis.mk ab.1 ab.2)).filter
      (fun x => x.c % 3 = 2 ∧ x.d % 3 = 0 ∧
        (eisNorm x).toNat.Prime ∧ (eisNorm x).toNat ≤ X)

/-- The chosen image of ω in the residue field for a primary split prime. -/
def residueRoot (σ : Eis) : ZMod (eisNorm σ).toNat :=
  -(σ.c : ZMod (eisNorm σ).toNat) *
    (σ.d : ZMod (eisNorm σ).toNat)⁻¹

/-- A complex primitive sixth root of unity. -/
noncomputable def complexZeta6 : ℂ :=
  Complex.exp (Complex.I * ((Real.pi : ℂ) / 3))

/-- Sextic symbol, interpreted in ℂ, including the zero case. -/
noncomputable def complexSymbol (num den : Eis) : ℂ :=
  match symExp (residueRoot den) num with
  | none => 0
  | some k => complexZeta6 ^ k.val

/-- The unnormalised sextic Gauss sum with rational additive character e(t/p). -/
noncomputable def rawGauss (σ : Eis) : ℂ :=
  ∑ t ∈ Finset.range (eisNorm σ).toNat,
    complexSymbol ⟨(t : ℤ), 0⟩ σ *
      Complex.exp (2 * (Real.pi : ℂ) * Complex.I * (t : ℂ) /
        ((eisNorm σ).toNat : ℂ))

/-- Rational normalisation: gtilde(σ) = g(σ) / sqrt(N σ). -/
noncomputable def normalizedGauss (σ : Eis) : ℂ :=
  rawGauss σ / (Real.sqrt ((eisNorm σ).toNat : ℝ) : ℂ)

/-- Finite formal sextic twist classes, with all exponents modulo six.
The admissibility predicate below excludes exponent zero from the support. -/
abbrev TwistClass := Eis →₀ ZMod 6

/-- The frozen exponent and support restrictions for the crossover law. -/
def admissibleSmallClass (bound : ℕ) (κ : TwistClass) : Prop :=
  κ.support.card ≤ bound ∧
    ∀ a ∈ κ.support, admissibleAtom a ∧
      ((κ a).val = 1 ∨ (κ a).val = 2 ∨ (κ a).val = 3 ∨ (κ a).val = 4)

/-- The exponent-five family consists of a single admissible prime to the fifth power. -/
def fifthClass (π : Eis) : TwistClass := Finsupp.single π (5 : ZMod 6)

/-- The sixth-power-free class norm (with exponents 1,...,5). -/
def classNorm6 (κ : TwistClass) : ℕ :=
  κ.support.prod (fun π => (eisNorm π).toNat ^ (κ π).val)

/-- The class factor product, automatically zero if a prime divides the twist. -/
noncomputable def classSymbol (κ : TwistClass) (σ : Eis) : ℂ :=
  κ.support.prod (fun π => complexSymbol π σ ^ (κ π).val)

/-- Exact finite vector w_kappa, with conjugate of the rational Gauss sum. -/
noncomputable def classVector (κ : TwistClass) (σ : Eis) : ℂ :=
  star (normalizedGauss σ) * classSymbol κ σ

/-- R_X row numerator ρ, column denominator σ, with its zero diagonal. -/
noncomputable def residueMatrix (ρ σ : Eis) : ℂ :=
  complexSymbol ρ σ

/-- The finite matrix-vector product (R_X w_kappa)_ρ. -/
noncomputable def residueMatVec (X : ℕ) (κ : TwistClass) (ρ : Eis) : ℂ :=
  ∑ σ ∈ primarySplitPrimes X, residueMatrix ρ σ * classVector κ σ

/-- Squared Euclidean norm of w_kappa over the prime columns. -/
noncomputable def vectorNormSq (X : ℕ) (κ : TwistClass) : ℝ :=
  ∑ σ ∈ primarySplitPrimes X, Complex.normSq (classVector κ σ)

/-- Squared Euclidean norm of R_X w_kappa over the prime rows. -/
noncomputable def imageNormSq (X : ℕ) (κ : TwistClass) : ℝ :=
  ∑ ρ ∈ primarySplitPrimes X, Complex.normSq (residueMatVec X κ ρ)

/-- The normalized strength; zero denominators are excluded in asymptotic
statements by separate hypotheses. -/
noncomputable def strength (X : ℕ) (κ : TwistClass) : ℝ :=
  Real.sqrt (imageNormSq X κ /
    (vectorNormSq X κ * (primarySplitPrimes X).card))

/-- The untwisted class κ = 1. -/
def unitClass : TwistClass := 0

/-- The signed relative excess, ε = (r² - 1)/(r₁² - 1). -/
noncomputable def relativeExcess (X : ℕ) (κ : TwistClass) : ℝ :=
  (strength X κ ^ 2 - 1) / (strength X unitClass ^ 2 - 1)

/-- s = ε N₆(κ)^(1/6), the frozen normalization. -/
noncomputable def scaledExcess (X : ℕ) (κ : TwistClass) : ℝ :=
  relativeExcess X κ * ((classNorm6 κ : ℝ) ^ ((1 : ℝ) / 6))

/-- t = N₆(κ) / X (X is understood positive in limit statements). -/
def aspect (X : ℕ) (κ : TwistClass) : ℝ :=
  (classNorm6 κ : ℝ) / (X : ℝ)

end ReciprocitySpectra
