Run RS-S024 in C:\PRIMES on a new branch from main. Read `reciprocity_spectra/PROTOCOL.md` section 10, `reciprocity_spectra/RELEASE_INVENTORY.md`, CAND-002 in `research/CONJECTURE_REGISTER.md`, `formalisation/README.md` and `formalisation/ReciprocitySpectra/Sextic.lean`. Lean: add ~/.elan/bin to PATH and run `lake build` in `formalisation/`. The Mathlib packages are already in formalisation/.lake (git-ignored).

Novelty assessment and external review are owner-run and are not gates. Route: formalise in Lean -> Palomar -> paper -> arXiv -> journal.

STATE: proved with no sorry: E0, E1, E2, E3, E5 and E6. Faithfulness: 1764/1764 at X = 200.

ONE BOUNDED UNIT, RS-S024 (Lean):
1. Build the sextic character chi_rho as a `MulChar (ZMod p) ℂ` from `sexticExp` (multiplicativity from E3; zero at 0). Prove it nontrivial (order 6).
2. E7: |gaussSum chi psi|^2 = p for the primitive additive character psi(t) = e(t/p), using Mathlib's `gaussSum_mul_gaussSum_eq_card` (or `gaussSum_sq`) and the character's conjugation. Record the normalisation g~ = g/sqrt p.
3. E4: the shifted Gauss-sum identity g(r, chi) = conj(chi(r)) g(1, chi) (`gaussSum_mulShift`), and the matrix-orientation identity as a finite-sum lemma.
4. Define the finite index set of primary split primes with N <= X, the matrix R_X, the class vectors w_kappa and the statistics r, eps and s (computable where possible). Extend the faithfulness check to the normalized Gauss sums at X = 200, against an exported fixture, to a stated tolerance.
5. State CAND-002 (1) and (2) as Lean `Prop`s, with every interpretive choice documented. State the conditional (3) with an abstract hypothesis H_P.
Update `RELEASE_INVENTORY.md` status, `formalisation/README.md`, and the LEDGER. Run `lake build` (both targets), PYTHONUTF8=1 pytest, and both audit checkers. Close out under PROTOCOL section 7: merge to main, push and delete the branch without asking, with exactly one justified next prompt.
