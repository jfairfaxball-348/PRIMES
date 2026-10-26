Run RS-S023 in C:\PRIMES on a new branch from main. Read `reciprocity_spectra/PROTOCOL.md` (section 10 in full; sections 2, 7 and 9), `AGENTS.md` (the graduation rule), CAND-002 in `research/CONJECTURE_REGISTER.md` (especially "Exact-identity inventory" and "Proof targets"), the RS-S022 LEDGER entry, `reciprocity_spectra/arith.py`, and the exact tests in `tests/test_reciprocity_spectra.py`. Lean 4.35 and lake are installed locally (~/.elan).

RELEASE GATE: no paper or preprint drafting.

STATE: CAND-002 is frozen (CANDIDATE; NOVELTY_REQUIRES_EXPERT_REVIEW). Phase 1 (science) is done. Phase 2 (PROTOCOL section 10) starts here.

ONE BOUNDED UNIT, RS-S023: release-gate stage 1, plus the start of the Lean scaffold.
1. Write `reciprocity_spectra/RELEASE_INVENTORY.md`: for each item E1–E9 and each paper-proved or conjectural item, give the precise mathematical statement, its Python test, its dependencies, and its proposed Lean formulation (types and definitions).
2. Assess Mathlib (search the installed or fetched Mathlib sources) for: number fields and the cyclotomic or Eisenstein integers Z[omega]; residue fields of primes; power-residue symbols (likely absent); MulChar, AddChar, gaussSum and the |gaussSum|^2 = p results; ZMod. Record each gap, and the cheapest route (for example, working in ZMod p via omega's image r for split primes, with the residue-field isomorphism stated separately).
3. Create the Lean project skeleton in a new sibling directory outside PRIMES (for example C:\PRIMES-lean or a path the owner prefers). The graduation rule keeps proof work out of PRIMES. Pin a Mathlib version. Write the definitions for the split-prime case in ZMod p (the symbol as an exponent mod 6 via Euler's criterion, the class exponent, the Gauss-sum vector), plus E3 and E5 stated and, if quick, proved. Add the computable faithfulness check (section 10.2c) at tiny X, against an exported engine fixture.
4. Record which items look quick, medium or hard, and the order of formalization for RS-S024+.
Do not publish anything. Creating a public GitHub repository and registering on Palomar are owner actions: ask only when a registrable lemma exists.

Run targeted Ruff and PYTHONUTF8=1 pytest if any PRIMES code is touched, and both audit checkers. Close out under PROTOCOL section 7: merge PRIMES records to main, push and delete the branch without asking, with exactly one justified next prompt.
