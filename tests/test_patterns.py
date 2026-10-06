from collections import Counter

from primes_lab.patterns import occupancy_extrema, ranked_counts


def test_ranked_counts_is_deterministic() -> None:
    counts = Counter({(2, 4): 3, (4, 2): 3, (6, 6): 1})
    assert ranked_counts(counts, 2) == [((2, 4), 3), ((4, 2), 3)]


def test_occupancy_extrema() -> None:
    blocks = [(0, 10, 4), (10, 20, 4), (20, 30, 2)]
    assert occupancy_extrema(blocks) == {
        "minimum": (20, 30, 2),
        "maximum": (0, 10, 4),
    }
    assert occupancy_extrema([]) == {"minimum": None, "maximum": None}
