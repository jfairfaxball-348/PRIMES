# E001 H0 Replication — 2026-10-06

**Stage:** replication  
**Related task:** D1-01 / SQ-001  
**Frozen specification:** `experiments/E001_REPRESENTATION_GRID.md` (unchanged)  
**Frozen observation criteria:** `research/OBSERVATION_LEDGER.md` as committed before H0 generation  
**Implementation commit:** `beab213501dab318075199c3fcac6d5501d0b9d3`

## Execution boundary

Only untouched holdout H0 = `[1_000_000, 2_000_000)` was generated.

Reserved adversarial A0 = `[10_000_000, 11_000_000)` was not generated or inspected. H0 was inspected only as required to evaluate the four frozen replication criteria for OBS-001 through OBS-004. No new H0 observation was mined, no criterion was tuned, and no candidate, mechanism work, or prior-art search was started.

## Frozen-source and validation check before H0

The executable `experiments/E001_representation_grid.py` on `main` has Git blob SHA `01edecf0a1e992459807264fbf92bb816d242c7f`, exactly equal to the same file at implementation commit `beab213501dab318075199c3fcac6d5501d0b9d3`. The connector-backed local reconstruction also produced that exact blob SHA before execution.

Local validation on the exact reconstructed sources:

```text
PYTHONPATH=src pytest -q
14 passed

python -m compileall -q src experiments tests
success

ruff --version
command not found (exit 127)
```

The first reconstructed test invocation omitted the repository `pyproject.toml` and therefore failed import collection; the reconstruction was corrected to the exact committed `pyproject.toml` blob `dc4f15f98caf407eaaddd1506e1c323c5c2efbff`, after which all 14 tests passed before H0 generation. This was a local reconstruction issue, not an implementation-semantic defect.

The known CI-observability limitation also recurred: the available connector returned no combined-status objects and no PR-triggered workflow-run objects for either the frozen implementation commit or the then-current main head. These empty responses are not treated as CI pass/fail evidence. This reuses FAIL-002; no new repository defect is recorded.

## Deterministic H0 artifact

Command:

```bash
PYTHONPATH=src python experiments/E001_representation_grid.py \
  --band H0 \
  --code-commit beab213501dab318075199c3fcac6d5501d0b9d3 \
  --output /tmp/e001-h0.json
```

The identical H0 command was executed twice solely to verify byte determinism. The outputs were byte-identical.

- bytes: 25,557,012
- SHA-256: `80c8c49f1845e941764b31471404a8e674fa794394687cb6502dbd2eca980254`
- prime count: 70,435
- first prime: 1,000,003
- last prime: 1,999,993

Compact machine-readable criterion evidence is committed at `research/evidence/E001_H0_replication.json`. The full artifact is reproducible from the frozen specification, implementation commit, command, and digest above and is not duplicated in Git history.

## Frozen criterion results

1. **OBS-001 — REPLICATED.** Third forward difference value 0 is the unique H0 mode: 3,764 occurrences. The runner-up nonzero value is 12 with 3,408.
2. **OBS-002 — REPLICATED.** Width-2 gap motif `[6, 6]` is the unique H0 mode: 1,409 occurrences. The runner-up motif is `[6, 4]` with 1,335.
3. **OBS-003 — REPLICATED.** Directed reduced-residue transition support is complete for every frozen modulus: 4/4 for 6, 16/16 for 10, 16/16 for 12, 64/64 for 30, and 256/256 for 60. No allowed directed pair is missing.
4. **OBS-004 — REFUTED.** Exactly one globally anchored width-100 H0 block is empty. The first (and only) empty block is `[1_671_800, 1_671_900)`, with occupancy 0.

## Stop rule

D1-01 ends at the replication checkpoint. A0 remains untouched. No conjecture/candidate was created and no mechanism or prior-art work was performed. Candidate synthesis, if pursued for the replicated observations, is a separate bounded unit.
