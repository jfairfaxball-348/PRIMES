#!/usr/bin/env python3
"""E006: frozen translation-overlap spectrum discovery evaluator."""

from __future__ import annotations

import argparse
import json
from collections.abc import Iterable, Mapping, Sequence
from math import isqrt
from pathlib import Path
from typing import Any

from primes_lab.core import sieve

EXPERIMENT_ID = "E006"
WIDTH = 1_000_000
HORIZON = 1_000
SHIFTS = tuple(range(2, HORIZON + 1, 2))
PROMOTION_CAP = 5
PROMOTION_CLASS_FLOOR = 8
PROMOTION_OCCURRENCE_FLOOR = 8
LOW_SUPPORT_STOP = 100_000

BANDS: dict[str, tuple[int, int]] = {
    "D6": (42_000_000, 43_000_000),
    "H6": (44_000_000, 45_000_000),
    "A6": (84_000_000, 85_000_000),
}
FROZEN_PARTITION: tuple[tuple[str, str, tuple[int, int]], ...] = (
    ("D6", "discovery", BANDS["D6"]),
    ("G6-mid", "guard", (43_000_000, 44_000_000)),
    ("H6", "holdout", BANDS["H6"]),
    ("A6", "adversarial", BANDS["A6"]),
)
PROTECTED_RANGES: dict[str, tuple[int, int]] = {
    "A1": (33_000_000, 34_000_000),
    "E003-pre-D3-guard": (34_000_000, 35_000_000),
    "D3": (35_000_000, 36_000_000),
    "E003-post-D3-guard": (36_000_000, 37_000_000),
    "H3": (37_000_000, 38_000_000),
    "G4-pre": (38_000_000, 39_000_000),
    "D4": (39_000_000, 40_000_000),
    "G4-mid": (40_000_000, 41_000_000),
    "H4": (41_000_000, 42_000_000),
    "G6-mid": (43_000_000, 44_000_000),
    "H6": BANDS["H6"],
    "A3": (70_000_000, 71_000_000),
    "A4": (78_000_000, 79_000_000),
    "A6": BANDS["A6"],
}


def _intersects(left: tuple[int, int], right: tuple[int, int]) -> bool:
    return max(left[0], right[0]) < min(left[1], right[1])


def generation_plan(band_name: str) -> list[dict[str, Any]]:
    try:
        start, stop = BANDS[band_name]
    except KeyError as exc:
        raise ValueError(f"unknown frozen E006 band: {band_name}") from exc
    return [
        {
            "purpose": "base_sieve_support",
            "strategy": "whole_prefix",
            "start": 0,
            "stop": isqrt(stop - 1) + 1,
        },
        {
            "purpose": "segmented_target",
            "strategy": "segmented",
            "start": start,
            "stop": stop,
        },
    ]


def validate_generation_plan(plan: list[dict[str, Any]], *, band_name: str) -> None:
    """Fail closed before any prime generator is invoked."""
    try:
        target = BANDS[band_name]
    except KeyError as exc:
        raise ValueError(f"unknown frozen E006 band: {band_name}") from exc

    if len(plan) != 2:
        raise ValueError("generation plan must contain exactly base support and one target")

    base_rows = [row for row in plan if row.get("purpose") == "base_sieve_support"]
    target_rows = [row for row in plan if row.get("purpose") == "segmented_target"]
    if len(base_rows) != 1 or len(target_rows) != 1:
        raise ValueError("generation plan must contain one base request and one target request")

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
            if purpose != "base_sieve_support" or strategy != "whole_prefix" or start != 0:
                raise ValueError("low support must be a whole-prefix base sieve from zero")
            continue

        if purpose != "segmented_target" or strategy != "segmented":
            raise ValueError("all high-value generation must use segmented target generation")
        if not (target[0] <= start and stop <= target[1]):
            raise ValueError("high-value interval is not a subset of the authorized target band")
        for name, excluded in PROTECTED_RANGES.items():
            if name == band_name:
                continue
            if _intersects(interval, excluded):
                raise ValueError(f"generation interval intersects protected/non-target range {name}")

    base = base_rows[0]
    target_row = target_rows[0]
    required_stop = isqrt(target[1] - 1) + 1
    if (int(base["start"]), int(base["stop"])) != (0, required_stop):
        raise ValueError("base sieve support must be exactly [0, floor(sqrt(U-1))+1)")
    if required_stop > LOW_SUPPORT_STOP:
        raise ValueError("required base support exceeds frozen safe low-support ceiling")
    if (int(target_row["start"]), int(target_row["stop"])) != target:
        raise ValueError("canonical E006 plan must generate the complete authorized target band")


def _execute_generation_plan(plan: list[dict[str, Any]], *, band_name: str) -> list[int]:
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


def band_prime_support(primes: Iterable[int], *, start: int, stop: int) -> frozenset[int]:
    """Return the exact band-local support of the supplied prime indicator."""
    if start < 0 or stop <= start:
        raise ValueError("start and stop must define a non-empty half-open band")
    return frozenset(prime for prime in primes if start <= prime < stop)


def _translation_overlap_count_from_support(
    support: frozenset[int], *, start: int, stop: int, shift: int
) -> int:
    if shift not in SHIFTS:
        raise ValueError("shift is outside the frozen even shift set")
    anchor_stop = stop - HORIZON
    if anchor_stop <= start:
        raise ValueError("band is too short for the frozen common anchor domain")
    return sum(
        1
        for left in support
        if start <= left < anchor_stop and left + shift in support
    )


def translation_overlap_counts(
    primes: Iterable[int], *, start: int, stop: int
) -> dict[int, int]:
    support = band_prime_support(primes, start=start, stop=stop)
    anchor_stop = stop - HORIZON
    if anchor_stop <= start:
        raise ValueError("band is too short for the frozen common anchor domain")
    anchors = tuple(sorted(prime for prime in support if prime < anchor_stop))
    return {
        shift: sum(1 for left in anchors if left + shift in support)
        for shift in SHIFTS
    }


def odd_radical(shift: int) -> int:
    if shift not in SHIFTS:
        raise ValueError("shift is outside the frozen even shift set")
    value = shift
    while value % 2 == 0:
        value //= 2
    radical = 1
    factor = 3
    while factor * factor <= value:
        if value % factor == 0:
            radical *= factor
            while value % factor == 0:
                value //= factor
        factor += 2
    if value > 1:
        radical *= value
    return radical


def radical_classes(shifts: Sequence[int] = SHIFTS) -> dict[int, tuple[int, ...]]:
    classes: dict[int, list[int]] = {}
    for shift in shifts:
        rho = odd_radical(shift)
        classes.setdefault(rho, []).append(shift)
    return {rho: tuple(sorted(classes[rho])) for rho in sorted(classes)}


def summarise_radical_classes(
    counts: Mapping[int, int],
    *,
    classes: Mapping[int, Sequence[int]] | None = None,
) -> list[dict[str, Any]]:
    class_map = radical_classes() if classes is None else classes
    summaries: list[dict[str, Any]] = []
    for rho in sorted(class_map):
        members = tuple(sorted(int(shift) for shift in class_map[rho]))
        if not members:
            raise ValueError("radical classes must be non-empty")
        member_counts = [int(counts[shift]) for shift in members]
        ranked = sorted(members, key=lambda shift: (-int(counts[shift]), shift))
        max_count = int(counts[ranked[0]])
        maximizing_shifts = [shift for shift in members if int(counts[shift]) == max_count]
        strict_unique = len(maximizing_shifts) == 1
        runner_up_count = int(counts[ranked[1]]) if len(ranked) >= 2 else 0
        row: dict[str, Any] = {
            "rho": int(rho),
            "member_shifts": list(members),
            "class_size": len(members),
            "member_counts": member_counts,
            "max_count": max_count,
            "runner_up_count": runner_up_count,
            "maximizing_shifts": maximizing_shifts,
            "strict_unique_maximum": strict_unique,
        }
        if len(members) >= 2:
            row["dominance_margin"] = max_count - runner_up_count
        summaries.append(row)
    return summaries


def promotion_pool(class_summaries: Sequence[Mapping[str, Any]]) -> list[dict[str, int]]:
    rows: list[dict[str, int]] = []
    for summary in class_summaries:
        class_size = int(summary["class_size"])
        max_count = int(summary["max_count"])
        strict_unique = bool(summary["strict_unique_maximum"])
        if class_size < PROMOTION_CLASS_FLOOR:
            continue
        if not strict_unique:
            continue
        if max_count < PROMOTION_OCCURRENCE_FLOOR:
            continue
        target_shift = int(summary["maximizing_shifts"][0])
        runner_up_count = int(summary["runner_up_count"])
        rows.append(
            {
                "rho": int(summary["rho"]),
                "class_size": class_size,
                "target_shift": target_shift,
                "target_count": max_count,
                "runner_up_count": runner_up_count,
                "dominance_margin": max_count - runner_up_count,
            }
        )

    return sorted(
        rows,
        key=lambda row: (
            -row["dominance_margin"],
            -row["target_count"],
            -row["class_size"],
            row["rho"],
            row["target_shift"],
        ),
    )


def selected_promotions(class_summaries: Sequence[Mapping[str, Any]]) -> list[dict[str, int]]:
    return promotion_pool(class_summaries)[:PROMOTION_CAP]


def summarise_primes(
    primes: Sequence[int],
    *,
    band_name: str,
    code_commit: str,
    plan: list[dict[str, Any]],
) -> dict[str, Any]:
    start, stop = BANDS[band_name]
    if any(prime < start or prime >= stop for prime in primes):
        raise ValueError("prime input contains a value outside the selected band")
    counts = translation_overlap_counts(primes, start=start, stop=stop)
    class_summaries = summarise_radical_classes(counts)
    return {
        "experiment": EXPERIMENT_ID,
        "implementation_commit": code_commit,
        "band": {
            "name": band_name,
            "range": [start, stop],
            "interval_semantics": "half-open",
        },
        "partition": [
            {"name": name, "role": role, "range": list(interval)}
            for name, role, interval in FROZEN_PARTITION
        ],
        "translation": {
            "horizon": HORIZON,
            "shift_set": list(SHIFTS),
            "common_anchor_domain": [start, stop - HORIZON],
            "overlap_definition": "sum_{x in [L,U-H)} I_B(x) I_B(x+h)",
        },
        "generation_plan": plan,
        "prime_summary": {
            "count": len(primes),
            "first_prime": primes[0] if primes else None,
            "last_prime": primes[-1] if primes else None,
        },
        "shifts": [
            {"h": shift, "rho": odd_radical(shift), "count": counts[shift]}
            for shift in SHIFTS
        ],
        "radical_classes": class_summaries,
        "promotion_pool": promotion_pool(class_summaries),
    }


def build_payload(*, band_name: str, code_commit: str) -> dict[str, Any]:
    plan = generation_plan(band_name)
    validate_generation_plan(plan, band_name=band_name)
    primes = _execute_generation_plan(plan, band_name=band_name)
    return summarise_primes(
        primes,
        band_name=band_name,
        code_commit=code_commit,
        plan=plan,
    )


def serialise_payload(payload: Mapping[str, Any]) -> bytes:
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
