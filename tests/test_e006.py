import pytest

from experiments.E006_translation_overlap_spectrum import (
    BANDS,
    HORIZON,
    PROMOTION_CAP,
    SHIFTS,
    _execute_generation_plan,
    _translation_overlap_count_from_support,
    band_prime_support,
    generation_plan,
    odd_radical,
    promotion_pool,
    radical_classes,
    selected_promotions,
    serialise_payload,
    summarise_primes,
    summarise_radical_classes,
    validate_generation_plan,
)


def test_exact_band_local_prime_indicator_semantics() -> None:
    support = band_prime_support(
        [997, 1009, 1013, 2999, 3001], start=1000, stop=3000
    )
    assert support == frozenset({1009, 1013, 2999})


def test_common_anchor_exclusion_at_u_minus_h() -> None:
    start, stop = 1000, 3011
    support = frozenset({1999, 2011, 2023})
    assert stop - HORIZON == 2011
    assert _translation_overlap_count_from_support(
        support, start=start, stop=stop, shift=12
    ) == 1
    # 1999 -> 2011 counts, while 2011 -> 2023 is excluded solely because
    # its left endpoint is exactly U-H.


def test_exact_even_shift_set() -> None:
    assert SHIFTS == tuple(range(2, 1001, 2))
    assert len(SHIFTS) == 500
    assert SHIFTS[0] == 2
    assert SHIFTS[-1] == 1000
    assert all(shift % 2 == 0 for shift in SHIFTS)


def test_all_pairs_overlap_does_not_require_adjacency() -> None:
    support = frozenset({1009, 1013, 1019})
    assert _translation_overlap_count_from_support(
        support, start=1000, stop=3011, shift=10
    ) == 1
    # The pair 1009 -> 1019 is counted despite 1013 lying between them.


def test_band_boundary_exclusion() -> None:
    support = band_prime_support([2999, 3001], start=1000, stop=3000)
    assert 3001 not in support
    assert _translation_overlap_count_from_support(
        support, start=1000, stop=3000, shift=2
    ) == 0


def test_exact_odd_radical_factorization_and_class_membership() -> None:
    assert odd_radical(2) == 1
    assert odd_radical(4) == 1
    assert odd_radical(6) == 3
    assert odd_radical(12) == 3
    assert odd_radical(18) == 3
    assert odd_radical(30) == 15
    assert odd_radical(90) == 15
    assert odd_radical(1000) == 5

    classes = radical_classes()
    assert classes[1] == (2, 4, 8, 16, 32, 64, 128, 256, 512)
    assert all(odd_radical(shift) == 1 for shift in classes[1])


def test_frozen_shift_class_metadata_facts() -> None:
    classes = radical_classes()
    assert len(SHIFTS) == 500
    assert len(classes) == 204
    assert sum(1 for members in classes.values() if len(members) >= 8) == 11


def _class_summary(counts: dict[int, int]) -> dict[str, object]:
    members = tuple(sorted(counts))
    return summarise_radical_classes(counts, classes={1: members})[0]


def test_strict_unique_maximum_and_tie_failure_with_deterministic_runner_up() -> None:
    counts = {2: 8, 4: 9, 8: 10, 16: 11, 32: 12, 64: 20, 128: 13, 256: 14}
    unique = _class_summary(counts)
    assert unique["strict_unique_maximum"] is True
    assert unique["maximizing_shifts"] == [64]
    assert unique["max_count"] == 20
    assert unique["runner_up_count"] == 14
    assert unique["dominance_margin"] == 6

    counts[128] = 20
    tied = _class_summary(counts)
    assert tied["strict_unique_maximum"] is False
    assert tied["maximizing_shifts"] == [64, 128]
    assert tied["runner_up_count"] == 20
    assert tied["dominance_margin"] == 0
    assert promotion_pool([tied]) == []


def test_occurrence_floor_handling() -> None:
    low = _class_summary({2: 1, 4: 2, 8: 3, 16: 4, 32: 5, 64: 6, 128: 7, 256: 1})
    assert low["strict_unique_maximum"] is True
    assert low["max_count"] == 7
    assert promotion_pool([low]) == []

    passing = _class_summary({2: 1, 4: 2, 8: 3, 16: 4, 32: 5, 64: 6, 128: 8, 256: 1})
    pool = promotion_pool([passing])
    assert len(pool) == 1
    assert pool[0]["target_shift"] == 128
    assert pool[0]["target_count"] == 8


def _promotion_summary(
    *, rho: int, size: int, target: int, maximum: int, runner_up: int
) -> dict[str, object]:
    return {
        "rho": rho,
        "class_size": size,
        "max_count": maximum,
        "runner_up_count": runner_up,
        "maximizing_shifts": [target],
        "strict_unique_maximum": True,
    }


def test_deterministic_promotion_order_and_cap() -> None:
    summaries = [
        _promotion_summary(rho=11, size=8, target=22, maximum=30, runner_up=29),
        _promotion_summary(rho=13, size=8, target=26, maximum=30, runner_up=25),
        _promotion_summary(rho=15, size=9, target=30, maximum=29, runner_up=24),
        _promotion_summary(rho=17, size=10, target=34, maximum=29, runner_up=24),
        _promotion_summary(rho=19, size=10, target=38, maximum=31, runner_up=26),
        _promotion_summary(rho=21, size=12, target=42, maximum=31, runner_up=26),
    ]
    pool = promotion_pool(summaries)
    assert [(row["rho"], row["dominance_margin"]) for row in pool] == [
        (21, 5),
        (19, 5),
        (13, 5),
        (17, 5),
        (15, 5),
        (11, 1),
    ]
    assert len(selected_promotions(summaries)) == PROMOTION_CAP == 5
    assert selected_promotions(summaries) == pool[:5]


def test_exact_descriptive_allowlist_shape() -> None:
    plan = generation_plan("D6")
    payload = summarise_primes(
        [], band_name="D6", code_commit="test-commit", plan=plan
    )
    assert set(payload) == {
        "experiment",
        "implementation_commit",
        "band",
        "partition",
        "translation",
        "generation_plan",
        "prime_summary",
        "shifts",
        "radical_classes",
        "promotion_pool",
    }
    assert set(payload["prime_summary"]) == {"count", "first_prime", "last_prime"}
    assert all(set(row) == {"h", "rho", "count"} for row in payload["shifts"])
    for row in payload["radical_classes"]:
        expected = {
            "rho",
            "member_shifts",
            "class_size",
            "member_counts",
            "max_count",
            "runner_up_count",
            "maximizing_shifts",
            "strict_unique_maximum",
        }
        if row["class_size"] >= 2:
            expected.add("dominance_margin")
        assert set(row) == expected


def test_byte_deterministic_serialization() -> None:
    payload = {
        "experiment": "E006",
        "x": {"b": 2, "a": 1},
        "shifts": [{"h": 2, "rho": 1, "count": 3}],
    }
    assert serialise_payload(payload) == serialise_payload(payload)
    assert serialise_payload(payload).endswith(b"\n")


def test_d6_generation_plan_exact_support_and_target() -> None:
    plan = generation_plan("D6")
    assert plan == [
        {
            "purpose": "base_sieve_support",
            "strategy": "whole_prefix",
            "start": 0,
            "stop": 6558,
        },
        {
            "purpose": "segmented_target",
            "strategy": "segmented",
            "start": 42_000_000,
            "stop": 43_000_000,
        },
    ]
    validate_generation_plan(plan, band_name="D6")


def test_fail_closed_generation_rejection_before_prime_generator(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    plan = generation_plan("D6")
    called = False

    def forbidden_sieve(_: int) -> list[int]:
        nonlocal called
        called = True
        return []

    monkeypatch.setattr(
        "experiments.E006_translation_overlap_spectrum.sieve",
        forbidden_sieve,
    )

    bad_prefix = [
        {
            "purpose": "base_sieve_support",
            "strategy": "whole_prefix",
            "start": 0,
            "stop": 200_000,
        },
        plan[1],
    ]
    with pytest.raises(ValueError, match="whole-prefix"):
        _execute_generation_plan(bad_prefix, band_name="D6")
    assert called is False

    forbidden_intervals = (
        (33_000_000, 34_000_000),
        (34_000_000, 35_000_000),
        (35_000_000, 36_000_000),
        (36_000_000, 37_000_000),
        (37_000_000, 38_000_000),
        (38_000_000, 39_000_000),
        (39_000_000, 40_000_000),
        (40_000_000, 41_000_000),
        (41_000_000, 42_000_000),
        (43_000_000, 44_000_000),
        (44_000_000, 45_000_000),
        (70_000_000, 71_000_000),
        (78_000_000, 79_000_000),
        (84_000_000, 85_000_000),
    )
    for start, stop in forbidden_intervals:
        bad = [
            plan[0],
            {
                "purpose": "segmented_target",
                "strategy": "segmented",
                "start": start,
                "stop": stop,
            },
        ]
        with pytest.raises(ValueError):
            _execute_generation_plan(bad, band_name="D6")
        assert called is False

    partial_d6 = [
        plan[0],
        {
            "purpose": "segmented_target",
            "strategy": "segmented",
            "start": BANDS["D6"][0],
            "stop": BANDS["D6"][1] - 1,
        },
    ]
    with pytest.raises(ValueError, match="complete authorized target"):
        _execute_generation_plan(partial_d6, band_name="D6")
    assert called is False
