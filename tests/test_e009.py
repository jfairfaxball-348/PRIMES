from __future__ import annotations

from collections import Counter
from copy import deepcopy
from math import gcd, lcm

import pytest

from experiments.E009_unit_action_cover_shapes import (
    ANCHOR_SUMMARY_KEYS,
    BASIS,
    BANDS,
    EXCLUDED_RANGES,
    FAMILY_ORDER,
    FAMILY_ROW_KEYS,
    FROZEN_PARTITION,
    OCCURRENCE_FLOOR,
    PAYLOAD_KEYS,
    POPULATION_FLOOR,
    PROMOTION_CAP,
    Q,
    SUBSETS,
    VALIDATION_KEYS,
    WIDTH,
    _family_row,
    _signature_sort_key,
    apply_duplicate_suppression,
    cover_flags,
    cover_monotonicity_holds,
    cover_shape,
    enrichment_numerator,
    execute_generation_plan,
    factor_exact,
    factorization_is_canonical,
    frequency_table,
    generation_plan,
    is_q_admissible,
    lambda_terms,
    lcm_many,
    minimal_antichain_is_exact,
    minimal_cover_antichain_from_flags,
    mode_summary,
    multiplicative_order,
    order_witness_is_exact,
    partition_admissible_anchors,
    reconstruct_factors,
    serialise_payload,
    signatures_from_cover,
    subset_lcms,
    unit_group_exponent,
    validate_frozen_metadata,
    validate_generation_plan,
)
from primes_lab.core import sieve


def test_partition_protected_range_arithmetic_and_disjointness() -> None:
    validate_frozen_metadata()
    assert WIDTH == 1_000_000
    assert BANDS == {
        "D9": (54_000_000, 55_000_000),
        "H9": (56_000_000, 57_000_000),
        "A9": (108_000_000, 109_000_000),
    }
    rows = {name: interval for name, _, interval in FROZEN_PARTITION}
    assert rows == {
        "G9-pre": (53_000_000, 54_000_000),
        "D9": (54_000_000, 55_000_000),
        "G9-mid": (55_000_000, 56_000_000),
        "H9": (56_000_000, 57_000_000),
        "A9": (108_000_000, 109_000_000),
    }
    intervals = list(rows.values())
    for i, left in enumerate(intervals):
        assert left[1] - left[0] == WIDTH
        for right in intervals[i + 1 :]:
            assert max(left[0], right[0]) >= min(left[1], right[1])
    assert BANDS["A9"][0] == 2 * BANDS["D9"][0]
    for name, interval in EXCLUDED_RANGES.items():
        if name == "D9":
            continue
        assert max(BANDS["D9"][0], interval[0]) >= min(BANDS["D9"][1], interval[1])


def test_q_basis_domain_semantics() -> None:
    assert Q == 210 == 2 * 3 * 5 * 7
    assert BASIS == (2, 3, 5, 7)
    assert is_q_admissible(11)
    assert is_q_admissible(121)
    for value in (2, 3, 5, 7, 14, 15, 21, 35, 77):
        assert not is_q_admissible(value)
    for anchor in (11, 121, 143):
        if is_q_admissible(anchor):
            assert all(gcd(anchor, base) == 1 for base in BASIS)


def test_prime_composite_partition_on_hand_checkable_domain() -> None:
    prime, composite = partition_admissible_anchors([121, 127, 131, 143], [127, 131])
    assert prime == (127, 131)
    assert composite == (121, 143)
    assert set(prime).isdisjoint(composite)
    with pytest.raises(ValueError, match="Q-admissible"):
        partition_admissible_anchors([127, 129], [127])


def test_exact_deterministic_factorization_reconstruction_and_canonical_order() -> None:
    base = sieve(100)
    value = 2**4 * 3**3 * 5**2 * 11
    factors = factor_exact(value, base)
    assert factors == ((2, 4), (3, 3), (5, 2), (11, 1))
    assert reconstruct_factors(factors) == value
    assert factorization_is_canonical(value, factors, base)
    assert factor_exact(1, base) == ()
    assert factor_exact(11**2 * 13, base) == ((11, 2), (13, 1))
    assert not factorization_is_canonical(45, ((3, 1), (15, 1)), base)
    assert not factorization_is_canonical(45, ((5, 1), (3, 2)), base)


def test_exact_lambda_construction_from_odd_prime_powers() -> None:
    base = sieve(100)
    factors = factor_exact(11**2 * 13, base)
    assert lambda_terms(factors) == (110, 12)
    assert unit_group_exponent(factors) == lcm(110, 12) == 660
    factors_225 = ((3, 2), (5, 2))
    assert lambda_terms(factors_225) == (6, 20)
    assert unit_group_exponent(factors_225) == 60
    assert lcm_many((6, 20)) == 60
    with pytest.raises(ValueError, match="odd anchors"):
        unit_group_exponent(((2, 3),))


def test_exact_multiplicative_orders_and_minimality_witnesses() -> None:
    base_primes = sieve(100)
    modulus = 11
    lam = 10
    lam_factors = factor_exact(lam, base_primes)
    expected = {2: 10, 3: 5, 5: 5, 7: 10}
    for base, target in expected.items():
        order = multiplicative_order(base, modulus, lam, lam_factors)
        assert order == target
        assert lam % order == 0
        assert pow(base, order, modulus) == 1
        assert order_witness_is_exact(base, modulus, order, lam, base_primes)
    assert not order_witness_is_exact(2, 11, 20, 10, base_primes)
    assert not order_witness_is_exact(2, 11, 5, 10, base_primes)


def test_canonical_enumeration_of_all_15_nonempty_subsets() -> None:
    assert len(SUBSETS) == 15
    assert SUBSETS == (
        (2,), (3,), (5,), (7,),
        (2, 3), (2, 5), (2, 7), (3, 5), (3, 7), (5, 7),
        (2, 3, 5), (2, 3, 7), (2, 5, 7), (3, 5, 7),
        (2, 3, 5, 7),
    )
    assert list(SUBSETS) == sorted(SUBSETS, key=lambda item: (len(item), item))


def test_subset_lcm_cover_predicate_and_upward_monotonicity() -> None:
    orders = (2, 3, 1, 1)
    lcms = subset_lcms(orders)
    flags = cover_flags(orders, 6)
    assert lcms[SUBSETS.index((2, 3))] == 6
    assert flags[SUBSETS.index((2, 3))] is True
    assert flags[SUBSETS.index((2, 3, 5))] is True
    assert flags[SUBSETS.index((2,))] is False
    assert cover_monotonicity_holds(flags)
    broken = list(flags)
    broken[SUBSETS.index((2, 3, 5))] = False
    assert not cover_monotonicity_holds(tuple(broken))


def test_minimal_antichain_empty_singleton_and_multiple_incomparable_cases() -> None:
    empty_flags = cover_flags((2, 2, 2, 2), 8)
    empty = minimal_cover_antichain_from_flags(empty_flags)
    assert empty == ()
    assert minimal_antichain_is_exact(empty_flags, empty)

    singleton_flags = cover_flags((6, 2, 3, 1), 6)
    singleton = minimal_cover_antichain_from_flags(singleton_flags)
    assert singleton[0] == (2,)
    assert (3, 5) in singleton
    assert minimal_antichain_is_exact(singleton_flags, singleton)

    multiple_flags = cover_flags((2, 3, 2, 3), 6)
    multiple = minimal_cover_antichain_from_flags(multiple_flags)
    assert multiple == ((2, 3), (2, 7), (3, 5), (5, 7))
    assert minimal_antichain_is_exact(multiple_flags, multiple)


def test_c1_c4_signature_semantics() -> None:
    sigs, flags, minimal = cover_shape((2, 3, 2, 3), 6)
    assert minimal == ((2, 3), (2, 7), (3, 5), (5, 7))
    assert sigs == {
        "C1": 2,
        "C2": (0, 4, 0, 0),
        "C3": (0, 4, 4, 1),
        "C4": ((2, 3), (2, 7), (3, 5), (5, 7)),
    }
    assert signatures_from_cover(flags, minimal) == sigs

    empty_sigs, _, _ = cover_shape((2, 2, 2, 2), 8)
    assert empty_sigs == {
        "C1": 0,
        "C2": (0, 0, 0, 0),
        "C3": (0, 0, 0, 0),
        "C4": (),
    }


def test_canonical_signature_ordering_for_all_families() -> None:
    assert sorted([3, 1, 2], key=lambda x: _signature_sort_key("C1", x)) == [1, 2, 3]
    c2 = [(0, 2, 0, 0), (0, 1, 2, 0), (0, 1, 1, 1)]
    assert sorted(c2, key=lambda x: _signature_sort_key("C2", x)) == [
        (0, 1, 1, 1), (0, 1, 2, 0), (0, 2, 0, 0)
    ]
    c4 = [((2,), (3, 5)), (), ((2,),), ((2, 3),)]
    assert sorted(c4, key=lambda x: _signature_sort_key("C4", x)) == [
        (), ((2,),), ((2,), (3, 5)), ((2, 3),)
    ]


def test_complete_frequency_tables_population_totals_and_canonical_ordering() -> None:
    counter = Counter({(0, 2, 0, 0): 2, (0, 1, 2, 0): 4, (0, 1, 1, 1): 1})
    table = frequency_table("C2", counter)
    assert [row["signature"] for row in table] == [
        [0, 1, 1, 1], [0, 1, 2, 0], [0, 2, 0, 0]
    ]
    assert sum(row["count"] for row in table) == sum(counter.values())

    c4_counter = Counter({(): 2, ((2,),): 1, ((2,), (3, 5)): 3})
    c4_table = frequency_table("C4", c4_counter)
    assert [row["signature"] for row in c4_table] == [
        [], [[2]], [[2], [3, 5]]
    ]


def test_strict_unique_mode_ranking_and_tie_rejection() -> None:
    unique = mode_summary("C1", Counter({3: 5, 2: 4, 1: 1}))
    assert unique == {
        "prime_mode_count": 5,
        "prime_maximizing_signatures": [3],
        "runner_up_count": 4,
        "strict_unique_prime_mode": True,
    }
    tied = mode_summary("C1", Counter({3: 5, 2: 5, 1: 1}))
    assert tied["prime_maximizing_signatures"] == [2, 3]
    assert tied["runner_up_count"] == 5
    assert tied["strict_unique_prime_mode"] is False


def test_exact_enrichment_positive_zero_negative_cases() -> None:
    assert enrichment_numerator(
        n_prime=3, n_composite=1, N_prime=10, N_composite=10
    ) == 20
    assert enrichment_numerator(
        n_prime=1, n_composite=1, N_prime=10, N_composite=10
    ) == 0
    assert enrichment_numerator(
        n_prime=1, n_composite=2, N_prime=10, N_composite=10
    ) == -10


def test_population_occurrence_floors_and_family_row_semantics() -> None:
    assert POPULATION_FLOOR == 1000
    assert OCCURRENCE_FLOOR == 32
    prime = Counter({2: 32, 1: 31})
    composite = Counter({2: 1})
    passing, target = _family_row(
        family="C1",
        prime_counter=prime,
        composite_counter=composite,
        N_prime=1000,
        N_composite=1000,
    )
    assert target == 2
    assert passing["population_floor_passed"] is True
    assert passing["occurrence_floor_passed"] is True
    assert passing["enrichment_passed"] is True

    failing, _ = _family_row(
        family="C1",
        prime_counter=Counter({2: 31, 1: 30}),
        composite_counter=composite,
        N_prime=999,
        N_composite=1000,
    )
    assert failing["population_floor_passed"] is False
    assert failing["occurrence_floor_passed"] is False


def _eligible_row(family: str, signature: object, prime_count: int = 40) -> dict[str, object]:
    return {
        "family": family,
        "prime_frequency_table": [],
        "composite_frequency_table": [],
        "prime_mode_count": prime_count,
        "prime_maximizing_signatures": [signature],
        "runner_up_count": prime_count - 1,
        "strict_unique_prime_mode": True,
        "unique_mode_composite_count": 1,
        "unique_mode_enrichment_numerator": 1,
        "population_floor_passed": True,
        "occurrence_floor_passed": True,
        "enrichment_passed": True,
        "mechanically_eligible": False,
    }


def test_exact_duplicate_suppression_family_order_and_promotion_cap() -> None:
    rows = [
        _eligible_row("C1", 2),
        _eligible_row("C2", [0, 2, 0, 0]),
        _eligible_row("C3", [0, 4, 4, 1]),
        _eligible_row("C4", [[2, 3]]),
    ]
    sets = {
        "C1": frozenset({101, 103}),
        "C2": frozenset({101, 103}),
        "C3": frozenset({107}),
        "C4": frozenset({109}),
    }
    promotions = apply_duplicate_suppression(rows, sets)
    assert [row["family"] for row in promotions] == ["C1", "C3", "C4"]
    assert rows[0]["mechanically_eligible"] is True
    assert rows[1]["mechanically_eligible"] is False
    assert len(promotions) <= PROMOTION_CAP == 4


def test_descriptive_allowlist_shape_excludes_per_anchor_and_unlisted_objects() -> None:
    assert PAYLOAD_KEYS == {
        "experiment", "implementation_commit", "band", "partition", "parameters",
        "generation_plan", "anchor_summary", "validation", "families", "promotions",
    }
    assert ANCHOR_SUMMARY_KEYS == {
        "admissible_count", "prime_count", "composite_count", "first_prime", "last_prime",
    }
    assert VALIDATION_KEYS == {
        "factorization_reconstruction_failure_count",
        "nonprime_factor_or_canonical_order_failure_count",
        "lambda_construction_failure_count",
        "basis_unit_gcd_failure_count",
        "order_divides_lambda_failure_count",
        "order_witness_or_minimality_failure_count",
        "cover_monotonicity_failure_count",
        "minimal_antichain_failure_count",
    }
    assert FAMILY_ROW_KEYS == {
        "family", "prime_frequency_table", "composite_frequency_table", "prime_mode_count",
        "prime_maximizing_signatures", "runner_up_count", "strict_unique_prime_mode",
        "unique_mode_composite_count", "unique_mode_enrichment_numerator",
        "population_floor_passed", "occurrence_floor_passed", "enrichment_passed",
        "mechanically_eligible",
    }
    forbidden = {
        "anchors", "factors", "lambda_values", "order_vectors", "subset_lcms",
        "cover_tables", "modular_power_witnesses", "non_mode_enrichment",
    }
    assert forbidden.isdisjoint(PAYLOAD_KEYS | ANCHOR_SUMMARY_KEYS | FAMILY_ROW_KEYS)


def test_byte_deterministic_serialization() -> None:
    payload = {"experiment": "E009", "x": {"b": 2, "a": 1}}
    first = serialise_payload(payload)
    second = serialise_payload(deepcopy(payload))
    assert first == second
    assert first.endswith(b"\n")
    assert first.index(b'"a"') < first.index(b'"b"')


def test_d9_generation_plan_is_exact_low_support_plus_whole_d9() -> None:
    plan = generation_plan("D9")
    assert plan == [
        {"purpose": "base_sieve_support", "strategy": "whole_prefix", "start": 0, "stop": 7417},
        {"purpose": "segmented_target", "strategy": "segmented", "start": 54_000_000, "stop": 55_000_000},
    ]
    validate_generation_plan(plan, band_name="D9")


def test_fail_closed_d9_rejects_every_forbidden_plan_before_prime_generator(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    plan = generation_plan("D9")
    called = False

    def forbidden_sieve(_: int) -> list[int]:
        nonlocal called
        called = True
        return []

    monkeypatch.setattr("experiments.E009_unit_action_cover_shapes.sieve", forbidden_sieve)

    invalid_plans: list[list[dict[str, object]]] = [
        [
            {"purpose": "base_sieve_support", "strategy": "whole_prefix", "start": 0, "stop": 200_000},
            plan[1],
        ],
        [
            {"purpose": "base_sieve_support", "strategy": "whole_prefix", "start": 0, "stop": 7416},
            plan[1],
        ],
        [
            {"purpose": "base_sieve_support", "strategy": "whole_prefix", "start": 0, "stop": 7418},
            plan[1],
        ],
        [
            {"purpose": "base_sieve_support", "strategy": "whole_prefix", "start": 1, "stop": 7417},
            plan[1],
        ],
        [
            plan[0],
            {"purpose": "segmented_target", "strategy": "segmented", "start": 54_000_000, "stop": 54_999_999},
        ],
        [
            plan[0],
            {"purpose": "segmented_target", "strategy": "segmented", "start": 53_999_999, "stop": 55_000_000},
        ],
        [
            plan[0],
            {"purpose": "segmented_target", "strategy": "segmented", "start": 54_000_001, "stop": 55_000_001},
        ],
        [
            plan[0],
            {"purpose": "segmented_target", "strategy": "segmented", "start": 54_000_000, "stop": 54_500_000},
            {"purpose": "segmented_target", "strategy": "segmented", "start": 54_500_000, "stop": 55_000_000},
        ],
    ]

    forbidden_intervals = (
        (0, 1_000_000), (1_000_000, 2_000_000), (2_000_000, 3_000_000),
        (4_000_000, 5_000_000), (8_000_000, 9_000_000), (10_000_000, 11_000_000),
        (16_000_000, 17_000_000), (32_000_000, 33_000_000),
        (33_000_000, 34_000_000), (34_000_000, 35_000_000), (35_000_000, 36_000_000),
        (36_000_000, 37_000_000), (37_000_000, 38_000_000), (38_000_000, 39_000_000),
        (39_000_000, 40_000_000), (40_000_000, 41_000_000), (41_000_000, 42_000_000),
        (42_000_000, 43_000_000), (43_000_000, 44_000_000), (44_000_000, 45_000_000),
        (45_000_000, 46_000_000), (46_000_000, 47_000_000), (47_000_000, 48_000_000),
        (48_000_000, 49_000_000), (49_000_000, 50_000_000), (50_000_000, 51_000_000),
        (51_000_000, 52_000_000), (52_000_000, 53_000_000), (53_000_000, 54_000_000),
        (55_000_000, 56_000_000), (56_000_000, 57_000_000), (66_000_000, 67_000_000),
        (70_000_000, 71_000_000), (78_000_000, 79_000_000), (84_000_000, 85_000_000),
        (92_000_000, 93_000_000), (108_000_000, 109_000_000),
        (128_000_000, 129_000_000),  # quarantined E005 region begins at 128M
        (60_000_000, 61_000_000),   # arbitrary other non-target
    )
    for start, stop in forbidden_intervals:
        invalid_plans.append([
            plan[0],
            {"purpose": "segmented_target", "strategy": "segmented", "start": start, "stop": stop},
        ])

    for bad in invalid_plans:
        with pytest.raises(ValueError):
            execute_generation_plan(bad, band_name="D9")
        assert called is False
