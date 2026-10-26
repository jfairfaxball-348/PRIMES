Run RS-S021 in C:\PRIMES on a new branch from main. Read `AGENTS.md` (candidate discipline and the graduation rule), `reciprocity_spectra/PROTOCOL.md` (sections 2, 7, 9 and 10), `reciprocity_spectra/EXTERNAL_REVIEW_2026-10-26.md` (the reviewer is anonymous: never name or cite them), `reciprocity_spectra/RS_S018_COLLISION_AUDIT.md`, `reciprocity_spectra/RS_S016_CROSSOVER.md`, the RS-S015 to RS-S020 entries in `LEDGER.md` and `CONJECTURES.md`, and CAND-001 plus the template in `research/CONJECTURE_REGISTER.md`.

RELEASE GATE: no paper or preprint drafting (PROTOCOL section 10). Candidate freezing is allowed.

STATE (all at X <= 1e6, local):
- Crossover law: s = F(N6/X) for classes without exponent 5. Holdout PASS on 440 fresh classes (RS-S017). The profile persists over all squarefree moduli (RS-S019), so it is a shift-aspect property of sextic Gauss-sum first moments.
- pi^5 law: s -> -1 for t >> 1. Registered PASS three times (RS-S015-P2; RS-S017-Q3 mean clause; RS-S020-H-: -0.919 +- 0.083 on 88 fresh primes, N <= 1000). INTRINSIC, not a sieve effect (RS-S019).
- Mechanism evidence: rho-averaged shift u = rho*kappa (the reviewer's mechanism). The k = 2 excess sits on quadratic-residue rows (RS-S020), consistent with the rho-dependent vanishing in Broker–Hoffstein's Hecke relation.
- Open: H+ (F(0+) = 1) and a new-scale holdout need >= 32 GB RAM or cloud (owner decision; not a blocker). The plateau is still rising as t -> 0. The unit-class selection of statement 2 is prime-specific.

ONE BOUNDED UNIT, RS-S021 (stage: candidate freezing; no new matrices):
1. Write the exact CAND-002 statement as a rho-averaged shift-aspect law for sextic Gauss-sum first moments, in matrix form, with definitions identical to the code (rows rho; columns prime moduli; rational normalization), and an unrestricted-moduli variant noted. Parts:
   (a) the crossover profile (a common F, positive for t -> 0, about 0 near t = 1);
   (b) the pi^5 law s -> -1 for N(pi)^5/X -> infinity;
   (c) conjectural fixed-class limits, stated conditionally on a sextic Patterson-type prime asymptotic (per the review).
   Keep F(0+) = 1 as an open sub-question, not part of the frozen claim.
2. Fill every AGENTS.md candidate field: provenance; discovery range (RS-S015/16); holdouts (RS-S017, RS-S019, RS-S020) with machine-readable sources; falsification strategy (H+ at X >= 4e6; new-scale holdout; Q3 redesign with power-filtered per-class clauses); triviality checks (sixth-power and conjugation invariance; the normalization-artefact check: recompute s using the random-control level instead of r_1 from stored data, as a stored-data script); mechanism notes; prior-art status NOVELTY_REQUIRES_EXPERT_REVIEW; lifecycle status CANDIDATE.
3. Identify the exact-identity inventory items this candidate relies on (input to PROTOCOL section 10 stage 1) and the proof targets under section 9 (hard version first), without starting proof work.
4. Update CONJECTURES.md (a new RS-n entry), PROGRAM_STATUS.md, ROADMAP.md and the LEDGER.

Run targeted Ruff and PYTHONUTF8=1 pytest if any code is touched, and both audit checkers. Close out under PROTOCOL section 7: merge to main, push and delete the branch without asking, with exactly one justified next prompt.
