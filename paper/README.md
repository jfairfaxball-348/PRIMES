# RS-S041 paper workspace

Build reproducibly from the repository root:

```sh
python -m pip install matplotlib numpy
python paper/figures/make_all.py
make -C paper
```

The figure script reads only committed `reciprocity_spectra/results/` JSON. Each of the fourteen figures gets a vector PDF and PNG preview in `paper/figures/generated/` (generated files are not evidence; source JSON is the evidence). Run `make -C paper clean` to remove TeX intermediates. Figures named “conceptual” or “illustrative” are not numerical support for conjectures. Frozen RS-S015/RS-S017 failures remain in the paper. All proofs and source claims must be checked against their referenced repository files before submission. No registration, arXiv submission or journal submission has occurred.
