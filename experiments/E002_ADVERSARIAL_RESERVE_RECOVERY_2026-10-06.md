# E002 Adversarial Reserve Recovery — 2026-10-06

**Stage:** replication / protocol recovery  
**Related task:** D1-05 / SQ-002  
**Status:** FROZEN / DESIGN-ONLY / NOT EXECUTED  
**Parent incident:** FAIL-003

This record repairs the adversarial-reserve protocol after FAIL-003 without rewriting the frozen E001 or E002 specifications and without generating any new prime-derived result.

## Frozen historical facts

The following remain historical facts and are not retuned here:

- E001 D0 = `[0, 1_000_000)` and H0 = `[1_000_000, 2_000_000)`;
- OBS-001, OBS-002, and OBS-003 replicated on H0; OBS-004 was refuted;
- D1-02 created no candidate;
- E002 S1-S5 and all E002 criteria remain exactly as frozen;
- valid E002 outcome: OBS-001 NOT PERSISTENT, OBS-002 PERSISTENT, OBS-003 PERSISTENT;
- candidate count remains zero.

## A0 contamination history

Historical E001 reserve A0 is `[10_000_000, 11_000_000)`.

A0 was not generated during E001 D0 discovery, E001 H0 replication, D1-02 synthesis triage, or D1-03 E002 preflight. During D1-04, however, the discarded first E002 implementation called `sieve(32_999_999)` before filtering the declared S-bands. That whole-prefix generation path internally generated primes lying in A0.

No A0 prime values, representations, or A0-derived criterion outputs were serialized or inspected. A0 is therefore **contaminated by generation but uninspected**. Under the project's literal generation rule it is permanently retired from use as an untouched adversarial reserve.

## Deterministic replacement rule

Preserve the established adversarial-band width:

`W = 1_000_000`.

Let `G_max` be the greatest integer value that committed PRIMES generation metadata records as having been passed through a prime-generation path before this recovery, including discarded protocol-invalid runs.

FAIL-003 fixes:

`G_max = 32_999_999`.

Choose the replacement lower endpoint by:

`L = W * ceil((G_max + 1) / W)`.

Then freeze exactly one replacement reserve:

`A1 = [L, L + W)`.

Substitution gives:

- `L = 33_000_000`;
- **A1 = `[33_000_000, 34_000_000)`**.

This rule is deterministic and depends only on committed generation provenance and the pre-existing width convention. It does not depend on any observed prime behaviour, motif count, finite-difference count, residue-transition result, E002 pass/fail value, or other prime-derived criterion.

## Metadata-only disjointness check

Previously generated or explicitly evaluated numerical regions recorded in committed session/experiment metadata are:

- E000 limits 10,000 and 100,000, both contained in `[0,100_000)`;
- E001 D0 = `[0,1_000_000)`;
- E001 H0 = `[1_000_000,2_000_000)`;
- valid E002 S1 = `[2_000_000,3_000_000)`;
- valid E002 S2 = `[4_000_000,5_000_000)`;
- valid E002 S3 = `[8_000_000,9_000_000)`;
- historical A0 = `[10_000_000,11_000_000)`, internally generated only by the discarded prefix path and never inspected;
- valid E002 S4 = `[16_000_000,17_000_000)`;
- valid E002 S5 = `[32_000_000,33_000_000)`;
- the discarded FAIL-003 prefix generator covered prime generation through integer value 32,999,999, i.e. below the half-open boundary 33,000,000.

Therefore A1 starts exactly at the first million boundary after the maximum recorded generated value. It is disjoint from D0, H0, S1-S5, A0, the smaller E000 ranges, and the discarded prefix-generation coverage.

## Untouched status

At this freeze:

- A1 has **not been generated**;
- A1 has **not been inspected**;
- A1 has **not been executed against any criterion**;
- no A1 prime values or summaries exist in committed evidence;
- the committed `research/evidence/` inventory contains only the historical E001 D0, E001 H0, and valid E002 S1-S5 artifacts.

A1 is therefore **FROZEN / UNTOUCHED / UNINSPECTED / NOT EXECUTED** and is the sole replacement adversarial reserve.

## Execution guard

Any future A1 execution must inspect its generation path before producing prime-derived output and must use isolated/segmented generation or another exact method that cannot traverse an excluded reserve by construction. A1 must not be generated during candidate synthesis, mechanism work, prior-art audit, or any unrelated experiment.

## Stop rule

D1-05 ends with this design-only recovery record and authoritative state updates. No A0/A1/E002 execution, new prime-derived computation, candidate creation, mechanism/proof work, prior-art audit, or representation mining belongs to this unit.
