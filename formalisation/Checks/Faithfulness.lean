module

public import Checks.Fixture200
public import ReciprocitySpectra.Sextic

@[expose] public section

/-!
# Faithfulness check (PROTOCOL §10.2c)

Recomputes every entry of the engine's sextic exponent matrix at `X = 200` from the Lean definition
`ReciprocitySpectra.symExp` and reports the number of mismatches. Evaluation only (`#eval`); it is
not a kernel proof and not part of any Palomar Solution.
-/

namespace ReciprocitySpectra.Checks

/-- Exponent of the row element `(c, d)` at the column prime `(p, a, b)`; `255` for zero. -/
def leanExp (p : ℕ) (a b c d : ℤ) : ℕ :=
  let r : ZMod p := -(a : ZMod p) * (b : ZMod p)⁻¹
  match symExp r ⟨c, d⟩ with
  | some k => k.val
  | none => 255

/-- Parsed fixture records `(p, a, b, c, d, e)`. -/
def fixture200 : List (ℕ × ℤ × ℤ × ℤ × ℤ × ℕ) :=
  (fixture200Text.splitOn ";").filterMap fun rec =>
    match (rec.splitOn " ").filterMap String.toInt? with
    | [p, a, b, c, d, e] => some (p.toNat, a, b, c, d, e.toNat)
    | _ => none

/-- Mismatches between the Lean definition and the engine (diagonal entries compare as 255). -/
def mismatches : List (ℕ × ℤ × ℤ × ℤ × ℤ × ℕ × ℕ) :=
  fixture200.filterMap fun (p, a, b, c, d, e) =>
    let l := leanExp p a b c d
    if l = e then none else some (p, a, b, c, d, e, l)

#eval s!"entries: {fixture200.length}, mismatches: {mismatches.length}"

end ReciprocitySpectra.Checks
