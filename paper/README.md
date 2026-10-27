# RS-S041 paper workspace

Build reproducibly from the repository root:

```sh
python -m pip install matplotlib numpy
python paper/figures/make_all.py
make -C paper
```

The figure script reads only committed `reciprocity_spectra/results/` JSON. Each of the fourteen figures gets a vector PDF and PNG preview in `paper/figures/generated/` (generated files are not evidence; source JSON is the evidence). Run `make -C paper clean` to remove TeX intermediates. Figures named “conceptual” or “illustrative” are not numerical support for conjectures. Frozen RS-S015/RS-S017 failures remain in the paper. All proofs and source claims must be checked against their referenced repository files before submission. No registration, arXiv submission or journal submission has occurred.

**RS-S041 build:** [GitHub Actions run 40587444244](https://github.com/jfairfaxball-348/PRIMES/actions/runs/40587444244) PASS on code head `62751c4`: fourteen PDF+PNG figure pairs, Ruff, compiled manuscript PDF and `rs-s041-paper-preview` artifact. Exact references/layout/numeric audit are RS-S042 tasks. No external submission.


## RS-S042 internal editorial revision

The RS-S042 candidate keeps 12 evidentiary/conceptual figures in the manuscript; all 14 vector+PNG pairs still regenerate (the redundant boxed visual overview and verification-process diagram are no longer embedded). The key corrected source distinction is RS-S021's **pre-registered ±0.12** holdout threshold versus the tighter **observed ±0.05** residual range. See `NUMERICAL_SOURCE_AUDIT.md` for JSON-key/commit traceability and failure retention, and `ARXIV_METADATA.md` for copy-ready metadata, precise AI-use disclosure and unapproved owner-only submission decisions. No external upload/submission.
