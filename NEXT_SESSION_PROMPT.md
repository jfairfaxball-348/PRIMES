Run RS-S018 in C:\PRIMES on a new branch from main. Read `reciprocity_spectra/PROTOCOL.md` (sections 2, 7 and 9), the RS-S015 to RS-S017 entries in `reciprocity_spectra/LEDGER.md` and `CONJECTURES.md`, `reciprocity_spectra/RS_S016_CROSSOVER.md`, `reciprocity_spectra/PRIOR_ART.md`, `reciprocity_spectra/RS_S013_LITERATURE.md`, RS-9 in `CONJECTURES.md`, and CAND-001 in `research/CONJECTURE_REGISTER.md`.

STATE: the surviving core after RS-S017 is three statements:
(i) CAND-001 statement 2 / RS-9, the prime-level unit-class bias of sextic Gauss sums (registered PASS at X = 1.28e6);
(ii) the mean form of law (B): for kappa = pi^5 with t = N^5/X >> 1, s = eps*N^(5/6) is about -1.05 (registered PASS twice, RS-S015-P2 and RS-S017-Q3 mean clause);
(iii) (A''): s_kappa(X) = F(N6/X) + o(1) for classes without exponent 5, with a positive fixed-class limit (registered PASS on 440 fresh classes, RS-S017 Q1/Q2/Q4).
(B'') as stated is refuted (an underpowered per-class r < 1 clause). There is no live CAND.

ONE BOUNDED UNIT, RS-S018, stage collision-audit (no new matrices):
1. For each of (i)–(iii), write the exact statement, then search the literature for equivalent or implying results, citing every source. Search at least: Patterson and Heath-Brown–Patterson (cubic/sextic Gauss-sum distribution and theta coefficients); Kubota; Chinta–Friedberg–Hoffstein and Bröker–Hoffstein (sextic theta and Gauss-sum Dirichlet series); Blomer–Goldmakher–Louvel (large sieve for n-th order symbols); Dunn–Radziwill and David–Dunn–Hamieh–Lin (bias and cancellation in cubic/higher-order Gauss sums, Patterson's conjecture); and random-matrix or spectral studies of power-residue-symbol matrices. Use the web search tools.
2. Assign each statement a novelty status from the PROTOCOL vocabulary (never "new"), and give the specific overlap. In particular, decide whether (i) and the sign and size of (ii) are implied by known Gauss-sum main terms (KNOWN_IMPLIED), and whether the N6/X crossover in (iii) is a known conductor/length transition.
3. Record the audit in `reciprocity_spectra/RS_S018_COLLISION_AUDIT.md` and update `PRIOR_ART.md`.
4. Decision: if at least one statement remains SEARCHED_NO_COLLISION_FOUND or NOVELTY_REQUIRES_EXPERT_REVIEW with strong registered evidence, draft (do not freeze) a candidate statement for freezing in RS-S019. If everything is KNOWN_EQUIVALENT or KNOWN_IMPLIED, record that and state the programme's honest standing.

Run targeted Ruff and PYTHONUTF8=1 pytest if any code is touched, and both audit checkers. Close out under PROTOCOL section 7: merge to main, push and delete the branch without asking (section 9 item 4), with exactly one justified next prompt or the genuine owner blocker.
