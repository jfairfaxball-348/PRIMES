"""E022: frozen proper-cycle-colouring R1, D22-only aggregate discovery."""
from __future__ import annotations

import argparse
import json
from itertools import product
from math import gcd, isqrt
from pathlib import Path

from primes_lab.core import sieve

Q = 210
R210 = (1, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67,
        71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 121, 127, 131,
        137, 139, 143, 149, 151, 157, 163, 167, 169, 173, 179, 181, 187,
        191, 193, 197, 199, 209)
SIGNATURES = (0, 1, 2)
ROLES = (
    ("G22-pre", 154000000, 156000000, "guard"),
    ("D22", 156000000, 158000000, "discovery"),
    ("G22-mid", 158000000, 160000000, "guard"),
    ("H22", 160000000, 162000000, "holdout"),
    ("A22", 312000000, 314000000, "adversarial"),
)
PLAN = (
    ("base_sieve_support", 0, 12570, "whole_prefix"),
    ("segmented_target", 156000000, 158000000, "direct_segmented"),
)
EARLY = """
D0 0 1
H0 1 2
S1 2 3
S2 4 5
S3 8 9
A0 10 11
S4 16 17
S5 32 33
D3 35 36
D4 39 40
D6 42 43
H6 44 45
D7 46 47
H7 48 49
D8 50 51
D9 54 55
H9 56 57
D10 58 59
H10 60 61
D11 62 63
H11 64 65
D12 67 68
A1 33 34
H3 37 38
H4 41 42
H8 52 53
A8 66 67
H12 69 70
A3 70 71
A4 78 79
A6 84 85
A7 92 93
A9 108 109
A10 116 117
A11 124 125
A12 134 135
G3-pre 34 35
G3-post 36 37
G4-pre 38 39
G4-mid 40 41
G6-mid 43 44
G7-pre 45 46
G7-mid 47 48
G8-pre 49 50
G8-mid 51 52
G9-pre 53 54
G9-mid 55 56
G10-pre 57 58
G10-mid 59 60
G11-pre 61 62
G11-mid 63 64
G12-pre 65 66
G12-mid 68 69
"""
FIVE_ROLE = (
    ("E013", ((71, 72), (72, 73), (73, 74), (74, 75), (144, 145))),
    ("E014", ((75, 76), (76, 77), (77, 78), (79, 80), (152, 153))),
    ("E015", ((80, 81), (81, 82), (82, 83), (83, 84), (162, 163))),
    ("E016", ((85, 86), (86, 87), (87, 88), (88, 89), (172, 173))),
    ("E017", ((89, 90), (90, 91), (91, 92), (93, 94), (180, 181))),
    ("E018", ((94, 95), (95, 96), (96, 97), (97, 98), (190, 191))),
    ("E019", ((98, 99), (99, 100), (100, 101), (101, 102), (198, 199))),
    ("E020", ((102, 103), (103, 104), (104, 105), (105, 106), (206, 207))),
    ("E021", ((136, 138), (138, 140), (140, 142), (142, 144), (276, 278))),
)
E005_STARTS = (128000000, 256000000, 512000000, 1024000000, 2048000000, 4096000000)
E005_WIDTHS = (4096, 16384, 65536, 262144, 1048576)
VALIDATORS = (
    "plan_failure_count", "interval_exclusion_failure_count",
    "cycle_definition_failure_count", "chromatic_count_failure_count",
    "remainder_order_failure_count", "wheel_label_failure_count",
    "frequency_conservation_failure_count", "signed_control_failure_count",
    "mode_duplicate_failure_count", "serializer_failure_count",
)
TOP = {"experiment", "implementation_commit", "band", "partition", "parameters",
       "generation_plan", "anchor_summary", "validation", "families", "promotions"}
PARAMETERS = dict(
    width=2000000, wheel=210, residues_R210=list(R210), palette_sizes=[3, 4],
    cycle_definition="simple-closed-labelled-vertices",
    colouring_constraint="adjacent-distinct", colour_labels="distinct",
    count_formula="(q-1)^x+(q-1)*(-1)^x", modulus="anchor_plus_one",
    feature="three_way_canonical_remainder_order", signature_domain=[0, 1, 2],
    selector="strict_unique_prime_frequency_mode", population_floor=2000,
    class_floor=20, occurrence_floor=64, mixed_class_floor=36,
    positive_class_floor=30, full_mixed_required=True,
)
FAMILY_FIELDS = {
    "family", "prime_mode_count", "highest_competing_prime_count",
    "strict_unique_prime_mode", "candidate_signature", "evaluated_signature",
    "target_prime_count", "target_composite_count", "population_floor_passed",
    "class_floor_passed", "occurrence_floor_passed", "mixed_class_count",
    "mixed_class_floor_passed", "positive_class_count",
    "positive_class_floor_passed", "target_enrichment_numerator",
    "target_enrichment_positive", "mechanically_eligible",
}
PROMO_FIELDS = {"family", "target_signature", "target_prime_count",
                "target_composite_count", "mixed_class_count",
                "positive_class_count", "target_enrichment_numerator"}


def overlap(a, b):
    return a[0] < b[1] and b[0] < a[1]


def old_intervals():
    early = []
    for line in EARLY.strip().splitlines():
        name, a, b = line.split()
        early.append((name, int(a) * 1000000, int(b) * 1000000))
    blocks = [(f"{exp}-{role}", a * 1000000, b * 1000000)
              for exp, rows in FIVE_ROLE
              for role, (a, b) in zip(("G-pre", "D", "G-mid", "H", "A"), rows, strict=True)]
    maximums = [(f"E005-{i}", s, s + E005_WIDTHS[-1])
                for i, s in enumerate(E005_STARTS)]
    return early + blocks + maximums


def audit_intervals():
    old = old_intervals()
    newer = [(name, a, b) for name, a, b, _ in ROLES]
    nested = [(s, s + w) for s in E005_STARTS for w in E005_WIDTHS]
    if len(old) != 104 or len({a for a, _, _ in old}) != 104 or len(nested) != 30:
        raise ValueError("incomplete old role inventory")
    if len(newer) != 5 or len({a for a, _, _ in newer}) != 5:
        raise ValueError("invalid E022 inventory")
    if any(a >= b for _, a, b in old + newer):
        raise ValueError("invalid interval")
    count = dict(old_old=0, new_old=0, new_new=0, new_nested=0,
                 old_non_e005_nested=0, nested_contained=0, nested_within=0,
                 nested_across=0)
    for i, (_, a, b) in enumerate(old):
        for _, c, d in old[i + 1:]:
            if overlap((a, b), (c, d)):
                raise ValueError("old roles overlap")
            count["old_old"] += 1
    for _, a, b in newer:
        for _, c, d in old:
            if overlap((a, b), (c, d)):
                raise ValueError("new/old role collision")
            count["new_old"] += 1
    for i, (_, a, b) in enumerate(newer):
        for _, c, d in newer[i + 1:]:
            if overlap((a, b), (c, d)):
                raise ValueError("new/new collision")
            count["new_new"] += 1
    for _, a, b in newer:
        for c, d in nested:
            if overlap((a, b), (c, d)):
                raise ValueError("new/nested collision")
            count["new_nested"] += 1
    for name, a, b in old:
        if name.startswith("E005-"):
            continue
        for c, d in nested:
            if overlap((a, b), (c, d)):
                raise ValueError("old/nested collision")
            count["old_non_e005_nested"] += 1
    for s in E005_STARTS:
        for w in E005_WIDTHS:
            if not (s <= s and s + w <= s + E005_WIDTHS[-1]):
                raise ValueError("nested not contained")
            count["nested_contained"] += 1
    for i, (a, b) in enumerate(nested):
        for c, d in nested[i + 1:]:
            if a == c:
                if not overlap((a, b), (c, d)):
                    raise ValueError("lost mandatory nesting")
                count["nested_within"] += 1
            else:
                if overlap((a, b), (c, d)):
                    raise ValueError("nested maxima collision")
                count["nested_across"] += 1
    named = sorted(old + newer, key=lambda row: row[1])
    if any(named[i][2] > named[i + 1][1] for i in range(len(named) - 1)):
        raise ValueError("named sorted disjointness failure")
    expected = dict(old_old=5356, new_old=520, new_new=10, new_nested=150,
                    old_non_e005_nested=2940, nested_contained=30,
                    nested_within=60, nested_across=375)
    if count != expected:
        raise ValueError("audit counts do not match frozen inventory")
    # Check exact first valid aligned guard start without sampling primes.
    for g in range(144000000, 154000000, 2000000):
        proposals = ((g, g + 2000000), (g + 2000000, g + 4000000),
                     (g + 4000000, g + 6000000), (g + 6000000, g + 8000000),
                     (2 * (g + 2000000), 2 * (g + 2000000) + 2000000))
        if not any(overlap(band, (a, b)) for band in proposals for _, a, b in old):
            raise ValueError("skipped earlier free allocation")
    if isqrt(158000000 - 1) + 1 != 12570:
        raise ValueError("low support arithmetic drift")
    return count


def proper_count_direct(n, q):
    if n < 3 or q not in (3, 4):
        raise ValueError("invalid cycle")
    return sum(all(word[i] != word[(i + 1) % n] for i in range(n))
               for word in product(range(q), repeat=n))


def closed_walk_trace(n, q):
    # Independently count labelled closed walks; no closed-form power shortcut.
    total = 0
    for start in range(q):
        states = [0] * q
        states[start] = 1
        for _ in range(n):
            states = [sum(states[j] for j in range(q) if j != k)
                      for k in range(q)]
        total += states[start]
    return total


def colour_remainder(x, q):
    if type(x) is not int or x < 3 or q not in (3, 4) or type(q) is not int:
        raise ValueError("invalid cycle or palette")
    m = x + 1
    correction = (q - 1) if x % 2 == 0 else -(q - 1)
    return (pow(q - 1, x, m) + correction) % m


def signature_from_remainders(x, a, b):
    if any(type(v) is not int for v in (x, a, b)) or x < 3:
        raise ValueError("bad remainder input")
    if not (0 <= a < x + 1 and 0 <= b < x + 1):
        raise ValueError("noncanonical remainder")
    return 0 if a < b else (1 if a == b else 2)


def signature(x):
    return signature_from_remainders(x, colour_remainder(x, 3),
                                     colour_remainder(x, 4))


def mode(counts):
    if len(counts) != 3 or any(type(v) is not int or v < 0 for v in counts):
        raise ValueError("invalid mode counts")
    ordering = sorted(counts, reverse=True)
    winner = counts.index(ordering[0]) if ordering[0] > ordering[1] else None
    return winner, ordering[0], ordering[1]


def dedup_support(support, prior):
    if type(support) is not set or any(type(v) is not int for v in support):
        raise ValueError("support must be an integer set")
    if any(support == previous for previous in prior):
        return False
    if prior:
        return False
    prior.append(set(support))
    return True


def synthetic_failures():
    """Independent bounded synthetic conventions, no primality/high-band data."""
    cycle_errors = 0
    count_errors = 0
    order_errors = 0
    for n in (3, 4, 5, 6):
        for q in (3, 4):
            direct = proper_count_direct(n, q)
            trace = closed_walk_trace(n, q)
            formula = (q - 1) ** n + ((q - 1) if n % 2 == 0 else -(q - 1))
            cycle_errors += int(direct != trace)
            count_errors += int(trace != formula)
            count_errors += int(colour_remainder(n, q) != direct % (n + 1))
    for n in range(3, 20):
        a = colour_remainder(n, 3)
        b = colour_remainder(n, 4)
        exact_a = (2 ** n + (2 if n % 2 == 0 else -2)) % (n + 1)
        exact_b = (3 ** n + (3 if n % 2 == 0 else -3)) % (n + 1)
        order_errors += int((a, b) != (exact_a, exact_b))
        order_errors += int(signature(n) != (0 if exact_a < exact_b else
                                            (1 if exact_a == exact_b else 2)))
    for n in (3, 4, 12):
        for a, b in ((0, 0), (0, n), (n, 0), (n, n)):
            expected = 0 if a < b else (1 if a == b else 2)
            order_errors += int(signature_from_remainders(n, a, b) != expected)
    return cycle_errors, count_errors, order_errors


def triviality_clear():
    """Prime-label-free necessary check: no parity or fixed Q210 class forces R1.

    K3=2^x+2(-1)^x and K4=3^x+3(-1)^x count labelled adjacent-
    unequal cyclic maps; neither is the E021 unlabelled block-partition
    object. Sharing integer powers does not make these finite sets
    equivalent. We do not infer originality or prime significance.
    """
    signatures_by_class = {r: set() for r in R210}
    for x in range(3, 5000):
        if gcd(x, 210) == 1:
            signatures_by_class[x % 210].add(signature(x))
    # Each fixed wheel class has at least two distinct outputs with all x odd.
    return all(len(s) >= 2 for s in signatures_by_class.values())


def plan_dicts(plan=PLAN):
    return [dict(purpose=p, start=a, stop=b, strategy=s) for p, a, b, s in plan]


class GeneratorGate:
    def __init__(self, plan=PLAN, phase="D22", *, indirect=False, per_anchor=False):
        if phase != "D22" or indirect or per_anchor:
            raise ValueError("unauthorised phase or indirect prime generator")
        if type(plan) is not tuple or len(plan) != 2 or any(type(e) is not tuple for e in plan):
            raise ValueError("generator call list must be exact")
        for got, expected in zip(plan, PLAN, strict=True):
            if len(got) != 4 or any(type(a) is not type(b) or a != b
                                    for a, b in zip(got, expected, strict=True)):
                raise ValueError("invalid complete generator plan")
        audit_intervals()
        self.plan = plan
        self.phase = phase
        self.next_entry = 0

    def enter(self, index, *entry):
        if index != self.next_entry or index not in (0, 1) or tuple(entry) != PLAN[index]:
            raise ValueError("unexpected generator entry/order")
        if self.phase != "D22" or self.plan != PLAN:
            raise ValueError("phase/plan altered")
        audit_intervals()
        if index == 1:
            for _, a, b in old_intervals():
                if overlap((entry[1], entry[2]), (a, b)):
                    raise ValueError("target collides with old role")
            for s in E005_STARTS:
                for w in E005_WIDTHS:
                    if overlap((entry[1], entry[2]), (s, s + w)):
                        raise ValueError("target collides with calibration")
            for name, a, b, _ in ROLES:
                if name != "D22" and overlap((entry[1], entry[2]), (a, b)):
                    raise ValueError("off-phase new role")
        self.next_entry += 1

    def finished(self):
        if self.next_entry != 2:
            raise ValueError("generator incomplete")


def base_sieve(stop):
    # Only generator entry zero can call this; stop is exclusive.
    return sieve(stop - 1)


def target_segment(start, stop, low_primes):
    # Direct segmented sieve over exactly [start, stop), never a high prefix.
    marks = bytearray(b"\x01") * (stop - start)
    for p in low_primes:
        first = max(p * p, ((start + p - 1) // p) * p)
        if first < stop:
            marks[first - start:stop - start:p] = b"\x00" * (
                ((stop - 1 - first) // p) + 1
            )
    return marks


def compute_tables(marks):
    L, U = 156000000, 158000000
    if len(marks) != U - L:
        raise ValueError("segment width drift")
    idx = {r: i for i, r in enumerate(R210)}
    p = [[0] * 48 for _ in SIGNATURES]
    c = [[0] * 48 for _ in SIGNATURES]
    supports = [set() for _ in SIGNATURES]
    wheel_total = 0
    for x in range(L, U):
        r = x % Q
        if r not in idx:
            continue
        wheel_total += 1
        t = signature(x)  # Computed before any label inspection.
        prime = bool(marks[x - L])
        if prime:
            p[t][idx[r]] += 1
            supports[t].add(x)
        else:
            c[t][idx[r]] += 1
    return p, c, supports, wheel_total


def aggregate(p, c, supports, wheel_total, marks, commit):
    np_t = [sum(row) for row in p]
    nc_t = [sum(row) for row in c]
    p_r = [sum(p[t][r] for t in SIGNATURES) for r in range(48)]
    c_r = [sum(c[t][r] for t in SIGNATURES) for r in range(48)]
    np = sum(np_t)
    nc = sum(nc_t)
    candidate, highest, competing = mode(np_t)
    evaluated = candidate  # D22 only. H22 never runs in this module.
    population_ok = np >= 2000 and nc >= 2000
    class_ok = all(a >= 20 and b >= 20 for a, b in zip(p_r, c_r, strict=True))
    t_prime = sum(p[evaluated]) if evaluated is not None else None
    t_comp = sum(c[evaluated]) if evaluated is not None else None
    occurs = evaluated is not None and t_prime >= 64
    if evaluated is not None:
        mixed = sum(
            p[evaluated][r] > 0 and p_r[r] - p[evaluated][r] > 0
            and c[evaluated][r] > 0 and c_r[r] - c[evaluated][r] > 0
            for r in range(48)
        )
        positive_classes = sum(
            p[evaluated][r] * c_r[r] - c[evaluated][r] * p_r[r] > 0
            for r in range(48)
        )
        enrichment = t_prime * nc - t_comp * np
    else:
        mixed = None
        positive_classes = None
        enrichment = None

    cycle_errors, chromatic_errors, order_errors = synthetic_failures()
    wheel_errors = int(tuple(r for r in range(210) if gcd(r, 210) == 1) != R210)
    wheel_errors += int(sum(1 for x in range(156000000, 158000000)
                            if gcd(x, 210) == 1) != wheel_total)
    wheel_errors += int(np + nc != wheel_total)
    frequency_errors = int(np != sum(p_r) or nc != sum(c_r))
    frequency_errors += sum(
        int(sum(p[t]) != np_t[t] or sum(c[t]) != nc_t[t]) for t in SIGNATURES
    )
    frequency_errors += int(sum(np_t) != np or sum(nc_t) != nc)
    # Independent re-derivation from cell loops, checking signed arithmetic
    # and all four strictly positive mixed-cell requirements.
    signed_errors = 0
    if evaluated is not None:
        signed_errors += int(
            enrichment != np_t[evaluated] * sum(nc_t)
            - nc_t[evaluated] * sum(np_t)
        )
        independently_positive = 0
        independently_mixed = 0
        for r in range(48):
            pr = p[evaluated][r]
            cr = c[evaluated][r]
            other_p = sum(p[t][r] for t in SIGNATURES if t != evaluated)
            other_c = sum(c[t][r] for t in SIGNATURES if t != evaluated)
            independently_positive += int(pr * (cr + other_c)
                                          - cr * (pr + other_p) > 0)
            independently_mixed += int(min(pr, cr, other_p, other_c) > 0)
        signed_errors += int(independently_positive != positive_classes)
        signed_errors += int(independently_mixed != mixed)
    mode_errors = int(mode([3, 3, 1]) != (None, 3, 3))
    mode_errors += int(mode([1, 4, 2]) != (1, 4, 2))
    checked = []
    mode_errors += int(not dedup_support({3, 5}, checked))
    mode_errors += int(dedup_support({5, 3}, checked))
    mode_errors += int(dedup_support({3, 7}, checked))
    mode_errors += int(len(checked) != 1)
    mode_errors += int(candidate is not None and len(supports[candidate]) != t_prime)
    exclusion_errors = 0
    try:
        audit_intervals()
    except ValueError:
        exclusion_errors += 1
    gate_errors = 0
    try:
        GeneratorGate()
    except ValueError:
        gate_errors += 1
    validation = dict(zip(VALIDATORS, (
        gate_errors, exclusion_errors, cycle_errors, chromatic_errors, order_errors,
        wheel_errors, frequency_errors, signed_errors, mode_errors, 0
    ), strict=True))
    trivial = triviality_clear()
    eligible = bool(
        evaluated is not None and population_ok and class_ok and occurs
        and mixed >= 36 and positive_classes >= 30 and enrichment > 0
        and trivial and not any(validation.values())
    )
    # No serialized supports or proxy hashes; duplicate by exact set equality.
    accepted = []
    if eligible and not dedup_support(supports[evaluated], accepted):
        eligible = False
    if len(accepted) > 1:
        raise ValueError("support cap breached")

    family = dict(
        family="R1", prime_mode_count=highest, highest_competing_prime_count=competing,
        strict_unique_prime_mode=candidate is not None,
        candidate_signature=candidate, evaluated_signature=evaluated,
        target_prime_count=t_prime, target_composite_count=t_comp,
        population_floor_passed=population_ok, class_floor_passed=class_ok,
        occurrence_floor_passed=bool(occurs), mixed_class_count=mixed,
        mixed_class_floor_passed=bool(mixed is not None and mixed >= 36),
        positive_class_count=positive_classes,
        positive_class_floor_passed=bool(positive_classes is not None
                                         and positive_classes >= 30),
        target_enrichment_numerator=enrichment,
        target_enrichment_positive=bool(enrichment is not None and enrichment > 0),
        mechanically_eligible=eligible,
    )
    promo = []
    if eligible:
        promo = [dict(
            family="R1", target_signature=evaluated, target_prime_count=t_prime,
            target_composite_count=t_comp, mixed_class_count=mixed,
            positive_class_count=positive_classes,
            target_enrichment_numerator=enrichment,
        )]
    payload = dict(
        experiment="E022", implementation_commit=commit,
        band=dict(name="D22", range=[156000000, 158000000],
                  interval_semantics="half-open"),
        partition=[dict(name=n, range=[a, b], role=role) for n, a, b, role in ROLES],
        parameters=PARAMETERS, generation_plan=plan_dicts(),
        anchor_summary=dict(
            wheel_anchor_count=wheel_total, prime_count=np, composite_count=nc,
            prime_counts_by_R210=p_r, composite_counts_by_R210=c_r,
        ), validation=validation, families=[family], promotions=promo,
    )
    # The first eight zero counters have independent mathematical derivations;
    # the ninth includes exact set equality. Check the tenth by an independent
    # strict typed tree inspection plus canonical whole-byte parse round trip.
    wire = canonical(payload)
    if not validate_payload(payload) or canonical(json.loads(wire)) != wire:
        raise ValueError("serializer or aggregate validator failed")
    return wire


def canonical(payload):
    return (json.dumps(payload, sort_keys=True, indent=2, ensure_ascii=True)
            + "\n").encode("ascii")


def _strict_equal(a, b):
    if type(a) is not type(b):
        return False
    if type(a) is dict:
        return set(a) == set(b) and all(_strict_equal(a[k], b[k]) for k in b)
    if type(a) is list:
        return len(a) == len(b) and all(_strict_equal(x, y)
                                        for x, y in zip(a, b, strict=True))
    return a == b


def _is_int(v, nonnegative=False):
    return type(v) is int and (not nonnegative or v >= 0)


def _int_list(v, length, *, nonnegative=False):
    return type(v) is list and len(v) == length and all(
        _is_int(z, nonnegative) for z in v
    )


def validate_payload(obj):
    """Strict exact recursive JSON contract, forbidding every extra field."""
    if type(obj) is not dict or set(obj) != TOP:
        return False
    if obj["experiment"] != "E022":
        return False
    sha = obj["implementation_commit"]
    if type(sha) is not str or len(sha) != 40 or any(z not in "0123456789abcdef" for z in sha):
        return False
    band = obj["band"]
    if type(band) is not dict or set(band) != {"name", "range", "interval_semantics"}:
        return False
    if not _strict_equal(band, dict(name="D22", range=[156000000, 158000000],
                                      interval_semantics="half-open")):
        return False
    partition = obj["partition"]
    if type(partition) is not list or len(partition) != 5:
        return False
    if any(type(item) is not dict or set(item) != {"name", "range", "role"}
           or not _strict_equal(item, dict(name=n, range=[a, b], role=role))
           for item, (n, a, b, role) in zip(partition, ROLES, strict=True)):
        return False
    params = obj["parameters"]
    if type(params) is not dict or set(params) != set(PARAMETERS):
        return False
    if any(not _strict_equal(params[k], v) for k, v in PARAMETERS.items()):
        return False
    plan = obj["generation_plan"]
    if type(plan) is not list or len(plan) != 2 or any(
        type(item) is not dict or set(item) != {"purpose", "start", "stop", "strategy"}
        or not _strict_equal(item, expected)
        or any(type(item[k]) is not type(expected[k]) for k in expected)
        for item, expected in zip(plan, plan_dicts(), strict=True)
    ):
        return False
    a = obj["anchor_summary"]
    if type(a) is not dict or set(a) != {
        "wheel_anchor_count", "prime_count", "composite_count",
        "prime_counts_by_R210", "composite_counts_by_R210"
    }:
        return False
    if any(not _is_int(a[k], True)
           for k in ("wheel_anchor_count", "prime_count", "composite_count")):
        return False
    if not (_int_list(a["prime_counts_by_R210"], 48, nonnegative=True)
            and _int_list(a["composite_counts_by_R210"], 48, nonnegative=True)):
        return False
    if not (a["wheel_anchor_count"] == a["prime_count"] + a["composite_count"]
            and a["prime_count"] == sum(a["prime_counts_by_R210"])
            and a["composite_count"] == sum(a["composite_counts_by_R210"])):
        return False
    v = obj["validation"]
    if type(v) is not dict or set(v) != set(VALIDATORS):
        return False
    if any(not _is_int(v[k], True) or v[k] != 0 for k in VALIDATORS):
        return False
    fs = obj["families"]
    if type(fs) is not list or len(fs) != 1 or type(fs[0]) is not dict:
        return False
    f = fs[0]
    if set(f) != FAMILY_FIELDS or f["family"] != "R1":
        return False
    integers = ("prime_mode_count", "highest_competing_prime_count",
                "mixed_class_count", "positive_class_count", "target_prime_count",
                "target_composite_count", "target_enrichment_numerator")
    signed_nullable = {"target_enrichment_numerator"}
    for k in integers:
        if f[k] is not None and not _is_int(f[k], k not in signed_nullable):
            return False
    if not _is_int(f["prime_mode_count"], True) or not _is_int(
        f["highest_competing_prime_count"], True
    ):
        return False
    if f["prime_mode_count"] < f["highest_competing_prime_count"]:
        return False
    bools = (
        "strict_unique_prime_mode", "population_floor_passed", "class_floor_passed",
        "occurrence_floor_passed", "mixed_class_floor_passed",
        "positive_class_floor_passed", "target_enrichment_positive",
        "mechanically_eligible"
    )
    if any(type(f[k]) is not bool for k in bools):
        return False
    candidate = f["candidate_signature"]
    target = f["evaluated_signature"]
    if candidate is not None and not (_is_int(candidate) and candidate in SIGNATURES):
        return False
    if target != candidate or f["strict_unique_prime_mode"] != (candidate is not None):
        return False
    if f["strict_unique_prime_mode"] != (
        f["prime_mode_count"] > f["highest_competing_prime_count"]
    ):
        return False
    target_fields = ("target_prime_count", "target_composite_count", "mixed_class_count",
                     "positive_class_count", "target_enrichment_numerator")
    if target is None:
        if any(f[k] is not None for k in target_fields):
            return False
        if any(f[k] for k in ("occurrence_floor_passed", "mixed_class_floor_passed",
                             "positive_class_floor_passed",
                             "target_enrichment_positive", "mechanically_eligible")):
            return False
    else:
        if any(f[k] is None for k in target_fields):
            return False
        if (f["target_prime_count"] != f["prime_mode_count"]
            or f["occurrence_floor_passed"] != (f["target_prime_count"] >= 64)
            or f["mixed_class_floor_passed"] != (f["mixed_class_count"] >= 36)
            or f["positive_class_floor_passed"] != (f["positive_class_count"] >= 30)
            or f["target_enrichment_positive"] != (f["target_enrichment_numerator"] > 0)):
            return False
        if not (0 <= f["mixed_class_count"] <= 48
                and 0 <= f["positive_class_count"] <= 48):
            return False
    if f["population_floor_passed"] != (a["prime_count"] >= 2000
                                       and a["composite_count"] >= 2000):
        return False
    if f["class_floor_passed"] != all(
        p >= 20 and c >= 20 for p, c in zip(
            a["prime_counts_by_R210"], a["composite_counts_by_R210"], strict=True
        )
    ):
        return False
    necessary = (f["strict_unique_prime_mode"] and f["population_floor_passed"]
                 and f["class_floor_passed"] and f["occurrence_floor_passed"]
                 and f["mixed_class_floor_passed"]
                 and f["positive_class_floor_passed"]
                 and f["target_enrichment_positive"])
    if f["mechanically_eligible"] and not necessary:
        return False
    promos = obj["promotions"]
    if type(promos) is not list or len(promos) > 1:
        return False
    if bool(promos) != f["mechanically_eligible"]:
        return False
    if promos:
        p = promos[0]
        if type(p) is not dict or set(p) != PROMO_FIELDS:
            return False
        if p != {
            "family": "R1", "target_signature": target,
            "target_prime_count": f["target_prime_count"],
            "target_composite_count": f["target_composite_count"],
            "mixed_class_count": f["mixed_class_count"],
            "positive_class_count": f["positive_class_count"],
            "target_enrichment_numerator": f["target_enrichment_numerator"],
        }:
            return False
    return True


def run(commit, output):
    if type(commit) is not str or len(commit) != 40 or any(
        s not in "0123456789abcdef" for s in commit
    ):
        raise ValueError("source commit SHA required")
    gate = GeneratorGate()  # Entire plan / metadata verified before first sieve.
    gate.enter(0, *PLAN[0])
    low = base_sieve(12570)
    gate.enter(1, *PLAN[1])
    flags = target_segment(156000000, 158000000, low)
    gate.finished()
    p, c, supports, wheel_total = compute_tables(flags)
    raw = aggregate(p, c, supports, wheel_total, flags, commit)
    # Absolutely no alternate output, raw per-anchor traces or support hashes.
    Path(output).write_bytes(raw)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--band", required=True, choices=("D22",))
    parser.add_argument("--code-commit", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    if args.band != "D22":
        raise ValueError("only D22 is permitted")
    run(args.code_commit, args.output)


if __name__ == "__main__":
    main()
