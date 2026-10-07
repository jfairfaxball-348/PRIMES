from collections import Counter

import pytest

from experiments.E008_binary_core_shapes import (
    ANCHOR_SUMMARY_KEYS,
    BANDS,
    FAMILY_ORDER,
    FAMILY_ROW_KEYS,
    J,
    OCCURRENCE_FLOOR,
    PAYLOAD_KEYS,
    POPULATION_FLOOR,
    PROMOTION_CAP,
    Q,
    SHELL,
    VALIDATION_KEYS,
    WIDTH,
    _apply_duplicate_suppression,
    _family_row,
    b1_signature,
    b2_signature,
    b3_signature,
    b4_signature,
    binary_core,
    binary_digits_26,
    enrichment_numerator,
    execute_generation_plan,
    frequency_table,
    generation_plan,
    is_q_admissible,
    mode_summary,
    partition_admissible_anchors,
    reconstruct_binary,
    serialise_payload,
    signatures,
    validate_frozen_metadata,
    validate_generation_plan,
)


def test_partition_boundaries_shell_and_frozen_arithmetic() -> None:
    validate_frozen_metadata()
    assert WIDTH == 1_000_000
    assert Q == 210
    assert J == 19 == (WIDTH - 1).bit_length() - 1
    assert SHELL == (2**25, 2**26)
    assert BANDS == {
        "D8": (50_000_000, 51_000_000),
        "H8": (52_000_000, 53_000_000),
        "A8": (66_000_000, 67_000_000),
    }
    assert all(SHELL[0] <= lo < hi <= SHELL[1] for lo, hi in BANDS.values())


def test_q_admissibility_hand_checkable() -> None:
    assert is_q_admissible(11)
    assert is_q_admissible(121)
    for value in (2, 3, 5, 7, 14, 15, 21, 35):
        assert not is_q_admissible(value)


def test_prime_composite_partition_on_hand_checkable_inputs() -> None:
    prime, composite = partition_admissible_anchors([121, 127, 131], [127, 131])
    assert prime == (127, 131)
    assert composite == (121,)
    with pytest.raises(ValueError, match="Q-admissible"):
        partition_admissible_anchors([127, 129], [127])


def test_exact_26_bit_decomposition_and_reconstruction() -> None:
    value = 50_123_457
    digits = binary_digits_26(value)
    assert len(digits) == 26
    assert digits[0] == 1
    assert reconstruct_binary(digits) == value
    with pytest.raises(ValueError, match="26-bit shell"):
        binary_digits_26(SHELL[0] - 1)


def test_j_core_order_parity_and_higher_coordinate_exclusion() -> None:
    value = (1 << 25) | (1 << 19) | (1 << 17) | (1 << 1) | 1
    core = binary_core(value)
    assert len(core) == 19
    assert core[0] == 1  # b19
    assert core[1] == 0  # b18
    assert core[2] == 1  # b17
    assert core[-1] == 1  # b1
    assert ((value >> 0) & 1) == 1
    assert core == tuple((value >> j) & 1 for j in range(19, 0, -1))
    changed_high = value ^ (1 << 20) ^ (1 << 22)
    assert binary_core(changed_high) == core


def test_b1_hamming_weight_semantics() -> None:
    core = (1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    assert b1_signature(core) == 4


def test_b2_transition_count_semantics() -> None:
    core = (1, 1, 0, 0, 1, 0) + (0,) * 13
    assert b2_signature(core) == 3


def test_b3_longest_runs_and_absent_bit_convention() -> None:
    assert b3_signature((0,) * 19) == (19, 0)
    assert b3_signature((1,) * 19) == (0, 19)
    core = (1, 1, 0, 0, 0, 1, 0, 0) + (1,) * 11
    assert b3_signature(core) == (3, 11)


def test_b4_run_decomposition_nonincreasing_shape() -> None:
    core = (1, 1, 0, 0, 0, 1, 0, 0) + (1,) * 11
    shape = b4_signature(core)
    assert shape == (11, 3, 2, 2, 1)
    assert sum(shape) == 19
    assert shape == tuple(sorted(shape, reverse=True))


def test_all_four_signature_families_and_core_validation() -> None:
    core = (1, 0) * 9 + (1,)
    sigs = signatures(core)
    assert tuple(sigs) == FAMILY_ORDER
    assert sigs["B1"] == 10
    assert sigs["B2"] == 18
    assert sigs["B3"] == (1, 1)
    assert sigs["B4"] == (1,) * 19
    with pytest.raises(ValueError, match="19-bit"):
        signatures((1, 0))


def test_canonical_frequency_ordering() -> None:
    b1 = frequency_table("B1", Counter({3: 2, 1: 4, 2: 1}))
    assert [row["signature"] for row in b1] == [1, 2, 3]
    b3 = frequency_table("B3", Counter({(3, 2): 1, (2, 4): 2, (3, 1): 3}))
    assert [row["signature"] for row in b3] == [[2, 4], [3, 1], [3, 2]]
    b4 = frequency_table("B4", Counter({(3, 2): 1, (3, 1, 1): 2, (4,): 3}))
    assert [row["signature"] for row in b4] == [[3, 1, 1], [3, 2], [4]]


def test_strict_unique_mode_and_tie_handling() -> None:
    unique = mode_summary("B1", Counter({3: 5, 2: 4, 1: 1}))
    assert unique == {
        "prime_mode_count": 5,
        "prime_maximizing_signatures": [3],
        "runner_up_count": 4,
        "strict_unique_prime_mode": True,
    }
    tied = mode_summary("B1", Counter({3: 5, 2: 5, 1: 1}))
    assert tied["prime_maximizing_signatures"] == [2, 3]
    assert tied["runner_up_count"] == 5
    assert tied["strict_unique_prime_mode"] is False


def test_exact_enrichment_positive_zero_negative() -> None:
    assert enrichment_numerator(n_prime=3, n_composite=1, N_prime=10, N_composite=10) == 20
    assert enrichment_numerator(n_prime=1, n_composite=1, N_prime=10, N_composite=10) == 0
    assert enrichment_numerator(n_prime=1, n_composite=2, N_prime=10, N_composite=10) == -10


def test_population_and_occurrence_floors() -> None:
    assert POPULATION_FLOOR == 1000
    assert OCCURRENCE_FLOOR == 32
    prime = Counter({9: 32, 8: 31})
    composite = Counter({9: 1})
    passing, _ = _family_row(
        family="B1", prime_counter=prime, composite_counter=composite,
        N_prime=1000, N_composite=1000,
    )
    assert passing["population_floor_passed"] is True
    assert passing["occurrence_floor_passed"] is True
    assert passing["enrichment_passed"] is True
    failing, _ = _family_row(
        family="B1", prime_counter=Counter({9: 31, 8: 30}), composite_counter=composite,
        N_prime=999, N_composite=1000,
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


def test_exact_duplicate_suppression_family_order_and_cap() -> None:
    rows = [
        _eligible_row("B1", 9),
        _eligible_row("B2", 8),
        _eligible_row("B3", [3, 3]),
        _eligible_row("B4", [4, 3, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1]),
    ]
    sets = {
        "B1": frozenset({101, 103}),
        "B2": frozenset({101, 103}),
        "B3": frozenset({107}),
        "B4": frozenset({109}),
    }
    promotions = _apply_duplicate_suppression(rows, sets)
    assert [row["family"] for row in promotions] == ["B1", "B3", "B4"]
    assert rows[0]["mechanically_eligible"] is True
    assert rows[1]["mechanically_eligible"] is False
    assert len(promotions) <= PROMOTION_CAP == 4


def test_descriptive_allowlist_shape_excludes_forbidden_catalogs() -> None:
    assert PAYLOAD_KEYS == {
        "experiment", "implementation_commit", "band", "partition", "parameters",
        "generation_plan", "anchor_summary", "validation", "families", "promotions",
    }
    assert ANCHOR_SUMMARY_KEYS == {
        "admissible_count", "prime_count", "composite_count", "first_prime", "last_prime"
    }
    assert VALIDATION_KEYS == {
        "admissible_partition_failure_count", "binary_reconstruction_failure_count",
        "core_length_failure_count", "parity_control_failure_count",
    }
    assert FAMILY_ROW_KEYS == {
        "family", "prime_frequency_table", "composite_frequency_table", "prime_mode_count",
        "prime_maximizing_signatures", "runner_up_count", "strict_unique_prime_mode",
        "unique_mode_composite_count", "unique_mode_enrichment_numerator",
        "population_floor_passed", "occurrence_floor_passed", "enrichment_passed",
        "mechanically_eligible",
    }
    forbidden = {"anchors", "binary_words", "exact_word_frequency_table", "non_mode_enrichment"}
    assert forbidden.isdisjoint(PAYLOAD_KEYS | ANCHOR_SUMMARY_KEYS | FAMILY_ROW_KEYS)


def test_byte_deterministic_serialization() -> None:
    payload = {"experiment": "E008", "x": {"b": 2, "a": 1}}
    first = serialise_payload(payload)
    second = serialise_payload(payload)
    assert first == second
    assert first.endswith(b"\n")
    assert first.index(b'"a"') < first.index(b'"b"')


def test_d8_generation_plan_exact_support_and_target() -> None:
    plan = generation_plan("D8")
    assert plan == [
        {"purpose": "base_sieve_support", "strategy": "whole_prefix", "start": 0, "stop": 7142},
        {"purpose": "segmented_target", "strategy": "segmented", "start": 50_000_000, "stop": 51_000_000},
    ]
    validate_generation_plan(plan, band_name="D8")


def test_fail_closed_generation_rejection_before_prime_generator(monkeypatch: pytest.MonkeyPatch) -> None:
    plan = generation_plan("D8")
    called = False

    def forbidden_sieve(_: int) -> list[int]:
        nonlocal called
        called = True
        return []

    monkeypatch.setattr("experiments.E008_binary_core_shapes.sieve", forbidden_sieve)

    invalid_plans = [
        [
            {"purpose": "base_sieve_support", "strategy": "whole_prefix", "start": 0, "stop": 200_000},
            plan[1],
        ],
        [
            plan[0],
            {"purpose": "segmented_target", "strategy": "segmented", "start": 50_000_000, "stop": 50_999_999},
        ],
        [
            plan[0],
            {"purpose": "segmented_target", "strategy": "segmented", "start": 49_999_999, "stop": 51_000_000},
        ],
    ]
    forbidden_intervals = (
        (0, 1_000_000), (1_000_000, 2_000_000), (2_000_000, 3_000_000),
        (4_000_000, 5_000_000), (8_000_000, 9_000_000), (10_000_000, 11_000_000),
        (16_000_000, 17_000_000), (32_000_000, 33_000_000), (33_000_000, 34_000_000),
        (34_000_000, 35_000_000), (35_000_000, 36_000_000), (36_000_000, 37_000_000),
        (37_000_000, 38_000_000), (38_000_000, 39_000_000), (39_000_000, 40_000_000),
        (40_000_000, 41_000_000), (41_000_000, 42_000_000), (42_000_000, 43_000_000),
        (43_000_000, 44_000_000), (44_000_000, 45_000_000), (45_000_000, 46_000_000),
        (46_000_000, 47_000_000), (47_000_000, 48_000_000), (48_000_000, 49_000_000),
        (49_000_000, 50_000_000), (51_000_000, 52_000_000), (52_000_000, 53_000_000),
        (66_000_000, 67_000_000), (70_000_000, 71_000_000), (78_000_000, 79_000_000),
        (84_000_000, 85_000_000), (92_000_000, 93_000_000), (60_000_000, 61_000_000),
    )
    for start, stop in forbidden_intervals:
        invalid_plans.append(
            [
                plan[0],
                {"purpose": "segmented_target", "strategy": "segmented", "start": start, "stop": stop},
            ]
        )
    invalid_plans.extend(
        [
            [
                {"purpose": "base_sieve_support", "strategy": "whole_prefix", "start": 0, "stop": 7141},
                plan[1],
            ],
            [
                {"purpose": "base_sieve_support", "strategy": "whole_prefix", "start": 0, "stop": 7143},
                plan[1],
            ],
        ]
    )

    for bad in invalid_plans:
        with pytest.raises(ValueError):
            execute_generation_plan(bad, band_name="D8")
        assert called is False
