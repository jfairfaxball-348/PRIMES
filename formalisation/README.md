# Reciprocity Spectra: Lean formalisation

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
