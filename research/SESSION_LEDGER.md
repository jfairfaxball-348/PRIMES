# Session Ledger

Permanent chronological record of bounded PRIMES research sessions.

## Session numbering

Use identifiers of the form `S001`, `S002`, ...

Never reuse or renumber a completed session.

### S001

**Date:** 2026-10-06  
**Stage:** discovery  
**Bounded objective:** D0-02 / SQ-001 preflight — confirm validated CI evidence, run E000 at at least two declared limits, verify deterministic summaries and data quality, freeze E001's representation grid and discovery/holdout partition before result inspection, and hand off one immediately runnable next unit.  
**Incoming state:** DISCOVERY-0 at main head `9cb129e337118a0c94bd2a96a32bc223362d38d0`; exact pipeline marked validated; no observations or candidates; E001 not yet defined; live prompt requested E000/E001 preflight.  
**Work performed:** Read all required authority and ledgers; reconciled the requested “conjecture ledger” to the repository's actual `research/CONJECTURE_REGISTER.md`; confirmed the durable GitHub Actions green checkpoint recorded for CI head `e47b272b6e3867fb10d0eefc199b1231557659da`; reconstructed the exact committed E000/core/test sources in an isolated runner; ran pytest; ran E000 twice at limits 10,000 and 100,000; compared outputs byte-for-byte and hashed them; independently regenerated primes by trial division at both limits; recorded the detached-runner network/Ruff limitation as FAIL-001; froze E001 gap, finite-difference, residue-transition, occupancy, and strict record-gap neighbourhood representations; predeclared D0/H0/A0 ranges; updated SQ-001, experiments documentation, programme status, and the live next-session prompt.  
**Result:** Preflight complete. E000 was deterministic at both declared limits and no data-quality defect was found. E001 is frozen before any E001 output inspection. Discovery D0 is `[0, 1_000_000)`; untouched holdout H0 is `[1_000_000, 2_000_000)`; reserved adversarial A0 is `[10_000_000, 11_000_000)`. E001 has not been executed. H0/A0 remain untouched. No observation or conjecture was created.  
**Observations/candidates affected:** none; active observations 0; active candidates 0.  
**Validation:** Project authority records package install, Ruff, pytest, and E000 smoke as passed at CI head `e47b272b6e3867fb10d0eefc199b1231557659da` (durably recorded by `66c3218320c79f329ccde8d4dfbd2de3e0102f5a`). Local reconstruction: `pytest` 9/9 passed. E000 limit 10,000 repeated byte-identically, SHA-256 `2a83b964998223251fc343b34a7b726c43c8996072a7910dac2de371bfbbca79`; E000 limit 100,000 repeated byte-identically, SHA-256 `4e4cbde9eb416c1c2162bec80c297440eac96d6da40fab480a9cb0721ed9b962`. Independent trial-division prime lists exactly matched the repository sieve at both limits.  
**Failures/limitations:** FAIL-001 — detached runner could not resolve github.com for direct clone and lacked Ruff locally. The GitHub connector available in-session did not expose current-head Actions check-run objects; therefore CI confirmation is tied exactly to the committed validated CI head rather than overstated for the later documentation-only head. No E000 data-quality failure found.  
**Decision blocker:** none  
**Outgoing state:** DISCOVERY-0; E001 preflight frozen; next task is implementation and D0-only discovery execution; H0/A0 untouched; candidate gate closed.  
**Next session:** D0-03 / SQ-001 — implement the frozen E001 specification, add deterministic/boundary tests, execute and inspect D0 only, freeze any exact observations and their H0 replication criteria, and do not run H0/A0 or create a candidate.  
**Commit:** substantive checkpoint commits `f3ae19fb38197948a9612c0f3d5c5556bc0166f8`, `98f4beb1e4c3a4c256849277737ba9757b6abc39`, `b3bc4ba65ac78f2655e2172eade79d42f21931dd`, `fbb1036228727f1a3e4515894be11cf0e5390bd9`, `80c8067a0d71465019e4cc6685e3aac06eebe373`, `96d13eda76992a421b2c1b108adaf5a9ba3102c6`, `d11c1308570d2202364d8582fa43a143952916c8`.

### S002

**Date:** 2026-10-06  
**Stage:** discovery  
**Bounded objective:** D0-03 / SQ-001 — implement the frozen E001 representation grid, validate boundary/determinism semantics, execute and inspect D0 only, freeze any exact observations and their one-shot H0 replication criteria, and leave H0/A0 untouched.  
**Incoming state:** DISCOVERY-0 at main head `32f93cfc4e89a64dab86f6767698a79761e63a30`; E001 specification and D0/H0/A0 partition frozen; no E001 output yet; no observations or candidates; candidate gate closed.  
**Work performed:** Read all required authority and experiment records before changing anything; implemented `experiments/E001_representation_grid.py` without changing the frozen representation grammar; added E001 tests for band-boundary exclusion, globally anchored occupancy, strict global record-gap event selection, deterministic counter ordering, and byte-deterministic serialization; locally ran pytest and compilation; generated D0 twice from implementation commit `beab213501dab318075199c3fcac6d5501d0b9d3`; verified byte identity and recorded the artifact digest; independently matched the D0 prime list against SymPy; inspected only D0; promoted four exact observations with frozen H0 criteria; recorded compact machine-readable evidence and the execution record; updated queue, programme status, failure ledger, and the live next-session prompt.  
**Result:** E001 D0 completed successfully. The repeated 24,923,621-byte discovery artifact is byte-identical with SHA-256 `822431d664d5a35949abdf230a1b8abb41afa1f97511b7c129e5d18779f2e284`. Four observations were promoted: OBS-001 (zero is the unique modal third forward difference), OBS-002 (`[6, 6]` is the unique modal width-2 gap motif), OBS-003 (complete directed reduced-residue transition support for every frozen modulus), and OBS-004 (no empty globally anchored width-100 D0 block). H0 and A0 remain untouched. No conjecture or candidate was created.  
**Observations/candidates affected:** OBS-001 through OBS-004 created at status OBSERVED; active observations 4; active candidates 0.  
**Validation:** `PYTHONPATH=src pytest -q` passed 14/14; `python -m compileall -q src experiments tests` succeeded; E001 D0 repeated byte-identically; independent SymPy `primerange(0, 1_000_000)` exactly matched the repository sieve with 78,498 primes and last prime 999,983. Local Ruff remained unavailable. The available GitHub connector returned no combined-status objects and no PR-triggered workflow-run objects for `beab213501dab318075199c3fcac6d5501d0b9d3`; this was recorded as an observability limitation rather than a CI result.  
**Failures/limitations:** FAIL-002 — local Ruff unavailable and current push/check-run status not exposed by the connector. No E001 implementation or D0 data-quality defect found. The full 24.9 MB artifact was not duplicated in Git history; its exact generation command, implementation commit, byte size, digest, and compact machine-readable promoted evidence are committed.  
**Decision blocker:** none  
**Outgoing state:** DISCOVERY-1; SQ-001 D0 complete; OBS-001 through OBS-004 frozen for one-shot untouched H0 replication; H0/A0 untouched; candidate gate still closed.  
**Next session:** D1-01 / SQ-001 — generate H0 only with the unchanged E001 implementation semantics, evaluate only the four frozen replication criteria, update each observation to REPLICATED or REFUTED, do not mine H0, do not generate A0, and do not create a candidate in the same bounded unit.  
**Commit:** substantive checkpoint commits `bb410cafd172263066e7c313407d708cf300b9e4`, `beab213501dab318075199c3fcac6d5501d0b9d3`, `00beaef7c7de36193d3ee096cb7ef2ea46a6d530`, `1063c8eb5a04e400bbd7b2308805fd4b01836577`, `b7fa33f2106d572cb9735c0a7c0a9acb9be0e3d9`, `9a37e89b899a1eef8bab4ee651901b01f782229b`, `b6c39e08cf8de055d7e06973a019b9fcae87e87a`, `80a83f740e747cab0a38e477fa19a3a6ef58f194`, `75df156ca219e7a35b7a0cdafe93a6ba085a66b0`.


### S003

**Date:** 2026-10-06  
**Stage:** replication  
**Bounded objective:** D1-01 / SQ-001 — verify the frozen E001 executable semantics, validate before holdout generation, execute untouched H0 only, evaluate only the four frozen replication criteria for OBS-001 through OBS-004, and leave A0/candidate/mechanism/prior-art work untouched.  
**Incoming state:** DISCOVERY-1 at main head `d087f332239817b128d810c08a75057ffcc1572b`; D0 complete; OBS-001 through OBS-004 frozen at status OBSERVED with exact H0 criteria; H0/A0 recorded untouched; no candidates.  
**Work performed:** Read all required authority, ledgers, frozen E001 specification, D0 execution record, compact D0 evidence, and live prompt before changing anything. Verified the current E001 executable blob `01edecf0a1e992459807264fbf92bb816d242c7f` is byte-identical to the file at implementation commit `beab213501dab318075199c3fcac6d5501d0b9d3`. Direct clone again failed because the detached runner could not resolve github.com, so the exact committed source/test set was reconstructed through the GitHub connector. An initial local pytest attempt omitted `pyproject.toml` from that reconstruction and failed import collection; after restoring the exact committed pyproject blob, pytest passed before any H0 generation. Generated H0 twice solely for byte-determinism verification, then inspected only the four frozen criteria. Recorded the bounded H0 execution report and compact evidence; updated observation statuses, search queue, programme status, the known failure recurrence, and the live next-session prompt.  
**Result:** H0 replication complete. The repeated 25,557,012-byte artifact is byte-identical with SHA-256 `80c8c49f1845e941764b31471404a8e674fa794394687cb6502dbd2eca980254`. OBS-001 REPLICATED: third-difference 0 is the unique mode, 3,764 versus runner-up value 12 at 3,408. OBS-002 REPLICATED: `[6, 6]` is the unique width-2 motif mode, 1,409 versus runner-up `[6, 4]` at 1,335. OBS-003 REPLICATED: complete directed reduced-residue support 4/4, 16/16, 16/16, 64/64, 256/256 for moduli 6, 10, 12, 30, 60. OBS-004 REFUTED: exactly one anchored width-100 H0 block is empty, `[1_671_800, 1_671_900)`. No H0 mining, candidate creation, mechanism work, prior-art search, or A0 execution occurred.  
**Observations/candidates affected:** OBS-001, OBS-002, OBS-003 -> REPLICATED; OBS-004 -> REFUTED; active replicated observations 3; active candidates 0.  
**Validation:** Frozen executable source equality confirmed by matching Git blob SHA `01edecf0a1e992459807264fbf92bb816d242c7f`; reconstructed core/pattern/test blobs also matched their committed SHAs. `PYTHONPATH=src pytest -q` passed 14/14 after exact pyproject restoration; `python -m compileall -q src experiments tests` succeeded. Two identical H0 commands were byte-identical. Local Ruff remained unavailable with exit 127. Connector combined-status and PR-triggered workflow-run collections remained empty for both `beab213501dab318075199c3fcac6d5501d0b9d3` and `d087f332239817b128d810c08a75057ffcc1572b`; no CI pass/fail inference was made.  
**Failures/limitations:** Reused FAIL-002 for detached-runner Ruff/network and CI-observability limitations. The initial reconstructed pytest collection failure was caused by omission of the repository pyproject in the local reconstruction, was corrected before H0 generation, and was not an E001 semantic defect. No implementation-semantic or H0 data-quality defect was found.  
**Decision blocker:** none  
**Outgoing state:** DISCOVERY-1; H0 replication complete; OBS-001 through OBS-003 replicated and eligible for a separate candidate-synthesis triage; OBS-004 permanently refuted under its frozen criterion; candidate gate eligible/open but no candidate created; A0 remains untouched.  
**Next session:** D1-02 / SQ-001 — candidate-synthesis triage over OBS-001 through OBS-003 only, using committed D0+H0 evidence without new mining or tuning; create only exact justified CAND records, keep novelty UNAUDITED, and do not run prior-art, mechanism work, or A0 in the same bounded unit.  
**Commit:** substantive checkpoint commits `0675fbae1fc59cf47f7ce6e94bfbd6e14f12eea8`, `cfb585d8ecbb881212d50ae1c927e03b68a759ed`, `2bb1ef79ab9deed55409fff42dd8815f32330c33`, `679be3774fc6eb80c0e560fccc490f591d08b62f`, `769f139df003693426c25dbb1d76bbb76e3c765f`, `72baff1db3cf06e5871d1ace433788d20413396d`, `2dbdf1e526067b42ccb9fa5e7e77f2629be2bd21`.


### S004

**Date:** 2026-10-06  
**Stage:** discovery  
**Bounded objective:** D1-02 / SQ-001 — triage the three replicated E001 observations for mathematically precise, falsifiable candidate synthesis using only committed D0+H0 evidence, without retuning, new computation, A0 inspection, mechanism work, proof work, or prior-art search.  
**Incoming state:** DISCOVERY-1 at main head `a5ea4c50afd7d94bae76d6d00e029c907aa377fa`; OBS-001 through OBS-003 REPLICATED, OBS-004 REFUTED, candidate gate eligible but no candidates, A0 untouched, live prompt requested candidate-synthesis triage.  
**Work performed:** Read all required authority, ledgers, frozen E001 specification, D0/H0 execution records, compact evidence, and the live prompt before changing anything; additionally checked the committed candidate-promotion protocol. Considered only OBS-001, OBS-002, and OBS-003. Tested whether the exact two-band evidence admitted a non-arbitrary mathematical statement rather than a finite restatement or an unsupported extrapolation. Recorded per-observation triage reasons in the conjecture register and observation ledger, preserved OBS-004 exactly as REFUTED, advanced SQ-002 to the next preflight unit, updated programme status, and replaced the live prompt with a cross-scale persistence preflight. No prime-derived computation was run.  
**Result:** No `CAND-###` was created. OBS-001 and OBS-002 remain replicated range-local modal-rank observations: promoting either now would require an unsupported quantifier over band origin, width, scale, or eventual/asymptotic behaviour, while a D0+H0-only statement would merely restate finite evidence. OBS-003 remains a replicated finite-grid support observation: the five frozen moduli across D0+H0 do not justify an all-moduli and/or infinite-occurrence claim, while a candidate restricted to the observed grid would largely restate finite coverage. OBS-004 remains REFUTED by `[1_671_800, 1_671_900)`.  
**Observations/candidates affected:** OBS-001, OBS-002, OBS-003 retained at REPLICATED with no candidate link; OBS-004 preserved at REFUTED; active candidates remain 0 and no candidate ID was allocated.  
**Validation:** Documentation-only consistency checks passed after checkpoint: no allocated `CAND-###` heading; active candidates still none; all three replicated observations contain explicit no-promotion notes; OBS-004 status and exact H0 counterexample are preserved; A0 remains recorded untouched; `PROGRAM_STATUS.md`, `research/SEARCH_QUEUE.md`, and `NEXT_SESSION_PROMPT.md` agree on D1-03 / SQ-002; the next prompt explicitly forbids E002 execution and A0 use. No code or mathematical computation changed, so pytest/Ruff/experiment reruns were not appropriate validation for this unit.  
**Failures/limitations:** No new execution or repository failure. Candidate synthesis remains evidence-limited: two adjacent low-scale bands are enough for replication but not for a non-arbitrary extrapolation. No novelty conclusion was attempted.  
**Decision blocker:** none  
**Outgoing state:** DISCOVERY-1; D1-02 complete with no candidate created; OBS-001 through OBS-003 remain replicated; OBS-004 remains refuted; A0 untouched; next task is a design-only cross-scale persistence preflight.  
**Next session:** D1-03 / SQ-002 — freeze E002 cross-scale persistence bands and exact criteria for OBS-001 through OBS-003 without executing E002, touching A0, creating a candidate, or performing mechanism/prior-art work.  
**Commit:** substantive checkpoint commit `89cdcfb432ea63a22b148a3596b6a5818b9633bb`.


### S005

**Date:** 2026-10-06  
**Stage:** replication preflight  
**Bounded objective:** D1-03 / SQ-002 — design and freeze a cross-scale persistence experiment for replicated OBS-001 through OBS-003 only, using unchanged E001 feature definitions, fresh disjoint value bands, and exact predeclared persistence criteria, without executing E002 or generating any new prime-derived result.  
**Incoming state:** DISCOVERY-1 at main head `dbfaa4a216621b1db7bc954e80fe5ea628e31691`; OBS-001 through OBS-003 REPLICATED, OBS-004 REFUTED, D1-02 completed with no candidate, A0 untouched, and SQ-002 awaiting preflight.  
**Work performed:** Read all requested project authority, protocols, ledgers, E001 frozen specification, D0/H0 execution records, compact D0/H0 evidence, and the live prompt before changing anything. Preserved the exact E001 definitions for OBS-001, OBS-002, and OBS-003. Froze E002 as a criterion-only test over five width-1,000,000 bands with lower endpoints 2M, 4M, 8M, 16M, and 32M; froze strict unique-mode criteria for OBS-001/002, complete frozen-modulus transition support for OBS-003, all-five-band overall persistence, full-ladder execution with no early stopping or replacement bands, deterministic criterion-only serialization, and an A0 exclusion. Updated the search queue, programme status, observation notes, and live execution prompt. No literature search, mechanism work, proof work, candidate creation, collision audit, code execution, or prime-derived computation occurred.  
**Result:** E002 is FROZEN / NOT YET EXECUTED. Bands are S1=`[2_000_000,3_000_000)`, S2=`[4_000_000,5_000_000)`, S3=`[8_000_000,9_000_000)`, S4=`[16_000_000,17_000_000)`, and S5=`[32_000_000,33_000_000)`. They are mutually disjoint and exclude D0, H0, and reserved A0=`[10_000_000,11_000_000)`. A tie fails the OBS-001/002 strict modal criterion; any missing allowed pair at any modulus in `{6,10,12,30,60}` fails OBS-003; overall E002 persistence requires passing every frozen band.  
**Observations/candidates affected:** OBS-001 through OBS-003 remain REPLICATED with definitions unchanged and now link to the frozen E002 preflight; OBS-004 remains REFUTED and excluded; active candidates remain 0 and no candidate ID was allocated.  
**Validation:** Documentation-only consistency checks passed after checkpoint. E002 is still marked FROZEN / NOT YET EXECUTED; S1-S5 agree across the frozen spec, search queue, programme status, observation notes where enumerated, and next prompt; a direct interval check confirms all five bands are mutually disjoint and disjoint from D0, H0, and A0; the frozen modulus family remains `{6,10,12,30,60}`; OBS-001 through OBS-003 remain REPLICATED; OBS-004 remains REFUTED; the conjecture register still reports no active candidates; and the `research/evidence/` directory contains only the two historical E001 evidence files, confirming no E002 result artifact was introduced. No code changed, so pytest/Ruff/experiment execution was not appropriate for this design-only unit.  
**Failures/limitations:** No new repository or execution failure. E002 deliberately tests value-scale persistence at fixed band width; it does not test arbitrary band widths/origins or establish an eventual/asymptotic statement.  
**Decision blocker:** none  
**Outgoing state:** DISCOVERY-1; D1-03 complete; E002 frozen before execution; no E002 prime-derived results; OBS-001 through OBS-003 remain replicated; OBS-004 remains refuted; no candidate; A0 untouched.  
**Next session:** D1-04 / SQ-002 — implement and execute the frozen E002 criterion-only test across S1 through S5, verify deterministic output, evaluate only the frozen persistence criteria, and keep A0/candidate/mechanism/prior-art work out of scope.  
**Commit:** substantive checkpoint commits `c214784e591e44192ad63f72b9611be3985d58b9`, `2e3b6fac196af821c4042115c6513e3f3961e4b4`, `aa0479da7838e085d196b015e8106806ecb53d59`, `bc8a586e9325f3b701efc42c818caacb2c748085`, `cce31de29eedbe80898665bae9b9f906a9837a82`.

## Entry template

### S###

**Date:**  
**Stage:** discovery / replication / falsification / mechanism / collision-audit / proof / certification  
**Bounded objective:**  
**Incoming state:**  
**Work performed:**  
**Result:**  
**Observations/candidates affected:**  
**Validation:**  
**Failures/limitations:**  
**Decision blocker:** none / exact blocker  
**Outgoing state:**  
**Next session:** exact bounded unit / SUPPRESSED_OWNER_BLOCKER / PROGRAMME_COMPLETE  
**Commit:**
