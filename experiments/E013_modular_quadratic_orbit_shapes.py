#!/usr/bin/env python3
"""Frozen E013 D13-only modular quadratic short-orbit evaluator."""
from __future__ import annotations

import argparse
import json
from collections import Counter
from math import isqrt
from pathlib import Path

W, Q, K, SEED = 1_000_000, 30, 10, 2
R30 = (1, 7, 11, 13, 17, 19, 23, 29)
FAMILIES = ("O1", "O2", "O3", "O4")
PARTITION = (
    ("G13-pre", (71_000_000, 72_000_000), "guard"),
    ("D13", (72_000_000, 73_000_000), "discovery"),
    ("G13-mid", (73_000_000, 74_000_000), "guard"),
    ("H13", (74_000_000, 75_000_000), "holdout"),
    ("A13", (144_000_000, 145_000_000), "adversarial"),
)
# All 53 historical intervals are provenance metadata only (million-aligned).
OLD_MILLIONS = (
    (0, 1), (1, 2), (2, 3), (4, 5), (8, 9), (10, 11), (16, 17),
    (32, 33), (35, 36), (39, 40), (42, 43), (44, 45), (46, 47),
    (48, 49), (50, 51), (54, 55), (56, 57), (58, 59), (60, 61),
    (62, 63), (64, 65), (67, 68),
    (33, 34), (37, 38), (41, 42), (52, 53), (66, 67), (69, 70),
    (70, 71), (78, 79), (84, 85), (92, 93), (108, 109), (116, 117),
    (124, 125), (134, 135),
    (34, 35), (36, 37), (38, 39), (40, 41), (43, 44), (45, 46),
    (47, 48), (49, 50), (51, 52), (53, 54), (55, 56), (57, 58),
    (59, 60), (61, 62), (63, 64), (65, 66), (68, 69),
)
E005 = tuple((i, i + 1_048_576) for i in (
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
         "generation_plan", "anchor_summary", "validation", "families", "promotions"},
    "band": {"name", "range", "interval_semantics"},
    "partition": {"name", "range", "role"},
    "parameters": {"width", "wheel", "reduced_residues", "seed", "polynomial_map",
                   "steps", "tail_start", "tail_length", "population_floor", "class_floor",
                   "occurrence_floor", "mixed_class_floor"},
    "generation_plan": {"purpose", "start", "stop", "strategy"},
    "anchor_summary": {"anchor_count", "prime_count", "composite_count",
                       "first_prime", "last_prime", "prime_counts_by_R30",
                       "composite_counts_by_R30", "collision_prime_count",
                       "collision_composite_count"},
    "validation": set(VALIDATION_KEYS),
    "families": {"family", "prime_mode_count", "maximizer_count",
                 "highest_competing_count", "strict_unique_prime_mode",
                 "unique_mode_signature", "unique_mode_is_noncollision",
                 "target_composite_count", "population_floor_passed", "class_floor_passed",
                 "occurrence_floor_passed", "mixed_class_count", "mixed_class_floor_passed",
                 "aggregate_enrichment_numerator", "aggregate_enrichment_positive",
                 "mechanically_eligible"},
    "promotions": {"family", "target_signature", "target_prime_count",
                   "target_composite_count", "mixed_class_count",
                   "aggregate_enrichment_numerator"},
}


def overlap(a, b):
    return a[0] < b[1] and b[0] < a[1]


def metadata_check():
    assert (W, Q, K, SEED, R30) == (1_000_000, 30, 10, 2, (1, 7, 11, 13, 17, 19, 23, 29))
    assert (W // 1000, W // 10000, isqrt(1000 - 1) + 1, (3 * len(R30) + 3) // 4) == (1000, 100, 32, 6)
    assert len(OLD_MILLIONS) == 53 and len(E005) == 6
    assert [x[0] for x in PARTITION] == ["G13-pre", "D13", "G13-mid", "H13", "A13"]
    assert PARTITION[4][1][0] == 2 * PARTITION[1][1][0]
    old = [(a * W, b * W) for a, b in OLD_MILLIONS] + list(E005)
    new = [row[1] for row in PARTITION]
    assert all(b - a == W for a, b in new)
    assert sum(overlap(a, b) for a in new for b in old) == 0
    assert sum(overlap(a, b) for i, a in enumerate(new) for b in new[i + 1:]) == 0
    assert len(new) * len(old) + len(new) * (len(new) - 1) // 2 == 305
    assert [isqrt(b - 1) + 1 for _, (a, b), role in PARTITION if role not in ("guard",)] == [8545, 8661, 12042]


def plan_d13():
    return [
        {"purpose": "base_sieve_support", "start": 0, "stop": 8545, "strategy": "whole_prefix"},
        {"purpose": "segmented_target", "start": 72_000_000, "stop": 73_000_000,
         "strategy": "segmented"},
    ]


def authorize(plan, band):
    metadata_check()
    if band != "D13" or type(plan) is not list or plan != plan_d13():
        raise ValueError("D1-39 only authorizes exact ordered two-entry D13 plan")
    if any(set(record) != SCHEMA["generation_plan"] for record in plan):
        raise ValueError("unexpected plan key")


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


def generate(plan, band, low_generator=low_sieve, high_generator=target_sieve):
    authorize(plan, band)  # full-plan authorization BEFORE *either* generator
    base = low_generator(plan[0]["stop"])
    primes = high_generator(plan[1]["start"], plan[1]["stop"], base)
    return primes


def orbit(x):
    if not isinstance(x, int) or x <= 2:
        raise ValueError("invalid orbit modulus")
    ys = [SEED]
    for _ in range(K):
        ys.append((ys[-1] * ys[-1] + 1) % x)
        if not 0 <= ys[-1] < x:
            raise AssertionError("modular bound failed")
    return tuple(ys)


def shapes(tail):
    if len(tail) != 7:
        raise ValueError("tail length must be seven")
    if len(set(tail)) < 7:
        return ("COLLISION",) * 4
    bits = tuple(int(a > b) for a, b in zip(tail, tail[1:]))
    maxima = sum(int(v > max(tail[:i])) for i, v in enumerate(tail) if i > 0)
    streak = best = 1
    for b in bits:
        streak = streak + 1 if b == 0 else 1
        best = max(best, streak)
    result = (sum(bits), maxima, bits, best)
    if result[0] != sum(result[2]) or result[3] != 1 + max(
        (len(z) for z in "".join(map(str, bits)).split("1")), default=0
    ) or not 0 <= maxima <= 6:
        raise AssertionError("forced shape identity failed")
    return result


def signature_json(signature):
    return list(signature) if isinstance(signature, tuple) else signature


def mode_info(counter):
    if not counter:
        return None, 0, 0, 0
    highest = max(counter.values())
    winners = [key for key, value in counter.items() if value == highest]
    if len(winners) != 1:
        return None, highest, len(winners), highest
    target = winners[0]
    return target, highest, 1, max((v for k, v in counter.items() if k != target), default=0)


def mixed_count(target, prime_by_residue, comp_by_residue, prime_pop, comp_pop):
    return sum(
        0 < prime_by_residue[r][target] < prime_pop[r]
        and 0 < comp_by_residue[r][target] < comp_pop[r]
        for r in R30
    )


def enrichment(np, nc, pop_p, pop_c):
    return np * pop_c - nc * pop_p


def choose_rows(prime_counters, comp_counters, prime_by_r, comp_by_r, prime_pop,
                comp_pop, support_sets, validation):
    p_total, c_total = sum(prime_pop.values()), sum(comp_pop.values())
    populations_ok = p_total >= 1000 and c_total >= 1000
    classes_ok = all(prime_pop[r] >= 100 and comp_pop[r] >= 100 for r in R30)
    if any(validation.values()):
        populations_ok = classes_ok = False
    rows, promotions, prior_support = [], [], []
    for j, family in enumerate(FAMILIES):
        pc, cc = prime_counters[j], comp_counters[j]
        if sum(pc.values()) != p_total or sum(cc.values()) != c_total:
            raise AssertionError("family frequency conservation failure")
        target, count, winners, runner = mode_info(pc)
        unique = target is not None
        comp_count = cc[target] if unique else None
        mixed = mixed_count(target, prime_by_r[j], comp_by_r[j], prime_pop, comp_pop) if unique else None
        e = enrichment(count, comp_count, p_total, c_total) if unique else None
        noncollision = unique and target != "COLLISION"
        occurrence_ok = count >= 32 and unique
        mixed_ok = mixed is not None and mixed >= 6
        enriched = e is not None and e > 0
        eligible = bool(populations_ok and classes_ok and noncollision and occurrence_ok and mixed_ok and enriched)
        if eligible:
            support = support_sets[j].get(target, set())
            if len(support) != count:
                raise AssertionError("support set/frequency mismatch")
            if any(support == previous for previous in prior_support):
                eligible = False
            else:
                prior_support.append(support)
                promotions.append({"family": family, "target_signature": signature_json(target),
                                   "target_prime_count": count, "target_composite_count": comp_count,
                                   "mixed_class_count": mixed, "aggregate_enrichment_numerator": e})
        rows.append({"family": family, "prime_mode_count": count, "maximizer_count": winners,
                     "highest_competing_count": runner, "strict_unique_prime_mode": unique,
                     "unique_mode_signature": signature_json(target) if unique else None,
                     "unique_mode_is_noncollision": bool(noncollision),
                     "target_composite_count": comp_count,
                     "population_floor_passed": populations_ok, "class_floor_passed": classes_ok,
                     "occurrence_floor_passed": occurrence_ok, "mixed_class_count": mixed,
                     "mixed_class_floor_passed": mixed_ok,
                     "aggregate_enrichment_numerator": e, "aggregate_enrichment_positive": enriched,
                     "mechanically_eligible": eligible})
    if len(promotions) > 4 or any(row["family"] != FAMILIES[i] for i, row in enumerate(rows)):
        raise AssertionError("promotion cap/order violation")
    return rows, promotions


def evaluate(primes, code_commit):
    start, stop = PARTITION[1][1]
    if any(x < start or x >= stop for x in primes):
        raise ValueError("prime membership outside authorized target")
    pcount, ccount = Counter(), Counter()
    pby = [{r: Counter() for r in R30} for _ in FAMILIES]
    cby = [{r: Counter() for r in R30} for _ in FAMILIES]
    pfreq, cfreq = [Counter() for _ in FAMILIES], [Counter() for _ in FAMILIES]
    supports = [dict() for _ in FAMILIES]
    collision = [0, 0]
    used_prime = []
    anchors = 0
    for x in range(start, stop):
        r = x % Q
        if r not in R30:
            continue
        anchors += 1
        prime = x in primes
        (pcount if prime else ccount)[r] += 1
        if prime:
            used_prime.append(x)
        ys = orbit(x)
        if ys[:5] != (2, 5, 26, 677, 458330):
            raise AssertionError("frozen prefix changed")
        tail = ys[4:11]
        signatures = shapes(tail)
        collision[int(not prime)] += int(signatures[0] == "COLLISION")
        for j, signature in enumerate(signatures):
            (pfreq if prime else cfreq)[j][signature] += 1
            (pby if prime else cby)[j][r][signature] += 1
            if prime:
                supports[j].setdefault(signature, set()).add(x)
    if anchors != sum(pcount.values()) + sum(ccount.values()) or anchors != 266_666:
        raise AssertionError("anchor/population conservation failed")
    if sum(pcount.values()) != len(used_prime) or any(x not in primes for x in used_prime):
        raise AssertionError("prime label conservation failed")
    if any(sum(pby[j][r].values()) != pcount[r] or sum(cby[j][r].values()) != ccount[r]
           for j in range(4) for r in R30):
        raise AssertionError("R30 frequency partition failed")
    validation = {key: 0 for key in VALIDATION_KEYS}
    rows, promotions = choose_rows(pfreq, cfreq, pby, cby, pcount, ccount, supports, validation)
    payload = {
        "experiment": "E013", "implementation_commit": code_commit,
        "band": {"name": "D13", "range": [start, stop], "interval_semantics": "half-open"},
        "partition": [{"name": name, "range": list(interval), "role": role} for name, interval, role in PARTITION],
        "parameters": {"width": W, "wheel": Q, "reduced_residues": list(R30),
                       "seed": SEED, "polynomial_map": "y^2+1 mod x", "steps": K,
                       "tail_start": 4, "tail_length": 7,
                       "population_floor": 1000, "class_floor": 100,
                       "occurrence_floor": 32, "mixed_class_floor": 6},
        "generation_plan": plan_d13(),
        "anchor_summary": {"anchor_count": anchors, "prime_count": sum(pcount.values()),
                           "composite_count": sum(ccount.values()),
                           "first_prime": min(used_prime) if used_prime else None,
                           "last_prime": max(used_prime) if used_prime else None,
                           "prime_counts_by_R30": [pcount[r] for r in R30],
                           "composite_counts_by_R30": [ccount[r] for r in R30],
                           "collision_prime_count": collision[0],
                           "collision_composite_count": collision[1]},
        "validation": validation, "families": rows, "promotions": promotions,
    }
    return payload


def canonical_json(payload):
    if set(payload) != SCHEMA[""]:
        raise ValueError("top-level allowlist violation")
    for key in ("band", "parameters", "anchor_summary", "validation"):
        if not isinstance(payload[key], dict) or set(payload[key]) != SCHEMA[key]:
            raise ValueError("object allowlist violation: " + key)
    for key in ("partition", "generation_plan", "families", "promotions"):
        if not isinstance(payload[key], list) or any(
            not isinstance(item, dict) or set(item) != SCHEMA[key] for item in payload[key]
        ):
            raise ValueError("array-object allowlist violation: " + key)
    if len(payload["partition"]) != 5 or len(payload["generation_plan"]) != 2 or len(payload["families"]) != 4 or len(payload["promotions"]) > 4:
        raise ValueError("invalid record multiplicity")
    if [v["family"] for v in payload["families"]] != list(FAMILIES) or [v["family"] for v in payload["promotions"]] != [v["family"] for v in payload["families"] if v["mechanically_eligible"]]:
        raise ValueError("noncanonical family order")
    if payload["generation_plan"] != plan_d13() or any(v["name"] != p[0] or v["range"] != list(p[1]) or v["role"] != p[2] for v, p in zip(payload["partition"], PARTITION)):
        raise ValueError("noncanonical metadata")
    if set(payload["validation"]) != set(VALIDATION_KEYS) or any(type(x) is not int or x != 0 for x in payload["validation"].values()):
        raise ValueError("nonzero validation failures")
    def check_sig(family, value):
        if value is None or value == "COLLISION":
            return True
        if family == "O3":
            return type(value) is list and len(value) == 6 and all(type(v) is int and v in (0, 1) for v in value)
        return type(value) is int and (0 <= value <= (6 if family in ("O1", "O2") else 7)) and (family != "O4" or value >= 1)
    if any(not check_sig(row["family"], row["unique_mode_signature"]) for row in payload["families"]) or any(not check_sig(row["family"], row["target_signature"]) for row in payload["promotions"]):
        raise ValueError("signature encoding violates frozen family grammar")
    return (json.dumps(payload, sort_keys=True, indent=2, allow_nan=False) + "\n").encode("utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--band", required=True)
    parser.add_argument("--code-commit", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    if args.band != "D13" or len(args.code_commit) != 40 or any(c not in "0123456789abcdef" for c in args.code_commit):
        raise ValueError("invalid frozen phase/code-commit")
    plan = plan_d13()
    primes = generate(plan, args.band)
    output = canonical_json(evaluate(primes, args.code_commit))
    Path(args.output).write_bytes(output)


if __name__ == "__main__":
    main()
