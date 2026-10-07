#!/usr/bin/env python3
"""E009: frozen unit-action cover-shape discovery evaluator."""
from __future__ import annotations

import argparse
import json
from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from itertools import combinations
from math import gcd, isqrt, lcm
from pathlib import Path
from typing import Any, TypeAlias

from primes_lab.core import sieve

EXPERIMENT_ID = "E009"
WIDTH = 1_000_000
Q = 210
BASIS = (2, 3, 5, 7)
LOW_SUPPORT_STOP = 100_000
POPULATION_FLOOR = 1_000
OCCURRENCE_FLOOR = 32
PROMOTION_CAP = 4
FAMILY_ORDER = ("C1", "C2", "C3", "C4")

BANDS: dict[str, tuple[int, int]] = {
    "D9": (54_000_000, 55_000_000),
    "H9": (56_000_000, 57_000_000),
    "A9": (108_000_000, 109_000_000),
}
FROZEN_PARTITION: tuple[tuple[str, str, tuple[int, int]], ...] = (
    ("G9-pre", "guard", (53_000_000, 54_000_000)),
    ("D9", "discovery", BANDS["D9"]),
    ("G9-mid", "guard", (55_000_000, 56_000_000)),
    ("H9", "holdout", BANDS["H9"]),
    ("A9", "adversarial", BANDS["A9"]),
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
    "D8": (50_000_000, 51_000_000),
    "G8-mid": (51_000_000, 52_000_000),
    "H8": (52_000_000, 53_000_000),
    "G9-pre": (53_000_000, 54_000_000),
    "D9": BANDS["D9"],
    "G9-mid": (55_000_000, 56_000_000),
    "H9": BANDS["H9"],
    "A8": (66_000_000, 67_000_000),
    "A3": (70_000_000, 71_000_000),
    "A4": (78_000_000, 79_000_000),
    "A6": (84_000_000, 85_000_000),
    "A7": (92_000_000, 93_000_000),
    "A9": BANDS["A9"],
}
# The complete generation validator also rejects every other non-target high interval
# by exact-target equality, so quarantined E005 segments (all >=128M) cannot pass.

SUBSETS: tuple[tuple[int, ...], ...] = tuple(
    subset
    for size in range(1, len(BASIS) + 1)
    for subset in combinations(BASIS, size)
)
_SUBSET_MASKS: tuple[int, ...] = tuple(
    sum(1 << BASIS.index(base) for base in subset) for subset in SUBSETS
)
_PROPER_SUBSET_INDICES: tuple[tuple[int, ...], ...] = tuple(
    tuple(
        j
        for j, other_mask in enumerate(_SUBSET_MASKS)
        if other_mask != mask and (other_mask & mask) == other_mask
    )
    for mask in _SUBSET_MASKS
)
_SUPERSET_INDICES: tuple[tuple[int, ...], ...] = tuple(
    tuple(
        j
        for j, other_mask in enumerate(_SUBSET_MASKS)
        if other_mask != mask and (other_mask & mask) == mask
    )
    for mask in _SUBSET_MASKS
)

FAMILY_DEFINITIONS = {
    "C1": "minimum minimal-cover size, or 0 when the minimal-cover antichain is empty",
    "C2": "minimal-cover size profile (m1,m2,m3,m4)",
    "C3": "all-cover size profile (c1,c2,c3,c4)",
    "C4": "exact canonical minimal-cover antichain",
}

C1Signature: TypeAlias = int
ProfileSignature: TypeAlias = tuple[int, int, int, int]
AntichainSignature: TypeAlias = tuple[tuple[int, ...], ...]
Signature: TypeAlias = C1Signature | ProfileSignature | AntichainSignature

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
        "factorization_reconstruction_failure_count",
        "nonprime_factor_or_canonical_order_failure_count",
        "lambda_construction_failure_count",
        "basis_unit_gcd_failure_count",
        "order_divides_lambda_failure_count",
        "order_witness_or_minimality_failure_count",
        "cover_monotonicity_failure_count",
        "minimal_antichain_failure_count",
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
    if WIDTH != 1_000_000:
        raise ValueError("frozen E009 width changed")
    if Q != 2 * 3 * 5 * 7 or Q != 210:
        raise ValueError("frozen E009 Q changed")
    if BASIS != (2, 3, 5, 7):
        raise ValueError("frozen E009 ordered basis changed")
    if len(SUBSETS) != 15:
        raise ValueError("E009 must have exactly 15 nonempty basis subsets")
    expected_subsets = tuple(
        subset
        for size in range(1, 5)
        for subset in combinations(BASIS, size)
    )
    if SUBSETS != expected_subsets:
        raise ValueError("canonical E009 subset ordering changed")
    expected_partition = {
        "G9-pre": (53_000_000, 54_000_000),
        "D9": (54_000_000, 55_000_000),
        "G9-mid": (55_000_000, 56_000_000),
        "H9": (56_000_000, 57_000_000),
        "A9": (108_000_000, 109_000_000),
    }
    rows = {name: interval for name, _, interval in FROZEN_PARTITION}
    if rows != expected_partition:
        raise ValueError("frozen E009 partition changed")
    if any(interval[1] - interval[0] != WIDTH for interval in rows.values()):
        raise ValueError("every E009 partition band must retain width 1,000,000")
    intervals = list(rows.values())
    for i, left in enumerate(intervals):
        for right in intervals[i + 1 :]:
            if _intersects(left, right):
                raise ValueError("frozen E009 partition intervals overlap")


def generation_plan(band_name: str) -> list[dict[str, Any]]:
    try:
        start, stop = BANDS[band_name]
    except KeyError as exc:
        raise ValueError(f"unknown frozen E009 band: {band_name}") from exc
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
        raise ValueError(f"unknown frozen E009 band: {band_name}") from exc

    if len(plan) != 2:
        raise ValueError("generation plan must contain exactly base support and one target")
    base_rows = [row for row in plan if row.get("purpose") == "base_sieve_support"]
    target_rows = [row for row in plan if row.get("purpose") == "segmented_target"]
    if len(base_rows) != 1 or len(target_rows) != 1:
        raise ValueError("generation plan must contain exactly one base request and one target request")

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
                raise ValueError("low support must be an exact whole-prefix base sieve from zero")
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
        raise ValueError("base support must be exactly [0, floor(sqrt(U-1))+1)")
    if required_stop > LOW_SUPPORT_STOP:
        raise ValueError("required base support exceeds frozen safe low-support ceiling")
    if (int(target_row["start"]), int(target_row["stop"])) != target:
        raise ValueError("canonical E009 plan must generate the complete authorized target band")


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


def factor_exact(value: int, base_primes: Sequence[int]) -> tuple[tuple[int, int], ...]:
    if value < 1:
        raise ValueError("exact factorization input must be positive")
    remainder = value
    factors: list[tuple[int, int]] = []
    for prime in base_primes:
        if prime * prime > remainder:
            break
        if remainder % prime:
            continue
        exponent = 0
        while remainder % prime == 0:
            remainder //= prime
            exponent += 1
        factors.append((int(prime), exponent))
    if remainder > 1:
        factors.append((int(remainder), 1))
    return tuple(factors)


def reconstruct_factors(factors: Sequence[tuple[int, int]]) -> int:
    result = 1
    for prime, exponent in factors:
        result *= int(prime) ** int(exponent)
    return result


def _is_prime_with_support(value: int, base_primes: Sequence[int]) -> bool:
    if value < 2:
        return False
    for prime in base_primes:
        if prime * prime > value:
            break
        if value % prime == 0:
            return value == prime
    return True


def factorization_is_canonical(
    value: int, factors: Sequence[tuple[int, int]], base_primes: Sequence[int]
) -> bool:
    if reconstruct_factors(factors) != value:
        return False
    previous = 1
    for prime, exponent in factors:
        if prime <= previous or exponent < 1:
            return False
        if not _is_prime_with_support(prime, base_primes):
            return False
        previous = prime
    return True


def lambda_terms(factors: Sequence[tuple[int, int]]) -> tuple[int, ...]:
    terms: list[int] = []
    for prime, exponent in factors:
        if prime == 2:
            raise ValueError("E009 Lambda construction is frozen for odd anchors")
        terms.append((prime ** (exponent - 1)) * (prime - 1))
    return tuple(terms)


def lcm_many(values: Iterable[int]) -> int:
    result = 1
    for value in values:
        result = lcm(result, int(value))
    return result


def unit_group_exponent(factors: Sequence[tuple[int, int]]) -> int:
    terms = lambda_terms(factors)
    if not terms:
        raise ValueError("E009 high-value anchors must have nonempty factorization")
    return lcm_many(terms)


def multiplicative_order(
    base: int,
    modulus: int,
    lambda_value: int,
    lambda_factors: Sequence[tuple[int, int]],
) -> int:
    if gcd(base, modulus) != 1:
        raise ValueError("multiplicative order requires a unit")
    if lambda_value < 1:
        raise ValueError("Lambda must be positive")
    result = lambda_value
    for prime, _ in lambda_factors:
        while result % prime == 0 and pow(base, result // prime, modulus) == 1:
            result //= prime
    return result


def order_witness_is_exact(
    base: int,
    modulus: int,
    order: int,
    lambda_value: int,
    base_primes: Sequence[int],
) -> bool:
    if order < 1 or lambda_value % order != 0 or pow(base, order, modulus) != 1:
        return False
    order_factors = factor_exact(order, base_primes)
    return all(pow(base, order // prime, modulus) != 1 for prime, _ in order_factors)


def subset_lcms(order_vector: Sequence[int]) -> tuple[int, ...]:
    if len(order_vector) != len(BASIS):
        raise ValueError("order vector must match the frozen four-base basis")
    by_base = dict(zip(BASIS, (int(value) for value in order_vector), strict=True))
    return tuple(lcm_many(by_base[base] for base in subset) for subset in SUBSETS)


def cover_flags(order_vector: Sequence[int], lambda_value: int) -> tuple[bool, ...]:
    return tuple(value == lambda_value for value in subset_lcms(order_vector))


def cover_monotonicity_holds(flags: Sequence[bool]) -> bool:
    if len(flags) != len(SUBSETS):
        return False
    for i, is_cover in enumerate(flags):
        if not is_cover:
            continue
        if any(not flags[j] for j in _SUPERSET_INDICES[i]):
            return False
    return True


def minimal_cover_antichain_from_flags(
    flags: Sequence[bool],
) -> tuple[tuple[int, ...], ...]:
    if len(flags) != len(SUBSETS):
        raise ValueError("cover flag vector must have length 15")
    minimal: list[tuple[int, ...]] = []
    for i, is_cover in enumerate(flags):
        if not is_cover:
            continue
        if any(flags[j] for j in _PROPER_SUBSET_INDICES[i]):
            continue
        minimal.append(SUBSETS[i])
    return tuple(minimal)


def minimal_antichain_is_exact(
    flags: Sequence[bool], minimal: Sequence[tuple[int, ...]]
) -> bool:
    expected = minimal_cover_antichain_from_flags(flags)
    if tuple(minimal) != expected:
        return False
    masks = [_SUBSET_MASKS[SUBSETS.index(tuple(subset))] for subset in minimal]
    for i, left in enumerate(masks):
        for right in masks[i + 1 :]:
            if (left & right) in {left, right}:
                return False
    return True


def signatures_from_cover(
    flags: Sequence[bool], minimal: Sequence[tuple[int, ...]]
) -> dict[str, Signature]:
    min_counts = tuple(
        sum(1 for subset in minimal if len(subset) == size) for size in range(1, 5)
    )
    cover_counts = tuple(
        sum(1 for subset, is_cover in zip(SUBSETS, flags, strict=True) if is_cover and len(subset) == size)
        for size in range(1, 5)
    )
    kappa = min((len(subset) for subset in minimal), default=0)
    return {
        "C1": kappa,
        "C2": min_counts,
        "C3": cover_counts,
        "C4": tuple(tuple(subset) for subset in minimal),
    }


def cover_shape(
    order_vector: Sequence[int], lambda_value: int
) -> tuple[dict[str, Signature], tuple[bool, ...], tuple[tuple[int, ...], ...]]:
    flags = cover_flags(order_vector, lambda_value)
    minimal = minimal_cover_antichain_from_flags(flags)
    return signatures_from_cover(flags, minimal), flags, minimal


def _signature_sort_key(family: str, signature: Signature) -> Any:
    if family == "C1":
        return int(signature)  # type: ignore[arg-type]
    if family in {"C2", "C3"}:
        return tuple(signature)  # type: ignore[arg-type]
    if family == "C4":
        return tuple(tuple(subset) for subset in signature)  # type: ignore[arg-type]
    raise ValueError(f"unknown frozen family {family}")


def _signature_json(family: str, signature: Signature) -> Any:
    if family == "C1":
        return int(signature)  # type: ignore[arg-type]
    if family in {"C2", "C3"}:
        return list(signature)  # type: ignore[arg-type]
    if family == "C4":
        return [list(subset) for subset in signature]  # type: ignore[arg-type]
    raise ValueError(f"unknown frozen family {family}")


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


def apply_duplicate_suppression(
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
        "basis": list(BASIS),
        "width": WIDTH,
        "canonical_nonempty_subsets": [list(subset) for subset in SUBSETS],
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
    base_primes: Sequence[int],
    target_primes: Sequence[int],
) -> dict[str, Any]:
    validate_generation_plan(plan, band_name=band_name)
    start, stop = BANDS[band_name]
    if any(prime < start or prime >= stop for prime in target_primes):
        raise ValueError("target prime input contains value outside the selected band")
    if any(not is_q_admissible(prime) for prime in target_primes):
        raise ValueError("every high-band prime must belong to the Q-admissible domain")

    prime_set = frozenset(target_primes)
    prime_counters: dict[str, Counter[Signature]] = {
        family: Counter() for family in FAMILY_ORDER
    }
    composite_counters: dict[str, Counter[Signature]] = {
        family: Counter() for family in FAMILY_ORDER
    }
    prime_signature_members: dict[str, dict[Signature, set[int]]] = {
        family: {} for family in FAMILY_ORDER
    }

    validation = {key: 0 for key in VALIDATION_KEYS}
    admissible_count = 0
    N_prime = 0
    N_composite = 0
    lambda_factor_cache: dict[int, tuple[tuple[int, int], ...]] = {}

    for anchor in range(start, stop):
        if not is_q_admissible(anchor):
            continue
        admissible_count += 1
        is_prime = anchor in prime_set
        if is_prime:
            N_prime += 1
            counters = prime_counters
        else:
            N_composite += 1
            counters = composite_counters

        factors = factor_exact(anchor, base_primes)
        if reconstruct_factors(factors) != anchor:
            validation["factorization_reconstruction_failure_count"] += 1
        if not factorization_is_canonical(anchor, factors, base_primes):
            validation["nonprime_factor_or_canonical_order_failure_count"] += 1

        terms = lambda_terms(factors)
        lambda_value = unit_group_exponent(factors)
        if lambda_value != lcm_many(terms):
            validation["lambda_construction_failure_count"] += 1
        if any(gcd(base, anchor) != 1 for base in BASIS):
            validation["basis_unit_gcd_failure_count"] += 1

        lambda_factors = lambda_factor_cache.get(lambda_value)
        if lambda_factors is None:
            lambda_factors = factor_exact(lambda_value, base_primes)
            if not factorization_is_canonical(lambda_value, lambda_factors, base_primes):
                validation["nonprime_factor_or_canonical_order_failure_count"] += 1
            lambda_factor_cache[lambda_value] = lambda_factors

        orders: list[int] = []
        for base in BASIS:
            order = multiplicative_order(base, anchor, lambda_value, lambda_factors)
            orders.append(order)
            if lambda_value % order != 0:
                validation["order_divides_lambda_failure_count"] += 1
            witness_ok = (
                order >= 1
                and lambda_value % order == 0
                and pow(base, order, anchor) == 1
                and all(
                    pow(base, order // prime, anchor) != 1
                    for prime, _ in lambda_factors
                    if order % prime == 0
                )
            )
            if not witness_ok:
                validation["order_witness_or_minimality_failure_count"] += 1

        sigs, flags, minimal = cover_shape(tuple(orders), lambda_value)
        if not cover_monotonicity_holds(flags):
            validation["cover_monotonicity_failure_count"] += 1
        if not minimal_antichain_is_exact(flags, minimal):
            validation["minimal_antichain_failure_count"] += 1

        for family in FAMILY_ORDER:
            signature = sigs[family]
            counters[family][signature] += 1
            if is_prime:
                prime_signature_members[family].setdefault(signature, set()).add(anchor)

    if N_prime != len(prime_set) or N_prime + N_composite != admissible_count:
        raise ValueError("Q-admissible prime/composite partition failed")
    if any(validation.values()):
        raise ValueError("validation aggregate failure detected during E009 evaluation")

    family_rows: list[dict[str, Any]] = []
    mode_anchor_sets: dict[str, frozenset[int]] = {}
    for family in FAMILY_ORDER:
        if sum(prime_counters[family].values()) != N_prime:
            raise ValueError("prime frequency table does not exhaust prime anchors")
        if sum(composite_counters[family].values()) != N_composite:
            raise ValueError("composite frequency table does not exhaust composite anchors")
        row, unique_signature = _family_row(
            family=family,
            prime_counter=prime_counters[family],
            composite_counter=composite_counters[family],
            N_prime=N_prime,
            N_composite=N_composite,
        )
        family_rows.append(row)
        if unique_signature is not None:
            mode_anchor_sets[family] = frozenset(
                prime_signature_members[family].get(unique_signature, set())
            )

    promotions = apply_duplicate_suppression(family_rows, mode_anchor_sets)
    target_primes_sorted = sorted(target_primes)
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
            "first_prime": target_primes_sorted[0] if target_primes_sorted else None,
            "last_prime": target_primes_sorted[-1] if target_primes_sorted else None,
        },
        "validation": validation,
        "families": family_rows,
        "promotions": promotions,
    }
    if frozenset(payload) != PAYLOAD_KEYS:
        raise ValueError("E009 payload escaped the frozen descriptive allowlist")
    if frozenset(payload["anchor_summary"]) != ANCHOR_SUMMARY_KEYS:
        raise ValueError("E009 anchor summary escaped the frozen descriptive allowlist")
    if frozenset(payload["validation"]) != VALIDATION_KEYS:
        raise ValueError("E009 validation escaped the frozen descriptive allowlist")
    if any(frozenset(row) != FAMILY_ROW_KEYS for row in family_rows):
        raise ValueError("E009 family row escaped the frozen descriptive allowlist")
    return payload


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
