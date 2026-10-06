#!/usr/bin/env python3
"""E004: frozen residue-transition factorization discovery evaluator."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from math import gcd, isqrt
from pathlib import Path
from typing import Any

from primes_lab.core import sieve

EXPERIMENT_ID = "E004"
MODULI = (6, 10, 12, 30, 60)
RELATIONS = ((6, 12), (6, 30), (10, 30), (12, 60), (30, 60))
FAMILY_ORDER = ("P1", "P2", "P3", "P4", "P5")
LOW_SUPPORT_STOP = 100_000
BANDS: dict[str, tuple[int, int]] = {
    "D4": (39_000_000, 40_000_000),
    "H4": (41_000_000, 42_000_000),
    "A4": (78_000_000, 79_000_000),
}
FROZEN_GUARDS: dict[str, tuple[int, int]] = {
    "G4-pre": (38_000_000, 39_000_000),
    "G4-mid": (40_000_000, 41_000_000),
}
PROTECTED_RANGES: dict[str, tuple[int, int]] = {
    "A1": (33_000_000, 34_000_000),
    "E003-pre-D3-guard": (34_000_000, 35_000_000),
    "D3": (35_000_000, 36_000_000),
    "E003-post-D3-guard": (36_000_000, 37_000_000),
    "H3": (37_000_000, 38_000_000),
    "G4-pre": FROZEN_GUARDS["G4-pre"],
    "G4-mid": FROZEN_GUARDS["G4-mid"],
    "H4": BANDS["H4"],
    "A3": (70_000_000, 71_000_000),
    "A4": BANDS["A4"],
}


def _intersects(left: tuple[int, int], right: tuple[int, int]) -> bool:
    return max(left[0], right[0]) < min(left[1], right[1])


def reduced_residues(modulus: int) -> tuple[int, ...]:
    if modulus < 2:
        raise ValueError("modulus must be at least 2")
    return tuple(value for value in range(modulus) if gcd(value, modulus) == 1)


def generation_plan(band_name: str) -> list[dict[str, Any]]:
    try:
        start, stop = BANDS[band_name]
    except KeyError as exc:
        raise ValueError(f"unknown frozen E004 band: {band_name}") from exc
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
    """Fail closed before generation unless the complete plan obeys E004."""
    try:
        target = BANDS[band_name]
    except KeyError as exc:
        raise ValueError(f"unknown frozen E004 band: {band_name}") from exc
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
                raise ValueError(f"generation interval intersects protected range {name}")

    base = base_rows[0]
    if int(base["stop"]) - 1 != isqrt(target[1] - 1):
        raise ValueError("base sieve must end at floor(sqrt(U-1)) inclusive")


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


def transition_counts(
    primes: list[int],
    modulus: int,
    *,
    start: int | None = None,
    stop: int | None = None,
) -> Counter[tuple[int, int]]:
    """Exact band-local reduced-residue directed transition counts."""
    selected = primes
    if start is not None or stop is not None:
        if start is None or stop is None or stop <= start:
            raise ValueError("start and stop must define a non-empty half-open band")
        selected = [prime for prime in primes if start <= prime < stop]
    filtered = [prime for prime in selected if gcd(prime, modulus) == 1]
    residues = [prime % modulus for prime in filtered]
    return Counter(zip(residues, residues[1:], strict=False))


def lift_set(coarse_modulus: int, fine_modulus: int, residue: int) -> tuple[int, ...]:
    if fine_modulus % coarse_modulus != 0:
        raise ValueError("coarse modulus must divide fine modulus")
    if residue not in reduced_residues(coarse_modulus):
        raise ValueError("coarse residue must be reduced")
    return tuple(
        fine
        for fine in reduced_residues(fine_modulus)
        if fine % coarse_modulus == residue
    )


def project_counts(
    fine_counts: Counter[tuple[int, int]], *, fine_modulus: int, coarse_modulus: int
) -> Counter[tuple[int, int]]:
    if fine_modulus % coarse_modulus != 0:
        raise ValueError("coarse modulus must divide fine modulus")
    projected: Counter[tuple[int, int]] = Counter()
    for (left, right), count in fine_counts.items():
        projected[(left % coarse_modulus, right % coarse_modulus)] += count
    return projected


def _matrix_objects(matrix: tuple[tuple[int, ...], ...], coarse_count: int) -> dict[str, Any]:
    h = len(matrix)
    if h < 1 or any(len(row) != h for row in matrix):
        raise ValueError("refinement matrix must be non-empty and square")
    flat = tuple(value for row in matrix for value in row)
    k = h * h
    forbidden_mask = tuple(1 if value == 0 else 0 for value in flat)
    balance_vector = tuple(k * value - coarse_count for value in flat)
    if sum(balance_vector) != 0:
        raise ValueError("balance vector must sum to zero under exact projection")

    determinants: list[int] = []
    for i1 in range(h):
        for i2 in range(i1 + 1, h):
            for j1 in range(h):
                for j2 in range(j1 + 1, h):
                    determinants.append(
                        matrix[i1][j1] * matrix[i2][j2]
                        - matrix[i1][j2] * matrix[i2][j1]
                    )
    determinant_vector = tuple(determinants)
    minor_zero_mask = tuple(1 if value == 0 else 0 for value in determinant_vector)
    uniform = all(value == 0 for value in balance_vector)
    positive_rank_one = all(value > 0 for value in flat) and all(
        value == 0 for value in determinant_vector
    )
    return {
        "forbidden_lift_mask": forbidden_mask,
        "balance_vector": balance_vector,
        "determinant_vector": determinant_vector,
        "minor_zero_mask": minor_zero_mask,
        "uniform": uniform,
        "positive_rank_one": positive_rank_one,
    }


def _frequency_table(counter: Counter[tuple[int, ...]]) -> list[dict[str, Any]]:
    return [{"value": list(value), "count": counter[value]} for value in sorted(counter)]


def _mode_stats(values: list[tuple[int, ...]]) -> dict[str, Any]:
    counter = Counter(values)
    ranked = sorted(counter.items(), key=lambda item: (-item[1], item[0]))
    mode_value = ranked[0][0] if ranked else None
    mode_count = ranked[0][1] if ranked else 0
    runner_up_count = ranked[1][1] if len(ranked) > 1 else 0
    strict_unique_mode = bool(ranked) and (len(ranked) == 1 or mode_count > runner_up_count)
    return {
        "eligible_coarse_pair_count": len(values),
        "mode_value": list(mode_value) if mode_value is not None else None,
        "mode_count": mode_count,
        "runner_up_count": runner_up_count,
        "dominance_margin": mode_count - runner_up_count,
        "strict_unique_mode": strict_unique_mode,
        "occurrence_floor_passed": mode_count >= 2,
        "coarse_pair_floor_passed": len(values) >= 4,
        "mechanical_eligible": len(values) >= 4 and mode_count >= 2 and strict_unique_mode,
    }


def _relation_summary(
    coarse_modulus: int,
    fine_modulus: int,
    counts: dict[int, Counter[tuple[int, int]]],
) -> dict[str, Any]:
    coarse_residues = reduced_residues(coarse_modulus)
    fine_residues = reduced_residues(fine_modulus)
    expected_h = len(fine_residues) // len(coarse_residues)
    source_lifts = {
        residue: lift_set(coarse_modulus, fine_modulus, residue)
        for residue in coarse_residues
    }
    if any(len(lifts) != expected_h for lifts in source_lifts.values()):
        raise ValueError("lift cardinality mismatch")

    projected = project_counts(
        counts[fine_modulus], fine_modulus=fine_modulus, coarse_modulus=coarse_modulus
    )
    fibres: list[dict[str, Any]] = []
    nonempty_masks: list[tuple[int, ...]] = []
    nonzero_balances: list[tuple[int, ...]] = []
    nontrivial_minor_masks: list[tuple[int, ...]] = []
    all_coarse_positive = True
    all_fine_positive = True
    all_uniform = True
    all_positive_rank_one = True

    for left in coarse_residues:
        for right in coarse_residues:
            coarse_count = counts[coarse_modulus].get((left, right), 0)
            projected_count = projected.get((left, right), 0)
            residual = coarse_count - projected_count
            if residual != 0:
                raise ValueError(
                    f"nonzero mandatory projection residual on {coarse_modulus}->{fine_modulus} "
                    f"pair {(left, right)}: {residual}"
                )
            left_lifts = source_lifts[left]
            right_lifts = source_lifts[right]
            matrix = tuple(
                tuple(
                    counts[fine_modulus].get((fine_left, fine_right), 0)
                    for fine_right in right_lifts
                )
                for fine_left in left_lifts
            )
            objects = _matrix_objects(matrix, coarse_count)
            flat = tuple(value for row in matrix for value in row)
            all_coarse_positive = all_coarse_positive and coarse_count > 0
            all_fine_positive = all_fine_positive and all(value > 0 for value in flat)
            all_uniform = all_uniform and bool(objects["uniform"])
            all_positive_rank_one = all_positive_rank_one and bool(
                objects["positive_rank_one"]
            )

            forbidden = objects["forbidden_lift_mask"]
            balance = objects["balance_vector"]
            minor_mask = objects["minor_zero_mask"]
            if any(forbidden):
                nonempty_masks.append(forbidden)
            if any(balance):
                nonzero_balances.append(balance)
            if minor_mask and any(minor_mask) and not all(minor_mask):
                nontrivial_minor_masks.append(minor_mask)

            fibres.append(
                {
                    "coarse_transition": [left, right],
                    "coarse_count": coarse_count,
                    "projected_fine_count": projected_count,
                    "projection_residual": residual,
                    "source_lifts": list(left_lifts),
                    "destination_lifts": list(right_lifts),
                    "refinement_matrix": [list(row) for row in matrix],
                    "forbidden_lift_mask": list(forbidden),
                    "balance_vector": list(balance),
                    "determinant_vector": list(objects["determinant_vector"]),
                    "minor_zero_mask": list(minor_mask),
                    "uniform": objects["uniform"],
                    "positive_rank_one": objects["positive_rank_one"],
                }
            )

    p1 = all_coarse_positive and all_fine_positive and all_uniform
    rank_one_complete = all_coarse_positive and all_fine_positive and all_positive_rank_one
    p2 = rank_one_complete and not p1
    p3_stats = _mode_stats(nonempty_masks)
    p4_stats = _mode_stats(nonzero_balances)
    p5_stats = _mode_stats(nontrivial_minor_masks)
    frequencies = {
        "nonempty_forbidden_lift_masks": _frequency_table(Counter(nonempty_masks)),
        "nonzero_balance_vectors": _frequency_table(Counter(nonzero_balances)),
        "nontrivial_minor_zero_masks": _frequency_table(Counter(nontrivial_minor_masks)),
    }
    return {
        "edge": [coarse_modulus, fine_modulus],
        "lift_cardinality": expected_h,
        "lift_sets": [
            {"coarse_residue": residue, "fine_residues": list(source_lifts[residue])}
            for residue in coarse_residues
        ],
        "fibres": fibres,
        "frequencies": frequencies,
        "complete_positive_uniform_refinement": p1,
        "complete_positive_rank_one_refinement": rank_one_complete,
        "promotion_records": [
            {"family": "P1", "mechanical_eligible": p1, "target": None},
            {
                "family": "P2",
                "mechanical_eligible": p2,
                "target": None,
                "suppressed_by_P1": p1,
            },
            {"family": "P3", **p3_stats, "target": p3_stats["mode_value"]},
            {"family": "P4", **p4_stats, "target": p4_stats["mode_value"]},
            {"family": "P5", **p5_stats, "target": p5_stats["mode_value"]},
        ],
    }


def _sort_promotion_pool(relations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    relation_priority = {edge: index for index, edge in enumerate(RELATIONS)}
    family_priority = {family: index for index, family in enumerate(FAMILY_ORDER)}
    rows: list[dict[str, Any]] = []
    for relation in relations:
        edge = tuple(relation["edge"])
        for record in relation["promotion_records"]:
            row = {"edge": list(edge), **record}
            rows.append(row)

    def key(row: dict[str, Any]) -> tuple[Any, ...]:
        family = row["family"]
        edge = tuple(row["edge"])
        target = tuple(row.get("target") or [])
        if family in ("P1", "P2"):
            return (family_priority[family], 0, 0, relation_priority[edge], target)
        return (
            family_priority[family],
            -int(row.get("dominance_margin", 0)),
            -int(row.get("mode_count", 0)),
            relation_priority[edge],
            target,
        )

    return sorted(rows, key=key)


def _transition_section(
    primes: list[int], modulus: int
) -> tuple[Counter[tuple[int, int]], dict[str, Any]]:
    residues = reduced_residues(modulus)
    counter = transition_counts(primes, modulus)
    possible = [(left, right) for left in residues for right in residues]
    missing = [pair for pair in possible if counter.get(pair, 0) == 0]
    table = [
        {"transition": [left, right], "count": counter.get((left, right), 0)}
        for left, right in possible
    ]
    return counter, {
        "modulus": modulus,
        "reduced_residues": list(residues),
        "transition_total": sum(counter.values()),
        "transition_counts": table,
        "support_size": len(counter),
        "missing_allowed_pairs": [list(pair) for pair in missing],
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
    if any(prime < start or prime >= stop for prime in primes):
        raise ValueError("prime input contains a value outside the selected band")
    counts: dict[int, Counter[tuple[int, int]]] = {}
    transition_sections: list[dict[str, Any]] = []
    for modulus in MODULI:
        counter, section = _transition_section(primes, modulus)
        counts[modulus] = counter
        transition_sections.append(section)

    relations = [_relation_summary(coarse, fine, counts) for coarse, fine in RELATIONS]
    promotion_pool = _sort_promotion_pool(relations)
    return {
        "experiment": EXPERIMENT_ID,
        "implementation_commit": code_commit,
        "band": {
            "name": band_name,
            "range": [start, stop],
            "interval_semantics": "half-open",
        },
        "guards": [
            {"name": name, "range": list(interval)}
            for name, interval in FROZEN_GUARDS.items()
        ],
        "generation_plan": plan,
        "modulus_family": list(MODULI),
        "relation_graph": [list(edge) for edge in RELATIONS],
        "prime_summary": {
            "count": len(primes),
            "first_prime": primes[0] if primes else None,
            "last_prime": primes[-1] if primes else None,
        },
        "transitions": transition_sections,
        "relations": relations,
        "promotion_pool": promotion_pool,
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
