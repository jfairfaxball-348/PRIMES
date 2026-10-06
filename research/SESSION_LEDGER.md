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
