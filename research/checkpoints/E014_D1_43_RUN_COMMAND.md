# E014 D1-43 — exact D14 discovery command checkpoint

**Purpose:** freeze D14-only execution before the first D14 prime-generation call; immutable E014 D1-42 specification, no H14/A14.

**Exact pre-generation implementation/test Git commit:** `a6a9d0f8066e5460fee9cac2c5e0dc700a62f1a1`.

**Verified Git blobs before generation:**
- `experiments/E014_primitive_three_cube_incidence_shapes.py`: `736789b92043b96366815c9a4ed24c882ca5718d`.
- `tests/test_e014.py`: `9515a2cce8ffb8f329dd660b499b8e1d7515e00b`.

**Exact complete runnable command** (run from repository root twice, with unchanged output path and code bytes):

```bash
PYTHONPATH=src:. python experiments/E014_primitive_three_cube_incidence_shapes.py --implementation-commit a6a9d0f8066e5460fee9cac2c5e0dc700a62f1a1 --output research/evidence/E014_D14_discovery.json
```

Only the fully checked D14 phase's ordered generator plan is permitted: low whole-prefix `[0,8775)` followed by directly segmented `[76_000_000,77_000_000)`. The frozen CLI, output basename and path, source bytes, pinned hash and JSON schema shall not be changed between repeats. Compare full bytes and SHA-256 from two complete runs before inspecting *any* descriptive output field; invalid schema, nonzero validation or disagreement fails closed. Never query H14/A14, a guard, historical protected band or E005 calibration segment. Do not invoke any other generator/primality helper.

**Validation before this command:** Python compilation PASS; focused metadata/synthetic/poison/schema pytest 7/7 PASS; Ruff unavailable in detached runner under previously recorded environment limitation. Source/tests committed and remote blob verified; the command itself must be separately committed and remote-verified before first valid call.
