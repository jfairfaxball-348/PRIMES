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

## Post-RS-S025 mathematical priority (owner, 2026-10-26)

Further Lean formalisation is **PAUSED** until the mathematical implication to
CAND-002(3) has been addressed. The rigorous abstract countermodel in
`RS_CAND002_LOGICAL_BRIDGE_AUDIT.md` shows (1)'s compact-aspect and (2)'s
large-aspect regimes, together with the normalization gap, do not imply
fixed-class limits in their own right. This is not a matrix counterexample,
and the independent abstract H_P remains unaudited as a sufficient bridge.

RS-S026 is mathematics-first: resolve whether H_P genuinely supplies the
missing endpoint control, including the raw/normalised Gauss weighting and
coefficient information, or provide a minimal separately labelled repair.
Existing verified Lean identities are retained; no new sextic E4/E7
specialization or Palomar packaging is authorized in the meantime.


## RS-S026 mathematics-first checkpoint (2026-10-27)

The mathematical proof record is `RS_S026_PRIME_MOMENT_BRIDGE.md`. It proves on paper the exact prime-row orientation, signed off-diagonal Gram expansion (with support/diagonal corrections) and a **fixed-shift** Abelian normalization lemma under the abstract H_P, with leading factor 4. The hypothesized H_P does not yet yield moving-shift uniformity or signed/averaged-square prime correlations. Neither fixed-class endpoint is proved; CAND-002(3) remains OPEN. The next unit RS-S027 stays mathematics-first. No new Lean E4/E7 specialization, release work or change to the frozen candidate is authorized by this checkpoint.

## Plan of record (owner decision, 2026-10-27)

Proof work is out of the pipeline. The Lean pause is lifted. Formalise what is exact; everything
else stays conjecture.

**(A) Lean-proved, to register on Palomar** (no `sorry`, standard axioms):

- **`Sextic.lean`:** E0 (`exists_exp`, `exp_unique`, `zeta_primitive`), E1, E2, E3, E5 and E6.
- **`Gauss.lean`** (generic characters): `gauss_modulus_sq`, `gauss_shift` and
  `finite_gauss_orientation`.
- **`CharacterBridge.lean`:** `rationalAddChar_primitive` and `rationalAddChar_apply`.

**(A′) Formalisable, still to do.** RS-S029 covers items 1–3; items 4 and 5 are optional.

1. The sextic `MulChar` χ_σ on `ZMod p`, built from `sexticExp`:
   - multiplicative, and zero at 0;
   - χ_σ ≠ 1;
   - agrees with `complexSymbol`, including zeros.
2. E7, sextic case: |`rawGauss` σ|² = p, from `gauss_modulus_sq`, `rationalAddChar_primitive` and
   `rationalAddChar_apply`.
3. E4, sextic case: `shiftedGauss u σ = conj(χ_σ(res u))·rawGauss σ` for σ ∤ u, and 0 otherwise.
   Then the row orientation identity for `residueMatVec` (RS-S026 Prop. 1).
4. Optional: the finite Gram identity for `imageNormSq` (RS-S026 Prop. 2).
5. Optional: the abstract countermodel of `RS_CAND002_LOGICAL_BRIDGE_AUDIT.md` §2 (scalar real
   analysis).

**(B) Paper-proved, not formalised** (stated in the paper with proofs and gaps):

- RS-S026 Props 1–2, if not formalised;
- RS-S027 Prop. 1 and the conductor lemma (they need sextic reciprocity, which is not in Mathlib);
- RS-S028's prime sieve, ideal Vaughan identity and trace-Gauss sign rule;
- L1 (BGL-dependent) and L2;
- the H_P scale analysis (`RS_HP_SCALE_ERRATUM.md` §3).

**(C) Conjectural or numerical:**

- CAND-002 (1) crossover, (2) exponent five and (3) fixed class, formalised as `Prop`s only;
- Q-a to Q-d;
- all registered numerical outcomes (RS-S015 to RS-S021, with commits).

**After (A′):** Palomar packaging (RS-S030), then the paper.

## RS-S029 checkpoint (2026-10-27): first sextic character bridge, kernel checked

**(A′) item 1: COMPLETE at the explicitly modelled split-prime level.**
`formalisation/ReciprocitySpectra/SexticCharacter.lean` constructs `sexticCharacter`
as a genuine `MulChar (ZMod p) ℂ` from the earlier computable
`sexticExp`, proved multiplicative and zero on nonunits. It proves
`sexticCharacter_ne_one` via the cyclic unit group and the primitive
complex sixth root, and `sexticCharacter_rational` comparing its values
with `complexSymbol ⟨n,0⟩ σ`, including zero. The `residueRoot_poly`
lemma derives r²+r+1=0 from prime norm and nonzero σ.d in `ZMod p`.
The character lemmas retain explicit hypotheses r²+r+1=0,
2≠0, 3≠0 and 6∣p−1. This is the model of a split residue field,
not a construction of the quotient ℤ[ω]/σ.

**Generic E4 extension:** `Gauss.lean` now proves
`gauss_zero_shift` and `gauss_shift_all` for any nontrivial
finite-field multiplicative character; shifts by zero have Gauss
sum exactly zero. This is kernel checked but not yet an equality
involving `Model.shiftedGauss` (that definition does not yet exist).

**(A′) items 2–3: OPEN.** No `rawGauss = gaussSum sexticCharacter
rationalAddChar` theorem, sextic `rawGauss` modulus (E7), sextic
shifted `rawGauss` formula (E4) or `residueMatVec` row identity was
proved. Generic identities must not be relabelled sextic identities.
The next unit RS-S030 tackles the actual Gauss bridge and orientation
before Palomar packaging. Group (B) and (C) statuses are unchanged.

**Validation:** GitHub Actions `40485959252`, pinned Lean 4.35.0 and
Mathlib, both `ReciprocitySpectra` and `Checks` targets PASS;
the axiom audit prints only standard axioms; exponent faithfulness
1764/1764; complete Python suite, targeted Ruff, native/Python Gauss
fixture and both evidence audit checkers PASS. The fixture is numerical
and is not a Lean theorem. Conjectural CAND-002 claims remain unproved.

## RS-S030 checkpoint (2026-10-27): group (A′) item 2 COMPLETE

**Lean, no proof placeholders:** `GaussBridge.lean` adds `zmod_sum_eq_range` (canonical finite reindexing), `rationalAddChar_nat` (positive-sign exponential at bounded rational residues), `gaussSum_sextic_eq_raw` (actual direct `rawGauss` = Mathlib `gaussSum` of the proven sextic character), and `rawGauss_modulus_sq` (sextic E7). All theorems retain explicit prime-field and sextic model hypotheses: prime norm, root equation, nonzero characteristic 2/3, and 6 | p-1. These are actual specialized results, not generic conditional character statements.

**Verification:** pinned Lean 4.35.0 / Mathlib 56a005855ea1, GitHub Actions run 40489442361 SUCCESS. Both library and Checks targets pass, and the axiom audit reports only propext, Classical.choice and Quot.sound. Faithfulness 1764/1764, 366 Python tests, 42 native/Python Gauss checks, Ruff and evidence audits pass.

**Group (A′) status:** item 1 (sextic MulChar) COMPLETE in RS-S029; item 2 (direct E7) COMPLETE in RS-S030; item 3 (specialized E4 including zero shifts and matrix row orientation) remains OPEN for RS-S031. Optional Gram, E8/E9 remain open/deferred. Palomar packaging is NOT authorized yet. Group (B) paper arguments and group (C) conjectures are unchanged; CAND-002 is unproved.


## RS-S031 checkpoint (2026-10-27): specialized sextic E4 and per-column row identity

**Lean library compiled on the pinned toolchain** for `ShiftedGauss.lean` and `RowBridge.lean`. These contain:

- `directShiftedGauss σ a`, the direct positive-sign rational exponential sum at every residue `a : ZMod (N σ)`, including zero;
- `shiftedGauss_eq_gaussSum`, exact finite reindexing to `gaussSum χ (ψ.mulShift a)`;
- `shiftedGauss_e4`, actual sextic E4, `directShiftedGauss σ a = star (χσ a) * rawGauss σ` at every residue, with zero branch, explicit prime/root/characteristic/divisibility hypotheses;
- `sexticCharacter_eis`, `sexticCharacter_class` and `rowShift_symbol`, using reductions of Eisenstein coordinate pairs and finite class products, including zero residues;
- `residueColumn_orientation`, the correct exact per-column `residueMatrix ρ σ * classVector κ σ = star (directShiftedGauss σ (rowShift κ ρ σ) / sqrt(N σ))` under the explicit split-prime assumptions.

**Precise remaining obligations:** prove that *every* `σ ∈ primarySplitPrimes X` satisfies those model hypotheses (not just assume them per column), sum the per-column theorem to obtain a theorem about the actual `residueMatVec`, and bridge the pre-existing `Conjecture.shiftedGauss (u σ : Eis)` convention (whose exponential uses a nonreduced product of rational representatives) to the new direct reduced-shift sum by exponential periodicity. The frozen conjecture definition is untouched. These are RS-S032 tasks, not completed RS-S031 theorems.

The earlier RS-S030 E7 remains proved. The group (A′) *specialized E4 and per-column orientation* is proved; the full finite `residueMatVec` claim is not yet proved, so **Palomar packaging remains gated**. Optional finite Gram, E8/E9 and paper-only group (B) remain pending. CAND-002 (1)–(3), group (C), remains conjectural. No asymptotic result is claimed. **Full validation passed:** pinned cloud workflow [40493962451](https://github.com/jfairfaxball-348/PRIMES/actions/runs/40493962451) built both Lean targets, audited only the standard three axioms, matched **1764/1764** exponent entries, passed **366** pytest tests, 42 Gauss comparisons (max 1.5e-15), targeted Ruff and both frozen-evidence audits. These do not prove the missing full finite sum.


## RS-S032 checkpoint (2026-10-27): prime membership and actual finite row sum

**Kernel-verified on the pinned runner:** `RowSum.lean` derives prime norm from every `primarySplitPrimes X` membership, proves primarity implies norm ≡ 1 (mod 3), and proves nonvanishing of the second Eisenstein coordinate modulo the prime norm by excluding a norm divisible by its square. `primarySplitPrimes_model` derives the residue-root equation, 2/3 nonvanishing and 6∣(p−1) with no extra model assumptions. `residueMatVec_orientation` is the **unconditional, actual** finite matrix-vector row sum of conjugates of reduced positive-sign direct shifted sextic Gauss sums, including zero residues, diagonal zeros and exact square-root normalisation. `ShiftConvention.lean` proves periodicity of the positive exponential and `shiftedGauss_frozen_eq_direct`, the equality of unchanged `Conjecture.shiftedGauss u σ` with reduced direct Gauss sums for **every** Eisenstein `u` (including zero) whenever p≠0.

The initial complete pinned validation is [40505888940](https://github.com/jfairfaxball-348/PRIMES/actions/runs/40505888940): both Lean targets, standard-axiom audit, 1764/1764 faithfulness, the entire Python suite, native/Python Gauss fixture, targeted Ruff and two evidence audits passed. This result predates documentation closeout, which requires a final run.

**Precisely open:** the existing `rowShift κ ρ σ` is a finite residue-class product depending on σ. Theorems do **not** identify it with reduction of one column-independent Eisenstein product `ρκ`. An attempt to construct that representative in `ClassProduct.lean` did not compile and was removed; it contributes no theorem or axiom. Consequently the already-proved finite matrix row sum and already-proved frozen shift convention cannot yet be combined into a statement using `Conjecture.shiftedGauss` with one true Eisenstein `ρκ`. This is the RS-S033 proof obligation. Group (A′) item 3: sextic E4 and actual finite `residueMatVec` orientation PROVED in the reduced model; full frozen-class representative bridge still OPEN. Do not initiate Palomar until that bridge is proved and all checks pass. Optional Gram E8/E9 and paper-only (B) remain deferred; all CAND-002 asymptotic claims are **unproved**.


## RS-S033 checkpoint (2026-10-27): group (A′) item 3 COMPLETE

Pinned cloud Lean build [40511639019](https://github.com/jfairfaxball-348/PRIMES/actions/runs/40511639019) **SUCCESS**, with no proof placeholders or
nonstandard axioms. `ClassProduct.lean` constructs a real finite
Eisenstein product `classNumerator κ : Eis` independent of the column and
proves its reduction equals `classResidue κ σ` for every split root,
including zero and all six residue exponents. The new unconditional
`residueMatVec_frozen_orientation` identifies the full finite matrix row
with the conjugated normalized sum of the **unchanged**
`Conjecture.shiftedGauss (ρ * classNumerator κ) σ`. E4, E7 and the
full finite orientation are therefore actually proved in the frozen model;
this is not an asymptotic theorem. 1764/1764 exponents, 366 tests, 42
Gauss fixture checks, Ruff and both frozen audits passed.

The release inventory's group (A′) items **1, 2 and 3 are all complete**
at the explicitly modeled finite split-prime level; the next bounded
unit is Palomar comparator/package preparation (RS-S034), after a clean
final closeout-head run and merge. Optional Gram/E8/E9 and all paper-only
and conjectural assertions remain outside this registration. CAND-002
(1)–(3) has not been proved; no Palomar entry exists yet.

## RS-S034 checkpoint (2026-10-27): first Palomar draft, NOT submission-ready

The current Palomar policy requires every submitted Lean source to use Lean's
module system, including the existing library and checks. RS-S034 added
`module`, `public import`, and an exposed public section to all 17
existing Lean source files without altering the mathematical theorem statements
or proof bodies. This migration **must be validated** in the pinned cloud run;
the RS-S033 baseline itself remains the most recent confirmed green checkpoint.

A first independent, Mathlib-only `formalisation/Challenge.lean` restates
the field-model definitions and 15 already-proved E0/E1/E2/E3/E5/E6 and
generic E4/E7 identities. `Solution.lean` imports the genuine pinned proof
library; `comparator.json` selects those 15 declarations. This Challenge
does **not** yet select the more substantial sextic `rawGauss_modulus_sq`,
`shiftedGauss_e4` or `residueMatVec_frozen_orientation` declarations.
Do not describe this initial comparator as complete E0–E7 certification, nor
assume that successful compilation is the independent Comparator check.

The root repository now has Apache-2.0 `LICENSE` and metadata draft
`formalisation/formalization.yaml`. Its `automation.methods` is
**deliberately left empty pending the owner's disclosure**, which makes the
metadata invalid for Palomar submission. AI-assisted work is known to have
occurred; no claim of “no AI used” has been made. Until the owner supplies an
accurate declaration and the full package validates in pinned Comparator and
NanoDa, **do not submit or claim a Palomar ID**. CAND-002 remains conjectural.

**RS-S034 pinned-cloud result:** Pinned cloud validation run [40516664832](https://github.com/jfairfaxball-348/PRIMES/actions/runs/40516664832) on code head `42d0607727aca68ad973da3903d845b0b949fa02` passed: library, Checks, Challenge, Solution built (all three Lean exit codes 0), the existing standard-axiom audit and exponent faithfulness ran, full pytest 366 passed, 42 Gauss comparison max error 1.5e-15, targeted Ruff and both frozen evidence audits passed. An earlier run failed because module visibility omitted native IR for `symExp` used by the faithfulness `#eval`; this was fixed using `import all ReciprocitySpectra.Sextic` and `import all Checks.Fixture200` in Checks/Faithfulness. This cloud validation does NOT run leanprover/comparator or NanoDa and does not make the metadata submission-valid.


## RS-S035: independent exact-theorem comparator coverage (work in progress)

The proof inventory does not change its mathematical classification: group
(A) and exact (A′) items 1–3 remain Lean-proved in the finite model;
optional E8/E9/Gram and CAND-002's asymptotic (1)–(3) remain outside the
claimed proofs. The first Palomar draft compared 15 generic/elementary
theorems. RS-S035 extends the independent Mathlib-only Challenge to 26
theorems including `gaussSum_sextic_eq_raw`,
`rawGauss_modulus_sq` (specialised E7), `shiftedGauss_e4`
(specialised E4 including zero), `classNumerator_reduction`,
`rowShift_eisenstein`, and `residueMatVec_frozen_orientation`.
No theorem statement or proof in the existing library is edited.

**Crucial comparator incident:** run 40520302610 failed on the
statement for `res_mul` even though Lake compiled the proof library and
Challenge/Solution: Challenge had erroneously placed `res_mul` inside
`[Fact p.Prime]` scope whereas the original source theorem has no such
assumption. RS-S035 removed this extra binder. Subsequent true Comparator
and NanoDa results, not merely source-text comparison or Lake builds, are
required before merging or claiming a verified Palomar package.

The root Apache-2.0 licence remains selected. `automation.methods`
is intentionally empty pending the owner's truthful AI-use declaration;
there is no assertion of no AI use. No submission or registry ID.

**RS-S035 completed checkpoint (2026-10-27):** The scope now compares 26
finite theorem statements, adding source-verified `sexticValue_one` and
`sexticValue_mul` as needed for the actual sextic MulChar definition.
Pinned cloud run **40522609418 PASS** on code commit `e15e314`.
Independent comparator **40522609498 FAIL**: `ReciprocitySpectra.shiftedGauss`
source-definition mismatch (a named unchanged frozen operation, not a
mathematical counterexample). Earlier Comparator errors corrected in the
branch: `res_mul` type, `Eis.instCommMonoid._proof_6` dependency, and
`sexticValue_zero` missing simplifier. Actual independent acceptance is NOT
proved; branch PR #14 remains unmerged. Next RS-S036 diagnoses exported
constant/implicit elaboration fidelity without touching frozen library claims.

**RS-S036 (2026-10-27) generated-constant fidelity checkpoint:** in unmerged draft PR #15 (stacked on #14), pinned Lean `#print` established that the literal positive-sign `shiftedGauss` Challenge and source had only a generated numeral proof-name difference. An explicit raw-literal witness corrected the *entire* exported `shiftedGauss` definition (40528521143: **zero printed differences**) but Comparator next rejected `ReciprocitySpectra.shiftedGauss._proof_1`. Code head `12b904b` is testing the exact raw-Nat class type; no Comparator/NanoDa acceptance yet. Experimental separate ChallengePrefix module was removed: Palomar forbids project-specific Challenge transitive imports. Original 26 proof-library statements, CAND-002 conjectures, Apache-2.0 licence and deferred AI-use declaration unchanged. **No merge or submission.** See `LEDGER.md` RS-S036.

**RS-S036 failed-closeout recovery (2026-10-27):** comparator #44 and cloud #133 originally failed to compile a Challenge-only raw-numeral witness (`omega` at line 228), not an established mathematical theorem. The repair now compiles and scoped cloud validation is green at [40534020351](https://github.com/jfairfaxball-348/PRIMES/actions/runs/40534020351); independent Comparator [40534020098](https://github.com/jfairfaxball-348/PRIMES/actions/runs/40534020098) has passed the original `shiftedGauss` witness mismatch and found its *next* exact-source mismatch at `sexticCharacter`, involving autogenerated `_proof_2/_proof_3` names. The required 26 statement surface is unchanged; no independent acceptance or Palomar ID. Root Apache-2.0 and owner-pending AI declaration unchanged. The final diagnostic run at code head `43c5ff5` must be checked in RS-S037. See `LEDGER.md` for full evidence.


## RS-S037 exported-definition fidelity checkpoint (2026-10-27)

The exact 26 selected formalized finite statements are unchanged. Pinned scoped suite [40542225221](https://github.com/jfairfaxball-348/PRIMES/actions/runs/40542225221) passed at `418c825` (Lean library/Checks/Challenge/Solution, 1764/1764 faithful exponents, 366 tests, 42 Gauss entries, Ruff and audits). Independent Comparator [40542225202](https://github.com/jfairfaxball-348/PRIMES/actions/runs/40542225202) confirmed that the strict `sexticCharacter` generated-witness mismatch is **resolved** and proceeded to a fresh mismatch at `directShiftedGauss`. This is **not** a completed 26-theorem/NanoDa verification. Source proofs are untouched; CAND-002's asymptotics remain conjectural. Stacked PRs #14–#16 are unmerged and metadata's owner-reviewed AI disclosure is still pending. See `LEDGER.md` and the single RS-S038 prompt.

## RS-S038 strict exported-direct fidelity checkpoint (2026-10-27)

In stacked draft PR [#17](https://github.com/jfairfaxball-348/PRIMES/pull/17), the source and independent Mathlib-only Challenge now export identical `ReciprocitySpectra.directShiftedGauss` types and values (zero full `pp.all` diff lines) and identical `directShiftedGauss._proof_1` witness type/value. This was a generated numeral witness reference mismatch, not a change to the finite Gauss sum. Scoped cloud [40555785210](https://github.com/jfairfaxball-348/PRIMES/actions/runs/40555785210) **SUCCESS** at `62091106`; true Comparator/NanoDa [40555785331](https://github.com/jfairfaxball-348/PRIMES/actions/runs/40555785331) **FAILED NEXT** at `ReciprocitySpectra.rationalAddChar`. The 26 theorem statements/proofs remain unchanged; whole-package acceptance, Palomar registration, and the automation disclosure are still pending. Keep #14–#17 unmerged. Next bounded unit RS-S039: strict exported additive-character fidelity.


## RS-S039 (2026-10-27): complete finite-package independent verification

On code head 4cb25de8, the independent 26-theorem leanprover/Comparator+lean4export+Landrun+NanoDa passed (run 40564457111) with BOTH NanoDa and default Lean kernel accepting the solution. Challenge rationalAddChar, rationalAddChar._proof_1 and rationalAddChar._proof_2 match the proof source full exported pp.all types and bodies byte-for-byte. The 26 original theorem statements, specialized sextic E4/E7 and actual full finite row theorem are unchanged. Full scoped cloud passed at same head (40564457029). Final docs-head verification and ordered PR merges still required. Metadata automation.methods [] deliberately awaits truthful owner AI declaration. No Palomar ID and CAND-002 asymptotics remain conjectural.


## RS-S040 Palomar live-policy preflight (2026-10-27)

See [RS-S040 preflight](RS_S040_PALOMAR_PREFLIGHT.md) for the exact nested-project paths,
26-theorem coverage, source-size and metadata audits, root licence, and the required
owner-invoked intake sequence. Independent Comparator/NanoDa and scoped cloud both passed
at the owner AI-disclosure main `ff6ef1742582a9acddefe4ab56203b16c30d4ed4` (runs 40569785577 and 40569785692).
The 515-line Challenge triggers a Palomar readability warning, not the 1,000-line hard cap.
Added the policy-requested theorem-level informal account to `formalisation/README.md`.
No mathematical source or proof was edited, no registration was made, and the final documentation
merge SHA still requires independent/scoped green workflows before intake. CAND-002 asymptotics
remain unproved. The declaration of substantial OpenAI ChatGPT assistance and root Apache-2.0
licence are retained.
