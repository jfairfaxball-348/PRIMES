"""E023: immutable distinct-summand triangular-shell P1; D23-only execution."""
from __future__ import annotations

import argparse
import json
from itertools import combinations
from math import gcd, isqrt
from pathlib import Path

from primes_lab.core import sieve

Q = 210
R210 = (1, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67,
        71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 121, 127, 131,
        137, 139, 143, 149, 151, 157, 163, 167, 169, 173, 179, 181, 187,
        191, 193, 197, 199, 209)
SIGNATURES = (
    (0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1), (0, 1, 2),
    (0, 2, 1), (1, 0, 0), (1, 0, 1), (1, 0, 2), (1, 1, 0),
    (1, 2, 0), (2, 0, 1), (2, 1, 0),
)
ROLES = (
    ("G23-pre", 164000000, 166000000, "guard"),
    ("D23", 166000000, 168000000, "discovery"),
    ("G23-mid", 168000000, 170000000, "guard"),
    ("H23", 170000000, 172000000, "holdout"),
    ("A23", 332000000, 334000000, "adversarial"),
)
PLAN = (
    ("base_sieve_support", 0, 12962, "whole_prefix"),
    ("segmented_target", 166000000, 168000000, "direct_segmented"),
)
E005_STARTS = (128000000, 256000000, 512000000, 1024000000, 2048000000, 4096000000)
E005_WIDTHS = (4096, 16384, 65536, 262144, 1048576)
VALIDATORS = (
    "plan_failure_count", "interval_exclusion_failure_count",
    "triangular_shell_failure_count", "distinct_partition_count_failure_count",
    "weak_rank_failure_count", "wheel_label_failure_count",
    "frequency_conservation_failure_count", "signed_mixing_failure_count",
    "mode_support_failure_count", "serializer_replay_failure_count",
)
TOP_FIELDS = {
    "experiment", "implementation_commit", "band", "partition", "parameters",
    "generation_plan", "anchor_summary", "validation", "families", "promotions",
}
FAMILY_FIELDS = {
    "family", "prime_mode_count", "highest_competing_prime_count",
    "strict_unique_prime_mode", "candidate_signature", "evaluated_signature",
    "target_prime_count", "target_composite_count", "population_floor_passed",
    "class_floor_passed", "occurrence_floor_passed", "mixed_class_count",
    "mixed_class_floor_passed", "positive_class_count",
    "positive_class_floor_passed", "target_enrichment_numerator",
    "target_enrichment_positive", "triviality_veto_passed", "mechanically_eligible",
}
PROMO_FIELDS = {
    "family", "target_signature", "target_prime_count", "target_composite_count",
    "mixed_class_count", "positive_class_count", "target_enrichment_numerator",
}
PARAMETERS = {
    "width": 2000000, "wheel": 210, "residues_R210": list(R210),
    "shell": "max_triangular_threshold",
    "summands": "unordered_distinct_positive",
    "partition_count": "finite_product_one_plus_z_power_j",
    "offsets": [0, 1, 2], "modulus": "anchor_plus_one",
    "feature": "dense_weak_rank_three_partition_residues",
    "signature_domain": [list(t) for t in SIGNATURES],
    "selector": "strict_unique_prime_frequency_mode",
    "population_floor": 2000, "class_floor": 20,
    "occurrence_floor": 64, "mixed_class_floor": 36,
    "positive_class_floor": 36, "support_cap": 1,
    "full_mixed_required": True,
}
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
    ("E022", ((154, 156), (156, 158), (158, 160), (160, 162), (312, 314))),
)


def overlaps(a, b):
    return a[0] < b[1] and b[0] < a[1]


def prior_roles():
    old = []
    for line in EARLY.strip().splitlines():
        name, lo, hi = line.split()
        old.append((name, int(lo) * 1000000, int(hi) * 1000000))
    old += [(f"{family}-{name}", a * 1000000, b * 1000000)
            for family, entries in FIVE_ROLE
            for name, (a, b) in zip(
                ("G-pre", "D", "G-mid", "H", "A"), entries, strict=True)]
    old += [(f"E005-{i}", s, s + E005_WIDTHS[-1])
            for i, s in enumerate(E005_STARTS)]
    return old


def allocation(g):
    w = 2000000
    return ((g, g + w), (g + w, g + 2*w), (g + 2*w, g + 3*w),
            (g + 3*w, g + 4*w), (2*(g + w), 2*(g + w) + w))


def audit_intervals():
    old = prior_roles()
    new = [(name, a, b) for name, a, b, _ in ROLES]
    nested = [(s, s + w) for s in E005_STARTS for w in E005_WIDTHS]
    if (len(EARLY.strip().splitlines()) != 53 or len(FIVE_ROLE) != 10
        or len(old) != 109 or len(set(name for name, _, _ in old)) != 109
        or len(nested) != 30 or len(new) != 5):
        raise ValueError("named-role inventory incomplete")
    if any(type(a) is not int or type(b) is not int or a >= b
           for _, a, b in old + new):
        raise ValueError("invalid named interval")
    old_old = sum(1 for i, _ in enumerate(old) for _ in old[i + 1:])
    new_old = len(new) * len(old)
    new_new = sum(1 for i, _ in enumerate(new) for _ in new[i + 1:])
    new_nested = len(new) * len(nested)
    old_nested = (len(old) - len(E005_STARTS)) * len(nested)
    if (old_old, new_old, new_new, new_nested, old_nested) != (
        5886, 545, 10, 150, 3090
    ):
        raise ValueError("wrong audit comparison cardinalities")
    if any(overlaps((a, b), (c, d)) for i, (_, a, b) in enumerate(old)
           for _, c, d in old[i + 1:]):
        raise ValueError("old/old intersection")
    if any(overlaps((a, b), (c, d)) for _, a, b in new
           for _, c, d in old):
        raise ValueError("new/old intersection")
    if any(overlaps((a, b), (c, d)) for i, (_, a, b) in enumerate(new)
           for _, c, d in new[i + 1:]):
        raise ValueError("new/new intersection")
    if any(overlaps((a, b), (c, d)) for _, a, b in new for c, d in nested):
        raise ValueError("new/nested intersection")
    if any(overlaps((a, b), (c, d)) for name, a, b in old
           if not name.startswith("E005-") for c, d in nested):
        raise ValueError("non-calibration/nested intersection")
    if any(not (s <= a < b <= s + E005_WIDTHS[-1])
           for s in E005_STARTS for a, b in nested if a == s):
        raise ValueError("nested out of maximum")
    within = sum(overlaps(x, y) for i, x in enumerate(nested)
                 for y in nested[i + 1:] if x[0] == y[0])
    across = sum(not overlaps(x, y) for i, x in enumerate(nested)
                 for y in nested[i + 1:] if x[0] != y[0])
    if (within, across) != (60, 375):
        raise ValueError("nested comparisons")
    ordered = sorted(old + new, key=lambda x: x[1])
    if any(x[2] > y[1] for x, y in zip(ordered, ordered[1:], strict=False)):
        raise ValueError("sorted named overlap")
    for g in range(162000000, 166000000, 2000000):
        candidate = allocation(g)
        valid = not any(overlaps(band, (a, b)) for band in candidate
                        for _, a, b in old) and not any(
                            overlaps(band, n) for band in candidate for n in nested
                        )
        if valid != (g == 164000000):
            raise ValueError("first-eligible allocation drift")
    if allocation(164000000) != tuple((a, b) for _, a, b, _ in ROLES):
        raise ValueError("new allocation drift")
    for stop, support in ((168000000, 12962), (172000000, 13115),
                          (334000000, 18276)):
        s = isqrt(stop - 1)
        if not (s*s <= stop - 1 < (s + 1)**2 and s + 1 == support):
            raise ValueError("exclusive support arithmetic drift")
    return dict(old_old=old_old, new_old=new_old, new_new=new_new,
                new_nested=new_nested, old_non_e005_nested=old_nested,
                nested_contained=len(nested), nested_within=within,
                nested_across=across)


def triangular(x):
    if type(x) is not int or x < 1:
        raise ValueError("positive integer anchor required")
    k = (isqrt(8*x + 1) - 1)//2
    t = k*(k + 1)//2
    if not (t <= x < (k + 1)*(k + 2)//2):
        raise ValueError("triangular threshold inequality violated")
    r = x - t
    if not (0 <= r <= k and (t + r) % 2 == x % 2):
        raise ValueError("triangular residual/parity")
    return k, r


def distinct_counts(limit):
    if type(limit) is not int or limit < 0:
        raise ValueError("invalid coefficient cap")
    c = [0] * (limit + 1)
    c[0] = 1
    for j in range(1, limit + 1):
        for n in range(limit, j - 1, -1):
            c[n] += c[n - j]
    return c


def exhaustive_count(n):
    if type(n) is not int or not (0 <= n <= 18):
        raise ValueError("synthetic subsets only")
    return sum(sum(indices) == n for size in range(n + 1)
               for indices in combinations(range(1, n + 1), size))


def finite_product_counts(limit):
    c = [1] + [0]*limit
    for j in range(1, limit + 1):
        old = c[:]
        for n in range(j, limit + 1):
            c[n] = old[n] + old[n - j]
    return c


def dense_rank(values):
    if type(values) is not tuple or len(values) != 3 or any(
        type(v) is not int or v < 0 for v in values
    ):
        raise ValueError("three canonical nonnegative integers required")
    order = sorted(set(values))
    result = tuple(order.index(v) for v in values)
    if result not in SIGNATURES:
        raise ValueError("weak-rank signature outside complete domain")
    return result


def feature(x, counts):
    k, r = triangular(x)
    if type(counts) is not list or len(counts) <= r + 2:
        raise ValueError("missing exact q counts")
    m = x + 1
    vals = tuple(counts[r + i] % m for i in (0, 1, 2))
    if any(type(v) is not int or not 0 <= v < m for v in vals):
        raise ValueError("noncanonical reduced q")
    return dense_rank(vals), k, r


def self_checks():
    shell = 0
    for x in range(1, 2001):
        k, r = triangular(x)
        brute = max(j for j in range(100) if j*(j + 1)//2 <= x)
        shell += int(k != brute or x != k*(k + 1)//2 + r)
    for k in range(1, 80):
        for x in (k*(k + 1)//2 - 1, k*(k + 1)//2,
                  k*(k + 1)//2 + k):
            if x > 0:
                a, r = triangular(x)
                shell += int(x != a*(a + 1)//2 + r)
    synthetic = distinct_counts(18)
    partition = sum(synthetic[n] != exhaustive_count(n) or
                    synthetic[n] != finite_product_counts(18)[n]
                    for n in range(19))
    # Specifically reject ascending reuse, whose q(2) differs.
    ascending = [1] + [0]*18
    for j in range(1, 19):
        for n in range(j, 19):
            ascending[n] += ascending[n - j]
    partition += int(ascending[2] == synthetic[2])
    words = {dense_rank((a, b, c)) for a in range(3)
             for b in range(3) for c in range(3)}
    rank = int(words != set(SIGNATURES))
    for i, expected in enumerate(SIGNATURES):
        # Build a hand-entered representative for each ordered weak-rank word.
        rank += int(dense_rank(expected) != expected)
        rank += int(SIGNATURES[i] != expected)
    for x in range(1, 30):
        word, _, r = feature(x, synthetic + [0]*20)
        vals = [synthetic[r + i] % (x + 1) for i in range(3)]
        independently = tuple(sum(v < vals[i] for v in set(vals))
                              for i in range(3))
        rank += int(word != independently)
    return shell, partition, rank


def plan_dicts(plan=PLAN):
    return [dict(purpose=p, start=a, stop=b, strategy=s) for p, a, b, s in plan]


class GeneratorGate:
    def __init__(self, plan=PLAN, phase="D23", *, indirect=False, per_anchor=False):
        if phase != "D23" or type(indirect) is not bool or type(per_anchor) is not bool:
            raise ValueError("off-phase or malformed generation provenance")
        if indirect or per_anchor:
            raise ValueError("hidden or per-anchor prime generator forbidden")
        if type(plan) is not tuple or len(plan) != 2:
            raise ValueError("exact ordered two-entry tuple required")
        if any(type(row) is not tuple or len(row) != 4 or any(
            type(got) is not type(want) or got != want
            for got, want in zip(row, expected, strict=True)
        ) for row, expected in zip(plan, PLAN, strict=True)):
            raise ValueError("unrecognised/partial/expanded generator plan")
        audit_intervals()
        self.plan = plan
        self.phase = phase
        self.next_entry = 0

    def enter(self, index, *entry):
        if (type(index) is not int or index != self.next_entry
            or index not in (0, 1) or tuple(entry) != PLAN[index]
            or self.phase != "D23" or self.plan != PLAN):
            raise ValueError("forbidden generator entry/order")
        audit_intervals()
        if index == 0 and isqrt(PLAN[1][2] - 1) + 1 != entry[2]:
            raise ValueError("incorrect low support")
        if index == 1:
            if any(overlaps((entry[1], entry[2]), (a, b))
                   for _, a, b in prior_roles()):
                raise ValueError("old role entered")
            if any(overlaps((entry[1], entry[2]), (a, b))
                   for name, a, b, _ in ROLES if name != "D23"):
                raise ValueError("off-phase role entered")
        self.next_entry += 1

    def finished(self):
        if self.next_entry != 2:
            raise ValueError("incomplete generator plan")


def base_sieve(stop):
    return sieve(stop - 1)


def segmented_target(start, stop, base):
    flags = bytearray(b"\x01")*(stop - start)
    for p in base:
        first = max(p*p, ((start + p - 1)//p)*p)
        if first < stop:
            flags[first - start:stop - start:p] = b"\x00" * (
                (stop - 1 - first)//p + 1)
    return flags


def precompute_features():
    left, right = ROLES[1][1:3]
    kmax, _ = triangular(right - 1)
    counts = distinct_counts(kmax + 2)
    idx = {r: j for j, r in enumerate(R210)}
    signatures = bytearray(right - left)
    wheel = 0
    for x in range(left, right):
        r210 = x % Q
        if r210 not in idx:
            continue
        word, k, r = feature(x, counts)
        if not (k*(k + 1)//2 + r == x and x % 2 == 1):
            raise ValueError("shell/wheel parity")
        signatures[x - left] = SIGNATURES.index(word)
        wheel += 1
    return signatures, wheel


def full_tables(flags, signatures):
    left, right = ROLES[1][1:3]
    if len(flags) != right - left or len(signatures) != right - left:
        raise ValueError("incorrect high-segment size")
    idx = {r: j for j, r in enumerate(R210)}
    p = [[0]*48 for _ in SIGNATURES]
    c = [[0]*48 for _ in SIGNATURES]
    supports = [set() for _ in SIGNATURES]
    wheel = 0
    for x in range(left, right):
        ri = idx.get(x % Q)
        if ri is None:
            continue
        wheel += 1
        code = signatures[x - left]
        if code >= len(SIGNATURES):
            raise ValueError("invalid encoded weak rank")
        if flags[x - left]:
            p[code][ri] += 1
            supports[code].add(x)
        else:
            c[code][ri] += 1
    return p, c, supports, wheel


def strict_mode(counts):
    if type(counts) is not list or len(counts) != 13 or any(
        type(v) is not int or v < 0 for v in counts
    ):
        raise ValueError("invalid full prime frequencies")
    largest = max(counts)
    others = sorted(counts, reverse=True)
    return (counts.index(largest) if largest > others[1] else None,
            largest, others[1])


def label_blind_triviality_clear(candidate, signatures):
    if candidate is None:
        return False
    # No prime labels consulted: reject an exact signature forced by a Q210
    # class across its full anchored support, or confined to shell edges.
    idx = {r: i for i, r in enumerate(R210)}
    seen = [[False, False] for _ in R210]
    non_edge = False
    parity_cases = set()
    left, right = ROLES[1][1:3]
    for x in range(left, right):
        ri = idx.get(x % Q)
        if ri is None:
            continue
        matched = signatures[x - left] == candidate
        seen[ri][int(matched)] = True
        if matched:
            k, r = triangular(x)
            non_edge |= 2 < r < k - 2
            parity_cases.add((k % 4, r % 2))
    return (all(a and b for a, b in seen)
            and non_edge and len(parity_cases) > 1)


def gates(p, c, supports, signatures, wheel, expected_wheel):
    npt = [sum(row) for row in p]
    nct = [sum(row) for row in c]
    np = sum(npt)
    nc = sum(nct)
    pr = [sum(p[t][r] for t in range(13)) for r in range(48)]
    cr = [sum(c[t][r] for t in range(13)) for r in range(48)]
    candidate, peak, competitor = strict_mode(npt)
    populated = np >= 2000 and nc >= 2000
    class_ok = all(a >= 20 and b >= 20 for a, b in zip(pr, cr, strict=True))
    targetp = npt[candidate] if candidate is not None else None
    targetc = nct[candidate] if candidate is not None else None
    mixed = None
    positive = None
    enrichment = None
    signed_errors = 0
    for t in range(13):
        whole = npt[t]*nc - nct[t]*np
        independent = sum(p[t])*sum(nct) - sum(c[t])*sum(npt)
        signed_errors += int(whole != independent)
        for ri in range(48):
            pt, ct = p[t][ri], c[t][ri]
            op = sum(p[j][ri] for j in range(13) if j != t)
            oc = sum(c[j][ri] for j in range(13) if j != t)
            er = pt*cr[ri] - ct*pr[ri]
            signed_errors += int(er != pt*oc - ct*op)
            signed_errors += int((min(pt, ct, op, oc) > 0) !=
                                 (pt > 0 and op > 0 and ct > 0 and oc > 0))
    if candidate is not None:
        mixed = sum(min(p[candidate][ri], c[candidate][ri],
                        pr[ri] - p[candidate][ri],
                        cr[ri] - c[candidate][ri]) > 0 for ri in range(48))
        positive = sum(p[candidate][ri]*cr[ri] -
                       c[candidate][ri]*pr[ri] > 0 for ri in range(48))
        enrichment = targetp*nc - targetc*np
        checkmixed = sum(p[candidate][ri] > 0 and c[candidate][ri] > 0
                         and sum(p[j][ri] for j in range(13) if j != candidate) > 0
                         and sum(c[j][ri] for j in range(13) if j != candidate) > 0
                         for ri in range(48))
        checkpositive = sum(p[candidate][ri] *
                            sum(c[j][ri] for j in range(13) if j != candidate) >
                            c[candidate][ri] *
                            sum(p[j][ri] for j in range(13) if j != candidate)
                            for ri in range(48))
        signed_errors += int(mixed != checkmixed or positive != checkpositive)
    clear = label_blind_triviality_clear(candidate, signatures)
    valid = dict.fromkeys(VALIDATORS, 0)
    valid["plan_failure_count"] = int(PLAN != (
        ("base_sieve_support", 0, 12962, "whole_prefix"),
        ("segmented_target", 166000000, 168000000, "direct_segmented")))
    try:
        audit_intervals()
    except ValueError:
        valid["interval_exclusion_failure_count"] += 1
    shell_errors, partition_errors, rank_errors = self_checks()
    valid["triangular_shell_failure_count"] = shell_errors
    valid["distinct_partition_count_failure_count"] = partition_errors
    valid["weak_rank_failure_count"] = rank_errors
    valid["wheel_label_failure_count"] = (
        int(R210 != tuple(i for i in range(210) if gcd(i, 210) == 1))
        + int(wheel != expected_wheel or np + nc != wheel)
        + int(any(pr[i] + cr[i] <= 0 for i in range(48)))
    )
    valid["frequency_conservation_failure_count"] = (
        int(np != sum(pr) or nc != sum(cr) or
            np != sum(npt) or nc != sum(nct))
        + sum(int(sum(p[t]) != npt[t] or sum(c[t]) != nct[t])
              for t in range(13))
        + sum(int(sum(p[t][r] for t in range(13)) != pr[r] or
                  sum(c[t][r] for t in range(13)) != cr[r])
              for r in range(48))
    )
    valid["signed_mixing_failure_count"] = signed_errors
    # Complete exact member-wise equality, never a proxy/hash/count.
    support = supports[candidate] if candidate is not None else set()
    full_rebuilt = {x for x in range(ROLES[1][1], ROLES[1][2])
                    if x % 210 in R210 and
                    signatures[x - ROLES[1][1]] == candidate and
                    x in support} if candidate is not None else set()
    valid["mode_support_failure_count"] = (
        int(strict_mode([3, 3] + [0]*11) != (None, 3, 3))
        + int(strict_mode([1, 4] + [0]*11) != (1, 4, 1))
        + int(candidate is not None and
              (len(support) != targetp or full_rebuilt != support))
    )
    population_gate = populated
    occurrence_gate = candidate is not None and targetp >= 64
    mix_gate = candidate is not None and mixed >= 36
    signed_gate = candidate is not None and enrichment > 0
    positive_gate = candidate is not None and positive >= 36
    eligible = (candidate is not None and population_gate and class_ok
                and occurrence_gate and mix_gate and signed_gate
                and positive_gate and clear and
                all(type(n) is int and n == 0 for n in valid.values()))
    family = dict(
        family="P1", prime_mode_count=peak,
        highest_competing_prime_count=competitor,
        strict_unique_prime_mode=candidate is not None,
        candidate_signature=(list(SIGNATURES[candidate])
                             if candidate is not None else None),
        evaluated_signature=(list(SIGNATURES[candidate])
                             if candidate is not None else None),
        target_prime_count=targetp, target_composite_count=targetc,
        population_floor_passed=population_gate, class_floor_passed=class_ok,
        occurrence_floor_passed=occurrence_gate,
        mixed_class_count=mixed, mixed_class_floor_passed=mix_gate,
        positive_class_count=positive, positive_class_floor_passed=positive_gate,
        target_enrichment_numerator=enrichment,
        target_enrichment_positive=signed_gate,
        triviality_veto_passed=clear, mechanically_eligible=eligible,
    )
    promotion = [dict(
        family="P1", target_signature=family["evaluated_signature"],
        target_prime_count=targetp, target_composite_count=targetc,
        mixed_class_count=mixed, positive_class_count=positive,
        target_enrichment_numerator=enrichment,
    )] if eligible else []
    return family, promotion, valid, (np, nc, pr, cr)


def _typed_equal(a, b):
    if type(a) is not type(b):
        return False
    if type(a) is dict:
        return set(a) == set(b) and all(_typed_equal(a[k], b[k]) for k in a)
    if type(a) is list:
        return len(a) == len(b) and all(_typed_equal(x, y)
                                        for x, y in zip(a, b, strict=True))
    return a == b


def canonical(data):
    return (json.dumps(data, sort_keys=True, indent=2, ensure_ascii=True)
            + "\n").encode("ascii")


def validate_payload(obj):
    if type(obj) is not dict or set(obj) != TOP_FIELDS:
        return False
    if obj["experiment"] != "E023":
        return False
    sha = obj["implementation_commit"]
    if type(sha) is not str or len(sha) != 40 or any(
        x not in "0123456789abcdef" for x in sha
    ):
        return False
    if not _typed_equal(obj["band"], dict(
        name="D23", range=[166000000, 168000000],
        interval_semantics="half-open"
    )):
        return False
    if not _typed_equal(obj["partition"], [
        dict(name=n, range=[a, b], role=role) for n, a, b, role in ROLES
    ]):
        return False
    if not _typed_equal(obj["parameters"], PARAMETERS):
        return False
    if not _typed_equal(obj["generation_plan"], plan_dicts()):
        return False
    a = obj["anchor_summary"]
    expected_a = {"wheel_anchor_count", "prime_count", "composite_count",
                  "prime_counts_by_R210", "composite_counts_by_R210"}
    if type(a) is not dict or set(a) != expected_a:
        return False
    if any(type(a[k]) is not int or a[k] < 0
           for k in ("wheel_anchor_count", "prime_count", "composite_count")):
        return False
    if any(type(a[k]) is not list or len(a[k]) != 48 or any(
        type(v) is not int or v < 0 for v in a[k])
        for k in ("prime_counts_by_R210", "composite_counts_by_R210")):
        return False
    if (sum(a["prime_counts_by_R210"]) != a["prime_count"]
        or sum(a["composite_counts_by_R210"]) != a["composite_count"]
        or a["wheel_anchor_count"] != a["prime_count"] + a["composite_count"]):
        return False
    v = obj["validation"]
    if type(v) is not dict or set(v) != set(VALIDATORS) or any(
        type(x) is not int or x != 0 for x in v.values()
    ):
        return False
    if type(obj["families"]) is not list or len(obj["families"]) != 1:
        return False
    f = obj["families"][0]
    if type(f) is not dict or set(f) != FAMILY_FIELDS or f["family"] != "P1":
        return False
    for k in ("prime_mode_count", "highest_competing_prime_count"):
        if type(f[k]) is not int or f[k] < 0:
            return False
    for k in ("target_prime_count", "target_composite_count",
              "mixed_class_count", "positive_class_count",
              "target_enrichment_numerator"):
        val = f[k]
        if val is not None and (type(val) is not int or
                                (k != "target_enrichment_numerator" and val < 0)):
            return False
    boolkeys = (
        "strict_unique_prime_mode", "population_floor_passed",
        "class_floor_passed", "occurrence_floor_passed",
        "mixed_class_floor_passed", "positive_class_floor_passed",
        "target_enrichment_positive", "triviality_veto_passed",
        "mechanically_eligible",
    )
    if any(type(f[k]) is not bool for k in boolkeys):
        return False
    candidate = f["candidate_signature"]
    evaluated = f["evaluated_signature"]
    if candidate is not None and (type(candidate) is not list or
                                  len(candidate) != 3 or
                                  any(type(x) is not int for x in candidate) or
                                  tuple(candidate) not in SIGNATURES):
        return False
    if candidate != evaluated:
        return False
    if f["strict_unique_prime_mode"] != (
        f["prime_mode_count"] > f["highest_competing_prime_count"]
    ) or f["strict_unique_prime_mode"] != (candidate is not None):
        return False
    if f["population_floor_passed"] != (
        a["prime_count"] >= 2000 and a["composite_count"] >= 2000
    ) or f["class_floor_passed"] != all(
        p >= 20 and c >= 20 for p, c in zip(
            a["prime_counts_by_R210"], a["composite_counts_by_R210"], strict=True)
    ):
        return False
    dep = ("target_prime_count", "target_composite_count",
           "mixed_class_count", "positive_class_count",
           "target_enrichment_numerator")
    if candidate is None:
        if any(f[k] is not None for k in dep):
            return False
        if any(f[k] for k in ("occurrence_floor_passed",
                             "mixed_class_floor_passed",
                             "positive_class_floor_passed",
                             "target_enrichment_positive",
                             "triviality_veto_passed", "mechanically_eligible")):
            return False
    else:
        if any(f[k] is None for k in dep):
            return False
        if (f["target_prime_count"] != f["prime_mode_count"]
            or f["occurrence_floor_passed"] != (f["target_prime_count"] >= 64)
            or f["mixed_class_floor_passed"] != (f["mixed_class_count"] >= 36)
            or f["positive_class_floor_passed"] != (f["positive_class_count"] >= 36)
            or f["target_enrichment_positive"] !=
            (f["target_enrichment_numerator"] > 0)
            or not (0 <= f["mixed_class_count"] <= 48
                    and 0 <= f["positive_class_count"] <= 48)):
            return False
    necessary = (f["strict_unique_prime_mode"] and f["population_floor_passed"]
                 and f["class_floor_passed"] and f["occurrence_floor_passed"]
                 and f["mixed_class_floor_passed"] and f["positive_class_floor_passed"]
                 and f["target_enrichment_positive"]
                 and f["triviality_veto_passed"])
    if f["mechanically_eligible"] != necessary:
        return False
    promos = obj["promotions"]
    if type(promos) is not list or len(promos) > 1:
        return False
    if bool(promos) != f["mechanically_eligible"]:
        return False
    if promos and (type(promos[0]) is not dict or set(promos[0]) != PROMO_FIELDS
                   or not _typed_equal(promos[0], dict(
                       family="P1", target_signature=f["evaluated_signature"],
                       target_prime_count=f["target_prime_count"],
                       target_composite_count=f["target_composite_count"],
                       mixed_class_count=f["mixed_class_count"],
                       positive_class_count=f["positive_class_count"],
                       target_enrichment_numerator=f["target_enrichment_numerator"]
                   ))):
        return False
    return True


def evaluate_h23_refutation(frozen, target, validations_zero=True):
    """Pure one-shot H23 gate grammar. NO H23 generator or computation allowed.

    frozen: full 13-state counts (global and per 48 classes) and target stats
    already obtained by a *separately authorised later* H23 run. This function
    only checks the originally committed P1 condition, never selects a new t.
    """
    if type(target) is not tuple or target not in SIGNATURES:
        raise ValueError("exact previously frozen H23 triple required")
    if type(validations_zero) is not bool:
        raise ValueError("malformed validation state")
    return bool(
        validations_zero and frozen["frozen_target"] == target
        and frozen["strict_unique_mode"] == target
        and frozen["np"] >= 2000 and frozen["nc"] >= 2000
        and all(p >= 20 and c >= 20 for p, c in frozen["class_populations"])
        and frozen["target_prime_count"] >= 64
        and frozen["mixed_class_count"] >= 36
        and frozen["positive_class_count"] >= 36
        and frozen["target_enrichment_numerator"] > 0
        and frozen["triviality_veto_passed"] and frozen["all_replay_checks_passed"]
    )


def run(commit, output):
    if type(commit) is not str or len(commit) != 40 or any(
        s not in "0123456789abcdef" for s in commit
    ):
        raise ValueError("full precommitted implementation Git SHA required")
    gate = GeneratorGate()
    # Finite combinatorics is label-blind and before the label partition.
    signatures, expected_wheel = precompute_features()
    gate.enter(0, *PLAN[0])
    support_primes = base_sieve(12962)
    gate.enter(1, *PLAN[1])
    flags = segmented_target(166000000, 168000000, support_primes)
    gate.finished()
    p, c, supports, wheel = full_tables(flags, signatures)
    family, promotions, validation, populations = gates(
        p, c, supports, signatures, wheel, expected_wheel)
    np, nc, pr, cr = populations
    payload = dict(
        experiment="E023", implementation_commit=commit,
        band=dict(name="D23", range=[166000000, 168000000],
                  interval_semantics="half-open"),
        partition=[dict(name=n, range=[a, b], role=role)
                   for n, a, b, role in ROLES],
        parameters=PARAMETERS, generation_plan=plan_dicts(),
        anchor_summary=dict(
            wheel_anchor_count=wheel, prime_count=np, composite_count=nc,
            prime_counts_by_R210=pr, composite_counts_by_R210=cr),
        validation=validation, families=[family], promotions=promotions,
    )
    if not validate_payload(payload):
        raise ValueError("strict canonical typed evidence validation failed")
    Path(output).write_bytes(canonical(payload))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--band", choices=("D23",), required=True)
    parser.add_argument("--code-commit", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    if args.band != "D23":
        raise ValueError("D23-only authority")
    run(args.code_commit, args.output)


if __name__ == "__main__":
    main()
