Run RS-S016 locally in C:\PRIMES (Windows; MSVC engine port validated in RS-S015) on branch `rs-s015-class-tests`, or on main if the owner has merged it. Read `reciprocity_spectra/PROTOCOL.md` (sections 4–9), the RS-S015 entries in `reciprocity_spectra/LEDGER.md` and `CONJECTURES.md`, `reciprocity_spectra/RS_S014_INVARIANCE_AUDIT.md` sections 5–6, `results/rs_s015_class_tests_2026-10-26.json` (`score`) and CAND-001 in `research/CONJECTURE_REGISTER.md`. Do not merge without owner instruction.

STATE: PROV-RS14 is REFUTED at X = 10^6 (P1 FAIL, P2 PASS, P3 FAIL; smallest failing class pi7^3*pi13^2, r = 1.049). Exponents 1 and 2 follow s = eps*N6^(1/6) ~ 0.86–0.95. For exponent 3, s falls from 0.94 (N = 4) to 0.14 (N = 73). Exponent-4 classes have r <= 1 for N >= 31. The exponent-5 law (B) passes (mean s = -1.05). No CAND-002.

ONE BOUNDED UNIT, RS-S016, EXPLORATORY (no registration, no CAND):
1. Rerun the RS-S015 single-prime classes (k = 1..5 over the same 20 primes; reuse `scripts/phase1k.py` building blocks in a new script `phase1l.py`, with a `--x` parameter) at X = 1.6e5, 3.2e5 and 6.4e5. Store them as EXPLORATORY in a new results JSON, together with the 10^6 values already stored.
2. For each (N, k), determine whether s rises with X toward the exponent-1 value (a finite-X cutoff, e.g. a dependence on N^k/X^a) or is X-stable (a different class law). Fit only simple candidate forms (power of N per k; a scale variable N6/X^a), and report the fits honestly with residuals.
3. Note the exact structure: (pi/.)_6^3 is the quadratic character and (pi/.)_6^2, ^4 are cubic. Record any mechanism hypothesis (theta-coefficient analogy, Patterson and Bröker–Hoffstein) as a hypothesis only.
4. Output either an explicit PROV-RS16 statement with a powered falsification plan for a later registered session, or an exact obstruction.

Never commit matrices; delete `reciprocity_spectra/data/*.bin` after use. Run targeted Ruff, PYTHONUTF8=1 pytest (record the three fcntl exclusions), and both audit checkers. Close out under PROTOCOL section 7 with exactly one justified next prompt or the genuine owner blocker.
