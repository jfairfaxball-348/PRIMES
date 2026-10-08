#!/usr/bin/env python3
"""E013 frozen H13-only replication of OBS-018/O1=3 and OBS-019/O2=2."""
from __future__ import annotations

import argparse
import json
from collections import Counter
from math import isqrt
from pathlib import Path

W, Q, K, SEED = 1_000_000, 30, 10, 2
R30 = (1, 7, 11, 13, 17, 19, 23, 29)
TARGETS = (("OBS-018", "O1", 3), ("OBS-019", "O2", 2))
H13 = (74_000_000, 75_000_000)
PARTITION = (
    ("G13-pre", (71_000_000, 72_000_000), "guard"),
    ("D13", (72_000_000, 73_000_000), "discovery"),
    ("G13-mid", (73_000_000, 74_000_000), "guard"),
    ("H13", H13, "holdout"),
    ("A13", (144_000_000, 145_000_000), "adversarial"),
)
OLD_MILLIONS = (
    (0, 1), (1, 2), (2, 3), (4, 5), (8, 9), (10, 11), (16, 17),
    (32, 33), (35, 36), (39, 40), (42, 43), (44, 45), (46, 47),
    (48, 49), (50, 51), (54, 55), (56, 57), (58, 59), (60, 61),
    (62, 63), (64, 65), (67, 68), (33, 34), (37, 38), (41, 42),
    (52, 53), (66, 67), (69, 70), (70, 71), (78, 79), (84, 85),
    (92, 93), (108, 109), (116, 117), (124, 125), (134, 135),
    (34, 35), (36, 37), (38, 39), (40, 41), (43, 44), (45, 46),
    (47, 48), (49, 50), (51, 52), (53, 54), (55, 56), (57, 58),
    (59, 60), (61, 62), (63, 64), (65, 66), (68, 69),
)
E005 = tuple((n, n + 1_048_576) for n in (
    128_000_000, 256_000_000, 512_000_000,
    1_024_000_000, 2_048_000_000, 4_096_000_000,
))
VALIDATION_KEYS = (
    "plan_failure_count", "range_or_anchor_failure_count",
    "orbit_recurrence_or_bound_failure_count", "fixed_prefix_or_tail_failure_count",
    "collision_or_shape_failure_count", "family_identity_failure_count",
    "R30_partition_failure_count", "frequency_or_population_failure_count",
)
SCHEMA = {
    "": {"experiment", "implementation_commit", "band", "partition", "parameters",
         "generation_plan", "anchor_summary", "validation", "replications"},
    "band": {"name", "range", "interval_semantics"},
    "partition": {"name", "range", "role"},
    "parameters": {"width", "wheel", "reduced_residues", "seed", "polynomial_map",
                   "steps", "tail_start", "tail_length", "population_floor", "class_floor",
                   "occurrence_floor", "mixed_class_floor"},
    "generation_plan": {"purpose", "start", "stop", "strategy"},
    "anchor_summary": {"anchor_count", "prime_count", "composite_count",
                       "prime_counts_by_R30", "composite_counts_by_R30"},
    "validation": set(VALIDATION_KEYS),
    "replications": {"observation", "family", "frozen_target", "target_prime_count",
                     "highest_competing_prime_count", "target_composite_count",
                     "population_floor_passed", "class_floor_passed", "strict_unique_target_mode",
                     "occurrence_floor_passed", "mixed_class_count", "mixed_class_floor_passed",
                     "aggregate_enrichment_numerator", "aggregate_enrichment_positive", "status"},
}


def plan_h13():
    return [
        {"purpose": "base_sieve_support", "start": 0, "stop": 8661, "strategy": "whole_prefix"},
        {"purpose": "segmented_target", "start": 74_000_000, "stop": 75_000_000,
         "strategy": "segmented"},
    ]


def metadata_check():
    assert (W, Q, K, SEED, R30) == (1_000_000, 30, 10, 2, (1, 7, 11, 13, 17, 19, 23, 29))
    assert (W // 1000, W // 10000, isqrt(999) + 1, (3 * len(R30) + 3) // 4) == (1000, 100, 32, 6)
    assert isqrt(H13[1] - 1) + 1 == 8661
    assert len(OLD_MILLIONS) == 53 and len(E005) == 6
    assert [row[0] for row in PARTITION] == ["G13-pre", "D13", "G13-mid", "H13", "A13"]
    assert PARTITION[4][1][0] == 2 * PARTITION[1][1][0]
    old = [(a * W, b * W) for a, b in OLD_MILLIONS] + list(E005)
    new = [row[1] for row in PARTITION]
    overlap = lambda a, b: a[0] < b[1] and b[0] < a[1]
    assert all(b - a == W for a, b in new)
    assert len(new) * len(old) + len(new) * (len(new) - 1) // 2 == 305
    assert not any(overlap(a, b) for a in new for b in old)
    assert not any(overlap(a, b) for i, a in enumerate(new) for b in new[i + 1:])


def authorize(plan, phase):
    metadata_check()
    if phase != "H13" or type(plan) is not list or plan != plan_h13():
        raise ValueError("D1-40 authorizes only exact ordered H13 two-entry generation plan")
    if any(type(record) is not dict or set(record) != SCHEMA["generation_plan"] for record in plan):
        raise ValueError("unexpected plan keys")


def low_sieve(limit):
    flags = bytearray(b"\x01") * limit
    flags[:2] = b"\x00\x00"
    for p in range(2, isqrt(limit - 1) + 1):
        if flags[p]:
            flags[p * p:limit:p] = b"\x00" * ((limit - 1 - p * p) // p + 1)
    return [i for i, flag in enumerate(flags) if flag]


def target_sieve(start, stop, base):
    flags = bytearray(b"\x01") * (stop - start)
    for p in base:
        first = max(p * p, ((start + p - 1) // p) * p)
        if first < stop:
            flags[first - start:stop - start:p] = b"\x00" * ((stop - 1 - first) // p + 1)
    return {start + i for i, flag in enumerate(flags) if flag}


def generate(plan, phase, low_generator=low_sieve, high_generator=target_sieve):
    authorize(plan, phase)  # Entire ordered plan checked before EITHER generator.
    base = low_generator(plan[0]["stop"])
    return high_generator(plan[1]["start"], plan[1]["stop"], base)


def shapes(tail):
    if len(tail) != 7:
        raise ValueError("tail length")
    if len(set(tail)) != 7:
        return ("COLLISION", "COLLISION")
    b = [int(a > z) for a, z in zip(tail, tail[1:])]
    o1 = sum(b)
    o2 = sum(v > max(tail[:i]) for i, v in enumerate(tail) if i > 0)
    assert 0 <= o1 <= 6 and 0 <= o2 <= 6
    return (o1, o2)


def orbit_signatures(x):
    if type(x) is not int or x <= 2:
        raise ValueError("bad modulus")
    y = SEED
    tail = []
    for i in range(1, K + 1):
        y = (y * y + 1) % x
        if not 0 <= y < x:
            raise AssertionError("modular range failure")
        if i == 4 and x > 458330 and y != 458330:
            raise AssertionError("frozen prefix failure")
        if i >= 4:
            tail.append(y)
    return shapes(tail)


def criterion(counter_p, counter_c, by_p, by_c, pop_p, pop_c, target, observation, family, validation):
    np, nc = counter_p[target], counter_c[target]
    highest_competitor = max((n for s, n in counter_p.items() if s != target), default=0)
    pp, cp = sum(pop_p.values()), sum(pop_c.values())
    pop_ok = pp >= 1000 and cp >= 1000
    class_ok = all(pop_p[r] >= 100 and pop_c[r] >= 100 for r in R30)
    strict = target != "COLLISION" and np > highest_competitor and np > 0
    occurrence_ok = np >= 32
    mixed = sum(0 < by_p[r][target] < pop_p[r] and 0 < by_c[r][target] < pop_c[r] for r in R30)
    enriched = np * cp - nc * pp
    passed = (not any(validation.values()) and pop_ok and class_ok and strict
              and occurrence_ok and mixed >= 6 and enriched > 0)
    return {"observation": observation, "family": family, "frozen_target": target,
            "target_prime_count": np, "highest_competing_prime_count": highest_competitor,
            "target_composite_count": nc, "population_floor_passed": pop_ok,
            "class_floor_passed": class_ok, "strict_unique_target_mode": strict,
            "occurrence_floor_passed": occurrence_ok, "mixed_class_count": mixed,
            "mixed_class_floor_passed": mixed >= 6,
            "aggregate_enrichment_numerator": enriched,
            "aggregate_enrichment_positive": enriched > 0,
            "status": "REPLICATED" if passed else "REFUTED"}


def evaluate(primes, code_commit):
    start, stop = H13
    if any(type(x) is not int or not start <= x < stop for x in primes):
        raise ValueError("prime label outside H13")
    pcount, ccount = Counter(), Counter()
    ptotal, ctotal = [Counter(), Counter()], [Counter(), Counter()]
    pby = [{r: Counter() for r in R30} for _ in TARGETS]
    cby = [{r: Counter() for r in R30} for _ in TARGETS]
    anchors = 0
    for x in range(start, stop):
        residue = x % Q
        if residue not in R30:
            continue
        anchors += 1
        isp = x in primes
        (pcount if isp else ccount)[residue] += 1
        sigs = orbit_signatures(x)
        for j, sig in enumerate(sigs):
            (ptotal if isp else ctotal)[j][sig] += 1
            (pby if isp else cby)[j][residue][sig] += 1
    pp, cp = sum(pcount.values()), sum(ccount.values())
    if anchors != 266_666 or anchors != pp + cp:
        raise AssertionError("anchor count mismatch")
    if any(sum(ptotal[j].values()) != pp or sum(ctotal[j].values()) != cp for j in range(2)):
        raise AssertionError("frequency conservation failed")
    if any(sum(pby[j][r].values()) != pcount[r] or sum(cby[j][r].values()) != ccount[r]
           for j in range(2) for r in R30):
        raise AssertionError("R30 partition failure")
    validation = {key: 0 for key in VALIDATION_KEYS}
    rows = [criterion(ptotal[j], ctotal[j], pby[j], cby[j], pcount, ccount,
                      target, obs, family, validation)
            for j, (obs, family, target) in enumerate(TARGETS)]
    return {
        "experiment": "E013", "implementation_commit": code_commit,
        "band": {"name": "H13", "range": list(H13), "interval_semantics": "half-open"},
        "partition": [{"name": name, "range": list(interval), "role": role} for name, interval, role in PARTITION],
        "parameters": {"width": W, "wheel": Q, "reduced_residues": list(R30), "seed": SEED,
                       "polynomial_map": "y^2+1 mod x", "steps": K, "tail_start": 4,
                       "tail_length": 7, "population_floor": 1000, "class_floor": 100,
                       "occurrence_floor": 32, "mixed_class_floor": 6},
        "generation_plan": plan_h13(),
        "anchor_summary": {"anchor_count": anchors, "prime_count": pp, "composite_count": cp,
                           "prime_counts_by_R30": [pcount[r] for r in R30],
                           "composite_counts_by_R30": [ccount[r] for r in R30]},
        "validation": validation, "replications": rows,
    }


def canonical_json(payload):
    if type(payload) is not dict or set(payload) != SCHEMA[""]:
        raise ValueError("top-level allowlist failure")
    for key in ("band", "parameters", "anchor_summary", "validation"):
        if type(payload[key]) is not dict or set(payload[key]) != SCHEMA[key]:
            raise ValueError("object allowlist failure: " + key)
    for key in ("partition", "generation_plan", "replications"):
        if type(payload[key]) is not list or any(type(item) is not dict or set(item) != SCHEMA[key] for item in payload[key]):
            raise ValueError("array allowlist failure: " + key)
    if payload["generation_plan"] != plan_h13() or len(payload["partition"]) != 5 or any(
        row != {"name": name, "range": list(interval), "role": role}
        for row, (name, interval, role) in zip(payload["partition"], PARTITION)
    ) or len(payload["replications"]) != 2:
        raise ValueError("metadata multiplicity failure")
    if [(r["observation"], r["family"], r["frozen_target"]) for r in payload["replications"]] != list(TARGETS):
        raise ValueError("frozen criterion-target identity failure")
    if any(type(v) is not int or v != 0 for v in payload["validation"].values()):
        raise ValueError("nonzero validation aggregates")
    for row in payload["replications"]:
        if row["status"] not in ("REPLICATED", "REFUTED"):
            raise ValueError("illegal status")
    return (json.dumps(payload, sort_keys=True, indent=2, allow_nan=False) + "\n").encode("utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", required=True)
    parser.add_argument("--code-commit", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    if args.phase != "H13" or len(args.code_commit) != 40 or any(c not in "0123456789abcdef" for c in args.code_commit):
        raise ValueError("invalid phase or code commit")
    primes = generate(plan_h13(), args.phase)
    Path(args.output).write_bytes(canonical_json(evaluate(primes, args.code_commit)))


if __name__ == "__main__":
    main()
