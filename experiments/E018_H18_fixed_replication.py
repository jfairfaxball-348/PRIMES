"""D1-54, fixed-target-only E018 H18 evaluator. No discovery or reserve access."""
from __future__ import annotations

import argparse
import json
from itertools import combinations
from math import gcd, isqrt
from pathlib import Path

WIDTH = 1_000_000
LOW, HIGH = 97_000_000, 98_000_000
RESIDUES = tuple(a for a in range(210) if gcd(a, 210) == 1)
MATRIX = ((1, 1, 1), (1, 0, 0), (0, 1, 0))
SEED = (2, 1, 1)
EARLY = (
    ("D0", 0), ("H0", 1), ("S1", 2), ("S2", 4), ("S3", 8),
    ("A0-retired", 10), ("S4", 16), ("S5", 32), ("D3", 35),
    ("D4", 39), ("D6", 42), ("H6", 44), ("D7", 46), ("H7", 48),
    ("D8", 50), ("D9", 54), ("H9", 56), ("D10", 58), ("H10", 60),
    ("D11", 62), ("H11", 64), ("D12", 67), ("A1", 33), ("H3", 37),
    ("H4", 41), ("H8", 52), ("A8", 66), ("H12", 69), ("A3", 70),
    ("A4", 78), ("A6", 84), ("A7", 92), ("A9", 108),
    ("A10", 116), ("A11", 124), ("A12", 134),
    ("G3-pre", 34), ("G3-post", 36), ("G4-pre", 38), ("G4-mid", 40),
    ("G6-mid", 43), ("G7-pre", 45), ("G7-mid", 47),
    ("G8-pre", 49), ("G8-mid", 51), ("G9-pre", 53), ("G9-mid", 55),
    ("G10-pre", 57), ("G10-mid", 59), ("G11-pre", 61), ("G11-mid", 63),
    ("G12-pre", 65), ("G12-mid", 68),
)
LATE = (
    ("G13-pre", 71), ("D13", 72), ("G13-mid", 73), ("H13", 74), ("A13", 144),
    ("G14-pre", 75), ("D14", 76), ("G14-mid", 77), ("H14", 79), ("A14", 152),
    ("G15-pre", 80), ("D15", 81), ("G15-mid", 82), ("H15", 83), ("A15", 162),
    ("G16-pre", 85), ("D16", 86), ("G16-mid", 87), ("H16", 88), ("A16", 172),
    ("G17-pre", 89), ("D17", 90), ("G17-mid", 91), ("H17", 93), ("A17", 180),
)
CAL_STARTS = (128_000_000, 256_000_000, 512_000_000,
              1_024_000_000, 2_048_000_000, 4_096_000_000)
CAL_WIDTHS = (4096, 16384, 65536, 262144, 1048576)
HISTORY = tuple((n, x*WIDTH, (x+1)*WIDTH) for n, x in EARLY+LATE) + tuple(
    (f"E005-max-{i+1}", s, s+CAL_WIDTHS[-1])
    for i, s in enumerate(CAL_STARTS)
)
NESTED = tuple((f"E005-{i+1}-{w}", s, s+w)
               for i, s in enumerate(CAL_STARTS) for w in CAL_WIDTHS)
ROLES = (("G18-pre", 94_000_000, 95_000_000),
         ("D18", 95_000_000, 96_000_000),
         ("G18-mid", 96_000_000, 97_000_000),
         ("H18", LOW, HIGH), ("A18", 190_000_000, 191_000_000))
ROLE_LABELS = ("non-target guard", "discovery", "non-target guard",
               "one-shot holdout", "independently locked adversarial reserve")
PLAN = ({"purpose": "base_sieve_support", "start": 0, "stop": 9900,
         "strategy": "whole_prefix"},
        {"purpose": "segmented_target", "start": LOW, "stop": HIGH,
         "strategy": "direct_segmented"})
VALIDATION_KEYS = (
    "plan_failure_count", "domain_partition_failure_count",
    "tiling_recurrence_failure_count", "transfer_matrix_failure_count",
    "residue_bin_failure_count", "support_identity_failure_count",
    "class_label_failure_count", "frequency_mode_failure_count",
    "gate_duplicate_failure_count", "serializer_failure_count",
)
PARAMS = {
    "width": WIDTH, "wheel": 210, "residues_R210": list(RESIDUES),
    "tile_lengths": [1, 2, 3], "tiling_seed": list(SEED),
    "transfer_matrix": [list(z) for z in MATRIX],
    "remainder_modulus": "anchor", "residue_bin_counts": [4, 8],
    "population_floor": 1000, "class_floor": 10, "occurrence_floor": 32,
    "mixed_class_floor": 36, "positive_class_floor": 30,
    "strict_global_enrichment": True,
}
FAMILY_KEYS = (
    "family", "prime_mode_count", "highest_competing_count", "strict_unique_prime_mode",
    "unique_mode_signature", "target_composite_count", "population_floor_passed",
    "class_floor_passed", "occurrence_floor_passed", "mixed_class_count",
    "mixed_class_floor_passed", "positive_class_count", "positive_class_floor_passed",
    "aggregate_enrichment_numerator", "aggregate_enrichment_positive",
    "mechanically_eligible",
)
PROMO_KEYS = ("family", "target_signature", "target_prime_count", "target_composite_count",
              "mixed_class_count", "positive_class_count", "aggregate_enrichment_numerator")


def intersects(left, right):
    return left[1] < right[2] and right[1] < left[2]


def interval_audit():
    """Independent named provenance audit, never queries primes or anchors."""
    assert len(EARLY) == 53 and len(LATE) == 25 and len(HISTORY) == 84
    assert len(NESTED) == 30 and len(ROLES) == 5
    named = HISTORY+ROLES+NESTED
    assert len({v[0] for v in named}) == len(named)
    assert all(a < b for _, a, b in named)
    old = list(combinations(HISTORY, 2))
    new = [(r, h) for r in ROLES for h in HISTORY] + list(combinations(ROLES, 2))
    assert (len(old), len(new)) == (3486, 430)
    assert not any(intersects(a, b) for a, b in old+new)
    for _, a, b in NESTED:
        assert sum(1 for _, c, d in HISTORY if c <= a < b <= d) == 1
    assert len(ROLES)*len(NESTED) == 150
    assert not any(intersects(a, b) for a in ROLES for b in NESTED)
    assert all(a % WIDTH == 0 and b-a == WIDTH for _, a, b in ROLES)
    assert ROLES[-1][1] == 2*ROLES[1][1]
    k = isqrt(HIGH-1)
    assert k == 9899 and k*k <= HIGH-1 < (k+1)*(k+1)
    return 3486, 430, 30, 150


def checked_plan(phase, entries):
    """Check entire positive typed plan, not just a high-band exclusion list."""
    if phase != "H18" or type(entries) not in (list, tuple) or len(entries) != 2:
        raise ValueError("complete H18-only plan required")
    for item, reference in zip(entries, PLAN):
        if type(item) is not dict or set(item) != set(reference):
            raise ValueError("plan entry missing/extra/indirect fields")
        if any(type(item[key]) is not type(reference[key]) or item[key] != reference[key]
               for key in reference):
            raise ValueError("off-positive-allowlist plan")
    assert isqrt(HIGH-1) == 9899
    if entries[0]["stop"] != isqrt(entries[1]["stop"]-1)+1:
        raise ValueError("base prefix does not match exact integer root")
    forbidden = HISTORY+NESTED+tuple(r for r in ROLES if r[0] != "H18")
    if any(intersects(("H18", entries[1]["start"], entries[1]["stop"]), r)
           for r in forbidden):
        raise ValueError("high segment intersects protected role")
    return True


def _base(stop):
    if type(stop) is not int or stop != 9900:
        raise ValueError("wrong base limit")
    ok = bytearray(b"\x01")*stop
    ok[0:2] = b"\x00\x00"
    for p in range(2, isqrt(stop-1)+1):
        if ok[p]:
            for j in range(p*p, stop, p):
                ok[j] = 0
    return tuple(i for i, v in enumerate(ok) if v)


def _segment(first, last, base):
    if type(first) is not int or type(last) is not int or (first, last) != (LOW, HIGH):
        raise ValueError("wrong high segment")
    good = bytearray(b"\x01")*(last-first)
    for p in base:
        beginning = max(p*p, ((first+p-1)//p)*p)
        for q in range(beginning, last, p):
            good[q-first] = 0
    return {first+j for j, flag in enumerate(good) if flag}


def run_plan(phase, plan, base_fn=_base, segment_fn=_segment):
    interval_audit()
    checked_plan(phase, plan)  # entire plan BEFORE either generator
    checked_plan(phase, plan)  # base boundary
    small_primes = base_fn(plan[0]["stop"])
    checked_plan(phase, plan)  # high boundary
    return segment_fn(plan[1]["start"], plan[1]["stop"], small_primes)


def product(a, b, modulus):
    return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(3)) % modulus
                       for j in range(3)) for i in range(3))


def tiling_mod(n):
    if type(n) is not int or n < 1:
        raise ValueError("positive integral self modulus required")
    result = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    power = tuple(tuple(v % n for v in row) for row in MATRIX)
    steps = n
    while steps:
        if steps & 1:
            result = product(result, power, n)
        power = product(power, power, n)
        steps //= 2
    return sum(result[2][j]*SEED[j] for j in range(3)) % n


def bins(n, remainder):
    if (type(n) is not int or n <= 1 or type(remainder) is not int
            or not 0 <= remainder < n):
        raise ValueError("bad canonical tiling remainder")
    one, two = 4*remainder//n, 8*remainder//n
    assert 0 <= one < 4 and 0 <= two < 8 and one == two//2
    return one, two


def difference(tp, total_c, tc, total_p):
    if any(type(z) is not int or z < 0 for z in (tp, total_c, tc, total_p)):
        raise ValueError("signed counts must be exact nonnegative integers")
    if tp > total_p or tc > total_c:
        raise ValueError("target count exceeds population")
    return tp*total_c-tc*total_p


def mix(tp, np, tc, nc):
    return 0 < tp < np and 0 < tc < nc


def retain(supports):
    """Only zero target per family. Exact integer sets, L1 before L2, cap 2."""
    if type(supports) not in (list, tuple) or len(supports) > 2:
        raise ValueError("too many candidates")
    output = []
    for j, (name, target, support) in enumerate(supports):
        if (name != ("L1" if j == 0 else "L2") and
            not (len(supports) == 1 and name in ("L1", "L2"))):
            raise ValueError("noncanonical family ordering")
        if (target != 0 or type(target) is not int or type(support) is not set or
                any(type(v) is not int for v in support)):
            raise ValueError("nonfixed/invalid exact support")
        if all(support != prior[2] for prior in output):
            output.append((name, target, support))
    return output


def _keys(record, expected):
    if type(record) is not dict or set(record) != set(expected):
        raise ValueError("unknown/missing keys")


def _ints(xs, length):
    return type(xs) is list and len(xs) == length and all(type(a) is int and a >= 0 for a in xs)


def check_schema(p):
    """Frozen ten-key/nested-type/forbidden-data verifier; no loose maps."""
    _keys(p, ("experiment", "implementation_commit", "band", "partition", "parameters",
              "generation_plan", "anchor_summary", "validation", "families", "promotions"))
    if type(p["experiment"]) is not str or p["experiment"] != "E018":
        raise ValueError("wrong experiment")
    h = p["implementation_commit"]
    if type(h) is not str or len(h) != 40 or any(c not in "0123456789abcdef" for c in h):
        raise ValueError("bad implementation commit")
    _keys(p["band"], ("name", "range", "interval_semantics"))
    if (p["band"] != {"name": "H18", "range": [LOW, HIGH],
                      "interval_semantics": "half-open"} or
            not _ints(p["band"]["range"], 2)):
        raise ValueError("wrong band")
    if type(p["partition"]) is not list or len(p["partition"]) != 5:
        raise ValueError("bad partition")
    for item, (name, a, b), role in zip(p["partition"], ROLES, ROLE_LABELS):
        _keys(item, ("name", "range", "role"))
        if item != {"name": name, "range": [a, b], "role": role} or not _ints(item["range"], 2):
            raise ValueError("wrong partition role")
    _keys(p["parameters"], PARAMS)
    if p["parameters"] != PARAMS or any(type(p["parameters"][k]) is not type(v)
                                          for k, v in PARAMS.items()):
        raise ValueError("changed parameters")
    for key, n in (("residues_R210", 48), ("tile_lengths", 3), ("tiling_seed", 3),
                   ("residue_bin_counts", 2)):
        if not _ints(p["parameters"][key], n):
            raise ValueError("invalid nested parameter int")
    if not all(_ints(z, 3) for z in p["parameters"]["transfer_matrix"]):
        raise ValueError("invalid matrix")
    checked_plan("H18", p["generation_plan"])
    _keys(p["anchor_summary"], ("wheel_anchor_count", "prime_count", "composite_count",
                                "prime_counts_by_R210", "composite_counts_by_R210"))
    a = p["anchor_summary"]
    if (any(type(a[k]) is not int or a[k] < 0 for k in
            ("wheel_anchor_count", "prime_count", "composite_count")) or
            not _ints(a["prime_counts_by_R210"], 48) or
            not _ints(a["composite_counts_by_R210"], 48) or
            sum(a["prime_counts_by_R210"]) != a["prime_count"] or
            sum(a["composite_counts_by_R210"]) != a["composite_count"] or
            a["prime_count"]+a["composite_count"] != a["wheel_anchor_count"]):
        raise ValueError("unconserved population")
    _keys(p["validation"], VALIDATION_KEYS)
    if any(type(z) is not int or z != 0 for z in p["validation"].values()):
        raise ValueError("validation nonzero or ill-typed")
    if type(p["families"]) is not list or len(p["families"]) != 2:
        raise ValueError("two frozen families required")
    flags = ("strict_unique_prime_mode", "population_floor_passed", "class_floor_passed",
             "occurrence_floor_passed", "mixed_class_floor_passed", "positive_class_floor_passed",
             "aggregate_enrichment_positive", "mechanically_eligible")
    nullable = ("unique_mode_signature", "target_composite_count", "mixed_class_count",
                "positive_class_count", "aggregate_enrichment_numerator")
    for item, name in zip(p["families"], ("L1", "L2")):
        _keys(item, FAMILY_KEYS)
        if item["family"] != name or type(item["family"]) is not str:
            raise ValueError("family order")
        if any(type(item[k]) is not bool for k in flags):
            raise ValueError("ill-typed boolean")
        if any(type(item[k]) is not int or item[k] < 0 for k in
               ("prime_mode_count", "highest_competing_count")):
            raise ValueError("ill-typed counts")
        if item["strict_unique_prime_mode"]:
            if type(item["unique_mode_signature"]) is not int or item["unique_mode_signature"] != 0:
                raise ValueError("non-frozen target")
            if any(type(item[k]) is not int or item[k] < 0 for k in nullable[1:4]):
                raise ValueError("bad count field")
            if type(item["aggregate_enrichment_numerator"]) is not int:
                raise ValueError("bad enrichment")
            if item["mixed_class_count"] > 48 or item["positive_class_count"] > 48:
                raise ValueError("class overflow")
        elif any(item[k] is not None for k in nullable) or item["mechanically_eligible"]:
            raise ValueError("nonmode cannot retain target fallback")
    if type(p["promotions"]) is not list or len(p["promotions"]) > 2:
        raise ValueError("promotion list wrong")
    kept = []
    for record in p["promotions"]:
        _keys(record, PROMO_KEYS)
        if record["family"] not in ("L1", "L2") or type(record["family"]) is not str:
            raise ValueError("bad promotion family")
        f = p["families"][("L1", "L2").index(record["family"])]
        if not f["mechanically_eligible"] or record["family"] in kept:
            raise ValueError("unqualified/duplicate promotion")
        kept.append(record["family"])
        if (any(type(v) is not int for k, v in record.items() if k != "family") or
            record["target_signature"] != 0 or record["target_prime_count"] != f["prime_mode_count"] or
            record["target_composite_count"] != f["target_composite_count"] or
            record["mixed_class_count"] != f["mixed_class_count"] or
            record["positive_class_count"] != f["positive_class_count"] or
            record["aggregate_enrichment_numerator"] != f["aggregate_enrichment_numerator"]):
            raise ValueError("promotion mismatch")
    if kept != [f["family"] for f in p["families"] if f["mechanically_eligible"]]:
        raise ValueError("noncanonical promotion/eligibility")
    return True


def canonical(p):
    check_schema(p)
    raw = (json.dumps(p, sort_keys=True, indent=2, ensure_ascii=True)+"\n").encode("utf-8")
    if json.loads(raw) != p or not raw.endswith(b"\n") or raw.endswith(b"\n\n"):
        raise ValueError("canonical failure")
    return raw


def reference_checks():
    def enumerate_tiles(n):
        if n == 0:
            return [()]
        return [(k,)+tail for k in (1, 2, 3) if k <= n for tail in enumerate_tiles(n-k)]
    v = [2, 1, 1]
    table = [1, 1, 2]
    for _ in range(64):
        table.append(sum(table[-3:]))
    for n in range(0, 10):
        assert len(enumerate_tiles(n)) == table[n]
    for n in range(1, 40):
        v = [sum(v), v[0], v[1]]
        assert v == [table[n+2], table[n+1], table[n]]
        assert tiling_mod(n) == table[n] % n


def fixed_zero_gate(name, freq_p, freq_c, pop_p, pop_c, class_p, class_c, support):
    """Synthetic-testable unchanged H18 verdict for one frozen zero signature."""
    domain = 4 if name == "L1" else 8 if name == "L2" else None
    if domain is None or any(len(a) != domain for a in (freq_p, freq_c)):
        raise ValueError("full unchanged family domain required")
    if any(type(v) is not int or v < 0 for a in (freq_p, freq_c) for v in a):
        raise ValueError("invalid signature frequency")
    if not all(type(a) is list and len(a) == 48 and all(type(v) is int and v >= 0 for v in a)
               for a in (pop_p, pop_c, class_p, class_c)):
        raise ValueError("missing wheel strata")
    if sum(freq_p) != sum(pop_p) or sum(freq_c) != sum(pop_c):
        raise ValueError("unconserved complete frequency domain")
    if sum(class_p) != freq_p[0] or sum(class_c) != freq_c[0]:
        raise ValueError("target class/frequency disagreement")
    if type(support) is not set or any(type(v) is not int for v in support) or len(support) != freq_p[0]:
        raise ValueError("exact support discrepancy")
    np0 = freq_p[0]
    competitor = max(freq_p[1:])
    unique = np0 > competitor
    nprime, ncomp = sum(pop_p), sum(pop_c)
    floors = nprime >= 1000 and ncomp >= 1000
    class_floors = all(min(pop_p[k], pop_c[k]) >= 10 for k in range(48))
    if unique:
        nc0 = freq_c[0]
        mixed = sum(mix(class_p[k], pop_p[k], class_c[k], pop_c[k]) for k in range(48))
        positives = sum(difference(class_p[k], pop_c[k], class_c[k], pop_p[k]) > 0
                        for k in range(48))
        whole = difference(np0, ncomp, nc0, nprime)
        eligible = floors and class_floors and np0 >= 32 and mixed >= 36 and positives >= 30 and whole > 0
    else:
        nc0 = mixed = positives = whole = None
        eligible = False
    return {
        "family": name, "prime_mode_count": np0,
        "highest_competing_count": competitor, "strict_unique_prime_mode": unique,
        "unique_mode_signature": 0 if unique else None,
        "target_composite_count": nc0, "population_floor_passed": floors,
        "class_floor_passed": class_floors, "occurrence_floor_passed": unique and np0 >= 32,
        "mixed_class_count": mixed, "mixed_class_floor_passed": unique and mixed >= 36,
        "positive_class_count": positives,
        "positive_class_floor_passed": unique and positives >= 30,
        "aggregate_enrichment_numerator": whole,
        "aggregate_enrichment_positive": unique and whole > 0,
        "mechanically_eligible": eligible,
    }


def evaluate(commit, primes):
    """Full label-blind domain, only frozen L1/L2 signature ZERO evaluated as targets."""
    reference_checks()
    if type(primes) is not set or any(type(p) is not int or not LOW <= p < HIGH for p in primes):
        raise ValueError("non-H18 prime label source")
    rid = {r: i for i, r in enumerate(RESIDUES)}
    assert len(rid) == 48 and tuple(i for i in range(210) if gcd(i, 210) == 1) == RESIDUES
    populations = [[0]*48 for _ in range(2)]
    frequencies = [[[0]*d for _ in range(2)] for d in (4, 8)]
    target_by_class = [[[0]*48 for _ in range(2)] for _ in range(2)]
    prime_support = [set(), set()]
    anchors = 0
    for x in range(LOW, HIGH):
        position = rid.get(x % 210)
        if position is None:
            continue
        label = int(x in primes)
        r = tiling_mod(x)
        quarter, eighth = bins(x, r)
        populations[label][position] += 1
        anchors += 1
        for j, b in enumerate((quarter, eighth)):
            frequencies[j][label][b] += 1
            if b == 0:
                target_by_class[j][label][position] += 1
                if label:
                    prime_support[j].add(x)
    nprime, ncomp = sum(populations[1]), sum(populations[0])
    assert nprime+ncomp == anchors
    assert anchors == sum(1 for x in range(LOW, HIGH) if x % 210 in rid)
    assert all(sum(frequencies[j][lab]) == sum(populations[lab]) for j in (0, 1) for lab in (0, 1))
    family_rows = []
    candidates = []
    for j, name in enumerate(("L1", "L2")):
        f = fixed_zero_gate(name, frequencies[j][1], frequencies[j][0],
                            populations[1], populations[0],
                            target_by_class[j][1], target_by_class[j][0], prime_support[j])
        family_rows.append(f)
        if f["mechanically_eligible"]:
            candidates.append((name, 0, prime_support[j]))
        f["mechanically_eligible"] = False  # set again after exact cross-family dedup
    surviving = retain(candidates)
    promos = []
    for family, _, _ in surviving:
        f = family_rows[("L1", "L2").index(family)]
        f["mechanically_eligible"] = True
        promos.append({
            "family": family, "target_signature": 0,
            "target_prime_count": f["prime_mode_count"],
            "target_composite_count": f["target_composite_count"],
            "mixed_class_count": f["mixed_class_count"],
            "positive_class_count": f["positive_class_count"],
            "aggregate_enrichment_numerator": f["aggregate_enrichment_numerator"],
        })
    result = {
        "experiment": "E018", "implementation_commit": commit,
        "band": {"name": "H18", "range": [LOW, HIGH], "interval_semantics": "half-open"},
        "partition": [{"name": n, "range": [a, b], "role": role}
                      for (n, a, b), role in zip(ROLES, ROLE_LABELS)],
        "parameters": PARAMS,
        "generation_plan": [dict(x) for x in PLAN],
        "anchor_summary": {"wheel_anchor_count": anchors, "prime_count": nprime,
                           "composite_count": ncomp,
                           "prime_counts_by_R210": populations[1],
                           "composite_counts_by_R210": populations[0]},
        "validation": {name: 0 for name in VALIDATION_KEYS},
        "families": family_rows, "promotions": promos,
    }
    canonical(result)
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description="E018 one-shot fixed 0/0 H18 replication")
    parser.add_argument("--phase", required=True, choices=("H18",))
    parser.add_argument("--implementation-commit", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    if args.output != "research/evidence/E018_H18_replication.json":
        parser.error("off-pinned aggregate-only output path")
    if (len(args.implementation_commit) != 40 or any(c not in "0123456789abcdef"
                                                     for c in args.implementation_commit)):
        parser.error("invalid implementation commit")
    interval_audit()
    primes = run_plan(args.phase, [dict(p) for p in PLAN])
    result = evaluate(args.implementation_commit, primes)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(canonical(result))


if __name__ == "__main__":
    main()
