# E003 — Frozen Event-Centred Neighbourhood Discovery

**Stage:** discovery  
**Queue item:** SQ-003  
**Related task:** D1-07 / SQ-003  
**Status:** FROZEN / NOT YET EXECUTED  
**Freeze date:** 2026-10-06

This file freezes the E003 event-centred neighbourhood design before any E003 prime-derived result is generated or inspected. All E001/E002 definitions and outcomes, both no-candidate triages, OBS-001 through OBS-004 statuses, FAIL-003, and the D1-05 reserve recovery remain frozen historical facts.

## Purpose

Search for exact repeated local configurations and exact before/after asymmetries around three predeclared event classes without steering from known prime theory or prior-art search.

E003 is a new discovery experiment. It does not retune E001/E002, does not mine their artifacts, and does not use A1.

## Frozen historical exclusions

E003 must not generate, inspect, or repurpose:

- E001 D0 = `[0, 1_000_000)`;
- E001 H0 = `[1_000_000, 2_000_000)`;
- E002 S1 = `[2_000_000, 3_000_000)`;
- E002 S2 = `[4_000_000, 5_000_000)`;
- E002 S3 = `[8_000_000, 9_000_000)`;
- historical A0 = `[10_000_000, 11_000_000)`, contaminated-by-generation and retired;
- E002 S4 = `[16_000_000, 17_000_000)`;
- E002 S5 = `[32_000_000, 33_000_000)`;
- replacement SQ-002 adversarial reserve A1 = `[33_000_000, 34_000_000)`, which remains FROZEN / UNTOUCHED / UNINSPECTED / NOT EXECUTED.

No E003 code path may traverse A1.

## Frozen E003 partition

All target ranges are half-open and have width

`W = 1_000_000`.

The partition is selected from committed generation metadata only.

Let `U_A1 = 34_000_000`, the exclusive upper endpoint of A1. Define the discovery lower endpoint as the first million-aligned endpoint **strictly greater** than `U_A1`:

`L_D = W * (floor(U_A1 / W) + 1) = 35_000_000`.

Then define:

- **Discovery D3:** `[35_000_000, 36_000_000)`;
- leave one full-width guard band `[36_000_000, 37_000_000)` unused;
- **Untouched holdout H3:** `[37_000_000, 38_000_000)`;
- **Adversarial A3:** let `L_A = 2 * L_D = 70_000_000`, so A3 = `[70_000_000, 71_000_000)`.

This rule uses only A1 metadata, the established one-million width, and arithmetic. It uses no prime values, event counts, E001/E002 criterion values, or observed E003 behaviour.

### Untouched provenance

FAIL-003 records the greatest integer ever traversed by a committed or discarded PRIMES prime-generation path as 32,999,999. D1-05 established that A1 begins at 33,000,000 and remains ungenerated. No committed generation provenance reaches 33,000,000 or above.

Therefore D3, H3, and A3 are all strictly beyond A1, mutually disjoint, disjoint from every previously generated/evaluated range, and untouched at this freeze.

E003 execution is phased:

1. discovery may generate D3 only;
2. H3 remains untouched until any D3 observations and their exact one-shot replication criteria are frozen;
3. A3 remains untouched until a later adversarial unit;
4. A1 is never an E003 target.

## Primitive band semantics

For one E003 band `[L,U)`, let

`q_0 < q_1 < ... < q_{n-1}`

be exactly the primes satisfying `L <= q_i < U`.

All sequential objects are band-local. No gap, neighbourhood, or transition may use a prime outside the selected band.

Define in-band gaps

`g_i = q_{i+1} - q_i`

for `0 <= i < n-1`.

No floating-point arithmetic is permitted anywhere in E003.

## Event class E3-DENSE — local prime-dense occupancy blocks

Occupancy block width is frozen at

`B = 1_000`.

Blocks are globally anchored:

`I_k = [1000k, 1000(k+1))`.

For a candidate anchor block `I_k`, define the exact occupancy

`c_j = # { q in band : q in I_{k+j} }`.

Frozen radii:

- event-selection radius: `r_select = 2` blocks;
- descriptive neighbourhood radius: `R_block = 8` blocks.

An anchor is eligible for classification only if every block `I_{k-8}, ..., I_{k+8}` lies wholly inside the E003 band.

A **prime-dense event** occurs exactly when

`c_0 > c_{-2}, c_{-1}, c_1, c_2`.

All four inequalities are strict. Any tie means the anchor is not dense. There is no numerical occupancy cutoff and no post-result threshold fitting.

## Event class E3-SPARSE — local prime-sparse occupancy blocks

Using the same globally anchored width-1,000 blocks and the same eligible-anchor rule, a **prime-sparse event** occurs exactly when

`c_0 < c_{-2}, c_{-1}, c_1, c_2`.

All four inequalities are strict. Any tie means the anchor is not sparse. There is no numerical occupancy cutoff and no post-result threshold fitting.

Because both classes use strict opposite inequalities, one anchor cannot be both dense and sparse.

## Event class E3-RECORD — strict rolling-record gaps

This is a new SQ-003 event class and must not be confused with E001 G5's historical **strict global record-gap** definition.

Frozen descriptive gap radius:

`R_gap = 8`.

Frozen record lookback:

`L_record = 8 * R_gap = 64` preceding in-band gaps.

For the full in-band gap sequence `g_0, ..., g_{n-2}`, a gap `g_i` with `i >= 64` is a **strict rolling-record gap** exactly when

`g_i > max(g_{i-64}, ..., g_{i-1})`.

All 64 inequalities are strict. Equality with the lookback maximum is not a record. Gaps with `i < 64` are not record-event candidates.

Record status is computed on the complete in-band gap sequence before neighbourhood-boundary filtering.

A strict rolling-record event is serializable only if all gaps `g_{i-8}, ..., g_{i+8}` exist inside the band. A record event lacking the full descriptive radius is omitted from neighbourhood summaries and counted in `boundary_omission_count`. There is no padding, wrapping, or cross-band completion.

The lookback 64 is fixed algebraically from the frozen radius rather than from observed prime behaviour. This local record definition is chosen before E003 execution so the experiment can obey the A1 generation exclusion without reconstructing the prime prefix through excluded ranges.

## Frozen neighbourhood encodings

### Dense and sparse block events

For each eligible dense or sparse event, serialize in offset order `-8, -7, ..., 0, ..., 7, 8`:

1. **raw occupancy word**
   `C = (c_{-8}, ..., c_0, ..., c_8)`;
2. **centered residual word**
   `R = (c_{-8}-c_0, ..., 0, ..., c_8-c_0)`;
3. **outer integer asymmetry vector**
   `A = (c_{+3}-c_{-3}, c_{+4}-c_{-4}, ..., c_{+8}-c_{-8})`;
4. **outer asymmetry sign signature**
   `S = (sgn(A_3), ..., sgn(A_8))`, where `sgn(x)` is exactly -1, 0, or +1.

Offsets 1 and 2 are deliberately excluded from the promotable asymmetry signature because they participate in event selection.

The event coordinate is the integer block start `1000k`.

### Strict rolling-record-gap events

For each serializable rolling-record event at gap index `i`, serialize in offset order `-8, -7, ..., 0, ..., 7, 8`:

1. **raw gap word**
   `G = (g_{i-8}, ..., g_i, ..., g_{i+8})`;
2. **centered residual gap word**
   `R_g = (g_{i-8}-g_i, ..., 0, ..., g_{i+8}-g_i)`;
3. **integer asymmetry vector**
   `A_g = (g_{i+1}-g_{i-1}, ..., g_{i+8}-g_{i-8})`;
4. **asymmetry sign signature**
   `S_g = (sgn(A_{g,1}), ..., sgn(A_{g,8}))`.

The event coordinate is the pair of prime endpoints `(q_i, q_{i+1})` plus the in-band gap index `i`.

## Exact descriptive output allowlist

E003 may serialize only:

1. experiment/implementation metadata and the exact selected band;
2. frozen parameter values and event-class names;
3. prime summary: count, first in-band prime, last in-band prime;
4. dense/sparse eligible-anchor counts, event counts, and event catalogs;
5. record-event raw count, serializable count, and boundary omission count;
6. for every serialized event, its coordinate and the four frozen neighbourhood encodings above;
7. complete exact frequency tables for each raw word, centered residual word, integer asymmetry vector, and asymmetry sign signature within each event class;
8. deterministic top-20 convenience rankings of those same tables;
9. the exact promotion-pool records defined below.

No other transform is allowed. In particular E003 must not emit fitted curves, normalized floating statistics, p-values, entropy scores, correlations, unlisted moduli, unlisted block widths, alternative radii, smoothed series, plots, or post-result threshold variants.

## Deterministic frequency and serialization rules

Event-class order is frozen as:

1. `prime_dense`;
2. `prime_sparse`;
3. `strict_rolling_record_gap`.

Event catalogs are sorted:

- dense/sparse: increasing anchor-block start;
- record gaps: increasing left prime endpoint, then right endpoint, then gap index.

Tuple-valued frequency tables are serialized as arrays of `{"value": [...], "count": N}` entries sorted lexicographically by the integer tuple.

Top-20 rankings are sorted by:

1. descending count;
2. lexicographically ascending integer tuple.

All JSON keys use stable lexical ordering. The canonical writer is equivalent to

`json.dumps(payload, sort_keys=True, indent=2) + "\n"`

with UTF-8 encoding and no timestamps, host paths, random IDs, or other nondeterministic fields.

The same command on the same implementation commit must produce byte-identical output.

## Frozen observation-promotion grammar

SQ-003 has a hard promotion cap of **5 observations**.

A D3 pattern is eligible for an `OBS-###` only if all of the following hold:

1. it uses exactly one frozen event class and one of the four frozen serialized object families for that class: raw word, centered residual word, integer asymmetry vector, or asymmetry sign signature;
2. the applicable event class has at least 20 serializable D3 events;
3. one exact target tuple is the **strict unique mode** of that object's complete D3 frequency table;
4. the target occurs at least 3 times;
5. the statement is not a restatement of an event-selection condition, a boundary rule, a deterministic encoding identity, or a tie-breaking rule;
6. for dense/sparse asymmetry claims, only the predeclared outer offsets 3 through 8 may participate;
7. for rolling-record-gap claims, the observation cannot consist only of the definitional fact that the centre gap exceeds the preceding 64 in-band gaps;
8. the exact statement and one-shot H3 replication criterion are written to the observation ledger before H3 is generated.

If more than five non-duplicate patterns satisfy these rules, rank the promotion pool deterministically by:

1. object-family priority: raw word, centered residual word, integer asymmetry vector, asymmetry sign signature;
2. descending dominance margin `mode_count - runner_up_count`;
3. descending mode count;
4. event-class order above;
5. lexicographically ascending target tuple.

Promote at most the first five patterns that survive the definitional/triviality exclusions. Equivalent restatements of the same exact fact consume only one slot.

Visual impressions, approximate distribution shifts, one-off extreme events, or merely low-frequency anomalies are not OBS-eligible.

## Frozen one-shot H3 replication rule

Every promoted E003 observation must freeze its exact H3 criterion before any H3 generation.

For an observation asserting that target tuple `T` is the strict unique mode of object family `F` in event class `E`, H3 replication succeeds exactly when:

1. H3 is evaluated with the unchanged E003 event definitions, radii, encodings, and serialization semantics;
2. event class `E` has at least 20 serializable H3 events;
3. the exact same target tuple `T` occurs at least 3 times;
4. `T` has strictly greater frequency than every competing tuple in the complete H3 frequency table for `F`.

A tie for the mode, fewer than 20 serializable events, fewer than 3 target occurrences, or any higher-frequency competitor is a failure of the frozen replication criterion.

H3 may be executed twice before inspection solely to establish byte determinism. H3 must not be mined for new patterns. A changed definition creates a new experiment and cannot reuse H3 as untouched holdout evidence.

## Generation-path guard

The E003 implementation must fail closed before producing prime-derived output if its generation plan can traverse an excluded range.

Frozen support allowance:

- low base-sieve support is permitted only inside `[0, 100_000)`, a region already generated historically;
- high-value prime generation must be segmented directly inside the currently authorized E003 target band.

For the D3 discovery unit, the only authorized high-value generation interval is D3 = `[35_000_000, 36_000_000)`.

The implementation must therefore:

1. reject any whole-prefix or `sieve(high)` strategy above 100,000;
2. record every requested prime-generation interval before generation;
3. assert that every interval above 100,000 is a subset of the currently authorized target band;
4. assert that no interval intersects A1, H3, A3, either guard band, or any other non-target high-value range;
5. use only base primes at most `floor(sqrt(U-1))` for the active segmented target, which is below 100,000 for every frozen E003 band;
6. include tests that deliberately attempt an excluded traversal and verify a hard failure before prime generation.

For a later H3 unit, the high-value allowlist changes to H3 only. For a later A3 unit, it changes to A3 only. A1 is never placed on the E003 allowlist.

## Validation obligations for the execution unit

Before D3 generation, the implementation must test:

- globally anchored width-1,000 occupancy semantics;
- full-radius block-boundary exclusion;
- strict dense/sparse inequalities and tie rejection;
- strict 64-gap rolling-record semantics, including equal-lookback-maximum non-records;
- record classification before boundary omission;
- exact neighbourhood coordinates and offset ordering;
- asymmetry/sign encodings;
- deterministic event/frequency/ranking order;
- byte-deterministic serialization;
- generation-path guard rejection of A1/H3/A3/non-target traversal.

Only after those tests pass may D3 be generated.

## Stop rule for this preflight

D1-07 ends when this specification and the corresponding authoritative state are committed and consistency-checked.

This unit does **not** implement or execute E003, generate D3/H3/A3, generate or inspect A1, rerun E001/E002, mine historical artifacts, create an observation or candidate, perform mechanism/proof work, or run a prior-art/collision audit.
