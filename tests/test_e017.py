"""E017 synthetic and poisoned-plan pre-generation tests: never generate primes."""
import copy
import importlib.util
from collections import Counter
from math import gcd
from pathlib import Path

import pytest

PATH = Path(__file__).resolve().parents[1] / "experiments" / "E017_josephus_three_survivor_rank_shapes.py"
SPEC = importlib.util.spec_from_file_location("e017", PATH)
e = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(e)


def circle_survivor(n):
    """Independent deletion simulation only for bounded fabricated small circles."""
    seats = list(range(n))
    index = 0
    while len(seats) > 1:
        index = (index + 2) % len(seats)
        seats.pop(index)
    return seats[0]


def test_small_reference_recurrence_and_circle_identity():
    assert [e.josephus_fast(n) for n in range(1, 6)] == [0, 1, 1, 0, 3]
    for n in range(1, 512):
        assert circle_survivor(n) == e.josephus_reference(n) == e.josephus_fast(n)
        if n > 1:
            assert e.josephus_fast(n) == (e.josephus_fast(n - 1) + 3) % n
    for x in (0, -1, 0.5, True):
        with pytest.raises(ValueError):
            e.josephus_fast(x)
    with pytest.raises(ValueError):
        e.josephus_reference(4097)


def test_large_exact_integer_floor_full_domain_and_no_float():
    found = [set(), set()]
    for n in range(1, 500):
        j = e.josephus_fast(n)
        a, b = e.signatures(n)
        assert (a, b) == (4 * j // n, 8 * j // n)
        assert a == b // 2
        found[0].add(a)
        found[1].add(b)
    assert found == [set(range(4)), set(range(8))]
    assert [len(d) for d in e.DOMAINS] == [4, 8]
    n = 10**30 + 57
    a, b = e.signatures(n)
    assert (a, b) == (4 * e.josephus_fast(n) // n, 8 * e.josephus_fast(n) // n)


def test_wheel_and_full_interval_metadata():
    assert e.R210 == tuple(r for r in range(210) if gcd(r, 210) == 1)
    assert len(e.R210) == 48
    assert len(e.EARLY_ROLES) == 53
    assert len(e.LATER_ROLES) == 20
    assert len(e.historical_intervals()) == 79
    assert e.audit_partition() == (3081, 405, 30, 150)
    assert e.ROLES[4][1] == 2 * e.ROLES[1][1]
    assert e.isqrt(90_999_999) == 9539
    assert e.isqrt(93_999_999) == 9695
    assert e.isqrt(180_999_999) == 13453
    assert e.D17_PLAN == (("base_sieve_support", 0, 9540, "whole_prefix"),
                          ("segmented_target", 90_000_000, 91_000_000, "direct_segmented"))


def invented_tables(target_p=22, target_c=12, population=30):
    """Artificial signature/class populations; identifiers are invented, not primes."""
    pc, cc = [Counter(), Counter()], [Counter(), Counter()]
    pb = [[Counter() for _ in range(48)] for _ in range(2)]
    cb = [[Counter() for _ in range(48)] for _ in range(2)]
    supports = [{}, {}]
    for r in range(48):
        for is_p in (True, False):
            target = target_p if is_p else target_c
            assert 0 <= target <= population
            amounts = (target, (population - target) // 2,
                       population - target - (population - target) // 2)
            for (a, b), amount in zip(((1, 2), (0, 1), (3, 6)), amounts):
                for i, t in enumerate((a, b)):
                    (pc if is_p else cc)[i][t] += amount
                    (pb if is_p else cb)[i][r][t] += amount
                    if is_p:
                        old = len(supports[i].get(t, set()))
                        supports[i].setdefault(t, set()).update(r * 10000 + k for k in range(old, old + amount))
    return pc, cc, pb, cb, [population] * 48, [population] * 48, supports


def test_unique_mode_ties_and_no_runner_up_fallback():
    assert e.strict_mode(Counter({0: 50, 1: 40}), e.DOMAINS[0]) == (0, 50, 40)
    assert e.strict_mode(Counter({0: 50, 1: 50, 2: 1}), e.DOMAINS[0]) == (None, 50, 50)
    assert e.strict_mode(Counter(), e.DOMAINS[1]) == (None, 0, 0)
    with pytest.raises(ValueError):
        e.strict_mode(Counter({99: 1}), e.DOMAINS[0])
    pc, cc, pb, cb, p_by, c_by, supports = invented_tables()
    assert e.strict_mode(pc[0], e.DOMAINS[0])[0] == 1
    # Tied best prime signatures must NOT replace target with runner-up.
    pc[0][0] = pc[0][1]
    # preserve all consistency by moving invented counts from third signature.
    diff = pc[0][0] - (48 * 4)
    pc[0][3] -= diff
    for r in range(48):
        pb[0][r][0] += diff // 48
        pb[0][r][3] -= diff // 48
    # This example only tests the isolated complete-domain selection rule.
    assert e.strict_mode(pc[0], e.DOMAINS[0])[0] is None


def test_signed_mixed_48_class_and_integer_gate_thresholds():
    pc, cc, pb, cb, p_by, c_by, supports = invented_tables()
    assert e.exact_enrichment(22, 12, 30, 30) == 300
    assert e.exact_enrichment(12, 22, 30, 30) == -300
    assert e.exact_enrichment(10, 10, 30, 30) == 0
    assert e.class_metrics(1, pb[0], cb[0], p_by, c_by) == (48, 48)
    fs, ps = e.summarize(pc, cc, pb, cb, p_by, c_by, supports)
    assert [p["family"] for p in ps] == ["J1"]  # identical full sets suppress J2
    assert len(fs) == 2 and fs[0]["mechanically_eligible"] and not fs[1]["mechanically_eligible"]
    for r in range(48):
        cb[0][r][1] = 10 if r < 30 else 25
    assert e.class_metrics(1, pb[0], cb[0], p_by, c_by) == (48, 30)
    for r in range(12):
        pb[0][r][1] = p_by[r]
    assert e.class_metrics(1, pb[0], cb[0], p_by, c_by)[0] == 36
    pb[0][12][1] = p_by[12]
    assert e.class_metrics(1, pb[0], cb[0], p_by, c_by)[0] == 35


def test_population_class_occurrence_floor_and_empty_promotion():
    pc, cc, pb, cb, p_by, c_by, supports = invented_tables(target_p=8, target_c=3, population=9)
    fs, ps = e.summarize(pc, cc, pb, cb, p_by, c_by, supports)
    assert ps == []
    assert all(not f["population_floor_passed"] and not f["class_floor_passed"] for f in fs)
    pc, cc, pb, cb, p_by, c_by, supports = invented_tables(target_p=1, target_c=0, population=30)
    fs, ps = e.summarize(pc, cc, pb, cb, p_by, c_by, supports)
    assert ps == []
    assert all(not f["occurrence_floor_passed"] or not f["aggregate_enrichment_positive"] for f in fs)
    blank = [Counter(), Counter()]
    by = [[Counter() for _ in range(48)] for _ in range(2)]
    fs, ps = e.summarize(blank, blank, by, by, [0] * 48, [0] * 48, [{}, {}])
    assert ps == [] and all(f["unique_mode_signature"] is None for f in fs)
    assert all(f["prime_mode_count"] == f["highest_competing_count"] == 0 for f in fs)


def test_exact_prime_support_set_duplicate_not_count_and_cap():
    assert e.select_duplicates([("J1", {1, 2}), ("J2", {1, 2})]) == ["J1"]
    assert e.select_duplicates([("J1", {1, 2}), ("J2", {3, 4})]) == ["J1", "J2"]
    with pytest.raises(ValueError):
        e.select_duplicates([("J1", [1, 2])])
    with pytest.raises(ValueError):
        e.select_duplicates([("J1", {1}), ("J2", {2}), ("BAD", {3})])


def sample_payload():
    blank = [Counter(), Counter()]
    by = [[Counter() for _ in range(48)] for _ in range(2)]
    fs, ps = e.summarize(blank, blank, by, by, [0] * 48, [0] * 48, [{}, {}])
    return dict(experiment="E017", implementation_commit="a" * 40,
                band=dict(name="D17", range=[90_000_000, 91_000_000], interval_semantics="half-open"),
                partition=[dict(name=n, range=[a, b], role=role) for n, a, b, role in e.ROLES],
                parameters=e.PARAMETERS, generation_plan=e.expected_plan(),
                anchor_summary=dict(wheel_anchor_count=0, prime_count=0, composite_count=0,
                                    prime_counts_by_R210=[0] * 48, composite_counts_by_R210=[0] * 48),
                validation=dict.fromkeys(e.VALIDATION_KEYS, 0), families=fs, promotions=ps)


def test_canonical_strict_schema_extra_nested_and_types_rejected():
    original = sample_payload()
    raw = e.serialize(original)
    assert raw == e.serialize(copy.deepcopy(original))
    assert raw == (e.json.dumps(original, sort_keys=True, indent=2, ensure_ascii=True) + "\n").encode()
    assert raw.endswith(b"\n") and not raw.endswith(b"\n\n")
    changes = (
        lambda x: x.update(primes=[2, 3]),
        lambda x: x["band"].update(extra=0),
        lambda x: x["partition"][0].update(extra="no"),
        lambda x: x["parameters"].update(josephus_step=2),
        lambda x: x["generation_plan"][1].update(high_helper=True),
        lambda x: x["anchor_summary"]["prime_counts_by_R210"].append(0),
        lambda x: x["validation"].update(plan_failure_count=1),
        lambda x: x["validation"].update(plan_failure_count=False),
        lambda x: x["families"][0].update(extra="forbidden"),
        lambda x: x["families"][0].update(prime_mode_count=True),
        lambda x: x["families"][0].update(strict_unique_prime_mode=1),
        lambda x: x["promotions"].append(dict(family="J1")),
    )
    for change in changes:
        payload = copy.deepcopy(original)
        change(payload)
        with pytest.raises(ValueError):
            e.serialize(payload)


def test_poison_all_old_nested_new_and_adversarial_plans():
    def poison(_):
        raise AssertionError("GENERATOR ENTERED")

    good = e.expected_plan()
    assert e.validate_plan("D17", good)
    malformed = [None, (), [], good[:1], good + [good[-1]], good[::-1],
                 [good[0], good[0]], [good[1], good[1]],
                 [dict(good[0], stop=9539), good[1]],
                 [dict(good[0], stop=9541), good[1]],
                 [dict(good[0], start=1), good[1]],
                 [dict(good[0], strategy="direct_segmented"), good[1]],
                 [dict(good[0], stop=91_000_000), good[1]],
                 [good[0], dict(good[1], start=90_000_001)],
                 [good[0], dict(good[1], stop=90_999_999)],
                 [good[0], dict(good[1], start=89_999_999)],
                 [good[0], dict(good[1], stop=91_000_001)],
                 [good[0], dict(good[1], strategy="whole_prefix")],
                 [good[0], dict(good[1], strategy="segmented")],
                 [good[0], dict(good[1], purpose="base_sieve_support")],
                 [good[0], dict(good[1], high_helper=True)],
                 [good[0], dict(good[1], start=True)],
                 [good[0], dict(good[1], stop=91_000_000.0)]]
    for _, a, b in e.historical_intervals():
        malformed.append([good[0], dict(good[1], start=a, stop=b)])
    for _, a, b, _ in e.ROLES:
        if (a, b) != (90_000_000, 91_000_000):
            malformed.append([good[0], dict(good[1], start=a, stop=b)])
    for a in e.CALIBRATION_STARTS:
        for width in e.WIDTHS:
            malformed.append([good[0], dict(good[1], start=a, stop=a + width)])
    assert len(malformed) >= 79 + 4 + 30
    for plan in malformed:
        with pytest.raises(ValueError):
            e.generator_entry("D17", plan, 0, poison)
    for phase in ("H17", "A17", "D16", "", None):
        with pytest.raises(ValueError):
            e.generator_entry(phase, good, 0, poison)
    for i in (-1, 2, True, 0.0):
        with pytest.raises(ValueError):
            e.generator_entry("D17", good, i, poison)
    with pytest.raises(AssertionError, match="GENERATOR ENTERED"):
        e.generator_entry("D17", good, 0, poison)
