#!/usr/bin/env python3
"""E014 H14 one-shot target-specific OBS-020 I2=1 replication, never discovery."""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from math import gcd
from pathlib import Path

import E014_primitive_three_cube_incidence_shapes as frozen

R90 = frozen.R90
Q, CAP = frozen.Q, frozen.CAP
TARGET = 1
H14 = (79_000_000, 80_000_000)
VALIDATION_KEYS = frozen.VALIDATION_KEYS
TARGET_KEYS = {
    "observation", "family", "signature", "prime_target_count", "highest_competing_prime_count",
    "composite_target_count", "mixed_class_count", "positive_class_count",
    "aggregate_enrichment_numerator", "population_floor_passed", "class_floor_passed",
    "strict_unique_prime_mode", "occurrence_floor_passed", "mixed_class_floor_passed",
    "positive_class_floor_passed", "aggregate_enrichment_positive", "replicated",
}
SCHEMA = {
    "": {"experiment", "implementation_commit", "band", "partition", "parameters",
         "generation_plan", "anchor_summary", "validation", "target"},
    "band": frozen.SCHEMA["band"],
    "partition": frozen.SCHEMA["partition"],
    "parameters": frozen.SCHEMA["parameters"],
    "generation_plan": frozen.SCHEMA["generation_plan"],
    "anchor_summary": frozen.SCHEMA["anchor_summary"],
    "validation": set(VALIDATION_KEYS),
    "target": TARGET_KEYS,
}


def plan_h14():
    return [
        {"purpose": "base_sieve_support", "start": 0, "stop": 8945,
         "strategy": "whole_prefix"},
        {"purpose": "segmented_target", "start": 79_000_000, "stop": 80_000_000,
         "strategy": "segmented"},
    ]


def authorize(plan, phase):
    if frozen.metadata_check() != 330:
        raise ValueError("historical interval exclusions failed")
    if phase != "H14" or type(plan) is not list or len(plan) != 2:
        raise ValueError("only one frozen H14 two-call plan is authorized")
    if any(type(p) is not dict or set(p) != SCHEMA["generation_plan"] for p in plan):
        raise ValueError("malformed generator-plan fields")
    if any(type(p[k]) is not int for p in plan for k in ("start", "stop")):
        raise ValueError("generator-plan integer types required")
    if plan != plan_h14():
        raise ValueError("H14 requires exact positive allowlist, no other prime calls")


def generate(plan, phase, low_generator=frozen.low_sieve, high_generator=frozen.target_sieve):
    authorize(plan, phase)  # Entire ordered call list before either generator.
    authorize(plan, phase)  # Independent generator-boundary recheck.
    base = low_generator(plan[0]["stop"])
    authorize(plan, phase)  # Recheck before directly segmented high call.
    return high_generator(plan[1]["start"], plan[1]["stop"], base)


def enumerate_h14():
    """Identical D14 positive/sorted/primitive cubic loop; H14 sum-only bounds."""
    start, stop = H14
    result = defaultdict(list)
    ccap = frozen.icbrt(stop - 3)
    for c in range(1, ccap + 1):
        c3 = c**3
        for b in range(1, c + 1):
            bc = b**3 + c3
            if bc + 1 >= stop:
                break
            for a in range(1, b + 1):
                x = a**3 + bc
                if x >= stop:
                    break
                if x >= start and gcd(x, Q) == 1 and gcd(gcd(a, b), c) == 1:
                    result[x].append((a, b, c))
    return result


def frozen_gates(pfreq, cfreq, pby, cby, ppop, cpop, validation):
    """Only precommitted OBS-020 t=1; competitors counted, never serialized."""
    npop, ncomp = sum(ppop.values()), sum(cpop.values())
    if (set(pfreq) - {1, 2, 3, 4} or set(cfreq) - {1, 2, 3, 4}
            or sum(pfreq.values()) != npop or sum(cfreq.values()) != ncomp
            or any(sum(pby[r].values()) != ppop[r] or sum(cby[r].values()) != cpop[r]
                   for r in R90)):
        raise ValueError("invalid signature/population conservation")
    if any(v != 0 for v in validation.values()):
        raise ValueError("nonzero validation count")
    count = pfreq[TARGET]
    rival = max(pfreq[t] for t in (2, 3, 4))
    mixed = sum(0 < pby[r][TARGET] < ppop[r] and 0 < cby[r][TARGET] < cpop[r]
                for r in R90)
    positive = sum(pby[r][TARGET] * cpop[r] - cby[r][TARGET] * ppop[r] > 0
                   for r in R90)
    enrichment = count * ncomp - cfreq[TARGET] * npop
    checks = {
        "population_floor_passed": npop >= 1000 and ncomp >= 1000,
        "class_floor_passed": all(ppop[r] >= 10 and cpop[r] >= 10 for r in R90),
        "strict_unique_prime_mode": count > rival,
        "occurrence_floor_passed": count >= 32,
        "mixed_class_floor_passed": mixed >= 12,
        "positive_class_floor_passed": positive >= 10,
        "aggregate_enrichment_positive": enrichment > 0,
    }
    return {
        "observation": "OBS-020", "family": "I2", "signature": TARGET,
        "prime_target_count": count, "highest_competing_prime_count": rival,
        "composite_target_count": cfreq[TARGET], "mixed_class_count": mixed,
        "positive_class_count": positive,
        "aggregate_enrichment_numerator": enrichment,
        **checks, "replicated": all(checks.values()),
    }


def evaluate(prime_labels, implementation_commit):
    start, stop = H14
    if any(type(p) is not int or not start <= p < stop for p in prime_labels):
        raise ValueError("prime labels extend beyond H14")
    reps = enumerate_h14()
    ppop, cpop, pfreq, cfreq = Counter(), Counter(), Counter(), Counter()
    pby = {r: Counter() for r in R90}
    cby = {r: Counter() for r in R90}
    for x in sorted(reps):
        triples = reps[x]
        if not (start <= x < stop and gcd(x, Q) == 1):
            raise ValueError("anchor domain failure")
        if x % 9 in (4, 5) or x % 90 not in R90:
            raise ValueError("modulo9/class failure")
        if any(not frozen.primitive(t) for t in triples):
            raise ValueError("primitive normalization failure")
        if any(sum(v**3 for v in t) != x or t[2] > frozen.icbrt(stop - 3)
               for t in triples):
            raise ValueError("cubic sum/bound failure")
        signatures = frozen.incidence_shapes(triples)
        if signatures is None or not (1 <= signatures[1] <= signatures[0] <= CAP):
            raise ValueError("incidence/signature failure")
        i2 = signatures[1]
        r = x % 90
        if x in prime_labels:
            ppop[r] += 1
            pfreq[i2] += 1
            pby[r][i2] += 1
        else:
            cpop[r] += 1
            cfreq[i2] += 1
            cby[r][i2] += 1
    wheel = sum(gcd(x, Q) == 1 for x in range(start, stop))
    represented = len(reps)
    if represented > wheel or sum(ppop.values()) + sum(cpop.values()) != represented:
        raise ValueError("representation population conservation failure")
    validation = {key: 0 for key in VALIDATION_KEYS}
    target = frozen_gates(pfreq, cfreq, pby, cby, ppop, cpop, validation)
    return {
        "experiment": "E014-H14-OBS020", "implementation_commit": implementation_commit,
        "band": {"name": "H14", "range": list(H14), "interval_semantics": "half-open"},
        "partition": [{"name": n, "range": list(bounds), "role": role}
                      for n, bounds, role in frozen.PARTITION],
        "parameters": frozen.parameters(), "generation_plan": plan_h14(),
        "anchor_summary": {
            "wheel_anchor_count": wheel, "represented_anchor_count": represented,
            "unrepresented_anchor_count": wheel - represented,
            "prime_count": sum(ppop.values()), "composite_count": sum(cpop.values()),
            "prime_counts_by_R90": [ppop[r] for r in R90],
            "composite_counts_by_R90": [cpop[r] for r in R90],
        },
        "validation": validation, "target": target,
    }


def canonical_json(payload):
    if type(payload) is not dict or set(payload) != SCHEMA[""]:
        raise ValueError("top-level H14 JSON allowlist violation")
    for section in ("band", "parameters", "anchor_summary", "validation", "target"):
        if type(payload[section]) is not dict or set(payload[section]) != SCHEMA[section]:
            raise ValueError("H14 JSON section allowlist violation: " + section)
    for section, count in (("partition", 5), ("generation_plan", 2)):
        if (type(payload[section]) is not list or len(payload[section]) != count
                or any(type(v) is not dict or set(v) != SCHEMA[section]
                       for v in payload[section])):
            raise ValueError("H14 JSON row allowlist violation: " + section)
    if (payload["experiment"] != "E014-H14-OBS020"
            or type(payload["implementation_commit"]) is not str
            or len(payload["implementation_commit"]) != 40
            or any(c not in "0123456789abcdef" for c in payload["implementation_commit"])):
        raise ValueError("invalid implementation provenance")
    if payload["band"] != {"name": "H14", "range": list(H14), "interval_semantics": "half-open"}:
        raise ValueError("invalid H14 metadata")
    if payload["partition"] != [{"name": n, "range": list(b), "role": role}
                                for n, b, role in frozen.PARTITION]:
        raise ValueError("frozen partitions changed")
    if payload["parameters"] != frozen.parameters() or payload["generation_plan"] != plan_h14():
        raise ValueError("parameter/plan mismatch")
    if any(type(v) is not int or v != 0 for v in payload["validation"].values()):
        raise ValueError("nonzero/invalid validation failure counter")
    s = payload["anchor_summary"]
    scalars = ("wheel_anchor_count", "represented_anchor_count", "unrepresented_anchor_count",
               "prime_count", "composite_count")
    if (any(type(s[k]) is not int or s[k] < 0 for k in scalars)
            or any(type(s[k]) is not list or len(s[k]) != 16
                   or any(type(v) is not int or v < 0 for v in s[k])
                   for k in ("prime_counts_by_R90", "composite_counts_by_R90"))
            or s["represented_anchor_count"] + s["unrepresented_anchor_count"] != s["wheel_anchor_count"]
            or s["prime_count"] + s["composite_count"] != s["represented_anchor_count"]
            or sum(s["prime_counts_by_R90"]) != s["prime_count"]
            or sum(s["composite_counts_by_R90"]) != s["composite_count"]):
        raise ValueError("population/class conservation invalid")
    t = payload["target"]
    numeric = ("prime_target_count", "highest_competing_prime_count",
               "composite_target_count", "mixed_class_count", "positive_class_count",
               "aggregate_enrichment_numerator")
    bools = ("population_floor_passed", "class_floor_passed", "strict_unique_prime_mode",
             "occurrence_floor_passed", "mixed_class_floor_passed", "positive_class_floor_passed",
             "aggregate_enrichment_positive", "replicated")
    if (t["observation"] != "OBS-020" or t["family"] != "I2" or type(t["signature"]) is not int
            or t["signature"] != TARGET or any(type(t[k]) is not int for k in numeric)
            or any(type(t[k]) is not bool for k in bools)):
        raise ValueError("target-specific typed schema violation")
    n, c = s["prime_count"], s["composite_count"]
    if (not 0 <= t["prime_target_count"] <= n or not 0 <= t["composite_target_count"] <= c
            or not 0 <= t["highest_competing_prime_count"] <= n - t["prime_target_count"]
            or not 0 <= t["mixed_class_count"] <= 16 or not 0 <= t["positive_class_count"] <= 16
            or t["aggregate_enrichment_numerator"] != t["prime_target_count"] * c - t["composite_target_count"] * n):
        raise ValueError("target counts/enrichment inconsistent")
    checks = {
        "population_floor_passed": n >= 1000 and c >= 1000,
        "class_floor_passed": all(p >= 10 and q >= 10 for p, q in zip(s["prime_counts_by_R90"], s["composite_counts_by_R90"])),
        "strict_unique_prime_mode": t["prime_target_count"] > t["highest_competing_prime_count"],
        "occurrence_floor_passed": t["prime_target_count"] >= 32,
        "mixed_class_floor_passed": t["mixed_class_count"] >= 12,
        "positive_class_floor_passed": t["positive_class_count"] >= 10,
        "aggregate_enrichment_positive": t["aggregate_enrichment_numerator"] > 0,
    }
    if any(t[k] != v for k, v in checks.items()) or t["replicated"] != all(checks.values()):
        raise ValueError("frozen target gate/result mismatch")
    return (json.dumps(payload, sort_keys=True, indent=2, ensure_ascii=True) + "\n").encode("utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--implementation-commit", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    plan = plan_h14()
    authorize(plan, "H14")
    primes = generate(plan, "H14")
    raw = canonical_json(evaluate(primes, args.implementation_commit))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(raw)


if __name__ == "__main__":
    main()
