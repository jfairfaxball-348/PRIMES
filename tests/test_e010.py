from collections import Counter

import pytest

from experiments.E010_quadratic_surd_cycle_shapes import (
    ANCHOR_SUMMARY_KEYS,
    BANDS,
    E005_CALIBRATION_RANGES,
    FAMILY_ROW_KEYS,
    FROZEN_PARTITION,
    HISTORICAL_RANGES,
    PAYLOAD_KEYS,
    Q,
    VALIDATION_KEYS,
    WIDTH,
    execute_generation_plan,
    generation_plan,
    is_anchor_in_common_domain,
    is_q_admissible,
    partition_admissible_anchors,
    serialise_payload,
    validate_frequency_totals,
    validate_frozen_metadata,
    validate_generation_plan,
    _evaluate_anchor_block,
    _init_summary_worker,
)
from experiments.E010_quadratic_surd_cycle_shapes_runtime import FAMILY_ORDER


def test_frozen_partition_provenance_arithmetic_and_disjointness() -> None:
    validate_frozen_metadata()
    assert WIDTH == 1_000_000 and Q == 210
    assert BANDS == {
        "D10": (58_000_000, 59_000_000),
        "H10": (60_000_000, 61_000_000),
        "A10": (116_000_000, 117_000_000),
    }
    rows = {name: interval for name, _, interval in FROZEN_PARTITION}
    assert rows["G10-pre"] == (57_000_000, 58_000_000)
    assert rows["G10-mid"] == (59_000_000, 60_000_000)
    assert rows["A10"][0] == 2 * rows["D10"][0]
    for left in rows.values():
        for right in (*HISTORICAL_RANGES.values(), *E005_CALIBRATION_RANGES):
            assert max(left[0], right[0]) >= min(left[1], right[1])


def test_q_nonsquare_domain_and_prime_composite_partition() -> None:
    assert is_q_admissible(121) and not is_anchor_in_common_domain(121)
    assert is_anchor_in_common_domain(127)
    prime, composite = partition_admissible_anchors([127, 131, 143], [127, 131])
    assert prime == (127, 131) and composite == (143,)
    with pytest.raises(ValueError, match="Q-admissible nonsquares"):
        partition_admissible_anchors([121, 127], [127])


def test_prime_composite_frequency_totals() -> None:
    prime = {
        "L1": Counter({1: 2, 2: 1}), "L2": Counter({1: 1, 2: 2}),
        "L3": Counter({1: 3}), "L4": Counter({(1,): 2, (2,): 1}),
    }
    composite = {family: Counter({1 if family != "L4" else (1,): 4}) for family in FAMILY_ORDER}
    validate_frequency_totals(prime, composite, N_prime=3, N_composite=4)
    prime["L1"][9] += 1
    with pytest.raises(ValueError, match="L1 prime frequency"):
        validate_frequency_totals(prime, composite, N_prime=3, N_composite=4)


def test_descriptive_allowlist_shape_excludes_forbidden_fields() -> None:
    assert PAYLOAD_KEYS == {
        "experiment", "implementation_commit", "band", "partition", "parameters",
        "generation_plan", "anchor_summary", "validation", "families", "promotions",
    }
    assert ANCHOR_SUMMARY_KEYS == {
        "admissible_count", "prime_count", "composite_count",
        "q_admissible_perfect_squares_excluded", "first_prime", "last_prime",
    }
    assert VALIDATION_KEYS == {
        "integer_root_or_domain_failure_count",
        "recurrence_positivity_or_divisibility_failure_count",
        "recurrence_quotient_bound_failure_count",
        "premature_nonterminal_state_repeat_failure_count",
        "terminal_state_failure_count",
        "denominator_multiplicity_or_profile_identity_failure_count",
    }
    assert FAMILY_ROW_KEYS == {
        "family", "prime_frequency_table", "composite_frequency_table",
        "prime_mode_count", "prime_maximizing_signatures", "runner_up_count",
        "strict_unique_prime_mode", "unique_mode_composite_count",
        "unique_mode_enrichment_numerator", "population_floor_passed",
        "occurrence_floor_passed", "enrichment_passed", "mechanically_eligible",
    }
    forbidden = {
        "anchors", "recurrence_states", "a0_values", "denominator_words",
        "partial_quotient_words", "convergents", "non_mode_enrichment",
        "alternative_controls",
    }
    assert forbidden.isdisjoint(PAYLOAD_KEYS | ANCHOR_SUMMARY_KEYS | FAMILY_ROW_KEYS)


def test_byte_deterministic_serialization() -> None:
    payload = {"experiment": "E010", "x": {"b": 2, "a": 1}}
    assert serialise_payload(payload) == serialise_payload(payload)
    assert serialise_payload(payload).endswith(b"\n")
    assert serialise_payload(payload).index(b'"a"') < serialise_payload(payload).index(b'"b"')


def test_d10_generation_plan_is_exact_complete_plan() -> None:
    plan = generation_plan("D10")
    assert plan == [
        {"purpose": "base_sieve_support", "strategy": "whole_prefix", "start": 0, "stop": 7682},
        {"purpose": "segmented_target", "strategy": "segmented",
         "start": 58_000_000, "stop": 59_000_000},
    ]
    validate_generation_plan(plan, band_name="D10")


def test_fail_closed_generation_rejection_before_prime_generator(monkeypatch: pytest.MonkeyPatch) -> None:
    plan = generation_plan("D10")
    calls: list[str] = []

    def forbidden_sieve(_: int) -> list[int]:
        calls.append("sieve")
        return []

    def forbidden_segmented(_: int, __: int, ___: object) -> bytearray:
        calls.append("segmented")
        return bytearray()

    monkeypatch.setattr("experiments.E010_quadratic_surd_cycle_shapes.sieve", forbidden_sieve)
    monkeypatch.setattr(
        "experiments.E010_quadratic_surd_cycle_shapes._segmented_target_prime_flags",
        forbidden_segmented,
    )
    invalid = [
        [{**plan[0], "stop": 7681}, plan[1]],
        [{**plan[0], "stop": 7683}, plan[1]],
        [{**plan[0], "stop": 59_000_000}, plan[1]],
        [plan[0], {**plan[1], "stop": 58_999_999}],
        [plan[0], {**plan[1], "start": 57_999_999}],
        [plan[0], {**plan[1], "start": 58_000_001, "stop": 59_000_001}],
        [plan[0], {**plan[1], "strategy": "whole_prefix"}],
        [plan[0], {**plan[1], "stop": 58_500_000},
         {**plan[1], "start": 58_500_000}],
    ]
    forbidden_intervals = [
        (57_000_000, 58_000_000), (59_000_000, 60_000_000),
        (60_000_000, 61_000_000), (116_000_000, 117_000_000),
        (54_000_000, 55_000_000), (56_000_000, 57_000_000),
        (108_000_000, 109_000_000), (52_000_000, 53_000_000),
        (66_000_000, 67_000_000), *HISTORICAL_RANGES.values(),
        *E005_CALIBRATION_RANGES, (61_000_000, 62_000_000),
    ]
    for start, stop in forbidden_intervals:
        invalid.append([plan[0], {**plan[1], "start": start, "stop": stop}])
    for bad in invalid:
        with pytest.raises(ValueError):
            execute_generation_plan(bad, band_name="D10")
        assert calls == []
    with pytest.raises(ValueError, match="D10 generation only"):
        execute_generation_plan(generation_plan("H10"), band_name="H10")
    assert calls == []


def test_parallel_block_evaluator_preserves_exact_anchor_semantics() -> None:
    start, stop = 121, 151
    flags = bytearray(stop - start)
    for prime in (127, 131, 137, 139, 149):
        flags[prime - start] = 1
    _init_summary_worker(start, bytes(flags))
    result = _evaluate_anchor_block((start, stop))
    assert result["prime_count"] == 5
    assert result["first_prime"] == 127 and result["last_prime"] == 149
    assert result["admissible_count"] == result["prime_count"] + result["composite_count"]
    for family in FAMILY_ORDER:
        assert sum(result["prime_counters"][family].values()) == 5
        assert len(result["prime_signatures"][family]) == 5
