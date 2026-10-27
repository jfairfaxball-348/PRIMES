# RS-S042 arXiv metadata and owner decisions — internal, not submitted

**Working title (owner to confirm):** A shift-aspect crossover for twisted sextic Gauss-sum vectors: numerical evidence, conjectures, and a Lean-verified finite core

**Plain-text abstract (copy-ready):**
We investigate numerically the action of sextic residue-symbol matrices indexed by primary split primes of the Eisenstein integers on vectors of normalized sextic Gauss sums with multiplicative twists. A normalized excess statistic shows a finite-scale crossover when the sixth-power-free twist norm is compared with the prime cutoff. Fifth-power twists also show a negative large-aspect excess. Predictions were registered before fresh twist-class and scale tests, and failed precursor predictions are retained. We formulate three distinct conjectures: a compact-positive-aspect crossover, a large-aspect fifth-power limit, and a separate fixed-class limit. The fixed-class conjecture does not follow from the first two. A Lean 4/Mathlib development independently verifies 26 selected exact finite algebraic and Gauss-sum statements, including a residue-matrix row identity; it does not establish any of the proposed asymptotics. Exact signed Gram identities describe the further prime-correlation estimates that a proof would require.

**Category:** math.NT (Number Theory)

**Keywords:** sextic reciprocity; Gauss sums; Eisenstein integers; power-residue matrices; computational number theory; spectral statistics; Lean 4 formal verification; conjectures.

**Author field:** John Fairfax-Ball (institution and affiliation **owner decision**, do not invent).

**Code, data and verification (public):**
- Repository: https://github.com/jfairfaxball-348/PRIMES
- Paper LaTeX: https://github.com/jfairfaxball-348/PRIMES/tree/main/paper
- Committed numerical JSON: https://github.com/jfairfaxball-348/PRIMES/tree/main/reciprocity_spectra/results
- Figure generator: https://github.com/jfairfaxball-348/PRIMES/blob/main/paper/figures/make_all.py
- Formal Lean library: https://github.com/jfairfaxball-348/PRIMES/tree/main/formalisation
- Finite source baseline: commit `8b050b06d1195491b17b92e68b2d92d9d2478cb0`
- Successful independent 26-result Comparator/NanoDa: https://github.com/jfairfaxball-348/PRIMES/actions/runs/40569785577
- Matching scoped Lean verification: https://github.com/jfairfaxball-348/PRIMES/actions/runs/40569785692
- Theorems listed in `formalisation/README.md`; no Palomar registration asserted.

**AI-use disclosure (copy-ready, truthful):**
OpenAI's ChatGPT was used substantially in the Lean formalisation and assisted with drafting this manuscript. The exact model versions were not consistently recorded. The author takes responsibility for the mathematical claims, results, verification, text, figures, and submission. Machine checking of the finite Lean corpus does not establish the asymptotic conjectures.

**Source-package checklist (internal preflight, not evidence of upload):**
- [ ] Build from clean checkout with Python plotting requirements, reproducible 14 vector-PDF+PNG pairs.
- [ ] Run `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` from `paper/`, inspect rendered pages and citations.
- [ ] Bundle `main.tex`, `sections/*.tex`, `references.bib`, **12 used figures** from `figures/generated/*.pdf` (14 generated but 2 excluded); adapt `figures/generated` paths for arXiv if needed.
- [ ] Confirm arXiv submission toolchain supports the figure/font packages (`amsart`, `graphicx`, `microtype`, `hyperref`, `enumitem`).
- [ ] Bibliography verified from primary sources; no “Work on…” entries remain; recheck citation output in generated PDF.
- [ ] Confirm metadata, content, and AI disclosure with owner.
- [ ] Record actual version/commit/build artifact before any submission.

**Single owner-decision list:** (1) final title; (2) final author line and institution/affiliation or independent researcher; (3) arXiv posting licence (**not** automatically Apache-2.0, which is the repository licence); (4) arXiv endorsement if required; (5) target journal. These are not permission to upload or submit.

**Status:** Internal manuscript revision only. No arXiv upload, journal submission, Palomar registration, external review, or third-party contact is authorized or claimed by RS-S042.
