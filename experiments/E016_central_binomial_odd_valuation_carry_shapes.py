"""E016 frozen D16-only source-independent odd factorial-valuation evaluator.

No generation or primality queries at module import. All high generation is direct
segmented D16 after the exact entire two-entry positive plan is validated.
"""
import argparse
import itertools
import json
from collections import Counter
from math import gcd, isqrt
from pathlib import Path

R210 = tuple(r for r in range(210) if gcd(r, 210) == 1)
BASES = (3, 5, 7)
ROLES = (
    ("G16-pre", 85_000_000, 86_000_000, "guard"),
    ("D16", 86_000_000, 87_000_000, "discovery"),
    ("G16-mid", 87_000_000, 88_000_000, "guard"),
    ("H16", 88_000_000, 89_000_000, "holdout"),
    ("A16", 172_000_000, 173_000_000, "adversarial"),
)
D16_PLAN = (
    ("base_sieve_support", 0, 9328, "whole_prefix"),
    ("segmented_target", 86_000_000, 87_000_000, "segmented"),
)
# Only integer-role provenance, never historical prime-derived outcomes.
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
    ("G13-pre", 71), ("D13", 72), ("G13-mid", 73),
    ("H13", 74), ("A13", 144),
    ("G14-pre", 75), ("D14", 76), ("G14-mid", 77),
    ("H14", 79), ("A14", 152),
    ("G15-pre", 80), ("D15", 81), ("G15-mid", 82),
    ("H15", 83), ("A15", 162),
)
CALIBRATION_STARTS = (
    128_000_000, 256_000_000, 512_000_000,
    1_024_000_000, 2_048_000_000, 4_096_000_000,
)
WIDTHS = (4096, 16384, 65536, 262144, 1048576)
VALIDATION_KEYS = (
    "plan_failure_count", "domain_partition_failure_count",
    "factorial_valuation_failure_count", "digit_carry_identity_failure_count",
    "cap_signature_failure_count", "support_identity_failure_count",
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
DOMAINS = (tuple(range(13)), tuple(range(4)), tuple(itertools.product(range(5), repeat=3)))
NAMES = ("T1", "T2", "T3")
PARAMETERS = dict(width=1_000_000, wheel=210, residues_R210=list(R210),
                  valuation_bases=list(BASES), valuation_cap=4,
                  population_floor=1000, class_floor=10, occurrence_floor=32,
                  mixed_class_floor=36, positive_class_floor=30,
                  strict_global_enrichment=True)


def interval_overlap(a, b):
    return a[1] < b[2] and b[1] < a[2]


def historical_intervals():
    if len(EARLY_ROLES) != 53 or len(LATER_ROLES) != 15:
        raise ValueError("immutable role inventory cardinality")
    old = [(name, m * 1_000_000, (m + 1) * 1_000_000)
           for name, m in EARLY_ROLES + LATER_ROLES]
    old += [(f"E005-{i}", a, a + 1048576)
            for i, a in enumerate(CALIBRATION_STARTS)]
    if len(old) != 74 or len({e[0] for e in old}) != 74:
        raise ValueError("74 unique exclusions required")
    return old


def audit_partition():
    old = historical_intervals()
    recent = [(n, a, b) for n, a, b, _ in ROLES]
    if any(b - a != 1_000_000 for _, a, b in recent):
        raise ValueError("frozen role width")
    pairs = [(a, b) for a in recent for b in old]
    pairs += [(recent[i], recent[j]) for i in range(5) for j in range(i + 1, 5)]
    if len(pairs) != 380 or any(interval_overlap(a, b) for a, b in pairs):
        raise ValueError("380 interval metadata audit failed")
    nested = [(f"E005-{i}-{w}", a, a + w, i) for i, a in enumerate(CALIBRATION_STARTS) for w in WIDTHS]
    if len(nested) != 30 or any(not (old[68 + i][1] <= a and b <= old[68 + i][2])
                                    for _, a, b, i in nested):
        raise ValueError("30 calibration containment audit failed")
    cross = [(a, b) for a in recent for b in nested]
    if len(cross) != 150 or any(interval_overlap(a, b) for a, b in cross):
        raise ValueError("150 nested interval audit failed")
    if ROLES[4][1] != 2 * ROLES[1][1]:
        raise ValueError("A16 convention")
    return 380, 30, 150


def expected_plan():
    return [dict(zip(("purpose", "start", "stop", "strategy"), t)) for t in D16_PLAN]


def validate_plan(phase, plan):
    if phase != "D16" or type(plan) is not list or len(plan) != 2:
        raise ValueError("D16 phase and full two-entry plan required")
    for entry in plan:
        if type(entry) is not dict or set(entry) != {"purpose", "start", "stop", "strategy"}:
            raise ValueError("malformed generator call")
        if type(entry["start"]) is not int or type(entry["stop"]) is not int or type(entry["purpose"]) is not str or type(entry["strategy"]) is not str:
            raise ValueError("noncanonical generator call types")
    if plan != expected_plan() or isqrt(plan[1]["stop"] - 1) + 1 != 9328:
        raise ValueError("positive allowlist denied")
    if audit_partition() != (380, 30, 150):
        raise ValueError("provenance audit failed")
    return True


def generator_entry(phase, plan, index, generate):
    validate_plan(phase, plan)  # Revalidate full two-entry allowlist at EACH boundary.
    if type(index) is not int or index not in (0, 1) or plan[index] != expected_plan()[index]:
        raise ValueError("generator entry order denied")
    return generate(plan[index])


def guarded_primes(phase, plan):
    validate_plan(phase, plan)  # Entire two-entry plan before first generation.
    base = generator_entry(phase, plan, 0, _generate)
    validate_plan(phase, plan)  # Recheck before second boundary.
    return generator_entry(phase, plan, 1, lambda e: _generate(e, base))


def _generate(entry, base=None):
    if entry == expected_plan()[0] and base is None:
        stop = 9328
        sieve = bytearray(b"\x01") * stop
        sieve[:2] = b"\x00\x00"
        for p in range(2, isqrt(stop - 1) + 1):
            if sieve[p]:
                sieve[p * p:stop:p] = b"\x00" * ((stop - 1 - p * p) // p + 1)
        return [i for i in range(stop) if sieve[i]]
    if entry == expected_plan()[1] and base is not None:
        start, stop = 86_000_000, 87_000_000
        sieve = bytearray(b"\x01") * (stop - start)
        for p in base:
            first = max(p * p, ((start + p - 1) // p) * p)
            if first < stop:
                sieve[first - start:stop - start:p] = b"\x00" * ((stop - 1 - first) // p + 1)
        return {start + i for i, flag in enumerate(sieve) if flag}
    raise ValueError("generator outside frozen allowlist")


def valuation(x, q):
    if type(x) is not int or x < 0 or q not in BASES:
        raise ValueError("Legendre input")
    power, total = q, 0
    while power <= 2 * x:
        term = (2 * x) // power - 2 * (x // power)
        if term not in (0, 1):
            raise ValueError("Legendre term outside 0/1")
        total += term
        power *= q
    return total


def carry_count(x, q):
    """Synthetic-only independent base-q x+x carry identity check."""
    if type(x) is not int or x < 0 or q not in BASES:
        raise ValueError("carry check input")
    a = x
    carry = total = 0
    while a or carry:
        digit = a % q
        carry = int(2 * digit + carry >= q)
        total += carry
        a //= q
    return total


def signatures(x):
    capped = tuple(min(4, valuation(x, q)) for q in BASES)
    if any(c not in range(5) for c in capped):
        raise ValueError("valuation cap")
    sig = (sum(capped), sum(c > 0 for c in capped), capped)
    if any(s not in DOMAINS[i] for i, s in enumerate(sig)):
        raise ValueError("signature domain/coarsening")
    return sig


def strict_mode(counts, domain):
    if set(counts) - set(domain):
        raise ValueError("unexpected signature")
    ordered = sorted(domain, key=lambda s: (-counts.get(s, 0), s))
    first, second = counts.get(ordered[0], 0), counts.get(ordered[1], 0)
    return (ordered[0] if first > second else None, first, second)


def exact_enrichment(npt, nct, np, nc):
    return npt * nc - nct * np


def class_metrics(sig, pb, cb, np_by, nc_by):
    if not (len(pb) == len(cb) == len(np_by) == len(nc_by) == 48):
        raise ValueError("48 classes compulsory")
    mixed = positive = 0
    for i in range(48):
        p, c = pb[i].get(sig, 0), cb[i].get(sig, 0)
        if all((p, np_by[i] - p, c, nc_by[i] - c)):
            mixed += 1
        if exact_enrichment(p, c, np_by[i], nc_by[i]) > 0:
            positive += 1
    return mixed, positive


def select_duplicates(eligible_supports):
    kept = []
    for name, anchors in eligible_supports:
        if type(anchors) is not set:
            raise ValueError("complete exact set required")
        if all(anchors != previous for _, previous in kept):
            kept.append((name, anchors))
    if len(kept) > 3:
        raise ValueError("three-promotion cap")
    return [name for name, _ in kept]


def summarize(p_counts, c_counts, p_by, c_by, np_by, nc_by, supports):
    if any(len(x) != 3 for x in (p_counts, c_counts, p_by, c_by, supports)):
        raise ValueError("three families required")
    np, nc = sum(np_by), sum(nc_by)
    if len(np_by) != 48 or len(nc_by) != 48:
        raise ValueError("missing wheel classes")
    if any(sum(p_counts[i].values()) != np or sum(c_counts[i].values()) != nc for i in range(3)):
        raise ValueError("global support identity")
    for i in range(3):
        if len(p_by[i]) != 48 or len(c_by[i]) != 48:
            raise ValueError("per-class population")
        if any(sum(p_by[i][r].values()) != np_by[r] or sum(c_by[i][r].values()) != nc_by[r] for r in range(48)):
            raise ValueError("per-class support identity")
        if any(p_counts[i].get(t, 0) != sum(p_by[i][r].get(t, 0) for r in range(48)) or c_counts[i].get(t, 0) != sum(c_by[i][r].get(t, 0) for r in range(48)) for t in DOMAINS[i]):
            raise ValueError("signature-class conservation")
        if set(p_counts[i]) - set(DOMAINS[i]) or set(c_counts[i]) - set(DOMAINS[i]):
            raise ValueError("domain violation")
    population_ok = np >= 1000 and nc >= 1000
    class_ok = all(p >= 10 and c >= 10 for p, c in zip(np_by, nc_by))
    families, precandidates = [], []
    for i, name in enumerate(NAMES):
        sig, npt, rival = strict_mode(p_counts[i], DOMAINS[i])
        unique = sig is not None
        nct = c_counts[i].get(sig, 0) if unique else None
        mix, positive = class_metrics(sig, p_by[i], c_by[i], np_by, nc_by) if unique else (None, None)
        enrichment = exact_enrichment(npt, nct, np, nc) if unique else None
        occurrence_ok = unique and npt >= 32
        mixed_ok = unique and mix >= 36
        positives_ok = unique and positive >= 30
        signed_ok = unique and enrichment > 0
        eligible = bool(population_ok and class_ok and occurrence_ok and mixed_ok and positives_ok and signed_ok)
        if eligible:
            anchors = supports[i].get(sig, set())
            if len(anchors) != npt:
                raise ValueError("complete prime-support-set identity")
            precandidates.append((name, anchors))
        families.append(dict(family=name, prime_mode_count=npt,
                             highest_competing_count=rival, strict_unique_prime_mode=unique,
                             unique_mode_signature=(list(sig) if i == 2 else sig) if unique else None,
                             target_composite_count=nct, population_floor_passed=population_ok,
                             class_floor_passed=class_ok, occurrence_floor_passed=bool(occurrence_ok),
                             mixed_class_count=mix, mixed_class_floor_passed=bool(mixed_ok),
                             positive_class_count=positive, positive_class_floor_passed=bool(positives_ok),
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
    validate_plan("D16", plan)
    if type(prime_set) is not set or any(type(p) is not int or not 86_000_000 <= p < 87_000_000 or gcd(p, 210) != 1 for p in prime_set):
        raise ValueError("non-D16/off-wheel prime labels")
    p_counts, c_counts = [Counter() for _ in range(3)], [Counter() for _ in range(3)]
    pb = [[Counter() for _ in range(48)] for _ in range(3)]
    cb = [[Counter() for _ in range(48)] for _ in range(3)]
    supports = [dict() for _ in range(3)]
    np_by, nc_by = [0] * 48, [0] * 48
    residue_index = {r: i for i, r in enumerate(R210)}
    for x in range(86_000_000, 87_000_000):
        r = residue_index.get(x % 210)
        if r is None:
            continue
        isprime = x in prime_set
        (np_by if isprime else nc_by)[r] += 1
        for i, sig in enumerate(signatures(x)):
            (p_counts if isprime else c_counts)[i][sig] += 1
            (pb if isprime else cb)[i][r][sig] += 1
            if isprime:
                supports[i].setdefault(sig, set()).add(x)
    np, nc = sum(np_by), sum(nc_by)
    wheel_count = sum(1 for x in range(86_000_000, 87_000_000) if x % 210 in residue_index)
    if np + nc != wheel_count or sum(len(s) for s in supports[2].values()) != np:
        raise ValueError("domain/label conservation")
    families, promotions = summarize(p_counts, c_counts, pb, cb, np_by, nc_by, supports)
    payload = dict(experiment="E016", implementation_commit=commit,
                   band=dict(name="D16", range=[86_000_000, 87_000_000], interval_semantics="half-open"),
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
    def keys(obj, required):
        if type(obj) is not dict or set(obj) != set(required):
            raise ValueError("noncanonical field allowlist")

    keys(payload, TOP_KEYS)
    if payload["experiment"] != "E016" or type(payload["implementation_commit"]) is not str or len(payload["implementation_commit"]) != 40 or any(c not in "0123456789abcdef" for c in payload["implementation_commit"]):
        raise ValueError("implementation identity")
    keys(payload["band"], ("name", "range", "interval_semantics"))
    if payload["band"] != dict(name="D16", range=[86_000_000, 87_000_000], interval_semantics="half-open"):
        raise ValueError("D16 band")
    if payload["partition"] != [dict(name=n, range=[a, b], role=role) for n, a, b, role in ROLES]:
        raise ValueError("partition")
    keys(payload["parameters"], PARAMETERS)
    if payload["parameters"] != PARAMETERS:
        raise ValueError("immutable parameters")
    validate_plan("D16", payload["generation_plan"])
    a = payload["anchor_summary"]
    keys(a, ("wheel_anchor_count", "prime_count", "composite_count", "prime_counts_by_R210", "composite_counts_by_R210"))
    for key in ("wheel_anchor_count", "prime_count", "composite_count"):
        if type(a[key]) is not int or a[key] < 0:
            raise ValueError("anchor counts")
    for key in ("prime_counts_by_R210", "composite_counts_by_R210"):
        v = a[key]
        if type(v) is not list or len(v) != 48 or any(type(n) is not int or n < 0 for n in v):
            raise ValueError("48 class counts")
    if (a["wheel_anchor_count"] != a["prime_count"] + a["composite_count"] or
        sum(a["prime_counts_by_R210"]) != a["prime_count"] or
        sum(a["composite_counts_by_R210"]) != a["composite_count"]):
        raise ValueError("population conservation")
    keys(payload["validation"], VALIDATION_KEYS)
    if any(type(v) is not int or v != 0 for v in payload["validation"].values()):
        raise ValueError("mandatory zero validators")
    fs = payload["families"]
    if type(fs) is not list or len(fs) != 3 or [row.get("family") for row in fs] != list(NAMES):
        raise ValueError("three ordered families")
    for i, f in enumerate(fs):
        keys(f, FAMILY_KEYS)
        for k in ("prime_mode_count", "highest_competing_count"):
            if type(f[k]) is not int or f[k] < 0:
                raise ValueError("mode frequency")
        for k in ("strict_unique_prime_mode", "population_floor_passed", "class_floor_passed", "occurrence_floor_passed", "mixed_class_floor_passed", "positive_class_floor_passed", "aggregate_enrichment_positive", "mechanically_eligible"):
            if type(f[k]) is not bool:
                raise ValueError("boolean flags")
        sig = f["unique_mode_signature"]
        if sig is None:
            if f["strict_unique_prime_mode"] or any(f[k] is not None for k in ("target_composite_count", "mixed_class_count", "positive_class_count", "aggregate_enrichment_numerator")):
                raise ValueError("tie must have null target fields")
            if any(f[k] for k in ("occurrence_floor_passed", "mixed_class_floor_passed", "positive_class_floor_passed", "aggregate_enrichment_positive", "mechanically_eligible")):
                raise ValueError("tie cannot be eligible")
        else:
            if i == 2 and (type(sig) is not list or len(sig) != 3 or any(type(k) is not int for k in sig)):
                raise ValueError("T3 signature")
            if i != 2 and type(sig) is not int:
                raise ValueError("integer target")
            canonical = tuple(sig) if i == 2 else sig
            if canonical not in DOMAINS[i] or not f["strict_unique_prime_mode"] or f["prime_mode_count"] <= f["highest_competing_count"]:
                raise ValueError("unique-mode domain/competitor")
            for k in ("target_composite_count", "mixed_class_count", "positive_class_count", "aggregate_enrichment_numerator"):
                if type(f[k]) is not int:
                    raise ValueError("target metric type")
            if not (0 <= f["mixed_class_count"] <= 48 and 0 <= f["positive_class_count"] <= 48 and f["target_composite_count"] >= 0):
                raise ValueError("target metric bounds")
            if f["occurrence_floor_passed"] != (f["prime_mode_count"] >= 32) or f["mixed_class_floor_passed"] != (f["mixed_class_count"] >= 36) or f["positive_class_floor_passed"] != (f["positive_class_count"] >= 30) or f["aggregate_enrichment_positive"] != (f["aggregate_enrichment_numerator"] > 0):
                raise ValueError("gate mismatch")
        if f["population_floor_passed"] != (a["prime_count"] >= 1000 and a["composite_count"] >= 1000) or f["class_floor_passed"] != all(p >= 10 and c >= 10 for p, c in zip(a["prime_counts_by_R210"], a["composite_counts_by_R210"])):
            raise ValueError("label floor mismatch")
        if f["mechanically_eligible"] and not all(f[k] for k in ("strict_unique_prime_mode", "population_floor_passed", "class_floor_passed", "occurrence_floor_passed", "mixed_class_floor_passed", "positive_class_floor_passed", "aggregate_enrichment_positive")):
            raise ValueError("ineligible promotion")
    ps = payload["promotions"]
    if type(ps) is not list or len(ps) > 3 or [p.get("family") for p in ps] != [f["family"] for f in fs if f["mechanically_eligible"]]:
        raise ValueError("promotion order")
    for p in ps:
        keys(p, PROMOTION_KEYS)
        f = next(f for f in fs if f["family"] == p["family"])
        if p != dict(family=p["family"], target_signature=f["unique_mode_signature"],
                     target_prime_count=f["prime_mode_count"],
                     target_composite_count=f["target_composite_count"],
                     mixed_class_count=f["mixed_class_count"],
                     positive_class_count=f["positive_class_count"],
                     aggregate_enrichment_numerator=f["aggregate_enrichment_numerator"]):
            raise ValueError("promotion inconsistent with family")
    return True


def serialize(payload):
    validate_schema(payload)
    return (json.dumps(payload, sort_keys=True, indent=2, ensure_ascii=True) + "\n").encode("utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", required=True, choices=("D16",))
    parser.add_argument("--implementation-commit", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    if args.phase != "D16" or len(args.implementation_commit) != 40 or any(c not in "0123456789abcdef" for c in args.implementation_commit):
        raise ValueError("nonfrozen command")
    plan = expected_plan()
    validate_plan(args.phase, plan)
    primes = guarded_primes(args.phase, plan)
    payload = evaluate(args.implementation_commit, primes, plan)
    Path(args.output).write_bytes(serialize(payload))


if __name__ == "__main__":
    main()
