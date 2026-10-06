# E002 — Frozen Cross-Scale Persistence Test

**Stage:** replication  
**Queue item:** SQ-002  
**Related task:** D1-03 / SQ-002  
**Status:** FROZEN / NOT YET EXECUTED  
**Freeze date:** 2026-10-06

This file freezes the E002 cross-scale persistence design before any E002 prime-derived result is generated or inspected. E001, D0, H0, the D1-02 no-candidate triage, and the statuses of OBS-001 through OBS-004 remain frozen historical facts. OBS-004 is REFUTED and is not part of E002.

## Purpose

Test whether the three replicated E001 phenomena persist at increasing prime-value magnitudes without changing their definitions.

E002 is a targeted persistence test, not a new representation search. It may report only the predeclared criterion evidence needed for OBS-001, OBS-002, and OBS-003. It must not mine new motifs, finite-difference orders, moduli, thresholds, occupancy features, event neighbourhoods, or other representations.

## Frozen historical exclusions

E002 must not generate or inspect prime-derived results from:

- E001 discovery D0 = `[0, 1_000_000)`;
- E001 holdout H0 = `[1_000_000, 2_000_000)`;
- reserved adversarial A0 = `[10_000_000, 11_000_000)`.

A0 remains reserved and untouched for a later adversarial unit.

## Frozen scale ladder

All ranges are half-open value intervals. Every E002 band has width exactly 1,000,000.

| Band | Range |
|---|---|
| S1 | `[2_000_000, 3_000_000)` |
| S2 | `[4_000_000, 5_000_000)` |
| S3 | `[8_000_000, 9_000_000)` |
| S4 | `[16_000_000, 17_000_000)` |
| S5 | `[32_000_000, 33_000_000)` |

These five bands are mutually disjoint and disjoint from D0, H0, and A0.

### Scale-ladder rationale

The lower endpoints follow the deterministic geometric sequence `2^k × 1_000_000` for `k = 1, 2, 3, 4, 5`, while the band width is held fixed at the E001 width of 1,000,000. Holding width fixed isolates persistence with increasing value magnitude instead of simultaneously changing both location and sample-window width. The geometric spacing provides a simple increasing-scale test without choosing ranges in response to observed prime behaviour. S1 through S5 were selected before any E002 result exists.

This design tests persistence across band origin/value scale only. It does not establish persistence under arbitrary band widths, arbitrary origins, all sufficiently large values, or asymptotic limits.

## Frozen E001 feature semantics

For every E002 band, only primes lying inside that band participate. Sequential windows crossing a band boundary are excluded exactly as in E001.

### OBS-001 criterion — third forward difference

For ordered in-band primes `q_1 < ... < q_n`, form exactly

`Δ^3 q_i = q_{i+3} - 3q_{i+2} + 3q_{i+1} - q_i`

for every wholly in-band four-prime window and no other window.

No finite-difference order other than 3 is part of E002.

**Per-band pass criterion:** value `0` must have strictly greater frequency than every nonzero third-difference value. A tie for the maximum is a failure. If a band contains too few primes to define any third difference, the criterion fails.

The serialized criterion evidence must include the zero count, the highest-frequency competing value and its count under the repository's deterministic tie rule, and the boolean pass/fail result. Complete frequency tables may be used internally but must not be exposed for exploratory inspection in this targeted test.

### OBS-002 criterion — width-2 gap motif

For consecutive in-band prime gaps `g_i = q_{i+1} - q_i`, count every width-2 word `(g_i, g_{i+1})` wholly contained in the band, exactly as in E001.

No motif width other than 2 and no target motif other than `[6, 6]` is part of E002.

**Per-band pass criterion:** motif `[6, 6]` must have strictly greater frequency than every other width-2 motif. A tie for the maximum is a failure. If a band contains too few primes to define any width-2 gap motif, the criterion fails.

The serialized criterion evidence must include the `[6, 6]` count, the highest-frequency competing motif and its count under the repository's deterministic tie rule, and the boolean pass/fail result. Complete motif tables may be used internally but must not be exposed for exploratory inspection in this targeted test.

### OBS-003 criterion — directed reduced-residue transition support

Use exactly the frozen E001 modulus family:

`{6, 10, 12, 30, 60}`.

For each modulus `m`, apply E001's `reduced_residues_only=True` semantics exactly: remove prime divisors of `m`, reduce the remaining in-band primes modulo `m`, and take directed transitions between consecutive residues in that filtered sequence. Let `R_m` be the reduced residue system modulo `m`.

No modulus may be added, removed, or replaced in E002.

**Per-band pass criterion:** for every frozen modulus, the observed directed transition support must equal the full Cartesian product `R_m × R_m`. Any missing allowed ordered pair for any frozen modulus is a failure. No frequency threshold is imposed.

The serialized criterion evidence must include, for each modulus, the possible support size, observed distinct support size, the deterministically ordered list of missing allowed pairs, and the boolean pass/fail result.

## Frozen overall persistence outcomes

For each of OBS-001, OBS-002, and OBS-003 independently:

- **E002 PERSISTENT:** its per-band criterion passes in all five bands S1 through S5.
- **E002 NOT PERSISTENT:** its per-band criterion fails in one or more of S1 through S5.

The execution must still evaluate all five predeclared bands even if an earlier band fails. No early stopping, replacement band, added band, threshold, or revised criterion is permitted after E002 output exists.

An E002 NOT PERSISTENT result does not rewrite the frozen truth of the original D0/H0 observations. It records failure of this separately predeclared cross-scale persistence test.

## Implementation and artifact constraints for the next unit

1. Use exact integer arithmetic only.
2. Use no randomness.
3. Preserve the exact E001 band-boundary and feature semantics above.
4. Implement only the three targeted criterion families; do not serialize unrelated E001 grid output.
5. JSON output must use stable key ordering and deterministic ordering for values, motifs, moduli, and missing residue pairs.
6. Include the experiment ID, implementation commit, all five band definitions, frozen modulus family, and criterion results.
7. Execute the same full E002 command twice before criterion inspection solely to verify byte determinism; record byte size and SHA-256.
8. Validate implementation semantics before generating E002 results.
9. A0 must not be generated or inspected.

## Execution stop rule

The later E002 execution unit ends after all five frozen bands have been evaluated against only these three frozen criteria, deterministic evidence has been committed, and authoritative ledgers have recorded the E002 persistence outcomes. Do not create a candidate, perform mechanism work, run a collision/prior-art audit, start proof work, inspect A0, or mine E002 for additional phenomena in the same unit.

## Preflight stop rule

D1-03 ends when this specification and the corresponding authoritative state are committed and consistency-checked. No E002 implementation execution or new prime-derived result belongs to this preflight.
