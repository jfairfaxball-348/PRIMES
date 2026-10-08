# E015 D1-46 fixed D15 discovery command — pre-generation checkpoint

**Authorized phase:** D15 only. **Source/test commit:** `344b237bde1427b287a7fb8dd10cd3f56d327574`. The source Git blob is `8f4e4dfc7ddfc771ea6fba4e48a264c454cd25a1`; test blob `f2b0b560fb5738baba94eb6fd930dd2e2642e545`. Both were independently checked against the exact compiled/tested local bytes before D15 generation.

Working directory: repository root. Execute **this entire identical command twice** with the same code bytes and the same output path. Capture first-run bytes outside the command before running it again, compare bytes and SHA-256 before parsing or inspecting any result. This command authorizes exclusively low `[0,9056)` then directly segmented D15 `[81_000_000,82_000_000)`; H15/A15 and guards stay inaccessible.

```bash
python experiments/E015_square_shell_euclidean_remainder_quartile_shapes.py --phase D15 --implementation-commit 344b237bde1427b287a7fb8dd10cd3f56d327574 --output research/evidence/E015_D15_discovery.json
```

No flag, path, range, phase, generator strategy, selection criterion, output field or source change between runs is permitted. No H15/A15 execution belongs to this checkpoint.
