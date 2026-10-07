# E009 — Frozen Unit-Action Cover-Shape Discovery

**Stage:** discovery  
**Queue item:** SQ-009  
**Related task:** D1-25 / SQ-009  
**Status:** FROZEN / NOT YET EXECUTED  
**Freeze date:** 2026-10-07

This file freezes E009 before any E009 prime-derived output is generated or inspected. All E001/E002/E003/E004/E006/E007/E008 specifications, executions, outcomes, observation statuses, no-observation/no-candidate results, generated-range provenance, and protected-range states remain immutable historical facts. SQ-005 remains calibration-only history: only its committed closure/quarantine state and generic process rules apply here. No E005 object, score, residual, historical comparison, hidden target, or source-derived mechanism is used to choose, define, rank, or interpret E009.

## Purpose and qualitative distinction

E009 studies an exact algebraic action representation of each admissible integer anchor. A fixed target-agnostic basis of four small integer units acts multiplicatively modulo the anchor. For every anchor, E009 computes the exact multiplicative orders of those four units and asks which subsets of the basis are sufficient, through least common multiple, to attain the full unit-group exponent of the anchor. The inclusion-minimal sufficient subsets form a canonical finite antichain, called the **unit-action cover shape**.

This is qualitatively distinct from every exhausted novelty family:

- E001 used consecutive-prime gap motifs, finite differences, reduced-residue transitions, globally anchored occupancies, and strict global record-gap neighbourhoods;
- E003 used event-centred occupancy/gap neighbourhoods;
- E004 used projection/refinement structure of residue-transition fingerprints across related moduli;
- E006 used additive translations of the prime indicator and all-pairs overlap counts;
- E007 used exact multiplicative factorization profiles of the two neighbouring integers x-1 and x+1;
- E008 used fixed binary-coordinate words of individual admissible anchors and exact digital shape coarsenings;
- E009 instead uses exact multiplicative actions of a fixed small basis **modulo the anchor itself**, canonically summarized by which basis subsets collectively attain the anchor's unit-group exponent.

E009 does not use consecutive-prime adjacency, gaps, prime-index differences, occupancy blocks, selected events, residue-transition tables, modulus-refinement matrices, additive translation overlaps, neighbouring-integer factorization profiles, digit/base words, fitted curves, floating normalization, Fourier objects, or any historical observation as a seed.

Factorization of the anchor and of its exact exponent is permitted only as deterministic arithmetic needed to compute the representation. Per-anchor factorization profiles, factor identities, exponent values, and order values are validation/control objects and are not promotable discovery signatures.

E009 is an observation generator only. It cannot create a candidate, perform mechanism/proof work, execute an adversarial test, or run prior-art/collision/literature search.

## Frozen historical exclusions

No E009 code path may generate or inspect any historical protected/non-target novelty range or repurpose any historical generated band.

Historical generated novelty ranges include:

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
- E007 H7 = [48_000_000,49_000_000);
- E008 D8 = [50_000_000,51_000_000).

Protected untouched novelty ranges remain excluded:

- A1 = [33_000_000,34_000_000);
- H3 = [37_000_000,38_000_000);
- H4 = [41_000_000,42_000_000);
- H8 = [52_000_000,53_000_000);
- A8 = [66_000_000,67_000_000);
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
- E007 G7-mid = [47_000_000,48_000_000);
- E008 G8-pre = [49_000_000,50_000_000);
- E008 G8-mid = [51_000_000,52_000_000).

The quarantined E005 calibration segments begin at 128,000,000. They are not E009 targets, controls, or support regions.

## Frozen E009 numerical partition

Every E009 target/guard band has width

W = 1_000_000.

Selection uses only committed generation provenance, frozen historical range metadata, the frozen width, and integer arithmetic. E008's untouched H8 ends at the exclusive boundary 53,000,000. Preserve the first million-aligned band after H8 as a full-width guard, then place discovery, another guard, and one-shot holdout consecutively:

- **G9-pre:** [53_000_000,54_000_000) — frozen non-target guard;
- **Discovery D9:** [54_000_000,55_000_000);
- **G9-mid:** [55_000_000,56_000_000) — frozen non-target guard;
- **Untouched holdout H9:** [56_000_000,57_000_000).

Use the established metadata-only later-scale rule for the adversarial lower endpoint:

L_A9 = 2 * L_D9 = 108_000_000.

Therefore:

- **Adversarial A9:** [108_000_000,109_000_000).

This rule uses no prime values, prime counts, historical observation values, E008 output, or E009 behaviour. The five E009 bands are mutually disjoint, disjoint from every historical generated novelty band, and disjoint from A1, H3, H4, H8, A8, A3, A4, A6, A7, all frozen guards, and all other protected/non-target novelty intervals. A9 remains below and disjoint from the quarantined E005 calibration segments beginning at 128,000,000.

Execution is phased:

1. D9 may be generated only in the later D1-26 execution unit;
2. H9 remains untouched until any D9 observation and its exact unchanged same-family/same-target criterion are frozen;
3. A9 remains untouched for a later adversarial unit;
4. G9-pre and G9-mid are permanently non-target for E009;
5. every historical reserve, holdout, guard, and generated novelty band remains in its frozen historical role and is never an E009 target.

## Primitive anchor domain and fixed action basis

Freeze the ordered basis

A = (2,3,5,7),

chosen by the target-agnostic rule “the first four primes in increasing order.”

Freeze the associated admissibility wheel

Q = 2 * 3 * 5 * 7 = 210.

Q and the choice/order of A are fixed arithmetic controls. Their prior appearance as an admissibility control in E008 is historical representation metadata only; no E008 result or target is used here.

For an authorized E009 band B=[L,U), define the common admissible integer domain

A_B = {x in Z : L <= x < U and gcd(x,210)=1}.

Every prime in an E009 high-value band belongs to A_B because every such prime exceeds 7.

Partition A_B exactly into:

- P_B: anchors x that are prime;
- C_B: anchors x that are composite.

P_B and C_B are disjoint and exhaust A_B. The composite population is an artifact control, not an independent discovery target.

Because gcd(x,210)=1, every basis element a in A is a unit modulo x.

## Exact factorization and unit-group exponent

For every x in A_B, factor x exactly and canonically as

x = product_i q_i^{e_i},

with distinct prime q_i in increasing order and positive exponents e_i.

No probabilistic factorization is permitted. A future implementation must use deterministic ascending trial division from the prevalidated low base-prime support and must reconstruct x exactly from the resulting factors.

Every E009 anchor is odd. Define the exact unit-group exponent

Lambda(x) = lcm_i( q_i^{e_i-1} * (q_i - 1) ).

For x>1 in every frozen E009 band, Lambda(x) is a positive integer. This value is the Carmichael exponent of the odd anchor, but the conventional name is not a promotion target and supplies no historical target.

The following are validation-only facts:

- exact factorization reconstructs x;
- every factor q_i is prime and factors are in canonical increasing order;
- Lambda(x) is the exact lcm of the declared prime-power terms;
- per-anchor factor lists, prime-power terms, and Lambda(x) values are not discovery signatures.

## Exact multiplicative-order semantics

For each a in A and x in A_B, define

ord_x(a) = min { k >= 1 : a^k == 1 (mod x) }.

The future implementation must compute this exactly from Lambda(x):

1. factor Lambda(x) exactly;
2. set m = Lambda(x);
3. visit the distinct prime divisors r of Lambda(x) in increasing order;
4. while r divides m and pow(a, m/r, x) = 1, replace m by m/r;
5. after all r are exhausted, set ord_x(a)=m.

All modular powers use exact integer modular exponentiation. The implementation must validate both:

- pow(a,ord_x(a),x)=1;
- for every prime divisor r of ord_x(a), pow(a,ord_x(a)/r,x) != 1.

Also ord_x(a) must divide Lambda(x). These are correctness invariants, never promotable observations.

No per-anchor order values or order vectors may be serialized in discovery output.

## Canonical subset system and cover predicate

Let S be the 15 nonempty subsets of A.

Every subset is represented canonically as an increasing tuple of bases and ordered globally by:

1. increasing subset cardinality;
2. lexicographic tuple order within the same cardinality.

For x in A_B and nonempty subset S, define

L_x(S) = lcm( ord_x(a) : a in S ).

Call S a **cover** of x exactly when

L_x(S) = Lambda(x).

Cover status is monotone under set inclusion: if S covers x, every superset T containing S also covers x. This monotonicity is a validation/control identity and is not promotion-eligible.

Define the canonical **minimal cover antichain**

M(x) = { S : S covers x and no proper nonempty subset of S covers x }.

M(x) may be empty when even the complete four-base set A fails to attain Lambda(x).

Serialize a minimal cover as its increasing base tuple. Serialize M(x) as the list of its member tuples in the frozen global subset order.

No alternative bases, added bases, removed bases, reordered bases, weighted lcm, approximate order, or post-result cover rule is permitted.

## Frozen transform grammar

Exactly four promotable unit-action cover-shape families are allowed, in this order.

### C1 — minimum minimal-cover size

Define

kappa(x) = 0 if M(x) is empty,
and otherwise
kappa(x) = min{|S| : S in M(x)}.

C1(x)=kappa(x), an integer in {0,1,2,3,4}.

### C2 — minimal-cover size profile

For k=1,2,3,4 define

m_k(x) = # { S in M(x) : |S|=k }.

C2(x) = (m_1(x),m_2(x),m_3(x),m_4(x)).

### C3 — all-cover size profile

For k=1,2,3,4 define

c_k(x) = # { nonempty S subseteq A : |S|=k and L_x(S)=Lambda(x) }.

C3(x) = (c_1(x),c_2(x),c_3(x),c_4(x)).

Each c_k is an exact integer between 0 and binomial(4,k).

### C4 — exact minimal-cover antichain shape

C4(x) = M(x), serialized as the canonically ordered list of its increasing base tuples.

The empty antichain is represented by [].

C1-C3 are exact coarsenings of the same C4 action-cover structure. Their separate eligibility is frozen before output. No fifth transform may be introduced after inspection.

In particular E009 must not introduce:

- raw factorization signatures of x;
- raw Lambda(x) values;
- raw per-base orders or order ratios;
- actual prime-factor identities of x or Lambda(x);
- residue-transition tables, modulus-conditioned transition objects, or modulus-refinement objects;
- neighbour x-1/x+1 factorization;
- additive shifts, gaps, occupancies, events, digit words, or spectral/statistical transforms;
- floating normalization, fitted curves, p-values, entropy, correlations, smoothing, plots, or post-result thresholds.

## Exact frequency and composite-control comparison

For each family F in C1-C4 and exact signature t, define:

- n_P^F(t): number of prime anchors in P_B with signature t;
- n_C^F(t): number of composite control anchors in C_B with signature t;
- N_P = |P_B|;
- N_C = |C_B|.

Use no division or floating point. Define the exact enrichment numerator

E_F(t) = n_P^F(t) * N_C - n_C^F(t) * N_P.

E_F(t)>0 is exactly equivalent to t having larger relative frequency among prime anchors than among Q-admissible composite controls.

For each family, the only D9 target eligible for promotion is the strict unique mode of the complete prime-anchor frequency table. If the prime table has a tied maximum, that family has no promotable target. Lower-ranked signatures cannot be substituted.

## Frozen support floors

Derive the population floor from the frozen band width:

N_min = W / 1000 = 1000.

Both N_P and N_C must be at least 1000 for any promotion.

Freeze the target-occurrence floor as the least integer R satisfying R^2 >= N_min:

R = 32.

These thresholds are fixed arithmetically before D9 output and cannot be changed after inspection.

## Canonical signature ordering

Frozen family order is C1, C2, C3, C4.

Signature ordering:

- C1: increasing integer;
- C2 and C3: lexicographic integer-tuple order;
- C4: compare the sequences of canonical subset tuples lexicographically; when one sequence is an exact prefix of another, the shorter sequence sorts first. The empty antichain therefore sorts first.

Within every frequency ranking, sort by descending count and then by the applicable canonical signature order.

Promotion records use family order C1 through C4 after duplicate suppression.

## Exact descriptive output allowlist

A future D9 execution may serialize only:

1. experiment/implementation metadata and exact selected band;
2. the frozen partition, W, Q, A, canonical 15-subset system, family definitions, support floors, and complete validated generation plan;
3. anchor summary: |A_B|, N_P, N_C, first/last in-band prime anchor;
4. validation aggregates only:
   - factorization reconstruction failure count;
   - nonprime-factor/canonical-factor-order failure count;
   - Lambda construction failure count;
   - basis-unit gcd failure count;
   - order-divides-Lambda failure count;
   - order witness/minimality failure count;
   - cover-monotonicity failure count;
   - minimal-antichain failure count;
5. for each C1-C4 in frozen family order:
   - complete exact prime-anchor frequency table;
   - complete exact composite-control frequency table;
   - prime mode count and all maximizing signatures;
   - deterministic runner-up count when defined;
   - strict-unique-prime-mode boolean;
   - for the unique prime mode only, its composite count and exact enrichment numerator;
   - population-floor, occurrence-floor, enrichment, and overall mechanical-eligibility booleans;
6. the exact promotion records defined below.

No per-anchor prime list, factorization, Lambda value, multiplicative-order vector, subset-lcm table, cover table, modular-power witness, non-mode enrichment scan, alternative basis/control, unlisted transform, or exploratory derived field may be serialized.

## Deterministic byte serialization

All JSON keys use stable lexical ordering. The canonical writer is equivalent to

json.dumps(payload, sort_keys=True, indent=2) + "\n"

with UTF-8 encoding and no timestamps, host paths, random IDs, runtime-dependent set order, or other nondeterministic fields.

All set-like objects must first be converted to the canonical ordered arrays defined above.

The identical complete command on the same implementation commit must produce byte-identical output.

## Frozen triviality and artifact exclusions

The following are validation/control facts only and can never receive an observation:

1. gcd(x,210)=1 for anchors in A_B;
2. every a in (2,3,5,7) is a unit modulo x;
3. factorization reconstructs x;
4. Lambda(x) equals the declared lcm of odd-prime-power exponent terms;
5. ord_x(a) divides Lambda(x);
6. the modular-power witness and prime-divisor minimality checks defining ord_x(a);
7. any cover remains a cover after adding basis elements;
8. M(x) is an inclusion-minimal antichain by construction;
9. C1-C3 are deterministic coarsenings/counts of C4;
10. combinatorial bounds such as 0<=c_k<=binomial(4,k);
11. composite-control frequencies by themselves;
12. any serialization, ordering, population-floor, occurrence-floor, or duplicate-suppression consequence.

A promotable record must additionally have positive exact enrichment against Q-admissible composite controls. Thus direct divisibility by 2, 3, 5, and 7 is matched before any cover-shape target can pass mechanically.

## Duplicate suppression

If eligible records from two or more families select exactly the same subset of D9 prime anchors, retain only the lowest-numbered family record among them.

Duplicate suppression may remove an eligible record but can never substitute a runner-up, alternate signature, changed family, or relaxed target.

## Frozen observation-promotion grammar

SQ-009 has a hard promotion cap of **4 observations**, at most one from each C1-C4 family.

For family F, let t* be the strict unique mode of its complete D9 prime-anchor table. A record is OBS-eligible only if all of the following hold:

1. N_P >= 1000 and N_C >= 1000;
2. the prime-anchor table has exactly one mode t*;
3. n_P^F(t*) >= 32;
4. E_F(t*) > 0;
5. the statement is only the exact finite D9 fact that t* is the strict unique prime-anchor mode for family F, clears the occurrence floor, and has larger relative frequency among prime anchors than Q-admissible composite controls;
6. it is not one of the forced/control identities above;
7. it survives exact duplicate suppression.

Families are considered in order C1, C2, C3, C4. Because each family contributes at most one target and the global cap is four, there is no post-result cross-family score or discretionary ranking.

A tied prime mode, target count below 32, nonpositive enrichment numerator, population-floor failure, trivial/control identity, or duplicate suppression makes that family ineligible. No runner-up or alternate signature may replace it.

## Frozen one-shot H9 criterion template

Every promoted D9 observation must have its exact family F and target signature t* written to the observation ledger before H9 generation.

H9 replication succeeds exactly when, under unchanged E009 semantics:

1. N_P >= 1000 and N_C >= 1000;
2. the exact same t* is the strict unique mode of the H9 prime-anchor table for family F;
3. n_{P,H9}^F(t*) >= 32;
4. the exact H9 enrichment numerator
   E_{F,H9}(t*) = n_{P,H9}^F(t*) N_{C,H9} - n_{C,H9}^F(t*) N_{P,H9}
   is strictly positive.

A tied prime maximum, any higher competitor, target count below 32, insufficient prime/composite population, or nonpositive enrichment fails replication mechanically.

H9 may later be executed twice before criterion inspection solely to establish byte determinism. H9 must not be mined for new signatures. Any changed Q, action basis A, factorization semantics, Lambda definition, order algorithm/semantics, cover predicate, family definition, support floor, control population, or target defines a new experiment and cannot reuse H9 as untouched evidence. No fallback or retargeting is permitted.

## Fail-closed future generation planner

E009 inherits the literal generation-path discipline of the novelty lane.

### Historically safe low support

Whole-prefix prime generation is allowed only inside historically safe generated support [0,100_000).

For an authorized target [L,U), exact deterministic trial division, segmented sieving, anchor factorization, Lambda factorization, and multiplicative-order computation may use only base-prime support through floor(sqrt(U-1)).

The future implementation must use the exact prescribed exclusive low-support endpoint for each E009 phase:

- D9: floor(sqrt(54_999_999)) = 7416, so low support is exactly [0,7417);
- H9: floor(sqrt(56_999_999)) = 7549, so low support is exactly [0,7550);
- A9: floor(sqrt(108_999_999)) = 10440, so low support is exactly [0,10441).

All three endpoints are below 100,000.

### High-value generation

Every prime-generation interval above 100,000 must be segmented directly inside the one currently authorized E009 target. The complete generation plan must be constructed and validated before the prime generator is invoked.

Factorization, Lambda computation, modular exponentiation, order computation, and subset-lcm computation are ordinary integer arithmetic on authorized target anchors and do not authorize prime generation in any additional high-value interval.

For D1-26, the complete authorized plan is exactly:

- whole-prefix base support [0,7417);
- segmented target D9=[54_000_000,55_000_000).

The D9 guard must reject **before any prime generation**:

- any whole-prefix or sieve(high) strategy above 100,000;
- short, expanded, shifted, or otherwise nonexact low-support plans;
- any partial, expanded, shifted, or split high-value target not exactly D9;
- G9-pre, G9-mid, H9, or A9;
- H8 or A8;
- A1, H3, H4, G6-mid, A3, A4, A6, G7-pre, G7-mid, A7, G8-pre, G8-mid;
- every E003/E004 guard;
- every historical generated novelty band as a new target;
- every E005 calibration segment;
- every other protected, historical, partial, or non-target high-value interval.

For a later H9 unit, the high-value allowlist changes to H9 only and the low support changes to exactly [0,7550). For a later A9 unit, the high-value allowlist changes to A9 only and low support changes to exactly [0,10441). Historical reserves, guards, generated bands, and calibration segments are never E009 targets.

## Focused validation obligations for D1-26

Before any D9 prime generation, the later execution unit must test all outcome-relevant semantic boundaries:

1. exact G9-pre/D9/G9-mid/H9/A9 boundaries, widths, mutual disjointness, and protected-range disjointness;
2. exact Q=210 and ordered basis A=(2,3,5,7);
3. exact admissible-domain membership on hand-checkable integers;
4. exact prime/composite partition semantics on a hand-checkable domain;
5. deterministic ascending exact factorization, reconstruction, repeated prime powers, and canonical factor order;
6. exact Lambda construction from odd prime powers and lcm semantics;
7. exact factorization of Lambda where required;
8. exact multiplicative-order computation, including order divisibility, modular witness, and prime-divisor minimality;
9. exact enumeration and frozen ordering of all 15 nonempty subsets of A;
10. exact subset-lcm and cover-predicate semantics;
11. cover upward-monotonicity validation;
12. exact extraction and ordering of M(x), including empty, singleton, and multiple incomparable minimal-cover cases;
13. exact C1, C2, C3, and C4 signature semantics;
14. canonical signature comparison/order for every family;
15. complete frequency-table population totals and deterministic ranking;
16. strict-unique-mode detection and tie rejection;
17. exact integer enrichment arithmetic, including positive, zero, and negative cases;
18. population and occurrence floors;
19. exact duplicate suppression and four-observation cap;
20. exact descriptive allowlist shape, including absence of per-anchor factors, Lambda values, order vectors, subset-lcm/cover tables, and non-mode enrichment scans;
21. byte-deterministic serialization;
22. fail-closed rejection, before the prime generator is called, of whole-prefix high generation, wrong low support, partial/expanded target, guards, H9/A9, H8/A8, all historical protected/generated bands, E005 calibration segments, and arbitrary other non-target intervals.

Only after every obligation passes may D9 be generated.

## Generic process safeguard

E009 is a separately frozen qualitative representation switch, not a repair or retuning of E008 or any earlier novelty experiment. The switch reason is target-agnostic: E008 closed under its frozen grammar with no eligible observation, and the novelty lane therefore moves to a different declared exact representation family.

No E005 selected/unselected object, score, residual, historical comparison, hidden target, or source-derived mechanism is transferred into E009. No historical OBS target is recombined with the action-cover family.

## Stop rules

### D1-25 preflight stop

D1-25 ends when this specification and corresponding authoritative state are committed and metadata-consistency checked.

This unit does **not** implement or execute E009, generate D9/H9/A9, generate any prime-derived E009 output, inspect any protected reserve/holdout/guard, rerun or mine E001/E002/E003/E004/E006/E007/E008, allocate an observation or candidate, perform mechanism/proof/adversarial work, run prior-art/collision/literature search, make a novelty claim, or use calibration objects.

### D1-26 discovery stop

The later D1-26 unit may implement E009, validate it against every frozen obligation, commit the implementation/test checkpoint before generation, execute D9 twice for byte determinism, inspect only the frozen descriptive allowlist, and apply only the frozen C1-C4 promotion grammar.

If D9 yields eligible observations, D1-26 may allocate at most four OBS-### IDs and must freeze each exact unchanged same-family/same-target H9 criterion before any future H9 generation. It must not generate H9 or A9, create a candidate, perform mechanism/proof/adversarial work, or run prior-art/collision/literature search in that unit.

If the promotion pool is empty, record **NO ELIGIBLE OBSERVATION**, leave H9/A9 untouched, and close SQ-009 without relaxing, retuning, replacing, or extending the grammar.
