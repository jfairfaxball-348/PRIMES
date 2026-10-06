from collections import Counter

import pytest

from primes_lab.core import (
    block_occupancy,
    finite_differences,
    gap_motifs,
    prime_gaps,
    record_gaps,
    residue_transitions,
    sieve,
)


def test_sieve_small() -> None:
    assert sieve(1) == []
    assert sieve(2) == [2]
    assert sieve(30) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]


def test_prime_gaps_and_differences() -> None:
    primes = [2, 3, 5, 7, 11]
    assert prime_gaps(primes) == [1, 2, 2, 4]
    assert finite_differences(primes, 0) == primes
    assert finite_differences(primes, 1) == [1, 2, 2, 4]
    assert finite_differences(primes, 2) == [1, 0, 2]


def test_negative_difference_order_rejected() -> None:
    with pytest.raises(ValueError):
        finite_differences([2, 3, 5], -1)


def test_gap_motifs() -> None:
    assert gap_motifs([2, 3, 5, 7, 11], 2) == Counter(
        {
            (1, 2): 1,
            (2, 2): 1,
            (2, 4): 1,
        }
    )


def test_residue_transitions_reduced_residues() -> None:
    transitions = residue_transitions([2, 3, 5, 7, 11, 13, 17, 19], 6)
    assert transitions == Counter({(5, 1): 3, (1, 5): 2})


def test_block_occupancy() -> None:
    primes = sieve(30)
    assert block_occupancy(primes, 10, start=0, stop=30) == [
        (0, 10, 4),
        (10, 20, 4),
        (20, 30, 2),
    ]


def test_record_gaps_are_strict_records() -> None:
    assert record_gaps([2, 3, 5, 7, 11, 13]) == [
        (1, 2, 3, 1),
        (2, 3, 5, 2),
        (4, 7, 11, 4),
    ]
