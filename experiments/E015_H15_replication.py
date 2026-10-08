"""Single-shot OBS-021 H15 target-only replication; frozen E015 primitive unchanged.

No prime generation on import; H15 is the sole authorized phase. No target search.
"""
import argparse
import importlib.util
import json
from collections import Counter
from math import gcd
from pathlib import Path

ORIGINAL_PATH = Path(__file__).with_name("E015_square_shell_euclidean_remainder_quartile_shapes.py")
_spec = importlib.util.spec_from_file_location("frozen_e015_d15", ORIGINAL_PATH)
e = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(e)

PHASE = "H15"
TARGET = (9, 0, 0, 0)
LOW, HIGH = 83_000_000, 84_000_000
TARGET_KEYS = {"family", "signature", "prime_count", "highest_competing_prime_count",
               "composite_count", "strict_unique_prime_mode", "population_floor_passed",
               "class_floor_passed", "occurrence_floor_passed", "mixed_class_count",
               "mixed_class_floor_passed", "aggregate_enrichment_numerator",
               "aggregate_enrichment_positive", "criterion_passed"}
TOP_KEYS = {"experiment", "implementation_commit", "band", "partition", "parameters",
            "generation_plan", "anchor_summary", "validation", "target"}


def plan_checked(phase, plan):
    if phase != PHASE:
        raise ValueError("H15 phase only")
    if e.audit_partition() != 355 or len(e.historical_intervals()) != 69:
        raise ValueError("historical exclusion audit")
    e.validate_plan(phase, plan, authorized=PHASE)
    if plan != [
        {"purpose": "base_sieve_support", "start": 0, "stop": 9166, "strategy": "whole_prefix"},
        {"purpose": "segmented_target", "start": LOW, "stop": HIGH, "strategy": "segmented"},
    ]:
        raise ValueError("nonfrozen ordered H15 plan")
    return True


def guarded_primes(phase, plan):
    plan_checked(phase, plan)  # Entire exact plan before first generator call.
    base = e.generator_entry(phase, plan, 0, e._generate, authorized=PHASE)
    plan_checked(phase, plan)  # Recheck at high-segment boundary.
    return e.generator_entry(phase, plan, 1,
                             lambda call: e._generate(call, base), authorized=PHASE)


def target_metrics(p_counts, c_counts, np_by, nc_by, p_by, c_by):
    domain = e.domains()[2]
    if len(domain) != 220 or TARGET not in domain or len(p_by) != 8 or len(c_by) != 8:
        raise ValueError("R3 domain/classes")
    if any(k not in domain for k in p_counts | c_counts):
        raise ValueError("noncanonical R3")
    np, nc = sum(np_by), sum(nc_by)
    if sum(p_counts.values()) != np or sum(c_counts.values()) != nc:
        raise ValueError("frequency conservation")
    if any(sum(p_by[i].values()) != np_by[i] or sum(c_by[i].values()) != nc_by[i]
           for i in range(8)):
        raise ValueError("R30 conservation")
    if any(sum(p_by[i].get(sig, 0) for i in range(8)) != p_counts.get(sig, 0) or
           sum(c_by[i].get(sig, 0) for i in range(8)) != c_counts.get(sig, 0)
           for sig in domain):
        raise ValueError("stratified frequency conservation")
    npt, nct = p_counts.get(TARGET, 0), c_counts.get(TARGET, 0)
    rival = max(p_counts.get(sig, 0) for sig in domain if sig != TARGET)
    unique = npt > rival  # All 219 other R3 compositions, even zero-frequency.
    mixed = e.mixed_classes(p_by, c_by, np_by, nc_by, TARGET)
    enrich = e.exact_enrichment(np, nc, npt, nct)
    pop_ok = np >= 1000 and nc >= 1000
    cls_ok = all(p >= 100 and c >= 100 for p, c in zip(np_by, nc_by))
    occurrence_ok = npt >= 32
    mix_ok = mixed >= 6
    enrich_ok = enrich > 0
    passed = all((unique, pop_ok, cls_ok, occurrence_ok, mix_ok, enrich_ok))
    return dict(family="R3", signature=list(TARGET), prime_count=npt,
                highest_competing_prime_count=rival, composite_count=nct,
                strict_unique_prime_mode=unique, population_floor_passed=pop_ok,
                class_floor_passed=cls_ok, occurrence_floor_passed=occurrence_ok,
                mixed_class_count=mixed, mixed_class_floor_passed=mix_ok,
                aggregate_enrichment_numerator=enrich,
                aggregate_enrichment_positive=enrich_ok, criterion_passed=passed)


def evaluate(implementation_commit, prime_set, plan):
    plan_checked(PHASE, plan)
    if any(type(p) is not int or p < LOW or p >= HIGH or gcd(p, 30) != 1 for p in prime_set):
        raise ValueError("unexpected high prime support")
    p_counts, c_counts = Counter(), Counter()
    p_by, c_by = [Counter() for _ in range(8)], [Counter() for _ in range(8)]
    np_by, nc_by = [0] * 8, [0] * 8
    wheel = excluded = 0
    class_index = {residue: i for i, residue in enumerate(e.R30)}
    domain = set(e.domains()[2])
    for x in range(LOW, HIGH):
        i = class_index.get(x % 30)
        if i is None:
            continue
        wheel += 1
        word = e.shape(x)  # Unmodified frozen nine-remainder D15 primitive.
        if word is None:
            excluded += 1
            continue
        r1, r2, r3 = word
        if r3 not in domain or r1 != max(r3) or r2 != tuple(sorted(r3, reverse=True)):
            raise ValueError("R1/R2 forced coarsenings")
        if x in prime_set:
            np_by[i] += 1
            p_counts[r3] += 1
            p_by[i][r3] += 1
        else:
            nc_by[i] += 1
            c_counts[r3] += 1
            c_by[i][r3] += 1
    np, nc = sum(np_by), sum(nc_by)
    if np + nc != wheel - excluded:
        raise ValueError("anchor conservation")
    target = target_metrics(p_counts, c_counts, np_by, nc_by, p_by, c_by)
    result = dict(experiment="E015", implementation_commit=implementation_commit,
                  band=dict(name=PHASE, range=[LOW, HIGH], interval_semantics="half-open"),
                  partition=[dict(name=n, range=[lo, hi], role=role) for n, lo, hi, role in e.ROLES],
                  parameters=dict(width=1_000_000, wheel=30, residues_R30=list(e.R30),
                                  denominator_offsets=list(e.OFFSETS),
                                  quartile_edges_num=[0, 1, 2, 3, 4], quartile_denominator=4,
                                  zero_remainder_excluded=True, population_floor=1000,
                                  class_floor=100, occurrence_floor=32, mixed_class_floor=6),
                  generation_plan=plan,
                  anchor_summary=dict(wheel_anchor_count=wheel, conditioned_anchor_count=wheel - excluded,
                                      excluded_zero_remainder_count=excluded, prime_count=np,
                                      composite_count=nc, prime_counts_by_R30=np_by,
                                      composite_counts_by_R30=nc_by),
                  validation=dict.fromkeys(e.VALIDATION_KEYS, 0), target=target)
    serialize(result)
    return result


def validate_schema(payload):
    def keys(v, allowed):
        if type(v) is not dict or set(v) != set(allowed):
            raise ValueError("narrow schema allowlist")
    keys(payload, TOP_KEYS)
    commit = payload["implementation_commit"]
    if payload["experiment"] != "E015" or type(commit) is not str or len(commit) != 40 or any(c not in "0123456789abcdef" for c in commit):
        raise ValueError("implementation identity")
    keys(payload["band"], ("name", "range", "interval_semantics"))
    if payload["band"] != dict(name=PHASE, range=[LOW, HIGH], interval_semantics="half-open"):
        raise ValueError("band mismatch")
    if payload["partition"] != [dict(name=n, range=[lo, hi], role=role) for n, lo, hi, role in e.ROLES]:
        raise ValueError("partition mismatch")
    keys(payload["parameters"], ("width", "wheel", "residues_R30", "denominator_offsets",
                                 "quartile_edges_num", "quartile_denominator", "zero_remainder_excluded",
                                 "population_floor", "class_floor", "occurrence_floor", "mixed_class_floor"))
    p = payload["parameters"]
    if p != dict(width=1_000_000, wheel=30, residues_R30=list(e.R30), denominator_offsets=list(e.OFFSETS),
                 quartile_edges_num=[0, 1, 2, 3, 4], quartile_denominator=4, zero_remainder_excluded=True,
                 population_floor=1000, class_floor=100, occurrence_floor=32, mixed_class_floor=6):
        raise ValueError("parameters mismatch")
    plan_checked(PHASE, payload["generation_plan"])
    a = payload["anchor_summary"]
    keys(a, ("wheel_anchor_count", "conditioned_anchor_count", "excluded_zero_remainder_count",
             "prime_count", "composite_count", "prime_counts_by_R30", "composite_counts_by_R30"))
    for k in ("wheel_anchor_count", "conditioned_anchor_count", "excluded_zero_remainder_count", "prime_count", "composite_count"):
        if type(a[k]) is not int or a[k] < 0:
            raise ValueError("invalid population count")
    for k in ("prime_counts_by_R30", "composite_counts_by_R30"):
        if type(a[k]) is not list or len(a[k]) != 8 or any(type(x) is not int or x < 0 for x in a[k]):
            raise ValueError("invalid class counts")
    if a["prime_count"] + a["composite_count"] != a["conditioned_anchor_count"] or a["conditioned_anchor_count"] + a["excluded_zero_remainder_count"] != a["wheel_anchor_count"] or sum(a["prime_counts_by_R30"]) != a["prime_count"] or sum(a["composite_counts_by_R30"]) != a["composite_count"]:
        raise ValueError("anchor population conservation")
    keys(payload["validation"], e.VALIDATION_KEYS)
    if any(type(x) is not int or x != 0 for x in payload["validation"].values()):
        raise ValueError("mandatory nonzero validation")
    t = payload["target"]
    keys(t, TARGET_KEYS)
    if t["family"] != "R3" or t["signature"] != list(TARGET):
        raise ValueError("retarget denied")
    for k in ("prime_count", "highest_competing_prime_count", "composite_count", "mixed_class_count", "aggregate_enrichment_numerator"):
        if type(t[k]) is not int:
            raise ValueError("target count must be exact integer")
    for k in ("strict_unique_prime_mode", "population_floor_passed", "class_floor_passed", "occurrence_floor_passed", "mixed_class_floor_passed", "aggregate_enrichment_positive", "criterion_passed"):
        if type(t[k]) is not bool:
            raise ValueError("invalid boolean")
    if not (0 <= t["prime_count"] <= a["prime_count"] and 0 <= t["composite_count"] <= a["composite_count"] and 0 <= t["highest_competing_prime_count"] <= a["prime_count"] and 0 <= t["mixed_class_count"] <= 8):
        raise ValueError("target range")
    gates = (t["prime_count"] > t["highest_competing_prime_count"],
             a["prime_count"] >= 1000 and a["composite_count"] >= 1000,
             all(p >= 100 and c >= 100 for p, c in zip(a["prime_counts_by_R30"], a["composite_counts_by_R30"])),
             t["prime_count"] >= 32, t["mixed_class_count"] >= 6,
             t["aggregate_enrichment_numerator"] > 0)
    flags = ("strict_unique_prime_mode", "population_floor_passed", "class_floor_passed",
             "occurrence_floor_passed", "mixed_class_floor_passed", "aggregate_enrichment_positive")
    if any(t[k] != v for k, v in zip(flags, gates)) or t["aggregate_enrichment_numerator"] != e.exact_enrichment(a["prime_count"], a["composite_count"], t["prime_count"], t["composite_count"]) or t["criterion_passed"] != all(gates):
        raise ValueError("frozen criterion mismatch")
    return True


def serialize(payload):
    validate_schema(payload)
    return (json.dumps(payload, sort_keys=True, indent=2, ensure_ascii=True) + "\n").encode("utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", required=True, choices=(PHASE,))
    parser.add_argument("--implementation-commit", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    if args.phase != PHASE or len(args.implementation_commit) != 40 or any(c not in "0123456789abcdef" for c in args.implementation_commit):
        raise ValueError("nonfrozen execution identity")
    plan = e.expected_plan(PHASE)
    plan_checked(args.phase, plan)  # Fail closed BEFORE prime/primality generation.
    high_primes = guarded_primes(args.phase, plan)
    payload = evaluate(args.implementation_commit, high_primes, plan)
    Path(args.output).write_bytes(serialize(payload))


if __name__ == "__main__":
    main()
