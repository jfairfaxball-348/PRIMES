# E004 — Frozen Residue-Transition Factorization Discovery

**Stage:** discovery  
**Queue item:** SQ-004  
**Related task:** D1-09 / SQ-004  
**Status:** FROZEN / NOT YET EXECUTED  
**Freeze date:** 2026-10-06

This file freezes E004 before any E004 prime-derived result is generated or inspected. All E001/E002/E003 specifications, evidence, outcomes, observation statuses, no-candidate results, and the E003 no-observation result remain frozen historical facts.

## Purpose

Test exact projection and refinement relationships between directed reduced-residue transition fingerprints for a predeclared divisibility-related modulus family.

E004 is a blind discovery experiment. It may promote only exact non-definitional refinement/factorization patterns admitted by the grammar below. It must not rerun or mine E001/E002/E003, alter their outcomes, create a candidate, perform mechanism/proof work, or run a prior-art/collision audit.

The exact coarse-projection identity forced by residue reduction on the high E004 bands is a required correctness invariant, not an observation and never promotion-eligible.

## Frozen historical exclusions

E004 must not generate, inspect, or repurpose any of the following historical regions:

- E001 D0 = `[0, 1_000_000)`;
- E001 H0 = `[1_000_000, 2_000_000)`;
- E002 S1 = `[2_000_000, 3_000_000)`;
- E002 S2 = `[4_000_000, 5_000_000)`;
- E002 S3 = `[8_000_000, 9_000_000)`;
- historical A0 = `[10_000_000, 11_000_000)`, contaminated-by-generation and retired;
- E002 S4 = `[16_000_000, 17_000_000)`;
- E002 S5 = `[32_000_000, 33_000_000)`;
- replacement adversarial reserve A1 = `[33_000_000, 34_000_000)`, untouched/uninspected;
- E003 pre-D3 guard = `[34_000_000, 35_000_000)`;
- E003 D3 = `[35_000_000, 36_000_000)`, already executed;
- E003 post-D3 guard = `[36_000_000, 37_000_000)`;
- E003 H3 = `[37_000_000, 38_000_000)`, untouched/uninspected;
- E003 A3 = `[70_000_000, 71_000_000)`, untouched/uninspected.

A1, H3, and A3 retain their frozen historical roles and are not E004 targets.

## Frozen E004 partition

All target bands are half-open and have width

`W = 1_000_000`.

Selection uses only committed generation provenance and frozen range metadata.

The E003 holdout H3 ends at `U_H3 = 38_000_000`. Leave one full-width guard immediately after H3, then take the next million-aligned band:

- **E004 pre-discovery guard G4-pre:** `[38_000_000, 39_000_000)`;
- **Discovery D4:** `[39_000_000, 40_000_000)`.

Leave one full-width guard between discovery and holdout:

- **E004 discovery/holdout guard G4-mid:** `[40_000_000, 41_000_000)`;
- **Untouched holdout H4:** `[41_000_000, 42_000_000)`.

Use the same metadata-only later-scale rule used by E003 for the adversarial lower endpoint:

`L_A4 = 2 * L_D4 = 78_000_000`.

Therefore:

- **Adversarial A4:** `[78_000_000, 79_000_000)`.

This rule depends only on the pre-existing one-million width, H3 metadata, and arithmetic. It uses no prime values, transition counts, E003 event output, or E004 behaviour.

### Untouched provenance at freeze

The greatest integer reached by any recorded PRIMES high-value prime-generation path after E003 D3 execution is 35,999,999. No recorded generation path reaches 36,000,000 or above.

Accordingly D4, H4, and A4 are untouched at this freeze. They are mutually disjoint, disjoint from every previously generated band, and disjoint from A1, H3, and A3. G4-pre and G4-mid are also frozen as non-target guard ranges.

E004 execution is phased:

1. discovery may generate D4 only;
2. H4 remains untouched until any D4 observations and their exact one-shot criteria are frozen;
3. A4 remains untouched for a later adversarial unit;
4. A1, H3, and A3 are never E004 targets.

## Frozen modulus family

Use exactly the historical E001/E002 modulus family, without adding or deleting a modulus:

`M = (6, 10, 12, 30, 60)`.

The family is reused because SQ-004 was declared to study factorization structure among the already-declared residue-transition representations. Reuse does not inspect or tune against historical transition counts.

For each modulus `m`, define the reduced residue system in ascending representative order:

`R_m = { r in {0,...,m-1} : gcd(r,m)=1 }`.

## Frozen relation graph

The E004 relation graph is the Hasse cover graph of divisibility restricted to `M`. Write an edge `d -> m` from the coarser modulus `d` to the finer modulus `m`.

The exact edge set, in frozen deterministic order, is:

1. `6 -> 12`;
2. `6 -> 30`;
3. `10 -> 30`;
4. `12 -> 60`;
5. `30 -> 60`.

Equivalently, `d | m` and there is no distinct `k in M` with `d | k | m`.

No non-cover relation is an independent discovery edge. Composite projection consistency, including the two paths from 60 to 6 through 12 and through 30, is validation-only.

## Primitive band and filtering semantics

For one authorized E004 band `[L,U)`, let

`q_0 < q_1 < ... < q_{n-1}`

be exactly the primes in that band.

For each modulus `m`, apply the unchanged E001 `reduced_residues_only=True` semantics:

1. remove any in-band prime that is a prime divisor of `m`;
2. reduce the remaining ordered primes modulo `m`;
3. form directed transitions only between consecutive entries of that filtered in-band sequence.

Because every E004 target has `L > 60 = max(M)`, no in-band prime can divide any frozen modulus. Thus the filtered prime sequence is the same for all five moduli on D4/H4/A4. This arithmetic fact is frozen before execution and is what makes exact count projection across an edge a required invariant.

No transition may use a prime outside the selected band. There is no cross-band completion or prefix context.

## Directed transition fingerprints

For each `m in M` and each `(a,b) in R_m x R_m`, define

`C_m(a,b)`

to be the exact number of directed transitions `a -> b` in the filtered in-band residue sequence.

The complete count table `C_m` is the transition fingerprint for modulus `m`.

Pairs are ordered lexicographically by source residue and then destination residue, both ascending. All counts are exact nonnegative integers.

The support set is

`S_m = { (a,b) : C_m(a,b) > 0 }`.

Support is descriptive only. Restating complete support at a modulus is not promotion-eligible in E004 because that would merely repeat the type of finite coverage already represented by OBS-003.

## Exact projection map and mandatory identity

For an edge `d -> m`, define the residue projection

`pi_{m->d}(A) = A mod d`

from `R_m` to `R_d`.

For a coarse transition `(a,b) in R_d x R_d`, define the projected fine count

`P_{m->d}(a,b) = sum C_m(A,B)`

over all `(A,B) in R_m x R_m` satisfying

`A mod d = a` and `B mod d = b`.

Define the projection residual

`E_{d,m}(a,b) = C_d(a,b) - P_{m->d}(a,b)`.

On every authorized E004 target, the common filtered sequence makes

`E_{d,m}(a,b) = 0`

for every edge and every coarse pair. This identity is definitional/arithmetic under the frozen high-band semantics. Any nonzero residual is an implementation/semantic failure and execution must stop. Zero projection residuals cannot receive an `OBS-###`.

## Refinement fibres

For an edge `d -> m` and a coarse residue `a in R_d`, define its ordered lift set

`L_{d,m}(a) = (A in R_m : A mod d = a)`

sorted by ascending `A`.

Because reduction of unit groups is surjective for every frozen edge, each lift set has the constant size

`h_{d,m} = phi(m) / phi(d)`.

For a coarse transition `(a,b)`, define the `h x h` refinement matrix

`X_{d,m}^{a,b}[i,j] = C_m(A_i,B_j)`

where `A_i` is the i-th lift of `a` and `B_j` is the j-th lift of `b`.

The matrix is serialized row-major. Let

`K_{d,m} = h_{d,m}^2`.

By the mandatory projection identity,

`sum_{i,j} X[i,j] = C_d(a,b)`.

### Object F1 — forbidden-lift mask

For each refinement matrix, serialize the row-major binary mask

`Z[i,j] = 1 iff X[i,j] = 0`, otherwise `0`.

A `1` is an exact forbidden fine transition within an observed coarse transition fibre. The all-zero mask contains no forbidden lift and is descriptive but not itself promotion-eligible.

### Object F2 — integer balance vector

For each row-major cell of a refinement matrix, define

`B[i,j] = K * X[i,j] - C_d(a,b)`.

Serialize the row-major integer vector `B`.

Its entries sum exactly to zero. The all-zero vector is equivalent to exact uniform refinement of that coarse transition.

### Object F3 — exact 2x2 minor system

For every row pair `i1 < i2` and column pair `j1 < j2`, in lexicographic pair order, define the exact determinant

`D(i1,i2,j1,j2) = X[i1,j1]*X[i2,j2] - X[i1,j2]*X[i2,j1]`.

Serialize the ordered determinant vector and the corresponding binary zero-mask

`M2 = 1 iff D = 0`, otherwise `0`.

A refinement matrix is **positive rank-one** exactly when every cell is positive and every 2x2 determinant is zero.

A refinement matrix is **uniform** exactly when every balance entry is zero. Uniform implies positive rank-one when the coarse count is positive, so duplicate promotion rules below suppress the weaker restatement.

## Exact descriptive output allowlist

E004 D4 may serialize only:

1. experiment/implementation metadata, exact selected band, frozen guards, and generation plan;
2. frozen modulus family, relation graph, reduced-residue lists, and lift-set metadata;
3. prime summary: count, first in-band prime, last in-band prime;
4. for each modulus: transition total, complete exact transition-count table, support size, and deterministically ordered missing allowed pairs;
5. for each relation edge and coarse pair: projected fine count and projection residual;
6. for each relation edge and coarse pair: ordered source/destination lifts, refinement matrix, forbidden-lift mask, balance vector, determinant vector, minor-zero mask, uniform boolean, and positive-rank-one boolean;
7. per-relation exact frequency tables needed by the frozen promotion grammar for nonempty forbidden masks, nonzero balance vectors, and nontrivial minor-zero masks;
8. relation-level booleans for complete-positive uniform refinement and complete-positive rank-one refinement;
9. the exact promotion-pool records defined below.

No other transform is allowed. In particular E004 must not emit floating normalization, fitted curves, p-values, entropy, correlations, alternative moduli or relation edges, alternative filtering, approximate matrix rank, smoothed counts, plots, or post-result threshold variants.

## Deterministic ordering and serialization

Frozen modulus order is:

`6, 10, 12, 30, 60`.

Frozen relation order is the five-edge order declared above.

Within a modulus:

- reduced residues ascend numerically;
- transition pairs sort lexicographically `(source,destination)`.

Within a relation and coarse pair:

- coarse pairs sort lexicographically;
- lift sets ascend numerically;
- refinement cells serialize row-major;
- 2x2 minors sort first by row-index pair, then by column-index pair.

Tuple/vector/mask frequency tables are arrays of `{"value": [...], "count": N}` sorted lexicographically by the integer tuple.

Convenience rankings, where emitted, sort by:

1. descending count;
2. lexicographically ascending value.

All JSON keys use stable lexical ordering. The canonical writer is equivalent to

`json.dumps(payload, sort_keys=True, indent=2) + "\n"`

with UTF-8 encoding and no timestamps, host paths, random IDs, or other nondeterministic fields.

The same complete command on the same implementation commit must produce byte-identical output.

## Frozen observation-promotion grammar

SQ-004 has a hard promotion cap of **5 observations**.

Only the following five exact pattern families are admissible.

### P1 — complete uniform refinement relation

For one frozen edge `d -> m`, P1 is eligible only if:

- every coarse pair in `R_d x R_d` has positive coarse count;
- every fine cell in every refinement matrix is positive;
- every refinement matrix is uniform.

This is one relation-level exact identity.

### P2 — complete positive rank-one refinement relation

For one frozen edge `d -> m`, P2 is eligible only if:

- every coarse pair in `R_d x R_d` has positive coarse count;
- every fine cell in every refinement matrix is positive;
- every 2x2 minor of every refinement matrix is zero;
- P1 is not already true for the same edge.

This is one relation-level exact factorization identity. P1 suppresses P2 on the same edge to avoid promoting a weaker duplicate.

### P3 — repeated nonempty forbidden-lift mask

For one frozen edge, consider only coarse pairs whose F1 forbidden-lift mask is nonempty.

P3 is eligible only if:

- at least 4 coarse pairs have nonempty masks;
- one exact nonempty mask is the strict unique mode of that complete nonempty-mask table;
- the target mask occurs at least 2 times.

The all-zero mask is excluded.

### P4 — repeated nonzero balance vector

For one frozen edge, consider only coarse pairs whose F2 balance vector is nonzero.

P4 is eligible only if:

- at least 4 coarse pairs have nonzero balance vectors;
- one exact nonzero vector is the strict unique mode of that complete nonzero-vector table;
- the target vector occurs at least 2 times.

The all-zero vector is excluded because complete uniformity is handled by P1.

### P5 — repeated nontrivial minor-zero mask

For one frozen edge, consider F3 minor-zero masks that are neither all-zero nor all-one.

P5 is eligible only if:

- at least 4 coarse pairs have such nontrivial masks;
- one exact nontrivial mask is the strict unique mode of that complete table;
- the target mask occurs at least 2 times.

The all-one mask is handled by P2; the all-zero mask is excluded as an absence of exact minor equalities.

### General promotion exclusions

A pattern cannot be promoted if it is only:

- the mandatory zero projection residual;
- a residue/lift enumeration identity;
- a serialization or ordering consequence;
- complete transition support by itself;
- the statement that balance entries sum to zero;
- a restatement of another promoted pattern on the same edge.

Any promoted observation must state one frozen edge, one admissible family, and, for P3-P5, one exact target tuple.

If more than five non-duplicate patterns qualify, rank the promotion pool deterministically by:

1. family priority `P1, P2, P3, P4, P5`;
2. for P3-P5, descending dominance margin `mode_count - runner_up_count`;
3. for P3-P5, descending target count;
4. frozen relation order;
5. lexicographically ascending target tuple for P3-P5.

For P1/P2, relation order resolves ties within the family.

Promote at most the first five surviving patterns. No visual, approximate, near-rank-one, low-frequency anomaly, or post-result variant is eligible.

## Frozen one-shot H4 criterion templates

Every promoted D4 observation must have its exact H4 target written to the observation ledger before H4 is generated.

For a P1 observation on edge `d -> m`, H4 replication succeeds exactly when the unchanged E004 semantics make every H4 coarse pair positive, every fine cell positive, and every refinement matrix uniform.

For a P2 observation, H4 replication succeeds exactly when every H4 coarse pair is positive, every fine cell is positive, and every 2x2 minor of every refinement matrix is zero. P1 need not become true on H4; the frozen P2 target is rank-one.

For a P3, P4, or P5 observation with exact target tuple `T`, H4 replication succeeds exactly when:

1. the unchanged object-family eligibility filter is applied;
2. at least 4 H4 coarse pairs enter that filtered table;
3. the exact same target `T` occurs at least 2 times;
4. `T` has strictly greater frequency than every competing tuple in the complete filtered H4 table.

A tie, too few eligible H4 coarse pairs, too few target occurrences, or a higher-frequency competitor fails the frozen criterion.

H4 may be executed twice before inspection solely to establish byte determinism. H4 must not be mined for new patterns. Any changed modulus, edge, filter, object, threshold, or identity creates a new experiment and cannot reuse H4 as untouched holdout evidence.

## Generation-path guard

The E004 implementation must fail closed before producing prime-derived output if its generation plan can traverse an excluded range.

Frozen support allowance:

- low base-sieve support is permitted only inside `[0, 100_000)`, which was generated historically;
- every high-value prime-generation interval must be segmented directly inside the currently authorized E004 target.

For D4 execution, the only authorized high-value generation interval is

`D4 = [39_000_000, 40_000_000)`.

The implementation must:

1. reject any whole-prefix or `sieve(high)` strategy above 100,000;
2. construct and record the complete generation plan before invoking prime generation;
3. assert that every interval above 100,000 is a subset of the currently authorized target;
4. reject any interval intersecting A1, either E003 guard, D3, H3, A3, G4-pre, G4-mid, H4, A4, or any other non-target high-value range;
5. use only base primes at most `floor(sqrt(U-1))` for the active segmented target; this lies below 100,000 for D4, H4, and A4;
6. test deliberate excluded traversals and verify hard failure before the prime generator is called.

For a later H4 unit, the high-value allowlist changes to H4 only. For a later A4 unit, it changes to A4 only. A1, H3, and A3 are never placed on the E004 allowlist.

## Validation obligations for the execution unit

Before any D4 generation, the implementation must test:

- exact reduced-residue enumeration for all five moduli;
- exact `reduced_residues_only=True` filtering, including a synthetic case containing a prime divisor of a modulus;
- exclusion of transitions crossing a band boundary;
- exact directed transition counts on a hand-checkable sequence;
- exact frozen relation graph and deterministic edge ordering;
- residue projection and lift-set enumeration for every edge;
- constant lift cardinality `phi(m)/phi(d)`;
- exact projection aggregation and zero residual on a common filtered sequence;
- composite projection path consistency, including both 60-to-6 paths;
- exact refinement-matrix row/column ordering;
- exact forbidden-mask and balance-vector semantics, including the zero-sum balance identity;
- exact 2x2 determinant ordering and positive-rank-one classification;
- P1-P5 eligibility, tie rejection, occurrence floors, duplicate suppression, and deterministic promotion ordering;
- exact identity/failure encoding;
- byte-deterministic serialization;
- generation-path guard rejection of A1/H3/A3, E003 ranges/guards, E004 guards/non-targets, and whole-prefix traversal before generation.

Only after these tests pass may D4 be generated.

## Stop rule for this preflight

D1-09 ends when this specification and corresponding authoritative state are committed and consistency-checked.

This unit does **not** implement or execute E004, generate D4/H4/A4, generate or inspect A1/H3/A3, rerun or mine E001/E002/E003, relax any historical grammar, create an observation or candidate, perform mechanism/proof work, or run a prior-art/collision audit.
