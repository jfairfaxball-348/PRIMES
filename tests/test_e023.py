"""E023 independent tiny distinct-subset, typed-schema and generator-poison tests."""
import copy
import importlib.util
from itertools import combinations
from math import gcd, isqrt
from pathlib import Path

import pytest

PATH = (Path(__file__).resolve().parents[1] / "experiments" /
        "E023_distinct_summand_partition_triangular_shell_rank_shapes.py")
spec = importlib.util.spec_from_file_location("e023", PATH)
e = importlib.util.module_from_spec(spec)
spec.loader.exec_module(e)


def test_exact_distinct_summand_one_use_and_formal_product():
    q = e.distinct_counts(18)
    by_subsets = []
    for n in range(19):
        count = 0
        for size in range(n + 1):
            for parts in combinations(range(1, n + 1), size):
                if sum(parts) == n:
                    count += 1
        by_subsets.append(count)
    assert q == by_subsets == e.finite_product_counts(18)
    assert q[:10] == [1, 1, 1, 2, 2, 3, 4, 5, 6, 8]
    # Ascending, unbounded-part recurrence is *not* the one-use object.
    unlimited = [1] + [0]*18
    for j in range(1, 19):
        for n in range(j, 19):
            unlimited[n] += unlimited[n - j]
    assert unlimited[2] != q[2]
    assert e.self_checks() == (0, 0, 0)


def test_triangular_threshold_integer_boundaries_and_parity():
    for x in range(1, 5000):
        k, r = e.triangular(x)
        assert k*(k + 1)//2 <= x < (k + 1)*(k + 2)//2
        assert r == x - k*(k + 1)//2
        assert 0 <= r <= k
        assert (k*(k + 1)//2 + r) % 2 == x % 2
    for k in range(1, 90):
        t = k*(k + 1)//2
        assert e.triangular(t) == (k, 0)
        assert e.triangular(t + k) == (k, k)
        if t > 1:
            assert e.triangular(t - 1) == (k - 1, k - 1)
    for invalid in (-1, 0, 0.5, True):
        with pytest.raises(ValueError):
            e.triangular(invalid)
    for hi, low in ((168000000, 12962), (172000000, 13115),
                    (334000000, 18276)):
        s = isqrt(hi - 1)
        assert s*s <= hi - 1 < (s + 1)**2 and s + 1 == low


def test_complete_dense_weak_order_13_with_equalities_and_reductions():
    actual = {e.dense_rank((a, b, c)) for a in range(5)
              for b in range(5) for c in range(5)}
    assert len(actual) == 13
    assert actual == set(e.SIGNATURES)
    assert list(e.SIGNATURES) == sorted(e.SIGNATURES)
    q = e.distinct_counts(40)
    for x in range(1, 40):
        word, k, r = e.feature(x, q)
        values = tuple(q[r + j] % (x + 1) for j in range(3))
        distinct = set(values)
        independently = tuple(sum(a < v for a in distinct) for v in values)
        assert word == independently and word in actual
        assert r == x - k*(k + 1)//2
    for bad in ((0, 0), (0, -1, 1), (False, 0, 1), [0, 1, 2]):
        with pytest.raises(ValueError):
            e.dense_rank(bad)


def test_109_named_plus_30_nested_and_first_eligible_allocation():
    old = e.prior_roles()
    assert len(e.EARLY.strip().splitlines()) == 53
    assert len(e.FIVE_ROLE) == 10
    assert len(old) == 109
    assert e.audit_intervals() == dict(
        old_old=5886, new_old=545, new_new=10,
        new_nested=150, old_non_e005_nested=3090,
        nested_contained=30, nested_within=60, nested_across=375)
    assert e.allocation(164000000) == tuple(
        (a, b) for _, a, b, _ in e.ROLES)
    assert e.allocation(162000000)[0] == (162000000, 164000000)
    assert e.overlaps(e.allocation(162000000)[0], (162000000, 163000000))
    assert e.R210 == tuple(n for n in range(210) if gcd(n, 210) == 1)
    assert e.PLAN == (
        ("base_sieve_support", 0, 12962, "whole_prefix"),
        ("segmented_target", 166000000, 168000000, "direct_segmented"))


def test_all_forbidden_plans_poisoned_before_any_generator(monkeypatch):
    def poison(*args, **kwargs):
        raise AssertionError("protected prime generator reached")
    monkeypatch.setattr(e, "base_sieve", poison)
    monkeypatch.setattr(e, "segmented_target", poison)
    p = e.PLAN
    negatives = [
        p[::-1], p[:1], p + (p[1],),
        (p[0], p[1][:3]), (p[0], p[0]),
        (("base_sieve_support", 0, 168000000, "whole_prefix"), p[1]),
        (("base_sieve_support", 0, 12962, "direct_segmented"), p[1]),
        (("hidden_support", 0, 12962, "whole_prefix"), p[1]),
        (p[0], ("segmented_target", 166000000, 168000000, "whole_prefix")),
        (p[0], ("segmented_target", 166000000, 167000000, "direct_segmented")),
        (p[0], ("segmented_target", 167000000, 168000000, "direct_segmented")),
        (p[0], ("segmented_target", 166000000, 168000001, "direct_segmented")),
        (p[0], ("segmented_target", 165999999, 168000000, "direct_segmented")),
        (p[0], ("segmented_target", 170000000, 172000000, "direct_segmented")),
        (p[0], ("segmented_target", 332000000, 334000000, "direct_segmented")),
        (p[0], ("segmented_target", True, 168000000, "direct_segmented")),
    ]
    for i in (0, 1):
        for field in (1, 2):
            for diff in (-1, 1):
                changed = [list(x) for x in p]
                changed[i][field] += diff
                negatives.append(tuple(tuple(row) for row in changed))
    for _, a, b in e.prior_roles():
        negatives.append((p[0], ("segmented_target", a, b, "direct_segmented")))
    for n, a, b, _ in e.ROLES:
        if n != "D23":
            negatives.append((p[0], ("segmented_target", a, b, "direct_segmented")))
    for s in e.E005_STARTS:
        for w in e.E005_WIDTHS:
            negatives.append((p[0], ("segmented_target", s, s+w, "direct_segmented")))
    for plan in negatives:
        with pytest.raises(ValueError):
            e.GeneratorGate(plan=plan)
    for phase in ("H23", "A23", "G23-pre", "G23-mid", "D22",
                  "D21", "D20", "H19", "G22-pre", "D19", "A15"):
        with pytest.raises(ValueError):
            e.GeneratorGate(phase=phase)
    for opts in ({"indirect": True}, {"per_anchor": True},
                 {"indirect": 1}, {"per_anchor": 0}):
        with pytest.raises(ValueError):
            e.GeneratorGate(**opts)
    assert len(negatives) >= 155


def test_exact_entry_order_recheck_and_no_indirect_generator():
    gate = e.GeneratorGate()
    with pytest.raises(ValueError):
        gate.enter(1, *e.PLAN[1])
    with pytest.raises(ValueError):
        gate.enter(0, "base_sieve_support", 0, 12961, "whole_prefix")
    gate.enter(0, *e.PLAN[0])
    with pytest.raises(ValueError):
        gate.enter(0, *e.PLAN[0])
    gate.enter(1, *e.PLAN[1])
    gate.finished()
    with pytest.raises(ValueError):
        gate.enter(1, *e.PLAN[1])
    gate = e.GeneratorGate()
    with pytest.raises(ValueError):
        gate.finished()
    gate.plan = ()
    with pytest.raises(ValueError):
        gate.enter(0, *e.PLAN[0])


def test_direct_segmented_tiny_unprotected_against_trial_division():
    low = [p for p in range(2, 17) if all(p % d for d in range(2, p))]
    marks = e.segmented_target(103, 201, low)
    check = [n >= 2 and all(n % d for d in range(2, isqrt(n) + 1))
             for n in range(103, 201)]
    assert list(map(bool, marks)) == check


def example_object():
    f = dict(
        family="P1", prime_mode_count=0, highest_competing_prime_count=0,
        strict_unique_prime_mode=False, candidate_signature=None,
        evaluated_signature=None, target_prime_count=None,
        target_composite_count=None, population_floor_passed=False,
        class_floor_passed=False, occurrence_floor_passed=False,
        mixed_class_count=None, mixed_class_floor_passed=False,
        positive_class_count=None, positive_class_floor_passed=False,
        target_enrichment_numerator=None, target_enrichment_positive=False,
        triviality_veto_passed=False, mechanically_eligible=False,
    )
    return dict(
        experiment="E023", implementation_commit="a"*40,
        band=dict(name="D23", range=[166000000, 168000000],
                  interval_semantics="half-open"),
        partition=[dict(name=n, range=[a, b], role=role) for n, a, b, role
                   in e.ROLES],
        parameters=e.PARAMETERS, generation_plan=e.plan_dicts(),
        anchor_summary=dict(
            wheel_anchor_count=192, prime_count=96, composite_count=96,
            prime_counts_by_R210=[2]*48, composite_counts_by_R210=[2]*48),
        validation=dict.fromkeys(e.VALIDATORS, 0),
        families=[f], promotions=[],
    )


def test_strict_nested_typed_ten_key_serializer_and_poison():
    data = example_object()
    assert e.validate_payload(data)
    raw = e.canonical(data)
    assert raw == e.canonical(__import__("json").loads(raw))
    assert raw.endswith(b"\n") and not raw.endswith(b"\n\n")
    poisons = []
    bad = copy.deepcopy(data)
    bad["additional"] = 1
    poisons.append(bad)
    bad = copy.deepcopy(data)
    bad["validation"]["serializer_replay_failure_count"] = False
    poisons.append(bad)
    bad = copy.deepcopy(data)
    bad["parameters"]["wheel"] = True
    poisons.append(bad)
    bad = copy.deepcopy(data)
    bad["parameters"]["residues_R210"][0] = True
    poisons.append(bad)
    bad = copy.deepcopy(data)
    bad["band"]["range"][0] = 166000000.0
    poisons.append(bad)
    bad = copy.deepcopy(data)
    bad["anchor_summary"]["prime_count"] = True
    poisons.append(bad)
    bad = copy.deepcopy(data)
    bad["anchor_summary"]["prime_counts_by_R210"][0] = -1
    poisons.append(bad)
    bad = copy.deepcopy(data)
    bad["families"][0]["candidate_signature"] = [0, 1, True]
    poisons.append(bad)
    bad = copy.deepcopy(data)
    bad["families"][0]["extra"] = "hidden"
    poisons.append(bad)
    bad = copy.deepcopy(data)
    bad["families"][0]["target_prime_count"] = 10
    poisons.append(bad)
    bad = copy.deepcopy(data)
    bad["promotions"] = [{}]
    poisons.append(bad)
    bad = copy.deepcopy(data)
    del bad["generation_plan"]
    poisons.append(bad)
    bad = copy.deepcopy(data)
    bad["families"][0]["strict_unique_prime_mode"] = True
    poisons.append(bad)
    assert all(not e.validate_payload(bad) for bad in poisons)


def test_strict_selector_exact_support_and_frozen_holdout_gate():
    assert e.strict_mode([3, 3] + [0]*11) == (None, 3, 3)
    assert e.strict_mode([1, 4] + [0]*11) == (1, 4, 1)
    assert e.strict_mode([1, 3, 8] + [0]*10) == (2, 8, 3)
    assert e.strict_mode([0]*13) == (None, 0, 0)
    target = e.SIGNATURES[1]
    frozen = dict(
        frozen_target=target, strict_unique_mode=target, np=2000, nc=2000,
        class_populations=[(20, 20)]*48, target_prime_count=64,
        mixed_class_count=36, positive_class_count=36,
        target_enrichment_numerator=1, triviality_veto_passed=True,
        all_replay_checks_passed=True,
    )
    assert e.evaluate_h23_refutation(frozen, target)
    for key, value in (
        ("strict_unique_mode", e.SIGNATURES[2]),
        ("np", 1999), ("nc", 1999), ("target_prime_count", 63),
        ("mixed_class_count", 35), ("positive_class_count", 35),
        ("target_enrichment_numerator", 0),
        ("triviality_veto_passed", False),
        ("all_replay_checks_passed", False),
    ):
        wrong = dict(frozen, **{key: value})
        assert not e.evaluate_h23_refutation(wrong, target)
    with pytest.raises(ValueError):
        e.evaluate_h23_refutation(frozen, (2, 2, 2))


def test_injected_failure_suppresses_target_and_zero_validators():
    obj = example_object()
    for key in e.VALIDATORS:
        bad = copy.deepcopy(obj)
        bad["validation"][key] = 1
        assert not e.validate_payload(bad)
    bad = copy.deepcopy(obj)
    bad["families"][0]["mechanically_eligible"] = True
    assert not e.validate_payload(bad)
