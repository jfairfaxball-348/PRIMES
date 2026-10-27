Run RS-S041 as a CLOUD paper-drafting session on a fresh branch from main of jfairfaxball-348/PRIMES. Authoritative main overrides chat history. Do not inspect or modify the paused D1 records.

PLAN OF RECORD (owner, 2026-10-27): route = paper -> arXiv preprint -> journal. Palomar is OPTIONAL and NOT a gate (PROTOCOL sections 9.5 and 10 revised): the editorial review declined the 26 finite identities on research interest, not correctness. The Lean formalisation is a VERIFICATION ARTEFACT, cited in the paper. Proof work on CAND-002 is parked. Novelty assessment and external review are owner-run and not gates. The external reviewer of 2026-10-26 is anonymous: never name, cite or acknowledge them by name.

READ FIRST:
- reciprocity_spectra/PROTOCOL.md sections 7-10
- PROGRAM_STATUS.md (top banner)
- reciprocity_spectra/ROADMAP.md
- CAND-002 in research/CONJECTURE_REGISTER.md (frozen text plus the 2026-10-27 clarifications and restatement of (3))
- reciprocity_spectra/RELEASE_INVENTORY.md ("Plan of record" classification A / A' / B / C)
- reciprocity_spectra/CONJECTURES.md, RS-S015 onwards and RS-10
- reciprocity_spectra/LEDGER.md, RS-S014 onwards
- RS_S014_INVARIANCE_AUDIT.md, RS_S016_CROSSOVER.md, RS_S018_COLLISION_AUDIT.md, EXTERNAL_REVIEW_2026-10-26.md
- RS_CAND002_LOGICAL_BRIDGE_AUDIT.md, RS_S026..S028 notes, RS_HP_SCALE_ERRATUM.md
- formalisation/README.md (the reader's guide to the 26 Lean theorems)
- reciprocity_spectra/results/*.json

ONE BOUNDED UNIT, RS-S041: a complete first draft of an experimental-mathematics paper, FIGURE-RICH.

PAPER (LaTeX, in a new top-level `paper/` directory):
- Use amsart (or article with amsmath/amsthm), and a single `main.tex` with `\input` sections.
- Provide `references.bib`, a `figures/` directory and a `Makefile` or `latexmk` build.
- Build a PDF if a TeX engine is available. Try latexmk or pdflatex; else install texlive or tectonic if the container permits. Otherwise commit the sources with exact build instructions.
- Working title, editable: "A shift-aspect crossover for twisted sextic Gauss-sum vectors: numerical evidence, conjectures and a Lean-verified finite core."
- Sections:
  1. Introduction and results at a glance. Lead with a one-page visual summary figure.
  2. Setup and notation: primary primes in Z[omega], the sextic residue matrix, normalised Gauss sums, twist classes mod sixth powers, the statistics r, eps, s, and t = N6/X.
  3. Methodology: pre-registration, symmetry-matched null controls, engines and validation, the matrix-free engine. State it as a feature: every prediction committed before data, failures kept.
  4. Results:
     - the crossover law and its collapse in N6/X;
     - the exponent-five deficit;
     - prime versus all-moduli;
     - row-prime parity structure;
     - new-scale holdouts to X = 4e6.
  5. Conjectures: CAND-002 (1), (2) and standalone (3), each stated exactly and labelled CONJECTURE. Open sub-questions Q-a to Q-d.
  6. What is proved:
     - (A) the Lean-verified finite core, cited by commit, theorem name and Comparator/NanoDa run, with the residue-field modelling convention stated;
     - (B) paper-proved identities (row and Gram identities, reciprocity kernel transform, ideal prime sieve and Vaughan identity, the logical countermodel), with proofs or proof sketches and gaps stated.
  7. Heuristic mechanism (shifted Gauss-sum first moments, rho-averaged shift-aspect crossover, tau_6(p^5) = 0, parity concentration), clearly labelled HEURISTIC. Include the H_P scale lesson and why it is too weak at row scale.
  8. Relation to the literature: Patterson; Heath-Brown–Patterson; Dunn–Radziwill; David–Dunn–Hamieh–Lin; Broker–Hoffstein; Chinta–Friedberg–Hoffstein; Kazhdan–Patterson; Blomer–Goldmakher–Louvel; de Faveri–Dunn–Hoffstein; Xu–Sang; Dummit–Dummit–Kisilevsky. Factual only, no novelty claims; the owner decides novelty wording.
  9. Limitations and failures: PROV-RS14 refuted; the Q3 design flaw; the CAND-001 refutation; the H_P erratum; the crossover is measured at X <= 4e6 only.
  10. Data, code and formal-verification availability (repository commit; results JSON; the Lean project path).
  11. AI-assistance disclosure: Claude (Anthropic) and ChatGPT (OpenAI) used substantially for computation, formalisation and drafting; the owner is responsible. Author: John Fairfax-Ball.
- Every number in the text must come from a committed results JSON, cited in a comment next to it. Labels: Lean-verified, proved on paper, conjectural or numerical.

FIGURES AND DIAGRAMS. The owner wants as many relevant visuals as possible, so the paper is not all words and equations.
- Produce each figure with a committed script `paper/figures/make_*.py` (matplotlib; vector PDF plus PNG preview). Read only committed results JSONs where they suffice.
- If a figure needs data not stored (for example singular-value spectra), you may regenerate deterministically at X <= 3.2e5 with the existing engines. Commit the script and a small JSON, and label it ILLUSTRATIVE, not new evidence. No new predictions or claims.
- Style: one consistent style module; a colourblind-safe palette; consistent symbols per exponent class; readable at single-column width; axes labelled with units and notation; captions that state the data source (JSON and commit) and what to look at.
- Use TikZ, or matplotlib schematics, for conceptual diagrams.
- Aim for at least 12 figures. Candidates, in priority order:
  1. Visual abstract: the matrix R_X, the twist vector w_kappa, the excess s, and the crossover curve in one panel set.
  2. Schematic of the objects: primes in Z[omega] (a lattice plot of primary primes); the sextic symbol as a 6-colour heat map of a small R_X (X about 200); a Gauss-sum phase plot.
  3. The singular-value spectrum of R_X versus the symmetry-matched null, with outliers (from stored phase1 results, or illustrative regeneration).
  4. Growth of r_1 with X, from 1.6e5 to 4e6 (RS-S016, RS-S015 and RS-S021 JSONs).
  5. THE KEY FIGURE: s against log10 t for exponents 1-4 at all six scales, collapsing on the frozen F, with the discovery points and the fresh holdouts (RS-S017; RS-S021 X = 2e6 and 4e6) in distinct markers.
  6. Residuals from frozen F by bin, with tolerance bands, for each registered holdout (RS-S017-Q2 and RS-S021-A).
  7. The exponent-five law: s for pi^5 against N(pi), converging to -1, with band means and error bars (RS-S015/16/17/20/21).
  8. Prime versus all squarefree moduli (RS-S019): side-by-side profiles and the pi^5 comparison.
  9. Row-prime parity: s by part j = (rho/pi)_6 for k = 2, by N mod 12 and the (pi/pibar)_6 group (RS-S020 rho-partition JSON).
  10. The small-t plateau rising toward 1 (K1 against X).
  11. A pre-registration timeline diagram: hypotheses, then committed predictions with commit hashes, then outcomes (PASS/FAIL), including the refuted PROV-RS14 and the Q3 flaw.
  12. A regime diagram in the (log N6, log X) plane: the compact-t band of (1), the large-t region of (2), and the fixed-class boundary t -> 0 of (3), showing why (1) + (2) do not imply (3).
  13. A verification-pipeline diagram: C engine, then fixtures, then Lean definitions, faithfulness check (1764/1764), Challenge/Solution and Comparator/NanoDa.
  14. Normalisation check: the collapse with and without r_1 normalisation (RS-S022 audit JSON).
  15. Optional: a twist-class lattice diagram (exponent vectors mod 6; sixth-power invariance; pi^5 as the conjugate twist).
- Also include compact tables: registered predictions and outcomes; the claim classification A / B / C.

RULES:
- No new scientific claims, predictions or conjecture changes.
- The frozen CAND-002 text and historical evidence are unchanged.
- Never name the anonymous reviewer.
- Do not submit anything externally (arXiv or journal are owner actions).
- Do not re-submit to Palomar.

CLOSEOUT:
- Validate: all figure scripts run from a clean checkout; the paper builds (or the build blocker is stated); every quoted number traces to a JSON; full pytest (Linux) and both audit checkers pass; the Lean build is unaffected.
- Append to the LEDGER; update PROGRAM_STATUS and ROADMAP.
- Replace NEXT_SESSION_PROMPT.md with exactly one next unit: RS-S042, a revision pass. That covers internal consistency, figure polish, a reference check, the arXiv metadata and abstract, and a list of owner decisions (title, author line, licence, endorsement, venue).
- Merge to main without asking, push, and delete the session branch. Disclose anything not done.
