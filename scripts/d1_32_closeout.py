from __future__ import annotations

import os
import sys
from pathlib import Path


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"missing marker: {label}")
    return text.replace(old, new, 1)


SQ11 = """## SQ-011 — Finite-field polynomial factor-degree shapes

Stage: discovery

Status: **D1-32 PREFLIGHT COMPLETE — E011 FROZEN / NOT EXECUTED; D11/H11/A11 UNTOUCHED; D1-33 DISCOVERY EXECUTION NEXT**

Frozen specification: experiments/E011_FINITE_FIELD_FACTOR_DEGREE_SHAPES.md

E011 freezes one qualitatively distinct primitive family: for each prime anchor p, reduce the single predeclared polynomial F(T)=T^5+T+1 modulo p and retain only its exact irreducible factor-degree partition plus three predeclared coarsenings. Degree 5 is chosen before prime output as the least d>=2 with at least seven integer partitions, using P(2)=2, P(3)=3, P(4)=5, P(5)=7; F_d(T)=T^d+T+1 is the fixed sparse-polynomial rule. No E001-E010 observation value, E005 calibration object/mechanism, hidden historical target, prior-art result, or literature result selected the family.

This primitive is finite-field polynomial arithmetic at the prime anchor, not a prime-gap/difference, occupancy/event, residue-transition/refinement, additive-overlap, neighbouring-factorization, binary-word, modular-order/action-cover, or quadratic-surd recurrence representation.

Fresh metadata-only partition:

- G11-pre=[61_000_000,62_000_000) — frozen non-target / ungenerated;
- D11=[62_000_000,63_000_000) — frozen discovery / untouched;
- G11-mid=[63_000_000,64_000_000) — frozen non-target / ungenerated;
- H11=[64_000_000,65_000_000) — frozen untouched one-shot holdout;
- A11=[124_000_000,125_000_000) — frozen untouched adversarial reserve.

The partition uses only consumed H10's exclusive endpoint 61_000_000, W=1_000_000, one full guard before D11, one full guard before H11, and L_A11=2*L_D11. It consumes no prior reserve and is disjoint from every historical generated/protected/non-target novelty interval and all E005 calibration segments.

Exact finite-field arithmetic computes R_k=T^(p^k) mod F_p and s_k=deg gcd(F_p,R_k-T), k=1,...,5. The frozen divisor recursion derives nonnegative integer counts c_d satisfying all divisor-sum reconstruction identities and sum d*c_d=5. Raw polynomial coefficients modulo p, roots/factors, R_k, gcd polynomials, s_k, and per-anchor c_d vectors are validation/computation objects only.

Exactly four promotable families are frozen: K1 exact factor-degree partition; K2 number of irreducible factors; K3 number of linear factors; K4 largest factor degree. K2-K4 are predeclared coarsenings of K1. No fifth transform, alternate degree, alternate polynomial, coefficient search, or polynomial panel is permitted.

E011 has no composite-ring surrogate and imports no theory-informed distribution baseline. The target-agnostic artifact control is Q=210: for a strict-unique modal target, count reduced residue classes containing both a target prime and a non-target prime for the same family. The mixed-residue floor is 8; residue identities and per-residue counts are not serialized.

Promotion requires N_P>=1000, a strict unique D11 family mode, target count>=32, mixed-residue count>=8, and zero mandatory validation failures. Ties and failed gates have no fallback. Exact support-set duplicate suppression retains the lowest-numbered family K1<K2<K3<K4 when eligible targets select identical D11 prime supports. Hard cap: four observations.

Every promoted D11 target must freeze an unchanged same-family/same-signature H11 criterion before holdout generation. H11 requires N_P>=1000, the identical target as strict unique H11 mode, target count>=32, mixed-residue count>=8, and all validation controls passing. A tie, higher competitor, floor failure, control failure, or validation failure mechanically refutes; no holdout mining, retargeting, threshold/control/polynomial/degree/family change, or fallback is permitted.

The D11 serialization allowlist is minimal: experiment/checkpoint/band/partition/parameters/generation plan; prime count/first/last; seven aggregate validation counts; criterion-only family mode fields; and promotion precursors. Per-prime objects, prime lists, residue identities/counts, polynomial internals, complete frequency tables, non-mode signatures, alternate-polynomial output, timings, and exploratory fields are forbidden. Canonical UTF-8 JSON uses sorted keys, indent=2, one trailing newline, frozen ordering, and must repeat byte-identically for identical complete commands on the same checkpoint.

Future generation is fail-closed. D1-33 may authorize exactly whole-prefix support [0,7938) plus segmented D11. A later H11 phase would authorize exactly [0,8063) plus H11; a later A11 phase exactly [0,11181) plus A11. Wrong support, high whole-prefix generation, partial/expanded/shifted/split targets, E011 guards/H11/A11 outside the current phase, every historical generated/protected/guard interval, all E005 calibration segments, and arbitrary non-target high intervals must fail before prime generation.

D1-32 generated no primes or other E011 prime-derived output, inspected no protected range, allocated no OBS/CAND ID, and performed no candidate synthesis, mechanism/proof/adversarial work, prior-art/collision/literature search, novelty claim, historical-output mining, or calibration transfer. Observation, conjecture, and failure records remain unchanged.

Next bounded action: **D1-33 / SQ-011 E011 D11 discovery execution.** Implement and validate only the frozen E011 evaluator/planner, checkpoint exact implementation/test bytes before generation, authorize only [0,7938) plus segmented D11, execute the identical D11 command twice before allowlisted inspection, mechanically apply K1-K4 promotion/duplicate suppression, freeze exact H11 criteria for any promoted observations, and stop without H11/A11 or downstream work.
"""


E011_STATUS = """## Frozen E011 partition and representation

- G11-pre: [61_000_000,62_000_000) — **FROZEN / NON-TARGET / UNGENERATED**
- D11: [62_000_000,63_000_000) — **FROZEN / UNTOUCHED / NOT EXECUTED**
- G11-mid: [63_000_000,64_000_000) — **FROZEN / NON-TARGET / UNGENERATED**
- H11: [64_000_000,65_000_000) — **FROZEN / UNTOUCHED / ONE-SHOT HOLDOUT**
- A11: [124_000_000,125_000_000) — **FROZEN / UNTOUCHED / UNINSPECTED / NOT EXECUTED**

E011 is frozen in experiments/E011_FINITE_FIELD_FACTOR_DEGREE_SHAPES.md. Its primitive is exact finite-field polynomial factor-degree shape for the single target-agnostically selected polynomial F(T)=T^5+T+1 at each prime anchor. Degree 5 is fixed as the least d>=2 with at least seven integer partitions; the polynomial rule is F_d(T)=T^d+T+1. The exact discriminant 3381=3*7^2*23 and all polynomial-arithmetic identities are validation-only.

The partition is metadata-only: starting at consumed H10's exclusive endpoint 61_000_000, preserve G11-pre, then D11, G11-mid, and H11 as consecutive width-1,000,000 bands; set L_A11=2*L_D11=124_000_000. No existing reserve is consumed. The five bands are disjoint from all historical generated/protected/non-target novelty intervals, A10/A9/H8/A8, and every E005 calibration segment.

Exactly four promotable families are frozen: K1 exact factor-degree partition, K2 factor count, K3 linear-factor count, and K4 largest factor degree. Promotion is mechanical only: N_P>=1000, strict unique mode, target count>=32, at least 8 mixed reduced residue classes under the non-promotable Q=210 artifact control, and zero validation failures. Ties or failed gates have no fallback. Exact support-set duplicate suppression keeps the lowest-numbered family; hard cap is four.

There is no composite-ring surrogate or theory-informed expected-distribution baseline. Per-prime polynomial internals, roots/factors, s_k/c_d vectors, residue identities/counts, complete frequency tables, non-mode signatures, alternate-polynomial results, timings, and exploratory features are excluded from serialization. Canonical JSON semantics and family/signature ordering are frozen for byte-identical repeats.

Every promoted D11 target must freeze an unchanged same-family/same-signature H11 criterion before holdout generation. H11 uses the same population/occurrence/mixed-residue floors and strict-mode/validation gates; ties, higher competitors, floor/control failures, or validation failures mechanically refute. No holdout mining, retargeting, polynomial/degree/family/control/threshold change, or fallback is permitted.

Future generation is fail-closed. D1-33 may authorize only [0,7938) whole-prefix support plus segmented D11. Later H11 and A11 phases would authorize only [0,8063)+H11 and [0,11181)+A11 respectively. Wrong support, high whole-prefix generation, partial/expanded/shifted/split targets, guards, out-of-phase holdout/adversarial targets, every historical generated/protected/guard interval, E005 calibration segments, and arbitrary non-target high intervals fail before prime generation.

D1-32 was design-only: no E011 prime-derived output exists; no protected range was inspected; no OBS/CAND ID was allocated; no synthesis/mechanism/proof/adversarial/prior-art/collision/literature/novelty/calibration-transfer work occurred. Observation, conjecture, and failure ledgers are unchanged.

"""


NEXT_PROMPT = """Read "PROGRAM_STATUS.md", "PROJECT_CHARTER.md", "AGENTS.md", "docs/SESSION_PROTOCOL.md", "docs/DISCOVERY_PROTOCOL.md", "docs/CALIBRATION_PROTOCOL.md", "research/SESSION_LEDGER.md", "research/SEARCH_QUEUE.md", "research/OBSERVATION_LEDGER.md", "research/CONJECTURE_REGISTER.md", "research/FAILURE_LEDGER.md", "experiments/E011_FINITE_FIELD_FACTOR_DEGREE_SHAPES.md", "experiments/E010_QUADRATIC_SURD_CYCLE_SHAPES.md", "experiments/E010_D10_DISCOVERY_2026-10-07.md", "research/evidence/E010_D10_discovery.json", "experiments/E010_H10_REPLICATION_2026-10-07.md", "research/evidence/E010_H10_replication.json", "experiments/E009_UNIT_ACTION_COVER_SHAPES.md", "experiments/E009_D9_DISCOVERY_2026-10-07.md", "experiments/E009_H9_REPLICATION_2026-10-07.md", and the frozen historical novelty-lane records referenced by programme status before changing anything. Read SQ-005 only for its committed closure/quarantine state and generic target-agnostic protocol rules; do not import calibration objects, historical-unblinding mechanisms, hidden historical targets, or source-derived mechanisms.

Continue PRIMES at DISCOVERY-1 in the blind novelty lane.

Your bounded task is D1-33 / SQ-011 E011 D11 discovery execution:

1. Treat "experiments/E011_FINITE_FIELD_FACTOR_DEGREE_SHAPES.md" as frozen. Do not change the degree-selection rule, F(T)=T^5+T+1, finite-field arithmetic, s_k/c_d semantics, K1-K4 grammar/order, Q=210 mixed-residue control, N_min=1000/C_min=32/M_min=8 floors, duplicate suppression, four-observation cap, serialization allowlist, partition, H11 template, or generation rules after any D11 output exists.
2. Treat E010 D10/H10 and OBS-014's REFUTED outcome as immutable historical facts. Preserve A10=[116_000_000,117_000_000), A9=[108_000_000,109_000_000), H8/A8, A11=[124_000_000,125_000_000), H11=[64_000_000,65_000_000), G11-pre/G11-mid, and every historical protected/non-target range.
3. Implement only the frozen E011 evaluator, exact finite-field runtime if needed, fail-closed generation planner, deterministic serializer, and focused tests. Checkpoint exact implementation/test bytes before any prime generator call.
4. Validate all frozen D1-33 obligations before generation: partition/provenance arithmetic; degree/polynomial/discriminant metadata; exact polynomial normalization/add/multiply/divide/monic-gcd/modular-power semantics; derivative/squarefree validation; R_k/s_k for k=1..5; c_d recursion/divisibility/nonnegativity/divisor-sum reconstruction/total degree; K1-K4 semantics/order; strict-mode/tie handling; floors; Q=210 mixed-residue control; duplicate suppression/cap; allowlist; deterministic serialization; and fail-closed plan rejection.
5. Construct the complete generation plan before either prime generator. Authorize exactly whole-prefix support [0,7938) plus segmented D11=[62_000_000,63_000_000). Reject wrong/short/expanded/shifted/additional support, whole-prefix high generation, partial/expanded/shifted/split/duplicated D11, E011 guards/H11/A11, D10/H10/A10, D9/H9/A9, H8/A8, every historical generated/protected/guard interval, all E005 calibration segments, and arbitrary non-target high intervals before generation.
6. Execute the identical complete D11 command twice on the same implementation checkpoint and same output path. Establish byte identity before inspecting any descriptive field. If determinism fails, stop and record the failure; do not inspect or promote from a nondeterministic artifact.
7. After byte identity, inspect only the frozen E011 allowlist. Do not expose or mine per-prime records, prime lists beyond first/last/count, residue identities/counts, R_k/gcd polynomials, s_k/c_d vectors, irreducible factors/roots, complete family frequency tables, non-mode signatures, alternate-polynomial outputs, or any unlisted feature.
8. Apply only the frozen K1-K4 promotion grammar. A family is eligible only for its strict unique D11 mode with N_P>=1000, target count>=32, at least 8 mixed Q=210 residue classes, and zero mandatory validation failures. Ties or failed gates have no fallback. Apply exact support-set duplicate suppression in K1<K2<K3<K4 order and the hard cap of four.
9. For each mechanically promoted record, allocate the next OBS ID(s) in family order and commit the exact unchanged one-shot H11 same-family/same-signature criterion before future H11 generation. If no family is eligible, allocate no OBS ID, record NO ELIGIBLE OBSERVATION, leave H11/A11 untouched, and close SQ-011 without relaxing/replacing the grammar.
10. Generate no H11 or A11 primes. Allocate no CAND ID and perform no candidate synthesis, mechanism/proof work, adversarial execution, prior-art/collision/literature search, novelty claim, historical-output mining, calibration-object transfer, protected-range inspection, post-result feature invention, retargeting, threshold/control/polynomial/degree/family change, or fallback target.
11. Update all applicable authoritative state consistently, leave unrelated observation/conjecture/failure records unchanged, checkpoint D1-33 under "docs/SESSION_PROTOCOL.md", and automatically finish with exactly one runnable next-session prompt for the appropriate separately bounded follow-up (one-shot H11 replication if any observation is promoted; otherwise the next blind novelty preflight), unless a genuine owner decision blocker exists.
"""


def apply_state() -> None:
    p = Path("research/SEARCH_QUEUE.md")
    text = p.read_text()
    idx = text.find("## SQ-011 —")
    if idx < 0:
        raise RuntimeError("SQ-011 marker missing")
    p.write_text(text[:idx] + SQ11 + "\n")

    p = Path("PROGRAM_STATUS.md")
    text = p.read_text()
    text = replace_once(
        text,
        "**DISCOVERY-1 — D1-31 / SQ-010 H10 replication complete; OBS-014 REFUTED; SQ-010 closed; D1-32 / SQ-011 blind novelty preflight next**",
        "**DISCOVERY-1 — D1-32 / SQ-011 blind novelty preflight complete; E011 frozen; D1-33 / SQ-011 D11 discovery execution next**",
        "current stage",
    )
    text = replace_once(
        text,
        "| Pattern discovery | OPEN / SQ-010 CLOSED; SQ-011 PREFLIGHT NEXT | D1-31 consumed H10 under the frozen OBS-014 criterion; E010 closed after refutation and A10 remains untouched |",
        "| Pattern discovery | OPEN / SQ-011 FROZEN; D11 EXECUTION NEXT | D1-32 froze E011 before output; D11/H11/A11 remain untouched and A10/A9 remain protected |",
        "pattern gate",
    )
    text = replace_once(
        text,
        "- H10: [60_000_000,61_000_000) — **FROZEN / UNTOUCHED / NOT EXECUTED**",
        "- H10: [60_000_000,61_000_000) — **EXECUTED ONE-SHOT / REPLICATION-CONSUMED**",
        "H10 state",
    )
    old_active = """## Active task

**D1-32 / SQ-011:** design-only blind novelty representation-family preflight. Select and freeze exactly one qualitatively distinct family using only novelty-lane authority and generic target-agnostic protocol rules; choose fresh metadata-only ranges by deterministic provenance/arithmetic rules; freeze exact primitives/transforms, controls, descriptive allowlist, promotion/holdout criteria, deterministic serialization, and fail-closed future-generation rules. Generate no prime-derived output and preserve A10/A9 plus every historical reserve/holdout/guard.
"""
    new_active = """## Active task

**D1-33 / SQ-011:** execute only the frozen E011 D11 discovery unit. Implement and validate the exact finite-field polynomial evaluator/guard, checkpoint implementation/test bytes before generation, authorize exactly low support [0,7938) plus segmented D11=[62_000_000,63_000_000), establish byte determinism before descriptive inspection, apply only the frozen K1-K4 promotion grammar, and freeze unchanged H11 criteria for any promoted observations. Generate no H11/A11 output and preserve every historical protected/non-target interval.
"""
    text = replace_once(text, old_active, new_active, "active task")
    if "## Frozen E011 partition and representation" not in text:
        marker = "## Frozen E005 calibration benchmark"
        if marker not in text:
            raise RuntimeError("E005 insertion marker missing")
        text = text.replace(marker, E011_STATUS + marker, 1)
    ni = text.find("## Next stage\n")
    if ni < 0:
        raise RuntimeError("Next stage marker missing")
    next_stage = """## Next stage

DISCOVERY-1 remains in the blind novelty lane. SQ-010 stays closed historical novelty work: D10 and H10 are consumed, OBS-014 remains REFUTED, and A10=[116_000_000,117_000_000) remains frozen untouched/uninspected/unexecuted. SQ-009 remains closed with A9=[108_000_000,109_000_000) untouched.

D1-32 / SQ-011 is complete. E011 is frozen before output as the finite-field polynomial factor-degree family with D11=[62_000_000,63_000_000), H11=[64_000_000,65_000_000), A11=[124_000_000,125_000_000), and permanent guards G11-pre/G11-mid. No E011 prime-derived output exists, no OBS/CAND ID was allocated, and observation/conjecture/failure records are unchanged.

The next bounded unit is D1-33 / SQ-011 D11 discovery execution. It may implement/validate only the frozen E011 evaluator and fail-closed planner, checkpoint exact implementation/test bytes before generation, generate exactly low support [0,7938) plus segmented D11, run the identical D11 command twice before allowlisted inspection, mechanically apply K1-K4 promotion/duplicate suppression, and freeze exact H11 criteria for any promoted observations. It must not generate H11/A11 or perform candidate synthesis, mechanism/proof/adversarial work, prior-art/collision/literature/novelty work, historical-output mining, calibration transfer, retargeting, or protected-range inspection.
"""
    p.write_text(text[:ni] + next_stage)

    Path("NEXT_SESSION_PROMPT.md").write_text(NEXT_PROMPT)


def append_session(state_commit: str, install_commit: str) -> None:
    p = Path("research/SESSION_LEDGER.md")
    text = p.read_text()
    if "### S034" in text:
        raise RuntimeError("S034 already exists")
    marker = "## Entry template"
    if marker not in text:
        raise RuntimeError("session template marker missing")
    entry = f"""### S034

**Date:** 2026-10-07
**Stage:** discovery
**Bounded objective:** D1-32 / SQ-011 — design-only blind novelty representation-family preflight.
**Incoming state:** DISCOVERY-1 after D1-31; SQ-010 closed; D10/H10 consumed; OBS-014 REFUTED; A10/A9 untouched; H8/A8 and every historical reserve/holdout/guard preserved; active candidates 0; SQ-005 closed/quarantined.
**Work performed:** Re-read the requested authority, protocols, ledgers, frozen E010 specification/D10/H10 evidence and implementation/tests, E009 records, and frozen historical novelty-family specifications. Used SQ-005 only for generic target-agnostic freeze/switch safeguards. Selected exactly one distinct family using arithmetic metadata only: exact finite-field factor-degree shapes of F(T)=T^5+T+1 over prime anchors, with degree 5 fixed as the least d>=2 having at least seven integer partitions. Froze exact finite-field arithmetic, s_k/c_d semantics, K1-K4 signatures, validation/triviality exclusions, Q=210 mixed-residue artifact control, N/C/M floors, strict-mode/tie rules, duplicate suppression, four-observation cap, minimal serialization, unchanged H11 criteria, and fail-closed generation. Froze G11-pre=[61M,62M), D11=[62M,63M), G11-mid=[63M,64M), H11=[64M,65M), A11=[124M,125M) plus exact low-support endpoints [0,7938), [0,8063), [0,11181). No prime generator or E011 evaluator was executed.
**Result:** E011 is FROZEN / NOT EXECUTED in experiments/E011_FINITE_FIELD_FACTOR_DEGREE_SHAPES.md. D11/H11/A11 remain untouched and guards ungenerated. No OBS/CAND ID was allocated. Observation/conjecture/failure ledgers remain unchanged.
**Observations/candidates affected:** none. OBS ledger blob remains 27dcf97bfc0e65c20806832d95a160c5f6ee0c75; conjecture register blob remains 05af4a9442b123f53d7c15db0b6661cb3d622a80; failure ledger blob remains 6bb7c51a27b07344a6b1591707c1c41e6b45a053.
**Validation:** Exact metadata checks confirm P(2)=2, P(3)=3, P(4)=5, P(5)=7; disc(T^5+T+1)=3381=3*7^2*23; floor(sqrt(62,999,999))=7,937, floor(sqrt(64,999,999))=8,062, floor(sqrt(124,999,999))=11,180; and all E011 bands are disjoint from committed historical generated/protected/non-target intervals and E005 calibration segments. E011 specification commit: 7f05f1958bcf23be4cb8bb2c19f997882fe9e46e. Authoritative state commit: {state_commit}.
**Failures/limitations:** No new FAILURE_LEDGER ID. The GitHub connector's direct existing-file update/delete/blob/tree actions returned internal errors. An initial one-shot workflow definition also failed at workflow parsing before jobs ran. A simplified self-removing workflow then applied only the authorized text-state changes; no scientific computation, prime generation, protected-range access, or evidence interpretation was delegated to it. Helper installer commit: {install_commit}.
**Decision blocker:** none
**Outgoing state:** DISCOVERY-1; D1-32 complete; E011 frozen/not executed; D11/H11/A11 untouched; G11-pre/G11-mid ungenerated; A10/A9 and every historical protected range preserved; active candidates 0.
**Next session:** D1-33 / SQ-011 — implement/validate frozen E011, checkpoint bytes before generation, authorize exactly [0,7938) plus segmented D11, execute D11 twice before allowlisted inspection, mechanically apply K1-K4 promotion/duplicate suppression, freeze exact H11 criteria for any promoted observations, and stop without H11/A11 or downstream work.
**Commit:** E011 freeze 7f05f1958bcf23be4cb8bb2c19f997882fe9e46e; authoritative state {state_commit}; session checkpoint is this entry's containing commit.

"""
    p.write_text(text.replace(marker, entry + marker, 1))


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("usage: d1_32_closeout.py apply | session STATE INSTALL")
    if sys.argv[1] == "apply":
        apply_state()
        return
    if sys.argv[1] == "session":
        if len(sys.argv) != 4:
            raise SystemExit("session requires STATE_COMMIT INSTALL_COMMIT")
        append_session(sys.argv[2], sys.argv[3])
        return
    raise SystemExit(f"unknown command {sys.argv[1]}")


if __name__ == "__main__":
    main()
