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

## SQ-006 — Novelty representation-family preflight

Stage: discovery

Status: **D1-15 PREFLIGHT NEXT — DESIGN ONLY / NO PRIME GENERATION**

Purpose: restart blind novelty discovery after closing the calibration lane, without transferring target-specific historical content from E005.

D1-15 must:

- select exactly one new representation family using only novelty-lane history plus the generic project/discovery methodology;
- make the family qualitatively distinct from the already executed E001 baseline grid, E003 event-centred neighbourhood grammar, and E004 residue-transition factorization grammar;
- freeze primitive objects, transform grammar, deterministic ordering/serialization, descriptive allowlist, promotion grammar, and one-shot holdout criterion templates before any output;
- select fresh discovery/holdout/adversarial ranges by a metadata-only rule that preserves A1/H3/A3/H4/A4 and all guard ranges as untouched/non-target;
- define a fail-closed generation plan before any later execution;
- keep E005 design/results/unblinded theory outside the novelty feature-selection rationale.

D1-15 is preflight only. It must not generate prime-derived output, inspect a protected range, allocate an `OBS-###` or `CAND-###`, alter an existing status, perform mechanism/proof work, or run a prior-art/collision audit.
