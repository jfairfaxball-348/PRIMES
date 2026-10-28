# Reciprocity Spectra paper workspace (RS-S042 internal revision)

Build reproducibly from the repository root:

```sh
python -m pip install matplotlib numpy
python paper/figures/make_all.py
make -C paper
```

The figure script reads only committed `reciprocity_spectra/results/` JSON. Each of the fourteen figures gets a vector PDF and PNG preview in `paper/figures/generated/` (generated files are not evidence; source JSON is the evidence). Run `make -C paper clean` to remove TeX intermediates. Figures named “conceptual” or “illustrative” are not numerical support for conjectures. Frozen RS-S015/RS-S017 failures remain in the paper. All proofs and source claims must be checked against their referenced repository files before submission. No registration, arXiv submission or journal submission has occurred.

**RS-S041 build:** [GitHub Actions run 40587444244](https://github.com/jfairfaxball-348/PRIMES/actions/runs/40587444244) PASS on code head `62751c4`: fourteen PDF+PNG figure pairs, Ruff, compiled manuscript PDF and `rs-s041-paper-preview` artifact. Exact references/layout/numeric audit are RS-S042 tasks. No external submission.


**RS-S042:** The paper now cites twelve of fourteen reproducible figures; the two box-heavy schematic panels remain reproducible but are deliberately excluded from the manuscript. The title-page draft label and short-paper table of contents were removed. RS-S021's preregistered bin tolerance was corrected to ±0.12; all twelve observed differences were within ±0.05. See NUMERICAL_SOURCE_AUDIT.md and ARXIV_METADATA.md. No external submission is authorized or performed. A build fails if any referenced figure PDF is missing.
