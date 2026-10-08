# E016 D1-49 / SQ-016 — complete pinned D16 discovery command

**PRE-GENERATION CHECKPOINT.** Execute exactly the complete one-line command below, unaltered, **twice** from repository root. Both executions must use exactly the same implementation source and output path. Seal the entire first artifact before the second execution; byte-compare sealed and replay bytes and SHA-256 before inspecting any descriptive result.

**Pinned implementation source-and-test commit:** `01f9c3eb63ced60eebda4f590338ebda57ce5910`. Frozen evaluator blob `6da57860b3279fc646549092b8129f1a592de2fe` and synthetic test blob `1babe24a3f8ec4ee0b5e2a6a0dbe6c5d75569d9f`. This command checkpoint must itself be committed and independently blob-verified before any D16 prime generation.

```bash
python experiments/E016_central_binomial_odd_valuation_carry_shapes.py --phase D16 --implementation-commit 01f9c3eb63ced60eebda4f590338ebda57ce5910 --output research/evidence/E016_D16_discovery.json
```

**Strict generator allowlist per entire run, in order:** (1) `base_sieve_support`, `whole_prefix`, `[0,9328)`; (2) `segmented_target`, `segmented`, `[86_000_000,87_000_000)`. Full plan checked before first generator entry and at both boundaries, all 380/30/150 metadata checks zero violations. H16/A16/G16 and all historical protected/calibration intervals are inaccessible. Do not run any alternate command, added pass, other target, helper, per-anchor oracle, or high whole-prefix. D16 discovery only; STOP before H16.
