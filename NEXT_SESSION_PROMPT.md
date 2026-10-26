Run RS-S019 in C:\PRIMES on a new branch from main. Read `AGENTS.md` (candidate discipline and the graduation rule), `reciprocity_spectra/PROTOCOL.md` (sections 2, 7 and 9), `reciprocity_spectra/RS_S018_COLLISION_AUDIT.md` (especially section 5), `reciprocity_spectra/RS_S016_CROSSOVER.md`, the RS-S015 to RS-S018 entries in `reciprocity_spectra/LEDGER.md`, and CAND-001 plus the template in `research/CONJECTURE_REGISTER.md`.

STATE: RS-S018 drafted, but did not freeze, the "sextic twist-class crossover law" (matrix form):
(1) for classes kappa with every exponent in {1..4}, s_kappa(X) - F(N6/X) -> 0 for a single decreasing F with F(0+) = c > 0, so every such fixed class is enhanced in the limit;
(2) for kappa = pi^5, s -> -c5 < 0 as N^5/X -> infinity, and lim sup r <= 1 for every fixed class containing an exponent 5.
Evidence: discovery RS-S015/16; holdout RS-S017 (440 fresh classes; Q1/Q2/Q4 PASS; the mean form of (2) PASS). Novelty: NOVELTY_REQUIRES_EXPERT_REVIEW. Known caveats: plateau drift (0.85 -> 0.94 as t falls); the small-t limit of (2) is open; the excess is not a naive tau_6 readout (it is uniform across Broker-Hoffstein Lemma 5.3's tau_6(pi^2) = 0 condition).

EXTERNAL REVIEW: the owner sent an expert review request on 2026-10-26 (see the LEDGER). If the owner shares a reply, record it first and adjust the novelty status before freezing; otherwise proceed.

ONE BOUNDED UNIT, RS-S019 (stage: candidate freezing; no new matrices):
1. Allocate CAND-002 in `research/CONJECTURE_REGISTER.md` with every field AGENTS.md requires: exact statement and definitions; discovery provenance and range; holdout range (RS-S017); falsification strategy (including the X = 1.28e6 test that needs a machine with >= 16 GB free RAM, and a Q3 redesign with power-filtered per-class r clauses); current evidence with machine-readable sources; triviality checks (sixth-power invariance; conjugation; whether F could be an artefact of the r_1 normalization: test with a stored-data check using an alternative normalization, such as the random-control level); mechanism notes (theta-coefficient analogy and the section-3 contrast); prior-art status; lifecycle status CANDIDATE.
2. Decide which parts are proof targets under PROTOCOL section 9 (hard version first) and record the graduation path (export to a dedicated proof repository) without starting proof work.
3. Update CONJECTURES.md (RS-n entry), PROGRAM_STATUS.md, ROADMAP.md and the LEDGER.

Run targeted Ruff and PYTHONUTF8=1 pytest if any code is touched, and both audit checkers. Close out under PROTOCOL section 7: merge to main, push and delete the branch without asking (section 9 item 4), with exactly one justified next prompt or the genuine owner blocker.
