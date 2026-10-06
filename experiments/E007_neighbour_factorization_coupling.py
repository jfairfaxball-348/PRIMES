#!/usr/bin/env python3
"""E007: frozen neighbour-factorization coupling discovery evaluator."""
from __future__ import annotations

import argparse
import json
from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from math import gcd, isqrt
from pathlib import Path
from typing import Any, TypeAlias

from primes_lab.core import sieve

EXPERIMENT_ID = "E007"
WIDTH = 1_000_000
LOW_SUPPORT_STOP = 100_000
POPULATION_FLOOR = 1_000
OCCURRENCE_FLOOR = 32
PROMOTION_CAP = 4
FAMILY_ORDER = ("F1", "F2", "F3", "F4")

BANDS: dict[str, tuple[int, int]] = {
    "D7": (46_000_000, 47_000_000),
    "H7": (48_000_000, 49_000_000),
    "A7": (92_000_000, 93_000_000),
}
FROZEN_PARTITION: tuple[tuple[str, str, tuple[int, int]], ...] = (
    ("G7-pre", "guard", (45_000_000, 46_000_000)),
    ("D7", "discovery", BANDS["D7"]),
    ("G7-mid", "guard", (47_000_000, 48_000_000)),
    ("H7", "holdout", BANDS["H7"]),
    ("A7", "adversarial", BANDS["A7"]),
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
    "G7-mid": (47_000_000, 48_000_000),
    "H7": BANDS["H7"],
    "A3": (70_000_000, 71_000_000),
    "A4": (78_000_000, 79_000_000),
    "A6": (84_000_000, 85_000_000),
    "A7": BANDS["A7"],
}

Shape: TypeAlias = tuple[int, ...]
F1Signature: TypeAlias = tuple[Shape, Shape]
PairSignature: TypeAlias = tuple[int, int]
Signature: TypeAlias = F1Signature | PairSignature | int


def _intersects(left: tuple[int, int], right: tuple[int, int]) -> bool:
    return max(left[0], right[0]) < min(left[1], right[1])


def generation_plan(band_name: str) -> list[dict[str, Any]]:
    try:
        start, stop = BANDS[band_name]
    except KeyError as exc:
        raise ValueError(f"unknown frozen E007 band: {band_name}") from exc
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
        raise ValueError(f"unknown frozen E007 band: {band_name}") from exc
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
        raise ValueError("canonical E007 plan must generate the complete authorized target band")


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


def common_odd_anchors(*, start: int, stop: int) -> tuple[int, ...]:
    if stop <= start + 2:
        return ()
    first = start + 1 if start % 2 == 0 else start + 2
    return tuple(range(first, stop - 1, 2))


def partition_anchors(
    anchors: Iterable[int], prime_values: Iterable[int]
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    prime_set = frozenset(prime_values)
    prime_anchors: list[int] = []
    composite_anchors: list[int] = []
    for anchor in anchors:
        if anchor <= 1 or anchor % 2 == 0:
            raise ValueError("anchor domain must contain odd integers greater than one")
        if anchor in prime_set:
            prime_anchors.append(anchor)
        else:
            composite_anchors.append(anchor)
    return tuple(prime_anchors), tuple(composite_anchors)


def strip_power_of_two(value: int) -> tuple[int, int]:
    if value <= 0:
        raise ValueError("v2 is defined here only for positive integers")
    exponent = 0
    while value % 2 == 0:
        value //= 2
        exponent += 1
    return exponent, value


def thin_thick_cores(anchor: int) -> dict[str, Any]:
    if anchor <= 1 or anchor % 2 == 0:
        raise ValueError("anchor must be odd and greater than one")
    minus_v2, minus_core = strip_power_of_two(anchor - 1)
    plus_v2, plus_core = strip_power_of_two(anchor + 1)
    if (minus_v2 == 1) == (plus_v2 == 1):
        raise ValueError("exactly one neighbour must be the thin v2=1 side")
    if minus_v2 == 1:
        orientation = "minus"
        thin_v2, thin_core = minus_v2, minus_core
        thick_v2, thick_core = plus_v2, plus_core
    else:
        orientation = "plus"
        thin_v2, thin_core = plus_v2, plus_core
        thick_v2, thick_core = minus_v2, minus_core
    if thin_v2 != 1 or thick_v2 < 2:
        raise ValueError("invalid thin/thick classification")
    if gcd(thin_core, thick_core) != 1:
        raise ValueError("odd neighbour cores must be coprime")
    return {
        "thin_orientation": orientation,
        "thin_v2": thin_v2,
        "thick_v2": thick_v2,
        "thin_core": thin_core,
        "thick_core": thick_core,
    }


def factor_odd_exact(
    value: int, base_primes: Sequence[int]
) -> tuple[tuple[tuple[int, int], ...], int]:
    if value < 1 or value % 2 == 0:
        raise ValueError("odd factorization input must be a positive odd integer")
    original = value
    factors: list[tuple[int, int]] = []
    for prime in base_primes:
        if prime == 2:
            continue
        if prime * prime > value:
            break
        if value % prime != 0:
            continue
        exponent = 0
        while value % prime == 0:
            value //= prime
            exponent += 1
        factors.append((prime, exponent))
    if value > 1:
        factors.append((value, 1))
    reconstructed = 1
    for prime, exponent in factors:
        reconstructed *= prime**exponent
    if reconstructed != original:
        raise ValueError("odd factorization failed exact reconstruction")
    return tuple(factors), reconstructed


def factor_profile(value: int, base_primes: Sequence[int]) -> dict[str, Any]:
    factors, reconstructed = factor_odd_exact(value, base_primes)
    exponents = tuple(exponent for _, exponent in factors)
    shape = tuple(sorted(exponents, reverse=True))
    return {
        "omega": len(factors),
        "Omega": sum(exponents),
        "shape": shape,
        "Pplus": factors[-1][0] if factors else 1,
        "reconstructed": reconstructed,
    }


def signatures(thin: Mapping[str, Any], thick: Mapping[str, Any]) -> dict[str, Signature]:
    p_thin = int(thin["Pplus"])
    p_thick = int(thick["Pplus"])
    sign = (p_thin > p_thick) - (p_thin < p_thick)
    return {
        "F1": (tuple(thin["shape"]), tuple(thick["shape"])),
        "F2": (int(thin["omega"]), int(thick["omega"])),
        "F3": (int(thin["Omega"]), int(thick["Omega"])),
        "F4": sign,
    }


def _signature_sort_key(family: str, signature: Signature) -> Any:
    if family == "F1":
        thin_shape, thick_shape = signature  # type: ignore[misc]
        return (tuple(thin_shape), tuple(thick_shape))
    if family in {"F2", "F3"}:
        return tuple(signature)  # type: ignore[arg-type]
    if family == "F4":
        return int(signature)  # type: ignore[arg-type]
    raise ValueError(f"unknown frozen family {family}")


def _signature_json(family: str, signature: Signature) -> Any:
    if family == "F1":
        thin_shape, thick_shape = signature  # type: ignore[misc]
        return [list(thin_shape), list(thick_shape)]
    if family in {"F2", "F3"}:
        return list(signature)  # type: ignore[arg-type]
    return int(signature)  # type: ignore[arg-type]


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


def _profile_even_values(
    start: int, stop: int, base_primes: Sequence[int]
) -> tuple[list[int], list[dict[str, Any]]]:
    v2_values: list[int] = []
    profiles: list[dict[str, Any]] = []
    cache: dict[int, dict[str, Any]] = {}
    for value in range(start, stop, 2):
        exponent, core = strip_power_of_two(value)
        v2_values.append(exponent)
        profile = cache.get(core)
        if profile is None:
            profile = factor_profile(core, base_primes)
            cache[core] = profile
        profiles.append(profile)
    return v2_values, profiles


def _validate_family_rows(
    rows: list[dict[str, Any]], mode_anchor_sets: Mapping[str, frozenset[int]]
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
                    "prime_count": row["prime_mode_count"],
                    "composite_count": row["unique_mode_composite_count"],
                    "enrichment_numerator": row["unique_mode_enrichment_numerator"],
                }
            )
    return promotions[:PROMOTION_CAP]


def summarise_band(
    *,
    band_name: str,
    code_commit: str,
    plan: list[dict[str, Any]],
    base_primes: Sequence[int],
    target_primes: Sequence[int],
) -> dict[str, Any]:
    start, stop = BANDS[band_name]
    if any(prime < start or prime >= stop for prime in target_primes):
        raise ValueError("target prime input contains value outside the selected band")

    anchors = common_odd_anchors(start=start, stop=stop)
    prime_set = frozenset(target_primes)
    prime_anchor_set = frozenset(anchor for anchor in anchors if anchor in prime_set)
    N_prime = len(prime_anchor_set)
    N_composite = len(anchors) - N_prime

    v2_values, even_profiles = _profile_even_values(start, stop, base_primes)
    prime_counters: dict[str, Counter[Signature]] = {
        family: Counter() for family in FAMILY_ORDER
    }
    composite_counters: dict[str, Counter[Signature]] = {
        family: Counter() for family in FAMILY_ORDER
    }
    mode_anchor_members: dict[str, dict[Signature, set[int]]] = {
        family: {} for family in FAMILY_ORDER
    }
    orientation = {
        "prime": Counter({"minus": 0, "plus": 0}),
        "composite": Counter({"minus": 0, "plus": 0}),
    }
    thick_v2 = {"prime": Counter(), "composite": Counter()}
    reconstruction_failures = 0
    classification_failures = 0
    gcd_failures = 0

    for i, anchor in enumerate(anchors):
        left_v2, right_v2 = v2_values[i], v2_values[i + 1]
        left_profile, right_profile = even_profiles[i], even_profiles[i + 1]
        if (left_v2 == 1) == (right_v2 == 1):
            classification_failures += 1
            continue
        if left_v2 == 1:
            side = "minus"
            thin_profile, thick_profile = left_profile, right_profile
            thick_exp = right_v2
            thin_core = int(left_profile["reconstructed"])
            thick_core = int(right_profile["reconstructed"])
        else:
            side = "plus"
            thin_profile, thick_profile = right_profile, left_profile
            thick_exp = left_v2
            thin_core = int(right_profile["reconstructed"])
            thick_core = int(left_profile["reconstructed"])
        if thin_profile["reconstructed"] < 1 or thick_profile["reconstructed"] < 1:
            reconstruction_failures += 1
            continue
        if gcd(thin_core, thick_core) != 1:
            gcd_failures += 1
            continue

        population = "prime" if anchor in prime_anchor_set else "composite"
        orientation[population][side] += 1
        thick_v2[population][thick_exp] += 1
        sigs = signatures(thin_profile, thick_profile)
        for family in FAMILY_ORDER:
            sig = sigs[family]
            if population == "prime":
                prime_counters[family][sig] += 1
                mode_anchor_members[family].setdefault(sig, set()).add(anchor)
            else:
                composite_counters[family][sig] += 1

    family_rows: list[dict[str, Any]] = []
    mode_anchor_sets: dict[str, frozenset[int]] = {}
    population_floor_passed = N_prime >= POPULATION_FLOOR and N_composite >= POPULATION_FLOOR
    for family in FAMILY_ORDER:
        prime_counter = prime_counters[family]
        composite_counter = composite_counters[family]
        mode = mode_summary(family, prime_counter)
        strict_unique = bool(mode["strict_unique_prime_mode"])
        unique_composite_count: int | None = None
        unique_enrichment: int | None = None
        if strict_unique:
            max_count = int(mode["prime_mode_count"])
            candidates = [sig for sig, count in prime_counter.items() if int(count) == max_count]
            unique_signature = candidates[0]
            unique_composite_count = int(composite_counter.get(unique_signature, 0))
            unique_enrichment = enrichment_numerator(
                n_prime=max_count,
                n_composite=unique_composite_count,
                N_prime=N_prime,
                N_composite=N_composite,
            )
            mode_anchor_sets[family] = frozenset(mode_anchor_members[family][unique_signature])
        row = {
            "family": family,
            "prime_frequency_table": frequency_table(family, prime_counter),
            "composite_frequency_table": frequency_table(family, composite_counter),
            **mode,
            "unique_mode_composite_count": unique_composite_count,
            "unique_mode_enrichment_numerator": unique_enrichment,
            "population_floor_passed": population_floor_passed,
            "occurrence_floor_passed": strict_unique
            and int(mode["prime_mode_count"]) >= OCCURRENCE_FLOOR,
            "enrichment_passed": strict_unique
            and unique_enrichment is not None
            and unique_enrichment > 0,
            "mechanically_eligible": False,
        }
        family_rows.append(row)

    promotions = _validate_family_rows(family_rows, mode_anchor_sets)
    if reconstruction_failures or classification_failures or gcd_failures:
        raise ValueError("validation aggregate failure detected during E007 evaluation")

    prime_anchors_sorted = sorted(prime_anchor_set)
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
        "parameters": {
            "width": WIDTH,
            "common_anchor_domain": [start + 1, stop - 1],
            "anchor_population_floor": POPULATION_FLOOR,
            "target_occurrence_floor": OCCURRENCE_FLOOR,
            "family_order": list(FAMILY_ORDER),
            "promotion_cap": PROMOTION_CAP,
            "thin_v2": 1,
            "thick_v2_minimum": 2,
        },
        "generation_plan": plan,
        "anchor_summary": {
            "common_odd_anchor_count": len(anchors),
            "prime_anchor_count": N_prime,
            "composite_anchor_count": N_composite,
            "first_prime_anchor": prime_anchors_sorted[0] if prime_anchors_sorted else None,
            "last_prime_anchor": prime_anchors_sorted[-1] if prime_anchors_sorted else None,
        },
        "controls": {
            "prime": {
                "thin_orientation": [
                    {"orientation": key, "count": int(orientation["prime"][key])}
                    for key in ("minus", "plus")
                ],
                "thick_v2_frequency": [
                    {"valuation": key, "count": int(thick_v2["prime"][key])}
                    for key in sorted(thick_v2["prime"])
                ],
            },
            "composite": {
                "thin_orientation": [
                    {"orientation": key, "count": int(orientation["composite"][key])}
                    for key in ("minus", "plus")
                ],
                "thick_v2_frequency": [
                    {"valuation": key, "count": int(thick_v2["composite"][key])}
                    for key in sorted(thick_v2["composite"])
                ],
            },
        },
        "validation_aggregates": {
            "factorization_reconstruction_failure_count": reconstruction_failures,
            "thin_thick_classification_failure_count": classification_failures,
            "odd_core_gcd_failure_count": gcd_failures,
        },
        "families": family_rows,
        "promotion_records": promotions,
    }


def build_payload(*, band_name: str, code_commit: str) -> dict[str, Any]:
    plan = generation_plan(band_name)
    validate_generation_plan(plan, band_name=band_name)
    base_primes, target_primes = execute_generation_plan(plan, band_name=band_name)
    return summarise_band(
        band_name=band_name,
        code_commit=code_commit,
        plan=plan,
        base_primes=base_primes,
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
