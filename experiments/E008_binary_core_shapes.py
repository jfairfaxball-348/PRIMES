#!/usr/bin/env python3
"""E008: frozen binary core-shape discovery evaluator."""
from __future__ import annotations

import argparse
import json
from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from math import gcd, isqrt
from pathlib import Path
from typing import Any, TypeAlias

from primes_lab.core import sieve

EXPERIMENT_ID = "E008"
WIDTH = 1_000_000
Q = 210
SHELL = (1 << 25, 1 << 26)
J = 19
LOW_SUPPORT_STOP = 100_000
POPULATION_FLOOR = 1_000
OCCURRENCE_FLOOR = 32
PROMOTION_CAP = 4
FAMILY_ORDER = ("B1", "B2", "B3", "B4")

BANDS: dict[str, tuple[int, int]] = {
    "D8": (50_000_000, 51_000_000),
    "H8": (52_000_000, 53_000_000),
    "A8": (66_000_000, 67_000_000),
}
FROZEN_PARTITION: tuple[tuple[str, str, tuple[int, int]], ...] = (
    ("G8-pre", "guard", (49_000_000, 50_000_000)),
    ("D8", "discovery", BANDS["D8"]),
    ("G8-mid", "guard", (51_000_000, 52_000_000)),
    ("H8", "holdout", BANDS["H8"]),
    ("A8", "adversarial", BANDS["A8"]),
)

EXCLUDED_RANGES: dict[str, tuple[int, int]] = {
    "D0": (0, 1_000_000),
    "H0": (1_000_000, 2_000_000),
    "S1": (2_000_000, 3_000_000),
    "S2": (4_000_000, 5_000_000),
    "S3": (8_000_000, 9_000_000),
    "A0-retired": (10_000_000, 11_000_000),
    "S4": (16_000_000, 17_000_000),
    "S5": (32_000_000, 33_000_000),
    "A1": (33_000_000, 34_000_000),
    "E003-pre-D3-guard": (34_000_000, 35_000_000),
    "D3": (35_000_000, 36_000_000),
    "E003-post-D3-guard": (36_000_000, 37_000_000),
    "H3": (37_000_000, 38_000_000),
    "G4-pre": (38_000_000, 39_000_000),
    "D4": (39_000_000, 40_000_000),
    "G4-mid": (40_000_000, 41_000_000),
    "H4": (41_000_000, 42_000_000),
    "D6": (42_000_000, 43_000_000),
    "G6-mid": (43_000_000, 44_000_000),
    "H6": (44_000_000, 45_000_000),
    "G7-pre": (45_000_000, 46_000_000),
    "D7": (46_000_000, 47_000_000),
    "G7-mid": (47_000_000, 48_000_000),
    "H7": (48_000_000, 49_000_000),
    "G8-pre": (49_000_000, 50_000_000),
    "D8": BANDS["D8"],
    "G8-mid": (51_000_000, 52_000_000),
    "H8": BANDS["H8"],
    "A8": BANDS["A8"],
    "A3": (70_000_000, 71_000_000),
    "A4": (78_000_000, 79_000_000),
    "A6": (84_000_000, 85_000_000),
    "A7": (92_000_000, 93_000_000),
}

FAMILY_DEFINITIONS: dict[str, str] = {
    "B1": "Hamming weight of w(x)",
    "B2": "adjacent transition count of w(x)",
    "B3": "(longest zero run, longest one run) in w(x)",
    "B4": "nonincreasing sorted tuple of maximal run lengths of w(x)",
}

Signature: TypeAlias = int | tuple[int, ...]

PAYLOAD_KEYS = frozenset(
    {
        "experiment",
        "implementation_commit",
        "band",
        "partition",
        "parameters",
        "generation_plan",
        "anchor_summary",
        "validation",
        "families",
        "promotions",
    }
)
ANCHOR_SUMMARY_KEYS = frozenset(
    {"admissible_count", "prime_count", "composite_count", "first_prime", "last_prime"}
)
VALIDATION_KEYS = frozenset(
    {
        "admissible_partition_failure_count",
        "binary_reconstruction_failure_count",
        "core_length_failure_count",
        "parity_control_failure_count",
    }
)
FAMILY_ROW_KEYS = frozenset(
    {
        "family",
        "prime_frequency_table",
        "composite_frequency_table",
        "prime_mode_count",
        "prime_maximizing_signatures",
        "runner_up_count",
        "strict_unique_prime_mode",
        "unique_mode_composite_count",
        "unique_mode_enrichment_numerator",
        "population_floor_passed",
        "occurrence_floor_passed",
        "enrichment_passed",
        "mechanically_eligible",
    }
)


def _intersects(left: tuple[int, int], right: tuple[int, int]) -> bool:
    return max(left[0], right[0]) < min(left[1], right[1])


def validate_frozen_metadata() -> None:
    if Q != 2 * 3 * 5 * 7:
        raise ValueError("Q must remain exactly 210")
    if WIDTH != 1_000_000:
        raise ValueError("frozen width changed")
    if J != (WIDTH - 1).bit_length() - 1 or J != 19:
        raise ValueError("frozen J derivation changed")
    if SHELL != (33_554_432, 67_108_864):
        raise ValueError("frozen 26-bit shell changed")
    expected = {
        "G8-pre": (49_000_000, 50_000_000),
        "D8": (50_000_000, 51_000_000),
        "G8-mid": (51_000_000, 52_000_000),
        "H8": (52_000_000, 53_000_000),
        "A8": (66_000_000, 67_000_000),
    }
    for name, _, interval in FROZEN_PARTITION:
        if interval != expected[name] or interval[1] - interval[0] != WIDTH:
            raise ValueError("frozen E008 partition changed")
        if not (SHELL[0] <= interval[0] < interval[1] <= SHELL[1]):
            raise ValueError("E008 target/guard band left the frozen 26-bit shell")


def generation_plan(band_name: str) -> list[dict[str, Any]]:
    try:
        start, stop = BANDS[band_name]
    except KeyError as exc:
        raise ValueError(f"unknown frozen E008 band: {band_name}") from exc
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
    validate_frozen_metadata()
    try:
        target = BANDS[band_name]
    except KeyError as exc:
        raise ValueError(f"unknown frozen E008 band: {band_name}") from exc

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
        if interval != target:
            raise ValueError("high-value interval must equal the complete authorized target band")
        for name, excluded in EXCLUDED_RANGES.items():
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
        raise ValueError("canonical E008 plan must generate the complete authorized target band")


def _segmented_target_primes(start: int, stop: int, base_primes: Sequence[int]) -> list[int]:
    flags = bytearray(b"\x01") * (stop - start)
    if start == 0:
        flags[:2] = b"\x00\x00"
    elif start == 1:
        flags[0] = 0
    for prime in base_primes:
        first = max(prime * prime, ((start + prime - 1) // prime) * prime)
        if first >= stop:
            continue
        count = ((stop - 1 - first) // prime) + 1
        flags[first - start : stop - start : prime] = b"\x00" * count
    return [start + offset for offset, flag in enumerate(flags) if flag]


def execute_generation_plan(
    plan: list[dict[str, Any]], *, band_name: str
) -> tuple[list[int], list[int]]:
    validate_generation_plan(plan, band_name=band_name)
    base_request = next(row for row in plan if row["purpose"] == "base_sieve_support")
    target_request = next(row for row in plan if row["purpose"] == "segmented_target")
    base_primes = sieve(int(base_request["stop"]) - 1)
    target_primes = _segmented_target_primes(
        int(target_request["start"]), int(target_request["stop"]), base_primes
    )
    return base_primes, target_primes


def is_q_admissible(value: int) -> bool:
    return gcd(value, Q) == 1


def partition_admissible_anchors(
    anchors: Iterable[int], prime_values: Iterable[int]
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    prime_set = frozenset(prime_values)
    prime_anchors: list[int] = []
    composite_anchors: list[int] = []
    for anchor in anchors:
        if not is_q_admissible(anchor):
            raise ValueError("anchor domain must contain only Q-admissible integers")
        if anchor in prime_set:
            prime_anchors.append(anchor)
        else:
            composite_anchors.append(anchor)
    return tuple(prime_anchors), tuple(composite_anchors)


def binary_digits_26(value: int) -> tuple[int, ...]:
    if not (SHELL[0] <= value < SHELL[1]):
        raise ValueError("E008 binary decomposition requires the frozen 26-bit shell")
    return tuple((value >> j) & 1 for j in range(25, -1, -1))


def reconstruct_binary(digits: Sequence[int]) -> int:
    if len(digits) != 26 or any(bit not in {0, 1} for bit in digits):
        raise ValueError("binary reconstruction requires exactly 26 binary digits")
    value = 0
    for bit in digits:
        value = (value << 1) | int(bit)
    return value


def binary_core(value: int) -> tuple[int, ...]:
    binary_digits_26(value)
    return tuple((value >> j) & 1 for j in range(J, 0, -1))


def _longest_run(word: Sequence[int], bit: int) -> int:
    best = 0
    current = 0
    for value in word:
        if value == bit:
            current += 1
            best = max(best, current)
        else:
            current = 0
    return best


def b1_signature(core: Sequence[int]) -> int:
    return sum(int(bit) for bit in core)


def b2_signature(core: Sequence[int]) -> int:
    return sum(int(left != right) for left, right in zip(core, core[1:], strict=False))


def b3_signature(core: Sequence[int]) -> tuple[int, int]:
    return (_longest_run(core, 0), _longest_run(core, 1))


def b4_signature(core: Sequence[int]) -> tuple[int, ...]:
    if not core:
        return ()
    runs: list[int] = []
    current = 1
    for left, right in zip(core, core[1:], strict=False):
        if left == right:
            current += 1
        else:
            runs.append(current)
            current = 1
    runs.append(current)
    return tuple(sorted(runs, reverse=True))


def signatures(core: Sequence[int]) -> dict[str, Signature]:
    if len(core) != J or any(bit not in {0, 1} for bit in core):
        raise ValueError("E008 signatures require exactly the frozen 19-bit binary core")
    return {
        "B1": b1_signature(core),
        "B2": b2_signature(core),
        "B3": b3_signature(core),
        "B4": b4_signature(core),
    }


def _signature_sort_key(family: str, signature: Signature) -> Any:
    if family in {"B1", "B2"}:
        return int(signature)  # type: ignore[arg-type]
    if family in {"B3", "B4"}:
        return tuple(signature)  # type: ignore[arg-type]
    raise ValueError(f"unknown frozen family {family}")


def _signature_json(family: str, signature: Signature) -> Any:
    if family in {"B1", "B2"}:
        return int(signature)  # type: ignore[arg-type]
    return list(signature)  # type: ignore[arg-type]


def frequency_table(family: str, counter: Mapping[Signature, int]) -> list[dict[str, Any]]:
    return [
        {"signature": _signature_json(family, signature), "count": int(counter[signature])}
        for signature in sorted(counter, key=lambda item: _signature_sort_key(family, item))
    ]


def mode_summary(family: str, counter: Mapping[Signature, int]) -> dict[str, Any]:
    if not counter:
        return {
            "prime_mode_count": 0,
            "prime_maximizing_signatures": [],
            "runner_up_count": None,
            "strict_unique_prime_mode": False,
        }
    ranked = sorted(
        counter,
        key=lambda signature: (-int(counter[signature]), _signature_sort_key(family, signature)),
    )
    max_count = int(counter[ranked[0]])
    maximizing = [signature for signature in ranked if int(counter[signature]) == max_count]
    return {
        "prime_mode_count": max_count,
        "prime_maximizing_signatures": [_signature_json(family, sig) for sig in maximizing],
        "runner_up_count": int(counter[ranked[1]]) if len(ranked) >= 2 else None,
        "strict_unique_prime_mode": len(maximizing) == 1,
    }


def enrichment_numerator(
    *, n_prime: int, n_composite: int, N_prime: int, N_composite: int
) -> int:
    return n_prime * N_composite - n_composite * N_prime


def _family_row(
    *,
    family: str,
    prime_counter: Mapping[Signature, int],
    composite_counter: Mapping[Signature, int],
    N_prime: int,
    N_composite: int,
) -> tuple[dict[str, Any], Signature | None]:
    mode = mode_summary(family, prime_counter)
    strict_unique = bool(mode["strict_unique_prime_mode"])
    unique_signature: Signature | None = None
    unique_composite_count: int | None = None
    unique_enrichment: int | None = None
    if strict_unique:
        max_count = int(mode["prime_mode_count"])
        unique_signature = next(
            signature for signature, count in prime_counter.items() if int(count) == max_count
        )
        unique_composite_count = int(composite_counter.get(unique_signature, 0))
        unique_enrichment = enrichment_numerator(
            n_prime=max_count,
            n_composite=unique_composite_count,
            N_prime=N_prime,
            N_composite=N_composite,
        )
    population_passed = N_prime >= POPULATION_FLOOR and N_composite >= POPULATION_FLOOR
    occurrence_passed = strict_unique and int(mode["prime_mode_count"]) >= OCCURRENCE_FLOOR
    enrichment_passed = strict_unique and unique_enrichment is not None and unique_enrichment > 0
    row = {
        "family": family,
        "prime_frequency_table": frequency_table(family, prime_counter),
        "composite_frequency_table": frequency_table(family, composite_counter),
        **mode,
        "unique_mode_composite_count": unique_composite_count,
        "unique_mode_enrichment_numerator": unique_enrichment,
        "population_floor_passed": population_passed,
        "occurrence_floor_passed": occurrence_passed,
        "enrichment_passed": enrichment_passed,
        "mechanically_eligible": False,
    }
    return row, unique_signature


def _apply_duplicate_suppression(
    rows: Sequence[dict[str, Any]], mode_anchor_sets: Mapping[str, frozenset[int]]
) -> list[dict[str, Any]]:
    retained_sets: list[frozenset[int]] = []
    promotions: list[dict[str, Any]] = []
    for row in rows:
        family = str(row["family"])
        pre_duplicate = bool(
            row["population_floor_passed"]
            and row["strict_unique_prime_mode"]
            and row["occurrence_floor_passed"]
            and row["enrichment_passed"]
        )
        target_set = mode_anchor_sets.get(family, frozenset())
        duplicate = pre_duplicate and any(target_set == previous for previous in retained_sets)
        eligible = pre_duplicate and not duplicate
        row["mechanically_eligible"] = eligible
        if eligible:
            retained_sets.append(target_set)
            promotions.append(
                {
                    "family": family,
                    "target_signature": row["prime_maximizing_signatures"][0],
                    "prime_count": int(row["prime_mode_count"]),
                    "composite_count": int(row["unique_mode_composite_count"]),
                    "enrichment_numerator": int(row["unique_mode_enrichment_numerator"]),
                }
            )
    return promotions[:PROMOTION_CAP]


def _parameters() -> dict[str, Any]:
    return {
        "Q": Q,
        "width": WIDTH,
        "J": J,
        "binary_shell": list(SHELL),
        "binary_core": "(b_19,b_18,...,b_1)",
        "family_definitions": [
            {"family": family, "definition": FAMILY_DEFINITIONS[family]}
            for family in FAMILY_ORDER
        ],
        "population_floor": POPULATION_FLOOR,
        "occurrence_floor": OCCURRENCE_FLOOR,
        "promotion_cap": PROMOTION_CAP,
    }


def summarise_band(
    *,
    band_name: str,
    code_commit: str,
    plan: list[dict[str, Any]],
    target_primes: Sequence[int],
) -> dict[str, Any]:
    validate_generation_plan(plan, band_name=band_name)
    start, stop = BANDS[band_name]
    if any(prime < start or prime >= stop for prime in target_primes):
        raise ValueError("target prime input contains value outside the selected band")

    prime_set = frozenset(target_primes)
    prime_counters: dict[str, Counter[Signature]] = {
        family: Counter() for family in FAMILY_ORDER
    }
    composite_counters: dict[str, Counter[Signature]] = {
        family: Counter() for family in FAMILY_ORDER
    }
    mode_anchor_members: dict[str, dict[Signature, set[int]]] = {
        family: {} for family in FAMILY_ORDER
    }

    admissible_count = 0
    N_prime = 0
    N_composite = 0
    partition_failures = 0
    reconstruction_failures = 0
    core_length_failures = 0
    parity_failures = 0
    first_prime: int | None = None
    last_prime: int | None = None

    for anchor in range(start, stop):
        if not is_q_admissible(anchor):
            continue
        admissible_count += 1
        is_prime = anchor in prime_set
        if is_prime:
            N_prime += 1
            if first_prime is None:
                first_prime = anchor
            last_prime = anchor
            population_counters = prime_counters
        else:
            N_composite += 1
            population_counters = composite_counters

        if (is_prime and anchor not in prime_set) or ((not is_prime) and anchor in prime_set):
            partition_failures += 1

        digits = binary_digits_26(anchor)
        if reconstruct_binary(digits) != anchor:
            reconstruction_failures += 1
        if digits[-1] != 1:
            parity_failures += 1
        core = binary_core(anchor)
        if len(core) != J:
            core_length_failures += 1
        sigs = signatures(core)
        for family in FAMILY_ORDER:
            signature = sigs[family]
            population_counters[family][signature] += 1
            if is_prime:
                mode_anchor_members[family].setdefault(signature, set()).add(anchor)

    if N_prime != len(prime_set):
        partition_failures += abs(N_prime - len(prime_set))

    validation = {
        "admissible_partition_failure_count": partition_failures,
        "binary_reconstruction_failure_count": reconstruction_failures,
        "core_length_failure_count": core_length_failures,
        "parity_control_failure_count": parity_failures,
    }
    if any(validation.values()):
        raise ValueError("validation aggregate failure detected during E008 evaluation")
    if admissible_count != N_prime + N_composite:
        raise ValueError("admissible prime/composite partition does not exhaust the domain")

    family_rows: list[dict[str, Any]] = []
    mode_anchor_sets: dict[str, frozenset[int]] = {}
    for family in FAMILY_ORDER:
        row, unique_signature = _family_row(
            family=family,
            prime_counter=prime_counters[family],
            composite_counter=composite_counters[family],
            N_prime=N_prime,
            N_composite=N_composite,
        )
        if unique_signature is not None:
            mode_anchor_sets[family] = frozenset(
                mode_anchor_members[family].get(unique_signature, set())
            )
        family_rows.append(row)

    promotions = _apply_duplicate_suppression(family_rows, mode_anchor_sets)
    payload = {
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
        "parameters": _parameters(),
        "generation_plan": plan,
        "anchor_summary": {
            "admissible_count": admissible_count,
            "prime_count": N_prime,
            "composite_count": N_composite,
            "first_prime": first_prime,
            "last_prime": last_prime,
        },
        "validation": validation,
        "families": family_rows,
        "promotions": promotions,
    }
    if frozenset(payload) != PAYLOAD_KEYS:
        raise ValueError("E008 payload escaped the frozen descriptive allowlist")
    if frozenset(payload["anchor_summary"]) != ANCHOR_SUMMARY_KEYS:
        raise ValueError("E008 anchor summary escaped the frozen descriptive allowlist")
    if frozenset(payload["validation"]) != VALIDATION_KEYS:
        raise ValueError("E008 validation summary escaped the frozen descriptive allowlist")
    if any(frozenset(row) != FAMILY_ROW_KEYS for row in family_rows):
        raise ValueError("E008 family summary escaped the frozen descriptive allowlist")
    return payload


def build_payload(*, band_name: str, code_commit: str) -> dict[str, Any]:
    plan = generation_plan(band_name)
    validate_generation_plan(plan, band_name=band_name)
    _, target_primes = execute_generation_plan(plan, band_name=band_name)
    return summarise_band(
        band_name=band_name,
        code_commit=code_commit,
        plan=plan,
        target_primes=target_primes,
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
