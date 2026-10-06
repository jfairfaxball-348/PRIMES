#!/usr/bin/env python3
"""E003: frozen event-centred neighbourhood discovery evaluator."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from math import isqrt
from pathlib import Path
from typing import Any

from primes_lab.core import sieve

EXPERIMENT_ID = "E003"
BLOCK_WIDTH = 1_000
SELECTION_RADIUS = 2
BLOCK_RADIUS = 8
GAP_RADIUS = 8
RECORD_LOOKBACK = 64
LOW_SUPPORT_STOP = 100_000
EVENT_CLASS_ORDER = ("prime_dense", "prime_sparse", "strict_rolling_record_gap")
OBJECT_FAMILY_ORDER = (
    "raw_word",
    "centered_residual_word",
    "integer_asymmetry_vector",
    "asymmetry_sign_signature",
)
BANDS: dict[str, tuple[int, int]] = {
    "D3": (35_000_000, 36_000_000),
    "H3": (37_000_000, 38_000_000),
    "A3": (70_000_000, 71_000_000),
}
PROTECTED_RANGES: dict[str, tuple[int, int]] = {
    "A1": (33_000_000, 34_000_000),
    "guard_before_D3": (34_000_000, 35_000_000),
    "guard_between_D3_H3": (36_000_000, 37_000_000),
    "H3": BANDS["H3"],
    "A3": BANDS["A3"],
}


def _intersects(left: tuple[int, int], right: tuple[int, int]) -> bool:
    return max(left[0], right[0]) < min(left[1], right[1])


def generation_plan(band_name: str) -> list[dict[str, Any]]:
    """Construct the complete prime-generation plan without generating primes."""
    try:
        start, stop = BANDS[band_name]
    except KeyError as exc:
        raise ValueError(f"unknown frozen E003 band: {band_name}") from exc
    base_stop = isqrt(stop - 1) + 1
    return [
        {
            "purpose": "base_sieve_support",
            "strategy": "whole_prefix",
            "start": 0,
            "stop": base_stop,
        },
        {
            "purpose": "segmented_target",
            "strategy": "segmented",
            "start": start,
            "stop": stop,
        },
    ]


def validate_generation_plan(plan: list[dict[str, Any]], *, band_name: str) -> None:
    """Fail closed unless every requested interval obeys the frozen E003 guard."""
    try:
        target = BANDS[band_name]
    except KeyError as exc:
        raise ValueError(f"unknown frozen E003 band: {band_name}") from exc
    if not plan:
        raise ValueError("generation plan must not be empty")

    saw_base = False
    saw_target = False
    for request in plan:
        start = int(request["start"])
        stop = int(request["stop"])
        strategy = str(request["strategy"])
        purpose = str(request["purpose"])
        if start < 0 or stop <= start:
            raise ValueError("generation intervals must be non-empty non-negative half-open ranges")
        interval = (start, stop)

        if strategy == "whole_prefix" and stop > LOW_SUPPORT_STOP:
            raise ValueError("whole-prefix generation above 100,000 is forbidden")

        if stop <= LOW_SUPPORT_STOP:
            if purpose != "base_sieve_support" or start != 0 or strategy != "whole_prefix":
                raise ValueError("low support must be an explicit whole-prefix base sieve from zero")
            saw_base = True
            continue

        if purpose != "segmented_target" or strategy != "segmented":
            raise ValueError("all high-value generation must use the segmented target strategy")
        if not (target[0] <= start and stop <= target[1]):
            raise ValueError("high-value interval is not a subset of the authorized target band")

        for name, excluded in PROTECTED_RANGES.items():
            if name == band_name:
                continue
            if _intersects(interval, excluded):
                raise ValueError(f"generation interval intersects protected range {name}")
        saw_target = True

    if not saw_base or not saw_target:
        raise ValueError("generation plan must contain both low base support and the active target")

    base = next(row for row in plan if row["purpose"] == "base_sieve_support")
    if base["stop"] - 1 != isqrt(target[1] - 1):
        raise ValueError("base sieve must end at floor(sqrt(U-1)) inclusive")


def _execute_generation_plan(plan: list[dict[str, Any]], *, band_name: str) -> list[int]:
    """Generate the target primes only after the complete plan has been validated."""
    validate_generation_plan(plan, band_name=band_name)
    base_request = next(row for row in plan if row["purpose"] == "base_sieve_support")
    target_request = next(row for row in plan if row["purpose"] == "segmented_target")

    base_primes = sieve(int(base_request["stop"]) - 1)
    start = int(target_request["start"])
    stop = int(target_request["stop"])
    flags = bytearray(b"\x01") * (stop - start)
    for prime in base_primes:
        first = max(prime * prime, ((start + prime - 1) // prime) * prime)
        if first >= stop:
            continue
        count = ((stop - 1 - first) // prime) + 1
        flags[first - start : stop - start : prime] = b"\x00" * count
    return [start + offset for offset, flag in enumerate(flags) if flag]


def _sign(value: int) -> int:
    return (value > 0) - (value < 0)


def _frequency_table(counter: Counter[tuple[int, ...]]) -> list[dict[str, Any]]:
    return [{"value": list(value), "count": counter[value]} for value in sorted(counter)]


def _top_rankings(counter: Counter[tuple[int, ...]], limit: int = 20) -> list[dict[str, Any]]:
    ranked = sorted(counter.items(), key=lambda item: (-item[1], item[0]))[:limit]
    return [{"value": list(value), "count": count} for value, count in ranked]


def _frequency_section(events: list[dict[str, Any]]) -> dict[str, Any]:
    sections: dict[str, Any] = {}
    for family in OBJECT_FAMILY_ORDER:
        counter = Counter(tuple(event[family]) for event in events)
        sections[family] = {
            "complete_table": _frequency_table(counter),
            "top_20": _top_rankings(counter, 20),
        }
    return sections


def _promotion_record(
    event_class: str,
    object_family: str,
    events: list[dict[str, Any]],
) -> dict[str, Any]:
    counter = Counter(tuple(event[object_family]) for event in events)
    ranked = sorted(counter.items(), key=lambda item: (-item[1], item[0]))
    mode_value = ranked[0][0] if ranked else None
    mode_count = ranked[0][1] if ranked else 0
    runner_up_count = ranked[1][1] if len(ranked) > 1 else 0
    strict_unique_mode = bool(ranked) and (len(ranked) == 1 or mode_count > runner_up_count)
    enough_events = len(events) >= 20
    enough_occurrences = mode_count >= 3
    return {
        "event_class": event_class,
        "object_family": object_family,
        "serializable_event_count": len(events),
        "mode_value": list(mode_value) if mode_value is not None else None,
        "mode_count": mode_count,
        "runner_up_count": runner_up_count,
        "dominance_margin": mode_count - runner_up_count,
        "strict_unique_mode": strict_unique_mode,
        "event_floor_passed": enough_events,
        "occurrence_floor_passed": enough_occurrences,
        "mechanical_frequency_eligible": enough_events and enough_occurrences and strict_unique_mode,
    }


def _promotion_pool(event_sections: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows = [
        _promotion_record(event_class, family, event_sections[event_class]["events"])
        for event_class in EVENT_CLASS_ORDER
        for family in OBJECT_FAMILY_ORDER
    ]
    family_priority = {name: index for index, name in enumerate(OBJECT_FAMILY_ORDER)}
    class_priority = {name: index for index, name in enumerate(EVENT_CLASS_ORDER)}
    return sorted(
        rows,
        key=lambda row: (
            family_priority[row["object_family"]],
            -row["dominance_margin"],
            -row["mode_count"],
            class_priority[row["event_class"]],
            tuple(row["mode_value"] or []),
        ),
    )


def _block_counts(primes: list[int], *, start: int, stop: int) -> tuple[int, list[int]]:
    if start % BLOCK_WIDTH != 0 or stop % BLOCK_WIDTH != 0:
        raise ValueError("E003 bands must align to globally anchored width-1,000 blocks")
    first_k = start // BLOCK_WIDTH
    block_count = (stop - start) // BLOCK_WIDTH
    counts = [0] * block_count
    for prime in primes:
        if start <= prime < stop:
            counts[prime // BLOCK_WIDTH - first_k] += 1
    return first_k, counts


def _block_event(
    counts: list[int],
    *,
    first_k: int,
    local_index: int,
    event_class: str,
) -> dict[str, Any]:
    raw = tuple(
        counts[local_index + offset] for offset in range(-BLOCK_RADIUS, BLOCK_RADIUS + 1)
    )
    center = raw[BLOCK_RADIUS]
    residual = tuple(value - center for value in raw)
    asymmetry = tuple(
        counts[local_index + offset] - counts[local_index - offset]
        for offset in range(SELECTION_RADIUS + 1, BLOCK_RADIUS + 1)
    )
    signs = tuple(_sign(value) for value in asymmetry)
    return {
        "event_class": event_class,
        "coordinate": (first_k + local_index) * BLOCK_WIDTH,
        "raw_word": raw,
        "centered_residual_word": residual,
        "integer_asymmetry_vector": asymmetry,
        "asymmetry_sign_signature": signs,
    }


def _dense_sparse_events(primes: list[int], *, start: int, stop: int) -> dict[str, dict[str, Any]]:
    first_k, counts = _block_counts(primes, start=start, stop=stop)
    dense: list[dict[str, Any]] = []
    sparse: list[dict[str, Any]] = []
    eligible = 0
    for local_index in range(BLOCK_RADIUS, len(counts) - BLOCK_RADIUS):
        eligible += 1
        center = counts[local_index]
        neighbours = [
            counts[local_index - 2],
            counts[local_index - 1],
            counts[local_index + 1],
            counts[local_index + 2],
        ]
        if all(center > value for value in neighbours):
            dense.append(
                _block_event(
                    counts,
                    first_k=first_k,
                    local_index=local_index,
                    event_class="prime_dense",
                )
            )
        if all(center < value for value in neighbours):
            sparse.append(
                _block_event(
                    counts,
                    first_k=first_k,
                    local_index=local_index,
                    event_class="prime_sparse",
                )
            )
    return {
        "prime_dense": {"eligible_anchor_count": eligible, "events": dense},
        "prime_sparse": {"eligible_anchor_count": eligible, "events": sparse},
    }


def _rolling_record_indices(gaps: list[int]) -> list[int]:
    records: list[int] = []
    for index in range(RECORD_LOOKBACK, len(gaps)):
        if gaps[index] > max(gaps[index - RECORD_LOOKBACK : index]):
            records.append(index)
    return records


def _record_event(primes: list[int], gaps: list[int], *, index: int) -> dict[str, Any]:
    raw = tuple(gaps[index + offset] for offset in range(-GAP_RADIUS, GAP_RADIUS + 1))
    center = gaps[index]
    residual = tuple(value - center for value in raw)
    asymmetry = tuple(
        gaps[index + offset] - gaps[index - offset] for offset in range(1, GAP_RADIUS + 1)
    )
    signs = tuple(_sign(value) for value in asymmetry)
    return {
        "event_class": "strict_rolling_record_gap",
        "coordinate": {
            "left_prime": primes[index],
            "right_prime": primes[index + 1],
            "gap_index": index,
        },
        "raw_word": raw,
        "centered_residual_word": residual,
        "integer_asymmetry_vector": asymmetry,
        "asymmetry_sign_signature": signs,
    }


def _record_events(primes: list[int]) -> dict[str, Any]:
    gaps = [right - left for left, right in zip(primes, primes[1:], strict=False)]
    record_indices = _rolling_record_indices(gaps)
    events: list[dict[str, Any]] = []
    omissions = 0
    for index in record_indices:
        if index - GAP_RADIUS < 0 or index + GAP_RADIUS >= len(gaps):
            omissions += 1
            continue
        events.append(_record_event(primes, gaps, index=index))
    events.sort(
        key=lambda event: (
            event["coordinate"]["left_prime"],
            event["coordinate"]["right_prime"],
            event["coordinate"]["gap_index"],
        )
    )
    return {
        "raw_record_count": len(record_indices),
        "serializable_count": len(events),
        "boundary_omission_count": omissions,
        "events": events,
    }


def _serialise_event(event: dict[str, Any]) -> dict[str, Any]:
    return {
        "coordinate": event["coordinate"],
        "raw_word": list(event["raw_word"]),
        "centered_residual_word": list(event["centered_residual_word"]),
        "integer_asymmetry_vector": list(event["integer_asymmetry_vector"]),
        "asymmetry_sign_signature": list(event["asymmetry_sign_signature"]),
    }


def summarise_primes(
    primes: list[int],
    *,
    band_name: str,
    start: int,
    stop: int,
    code_commit: str,
    plan: list[dict[str, Any]],
) -> dict[str, Any]:
    dense_sparse = _dense_sparse_events(primes, start=start, stop=stop)
    records = _record_events(primes)
    event_sections: dict[str, dict[str, Any]] = {
        "prime_dense": {"events": dense_sparse["prime_dense"]["events"]},
        "prime_sparse": {"events": dense_sparse["prime_sparse"]["events"]},
        "strict_rolling_record_gap": {"events": records["events"]},
    }

    payload_events: dict[str, Any] = {}
    for event_class in EVENT_CLASS_ORDER:
        events = event_sections[event_class]["events"]
        section: dict[str, Any] = {
            "event_count": len(events),
            "event_catalog": [_serialise_event(event) for event in events],
            "frequencies": _frequency_section(events),
        }
        if event_class in ("prime_dense", "prime_sparse"):
            section["eligible_anchor_count"] = dense_sparse[event_class]["eligible_anchor_count"]
        else:
            section["raw_record_count"] = records["raw_record_count"]
            section["serializable_count"] = records["serializable_count"]
            section["boundary_omission_count"] = records["boundary_omission_count"]
        payload_events[event_class] = section

    return {
        "experiment": EXPERIMENT_ID,
        "implementation_commit": code_commit,
        "band": {
            "name": band_name,
            "range": [start, stop],
            "interval_semantics": "half-open",
        },
        "generation_plan": plan,
        "parameters": {
            "block_width": BLOCK_WIDTH,
            "selection_radius_blocks": SELECTION_RADIUS,
            "descriptive_radius_blocks": BLOCK_RADIUS,
            "descriptive_radius_gaps": GAP_RADIUS,
            "record_lookback_gaps": RECORD_LOOKBACK,
            "event_class_order": list(EVENT_CLASS_ORDER),
            "object_family_order": list(OBJECT_FAMILY_ORDER),
            "occupancy_anchor": 0,
        },
        "prime_summary": {
            "count": len(primes),
            "first_prime": primes[0] if primes else None,
            "last_prime": primes[-1] if primes else None,
        },
        "events": payload_events,
        "promotion_pool": _promotion_pool(event_sections),
    }


def build_payload(*, band_name: str, code_commit: str) -> dict[str, Any]:
    plan = generation_plan(band_name)
    validate_generation_plan(plan, band_name=band_name)
    primes = _execute_generation_plan(plan, band_name=band_name)
    start, stop = BANDS[band_name]
    return summarise_primes(
        primes,
        band_name=band_name,
        start=start,
        stop=stop,
        code_commit=code_commit,
        plan=plan,
    )


def serialise_payload(payload: dict[str, Any]) -> bytes:
    return (json.dumps(payload, sort_keys=True, indent=2) + "\n").encode("utf-8")


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
