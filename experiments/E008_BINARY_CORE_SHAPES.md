# E008 — Frozen Binary Core-Shape Discovery

**Stage:** discovery
**Queue item:** SQ-008
**Related task:** D1-23 / SQ-008
**Status:** FROZEN / NOT YET EXECUTED
**Freeze date:** 2026-10-06

This file freezes E008 before any E008 prime-derived output is generated or inspected. All E001/E002/E003/E004/E006/E007 specifications, evidence, outcomes, observation statuses, no-observation/no-candidate results, and protected-range states remain immutable historical facts. SQ-005 remains calibration-only history: only its committed closure/quarantine state and generic process rules apply here; no E005 object, score, residual, historical comparison, hidden target, or source-derived mechanism is used to choose or justify E008.

## Purpose and qualitative distinction

E008 studies an exact digital representation of individual integer anchors: the shape of a fixed low-order binary core after removing the parity bit and excluding higher coordinates that can be constant across a one-million-wide band.

Prime anchors are compared with composite anchors drawn from the same predeclared small-prime-admissible integer domain. The control population removes direct divisibility by 2, 3, 5, and 7 before any promotable binary signature is compared.

This is qualitatively distinct from the executed novelty families:

- E001 used consecutive-prime gap motifs, finite differences, reduced-residue transitions, globally anchored occupancies, and strict global record-gap neighbourhoods;
- E003 used event-centred occupancy/gap neighbourhoods;
- E004 used projection/refinement structure of residue-transition fingerprints across moduli;
- E006 used additive translations of the prime indicator and all-pairs overlap counts;
- E007 used exact multiplicative factorization profiles of x-1 and x+1;
- E008 instead maps each individual admissible integer anchor to a fixed binary-coordinate word and studies four exact word-shape coarsenings.

E008 uses no consecutive-prime adjacency, prime-index difference, occupancy block, selected event, residue-transition table, modulus refinement, translation overlap, neighbouring factorization, fitted curve, floating normalization, Fourier object, or historical observation as a seed.

E008 is an observation generator only. It cannot create a candidate, perform mechanism/proof work, or run prior-art/collision/literature search.

## Frozen historical exclusions

No E008 code path may generate or inspect any historical protected/non-target novelty range.

Previously generated/evaluated novelty ranges remain historical only:

- E001 D0 = [0,1_000_000);
- E001 H0 = [1_000_000,2_000_000);
- E002 S1 = [2_000_000,3_000_000);
- E002 S2 = [4_000_000,5_000_000);
- E002 S3 = [8_000_000,9_000_000);
- historical A0 = [10_000_000,11_000_000), contaminated by generation and retired;
- E002 S4 = [16_000_000,17_000_000);
- E002 S5 = [32_000_000,33_000_000);
- E003 D3 = [35_000_000,36_000_000);
- E004 D4 = [39_000_000,40_000_000);
- E006 D6 = [42_000_000,43_000_000);
- E006 H6 = [44_000_000,45_000_000);
- E007 D7 = [46_000_000,47_000_000);
- E007 H7 = [48_000_000,49_000_000).

Protected untouched novelty ranges remain excluded:

- A1 = [33_000_000,34_000_000);
- H3 = [37_000_000,38_000_000);
- H4 = [41_000_000,42_000_000);
- A3 = [70_000_000,71_000_000);
- A4 = [78_000_000,79_000_000);
- A6 = [84_000_000,85_000_000);
- A7 = [92_000_000,93_000_000).

Frozen non-target guards remain excluded:

- E003 pre-D3 guard = [34_000_000,35_000_000);
- E003 post-D3 guard = [36_000_000,37_000_000);
- E004 G4-pre = [38_000_000,39_000_000);
- E004 G4-mid = [40_000_000,41_000_000);
- E006 G6-mid = [43_000_000,44_000_000);
- E007 G7-pre = [45_000_000,46_000_000);
- E007 G7-mid = [47_000_000,48_000_000).

The quarantined E005 calibration segments begin at 128,000,000 and are not novelty targets.

## Frozen E008 numerical partition

All E008 target/guard bands have width

W = 1_000_000.

Selection uses only committed generation provenance, frozen range metadata, the frozen width, and integer arithmetic.

The last valid novelty generation ends at the exclusive H7 boundary 49,000,000. Preserve the first untouched million-aligned band after H7 as a pre-discovery guard, then separate discovery and holdout by another full-width guard:

- **G8-pre:** [49_000_000,50_000_000) — frozen non-target guard;
- **Discovery D8:** [50_000_000,51_000_000);
- **G8-mid:** [51_000_000,52_000_000) — frozen non-target guard;
- **Untouched holdout H8:** [52_000_000,53_000_000).

The binary family has a predeclared coordinate regime: D8 and H8 lie in the 26-bit shell [2^25,2^26), where

2^25 = 33_554_432
and
2^26 = 67_108_864.

To stress the same frozen binary representation later in that same bit-length shell, define the adversarial lower endpoint as the greatest million-aligned lower endpoint whose full width-W band remains below 2^26:

L_A8 = W * floor((2^26 - W) / W) = 66_000_000.

Therefore:

- **Adversarial A8:** [66_000_000,67_000_000).

This same-shell edge rule is frozen before any E008 output and uses no prime behaviour. A8 is later than H8, remains entirely 26-bit, and is disjoint from every historical generated band, protected reserve/holdout, and guard. It is also disjoint from A3, A4, A6, and A7 and lies below all E005 calibration segments.

Execution is phased:

1. D8 may be generated only in the later D1-24 execution unit;
2. H8 remains untouched until any D8 observation and its exact same-family/same-target one-shot criterion are frozen;
3. A8 remains untouched for a later adversarial unit;
4. G8-pre and G8-mid are permanently non-target for E008;
5. every historical reserve/holdout/guard remains in its frozen role and is never an E008 target.

## Primitive anchor and artifact-control domain

Freeze the small-prime control wheel

Q = 2 * 3 * 5 * 7 = 210,

chosen by the target-agnostic rule “product of the first four primes.” Q is an artifact-control parameter only and is never promotable.

For an authorized E008 band B=[L,U), define the common admissible integer domain

A_B = {x in Z : L <= x < U and gcd(x,210)=1}.

Every prime in an E008 high-value band belongs to A_B because every such prime exceeds 7.

Partition A_B exactly into:

- P_B: anchors x that are prime;
- C_B: anchors x that are composite.

P_B and C_B are disjoint and exhaust A_B. The composite population is a frozen artifact control, not an independent discovery target.

Because gcd(x,210)=1 forces oddness, every anchor has least-significant binary bit b_0=1. Parity is therefore controlled before any promotable signature is formed.

## Frozen binary coordinate normalization

Every E008 target lies in [2^25,2^26), so every anchor has a unique 26-bit expansion

x = sum_{j=0}^{25} b_j 2^j,

with b_j in {0,1} and b_25=1.

Derive the largest uniformly varying low coordinate from the frozen band width alone:

J = floor(log2(W-1)) = 19.

For every bit position j <= J, a constant run of b_j has length at most 2^j <= 2^19 = 524,288 < W. Thus every full width-W integer interval crosses both bit values at each position 0 through 19. Positions 20 through 25 need not vary inside an arbitrary width-W band and are excluded from discovery to prevent a band-location prefix from becoming a promotable feature.

The parity bit b_0 is also excluded because it is fixed by the Q-admissible control domain.

Define the exact **binary core word**

w(x) = (b_19,b_18,...,b_1),

an ordered 19-bit tuple.

The exact word itself is not a promotable object and its complete word-frequency table must not be serialized. This prevents E008 from reducing to an exact residue-class catalog modulo 2^20.

## Frozen transform grammar

Exactly four promotable binary core-shape families are allowed, in this order.

### B1 — Hamming weight

B1(x) = sum of the 19 bits in w(x).

The signature is one integer in {0,...,19}.

### B2 — transition count

B2(x) is the number of adjacent coordinate pairs in w(x) whose bits differ.

There are 18 adjacent pairs, so the signature is one integer in {0,...,18}.

### B3 — longest zero/one runs

Let R_0(x) be the length of the longest contiguous run of zero bits in w(x), with R_0=0 if no zero occurs. Define R_1 analogously.

B3(x) = (R_0(x), R_1(x)).

### B4 — unordered run-length shape

Decompose w(x) into its maximal constant-bit runs and take their positive integer lengths. Sort those run lengths into nonincreasing order.

B4(x) is that sorted tuple. Its entries sum to 19. Bit labels and the original left-to-right run order are discarded.

No other transform is allowed. In particular E008 must not introduce:

- the exact 19-bit word as a promotable signature;
- exact low-bit residues or residue-transition objects;
- other bases, other bit windows, Gray-code variants, cyclic rotations, reversed words, bitwise XORs between different anchors, neighbour words, gap/index objects, occupancy/event objects, or factorization objects;
- fitted curves, floating normalization, p-values, entropy, correlations, spectral transforms, smoothing, or plots;
- post-result changes to Q, J, the bit order, family definitions, thresholds, or control population.

## Exact frequency and composite-control comparison

For each family F in B1-B4 and exact signature t, define:

- n_P^F(t): number of prime anchors in P_B with signature t;
- n_C^F(t): number of composite control anchors in C_B with signature t;
- N_P = |P_B|;
- N_C = |C_B|.

Use no division or floating point. Define the exact enrichment numerator

E_F(t) = n_P^F(t) * N_C - n_C^F(t) * N_P.

E_F(t)>0 is exactly equivalent to t having higher relative frequency among prime anchors than among the Q-admissible composite controls.

For each family, the only D8 target eligible for promotion is the strict unique mode of the complete prime-anchor frequency table. If the prime table has a tied maximum, that family has no promotable target. Lower-ranked signatures cannot be substituted.

## Frozen support floors

Derive the population floor from the frozen band width:

N_min = W / 1000 = 1000.

Both N_P and N_C must be at least 1000 for any promotion.

Freeze the target-occurrence floor as the least integer R satisfying R^2 >= N_min:

R = 32.

These thresholds are arithmetic design rules fixed before D8 output.

## Exact descriptive output allowlist

A future D8 execution may serialize only:

1. experiment/implementation metadata and exact selected band;
2. the frozen partition, Q, W, J, binary-shell bounds, family definitions, and generation plan;
3. anchor summary: |A_B|, N_P, N_C, first/last in-band prime anchor;
4. validation aggregates:
   - admissible-domain partition failure count;
   - 26-bit reconstruction failure count;
   - core-length failure count;
   - parity-control failure count among A_B;
5. for each B1-B4 in frozen order:
   - complete exact prime-anchor frequency table;
   - complete exact composite-control frequency table;
   - prime mode count and all maximizing signatures;
   - deterministic runner-up count when defined;
   - strict-unique-prime-mode boolean;
   - for the unique prime mode only, its composite count and exact enrichment numerator;
   - population-floor, occurrence-floor, enrichment, and overall mechanical-eligibility booleans;
6. the exact promotion records defined below.

No per-anchor prime list, per-anchor binary word, exact-word frequency table, alternative bit window, alternative control table, non-mode enrichment scan, or unlisted derived field may be serialized.

## Deterministic ordering and serialization

Frozen family order is B1, B2, B3, B4.

Signature ordering:

- B1 and B2: increasing integer;
- B3: lexicographic integer-pair order (R_0, then R_1);
- B4: lexicographic order of the nonincreasing integer tuples; if one tuple is an exact prefix of another, the shorter tuple sorts first.

Within a frequency ranking, sort by descending count and then the same canonical signature order.

Promotion records use family order B1 through B4 after duplicate suppression.

All JSON keys use stable lexical ordering. The canonical writer is equivalent to

json.dumps(payload, sort_keys=True, indent=2) + "\n"

with UTF-8 encoding and no timestamps, host paths, random IDs, or other nondeterministic fields.

The identical complete command on the same implementation commit must produce byte-identical output.

## Frozen triviality and artifact controls

The following are validation/control facts only and can never receive an observation:

1. b_0=1 for every anchor in A_B;
2. gcd(x,210)=1 and membership in the Q-admissible control domain;
3. every anchor has 26-bit length on D8/H8/A8;
4. reconstruction of x from its binary digits;
5. J=19 and exclusion of positions 20 through 25 follow from W and the fixed shell;
6. B1-B4 are deterministic coarsenings of the same binary core;
7. exact binary-core decoding to x modulo 2^20;
8. composite-control frequencies by themselves;
9. any serialization, ordering, or support-floor consequence.

A promotable record must additionally have positive exact enrichment against Q-admissible composite controls. Thus parity and direct divisibility by 3, 5, and 7 have already been matched before a binary shape can pass mechanically.

If eligible records from two families select exactly the same subset of D8 prime anchors, retain only the lower-numbered family record. Duplicate suppression can remove a record but can never substitute a lower-ranked target.

## Frozen observation-promotion grammar

SQ-008 has a hard promotion cap of **4 observations**, at most one from each B1-B4 family.

For family F, let t* be the strict unique mode of its complete D8 prime-anchor table. A record is OBS-eligible only if all of the following hold:

1. N_P >= 1000 and N_C >= 1000;
2. the prime-anchor table has exactly one mode t*;
3. n_P^F(t*) >= 32;
4. E_F(t*) > 0;
5. the statement is only the exact finite D8 fact that t* is the strict unique prime-anchor mode for family F, clears the occurrence floor, and has larger relative frequency among prime anchors than Q-admissible composite controls;
6. it is not one of the forced/control identities above;
7. it survives exact duplicate suppression.

Families are considered in order B1, B2, B3, B4. Because each family contributes at most one target and the global cap is four, there is no post-result cross-family score or discretionary ranking.

A tied prime mode, target count below 32, nonpositive enrichment numerator, population-floor failure, trivial/control identity, or duplicate suppression makes that family ineligible. No runner-up or alternate signature may replace it.

This selector has no multi-subscale aggregate score, so the calibration protocol's subscale-influence diagnostic is not applicable. Introducing an aggregate score, new family, reweighting, or alternate control after result inspection would define a new experiment and cannot repair E008.

## Frozen one-shot H8 criterion template

Every promoted D8 observation must have its exact family F and target signature t* written to the observation ledger before H8 generation.

H8 replication succeeds exactly when, under unchanged E008 semantics:

1. N_P >= 1000 and N_C >= 1000;
2. the exact same t* is the strict unique mode of the H8 prime-anchor table for family F;
3. n_{P,H8}^F(t*) >= 32;
4. the exact H8 enrichment numerator
   E_{F,H8}(t*) = n_{P,H8}^F(t*) N_{C,H8} - n_{C,H8}^F(t*) N_{P,H8}
   is strictly positive.

A tied or higher prime competitor, target count below 32, insufficient population, or nonpositive enrichment fails replication.

H8 may later be executed twice before criterion inspection solely to establish byte determinism. H8 must not be mined for new signatures. Any changed Q, J, binary core, family definition, support floor, control population, or target creates a new experiment and cannot reuse H8 as untouched evidence.

## Fail-closed future generation plan

E008 inherits the literal generation-path discipline of the novelty lane.

Low support:

- whole-prefix prime generation is allowed only inside historically safe generated support [0,100_000);
- for an authorized target [L,U), the implementation may request only exact base support through floor(sqrt(U-1)).

High-value generation:

- every prime-generation interval above 100,000 must be segmented directly inside the currently authorized E008 target;
- the complete generation plan must be constructed and validated before the prime generator is invoked;
- Q-admissibility and binary transforms are ordinary integer arithmetic and do not authorize any additional prime generation;
- every protected/non-target traversal must fail before prime generation.

For D8, the only authorized high-value prime-generation interval is exactly

[50_000_000,51_000_000).

The maximum base prime required is

floor(sqrt(50_999_999)) = 7141,

so an exclusive base-support endpoint may be at most 7142.

The D8 guard must reject before generation:

- any whole-prefix or sieve(high) strategy above 100,000;
- G8-pre, G8-mid, H8, A8;
- A1, H3, H4, G6-mid, A3, A4, A6, G7-pre, G7-mid, A7;
- every E003/E004 guard;
- every historical generated novelty band as a new target;
- any partial/expanded high interval not exactly authorized by the frozen execution mode.

For a later H8 unit, the high-value allowlist changes to H8 only; floor(sqrt(52_999_999))=7280, so exclusive low support may be at most [0,7281). For a later A8 unit, the allowlist changes to A8 only; floor(sqrt(66_999_999))=8185, so exclusive low support may be at most [0,8186). Historical reserves/guards are never E008 targets.

## Validation obligations for D1-24 before D8 generation

The later execution unit must test, before any D8 prime generation:

1. exact D8/G8/H8/A8 boundaries and 26-bit-shell membership;
2. exact Q=210 admissible-domain semantics on hand-checkable integers;
3. exact prime/composite partition semantics on a hand-checkable domain;
4. exact 26-bit decomposition and reconstruction;
5. J=19 derivation from W and the core ordering b_19 through b_1;
6. parity-bit exclusion and higher-coordinate exclusion;
7. exact B1 Hamming-weight semantics;
8. exact B2 transition-count semantics;
9. exact B3 longest-zero/one-run semantics, including absent-bit convention;
10. exact B4 maximal-run decomposition, nonincreasing sort, and tuple ordering;
11. complete frequency tables and canonical ordering for all four families;
12. strict-unique-mode detection and tie rejection;
13. exact integer enrichment arithmetic, including positive, zero, and negative cases;
14. population and occurrence floors;
15. exact duplicate suppression and four-observation cap;
16. descriptive allowlist shape, including absence of per-anchor words and exact-word tables;
17. byte-deterministic serialization;
18. fail-closed rejection of whole-prefix, partial-target, guard, holdout, adversarial, historical protected/generated, and other non-target traversals before the prime generator is called.

Only after every obligation passes may D8 be generated.

## Generic calibration-process safeguard

E008 is a separately frozen qualitative representation switch, not a repair or retuning of E007. The reason for switching families is target-agnostic: SQ-007 closed after its frozen finite observations did not justify a candidate, and the next novelty unit is required to explore a different declared representation.

No E005 selected/unselected object, score, residual, historical comparison, hidden target, or source-derived mechanism is transferred into E008. No E007 observed target or historical observation is combined with the binary family.

## Stop rules

### D1-23 preflight stop

D1-23 ends when this specification and corresponding authoritative state are committed and metadata-consistency checked.

This unit does **not** implement or execute E008, generate D8/H8/A8, generate any prime-derived output, inspect any protected reserve/holdout/guard, rerun or mine E001/E002/E003/E004/E006/E007, allocate an observation or candidate, perform mechanism/proof work, or run prior-art/collision/literature search.

### D1-24 discovery stop

The later D1-24 unit may implement E008, validate it, execute D8 twice for byte determinism, inspect only the frozen descriptive allowlist, and mechanically apply only the B1-B4 promotion grammar.

If D8 yields eligible records, D1-24 may allocate at most four OBS-### IDs and must freeze each exact H8 same-family/same-target criterion before any H8 generation. It must not generate H8 or A8, create a candidate, perform mechanism/proof work, or run prior-art/collision/literature search in that unit.

If no family is eligible, record **NO ELIGIBLE OBSERVATION**, leave H8/A8 untouched, and close SQ-008 without relaxing the grammar.
