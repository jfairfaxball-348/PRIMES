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

Status: **D1-24 D8 DISCOVERY COMPLETE — NO ELIGIBLE OBSERVATION; H8/A8 UNTOUCHED; SQ-008 CLOSED**

Frozen specification: `experiments/E008_BINARY_CORE_SHAPES.md`

Execution record: `experiments/E008_D8_DISCOVERY_2026-10-07.md`

Compact evidence: `research/evidence/E008_D8_discovery.json`

Purpose: study exact word-shape coarsenings of a fixed 19-bit low-order binary core on individual integer anchors, comparing primes against composite controls from the same predeclared Q=210 admissible domain.

Frozen partition remains:

- G8-pre: `[49_000_000,50_000_000)` — non-target / ungenerated;
- D8: `[50_000_000,51_000_000)` — discovery / executed in D1-24 only;
- G8-mid: `[51_000_000,52_000_000)` — non-target / ungenerated;
- H8: `[52_000_000,53_000_000)` — untouched holdout;
- A8: `[66_000_000,67_000_000)` — untouched adversarial reserve.

D1-24 implementation/test checkpoint `234a11378c64749a0638cb580f1045817ed25062` preserves frozen Q=210, W=1,000,000, 26-bit shell, J=19, core `(b_19,...,b_1)`, B1-B4, exact composite control, integer enrichment, support floors, duplicate suppression, promotion cap, deterministic allowlist/serialization, and fail-closed generation guard. Exact committed blobs are evaluator `1293af766b1906339330406c829694f78b6debd8` and focused tests `faa04909656517ef95fcac547cfe1fff44e98373`.

Pre-generation validation passed 19/19 focused tests plus compilation on the exact committed bytes. The canonical D8 generation plan used only low support `[0,7142)` plus segmented D8. Deliberate whole-prefix, wrong-support, partial/expanded, guard, holdout, adversarial, historical generated/protected, and other non-target plans failed before the prime generator was called. Ruff remained unavailable only under existing FAIL-001/FAIL-002 environment limitations.

The identical complete D8 command was executed twice before descriptive inspection and produced byte-identical 220,817-byte artifacts, SHA-256 `f5cf0a93ac556d9634885a4ece6e1c2d1f59fd4c9241370295d9fbaef4722b28`. D8 has 228,571 Q-admissible anchors: 56,360 prime anchors and 172,211 composite controls. First/last prime anchors are 50,000,017 and 50,999,999. All four required validation-failure counts are zero.

Frozen mechanical promotion result: **NO ELIGIBLE OBSERVATION**. All four families have strict unique prime-anchor modes and clear the population/occurrence floors, but every exact mode enrichment numerator against Q-admissible composite controls is negative:

- B1 target `10`: prime 10,006, runner-up 9,725, composite 30,585, enrichment -627,334;
- B2 target `9`: prime 10,550, runner-up 9,638, composite 32,322, enrichment -4,841,870;
- B3 target `[3,3]`: prime 5,491, runner-up 4,146, composite 17,117, enrichment -19,103,519;
- B4 target `[4,3,2,2,2,1,1,1,1,1,1]`: prime 1,946, runner-up 1,633, composite 6,057, enrichment -6,249,914.

No fallback target is permitted, no `OBS-###` ID is allocated, and no H8 criterion is required. H8/A8 and all guards/historical protected ranges remain untouched/non-target. No candidate, mechanism/proof, adversarial, prior-art/collision, literature, novelty, or calibration-transfer work occurred.

SQ-008 is closed without retuning or replacement.

Next bounded action: **D1-25 / SQ-009 blind novelty representation-family preflight.** Choose and freeze exactly one qualitatively distinct blind novelty representation family using only novelty-lane authority and target-agnostic methodology. Select a fresh metadata-only partition, freeze exact primitive/transform, descriptive/promotion, one-shot holdout, determinism, and fail-closed future-generation rules, and generate no prime-derived output. Preserve H8/A8, A7, and every historical reserve/holdout/guard; allocate no OBS/CAND ID; perform no mechanism/proof or prior-art/literature work.

## SQ-009 — Unit-action cover shapes

Stage: discovery

Status: **D1-28 SYNTHESIS COMPLETE — NO CANDIDATE CREATED; SQ-009 CLOSED; A9 UNTOUCHED**

Frozen specification: `experiments/E009_UNIT_ACTION_COVER_SHAPES.md`

Purpose: study exact algebraic action-cover shapes of individual Q-admissible integer anchors. For the fixed ordered basis A=(2,3,5,7), E009 computes exact multiplicative orders modulo each anchor, the exact odd-anchor unit-group exponent Lambda(x), and the inclusion-minimal basis subsets whose order-lcm attains Lambda(x). Prime anchors are compared against composite controls from the same gcd(x,210)=1 domain.

Qualitative distinction: E009 is not a gap/difference, occupancy/event, residue-transition/refinement, additive translation-overlap, neighbouring-factorization-profile, or digit-word experiment. Factorization is deterministic computation only; per-anchor factors, Lambda values, and raw order vectors are non-promotable and non-serializable. The discovery object is the canonical finite antichain of minimal action covers and three frozen exact coarsenings.

Fresh metadata-only partition:

- G9-pre: `[53_000_000,54_000_000)` — non-target / ungenerated;
- D9: `[54_000_000,55_000_000)` — discovery consumed in D1-26;
- G9-mid: `[55_000_000,56_000_000)` — non-target / ungenerated;
- H9: `[56_000_000,57_000_000)` — replication consumed in D1-27;
- A9: `[108_000_000,109_000_000)` — untouched adversarial reserve, selected by the frozen metadata-only rule L_A9=2*L_D9.

The partition uses only W=1,000,000, H8's frozen exclusive endpoint 53,000,000, historical protected/generated range metadata, and arithmetic. It is disjoint from every historical generated novelty band, A1/H3/H4/H8/A8/A3/A4/A6/A7, G6-mid/G7-pre/G7-mid/G8-pre/G8-mid, every E003/E004 guard, and all other protected/non-target ranges. A9 lies below the quarantined E005 calibration segments beginning at 128,000,000.

Frozen primitive/control domain:

- ordered action basis A=(2,3,5,7), chosen as the first four primes;
- Q=210;
- common anchor domain A_B={x in B:gcd(x,210)=1};
- exact prime/composite partition of A_B;
- exact deterministic ascending factorization of x;
- exact Lambda(x)=lcm(q^(e-1)(q-1)) over the odd prime powers q^e || x;
- exact multiplicative orders ord_x(a) for a in A, computed by prime-divisor reduction from Lambda(x);
- all 15 nonempty subsets of A ordered by cardinality then lexicographically;
- a subset covers x iff the lcm of its member orders equals Lambda(x);
- M(x) is the canonically ordered inclusion-minimal cover antichain, with the empty antichain permitted.

Exactly four promotable families are frozen:

1. C1: minimum minimal-cover size kappa(x), with 0 for an empty antichain;
2. C2: four-entry profile counting minimal covers by cardinality;
3. C3: four-entry profile counting all covering subsets by cardinality;
4. C4: the exact canonically ordered minimal-cover antichain M(x).

Only a family's strict unique D9 prime-anchor mode may be considered, with no fallback target. Promotion additionally requires N_P>=1000, N_C>=1000, target count>=32, and strictly positive exact enrichment numerator against Q-admissible composite controls. Exact duplicate suppression retains the lowest-numbered family if eligible targets select the identical subset of D9 prime anchors. The hard promotion cap is four, one per family.

Forced/control identities are ineligible: factorization reconstruction, Lambda construction, basis-unit gcd facts, order-divides-Lambda and order-witness facts, upward cover monotonicity, minimal-antichain construction identities, C1-C3 coarsening identities, combinatorial bounds, control frequencies, and serialization/floor consequences cannot receive an OBS ID.

Every promoted D9 target must freeze the exact unchanged same-family/same-signature H9 criterion before H9 generation. Replication requires both H9 populations>=1000, the identical target as strict unique H9 prime mode, target count>=32, and strictly positive exact H9 enrichment. A tie, any higher competitor, floor failure, or nonpositive enrichment fails mechanically; there is no fallback, retargeting, or changed semantics.

Generation guard: D1-26 may use exactly low base support `[0,7417)` plus segmented D9 only. Whole-prefix generation above 100,000 and any wrong-support, partial/expanded/shifted target, guard, H9/A9, H8/A8, historical protected/generated, E005 calibration, or other non-target traversal must fail before any prime generator call. Later H9 would use exactly `[0,7550)` plus segmented H9; later A9 exactly `[0,10441)` plus segmented A9.

D1-26 implemented and validated the frozen evaluator/guard, with final runtime/test checkpoint `52f295f46ce8225f195f9e772dd7462a0dd873a1`. The canonical generation plan was exactly low support `[0,7417)` plus segmented D9. Two successful identical complete commands produced byte-identical 82,398-byte artifacts, SHA-256 `a157a7b62667a76fee741db33e1cbf60594cb83aa17c54c4cbf57eb399b7cde9`. Only the frozen descriptive allowlist was inspected; all eight validation-failure aggregates are zero.

D9 has 55,997 prime anchors and 172,574 Q-admissible composite controls. Frozen promotion produced exactly two observations. C2 target `[2,0,0,0]` is a strict unique prime mode with count 13,849 versus runner-up 11,341, composite count 35,767, and exact enrichment numerator 387,132,627 > 0, yielding OBS-012. C4 target `[]` is a strict unique prime mode with count 3,797 versus runner-up 3,078, composite count 5,003, and exact enrichment numerator 375,110,487 > 0, yielding OBS-013. C1 target `1` fails positive enrichment with numerator -457,132,656. C3 target `[2,5,4,1]` has positive enrichment but selects the identical D9 prime-anchor subset as C2 and is therefore duplicate-suppressed with no fallback.

OBS-012 and OBS-013 each had their exact unchanged same-family/same-signature H9 criteria frozen in the observation ledger before H9 generation. D1-27 then executed only H9 with exact low support `[0,7550)` plus segmented H9, after 22/22 focused tests, compilation, exact committed-byte verification, and 53 deliberate invalid-plan rejections before generation. The identical complete H9 command ran twice before criterion inspection and produced byte-identical 85,386-byte artifacts, SHA-256 `9fccccd71c49983870e226f6f03ab80bff60820874edc2fe09cfbc6fdd361126`. H9 has 56,105 prime anchors and 172,466 composite controls; all eight frozen runtime validation aggregates are zero. OBS-012 REPLICATED: target `[2,0,0,0]` has 13,900 prime occurrences versus highest competing count 11,411, 35,726 composite occurrences, and enrichment numerator 392,870,170 > 0. OBS-013 REPLICATED: target `[]` has 3,869 prime occurrences versus highest competing count 3,089, 5,075 composite occurrences, and enrichment numerator 382,538,079 > 0. No new H9 observation was allocated and no fallback, retargeting, or non-target signature mining occurred. A9 remains untouched/uninspected. No candidate was created and no candidate synthesis, mechanism/proof/adversarial work, prior-art/collision search, literature search, novelty claim, calibration-object transfer, or protected-range inspection was performed. Conjecture and failure ledgers remain unchanged.

D1-28 then performed synthesis-only candidate triage over the admissible pool `OBS-012` and `OBS-013` only. **NO CANDIDATE CREATED.** OBS-012 separately supports only the finite fact that C2 target `[2,0,0,0]` is the strict unique prime-anchor mode with positive exact composite-control enrichment in D9 and H9; confining a statement to those bands merely restates committed computation, while any extension requires an unsupported quantifier over band origin, width, scale, basis, wheel, anchor population, representation family, or infinitely many values. OBS-013 has the same synthesis outcome for C4 target `[]`: the D9+H9 statement is finite evidence, and persistence, eventuality, universality, broader-family or infinite-occurrence wording is unsupported.

The one permitted joint statement also fails candidate promotion. The exact conjunction that both targets satisfy their frozen criteria in D9 and H9 is only a packaging of two finite replicated facts. No anchor-level overlap or unlisted statistic was inspected, and no common mechanism, coupling, persistence law, scale law, basis/wheel generalization, or family-level claim is supported by the frozen evidence. Both observations remain REPLICATED with no candidate link; active candidates remain zero and no novelty status was allocated.

SQ-009 is closed without executing A9. A9=`[108_000_000,109_000_000)` remains frozen, untouched, uninspected, and unexecuted; G9-pre/G9-mid and all historical protected/non-target ranges retain their frozen roles. No new prime-derived computation, D9/H9 mining, retargeting, representation change, mechanism/proof work, adversarial execution, prior-art/collision search, literature search, novelty claim, calibration-object transfer, or protected-range inspection occurred.

Next bounded action: **D1-29 / SQ-010 blind novelty representation-family preflight.** Select and freeze exactly one qualitatively distinct blind novelty representation family using only novelty-lane authority and target-agnostic methodology. The unit is design-only: choose a fresh metadata-only partition by deterministic provenance/arithmetic rules, freeze exact primitives/transforms, artifact controls, descriptive allowlist, promotion grammar/cap, unchanged one-shot holdout criteria, deterministic serialization, and fail-closed future-generation rules. Generate no prime-derived output, preserve A9 and every historical reserve/holdout/guard, allocate no OBS/CAND ID, and perform no mechanism/proof/adversarial/prior-art/collision/literature/novelty work.

## SQ-010 — Quadratic-surd recurrence cycle shapes

Stage: discovery

Status: **D1-31 H10 COMPLETE — OBS-014 REFUTED; SQ-010 CLOSED; A10 UNTOUCHED**

Frozen specification: experiments/E010_QUADRATIC_SURD_CYCLE_SHAPES.md

Purpose: study exact multiplicity shapes of the denominator cycle in the integer-only periodic continued-fraction recurrence of sqrt(x) for individual Q-admissible nonsquare anchors. Prime anchors will be compared against composite controls from the same frozen common domain.

Qualitative distinction: E010 is a per-anchor quadratic-surd recurrence representation. It uses no consecutive-prime gaps/differences, occupancy/event neighbourhoods, residue-transition/refinement objects, additive translation overlaps, x±1 neighbour factorization, positional binary words, or modular unit-action/order/cover objects. No historical observation target seeds the family. SQ-005 contributes only generic freeze-before-output and qualitative-representation-switch discipline; no calibration object, score, residual, historical mechanism, or hidden target transfers into E010.

Fresh metadata-only partition:

- G10-pre: [57_000_000,58_000_000) — frozen non-target / ungenerated;
- D10: [58_000_000,59_000_000) — frozen discovery / untouched;
- G10-mid: [59_000_000,60_000_000) — frozen non-target / ungenerated;
- H10: [60_000_000,61_000_000) — frozen untouched one-shot holdout;
- A10: [116_000_000,117_000_000) — frozen untouched adversarial reserve.

The partition rule uses only committed range/provenance metadata and integer arithmetic. Starting at the exclusive upper endpoint 57,000,000 of consumed E009 H9, preserve one full million-width guard, then place D10, another guard, and H10 consecutively. Set L_A10=2*L_D10=116,000,000. These bands are mutually disjoint and disjoint from every historical generated novelty band, every historical guard, A1/H3/H4/H8/A8/A3/A4/A6/A7/A9, every other protected/non-target interval, and all quarantined E005 calibration segments. No existing reserve is consumed to place SQ-010.

Frozen common domain and recurrence:

- Q=210, the product of the first four primes, is a non-promotable small-prime artifact control only;
- A_B={x in B:gcd(x,210)=1 and x is not a perfect square};
- P_B and C_B are respectively prime and composite anchors in A_B;
- a0=isqrt(x), with exact nonsquare bracket a0^2<x<(a0+1)^2;
- exact recurrence m_{k+1}=d_k a_k-m_k, d_{k+1}=(x-m_{k+1}^2)/d_k, a_{k+1}=floor((a0+m_{k+1})/d_{k+1});
- positivity, divisibility, quotient bounds, first canonical terminal state (a0,1,2a0), and nonterminal-state-repeat rejection are validation-only;
- D(x)=(d_1,...,d_ell) is the exact denominator cycle through the terminal denominator;
- mu_x(v) counts occurrences of each distinct denominator value v;
- H(x)=(h_1,...,h_M), where h_j is the number of distinct denominator values occurring exactly j times and h_M>0.

Exactly four promotable families are frozen:

1. L1: period length ell;
2. L2: number of distinct recurrence denominators;
3. L3: maximum denominator multiplicity;
4. L4: exact denominator-multiplicity profile H(x).

Raw recurrence states, a0 values, denominator/partial-quotient words, convergents, and all unlisted transforms are non-promotable and non-serializable. L1-L3 are predeclared exact coarsenings of L4; the coarsening identities themselves are validation-only.

Promotion is frozen before D10: both P/C populations must be at least 1,000; only the strict unique D10 prime-anchor mode of a family can be considered; its prime count must be at least 32; and its exact enrichment numerator n_P(t)N_C-n_C(t)N_P must be strictly positive. A tie or failed gate gives no fallback. If eligible targets from multiple families select the identical D10 prime-anchor subset, retain only the lowest-numbered family. Hard cap: four observations, at most one per family.

Every promoted D10 observation must freeze its exact unchanged same-family/same-signature H10 criterion before H10 generation. H10 is replication-only: the same target must remain the strict unique prime mode, clear the unchanged 1,000/32 floors, and retain strictly positive exact enrichment. H10 cannot be mined, used for fallback/retargeting, or used to change the recurrence, family, threshold, control population, normalization, or feature set.

Determinism is frozen: canonical family/signature/ranking orders, stable lexical JSON keys, UTF-8, no nondeterministic metadata, and canonical writer equivalent to json.dumps(payload, sort_keys=True, indent=2)+"\n". The same complete command on the same implementation commit must be byte-identical.

Fail-closed future generation is frozen. Whole-prefix prime generation is allowed only inside historically safe [0,100_000). D1-30 may authorize exactly low support [0,7682) plus segmented D10=[58_000_000,59_000_000); floor(sqrt(58,999,999))=7,681. A later H10 mode would authorize exactly [0,7811) plus H10; a later A10 mode exactly [0,10817) plus A10. Any high whole-prefix, wrong low support, partial/expanded/shifted target, guard, historical generated/protected band, E005 calibration segment, or other non-target traversal must fail before the prime generator is called.

D1-29 generated no prime-derived data, executed no experiment, inspected no protected range, allocated no OBS/CAND ID, and performed no mechanism/proof/adversarial/prior-art/collision/literature/novelty work. Observation, conjecture, and failure records are unchanged.

D1-30 implemented and validated the frozen evaluator/runtime/guard before generation at final implementation checkpoint `e9ab511a06e612792cbf95953d2e1b71307fb40f`. Exact committed evaluator/runtime/native-helper/test blobs were reproduced locally; 19/19 focused tests passed and compilation succeeded. Ruff remains unavailable only under the existing FAIL-001/FAIL-002 detached-runner limitation. The canonical D10 generation plan was exactly low support `[0,7682)` plus segmented D10=`[58_000_000,59_000_000)`; deliberate wrong-support, high whole-prefix, partial/shifted/split, guard/H10/A10, historical, E005-calibration, and arbitrary non-target plans fail before the prime generator is called.

The identical complete D10 command was executed twice on the same checkpoint and same output path before descriptive inspection. Both artifacts are byte-identical: 52,653,877 bytes, SHA-256 `52c7be1bd4ba53eb78596fa7a0738a412742d10d31583a574901d47f1915ce74`. D10 has 228,558 Q-admissible nonsquare anchors, comprising 55,978 prime anchors and 172,580 composite controls; 15 Q-admissible perfect squares are excluded before labelling. All six frozen validation-failure aggregates are zero.

Mechanical L1-L4 promotion yields exactly one observation. L1 target `1331` is a strict unique prime mode with count 16 versus 15 and positive enrichment 2,033,566, but fails the frozen 32-occurrence floor. L2 target `1487` is a strict unique prime mode with count 44 versus 40, composite count 53, and exact enrichment `4,626,686 > 0`, so it is eligible. L3 target `8` has count 20,348 versus 20,232 but enrichment `-141,186,550`, so it fails. L4 target `[2,2]` has count 10 versus 9 and enrichment `-3,704,066`, so it fails both occurrence and enrichment. No duplicate suppression removes L2 because no other family survives the pre-duplicate gates.

**OBS-014** is allocated at status OBSERVED for exact L2 target `1487`; its unchanged same-family/same-signature one-shot H10 criterion is frozen in the observation ledger before any H10 generation. H10=`[60_000_000,61_000_000)` and A10=`[116_000_000,117_000_000)` remain untouched/uninspected/unexecuted. A9 and every historical protected/non-target range retain their prior roles. No candidate synthesis, mechanism/proof/adversarial work, prior-art/collision/literature search, novelty claim, historical-output mining, calibration transfer, fallback, retargeting, threshold/normalization change, or post-result feature invention occurred.

D1-31 executed only the frozen OBS-014 H10 criterion after checkpointing the H10 phase-control/test bytes at `9f9e6223ee0f05d64485cf713e75bd2160d19c92`. The H10 criterion artifact repeated byte-identically at 1,003 bytes with SHA-256 `8730125952a015951d4e2fa698e3e354ba59b03b0d5d1d3f29fb93c2f5d88ad9`. H10 has 55,930 prime anchors and 172,626 Q-admissible nonsquare composite controls. Frozen L2 target `1487` occurs 20 times among prime anchors, below the 32-occurrence floor, while the highest competing L2 prime count is 41; target composite count is 50 and exact target enrichment is still positive at `656,020`. Population floors and enrichment pass, but occurrence and strict-unique-mode fail, so **OBS-014 is REFUTED mechanically**. No competing signature identity was inspected or serialized, no fallback/retargeting occurred, and no new OBS/CAND ID was allocated.

SQ-010 is closed without A10 execution. A10=`[116_000_000,117_000_000)` remains frozen, untouched, uninspected, unexecuted, and ungenerated. G10-pre/G10-mid remain ungenerated non-target guards; A9 and all historical protected ranges retain their prior roles. Compact evidence is `research/evidence/E010_H10_replication.json`; execution record is `experiments/E010_H10_REPLICATION_2026-10-07.md`.

Next bounded action: **D1-32 / SQ-011 blind novelty representation-family preflight.** Select and freeze exactly one qualitatively distinct blind novelty representation family using only novelty-lane authority and target-agnostic methodology. The unit is design-only: choose a fresh metadata-only partition by deterministic provenance/arithmetic rules, freeze exact primitives/transforms, validation/triviality controls, descriptive allowlist, promotion grammar/cap, unchanged one-shot holdout criteria, deterministic serialization, and fail-closed future-generation rules. Generate no prime-derived output, preserve A10/A9 and every historical reserve/holdout/guard, allocate no OBS/CAND ID, and perform no mechanism/proof/adversarial/prior-art/collision/literature/novelty/calibration-transfer work.


## SQ-011 — Finite-field polynomial factor-degree shapes

Stage: discovery / replication / synthesis complete

Status: **CLOSED — D1-35 NO CANDIDATE CREATED; OBS-015 / OBS-016 / OBS-017 RETAINED REPLICATED; A11 UNTOUCHED**

Frozen specification: `experiments/E011_FINITE_FIELD_FACTOR_DEGREE_SHAPES.md`

D1-32 froze E011 before output. D1-33 implemented only the frozen exact finite-field evaluator, native arithmetic acceleration, fail-closed planner, deterministic serializer, and focused tests. The final pre-generation implementation/test checkpoint is `f9cfec77b4da93a714df00fc7513617a561c1f3c`, with evaluator blob `4344c3b94285e44da24a0f7eef1749a181ea4cdc`, native-helper blob `122728702f574afebefb4e0e8e37b1b702227000`, and focused-test blob `e03d359498ab35b670caf550af8a0cb3d45d7811`. The repository blobs were fetched back and matched the locally validated bytes before prime generation. Focused E011 validation passed 18 tests plus compilation; Ruff remains unavailable only under the existing FAIL-001/FAIL-002 detached-runner limitation.

The complete D11 generation plan was validated before either prime generator as exactly whole-prefix support `[0,7938)` plus segmented D11=`[62_000_000,63_000_000)`. The fail-closed gate rejects wrong support, high whole-prefix generation, partial/expanded/shifted/split/reordered D11, G11-pre/G11-mid/H11/A11, D10/H10/A10, D9/H9/A9, H8/A8, historical generated/protected/guard ranges, E005 calibration segments, and arbitrary non-target high intervals before generation.

The identical complete D11 command was executed twice on checkpoint `f9cfec77b4da93a714df00fc7513617a561c1f3c` with the same output path before descriptive inspection. The artifacts are byte-identical: 4,861 bytes, SHA-256 `8fa8aab43d0a7a452fdb7465f8ae42d4d2c7f8911b224d9d88a55e21ebd47d25`. Compact evidence is `research/evidence/E011_D11_discovery.json`; execution record is `experiments/E011_D11_DISCOVERY_2026-10-07.md`.

After byte identity, inspection was limited to the frozen allowlist. D11 has 55,706 prime anchors; first prime 62,000,009; last prime 62,999,999; all seven mandatory validation-failure aggregates are zero.

Frozen family results:

- K1: strict unique target `[2,1,1,1]`, count 18,575, highest competing count 13,868, 48 mixed Q=210 classes — eligible;
- K2: strict unique target `3`, count 23,152, highest competing count 18,575, 48 mixed classes — eligible;
- K3: strict unique target `3`, count 18,575, highest competing count 13,868, 48 mixed classes — passes individual gates but is exact-support duplicate-suppressed by lower-numbered K1;
- K4: strict unique target `2`, count 32,443, highest competing count 18,571, 48 mixed classes — eligible.

Mechanical promotion in frozen family order allocates exactly:

- OBS-015 — K1 target `[2,1,1,1]`;
- OBS-016 — K2 target `3`;
- OBS-017 — K4 target `2`.

For each, the observation ledger freezes the unchanged same-family/same-signature H11 criterion before any H11 generation: H11 prime population at least 1,000; identical target is the strict unique H11 mode of the same family; target count at least 32; target has at least 8 mixed Q=210 reduced residue classes; and all mandatory E011 validation aggregates are zero. A tie, higher competitor, any floor/control failure, or any validation failure mechanically REFUTES the observation. There is no fallback, retargeting, or polynomial/degree/family/control/threshold change.

D1-34 added only the minimal H11 phase-control and criterion-only serialization needed for the three frozen observations. The final pre-generation H11 checkpoint is `8194e8fa5e371e942c449e88d1abab0bea44839a`, with evaluator blob `610f962c99257a7148d0ef74b1d54963ebf05cf9`, focused-test blob `54c369328547a946ea0fb01bccea008bba969a81`, and the D1-33 native helper unchanged at `122728702f574afebefb4e0e8e37b1b702227000`. Core/config also remained unchanged. Before generation, checkpoint-pinned targeted validation passed Ruff, 20/20 focused E011 tests, compilation, exact blob checks, the unchanged native/reference finite-field checks, the exact frozen target map, criterion-only allowlist checks, and fail-closed H11 planning.

The canonical H11 plan was exactly whole-prefix support `[0,8063)` plus segmented H11=`[64_000_000,65_000_000)`. The identical complete H11 command was executed twice on the same checkpoint and same output path. Byte identity was established before criterion inspection. The criterion-only artifact is 2,205 bytes with SHA-256 `cfebc67d4bad294edd4d26e267ddab4ec434dbc73a34760ffb8445e5eb1ee9ef`; compact evidence is `research/evidence/E011_H11_replication.json` and the execution record is `experiments/E011_H11_REPLICATION_2026-10-07.md`.

After byte identity, inspection was limited to the three frozen criterion records and mandatory validation aggregates. H11 has 55,468 prime anchors and all seven validation-failure aggregates are zero. OBS-015 / K1 `[2,1,1,1]` has target count 18,508 versus highest competing count 13,863 and 48 mixed classes; OBS-016 / K2 `3` has 23,039 versus 18,508 and 48 mixed classes; OBS-017 / K4 `2` has 32,371 versus 18,490 and 48 mixed classes. Every unchanged population/occurrence/mixed-residue/strict-mode/validation gate passes for all three, so **OBS-015, OBS-016, and OBS-017 are REPLICATED mechanically**. No competing signature identity, unselected K3 mode, complete frequency table, per-prime object, residue identity/count table, polynomial internals, or new target was inspected.

Preserved state: G11-pre and G11-mid remain ungenerated non-target guards. H11 is now replication-consumed. A11=`[124_000_000,125_000_000)` remains frozen, untouched, uninspected, unexecuted, and ungenerated. A10, A9, H8/A8, and every historical protected range retain their prior frozen roles. No new OBS ID or CAND ID was allocated; no candidate synthesis, mechanism/proof/adversarial work, prior-art/collision/literature search, novelty claim, historical-output mining, calibration transfer, or protected-range inspection occurred.

D1-35 then performed synthesis-only triage over exactly OBS-015, OBS-016, and OBS-017 plus exact conjunctions of their already-committed aggregate facts. No `CAND-###` was allocated. Each individual target is a replicated strict unique mode in D11 and H11, but a statement restricted to those bands is only a finite restatement, while every stronger persistence, eventuality, universality, density, distributional, polynomial-family, degree-family, or scale statement would require a quantifier not supplied by the frozen E011 representation or evidence. Exact conjunctions likewise only package the finite facts; any stronger common coupling, simultaneous persistence, shared distribution, or factorization-law claim would introduce unsupported structure. No anchor-level overlap or new statistic was inspected.

**D1-35 conclusion: NO CANDIDATE CREATED.** OBS-015, OBS-016, and OBS-017 remain REPLICATED with no candidate link; active candidates remain zero and no novelty status was allocated. SQ-011 is closed without A11 execution. A11=`[124_000_000,125_000_000)` remains frozen, untouched, uninspected, unexecuted, and ungenerated. No new prime-derived computation, D11/H11 mining, retargeting, mechanism/proof/adversarial work, prior-art/collision/literature search, novelty claim, historical-output mining, calibration transfer, protected-range inspection, or post-result feature invention occurred.

Next bounded action: **D1-36 / SQ-012 blind novelty representation-family preflight.** Select and freeze exactly one qualitatively distinct, exact, target-agnostic representation family using only novelty-lane authority and generic target-agnostic protocol rules. This is design-only: generate no prime-derived output, preserve A11 and every historical protected/non-target range, allocate no OBS/CAND ID, and perform no mechanism/proof/adversarial/prior-art/collision/literature/novelty/calibration-transfer work.

## SQ-012 — Lattice-norm bracketing shapes

Stage: discovery

Status: **D1-36 PREFLIGHT COMPLETE — E012 FROZEN / NOT YET EXECUTED; D12/H12/A12 UNGENERATED**

Frozen specification: `experiments/E012_LATTICE_NORM_BRACKETING_SHAPES.md`

D1-36 selected exactly one new target-agnostic representation family before any E012 output: exact two-sided bracketing distances from an admissible integer anchor to the nearest strictly lower and strictly higher support values of the canonical integer-lattice squared Euclidean norm `a^2+b^2`, within a frozen horizon. The choice is explicitly labelled a theory-informed generic geometric primitive; it was not selected from a calibration object, historical target, prior observation, literature mechanism, or source-derived mechanism. Direct centre representability is excluded.

Qualitative distinction: E012 does not use prime-sequence adjacency/gaps/differences, occupancy or selected prime events, residue-transition/refinement tables, additive prime-pair overlaps, factorization of `x` or `x±1`, digit words, modular orders/action covers, quadratic-surd recurrences, finite-field polynomial factorization, or any prior observation value. Its auxiliary support set is an independently defined lattice-norm set, not a prime-derived sequence.

Frozen metadata-only partition, width `W=1_000_000`:

- G12-pre = `[65_000_000,66_000_000)` — non-target guard;
- historical A8 = `[66_000_000,67_000_000)` — preserved/skipped;
- D12 = `[67_000_000,68_000_000)` — discovery;
- G12-mid = `[68_000_000,69_000_000)` — non-target guard;
- H12 = `[69_000_000,70_000_000)` — untouched one-shot holdout;
- historical A3 = `[70_000_000,71_000_000)` — preserved;
- A12 = `[134_000_000,135_000_000)` — untouched adversarial reserve, from `L_A12=2*L_D12`.

Placement uses only committed range/protection provenance and arithmetic. No existing reserve is consumed. A12 is disjoint from A11/A10/A9 and from all quarantined E005 calibration segments.

Frozen controls and primitive:

- `Q=210` is a non-promotable small-prime admissibility control;
- `H=floor(sqrt(W))=1000`;
- common anchors satisfy `L+H<=x<U-H` and `gcd(x,210)=1`, then partition exactly into prime/composite populations;
- `S_B={a^2+b^2 in [L,U)}` is exact support only; representation multiplicity and lattice coordinates are non-promotable/non-serializable;
- brackets are the nearest strict lower/upper support values within distance H; the centre x is excluded;
- if either side is missing, every family signature is the distinguished `UNBRACKETED` value, which can never be promoted.

Exactly four families are frozen:

1. N1 = nearest bracket distance;
2. N2 = farther bracket distance;
3. N3 = bracket span;
4. N4 = unordered pair of the two bracket distances.

N1-N3 coarsening identities, lattice enumeration symmetries, UNBRACKETED status, residue classes, support/floor/serialization facts, and all other deterministic identities are validation/control only.

Artifact control and promotion are frozen before output. Overall prime/composite populations must each be at least 1,000; each odd mod-8 stratum `1,3,5,7` must contain at least 100 prime and 100 composite anchors; only a family's strict unique complete-prime-table mode may be considered; the target must be bracketed and occur at least 32 times. For each of the four mod-8 strata separately, exact enrichment `n_P(t)N_C-n_C(t)N_P` must be strictly positive. Any failed stratum fails promotion; there is no aggregate compensation or fallback. Exact support-set duplicate suppression retains the lowest family N1<N2<N3<N4. Hard cap: four observations.

Every promoted D12 record must freeze the exact unchanged same-family/same-signature H12 criterion before H12 generation. H12 must preserve the same total/per-stratum population floors, strict unique target, bracketed status, 32-occurrence floor, positive enrichment in every odd mod-8 stratum, and zero validation failures. No fallback, retargeting, norm/horizon/control/family/threshold change, or H12 mining is permitted.

Serialization is frozen and deliberately narrow: aggregate anchor/mod-8 populations, eight validation-failure counts, family modal summaries/gates, and promotion precursors only. Complete frequency tables, per-anchor records, lattice coordinates, norm multiplicities, raw support, centre representability, ordered bracket identities/values, non-mode signatures, alternate forms, and exploratory fields are forbidden. Canonical JSON ordering and byte-identical repeat semantics are frozen.

Fail-closed D12 prime generation is frozen as exactly whole-prefix low support `[0,8247)` plus segmented D12=`[67_000_000,68_000_000)`; lattice-norm enumeration is ordinary integer arithmetic restricted to norm values inside D12. A later H12 plan would be exactly `[0,8367)` plus H12; a later A12 plan exactly `[0,11619)` plus A12. Every historical generated/protected/guard/calibration range, A8/A3, G12-pre/G12-mid, out-of-phase H12/A12, wrong support, high whole-prefix generation, malformed targets, and arbitrary non-target interval must fail before prime generation.

D1-36 generated no primes, executed no evaluator, inspected no protected range, reran/mined no historical output, allocated no OBS/CAND ID, and performed no candidate/mechanism/proof/adversarial/prior-art/collision/literature/novelty work. Observation, conjecture, and failure ledgers remain unchanged.

Next bounded action: **D1-37 / SQ-012 — implement and execute frozen E012 D12 discovery only.** Validate the exact semantics and fail-closed plan, checkpoint implementation/test bytes before generation, run the identical D12 command twice before inspecting only the frozen allowlist, mechanically apply N1-N4 promotion, and leave H12/A12/A8/A3 and every historical protected/non-target range untouched.

