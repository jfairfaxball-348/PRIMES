"""E019 D19-only exact two-row ladder boundary forest discovery.

All graph controls are prime-independent. The only prime-generation entry is
run(), after validate_plan() checks the complete positive plan and exclusions.
"""
from __future__ import annotations

import argparse
from collections import Counter
from itertools import combinations
import json
from math import gcd, isqrt
from pathlib import Path

WIDTH = 1_000_000
Q = 210
R210 = tuple(r for r in range(Q) if gcd(r, Q) == 1)
M = ((3, 1), (2, 1))
ROLES = (
    ("G19-pre", 98_000_000, 99_000_000, "guard"),
    ("D19", 99_000_000, 100_000_000, "discovery"),
    ("G19-mid", 100_000_000, 101_000_000, "guard"),
    ("H19", 101_000_000, 102_000_000, "holdout"),
    ("A19", 198_000_000, 199_000_000, "adversarial"),
)
# E013 frozen named *interval provenance* (no historical results).
EARLY = (
    ("D0", 0), ("H0", 1), ("S1", 2), ("S2", 4), ("S3", 8),
    ("A0-retired", 10), ("S4", 16), ("S5", 32), ("D3", 35),
    ("D4", 39), ("D6", 42), ("H6", 44), ("D7", 46), ("H7", 48),
    ("D8", 50), ("D9", 54), ("H9", 56), ("D10", 58),
    ("H10", 60), ("D11", 62), ("H11", 64), ("D12", 67),
    ("A1", 33), ("H3", 37), ("H4", 41), ("H8", 52),
    ("A8", 66), ("H12", 69), ("A3", 70), ("A4", 78),
    ("A6", 84), ("A7", 92), ("A9", 108), ("A10", 116),
    ("A11", 124), ("A12", 134), ("G3-pre", 34),
    ("G3-post", 36), ("G4-pre", 38), ("G4-mid", 40),
    ("G6-mid", 43), ("G7-pre", 45), ("G7-mid", 47),
    ("G8-pre", 49), ("G8-mid", 51), ("G9-pre", 53),
    ("G9-mid", 55), ("G10-pre", 57), ("G10-mid", 59),
    ("G11-pre", 61), ("G11-mid", 63), ("G12-pre", 65),
    ("G12-mid", 68),
)
LATER = (
    (13, (71, 72, 73, 74, 144)),
    (14, (75, 76, 77, 79, 152)),
    (15, (80, 81, 82, 83, 162)),
    (16, (85, 86, 87, 88, 172)),
    (17, (89, 90, 91, 93, 180)),
    (18, (94, 95, 96, 97, 190)),
)
CAL_STARTS = (128_000_000, 256_000_000, 512_000_000,
              1_024_000_000, 2_048_000_000, 4_096_000_000)
CAL_WIDTHS = (4096, 16384, 65536, 262144, 1048576)
VALIDATORS = (
    "plan_failure_count", "interval_exclusion_failure_count",
    "graph_state_semantics_failure_count", "transfer_matrix_failure_count",
    "remainder_bin_failure_count", "wheel_label_partition_failure_count",
    "frequency_conservation_failure_count", "signed_control_failure_count",
    "mode_duplicate_gate_failure_count", "serializer_failure_count",
)
FAMILY_KEYS = (
    "family", "prime_mode_count", "highest_competing_count",
    "strict_unique_prime_mode", "unique_mode_signature", "target_composite_count",
    "population_floor_passed", "class_floor_passed", "occurrence_floor_passed",
    "mixed_class_count", "mixed_class_floor_passed", "positive_class_count",
    "positive_class_floor_passed", "aggregate_enrichment_numerator",
    "aggregate_enrichment_positive", "mechanically_eligible",
)
PROMOTION_KEYS = (
    "family", "target_signature", "target_prime_count", "target_composite_count",
    "mixed_class_count", "positive_class_count", "aggregate_enrichment_numerator",
)
PARAMETERS = {
    "width": WIDTH, "wheel": Q, "residues_R210": list(R210),
    "graph_rows": 2, "boundary_state_order": ["C", "D"],
    "initial_state": [1, 1], "transfer_matrix": [[3, 1], [2, 1]],
    "exponent": "x-1", "remainder_modulus": "anchor", "joint_half_bins": 2,
    "population_floor": 1000, "class_floor": 10, "occurrence_floor": 32,
    "mixed_class_floor": 36, "positive_class_floor": 30,
    "strict_global_enrichment": True,
}
PLAN = (
    {"purpose": "base_sieve_support", "start": 0, "stop": 10000,
     "strategy": "whole_prefix"},
    {"purpose": "segmented_target", "start": 99_000_000, "stop": 100_000_000,
     "strategy": "direct_segmented"},
)


def overlaps(a, b):
    return a[0] < b[1] and b[0] < a[1]


def inventories():
    hist = [(name, m * WIDTH, (m + 1) * WIDTH) for name, m in EARLY]
    for year, vals in LATER:
        hist += [(f"{role}{year}", m * WIDTH, (m + 1) * WIDTH)
                 for role, m in zip(("G-pre", "D", "G-mid", "H", "A"), vals)]
    hist += [(f"E005-{i}", v, v + CAL_WIDTHS[-1])
             for i, v in enumerate(CAL_STARTS)]
    nested = [(f"E005-{i}-{w}", v, v + w)
              for i, v in enumerate(CAL_STARTS) for w in CAL_WIDTHS]
    new = [(name, a, b) for name, a, b, _ in ROLES]
    return hist, new, nested


def audit_intervals():
    old, new, nested = inventories()
    assert len(EARLY) == 53 and len(old) == 89 and len(new) == 5 and len(nested) == 30
    assert len({n for n, _, _ in old}) == 89
    assert sum(overlaps(a[1:], b[1:]) for a, b in combinations(old, 2)) == 0
    assert sum(overlaps(a[1:], b[1:]) for a in old for b in new) == 0
    assert sum(overlaps(a[1:], b[1:]) for a, b in combinations(new, 2)) == 0
    assert all(any(a <= c and d <= b for _, a, b in old) for _, c, d in nested)
    assert sum(overlaps(a[1:], b[1:]) for a in new for b in nested) == 0
    assert all(a % WIDTH == b % WIDTH == 0 for _, a, b in new)
    assert ROLES[4][1] == 2 * ROLES[1][1]
    assert isqrt(99_999_999) == 9999
    return {"old_pairs": 3916, "old_new": 445, "new_pairs": 10,
            "nested_contained": 30, "new_nested": 150}


def positive_plan():
    return [dict(entry) for entry in PLAN]


def validate_plan(plan, phase="D19", *, entry="direct"):
    """Fail closed *before* any generator; exact typed equality and role audit."""
    audit_intervals()
    if type(phase) is not str or phase != "D19" or entry != "direct":
        raise ValueError("unauthorized phase/helper")
    if type(plan) is not list or len(plan) != 2:
        raise ValueError("complete two-entry plan required")
    for actual, expected in zip(plan, PLAN):
        if type(actual) is not dict or set(actual) != set(expected):
            raise ValueError("plan schema")
        for key, expected_value in expected.items():
            if type(actual[key]) is not type(expected_value) or actual[key] != expected_value:
                raise ValueError("positive allowlist mismatch")
    assert PLAN[0]["stop"] == isqrt(PLAN[1]["stop"] - 1) + 1
    a, b = plan[1]["start"], plan[1]["stop"]
    assert all(not overlaps((a, b), (lo, hi))
               for name, lo, hi in inventories()[0] + inventories()[2])
    assert all(not overlaps((a, b), (lo, hi))
               for name, lo, hi, _ in ROLES if name != "D19")
    return True


def product_mod(a, b, n):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(2)) % n
                       for j in range(2)) for i in range(2))


def forest_mod(x):
    if type(x) is not int or x < 1:
        raise ValueError("positive anchor required")
    acc = ((1 % x, 0), (0, 1 % x))
    base = tuple(tuple(z % x for z in row) for row in M)
    e = x - 1
    while e:
        if e & 1:
            acc = product_mod(acc, base, x)
        base = product_mod(base, base, x)
        e >>= 1
    return (sum(acc[0]) % x, sum(acc[1]) % x)


def direct_states(n):
    if not isinstance(n, int) or n < 1 or n > 16:
        raise ValueError("synthetic small n only")
    c = d = 1
    for _ in range(1, n):
        c, d = 3*c+d, 2*c+d
    return c, d


def tiny_graph_states(n):
    """Independently enumerate all acyclic edge sets in tiny ladder L_n."""
    if type(n) is not int or not 1 <= n <= 4:
        raise ValueError("tiny graphs only")
    edges = []
    for i in range(n):
        edges.append((2*i, 2*i+1))
        if i:
            edges.extend(((2*i-2, 2*i), (2*i-1, 2*i+1)))
    connected = disconnected = 0
    for mask in range(1 << len(edges)):
        parent = list(range(2*n))
        def root(k):
            while parent[k] != k:
                k = parent[k]
            return k
        cyclic = False
        for j, (a, b) in enumerate(edges):
            if mask & (1 << j):
                a, b = root(a), root(b)
                if a == b:
                    cyclic = True
                    break
                parent[a] = b
        if cyclic or any(root(v) not in {root(2*n-2), root(2*n-1)}
                         for v in range(2*n)):
            continue
        if root(2*n-2) == root(2*n-1):
            connected += 1
        else:
            disconnected += 1
    return connected, disconnected


def signature(x):
    c, d = forest_mod(x)
    assert 0 <= c < x and 0 <= d < x
    u, v = (2*c)//x, (2*d)//x
    assert u in (0, 1) and v in (0, 1)
    return 2*u+v


def base_sieve(stop):
    # This entry MUST be preceded by validate_plan of the whole plan.
    table = bytearray(b"\x01") * stop
    table[:2] = b"\x00\x00"
    for p in range(2, isqrt(stop - 1) + 1):
        if table[p]:
            table[p*p:stop:p] = b"\x00" * (((stop - 1 - p*p)//p)+1)
    return [i for i, good in enumerate(table) if good]


def segment_flags(start, stop, base):
    # This entry MUST be preceded by validate_plan of the whole plan.
    flags = bytearray(b"\x01") * (stop-start)
    for p in base:
        first = max(p*p, ((start+p-1)//p)*p)
        if first < stop:
            flags[first-start:stop-start:p] = b"\x00" * ((stop-1-first)//p+1)
    return flags


def summarize(prime_flags, plan, code_commit):
    start, stop = PLAN[1]["start"], PLAN[1]["stop"]
    if len(prime_flags) != stop-start:
        raise ValueError("target coverage not complete")
    pcounts, ccounts = Counter(), Counter()
    by_p = [[0]*4 for _ in R210]
    by_c = [[0]*4 for _ in R210]
    supports = [set() for _ in range(4)]
    pos = {r: i for i, r in enumerate(R210)}
    for x in range(start, stop):
        idx = pos.get(x % Q)
        if idx is None:
            continue
        t = signature(x)
        if prime_flags[x-start]:
            pcounts[t] += 1
            by_p[idx][t] += 1
            supports[t].add(x)
        else:
            ccounts[t] += 1
            by_c[idx][t] += 1
    np = sum(pcounts.values()); nc = sum(ccounts.values())
    rnp = [sum(row) for row in by_p]; rnc = [sum(row) for row in by_c]
    assert np+nc == sum(1 for x in range(start, stop) if x % Q in pos)
    assert sum(rnp) == np and sum(rnc) == nc
    assert [pcounts[t] for t in range(4)] == [sum(row[t] for row in by_p) for t in range(4)]
    assert [ccounts[t] for t in range(4)] == [sum(row[t] for row in by_c) for t in range(4)]
    best = max(pcounts[t] for t in range(4))
    modes = [t for t in range(4) if pcounts[t] == best]
    unique = len(modes) == 1
    target = modes[0] if unique else None
    competitor = max((pcounts[t] for t in range(4) if t != target), default=best) if unique else best
    populations = np >= 1000 and nc >= 1000
    classes = all(a >= 10 and b >= 10 for a, b in zip(rnp, rnc))
    if unique:
        t = target
        mixed = sum(all(v > 0 for v in (by_p[i][t], rnp[i]-by_p[i][t],
                                         by_c[i][t], rnc[i]-by_c[i][t])) for i in range(48))
        positives = sum(by_p[i][t]*rnc[i]-by_c[i][t]*rnp[i] > 0 for i in range(48))
        enrichment = pcounts[t]*nc-ccounts[t]*np
    else:
        mixed = positives = enrichment = None
    eligible = bool(unique and populations and classes and pcounts[target] >= 32
                    and mixed >= 36 and positives >= 30 and enrichment > 0)
    # Exact integer-support duplicate detector, cap one, no fallback.
    selected = []
    if eligible:
        candidate = supports[target]
        if not any(candidate == old for old in selected):
            selected.append(candidate)
    assert len(selected) <= 1
    family = {
        "family": "B1", "prime_mode_count": best,
        "highest_competing_count": competitor,
        "strict_unique_prime_mode": unique, "unique_mode_signature": target,
        "target_composite_count": ccounts[target] if unique else None,
        "population_floor_passed": populations, "class_floor_passed": classes,
        "occurrence_floor_passed": bool(unique and pcounts[target] >= 32),
        "mixed_class_count": mixed,
        "mixed_class_floor_passed": bool(unique and mixed >= 36),
        "positive_class_count": positives,
        "positive_class_floor_passed": bool(unique and positives >= 30),
        "aggregate_enrichment_numerator": enrichment,
        "aggregate_enrichment_positive": bool(unique and enrichment > 0),
        "mechanically_eligible": bool(selected),
    }
    promotions = ([{
        "family": "B1", "target_signature": target,
        "target_prime_count": pcounts[target],
        "target_composite_count": ccounts[target],
        "mixed_class_count": mixed, "positive_class_count": positives,
        "aggregate_enrichment_numerator": enrichment,
    }] if selected else [])
    return {
        "experiment": "E019", "implementation_commit": code_commit,
        "band": {"name": "D19", "range": [start, stop],
                 "interval_semantics": "half-open"},
        "partition": [{"name": name, "range": [a, b], "role": role}
                      for name, a, b, role in ROLES],
        "parameters": PARAMETERS, "generation_plan": plan,
        "anchor_summary": {"wheel_anchor_count": np+nc,
                           "prime_count": np, "composite_count": nc,
                           "prime_counts_by_R210": rnp,
                           "composite_counts_by_R210": rnc},
        "validation": dict.fromkeys(VALIDATORS, 0),
        "families": [family], "promotions": promotions,
    }


def check_keys(value, fields):
    if type(value) is not dict or set(value) != set(fields):
        raise ValueError("unknown or missing evidence keys")


def typed_equal(a, b):
    """Nested strict JSON value/type equality: 1 never stands for true."""
    if type(a) is not type(b):
        return False
    if type(b) is dict:
        return set(a) == set(b) and all(typed_equal(a[k], v) for k, v in b.items())
    if type(b) is list:
        return len(a) == len(b) and all(typed_equal(x, y) for x, y in zip(a, b))
    return a == b


def exact_int(value, *, low=None, high=None):
    if type(value) is not int or (low is not None and value < low) or (high is not None and value > high):
        raise ValueError("noncanonical integer or range")


def exact_bool(value):
    if type(value) is not bool:
        raise ValueError("noncanonical boolean")


def validate_payload(o):
    check_keys(o, ("experiment", "implementation_commit", "band", "partition",
                   "parameters", "generation_plan", "anchor_summary", "validation",
                   "families", "promotions"))
    if o["experiment"] != "E019" or type(o["implementation_commit"]) is not str or len(o["implementation_commit"]) != 40 or any(c not in "0123456789abcdef" for c in o["implementation_commit"]):
        raise ValueError("experiment/commit")
    check_keys(o["band"], ("name", "range", "interval_semantics"))
    if not typed_equal(o["band"], {"name": "D19", "range": [99_000_000, 100_000_000], "interval_semantics": "half-open"}):
        raise ValueError("band")
    if not typed_equal(o["partition"], [{"name": n, "range": [a,b], "role": r} for n,a,b,r in ROLES]):
        raise ValueError("partition")
    check_keys(o["parameters"], PARAMETERS)
    if not typed_equal(o["parameters"], PARAMETERS):
        raise ValueError("parameters")
    validate_plan(o["generation_plan"])
    a = o["anchor_summary"]
    check_keys(a, ("wheel_anchor_count", "prime_count", "composite_count", "prime_counts_by_R210", "composite_counts_by_R210"))
    for k in ("wheel_anchor_count", "prime_count", "composite_count"):
        exact_int(a[k], low=0)
    for k in ("prime_counts_by_R210", "composite_counts_by_R210"):
        if type(a[k]) is not list or len(a[k]) != 48:
            raise ValueError("R210 summary")
        for n in a[k]: exact_int(n, low=0)
    if a["wheel_anchor_count"] != a["prime_count"]+a["composite_count"] or a["prime_count"] != sum(a["prime_counts_by_R210"]) or a["composite_count"] != sum(a["composite_counts_by_R210"]):
        raise ValueError("label conservation")
    check_keys(o["validation"], VALIDATORS)
    for v in o["validation"].values(): exact_int(v, low=0, high=0)
    if type(o["families"]) is not list or len(o["families"]) != 1:
        raise ValueError("single family")
    f = o["families"][0]; check_keys(f, FAMILY_KEYS)
    if f["family"] != "B1": raise ValueError("wrong family")
    for k in ("prime_mode_count", "highest_competing_count"):
        exact_int(f[k], low=0)
    for k in ("strict_unique_prime_mode", "population_floor_passed", "class_floor_passed",
              "occurrence_floor_passed", "mixed_class_floor_passed", "positive_class_floor_passed",
              "aggregate_enrichment_positive", "mechanically_eligible"):
        exact_bool(f[k])
    unique = f["strict_unique_prime_mode"]
    for k in ("unique_mode_signature", "target_composite_count", "mixed_class_count",
              "positive_class_count", "aggregate_enrichment_numerator"):
        if not unique:
            if f[k] is not None: raise ValueError("tie target leak")
        else:
            exact_int(f[k], low=(0 if k != "aggregate_enrichment_numerator" else None),
                      high=(3 if k == "unique_mode_signature" else 48 if k in ("mixed_class_count", "positive_class_count") else None))
    if unique and f["prime_mode_count"] <= f["highest_competing_count"]: raise ValueError("non-unique mode")
    if not unique and (f["mechanically_eligible"] or f["occurrence_floor_passed"] or
                       f["mixed_class_floor_passed"] or f["positive_class_floor_passed"] or
                       f["aggregate_enrichment_positive"]): raise ValueError("tie fallback")
    if f["population_floor_passed"] != (a["prime_count"] >= 1000 and a["composite_count"] >= 1000): raise ValueError("population floor")
    if f["class_floor_passed"] != all(x >= 10 and y >= 10 for x,y in zip(a["prime_counts_by_R210"], a["composite_counts_by_R210"])): raise ValueError("class floor")
    if unique:
        if f["occurrence_floor_passed"] != (f["prime_mode_count"] >= 32) or f["mixed_class_floor_passed"] != (f["mixed_class_count"] >= 36) or f["positive_class_floor_passed"] != (f["positive_class_count"] >= 30) or f["aggregate_enrichment_positive"] != (f["aggregate_enrichment_numerator"] > 0):
            raise ValueError("gate inconsistent")
    expected_eligible = (unique and f["population_floor_passed"] and f["class_floor_passed"] and f["occurrence_floor_passed"] and f["mixed_class_floor_passed"] and f["positive_class_floor_passed"] and f["aggregate_enrichment_positive"])
    if f["mechanically_eligible"] != expected_eligible: raise ValueError("promotion gate")
    promotions = o["promotions"]
    if type(promotions) is not list or len(promotions) != int(expected_eligible):
        raise ValueError("singleton cap")
    if promotions:
        p = promotions[0]; check_keys(p, PROMOTION_KEYS)
        if p["family"] != "B1" or p["target_signature"] != f["unique_mode_signature"] or p["target_prime_count"] != f["prime_mode_count"] or p["target_composite_count"] != f["target_composite_count"] or p["mixed_class_count"] != f["mixed_class_count"] or p["positive_class_count"] != f["positive_class_count"] or p["aggregate_enrichment_numerator"] != f["aggregate_enrichment_numerator"]:
            raise ValueError("promotion content")
        for k in PROMOTION_KEYS[1:]: exact_int(p[k], low=None if k == "aggregate_enrichment_numerator" else 0)
    return True


def canonical(o):
    validate_payload(o)
    data = (json.dumps(o, sort_keys=True, indent=2, ensure_ascii=True, allow_nan=False)+"\n").encode("utf-8")
    if json.loads(data) != o or not data.isascii() or data.endswith(b"\n\n"):
        raise ValueError("noncanonical serializer")
    return data


def run(output, code_commit, plan=None, *, phase="D19", entry="direct",
        low_generator=base_sieve, high_generator=segment_flags):
    # No prime-generating function may be reached before *all* validation.
    if plan is None: plan = positive_plan()
    validate_plan(plan, phase, entry=entry)
    if type(code_commit) is not str or len(code_commit) != 40 or any(c not in "0123456789abcdef" for c in code_commit):
        raise ValueError("invalid pinned commit")
    validate_plan(plan, phase, entry=entry)
    if low_generator is not base_sieve or high_generator is not segment_flags:
        raise ValueError("indirect prime helper forbidden")
    small = low_generator(plan[0]["stop"])
    validate_plan(plan, phase, entry=entry)
    flags = high_generator(plan[1]["start"], plan[1]["stop"], small)
    payload = summarize(flags, plan, code_commit)
    data = canonical(payload)
    Path(output).write_bytes(data)
    return len(data)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--band", required=True, choices=("D19",))
    parser.add_argument("--code-commit", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    run(args.output, args.code_commit, phase=args.band)


if __name__ == "__main__":
    main()
