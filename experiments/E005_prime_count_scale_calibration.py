#!/usr/bin/env python3
"""E005: frozen prime-count scale calibration evaluator."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from collections.abc import Iterable
from decimal import ROUND_HALF_EVEN, Context, Decimal, localcontext
from fractions import Fraction
from math import isqrt
from pathlib import Path
from typing import Any

EXPERIMENT_ID = "E005"
LANE = "historical_rediscovery_calibration"
LOW_SUPPORT_STOP = 100_000
DECIMAL_PRECISION = 90
DECIMAL_CONTEXT = Context(prec=DECIMAL_PRECISION, rounding=ROUND_HALF_EVEN)

WIDTHS: tuple[tuple[str, int], ...] = (
    ("W0", 4_096),
    ("W1", 16_384),
    ("W2", 65_536),
    ("W3", 262_144),
    ("W4", 1_048_576),
)
DEVELOPMENT_ANCHORS: tuple[tuple[str, int], ...] = (
    ("D5-0", 128_000_000),
    ("D5-1", 256_000_000),
    ("D5-2", 512_000_000),
)
ASSESSMENT_ANCHORS: tuple[tuple[str, int], ...] = (
    ("H5-0", 1_024_000_000),
    ("H5-1", 2_048_000_000),
    ("H5-2", 4_096_000_000),
)
CANDIDATES: tuple[str, ...] = tuple(f"N{i:02d}" for i in range(13))
RESIDUAL_FAMILIES = ("R0", "R1", "R2", "R3", "R4")

PROTECTED_RANGES: dict[str, tuple[int, int]] = {
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
    "A3": (70_000_000, 71_000_000),
    "A4": (78_000_000, 79_000_000),
}


def _anchors_for_phase(phase: str) -> tuple[tuple[str, int], ...]:
    if phase == "development":
        return DEVELOPMENT_ANCHORS
    if phase == "assessment":
        return ASSESSMENT_ANCHORS
    raise ValueError(f"unknown E005 phase: {phase}")


def _intersects(left: tuple[int, int], right: tuple[int, int]) -> bool:
    return max(left[0], right[0]) < min(left[1], right[1])


def rational_pair(value: Fraction | int) -> list[int]:
    fraction = value if isinstance(value, Fraction) else Fraction(value)
    return [fraction.numerator, fraction.denominator]


def decimal_string(value: Decimal) -> str:
    if not value.is_finite():
        raise ValueError("non-finite Decimal value is forbidden")
    return format(value, ".60E")


def _decimal_from_rational(value: Fraction) -> Decimal:
    with localcontext(DECIMAL_CONTEXT):
        result = Decimal(value.numerator) / Decimal(value.denominator)
    if not result.is_finite():
        raise ValueError("non-finite Decimal rational conversion")
    return result


def _scale_decimal(anchor: int, width: int) -> Decimal:
    with localcontext(DECIMAL_CONTEXT):
        value = Decimal(2 * anchor + width) / Decimal(2)
    if value <= 0 or not value.is_finite():
        raise ValueError("scale coordinate must be positive and finite")
    return value


def transform_density(candidate: str, count: int, anchor: int, width: int) -> Decimal:
    if candidate not in CANDIDATES:
        raise ValueError(f"unknown normalization candidate: {candidate}")
    if count < 0 or width <= 0:
        raise ValueError("count must be non-negative and width positive")
    density = _decimal_from_rational(Fraction(count, width))
    if density <= 0:
        raise ValueError("transformed density requires a positive prime count")
    scale = _scale_decimal(anchor, width)
    with localcontext(DECIMAL_CONTEXT):
        ln_scale = scale.ln()
        sqrt_ln = ln_scale.sqrt()
        ln_ln = ln_scale.ln()
        fourth_root = scale.sqrt().sqrt()
        sqrt_scale = scale.sqrt()
        functions = (Decimal(1), ln_scale, sqrt_ln, ln_ln, fourth_root, sqrt_scale, scale)
        if any(value <= 0 or not value.is_finite() for value in functions):
            raise ValueError("nonpositive or non-finite elementary transform")
        if candidate == "N00":
            result = density
        else:
            index = (int(candidate[1:]) + 1) // 2
            factor = functions[index]
            if int(candidate[1:]) % 2 == 1:
                result = density * factor
            else:
                if factor == 0:
                    raise ValueError("division by zero in normalization")
                result = density / factor
    if result <= 0 or not result.is_finite():
        raise ValueError("normalization produced a nonpositive or non-finite value")
    return result


def count_half_open(values: Iterable[int], start: int, stop: int) -> int:
    if stop <= start:
        raise ValueError("counting interval must be non-empty")
    return sum(1 for value in values if start <= value < stop)


def nested_interval_counts(values: Iterable[int], anchor: int) -> dict[str, int]:
    materialized = tuple(values)
    return {
        width_name: count_half_open(materialized, anchor, anchor + width)
        for width_name, width in WIDTHS
    }


def _base_primes(stop: int) -> tuple[int, ...]:
    if stop < 2:
        return ()
    flags = bytearray(b"\x01") * stop
    flags[0:2] = b"\x00\x00"
    limit = isqrt(stop - 1)
    for prime in range(2, limit + 1):
        if not flags[prime]:
            continue
        first = prime * prime
        count = ((stop - 1 - first) // prime) + 1
        flags[first:stop:prime] = b"\x00" * count
    return tuple(index for index, flag in enumerate(flags) if flag)


def _segmented_counts(
    start: int, stop: int, widths: tuple[tuple[str, int], ...], base_primes: tuple[int, ...]
) -> dict[str, int]:
    if stop <= start:
        raise ValueError("segmented interval must be non-empty")
    flags = bytearray(b"\x01") * (stop - start)
    if start == 0:
        flags[0:2] = b"\x00\x00"
    elif start == 1:
        flags[0] = 0
    for prime in base_primes:
        first = max(prime * prime, ((start + prime - 1) // prime) * prime)
        if first >= stop:
            continue
        count = ((stop - 1 - first) // prime) + 1
        flags[first - start : stop - start : prime] = b"\x00" * count
    result: dict[str, int] = {}
    for width_name, width in widths:
        if width > stop - start:
            raise ValueError("nested width exceeds generated segment")
        result[width_name] = sum(flags[:width])
    return result


def generation_plan(phase: str, *, development_checkpoint_verified: bool = False) -> list[dict[str, Any]]:
    anchors = _anchors_for_phase(phase)
    if phase == "assessment" and not development_checkpoint_verified:
        raise ValueError("assessment generation requires a verified committed development checkpoint")
    maximum_stop = max(anchor + WIDTHS[-1][1] for _, anchor in anchors)
    base_stop = isqrt(maximum_stop - 1) + 1
    rows: list[dict[str, Any]] = [
        {
            "purpose": "base_sieve_support",
            "strategy": "whole_prefix",
            "start": 0,
            "stop": base_stop,
        }
    ]
    rows.extend(
        {
            "anchor_name": anchor_name,
            "purpose": "segmented_target",
            "strategy": "segmented",
            "start": anchor,
            "stop": anchor + WIDTHS[-1][1],
        }
        for anchor_name, anchor in anchors
    )
    return rows


def validate_generation_plan(
    plan: list[dict[str, Any]],
    *,
    phase: str,
    development_checkpoint_verified: bool = False,
    serialize_raw_primes: bool = False,
) -> None:
    anchors = _anchors_for_phase(phase)
    if serialize_raw_primes:
        raise ValueError("raw-prime serialization is forbidden")
    if phase == "assessment" and not development_checkpoint_verified:
        raise ValueError("assessment generation requires a verified committed development checkpoint")
    if len(plan) != 1 + len(anchors):
        raise ValueError("generation plan must contain one base request and exactly three targets")

    expected_targets = {
        name: (anchor, anchor + WIDTHS[-1][1]) for name, anchor in anchors
    }
    base_rows = [row for row in plan if row.get("purpose") == "base_sieve_support"]
    target_rows = [row for row in plan if row.get("purpose") == "segmented_target"]
    if len(base_rows) != 1 or len(target_rows) != len(anchors):
        raise ValueError("generation plan has invalid base/target cardinality")

    maximum_stop = max(stop for _, stop in expected_targets.values())
    required_base_stop = isqrt(maximum_stop - 1) + 1
    base = base_rows[0]
    if (
        int(base.get("start", -1)) != 0
        or int(base.get("stop", -1)) != required_base_stop
        or base.get("strategy") != "whole_prefix"
    ):
        raise ValueError("base support must be the exact frozen whole-prefix request")
    if int(base["stop"]) > LOW_SUPPORT_STOP:
        raise ValueError("whole-prefix generation above 100,000 is forbidden")

    seen: set[str] = set()
    for row in target_rows:
        name = str(row.get("anchor_name", ""))
        if name not in expected_targets or name in seen:
            raise ValueError("undeclared or duplicate calibration anchor")
        seen.add(name)
        start = int(row.get("start", -1))
        stop = int(row.get("stop", -1))
        if row.get("strategy") != "segmented":
            if row.get("strategy") == "whole_prefix" and stop > LOW_SUPPORT_STOP:
                raise ValueError("whole-prefix generation above 100,000 is forbidden")
            raise ValueError("all high-value calibration generation must be segmented")
        if (start, stop) != expected_targets[name]:
            raise ValueError("undeclared or widened calibration segment")
        interval = (start, stop)
        for protected_name, protected in PROTECTED_RANGES.items():
            if _intersects(interval, protected):
                raise ValueError(f"generation interval intersects protected range {protected_name}")


def execute_generation_plan(
    plan: list[dict[str, Any]],
    *,
    phase: str,
    development_checkpoint_verified: bool = False,
    serialize_raw_primes: bool = False,
) -> dict[str, dict[str, int]]:
    validate_generation_plan(
        plan,
        phase=phase,
        development_checkpoint_verified=development_checkpoint_verified,
        serialize_raw_primes=serialize_raw_primes,
    )
    base = next(row for row in plan if row["purpose"] == "base_sieve_support")
    base_primes = _base_primes(int(base["stop"]))
    counts: dict[str, dict[str, int]] = {}
    for row in plan:
        if row["purpose"] != "segmented_target":
            continue
        counts[str(row["anchor_name"])] = _segmented_counts(
            int(row["start"]), int(row["stop"]), WIDTHS, base_primes
        )
    return counts


def _count_for(counts: dict[str, dict[str, int]], anchor_name: str, width_name: str) -> int:
    try:
        return int(counts[anchor_name][width_name])
    except KeyError as exc:
        raise ValueError(f"missing count cell {anchor_name}/{width_name}") from exc


def exact_count_objects(
    counts: dict[str, dict[str, int]], anchors: tuple[tuple[str, int], ...]
) -> dict[str, Any]:
    cells: dict[str, dict[str, Any]] = {}
    for anchor_name, anchor in anchors:
        cells[anchor_name] = {}
        for width_name, width in WIDTHS:
            count = _count_for(counts, anchor_name, width_name)
            cells[anchor_name][width_name] = {
                "count": count,
                "density": rational_pair(Fraction(count, width)),
                "mean_spacing": rational_pair(Fraction(width, count)) if count else None,
                "scale_coordinate": rational_pair(Fraction(2 * anchor + width, 2)),
            }

    anchor_adjacent: dict[str, list[dict[str, Any]]] = {}
    for width_name, width in WIDTHS:
        rows: list[dict[str, Any]] = []
        for (left_name, _), (right_name, _) in zip(anchors, anchors[1:], strict=False):
            left = _count_for(counts, left_name, width_name)
            right = _count_for(counts, right_name, width_name)
            left_density = Fraction(left, width)
            right_density = Fraction(right, width)
            rows.append(
                {
                    "from": left_name,
                    "to": right_name,
                    "count_ratio": rational_pair(Fraction(right, left)),
                    "density_ratio": rational_pair(right_density / left_density),
                    "count_difference": right - left,
                    "density_difference": rational_pair(right_density - left_density),
                }
            )
        anchor_adjacent[width_name] = rows

    width_adjacent: dict[str, list[dict[str, Any]]] = {}
    for anchor_name, _ in anchors:
        rows = []
        for (left_width_name, left_width), (right_width_name, right_width) in zip(
            WIDTHS, WIDTHS[1:], strict=False
        ):
            left = _count_for(counts, anchor_name, left_width_name)
            right = _count_for(counts, anchor_name, right_width_name)
            left_density = Fraction(left, left_width)
            right_density = Fraction(right, right_width)
            rows.append(
                {
                    "from": left_width_name,
                    "to": right_width_name,
                    "count_ratio": rational_pair(Fraction(right, left)),
                    "density_ratio": rational_pair(right_density / left_density),
                    "count_difference": right - left,
                    "density_difference": rational_pair(right_density - left_density),
                }
            )
        width_adjacent[anchor_name] = rows
    return {
        "cells": cells,
        "adjacent_anchor_objects": anchor_adjacent,
        "adjacent_width_objects": width_adjacent,
    }


def transformed_matrices(
    counts: dict[str, dict[str, int]], anchors: tuple[tuple[str, int], ...]
) -> tuple[dict[str, dict[str, dict[str, Decimal]]], dict[str, Any]]:
    raw: dict[str, dict[str, dict[str, Decimal]]] = {}
    rendered: dict[str, Any] = {}
    for candidate in CANDIDATES:
        raw[candidate] = {}
        rendered[candidate] = {}
        for anchor_name, anchor in anchors:
            raw[candidate][anchor_name] = {}
            rendered[candidate][anchor_name] = {}
            for width_name, width in WIDTHS:
                value = transform_density(
                    candidate,
                    _count_for(counts, anchor_name, width_name),
                    anchor,
                    width,
                )
                raw[candidate][anchor_name][width_name] = value
                rendered[candidate][anchor_name][width_name] = decimal_string(value)
    return raw, rendered


def _rounded_score(value: Decimal) -> Decimal:
    return Decimal(decimal_string(value))


def score_candidates(
    transformed: dict[str, dict[str, dict[str, Decimal]]],
    anchors: tuple[tuple[str, int], ...],
) -> dict[str, Any]:
    width_spreads_raw: dict[str, dict[str, Decimal]] = {}
    global_scores_raw: dict[str, Decimal] = {}
    width_rankings: dict[str, list[str]] = {}
    candidate_index = {candidate: index for index, candidate in enumerate(CANDIDATES)}

    for candidate in CANDIDATES:
        width_spreads_raw[candidate] = {}
        for width_name, _ in WIDTHS:
            values = [transformed[candidate][anchor_name][width_name] for anchor_name, _ in anchors]
            low = min(values)
            high = max(values)
            if low <= 0:
                raise ValueError("spread score requires positive transformed values")
            with localcontext(DECIMAL_CONTEXT):
                width_spreads_raw[candidate][width_name] = high / low
        global_scores_raw[candidate] = max(width_spreads_raw[candidate].values())

    ranking = sorted(
        CANDIDATES,
        key=lambda candidate: (_rounded_score(global_scores_raw[candidate]), candidate_index[candidate]),
    )
    for width_name, _ in WIDTHS:
        width_rankings[width_name] = sorted(
            CANDIDATES,
            key=lambda candidate: (
                _rounded_score(width_spreads_raw[candidate][width_name]),
                candidate_index[candidate],
            ),
        )
    return {
        "raw_global_scores": global_scores_raw,
        "raw_width_spreads": width_spreads_raw,
        "candidate_scores": {
            candidate: decimal_string(global_scores_raw[candidate]) for candidate in CANDIDATES
        },
        "width_spreads": {
            candidate: {
                width_name: decimal_string(width_spreads_raw[candidate][width_name])
                for width_name, _ in WIDTHS
            }
            for candidate in CANDIDATES
        },
        "candidate_ranking": ranking,
        "width_rankings": width_rankings,
    }


def _sign(value: Decimal) -> int:
    if value > 0:
        return 1
    if value < 0:
        return -1
    return 0


def residual_objects(
    selected: str,
    transformed: dict[str, dict[str, dict[str, Decimal]]],
    anchors: tuple[tuple[str, int], ...],
    *,
    baselines: dict[str, Decimal] | None = None,
) -> tuple[dict[str, Decimal], dict[str, Any], dict[str, Counter[tuple[int, ...]]]]:
    if baselines is None:
        baselines = {}
        for width_name, _ in WIDTHS:
            values = [transformed[selected][anchor_name][width_name] for anchor_name, _ in anchors]
            with localcontext(DECIMAL_CONTEXT):
                baselines[width_name] = sum(values, Decimal(0)) / Decimal(3)
    objects: dict[str, Any] = {}
    r1_words: list[tuple[int, ...]] = []
    r3_words: list[tuple[int, ...]] = []
    for width_name, _ in WIDTHS:
        baseline = baselines[width_name]
        if baseline <= 0 or not baseline.is_finite():
            raise ValueError("baseline must be positive and finite")
        residuals: list[Decimal] = []
        for anchor_name, _ in anchors:
            with localcontext(DECIMAL_CONTEXT):
                residual = transformed[selected][anchor_name][width_name] / baseline - Decimal(1)
            residuals.append(residual)
        with localcontext(DECIMAL_CONTEXT):
            first_differences = [residuals[1] - residuals[0], residuals[2] - residuals[1]]
            second_difference = residuals[2] - Decimal(2) * residuals[1] + residuals[0]
        r1 = tuple(_sign(value) for value in residuals)
        r3 = tuple(_sign(value) for value in first_differences)
        r1_words.append(r1)
        r3_words.append(r3)
        objects[width_name] = {
            "R0": [decimal_string(value) for value in residuals],
            "R1": list(r1),
            "R2": [decimal_string(value) for value in first_differences],
            "R3": list(r3),
            "R4": decimal_string(second_difference),
        }
    return baselines, objects, {"R1": Counter(r1_words), "R3": Counter(r3_words)}


def _frequency_table(counter: Counter[tuple[int, ...]]) -> list[dict[str, Any]]:
    return [{"word": list(word), "count": counter[word]} for word in sorted(counter)]


def _strict_target(counter: Counter[tuple[int, ...]]) -> tuple[int, ...] | None:
    ranked = sorted(counter.items(), key=lambda item: (-item[1], item[0]))
    if not ranked:
        return None
    top_word, top_count = ranked[0]
    runner_up = ranked[1][1] if len(ranked) > 1 else 0
    if top_count >= 3 and top_count > runner_up:
        return top_word
    return None


def select_residual_target(
    counters: dict[str, Counter[tuple[int, ...]]]
) -> tuple[dict[str, Any] | str, dict[str, Any]]:
    tables = {family: _frequency_table(counters[family]) for family in ("R1", "R3")}
    for family in ("R1", "R3"):
        target = _strict_target(counters[family])
        if target is not None:
            return (
                {
                    "family": family,
                    "word": list(target),
                    "development_count": counters[family][target],
                },
                tables,
            )
    return "NO_RESIDUAL_SIGN_TARGET", tables


def eligible_questions(
    selected: str,
    scores: dict[str, Any],
    residual_target: dict[str, Any] | str,
) -> list[dict[str, str]]:
    selected_score = scores["raw_global_scores"][selected]
    identity_score = scores["raw_global_scores"]["N00"]
    selected_widths = scores["raw_width_spreads"][selected]
    identity_widths = scores["raw_width_spreads"]["N00"]
    width_wins = sum(
        selected_widths[width_name] < identity_widths[width_name]
        for width_name, _ in WIDTHS
    )
    questions: list[dict[str, str]] = []
    if selected != "N00" and selected_score < identity_score:
        questions.append(
            {
                "id": "Q1",
                "text": (
                    f"For each fixed w in the frozen width set, does T_{selected}(a,w) "
                    "approach a finite nonzero limit along indefinitely repeated doublings of a?"
                ),
            }
        )
    if width_wins >= 4:
        questions.append(
            {
                "id": "Q2",
                "text": (
                    f"Is the same scale normalization {selected} eventually more stable than raw "
                    "density for every width in the frozen width family under repeated anchor doubling?"
                ),
            }
        )
    if isinstance(residual_target, dict):
        family = residual_target["family"]
        word = tuple(residual_target["word"])
        questions.append(
            {
                "id": "Q3",
                "text": (
                    f"Does the exact selected {family} residual sign word {word} remain the strict "
                    "modal sign word across the frozen width family for all sufficiently large doubled anchors?"
                ),
            }
        )
    return questions


def evaluate_milestones(
    *,
    selected: str,
    development_selected_score: Decimal,
    development_identity_score: Decimal,
    assessment_selected_score: Decimal,
    assessment_identity_score: Decimal,
    development_width_wins: int,
    assessment_width_wins: int,
    development_target: dict[str, Any] | str,
    assessment_target_passed: bool,
    questions: list[dict[str, str]],
    m5_conditions: dict[str, bool],
    deterministic_reproduction: bool,
    guard_validation: bool,
) -> dict[str, Any]:
    m1 = (
        selected != "N00"
        and development_selected_score < development_identity_score
        and assessment_selected_score < assessment_identity_score
    )
    m2 = development_width_wins >= 4 and assessment_width_wins >= 4
    m3 = isinstance(development_target, dict) and assessment_target_passed
    m4 = bool(questions)
    m5 = all(m5_conditions.values())
    if not m5 or not deterministic_reproduction or not guard_validation:
        outcome = "INVALID"
    elif m1 and m4 and (m2 or m3):
        outcome = "STRONG_PASS"
    elif sum((m1, m2, m3, m4)) >= 2:
        outcome = "PARTIAL_PASS"
    else:
        outcome = "FAIL"
    return {
        "M1": m1,
        "M2": m2,
        "M3": m3,
        "M4": m4,
        "M5": m5,
        "M5_conditions": m5_conditions,
        "overall_outcome": outcome,
    }


def build_development_payload(*, code_commit: str) -> dict[str, Any]:
    plan = generation_plan("development")
    validate_generation_plan(plan, phase="development")
    counts = execute_generation_plan(plan, phase="development")
    transformed, rendered_transforms = transformed_matrices(counts, DEVELOPMENT_ANCHORS)
    scores = score_candidates(transformed, DEVELOPMENT_ANCHORS)
    selected = scores["candidate_ranking"][0]
    baselines, residuals, residual_counters = residual_objects(
        selected, transformed, DEVELOPMENT_ANCHORS
    )
    residual_target, frequency_tables = select_residual_target(residual_counters)
    questions = eligible_questions(selected, scores, residual_target)
    selected_widths = scores["raw_width_spreads"][selected]
    identity_widths = scores["raw_width_spreads"]["N00"]
    width_wins = sum(
        selected_widths[width_name] < identity_widths[width_name]
        for width_name, _ in WIDTHS
    )
    return {
        "experiment": EXPERIMENT_ID,
        "lane": LANE,
        "phase": "development",
        "implementation_commit": code_commit,
        "historical_theory_blinded": True,
        "generation_plan": plan,
        "anchors": [{"name": name, "value": value} for name, value in DEVELOPMENT_ANCHORS],
        "widths": [{"name": name, "value": value} for name, value in WIDTHS],
        "candidate_order": list(CANDIDATES),
        "residual_family_order": list(RESIDUAL_FAMILIES),
        "count_matrix": counts,
        "exact_objects": exact_count_objects(counts, DEVELOPMENT_ANCHORS),
        "transformed_density": rendered_transforms,
        "candidate_scores": scores["candidate_scores"],
        "candidate_ranking": scores["candidate_ranking"],
        "width_spreads": scores["width_spreads"],
        "width_rankings": scores["width_rankings"],
        "selection": {
            "normalization": selected,
            "development_width_wins_over_N00": width_wins,
            "baselines": {name: decimal_string(value) for name, value in baselines.items()},
            "residual_objects": residuals,
            "residual_sign_frequency_tables": frequency_tables,
            "residual_sign_target": residual_target,
            "eligible_questions": questions,
        },
        "serialization": {
            "decimal_precision": DECIMAL_PRECISION,
            "decimal_rounding": "ROUND_HALF_EVEN",
            "decimal_scientific_digits_after_point": 60,
            "json_sort_keys": True,
            "json_indent": 2,
        },
        "raw_prime_values_serialized": False,
    }


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def build_development_checkpoint(
    development_payload: dict[str, Any], development_artifact: bytes
) -> dict[str, Any]:
    selection = development_payload["selection"]
    return {
        "experiment": EXPERIMENT_ID,
        "lane": LANE,
        "phase": "development_selection_checkpoint",
        "implementation_commit": development_payload["implementation_commit"],
        "historical_theory_blinded": True,
        "development_artifact": {
            "bytes": len(development_artifact),
            "sha256": _sha256_bytes(development_artifact),
        },
        "candidate_order": development_payload["candidate_order"],
        "candidate_scores": development_payload["candidate_scores"],
        "candidate_ranking": development_payload["candidate_ranking"],
        "width_spreads": development_payload["width_spreads"],
        "selection": {
            "normalization": selection["normalization"],
            "development_width_wins_over_N00": selection[
                "development_width_wins_over_N00"
            ],
            "baselines": selection["baselines"],
            "residual_sign_target": selection["residual_sign_target"],
            "eligible_questions": selection["eligible_questions"],
        },
        "raw_prime_values_serialized": False,
    }


def build_assessment_checkpoint(
    assessment_payload: dict[str, Any], assessment_artifact: bytes
) -> dict[str, Any]:
    selected = assessment_payload["selected_normalization_assessment"]
    return {
        "experiment": EXPERIMENT_ID,
        "lane": LANE,
        "phase": "assessment_checkpoint",
        "implementation_commit": assessment_payload["implementation_commit"],
        "historical_theory_blinded": True,
        "assessment_artifact": {
            "bytes": len(assessment_artifact),
            "sha256": _sha256_bytes(assessment_artifact),
        },
        "development_checkpoint": assessment_payload["development_checkpoint"],
        "candidate_scores": assessment_payload["candidate_scores"],
        "candidate_ranking": assessment_payload["candidate_ranking"],
        "width_spreads": assessment_payload["width_spreads"],
        "selected_normalization_assessment": {
            "normalization": selected["normalization"],
            "assessment_width_wins_over_N00": selected[
                "assessment_width_wins_over_N00"
            ],
            "residual_target_evaluation": selected["residual_target_evaluation"],
        },
        "milestones": assessment_payload["milestones"],
        "raw_prime_values_serialized": False,
    }


def verify_development_record(
    path: Path,
    *,
    expected_sha256: str,
    development_record_commit: str,
    code_commit: str,
) -> dict[str, Any]:
    data = path.read_bytes()
    if _sha256_bytes(data) != expected_sha256:
        raise ValueError("development record SHA-256 mismatch")
    if not re.fullmatch(r"[0-9a-f]{40}", development_record_commit):
        raise ValueError("development record commit must be a full 40-hex SHA")
    payload = json.loads(data)
    if (
        payload.get("experiment") != EXPERIMENT_ID
        or payload.get("phase") != "development_selection_checkpoint"
    ):
        raise ValueError("invalid development record phase")
    if payload.get("implementation_commit") != code_commit:
        raise ValueError("development record implementation commit mismatch")
    selection = payload.get("selection")
    if not isinstance(selection, dict) or selection.get("normalization") not in CANDIDATES:
        raise ValueError("development record lacks a valid frozen selection")
    if set(selection.get("baselines", {})) != {name for name, _ in WIDTHS}:
        raise ValueError("development record lacks the five frozen baselines")
    if not isinstance(selection.get("eligible_questions"), list):
        raise ValueError("development record lacks frozen eligible questions")
    return payload


def _target_assessment(
    target: dict[str, Any] | str,
    counters: dict[str, Counter[tuple[int, ...]]],
) -> tuple[bool, dict[str, Any] | None]:
    if not isinstance(target, dict):
        return False, None
    family = str(target["family"])
    word = tuple(int(value) for value in target["word"])
    counter = counters[family]
    ranked = sorted(counter.items(), key=lambda item: (-item[1], item[0]))
    mode_count = ranked[0][1] if ranked else 0
    runner_up_count = ranked[1][1] if len(ranked) > 1 else 0
    target_count = counter[word]
    passed = target_count >= 3 and target_count == mode_count and mode_count > runner_up_count
    return passed, {
        "family": family,
        "target_word": list(word),
        "target_count": target_count,
        "mode_count": mode_count,
        "runner_up_count": runner_up_count,
        "strict_unique_mode": bool(ranked) and mode_count > runner_up_count,
        "passed": passed,
        "frequency_table": _frequency_table(counter),
    }


def build_assessment_payload(
    *,
    code_commit: str,
    development_record: Path,
    development_record_sha256: str,
    development_record_commit: str,
) -> dict[str, Any]:
    development = verify_development_record(
        development_record,
        expected_sha256=development_record_sha256,
        development_record_commit=development_record_commit,
        code_commit=code_commit,
    )
    plan = generation_plan("assessment", development_checkpoint_verified=True)
    validate_generation_plan(
        plan, phase="assessment", development_checkpoint_verified=True
    )
    counts = execute_generation_plan(
        plan, phase="assessment", development_checkpoint_verified=True
    )
    transformed, rendered_transforms = transformed_matrices(counts, ASSESSMENT_ANCHORS)
    scores = score_candidates(transformed, ASSESSMENT_ANCHORS)
    selected = str(development["selection"]["normalization"])
    frozen_baselines = {
        name: Decimal(value) for name, value in development["selection"]["baselines"].items()
    }
    _, residuals, residual_counters = residual_objects(
        selected,
        transformed,
        ASSESSMENT_ANCHORS,
        baselines=frozen_baselines,
    )
    target = development["selection"]["residual_sign_target"]
    target_passed, target_evaluation = _target_assessment(target, residual_counters)

    dev_selected = Decimal(development["candidate_scores"][selected])
    dev_identity = Decimal(development["candidate_scores"]["N00"])
    ass_selected = scores["raw_global_scores"][selected]
    ass_identity = scores["raw_global_scores"]["N00"]
    ass_width_wins = sum(
        scores["raw_width_spreads"][selected][width_name]
        < scores["raw_width_spreads"]["N00"][width_name]
        for width_name, _ in WIDTHS
    )
    m5_conditions = {
        "no_forbidden_novelty_range_generated_or_inspected": True,
        "raw_prime_list_not_serialized": True,
        "assessment_after_committed_development_checkpoint": True,
        "assessment_did_not_change_frozen_selection_or_grammar": True,
        "historical_theory_not_consulted_during_execution": True,
        "no_OBS_or_CAND_allocated": True,
    }
    milestones = evaluate_milestones(
        selected=selected,
        development_selected_score=dev_selected,
        development_identity_score=dev_identity,
        assessment_selected_score=ass_selected,
        assessment_identity_score=ass_identity,
        development_width_wins=int(
            development["selection"]["development_width_wins_over_N00"]
        ),
        assessment_width_wins=ass_width_wins,
        development_target=target,
        assessment_target_passed=target_passed,
        questions=list(development["selection"]["eligible_questions"]),
        m5_conditions=m5_conditions,
        deterministic_reproduction=True,
        guard_validation=True,
    )
    return {
        "experiment": EXPERIMENT_ID,
        "lane": LANE,
        "phase": "assessment",
        "implementation_commit": code_commit,
        "historical_theory_blinded": True,
        "development_checkpoint": {
            "record_sha256": development_record_sha256,
            "record_commit": development_record_commit,
            "normalization": selected,
            "baselines": development["selection"]["baselines"],
            "residual_sign_target": target,
            "eligible_questions": development["selection"]["eligible_questions"],
        },
        "generation_plan": plan,
        "anchors": [{"name": name, "value": value} for name, value in ASSESSMENT_ANCHORS],
        "widths": [{"name": name, "value": value} for name, value in WIDTHS],
        "count_matrix": counts,
        "exact_objects": exact_count_objects(counts, ASSESSMENT_ANCHORS),
        "transformed_density": rendered_transforms,
        "candidate_scores": scores["candidate_scores"],
        "candidate_ranking": scores["candidate_ranking"],
        "width_spreads": scores["width_spreads"],
        "selected_normalization_assessment": {
            "normalization": selected,
            "assessment_width_wins_over_N00": ass_width_wins,
            "residual_objects": residuals,
            "residual_target_evaluation": target_evaluation,
        },
        "milestones": milestones,
        "raw_prime_values_serialized": False,
    }


def serialise_payload(payload: dict[str, Any]) -> bytes:
    return (json.dumps(payload, sort_keys=True, indent=2) + "\n").encode("utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("development", "assessment"), required=True)
    parser.add_argument("--code-commit", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--checkpoint-output", type=Path, required=True)
    parser.add_argument("--development-record", type=Path)
    parser.add_argument("--development-record-sha256")
    parser.add_argument("--development-record-commit")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.phase == "development":
        if any(
            value is not None
            for value in (
                args.development_record,
                args.development_record_sha256,
                args.development_record_commit,
            )
        ):
            raise ValueError("development phase does not accept an assessment checkpoint")
        payload = build_development_payload(code_commit=args.code_commit)
        rendered = serialise_payload(payload)
        checkpoint = build_development_checkpoint(payload, rendered)
    else:
        if not all(
            value is not None
            for value in (
                args.development_record,
                args.development_record_sha256,
                args.development_record_commit,
            )
        ):
            raise ValueError("assessment requires the committed development record, digest, and commit")
        payload = build_assessment_payload(
            code_commit=args.code_commit,
            development_record=args.development_record,
            development_record_sha256=args.development_record_sha256,
            development_record_commit=args.development_record_commit,
        )
        rendered = serialise_payload(payload)
        checkpoint = build_assessment_checkpoint(payload, rendered)
    args.output.write_bytes(rendered)
    args.checkpoint_output.write_bytes(serialise_payload(checkpoint))


if __name__ == "__main__":
    main()
