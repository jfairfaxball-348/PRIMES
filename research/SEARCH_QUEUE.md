# Search Queue

This queue contains bounded discovery work, not claims.

## SQ-001 — Baseline representation sweep

Stage: discovery

Status: **CANDIDATE TRIAGE COMPLETE — NO CANDIDATE CREATED; THREE REPLICATED OBSERVATIONS RETAINED; A0 WAS UNTOUCHED THROUGH SQ-001, LATER CONTAMINATED BY FAIL-003**

Frozen specification: `experiments/E001_REPRESENTATION_GRID.md`

Predeclared value ranges:

- discovery D0: `[0, 1_000_000)`;
- untouched holdout H0: `[1_000_000, 2_000_000)`;
- reserved adversarial A0: `[10_000_000, 11_000_000)`.

Run exact scans over:

- gap words of widths 2 through 6;
- finite differences through order 4;
- residue transitions for the frozen modulus family `6, 10, 12, 30, 60`;
- globally anchored block occupancies at widths `100, 1_000, 10_000, 100_000`;
- strict global record-gap neighbourhoods at gap radii `2, 4, 8`.

Goal: produce descriptive summaries and artifact checks only.

Promotion cap: 10 observations.

D0 result: deterministic discovery artifact SHA-256 `822431d664d5a35949abdf230a1b8abb41afa1f97511b7c129e5d18779f2e284`; four observations were frozen before holdout.

H0 result: deterministic holdout artifact SHA-256 `80c8c49f1845e941764b31471404a8e674fa794394687cb6502dbd2eca980254`. `OBS-001`, `OBS-002`, and `OBS-003` replicated under their frozen criteria. `OBS-004` was refuted by the empty anchored block `[1_671_800, 1_671_900)`. A0 remained untouched through SQ-001; it was later contaminated by generation during the discarded D1-04 E002 implementation (FAIL-003) without inspection.

Candidate-synthesis result: D1-02 considered `OBS-001` through `OBS-003` only and allocated no `CAND-###`. OBS-001 and OBS-002 remain exact replicated modal-rank facts but do not yet support a non-arbitrary scale/band quantifier. OBS-003 remains exact replicated finite-grid coverage but does not yet justify an all-moduli or infinite-occurrence extrapolation. OBS-004 remains REFUTED and excluded.

Next bounded action: D1-03 / SQ-002 cross-scale persistence preflight. Freeze a new E002 design and fresh disjoint ranges before execution, using the E001 definitions unchanged and excluding reserved A0. Do not generate new results, create a candidate, perform mechanism work, or run prior-art search in that preflight unit.

## SQ-002 — Cross-scale persistence

Stage: replication

Status: **D1-06 TRIAGE COMPLETE — NO CANDIDATE; OBS-002/003 PERSISTENT; A1 FROZEN / UNTOUCHED**

Frozen specification: `experiments/E002_CROSS_SCALE_PERSISTENCE.md`

Scope: `OBS-001`, `OBS-002`, and `OBS-003` only. `OBS-004` remains REFUTED and excluded.

Fresh fixed-width scale ladder:

- S1: `[2_000_000, 3_000_000)`;
- S2: `[4_000_000, 5_000_000)`;
- S3: `[8_000_000, 9_000_000)`;
- S4: `[16_000_000, 17_000_000)`;
- S5: `[32_000_000, 33_000_000)`.

All five bands are mutually disjoint and exclude E001 D0, H0, and historical reserved A0 = `[10_000_000, 11_000_000)`. A0 was untouched when E002 was frozen; FAIL-003 later contaminated it by internal generation without inspection.

Frozen persistence tests preserve the exact E001 definitions:

- OBS-001: third forward difference `0` must be the strict unique mode in every E002 band;
- OBS-002: width-2 gap motif `[6, 6]` must be the strict unique mode in every E002 band;
- OBS-003: directed reduced-residue transition support must be complete for every modulus in the unchanged family `{6,10,12,30,60}` in every E002 band.

A tie fails the applicable modal-rank criterion; any missing allowed transition fails OBS-003. Overall E002 persistence requires passing all five bands. The full predeclared ladder is evaluated even after an earlier failure; no replacement/additional bands or post-result thresholds are allowed.

Goal: test definition-preserving persistence with increasing value magnitude while holding the one-million band width fixed.

Promotion cap: no new observations or candidates in the E002 execution unit; it records persistence outcomes for the existing replicated observations only.

Execution result: valid implementation checkpoint `1d819af033b1869a144de6e840c72af0c13abea6` produced a byte-deterministic 10,107-byte criterion artifact, SHA-256 `32d24d5ea2417b1fdbf02b0787e6a616170162e0f7373dae32cf6906f19d37d5`. OBS-001 is **NOT PERSISTENT** because S1 and S3 fail the frozen strict unique-mode criterion. OBS-002 is **PERSISTENT** across S1-S5. OBS-003 is **PERSISTENT** across S1-S5 with complete support for every frozen modulus in every band. Historical E001 REPLICATED/REFUTED statuses are unchanged.

Protocol incident: the discarded first implementation constructed a whole-prefix prime list through 32,999,999 and therefore internally generated A0 before filtering. No A0 values or A0-derived criterion output were inspected, but under the literal exclusion rule A0 is contaminated and quarantined; see FAIL-003. The corrected valid E002 run used isolated segmented generation and did not traverse A0.

Protocol recovery (D1-05): exactly one replacement adversarial reserve is frozen: **A1 = `[33_000_000, 34_000_000)`**. Selection rule: preserve width 1,000,000 and choose the first million-aligned band whose lower endpoint lies strictly beyond every integer value previously generated by any recorded PRIMES prime-generation path. The maximum such value is 32,999,999 from FAIL-003, so the rule deterministically selects 33,000,000 as A1's lower endpoint. This depends only on generation provenance, not observed prime behaviour or E002 criterion values. A1 is disjoint from D0, H0, S1-S5, and A0; it has not been generated, inspected, or executed, and no prime-derived A1 result exists in `research/evidence/`. Recovery record: `experiments/E002_ADVERSARIAL_RESERVE_RECOVERY_2026-10-06.md`.

D1-06 candidate-synthesis result: no `CAND-###` was allocated. OBS-002 persists in all seven tested width-1,000,000 bands, but any statement beyond those bands needs an unsupported quantifier over untested locations, widths, later scales, or infinitely many ladder members. OBS-003 has complete support for all five frozen moduli in all seven tested bands, but a stronger statement needs an unsupported all-moduli, broader-family, all-band/eventual, or infinite-occurrence quantifier. A finite-grid statement would only restate the committed evidence. OBS-001 remains historically REPLICATED but E002 NOT PERSISTENT; OBS-004 remains REFUTED; A1 remains untouched.

Next bounded action: D1-07 / SQ-003 — design and freeze an event-centred neighbourhood preflight before any new prime-derived execution. Declare exact event definitions, thresholds, neighbourhood encodings, fresh discovery/holdout/adversarial ranges, promotion rules, and determinism requirements. Keep A1 untouched and outside SQ-003.

## SQ-003 — Event-centred neighbourhoods

Stage: discovery

Status: **D3 DISCOVERY COMPLETE — NO ELIGIBLE OBSERVATION; H3/A3/A1 UNTOUCHED; SQ-003 CLOSED WITHOUT PROMOTION**

Frozen specification: `experiments/E003_EVENT_CENTRED_NEIGHBOURHOODS.md`

Fresh metadata-only partition:

- discovery D3: `[35_000_000, 36_000_000)`;
- untouched holdout H3: `[37_000_000, 38_000_000)`;
- adversarial A3: `[70_000_000, 71_000_000)`.

The selection rule uses only the frozen one-million width and A1's metadata. D3 starts at the first million-aligned lower endpoint strictly greater than A1's exclusive upper endpoint 34,000,000; H3 leaves one full-width guard band after D3; A3 starts at twice the D3 lower endpoint. FAIL-003 records generation only through 32,999,999, and A1=`[33_000_000,34_000_000)` remains ungenerated, so all three E003 targets are untouched under committed generation provenance. A1 is not an E003 target.

Frozen event classes:

- `prime_dense`: globally anchored width-1,000 occupancy block whose centre occupancy is strictly greater than the two neighbouring block occupancies on each side;
- `prime_sparse`: same, with the centre occupancy strictly lower than the two neighbouring occupancies on each side;
- `strict_rolling_record_gap`: an in-band prime gap strictly larger than each of the preceding 64 in-band gaps, with 64 fixed as 8 times the frozen gap-neighbourhood radius. This is intentionally distinct from E001's historical strict global record-gap event.

Dense/sparse descriptive radius is 8 blocks; rolling-record descriptive radius is 8 gaps with a frozen 64-gap lookback. Dense/sparse promotion asymmetry uses only outer offsets 3 through 8 so the selection halo cannot itself become an observation. Exact raw words, centred residual words, integer asymmetry vectors, and sign signatures are the only neighbourhood object families.

Goal: search for repeated exact local configurations and before/after asymmetries under the frozen grammar.

Promotion cap: 5 observations. OBS eligibility requires at least 20 serializable events in the class, an exact target tuple that is the strict unique mode of one frozen object family, at least 3 target occurrences, and survival of explicit definitional/triviality exclusions. If more than five patterns qualify, the frozen deterministic ranking in the E003 specification selects the first five.

Any promoted D3 observation must freeze the exact same-target strict-unique-mode H3 criterion before H3 generation. A tie, fewer than 20 serializable H3 events, fewer than 3 target occurrences, or a higher-frequency competitor fails replication.

Generation guard: discovery execution may generate only low base support within `[0,100_000)` plus segmented D3. Whole-prefix generation above 100,000 is forbidden. The implementation must fail before generation if any requested interval can intersect A1, H3, A3, a guard band, or another non-target high range.

D3 execution result: implementation checkpoint `64d0d0ce485872e2cbdf17a17b31c0452787a06d` validated a fail-closed plan consisting only of low base-sieve support `[0,6000)` plus segmented D3. The identical D3 command was executed twice before inspection and produced byte-identical 2,848,769-byte artifacts, SHA-256 `885a0b7f50b36157c4b57ae72ae10748e5f84927aa9c261122bf6ae7bdb181b3`. D3 contains 57,487 primes. Frozen event counts are 187 dense events from 984 eligible anchors, 193 sparse events from 984 eligible anchors, and 790 serializable strict rolling-record gaps with zero boundary omissions.

Promotion result: **NO ELIGIBLE OBSERVATION**. All raw-word, centred-residual-word, and integer-asymmetry-vector modes have count 1. Each asymmetry-sign-signature family reaches mode count 6 but ties a runner-up at count 6, so all fail the frozen strict-unique-mode rule. No `OBS-###` ID was allocated and the grammar was not relaxed. Because there is no promoted D3 observation, no H3 replication criterion is required and H3 was not generated. Compact evidence: `research/evidence/E003_D3_discovery.json`; execution record: `experiments/E003_D3_DISCOVERY_2026-10-06.md`.

Next bounded action: D1-09 / SQ-004 — design and freeze a residue-transition factorization experiment before any SQ-004 prime-derived execution. Declare the exact related-modulus family, projection/refinement maps, object grammar, fresh untouched discovery/holdout/adversarial ranges, promotion rules, determinism, and generation-path guard. Preserve A1, H3, and A3 as untouched historical reserves and do not mine E003 further.

## SQ-004 — Residue-transition factorization

Stage: discovery

Status: **D4 DISCOVERY COMPLETE — NO ELIGIBLE OBSERVATION; H4/A4/A1/H3/A3 UNTOUCHED; SQ-004 CLOSED WITHOUT PROMOTION**

Frozen specification: `experiments/E004_RESIDUE_TRANSITION_FACTORIZATION.md`

Frozen modulus family:

`{6, 10, 12, 30, 60}`.

Frozen divisibility-cover relation graph, in deterministic order:

1. `6 -> 12`;
2. `6 -> 30`;
3. `10 -> 30`;
4. `12 -> 60`;
5. `30 -> 60`.

E004 reuses E001's exact reduced-residue filtering semantics but does not inspect or retune against E001/E002 transition counts. For each edge it freezes exact coarse projection, ordered refinement fibres, forbidden-lift masks, integer balance vectors, and exact 2x2-minor systems. The forced zero projection residual on the high E004 bands is validation-only and cannot be promoted.

Fresh metadata-only partition:

- E004 pre-discovery guard G4-pre: `[38_000_000, 39_000_000)`;
- discovery D4: `[39_000_000, 40_000_000)`;
- E004 discovery/holdout guard G4-mid: `[40_000_000, 41_000_000)`;
- untouched holdout H4: `[41_000_000, 42_000_000)`;
- adversarial A4: `[78_000_000, 79_000_000)`.

The range rule uses only the established width, H3 metadata, and arithmetic: leave one full-width guard after H3, take D4, leave one full-width guard before H4, and set A4's lower endpoint to twice D4's lower endpoint. At freeze, committed generation provenance reaches only through D3's final integer 35,999,999, so D4/H4/A4 are untouched. A1=`[33_000_000,34_000_000)`, H3=`[37_000_000,38_000_000)`, and A3=`[70_000_000,71_000_000)` retain their frozen historical roles and are excluded from E004.

Promotion cap: 5 observations. The only admissible families are complete uniform refinement on one relation, complete positive rank-one refinement on one relation, a strict unique repeated nonempty forbidden-lift mask, a strict unique repeated nonzero balance vector, or a strict unique repeated nontrivial minor-zero mask. Projection identities, support completeness by itself, enumeration identities, and serialization consequences are excluded. Exact one-shot H4 templates and deterministic tie/ordering rules are frozen in the E004 specification.

Generation guard: D4 execution may generate only historically generated low base support inside `[0,100_000)` plus segmented D4. Whole-prefix generation above 100,000 is forbidden. Every high-value interval must be predeclared, be a subset of the currently authorized E004 target, and reject A1/H3/A3, E003 ranges/guards, E004 guards, and all non-target E004 bands before generation.

Goal: test whether exact non-definitional refinement/factorization structure exists across the predeclared related moduli.

D4 execution result: implementation/test checkpoint `15fd85b14a079ece06bb89e786695d093c7b574b` passed 13/13 focused E004 tests plus compilation before generation. The validated plan used only low base support `[0,6325)` plus segmented D4. The identical complete D4 command was executed twice before inspection and produced byte-identical 224,641-byte artifacts, SHA-256 `4d0fa870a3bb304809bc713fbf0536d7c9a1e69d73273b8b6aeae9af570b2b1c`. D4 contains 57,252 primes. All frozen transition supports are complete and all mandatory projection residuals are zero.

Promotion result: **NO ELIGIBLE OBSERVATION**. P1 and P2 fail on every relation. P3 and P5 have zero filtered coarse pairs on every relation. P4 has 4, 4, 16, 16, and 64 eligible nonzero balance vectors across the frozen relation order, but every exact vector occurs once, so every modal count ties its runner-up 1–1 and fails both strict-unique-mode and occurrence-floor requirements. No `OBS-###` was allocated, no H4 criterion was needed, and H4/A4/A1/H3/A3 remain untouched. Compact evidence: `research/evidence/E004_D4_discovery.json`; execution record: `experiments/E004_D4_DISCOVERY_2026-10-06.md`.

Next bounded action: D1-11 / SQ-005 — design and freeze the first quarantined historical rediscovery calibration benchmark before any calibration execution or unblinding. Do not mine D4 further.

## SQ-005 — Historical rediscovery calibration

Stage: calibration

Status: **METHODOLOGICALLY COMPLETE — E005 MECHANICAL PARTIAL_PASS; HISTORICAL COMPARISON STALLED_BEFORE_KEY_IDEA; D1-14 PROCESS-HARDENING COMPLETE; QUARANTINE PRESERVED**

Governing protocol: `docs/CALIBRATION_PROTOCOL.md`.

Frozen benchmark and execution history remain unchanged:

- `experiments/E005_PRIME_COUNT_SCALE_CALIBRATION.md`;
- `experiments/E005_BLINDED_EXECUTION_2026-10-06.md`;
- `experiments/E005_PRE_UNBLINDING_SUMMARY_2026-10-06.md`;
- `experiments/E005_HISTORICAL_UNBLINDING_2026-10-06.md`;
- `research/evidence/E005_development_selection.json`;
- `research/evidence/E005_assessment.json`.

The D1-12 mechanical result remains exactly **PARTIAL_PASS** and the D1-13 historical comparison remains exactly **STALLED_BEFORE_KEY_IDEA**. D1-14 did not rerun, recompute, retune, relabel, or reinterpret E005.

D1-14 extracted only target-agnostic process lessons and encoded them in the calibration protocol:

1. **Representation-switch trigger.** When a frozen representation family achieves some development compression but fails predeclared assessment/holdout/residual-persistence criteria, freeze that result rather than retuning the failed grammar on inspected data. Any continuation must be a separately frozen stage with a qualitatively different representation family and untouched assessment data; after historical unblinding, no new target-specific stage on that benchmark counts as blinded rediscovery.
2. **Scoring diagnostics.** Future multi-subscale selectors must expose per-subscale scores/contributions, identify the dominant or worst-case subscale under the frozen aggregation rule, predeclare an influence diagnostic such as leave-one-subscale-out re-ranking, and flag subscale-sensitive winners without retrospectively changing them. Post-assessment reweighting/removal creates a new design requiring fresh untouched assessment data.

These safeguards are calibration-method rules only. They do not import any E005 historical object, transform, selected/unselected candidate, mechanism, or source-derived structure into the novelty lane.

Novelty reserves A1=`[33_000_000,34_000_000)`, H3=`[37_000_000,38_000_000)`, H4=`[41_000_000,42_000_000)`, A3=`[70_000_000,71_000_000)`, and A4=`[78_000_000,79_000_000)` remain untouched/uninspected. No existing observation/candidate/failure status changed, no novelty evidence was created, and no novelty collision audit was performed.

SQ-005 is closed methodologically. Historical calibration records remain permanently quarantined from novelty synthesis.

Next bounded action: **D1-15 / SQ-006 novelty representation-family preflight.** Return to the novelty lane in a design-only unit. Using only the project charter, discovery protocol, frozen novelty-lane records, and target-agnostic methodology, choose and freeze one qualitatively distinct representation family not already exhausted by E001/E003/E004. Do not generate prime data, inspect protected reserves, allocate OBS/CAND IDs, run prior-art search, or use E005 historical objects to choose the family.

## SQ-006 — Translation-overlap spectrum

Stage: discovery / replication complete

Status: **D1-18 CANDIDATE TRIAGE COMPLETE — NO CANDIDATE; OBS-008 RETAINED REPLICATED; OBS-005/006/007/009 REFUTED; A6 UNTOUCHED; SQ-006 CLOSED**

Frozen specification: experiments/E006_TRANSLATION_OVERLAP_SPECTRUM.md

Purpose: exact value-space translation overlap of the band-local prime indicator, counting all prime pairs at frozen even shifts whether or not consecutive.

Frozen partition remains unchanged:

- D6: [42_000_000,43_000_000) — executed in D1-16;
- G6-mid: [43_000_000,44_000_000) — non-target / ungenerated;
- H6: [44_000_000,45_000_000) — executed in D1-17 as one-shot criterion-only holdout;
- A6: [84_000_000,85_000_000) — untouched adversarial band.

Historical A1, H3, H4, A3, A4, and every E003/E004 guard retain their frozen untouched/non-target roles.

Frozen grammar remains exactly H=1000, shifts {2,4,...,1000}, common anchor [L,U-H), all-pairs C_B(h), and non-promotable odd-radical control classes. Metadata remain 500 shifts, 204 radical classes, and exactly 11 classes of size at least 8.

Implementation/test checkpoint: 8bfcc27d96dc1b0858c514cf2bfab81790ab71b0. Focused validation passed 14/14 tests plus compilation before D6 generation. Ruff/current-head CI observability remain only the existing FAIL-001/FAIL-002 environment limitations.

D6 generation plan was exactly low support [0,6558) plus segmented D6. The identical complete D6 command was executed twice before inspection and produced byte-identical 111,534-byte artifacts, SHA-256 0e3e1565f3d26b221ffc17ecd8e550db445390e210213aaa27c77045e339a23c. D6 contains 56,915 primes. No high-value prime generation occurred outside D6.

Mechanical promotion result: all 11 size-at-least-8 radical classes had strict unique maxima with target counts at least 8. The frozen ranking/cap promoted exactly five observations:

- OBS-005: rho=15, h=900, count 11,503 vs runner-up 11,440, margin 63;
- OBS-006: rho=35, h=280, count 6,905 vs 6,852, margin 53;
- OBS-007: rho=7, h=56, count 5,225 vs 5,184, margin 41;
- OBS-008: rho=21, h=294, count 10,373 vs 10,333, margin 40;
- OBS-009: rho=3, h=324, count 8,675 vs 8,643, margin 32.

The six lower-ranked eligible classes were not promoted because of the frozen cap. No grammar was relaxed. Compact evidence is research/evidence/E006_D6_discovery.json and the execution record is experiments/E006_D6_DISCOVERY_2026-10-06.md.

The exact one-shot H6 criteria for OBS-005 through OBS-009 were frozen in the observation ledger before H6 generation. D1-17 reused the unchanged implementation/test checkpoint `8bfcc27d96dc1b0858c514cf2bfab81790ab71b0`, validated the H6-only plan `[0,6709)` plus segmented H6, and executed the identical H6 command twice before criterion inspection. The outputs were byte-identical: 111,561 bytes, SHA-256 `be1694f488777be97202d9ccb047d56ba97a2d8fe087bab968090837dfc6ca3e`.

Frozen H6 outcomes: **OBS-008 REPLICATED** with target h=294 at 10,305 versus highest rho=21 competitor h=126 at 10,301 (margin +4). **OBS-005 REFUTED**: h=900 has 11,397 versus h=90 at 11,456. **OBS-006 REFUTED**: h=280 has 6,776 versus h=560 at 6,855. **OBS-007 REFUTED**: h=56 has 5,047 versus h=28 at 5,179. **OBS-009 REFUTED**: h=324 has 8,527 versus h=216 at 8,667. Every target count exceeds the occurrence floor of 8; all four failures are solely higher-frequency same-class competitors. Compact evidence is `research/evidence/E006_H6_replication.json`; replication record is `experiments/E006_H6_REPLICATION_2026-10-06.md`.

H6 was inspected only against those five frozen criteria. No new H6 observation was promoted, no failed target was retargeted, and no unselected class was mined. A6 and all historical protected ranges/guards remain untouched/non-target.

D1-18 candidate-synthesis result: **NO CANDIDATE CREATED.** Only OBS-008 was eligible for consideration. Its exact committed evidence is the rho=21 within-class strict maximum at h=294 on D6 (10,373 versus 10,333) and H6 (10,305 versus highest same-class competitor h=126 at 10,301). A statement restricted to exactly D6 and H6 would only restate those finite computations. Any broader statement would require an unsupported quantifier over an untested band, origin, width, later scale, infinite family, or broader shift/class family. No such quantifier is supplied by E006, so no `CAND-###` was allocated. OBS-008 remains REPLICATED with no candidate link. A6 remains frozen, untouched, uninspected, and unexecuted.

SQ-006 is closed without candidate promotion. No mechanism/proof work, prior-art/collision search, literature search, new prime-derived computation, H6 mining, retargeting, or protected-range inspection occurred.

Next bounded action: **D1-19 / SQ-007 blind novelty representation-family preflight.** Select and freeze exactly one qualitatively distinct novelty representation family using only novelty-lane authority and target-agnostic methodology. Generate no prime-derived data, preserve all historical reserves/guards including A6, allocate no OBS/CAND IDs, and do not use SQ-005 calibration objects or historical-unblinding mechanisms to steer the family.

## SQ-007 — Blind novelty neighbour-factorization coupling

Stage: discovery

Status: **D1-22 CANDIDATE TRIAGE COMPLETE — NO CANDIDATE; OBS-010/OBS-011 RETAINED REPLICATED; A7 UNTOUCHED; SQ-007 CLOSED**

Frozen specification: `experiments/E007_NEIGHBOUR_FACTORIZATION_COUPLING.md`

Purpose: test exact multiplicative coupling between the two neighbouring composites around an odd anchor. E007 strips every power of two from `x-1` and `x+1`, canonically aligns the two sides by their forced thin/thick 2-adic roles, factors the odd cores exactly, and compares four frozen profile families at prime anchors against odd-composite control anchors.

Qualitative distinction: E007 is not a gap/difference/occupancy/event representation (E001/E003), not residue-transition factorization (E004), and not additive translation overlap (E006). Its primitive discovery object is the exact multiplicative factorization profile of the adjacent even composites around each odd anchor.

Fresh metadata-only partition:

- G7-pre: `[45_000_000,46_000_000)` — non-target / ungenerated;
- D7: `[46_000_000,47_000_000)` — discovery / untouched at freeze;
- G7-mid: `[47_000_000,48_000_000)` — non-target / ungenerated;
- H7: `[48_000_000,49_000_000)` — untouched holdout;
- A7: `[92_000_000,93_000_000)` — untouched adversarial reserve, from the frozen `2*L_D` convention.

A1=`[33_000_000,34_000_000)`, H3=`[37_000_000,38_000_000)`, H4=`[41_000_000,42_000_000)`, G6-mid=`[43_000_000,44_000_000)`, A3=`[70_000_000,71_000_000)`, A4=`[78_000_000,79_000_000)`, A6=`[84_000_000,85_000_000)`, and every E003/E004 guard remain frozen untouched/non-target and are never E007 targets.

Frozen anchor/control semantics:

- common odd-anchor domain `A_B={x: L<x<U-1, x odd}`, so both neighbours lie in-band;
- prime anchors `P_B` and odd composite controls `C_B` partition that common domain;
- exactly one neighbour has `v2=1` (thin T) and the other has `v2>=2` (thick K);
- all powers of two are stripped before any promotable signature;
- `gcd(o_T,o_K)=1`, thin-side physical orientation, 2-adic control counts, factorization reconstruction, and composite-control frequencies by themselves are non-promotable controls.

Frozen promotable families, at most one observation each:

1. F1 exponent-shape pair `(sigma(o_T),sigma(o_K))`;
2. F2 distinct-factor-count pair `(omega(o_T),omega(o_K))`;
3. F3 total-multiplicity pair `(Omega(o_T),Omega(o_K))`;
4. F4 sign of the largest-odd-factor comparison `sgn(Pplus(o_T)-Pplus(o_K))`.

For each family, only the strict unique mode of the complete D7 prime-anchor table can be considered. The family fails mechanically on a tied prime mode. Frozen population floor is 1,000 prime anchors and 1,000 composite controls; frozen target-occurrence floor is 32. A target must also have strictly positive exact enrichment numerator `n_P(t)N_C-n_C(t)N_P`; no floating normalization is allowed. A family can contribute no alternate target if its mode fails. Hard promotion cap: 4 observations, with exact duplicate suppression as specified in E007.

Any promoted D7 observation must freeze the exact same-family/same-target H7 criterion before H7 generation. H7 requires unchanged semantics, both population floors, the same target as strict unique prime mode, target count at least 32, and strictly positive exact enrichment numerator. H7 is not available for mining.

Future generation is fail-closed. Low whole-prefix prime support is confined to historically safe `[0,100_000)`; every new high-value prime-generation interval must be segmented directly inside the authorized target. D7 may generate only segmented `[46_000_000,47_000_000)` plus exact low support through 6,855 (exclusive endpoint at most 6,856). Any whole-prefix, partial-target, guard, holdout, adversarial, historical protected, or other non-target traversal must fail before prime generation.

D1-19 generated no primes or other prime-derived output, inspected no protected range, allocated no OBS/CAND ID, performed no mechanism/proof or prior-art/literature work, and did not use SQ-005 calibration objects or historical-unblinding mechanisms to steer E007.

D1-20 implemented the frozen evaluator and fail-closed planner at implementation/test checkpoint `ad09ec3d72dc291d4930f13d9954a5a155590574`. Focused E007 validation passed 22/22 tests and compilation before D7 generation; Ruff remained unavailable under existing FAIL-001/FAIL-002. The canonical D7 plan used only low support `[0,6856)` plus segmented D7=`[46_000_000,47_000_000)`; all deliberate whole-prefix, partial-target, guard, holdout, adversarial, historical protected/generated, and other non-target requests failed before generation.

The identical complete D7 command ran twice before descriptive inspection and produced byte-identical 448,997-byte artifacts, SHA-256 `dde63c44ed6090c0dbdd7897e440b7cbd642336c82dbc126c513acc1357f4635`. D7 has 499,999 common odd anchors: 56,640 prime anchors and 443,359 composite controls. All factorization reconstruction, thin/thick classification, and odd-core gcd validation-failure counts are zero.

Frozen mechanical promotion result: F1 and F4 fail positive enrichment and have no fallback; F2 target `[3,3]` is eligible with prime count 7,740, runner-up 6,364, composite count 52,501, and enrichment numerator 457,942,020; F3 target `[3,3]` is eligible with prime count 5,009, runner-up 3,958, composite count 39,183, and enrichment numerator 1,460,111. The F2 and F3 targets select different prime-anchor subsets, so duplicate suppression removes neither. `OBS-010` and `OBS-011` are allocated at status OBSERVED with exact unchanged one-shot H7 criteria frozen in the observation ledger. H7/A7 and all guards/historical protected ranges remain untouched/non-target.

D1-21 verified the frozen evaluator/test bytes against checkpoint `ad09ec3d72dc291d4930f13d9954a5a155590574`, passed 22/22 focused tests and compilation, and reused FAIL-001/FAIL-002 for unavailable Ruff and empty GitHub CI-observability collections. Before generation, the exact H7 plan `[0,7000)` low support plus segmented H7=`[48_000_000,49_000_000)` was validated; 30 deliberate whole-prefix, wrong-support, partial/expanded, guard, protected/generated, adversarial, and other non-target plans failed before generation.

The identical complete H7 command then ran twice before criterion inspection and produced byte-identical 450,687-byte artifacts, SHA-256 `6a25381c7430a6e720e619fb27696ec75e8696514d72a8f7a26398f616d85ced`. Only the frozen anchor-population and F2/F3 same-target criteria were inspected. H7 has 56,387 prime anchors and 443,612 composite controls. OBS-010/F2 `[3,3]` REPLICATED with prime count 7,917 versus highest competitor `[3,2]` at 6,404, composite target count 52,339, and enrichment numerator 560,837,011. OBS-011/F3 `[3,3]` REPLICATED with prime count 5,106 versus highest competitor `[3,2]` at 3,977, composite target count 38,940, and enrichment numerator 69,373,092. No fallback, retargeting, H7 mining, or non-target-family promotion inspection occurred. A7 and all guards/historical protected ranges remain untouched/non-target.

D1-22 candidate-synthesis result: **NO CANDIDATE CREATED.** Only OBS-010 and OBS-011 were eligible. Separately, each frozen family statement is established only on D7 and H7: exact target `[3,3]` remains the strict unique prime-anchor mode, both support floors pass, and exact composite-control enrichment is positive under unchanged F2 or F3 semantics. A statement confined to those two bands would only restate committed finite computation. Any stronger statement requires an unsupported quantifier over an untested band, origin, width, later scale, anchor population, factorization/representation family, or infinitely many values.

The one permitted joint synthesis also fails candidate promotion. Saying that both F2 and F3 target `[3,3]` satisfy their frozen criteria on D7 and H7 is only the conjunction of OBS-010 and OBS-011; asserting common persistence or stronger cross-family coupling beyond those bands adds structure and a quantifier not supplied by the committed evidence. No `CAND-###` was allocated, both observations remain REPLICATED with no candidate link, and no novelty status was assigned.

SQ-007 is closed without candidate promotion. A7=`[92_000_000,93_000_000)` remains frozen, untouched, uninspected, and unexecuted. No new prime-derived computation, D7/H7 mining, retargeting, factorization-rule change, mechanism/proof work, adversarial execution, prior-art/collision search, literature search, novelty claim, calibration-object transfer, or protected-range inspection occurred.

Next bounded action: **D1-23 / SQ-008 blind novelty representation-family preflight.** Select and freeze exactly one qualitatively distinct blind novelty representation family using only novelty-lane authority and target-agnostic methodology. The next unit is design-only: it may choose a fresh metadata-only partition and freeze exact primitive/transform, descriptive/promotion, one-shot holdout, determinism, and fail-closed future-generation rules, but it must generate no prime-derived output, preserve A7 and all historical reserves/guards, allocate no OBS/CAND ID, and perform no mechanism/proof or prior-art/literature work.

## SQ-008 — Binary core-shape signatures

Stage: discovery

Status: **D1-23 PREFLIGHT COMPLETE — E008 FROZEN / NOT EXECUTED; D8/H8/A8 UNGENERATED; D1-24 DISCOVERY EXECUTION NEXT**

Frozen specification: `experiments/E008_BINARY_CORE_SHAPES.md`

Purpose: study exact word-shape coarsenings of a fixed 19-bit low-order binary core on individual integer anchors, comparing primes against composite controls from the same predeclared small-prime-admissible domain.

Qualitative distinction: E008 is not a consecutive-gap/finite-difference/residue-transition/occupancy/global-record representation (E001), not event-centred (E003), not residue-transition factorization (E004), not additive translation overlap (E006), and not neighbour-factorization coupling (E007). Its primitive discovery object is the binary coordinate word of one admissible integer anchor.

Fresh metadata-only partition:

- G8-pre: `[49_000_000,50_000_000)` — non-target / ungenerated;
- D8: `[50_000_000,51_000_000)` — discovery / untouched at freeze;
- G8-mid: `[51_000_000,52_000_000)` — non-target / ungenerated;
- H8: `[52_000_000,53_000_000)` — untouched holdout;
- A8: `[66_000_000,67_000_000)` — untouched adversarial reserve.

D8 and H8 lie in the 26-bit shell `[2^25,2^26)`. A8 is selected by the frozen arithmetic same-shell edge rule: it is the greatest million-aligned full-width band below `2^26=67_108_864`. This keeps the future adversarial test in the identical 26-bit coordinate regime without using prime behaviour. The partition is disjoint from every historical generated novelty band, every historical guard, and A1/H3/H4/A3/A4/A6/A7.

Frozen anchor/control domain:

- `Q=2*3*5*7=210`, chosen as the product of the first four primes and used only as an artifact-control wheel;
- `A_B={x in [L,U): gcd(x,210)=1}`;
- prime anchors `P_B` and composite anchors `C_B` partition `A_B`;
- parity and direct divisibility by 3, 5, and 7 are therefore matched before binary signatures are compared.

Frozen coordinate normalization:

- every D8/H8/A8 anchor has a unique 26-bit expansion;
- with `W=1_000_000`, `J=floor(log2(W-1))=19`;
- define `w(x)=(b_19,b_18,...,b_1)`;
- omit `b_0` because Q-admissibility forces it to 1;
- omit `b_20,...,b_25` because a width-W interval need not make those coordinates vary;
- the exact 19-bit word and its exact-word frequency table are non-promotable/non-serializable discovery objects.

Exactly four promotable shape families are frozen:

1. B1 — Hamming weight of the 19-bit core;
2. B2 — adjacent bit-transition count;
3. B3 — ordered pair of longest zero-run and longest one-run lengths;
4. B4 — nonincreasing sorted tuple of maximal run lengths, discarding bit labels and run order.

For each family, only the strict unique mode of the complete D8 prime-anchor frequency table may be considered. The frozen population floor is 1,000 for both prime and composite populations; the target-occurrence floor is 32. A target must also have strictly positive exact enrichment numerator `n_P(t)N_C-n_C(t)N_P` against the Q-admissible composite controls. A tied mode or failed target has no fallback. Exact duplicate suppression keeps the lower-numbered family when two eligible targets select exactly the same D8 prime-anchor subset. Hard promotion cap: 4 observations.

Any promoted D8 observation must freeze its exact same-family/same-target H8 criterion before H8 generation. H8 succeeds only if unchanged E008 semantics preserve both population floors, the exact target as strict unique prime mode, target count at least 32, and strictly positive exact enrichment. H8 is never available for mining or retargeting.

Future generation is fail-closed. Low whole-prefix support is confined to historically safe `[0,100_000)`; every new high-value interval must be segmented directly inside the one currently authorized target. D8 may use only segmented `[50_000_000,51_000_000)` plus exact low support through 7,141 (exclusive endpoint at most 7,142). H8 would require at most `[0,7281)`; A8 at most `[0,8186)`. Whole-prefix, partial/expanded target, guard, holdout, adversarial, historical protected/generated, or other non-target traversals must fail before prime generation.

D1-23 generated no primes or other prime-derived output, inspected no protected target/reserve/guard, allocated no OBS/CAND ID, did not edit the observation or conjecture ledgers, performed no mechanism/proof/adversarial/prior-art/collision/literature work, and transferred no E005 calibration object or E007 observation into E008.

Next bounded action: **D1-24 / SQ-008 E008 D8 discovery execution.** Implement the frozen E008 evaluator and fail-closed planner, satisfy every pre-generation validation obligation, execute D8 only twice for byte determinism, inspect only the frozen allowlist, mechanically apply only B1-B4 promotion, freeze exact H8 criteria for any promoted observations, and stop without H8/A8, candidate, mechanism/proof, or prior-art/literature work.
