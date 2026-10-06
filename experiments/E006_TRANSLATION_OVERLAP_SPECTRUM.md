# E006 — Frozen Translation-Overlap Spectrum Discovery

**Stage:** discovery  
**Queue item:** SQ-006  
**Related task:** D1-15 / SQ-006  
**Status:** FROZEN / NOT YET EXECUTED  
**Freeze date:** 2026-10-06

This file freezes E006 before any E006 prime-derived result is generated or inspected. All E001/E002/E003/E004 novelty-lane specifications, evidence, outcomes, observation statuses, no-candidate/no-observation results, and protected-range statuses remain frozen historical facts. SQ-005 is calibration-only history and contributes no novelty primitive, target, transform, candidate seed, or representation-selection rationale.

## Purpose

Search for exact value-space translation overlap among prime indicators: how often two primes occur at a declared fixed additive displacement, whether or not they are consecutive primes.

This is qualitatively distinct from the executed novelty grammars:

- E001 counted consecutive-prime gaps/motifs, finite differences, reduced-residue transitions, globally anchored occupancies, and strict global record-gap neighbourhoods;
- E003 conditioned local occupancy/gap neighbourhoods on selected events;
- E004 factorized directed reduced-residue transition fingerprints across related moduli;
- E006 instead applies exact translations to the band-local prime indicator and counts all prime pairs at each declared displacement. It does not require adjacency, event selection, occupancy aggregation, residue-transition counting, or modulus-refinement structure.

E006 is an observation generator only. It must not create a candidate, perform mechanism/proof work, or run a prior-art/collision audit.

## Frozen historical exclusions

No E006 code path may generate, inspect, or repurpose any protected or non-target novelty region.

Previously generated novelty regions remain historical only:

- E001 D0 = `[0, 1_000_000)`;
- E001 H0 = `[1_000_000, 2_000_000)`;
- E002 S1 = `[2_000_000, 3_000_000)`;
- E002 S2 = `[4_000_000, 5_000_000)`;
- E002 S3 = `[8_000_000, 9_000_000)`;
- historical A0 = `[10_000_000, 11_000_000)`, contaminated by generation and retired;
- E002 S4 = `[16_000_000, 17_000_000)`;
- E002 S5 = `[32_000_000, 33_000_000)`;
- E003 D3 = `[35_000_000, 36_000_000)`;
- E004 D4 = `[39_000_000, 40_000_000)`.

Protected untouched novelty ranges remain excluded:

- A1 = `[33_000_000, 34_000_000)`;
- H3 = `[37_000_000, 38_000_000)`;
- H4 = `[41_000_000, 42_000_000)`;
- A3 = `[70_000_000, 71_000_000)`;
- A4 = `[78_000_000, 79_000_000)`.

Frozen non-target guard bands also remain excluded:

- E003 pre-D3 guard = `[34_000_000, 35_000_000)`;
- E003 post-D3 guard = `[36_000_000, 37_000_000)`;
- E004 G4-pre = `[38_000_000, 39_000_000)`;
- E004 G4-mid = `[40_000_000, 41_000_000)`.

## Frozen E006 partition

All E006 target bands have width

`W = 1_000_000`.

Range selection uses novelty-lane generation provenance and frozen range metadata only. It does not inspect prime behaviour.

At this freeze, the greatest integer reached by a valid novelty discovery target is D4's final integer 39,999,999. Starting at the first million-aligned width-`W` band beyond that point, scan upward by whole bands while excluding every frozen protected/non-target novelty interval. The candidates `[40_000_000,41_000_000)` and `[41_000_000,42_000_000)` are unavailable because they are respectively G4-mid and H4. The first eligible band is therefore:

- **Discovery D6:** `[42_000_000, 43_000_000)`.

Leave one full-width guard after discovery:

- **E006 discovery/holdout guard G6-mid:** `[43_000_000, 44_000_000)`;
- **Untouched holdout H6:** `[44_000_000, 45_000_000)`.

Use the already-established metadata-only later-scale convention for the adversarial lower endpoint:

`L_A6 = 2 * L_D6 = 84_000_000`.

Therefore:

- **Adversarial A6:** `[84_000_000, 85_000_000)`.

D6, G6-mid, H6, and A6 are mutually disjoint and disjoint from every generated novelty band, A1/H3/H4/A3/A4, and every frozen E003/E004 guard band.

Execution is phased:

1. D6 discovery may be generated only in the later D1-16 execution unit;
2. H6 remains untouched until any D6 observation and its exact one-shot criterion are frozen;
3. A6 remains untouched for a later adversarial unit;
4. G6-mid is permanently non-target for E006;
5. A1, H3, H4, A3, A4, and all historical guards are never E006 targets.

## Primitive object

For one authorized E006 band `B = [L,U)`, define the band-local prime indicator

`I_B(x) = 1` if `x` is prime and `L <= x < U`, and `I_B(x) = 0` otherwise.

E006 does not form consecutive-prime gaps, prime-index differences, occupancy blocks, residue words, or event-centred windows.

## Frozen translation grammar

The common maximum translation is fixed from the already-established target width by

`H = floor(sqrt(W)) = 1000`.

The frozen shift set is

`S = {2,4,6,...,1000}`.

Only positive even shifts are allowed:

- `h = 0` is excluded as the tautological self-overlap;
- odd shifts are excluded before execution because on these high bands an odd displacement between two odd primes is parity-forbidden;
- no shift above 1000 may be introduced after output inspection.

To make every shift use exactly the same number of possible anchor integers, define the common anchor domain

`A_B = {x in Z : L <= x < U-H}`.

For every `h in S`, define the exact translation-overlap count

`C_B(h) = sum_{x in A_B} I_B(x) I_B(x+h)`.

Equivalently, `C_B(h)` is the number of prime pairs `(p,p+h)` whose left endpoint lies in the common anchor domain. Intervening primes are irrelevant; the pair need not be consecutive.

No h-specific edge extension is allowed. Prime pairs with left endpoint `x >= U-H` are excluded for every shift, even when a smaller `h` would keep `x+h` inside the band. This common exposure rule is frozen to prevent boundary opportunity from changing with `h`.

All E006 promotable objects are exact integers.

## Exact non-promotable modular-admissibility control

For each shift `h`, define its odd radical from the shift integer alone:

`rho(h) = product p`

over the distinct odd prime divisors `p` of `h`, with empty product `rho(h)=1`.

This factorization is metadata about `h`; it is not derived from band primes.

Define the equivalence class

`E_r = { h in S : rho(h) = r }`.

Because every `h in S` is even, and two shifts have the same odd radical exactly when they have the same set of odd prime divisors, any two members of the same `E_r` have the same exact two-point modular-admissibility profile: for every prime modulus `ell`, the two offsets `{0,h}` occupy one residue class when `ell | h` and two otherwise. Thus parity and the deterministic local-sieve advantage coming solely from which primes divide the displacement are held fixed inside each promotion class.

The radical, its factorization, class membership, and this admissibility identity are control metadata only and can never be promoted as observations.

Metadata-only preflight validation of `S` gives 500 shifts, 204 distinct odd-radical classes, and 11 classes with at least eight members. This confirms that the frozen promotion grammar below is non-vacuous without using prime-derived data.

## Exact descriptive output allowlist

A D6 execution may serialize only:

1. experiment/implementation metadata and exact selected band;
2. the frozen partition, shift horizon, shift set, common anchor domain, and generation plan;
3. prime summary: in-band count, first in-band prime, and last in-band prime;
4. for every `h in S`, exactly:
   - `h`,
   - `rho(h)`,
   - exact `C_B(h)`;
5. for every odd-radical class, in increasing `r` order:
   - ordered member shifts;
   - class size;
   - exact member counts in shift order;
   - maximum count;
   - deterministic runner-up count;
   - all maximizing shifts;
   - strict-unique-maximum boolean;
   - dominance margin `max_count - runner_up_count` when class size is at least 2;
6. the exact promotion-pool records defined below.

No other prime-derived transform is allowed. In particular E006 must not emit:

- consecutive-gap or gap-motif counts;
- prime-index features or finite differences;
- occupancy summaries or event-centred windows;
- prime residue-transition tables or modulus-refinement objects;
- fitted curves, floating normalizations, correlations, Fourier transforms, spectral estimates, p-values, entropy, smoothing, or plots;
- h-specific anchor domains;
- post-result shift additions, deletions, regroupings, thresholds, or alternate fingerprints.

## Deterministic ordering and serialization

Frozen ordering rules are:

- shifts: increasing integer `h`;
- odd-radical classes: increasing integer `r`;
- members within a class: increasing `h`;
- a count ranking: descending `C_B(h)`, then increasing `h`;
- promotion records: the frozen ranking below.

For a class with at least two members, the runner-up is the first non-winning entry under the count ranking. If the maximum is tied, the class is not strict-unique and all tied maxima are serialized in increasing `h`.

All JSON keys use stable lexical ordering. The canonical writer is equivalent to

`json.dumps(payload, sort_keys=True, indent=2) + "\n"`

with UTF-8 encoding and no timestamps, host paths, random IDs, or other nondeterministic fields.

The same complete command on the same implementation commit must produce byte-identical output.

## Frozen observation-promotion grammar

SQ-006 has a hard promotion cap of **5 observations**.

A radical class `E_r` can contribute at most one promotable pattern. It enters the promotion pool only if all of the following are true:

1. `|E_r| >= 8`;
2. exactly one shift `h*` has the largest exact translation-overlap count in the class;
3. `C_D6(h*) >= 8`;
4. the observation is stated only as the exact within-class strict-maximum fact:
   "Among the frozen shifts `h in E_r`, `h*` has strictly greatest `C_D6(h)`.";
5. the statement is not a restatement of parity, odd-radical membership, factorization, the common-anchor rule, serialization order, or another deterministic encoding identity;
6. no conversion is made from this all-pairs overlap count into a claim about consecutive gaps or prime-index adjacency.

A tie for the maximum fails. Classes with fewer than eight shifts are descriptive only. The occurrence floor of eight is fixed before prime output and prevents a strict maximum supported only by a sparse handful of pair incidences.

If more than five classes qualify, rank mechanically by:

1. descending dominance margin `C_D6(h*) - runner_up_count`;
2. descending `C_D6(h*)`;
3. descending class size;
4. increasing odd radical `r`;
5. increasing target shift `h*`.

Promote at most the first five non-duplicate records. Equivalent restatements consume one slot. No approximate, visual, near-tie, low-count anomaly, cross-class comparison, or post-result regrouping is OBS-eligible.

## Frozen one-shot H6 criterion template

Every promoted D6 observation must have its exact target `(r,h*)` written to the observation ledger before H6 generation.

For a D6 observation asserting that `h*` is the strict unique maximum inside `E_r`, H6 replication succeeds exactly when:

1. H6 uses the unchanged band-local indicator, shift set, common anchor domain, odd-radical classes, ordering, and serialization semantics;
2. the same class `E_r` still has at least eight frozen member shifts;
3. `C_H6(h*) >= 8`;
4. `h*` has strictly greater `C_H6` count than every other shift in `E_r`.

A tie, fewer than eight target pair occurrences, or any higher-frequency competitor fails the frozen replication criterion.

H6 may later be executed twice before inspection solely to establish byte determinism. H6 must not be mined for new patterns. Any changed shift horizon, shift set, anchor domain, class definition, occurrence floor, ranking, or target creates a new experiment and cannot reuse H6 as untouched holdout evidence.

## Fail-closed generation plan

E006 inherits the literal generation-path discipline learned from the novelty lane.

Low support:

- whole-prefix base-sieve support is allowed only inside `[0,100_000)`, which is historically generated safe support;
- for a target `[L,U)`, the implementation may request only the exact base support needed through `floor(sqrt(U-1))`.

High-value generation:

- every interval above 100,000 must be segmented directly inside the currently authorized E006 target;
- the complete generation plan must be constructed and validated before the prime generator is invoked;
- any deliberate or accidental protected/non-target traversal must fail before prime generation.

For D6 execution, the only authorized high-value interval is exactly

`[42_000_000,43_000_000)`.

The corresponding maximum required base prime is `floor(sqrt(42_999_999)) = 6557`, so an implementation using an exclusive support endpoint may use at most `[0,6558)`.

The guard must reject before generation:

- whole-prefix or `sieve(high)` strategies above 100,000;
- A1, either E003 guard, D3, H3, A3;
- either E004 guard, D4, H4, A4;
- G6-mid, H6, A6;
- every other non-target high-value interval.

For a later H6 unit, the high-value allowlist changes to H6 only. For a later A6 unit, it changes to A6 only. Historical protected ranges and guards are never allowlisted by E006.

## Validation obligations for D1-16 execution

Before D6 generation, the implementation must test:

- exact band-local prime-indicator semantics;
- common-anchor exclusion at `U-H`;
- inclusion of all and only even shifts 2 through 1000;
- all-pairs translation-overlap counting on a hand-checkable sequence, including a case where an intervening prime proves that adjacency is not required;
- exclusion of any pair crossing the band boundary;
- exact odd-radical factorization and class membership;
- the metadata-only fact that 500 shifts form 204 radical classes and 11 classes meet the size-eight promotion floor;
- strict-unique-maximum and tie rejection;
- occurrence-floor handling;
- deterministic runner-up and promotion ordering;
- exact descriptive allowlist shape;
- byte-deterministic serialization;
- fail-closed rejection of protected/non-target/whole-prefix traversal before prime generation.

Only after these tests pass may D6 be generated.

## Stop rules

### D1-15 preflight stop

D1-15 ends when this specification and the corresponding authoritative state are committed and consistency-checked.

This unit does **not** implement or execute E006, generate D6/H6/A6, generate any prime-derived output, inspect A1/H3/H4/A3/A4 or any guard, rerun or mine E001/E002/E003/E004, allocate an observation or candidate, perform mechanism/proof work, or run a prior-art/collision audit.

### D1-16 discovery stop

The later D1-16 unit may implement E006, validate it, execute D6 twice for determinism, inspect only the frozen allowlist, and apply only the frozen promotion grammar.

If D6 yields eligible observations, D1-16 may allocate at most five `OBS-###` IDs and must freeze each exact H6 criterion before any future H6 execution. It must not generate H6 or A6, create a candidate, perform mechanism/proof work, or run prior-art search in that unit.

If the promotion pool is empty, record **NO ELIGIBLE OBSERVATION**, leave H6/A6 untouched, and close SQ-006 without relaxing the grammar.
