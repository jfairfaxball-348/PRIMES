Run RS-S019 locally in C:\PRIMES (Windows; MSVC engine) on a new branch from main. Read `reciprocity_spectra/PROTOCOL.md` (sections 4–9), `reciprocity_spectra/EXTERNAL_REVIEW_2026-10-26.md` (the reviewer is anonymous: never name or cite them), `reciprocity_spectra/RS_S018_COLLISION_AUDIT.md`, `reciprocity_spectra/RS_S016_CROSSOVER.md`, the RS-S015 to RS-S018 and review entries in `reciprocity_spectra/LEDGER.md`, and `scripts/phase1k.py` and `phase1m.py`.

RELEASE GATE: no paper or preprint drafting (PROTOCOL section 10: Lean formalization and Palomar registration come first). This session is research only.

STATE: the crossover law (s = F(N6/X) for classes without exponent 5) passed fresh-class tests (RS-S017), and the pi^5 deficit (s about -1.05 for t >> 1) passed in mean form. An anonymous expert suggests both come from prime-modulus first moments of shifted sextic Gauss sums with shift u = rho*kappa: the profile would be a rho-averaged shift-aspect crossover, and the pi^5 deficit possibly an opposite-sign prime-sieve term left once tau_6(p^5) = 0 removes the principal local term. Freezing CAND-002 is deferred.

ONE BOUNDED UNIT, RS-S019: pre-registered decisive tests.
1. Build the unrestricted-moduli variant at a locally feasible X (about 1e5 to 3e5). Rows are the primary degree-one primes rho as now. Columns are all squarefree primary c coprime to 6 with N(c) <= X (non-squarefree c have g(1,c) = 0). Entries are (rho/c)_6 by multiplicativity. Column weights are g6~(c), built from prime Gauss sums by twisted multiplicativity (g(c1 c2) = (c1/c2)(c2/c1) g(c1) g(c2)). Validate exactly against a pure-Python implementation at small X, with a new test in tests/test_reciprocity_spectra.py. Define the analogue r_kappa = ||R w_kappa|| / ||w_kappa|| normalized by the matched random control for the rectangular shape, and compute the prime-moduli version at the same X for direct comparison.
2. Before any unrestricted-moduli class data: register in a new results JSON and LEDGER block, then commit and push.
   - (P) the reviewer's sieve hypothesis predicts that the pi^5 deficit disappears or changes substantially with unrestricted moduli. Fix numerical thresholds in advance: for example, the mean s over pi^5 classes with t >= 3 moves by >= 0.5 toward 0 or changes sign. State the alternative outcome too.
   - (Q) for exponents 1–4, state whether the profile shape is expected to persist.
   Use the same class families (powered classes only), seeds and controls.
3. Run, then score verbatim.
4. Also (exploratory) fit an explicit 1/log X correction to the plateau using the stored RS-S016/17 data, and the trend of the pi^5 coefficient with N(pi) (the reviewer's Q3a).

Never commit matrices; delete data/*.bin after use. Run targeted Ruff, PYTHONUTF8=1 pytest (record the three fcntl exclusions), and both audit checkers. Close out under PROTOCOL section 7: merge to main, push and delete the branch without asking, with exactly one justified next prompt (the rho-partition test and the exact unit-normalization calculation are the queued follow-ups).
