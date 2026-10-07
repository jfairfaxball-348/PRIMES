# E011 — Frozen Finite-Field Polynomial Factor-Degree Shape Discovery

**Stage:** discovery
**Queue item:** SQ-011
**Related task:** D1-32 / SQ-011
**Status:** FROZEN / NOT YET EXECUTED
**Freeze date:** 2026-10-07

This file freezes E011 before any E011 prime-derived output is generated or inspected. All E001-E010 novelty specifications, executions, outcomes, observation statuses, no-observation/no-candidate results, generated-range provenance, guards, holdouts, and adversarial reserves remain immutable historical facts. In particular, E010 D10 discovery and H10 replication are consumed evidence, OBS-014 remains mechanically REFUTED under its frozen H10 criterion, and A10 remains frozen untouched/uninspected/unexecuted. A9, H8/A8, and every earlier protected range retain their committed roles.

SQ-005 remains calibration-only history. E011 uses only its committed closure/quarantine state and generic target-agnostic safeguards: freeze before output, do not repair an inspected family, and switch representation only through a separately frozen family. No E005 object, score, residual, selected or unselected transform, historical target, source-derived mechanism, unblinded terminology, or historical comparison is used to choose, define, rank, or interpret E011.

## Purpose and qualitative distinction

E011 studies an exact finite-field polynomial object attached independently to each prime anchor. A single canonically chosen integer polynomial is reduced modulo the prime anchor, and the only discovery primitive retained is the multiset of degrees of its monic irreducible factors.

The degree is selected without prime output. Let P(n) be the number of integer partitions of n. Freeze

- P(2)=2;
- P(3)=3;
- P(4)=5;
- P(5)=7;

and choose d=5 by the target-agnostic rule: the least integer d at least 2 for which P(d) is at least 7. This gives a small exact factor-degree state space with more than five possible shapes while keeping finite-field arithmetic bounded.

For every selected degree d, use the canonical sparse polynomial family F_d(T)=T^d+T+1. Therefore E011 freezes exactly one polynomial:

F(T)=T^5+T+1.

No alternative polynomial, coefficient search, polynomial panel, degree search after output, or target-conditioned replacement is permitted.

This is a qualitative representation switch rather than a retuning or recombination of an earlier family:

- E001 used prime gaps, finite differences, residue transitions, occupancies, and record-gap neighbourhoods;
- E003 used event-centred occupancy/gap neighbourhoods;
- E004 used projection/refinement structure of residue-transition tables;
- E006 used additive translations of the prime indicator;
- E007 used factorization profiles of x-1 and x+1;
- E008 used binary-coordinate word shapes of integer anchors;
- E009 used multiplicative orders and subset-cover antichains modulo integer anchors;
- E010 used exact quadratic-surd recurrence cycles;
- E011 instead uses exact polynomial arithmetic in the finite field with the prime anchor as characteristic and records only the degree partition of one fixed reduced polynomial.

E011 does not use consecutive-prime adjacency, prime gaps/differences, occupancy windows, event selection, residue-transition matrices, additive overlaps, factorization of neighbouring integers, positional digit words, multiplicative-order/action-cover objects, quadratic-surd recurrences, fitted curves, floating normalization, spectral transforms, or any historical observation value as a seed.

E011 is an observation generator only. It cannot create a candidate, perform mechanism/proof work, execute an adversarial test, or run prior-art/collision/literature/novelty work.

## Frozen historical exclusions

No E011 code path may generate, inspect, repurpose, or traverse any historical protected or non-target high-value novelty range.

Historical generated or consumed novelty ranges include:

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
- E008 D8 = [50_000_000,51_000_000);
- E009 D9 = [54_000_000,55_000_000);
- E009 H9 = [56_000_000,57_000_000);
- E010 D10 = [58_000_000,59_000_000);
- E010 H10 = [60_000_000,61_000_000).

Protected untouched novelty ranges include:

- A1 = [33_000_000,34_000_000);
- H3 = [37_000_000,38_000_000);
- H4 = [41_000_000,42_000_000);
- H8 = [52_000_000,53_000_000);
- A8 = [66_000_000,67_000_000);
- A3 = [70_000_000,71_000_000);
- A4 = [78_000_000,79_000_000);
- A6 = [84_000_000,85_000_000);
- A7 = [92_000_000,93_000_000);
- A9 = [108_000_000,109_000_000);
- A10 = [116_000_000,117_000_000).

Frozen non-target guards include:

- E003 pre-D3 guard = [34_000_000,35_000_000);
- E003 post-D3 guard = [36_000_000,37_000_000);
- E004 G4-pre = [38_000_000,39_000_000);
- E004 G4-mid = [40_000_000,41_000_000);
- E006 G6-mid = [43_000_000,44_000_000);
- E007 G7-pre = [45_000_000,46_000_000);
- E007 G7-mid = [47_000_000,48_000_000);
- E008 G8-pre = [49_000_000,50_000_000);
- E008 G8-mid = [51_000_000,52_000_000);
- E009 G9-pre = [53_000_000,54_000_000);
- E009 G9-mid = [55_000_000,56_000_000);
- E010 G10-pre = [57_000_000,58_000_000);
- E010 G10-mid = [59_000_000,60_000_000).

All E005 calibration segments are quarantined and excluded. In particular the six maximum segments begin at 128_000_000, 256_000_000, 512_000_000, 1_024_000_000, 2_048_000_000, and 4_096_000_000 and each has width 1_048_576.

Every other historical generated, protected, reserved, guard, partial, or non-target high interval is rejected by default even when not named above.

## Frozen E011 numerical partition

Freeze width

W=1_000_000.

Selection uses only committed generation/protection provenance and integer arithmetic. Let U_last=61_000_000, the exclusive upper endpoint of the latest consumed valid novelty target, E010 H10. Starting at U_last, preserve one full million-aligned band as a new non-target guard, then place discovery, another guard, and the one-shot holdout consecutively:

- G11-pre = [61_000_000,62_000_000), frozen non-target guard;
- D11 = [62_000_000,63_000_000), discovery;
- G11-mid = [63_000_000,64_000_000), frozen non-target guard;
- H11 = [64_000_000,65_000_000), untouched one-shot holdout.

Freeze the later-scale adversarial arithmetic rule

L_A11 = 2 * L_D11 = 124_000_000.

Therefore:

- A11 = [124_000_000,125_000_000), untouched adversarial reserve.

No existing reserve is consumed to place E011. The five E011 bands are mutually disjoint and disjoint from every historical generated/protected/non-target novelty interval above, including A10, A9, H8/A8, and all earlier guards/holdouts/reserves. A11 ends below the first E005 calibration segment beginning at 128_000_000.

Execution is phased:

1. D11 may be generated only in the separately bounded D1-33 discovery execution.
2. H11 remains untouched until every promoted D11 observation has its exact same-family/same-signature one-shot replication criterion committed.
3. A11 remains untouched for a later adversarial unit and is not consumed merely because it has been reserved.
4. G11-pre and G11-mid are permanent non-target guards for E011.
5. Historical ranges retain their prior roles and are never E011 targets.

## Primitive anchor domain

For an authorized E011 band B=[L,U), define the anchor population

P_B = { p prime : L <= p < U }.

E011 has no composite-anchor discovery/control population. The primitive is polynomial factorization over a finite field, so replacing a prime modulus by a composite modulus would change the mathematical object rather than provide a like-for-like control. E011 therefore does not invent a composite-ring surrogate.

Prime generation is used only to enumerate P_B. No consecutive-prime order, index, gap, or cross-anchor relation is part of the representation.

The following are descriptive metadata only and cannot be promoted:

- |P_B|;
- first and last prime in P_B;
- band endpoints;
- prime residues used by the artifact control below.

## Frozen polynomial metadata

Use exactly

F(T)=T^5+T+1.

Its coefficient vector, from constant term upward, is

(1,1,0,0,0,1).

Its exact integer discriminant is

3381 = 3 * 7^2 * 23.

Every E011 target prime exceeds 23. Therefore no E011 target prime divides the discriminant. A future implementation must still validate squarefreeness directly in the finite field and fail closed on any contradiction; the discriminant fact is validation metadata only and cannot become an observation.

No coefficient, exponent, polynomial, degree, discriminant, or factor of the discriminant may be changed after D11 output exists.

## Exact finite-field polynomial arithmetic

For one prime anchor p, reduce F coefficientwise modulo p to F_p(T) in the polynomial ring over the field with p elements.

Canonical polynomial representation:

- coefficients are integers in [0,p-1];
- coefficient lists are stored from lowest degree to highest degree internally;
- trailing zero coefficients are removed;
- the zero polynomial is represented by the empty coefficient tuple;
- every nonzero gcd is normalized to monic form;
- degree is the largest exponent with nonzero coefficient.

All additions, subtractions, multiplications, Euclidean divisions, inverses, gcds, and modular exponentiations are exact integer operations reduced modulo p. No floating arithmetic, approximation, randomized factorization, probabilistic irreducibility test, tolerance, or externally seeded randomness is permitted.

Let X denote the residue class of T. Define the exact derivative

F'_p(T)=5T^4+1 modulo p.

Validate

gcd(F_p,F'_p)=1.

For k=1,2,3,4,5 compute exactly

R_k(T) = T^(p^k) mod F_p(T)

by deterministic binary modular exponentiation, then

s_k(p) = degree(gcd(F_p(T), R_k(T)-T)).

The s_k values are computation/validation objects only and are not promotable or serializable per anchor.

## Canonical factor-degree profile

For d=1,2,3,4,5 define c_d(p) recursively from the exact gcd degrees:

c_1 = s_1,

c_2 = (s_2 - c_1)/2,

c_3 = (s_3 - c_1)/3,

c_4 = (s_4 - c_1 - 2*c_2)/4,

c_5 = (s_5 - c_1)/5.

A future implementation must require every numerator above to be divisible by its denominator, every c_d to be a nonnegative integer, and

sum from d=1 to 5 of d*c_d = 5.

It must also recompute every s_k from the derived c_d using

s_k = sum over d dividing k of d*c_d

for k=1,...,5.

Any failure is a hard validation failure.

Define the exact canonical factor-degree partition Lambda(p) by listing degree d exactly c_d times and sorting the resulting five-total-degree multiset in nonincreasing order.

Exactly seven Lambda values are possible under the frozen degree-5 grammar:

- (5);
- (4,1);
- (3,2);
- (3,1,1);
- (2,2,1);
- (2,1,1,1);
- (1,1,1,1,1).

Membership in this seven-element set and total degree 5 are validation identities, not observations.

No irreducible factor coefficient, finite-field root value, gcd polynomial coefficient, R_k coefficient, or per-anchor c_d vector may be serialized.

## Frozen promotable transform grammar

Exactly four promotable families are allowed, in this order.

### K1 — exact factor-degree partition

K1(p)=Lambda(p).

The signature is the finite positive-integer tuple sorted in nonincreasing order.

### K2 — irreducible-factor count

K2(p)=sum from d=1 to 5 of c_d(p).

Equivalently this is the number of entries in K1. The signature is one positive integer.

### K3 — linear-factor count

K3(p)=c_1(p).

The signature is an integer from 0 through 5.

### K4 — largest factor degree

K4(p)=max { d : c_d(p)>0 }.

The signature is an integer from 1 through 5.

K2-K4 are predeclared coarsenings of K1. Their coarsening identities are validation/triviality facts only; separate eligibility is frozen before output.

No fifth family may be introduced after D11 inspection. In particular E011 may not promote or inspect as discovery features:

- raw polynomial coefficients modulo p;
- irreducible factor coefficients or roots;
- the raw s_k vector;
- the raw c_d vector other than through K1-K4;
- discriminant residues;
- p modulo a chosen number except for the frozen artifact control below;
- polynomial values F(a) at selected a;
- alternate polynomials, degrees, coefficient searches, polynomial panels, shifted/scaled polynomials, products, resultants with another target polynomial, or cross-polynomial comparisons;
- fitted statistics, entropy, p-values, floating normalization, spectral transforms, or plots;
- cross-anchor sequences, transitions, gaps, runs, or neighbourhoods of K1-K4 signatures.

## Canonical family/signature ordering

Freeze family order

K1, K2, K3, K4.

K1 signatures are represented as JSON arrays corresponding to the nonincreasing integer tuple. Internally they are ordered lexicographically by the tuple in ordinary increasing integer lexicographic order.

K2-K4 signatures are ordered by increasing integer value.

Frequency ranking uses:

1. descending occurrence count;
2. canonical signature order only to make internal tables deterministic.

A family has a strict unique mode exactly when one signature alone attains the maximum count. If two or more signatures attain the maximum, strict uniqueness fails regardless of canonical tie order. Canonical ordering must never convert a tie into a winner.

No runner-up identity is required for serialization. Only the highest competing count is criterion-relevant.

## Frozen small-residue artifact control

Freeze the non-promotable control wheel

Q = 2*3*5*7 = 210,

chosen by the target-agnostic rule 'product of the first four primes'.

Q does not filter E011 anchors. Every E011 prime is already greater than 7 and therefore lies in a reduced residue class modulo 210.

For a family J and a strict-unique D11 modal target t, call a reduced residue class r modulo 210 mixed for t when D11 contains:

- at least one prime p with p mod 210 = r and J(p)=t; and
- at least one prime q with q mod 210 = r and J(q) != t.

Let M_J(t) be the number of mixed reduced residue classes.

Freeze the mixed-residue floor

M_min = 8 = 2 * 4,

twice the number of prime factors used in Q.

This is an artifact-control gate only. Residue identities, per-residue counts, and which residue classes are mixed are not promotable and must not be serialized. Only the integer mixed-residue-class count for a strict-unique mode may be serialized.

No composite comparison or distributional baseline is used. This omission is deliberate: E011 does not import a theory-informed expected factorization distribution as a hidden target, and a composite modulus would change the finite-field primitive.

## Frozen support floors

Freeze the population floor

N_min = 1000 = W/1000.

Freeze the target occurrence floor

C_min = 32,

the least integer c with c^2 >= N_min.

Freeze the mixed-residue floor M_min=8 as above.

These floors are fixed before D11 output and cannot be changed using discovery or holdout results.

## Frozen D11 promotion grammar

For each family K1-K4 independently, only its strict unique D11 prime-anchor mode may be considered. There is no fallback to a runner-up or any other signature.

A family target is pre-duplicate eligible if and only if all conditions hold:

1. D11 prime population N_P is at least 1000.
2. The family has a strict unique D11 mode.
3. The unique modal target occurs at least 32 times.
4. The unique modal target has M_J(t) at least 8 under the frozen Q=210 mixed-residue control.
5. Every mandatory finite-field/profile/frequency validation check passes exactly.

A tie, too-small population, too-small target count, mixed-residue count below 8, or any validation failure makes that family ineligible. There is no fallback target and no threshold relaxation.

### Exact duplicate suppression

For every pre-duplicate eligible target, define its D11 support set as the set of D11 prime anchors having that family/signature.

If two or more eligible family targets select exactly the same D11 prime-anchor support set, retain only the lowest-numbered family in the frozen order K1<K2<K3<K4. Suppressed families receive no fallback target.

### Hard promotion cap

At most one observation may come from each family and the total E011 promotion cap is four.

Eligible surviving records are ordered by K1,K2,K3,K4. No score, margin, p-value, effect-size ranking, or post-result priority rule is allowed.

A promoted record must state only the exact finite D11 modal fact defined by its family/signature and frozen gates. It is not a candidate and carries no novelty claim.

## Validation-only and triviality exclusions

The following can never receive an OBS ID by themselves:

- prime population, first/last prime, or band boundaries;
- the degree-selection rule d=5 or partition count P(5)=7;
- the polynomial F(T)=T^5+T+1, its coefficients, discriminant, or discriminant factorization;
- squarefreeness of F_p forced by p not dividing 3381;
- exact polynomial arithmetic/reconstruction facts;
- monic-gcd normalization;
- the s_k divisor-sum identities;
- integrality/nonnegativity of c_d;
- total-degree identity sum d*c_d=5;
- membership of K1 in the seven degree-5 partitions;
- K2-K4 bounds;
- K2/K3/K4 being deterministic coarsenings of K1;
- residue-class membership, mixed-residue identities, or control counts by themselves;
- population/occurrence/control floors;
- serialization, ranking, or duplicate-suppression consequences.

An observation must survive these exclusions in addition to the mechanical promotion gates.

## Frozen one-shot H11 replication template

Before any H11 prime generation, every D11 observation that survives promotion must have its observation ID, family, exact target signature, and the following unchanged replication criterion committed.

For a frozen observation in family J with target t, H11 replication succeeds exactly when all conditions hold under unchanged E011 semantics:

1. H11 contains at least 1000 prime anchors.
2. The identical signature t is the strict unique H11 mode of the same family J.
3. The identical target t occurs at least 32 times in H11.
4. The identical target has at least 8 mixed reduced residue classes under the same Q=210 control definition.
5. Every mandatory finite-field/profile/frequency validation check passes exactly.

A tie, any higher-frequency competitor, population-floor failure, occurrence-floor failure, mixed-residue-control failure, or validation failure mechanically REFUTES that observation.

H11 is replication-only. Its criterion artifact may serialize the frozen target signature, target count, highest competing count, mixed-residue count, population, pass/fail fields, and validation aggregate required by the criterion. It must not serialize a competing signature identity, unselected family modes, complete frequency tables, per-prime objects, or new target values.

No holdout mining, retargeting, threshold change, control change, polynomial change, degree change, normalization change, family replacement, fallback target, or new feature is permitted. A changed definition requires a new experiment and fresh untouched data.

If D11 promotes no observation, H11 remains untouched and no H11 execution is authorized.

## Frozen descriptive serialization allowlist

The full D11 discovery artifact may contain only these top-level fields:

- experiment;
- implementation_commit;
- band;
- partition;
- parameters;
- generation_plan;
- anchor_summary;
- validation;
- families;
- promotions.

### anchor_summary allowlist

Only:

- prime_count;
- first_prime;
- last_prime.

### validation allowlist

Only aggregate integer failure counts for:

- polynomial_metadata_or_discriminant_failure_count;
- finite_field_squarefree_failure_count;
- gcd_degree_range_failure_count;
- factor_count_integrality_or_nonnegativity_failure_count;
- divisor_sum_reconstruction_failure_count;
- total_degree_or_partition_failure_count;
- family_frequency_total_failure_count.

A valid execution requires all seven counts to be zero. An implementation may fail immediately rather than complete after a detected error, but a successful artifact cannot contain a nonzero validation count.

### family row allowlist

For each family K1-K4, only:

- family;
- prime_mode_count;
- maximizer_count;
- highest_competing_count;
- strict_unique_prime_mode;
- unique_mode_signature, null when the mode is not unique;
- population_floor_passed;
- occurrence_floor_passed;
- unique_mode_mixed_residue_count, null when the mode is not unique;
- residue_control_passed;
- mechanically_eligible after duplicate suppression.

Complete frequency tables are not serialized.

### promotions allowlist

For each promoted observation precursor, before an OBS ID is assigned:

- family;
- target_signature;
- target_prime_count;
- target_mixed_residue_count.

The execution record may later pair these mechanically eligible records with allocated OBS IDs and freeze their H11 criteria.

### Forbidden serialization

The D11 artifact must not contain:

- per-prime records;
- prime lists beyond first/last/count;
- raw p mod 210 values or residue-class identities;
- per-residue counts;
- R_k polynomials;
- gcd polynomials;
- s_k vectors;
- c_d vectors;
- irreducible factors or roots;
- factor coefficients;
- complete K1-K4 frequency tables;
- non-mode signatures;
- non-mode control scans;
- alternate polynomial results;
- timings, hostnames, timestamps, random seeds, temporary paths, environment-specific ordering, or exploratory fields.

No unlisted field may be added after output merely because it looks useful.

## Deterministic byte serialization

Freeze JSON serialization as UTF-8 bytes produced by the logical equivalent of

json.dumps(payload, sort_keys=True, indent=2) + newline.

Additional deterministic rules:

1. No floating-point values appear anywhere.
2. No NaN or infinity can appear.
3. Family rows are emitted in K1,K2,K3,K4 order.
4. Promotion rows are emitted in the same family order after duplicate suppression.
5. K1 signatures use the canonical nonincreasing integer list representation.
6. All set-like objects used internally are sorted before any allowed aggregate/list serialization.
7. Dictionary keys are sorted by the canonical writer.
8. No timestamp, runtime duration, process ID, host path, worker completion order, or nondeterministic metadata is serialized.
9. The same complete command on the same implementation checkpoint must produce byte-identical output.

The later discovery unit must execute the identical complete D11 command twice and establish byte identity before inspecting any allowlisted descriptive field.

## Frozen fail-closed future generation

Whole-prefix prime generation is permitted only inside the historically safe low-support interval [0,100_000). Every high-value prime interval must be generated directly by segmented generation inside the one currently authorized exact target.

For D11, exact low support is determined solely by the target endpoint:

floor(sqrt(62_999_999)) = 7_937,

so D1-33 may authorize only this complete plan:

1. whole-prefix base support [0,7_938);
2. segmented target D11=[62_000_000,63_000_000).

For a later H11 replication unit:

floor(sqrt(64_999_999)) = 8_062,

so the only canonical plan would be:

1. whole-prefix base support [0,8_063);
2. segmented target H11=[64_000_000,65_000_000).

For a later A11 adversarial unit:

floor(sqrt(124_999_999)) = 11_180,

so the only canonical plan would be:

1. whole-prefix base support [0,11_181);
2. segmented target A11=[124_000_000,125_000_000).

A future phase must reject before any prime generator call:

- wrong, shortened, expanded, shifted, or additional low support;
- any whole-prefix generation above 100_000;
- partial, expanded, shifted, split, duplicated, or reordered high-value targets;
- G11-pre or G11-mid;
- H11 when the phase is D11 discovery;
- A11 except in a separately authorized later adversarial phase;
- A10, A9, H8/A8, A1/H3/H4, A3/A4/A6/A7, and every other historical reserve/holdout;
- every historical guard;
- every historical generated/consumed novelty band including D10/H10;
- every E005 calibration segment;
- any arbitrary high-value interval not equal to the single phase-authorized target.

Validation of the complete plan must occur before either the low-support sieve or the segmented target generator is called. Internal generation through a forbidden range counts as contamination even if values are never serialized or inspected.

No prime-derived E011 output exists at this freeze.

## Validation obligations for D1-33 before D11 generation

The separately bounded execution unit must test, before any D11 prime generation:

1. exact E011 partition arithmetic and disjointness from all committed historical/protected/calibration intervals;
2. exact degree-selection metadata P(2)=2, P(3)=3, P(4)=5, P(5)=7 and d=5;
3. exact polynomial coefficients and discriminant 3381=3*7^2*23;
4. exact finite-field coefficient normalization, addition, multiplication, Euclidean division, monic gcd, and modular exponentiation on hand-checkable small fields;
5. exact derivative and squarefree validation;
6. exact R_k and s_k semantics for k=1,...,5 on hand-checkable cases;
7. exact c_d recursion, divisibility, nonnegativity, divisor-sum reconstruction, and total degree;
8. exact K1-K4 semantics and the seven allowed K1 partitions;
9. canonical signature ordering;
10. strict unique mode and tie rejection;
11. population and occurrence floors;
12. exact Q=210 mixed-residue-control semantics, including pass/fail boundary cases at 7 and 8 mixed classes;
13. exact duplicate suppression and four-observation cap;
14. descriptive allowlist shape and forbidden-field absence;
15. byte-deterministic serialization;
16. exact D11 low-support endpoint [0,7938);
17. fail-closed rejection, before prime generation, of wrong support, whole-prefix high generation, partial/expanded/shifted/split D11, E011 guards/H11/A11, every historical generated/protected/guard interval, every E005 calibration segment, and arbitrary non-target high intervals.

Only after every obligation passes may D11 be generated.

## D1-32 preflight stop

D1-32 ends when this specification and corresponding authoritative state are committed and metadata-consistency checked.

D1-32 does not:

- implement or execute E011;
- generate D11, H11, A11, or any other prime-derived E011 output;
- inspect a protected reserve, holdout, guard, or adversarial band;
- rerun or mine E010 D10/H10 or any earlier novelty artifact;
- allocate an OBS or CAND ID;
- perform candidate synthesis, mechanism/proof work, adversarial execution, prior-art/collision/literature search, novelty claims, historical-output mining, or calibration-object transfer.

## D1-33 discovery stop

The later D1-33 unit may implement E011, validate the frozen semantics/guard, checkpoint exact implementation/test bytes before generation, execute only D11 twice for byte determinism, inspect only the frozen allowlist, and mechanically apply only K1-K4 promotion.

If D11 yields eligible records, D1-33 may allocate at most four OBS IDs in frozen family order and must freeze each exact unchanged H11 criterion before any H11 generation. It must not generate H11 or A11, create a candidate, perform mechanism/proof/adversarial work, or run prior-art/collision/literature/novelty search in that unit.

If no family is eligible, record NO ELIGIBLE OBSERVATION, leave H11/A11 untouched, close SQ-011 without relaxing the grammar, and return to the next separately frozen blind novelty step.
