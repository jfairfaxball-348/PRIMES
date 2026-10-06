#!/usr/bin/env python3
"""E001: frozen deterministic representation grid for PRIMES discovery."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

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

EXPERIMENT_ID = "E001"
GAP_MOTIF_WIDTHS = (2, 3, 4, 5, 6)
DIFFERENCE_ORDERS = (1, 2, 3, 4)
RESIDUE_MODULI = (6, 10, 12, 30, 60)
OCCUPANCY_WIDTHS = (100, 1_000, 10_000, 100_000)
EVENT_RADII = (2, 4, 8)
BANDS: dict[str, tuple[int, int]] = {
    "D0": (0, 1_000_000),
    "H0": (1_000_000, 2_000_000),
    "A0": (10_000_000, 11_000_000),
}


def _ranked_rows(counter: Counter[Any], limit: int = 20) -> list[dict[str, Any]]:
    return [{"item": item, "count": count} for item, count in ranked_counts(counter, limit)]


def _tuple_counter_table(
    counter: Counter[tuple[int, ...]], *, key_name: str
) -> list[dict[str, Any]]:
    return [{key_name: list(key), "count": counter[key]} for key in sorted(counter)]


def _integer_counter_table(counter: Counter[int]) -> list[dict[str, int]]:
    return [{"value": value, "count": counter[value]} for value in sorted(counter)]


def _serialise_block(row: tuple[int, int, int] | None) -> dict[str, int] | None:
    if row is None:
        return None
    lo, hi, count = row
    return {"start": lo, "stop": hi, "count": count}


def _serialise_occupancy(blocks: list[tuple[int, int, int]]) -> list[dict[str, int]]:
    return [
        {"start": lo, "stop": hi, "count": count}
        for lo, hi, count in blocks
    ]


def _event_neighbourhoods(
    global_primes: list[int],
    *,
    start: int,
    stop: int,
    radii: tuple[int, ...] = EVENT_RADII,
) -> dict[str, Any]:
    gaps = prime_gaps(global_primes)
    strict_records = record_gaps(global_primes)
    selected_records = [
        (left_index, left, right, gap)
        for left_index, left, right, gap in strict_records
        if start <= left < stop and start <= right < stop
    ]

    by_radius: dict[str, Any] = {}
    for radius in radii:
        neighbourhoods: list[dict[str, Any]] = []
        omission_count = 0
        for left_index, left, right, gap in selected_records:
            gap_index = left_index - 1
            first_gap = gap_index - radius
            last_gap = gap_index + radius
            if first_gap < 0 or last_gap >= len(gaps):
                omission_count += 1
                continue

            first_prime_index = first_gap
            last_prime_index = last_gap + 1
            if not (
                start <= global_primes[first_prime_index] < stop
                and start <= global_primes[last_prime_index] < stop
            ):
                omission_count += 1
                continue

            word = gaps[first_gap : last_gap + 1]
            neighbourhoods.append(
                {
                    "left_index": left_index,
                    "left_prime": left,
                    "right_prime": right,
                    "record_gap": gap,
                    "gap_word": word,
                }
            )

        by_radius[str(radius)] = {
            "radius": radius,
            "neighbourhood_count": len(neighbourhoods),
            "omission_count": omission_count,
            "neighbourhoods": neighbourhoods,
        }

    return {
        "event_definition": "strict_global_record_prime_gap",
        "selected_event_count": len(selected_records),
        "selected_events": [
            {
                "left_index": left_index,
                "left_prime": left,
                "right_prime": right,
                "gap": gap,
            }
            for left_index, left, right, gap in selected_records
        ],
        "radii": by_radius,
    }


def summarise_band(
    global_primes: list[int],
    *,
    band_name: str,
    start: int,
    stop: int,
    code_commit: str,
) -> dict[str, Any]:
    if start < 0 or stop <= start:
        raise ValueError("band must be a non-empty non-negative half-open interval")
    for width in OCCUPANCY_WIDTHS:
        if start % width != 0 or stop % width != 0:
            raise ValueError("E001 occupancy bands must align to every frozen global block width")

    selected = [p for p in global_primes if start <= p < stop]

    gap_sections: dict[str, Any] = {}
    for width in GAP_MOTIF_WIDTHS:
        counter = gap_motifs(selected, width=width)
        gap_sections[str(width)] = {
            "width": width,
            "window_count": sum(counter.values()),
            "distinct_count": len(counter),
            "complete_table": _tuple_counter_table(counter, key_name="motif"),
            "top_20": _ranked_rows(counter, 20),
        }

    difference_sections: dict[str, Any] = {}
    for order in DIFFERENCE_ORDERS:
        values = finite_differences(selected, order=order)
        counter = Counter(values)
        difference_sections[str(order)] = {
            "order": order,
            "sequence_length": len(values),
            "minimum": min(values) if values else None,
            "maximum": max(values) if values else None,
            "zero_count": counter.get(0, 0),
            "complete_table": _integer_counter_table(counter),
            "top_20": _ranked_rows(counter, 20),
        }

    transition_sections: dict[str, Any] = {}
    for modulus in RESIDUE_MODULI:
        counter = residue_transitions(selected, modulus, reduced_residues_only=True)
        transition_sections[str(modulus)] = {
            "modulus": modulus,
            "reduced_residues_only": True,
            "transition_count": sum(counter.values()),
            "distinct_count": len(counter),
            "complete_table": _tuple_counter_table(counter, key_name="transition"),
            "top_20": _ranked_rows(counter, 20),
        }

    occupancy_sections: dict[str, Any] = {}
    for width in OCCUPANCY_WIDTHS:
        blocks = block_occupancy(selected, width, start=start, stop=stop)
        extrema = occupancy_extrema(blocks)
        occupancy_sections[str(width)] = {
            "block_width": width,
            "blocks": _serialise_occupancy(blocks),
            "minimum": _serialise_block(extrema["minimum"]),
            "maximum": _serialise_block(extrema["maximum"]),
        }

    return {
        "experiment": EXPERIMENT_ID,
        "code_commit": code_commit,
        "band": {
            "name": band_name,
            "range": [start, stop],
            "interval_semantics": "half-open",
        },
        "grid_parameters": {
            "gap_motif_widths": list(GAP_MOTIF_WIDTHS),
            "difference_orders": list(DIFFERENCE_ORDERS),
            "residue_moduli": list(RESIDUE_MODULI),
            "reduced_residues_only": True,
            "occupancy_widths": list(OCCUPANCY_WIDTHS),
            "occupancy_anchor": 0,
            "record_gap_neighbourhood_radii": list(EVENT_RADII),
            "record_gap_event_definition": "strict_global_record_prime_gap",
        },
        "prime_summary": {
            "count": len(selected),
            "first_prime": selected[0] if selected else None,
            "last_prime": selected[-1] if selected else None,
        },
        "gap_motifs": gap_sections,
        "finite_differences": difference_sections,
        "residue_transitions": transition_sections,
        "occupancy": occupancy_sections,
        "record_gap_neighbourhoods": _event_neighbourhoods(
            global_primes, start=start, stop=stop
        ),
    }


def build_payload(*, band_name: str, code_commit: str) -> dict[str, Any]:
    try:
        start, stop = BANDS[band_name]
    except KeyError as exc:
        raise ValueError(f"unknown frozen E001 band: {band_name}") from exc
    global_primes = sieve(stop - 1)
    return summarise_band(
        global_primes,
        band_name=band_name,
        start=start,
        stop=stop,
        code_commit=code_commit,
    )


def serialise_payload(payload: dict[str, Any]) -> bytes:
    return (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--band", choices=tuple(BANDS), required=True)
    parser.add_argument("--code-commit", required=True)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_payload(band_name=args.band, code_commit=args.code_commit)
    rendered = serialise_payload(payload)
    if args.output is None:
        print(rendered.decode("utf-8"), end="")
    else:
        args.output.write_bytes(rendered)


if __name__ == "__main__":
    main()
