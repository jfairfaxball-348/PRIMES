# arXiv release metadata — RS-S042 internal candidate (NOT SUBMITTED)

## Copy-ready title
A shift-aspect crossover for twisted sextic Gauss-sum vectors: numerical evidence, conjectures, and a Lean-verified finite core

## Plain-text abstract
We numerically study sextic residue-symbol matrices indexed by primary split primes of the Eisenstein integers, applied to vectors constructed from normalized sextic Gauss sums and multiplicative twists. After baseline normalization, the finite measurements display a crossover as the ratio of the sixth-power-free twist norm to the prime cutoff varies. Fifth-power prime twists exhibit a negative large-aspect excess. Pre-registered fresh-class and new-scale comparisons, including cutoffs up to four million, support portions of the observed pattern, while failed predecessor predictions remain documented. We formulate three separate asymptotic conjectures, distinguishing compact positive aspect from the unproved fixed-class boundary. A Lean 4 and Mathlib formalization verifies twenty-six selected finite residue-field, character, Gauss-sum and matrix-row identities; it does not establish any of the three conjectures. Exact finite signed-Gram and reciprocity reductions explain the outstanding analytic challenge. All numerical input data, code and formal proofs are openly available in a versioned repository.

## Categories and indexing
- arXiv primary: math.NT (Number Theory).
- Suggested keywords: sextic reciprocity; Gauss sums; residue matrices; Eisenstein integers; spectral numerics; metaplectic theta functions; Lean 4; formal verification.
- Author: John Fairfax-Ball; institution/author-line format pending owner decision. No institution inferred.

## Code and proof links
- Repository: https://github.com/jfairfaxball-348/PRIMES
- Paper source: https://github.com/jfairfaxball-348/PRIMES/tree/main/paper (use the final release commit at upload).
- Numeric records: https://github.com/jfairfaxball-348/PRIMES/tree/main/reciprocity_spectra/results
- Frozen claims: https://github.com/jfairfaxball-348/PRIMES/blob/main/research/CONJECTURE_REGISTER.md
- Finite Lean package: https://github.com/jfairfaxball-348/PRIMES/tree/main/formalisation
- Independently verified finite comparator: https://github.com/jfairfaxball-348/PRIMES/actions/runs/40569785577
- Scoped cloud Lean verification: https://github.com/jfairfaxball-348/PRIMES/actions/runs/40569785692

## AI-use disclosure
OpenAI's ChatGPT was used substantially in the Lean formalisation and assisted with drafting and editing the manuscript. The author remains responsible for the mathematical claims, experimental data, verification, interpretation and final manuscript. Exact underlying model identifiers were not consistently recorded, so none are claimed. Automated proof checking covers selected finite identities only, not the asymptotic conjectures or the manuscript as a whole.

## Release package checklist (owner approval required)
- [ ] Confirm final title and abstract wording.
- [ ] Confirm author name, affiliations and contact details.
- [ ] Select an arXiv preprint licence separately from the repository's Apache-2.0 code licence.
- [ ] Confirm arXiv account and math.NT endorsement eligibility if needed.
- [ ] Approve intended journal and submission order.
- [ ] Recompile the exact final Git SHA with all cited vector figure PDFs, sections and bibliographic sources; inspect every page and PDF metadata.
- [ ] Check that all 3 conjectures and historical FAIL outcomes remain explicit, and verify no unresolved citations or missing fonts.
- [ ] Prepare an arXiv source bundle containing paper/main.tex, sections/*.tex, references.bib, figures/generated/*.pdf and any required class/style files; confirm no temporary build artefacts.
- [ ] Upload only on a separately explicit owner instruction (none in RS-S042).

## Single owner-decision list
Final title; exact author/institution line; arXiv distribution licence; endorsement if required; target journal. Any external upload or contact requires explicit separate authorization.
