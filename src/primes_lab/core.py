"""Exact elementary transforms used by PRIMES discovery experiments."""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable, Sequence
from math import gcd, isqrt


def sieve(limit: int) -> list[int]:
    """Return all primes p with 2 <= p <= limit using an exact Eratosthenes sieve."""
    if limit < 2:
        return []

    flags = bytearray(b"\x01") * (limit + 1)
    flags[0:2] = b"\x00\x00"

    for p in range(2, isqrt(limit) + 1):
        if flags[p]:
            start = p * p
            count = ((limit - start) // p) + 1
            flags[start : limit + 1 : p] = b"\x00" * count

    return [n for n in range(2, limit + 1) if flags[n]]


def prime_gaps(primes: Sequence[int]) -> list[int]:
    """Return consecutive prime gaps."""
    return [b - a for a, b in zip(primes, primes[1:], strict=False)]


def finite_differences(values: Sequence[int], order: int = 1) -> list[int]:
    """Return the requested exact forward-difference order."""
    if order < 0:
        raise ValueError("order must be non-negative")

    result = list(values)
    for _ in range(order):
        result = [b - a for a, b in zip(result, result[1:], strict=False)]
    return result


def gap_motifs(primes: Sequence[int], width: int = 2) -> Counter[tuple[int, ...]]:
    """Count consecutive gap words of a fixed width."""
    if width < 1:
        raise ValueError("width must be at least 1")

    gaps = prime_gaps(primes)
    if len(gaps) < width:
        return Counter()

    return Counter(tuple(gaps[i : i + width]) for i in range(len(gaps) - width + 1))


def residue_transitions(
    primes: Sequence[int],
    modulus: int,
    *,
    reduced_residues_only: bool = True,
) -> Counter[tuple[int, int]]:
    """Count transitions between consecutive prime residues modulo the modulus.

    When reduced_residues_only is true, primes sharing a factor with the
    modulus are removed first. This prevents the finitely many prime divisors
    of the modulus from dominating short scans.
    """
    if modulus < 2:
        raise ValueError("modulus must be at least 2")

    selected: Iterable[int] = primes
    if reduced_residues_only:
        selected = (p for p in primes if gcd(p, modulus) == 1)

    residues = [p % modulus for p in selected]
    return Counter(zip(residues, residues[1:], strict=False))


def block_occupancy(
    primes: Sequence[int],
    block_width: int,
    *,
    start: int = 0,
    stop: int | None = None,
) -> list[tuple[int, int, int]]:
    """Count primes in exact half-open blocks [lo, hi)."""
    if block_width < 1:
        raise ValueError("block_width must be positive")
    if start < 0:
        raise ValueError("start must be non-negative")

    if stop is None:
        stop = (primes[-1] + 1) if primes else start
    if stop < start:
        raise ValueError("stop must be at least start")
    if stop == start:
        return []

    n_blocks = (stop - start + block_width - 1) // block_width
    counts = [0] * n_blocks

    for p in primes:
        if p < start:
            continue
        if p >= stop:
            break
        counts[(p - start) // block_width] += 1

    result: list[tuple[int, int, int]] = []
    for i, count in enumerate(counts):
        lo = start + i * block_width
        hi = min(lo + block_width, stop)
        result.append((lo, hi, count))
    return result


def record_gaps(primes: Sequence[int]) -> list[tuple[int, int, int, int]]:
    """Return record prime gaps as (left_index, left_prime, right_prime, gap)."""
    records: list[tuple[int, int, int, int]] = []
    current_record = -1

    for i, (left, right) in enumerate(zip(primes, primes[1:], strict=False), start=1):
        gap = right - left
        if gap > current_record:
            records.append((i, left, right, gap))
            current_record = gap

    return records
