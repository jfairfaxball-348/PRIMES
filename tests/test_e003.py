from collections import Counter

import pytest

from experiments.E003_event_centred_neighbourhoods import (
    BANDS,
    BLOCK_RADIUS,
    _block_event,
    _dense_sparse_events,
    _execute_generation_plan,
    _frequency_table,
    _record_event,
    _record_events,
    _rolling_record_indices,
    _top_rankings,
    generation_plan,
    serialise_payload,
    validate_generation_plan,
)


def _primes_from_block_counts(start: int, counts: list[int]) -> list[int]:
    primes: list[int] = []
    for index, count in enumerate(counts):
        block_start = start + index * 1_000
        primes.extend(block_start + 1 + offset for offset in range(count))
    return primes


def test_globally_anchored_width_1000_occupancy() -> None:
    start = 100_000
    counts = [0] * 20
    counts[8:13] = [2, 3, 6, 4, 1]
    result = _dense_sparse_events(
        _primes_from_block_counts(start, counts),
        start=start,
        stop=120_000,
    )
    assert result["prime_dense"]["eligible_anchor_count"] == 4
    assert result["prime_dense"]["events"][0]["coordinate"] == 110_000


def test_full_radius_boundary_exclusion() -> None:
    start = 100_000
    counts = [1] * 20
    counts[7] = 10
    counts[8] = 9
    counts[11] = 8
    result = _dense_sparse_events(
        _primes_from_block_counts(start, counts),
        start=start,
        stop=120_000,
    )
    coordinates = [event["coordinate"] for event in result["prime_dense"]["events"]]
    assert 107_000 not in coordinates
    assert all(
        start + BLOCK_RADIUS * 1_000 <= value < 120_000 - BLOCK_RADIUS * 1_000
        for value in coordinates
    )


def test_strict_dense_sparse_inequalities_and_tie_rejection() -> None:
    start = 100_000
    counts = [5] * 20
    counts[8:13] = [4, 4, 7, 4, 4]
    result = _dense_sparse_events(
        _primes_from_block_counts(start, counts),
        start=start,
        stop=120_000,
    )
    assert [event["coordinate"] for event in result["prime_dense"]["events"]] == [110_000]

    counts[10] = 4
    tied = _dense_sparse_events(
        _primes_from_block_counts(start, counts),
        start=start,
        stop=120_000,
    )
    assert all(event["coordinate"] != 110_000 for event in tied["prime_dense"]["events"])
    assert all(event["coordinate"] != 110_000 for event in tied["prime_sparse"]["events"])

    counts[10] = 1
    sparse = _dense_sparse_events(
        _primes_from_block_counts(start, counts),
        start=start,
        stop=120_000,
    )
    assert [event["coordinate"] for event in sparse["prime_sparse"]["events"]] == [110_000]


def test_strict_64_gap_rolling_record_and_equal_max_nonrecord() -> None:
    gaps = list(range(1, 65)) + [64, 65, 64, 66]
    assert _rolling_record_indices(gaps) == [65, 67]


def test_record_classification_precedes_boundary_omission() -> None:
    gaps = [2] * 80
    gaps[70] = 100
    gaps[79] = 120
    primes = [1_000]
    for gap in gaps:
        primes.append(primes[-1] + gap)
    result = _record_events(primes)
    assert result["raw_record_count"] == 2
    assert result["serializable_count"] == 1
    assert result["boundary_omission_count"] == 1
    assert result["events"][0]["coordinate"]["gap_index"] == 70


def test_exact_block_neighbourhood_and_asymmetry_encodings() -> None:
    counts = list(range(1, 18))
    event = _block_event(counts, first_k=100, local_index=8, event_class="prime_dense")
    assert event["raw_word"] == tuple(range(1, 18))
    assert event["centered_residual_word"] == tuple(range(-8, 9))
    assert event["integer_asymmetry_vector"] == (6, 8, 10, 12, 14, 16)
    assert event["asymmetry_sign_signature"] == (1, 1, 1, 1, 1, 1)
    assert event["coordinate"] == 108_000


def test_exact_record_neighbourhood_and_asymmetry_encodings() -> None:
    gaps = list(range(2, 36, 2))
    primes = [1_000]
    for gap in gaps:
        primes.append(primes[-1] + gap)
    event = _record_event(primes, gaps, index=8)
    assert event["raw_word"] == tuple(range(2, 36, 2))
    assert event["centered_residual_word"] == tuple(range(-16, 18, 2))
    assert event["integer_asymmetry_vector"] == (4, 8, 12, 16, 20, 24, 28, 32)
    assert event["asymmetry_sign_signature"] == (1, 1, 1, 1, 1, 1, 1, 1)
    assert event["coordinate"] == {
        "left_prime": primes[8],
        "right_prime": primes[9],
        "gap_index": 8,
    }


def test_deterministic_frequency_and_ranking_order() -> None:
    counter = Counter({(2, 10): 3, (10, 2): 3, (2, 2): 1})
    assert _frequency_table(counter) == [
        {"value": [2, 2], "count": 1},
        {"value": [2, 10], "count": 3},
        {"value": [10, 2], "count": 3},
    ]
    assert _top_rankings(counter) == [
        {"value": [2, 10], "count": 3},
        {"value": [10, 2], "count": 3},
        {"value": [2, 2], "count": 1},
    ]


def test_byte_deterministic_serialization() -> None:
    payload = {"experiment": "E003", "events": {"prime_dense": []}, "range": [1, 2]}
    assert serialise_payload(payload) == serialise_payload(payload)


def test_fail_closed_generation_plan_guard(monkeypatch: pytest.MonkeyPatch) -> None:
    plan = generation_plan("D3")
    validate_generation_plan(plan, band_name="D3")
    assert plan[0]["stop"] < 100_000
    assert (plan[1]["start"], plan[1]["stop"]) == BANDS["D3"]

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
        validate_generation_plan(bad_prefix, band_name="D3")

    called = False

    def forbidden_sieve(_: int) -> list[int]:
        nonlocal called
        called = True
        return []

    monkeypatch.setattr(
        "experiments.E003_event_centred_neighbourhoods.sieve",
        forbidden_sieve,
    )
    with pytest.raises(ValueError, match="whole-prefix"):
        _execute_generation_plan(bad_prefix, band_name="D3")
    assert called is False

    for forbidden in (
        (33_500_000, 33_600_000),
        (36_500_000, 36_600_000),
        (37_000_000, 37_100_000),
        (70_000_000, 70_100_000),
    ):
        bad = [
            plan[0],
            {
                "purpose": "segmented_target",
                "strategy": "segmented",
                "start": forbidden[0],
                "stop": forbidden[1],
            },
        ]
        with pytest.raises(ValueError):
            validate_generation_plan(bad, band_name="D3")
