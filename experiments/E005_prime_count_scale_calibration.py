#!/usr/bin/env python3
"""E005: frozen prime-count scale calibration evaluator."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from decimal import Context, Decimal, ROUND_HALF_EVEN, localcontext
from fractions import Fraction
from math import isqrt
from pathlib import Path
from typing import Any, Iterable

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
