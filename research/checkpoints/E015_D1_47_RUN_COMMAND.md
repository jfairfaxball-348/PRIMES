# E015 D1-47 fixed H15 one-shot OBS-021 replication command — pre-generation checkpoint

**Authorized phase:** H15 only. **Immutable target:** OBS-021 / R3 `[9,0,0,0]` under frozen unchanged H15 criterion. **Source/test commit:** `fe98ec9c931ad153fd4cb6912c4fc6d91c235b89` (evaluator blob `aa989185153fc979eb9349c051661ad6b19e8311`, tests blob `530aff578f0d37fa3a3462fd7dfbdf1e705904e0`). Original E015 D15 source Git blob remains `8f4e4dfc7ddfc771ea6fba4e48a264c454cd25a1`.

Working directory: repository root. Run this entire exact command **twice**, same source and test bytes and same output path. Seal the first complete output bytes outside this command before the second run; prove complete byte equality and SHA-256 equality **before** parsing or inspecting target-only canonical aggregate fields. No mode retarget, alternative signature, R30 positive-class criterion, additional H15 attempt, or changed thresholds.

```bash
python experiments/E015_H15_replication.py --phase H15 --implementation-commit fe98ec9c931ad153fd4cb6912c4fc6d91c235b89 --output research/evidence/E015_H15_replication.json
```

**The only allowed ordered prime-generator calls per execution:** first `base_sieve_support` `[0,9166)` with `whole_prefix`, then `segmented_target` H15 `[83_000_000,84_000_000)` with `segmented`. Entire plan and both entries are positively checked before first call and rechecked at each boundary. No other high interval, H15 extra pass, D15, A15, G15 guards, historical protection or calibration is authorized. This command is fixed before the first H15 prime call.
