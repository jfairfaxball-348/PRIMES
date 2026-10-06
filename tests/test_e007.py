from __future__ import annotations

from collections import Counter
from copy import deepcopy
from math import gcd

import pytest

from experiments.E007_neighbour_factorization_coupling import (
    BANDS,
    FAMILY_ORDER,
    OCCURRENCE_FLOOR,
    POPULATION_FLOOR,
    PROMOTION_CAP,
    _validate_family_rows,
    common_odd_anchors,
    enrichment_numerator,
    factor_odd_exact,
    factor_profile,
    frequency_table,
    generation_plan,
    mode_summary,
    partition_anchors,
    serialise_payload,
    signatures,
    strip_power_of_two,
    summarise_band,
    thin_thick_cores,
    validate_generation_plan,
)
from primes_lab.core import sieve


def test_common_odd_anchor_boundary_semantics_excludes_u_minus_1() -> None:
    anchors = common_odd_anchors(start=10, stop=20)
    assert anchors == (11, 13, 15, 17)
    assert 19 not in anchors


def test_exact_prime_composite_partition_on_hand_checkable_domain() -> None:
    anchors = common_odd_anchors(start=10, stop=20)
    prime, composite = partition_anchors(anchors, [11, 13, 17, 19])
    assert prime == (11, 13, 17)
    assert composite == (15,)
    assert set(prime).isdisjoint(composite)
    assert len(prime) + len(composite) == len(anchors)


def test_v2_complete_stripping_and_thin_thick_both_orientations() -> None:
    assert strip_power_of_two(40) == (3, 5)
    assert strip_power_of_two(48) == (4, 3)
    minus = thin_thick_cores(11)
    assert minus == {
        "thin_orientation": "minus",
        "thin_v2": 1,
        "thick_v2": 2,
        "thin_core": 5,
        "thick_core": 3,
    }
    plus = thin_thick_cores(13)
    assert plus == {
        "thin_orientation": "plus",
        "thin_v2": 1,
        "thick_v2": 2,
        "thin_core": 7,
        "thick_core": 3,
    }


def test_exact_odd_factorization_reconstruction_repeated_and_one() -> None:
    base = sieve(100)
    factors, reconstructed = factor_odd_exact(3**3 * 5**2 * 11, base)
    assert factors == ((3, 3), (5, 2), (11, 1))
    assert reconstructed == 7425
    factors_one, reconstructed_one = factor_odd_exact(1, base)
    assert factors_one == ()
    assert reconstructed_one == 1
    profile = factor_profile(7425, base)
    assert profile == {
        "omega": 3,
        "Omega": 6,
        "shape": (3, 2, 1),
        "Pplus": 11,
        "reconstructed": 7425,
    }
    one = factor_profile(1, base)
    assert one["shape"] == () and one["Pplus"] == 1


def test_gcd_odd_core_invariant() -> None:
    for anchor in (11, 13, 15, 17, 21, 25, 31):
        row = thin_thick_cores(anchor)
        assert gcd(row["thin_core"], row["thick_core"]) == 1


def test_f1_f4_signature_semantics() -> None:
    thin = {"shape": (2, 1), "omega": 2, "Omega": 3, "Pplus": 7}
    thick = {"shape": (3,), "omega": 1, "Omega": 3, "Pplus": 5}
    assert signatures(thin, thick) == {
        "F1": ((2, 1), (3,)),
        "F2": (2, 1),
        "F3": (3, 3),
        "F4": 1,
    }


def test_complete_frequency_tables_use_frozen_canonical_order() -> None:
    f1 = Counter({((2,), (1,)): 2, ((1,), (3,)): 4, ((), (1, 1)): 1})
    assert [row["signature"] for row in frequency_table("F1", f1)] == [
        [[], [1, 1]],
        [[1], [3]],
        [[2], [1]],
    ]
    f2 = Counter({(2, 1): 1, (1, 3): 2, (1, 2): 3})
    assert [row["signature"] for row in frequency_table("F2", f2)] == [
        [1, 2],
        [1, 3],
        [2, 1],
    ]
    f4 = Counter({1: 3, -1: 2, 0: 1})
    assert [row["signature"] for row in frequency_table("F4", f4)] == [-1, 0, 1]


def test_strict_unique_mode_and_tie_handling_with_runner_up() -> None:
    unique = mode_summary("F4", {-1: 2, 0: 5, 1: 3})
    assert unique == {
        "prime_mode_count": 5,
        "prime_maximizing_signatures": [0],
        "runner_up_count": 3,
        "strict_unique_prime_mode": True,
    }
    tied = mode_summary("F4", {-1: 5, 0: 5, 1: 1})
    assert tied["prime_maximizing_signatures"] == [-1, 0]
    assert tied["runner_up_count"] == 5
    assert tied["strict_unique_prime_mode"] is False


def test_exact_enrichment_integer_arithmetic_positive_zero_negative() -> None:
    assert (
        enrichment_numerator(
            n_prime=6, n_composite=4, N_prime=10, N_composite=10
        )
        == 20
    )
    assert (
        enrichment_numerator(
            n_prime=5, n_composite=5, N_prime=10, N_composite=10
        )
        == 0
    )
    assert (
        enrichment_numerator(
            n_prime=4, n_composite=6, N_prime=10, N_composite=10
        )
        == -20
    )


def _family_row(
    family: str, target: object, count: int = OCCURRENCE_FLOOR
) -> dict[str, object]:
    return {
        "family": family,
        "prime_maximizing_signatures": [target],
        "prime_mode_count": count,
        "unique_mode_composite_count": 1,
        "unique_mode_enrichment_numerator": 1,
        "population_floor_passed": True,
        "strict_unique_prime_mode": True,
        "occurrence_floor_passed": count >= OCCURRENCE_FLOOR,
        "enrichment_passed": True,
        "mechanically_eligible": False,
    }


def test_population_occurrence_floor_and_duplicate_suppression_cap() -> None:
    assert POPULATION_FLOOR == 1000
    assert OCCURRENCE_FLOOR == 32
    assert PROMOTION_CAP == 4
    rows = [
        _family_row("F1", [[1], [1]]),
        _family_row("F2", [1, 1]),
        _family_row("F3", [2, 2]),
        _family_row("F4", 1),
    ]
    sets = {
        "F1": frozenset({1, 3, 5}),
        "F2": frozenset({1, 3, 5}),
        "F3": frozenset({7, 9}),
        "F4": frozenset({11, 13}),
    }
    promotions = _validate_family_rows(rows, sets)
    assert [row["family"] for row in promotions] == ["F1", "F3", "F4"]
    assert rows[0]["mechanically_eligible"] is True
    assert rows[1]["mechanically_eligible"] is False

    low = [_family_row("F1", [[1], [1]], count=31)]
    assert _validate_family_rows(low, {"F1": frozenset({1})}) == []


def test_descriptive_allowlist_shape_on_hand_checkable_band(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setitem(BANDS, "D7", (10, 30))
    plan = [
        {
            "purpose": "base_sieve_support",
            "strategy": "whole_prefix",
            "start": 0,
            "stop": 6,
        },
        {
            "purpose": "segmented_target",
            "strategy": "segmented",
            "start": 10,
            "stop": 30,
        },
    ]
    payload = summarise_band(
        band_name="D7",
        code_commit="test-commit",
        plan=plan,
        base_primes=sieve(5),
        target_primes=[11, 13, 17, 19, 23, 29],
    )
    assert set(payload) == {
        "experiment",
        "implementation_commit",
        "band",
        "partition",
        "parameters",
        "generation_plan",
        "anchor_summary",
        "controls",
        "validation_aggregates",
        "families",
        "promotion_records",
    }
    assert set(payload["anchor_summary"]) == {
        "common_odd_anchor_count",
        "prime_anchor_count",
        "composite_anchor_count",
        "first_prime_anchor",
        "last_prime_anchor",
    }
    assert set(payload["validation_aggregates"]) == {
        "factorization_reconstruction_failure_count",
        "thin_thick_classification_failure_count",
        "odd_core_gcd_failure_count",
    }
    assert [row["family"] for row in payload["families"]] == list(FAMILY_ORDER)
    for row in payload["families"]:
        assert set(row) == {
            "family",
            "prime_frequency_table",
            "composite_frequency_table",
            "prime_mode_count",
            "prime_maximizing_signatures",
            "runner_up_count",
            "strict_unique_prime_mode",
            "unique_mode_composite_count",
            "unique_mode_enrichment_numerator",
            "population_floor_passed",
            "occurrence_floor_passed",
            "enrichment_passed",
            "mechanically_eligible",
        }


def test_byte_deterministic_serialization() -> None:
    payload = {"experiment": "E007", "x": {"b": 2, "a": 1}}
    first = serialise_payload(payload)
    second = serialise_payload(deepcopy(payload))
    assert first == second
    assert first.endswith(b"\n")


def test_d7_generation_plan_exact_base_support_and_target() -> None:
    plan = generation_plan("D7")
    assert plan == [
        {
            "purpose": "base_sieve_support",
            "strategy": "whole_prefix",
            "start": 0,
            "stop": 6856,
        },
        {
            "purpose": "segmented_target",
            "strategy": "segmented",
            "start": 46_000_000,
            "stop": 47_000_000,
        },
    ]
    validate_generation_plan(plan, band_name="D7")


@pytest.mark.parametrize(
    "bad_plan",
    [
        [
            {
                "purpose": "base_sieve_support",
                "strategy": "whole_prefix",
                "start": 0,
                "stop": 47_000_000,
            },
            {
                "purpose": "segmented_target",
                "strategy": "segmented",
                "start": 46_000_000,
                "stop": 47_000_000,
            },
        ],
        [
            {
                "purpose": "base_sieve_support",
                "strategy": "whole_prefix",
                "start": 0,
                "stop": 6856,
            },
            {
                "purpose": "segmented_target",
                "strategy": "segmented",
                "start": 46_000_001,
                "stop": 47_000_000,
            },
        ],
        [
            {
                "purpose": "base_sieve_support",
                "strategy": "whole_prefix",
                "start": 0,
                "stop": 6856,
            },
            {
                "purpose": "segmented_target",
                "strategy": "segmented",
                "start": 45_000_000,
                "stop": 46_000_000,
            },
        ],
        [
            {
                "purpose": "base_sieve_support",
                "strategy": "whole_prefix",
                "start": 0,
                "stop": 6856,
            },
            {
                "purpose": "segmented_target",
                "strategy": "segmented",
                "start": 48_000_000,
                "stop": 49_000_000,
            },
        ],
        [
            {
                "purpose": "base_sieve_support",
                "strategy": "whole_prefix",
                "start": 0,
                "stop": 6856,
            },
            {
                "purpose": "segmented_target",
                "strategy": "segmented",
                "start": 92_000_000,
                "stop": 93_000_000,
            },
        ],
        [
            {
                "purpose": "base_sieve_support",
                "strategy": "whole_prefix",
                "start": 0,
                "stop": 6856,
            },
            {
                "purpose": "segmented_target",
                "strategy": "segmented",
                "start": 33_000_000,
                "stop": 34_000_000,
            },
        ],
        [
            {
                "purpose": "base_sieve_support",
                "strategy": "whole_prefix",
                "start": 0,
                "stop": 6856,
            },
            {
                "purpose": "segmented_target",
                "strategy": "segmented",
                "start": 43_000_000,
                "stop": 44_000_000,
            },
        ],
        [
            {
                "purpose": "base_sieve_support",
                "strategy": "whole_prefix",
                "start": 0,
                "stop": 6856,
            },
            {
                "purpose": "segmented_target",
                "strategy": "segmented",
                "start": 39_000_000,
                "stop": 40_000_000,
            },
        ],
        [
            {
                "purpose": "base_sieve_support",
                "strategy": "whole_prefix",
                "start": 0,
                "stop": 6857,
            },
            {
                "purpose": "segmented_target",
                "strategy": "segmented",
                "start": 46_000_000,
                "stop": 47_000_000,
            },
        ],
    ],
)
def test_generation_guard_rejects_whole_prefix_partial_guard_holdout_adversarial_historical_and_wrong_support(
    bad_plan: list[dict[str, object]],
) -> None:
    with pytest.raises(ValueError):
        validate_generation_plan(bad_plan, band_name="D7")
