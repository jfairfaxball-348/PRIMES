# E015 — Frozen Square-Shell Euclidean Remainder Quartile Shapes

**Stage:** DISCOVERY-1 / blind novelty lane
**Queue item:** SQ-015
**Design unit:** D1-45
**Freeze date:** 2026-10-08
**Status:** DESIGN FROZEN; D15 UNEXECUTED; H15/A15 UNTOUCHED

## 1. Firewall and sole independent representation

Freeze exactly one exact, target-agnostic representation family: the **near-square Euclidean-division remainder quartile profile** of an integer anchor. This is a deterministic quotient/remainder landscape over a nine-denominator integer shell near isqrt(x), constructed without a prime label, factorization, prime neighbours, arithmetic target, random choice, statistical fit, or any previous experimental frequency. No E012/D12, E013/D13/H13 or E014/D14/H14 outcome, signature, I1/I2 result, holdout failure, target, or calibration information selected any component. SQ-005 is CLOSED/QUARANTINED; no E005 calibration object, unblinded target, or source-derived mechanism transfers.

**Explicit generic theory-informed conventions:** Euclidean division x=q*d+r with 0<=r<d, the integer square-root shell s=isqrt(x), nine consecutive denominators d=s+j for j=-4,...,4, four equally spaced unit-fraction bins, the Q=30 wheel, fixed million-wide bands, and integer exact prime/composite modal controls are elementary mathematical/methodological choices. They are not predictions of a known problem, source-derived criteria, or retrospectively selected settings. The constants nine/four and the width are frozen conventions, not fitted outcomes. There is no theorem, mechanism, conjecture, novelty or prior-art assertion.

**Representation distinction:** E001/E002 prime-gap/occupancy/residue and scale persistence; E003 event-centred prime-neighbourhood statistics; E004 residue-transition refinement; E006 translated prime-indicator overlaps; E007 x±1 factorization; E008 fixed binary positional words; E009 unit-group orders/covers mod x; E010 quadratic-surd continued-fraction cycles; E011 finite-field polynomial factor-degree partitions; E012 nearest squared-lattice-norm bracketing; E013 polynomial modular iteration/ordinal orbit tails; E014 primitive three-cube additive representation incidence graphs. E015 instead uses **nine ordinary Euclidean divisions of x by denominators near isqrt(x)** and the occupancy of *normalized nonzero remainders* in fixed rational quartiles. It performs no prime-gap/index operation, local prime occupancy, factorization of x/x±1, integer representation search, norm-support bracketing, finite-field factoring, modular orbit iteration, continued fractions, positional bit-word scan, primitive cube graph, or shared-summand component statistic. Its quartile occupancy histogram is not a projection/refinement of prime residue transitions: the bins are defined by exact rational inequalities for x mod d with d varying by anchor. Mere shared words such as "shape" or "count" are not shared primitives. Any forced encoding/coarsening identities remain non-promotable.

## 2. Frozen metadata-only D/H/A and guard partition

All intervals are half-open. Freeze W=1_000_000. Starting at exclusive end 80_000_000 of consumed E014 H14, take the earliest four consecutive W-aligned units with no historical provenance exclusion as G15-pre, D15, G15-mid and H15; freeze A15 with the prior purely arithmetic convention lower(A15)=2*lower(D15)=162_000_000. A15 is NOT an authorized execution phase merely because it has a reserve role.

| Role | Exact interval | State at D1-45 | Permission |
|---|---|---|---|
| G15-pre | [80_000_000,81_000_000) | untouched | permanent non-target guard |
| D15 | [81_000_000,82_000_000) | ungenerated | discovery only in a later D1-46 session |
| G15-mid | [82_000_000,83_000_000) | untouched | permanent non-target guard |
| H15 | [83_000_000,84_000_000) | untouched | one-shot holdout only after D15 OBS criterion freeze |
| A15 | [162_000_000,163_000_000) | untouched | reserved, separately authorized adversarial |

**Metadata-only exhaustive audit:** The E013 specification lists 53 named prior generated/consumed/contaminated, reserved/held-back and guard million intervals; append E013's five G13/D13/G13/H13/A13 roles, E014's five G14/D14/G14/H14/A14 roles, and all six maximum E005 calibration intervals [128_000_000,129_048_576), [256_000_000,257_048_576), [512_000_000,513_048_576), [1_024_000_000,1_025_048_576), [2_048_000_000,2_049_048_576), [4_096_000_000,4_097_048_576); all nested E005 widths lie inside a maximum segment. Thus 53+5+5+6=69 historical exclusions. Compare each E015 role with each exclusion (5*69=345) and all ten E015 role pairs using exact integer half-open predicate (a<d and c<b). **355/355 checked, zero overlaps.** E014 H14 [79M,80M) is replication-consumed and strictly adjacent to, never inside, G15-pre. Historical A6 [84M,85M) is adjacent to but disjoint from H15. A13 [144M,145M) and A14 [152M,153M) remain untouched; A15 is disjoint from both, A12 [134M,135M), E005's first maximum [128M,129_048_576) and all later E005 maxima. A0 remains generation-contaminated/retired, not clean. H12/A12/A8/A3, guards, all historical held-back/other adversarial roles and E005 calibration are excluded. All protected roles keep their prior status. If any new provenance exclusion is found, fail closed before generation; do not silently relocate a frozen role.

## 3. Exact prime-independent primitive, conditioning and quartile map

For a future explicitly authorized target band B=[L,U), common wheel domain X_B={x integer: L<=x<U, gcd(x,30)=1}, with fixed ordered R30=(1,7,11,13,17,19,23,29). Every x here is >1. Compute s=isqrt(x) using integer-only arithmetic and verify s*s<=x<(s+1)*(s+1). For each index j in J=(-4,-3,-2,-1,0,1,2,3,4), in this order, define positive d_j=s+j and the unique exact q_j,r_j from x=q_j*d_j+r_j and 0<=r_j<d_j. The phase ranges guarantee 1<d_j<x; validate this rather than assume it in the evaluator. No factorization, probabilistic test, floating point, p-adic/continued-fraction transform, fitted normalization or prime-dependent choice is allowed.

To prevent the tautological zero remainder/divisor signal from being promoted, define the **common label-blind conditioning domain**
Y_B={x in X_B: all nine r_j are strictly positive}.
The complement X_B\Y_B is a non-promotable divisor-artifact exclusion; report only its total count, not a prime/composite split. The exact same Y_B serves both labels. There is **no** alternative if Y_B is small. On Y_B freeze the exact rational quartile index
b_j=floor(4*r_j/d_j), an integer in {0,1,2,3}.
Compute it by integer division (4*r_j)//d_j, equivalently exact cross-multiplied thresholds r_j/d_j=1/4,1/2,3/4, with equality assigned to the upper bin. Do not use floating approximations, rescale by q_j, rearrange denominators, bin on the raw remainder, omit any j, change bin edges, or select a different shell. The nine-entry vector (b_-4,...,b_4) is internal-only; never emit it.

Define four bin counts c_k(x)=sum_{j in J} 1[b_j=k], for k=0,1,2,3. This exact nonnegative four-vector has sum 9. Prime labels P_B and composite labels C_B partition Y_B, determined **only** by membership in the future *authorized directly segmented B prime list*, after computing the domain and shape independently. Neither the excluded membership, isqrt shell, denominator list, q/r array, divisisibility witness, or raw nine-bin word can itself be a discovery.

## 4. Exactly three finite promotable transforms

The complete ordered frozen transform pool consists solely of:
- **R1 — modal quartile occupancy:** max(c_0,c_1,c_2,c_3); an integer in {3,4,5,6,7,8,9}. The lower bound 3 is pigeonhole, not evidence.
- **R2 — unlabeled quartile occupancy partition:** the four c_k values sorted in weakly decreasing order, **including zeros**, serialized as a four-element nonnegative integer array summing to 9.
- **R3 — ordered quartile occupancy composition:** the four-vector [c_0,c_1,c_2,c_3], serialized as a four-element nonnegative integer array summing to 9.

Allowed transformations stop here. R1 is the first entry of R2, and R2 is the sorted coarsening of R3; those identities are validation only, not observations. Signature domains are enumerated **in advance**, including possible zero-frequency entries: R1 ascending 3..9; R2 all weakly decreasing nonnegative four-tuples summing to 9 in lexicographic ascending order; R3 all nonnegative ordered four-tuples summing to 9 in lexicographic ascending order. No fourth shape, denominator-order run, per-j identity, alternative quartile, entropy, parity histogram, shape conditioned on label, alternative anchor subset, or post-result mode is permitted.

## 5. Forced identities and artifact checks

Before promoting any observation require exact zero failures for: phase/range/partition and Q=30 admissibility; independent integer isqrt and shell bounds; ordered nine denominators; division conservation x=q*d+r and 0<=r<d; exclusion of **all** zero-remainder anchors and no promotion of that exclusion; exact quartile inequality including boundary equality to upper bin; all nine b_j in 0..3 and sum_k c_k=9; R1/R2/R3 coarsening identities and signature-domain enumeration; prime/composite disjoint-exhaustive common Y_B; ordered eight R30 class assignments; complete frequency conservation and strict-mode logic; exact prime-support-set duplicate suppression; canonical serializer/field allowlist; generator positive-allowlist before entry. Parity, small-modulus wheel selection, degree-of-freedom/occupancy pigeonhole facts, fixed quartile thresholds, representation conditioning and deterministic coding identities cannot qualify as observations.

## 6. Promotion gates, ranking, duplicates

Fix W=1_000_000, N_min=W/1000=1000 and class_min=W/10000=100 (the fixed eight R30 controls). Require represented/conditioned prime and composite populations N_P,N_C >=1000; **each** R30 class has >=100 of *each* label; target prime count n_P(t)>=ceil(sqrt(N_min))=32. Define r mixed for target (F,t) if n_{P,r}(t), N_{P,r}-n_{P,r}(t), n_{C,r}(t), N_{C,r}-n_{C,r}(t) are all >0; require >=ceil(3*8/4)=6 mixed classes. Require strictly positive exact global enrichment E_F(t)=n_P(t)*N_C-n_C(t)*N_P>0. All validation failures must be zero. These are **generic theory-informed methodological thresholds** computed from band width and wheel cardinality alone, not E012/E013/E014 discoveries, D14/H14 class signs or inspected failures. No extra positive-class enrichment test, fitted p-value, significance selection, post-hoc group merge or class omission is allowed.

For R1 then R2 then R3, compute the complete prime and composite signature frequencies over the identical Y_D15. Rank by descending prime count, then by the above frozen canonical signature order **for deterministic display only**. A promotable target is the **strict unique prime mode**: its count must be strictly greater than every competitor, including zero-frequency domain signatures; ties yield null and fail, irrespective of tie-break rank. Eligibility also requires every population/class/target occurrence/mixed/enrichment/validation gate and a genuinely non-forced comparison between prime and composite labels. Failed families have **no** fallback/runner-up, altered shell/width/quarter threshold, target-conditioned domain or relaxed floor.

For each preduplicate eligible (F,t), internally collect the exact integer support S_F={x in P_D15:F(x)=t}. If two eligible supports are equal **as sets**, keep the earliest family in R1,R2,R3 order and suppress later exact duplicates without fallback. Equal cardinality or equal signature formatting alone is not duplicate evidence. Max three precursors; **no OBS or CAND ID at design freeze**. Promotion in D1-46 requires a separate committed observation and unchanged one-shot H15 criterion before H15 is ever generated.

## 7. Unchanged one-shot H15 and permanent reserve

If zero eligible D15 proposals, close SQ-015 NO ELIGIBLE OBSERVATION and **do not generate H15**. Otherwise commit each permanent OBS ID, exact R-family and integer/array target and unchanged H15 criterion *before any H15 prime generation*. On a separately authorized H15 run, using precisely identical s,J,nonzero Y_H15, rational quartiles, R30, signatures and canonical families, pass iff both conditioned label populations >=1000; every one of eight R30 classes >=100 each label; **the exact original target** remains strict unique H15 prime mode versus every same-family possible signature; n_P(t)>=32; >=6 mixed classes; E_F(t)>0; and every validation failure zero. Ties, higher competing counts, absence, low floors, nonpositive E or invalid schema **REFUTE** mechanically. Do not reuse H15 for second attempts, alter class counts or derive replacement targets. A15=[162M,163M) requires separate later adversarial authorization; no automatic access.

## 8. Narrow deterministic aggregate-only artifact schema

Freeze the future D15 JSON top-level keys **exactly**: experiment, implementation_commit, band, partition, parameters, generation_plan, anchor_summary, validation, families, promotions. No extensions.
- band: exactly name, range (two integer endpoints), interval_semantics="half-open".
- partition: exactly five ordered objects G15-pre,D15,G15-mid,H15,A15, each with only name,range,role.
- parameters: exactly width=1000000, wheel=30, residues_R30 (the ascending eight integers), denominator_offsets (ordered -4..4), quartile_edges_num=[0,1,2,3,4], quartile_denominator=4, zero_remainder_excluded=true, population_floor=1000, class_floor=100, occurrence_floor=32, mixed_class_floor=6.
- generation_plan: exactly two ordered objects, each only purpose,start,stop,strategy; exact low support then segmented target.
- anchor_summary: exactly wheel_anchor_count, conditioned_anchor_count, excluded_zero_remainder_count, prime_count, composite_count, prime_counts_by_R30, composite_counts_by_R30. R30 arrays length 8, in ascending order. No excluded-label split.
- validation: exactly plan_failure_count, shell_or_division_failure_count, zero_condition_failure_count, quartile_boundary_failure_count, histogram_identity_failure_count, signature_domain_failure_count, anchor_or_label_failure_count, R30_population_failure_count, frequency_or_mode_failure_count, serializer_or_duplicate_failure_count. All nonnegative integers and **all zero** to inspect/promote.
- families: exactly three ordered R1,R2,R3 objects, each with only family, prime_mode_count, highest_competing_count, strict_unique_prime_mode, unique_mode_signature (integer for R1, four-int array for R2/R3, or null on tie), target_composite_count (null on tie), population_floor_passed, class_floor_passed, occurrence_floor_passed, mixed_class_count (null on tie), mixed_class_floor_passed, aggregate_enrichment_numerator (null on tie), aggregate_enrichment_positive, mechanically_eligible (after duplicate suppression). All counts exact ints, flags booleans, no NaN/floats.
- promotions: 0..3 objects R1,R2,R3 order; each has only family,target_signature,target_prime_count,target_composite_count,mixed_class_count,aggregate_enrichment_numerator. No observation ID until separately promoted.

Forbidden: anchor identifiers or examples, prime list, individual x, nine denominator values/quotients/remainders/bins, shell patterns, factor/divisor witnesses, per-anchor records, support sets, full family frequency table, competitor identity, per-class target counts/identities, hidden statistics, diagnostic plots, environment/time/host/file paths, randomness, alternative signatures, post-result new thresholds, raw results from other lanes. Complete frequencies and S_F are **internal only** for mechanical frozen gates.

Canonical bytes are UTF-8 of Python json.dumps(payload,sort_keys=True,indent=2,ensure_ascii=True)+"\n", stable list order, then exact SHA-256. The D15 executable must write the same path with the same fully pinned complete command **twice** on identical code, prove complete byte equality/SHA **before inspecting any descriptive field**, then verify exact schema and zero counters. Any mismatch, missing field, unexpected extra, failure counter or noncanonical bytes fails closed without OBS.

## 9. Explicit positive-allowlist segmented generation by phase

Using exact integer arithmetic b(B)=isqrt(U-1)+1, only these **two ordered generator calls** are ever valid for an authorized phase. Whole-prefix means exclusively low base support [0,b); high target must be directly segmented [L,U), with no high prefix, primality oracle, factorization helper internally generating high primes or any other prime query.

| Phase | Exact first call (purpose base_sieve_support, strategy whole_prefix) | Exact second call (purpose segmented_target, strategy segmented) |
|---|---|---|
| D15 (only after D1-46 pre-generation checkpoints) | [0,9056) | [81_000_000,82_000_000) |
| H15 (future separately authorized one-shot only if OBS) | [0,9166) | [83_000_000,84_000_000) |
| A15 (future separately authorized adversarial only) | [0,12768) | [162_000_000,163_000_000) |

Exact squares: isqrt(81_999_999)=9055, isqrt(83_999_999)=9165, isqrt(162_999_999)=12767. The plan validator must compare **the whole ordered call list**, including purpose, start, stop and strategy, against exactly the authorized phase's two rows **before invoking either generator** and recheck at both generator boundaries. Reject wrong length/order, missing/extra/split/duplicate, partial/shifted/expanded base or high range, wrong strategy/phase, high whole-prefix, any protected historical band or other arbitrary high interval (including any A/G/H out of phase), E005 calibration maximum and nested segments, and direct per-anchor primality tests. A prime generator touched outside the allowlist contaminates the range even when output omits it. Explicit positive allowlist overrides all negative examples.

## 10. Future D1-46 implementation obligations (NOT performed now)

In D1-46, independently implement the exact frozen primitive and narrow D15-only evaluator, focused tests and fail-closed phase-aware planner. **Before first prime/primality generation**, commit exact source/tests and verify remote bytes/blobs; separately commit the full actual runnable command with pinned source commit and one fixed output path, remote-byte-verify it. Run focused synthetic tests and compilation; run lint if available, reporting unavailable tools precisely.

Synthetic hand-checkable tests without prime data must cover exact isqrt boundaries; x=q*d+r at positive/zero/nonzero remainders; s±4 endpoints and ordering; quartile boundaries at 1/4,1/2,3/4 with equality assigned to upper bin; fabricated nine-bin words giving four counts summing to nine, R1/R2/R3 with zeros included, all finite signature possibilities, coarsening, strict modes/ties/non-mode fallback rejection, per-class mixed counts, exact signed E, floor failures, duplicate supports of equal and unequal cardinality, max-three promotion cap, canonical JSON and forbidden-field rejection. Use fabricated prime/composite labels only; no valid D15/other high prime call in a synthetic test.

**Poison generator obligations:** instrument a generator that throws on entry and prove invalid plans are denied *before it is entered*. Include all 69 historical exclusions with their roles, E005 six maximum and nested width segments, G15-pre/G15-mid, phase-inaccessible H15/A15, D14/H14 consumed and A14 untouched, A13, H12/A12/A8/A3, arbitrary non-target high intervals, high whole-prefix, alternate low bound, plan reorder/duplicate/split/shift/extension/shortening/extra entry, concealed helper and direct primality query. Verify exactly two D15 positive plan entries without accidentally calling a real prime generator in design tests. Repeat **one complete identical D15 run** twice after pre-generation checkpoints, compare all artifact bytes and digest before inspecting the narrow aggregate, then mechanically promote at most three OBS with exact unchanged H15 criteria or close SQ-015 with no eligible observation. No H15/A15 execution in D1-46; never interpret D12/D13/H13 or D14/H14 outputs to tune E015.

## 11. D1-45 stop and preservation

**Design-only:** no evaluator or test file created or executed, no new prime generation/primality query, no D12/D13/H13/D14/H14 result mining, no A14/A13/guards/protected access, no observation, CAND, calibration transfer or unblinding, mechanism/proof/adversarial/prior-art/collision/literature/novelty work. OBS-018/019 stay REPLICATED, OBS-020 stays REFUTED, all original ledgers/evidence/code unchanged. SQ-014 stays CLOSED; SQ-015 is design-frozen awaiting D1-46. Documentation and exact historical metadata arithmetic only.
