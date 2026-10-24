Read "reciprocity_spectra/PROTOCOL.md", "reciprocity_spectra/LEDGER.md", "reciprocity_spectra/CONJECTURES.md", "reciprocity_spectra/ROADMAP.md" (Phase 1), "reciprocity_spectra/README.md" and this entire prompt BEFORE changing anything. The committed repository on main is authoritative.

STATE: Reciprocity Spectra is the active PRIMES programme. It was opened in RS-S001 on 2026-10-24 by owner decision. The DISCOVERY-1 blind chain is PAUSED at D1-72/S074, with 16 REPLICATED / 0 OBSERVED / 9 REFUTED and zero candidates. Do not resume it, and do not read, reconstruct or modify D1 interval roles, guard bands, E005 objects or D1 ledgers. Conjectures RS-1, RS-2, RS-3, RS-4 and RS-6 are PILOT; RS-5 is UNTESTED. The Phase-1 predictions were committed at commit 0b77769, before any run above X = 160000. They are:
- kappa3 in [1.38, 1.47];
- cubic top-singular-vector overlap with conj(g~) within 0.03 of sqrt(1 - D/theta^2);
- quartic theta_n = 0.166*ln X - 0.18 +- 0.05, which is 1.924 at X = 320000 and 2.039 at X = 640000;
- quadratic (2 - m4)*ln D in [1.0, 1.4].

ONE BOUNDED UNIT. RS-S002 / Phase 1a: build the scalable engine, then test the committed predictions at X = 320000.

1. ENGINE. Add native code, either a new file "reciprocity_spectra/native/residue_engine.c" or an extension of residue_matrix.c, that does the following:
   (a) builds the uint8 exponent matrix with OpenMP over 4 threads;
   (b) computes the normalized Gauss sums with OpenMP;
   (c) provides blocked matrix-vector products y = C x and y = C^* x for complex x, reading the uint8 matrix directly. Use a small shared library loaded with ctypes, or a standalone C Lanczos routine;
   (d) computes the quadratic m4 without a dense float matrix. Use either the exact blocked integer Gram trace, or a Hutchinson estimate with at least 64 probes and a reported standard error.
   Also generate the symmetry-matched random control with the same engine, using random exponents with seed 0 and the same reciprocity signs.

2. VALIDATE before any run above X = 160000:
   - matrices byte-identical to native/residue_matrix.c at X = 20000 for quad, cubic and quartic;
   - top-8 singular values within 1e-8 relative of scipy svds at X = 40000;
   - m4 equal to the dense value at X = 40000 (exact method), or within 2 standard errors (stochastic method).

3. RUN X = 320000 for cubic, quartic and quad. Report:
   - the top-12 singular values;
   - the BBP strength theta, from sigma1 = theta + D/theta;
   - the cubic overlap with conj(g~);
   - the quadratic m4 and sigma1/(2 sqrt D);
   - the random-control top singular values at the same D.
   Write results incrementally to "reciprocity_spectra/results/phase1_<date>.json", with the commit, command, X, D and seeds.

4. COMPARE each committed prediction and record PASS or FAIL verbatim in LEDGER.md and CONJECTURES.md. A conjecture becomes STRESSED only if every one of its predictions passes. Otherwise record REFUTED, or REVISE with a newly committed prediction for a new scale. Never edit a committed prediction after seeing data.

5. ONLY IF steps 1-4 are complete with time and RAM to spare, repeat steps 3-4 at X = 640000. Otherwise record exactly why this was skipped.

CONSTRAINTS:
- No mechanism derivations.
- No new families (sextic, quintic).
- No changes to committed predictions.
- Keep each run to about 45 minutes or less, and commit results as they arrive. The container is ephemeral.
- Matrices are never committed.
- Run ruff check on the touched Python files, and pytest, before closeout. Do not edit frozen D1 files to fix the pre-existing repository-wide ruff findings.

CLOSEOUT (PROTOCOL.md section 7):
- add an RS-S002 entry to LEDGER.md;
- update the CONJECTURES.md statuses;
- add the results JSON;
- update the PROGRAM_STATUS.md current-stage line if the state changes;
- write exactly ONE justified next prompt to NEXT_SESSION_PROMPT.md. The likely next unit is RS-S003: Phase 1b (sextic test of RS-5 plus local statistics) or Phase 2 mechanisms (derive kappa3 and c4). Suppress the prompt if an owner decision is required;
- commit and push to the session branch. Merge to main only on the owner's explicit instruction.
