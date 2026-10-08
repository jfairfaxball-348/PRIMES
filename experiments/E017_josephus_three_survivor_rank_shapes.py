"""Frozen E017 D17-only Josephus-three survivor rank experiment.

There are no prime computations on import. All generation follows the exact two-entry
positive D17 plan; all result fields are the narrow frozen aggregate schema.
"""
import argparse
import json
from collections import Counter
from math import gcd, isqrt
from pathlib import Path

R210 = tuple(r for r in range(210) if gcd(r, 210) == 1)
ROLES = (
    ("G17-pre", 89_000_000, 90_000_000, "guard"),
    ("D17", 90_000_000, 91_000_000, "discovery"),
    ("G17-mid", 91_000_000, 92_000_000, "guard"),
    ("H17", 93_000_000, 94_000_000, "holdout"),
    ("A17", 180_000_000, 181_000_000, "adversarial"),
)
D17_PLAN = (
    ("base_sieve_support", 0, 9540, "whole_prefix"),
    ("segmented_target", 90_000_000, 91_000_000, "direct_segmented"),
)
# Named integer-role provenance only; no historical experiment outputs.
EARLY_ROLES = (
    ("D0", 0), ("H0", 1), ("S1", 2), ("S2", 4), ("S3", 8),
    ("A0-contaminated", 10), ("S4", 16), ("S5", 32),
    ("D3", 35), ("D4", 39), ("D6", 42), ("H6", 44),
    ("D7", 46), ("H7", 48), ("D8", 50), ("D9", 54),
    ("H9", 56), ("D10", 58), ("H10", 60), ("D11", 62),
    ("H11", 64), ("D12", 67),
    ("A1", 33), ("H3", 37), ("H4", 41), ("H8", 52),
    ("A8", 66), ("H12", 69), ("A3", 70), ("A4", 78),
    ("A6", 84), ("A7", 92), ("A9", 108), ("A10", 116),
    ("A11", 124), ("A12", 134),
    ("G3-pre", 34), ("G3-post", 36), ("G4-pre", 38),
    ("G4-mid", 40), ("G6-mid", 43), ("G7-pre", 45),
    ("G7-mid", 47), ("G8-pre", 49), ("G8-mid", 51),
    ("G9-pre", 53), ("G9-mid", 55), ("G10-pre", 57),
    ("G10-mid", 59), ("G11-pre", 61), ("G11-mid", 63),
    ("G12-pre", 65), ("G12-mid", 68),
)
LATER_ROLES = (
    ("G13-pre", 71), ("D13", 72), ("G13-mid", 73), ("H13", 74), ("A13", 144),
    ("G14-pre", 75), ("D14", 76), ("G14-mid", 77), ("H14", 79), ("A14", 152),
    ("G15-pre", 80), ("D15", 81), ("G15-mid", 82), ("H15", 83), ("A15", 162),
    ("G16-pre", 85), ("D16", 86), ("G16-mid", 87), ("H16", 88), ("A16", 172),
)
CALIBRATION_STARTS = (128_000_000, 256_000_000, 512_000_000,
                      1_024_000_000, 2_048_000_000, 4_096_000_000)
WIDTHS = (4096, 16384, 65536, 262144, 1048576)
VALIDATION_KEYS = (
    "plan_failure_count", "domain_partition_failure_count",
    "josephus_recurrence_failure_count", "josephus_reference_failure_count",
    "survivor_signature_failure_count", "support_identity_failure_count",
    "class_label_failure_count", "frequency_mode_failure_count",
    "gate_duplicate_failure_count", "serializer_failure_count",
)
TOP_KEYS = {"experiment", "implementation_commit", "band", "partition",
            "parameters", "generation_plan", "anchor_summary", "validation",
            "families", "promotions"}
FAMILY_KEYS = {"family", "prime_mode_count", "highest_competing_count",
               "strict_unique_prime_mode", "unique_mode_signature", "target_composite_count",
               "population_floor_passed", "class_floor_passed", "occurrence_floor_passed",
               "mixed_class_count", "mixed_class_floor_passed", "positive_class_count",
               "positive_class_floor_passed", "aggregate_enrichment_numerator",
               "aggregate_enrichment_positive", "mechanically_eligible"}
PROMOTION_KEYS = {"family", "target_signature", "target_prime_count",
                  "target_composite_count", "mixed_class_count", "positive_class_count",
                  "aggregate_enrichment_numerator"}
DOMAINS = (tuple(range(4)), tuple(range(8)))
NAMES = ("J1", "J2")
PARAMETERS = dict(width=1_000_000, wheel=210, residues_R210=list(R210),
                  josephus_step=3, seat_index_base=0, survivor_bin_counts=[4, 8],
                  population_floor=1000, class_floor=10, occurrence_floor=32,
                  mixed_class_floor=36, positive_class_floor=30,
                  strict_global_enrichment=True)


def interval_overlap(a, b):
    return a[1] < b[2] and b[1] < a[2]


def historical_intervals():
    if len(EARLY_ROLES) != 53 or len(LATER_ROLES) != 20:
        raise ValueError("79-role provenance cannot be reconstructed")
    old = [(name, m * 1_000_000, (m + 1) * 1_000_000)
           for name, m in EARLY_ROLES + LATER_ROLES]
    old += [(f"E005-{i}", a, a + 1048576)
            for i, a in enumerate(CALIBRATION_STARTS)]
    if len(old) != 79 or len({e[0] for e in old}) != 79:
        raise ValueError("79 unique exclusions required")
    return old


def audit_partition():
    old = historical_intervals()
    new = [(n, a, b) for n, a, b, _ in ROLES]
    if any(b - a != 1_000_000 for _, a, b in new):
        raise ValueError("frozen role width")
    old_pairs = [(old[i], old[j]) for i in range(79) for j in range(i + 1, 79)]
    if len(old_pairs) != 3081 or any(interval_overlap(a, b) for a, b in old_pairs):
        raise ValueError("3081 historical-overlap checks failed")
    new_pairs = [(a, b) for a in new for b in old]
    new_pairs += [(new[i], new[j]) for i in range(5) for j in range(i + 1, 5)]
    if len(new_pairs) != 405 or any(interval_overlap(a, b) for a, b in new_pairs):
        raise ValueError("405 new-overlap checks failed")
    nested = [(a, a + w, i) for i, a in enumerate(CALIBRATION_STARTS) for w in WIDTHS]
    if len(nested) != 30 or any(not (old[73 + i][1] <= a and b <= old[73 + i][2])
                                    for a, b, i in nested):
        raise ValueError("30 E005 nested containment checks failed")
    cross = [(a, ("nested", b, c)) for a in new for b, c, _ in nested]
    if len(cross) != 150 or any(interval_overlap(a, b) for a, b in cross):
        raise ValueError("150 new-E005-nested overlaps")
    if ROLES[4][1] != 2 * ROLES[1][1] or isqrt(90_999_999) != 9539:
        raise ValueError("D17 root or A17 role convention")
    return 3081, 405, 30, 150


def expected_plan():
    return [dict(zip(("purpose", "start", "stop", "strategy"), t)) for t in D17_PLAN]


def validate_plan(phase, plan):
    if phase != "D17" or type(plan) is not list or len(plan) != 2:
        raise ValueError("D17 only, exactly two generator entries")
    for entry in plan:
        if type(entry) is not dict or set(entry) != {"purpose", "start", "stop", "strategy"}:
            raise ValueError("malformed generator entry")
        if (type(entry["start"]) is not int or type(entry["stop"]) is not int or
                type(entry["purpose"]) is not str or type(entry["strategy"]) is not str):
            raise ValueError("generator entry types")
    if (plan != expected_plan() or isqrt(plan[1]["stop"] - 1) + 1 != 9540 or
            not (9539 ** 2 <= plan[1]["stop"] - 1 < 9540 ** 2)):
        raise ValueError("positive generator allowlist violation")
    if audit_partition() != (3081, 405, 30, 150):
        raise ValueError("provenance protection audit")
    return True


def generator_entry(phase, plan, index, generate):
    validate_plan(phase, plan)
    if type(index) is not int or index not in (0, 1) or plan[index] != expected_plan()[index]:
        raise ValueError("wrong generator boundary")
    return generate(plan[index])


def _generate(entry, base=None):
    if entry == expected_plan()[0] and base is None:
        stop = 9540
        sieve = bytearray(b"\x01") * stop
        sieve[:2] = b"\x00\x00"
        for p in range(2, isqrt(stop - 1) + 1):
            if sieve[p]:
                sieve[p * p:stop:p] = b"\x00" * ((stop - 1 - p * p) // p + 1)
        return [p for p in range(stop) if sieve[p]]
    if entry == expected_plan()[1] and base is not None:
        start, stop = 90_000_000, 91_000_000
        sieve = bytearray(b"\x01") * (stop - start)
        for p in base:
            first = max(p * p, ((start + p - 1) // p) * p)
            if first < stop:
                sieve[first - start:stop - start:p] = b"\x00" * ((stop - 1 - first) // p + 1)
        return {start + i for i, flag in enumerate(sieve) if flag}
    raise ValueError("unapproved generator entry")


def guarded_primes(phase, plan):
    validate_plan(phase, plan)
    base = generator_entry(phase, plan, 0, _generate)
    validate_plan(phase, plan)
    return generator_entry(phase, plan, 1, lambda entry: _generate(entry, base))


def josephus_reference(n):
    """The exact defining recurrence; bounded synthetic n only."""
    if type(n) is not int or n < 1 or n > 4096:
        raise ValueError("reference only for small invented n")
    j = 0
    for m in range(2, n + 1):
        j = (j + 3) % m
    return j


def josephus_fast(n):
    if type(n) is not int or n < 1:
        raise ValueError("positive integer population required")
    if n == 1:
        return 0
    if n < 3:
        ans = (josephus_fast(n - 1) + 3) % n
    else:
        c, rem = divmod(n, 3)
        u = josephus_fast(n - c)
        v = u - rem
        ans = v + n if v < 0 else v + v // 2
    if not 0 <= ans < n:
        raise ValueError("survivor outside original seats")
    return ans


def signatures(n):
    j = josephus_fast(n)
    b4, b8 = 4 * j // n, 8 * j // n
    if j not in range(n) or b4 not in DOMAINS[0] or b8 not in DOMAINS[1] or b4 != b8 // 2:
        raise ValueError("survivor/coarsening invariant")
    return b4, b8


def strict_mode(counts, domain):
    if set(counts) - set(domain):
        raise ValueError("signature outside complete frozen domain")
    ordered = sorted(domain, key=lambda sig: (-counts.get(sig, 0), sig))
    highest, rival = counts.get(ordered[0], 0), counts.get(ordered[1], 0)
    return (ordered[0] if highest > rival else None, highest, rival)


def exact_enrichment(p, c, np, nc):
    return p * nc - c * np


def class_metrics(sig, p_by, c_by, np_by, nc_by):
    if not all(len(a) == 48 for a in (p_by, c_by, np_by, nc_by)):
        raise ValueError("every residue class required")
    mixed = positive = 0
    for i in range(48):
        p, c = p_by[i].get(sig, 0), c_by[i].get(sig, 0)
        if all((p > 0, np_by[i] - p > 0, c > 0, nc_by[i] - c > 0)):
            mixed += 1
        if exact_enrichment(p, c, np_by[i], nc_by[i]) > 0:
            positive += 1
    return mixed, positive


def select_duplicates(eligible_supports):
    retained = []
    for family, anchors in eligible_supports:
        if type(anchors) is not set:
            raise ValueError("exact original-anchor prime-support set required")
        if all(anchors != prior for _, prior in retained):
            retained.append((family, anchors))
    if len(retained) > 2:
        raise ValueError("two-family promotion cap")
    return [name for name, _ in retained]


def summarize(p_counts, c_counts, p_by, c_by, np_by, nc_by, supports):
    if not all(len(x) == 2 for x in (p_counts, c_counts, p_by, c_by, supports)):
        raise ValueError("exactly two family domains")
    if len(np_by) != 48 or len(nc_by) != 48:
        raise ValueError("48 exact wheel classes")
    np, nc = sum(np_by), sum(nc_by)
    for i in range(2):
        if len(p_by[i]) != 48 or len(c_by[i]) != 48:
            raise ValueError("missing class")
        if sum(p_counts[i].values()) != np or sum(c_counts[i].values()) != nc:
            raise ValueError("domain support not exhaustive")
        if any(sum(p_by[i][r].values()) != np_by[r] or sum(c_by[i][r].values()) != nc_by[r]
               for r in range(48)):
            raise ValueError("class support not exhaustive")
        if set(p_counts[i]) - set(DOMAINS[i]) or set(c_counts[i]) - set(DOMAINS[i]):
            raise ValueError("domain violation")
        if any(p_counts[i].get(t, 0) != sum(p_by[i][r].get(t, 0) for r in range(48)) or
               c_counts[i].get(t, 0) != sum(c_by[i][r].get(t, 0) for r in range(48))
               for t in DOMAINS[i]):
            raise ValueError("class-signature conservation")
        if set(supports[i]) - set(DOMAINS[i]) or any(len(v) != p_counts[i].get(t, 0)
                                                    for t, v in supports[i].items()):
            raise ValueError("full exact prime anchor sets required")
    population_ok = np >= 1000 and nc >= 1000
    class_ok = all(p >= 10 and c >= 10 for p, c in zip(np_by, nc_by))
    families, precandidates = [], []
    for i, name in enumerate(NAMES):
        sig, npt, rival = strict_mode(p_counts[i], DOMAINS[i])
        unique = sig is not None
        nct = c_counts[i].get(sig, 0) if unique else None
        mixed, positive = class_metrics(sig, p_by[i], c_by[i], np_by, nc_by) if unique else (None, None)
        enrichment = exact_enrichment(npt, nct, np, nc) if unique else None
        occurrence_ok = unique and npt >= 32
        mixed_ok = unique and mixed >= 36
        positive_ok = unique and positive >= 30
        signed_ok = unique and enrichment > 0
        eligible = bool(population_ok and class_ok and occurrence_ok and mixed_ok and positive_ok and signed_ok)
        if eligible:
            anchors = supports[i].get(sig, set())
            if len(anchors) != npt:
                raise ValueError("target full prime-support identity")
            precandidates.append((name, anchors))
        families.append(dict(family=name, prime_mode_count=npt,
                             highest_competing_count=rival, strict_unique_prime_mode=unique,
                             unique_mode_signature=sig, target_composite_count=nct,
                             population_floor_passed=population_ok, class_floor_passed=class_ok,
                             occurrence_floor_passed=bool(occurrence_ok), mixed_class_count=mixed,
                             mixed_class_floor_passed=bool(mixed_ok), positive_class_count=positive,
                             positive_class_floor_passed=bool(positive_ok),
                             aggregate_enrichment_numerator=enrichment,
                             aggregate_enrichment_positive=bool(signed_ok), mechanically_eligible=False))
    accepted = select_duplicates(precandidates)
    promotions = []
    for row in families:
        if row["family"] in accepted:
            row["mechanically_eligible"] = True
            promotions.append(dict(family=row["family"], target_signature=row["unique_mode_signature"],
                                   target_prime_count=row["prime_mode_count"],
                                   target_composite_count=row["target_composite_count"],
                                   mixed_class_count=row["mixed_class_count"],
                                   positive_class_count=row["positive_class_count"],
                                   aggregate_enrichment_numerator=row["aggregate_enrichment_numerator"]))
    return families, promotions


def evaluate(commit, prime_set, plan):
    validate_plan("D17", plan)
    if (type(prime_set) is not set or any(type(p) is not int or not 90_000_000 <= p < 91_000_000
                                           or gcd(p, 210) != 1 for p in prime_set)):
        raise ValueError("invalid segmented prime labels")
    p_counts, c_counts = [Counter() for _ in range(2)], [Counter() for _ in range(2)]
    p_by = [[Counter() for _ in range(48)] for _ in range(2)]
    c_by = [[Counter() for _ in range(48)] for _ in range(2)]
    supports = [dict() for _ in range(2)]
    np_by, nc_by = [0] * 48, [0] * 48
    residue_index = {r: i for i, r in enumerate(R210)}
    wheel_count = 0
    for x in range(90_000_000, 91_000_000):
        r = residue_index.get(x % 210)
        if r is None:
            continue
        wheel_count += 1
        prime = x in prime_set
        (np_by if prime else nc_by)[r] += 1
        for i, sig in enumerate(signatures(x)):
            (p_counts if prime else c_counts)[i][sig] += 1
            (p_by if prime else c_by)[i][r][sig] += 1
            if prime:
                supports[i].setdefault(sig, set()).add(x)
    np, nc = sum(np_by), sum(nc_by)
    if np + nc != wheel_count or sum(map(len, supports[0].values())) != np or sum(map(len, supports[1].values())) != np:
        raise ValueError("prime/composite wheel partition")
    families, promotions = summarize(p_counts, c_counts, p_by, c_by, np_by, nc_by, supports)
    payload = dict(experiment="E017", implementation_commit=commit,
                   band=dict(name="D17", range=[90_000_000, 91_000_000], interval_semantics="half-open"),
                   partition=[dict(name=n, range=[a, b], role=role) for n, a, b, role in ROLES],
                   parameters=PARAMETERS, generation_plan=plan,
                   anchor_summary=dict(wheel_anchor_count=wheel_count, prime_count=np,
                                       composite_count=nc, prime_counts_by_R210=np_by,
                                       composite_counts_by_R210=nc_by),
                   validation=dict.fromkeys(VALIDATION_KEYS, 0),
                   families=families, promotions=promotions)
    serialize(payload)
    return payload


def validate_schema(payload):
    def exactly(a, b):
        if type(a) is not type(b):
            return False
        if type(a) is dict:
            return a.keys() == b.keys() and all(exactly(a[k], b[k]) for k in a)
        if type(a) is list:
            return len(a) == len(b) and all(exactly(x, y) for x, y in zip(a, b))
        return a == b

    def keys(obj, required):
        if type(obj) is not dict or set(obj) != set(required):
            raise ValueError("forbidden/missing serializer fields")

    keys(payload, TOP_KEYS)
    if (payload["experiment"] != "E017" or type(payload["implementation_commit"]) is not str or
            len(payload["implementation_commit"]) != 40 or
            any(ch not in "0123456789abcdef" for ch in payload["implementation_commit"])):
        raise ValueError("wrong implementation commit")
    keys(payload["band"], ("name", "range", "interval_semantics"))
    if not exactly(payload["band"], dict(name="D17", range=[90_000_000, 91_000_000], interval_semantics="half-open")):
        raise ValueError("wrong discovery interval")
    if not exactly(payload["partition"],
                   [dict(name=n, range=[a, b], role=role) for n, a, b, role in ROLES]):
        raise ValueError("invalid 5-role partition")
    keys(payload["parameters"], PARAMETERS)
    if not exactly(payload["parameters"], PARAMETERS):
        raise ValueError("parameters changed")
    validate_plan("D17", payload["generation_plan"])
    a = payload["anchor_summary"]
    keys(a, ("wheel_anchor_count", "prime_count", "composite_count",
             "prime_counts_by_R210", "composite_counts_by_R210"))
    for k in ("wheel_anchor_count", "prime_count", "composite_count"):
        if type(a[k]) is not int or a[k] < 0:
            raise ValueError("anchor scalar type")
    for k in ("prime_counts_by_R210", "composite_counts_by_R210"):
        if type(a[k]) is not list or len(a[k]) != 48 or any(type(v) is not int or v < 0 for v in a[k]):
            raise ValueError("wheel count vector")
    if (a["prime_count"] + a["composite_count"] != a["wheel_anchor_count"] or
            sum(a["prime_counts_by_R210"]) != a["prime_count"] or
            sum(a["composite_counts_by_R210"]) != a["composite_count"]):
        raise ValueError("class-label conservation")
    keys(payload["validation"], VALIDATION_KEYS)
    if any(type(v) is not int or v != 0 for v in payload["validation"].values()):
        raise ValueError("nonzero/invalid mandatory validator")
    fs = payload["families"]
    if (type(fs) is not list or len(fs) != 2 or any(type(row) is not dict for row in fs)
            or [row.get("family") for row in fs] != list(NAMES)):
        raise ValueError("two ordered families")
    for i, f in enumerate(fs):
        keys(f, FAMILY_KEYS)
        for k in ("prime_mode_count", "highest_competing_count"):
            if type(f[k]) is not int or f[k] < 0:
                raise ValueError("mode frequencies")
        for k in ("strict_unique_prime_mode", "population_floor_passed", "class_floor_passed",
                  "occurrence_floor_passed", "mixed_class_floor_passed", "positive_class_floor_passed",
                  "aggregate_enrichment_positive", "mechanically_eligible"):
            if type(f[k]) is not bool:
                raise ValueError("boolean serializer field")
        sig = f["unique_mode_signature"]
        if sig is None:
            if f["strict_unique_prime_mode"] or any(f[k] is not None for k in (
                    "target_composite_count", "mixed_class_count", "positive_class_count",
                    "aggregate_enrichment_numerator")):
                raise ValueError("tie must have null target fields")
            if any(f[k] for k in ("occurrence_floor_passed", "mixed_class_floor_passed",
                                   "positive_class_floor_passed", "aggregate_enrichment_positive",
                                   "mechanically_eligible")):
                raise ValueError("no fallback from tie")
        else:
            if type(sig) is not int or sig not in DOMAINS[i] or not f["strict_unique_prime_mode"] or f["prime_mode_count"] <= f["highest_competing_count"]:
                raise ValueError("unique target semantics")
            for k in ("target_composite_count", "mixed_class_count", "positive_class_count",
                      "aggregate_enrichment_numerator"):
                if type(f[k]) is not int:
                    raise ValueError("target metric type")
            if (f["target_composite_count"] < 0 or not 0 <= f["mixed_class_count"] <= 48 or
                    not 0 <= f["positive_class_count"] <= 48):
                raise ValueError("target metrics range")
            if (f["occurrence_floor_passed"] != (f["prime_mode_count"] >= 32) or
                    f["mixed_class_floor_passed"] != (f["mixed_class_count"] >= 36) or
                    f["positive_class_floor_passed"] != (f["positive_class_count"] >= 30) or
                    f["aggregate_enrichment_positive"] != (f["aggregate_enrichment_numerator"] > 0)):
                raise ValueError("inconsistent target gates")
        if (f["population_floor_passed"] != (a["prime_count"] >= 1000 and a["composite_count"] >= 1000) or
                f["class_floor_passed"] != all(p >= 10 and c >= 10 for p, c in
                                                    zip(a["prime_counts_by_R210"], a["composite_counts_by_R210"]))):
            raise ValueError("inconsistent population gates")
        if f["mechanically_eligible"] and not all(f[k] for k in (
                "strict_unique_prime_mode", "population_floor_passed", "class_floor_passed",
                "occurrence_floor_passed", "mixed_class_floor_passed",
                "positive_class_floor_passed", "aggregate_enrichment_positive")):
            raise ValueError("invalid eligible family")
    ps = payload["promotions"]
    if (type(ps) is not list or len(ps) > 2 or any(type(p) is not dict for p in ps) or
            [p.get("family") for p in ps] != [f["family"] for f in fs if f["mechanically_eligible"]]):
        raise ValueError("promotions changed")
    for p in ps:
        keys(p, PROMOTION_KEYS)
        f = next(f for f in fs if f["family"] == p["family"])
        if not exactly(p, dict(family=p["family"], target_signature=f["unique_mode_signature"],
                     target_prime_count=f["prime_mode_count"], target_composite_count=f["target_composite_count"],
                     mixed_class_count=f["mixed_class_count"], positive_class_count=f["positive_class_count"],
                     aggregate_enrichment_numerator=f["aggregate_enrichment_numerator"])):
            raise ValueError("promotion metrics inconsistent")
    return True


def serialize(payload):
    validate_schema(payload)
    return (json.dumps(payload, sort_keys=True, indent=2, ensure_ascii=True) + "\n").encode("utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", required=True, choices=("D17",))
    parser.add_argument("--implementation-commit", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    if (args.phase != "D17" or len(args.implementation_commit) != 40 or
            any(ch not in "0123456789abcdef" for ch in args.implementation_commit)):
        raise ValueError("unfrozen D17 command")
    plan = expected_plan()
    validate_plan(args.phase, plan)
    primes = guarded_primes(args.phase, plan)
    payload = evaluate(args.implementation_commit, primes, plan)
    Path(args.output).write_bytes(serialize(payload))


if __name__ == "__main__":
    main()
