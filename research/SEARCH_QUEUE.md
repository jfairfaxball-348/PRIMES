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

Status: **PREFLIGHT NEXT — NOT YET FROZEN / NOT EXECUTED**

Compare transition fingerprints across related moduli and ask whether one fingerprint can be exactly derived from another by a simple projection/refinement rule.

Goal: exact inter-modulus identities or forbidden transition patterns.

Promotion cap: 5 observations.

## SQ-005 — Historical rediscovery calibration

Stage: calibration

Run the method in the quarantined calibration lane described in docs/CALIBRATION_PROTOCOL.md.

Goal: learn which discovery operations are capable of producing genuinely explanatory objects.

Nothing from this queue item can be promoted as novel.
