# Results

`pilot_2026-10-24.json` holds every number quoted in `../README.md` and `../CONJECTURES.md`.

Provenance:

- matrices from `native/residue_matrix.c`; the pilot builds are byte-identical to the committed
  builder;
- analysis with numpy 2.5.3 and scipy 1.18.1 (`svds`, full SVD for the bulk moments);
- symmetry-matched random controls with seeds 0 and 1 (`scripts/spectra.py`, `structured_random`);
- the full pilot is reproduced by `scripts/run_pilot.sh 160000`.

Matrices themselves are not committed. They are deterministic and are rebuilt into `../data/`,
which is git-ignored.
