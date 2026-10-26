# Reciprocity Spectra: Lean formalisation

Lean 4 (v4.35.0) and Mathlib (`56a005855ea1`, tag v4.35.0) formalisation of the exact identities
behind CAND-002. See `../reciprocity_spectra/RELEASE_INVENTORY.md` and PROTOCOL §10. The conjecture
itself is stated, not proved.

## Build

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

**Planned next:**

- E7 (|g|² = p) and E4 (the orientation identity), via `MulChar` and `gaussSum`;
- the matrix and vector definitions;
- CAND-002 as a `Prop`;
- Palomar Challenge/Solution packaging.
