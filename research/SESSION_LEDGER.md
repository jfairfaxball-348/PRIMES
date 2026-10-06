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
