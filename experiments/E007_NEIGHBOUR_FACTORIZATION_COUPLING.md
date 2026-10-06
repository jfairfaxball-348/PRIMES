# E007 — Frozen Neighbour-Factorization Coupling Discovery

**Stage:** discovery  
**Queue item:** SQ-007  
**Related task:** D1-19 / SQ-007  
**Status:** FROZEN / NOT YET EXECUTED  
**Freeze date:** 2026-10-06

This file freezes E007 before any E007 prime-derived output is generated or inspected. All E001/E002/E003/E004/E006 specifications, evidence, outcomes, observation statuses, no-observation/no-candidate results, and protected-range statuses remain immutable historical facts. SQ-005 is calibration-only history: only its committed closure/quarantine state and generic protocol rules apply here; no calibration object, historical match, source-derived mechanism, or unblinded target steers E007.

## Purpose and qualitative distinction

E007 studies the exact multiplicative structure of the two neighbouring integers (x-1) and (x+1) around an odd anchor (x), comparing profiles at prime anchors with the same profiles at odd composite control anchors.

For every anchor, all powers of two are removed from the two neighbours, the sides are canonically aligned by their forced 2-adic roles, and only four frozen multiplicative signatures are counted. This is qualitatively distinct from the executed novelty families:

- E001 used consecutive-prime gap motifs, finite differences, reduced-residue transitions, globally anchored occupancies, and strict global record-gap neighbourhoods;
- E003 used event-centred occupancy/gap neighbourhoods;
- E004 used projection/refinement structure of residue-transition fingerprints across moduli;
- E006 used additive translations of the prime indicator and all-pairs overlap counts;
- E007 instead factors the adjacent even composites around each odd anchor and studies exact multiplicative-profile coupling after removing the forced power-of-two component.

E007 does not use prime gaps, prime-index differences, residue-transition tables, occupancy blocks, event-centred windows, additive shift overlaps, fitted/scaled objects, or floating statistics.

E007 is an observation generator only. It must not create a candidate, perform mechanism/proof work, or run prior-art/collision or literature search.

## Frozen historical exclusions

No E007 code path may generate or inspect any historical protected/non-target novelty range.

Historical generated novelty ranges remain historical only:

- E001 D0 = `[0,1_000_000)`;
- E001 H0 = `[1_000_000,2_000_000)`;
- E002 S1 = `[2_000_000,3_000_000)`;
- E002 S2 = `[4_000_000,5_000_000)`;
- E002 S3 = `[8_000_000,9_000_000)`;
- historical A0 = `[10_000_000,11_000_000)`, contaminated by generation and retired;
- E002 S4 = `[16_000_000,17_000_000)`;
- E002 S5 = `[32_000_000,33_000_000)`;
- E003 D3 = `[35_000_000,36_000_000)`;
- E004 D4 = `[39_000_000,40_000_000)`;
- E006 D6 = `[42_000_000,43_000_000)`;
- E006 H6 = `[44_000_000,45_000_000)`.

Protected untouched novelty ranges remain excluded:

- A1 = `[33_000_000,34_000_000)`;
- H3 = `[37_000_000,38_000_000)`;
- H4 = `[41_000_000,42_000_000)`;
- A3 = `[70_000_000,71_000_000)`;
- A4 = `[78_000_000,79_000_000)`;
- A6 = `[84_000_000,85_000_000)`.

Frozen non-target guards remain excluded:

- E003 pre-D3 guard = `[34_000_000,35_000_000)`;
- E003 post-D3 guard = `[36_000_000,37_000_000)`;
- E004 G4-pre = `[38_000_000,39_000_000)`;
- E004 G4-mid = `[40_000_000,41_000_000)`;
- E006 G6-mid = `[43_000_000,44_000_000)`.

## Frozen E007 numerical partition

All E007 target/guard bands have width

`W = 1_000_000`.

Selection uses committed novelty-generation provenance and frozen range metadata only. The last valid novelty generation ended with H6 at the exclusive boundary 45,000,000. The first untouched million-aligned band after H6 is deliberately retained as a pre-discovery guard, then discovery/holdout are separated by a second full-width guard:

- **G7-pre:** `[45_000_000,46_000_000)` — frozen non-target guard;
- **Discovery D7:** `[46_000_000,47_000_000)`;
- **G7-mid:** `[47_000_000,48_000_000)` — frozen non-target guard;
- **Untouched holdout H7:** `[48_000_000,49_000_000)`.

Use the established metadata-only later-scale convention for the adversarial lower endpoint:

`L_A7 = 2 * L_D7 = 92_000_000`.

Therefore:

- **Adversarial A7:** `[92_000_000,93_000_000)`.

These ranges are mutually disjoint and disjoint from every historical generated novelty band, every protected reserve/holdout, and every frozen guard listed above. A7 is also below and disjoint from the quarantined E005 calibration segments, which begin at 128,000,000; no calibration output is used to select it.

Execution is phased:

1. D7 may be generated only in the later D1-20 execution unit;
2. H7 remains untouched until any D7 observation and its exact same-target one-shot criterion are frozen;
3. A7 remains untouched for a later adversarial unit;
4. G7-pre and G7-mid are permanently non-target for E007;
5. A1, H3, H4, A3, A4, A6, G6-mid, and all E003/E004 guards are never E007 targets.

## Common anchor domain and control partition

For one authorized E007 band `B=[L,U)`, define the common odd-anchor domain

`A_B = { x in Z : L < x < U-1 and x is odd }`.

This guarantees that both neighbours `x-1` and `x+1` lie inside `[L,U)` and gives prime and control anchors identical edge exposure.

For D7, the size of `A_B` is metadata-only arithmetic: 499,999 odd anchors.

Partition `A_B` exactly into:

- `P_B`: anchors `x` that are prime;
- `C_B`: anchors `x` that are composite.

Because every anchor is greater than 1 and odd, `P_B` and `C_B` are disjoint and exhaust `A_B`.

The composite-anchor table is a frozen artifact control. It is not a second discovery target and cannot itself generate an observation.

## Exact neighbour normalization

For an odd anchor `x`, let

- `n_- = x-1`;
- `n_+ = x+1`;
- `a_- = v_2(n_-)`;
- `a_+ = v_2(n_+)`,

where `v_2(n)` is the largest nonnegative integer `a` such that `2^a` divides `n`.

For every odd `x`, exactly one of `a_-`, `a_+` equals 1 and the other is at least 2. Define:

- the **thin side T** as the side with 2-adic valuation exactly 1;
- the **thick side K** as the other side.

Record whether T is the minus or plus side as non-promotable control metadata only.

Remove the complete power of two:

- `o_T = n_T / 2^{a_T}`;
- `o_K = n_K / 2^{a_K}`.

Both are positive odd integers. Since `gcd(x-1,x+1)=2`, the exact identity

`gcd(o_T,o_K)=1`

must hold for every anchor. This is a required validation invariant and is never promotion-eligible.

## Exact odd factorization and primitive profile

Factor each odd core exactly:

`o = product_j ell_j^{e_j}`

with odd primes `ell_j` in increasing order and positive integer exponents `e_j`.

For `o=1`, the factor list is empty.

Define:

- `omega(o)`: number of distinct odd prime factors;
- `Omega(o)`: sum of factor exponents;
- `sigma(o)`: exponent-shape tuple obtained by sorting the exponents in nonincreasing order;
- `Pplus(o)`: largest odd prime factor, with the convention `Pplus(1)=1`.

Every factorization must reconstruct `o` exactly. Probabilistic factorization or floating arithmetic is forbidden.

## Frozen transform grammar

Exactly four promotable signature families are allowed, in this order:

### F1 — exponent-shape pair

`F1(x) = (sigma(o_T), sigma(o_K))`.

This keeps multiplicative partition shape while discarding the identities and magnitudes of the odd prime factors.

### F2 — distinct-factor-count pair

`F2(x) = (omega(o_T), omega(o_K))`.

### F3 — total-multiplicity pair

`F3(x) = (Omega(o_T), Omega(o_K))`.

### F4 — largest-odd-factor order

`F4(x) = sgn(Pplus(o_T) - Pplus(o_K))`,

where `sgn` is exactly -1, 0, or +1.

No other transform is allowed. In particular E007 must not introduce:

- actual factor-value motifs or per-prime factor catalogs;
- residue classes or modulus-conditioned tables;
- gap, finite-difference, occupancy, event, index, or translation objects;
- digit/base representations;
- logarithms, fitted curves, floating normalization, p-values, entropy, correlations, smoothing, spectra, or plots;
- post-result thresholds, alternative side alignments, added factor statistics, or changed factorization shapes.

F2 and F3 are frozen coarse views of F1; their separate eligibility is predeclared and cannot be added or removed after D7 output.

## Exact frequency and control comparison

For each family `F` and exact signature `t`, define:

- `n_P^F(t)`: number of prime anchors in `P_B` with signature `t`;
- `n_C^F(t)`: number of composite control anchors in `C_B` with signature `t`;
- `N_P = |P_B|`;
- `N_C = |C_B|`.

No division or floating point is used. Define the exact enrichment numerator

`E_F(t) = n_P^F(t) * N_C - n_C^F(t) * N_P`.

Thus `E_F(t)>0` is exactly equivalent to the signature having larger relative frequency among prime anchors than among composite controls.

For each family, the D7 target considered for promotion is only the strict unique mode of the complete prime-anchor frequency table. If the prime table has a tied maximum, that family has no promotable target. E007 never searches lower-ranked signatures for a replacement target.

## Frozen support floors

The anchor-population floor is derived from the frozen width:

`N_min = W / 1000 = 1000`.

Both `N_P` and `N_C` must be at least `N_min` for any E007 promotion.

The target-occurrence floor is the least integer `R` with `R^2 >= N_min`, giving

`R = 32`.

These values are frozen before D7 output.

## Exact descriptive output allowlist

A D7 execution may serialize only:

1. experiment/implementation metadata and exact selected band;
2. frozen partition, common anchor domain, generation plan, and all frozen parameters;
3. anchor summary: `|A_B|`, `N_P`, `N_C`, first/last in-domain prime anchor;
4. non-promotable control counts, separately for prime/composite anchors:
   - thin-side orientation (minus versus plus);
   - exact thick-side 2-adic valuation frequency table;
5. validation aggregates:
   - factorization reconstruction failure count;
   - thin/thick classification failure count;
   - odd-core gcd-invariant failure count;
6. for each F1-F4 in frozen order:
   - complete exact prime-anchor frequency table;
   - complete exact composite-control frequency table;
   - prime mode count and all maximizing signatures;
   - deterministic runner-up count when defined;
   - strict-unique-prime-mode boolean;
   - for the unique prime mode only, its composite count and exact enrichment numerator;
   - occurrence-floor, population-floor, enrichment, and overall mechanical-eligibility booleans;
7. the exact promotion records defined below.

No per-anchor prime list, per-anchor factorization, actual odd factor values, non-mode enrichment scan, alternative ranking, or unlisted derived field may be serialized.

## Deterministic ordering and serialization

Frozen family order is F1, F2, F3, F4.

Frequency-table ordering:

- F1 shape pairs: lexicographic by thin shape tuple, then thick shape tuple;
- F2/F3 pairs: lexicographic integer-pair order;
- F4: integer order -1, 0, +1.

Within a frequency ranking, sort by descending count and then the same canonical signature order.

Thick-side 2-adic controls sort by increasing valuation; orientation controls sort `minus`, then `plus`.

All JSON keys use stable lexical ordering. The canonical writer is equivalent to

`json.dumps(payload, sort_keys=True, indent=2) + "\n"`

with UTF-8 encoding and no timestamps, host paths, random IDs, or other nondeterministic fields.

The identical complete command on the same implementation commit must produce byte-identical output.

## Frozen triviality and artifact controls

The following are validation/control facts only and can never receive an observation:

1. one neighbour has 2-adic valuation exactly 1 and the other at least 2;
2. which physical side is thin is determined by the anchor modulo 4;
3. `gcd(o_T,o_K)=1`;
4. factorization reconstructs the odd cores;
5. F2/F3 values are deterministic coarsenings of F1;
6. composite-control frequencies by themselves;
7. any serialization/ranking consequence.

All powers of two are removed before every promotable signature, and minus/plus orientation is replaced by canonical thin/thick roles. A promotable record must additionally have positive exact enrichment against odd composite anchors, preventing a strict prime mode that is no more frequent proportionally than the same generic odd-anchor profile from passing mechanically.

If eligible records from two families select exactly the same subset of D7 prime anchors, retain only the lower-numbered family record. This duplicate suppression can remove a record but can never substitute a lower-ranked target.

## Frozen observation-promotion grammar

SQ-007 has a hard promotion cap of **4 observations**, at most one from each F1-F4 family.

For family `F`, let `t*` be the strict unique mode of its complete D7 prime-anchor table. A record is OBS-eligible only if all of the following hold:

1. `N_P >= 1000` and `N_C >= 1000`;
2. the prime-anchor table has exactly one mode `t*`;
3. `n_P^F(t*) >= 32`;
4. `E_F(t*) > 0`;
5. the statement is only the exact finite D7 fact that `t*` is the strict unique prime-anchor mode for family F, meets the occurrence floor, and has larger relative frequency among prime anchors than composite controls;
6. it is not one of the forced/control identities above;
7. it survives the exact duplicate-suppression rule.

Families are considered in order F1, F2, F3, F4. Because each family can contribute at most one record and the cap is four, no post-result cross-family score or discretionary ranking is allowed.

A tied prime mode, target count below 32, nonpositive enrichment numerator, population-floor failure, trivial/control identity, or duplicate suppression makes that family ineligible. No runner-up or alternate signature may replace it.

## Frozen one-shot H7 criterion template

Every promoted D7 observation must have its exact family `F` and target signature `t*` written to the observation ledger before H7 generation.

H7 replication succeeds exactly when, under unchanged E007 semantics:

1. `N_P >= 1000` and `N_C >= 1000`;
2. the exact same `t*` is the strict unique mode of the H7 prime-anchor table for family `F`;
3. `n_{P,H7}^F(t*) >= 32`;
4. the exact H7 enrichment numerator
   `E_{F,H7}(t*) = n_{P,H7}^F(t*) N_{C,H7} - n_{C,H7}^F(t*) N_{P,H7}`
   is strictly positive.

A tied/higher prime competitor, target count below 32, insufficient anchor population, or nonpositive enrichment fails replication.

H7 may later be executed twice before criterion inspection solely to establish byte determinism. H7 must not be mined for new signatures. Any changed side normalization, factorization statistic, family definition, floor, control population, or target creates a new experiment and cannot reuse H7 as untouched evidence.

## Fail-closed future generation plan

E007 inherits the literal generation-path discipline of the novelty lane.

Low support:

- whole-prefix prime generation is allowed only inside historically safe generated support `[0,100_000)`;
- for an authorized band `[L,U)`, the implementation may request only the exact base support needed through `floor(sqrt(U-1))`.

High-value generation:

- every prime-generation interval above 100,000 must be segmented directly inside the currently authorized E007 target;
- the complete generation plan must be constructed and validated before the prime generator is invoked;
- factorization of integers `x-1` and `x+1` inside the target uses only the validated low base-prime support and is not permission to generate primes in any other high-value interval;
- any protected/non-target traversal must fail before prime generation.

For D7, the only authorized high-value prime-generation interval is exactly

`[46_000_000,47_000_000)`.

The maximum base prime required is

`floor(sqrt(46_999_999)) = 6855`,

so an exclusive base-support endpoint may be at most `6856`.

The D7 guard must reject before generation:

- any whole-prefix or `sieve(high)` strategy above 100,000;
- G7-pre, G7-mid, H7, A7;
- A1, H3, H4, A3, A4, A6, G6-mid;
- every E003/E004 guard;
- every historical generated novelty band as a new target;
- any partial/expanded high interval not exactly authorized by the frozen execution mode.

For a later H7 unit, the high-value allowlist changes to H7 only; its maximum required base prime is 6,999, so exclusive low support may be at most `[0,7000)`. For a later A7 unit, the allowlist changes to A7 only. Historical reserves/guards are never E007 targets.

## Validation obligations for D1-20 before D7 generation

The later execution unit must test, before any D7 prime generation:

1. exact common odd-anchor boundary semantics, including exclusion of `U-1`;
2. exact prime/composite partition of a hand-checkable odd-anchor domain;
3. exact `v_2` semantics and thin/thick canonicalization for both physical orientations;
4. complete power-of-two stripping;
5. exact deterministic odd factorization and reconstruction on hand-checkable integers, including repeated factors and odd core 1;
6. `gcd(o_T,o_K)=1` validation;
7. exact F1 shape sorting and F2/F3/F4 signature semantics;
8. complete frequency tables and canonical ordering for all four families;
9. strict-unique-mode detection and tie rejection;
10. exact integer enrichment-numerator arithmetic, including positive/zero/negative cases;
11. population and occurrence floors;
12. exact duplicate suppression and four-observation cap;
13. descriptive allowlist shape;
14. byte-deterministic serialization;
15. fail-closed rejection of whole-prefix, partial-target, guard, holdout, adversarial, historical protected, and other non-target traversals before the prime generator is called.

Only after all obligations pass may D7 be generated.

## Stop rules

### D1-19 preflight stop

D1-19 ends when this specification and the corresponding authoritative state are committed and consistency-checked.

This unit does **not** implement or execute E007, generate D7/H7/A7, generate any prime-derived output, inspect any reserve/holdout/guard, rerun or mine E001/E002/E003/E004/E006, allocate an observation or candidate, perform mechanism/proof work, or run prior-art/collision/literature search.

### D1-20 discovery stop

The later D1-20 unit may implement E007, validate it, execute D7 twice for byte determinism, inspect only the frozen descriptive allowlist, and mechanically apply only the frozen promotion grammar.

If D7 yields eligible records, D1-20 may allocate at most four `OBS-###` IDs and must freeze each exact H7 same-family/same-target criterion before any H7 generation. It must not generate H7 or A7, create a candidate, perform mechanism/proof work, or run prior-art/collision/literature search in that unit.

If no family is eligible, record **NO ELIGIBLE OBSERVATION**, leave H7/A7 untouched, and close SQ-007 without relaxing the grammar.
