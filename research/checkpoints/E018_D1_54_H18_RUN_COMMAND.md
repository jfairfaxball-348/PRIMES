# E018 D1-54 / S056: complete frozen one-shot H18 replication command

**Scope:** H18 [97_000_000,98_000_000) only; exact immutable OBS-022 L1=0 and OBS-023 L2=0 target-specific criteria. Neither D18 nor any historical, guard, off-phase or adversarial band is authorized. Source and focused poison tests were separately precommitted at complete checkpoint `7a7b265216506c7eadace5a6e9c92c417fce2741`; source Git blob `3f40417b3e9df0a9ec4f55df38f1544c3717d866`, tests Git blob `ec2e0b5828c70792a87a873a520818140184efef`. Before either generator: 10/10 focused synthetic/poison tests passed; Python compilation passed; Ruff unavailable and not claimed. Complete named-interval audit is 3,486 old pairs, 430 new comparisons, 30 E005 nested containments and 150 new/nested disjoint, and integer isqrt(97_999_999)=9899.

**The only ordered positive prime-generator calls per invocation:** `(base_sieve_support,0,9900,whole_prefix)`, followed by `(segmented_target,97000000,98000000,direct_segmented)`, with whole plan checked before generator entry and again at both boundaries. No individual high primality helper, extra traversal, fallback or retarget.

Execute **exactly twice**, without command changes, from the repository root on the identical output path:

```bash
python experiments/E018_H18_fixed_replication.py --phase H18 --implementation-commit 7a7b265216506c7eadace5a6e9c92c417fce2741 --output research/evidence/E018_H18_replication.json
```

**Mandatory replay protocol:** Seal first uninterpreted complete raw bytes before replay; compare every output byte and both SHA-256 hashes after the second identical execution, *before inspecting any descriptive aggregate*. Then apply both already frozen fixed-zero holdout criteria exactly once, independently as REPLICATED or REFUTED, including full schema/ten-zero-validator checks and L1-before-L2 exact support comparison. The run command file itself must be committed and remote-byte-verified before either generator call.
