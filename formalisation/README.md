# Reciprocity Spectra: Lean formalisation

## Palomar reader's guide: exactly 26 finite compared statements (RS-S040)

The externally auditable `Challenge.lean` repeats the finite definitions and states the 26
selected results; `Solution.lean` imports the proved library. Each item below is a plain-language
account of the precise **finite** theorem listed by `comparator.json`, not an additional claim
or an assertion of novelty. The displayed hypotheses in `Challenge.lean` are authoritative.

| # | Selected declaration | Mathematical content and scope |
|---:|---|---|
| 1 | `ReciprocitySpectra.res_mul` | Reduction of Eisenstein-coordinate multiplication to `ZMod p` preserves products, assuming the stated Eisenstein root equation. |
| 2 | `ReciprocitySpectra.zeta_primitive` | `1+r` is a primitive sixth root for the stated prime-field and characteristic hypotheses. |
| 3 | `ReciprocitySpectra.exists_exp` | Every nonzero residue has a sixth-root exponent for the Euler sextic power when six divides `p−1`. |
| 4 | `ReciprocitySpectra.exp_unique` | The exponent between zero and five for a power of that primitive sixth root is unique. |
| 5 | `ReciprocitySpectra.sexticExp_mul` | Nonzero sextic residue exponents add modulo six on multiplication. |
| 6 | `ReciprocitySpectra.symExp_mul` | The corresponding exponent-addition law holds for Eisenstein-coordinate representatives. |
| 7 | `ReciprocitySpectra.sexticExp_mul_sixth_pow` | Multiplication by a nonzero sixth power does not change the sextic exponent. |
| 8 | `ReciprocitySpectra.sexticExp_pow_five` | Taking the fifth power negates the sextic exponent modulo six. |
| 9 | `ReciprocitySpectra.sexticExp_zeta` | The chosen sixth root has the residue exponent `(p−1)/6` modulo six. |
| 10 | `ReciprocitySpectra.unit_exponent_additive` | Unit exponents associated with integers of the form `6m+1` add modulo six under multiplication. |
| 11 | `ReciprocitySpectra.trace_residue` | An exact residue-field trace normalisation identity holds when `br=−a`. |
| 12 | `ReciprocitySpectra.gauss_modulus_sq` | A generic nontrivial multiplicative character and primitive additive character yield a Gauss sum with squared modulus equal to the finite-field cardinality. |
| 13 | `ReciprocitySpectra.gauss_shift` | Shifting the additive character by a unit multiplies its Gauss sum by the inverse multiplicative character value. |
| 14 | `ReciprocitySpectra.gauss_zero_shift` | The zero additive shift gives zero Gauss sum when the multiplicative character is nontrivial. |
| 15 | `ReciprocitySpectra.gauss_shift_all` | One piecewise formula combines the generic nonzero-shift and zero-shift cases. |
| 16 | `ReciprocitySpectra.sexticCharacter_apply` | The constructed specialised sextic multiplicative character evaluates to the exponent-defined complex sextic value on every field residue. |
| 17 | `ReciprocitySpectra.sexticCharacter_ne_one` | Under the split-prime/root hypotheses, the specialised sextic multiplicative character is nontrivial. |
| 18 | `ReciprocitySpectra.gaussSum_sextic_eq_raw` | The specialised sextic Gauss sum using the canonical positive-sign additive character equals the directly defined finite sum `rawGauss`. |
| 19 | `ReciprocitySpectra.rawGauss_modulus_sq` | The specialised sextic direct Gauss sum has squared modulus equal to the prime norm under the required prime/root/six-divisibility hypotheses. |
| 20 | `ReciprocitySpectra.shiftedGauss_eq_gaussSum` | The direct shifted sextic sum equals the library Gauss sum formed with the shifted additive character, for every shift. |
| 21 | `ReciprocitySpectra.shiftedGauss_e4` | The direct shifted sextic sum equals the conjugate sextic character at the shift times the unshifted sum, including the zero-shift case. |
| 22 | `ReciprocitySpectra.classNumerator_reduction` | Reduction of the finite Eisenstein class numerator agrees with the class-residue definition. |
| 23 | `ReciprocitySpectra.rowShift_eisenstein` | The row shift is the reduced Eisenstein product of the row representative with the class numerator. |
| 24 | `ReciprocitySpectra.residueMatVec_frozen_orientation` | The frozen finite residue-matrix/vector row is exactly the sum of conjugated normalized shifted Gauss sums over its indexed split primes. |
| 25 | `ReciprocitySpectra.sexticValue_one` | The exponent-defined complex sextic residue value at one is one. |
| 26 | `ReciprocitySpectra.sexticValue_mul` | The exponent-defined complex sextic residue value is multiplicative under the stated root and divisibility assumptions. |

**Scope and known gaps.** The Eisenstein-coordinate ring is modelled using pairs of integers,
with an explicitly chosen residue root in `ZMod p`, rather than a construction of the
quotient ℤ[ω]/ρ inside Mathlib. Prime characteristic, the Eisenstein root equation,
nonzero characteristic-two/three conditions, and divisibility by six are used only where
shown in the formal statements; generic Gauss lemmas have their own character hypotheses.
The matrix-row result is an exact **finite definitional identity**, not a spectral or
asymptotic theorem. CAND-002(1), (2), (3) are stated without proofs and are **not** selected
by Comparator. The statement-level `by sorry` placeholders in the independent Challenge
are replaced by proofs from the Solution during Comparator verification; there are no
admitted theorems in the proved library or Solution. This package is not a claim that
Palomar has registered, endorsed, or reviewed the mathematics.

For the policy and reproducible submission preflight, see
[`reciprocity_spectra/RS_S040_PALOMAR_PREFLIGHT.md`](../reciprocity_spectra/RS_S040_PALOMAR_PREFLIGHT.md).

Lean 4 (v4.35.0) and Mathlib (`56a005855ea1`, tag v4.35.0) formalisation of the exact identities
behind CAND-002. See `../reciprocity_spectra/RELEASE_INVENTORY.md` and PROTOCOL §10. The conjecture
itself is stated, not proved.

## Build

### Fresh clone or cloud session

Use the same method as Almost-Stacked-Proof `formal/`:

```bash
bash formalisation/cloud_setup.sh
```

The script:

- installs elan if needed (the toolchain is pinned by `lean-toolchain`);
- runs `lake exe cache get`, which fetches prebuilt Mathlib oleans for the pinned commit (several
  GB);
- builds the library and the checks.

`.lake/` is never committed.

### Local (owner's Windows machine)

The Mathlib packages are already in `formalisation/.lake`. Add `~/.elan/bin` to `PATH`, then build:

```bash
lake build ReciprocitySpectra
```

```bash
lake build Checks
```

- `ReciprocitySpectra` is the library.
- `Checks` runs the axiom audit and the faithfulness check against the numerical engine.

## Contents

`ReciprocitySpectra/Sextic.lean` covers split primes of ℤ[ω] through `ZMod p`, with ω ↦ r and
r² + r + 1 = 0.

| Item | Theorem(s) |
|---|---|
| E0: the symbol is well defined | `exists_exp`, `exp_unique`, `zeta_primitive` |
| E3: exponents add | `res_mul`, `sexticExp_mul`, `symExp_mul` |
| E1: sixth-power invariance | `sexticExp_mul_sixth_pow` |
| E2: the fifth power gives the conjugate exponent | `sexticExp_pow_five` |
| E5: unit twist and norm arithmetic | `sexticExp_zeta`, `unit_exponent_additive` |
| E6: Tr ρ ≡ −b√−3 mod ρ | `trace_residue` |

**Checks.**

- `Checks/Faithfulness.lean` recomputes all 1764 entries of the engine's exponent matrix at
  X = 200 (`fixtures/sextic_200.json`). Mismatches: 0.
- `Checks/Axioms.lean` confirms the theorems use only `propext`, `Classical.choice` and
  `Quot.sound`.

**Modelling convention.** The residue field ℤ[ω]/ρ is identified with `ZMod p` via ω ↦ r = −a/b. This
is stated, not derived from a Mathlib ℤ[ω].

## RS-S024 cloud checkpoint (partial, validated)

- `ReciprocitySpectra/Gauss.lean`: the conditional character-level Gauss
  modulus identity, multiplicative shift, and finite orientation sum are
  **proved** using Mathlib. The hypotheses `χ ≠ 1` and primitive `ψ`
  have **not** been discharged for the sextic exponent character.
- `ReciprocitySpectra/Model.lean`: finite primary split-prime index,
  sextic-symbol matrix, twist classes/vectors and normalized statistics.
  These are definitions, not asymptotic theorems.
- `ReciprocitySpectra/Conjecture.lean`: CAND-002 (1), (2) and conditional
  (3) are stated as Lean `Prop`s, with denominator/quantifier choices
  documented. None is proved.
- `fixtures/sextic_gauss_200.json`: 42 complex double Gauss values from the
  C engine; `python -m reciprocity_spectra.scripts.rs_s024_gauss_check --check`
  verifies these and an independent Python computation to absolute
  tolerance 2e-12 (observed max 1.4983512726234129e-15).
  These complex exponential values are NOT evaluated by Lean.
- `Checks/Axioms.lean` audits all proved Gauss identities and the
  original sextic exponent lemmas. The 1764/1764 exponent check remains.
- `.github/workflows/rs_s024_cloud.yml` installs the pinned Mathlib
  cache and validates the Lean, Python and audit targets on GitHub runners.

**Former RS-S025 target (only partially reached):** construct and prove the actual sextic
`MulChar (ZMod p) ℂ` (including order 6), connect to the primitive
additive character, instantiate E7/E4 including zero shifts.
Do not proceed to Palomar packaging as though that bridge were complete.

**Important logic gap:** CAND-002 (2) handles N(π)^5/X large but (3)
asks for a fixed π while X→∞, making N(π)^5/X→0. A separate
argument or corrected statement is required. No frozen claim was edited.

## RS-S025 cloud checkpoint (validated, partial)

`ReciprocitySpectra/CharacterBridge.lean` now defines
`rationalAddChar p`, the positive-sign rational additive character on
`ZMod p`, and proves `rationalAddChar_primitive` and
`rationalAddChar_apply`. `ReciprocitySpectra.lean` imports it and
`Checks/Axioms.lean` audits the two new theorems. Neither has a `sorry`
or a nonstandard axiom.

**Cloud success:** https://github.com/jfairfaxball-348/PRIMES/actions/runs/40405177673:
Lean library and Checks, 1764/1764 exponent entries, 366 Python tests,
targeted Ruff, X=200 42 Gauss comparisons (max ~1.5e-15), and both
historical evidence audit scripts. The unrelated global Ruff CI still
fails on protected D1 files.

**Not yet proved:** construct the sextic `MulChar` from `sexticExp`,
prove its order-six/nontriviality and value equality to `complexSymbol`,
identify the full `gaussSum` with `rawGauss`, prove sextic E7 and E4
including zero shifts and row/column orientation. Generic E4/E7 from
RS-S024 must not be advertised as sextic E4/E7.

**Next RS-S026:** finish the character-level sextic bridge and
specializations. No Challenge/Solution split or Palomar submission yet.

**Formal conjecture limitation:** CAND-002 is still unproved and frozen.
Its large-t exponent-five condition and its compact-t crossover do
not directly imply fixed-class X→∞ behaviour where t→0; additional
arguments would be needed for the conditional fixed-class statement.

## Owner priority switch (2026-10-26): mathematics first

**No new Lean until the CAND-002 mathematical implication gap is resolved.**
Existing kernel-checked lemmas and their validation are retained. The next
session RS-S026, previously planned for the sextic `MulChar` bridge, is now a
prime-level/matrix-level mathematical proof/repair session. See
`../reciprocity_spectra/RS_CAND002_LOGICAL_BRIDGE_AUDIT.md` for the
abstract countermodel, boundary-uniformity issue and H_P obligations.
That countermodel does not refute the actual residue matrix or H_P.
Palomar packaging is on hold.

## Plan of record (2026-10-27)

- Proof work is out of the pipeline, and the Lean pause is lifted.
- `Conjecture.lean` now packages `CAND002 = CAND002_Crossover ∧ CAND002_Fifth ∧
  CAND002_FixedClass`. (3) is a standalone conjecture.
- The H_P-conditional form is kept outside the package. H_P is stated at the corrected normalised
  scale; see `RS_HP_SCALE_ERRATUM.md`.
- **Next (RS-S029):** the sextic `MulChar` built from `sexticExp`, E7 and E4 in the sextic case, and
  the row orientation identity. Then Palomar packaging (RS-S030).
- The full list is in `../reciprocity_spectra/RELEASE_INVENTORY.md`, "Plan of record".

## RS-S029 checkpoint (2026-10-27): character, root and zero shift

The new `ReciprocitySpectra/SexticCharacter.lean` builds the
actual `sexticCharacter` from `sexticExp`. It proves multiplicativity,
`sexticCharacter_ne_one`, matching `complexSymbol` on rational residues
(including zero), and `residueRoot_poly` assuming prime norm and
the second coordinate is nonzero in the residue field. The
`Gauss.lean` lemmas `gauss_zero_shift` and `gauss_shift_all`
handle the zero case for arbitrary nontrivial characters.

All new theorems are printed in `Checks/Axioms.lean`. Cloud validation
run [40485959252](https://github.com/jfairfaxball-348/PRIMES/actions/runs/40485959252)
passed the pinned build, axiom audit, 1764/1764 exponent check,
full pytest, Ruff, 42 Gauss fixture comparisons and both audits.

**Still missing:** identify the direct `rawGauss` finite range sum
with `gaussSum` on `ZMod p` using the positive additive-character
convention; specialize E7; connect shifted Gauss sums and handle zeros;
prove the `residueMatVec` row orientation. These are RS-S030 tasks.
No Palomar comparator or submission was prepared.

## RS-S030 checkpoint (2026-10-27): direct Gauss bridge and sextic E7

`ReciprocitySpectra/GaussBridge.lean` proves four exact identities, without new axioms:

- `zmod_sum_eq_range`: bijective finite reindexing between `ZMod p` and `Finset.range p`;
- `rationalAddChar_nat`: canonical positive additive character equals the direct exponential on each bounded representative;
- `gaussSum_sextic_eq_raw`: actual rational sextic `rawGauss` equals Mathlib `gaussSum` for the exponent-defined `sexticCharacter`, with explicit model assumptions;
- `rawGauss_modulus_sq`: specialized E7, `rawGauss σ * star (rawGauss σ) = Nσ` over ℂ.

All four are imported by `ReciprocitySpectra.lean` and audited in `Checks/Axioms.lean`. GitHub Actions [40489442361](https://github.com/jfairfaxball-348/PRIMES/actions/runs/40489442361) passed both Lean targets (standard axioms only), 1764/1764 faithfulness, the 42-Gauss native/Python comparison, 366 tests, Ruff and the historical evidence audits.

**Remaining (RS-S031):** direct shifted Gauss-sum E4 for all residues including zero, and the exact finite `residueMatVec` row-orientation identity with per-class products/conjugation/normalisation. No Palomar comparator or submission yet. CAND-002 remains an unproved conjecture.


## RS-S031 checkpoint (2026-10-27): shifted sextic E4 and per-column orientation

- `ReciprocitySpectra/ShiftedGauss.lean`: defines `directShiftedGauss σ a` on the full finite residue field (including zero), checks the positive exponential sign by finite reindexing into Mathlib `gaussSum`, proves specialized sextic E4 using the actual nontrivial `sexticCharacter`, and proves equality of the character with `complexSymbol α σ` at every Eisenstein residue.
- `ReciprocitySpectra/RowBridge.lean`: defines the finite class-residue product and the row shift; proves character compatibility across support and the correct *per-column* matrix orientation with conjugation and square-root denominator. All theorems retain explicit split-prime field/root assumptions.
- `Checks/Axioms.lean` imports `RowBridge` and audits the new theorems. Library Lean compilation succeeded on the pinned runner; GitHub Actions [40493962451](https://github.com/jfairfaxball-348/PRIMES/actions/runs/40493962451) passed the pinned library and Checks builds; all audited new theorems use only propext, Classical.choice and Quot.sound. Faithfulness 1764/1764, 366 tests, 42 Gauss comparisons, targeted Ruff and evidence audits passed.

**Not yet claimed:** the all-column sum over `primarySplitPrimes X` (requires membership-to-hypothesis lemmas), and identification of the pre-existing `Conjecture.shiftedGauss (u σ : Eis)` with `directShiftedGauss σ (res (residueRoot σ) u)` (requires an exponential-periodicity calculation for reduced and unreduced products). No conjecture `Prop` was altered and no Palomar package is authorized yet. RS-S032 should close these exact finite bridges before registration.


## RS-S032 (2026-10-27): full finite row sum and exponential convention

- `RowSum.lean`: `primarySplitPrimes_prime`, `primary_norm_mod_three`, `primeNorm_d_ne_zero`, `primarySplitPrimes_model` discharge the exact per-column hypotheses from finite prime-index membership, including the characteristic and residue-root conditions. `residueMatVec_orientation_of` is an intermediate conditional summation; **`residueMatVec_orientation` has no extra arithmetic premises**, proving the genuine finite matrix row sum with zero factors and normalized conjugation.
- `ShiftConvention.lean`: `positiveExp_mod` and `shiftedGauss_frozen_eq_direct` prove the unchanged `Conjecture.shiftedGauss` exponential convention agrees with the reduced direct sum for any Eisenstein shift (including zero). The frozen conjecture file was not edited.
- All eight new theorem names are in `Checks/Axioms.lean`; pinned library+Checks validation [40505888940](https://github.com/jfairfaxball-348/PRIMES/actions/runs/40505888940) passed, as did 1764/1764 exponents, 366 pytest tests, 42 Gauss checks, Ruff and both evidence audits. A final documentation-head run must also pass before merge.
- **Open:** a column-independent Eisenstein representative for a general finite `TwistClass`, with a proof that reducing it equals `classResidue` for each column. The uncompiled attempt was removed; no representative identification is claimed. Therefore `residueMatVec_orientation` is presently expressed through the exact **residue-field** `rowShift`, not one frozen `shiftedGauss` of an Eisenstein product. This is RS-S033; Palomar is gated. Gram identity optional. CAND-002 unchanged and conjectural.


## RS-S033 (2026-10-27): exact Eisenstein class product and frozen row sum

`ReciprocitySpectra/ClassProduct.lean` now supplies the genuine coordinate-pair
Eisenstein `CommMonoid`, finite class numerator
`classNumerator κ := ∏ a ∈ κ.support, a ^ (κ a).val`,
`res_one`, `res_pow_eis`, `res_prod_eis`,
`classNumerator_reduction` and `rowShift_eisenstein`. The last theorem
identifies the column-dependent reduced row shift with reduction of the
**one actual** Eisenstein integer `ρ * classNumerator κ`.

`residueMatVec_frozen_orientation` then proves the full, unconditional
finite matrix row identity using the literal **unchanged**
`Conjecture.shiftedGauss` and the exact conjugation/sqrt norm. This
retains all zero cases and every class exponent. The code-checkpoint
pinned Actions run [40511639019](https://github.com/jfairfaxball-348/PRIMES/actions/runs/40511639019) passed both Lean builds, standard-axiom audit,
1764/1764 exponent faithfulness, 366 Python tests, 42 Gauss values,
Ruff and frozen audits. The new result is **finite algebra**, not
the asymptotic CAND-002 conjecture. After a successful closeout-head
validation and merge, RS-S034 should prepare a Palomar Challenge/Solution
and `formalization.yaml` for proved identities only. Optional Gram
and CAND-002 proof remain out of the release pipeline.

## RS-S034 Palomar staging — NOT YET ACCEPTED

The Palomar policy now requires `module`-format Lean for **every** submitted
source, including library and Checks. RS-S034's source-only migration wraps
all 17 existing Lean files in public module scope and retains all existing
theorem statements and proof terms. Run the pinned cloud action and repair
any visibility regressions before describing the migration as validated.

The initial statement surface is `Challenge.lean` (Mathlib-only,
intentional `sorry` on compared theorem statements); `Solution.lean`
exposes the corresponding proven declarations from the existing library.
`comparator.json` currently covers 15 exact sextic/character lemmas, NOT
the specialised E7/E4 or the full frozen finite matrix row identity. The
challenge intentionally does not import the proof library. Compilation is
necessary but **not** a successful Comparator or NanoDa result.

`formalization.yaml` is a **draft**: `automation.methods` is deliberately
empty pending owner review; it does not assert “no AI used” and does not pass
Palomar's nonempty automation requirement. The root `../LICENSE` is
Apache-2.0, as directed. No Palomar submission is authorised at this stage.

**RS-S034 code-head green:** Pinned cloud validation run [40516664832](https://github.com/jfairfaxball-348/PRIMES/actions/runs/40516664832) on code head `42d0607727aca68ad973da3903d845b0b949fa02` passed: library, Checks, Challenge, Solution built (all three Lean exit codes 0), the existing standard-axiom audit and exponent faithfulness ran, full pytest 366 passed, 42 Gauss comparison max error 1.5e-15, targeted Ruff and both frozen evidence audits passed. An earlier run failed because module visibility omitted native IR for `symExp` used by the faithfulness `#eval`; this was fixed using `import all ReciprocitySpectra.Sextic` and `import all Checks.Fixture200` in Checks/Faithfulness. This cloud validation does NOT run leanprover/comparator or NanoDa and does not make the metadata submission-valid.


## RS-S035: expanded independent Palomar statement surface (pending verification)

The independent Mathlib-only `Challenge.lean` now declares 26 exact theorem
statements, compared by `comparator.json`: the previous 15 E0/E1/E2/E3/E5/E6
and generic-character statements, plus the actual sextic MulChar applications,
raw/direct Gauss bridge, specialised sextic E7 squared modulus, shifted E4
(including zero), Eisenstein class numerator reduction, and the full frozen
`residueMatVec_frozen_orientation` finite row identity. The definitions in
the Challenge reproduce the mathematical operations from the proof library,
without importing any proof-library files. The Solution imports the actual
proved library. This is not an asymptotic proof.

The 19 source files use `module`, and the independent Challenge imports
only Mathlib; its 379-line size is below Palomar's 1,000-line cap. A source
signature check reports nine out of nine newly selected theorem declarations
match their original text. This does **not** imply independent theorem
comparison has succeeded.

Independent Comparator/NanoDa execution is now exercised in
`.github/workflows/rs_s035_comparator.yml`; it is distinct from the
pinned library, axioms, faithfulness and Python tests in the main cloud
workflow. The first run 40520302610 built Challenge and Solution, but
**Comparator failed** on `res_mul` because Challenge placed it under
an extra implicit prime-field assumption; the extra scope has been
removed. The corrected package requires a new complete verification.
No Palomar ID, registration, or AI-disclosure assertion exists.
`formalization.yaml` deliberately retains `automation.methods: []`
pending the owner's accurate declaration; it is not submission-ready.

**RS-S035 final verification finding:** The existing full pinned cloud pipeline
[40522609418](https://github.com/jfairfaxball-348/PRIMES/actions/runs/40522609418)
passed at code head `e15e314` (library, Checks, Challenge, Solution,
axioms, 1764/1764, 366 tests, 42 Gauss checks, Ruff and frozen audits).
The separate independently pinned Comparator/NanoDa run
[40522609498](https://github.com/jfairfaxball-348/PRIMES/actions/runs/40522609498)
**failed**, precisely: `Const does not match between challenge and target
'ReciprocitySpectra.shiftedGauss'`. Prior runs detected an extra prime
assumption on `res_mul`, mismatch in Eisenstein monoid proof constants, and a
missing `sexticValue_zero` simp proof; these were corrected on the branch.
26 theorem names are selected (two additional sextic character prerequisite
laws), but **none of the 26 is certified as a full accepted comparator package**.
PR #14 remains draft and unmerged; RS-S036 must resolve strict definition
fidelity before any registration. Owner automation disclosure is still pending.

**RS-S036 (2026-10-27) generated-constant fidelity checkpoint:** in unmerged draft PR #15 (stacked on #14), pinned Lean `#print` established that the literal positive-sign `shiftedGauss` Challenge and source had only a generated numeral proof-name difference. An explicit raw-literal witness corrected the *entire* exported `shiftedGauss` definition (40528521143: **zero printed differences**) but Comparator next rejected `ReciprocitySpectra.shiftedGauss._proof_1`. Code head `12b904b` is testing the exact raw-Nat class type; no Comparator/NanoDa acceptance yet. Experimental separate ChallengePrefix module was removed: Palomar forbids project-specific Challenge transitive imports. Original 26 proof-library statements, CAND-002 conjectures, Apache-2.0 licence and deferred AI-use declaration unchanged. **No merge or submission.** See `LEDGER.md` RS-S036.

**RS-S036 failed-closeout recovery (2026-10-27):** comparator #44 and cloud #133 originally failed to compile a Challenge-only raw-numeral witness (`omega` at line 228), not an established mathematical theorem. The repair now compiles and scoped cloud validation is green at [40534020351](https://github.com/jfairfaxball-348/PRIMES/actions/runs/40534020351); independent Comparator [40534020098](https://github.com/jfairfaxball-348/PRIMES/actions/runs/40534020098) has passed the original `shiftedGauss` witness mismatch and found its *next* exact-source mismatch at `sexticCharacter`, involving autogenerated `_proof_2/_proof_3` names. The required 26 statement surface is unchanged; no independent acceptance or Palomar ID. Root Apache-2.0 and owner-pending AI declaration unchanged. The final diagnostic run at code head `43c5ff5` must be checked in RS-S037. See `LEDGER.md` for full evidence.


**RS-S037 (2026-10-27):** the single-file independent Mathlib-only Challenge now reproduces the exact character's separate Pi-signature and lambda-binder numeral witnesses, with no alteration to the Solution proof library. The independently pinned Comparator [40542225202](https://github.com/jfairfaxball-348/PRIMES/actions/runs/40542225202) advanced through `sexticCharacter`, then **FAILED** on `ReciprocitySpectra.directShiftedGauss`. This is still not independent acceptance of the 26-theorem package. Scoped full cloud suite [40542225221](https://github.com/jfairfaxball-348/PRIMES/actions/runs/40542225221) **PASSED** on code head `418c825` (three Lean exit codes 0, 1764/1764, 366 tests, 42 Gauss fixtures, Ruff and audits). No unlisted axioms or mathematical statement changes. Apache-2.0 persists and accurate owner-reviewed AI automation disclosure remains pending. Continue with RS-S038; do not merge PR #14/#15/#16 or claim Palomar registration until the appropriate validation and release gates are met.

## RS-S038 checkpoint (2026-10-27): direct shifted-sum constant exact, package not accepted

The independent Challenge's `directShiftedGauss` had reused `rawGauss._proof_1` for the literal `2`, whereas the actual source exports `directShiftedGauss._proof_1`. The Challenge now supplies that exact proof-irrelevant generated witness; **complete** pinned Lean `pp.all` Challenge/source `#print` diff = **0** and auxiliary theorem type/value are equal (run [40555785331](https://github.com/jfairfaxball-348/PRIMES/actions/runs/40555785331), code head `62091106`). The **real independent Comparator/NanoDa still FAILS at the next definition `rationalAddChar`**; passing a single strict constant is not an accepted 26-theorem proof package. Pinned full scoped cloud [40555785210](https://github.com/jfairfaxball-348/PRIMES/actions/runs/40555785210) SUCCESS on code head `62091106`: Lean/Checks/Challenge/Solution, axioms, 1764/1764, 366 pytest, 42 Gauss, Ruff and frozen audits. No proof-library or conjectural assertion changed; no merge, Palomar registration or AI-disclosure completion. RS-S039 diagnoses `rationalAddChar` export fidelity next.


## RS-S039 (2026-10-27): independent 26-theorem Comparator and NanoDa PASS

Run https://github.com/jfairfaxball-348/PRIMES/actions/runs/40564457111 passed the ACTUAL pinned independent Comparator; NanoDa and Lean kernels accepted the full 26-statement finite package on 4cb25de8. The Challenge-only fixes replicate source-generated rationalAddChar numeral and root-of-unity proof witnesses, including exact CommRing typeclass instance paths. Full exported rationalAddChar and both helper theorems have zero pp.all diff. Paired cloud validation https://github.com/jfairfaxball-348/PRIMES/actions/runs/40564457029 passed all pinned Lean, axiom, 1764/1764 exponent, 366 Python, 42 Gauss, Ruff, and frozen audits. A final documentation-head rerun is required before merge. Source mathematics is unchanged; all CAND-002 asymptotics unproved. Apache-2.0 remains, the owner AI-use methods disclosure is PENDING, and no Palomar entry has been made.


## Owner AI-use disclosure (2026-10-27)

The author explicitly confirms substantial use of **OpenAI's ChatGPT** in
the Lean formalisation. The structured `formalization.yaml`
`automation.methods` now records ChatGPT and the AI-assisted,
human-directed development workflow, without inventing unrecorded model
versions. This replaces the previous intentionally empty disclosure.
The original 26 selected mathematical statements remain unchanged.
Post-merge independent verification on main `98c8f54d` succeeded in
Comparator/NanoDa/Lean (40566801477) and scoped cloud (40566801479).
No Palomar registration or editorial review has occurred; RS-S040 is a
separate preflight of Palomar submission requirements.
