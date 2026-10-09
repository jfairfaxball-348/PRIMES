"""E025 H25-only evaluator. Frozen original E025 section 5.

No hidden generator helpers: only the two exact H25 entries are allowed.
Only H25 may be generated; D25, guards and adversarial roles are forbidden.
"""
from __future__ import annotations

import argparse
import json
import re
from functools import cache
from hashlib import sha256
from math import factorial, gcd, isqrt
from pathlib import Path

LOW, HIGH = 214_000_000, 216_000_000
BASE_STOP = 14_697
PLAN = (
    ("base_sieve_support", 0, BASE_STOP, "whole_prefix"),
    ("segmented_target", LOW, HIGH, "direct_segmented"),
)
WHEEL = 210
RESIDUES = tuple(a for a in range(210) if gcd(a, 210) == 1)
STATES = tuple(range(8))
PARTITION = (
    ("G25-pre", 208_000_000, 210_000_000, "guard"),
    ("D25", 210_000_000, 212_000_000, "discovery"),
    ("G25-mid", 212_000_000, 214_000_000, "guard"),
    ("H25", LOW, HIGH, "holdout"),
    ("A25", 420_000_000, 422_000_000, "adversarial"),
)
VALIDATORS = (
    "plan_failure_count",
    "interval_exclusion_failure_count",
    "tableau_semantics_failure_count",
    "hook_integrality_failure_count",
    "octile_boundary_failure_count",
    "wheel_label_failure_count",
    "frequency_conservation_failure_count",
    "signed_mixing_failure_count",
    "mode_support_failure_count",
    "serializer_replay_failure_count",
)


def strict_int(value: object) -> bool:
    return type(value) is int


@cache
def ballot_reference(k: int) -> int:
    """Independent constrained-word DP, intentionally only for k <= 4."""
    if type(k) is not int or not 0 <= k <= 4:
        raise ValueError("finite reference only")
    @cache
    def walk(a: int, b: int, c: int) -> int:
        if (a, b, c) == (k, k, k):
            return 1
        return (
            (walk(a + 1, b, c) if a < k else 0)
            + (walk(a, b + 1, c) if b < a and b < k else 0)
            + (walk(a, b, c + 1) if c < b and c < k else 0)
        )
    return walk(0, 0, 0)


def hook_quotient(k: int) -> int:
    if type(k) is not int or k < 0:
        raise ValueError("k")
    numerator = 2 * factorial(3 * k)
    denominator = factorial(k) * factorial(k + 1) * factorial(k + 2)
    q, r = divmod(numerator, denominator)
    if r:
        raise ArithmeticError("nonexact hook quotient")
    return q


def tableau_window(min_k: int, max_k: int) -> dict[int, int]:
    """Exact adjacent recurrence; keep only requested k, never a high table."""
    if any(type(v) is not int for v in (min_k, max_k)) or not 0 <= min_k <= max_k:
        raise ValueError("k window")
    t = 1
    selected = {}
    for k in range(max_k + 1):
        if k >= min_k:
            selected[k] = t
        if k < max_k:
            numerator = t * (3 * k + 1) * (3 * k + 2) * (3 * k + 3)
            denominator = (k + 1) * (k + 2) * (k + 3)
            t, rem = divmod(numerator, denominator)
            if rem:
                raise ArithmeticError("nonexact tableau recurrence")
    return selected


def octile_from_remainder(remainder: int, modulus: int) -> int:
    if not strict_int(modulus) or not strict_int(remainder):
        raise ValueError("integer residue")
    if modulus <= 0 or not 0 <= remainder < modulus:
        raise ValueError("canonical residue")
    out = (8 * remainder) // modulus
    if not 0 <= out <= 7:
        raise ArithmeticError("octile outside complete domain")
    return out


def signature(x: int, t_k: int) -> int:
    if not strict_int(x) or x < 1 or not strict_int(t_k) or t_k < 0:
        raise ValueError("unlabelled positive anchor and exact count")
    return octile_from_remainder(t_k % (x + 1), x + 1)


def overlaps(a: tuple[int, int], b: tuple[int, int]) -> bool:
    return a[0] < b[1] and b[0] < a[1]


def audit_named_intervals(design_text: str) -> dict[str, tuple[int, int]]:
    """Read only frozen metadata section, never earlier outcomes."""
    section = design_text.split("## 3.", 1)[1].split("## 4.", 1)[0]
    pairs = re.findall(r"([A-Za-z0-9-]+)=\[(\d+),(\d+)\)", section)
    old: dict[str, tuple[int, int]] = {}
    for name, start, stop in pairs:
        bounds = (int(start), int(stop))
        if name in old and old[name] != bounds:
            raise ValueError("conflicting named interval")
        old[name] = bounds
    maximum = {n: b for n, b in old.items() if n.startswith("E005-") and n.endswith("-maximum")}
    nested = {n: b for n, b in old.items() if "-nested-" in n}
    older = {n: b for n, b in old.items() if n not in nested}
    if len(older) != 119 or len(maximum) != 6 or len(nested) != 30 or len(old) != 149:
        raise ValueError("incomplete 119+30 provenance")
    for n, (start, stop) in old.items():
        if start >= stop:
            raise ValueError("empty role")
        if n in nested:
            parent = n.split("-nested-", 1)[0] + "-maximum"
            if parent not in maximum or not maximum[parent][0] <= start < stop <= maximum[parent][1]:
                raise ValueError("nested escaped maximum")
    old_list = list(older.items())
    if any(overlaps(a, b) for i, (_, a) in enumerate(old_list) for _, b in old_list[i + 1:]):
        raise ValueError("historical old-old intersection")
    independent = [(n, a) for n, a in older.items() if n not in maximum]
    if any(overlaps(a, b) for _, a in independent for _, b in nested.items()):
        raise ValueError("noncalibration/nested overlap")
    newer = [(name, (start, stop)) for name, start, stop, _ in PARTITION]
    if any(overlaps(a, b) for _, a in newer for _, b in old.items()):
        raise ValueError("new/old intersection")
    if any(overlaps(a, b) for i, (_, a) in enumerate(newer) for _, b in newer[i + 1:]):
        raise ValueError("new/new intersection")
    if len(RESIDUES) != 48 or len(set(RESIDUES)) != 48:
        raise ValueError("wheel order")
    return old


def assert_plan(plan: object, design_text: str, phase: str = "H25") -> None:
    if phase != "H25" or type(plan) is not tuple or plan != PLAN:
        raise PermissionError("frozen H25 whole-plan mismatch or forbidden phase")
    if len(plan) != 2 or any(type(e) is not tuple or len(e) != 4 for e in plan):
        raise PermissionError("invalid phase entry")
    if isqrt(HIGH - 1) + 1 != BASE_STOP:
        raise PermissionError("invalid low support upper-exclusive bound")
    named = audit_named_intervals(design_text)
    lo, hi = plan[1][1:3]
    if any(overlaps((lo, hi), b) for name, b in named.items()):
        raise PermissionError("forbidden old named role")
    if (lo, hi) != PARTITION[3][1:3]:
        raise PermissionError("forbidden new role")


def generation_entry(index: int, plan: tuple, design: str, phase: str) -> None:
    assert_plan(plan, design, phase)
    if type(index) is not int or index not in (0, 1):
        raise PermissionError("third, negative, indirect or unknown generator")
    if plan[index] != PLAN[index]:
        raise PermissionError("per-entry mismatch")


def low_base_sieve(stop: int) -> list[int]:
    """Whole-prefix low support, callable ONLY after generation_entry(0)."""
    if stop != BASE_STOP:
        raise PermissionError("base helper refused")
    flags = bytearray(b"\x01") * stop
    flags[:2] = b"\x00\x00"
    for p in range(2, isqrt(stop - 1) + 1):
        if flags[p]:
            for j in range(p * p, stop, p):
                flags[j] = 0
    return [p for p, ok in enumerate(flags) if ok]


def direct_target_mask(start: int, stop: int, bases: list[int]) -> bytearray:
    """Only targeted high segment: never whole prefix or per-anchor oracle."""
    if (start, stop) != (LOW, HIGH):
        raise PermissionError("direct segment helper refused")
    flags = bytearray(b"\x01") * (stop - start)
    for p in bases:
        first = max(p * p, ((start + p - 1) // p) * p)
        if first < stop:
            flags[first - start::p] = b"\x00" * ((stop - 1 - first) // p + 1)
    return flags


def independent_small_checks() -> None:
    refs = (1, 1, 5, 42, 462)
    for k, expected in enumerate(refs):
        if ballot_reference(k) != expected or hook_quotient(k) != expected:
            raise ArithmeticError("independent tableau semantics")
        if tableau_window(k, k)[k] != expected:
            raise ArithmeticError("recurrence/quotient mismatch")
    fixtures = ((1, 1, 2, 1, 4), (3, 1, 4, 1, 2), (4, 2, 5, 0, 0),
                (8, 2, 9, 5, 4), (9, 3, 10, 2, 1), (15, 3, 16, 10, 5),
                (16, 4, 17, 3, 1))
    for x, k, m, r, value in fixtures:
        if isqrt(x) != k or hook_quotient(k) % m != r or signature(x, hook_quotient(k)) != value:
            raise ArithmeticError("octile fixture")



def independent_triviality_veto() -> bool:
    """Label-free definitional test; finite witnesses refute exact E024 recoding.

    E016 central-binomial odd valuations/carries concern C(2x,x);
    E018 uses full-x tribonacci tilings mod x; E023 uses distinct-summand
    partition shell ranks. None is the 3-by-isqrt(x) tableau quotient.
    Common factorial algebra (E016), octile encoding (E018), square-shell
    index (E023) or anchor-plus-one remainder and combinatorial quotients
    (E024) are NONPROMOTABLE controls. Review representation definitions,
    never earlier outcomes. This finite test does not prove general
    algebraic independence or historical originality.
    """
    names = (
        "E016_CENTRAL_BINOMIAL_ODD_VALUATION_CARRY_SHAPES.md",
        "E018_MONOMER_DOMINO_TROMINO_TILING_RESIDUE_SHAPES.md",
        "E023_DISTINCT_SUMMAND_PARTITION_TRIANGULAR_SHELL_RANK_SHAPES.md",
        "E024_BINARY_GRASSMANNIAN_RANK_RESIDUE_ORDER_SHAPES.md",
    )
    if not all((Path("experiments") / name).is_file() for name in names):
        raise PermissionError("old primitive definitions unavailable for veto")
    rank_to_octile: dict[int, set[int]] = {}
    octile_to_rank: dict[int, set[int]] = {}
    for x in range(3, 160):
        r2 = ((2**x - 1) * (2 ** (x - 1) - 1) // 3) % (x + 1)
        r3 = ((2**x - 1) * (2 ** (x - 1) - 1) * (2 ** (x - 2) - 1) // 21) % (x + 1)
        rank = (0 if r2 < r3 else 1 if r2 == r3 else 2)
        octile = signature(x, hook_quotient(isqrt(x)))
        rank_to_octile.setdefault(rank, set()).add(octile)
        octile_to_rank.setdefault(octile, set()).add(rank)
    # E025 is not an exact coarsening of E024's three-state rank order,
    # nor vice versa, by actual counterexamples to the functional mapping.
    if not any(len(v) > 1 for v in rank_to_octile.values()):
        return False
    if not any(len(v) > 1 for v in octile_to_rank.values()):
        return False
    # Both label classes always share the full wheel. Detect class-constant
    # signatures forced merely by 210 arithmetic on a label-free small grid.
    table = tableau_window(isqrt(211), isqrt(6_000))
    by_class: dict[int, set[int]] = {r: set() for r in RESIDUES}
    for x in range(211, 6_000):
        residue = x % 210
        if residue in by_class:
            by_class[residue].add(signature(x, table[isqrt(x)]))
    return all(len(signatures) >= 2 for signatures in by_class.values())

def candidate_analysis(prime: list[list[int]], comp: list[list[int]]) -> tuple[dict, list]:
    """H25 always evaluates frozen D25 target zero, never a new winner."""
    np_a = [sum(row) for row in prime]
    nc_a = [sum(row) for row in comp]
    np, nc = sum(np_a), sum(nc_a)
    cp = [sum(row[t] for row in prime) for t in STATES]
    cc = [sum(row[t] for row in comp) for t in STATES]
    best = max(cp)
    winners = [t for t in STATES if cp[t] == best]
    diagnostic = winners[0] if len(winners) == 1 else None
    frozen = 0
    competitor = max(cp[1:])
    fixed_unique = cp[frozen] > competitor
    pop_ok = np >= 2000 and nc >= 2000
    cls_ok = all(p >= 20 and c >= 20 for p, c in zip(np_a, nc_a, strict=True))
    target_p, target_c = cp[frozen], cc[frozen]
    occur_ok = target_p >= 64
    mixed = sum(
        prime[i][frozen] > 0 and np_a[i] - prime[i][frozen] > 0
        and comp[i][frozen] > 0 and nc_a[i] - comp[i][frozen] > 0
        for i in range(48)
    )
    positive = sum(
        prime[i][frozen] * nc_a[i] - comp[i][frozen] * np_a[i] > 0
        for i in range(48)
    )
    signed = target_p * nc - target_c * np
    veto_ok = independent_triviality_veto()
    eligible = all((fixed_unique, pop_ok, cls_ok, occur_ok, mixed >= 36,
                    positive >= 36, signed > 0, veto_ok))
    family = {
        "family": "F1",
        "prime_mode_count": best,
        "highest_competing_prime_count": competitor,
        "strict_unique_prime_mode": fixed_unique,
        "candidate_signature": diagnostic,
        "evaluated_signature": frozen,
        "target_prime_count": target_p,
        "target_composite_count": target_c,
        "population_floor_passed": pop_ok,
        "class_floor_passed": cls_ok,
        "occurrence_floor_passed": occur_ok,
        "mixed_class_count": mixed,
        "mixed_class_floor_passed": mixed >= 36,
        "positive_class_count": positive,
        "positive_class_floor_passed": positive >= 36,
        "target_enrichment_numerator": signed,
        "target_enrichment_positive": signed > 0,
        "triviality_veto_passed": veto_ok,
        "mechanically_eligible": bool(eligible),
    }
    return family, []  # H25 may NEVER promote a new target.

def canonical(value: dict) -> bytes:
    return (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True) + "\n").encode("ascii")


def payload_schema(value: object) -> None:
    if type(value) is not dict or set(value) != {
        "anchor_summary", "band", "experiment", "families", "generation_plan",
        "implementation_commit", "parameters", "partition", "promotions", "validation",
    }:
        raise ValueError("ten top keys")
    def no_float(tree: object) -> None:
        if type(tree) is dict:
            if any(type(k) is not str for k in tree):
                raise ValueError("non-string key")
            for v in tree.values():
                no_float(v)
        elif type(tree) is list:
            for v in tree:
                no_float(v)
        elif type(tree) not in (str, int, bool, type(None)):
            raise ValueError("noncanonical type")
    no_float(value)
    if value["experiment"] != "E025":
        raise ValueError("experiment")
    if not re.fullmatch("[0-9a-f]{40}", value["implementation_commit"]):
        raise ValueError("commit")
    if value["band"] != {"name": "H25", "range": [LOW, HIGH], "interval_semantics": "half-open"}:
        raise ValueError("phase")
    if type(value["validation"]) is not dict or set(value["validation"]) != set(VALIDATORS):
        raise ValueError("ten validation roles")
    if any(not strict_int(v) or v != 0 for v in value["validation"].values()):
        raise ValueError("nonzero integer-only validators")
    if value["partition"] != [
        {"name": n, "range": [a, b], "role": role} for n, a, b, role in PARTITION
    ]:
        raise ValueError("partition")
    if value["generation_plan"] != [
        {"purpose": e[0], "start": e[1], "stop": e[2], "strategy": e[3]} for e in PLAN
    ]:
        raise ValueError("plan")
    p = value["parameters"]
    expected_p = {"width": 2_000_000, "wheel": 210, "residues_R210": list(RESIDUES),
                  "rows": 3, "index_rule": "isqrt_x",
                  "object": "three_row_rectangular_standard_young_tableau_linear_extensions",
                  "modulus": "anchor_plus_one", "feature": "tableau_remainder_octile",
                  "signature_domain": list(STATES), "selector": "strict_unique_prime_frequency_mode",
                  "population_floor": 2000, "class_floor": 20,
                  "occurrence_floor": 64, "mixed_class_floor": 36,
                  "positive_class_floor": 36, "support_cap": 1,
                  "full_mixed_required": True}
    if p != expected_p or any(type(p[k]) is not type(v) for k, v in expected_p.items()):
        raise ValueError("parameters")
    summary = value["anchor_summary"]
    if set(summary) != {"wheel_anchor_count", "prime_count", "composite_count",
                        "prime_counts_by_R210", "composite_counts_by_R210"}:
        raise ValueError("summary")
    ap, ac = summary["prime_counts_by_R210"], summary["composite_counts_by_R210"]
    if any(type(v) is not list or len(v) != 48 or
           any(not strict_int(x) or x < 0 for x in v) for v in (ap, ac)):
        raise ValueError("class array")
    np, nc, nx = summary["prime_count"], summary["composite_count"], summary["wheel_anchor_count"]
    if any(not strict_int(n) or n < 0 for n in (np, nc, nx)) or \
            (sum(ap), sum(ac), np + nc) != (np, nc, nx):
        raise ValueError("conservation")
    if type(value["families"]) is not list or len(value["families"]) != 1:
        raise ValueError("family count")
    f = value["families"][0]
    keys = {"family", "prime_mode_count", "highest_competing_prime_count",
            "strict_unique_prime_mode", "candidate_signature", "evaluated_signature",
            "target_prime_count", "target_composite_count", "population_floor_passed",
            "class_floor_passed", "occurrence_floor_passed", "mixed_class_count",
            "mixed_class_floor_passed", "positive_class_count",
            "positive_class_floor_passed", "target_enrichment_numerator",
            "target_enrichment_positive", "triviality_veto_passed", "mechanically_eligible"}
    if type(f) is not dict or set(f) != keys or f["family"] != "F1":
        raise ValueError("family fields")
    flags = ("strict_unique_prime_mode", "population_floor_passed", "class_floor_passed",
             "occurrence_floor_passed", "mixed_class_floor_passed",
             "positive_class_floor_passed", "target_enrichment_positive",
             "triviality_veto_passed", "mechanically_eligible")
    if any(type(f[name]) is not bool for name in flags):
        raise ValueError("flag types")
    if any(not strict_int(f[k]) or f[k] < 0 for k in
           ("prime_mode_count", "highest_competing_prime_count")):
        raise ValueError("mode counts")
    diagnostic = f["candidate_signature"]
    if diagnostic is not None and (not strict_int(diagnostic) or diagnostic not in STATES):
        raise ValueError("H25 diagnostic")
    if not strict_int(f["evaluated_signature"]) or f["evaluated_signature"] != 0:
        raise ValueError("H25 frozen target zero")
    if f["strict_unique_prime_mode"] and diagnostic != 0:
        raise ValueError("H25 strict target inconsistent with diagnostic")
    target_fields = ("target_prime_count", "target_composite_count", "mixed_class_count",
                     "positive_class_count", "target_enrichment_numerator")
    if any(not strict_int(f[k]) for k in target_fields):
        raise ValueError("H25 target types")
    if any(f[k] < 0 for k in target_fields[:-1]):
        raise ValueError("target count")
    if f["target_prime_count"] > np or f["target_composite_count"] > nc:
        raise ValueError("target conservation")
    if f["mixed_class_count"] > 48 or f["positive_class_count"] > 48:
        raise ValueError("class count")
    if f["target_enrichment_numerator"] != f["target_prime_count"] * nc - f["target_composite_count"] * np:
        raise ValueError("signed arithmetic")
    if f["target_enrichment_positive"] != (f["target_enrichment_numerator"] > 0):
        raise ValueError("signed bool")
    if f["occurrence_floor_passed"] != (f["target_prime_count"] >= 64):
        raise ValueError("occurrence")
    if f["mixed_class_floor_passed"] != (f["mixed_class_count"] >= 36) or f["positive_class_floor_passed"] != (f["positive_class_count"] >= 36):
        raise ValueError("H25 signed/mixed floors")
    if f["mechanically_eligible"] != all((
        f["strict_unique_prime_mode"], f["population_floor_passed"],
        f["class_floor_passed"], f["occurrence_floor_passed"],
        f["mixed_class_floor_passed"], f["positive_class_floor_passed"],
        f["target_enrichment_positive"], f["triviality_veto_passed"]
    )):
        raise ValueError("H25 exact frozen conjunction")
    if f["population_floor_passed"] != (np >= 2000 and nc >= 2000) or \
            f["class_floor_passed"] != all(a >= 20 and b >= 20 for a, b in zip(ap, ac, strict=True)):
        raise ValueError("class/population flags")
    if type(value["promotions"]) is not list or value["promotions"] != []:
        raise ValueError("H25 promotions always empty")\n

def run(implementation_commit: str, output: Path) -> bytes:
    design = Path("experiments/E025_THREE_ROW_YOUNG_TABLEAU_LINEAR_EXTENSION_REMAINDER_OCTILES.md").read_text()
    independent_small_checks()
    assert_plan(PLAN, design)
    generation_entry(0, PLAN, design, "H25")
    bases = low_base_sieve(BASE_STOP)
    generation_entry(1, PLAN, design, "D25")
    mask = direct_target_mask(LOW, HIGH, bases)
    if len(mask) != HIGH - LOW:
        raise ArithmeticError("target length")
    # Complete unconditional domain and all features BEFORE consulting one label.
    min_k, max_k = isqrt(LOW), isqrt(HIGH - 1)
    tableau = tableau_window(min_k, max_k)
    anchors: list[int] = []
    states = bytearray()
    positions: list[int] = []
    class_id = {r: i for i, r in enumerate(RESIDUES)}
    for x in range(LOW, HIGH):
        r = x % WHEEL
        if r in class_id:
            k = isqrt(x)
            anchors.append(x)
            states.append(signature(x, tableau[k]))
            positions.append(class_id[r])
    prime = [[0] * 8 for _ in RESIDUES]
    comp = [[0] * 8 for _ in RESIDUES]
    for x, t, i in zip(anchors, states, positions, strict=True):
        if mask[x - LOW]:
            prime[i][t] += 1
        else:
            comp[i][t] += 1
    family, promotions = candidate_analysis(prime, comp)
    # A literal integer-support set is formed ONLY after every F1 gate passes.
    # There are no previous eligible supports in this one-family bounded unit.
    if family["mechanically_eligible"]:
        target = 0
        witness = {x for x, t in zip(anchors, states, strict=True)
                   if t == target and mask[x - LOW]}
        if len(witness) != family["target_prime_count"] or not witness:
            raise ArithmeticError("H25 literal integer support mismatch")
        del witness
    np_a = [sum(row) for row in prime]
    nc_a = [sum(row) for row in comp]
    np, nc = sum(np_a), sum(nc_a)
    if np + nc != len(anchors) or any(
        sum(prime[i]) + sum(comp[i]) != positions.count(i) for i in range(48)
    ):
        raise ArithmeticError("frequency conservation")
    parameters = {"width": 2_000_000, "wheel": 210, "residues_R210": list(RESIDUES),
                  "rows": 3, "index_rule": "isqrt_x",
                  "object": "three_row_rectangular_standard_young_tableau_linear_extensions",
                  "modulus": "anchor_plus_one", "feature": "tableau_remainder_octile",
                  "signature_domain": list(STATES), "selector": "strict_unique_prime_frequency_mode",
                  "population_floor": 2000, "class_floor": 20,
                  "occurrence_floor": 64, "mixed_class_floor": 36,
                  "positive_class_floor": 36, "support_cap": 1,
                  "full_mixed_required": True}
    value = {
        "experiment": "E025",
        "implementation_commit": implementation_commit,
        "band": {"name": "D25", "range": [LOW, HIGH], "interval_semantics": "half-open"},
        "partition": [
            {"name": n, "range": [a, b], "role": role} for n, a, b, role in PARTITION
        ],
        "parameters": parameters,
        "generation_plan": [
            {"purpose": e[0], "start": e[1], "stop": e[2], "strategy": e[3]} for e in PLAN
        ],
        "anchor_summary": {
            "wheel_anchor_count": len(anchors), "prime_count": np,
            "composite_count": nc,
            "prime_counts_by_R210": np_a, "composite_counts_by_R210": nc_a
        },
        "families": [family], "promotions": promotions,
        "validation": {k: 0 for k in VALIDATORS},
    }
    payload_schema(value)
    raw = canonical(value)
    if b"\r" in raw or raw[-1:] != b"\n" or canonical(json.loads(raw)) != raw:
        raise ArithmeticError("canonical serialization")
    output.write_bytes(raw)
    return sha256(raw).digest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", required=True, choices=("H25",))
    parser.add_argument("--implementation-commit", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    if args.phase != "H25" or args.output != "/tmp/e025_h25_raw.json":
        raise PermissionError("forbidden phase/path")
    if not re.fullmatch("[a-f0-9]{40}", args.implementation_commit):
        raise ValueError("uncommitted source reference")
    run(args.implementation_commit, Path(args.output))


if __name__ == "__main__":
    main()
