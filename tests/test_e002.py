from collections import Counter

from experiments.E002_cross_scale_persistence import (
    _obs001_evidence,
    _obs002_evidence,
    _residue_support_evidence,
    _strict_target_mode,
    evaluate_band,
    serialise_payload,
)


def test_band_boundary_exclusion() -> None:
    global_primes = [99_989, 100_003, 100_019, 100_043, 100_049, 100_057, 100_069, 200_003]
    result = evaluate_band(
        global_primes,
        band_name="TEST",
        start=100_000,
        stop=200_000,
    )
    assert result["prime_summary"] == {
        "count": 6,
        "first_prime": 100_003,
        "last_prime": 100_069,
    }
    assert result["OBS-001"]["third_difference_count"] == 3
    assert result["OBS-002"]["motif_window_count"] == 4


def test_obs001_strict_mode_and_tie_failure() -> None:
    assert _strict_target_mode(Counter({0: 3, 6: 2}), 0) == (3, 6, 2, True)
    assert _strict_target_mode(Counter({0: 2, 6: 2}), 0) == (2, 6, 2, False)
    assert _obs001_evidence([2, 3, 5])["passed"] is False


def test_obs002_strict_mode_and_tie_failure() -> None:
    target = (6, 6)
    assert _strict_target_mode(Counter({target: 3, (4, 6): 2}), target) == (
        3,
        (4, 6),
        2,
        True,
    )
    assert _strict_target_mode(Counter({target: 2, (4, 6): 2}), target) == (
        2,
        (4, 6),
        2,
        False,
    )
    assert _obs002_evidence([2, 3])["passed"] is False


def test_obs003_reduced_residue_filter_and_full_support() -> None:
    full = _residue_support_evidence([2, 3, 7, 13, 17, 23, 31], 6)
    assert full == {
        "modulus": 6,
        "possible_support_size": 4,
        "observed_distinct_support_size": 4,
        "missing": [],
        "passed": True,
    }

    incomplete = _residue_support_evidence([2, 3, 5, 7, 11, 13, 17, 19], 6)
    assert incomplete["observed_distinct_support_size"] == 2
    assert incomplete["missing"] == [[1, 1], [5, 5]]
    assert incomplete["passed"] is False


def test_deterministic_tie_and_missing_pair_ordering() -> None:
    target_count, competitor, competitor_count, passed = _strict_target_mode(
        Counter({0: 6, 12: 5, 6: 5}), 0
    )
    assert (target_count, competitor, competitor_count, passed) == (6, 12, 5, True)

    incomplete = _residue_support_evidence([5, 7, 11], 6)
    assert incomplete["missing"] == [[1, 1], [5, 5]]


def test_byte_deterministic_serialization() -> None:
    payload = {
        "experiment": "E002",
        "overall_outcomes": {"OBS-002": "PERSISTENT", "OBS-001": "PERSISTENT"},
        "results": [],
    }
    assert serialise_payload(payload) == serialise_payload(payload)
