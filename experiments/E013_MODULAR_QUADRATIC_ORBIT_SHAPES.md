# E013 — Frozen Modular Quadratic Short-Orbit Order Shapes

**Stage:** DISCOVERY-1 / blind novelty discovery
**Queue item:** SQ-013
**Design unit:** D1-38
**Status:** FROZEN / NOT EXECUTED
**Freeze date:** 2026-10-08

## Firewall and selection provenance

This document freezes **exactly one** new exact, target-agnostic primitive family before any E013 prime-derived output. D1-37/E012/SQ-012 is immutable historical closure: **NO ELIGIBLE OBSERVATION**, SQ-012 CLOSED. Its D12 results are not an input to this design and cannot be rescanned, transferred, repaired, retuned, or reinterpreted. H12 and A12 remain untouched; A8 and A3 remain protected. No hidden historical problem, SQ-005 calibration/unblinding mechanism, literature, previous observation frequency, failure signature, or source-derived feature was used.

**One family:** a finite, deterministic *nonlinear modular dynamical orbit* for an independently chosen integer anchor x. The primitive is the ordered residue orbit of the map
`f_x(y)=(y^2+1) mod x`, with canonical seed `y_0=2`; the only promotable properties are predeclared ordinal-comparison shapes of a fixed short tail. This is not a search over polynomials, seeds, orbit lengths, moduli, targets, or dynamical laws.

**Explicit theory-informed generic choice:** integer polynomial iteration in a finite residue ring, with the simplest monic quadratic-plus-constant `y^2+1`, is a standard generic discrete-dynamics construction. It is selected as a self-contained exact nonlinear map, not because of a known prime theorem, hidden target, or any E011 polynomial factor-degree result. The exponent 2, constant 1 and seed 2 are frozen mathematical conventions. They are not subject to later search or adjustment.

Qualitative distinction from **all** frozen novelty work:

- E001: consecutive prime gaps/differences, residue transitions, occupancy, and record gaps; E002: cross-scale retest of E001; E003: selected event-centred gap/occupancy neighbourhoods; E004: modulus-divisibility refinement of prime residue-transition fingerprints.
- E006: prime-indicator translation-pair overlaps; E007: factorization coupling of x−1 and x+1; E008: fixed positional binary words of x.
- E009: *multiplicative unit* orders/exponents and minimal subset covers modulo x. E013 instead iterates a *noninvertible nonlinear additive-plus-square map*, never computes a unit order or cover, and records short-run **ordinal comparisons**, not group invariants.
- E010: continued-fraction recurrence/cycle of a quadratic surd. E013 has no surds, continued fractions, recurrence cycle extraction or period search; it performs a fixed number of polynomial iterations modulo the varying integer anchor.
- E011: irreducible-factor *degree partitions* of one polynomial over prime fields. E013 factors no polynomial, works identically in Z/xZ for primes and composite controls, and is about the trajectory of iteration, not factor degrees.
- E012: nearest strict bracketing of anchor by an independent lattice-norm support set. E013 has no geometric norm, support-set search, nearest-neighbour, bracketing distance, E012 residue-stratum selection, or E012 signature/threshold transfer.

No prime gaps/indices, neighbour factorizations, digit words, prime pair shifts, norm supports, polynomial factorization, plots, fitted statistics, Fourier objects, or calibration results are admitted. Only the *prime/composite label* of each predeclared common anchor domain is prime-derived; its orbit is computed by the same exact arithmetic for either label.

## Provenance-only partition and exact disjointness

Every interval is **half-open**. Width `W=1_000_000` is the existing programme-wide alignment convention; no output is used in placement. The latest frozen E012 holdout endpoint is 70_000_000 (H12 is **untouched**, not consumed), but [70_000_000,71_000_000) is already historical A3. Scan forward in increasing W-aligned units, rejecting *any* interval with historical generated, consumed, held-back, reserved, guard, or calibration provenance. The first free unit [71_000_000,72_000_000) is reserved as pre-guard; the next as discovery; the next as mid-guard; and the next as one-shot holdout:

| ID | Exact range | Frozen role |
|---|---|---|
| G13-pre | [71_000_000,72_000_000) | ungenerated non-target guard |
| D13 | [72_000_000,73_000_000) | discovery; only D1-39 can execute |
| G13-mid | [73_000_000,74_000_000) | ungenerated non-target guard |
| H13 | [74_000_000,75_000_000) | untouched one-shot holdout; **not** D1-39 |
| A13 | [144_000_000,145_000_000) | untouched later adversarial reserve; **not** D1-39 |

The later reserve is fixed solely by the inherited provenance convention `L_A13=2*L_D13=144_000_000`. This arithmetic does not involve prime values. H12=[69_000_000,70_000_000), A12=[134_000_000,135_000_000), A8=[66_000_000,67_000_000) and A3=[70_000_000,71_000_000) remain protected and unchanged.

**Exhaustive million-aligned historical check**, preserving named roles (numbers below are millions; e.g. `[42,43)` means [42_000_000,43_000_000)):

- Previously generated/consumed or contaminated: D0 [0,1), H0 [1,2), E002 S1 [2,3), S2 [4,5), S3 [8,9), A0 [10,11) **contaminated/retired**, S4 [16,17), S5 [32,33), D3 [35,36), D4 [39,40), D6 [42,43), H6 [44,45), D7 [46,47), H7 [48,49), D8 [50,51), D9 [54,55), H9 [56,57), D10 [58,59), H10 [60,61), D11 [62,63), H11 [64,65), D12 [67,68).
- Held-back/protected: A1 [33,34), H3 [37,38), H4 [41,42), H8 [52,53), A8 [66,67), H12 [69,70), A3 [70,71), A4 [78,79), A6 [84,85), A7 [92,93), A9 [108,109), A10 [116,117), A11 [124,125), A12 [134,135).
- Frozen ungenerated non-target guards: G3-pre [34,35), G3-post [36,37), G4-pre [38,39), G4-mid [40,41), G6-mid [43,44), G7-pre [45,46), G7-mid [47,48), G8-pre [49,50), G8-mid [51,52), G9-pre [53,54), G9-mid [55,56), G10-pre [57,58), G10-mid [59,60), G11-pre [61,62), G11-mid [63,64), G12-pre [65,66), G12-mid [68,69).
- All quarantined E005 maximum calibration segments: [128_000_000,129_048_576), [256_000_000,257_048_576), [512_000_000,513_048_576), [1_024_000_000,1_025_048_576), [2_048_000_000,2_049_048_576), [4_096_000_000,4_097_048_576). Every nested E005 width is contained in its listed maximum segment.

**Exact integer interval audit:** for half-open intervals [a,b),[c,d), overlap iff `a<d && c<b`. The historical table contains **53** named generated/protected/guard intervals plus six maximum E005 calibration intervals. The five new intervals above were each compared with all 59 historical intervals (295 comparisons) and pairwise with each other (10 more), yielding **0 overlaps / 305 exact checks**. Equivalently, every new interval lies in [71M,75M) or [144M,145M); the historical table has no interval intersecting either region. E005's first maximum ends at 129_048_576 < 144_000_000, while its second begins at 256_000_000 > 145_000_000. This is a metadata-only calculation; **no primes or protected intervals were probed**. The list and planner must also fail closed on any newly discovered historical exclusion, even if not named here.

## Exact primitive, anchor domain, and transforms

Freeze the artifact-control wheel `Q=2*3*5=30` (product of first three prime integers, no empirical choice). Reduced residue order is `R30=(1,7,11,13,17,19,23,29)`.

For any authorized target band `B=[L,U)`, freeze the **same** anchor domain for both populations:
`X_B={x integer : L <= x < U and gcd(x,30)=1}`.
Define P_B as anchors with prime label and C_B as all remaining anchors, which are composite (x>1). Labels must come exclusively from the precisely targeted segmented prime generation and a membership test. No primality-derived auxiliary statistics or additional sieved high ranges are permitted.

Freeze the orbit length from width only: `K=floor(log_10(W))+4=10` transitions (`10^6=W`, hence K=10). For each anchor independently, set `y_0=2`, then `y_{i+1}=(y_i*y_i+1) % x` for `i=0,...,9`, always using nonnegative remainders `0<=y_i<x`. Use exact unbounded integer multiplication (or proved safe integer bounds), no floats, no randomized start.

The initial prime-independent unreduced values are `y_0=2, y_1=5, y_2=26, y_3=677, y_4=458330`. All anchors in the three E013 target bands exceed 458330, so these four transitions are constant; **they are excluded** from the promotable shape, rather than admitted as spurious evidence. The next unreduced value is `458330^2+1=210066388901`, which exceeds every E013 target band endpoint, so reduction necessarily begins to matter in the retained tail. This burn-in is justified *only* from exact map and band metadata, not inspected prime behaviour. The sole retained ordered tail is `T_x=(y_4,y_5,y_6,y_7,y_8,y_9,y_10)` of length seven.

If two entries of T_x are equal (any pair, not merely adjacent), all four family signatures are the distinguished `COLLISION`, ranked before noncollision signatures, and **not promotable**. No orbit is extended after collision and no later choice of a different tail is authorized.

For seven pairwise-distinct tail entries define comparisons `b_i=1` if `T_i>T_{i+1}`, otherwise `b_i=0`, for i=0,...,5. No equality is allowed in this branch. Exactly four ordered promotable families are frozen:

- **O1**: `sum(b_0,...,b_5)`, the number of adjacent descents (integer 0..6).
- **O2**: number of strict left-to-right *new record highs* among `T_1,...,T_6` compared to all previous entries of T (integer 0..6); T_0 is excluded as a tautological record.
- **O3**: exact binary descent word `(b_0,b_1,b_2,b_3,b_4,b_5)` (serialized as six-element integer array).
- **O4**: maximum length in **entries** of a consecutive strictly increasing run anywhere in T (integer 1..7).

O1 and O4 are exact coarsenings of O3; O2 needs the order of nonadjacent tail values and cannot be inferred from the descent word alone. None is an index-space prime word or an x binary-digit encoding. No other orbit length/seed/map, lag, wrap count, value rank permutation, invariant, periodicity, preperiod, factorization, cycle statistics, transform, grouping, normalization or alternative signature may be introduced after D13.

## Forced-artifact controls (not promotable)

All of the following are mandatory checks or non-promotable identities: gcd-wheel exclusion; target-band-exclusive membership; prime/composite partition; every orbit update and remainder bound; the fixed initial y0..y4; strict selection of T only; COLLISION iff any duplicate retained value; b_i semantics; O1=sum(O3), O4=one plus longest consecutive zero-run in O3 (taking empty zero-run as zero), 0<=O2<=6; signatures within exact domains; complete frequency/population sums; R30 partition and canonical order; strict-mode and duplicate-suppression tautologies. Mathematical identities forced by these definitions may not themselves become observations.

The control is **not** E012's per-mod-8 enrichment gate. Instead use a separately frozen mixed-configuration test over the eight generic Q=30 admissibility classes. For any family F and candidate signature t and residue r in R30, let `N_{P,r},N_{C,r}` be all prime/composite anchor counts and `n_{P,r}(t),n_{C,r}(t)` the target counts. Call r **mixed** iff all four counts `n_{P,r}(t), N_{P,r}-n_{P,r}(t), n_{C,r}(t), N_{C,r}-n_{C,r}(t)` are **strictly positive**. This excludes targets entirely dictated by a Q-residue and ensures both outcomes occur for both labels in qualifying classes. The mixed-class requirement is `M_min=ceil(3*phi(30)/4)=6` of the eight, computed without prime data. The separate exact aggregate enrichment numerator is `E_F(t)=n_P^F(t)*|C_B|-n_C^F(t)*|P_B|`; it must be **strictly positive**. No per-residue enrichment sign is used, and no post-result stratum splitting or class omission is allowed. Neither residue identity nor a forced encoding identity is promotable.

## Frozen floors, canonical ranking, promotion and duplicate suppression

All derived from W and fixed Q, without measuring data:

- Total label populations: `N_min=W/1000=1000`; require `|P_B|>=1000` and `|C_B|>=1000`.
- Every r in R30: `N_{P,r}>=100` and `N_{C,r}>=100`, with `100=W/10000`.
- Minimum target prime occurrence `C_min=min{n>0 : n^2>=N_min}=32`.
- Mixed-residue control `M_min=6` as above; exact total enrichment `E_F(t)>0`.
- All mandatory validation-failure aggregates must equal zero.

Canonical family order: O1,O2,O3,O4. Signature order: COLLISION first, then increasing integer for O1/O2/O4 and lexicographic six-bit tuples for O3. Prime frequency ranking is descending count then this signature order **for serialization only**; a tied mode has no target, regardless of ranking.

For each family F independently, compute its *complete internal* prime and composite signature frequency tables over X_D13. Let t* be a **strict unique** prime mode of the complete table including COLLISION. The family is pre-duplicate eligible **iff**: all overall and each-class label floors pass; a unique mode exists; t* != COLLISION; its prime occurrence is >=32; it has >=6 mixed R30 classes as defined above; `E_F(t*)>0`; all validation aggregates equal zero; the statement is the exact finite D13 same-family/same-signature fact and not a forced/control identity. Otherwise fail the family: **no second-best, different signature, lower floor, new stratum, or adjusted K allowed**. At most **four** records may be promoted.

Exact support-set duplicate suppression: for each pre-duplicate-eligible (F,t*) define `S_F={x in P_D13 : F(x)=t*}`. If two S_F are exactly identical as sets of integer prime anchors, keep **only** the earliest in O1<O2<O3<O4; later duplicates get no fallback. Never choose by margin, frequency strength, enrichment, novelty, post-result rank or judgement. Emit eligible survivors in family order as observation precursors; OBS IDs may be assigned only in the **later D1-39 execution unit**, not in this design unit. Even promoted records are finite observations, **not** candidates or novelty claims.

## Frozen unchanged one-shot holdout and adversarial reserve

Before any H13 generator call, each D13 promoted observation must have its permanent OBS ID, exact family, canonical target signature and *this same unchanged* H13 criterion committed. Execute H13 only if at least one D13 OBS exists; otherwise H13 remains untouched and SQ-013 closes as NO ELIGIBLE OBSERVATION.

For each frozen target t from family F, one-shot H13 passes iff: both label populations >=1000; each R30 class contains >=100 of each label; **the identical t** is the strict unique H13 prime-anchor mode in the **identical F**; t != COLLISION and count >=32; >=6 H13 classes are mixed for this exact target; exact H13 aggregate `E_F(t)>0`; all mandatory validation failures zero. Tie, competitor with >=target count, absent t, insufficient counts/mixed classes, nonpositive E, or any validation failure mechanically **REFUTES**. No holdout target substitution, new candidate-signature scan, reweighting, retuning, composite control change, or fallback. H13 is never mined. A13 remains untouched for a *separate future adversarial unit* and has no automatic execution authorization.

## Narrow descriptive artifact and exact bytes

The complete D13 discovery artifact may include **only** these JSON top-level keys: `experiment`, `implementation_commit`, `band`, `partition`, `parameters`, `generation_plan`, `anchor_summary`, `validation`, `families`, `promotions`.

- `band`: only `name`, `range` [L,U], `interval_semantics`. `partition`: precisely five entries with only `name`, `range`, `role`, in table order above.
- `parameters`: only `width`, `wheel`, `reduced_residues`, `seed`, `polynomial_map` (fixed string `"y^2+1 mod x"`), `steps`, `tail_start`, `tail_length`, `population_floor`, `class_floor`, `occurrence_floor`, `mixed_class_floor`.
- `generation_plan`: exactly two ordered objects with only `purpose`, `start`, `stop`, `strategy`; support first, target second. No extra support.
- `anchor_summary`: only `anchor_count`, `prime_count`, `composite_count`, `first_prime`, `last_prime`, `prime_counts_by_R30`, `composite_counts_by_R30`, `collision_prime_count`, `collision_composite_count`.
- `validation`: only integer failure aggregates `plan_failure_count`, `range_or_anchor_failure_count`, `orbit_recurrence_or_bound_failure_count`, `fixed_prefix_or_tail_failure_count`, `collision_or_shape_failure_count`, `family_identity_failure_count`, `R30_partition_failure_count`, `frequency_or_population_failure_count`; **all must be zero**.
- Each family row, ordered O1..O4: only `family`, `prime_mode_count`, `maximizer_count`, `highest_competing_count`, `strict_unique_prime_mode`, `unique_mode_signature` (null iff tied), `unique_mode_is_noncollision`, `target_composite_count` (null iff tied), `population_floor_passed`, `class_floor_passed`, `occurrence_floor_passed`, `mixed_class_count` (null iff tied), `mixed_class_floor_passed`, `aggregate_enrichment_numerator` (null iff tied), `aggregate_enrichment_positive`, `mechanically_eligible` (after duplicate suppression).
- Each `promotions` precursor, in O1..O4 order: only `family`, `target_signature`, `target_prime_count`, `target_composite_count`, `mixed_class_count`, `aggregate_enrichment_numerator`.

**Forbidden**: per-anchor x, prime lists except first/last/count, raw orbit residues, comparison tails, complete frequency tables, any non-modal signature, full residue-conditioned *target* counts, mixed-class identity lists, full support sets, x factorization/primality witnesses, alternate seeds/maps/lengths/tails, cross-family overlap statistics, per-anchor rank words, positional binary words, timings, random seeds, timestamps, paths, hostnames, plots, auxiliary post-result diagnostics, or exploratory fields. The evaluator may hold required counters and exact support sets *internally* for frozen gate and duplicate suppression, never serialize them.

Canonical UTF-8 JSON bytes: logical `json.dumps(payload,sort_keys=True,indent=2)+"\n"`; no floats, NaN, timestamps, machine-dependent metadata, unseeded randomness, variable worker ordering or dynamic identifiers. Empty promotions is `[]`. O3 signature arrays have length six and elements 0/1; COLLISION serializes exactly `"COLLISION"`; R30 arrays are in increasing R30 order; family and partition arrays preserve frozen order. The **identical complete D13 command**, including fixed `--code-commit` and one output path, must be run twice on the same checkpoint; byte equality and SHA-256 must be established **before** viewing any descriptive field. Only then inspect this allowlist. A deterministic invocation prototype to implement *unchanged* is `PYTHONPATH=.:src python experiments/E013_modular_quadratic_orbit_shapes.py --band D13 --code-commit <EXACT_PREGEN_CHECKPOINT> --output /tmp/e013-d13.json`; the future session substitutes its actual committed hash and uses identical bytes of this command twice.

## Fail-closed per-phase prime generation

Derive safe base-prime support by **integer square root** of the authorized target's inclusive maximum `U-1`, plus one for an exclusive endpoint: `b(B)=isqrt(U-1)+1`. Whole-prefix generation is permitted **only** for these exact small supports (all below the historically safe 100_000 boundary); every high prime is generated **segmented directly within the target**:

| Phase | Exclusive low whole-prefix interval | Only high segmented target |
|---|---|---|
| D13 (D1-39 only) | [0,8545) | [72_000_000,73_000_000) |
| H13 (later one-shot unit if OBS promoted) | [0,8661) | [74_000_000,75_000_000) |
| A13 (later separately authorized adversarial unit) | [0,12042) | [144_000_000,145_000_000) |

These endpoints follow exact `isqrt(72_999_999)=8544`, `isqrt(74_999_999)=8660`, and `isqrt(144_999_999)=12041`. Check the **complete requested generation plan** for exact two-entry ordered equality, correct current authorized phase and exact target/support intervals **before either generator can be called**. The plan validator must reject wrong/shortened/expanded/shifted low support; whole-prefix generation to any high endpoint; wrong, partial, expanded, shifted, split, duplicated, out-of-order or extra high intervals; G13-pre/G13-mid; out-of-phase H13/A13; H12/A12/A8/A3; all historical generated/contaminated/reserved/holdout/adversarial/guard ranges (including every E012 guard and D12); all six E005 calibration segments and nested widths; and **any arbitrary non-target high range**. Explicitly deny any prime-generating helper hidden in anchor evaluation, including whole-prefix traversals, per-anchor prime tests or extra support.

Use a positive allowlist, not an exclusion-only list. Guard rejection must be observable with a poison generator that raises if **any** generator is reached on a negative-plan test. Even generation without serialization counts as protected-range contamination. Generic prime-independent orbit arithmetic needs no generated primes outside the target and no lattice/norm support.

## Mandatory D1-39 validation before any primes

The next separately bounded unit must first checkpoint exact evaluator/test source bytes and versioned command before generator use, then pass targeted lint if available, focused tests, and compilation:

1. metadata-only disjointness using half-open overlap over every named historical generated/protected/guard interval and all six maximum E005 segments; exact five E013 roles and L_A13=2L_D13;
2. integer-only W/K/Q/R30/phi(30)/floors/6-class and isqrt/exclusive-support derivations;
3. hand-checkable X_B boundaries, Q-admissibility and exact two-label prime/composite partition on *small synthetic/manual examples only* (not an E013 target);
4. fixed y0..y4, exact f_x recurrence, nonnegative mod, integer overflow control, and seven-entry retained tail on a tiny toy modulus not in any high band;
5. collision by any repeated tail entry and COLLISION dominance/rejection; all possible canonical O1/O2/O3/O4 signatures on hand-chosen distinct tails;
6. O1 and O4 identities relative to O3, canonical integer/word orders, exact tied and strict unique mode, and no runner-up fallback;
7. mixed-class four-count semantics including boundary cases, exact aggregate enrichment positive/zero/negative arithmetic, no per-stratum E012 rule, all floors;
8. complete population-frequency conservation, promotion cap/family ordering, exact support-set duplicate suppression and no fallback;
9. exact JSON allowlist acceptance and rejection of every forbidden field, O3 six-bit arrays, COLLISION token, R30/canonical ordering and byte-deterministic repeat serialization;
10. plan guard pre-generator poison checks for exact D13, wrong/shortened/expanded/split/shifted/extra support, high whole-prefix, off-phase H13/A13, G13 guards, H12/A12/A8/A3, every historical range/calibration maximum/nested segment, and arbitrary non-target high intervals;
11. demonstrate no hidden generator in orbit/control computations, and exact D13 `[0,8545)` plus segmented `[72_000_000,73_000_000)` as the **only** valid discovery plan;
12. failure-injection/invalid-validation aggregate must suppress all promotions, with no partial artifact treated as success.

Tests may use fabricated small integer anchors and manually supplied primality labels; they must not enumerate primes in any protected E013, historical or calibration high interval. No discovery run may start until code/tests are Git-committed and validations pass.

## Phase boundaries and stop

**D1-38 design-only stop:** commit this spec plus the queue/programme/session/handoff records. Generate **no** primes or other E013 output, implement **no** evaluator, inspect no protected or per-anchor E012 output, allocate no OBS/CAND, open no candidate, mechanism, proof, adversarial or literature/collision/novelty lane. Historical observation, conjecture and failure records remain unchanged.

**D1-39 execution stop:** implement exactly this spec, pre-validate and checkpoint, run only D13 twice before looking at allowlisted aggregate output, then apply only the exact O1..O4 promotion/duplicate rules. If eligible, allocate OBS IDs only in family order and commit frozen same-family/same-signature H13 criteria **before** any later H13 generation. If none, record **NO ELIGIBLE OBSERVATION**, close SQ-013 without repairs and leave H13 untouched. Under either outcome, leave G13-pre/G13-mid, H13, A13, H12, A12, A8, A3 and every historical held-back region ungenerated/uninspected in D1-39. No candidate, mechanism, proof, adversarial or prior-art/collision/literature/novelty work.
