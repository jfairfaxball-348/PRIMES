# E013 D1-39 immutable pre-generation run command

Frozen E013 specification: `experiments/E013_MODULAR_QUADRATIC_ORBIT_SHAPES.md`.

Exact validated source/test checkpoint (no D13 prime generation before this commit): `b9e1c7a9186cc066328022869d85793ecbdb02a5`.

Exact evaluator blob: `1ecc6f60b0c3527694123e39c740e8d128a223e8`.
Exact focused test blob: `fba632a16b820e311467aafe29389aef929c817d`.

Before prime generation: 9/9 focused pytest tests passed, Python compilation passed; Ruff unavailable in detached runner (existing FAIL-001/002 limitation). Metadata 305 disjointness comparisons and poison-generator negatives passed.

From repository root, execute the following **identical complete command twice**, same code checkpoint and output path. Compare output bytes and SHA-256 **before any descriptive-field inspection**:

```bash
PYTHONPATH=.:src python experiments/E013_modular_quadratic_orbit_shapes.py --band D13 --code-commit b9e1c7a9186cc066328022869d85793ecbdb02a5 --output /tmp/e013-d13.json
```

Only `[0,8545)` low whole-prefix plus directly segmented D13=`[72_000_000,73_000_000)` are authorized. No other target, support, or off-phase generation is permitted. This command/checkpoint file is not a change to E013 semantics or permission to execute H13/A13.
