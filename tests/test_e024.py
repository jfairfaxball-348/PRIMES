"""E024 generator-free independent RREF, quotient, typed schema and poison tests."""
import copy
import importlib.util
import json
from itertools import combinations, product
from math import gcd, isqrt
from pathlib import Path

import pytest

PATH = (Path(__file__).resolve().parents[1] / "experiments" /
        "E024_binary_grassmannian_rank_residue_order_shapes.py")
spec = importlib.util.spec_from_file_location("e024", PATH)
e = importlib.util.module_from_spec(spec)
spec.loader.exec_module(e)


def independent_spaces(n, k):
    """Independent canonical matrices with arbitrary free binary entries."""
    unique = set()
    for pivots in combinations(range(n), k):
        positions = [(r, c) for r in range(k)
                     for c in range(n)
                     if c not in pivots and c > pivots[r]]
        for vector in product((0, 1), repeat=len(positions)):
            rows = [1 << p for p in pivots]
            for (r, c), bit in zip(positions, vector, strict=True):
                if bit:
                    rows[r] |= 1 << c
            unique.add(tuple(rows))
    return len(unique)


def gaussian_via_integer_orbits(n, k):
    numerator = 1
    denominator = 1
    for j in range(k):
        numerator *= (2 ** (n - j) - 1)
        denominator *= (2 ** (k - j) - 1)
    assert numerator % denominator == 0
    return numerator // denominator


def test_small_rref_independent_gaussian_pascal_and_four_fixed_ordinals():
    pairs = {3: (7, 1, 2), 4: (35, 15, 1),
             5: (155, 155, 1), 6: (651, 1395, 0)}
    for n in range(3, 7):
        a, b, t = pairs[n]
        for k, expected in ((2, a), (3, b)):
            assert independent_spaces(n, k) == expected
            assert gaussian_via_integer_orbits(n, k) == expected
            assert e.rref_enumerator(n, k) == expected
            assert e.gaussian_pascal(n, k) == expected
        assert e.signature(n) == t
        assert e.signature(n) == e.order_from_remainders(
            n, a % (n + 1), b % (n + 1))
    assert e.self_checks() == (0, 0, 0)


def test_modular_integer_quotient_and_binary_exponent_edges():
    for x in range(3, 111):
        for k in (2, 3):
            d = 3 if k == 2 else 21
            product_int = 1
            for j in range(k):
                product_int *= (2 ** (x - j) - 1)
            assert product_int % d == 0
            expected = (product_int // d) % (x + 1)
            assert e.subspace_remainder(x, k) == expected
            assert e.subspace_remainder(x, k) == e.full_gaussian(x, k) % (x + 1)
        r2, r3 = (e.subspace_remainder(x, k) for k in (2, 3))
        assert e.signature(x) == (0 if r2 < r3 else (1 if r2 == r3 else 2))
    for exp in range(21):
        for m in (1, 2, 3, 5, 21, 209, 1131):
            assert e.pow_mod_two(exp, m) == pow(2, exp, m)
    for n in (3, 4, 111):
        for r2, r3 in ((0, 0), (0, n), (n, 0), (n, n)):
            assert e.order_from_remainders(n, r2, r3) in (0, 1, 2)
    assert {e.order_from_remainders(5, x, y) for x in range(6)
            for y in range(6)} == {0, 1, 2}
    for x, k in ((True, 2), (3.4, 2), (2, 2), (3, 1),
                 (3, 4), (3, True), (0, 3)):
        with pytest.raises(ValueError):
            e.subspace_remainder(x, k)
    for n, a, b in ((3, True, 1), (3, -1, 0), (3, 4, 0),
                    (2, 0, 0), (3, 0, 4)):
        with pytest.raises(ValueError):
            e.order_from_remainders(n, a, b)
    for exp, mod in ((-1, 3), (1, 0), (True, 3), (3, 0.5)):
        with pytest.raises(ValueError):
            e.pow_mod_two(exp, mod)


def test_role_provenance_114_old_30_nested_five_roles_and_isqrt():
    assert len(e.EARLY.strip().splitlines()) == 53
    assert len(e.FIVE_ROLE) == 11
    assert [name for name, *_ in e.prior_roles() if name.startswith("E023-")] == [
        "E023-G-pre", "E023-D", "E023-G-mid", "E023-H", "E023-A"
    ]
    assert e.audit_intervals() == {
        "old_old": 6441, "new_old": 570, "new_new": 10,
        "new_nested": 150, "old_non_e005_nested": 3240,
        "nested_contained": 30, "nested_within": 60, "nested_across": 375,
    }
    assert e.allocation(182000000) == tuple((a, b) for _, a, b, _ in e.ROLES)
    for high, stop in ((186000000, 13639), (190000000, 13785),
                       (370000000, 19236)):
        root = isqrt(high - 1)
        assert root + 1 == stop
        assert root**2 <= high - 1 < (root + 1)**2
    assert e.R210 == tuple(r for r in range(210) if gcd(r, 210) == 1)


def test_complete_generator_plan_negative_poison_family_no_sieve():
    base = e.PLAN
    assert base == (("base_sieve_support", 0, 13639, "whole_prefix"),
                    ("segmented_target", 184000000, 186000000, "direct_segmented"))
    poison = [(), (base[0],), (base[1], base[0]),
              base + (base[1],), (base[0], base[0]),
              [base[0], base[1]], (list(base[0]), base[1])]
    for idx, variants in ((0, ("auxiliary", -1, 1, 13638, 13640,
                              "direct_segmented", "whole-prefix")),
                          (1, ("H24", 183999999, 184000001, 185999999,
                               186000001, 188000000, 190000000,
                               368000000, 370000000, 166000000, 168000000,
                               "whole_prefix", "helper_segmented", "indirect"))):
        for variant in variants:
            changed = list(base)
            row = list(changed[idx])
            for col in range(4):
                new = row[:]
                new[col] = variant
                changed[idx] = tuple(new)
                poison.append(tuple(changed))
    for plan in poison:
        with pytest.raises((ValueError, TypeError)):
            e.GeneratorGate(plan=plan)
    for phase in ("H24", "A24", "D23", "D22", "H19", "G24-pre", "", None):
        with pytest.raises(ValueError):
            e.GeneratorGate(phase=phase)
    for args in ({"indirect": True}, {"per_anchor": True},
                 {"indirect": 1}, {"per_anchor": 1}):
        with pytest.raises(ValueError):
            e.GeneratorGate(**args)
    gate = e.GeneratorGate()
    with pytest.raises(ValueError):
        gate.enter(1, *base[1])
    with pytest.raises(ValueError):
        gate.enter(0, "base_sieve_support", 0, 13640, "whole_prefix")
    gate.enter(0, *base[0])
    with pytest.raises(ValueError):
        gate.enter(0, *base[0])
    with pytest.raises(ValueError):
        gate.enter(True, *base[1])
    with pytest.raises(ValueError):
        gate.enter(1, "segmented_target", 188000000, 190000000,
                   "direct_segmented")
    gate.enter(1, *base[1])
    gate.finished()
    with pytest.raises(ValueError):
        gate.enter(1, *base[1])
    incomplete = e.GeneratorGate()
    with pytest.raises(ValueError):
        incomplete.finished()
    tampered = e.GeneratorGate()
    tampered.plan = (base[1], base[0])
    with pytest.raises(ValueError):
        tampered.enter(0, *base[0])


def empty_payload():
    family = dict(
        family="F1", prime_mode_count=0, highest_competing_prime_count=0,
        strict_unique_prime_mode=False, candidate_signature=None,
        evaluated_signature=None, target_prime_count=None,
        target_composite_count=None, population_floor_passed=False,
        class_floor_passed=False, occurrence_floor_passed=False,
        mixed_class_count=None, mixed_class_floor_passed=False,
        positive_class_count=None, positive_class_floor_passed=False,
        target_enrichment_numerator=None, target_enrichment_positive=False,
        triviality_veto_passed=False, mechanically_eligible=False,
    )
    payload = dict(
        experiment="E024", implementation_commit="a"*40,
        band={"name": "D24", "range": [184000000, 186000000],
              "interval_semantics": "half-open"},
        partition=[dict(name=n, range=[a, b], role=r)
                   for n, a, b, r in e.ROLES],
        parameters=copy.deepcopy(e.PARAMETERS),
        generation_plan=e.plan_dicts(),
        anchor_summary=dict(
            wheel_anchor_count=0, prime_count=0, composite_count=0,
            prime_counts_by_R210=[0]*48, composite_counts_by_R210=[0]*48),
        validation=dict.fromkeys(e.VALIDATORS, 0),
        families=[family], promotions=[],
    )
    return payload


def test_recursive_typed_exact_ten_key_schema_and_strict_canonical_bytes():
    obj = empty_payload()
    assert e.validate_payload(obj)
    raw = e.canonical(obj)
    assert raw.endswith(b"\n") and not raw.endswith(b"\n\n")
    assert raw == (json.dumps(obj, sort_keys=True, indent=2,
                             ensure_ascii=True) + "\n").encode("ascii")
    assert e.validate_payload(json.loads(raw))
    for edits in (
        lambda d: d.update(extra=1),
        lambda d: d["validation"].update(extra=0),
        lambda d: d["validation"].update(plan_failure_count=True),
        lambda d: d["validation"].update(plan_failure_count=1),
        lambda d: d["band"].update(name="H24"),
        lambda d: d["band"].update(range=[184000000, 185999999]),
        lambda d: d["generation_plan"].reverse(),
        lambda d: d["parameters"].update(wheel=True),
        lambda d: d["parameters"].update(denominators=[21, 3]),
        lambda d: d["parameters"].update(extra="open"),
        lambda d: d["anchor_summary"].update(prime_count=True),
        lambda d: d["anchor_summary"].update(prime_counts_by_R210=[0]*47),
        lambda d: d["families"][0].update(candidate_signature=True),
        lambda d: d["families"][0].update(mixed_class_count=0),
        lambda d: d["families"][0].update(mechanically_eligible=True),
        lambda d: d["families"][0].update(family="R1"),
        lambda d: d.update(promotions=[{"target_signature": 0}]),
    ):
        changed = copy.deepcopy(obj)
        edits(changed)
        assert not e.validate_payload(changed)


def test_mode_support_and_pure_holdout_criterion_without_h24_data():
    assert e.strict_mode([9, 2, 3]) == (0, 9, 3)
    assert e.strict_mode([1, 9, 3]) == (1, 9, 3)
    assert e.strict_mode([1, 2, 9]) == (2, 9, 2)
    assert e.strict_mode([4, 4, 1]) == (None, 4, 4)
    for bad in ([1, 2], [1, True, 3], [1, -1, 3], (1, 2, 3)):
        with pytest.raises(ValueError):
            e.strict_mode(bad)
    pure = dict(frozen_target=2, strict_unique_mode=2,
                np=3000, nc=3000,
                class_populations=[(30, 30)]*48,
                target_prime_count=64, mixed_class_count=36,
                positive_class_count=36, target_enrichment_numerator=1,
                triviality_veto_passed=True, all_replay_checks_passed=True)
    assert e.evaluate_h24_refutation(pure, 2)
    for key, value in (("frozen_target", 1),
                       ("positive_class_count", 35),
                       ("target_enrichment_numerator", 0),
                       ("mixed_class_count", 35)):
        changed = dict(pure)
        changed[key] = value
        assert not e.evaluate_h24_refutation(changed, 2)
