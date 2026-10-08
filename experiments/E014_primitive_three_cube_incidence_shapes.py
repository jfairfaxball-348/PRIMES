#!/usr/bin/env python3
"""Frozen E014 D14 primitive positive three-cube incidence discovery only."""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from math import gcd, isqrt
from pathlib import Path

W, Q, CAP = 1_000_000, 30, 4
R90 = tuple(r for r in range(90) if gcd(r, 30) == 1 and r % 9 in (1, 2, 7, 8))
FAMILIES = ("I1", "I2")
PARTITION = (
    ("G14-pre", (75_000_000, 76_000_000), "guard"),
    ("D14", (76_000_000, 77_000_000), "discovery"),
    ("G14-mid", (77_000_000, 78_000_000), "guard"),
    ("H14", (79_000_000, 80_000_000), "holdout"),
    ("A14", (152_000_000, 153_000_000), "adversarial"),
)
# Frozen E013 historical provenance: 53 named million-aligned intervals; metadata only.
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
E013_ROLES = ((71, 72), (72, 73), (73, 74), (74, 75), (144, 145))
E005 = tuple((v, v + 1_048_576) for v in (
    128_000_000, 256_000_000, 512_000_000,
    1_024_000_000, 2_048_000_000, 4_096_000_000,
))
VALIDATION_KEYS = (
    "plan_failure_count", "anchor_domain_failure_count",
    "triple_normalization_failure_count", "cubic_sum_or_bound_failure_count",
    "modulo9_feasibility_failure_count", "incidence_graph_failure_count",
    "signature_identity_failure_count", "population_or_frequency_failure_count",
    "serializer_or_duplicate_failure_count",
)
SCHEMA = {
    "": {"experiment", "implementation_commit", "band", "partition", "parameters",
         "generation_plan", "anchor_summary", "validation", "families", "promotions"},
    "band": {"name", "range", "interval_semantics"},
    "partition": {"name", "range", "role"},
    "parameters": {"width", "wheel", "control_modulus", "control_residues", "summands",
                   "exponent", "primitive_gcd", "sorted_positive", "signature_cap",
                   "population_floor", "class_floor", "occurrence_floor",
                   "mixed_class_floor", "positive_class_floor"},
    "generation_plan": {"purpose", "start", "stop", "strategy"},
    "anchor_summary": {"wheel_anchor_count", "represented_anchor_count",
                       "unrepresented_anchor_count", "prime_count", "composite_count",
                       "prime_counts_by_R90", "composite_counts_by_R90"},
    "validation": set(VALIDATION_KEYS),
    "families": {"family", "prime_mode_count", "highest_competing_count",
                 "strict_unique_prime_mode", "unique_mode_signature", "target_composite_count",
                 "population_floor_passed", "class_floor_passed", "occurrence_floor_passed",
                 "mixed_class_count", "mixed_class_floor_passed", "positive_class_count",
                 "positive_class_floor_passed", "aggregate_enrichment_numerator",
                 "aggregate_enrichment_positive", "mechanically_eligible"},
    "promotions": {"family", "target_signature", "target_prime_count",
                   "target_composite_count", "mixed_class_count", "positive_class_count",
                   "aggregate_enrichment_numerator"},
}


def icbrt(n):
    """Exact floor nonnegative cube root without floats or primality queries."""
    if type(n) is not int or n < 0:
        raise ValueError("cube-root argument must be a nonnegative integer")
    lo, hi = 0, 1
    while hi**3 <= n:
        hi *= 2
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if mid**3 <= n:
            lo = mid
        else:
            hi = mid
    assert lo**3 <= n < (lo + 1)**3
    return lo


def overlap(a, b):
    return a[0] < b[1] and b[0] < a[1]


def metadata_check():
    historical = ([(a * W, b * W) for a, b in (*OLD_MILLIONS, *E013_ROLES)]
                  + list(E005))
    new = [band for _, band, _ in PARTITION]
    if len(OLD_MILLIONS) != 53 or len(historical) != 64 or len(R90) != 16:
        raise AssertionError("frozen metadata count changed")
    if any(b - a != W for a, b in new):
        raise AssertionError("invalid frozen band width")
    checks = [(a, b) for a in new for b in historical]
    checks += [(a, b) for i, a in enumerate(new) for b in new[i + 1:]]
    if len(checks) != 330 or any(overlap(a, b) for a, b in checks):
        raise AssertionError("protected interval overlap")
    if [isqrt(b - 1) + 1 for _, (a, b), role in PARTITION if role not in ("guard",)] != [8775, 8945, 12370]:
        raise AssertionError("low support bound changed")
    if [icbrt(b - 3) for _, (a, b), role in PARTITION if role not in ("guard",)] != [425, 430, 534]:
        raise AssertionError("cube cap changed")
    if PARTITION[4][1][0] != 2 * PARTITION[1][1][0]:
        raise AssertionError("adversarial reserve convention changed")
    return len(checks)


def plan_d14():
    return [
        {"purpose": "base_sieve_support", "start": 0, "stop": 8775, "strategy": "whole_prefix"},
        {"purpose": "segmented_target", "start": 76_000_000, "stop": 77_000_000,
         "strategy": "segmented"},
    ]


def authorize(plan, phase):
    metadata_check()
    if phase != "D14" or type(plan) is not list or len(plan) != 2:
        raise ValueError("only frozen D14 phase is authorized")
    if any(type(p) is not dict or set(p) != SCHEMA["generation_plan"] for p in plan):
        raise ValueError("unknown/missing generator-plan fields")
    if any(type(p[k]) is not int for p in plan for k in ("start", "stop")):
        raise ValueError("generator-plan integers required")
    if plan != plan_d14():
        raise ValueError("D14 requires exactly two positive-allowlist calls")


def low_sieve(stop):
    flags = bytearray(b"\x01") * stop
    flags[:2] = b"\x00\x00"
    for p in range(2, isqrt(stop - 1) + 1):
        if flags[p]:
            flags[p * p:stop:p] = b"\x00" * ((stop - 1 - p * p) // p + 1)
    return [i for i, yes in enumerate(flags) if yes]


def target_sieve(start, stop, base):
    flags = bytearray(b"\x01") * (stop - start)
    for p in base:
        first = max(p * p, ((start + p - 1) // p) * p)
        if first < stop:
            flags[first - start:stop - start:p] = b"\x00" * ((stop - 1 - first) // p + 1)
    return {start + i for i, yes in enumerate(flags) if yes}


def generate(plan, phase, low_generator=low_sieve, high_generator=target_sieve):
    authorize(plan, phase)  # Complete plan checked before any generator entry.
    authorize(plan, phase)  # Independent boundary recheck: no alternate helper.
    base = low_generator(plan[0]["stop"])
    authorize(plan, phase)  # Recheck before entry to high generator too.
    return high_generator(plan[1]["start"], plan[1]["stop"], base)


def primitive(triple):
    a, b, c = triple
    return 1 <= a <= b <= c and gcd(gcd(a, b), c) == 1


def enumerate_representations(start, stop):
    """Enumerate only triples whose *sum* lies in the target, before any labels."""
    if (start, stop) != PARTITION[1][1]:
        raise ValueError("only target-strict D14 enumeration authorized")
    result = defaultdict(list)
    ccap = icbrt(stop - 3)
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


def incidence_shapes(representations):
    """Shared *integer summand value* edges; BFS connected components."""
    triples = tuple(sorted(set(representations)))
    if not triples:
        return None
    if len(triples) != len(representations) or any(not primitive(t) for t in triples):
        raise AssertionError("noncanonical or repeated representation")
    n = len(triples)
    adjacency = [set() for _ in range(n)]
    for i in range(n):
        values = set(triples[i])
        for j in range(i + 1, n):
            if not values.isdisjoint(triples[j]):
                adjacency[i].add(j)
                adjacency[j].add(i)
    visited = set()
    largest = 0
    for i in range(n):
        if i in visited:
            continue
        component = {i}
        visited.add(i)
        stack = [i]
        while stack:
            for neighbour in adjacency[stack.pop()]:
                if neighbour not in visited:
                    visited.add(neighbour)
                    component.add(neighbour)
                    stack.append(neighbour)
        largest = max(largest, len(component))
    if len(visited) != n:
        raise AssertionError("incidence component conservation failure")
    i1, i2 = min(n, CAP), min(largest, CAP)
    if not (1 <= i2 <= i1 <= CAP) or (i1 == 1 and i2 != 1):
        raise AssertionError("signature identity failure")
    return i1, i2


def mode_info(counts):
    if any(counts[t] < 0 for t in (1, 2, 3, 4)):
        raise AssertionError("negative frequency")
    maximum = max(counts[t] for t in (1, 2, 3, 4))
    modes = [t for t in (1, 2, 3, 4) if counts[t] == maximum]
    return (modes[0], maximum, max(counts[t] for t in (1, 2, 3, 4) if t != modes[0])) if len(modes) == 1 else (None, maximum, maximum)


def choose_rows(prime_freq, comp_freq, pby, cby, ppop, cpop, supports, validation):
    npop, cpop_total = sum(ppop.values()), sum(cpop.values())
    floors = npop >= 1000 and cpop_total >= 1000
    class_floors = all(ppop[r] >= 10 and cpop[r] >= 10 for r in R90)
    if any(validation.values()):
        floors = class_floors = False
    rows, promotions, accepted_supports = [], [], []
    for j, family in enumerate(FAMILIES):
        pc, cc = prime_freq[j], comp_freq[j]
        if (set(pc) - {1, 2, 3, 4} or set(cc) - {1, 2, 3, 4}
                or sum(pc.values()) != npop or sum(cc.values()) != cpop_total):
            raise AssertionError("family frequency conservation failure")
        if any(sum(pby[j][r].values()) != ppop[r] or sum(cby[j][r].values()) != cpop[r]
               for r in R90):
            raise AssertionError("class frequency conservation failure")
        target, count, competing = mode_info(pc)
        unique = target is not None
        nc = cc[target] if unique else None
        mixed = sum(0 < pby[j][r][target] < ppop[r] and 0 < cby[j][r][target] < cpop[r]
                    for r in R90) if unique else None
        pos = sum(pby[j][r][target] * cpop[r] - cby[j][r][target] * ppop[r] > 0
                  for r in R90) if unique else None
        enrichment = count * cpop_total - nc * npop if unique else None
        occ_ok = unique and count >= 32
        mixed_ok = mixed is not None and mixed >= 12
        pos_ok = pos is not None and pos >= 10
        enriched = enrichment is not None and enrichment > 0
        eligible = bool(floors and class_floors and occ_ok and mixed_ok and pos_ok and enriched and not any(validation.values()))
        if eligible:
            support = supports[j].get(target, set())
            if len(support) != count:
                raise AssertionError("target support count mismatch")
            if any(support == prior for prior in accepted_supports):
                eligible = False
            else:
                accepted_supports.append(support)
                promotions.append({"family": family, "target_signature": target,
                                   "target_prime_count": count, "target_composite_count": nc,
                                   "mixed_class_count": mixed, "positive_class_count": pos,
                                   "aggregate_enrichment_numerator": enrichment})
        rows.append({"family": family, "prime_mode_count": count,
                     "highest_competing_count": competing, "strict_unique_prime_mode": unique,
                     "unique_mode_signature": target, "target_composite_count": nc,
                     "population_floor_passed": floors, "class_floor_passed": class_floors,
                     "occurrence_floor_passed": bool(occ_ok), "mixed_class_count": mixed,
                     "mixed_class_floor_passed": bool(mixed_ok), "positive_class_count": pos,
                     "positive_class_floor_passed": bool(pos_ok),
                     "aggregate_enrichment_numerator": enrichment,
                     "aggregate_enrichment_positive": bool(enriched),
                     "mechanically_eligible": eligible})
    if len(promotions) > 2 or [row["family"] for row in rows] != list(FAMILIES):
        raise AssertionError("family order or cap failure")
    return rows, promotions


def parameters():
    return {"width": W, "wheel": Q, "control_modulus": 90, "control_residues": list(R90),
            "summands": 3, "exponent": 3, "primitive_gcd": 1,
            "sorted_positive": True, "signature_cap": CAP,
            "population_floor": 1000, "class_floor": 10, "occurrence_floor": 32,
            "mixed_class_floor": 12, "positive_class_floor": 10}


def evaluate(target_primes, implementation_commit):
    start, stop = PARTITION[1][1]
    if any(type(p) is not int or not start <= p < stop for p in target_primes):
        raise ValueError("prime labels extend outside D14")
    reps = enumerate_representations(start, stop)  # No labels influence representation set.
    ppop, cpop = Counter(), Counter()
    pfreq, cfreq = [Counter() for _ in FAMILIES], [Counter() for _ in FAMILIES]
    pby = [{r: Counter() for r in R90} for _ in FAMILIES]
    cby = [{r: Counter() for r in R90} for _ in FAMILIES]
    supports = [{} for _ in FAMILIES]
    for x in sorted(reps):
        triples = reps[x]
        if not (start <= x < stop and gcd(x, Q) == 1):
            raise AssertionError("anchor domain failure")
        if x % 9 in (4, 5) or x % 90 not in R90:
            raise AssertionError("modulo-9 feasibility/control class failure")
        if any(not primitive(t) for t in triples):
            raise AssertionError("triple normalization failure")
        if any(sum(v**3 for v in t) != x or t[2] > icbrt(stop - 3) for t in triples):
            raise AssertionError("sum or bound failure")
        shapes = incidence_shapes(triples)
        if shapes is None:
            raise AssertionError("empty represented anchor")
        r = x % 90
        isprime = x in target_primes
        (ppop if isprime else cpop)[r] += 1
        for j, sig in enumerate(shapes):
            (pfreq if isprime else cfreq)[j][sig] += 1
            (pby if isprime else cby)[j][r][sig] += 1
            if isprime:
                supports[j].setdefault(sig, set()).add(x)
    anchor_count = sum(gcd(x, Q) == 1 for x in range(start, stop))
    represented = len(reps)
    if (represented > anchor_count or sum(ppop.values()) + sum(cpop.values()) != represented
            or any(sum(pby[j][r].values()) != ppop[r] or sum(cby[j][r].values()) != cpop[r]
                   for j in range(2) for r in R90)):
        raise AssertionError("represented/label/class conservation failure")
    validation = {key: 0 for key in VALIDATION_KEYS}
    rows, promotions = choose_rows(pfreq, cfreq, pby, cby, ppop, cpop, supports, validation)
    return {
        "experiment": "E014", "implementation_commit": implementation_commit,
        "band": {"name": "D14", "range": [start, stop], "interval_semantics": "half-open"},
        "partition": [{"name": name, "range": list(bounds), "role": role}
                      for name, bounds, role in PARTITION],
        "parameters": parameters(), "generation_plan": plan_d14(),
        "anchor_summary": {"wheel_anchor_count": anchor_count,
                           "represented_anchor_count": represented,
                           "unrepresented_anchor_count": anchor_count - represented,
                           "prime_count": sum(ppop.values()), "composite_count": sum(cpop.values()),
                           "prime_counts_by_R90": [ppop[r] for r in R90],
                           "composite_counts_by_R90": [cpop[r] for r in R90]},
        "validation": validation, "families": rows, "promotions": promotions,
    }


def canonical_json(payload):
    if type(payload) is not dict or set(payload) != SCHEMA[""]:
        raise ValueError("top-level JSON allowlist violation")
    for key in ("band", "parameters", "anchor_summary", "validation"):
        if type(payload[key]) is not dict or set(payload[key]) != SCHEMA[key]:
            raise ValueError("object JSON allowlist violation: " + key)
    for key in ("partition", "generation_plan", "families", "promotions"):
        if type(payload[key]) is not list or any(type(row) is not dict or set(row) != SCHEMA[key]
                                               for row in payload[key]):
            raise ValueError("row JSON allowlist violation: " + key)
    if len(payload["partition"]) != 5 or len(payload["generation_plan"]) != 2 or len(payload["families"]) != 2 or len(payload["promotions"]) > 2:
        raise ValueError("JSON row cardinality violation")
    if (payload["experiment"] != "E014" or type(payload["implementation_commit"]) is not str
            or len(payload["implementation_commit"]) != 40
            or any(c not in "0123456789abcdef" for c in payload["implementation_commit"])):
        raise ValueError("implementation provenance violation")
    if payload["band"] != {"name": "D14", "range": [76_000_000, 77_000_000], "interval_semantics": "half-open"}:
        raise ValueError("band metadata violation")
    if payload["parameters"] != parameters() or payload["generation_plan"] != plan_d14():
        raise ValueError("parameter or generator metadata violation")
    if payload["partition"] != [{"name": n, "range": list(b), "role": role} for n, b, role in PARTITION]:
        raise ValueError("protected partition metadata violation")
    if any(type(v) is not int or v != 0 for v in payload["validation"].values()):
        raise ValueError("nonzero/invalid validation: no success artifact allowed")
    s = payload["anchor_summary"]
    integer_fields = ("wheel_anchor_count", "represented_anchor_count", "unrepresented_anchor_count", "prime_count", "composite_count")
    if (any(type(s[k]) is not int or s[k] < 0 for k in integer_fields)
            or type(s["prime_counts_by_R90"]) is not list
            or type(s["composite_counts_by_R90"]) is not list
            or any(len(s[k]) != 16 or any(type(v) is not int or v < 0 for v in s[k])
                   for k in ("prime_counts_by_R90", "composite_counts_by_R90"))
            or s["represented_anchor_count"] + s["unrepresented_anchor_count"] != s["wheel_anchor_count"]
            or s["prime_count"] + s["composite_count"] != s["represented_anchor_count"]
            or sum(s["prime_counts_by_R90"]) != s["prime_count"]
            or sum(s["composite_counts_by_R90"]) != s["composite_count"]):
        raise ValueError("invalid population conservation")
    for j, row in enumerate(payload["families"]):
        if row["family"] != FAMILIES[j]:
            raise ValueError("family order violation")
        for key in ("prime_mode_count", "highest_competing_count"):
            if type(row[key]) is not int or row[key] < 0:
                raise ValueError("invalid mode frequencies")
        for key in ("strict_unique_prime_mode", "population_floor_passed", "class_floor_passed",
                    "occurrence_floor_passed", "mixed_class_floor_passed", "positive_class_floor_passed",
                    "aggregate_enrichment_positive", "mechanically_eligible"):
            if type(row[key]) is not bool:
                raise ValueError("invalid boolean gate")
        target = row["unique_mode_signature"]
        for key in ("target_composite_count", "mixed_class_count", "positive_class_count", "aggregate_enrichment_numerator"):
            if not ((row[key] is None and target is None) or (target is not None and type(row[key]) is int)):
                raise ValueError("invalid tied-mode null semantics")
        if ((target is None) != (not row["strict_unique_prime_mode"]) or
                (target is not None and (type(target) is not int or target not in (1, 2, 3, 4))) or
                (target is not None and row["prime_mode_count"] <= row["highest_competing_count"]) or
                (target is None and row["prime_mode_count"] != row["highest_competing_count"])):
            raise ValueError("invalid strict-mode semantics")
    expected = [row["family"] for row in payload["families"] if row["mechanically_eligible"]]
    if [row["family"] for row in payload["promotions"]] != expected:
        raise ValueError("promotion/family mechanical consistency violation")
    for promotion in payload["promotions"]:
        row = next(item for item in payload["families"] if item["family"] == promotion["family"])
        if (promotion["target_signature"] != row["unique_mode_signature"]
                or promotion["target_prime_count"] != row["prime_mode_count"]
                or promotion["target_composite_count"] != row["target_composite_count"]
                or promotion["mixed_class_count"] != row["mixed_class_count"]
                or promotion["positive_class_count"] != row["positive_class_count"]
                or promotion["aggregate_enrichment_numerator"] != row["aggregate_enrichment_numerator"]):
            raise ValueError("promotion/selection mismatch")
    return (json.dumps(payload, sort_keys=True, indent=2, ensure_ascii=True) + "\n").encode("utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--implementation-commit", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    plan = plan_d14()
    authorize(plan, "D14")
    primes = generate(plan, "D14")
    data = canonical_json(evaluate(primes, args.implementation_commit))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(data)


if __name__ == "__main__":
    main()
