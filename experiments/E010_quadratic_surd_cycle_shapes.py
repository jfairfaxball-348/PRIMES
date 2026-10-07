#!/usr/bin/env python3
"""E010: frozen quadratic-surd recurrence cycle-shape discovery evaluator."""
from __future__ import annotations

import argparse
import json
from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from math import gcd, isqrt
from multiprocessing import get_context
from pathlib import Path
from typing import Any

from primes_lab.core import sieve

from experiments.E010_quadratic_surd_cycle_shapes_runtime import (
    FAMILY_ORDER,
    OCCURRENCE_FLOOR,
    POPULATION_FLOOR,
    PROMOTION_CAP,
    Signature,
    apply_duplicate_suppression,
    cycle_signatures,
    family_row,
)

EXPERIMENT_ID = "E010"
WIDTH = 1_000_000
Q = 210
LOW_SUPPORT_STOP = 100_000
SUMMARY_WORKERS = 5
SUMMARY_BLOCK_SIZE = 10_000
H10_OBSERVATION_ID = "OBS-014"
H10_FAMILY = "L2"
H10_TARGET_SIGNATURE = 1487
BANDS = {
    "D10": (58_000_000, 59_000_000),
    "H10": (60_000_000, 61_000_000),
    "A10": (116_000_000, 117_000_000),
}
FROZEN_PARTITION = (
    ("G10-pre", "guard", (57_000_000, 58_000_000)),
    ("D10", "discovery", BANDS["D10"]),
    ("G10-mid", "guard", (59_000_000, 60_000_000)),
    ("H10", "holdout", BANDS["H10"]),
    ("A10", "adversarial", BANDS["A10"]),
)
HISTORICAL_RANGES = {
    "D0": (0, 1_000_000), "H0": (1_000_000, 2_000_000),
    "S1": (2_000_000, 3_000_000), "S2": (4_000_000, 5_000_000),
    "S3": (8_000_000, 9_000_000), "A0-retired": (10_000_000, 11_000_000),
    "S4": (16_000_000, 17_000_000), "S5": (32_000_000, 33_000_000),
    "A1": (33_000_000, 34_000_000), "E003-pre-D3-guard": (34_000_000, 35_000_000),
    "D3": (35_000_000, 36_000_000), "E003-post-D3-guard": (36_000_000, 37_000_000),
    "H3": (37_000_000, 38_000_000), "G4-pre": (38_000_000, 39_000_000),
    "D4": (39_000_000, 40_000_000), "G4-mid": (40_000_000, 41_000_000),
    "H4": (41_000_000, 42_000_000), "D6": (42_000_000, 43_000_000),
    "G6-mid": (43_000_000, 44_000_000), "H6": (44_000_000, 45_000_000),
    "G7-pre": (45_000_000, 46_000_000), "D7": (46_000_000, 47_000_000),
    "G7-mid": (47_000_000, 48_000_000), "H7": (48_000_000, 49_000_000),
    "G8-pre": (49_000_000, 50_000_000), "D8": (50_000_000, 51_000_000),
    "G8-mid": (51_000_000, 52_000_000), "H8": (52_000_000, 53_000_000),
    "G9-pre": (53_000_000, 54_000_000), "D9": (54_000_000, 55_000_000),
    "G9-mid": (55_000_000, 56_000_000), "H9": (56_000_000, 57_000_000),
    "A8": (66_000_000, 67_000_000), "A3": (70_000_000, 71_000_000),
    "A4": (78_000_000, 79_000_000), "A6": (84_000_000, 85_000_000),
    "A7": (92_000_000, 93_000_000), "A9": (108_000_000, 109_000_000),
}
E005_CALIBRATION_RANGES = tuple(
    (start, start + 1_048_576)
    for start in (128_000_000, 256_000_000, 512_000_000, 1_024_000_000,
                  2_048_000_000, 4_096_000_000)
)
FAMILY_DEFINITIONS = {
    "L1": "period length ell of the exact denominator cycle",
    "L2": "number of distinct positive denominator values in the cycle",
    "L3": "maximum multiplicity of a denominator value in the cycle",
    "L4": "exact denominator-multiplicity profile H=(h1,...,hM)",
}
PAYLOAD_KEYS = frozenset({
    "experiment", "implementation_commit", "band", "partition", "parameters",
    "generation_plan", "anchor_summary", "validation", "families", "promotions",
})
ANCHOR_SUMMARY_KEYS = frozenset({
    "admissible_count", "prime_count", "composite_count",
    "q_admissible_perfect_squares_excluded", "first_prime", "last_prime",
})
VALIDATION_KEYS = frozenset({
    "integer_root_or_domain_failure_count",
    "recurrence_positivity_or_divisibility_failure_count",
    "recurrence_quotient_bound_failure_count",
    "premature_nonterminal_state_repeat_failure_count",
    "terminal_state_failure_count",
    "denominator_multiplicity_or_profile_identity_failure_count",
})
FAMILY_ROW_KEYS = frozenset({
    "family", "prime_frequency_table", "composite_frequency_table",
    "prime_mode_count", "prime_maximizing_signatures", "runner_up_count",
    "strict_unique_prime_mode", "unique_mode_composite_count",
    "unique_mode_enrichment_numerator", "population_floor_passed",
    "occurrence_floor_passed", "enrichment_passed", "mechanically_eligible",
})


H10_PAYLOAD_KEYS = frozenset({
    "experiment", "implementation_commit", "band", "generation_plan", "replication",
})
H10_REPLICATION_KEYS = frozenset({
    "observation_id", "family", "target_signature",
    "prime_population", "composite_population",
    "target_prime_count", "highest_competing_prime_count",
    "target_composite_count", "target_enrichment_numerator",
    "population_floor_passed", "occurrence_floor_passed",
    "strict_unique_prime_mode", "enrichment_passed", "replication_passed",
})


def _intersects(left: tuple[int, int], right: tuple[int, int]) -> bool:
    return max(left[0], right[0]) < min(left[1], right[1])


def validate_frozen_metadata() -> None:
    if WIDTH != 1_000_000 or Q != 210 or Q != 2 * 3 * 5 * 7:
        raise ValueError("frozen E010 width/Q changed")
    expected = {
        "G10-pre": (57_000_000, 58_000_000), "D10": (58_000_000, 59_000_000),
        "G10-mid": (59_000_000, 60_000_000), "H10": (60_000_000, 61_000_000),
        "A10": (116_000_000, 117_000_000),
    }
    rows = {name: interval for name, _, interval in FROZEN_PARTITION}
    if rows != expected or BANDS != {name: expected[name] for name in ("D10", "H10", "A10")}:
        raise ValueError("frozen E010 partition changed")
    if any(hi - lo != WIDTH for lo, hi in rows.values()):
        raise ValueError("frozen E010 width arithmetic changed")
    intervals = list(rows.values())
    if any(_intersects(left, right) for i, left in enumerate(intervals) for right in intervals[i + 1:]):
        raise ValueError("frozen E010 partition overlaps")
    for interval in intervals:
        if any(_intersects(interval, prior) for prior in HISTORICAL_RANGES.values()):
            raise ValueError("E010 partition intersects historical novelty range")
        if any(_intersects(interval, prior) for prior in E005_CALIBRATION_RANGES):
            raise ValueError("E010 partition intersects quarantined E005 calibration segment")
    if expected["A10"][0] != 2 * expected["D10"][0]:
        raise ValueError("frozen E010 adversarial arithmetic changed")
    if POPULATION_FLOOR != 1000 or POPULATION_FLOOR != WIDTH // 1000:
        raise ValueError("frozen E010 population floor changed")
    if OCCURRENCE_FLOOR != 32 or 31**2 >= POPULATION_FLOOR or 32**2 < POPULATION_FLOOR:
        raise ValueError("frozen E010 occurrence floor changed")


def generation_plan(band_name: str) -> list[dict[str, Any]]:
    if band_name not in BANDS:
        raise ValueError(f"unknown frozen E010 band: {band_name}")
    start, stop = BANDS[band_name]
    return [
        {"purpose": "base_sieve_support", "strategy": "whole_prefix",
         "start": 0, "stop": isqrt(stop - 1) + 1},
        {"purpose": "segmented_target", "strategy": "segmented",
         "start": start, "stop": stop},
    ]


def validate_generation_plan(plan: list[dict[str, Any]], *, band_name: str) -> None:
    """D1-31 fail-closed H10 gate; runs before either prime generator."""
    validate_frozen_metadata()
    if band_name != "H10":
        raise ValueError("D1-31 authorizes H10 generation only")
    canonical = generation_plan("H10")
    if plan != canonical:
        raise ValueError("D1-31 plan must equal exact canonical H10 plan")
    if canonical != [
        {"purpose": "base_sieve_support", "strategy": "whole_prefix", "start": 0, "stop": 7811},
        {"purpose": "segmented_target", "strategy": "segmented",
         "start": 60_000_000, "stop": 61_000_000},
    ]:
        raise ValueError("canonical H10 generation arithmetic changed")
    if canonical[0]["stop"] > LOW_SUPPORT_STOP:
        raise ValueError("whole-prefix generation above 100,000 is forbidden")
    target = BANDS["H10"]
    if any(_intersects(target, prior) for prior in HISTORICAL_RANGES.values()):
        raise ValueError("H10 intersects historical novelty range")
    if any(_intersects(target, prior) for prior in E005_CALIBRATION_RANGES):
        raise ValueError("H10 intersects E005 calibration range")
    if any(name != "H10" and _intersects(target, interval)
           for name, _, interval in FROZEN_PARTITION):
        raise ValueError("H10 intersects E010 non-target")


def _segmented_target_prime_flags(start: int, stop: int, base_primes: Sequence[int]) -> bytearray:
    flags = bytearray(b"\x01") * (stop - start)
    for prime in base_primes:
        first = max(prime * prime, ((start + prime - 1) // prime) * prime)
        if first >= stop:
            continue
        count = ((stop - 1 - first) // prime) + 1
        flags[first - start: stop - start: prime] = b"\x00" * count
    return flags


def execute_generation_plan(plan: list[dict[str, Any]], *, band_name: str) -> tuple[list[int], bytearray]:
    validate_generation_plan(plan, band_name=band_name)
    base_primes = sieve(int(plan[0]["stop"]) - 1)
    flags = _segmented_target_prime_flags(
        int(plan[1]["start"]), int(plan[1]["stop"]), base_primes
    )
    return base_primes, flags


def is_q_admissible(value: int) -> bool:
    return gcd(value, Q) == 1


def is_anchor_in_common_domain(value: int) -> bool:
    return is_q_admissible(value) and isqrt(value) ** 2 != value


def partition_admissible_anchors(
    anchors: Iterable[int], prime_values: Iterable[int]
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    prime_set = frozenset(prime_values)
    primes, composites = [], []
    for anchor in anchors:
        if not is_anchor_in_common_domain(anchor):
            raise ValueError("anchor domain must contain only Q-admissible nonsquares")
        (primes if anchor in prime_set else composites).append(anchor)
    return tuple(primes), tuple(composites)


def validate_frequency_totals(
    prime_counters: Mapping[str, Counter[Signature]],
    composite_counters: Mapping[str, Counter[Signature]], *, N_prime: int, N_composite: int,
) -> None:
    for family in FAMILY_ORDER:
        if sum(prime_counters[family].values()) != N_prime:
            raise ValueError(f"{family} prime frequency table does not exhaust prime anchors")
        if sum(composite_counters[family].values()) != N_composite:
            raise ValueError(f"{family} composite frequency table does not exhaust composite anchors")


def _parameters() -> dict[str, Any]:
    return {
        "Q": Q, "width": WIDTH,
        "common_anchor_domain": "gcd(x,210)=1 and x is not a perfect square",
        "recurrence": {
            "initial_state": ["m_0=0", "d_0=1", "a_0=isqrt(x)"],
            "m_update": "m_{k+1}=d_k*a_k-m_k",
            "d_update": "d_{k+1}=(x-m_{k+1}^2)/d_k",
            "a_update": "a_{k+1}=floor((a0+m_{k+1})/d_{k+1})",
            "terminal_state": "(a0,1,2*a0)",
        },
        "denominator_cycle": "D(x)=(d_1,...,d_ell), including terminal d_ell=1",
        "family_definitions": [
            {"family": family, "definition": FAMILY_DEFINITIONS[family]}
            for family in FAMILY_ORDER
        ],
        "population_floor": POPULATION_FLOOR,
        "occurrence_floor": OCCURRENCE_FLOOR,
        "promotion_cap": PROMOTION_CAP,
    }


_WORKER_BAND_START = 0
_WORKER_PRIME_FLAGS = b""


def _init_summary_worker(band_start: int, prime_flags: bytes) -> None:
    global _WORKER_BAND_START, _WORKER_PRIME_FLAGS
    _WORKER_BAND_START = band_start
    _WORKER_PRIME_FLAGS = prime_flags


def _evaluate_anchor_block(bounds: tuple[int, int]) -> dict[str, Any]:
    block_start, block_stop = bounds
    prime_counters = {family: Counter() for family in FAMILY_ORDER}
    composite_counters = {family: Counter() for family in FAMILY_ORDER}
    prime_signatures: dict[str, list[Signature]] = {family: [] for family in FAMILY_ORDER}
    admissible_count = square_excluded = N_prime = N_composite = 0
    first_prime = last_prime = None
    for anchor in range(block_start, block_stop):
        if not is_q_admissible(anchor):
            continue
        root = isqrt(anchor)
        if root * root == anchor:
            square_excluded += 1
            continue
        admissible_count += 1
        is_prime = bool(_WORKER_PRIME_FLAGS[anchor - _WORKER_BAND_START])
        if is_prime:
            N_prime += 1
            first_prime = anchor if first_prime is None else first_prime
            last_prime = anchor
            counters = prime_counters
        else:
            N_composite += 1
            counters = composite_counters
        signatures = cycle_signatures(anchor)
        for family in FAMILY_ORDER:
            signature = signatures[family]
            counters[family][signature] += 1
            if is_prime:
                prime_signatures[family].append(signature)
    return {
        "prime_counters": prime_counters,
        "composite_counters": composite_counters,
        "prime_signatures": prime_signatures,
        "admissible_count": admissible_count,
        "square_excluded": square_excluded,
        "prime_count": N_prime,
        "composite_count": N_composite,
        "first_prime": first_prime,
        "last_prime": last_prime,
    }


def _evaluate_all_anchor_blocks(
    *, start: int, stop: int, target_prime_flags: Sequence[int]
) -> list[dict[str, Any]]:
    blocks = [
        (block_start, min(block_start + SUMMARY_BLOCK_SIZE, stop))
        for block_start in range(start, stop, SUMMARY_BLOCK_SIZE)
    ]
    with get_context("spawn").Pool(
        processes=SUMMARY_WORKERS,
        initializer=_init_summary_worker,
        initargs=(start, bytes(target_prime_flags)),
    ) as pool:
        return pool.map(_evaluate_anchor_block, blocks, chunksize=1)


def summarise_band(
    *, band_name: str, code_commit: str, plan: list[dict[str, Any]],
    target_prime_flags: Sequence[int],
) -> dict[str, Any]:
    validate_generation_plan(plan, band_name=band_name)
    start, stop = BANDS[band_name]
    if len(target_prime_flags) != stop - start:
        raise ValueError("target flags must span exactly D10")
    prime_counters = {family: Counter() for family in FAMILY_ORDER}
    composite_counters = {family: Counter() for family in FAMILY_ORDER}
    prime_signatures: dict[str, list[Signature]] = {family: [] for family in FAMILY_ORDER}
    admissible_count = square_excluded = N_prime = N_composite = 0
    first_prime = last_prime = None
    validation = {key: 0 for key in sorted(VALIDATION_KEYS)}

    for result in _evaluate_all_anchor_blocks(
        start=start, stop=stop, target_prime_flags=target_prime_flags
    ):
        admissible_count += int(result["admissible_count"])
        square_excluded += int(result["square_excluded"])
        N_prime += int(result["prime_count"])
        N_composite += int(result["composite_count"])
        if first_prime is None and result["first_prime"] is not None:
            first_prime = int(result["first_prime"])
        if result["last_prime"] is not None:
            last_prime = int(result["last_prime"])
        for family in FAMILY_ORDER:
            prime_counters[family].update(result["prime_counters"][family])
            composite_counters[family].update(result["composite_counters"][family])
            prime_signatures[family].extend(result["prime_signatures"][family])

    if admissible_count != N_prime + N_composite:
        raise ValueError("prime/composite partition does not exhaust common domain")
    if N_prime != sum(int(flag) for flag in target_prime_flags):
        raise ValueError("D10 prime flags do not equal prime anchor population")
    validate_frequency_totals(
        prime_counters, composite_counters, N_prime=N_prime, N_composite=N_composite
    )
    family_rows, mode_sets = [], {}
    for family in FAMILY_ORDER:
        row, unique = family_row(
            family=family, prime_counter=prime_counters[family],
            composite_counter=composite_counters[family],
            N_prime=N_prime, N_composite=N_composite,
        )
        if unique is not None:
            mode_sets[family] = frozenset(
                i for i, signature in enumerate(prime_signatures[family]) if signature == unique
            )
        family_rows.append(row)
    promotions = apply_duplicate_suppression(family_rows, mode_sets)
    payload = {
        "experiment": EXPERIMENT_ID, "implementation_commit": code_commit,
        "band": {"name": band_name, "range": [start, stop], "interval_semantics": "half-open"},
        "partition": [
            {"name": name, "role": role, "range": list(interval)}
            for name, role, interval in FROZEN_PARTITION
        ],
        "parameters": _parameters(), "generation_plan": plan,
        "anchor_summary": {
            "admissible_count": admissible_count, "prime_count": N_prime,
            "composite_count": N_composite,
            "q_admissible_perfect_squares_excluded": square_excluded,
            "first_prime": first_prime, "last_prime": last_prime,
        },
        "validation": validation, "families": family_rows, "promotions": promotions,
    }
    if frozenset(payload) != PAYLOAD_KEYS:
        raise ValueError("E010 payload escaped frozen descriptive allowlist")
    if frozenset(payload["anchor_summary"]) != ANCHOR_SUMMARY_KEYS:
        raise ValueError("E010 anchor summary escaped frozen descriptive allowlist")
    if frozenset(payload["validation"]) != VALIDATION_KEYS:
        raise ValueError("E010 validation escaped frozen descriptive allowlist")
    if any(frozenset(row) != FAMILY_ROW_KEYS for row in family_rows):
        raise ValueError("E010 family row escaped frozen descriptive allowlist")
    return payload

def h10_replication_fields(
    *, prime_counter: Mapping[int, int], composite_counter: Mapping[int, int],
    N_prime: int, N_composite: int,
) -> dict[str, Any]:
    """Evaluate only the precommitted OBS-014 L2/1487 H10 criterion."""
    if sum(int(count) for count in prime_counter.values()) != N_prime:
        raise ValueError("H10 L2 prime counter does not exhaust prime anchors")
    if sum(int(count) for count in composite_counter.values()) != N_composite:
        raise ValueError("H10 L2 composite counter does not exhaust composite anchors")
    if any(not isinstance(signature, int) or signature < 1 for signature in prime_counter):
        raise ValueError("H10 L2 prime signatures must be positive integers")
    if any(not isinstance(signature, int) or signature < 1 for signature in composite_counter):
        raise ValueError("H10 L2 composite signatures must be positive integers")

    target_prime_count = int(prime_counter.get(H10_TARGET_SIGNATURE, 0))
    highest_competing_prime_count = max(
        (int(count) for signature, count in prime_counter.items()
         if signature != H10_TARGET_SIGNATURE),
        default=0,
    )
    target_composite_count = int(composite_counter.get(H10_TARGET_SIGNATURE, 0))
    target_enrichment_numerator = (
        target_prime_count * N_composite - target_composite_count * N_prime
    )
    population_floor_passed = (
        N_prime >= POPULATION_FLOOR and N_composite >= POPULATION_FLOOR
    )
    occurrence_floor_passed = target_prime_count >= OCCURRENCE_FLOOR
    strict_unique_prime_mode = target_prime_count > highest_competing_prime_count
    enrichment_passed = target_enrichment_numerator > 0
    replication_passed = bool(
        population_floor_passed
        and occurrence_floor_passed
        and strict_unique_prime_mode
        and enrichment_passed
    )
    fields = {
        "observation_id": H10_OBSERVATION_ID,
        "family": H10_FAMILY,
        "target_signature": H10_TARGET_SIGNATURE,
        "prime_population": N_prime,
        "composite_population": N_composite,
        "target_prime_count": target_prime_count,
        "highest_competing_prime_count": highest_competing_prime_count,
        "target_composite_count": target_composite_count,
        "target_enrichment_numerator": target_enrichment_numerator,
        "population_floor_passed": population_floor_passed,
        "occurrence_floor_passed": occurrence_floor_passed,
        "strict_unique_prime_mode": strict_unique_prime_mode,
        "enrichment_passed": enrichment_passed,
        "replication_passed": replication_passed,
    }
    if frozenset(fields) != H10_REPLICATION_KEYS:
        raise ValueError("H10 replication fields escaped frozen criterion allowlist")
    return fields


def _evaluate_h10_l2_block(bounds: tuple[int, int]) -> dict[str, Any]:
    block_start, block_stop = bounds
    prime_counter: Counter[int] = Counter()
    composite_counter: Counter[int] = Counter()
    admissible_count = N_prime = N_composite = 0
    for anchor in range(block_start, block_stop):
        if not is_q_admissible(anchor):
            continue
        root = isqrt(anchor)
        if root * root == anchor:
            continue
        admissible_count += 1
        is_prime = bool(_WORKER_PRIME_FLAGS[anchor - _WORKER_BAND_START])
        if is_prime:
            N_prime += 1
            counter = prime_counter
        else:
            N_composite += 1
            counter = composite_counter
        signature = cycle_signatures(anchor)[H10_FAMILY]
        if not isinstance(signature, int):
            raise ValueError("frozen H10 L2 signature must be an integer")
        counter[signature] += 1
    return {
        "prime_counter": prime_counter,
        "composite_counter": composite_counter,
        "admissible_count": admissible_count,
        "prime_count": N_prime,
        "composite_count": N_composite,
    }


def _evaluate_all_h10_l2_blocks(
    *, start: int, stop: int, target_prime_flags: Sequence[int]
) -> list[dict[str, Any]]:
    blocks = [
        (block_start, min(block_start + SUMMARY_BLOCK_SIZE, stop))
        for block_start in range(start, stop, SUMMARY_BLOCK_SIZE)
    ]
    with get_context("spawn").Pool(
        processes=SUMMARY_WORKERS,
        initializer=_init_summary_worker,
        initargs=(start, bytes(target_prime_flags)),
    ) as pool:
        return pool.map(_evaluate_h10_l2_block, blocks, chunksize=1)


def summarise_h10_replication(
    *, code_commit: str, plan: list[dict[str, Any]], target_prime_flags: Sequence[int],
) -> dict[str, Any]:
    validate_generation_plan(plan, band_name="H10")
    start, stop = BANDS["H10"]
    if len(target_prime_flags) != stop - start:
        raise ValueError("target flags must span exactly H10")

    prime_counter: Counter[int] = Counter()
    composite_counter: Counter[int] = Counter()
    admissible_count = N_prime = N_composite = 0
    for result in _evaluate_all_h10_l2_blocks(
        start=start, stop=stop, target_prime_flags=target_prime_flags
    ):
        admissible_count += int(result["admissible_count"])
        N_prime += int(result["prime_count"])
        N_composite += int(result["composite_count"])
        prime_counter.update(result["prime_counter"])
        composite_counter.update(result["composite_counter"])

    if admissible_count != N_prime + N_composite:
        raise ValueError("H10 prime/composite partition does not exhaust common domain")
    if N_prime != sum(int(flag) for flag in target_prime_flags):
        raise ValueError("H10 prime flags do not equal prime anchor population")

    replication = h10_replication_fields(
        prime_counter=prime_counter,
        composite_counter=composite_counter,
        N_prime=N_prime,
        N_composite=N_composite,
    )
    payload = {
        "experiment": EXPERIMENT_ID,
        "implementation_commit": code_commit,
        "band": {"name": "H10", "range": [start, stop], "interval_semantics": "half-open"},
        "generation_plan": plan,
        "replication": replication,
    }
    if frozenset(payload) != H10_PAYLOAD_KEYS:
        raise ValueError("H10 payload escaped frozen replication allowlist")
    return payload


def build_payload(*, band_name: str, code_commit: str) -> dict[str, Any]:
    if band_name != "H10":
        raise ValueError("D1-31 build path authorizes H10 only")
    plan = generation_plan("H10")
    validate_generation_plan(plan, band_name="H10")
    _, flags = execute_generation_plan(plan, band_name="H10")
    return summarise_h10_replication(
        code_commit=code_commit, plan=plan, target_prime_flags=flags
    )


def serialise_payload(payload: Mapping[str, Any]) -> bytes:
    return (json.dumps(payload, sort_keys=True, indent=2) + "\n").encode("utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--band", choices=("H10",), required=True)
    parser.add_argument("--code-commit", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rendered = serialise_payload(build_payload(band_name=args.band, code_commit=args.code_commit))
    if args.output is None:
        print(rendered.decode(), end="")
    else:
        args.output.write_bytes(rendered)


if __name__ == "__main__":
    main()
