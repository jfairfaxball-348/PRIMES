Run RS-S020 locally in C:\PRIMES (Windows; MSVC engine) on a new branch from main. Read `reciprocity_spectra/PROTOCOL.md` (sections 4–10), `reciprocity_spectra/EXTERNAL_REVIEW_2026-10-26.md` (the reviewer is anonymous: never name or cite them), the RS-S019 entries in `reciprocity_spectra/LEDGER.md` and `CONJECTURES.md`, `results/rs_s019_moduli_2026-10-26.json`, and `scripts/phase1n.py`.

RELEASE GATE: no paper or preprint drafting (PROTOCOL section 10). Research only.

STATE: RS-S019 (registered, X = 2e5, trace normalization) found:
- the pi^5 deficit is INTRINSIC: s = -1.08 with prime moduli and -1.22 with all squarefree moduli, so it is not a sieve effect;
- the crossover profile is present for both modulus sets.
Exploratory findings:
- the pi^5 coefficient tends to -1 as N(pi) grows (-1.08 -> -1.00 over N = 19..400; fit s = -0.995 - 2.6/N);
- the plateau keeps rising as t -> 0 (0.97–0.99 at the smallest t) and is not a single 1/log X correction;
- statement 2's unit-class selection (j in {0,3}) is strong with prime moduli and vanishes with unrestricted moduli.

ONE BOUNDED UNIT, RS-S020:
1. Reviewer's rho-partition test (EXPLORATORY): for exponent-2 singles with N = 1 mod 12, split the row primes rho by (rho/pi)_6 and compute the per-class excess within each residue class (rational and trace normalization, prime moduli, X about 3.2e5). Ask whether the concentration correlates with (pi/pibar)_6, i.e. whether Broker–Hoffstein Lemma 5.3's tau_6(pi^2) = 0 condition reappears inside the rho-average.
2. Exact unit-normalization factor (stage: mechanism): derive and test (pure-Python exact test) the factor relating the rational e(t/p) and trace prime Gauss sums, ((2a-b)/rho)_6 = (pibar/pi)_6, decomposed into (-1/rho)_6, (-3/rho)_6 (b mod 9) and the residual (b'/rho)_6. Explain, or show unexplained, why the prime-moduli selection j in {0,3} vanishes for unrestricted moduli.
3. Register (commit and push before data) the limit hypotheses at a fresh scale or fresh classes feasible locally:
   - H+: F(0+) = 1, i.e. s -> 1 as t -> 0;
   - H-: s(pi^5) -> -1 as N(pi) -> infinity with t >> 1.
   Use numerical tolerances and a power calculation. Prefer fresh primes (N > 400 for H-; small N at the largest feasible X for H+). Run and score if time allows; otherwise leave registered for RS-S021.

Never commit matrices; delete data/*.bin after use. Run targeted Ruff, PYTHONUTF8=1 pytest (record the three fcntl exclusions), and both audit checkers. Close out under PROTOCOL section 7: merge to main, push and delete the branch without asking, with exactly one justified next prompt.
