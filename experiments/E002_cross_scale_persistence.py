#!/usr/bin/env python3
"""E002: frozen criterion-only cross-scale persistence evaluation."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from math import gcd, isqrt
from pathlib import Path
from typing import Any, TypeVar

from primes_lab.core import finite_differences, gap_motifs, residue_transitions, sieve
from primes_lab.patterns import ranked_counts

EXPERIMENT_ID = "E002"
BANDS: dict[str, tuple[int, int]] = {
    "S1": (2_000_000, 3_000_000),
    "S2": (4_000_000, 5_000_000),
    "S3": (8_000_000, 9_000_000),
    "S4": (16_000_000, 17_000_000),
    "S5": (32_000_000, 33_000_000),
}
RESIDUE_MODULI = (6, 10, 12, 30, 60)
TARGET_THIRD_DIFFERENCE = 0
TARGET_GAP_MOTIF = (6, 6)

T = TypeVar("T")


def _sieve_band(start: int, stop: int) -> list[int]:
    """Return primes in [start, stop) without generating primes in intervening ranges."""
    if start < 0 or stop <= start:
        raise ValueError("band must be a non-empty non-negative half-open interval")

    flags = bytearray(b"\x01") * (stop - start)
    for value in range(start, min(stop, 2)):
        flags[value - start] = 0

    for prime in sieve(isqrt(stop - 1)):
        first = max(prime * prime, ((start + prime - 1) // prime) * prime)
        if first >= stop:
            continue
        count = ((stop - 1 - first) // prime) + 1
        flags[first - start : stop - start : prime] = b"\x00" * count

    return [start + offset for offset, flag in enumerate(flags) if flag]


def _strict_target_mode(counter: Counter[T], target: T) -> tuple[int, T | None, int, bool]:
    """Return target count, deterministic best competitor, its count, and strict-win status."""
    target_count = counter.get(target, 0)
    competitors = Counter({item: count for item, count in counter.items() if item != target})
    ranked = ranked_counts(competitors, 1)
    if ranked:
        competitor, competitor_count = ranked[0]
    else:
        competitor, competitor_count = None, 0
    passed = target_count > 0 and target_count > competitor_count
    return target_count, competitor, competitor_count, passed


def _obs001_evidence(primes: list[int]) -> dict[str, Any]:
    values = finite_differences(primes, order=3)
    counter = Counter(values)
    target_count, competitor, competitor_count, passed = _strict_target_mode(
        counter, TARGET_THIRD_DIFFERENCE
    )
    if not values:
        passed = False
    return {
        "third_difference_count": len(values),
        "zero_count": target_count,
        "highest_frequency_competitor": {
            "value": competitor,
            "count": competitor_count,
        },
        "passed": passed,
    }


def _obs002_evidence(primes: list[int]) -> dict[str, Any]:
    counter = gap_motifs(primes, width=2)
    target_count, competitor, competitor_count, passed = _strict_target_mode(
        counter, TARGET_GAP_MOTIF
    )
    if not counter:
        passed = False
    return {
        "motif_window_count": sum(counter.values()),
        "target_motif": list(TARGET_GAP_MOTIF),
        "target_count": target_count,
        "highest_frequency_competitor": {
            "motif": list(competitor) if competitor is not None else None,
            "count": competitor_count,
        },
        "passed": passed,
    }


def _reduced_residues(modulus: int) -> tuple[int, ...]:
    return tuple(residue for residue in range(modulus) if gcd(residue, modulus) == 1)


def _residue_support_evidence(primes: list[int], modulus: int) -> dict[str, Any]:
    residues = _reduced_residues(modulus)
    possible = [(left, right) for left in residues for right in residues]
    counter = residue_transitions(primes, modulus, reduced_residues_only=True)
    observed = set(counter)
    missing = [pair for pair in possible if pair not in observed]
    return {
        "modulus": modulus,
        "possible_support_size": len(possible),
        "observed_distinct_support_size": len(observed),
        "missing": [list(pair) for pair in missing],
        "passed": not missing and observed == set(possible),
    }


def _obs003_evidence(primes: list[int]) -> dict[str, Any]:
    support = [_residue_support_evidence(primes, modulus) for modulus in RESIDUE_MODULI]
    return {
        "moduli": support,
        "passed": all(row["passed"] for row in support),
    }


def evaluate_band(
    global_primes: list[int], *, band_name: str, start: int, stop: int
) -> dict[str, Any]:
    """Evaluate only the three frozen E002 criteria on one half-open band."""
    selected = [prime for prime in global_primes if start <= prime < stop]
    return {
        "band": band_name,
        "range": [start, stop],
        "prime_summary": {
            "count": len(selected),
            "first_prime": selected[0] if selected else None,
            "last_prime": selected[-1] if selected else None,
        },
        "OBS-001": _obs001_evidence(selected),
        "OBS-002": _obs002_evidence(selected),
        "OBS-003": _obs003_evidence(selected),
    }


def build_payload(*, code_commit: str) -> dict[str, Any]:
    """Evaluate the complete frozen five-band ladder without early stopping."""
    bands = [
        evaluate_band(
            _sieve_band(start, stop),
            band_name=name,
            start=start,
            stop=stop,
        )
        for name, (start, stop) in BANDS.items()
    ]
    outcomes = {
        observation: (
            "PERSISTENT"
            if all(band[observation]["passed"] for band in bands)
            else "NOT PERSISTENT"
        )
        for observation in ("OBS-001", "OBS-002", "OBS-003")
    }
    return {
        "experiment": EXPERIMENT_ID,
        "implementation_commit": code_commit,
        "bands": [
            {"name": name, "range": [start, stop]}
            for name, (start, stop) in BANDS.items()
        ],
        "frozen_moduli": list(RESIDUE_MODULI),
        "criteria": {
            "OBS-001": "third difference 0 is the strict unique mode",
            "OBS-002": "width-2 gap motif [6,6] is the strict unique mode",
            "OBS-003": "complete directed reduced-residue transition support at every frozen modulus",
        },
        "results": bands,
        "overall_outcomes": outcomes,
    }


def serialise_payload(payload: dict[str, Any]) -> bytes:
    return (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--code-commit", required=True)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rendered = serialise_payload(build_payload(code_commit=args.code_commit))
    if args.output is None:
        print(rendered.decode("utf-8"), end="")
    else:
        args.output.write_bytes(rendered)


if __name__ == "__main__":
    main()
