# E005 — Frozen Calibration Benchmark: Prime-Count Scale Structure

**Lane:** historical rediscovery calibration (permanently quarantined from novelty)
**Queue item:** SQ-005
**Related task:** D1-11 / SQ-005
**Status:** FROZEN / NOT YET EXECUTED
**Freeze date:** 2026-10-06

This file freezes the first PRIMES historical-rediscovery calibration benchmark before any E005 prime-derived output is generated or inspected.

The hidden historical target is intentionally not named or described here. Mature terminology, mature formulas, theorem statements, analytic objects, and equivalent target formulations are outside the active benchmark. E005 begins only from exact prime counts in predeclared intervals and elementary derived data.

E005 is not a novelty experiment. Its design, outputs, process record, later historical comparison, and every object derived from them are permanently quarantined from novelty promotion. **E005 can never allocate an `OBS-###` or `CAND-###` ID, cannot support a novelty claim, and cannot be imported as discovery/holdout/adversarial evidence for the novelty lane.**

## 1. Calibration purpose

Test whether the blinded PRIMES discovery process can, from interval prime counts alone:

1. compare counts across repeated changes of absolute scale and window scale;
2. identify a simple leading scale normalization without being given a target formula;
3. separate that leading normalization from residual behaviour;
4. inspect elementary alternative representations of the residual;
5. prefer one transform that compresses several window scales at once;
6. instantiate exact structural questions from the selected objects.

The benchmark measures the discovery process. It does not ask whether a hidden theorem is proved, and it does not create a conjecture.

## 2. Frozen novelty-lane firewall

All E001/E002/E003/E004 specifications, evidence, outcomes, observation statuses, and no-candidate/no-observation results are frozen historical facts and are not E005 inputs.

The following novelty-lane ranges remain untouched/uninspected and are forbidden to every E005 generation plan:

- A1 = `[33_000_000, 34_000_000)`;
- H3 = `[37_000_000, 38_000_000)`;
- H4 = `[41_000_000, 42_000_000)`;
- A3 = `[70_000_000, 71_000_000)`;
- A4 = `[78_000_000, 79_000_000)`.

E005 also forbids traversal through any E003/E004 guard band or other non-E005 high-value range. It does not reuse novelty-lane descriptive artifacts or prime summaries.

The calibration ranges below were selected from range metadata only. Their first anchor is strictly beyond the exclusive upper endpoint of A4, and no prime behaviour at any calibration anchor was inspected before this freeze.

## 3. Primitive inputs

For an authorized calibration anchor `a` and window width `w`, the sole prime-derived primitive is

`C(a,w) = # {p prime : a <= p < a+w}`.

The active benchmark may also use the exact metadata values `a` and `w`.

No raw prime list, prime value, gap, residue, finite-difference sequence, zero location, historical formula, historical coefficient, fitted asymptotic target, or literature-derived object is a primitive.

Implementation may generate primes internally only to obtain the declared counts, but raw prime values must not be serialized in E005 evidence.

## 4. Frozen calibration ranges and assessment split

Let the calibration anchor unit be

`U = 1_000_000`.

Use exactly six geometrically doubled anchors:

### Development anchors

1. `D5-0: a = 128U = 128_000_000`;
2. `D5-1: a = 256U = 256_000_000`;
3. `D5-2: a = 512U = 512_000_000`.

### One-shot assessment anchors

4. `H5-0: a = 1024U = 1_024_000_000`;
5. `H5-1: a = 2048U = 2_048_000_000`;
6. `H5-2: a = 4096U = 4_096_000_000`.

The assessment anchors are calibration holdout only. They are not novelty holdouts and never become novelty evidence.

Use exactly five nested widths at every anchor, in ascending order:

- `W0 = 2^12 = 4_096`;
- `W1 = 2^14 = 16_384`;
- `W2 = 2^16 = 65_536`;
- `W3 = 2^18 = 262_144`;
- `W4 = 2^20 = 1_048_576`.

For each anchor, the maximum generation segment is therefore `[a, a+1_048_576)`; all smaller count windows are nested prefixes of that segment.

These six high-value segments are mutually disjoint. The lowest starts at 128,000,000, strictly above A4's upper endpoint 79,000,000. At freeze, none is recorded as previously generated or inspected by PRIMES.

### Split discipline

Selections are made from D5-0/D5-1/D5-2 only.

H5-0/H5-1/H5-2 may not be generated until:

1. the implementation and guard are validated;
2. the development artifact is byte-deterministic;
3. the mechanically selected leading normalization, development baselines, and any development residual-sign target are written to a committed process record.

Assessment then evaluates only those frozen selected objects. It must not add a transform, alter a score, choose a new residual target, or mine H5 for a new pattern.

## 5. Exact count-derived objects

For every count cell define the exact rational density

`d(a,w) = C(a,w) / w`

and, when `C(a,w) > 0`, the exact rational mean spacing

`m(a,w) = w / C(a,w)`.

Also serialize, using exact rational arithmetic:

1. adjacent-anchor count ratios and density ratios at fixed `w`;
2. adjacent-width count ratios and density ratios at fixed `a`;
3. first finite differences of `C` and `d` in frozen anchor order at fixed `w`;
4. first finite differences of `C` and `d` in frozen width order at fixed `a`.

Rationals are serialized as reduced integer pairs `[numerator, denominator]` with positive denominator.

No polynomial fit, regression, smoothing, optimization over continuous parameters, stochastic model, p-value, entropy score, Fourier transform, complex-valued transform, or mature historical object is allowed.

## 6. Frozen elementary scale-normalization tournament

For a count cell, define the positive scale coordinate

`s(a,w) = a + w/2`.

For exact serialization of the coordinate itself use the rational pair `[2a+w, 2]`.

The tournament uses a broad, fixed elementary function palette. Define:

- `f0(s) = 1`;
- `f1(s) = ln(s)`;
- `f2(s) = sqrt(ln(s))`;
- `f3(s) = ln(ln(s))`;
- `f4(s) = sqrt(sqrt(s))`;
- `f5(s) = sqrt(s)`;
- `f6(s) = s`.

The normalization candidates, in frozen order, are:

1. `N00: d`;
2. `N01: d * f1(s)`;
3. `N02: d / f1(s)`;
4. `N03: d * f2(s)`;
5. `N04: d / f2(s)`;
6. `N05: d * f3(s)`;
7. `N06: d / f3(s)`;
8. `N07: d * f4(s)`;
9. `N08: d / f4(s)`;
10. `N09: d * f5(s)`;
11. `N10: d / f5(s)`;
12. `N11: d * f6(s)`;
13. `N12: d / f6(s)`.

No coefficient is fitted inside a candidate. No candidate may be added, removed, or algebraically privileged after development output exists.

### Explicit theory-informed design label

Including natural logarithm and iterated logarithm among the elementary unary functions is an unavoidable theory-informed calibration choice: logarithms are standard scale transforms and may be historically relevant to the hidden benchmark family. To limit leakage, they are included only inside a deliberately broad symmetric palette alongside roots, the identity scale, multiplication, and division; no prime-specific logarithmic formula, target constant, integral, series, complex function, zero set, or equivalent historical solution is predeclared. The tournament must treat all 13 candidates by the same frozen score and tie rule.

The geometric doubling of anchors is a generic scale-comparison device and is not selected from prime behaviour.

## 7. Deterministic numerical evaluation

Exact counts and rational objects remain exact.

Elementary irrational transforms are calibration diagnostics only and use Python `decimal.Decimal` semantics with:

- working precision: 90 decimal digits;
- rounding: `ROUND_HALF_EVEN`;
- `ln` and `sqrt` evaluated in that context;
- fourth root evaluated as `sqrt(sqrt(s))`;
- serialized transformed values and scores formatted in uppercase scientific notation with exactly 60 digits after the decimal point.

The implementation must reject a nonpositive function argument, division by zero, NaN, or infinity rather than silently changing the grammar.

## 8. Frozen leading-normalization score and selection

For a candidate `N`, an anchor subset `A`, and one width `w`, let `T_N(a,w)` be its positive transformed density.

Define the width-specific spread ratio

`R_N(A,w) = max_{a in A} T_N(a,w) / min_{a in A} T_N(a,w)`.

Define the global spread score

`S_N(A) = max_{w in W} R_N(A,w)`.

Lower is better. This score has no fitted coefficient.

### Development selection

Using development anchors only, select the unique `N*` with minimum `S_N(D5)`. If numerical equality occurs at the 60-digit serialized score, the earlier frozen candidate order wins.

Also record the complete development candidate ranking by:

1. ascending `S_N(D5)`;
2. frozen candidate order.

For each width, separately record the candidate ranking by ascending `R_N(D5,w)`, then frozen candidate order.

### Assessment

After the development selection record is committed, compute `S_N(H5)` for all frozen candidates for diagnostic ranking, but calibration success/failure may evaluate only the already selected `N*` against the identity candidate `N00`. No assessment result may change `N*`.

## 9. Frozen leading/residual separation

For the selected development normalization `N*`, define one development-only baseline for each width:

`B_w = (T_{N*}(D5-0,w) + T_{N*}(D5-1,w) + T_{N*}(D5-2,w)) / 3`.

Freeze all five `B_w` values in the development process record before assessment generation.

For every development cell define the dimensionless residual

`r(a,w) = T_{N*}(a,w) / B_w - 1`.

For assessment, use the same frozen `B_w`; do not refit them.

The benchmark may serialize exactly these residual representations:

- **R0 raw residual word:** `(r_0,r_1,r_2)` across the three anchors, separately for each width;
- **R1 residual sign word:** `(sgn(r_0),sgn(r_1),sgn(r_2))`;
- **R2 first-difference word:** `(r_1-r_0, r_2-r_1)`;
- **R3 first-difference sign word:** `(sgn(r_1-r_0), sgn(r_2-r_1))`;
- **R4 second difference:** `r_2 - 2r_1 + r_0`.

Signs are exact comparisons of deterministic Decimal values to zero and serialize as -1, 0, or +1.

No other residual transform is allowed.

## 10. Frozen residual compression test

Across the five widths, build complete frequency tables for R1 residual sign words and R3 first-difference sign words.

For each family independently on development:

- a target exists only if one exact sign word is the strict unique mode;
- the target must occur for at least 3 of the 5 widths;
- ties fail.

Family priority is R1 before R3. The first family meeting the rule supplies the frozen development residual-sign target. If neither qualifies, record `NO_RESIDUAL_SIGN_TARGET`.

Assessment may test only that frozen family/target:

- the exact same target must occur for at least 3 of the 5 widths;
- it must again be the strict unique mode of the complete assessment five-width table.

No assessment-only target can be created.

This is a calibration compression diagnostic, not an `OBS-###`.

## 11. Frozen exact-question grammar

The process record may instantiate only the following question templates, with symbols replaced by already selected E005 objects.

### Q1 — scale-normalized limit question

Eligible only if `N* != N00` and `N*` beats `N00` on the frozen development score:

> For each fixed `w` in the frozen width set, does `T_{N*}(a,w)` approach a finite nonzero limit along indefinitely repeated doublings of `a`?

### Q2 — cross-width coherence question

Eligible only if `N*` beats `N00` at at least four of five widths on development:

> Is the same scale normalization `N*` eventually more stable than raw density for every width in the frozen width family under repeated anchor doubling?

### Q3 — residual-sign persistence question

Eligible only if a development residual-sign target exists:

> Does the exact selected residual sign word remain the strict modal sign word across the frozen width family for all sufficiently large doubled anchors?

These are exact structural questions, not claims. They receive no observation/candidate ID and are not imported into novelty synthesis.

## 12. Frozen discovery-process success criteria

Evaluate the following milestones after one-shot assessment.

### M1 — useful scale normalization

Pass iff all are true:

1. `N* != N00`;
2. `S_{N*}(D5) < S_{N00}(D5)`;
3. `S_{N*}(H5) < S_{N00}(H5)`.

### M2 — compressive cross-width unification

Pass iff `N*` has strictly lower width-specific spread than `N00` for at least 4 of 5 widths on development **and** at least 4 of 5 widths on assessment.

### M3 — residual representation persistence

Pass iff a development residual-sign target is frozen and the unchanged target passes the assessment rule in Section 10.

### M4 — exact structural question formation

Pass iff at least one of Q1-Q3 is mechanically eligible from development-selected objects and is serialized exactly without historical terminology or an imported target formula.

### M5 — firewall and holdout discipline

Pass iff:

- no forbidden novelty range is generated or inspected;
- no raw prime list is serialized;
- no assessment output is generated before the development selection/baseline/target record is committed;
- no assessment result changes a selection, transform, threshold, question grammar, or target;
- no historical source/theory is consulted during execution;
- no `OBS-###` or `CAND-###` is allocated.

Any violation makes M5 fail and invalidates the benchmark execution.

### Overall process outcome

- **STRONG_PASS:** M5 passes, M1 passes, M4 passes, and at least one of M2 or M3 passes.
- **PARTIAL_PASS:** M5 passes and at least two of M1-M4 pass, but the STRONG_PASS rule is not met.
- **FAIL:** otherwise.
- **INVALID:** M5 fails or deterministic reproduction/guard validation fails.

This outcome rates the blinded discovery process only. It is not a statement about novelty, proof, or historical equivalence.

## 13. Exact descriptive output allowlist

E005 development may serialize only:

1. experiment/implementation metadata and frozen parameters;
2. generation plan;
3. anchor/width table and exact count matrix;
4. exact rational densities, mean spacings, declared ratios, and declared first differences;
5. the 13 transformed-density matrices;
6. development spread scores and deterministic rankings;
7. selected `N*`, its five development baselines, residual objects R0-R4, residual-sign frequency tables, and any frozen development target;
8. mechanically eligible Q1-Q3 instances;
9. validation and byte-determinism metadata.

E005 assessment may serialize only:

1. assessment count matrix and corresponding allowlisted exact/transform objects;
2. frozen `N*` and development baselines/target copied by identifier/value;
3. assessment scores needed for M1-M3;
4. assessment residual-sign table for the already frozen target family;
5. M1-M5 and overall outcome;
6. validation and byte-determinism metadata.

No plot, raw prime list, fitted coefficient, alternative transform, alternative width, alternative anchor, post-result threshold, historical name, source citation, theory comparison, or novelty language is allowed before unblinding.

## 14. Deterministic ordering and serialization

Frozen anchor order is ascending numerical anchor.

Frozen width order is `W0,W1,W2,W3,W4`.

Frozen candidate order is `N00,...,N12`.

Residual family order is `R0,R1,R2,R3,R4`; residual compression family priority is R1 then R3.

Sign-word frequency tables sort lexicographically by integer tuple. Candidate rankings use the score/tie rules above.

JSON uses stable lexical key ordering and canonical indentation equivalent to:

`json.dumps(payload, sort_keys=True, indent=2) + "\n"`.

No timestamp, host path, random identifier, unordered set iteration, or machine-dependent float is permitted.

The same complete phase command on the same implementation commit must produce byte-identical output.

## 15. Fail-closed generation plan and guard

The implementation must construct and validate the complete generation plan before invoking prime generation.

Low support allowance:

- base-sieve support may use only `[0,100_000)`, which has been historically generated;
- for the largest E005 endpoint, `floor(sqrt(4_097_048_575)) < 100_000`, so this allowance is sufficient.

Development phase high-value allowlist:

- `[128_000_000,129_048_576)`;
- `[256_000_000,257_048_576)`;
- `[512_000_000,513_048_576)`.

Assessment phase high-value allowlist, activated only after the committed development selection record:

- `[1_024_000_000,1_025_048_576)`;
- `[2_048_000_000,2_049_048_576)`;
- `[4_096_000_000,4_097_048_576)`.

The guard must reject before prime generation:

1. any whole-prefix or `sieve(high)` strategy above 100,000;
2. any high interval not wholly contained in the currently authorized phase allowlist;
3. any interval intersecting A1, H3, A3, H4, A4, any E003/E004 guard band, or any novelty-lane range;
4. any attempt to generate an assessment segment before the development selection checkpoint is supplied and verified;
5. any undeclared anchor/width or widened segment;
6. any request to serialize raw prime values.

Every generated E005 segment is permanently calibration-only after generation and can never later serve as untouched novelty evidence.

## 16. Validation obligations for the execution unit

Before any E005 prime generation, test:

- exact half-open interval counting on hand-checkable synthetic prime lists;
- nested-width counting from one max-width segment;
- exact rational reduction/serialization;
- frozen anchor/width/candidate ordering;
- deterministic Decimal `ln`, square-root, fourth-root, formatting, and tie behaviour;
- the exact spread score and deterministic candidate ranking;
- development-only selection and baseline construction;
- residual R0-R4 semantics and exact sign-word frequency/tie rules;
- Q1-Q3 eligibility;
- M1-M5 and overall outcome encoding;
- byte-deterministic serialization;
- guard rejection of A1/H3/A3/H4/A4, novelty guards/ranges, whole-prefix traversal, undeclared segments, assessment-before-checkpoint, and raw-prime serialization before generation.

Only after these tests pass may D5 development counts be generated.

## 17. Frozen two-phase execution protocol

### Phase A — development

1. implement and validate E005;
2. checkpoint implementation/tests before prime generation;
3. generate only the three development segments;
4. run the identical development command twice before inspection and verify byte identity;
5. compute the frozen tournament, `N*`, baselines, residual-sign target, and eligible questions;
6. commit the development artifact digest plus the exact selection/process record.

### Phase B — one-shot assessment

Only after Phase A is committed:

1. authorize exactly the three assessment segments;
2. generate assessment counts without changing E005;
3. run the identical assessment command twice before inspection and verify byte identity;
4. evaluate only frozen `N*`, baselines, target, M1-M5, and overall process outcome;
5. commit the assessment/process result.

The execution unit remains historically blinded throughout both phases.

## 18. Future unblinding protocol

Unblinding is a separate bounded calibration unit and is forbidden until the complete Phase A and Phase B outputs/process records are committed.

Before consulting historical theory, the unblinding unit must freeze a short calibration summary containing:

- selected normalization and rankings;
- which of M1-M5 passed;
- residual representations/targets found or not found;
- exact questions instantiated;
- where the blinded process stalled.

Only then may the unit consult historical mathematical sources/theory.

The unblinding comparison must assess, without novelty language:

1. whether the selected scale normalization corresponds to a historically useful leading description;
2. whether the residual separation resembles a historically useful residual object or remains merely descriptive;
3. whether the residual transform search found anything structurally relevant;
4. whether one discovered representation compressed several count/scale observations in a historically meaningful way;
5. which crucial historical representation change was absent from the frozen elementary grammar;
6. whether Q1-Q3 were mathematically productive questions in hindsight.

The comparison must explicitly distinguish `DIRECT_HISTORICAL_MATCH`, `USEFUL_PARTIAL_REDISCOVERY`, `DESCRIPTIVE_ONLY`, and `STALLED_BEFORE_KEY_IDEA` as calibration labels only.

No unblinding result may create or support an `OBS-###`, `CAND-###`, novelty status, prior-art collision audit, or proof programme. Historical rediscovery is expected overlap, not novelty.

## 19. Stop rule for this preflight

D1-11 ends when this specification and the corresponding authoritative state are committed and consistency-checked.

This preflight does **not**:

- implement or execute E005;
- generate any calibration or novelty prime-derived output;
- inspect any E005 development/assessment count;
- generate or inspect A1/H3/A3/H4/A4;
- rerun or mine E001/E002/E003/E004;
- consult historical sources or unblind the hidden theory;
- create an observation or candidate;
- perform mechanism, proof, novelty, or prior-art work.

The next bounded unit, if unblocked, is the exact two-phase execution of this frozen E005 benchmark while historical theory remains blinded.
