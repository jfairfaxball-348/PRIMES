#!/usr/bin/env python3
"""E000: deterministic baseline scan for the PRIMES discovery pipeline."""

from __future__ import annotations

import argparse
import json
from collections import Counter

from primes_lab.core import (
    block_occupancy,
    finite_differences,
    gap_motifs,
    prime_gaps,
    record_gaps,
    residue_transitions,
    sieve,
)
from primes_lab.patterns import occupancy_extrema, ranked_counts


def _serialise_ranked(rows: list[tuple[object, int]]) -> list[dict[str, object]]:
    return [{"item": item, "count": count} for item, count in rows]


def summarise(
    primes: list[int],
    *,
    start: int,
    stop: int,
    motif_width: int,
    modulus: int,
    block_width: int,
) -> dict[str, object]:
    selected = [p for p in primes if start <= p < stop]
    gaps = prime_gaps(selected)
    second_differences = finite_differences(selected, order=2)

    motifs = gap_motifs(selected, width=motif_width)
    transitions = residue_transitions(selected, modulus)
    occupancy = block_occupancy(
        selected,
        block_width,
        start=start,
        stop=stop,
    )

    return {
        "range": [start, stop],
        "prime_count": len(selected),
        "first_prime": selected[0] if selected else None,
        "last_prime": selected[-1] if selected else None,
        "gap": {
            "count": len(gaps),
            "minimum": min(gaps) if gaps else None,
            "maximum": max(gaps) if gaps else None,
            "distinct": len(set(gaps)),
        },
        "second_difference": {
            "count": len(second_differences),
            "minimum": min(second_differences) if second_differences else None,
            "maximum": max(second_differences) if second_differences else None,
            "zero_count": Counter(second_differences).get(0, 0),
        },
        "top_gap_motifs": _serialise_ranked(ranked_counts(motifs, 12)),
        "top_residue_transitions": _serialise_ranked(ranked_counts(transitions, 20)),
        "block_occupancy_extrema": occupancy_extrema(occupancy),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=100_000)
    parser.add_argument("--motif-width", type=int, default=3)
    parser.add_argument("--modulus", type=int, default=30)
    parser.add_argument("--block-width", type=int, default=1_000)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.limit < 100:
        raise SystemExit("--limit must be at least 100 for E000")

    primes = sieve(args.limit)
    split = args.limit // 2

    payload = {
        "experiment": "E000",
        "purpose": "pipeline validation and baseline observation bundle; no novelty claim",
        "parameters": {
            "limit": args.limit,
            "motif_width": args.motif_width,
            "modulus": args.modulus,
            "block_width": args.block_width,
            "split": split,
        },
        "whole_range": summarise(
            primes,
            start=0,
            stop=args.limit + 1,
            motif_width=args.motif_width,
            modulus=args.modulus,
            block_width=args.block_width,
        ),
        "early_range": summarise(
            primes,
            start=0,
            stop=split,
            motif_width=args.motif_width,
            modulus=args.modulus,
            block_width=args.block_width,
        ),
        "late_range": summarise(
            primes,
            start=split,
            stop=args.limit + 1,
            motif_width=args.motif_width,
            modulus=args.modulus,
            block_width=args.block_width,
        ),
        "record_gaps": [
            {
                "left_index": i,
                "left_prime": left,
                "right_prime": right,
                "gap": gap,
            }
            for i, left, right, gap in record_gaps(primes)
        ],
    }

    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
