# Release inventory (PROTOCOL §10, stage 1): CAND-002

**Date:** 2026-10-26 (RS-S023). The Lean project is `formalisation/`, in this repository. It pins
Lean v4.35.0 and Mathlib `56a005855ea17e0b0958f73ec801ae140b0a1679` (tag v4.35.0), the same pin as
the owner's other Palomar-ready projects.

## Formalisation route

Mathlib has no power-residue symbol and no Eisenstein-integer API. It does have:

- `ZMod p`;
- multiplicative and additive characters: `MulChar`, `AddChar`, `MulChar.ofUnitHom`;
- `gaussSum`, `gaussSum_mulShift`, `gaussSum_sq` and `gaussSum_mul_gaussSum_eq_card`;
- Fermat's little theorem in finite fields;
- bounds on polynomial roots.

**The route for split primes.**

- A primary prime ρ = a + bω with N(ρ) = p ≡ 1 (mod 6) is handled through its residue field,
  identified with `ZMod p` by ω ↦ r = −a·b⁻¹.
- An element α = c + dω reduces to `res α = c + d·r`.
- The sextic exponent of x ≠ 0 is the unique k ∈ Fin 6 with x^((p−1)/6) = ζ^k, where ζ = 1 + r.

The identification ℤ[ω]/ρ ≅ 𝔽_p is stated as a modelling convention, documented in the Lean
sources and the paper, rather than proved from a Mathlib ℤ[ω]. Inert primes and composite moduli
are not needed for the CAND-002 matrix form, which uses split primes only.

## Items

Each item gives the statement, its Python test, its Lean formulation, and an effort rating.

### Group (a): exact, formalizable

**E0. The symbol is well defined.**

- **Statement:** for split p, r with r² + r + 1 = 0 and x ≠ 0 in 𝔽_p, there is a unique
  k ∈ Fin 6 with x^((p−1)/6) = (1 + r)^k.
- **Python test:** implicit in `arith.sextic_residue_exponent`, which raises if no k exists.
- **Lean:** prove (1 + r)² = r and (1 + r)³ = −1, so ζ = 1 + r has order 6. Then
  y = x^((p−1)/6) satisfies y⁶ = 1, the six powers of ζ are distinct roots of X⁶ − 1, and that
  polynomial has at most 6 roots, so y is one of them.
- **Effort:** quick to medium.

**E3. Exponents add.**

- **Statement:** res(αβ) = res α·res β, and exp(αβ) = exp α + exp β (mod 6) when both are nonzero.
- **Python test:** `test_sextic_class_exponents_match_direct_symbols`.
- **Lean:** a multiplication law on pairs (c, d) for ℤ[ω], using r² = −1 − r, then uniqueness from
  E0.
- **Effort:** quick.

**E1. Sixth-power invariance.**

- **Statement:** exp(u·v⁶) = exp u when ρ ∤ v.
- **Python test:** `test_sextic_twist_classes_sixth_powers_and_inversion`.
- **Lean:** a corollary of E3.
- **Effort:** quick.

**E2. Conjugate twist.**

- **Statement:** exp(u⁵) = −exp u (mod 6).
- **Python test:** the same.
- **Lean:** a corollary of E3.
- **Effort:** quick.

**E5. Unit twist as a character of the norm.**

- **Statement:** exp(ζ₆) = ((p − 1)/6) mod 6. For p₁, p₂ ≡ 1 (mod 6),
  (p₁p₂ − 1)/6 ≡ (p₁ − 1)/6 + (p₂ − 1)/6 (mod 6).
- **Python test:** `test_trace_normalization_factor_and_unit_twist_by_norm`.
- **Lean:** res ζ₆ = ζ, plus pure ℕ arithmetic.
- **Effort:** quick.

**E6. Normalization factor.**

- **Statement:** res(2a − b) = −b·(1 + 2r) in 𝔽_p, hence exp(2a − b) = exp(−1) + exp(√−3) +
  exp(3) + exp(b′).
- **Python test:** the same.
- **Lean:** a ring identity in `ZMod p` from r = −a/b, plus E3.
- **Effort:** quick.

**E7. Gauss-sum modulus.**

- **Statement:** |g(σ)|² = p for the sextic character χ = ζ₆^{exp(·)} and ψ(t) = e(t/p).
- **Python test:** `test_kubota_sextic_gauss_sums_and_twisted_multiplicativity`.
- **Lean:** build χ as a `MulChar (ZMod p) ℂ` via E0 and E3. χ is nontrivial because exp is
  surjective. Then apply Mathlib's `gaussSum_mul_gaussSum_eq_card` with a primitive ψ.
- **Effort:** medium.

**E4. Orientation identity.**

- **Statement:** (R w_κ)_ρ = Σ_σ conj(g̃(ρκ, σ)), using g(r, σ) = conj(χ_σ(r))·g(1, σ).
- **Python test:** the rows of `phase1n` validated against the engine.
- **Lean:** `gaussSum_mulShift`, plus the definition of R as a finite sum over an index `Finset`.
- **Effort:** medium.

**E8. Twisted multiplicativity of trace Gauss sums over composite moduli.**

- **Statement:** as stated.
- **Python test:** `test_trace_gauss_sums_twisted_multiplicativity`.
- **Lean:** needs ℤ[ω]/(c) with the Chinese remainder theorem and the trace character.
- **Effort:** hard. It is optional: CAND-002's frozen form uses prime moduli only.

**E9. Invariance of r under the −1 twist.**

- **Statement:** r_{−u} = r_u (RS-S006).
- **Lean:** the column sign pattern (−1/σ)₆ must cancel in ‖Rw‖. That needs the reciprocity
  structure.
- **Effort:** hard. Defer, or state as paper-proved.

### Group (b): proved on paper, or dependent on unformalized literature

- **L1.** The u → uv⁶ limit-invariance lemma (RS-S014). It uses the Blomer–Goldmakher–Louvel large
  sieve, with a convention-matching caveat.
- **L2.** The cubic reduction of the reciprocal sextic product (RS-S013). It needs sextic
  reciprocity, which is not in Mathlib.

### Group (c): conjectural or numerical

- **C1.** CAND-002 (1), the crossover; (2), the exponent-five law; and (3), the conditional
  corollary.
- **C2.** The open sub-questions Q-a to Q-d.
- All registered numerical outcomes (RS-S015 to RS-S021), with commit hashes.

**Formalising C1 as a Lean `Prop` (§10.2b).** The Prop must fix choices that the informal
statement leaves open:

- X ranges over ℕ, tending to infinity;
- classes are finite maps from primary primes to Fin 6 \ {0} with no exponent 5, with a bounded
  number of factors;
- uniformity is over t in a compact subset of (0, ∞);
- r₁(X)² − 1 is bounded away from 0, as a stated hypothesis;
- H_P is stated abstractly, as an asymptotic for prime first moments with some coefficient
  function c(u). It is not identified with τ₆.

### Faithfulness check (§10.2c)

- The Lean definitions are computable: primary primes, `res`, `exp`, and the exponent matrix.
- A fixture `formalisation/fixtures/sextic_200.json` holds the engine's metadata and exponent
  matrix at X = 200.
- A Lean `#eval` check compares every entry and reports any mismatch.
- This is not part of the Palomar Solution, because it uses evaluation rather than kernel proof.

## Order of formalisation

1. **RS-S023:** E0 definitions, E3, E1, E2, E5 and E6, plus the faithfulness check.
2. **RS-S024:** generic Gauss lemmas, the matrix/vector/statistic definitions, CAND-002
   `Prop`s, and an independent native/Python Gauss fixture. Full sextic `MulChar` bridge open.
2b. **RS-S025:** construct the sextic `MulChar` and primitive additive character, instantiate
    E7/E4, and settle zero shifts before claiming either exact identity complete.
3. **After full sextic bridge (not RS-S026 until proved):** the Challenge/Solution split, `comparator.json` and `formalization.yaml`, following
   `C:/Almost-Stacked-Proof/formal`. Then a local comparator run.
4. **Owner action:** make the repository public on GitHub, then submit to Palomar.
5. **Optional:** E8 and E9.

## Status (RS-S023)

**Formalised in `formalisation/ReciprocitySpectra/Sextic.lean`, no `sorry`, standard axioms only:**

- E0: `exists_exp`, `exp_unique`, `zeta_primitive`;
- E3: `res_mul`, `sexticExp_mul`, `symExp_mul`;
- E1: `sexticExp_mul_sixth_pow`;
- E2: `sexticExp_pow_five`;
- E5: `sexticExp_zeta`, `unit_exponent_additive`;
- E6: `trace_residue`.

**Faithfulness check:** 1764 of 1764 engine entries at X = 200 match. Mismatches: 0.

**Remaining:** E7, E4, the matrix and vector definitions, C1 as a `Prop`, and the Palomar packaging.

## RS-S024 checkpoint (2026-10-26)

- **E7:** `gauss_modulus_sq` is a proved theorem for any nontrivial
  multiplicative character and primitive additive character. Its sextic
  specialization is **NOT YET FORMALIZED**.
- **E4:** `gauss_shift` and the finite orientation sum are proved with
  unit shifts for generic characters. The sextic instance and zero-shift
  handling remain **OPEN**.
- **C1:** frozen CAND-002 statements (1), (2), (3) are represented as
  unproved Lean propositions. An explicit abstract H_P is not equated to
  Kubota-series theta coefficients.
- **Matrix/vectors/statistics:** explicit Lean definitions in `Model.lean`.
- **Numerical check:** native/Python at X=200, 42 Gauss entries, max
  difference 1.4983512726234129e-15 against tolerance 2e-12,
  fixture `formalisation/fixtures/sextic_gauss_200.json`. This is NOT
  a Lean `#eval` comparison of complex transcendental sums.
- **Faithfulness:** previously verified 1764/1764 exponent entries in Lean.
- **Logic note:** statement (2)'s large-`N(pi)^5/X` regime does not
  imply statement (3)'s fixed-`pi`, X→∞ limit by itself.
  Record this as a proof/statement obligation, not a refutation of
  either experimental asymptotic observation.
- **Release:** no Palomar registration, manuscript or public result claim.
  Move to full sextic character formalization in RS-S025 before packaging.

## RS-S025 checkpoint (2026-10-26)

**Proved, standard Lean axioms only:** `rationalAddChar_primitive` and
`rationalAddChar_apply` construct and certify the positive-sign canonical
additive character on `ZMod p` (`NeZero p`). This discharges the abstract
primitivity hypothesis of the future sextic E7 application, **not** the
multiplicative-character hypothesis. Cloud run 40405177673 passed both
Lean targets, printed axioms, 1764/1764 matrix fidelity, 366 Python tests,
the 42-value Gauss fixture (max ~1.5e-15), targeted Ruff and both audits.

**Open:** sextic `MulChar` with nontrivial order six, equality to the
computable exponent-based `complexSymbol` (including zero), identification
of the additive character's values with `rawGauss`'s direct exponential,
E7/E4 specialization and zero shifts. E7/E4 are still generic-only.
Next RS-S026 is another Lean bridge session: it is **not** Palomar
packaging. Packaging remains blocked until these sextic identities are
kernel checked.

**CAND-002 (3) logic audit:** (2)'s large-`N(π)^5/X` regime cannot
yield its fixed-prime conclusion. Additionally, (1)'s compact-uniform
`t>0` statement does not give a fixed-class limit at `t→0`.
The frozen conjecture remains unchanged and unproved.