#!/usr/bin/env python3
"""E011: frozen finite-field polynomial factor-degree shape discovery evaluator."""
from __future__ import annotations

import argparse
import ctypes
import fcntl
import hashlib
import json
import subprocess
import tempfile
from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from math import isqrt
from pathlib import Path
from typing import Any, TypeAlias

from primes_lab.core import sieve

EXPERIMENT_ID = "E011"
WIDTH = 1_000_000
Q = 210
DEGREE = 5
POLYNOMIAL = (1, 1, 0, 0, 0, 1)
DISCRIMINANT = 3381
DISCRIMINANT_FACTORIZATION = (3, 7, 7, 23)
POPULATION_FLOOR = 1000
OCCURRENCE_FLOOR = 32
MIXED_RESIDUE_FLOOR = 8
PROMOTION_CAP = 4
LOW_SUPPORT_STOP = 100_000
FAMILY_ORDER = ("K1", "K2", "K3", "K4")
BANDS = {
    "D11": (62_000_000, 63_000_000),
    "H11": (64_000_000, 65_000_000),
    "A11": (124_000_000, 125_000_000),
}
FROZEN_PARTITION = (
    ("G11-pre", "guard", (61_000_000, 62_000_000)),
    ("D11", "discovery", BANDS["D11"]),
    ("G11-mid", "guard", (63_000_000, 64_000_000)),
    ("H11", "holdout", BANDS["H11"]),
    ("A11", "adversarial", BANDS["A11"]),
)
HISTORICAL_RANGES = {
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
    "D9": (54_000_000, 55_000_000),
    "G9-mid": (55_000_000, 56_000_000),
    "H9": (56_000_000, 57_000_000),
    "G10-pre": (57_000_000, 58_000_000),
    "D10": (58_000_000, 59_000_000),
    "G10-mid": (59_000_000, 60_000_000),
    "H10": (60_000_000, 61_000_000),
    "A8": (66_000_000, 67_000_000),
    "A3": (70_000_000, 71_000_000),
    "A4": (78_000_000, 79_000_000),
    "A6": (84_000_000, 85_000_000),
    "A7": (92_000_000, 93_000_000),
    "A9": (108_000_000, 109_000_000),
    "A10": (116_000_000, 117_000_000),
}
E005_CALIBRATION_RANGES = tuple(
    (start, start + 1_048_576)
    for start in (
        128_000_000,
        256_000_000,
        512_000_000,
        1_024_000_000,
        2_048_000_000,
        4_096_000_000,
    )
)
ALLOWED_K1 = {
    (5,),
    (4, 1),
    (3, 2),
    (3, 1, 1),
    (2, 2, 1),
    (2, 1, 1, 1),
    (1, 1, 1, 1, 1),
}
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
ANCHOR_SUMMARY_KEYS = frozenset({"prime_count", "first_prime", "last_prime"})
VALIDATION_KEYS = frozenset(
    {
        "polynomial_metadata_or_discriminant_failure_count",
        "finite_field_squarefree_failure_count",
        "gcd_degree_range_failure_count",
        "factor_count_integrality_or_nonnegativity_failure_count",
        "divisor_sum_reconstruction_failure_count",
        "total_degree_or_partition_failure_count",
        "family_frequency_total_failure_count",
    }
)
FAMILY_ROW_KEYS = frozenset(
    {
        "family",
        "prime_mode_count",
        "maximizer_count",
        "highest_competing_count",
        "strict_unique_prime_mode",
        "unique_mode_signature",
        "population_floor_passed",
        "occurrence_floor_passed",
        "unique_mode_mixed_residue_count",
        "residue_control_passed",
        "mechanically_eligible",
    }
)
PROMOTION_KEYS = frozenset(
    {"family", "target_signature", "target_prime_count", "target_mixed_residue_count"}
)

K1Signature: TypeAlias = tuple[int, ...]
Signature: TypeAlias = K1Signature | int

_NATIVE_LIBRARY: ctypes.CDLL | None = None


def _intersects(left: tuple[int, int], right: tuple[int, int]) -> bool:
    return max(left[0], right[0]) < min(left[1], right[1])


def validate_frozen_metadata() -> None:
    if WIDTH != 1_000_000 or Q != 2 * 3 * 5 * 7 or Q != 210:
        raise ValueError("frozen E011 width/Q changed")
    partition_counts = {2: 2, 3: 3, 4: 5, 5: 7}
    chosen = min(n for n in range(2, 6) if partition_counts[n] >= 7)
    if partition_counts != {2: 2, 3: 3, 4: 5, 5: 7} or chosen != DEGREE or DEGREE != 5:
        raise ValueError("frozen E011 degree-selection metadata changed")
    if POLYNOMIAL != (1, 1, 0, 0, 0, 1):
        raise ValueError("frozen E011 polynomial coefficients changed")
    if DISCRIMINANT != 3381 or 3 * 7 * 7 * 23 != DISCRIMINANT:
        raise ValueError("frozen E011 discriminant metadata changed")
    expected = {
        "G11-pre": (61_000_000, 62_000_000),
        "D11": (62_000_000, 63_000_000),
        "G11-mid": (63_000_000, 64_000_000),
        "H11": (64_000_000, 65_000_000),
        "A11": (124_000_000, 125_000_000),
    }
    rows = {name: interval for name, _, interval in FROZEN_PARTITION}
    if rows != expected or BANDS != {name: expected[name] for name in ("D11", "H11", "A11")}:
        raise ValueError("frozen E011 partition changed")
    if any(hi - lo != WIDTH for lo, hi in rows.values()):
        raise ValueError("frozen E011 width arithmetic changed")
    intervals = list(rows.values())
    if any(
        _intersects(left, right)
        for i, left in enumerate(intervals)
        for right in intervals[i + 1 :]
    ):
        raise ValueError("frozen E011 partition overlaps")
    for interval in intervals:
        if any(_intersects(interval, prior) for prior in HISTORICAL_RANGES.values()):
            raise ValueError("E011 partition intersects historical novelty range")
        if any(_intersects(interval, prior) for prior in E005_CALIBRATION_RANGES):
            raise ValueError("E011 partition intersects E005 calibration range")
    if expected["A11"][0] != 2 * expected["D11"][0]:
        raise ValueError("frozen E011 adversarial arithmetic changed")
    if POPULATION_FLOOR != 1000 or POPULATION_FLOOR != WIDTH // 1000:
        raise ValueError("frozen E011 population floor changed")
    if OCCURRENCE_FLOOR != 32 or 31**2 >= POPULATION_FLOOR or 32**2 < POPULATION_FLOOR:
        raise ValueError("frozen E011 occurrence floor changed")
    if MIXED_RESIDUE_FLOOR != 8:
        raise ValueError("frozen E011 mixed-residue floor changed")
    if FAMILY_ORDER != ("K1", "K2", "K3", "K4") or PROMOTION_CAP != 4:
        raise ValueError("frozen E011 family order/cap changed")


def generation_plan(band_name: str) -> list[dict[str, Any]]:
    if band_name not in BANDS:
        raise ValueError(f"unknown frozen E011 band: {band_name}")
    start, stop = BANDS[band_name]
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
    """D1-33 fail-closed gate; must run before either prime generator."""
    validate_frozen_metadata()
    if band_name != "D11":
        raise ValueError("D1-33 authorizes D11 generation only")
    canonical = generation_plan("D11")
    if plan != canonical:
        raise ValueError("D1-33 plan must equal exact canonical D11 plan")
    if canonical != [
        {
            "purpose": "base_sieve_support",
            "strategy": "whole_prefix",
            "start": 0,
            "stop": 7938,
        },
        {
            "purpose": "segmented_target",
            "strategy": "segmented",
            "start": 62_000_000,
            "stop": 63_000_000,
        },
    ]:
        raise ValueError("canonical D11 generation arithmetic changed")
    if canonical[0]["stop"] > LOW_SUPPORT_STOP:
        raise ValueError("whole-prefix generation above 100,000 is forbidden")
    target = BANDS["D11"]
    if any(_intersects(target, prior) for prior in HISTORICAL_RANGES.values()):
        raise ValueError("D11 intersects historical novelty range")
    if any(_intersects(target, prior) for prior in E005_CALIBRATION_RANGES):
        raise ValueError("D11 intersects E005 calibration range")
    if any(
        name != "D11" and _intersects(target, interval)
        for name, _, interval in FROZEN_PARTITION
    ):
        raise ValueError("D11 intersects E011 non-target range")


def _segmented_target_prime_flags(
    start: int, stop: int, base_primes: Sequence[int]
) -> bytearray:
    flags = bytearray(b"\x01") * (stop - start)
    for prime in base_primes:
        first = max(prime * prime, ((start + prime - 1) // prime) * prime)
        if first >= stop:
            continue
        count = ((stop - 1 - first) // prime) + 1
        flags[first - start : stop - start : prime] = b"\x00" * count
    return flags


def execute_generation_plan(
    plan: list[dict[str, Any]], *, band_name: str
) -> tuple[list[int], list[int]]:
    validate_generation_plan(plan, band_name=band_name)
    base_primes = sieve(int(plan[0]["stop"]) - 1)
    start, stop = int(plan[1]["start"]), int(plan[1]["stop"])
    flags = _segmented_target_prime_flags(start, stop, base_primes)
    primes = [start + i for i, flag in enumerate(flags) if flag]
    return base_primes, primes


def poly_normalize(poly: Iterable[int], p: int) -> tuple[int, ...]:
    if p < 2:
        raise ValueError("field modulus must be at least 2")
    values = [int(value) % p for value in poly]
    while values and values[-1] == 0:
        values.pop()
    return tuple(values)


def poly_add(left: Sequence[int], right: Sequence[int], p: int) -> tuple[int, ...]:
    n = max(len(left), len(right))
    return poly_normalize(
        [
            (left[i] if i < len(left) else 0) + (right[i] if i < len(right) else 0)
            for i in range(n)
        ],
        p,
    )


def poly_sub(left: Sequence[int], right: Sequence[int], p: int) -> tuple[int, ...]:
    n = max(len(left), len(right))
    return poly_normalize(
        [
            (left[i] if i < len(left) else 0) - (right[i] if i < len(right) else 0)
            for i in range(n)
        ],
        p,
    )


def poly_mul(left: Sequence[int], right: Sequence[int], p: int) -> tuple[int, ...]:
    if not left or not right:
        return ()
    out = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            out[i + j] = (out[i + j] + a * b) % p
    return poly_normalize(out, p)


def poly_divmod(
    numerator: Sequence[int], denominator: Sequence[int], p: int
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    num = list(poly_normalize(numerator, p))
    den = poly_normalize(denominator, p)
    if not den:
        raise ZeroDivisionError("polynomial division by zero")
    if len(num) < len(den):
        return (), tuple(num)
    quotient = [0] * (len(num) - len(den) + 1)
    inv_lead = pow(den[-1], p - 2, p)
    while num and len(num) >= len(den):
        shift = len(num) - len(den)
        coeff = num[-1] * inv_lead % p
        quotient[shift] = coeff
        for i, value in enumerate(den):
            num[shift + i] = (num[shift + i] - coeff * value) % p
        while num and num[-1] == 0:
            num.pop()
    return poly_normalize(quotient, p), poly_normalize(num, p)


def poly_monic(poly: Sequence[int], p: int) -> tuple[int, ...]:
    value = poly_normalize(poly, p)
    if not value:
        return ()
    inv = pow(value[-1], p - 2, p)
    return poly_normalize((coefficient * inv for coefficient in value), p)


def poly_gcd(left: Sequence[int], right: Sequence[int], p: int) -> tuple[int, ...]:
    a, b = poly_normalize(left, p), poly_normalize(right, p)
    while b:
        _, remainder = poly_divmod(a, b, p)
        a, b = b, remainder
    return poly_monic(a, p)


def poly_mod(poly: Sequence[int], modulus: Sequence[int], p: int) -> tuple[int, ...]:
    return poly_divmod(poly, modulus, p)[1]


def poly_pow_mod(
    base: Sequence[int], exponent: int, modulus: Sequence[int], p: int
) -> tuple[int, ...]:
    if exponent < 0:
        raise ValueError("polynomial exponent must be nonnegative")
    result: tuple[int, ...] = (1,)
    factor = poly_mod(base, modulus, p)
    power = exponent
    while power:
        if power & 1:
            result = poly_mod(poly_mul(result, factor, p), modulus, p)
        power >>= 1
        if power:
            factor = poly_mod(poly_mul(factor, factor, p), modulus, p)
    return result


def factor_counts_reference(p: int) -> tuple[int, int, int, int, int]:
    """Direct exact Python reference for the frozen s_k/c_d semantics."""
    f = poly_normalize(POLYNOMIAL, p)
    derivative = poly_normalize((1, 0, 0, 0, 5), p)
    if poly_gcd(f, derivative, p) != (1,):
        raise ValueError("finite-field polynomial is not squarefree")
    x = (0, 1)
    r = x
    s: list[int] = []
    for _ in range(5):
        r = poly_pow_mod(r, p, f, p)
        g = poly_gcd(f, poly_sub(r, x, p), p)
        degree = len(g) - 1 if g else -1
        if not 0 <= degree <= 5:
            raise ValueError("gcd degree outside frozen range")
        s.append(degree)
    counts: list[int] = []
    c1 = s[0]
    if c1 < 0:
        raise ValueError("factor count is negative")
    counts.append(c1)
    n2 = s[1] - c1
    if n2 < 0 or n2 % 2:
        raise ValueError("factor-count recursion is not integral/nonnegative")
    c2 = n2 // 2
    counts.append(c2)
    n3 = s[2] - c1
    if n3 < 0 or n3 % 3:
        raise ValueError("factor-count recursion is not integral/nonnegative")
    c3 = n3 // 3
    counts.append(c3)
    n4 = s[3] - c1 - 2 * c2
    if n4 < 0 or n4 % 4:
        raise ValueError("factor-count recursion is not integral/nonnegative")
    c4 = n4 // 4
    counts.append(c4)
    n5 = s[4] - c1
    if n5 < 0 or n5 % 5:
        raise ValueError("factor-count recursion is not integral/nonnegative")
    c5 = n5 // 5
    counts.append(c5)
    reconstructed = [
        c1,
        c1 + 2 * c2,
        c1 + 3 * c3,
        c1 + 2 * c2 + 4 * c4,
        c1 + 5 * c5,
    ]
    if reconstructed != s:
        raise ValueError("divisor-sum reconstruction failed")
    if c1 + 2 * c2 + 3 * c3 + 4 * c4 + 5 * c5 != 5:
        raise ValueError("total factor degree is not 5")
    signature = tuple(
        degree for degree, count in reversed(tuple(enumerate(counts, start=1))) for _ in range(count)
    )
    if signature not in ALLOWED_K1:
        raise ValueError("factor-degree partition escaped frozen grammar")
    return tuple(counts)  # type: ignore[return-value]


def signatures_from_counts(counts: Sequence[int]) -> dict[str, Signature]:
    if len(counts) != 5 or any(not isinstance(value, int) or value < 0 for value in counts):
        raise ValueError("c_d counts must be five nonnegative integers")
    partition = tuple(
        degree
        for degree in range(5, 0, -1)
        for _ in range(int(counts[degree - 1]))
    )
    if partition not in ALLOWED_K1 or sum(partition) != 5:
        raise ValueError("K1 partition escaped frozen degree-5 grammar")
    k2 = sum(int(value) for value in counts)
    k3 = int(counts[0])
    k4 = max(degree for degree in range(1, 6) if int(counts[degree - 1]) > 0)
    return {"K1": partition, "K2": k2, "K3": k3, "K4": k4}


def _native_library() -> ctypes.CDLL:
    global _NATIVE_LIBRARY
    if _NATIVE_LIBRARY is not None:
        return _NATIVE_LIBRARY
    source = Path(__file__).with_name("e011_ff_runtime.c")
    source_bytes = source.read_bytes()
    digest = hashlib.sha256(source_bytes).hexdigest()[:20]
    output = Path(tempfile.gettempdir()) / f"primes-e011-{digest}.so"
    lock_path = output.with_suffix(".lock")
    with lock_path.open("w") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        if not output.exists():
            temp_output = output.with_suffix(".tmp.so")
            subprocess.run(
                ["cc", "-O3", "-std=c11", "-shared", "-fPIC", str(source), "-o", str(temp_output)],
                check=True,
                capture_output=True,
            )
            temp_output.replace(output)
    library = ctypes.CDLL(str(output))
    function = library.e011_factor_counts
    function.argtypes = [ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint32)]
    function.restype = ctypes.c_int
    _NATIVE_LIBRARY = library
    return library


def factor_counts(p: int) -> tuple[int, int, int, int, int]:
    if p < 2:
        raise ValueError("prime anchor must be at least 2")
    output = (ctypes.c_uint32 * 5)()
    result = _native_library().e011_factor_counts(ctypes.c_uint64(p), output)
    if result == 1:
        raise ValueError("native finite-field squarefree validation failed")
    if result == 2:
        raise ValueError("native gcd degree range validation failed")
    if result == 3:
        raise ValueError("native factor-count integrality/nonnegativity failed")
    if result == 4:
        raise ValueError("native divisor-sum reconstruction failed")
    if result == 5:
        raise ValueError("native total-degree/partition validation failed")
    if result != 0:
        raise ValueError(f"native E011 runtime failure: {result}")
    counts = tuple(int(output[i]) for i in range(5))
    signatures_from_counts(counts)
    return counts  # type: ignore[return-value]


def signature_sort_key(family: str, signature: Signature) -> Any:
    if family == "K1" and isinstance(signature, tuple):
        return signature
