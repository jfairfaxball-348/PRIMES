from collections import Counter

from experiments.E001_representation_grid import (
    _event_neighbourhoods,
    _tuple_counter_table,
    serialise_payload,
    summarise_band,
)


def _tiny_summary() -> dict[str, object]:
    global_primes = [
        2,
        3,
        5,
        7,
        11,
        13,
        17,
        19,
        23,
        29,
        31,
        37,
        41,
        43,
        47,
    ]
    return summarise_band(
        global_primes,
        band_name="TEST",
        start=0,
        stop=100_000,
        code_commit="deadbeef",
    )


def test_band_boundary_exclusion() -> None:
    # Crossing gaps 99_989->100_003 and 100_069->200_003 are not band-local.
    global_primes = [99_989, 100_003, 100_019, 100_043, 100_049, 100_057, 100_069, 200_003]
    summary = summarise_band(
        global_primes,
        band_name="TEST",
        start=100_000,
        stop=200_000,
        code_commit="deadbeef",
    )
    assert summary["prime_summary"] == {
        "count": 6,
        "first_prime": 100_003,
        "last_prime": 100_069,
    }
    assert summary["finite_differences"]["1"]["complete_table"] == [
        {"value": 6, "count": 1},
        {"value": 8, "count": 1},
        {"value": 12, "count": 1},
        {"value": 16, "count": 1},
        {"value": 24, "count": 1},
    ]
    assert summary["gap_motifs"]["2"]["window_count"] == 4


def test_globally_anchored_occupancy_blocks() -> None:
    global_primes = [100_003, 100_019, 100_043, 100_049, 100_057, 100_069, 100_103]
    summary = summarise_band(
        global_primes,
        band_name="TEST",
        start=100_000,
        stop=200_000,
        code_commit="deadbeef",
    )
    blocks = summary["occupancy"]["100"]["blocks"]
    assert blocks[0] == {"start": 100_000, "stop": 100_100, "count": 6}
    assert blocks[1] == {"start": 100_100, "stop": 100_200, "count": 1}


def test_strict_global_record_gap_event_selection() -> None:
    global_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]
    events = _event_neighbourhoods(global_primes, start=10, stop=40, radii=(2,))
    assert events["selected_events"] == [
        {"left_index": 9, "left_prime": 23, "right_prime": 29, "gap": 6}
    ]
    radius = events["radii"]["2"]
    assert radius["omission_count"] == 0
    assert radius["neighbourhoods"][0]["gap_word"] == [2, 4, 6, 2, 6]


def test_deterministic_counter_ordering() -> None:
    counter = Counter({(10, 2): 5, (2, 10): 5, (2, 2): 1})
    assert _tuple_counter_table(counter, key_name="motif") == [
        {"motif": [2, 2], "count": 1},
        {"motif": [2, 10], "count": 5},
        {"motif": [10, 2], "count": 5},
    ]


def test_byte_deterministic_output() -> None:
    first = serialise_payload(_tiny_summary())
    second = serialise_payload(_tiny_summary())
    assert first == second
