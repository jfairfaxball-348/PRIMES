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
H11_TARGETS = (
    ("OBS-015", "K1", (2, 1, 1, 1)),
    ("OBS-016", "K2", 3),
    ("OBS-017", "K4", 2),
)
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
H11_PAYLOAD_KEYS = frozenset(
    {"experiment", "implementation_commit", "band", "generation_plan", "validation", "criteria"}
)
H11_CRITERION_KEYS = frozenset(
    {
        "target_signature",
        "target_count",
        "highest_competing_count",
        "mixed_residue_count",
        "prime_population",
        "population_floor_passed",
        "occurrence_floor_passed",
        "strict_unique_mode_passed",
        "mixed_residue_floor_passed",
        "validation_passed",
        "replication_passed",
    }
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
    """D1-34 fail-closed H11 gate; must run before either prime generator."""
    validate_frozen_metadata()
    if band_name != "H11":
        raise ValueError("D1-34 authorizes H11 generation only")
    canonical = generation_plan("H11")
    if plan != canonical:
        raise ValueError("D1-34 plan must equal exact canonical H11 plan")
    if canonical != [
        {
            "purpose": "base_sieve_support",
            "strategy": "whole_prefix",
            "start": 0,
            "stop": 8063,
        },
        {
            "purpose": "segmented_target",
            "strategy": "segmented",
            "start": 64_000_000,
            "stop": 65_000_000,
        },
    ]:
        raise ValueError("canonical H11 generation arithmetic changed")
    if canonical[0]["stop"] > LOW_SUPPORT_STOP:
        raise ValueError("whole-prefix generation above 100,000 is forbidden")
    target = BANDS["H11"]
    if any(_intersects(target, prior) for prior in HISTORICAL_RANGES.values()):
        raise ValueError("H11 intersects historical novelty range")
    if any(_intersects(target, prior) for prior in E005_CALIBRATION_RANGES):
        raise ValueError("H11 intersects E005 calibration range")
    if any(
        name != "H11" and _intersects(target, interval)
        for name, _, interval in FROZEN_PARTITION
    ):
        raise ValueError("H11 intersects E011 non-target range")


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
    if family in {"K2", "K3", "K4"} and isinstance(signature, int):
        return signature
    raise ValueError(f"invalid signature for frozen family {family}")


def signature_to_json(family: str, signature: Signature) -> int | list[int]:
    signature_sort_key(family, signature)
    return list(signature) if isinstance(signature, tuple) else int(signature)


def mode_summary(family: str, counter: Mapping[Signature, int]) -> dict[str, Any]:
    if not counter:
        return {
            "prime_mode_count": 0,
            "maximizer_count": 0,
            "highest_competing_count": 0,
            "strict_unique_prime_mode": False,
            "unique_mode": None,
        }
    ranking = sorted(
        counter.items(), key=lambda item: (-int(item[1]), signature_sort_key(family, item[0]))
    )
    maximum = int(ranking[0][1])
    maximizers = [signature for signature, count in ranking if int(count) == maximum]
    unique = maximizers[0] if len(maximizers) == 1 else None
    if unique is None:
        highest_competing = maximum if len(ranking) >= 2 else 0
    else:
        highest_competing = max(
            (int(count) for signature, count in counter.items() if signature != unique), default=0
        )
    return {
        "prime_mode_count": maximum,
        "maximizer_count": len(maximizers),
        "highest_competing_count": highest_competing,
        "strict_unique_prime_mode": unique is not None,
        "unique_mode": unique,
    }


def mixed_residue_count(
    target: Signature,
    signatures: Sequence[Signature],
    residues: Sequence[int],
) -> int:
    if len(signatures) != len(residues):
        raise ValueError("signature/residue lengths differ")
    target_residues: set[int] = set()
    other_residues: set[int] = set()
    for signature, residue in zip(signatures, residues, strict=True):
        if signature == target:
            target_residues.add(int(residue))
        else:
            other_residues.add(int(residue))
    return len(target_residues & other_residues)


def _family_row(
    *,
    family: str,
    counter: Mapping[Signature, int],
    signatures: Sequence[Signature],
    residues: Sequence[int],
    population: int,
) -> tuple[dict[str, Any], Signature | None, frozenset[int] | None, bool]:
    if sum(int(count) for count in counter.values()) != population:
        raise ValueError(f"{family} frequency table does not exhaust prime anchors")
    summary = mode_summary(family, counter)
    unique = summary.pop("unique_mode")
    population_ok = population >= POPULATION_FLOOR
    occurrence_ok = bool(unique is not None and summary["prime_mode_count"] >= OCCURRENCE_FLOOR)
    mixed = mixed_residue_count(unique, signatures, residues) if unique is not None else None
    residue_ok = bool(mixed is not None and mixed >= MIXED_RESIDUE_FLOOR)
    pre_duplicate = bool(
        population_ok
        and summary["strict_unique_prime_mode"]
        and occurrence_ok
        and residue_ok
    )
    support = (
        frozenset(i for i, signature in enumerate(signatures) if signature == unique)
        if unique is not None
        else None
    )
    row = {
        "family": family,
        **summary,
        "unique_mode_signature": signature_to_json(family, unique) if unique is not None else None,
        "population_floor_passed": population_ok,
        "occurrence_floor_passed": occurrence_ok,
        "unique_mode_mixed_residue_count": mixed,
        "residue_control_passed": residue_ok,
        "mechanically_eligible": pre_duplicate,
    }
    if frozenset(row) != FAMILY_ROW_KEYS:
        raise ValueError("E011 family row escaped frozen descriptive allowlist")
    return row, unique, support, pre_duplicate


def apply_duplicate_suppression(
    family_rows: Sequence[dict[str, Any]],
    unique_modes: Mapping[str, Signature | None],
    support_sets: Mapping[str, frozenset[int] | None],
) -> list[dict[str, Any]]:
    retained_supports: list[frozenset[int]] = []
    promotions: list[dict[str, Any]] = []
    for row in family_rows:
        family = str(row["family"])
        if not row["mechanically_eligible"]:
            continue
        support = support_sets[family]
        target = unique_modes[family]
        if support is None or target is None:
            raise ValueError("eligible family lacks frozen unique mode/support")
        if any(support == earlier for earlier in retained_supports):
            row["mechanically_eligible"] = False
            continue
        retained_supports.append(support)
        promotions.append(
            {
                "family": family,
                "target_signature": signature_to_json(family, target),
                "target_prime_count": int(row["prime_mode_count"]),
                "target_mixed_residue_count": int(row["unique_mode_mixed_residue_count"]),
            }
        )
    if len(promotions) > PROMOTION_CAP:
        raise ValueError("E011 promotion cap exceeded")
    if any(frozenset(row) != PROMOTION_KEYS for row in promotions):
        raise ValueError("E011 promotion escaped frozen allowlist")
    return promotions


def _parameters() -> dict[str, Any]:
    return {
        "degree_selection": {"partition_counts": {"2": 2, "3": 3, "4": 5, "5": 7}, "degree": 5},
        "polynomial": {
            "coefficient_order": "constant_to_highest_degree",
            "coefficients": list(POLYNOMIAL),
            "discriminant": DISCRIMINANT,
            "discriminant_factorization": [3, 7, 7, 23],
        },
        "Q": Q,
        "width": WIDTH,
        "population_floor": POPULATION_FLOOR,
        "occurrence_floor": OCCURRENCE_FLOOR,
        "mixed_residue_floor": MIXED_RESIDUE_FLOOR,
        "promotion_cap": PROMOTION_CAP,
        "family_definitions": [
            {"family": "K1", "definition": "exact nonincreasing factor-degree partition"},
            {"family": "K2", "definition": "number of irreducible factors"},
            {"family": "K3", "definition": "number of linear factors"},
            {"family": "K4", "definition": "largest irreducible-factor degree"},
        ],
    }



def validate_payload_allowlist(payload: Mapping[str, Any]) -> None:
    if frozenset(payload) != PAYLOAD_KEYS:
        raise ValueError("E011 payload escaped frozen descriptive allowlist")
    if not isinstance(payload.get("anchor_summary"), Mapping) or frozenset(payload["anchor_summary"]) != ANCHOR_SUMMARY_KEYS:
        raise ValueError("E011 anchor summary escaped frozen descriptive allowlist")
    if not isinstance(payload.get("validation"), Mapping) or frozenset(payload["validation"]) != VALIDATION_KEYS:
        raise ValueError("E011 validation escaped frozen descriptive allowlist")
    families = payload.get("families")
    if not isinstance(families, list) or any(not isinstance(row, Mapping) or frozenset(row) != FAMILY_ROW_KEYS for row in families):
        raise ValueError("E011 family row escaped frozen descriptive allowlist")
    promotions = payload.get("promotions")
    if not isinstance(promotions, list) or any(not isinstance(row, Mapping) or frozenset(row) != PROMOTION_KEYS for row in promotions):
        raise ValueError("E011 promotion escaped frozen descriptive allowlist")


def validate_h11_payload_allowlist(payload: Mapping[str, Any]) -> None:
    if frozenset(payload) != H11_PAYLOAD_KEYS:
        raise ValueError("H11 payload escaped frozen criterion allowlist")
    validation = payload.get("validation")
    if not isinstance(validation, Mapping) or frozenset(validation) != VALIDATION_KEYS:
        raise ValueError("H11 validation escaped frozen criterion allowlist")
    criteria = payload.get("criteria")
    expected_ids = tuple(observation_id for observation_id, _, _ in H11_TARGETS)
    if not isinstance(criteria, Mapping) or tuple(criteria) != expected_ids:
        raise ValueError("H11 criteria escaped frozen observation order")
    if any(
        not isinstance(criteria[observation_id], Mapping)
        or frozenset(criteria[observation_id]) != H11_CRITERION_KEYS
        for observation_id in expected_ids
    ):
        raise ValueError("H11 criterion record escaped frozen allowlist")


def summarise_primes(
    *, band_name: str, code_commit: str, plan: list[dict[str, Any]], primes: Sequence[int]
) -> dict[str, Any]:
    validate_generation_plan(plan, band_name=band_name)
    start, stop = BANDS[band_name]
    if any(prime < start or prime >= stop for prime in primes):
        raise ValueError("prime anchors escaped exact D11 band")
    if any(a >= b for a, b in zip(primes, primes[1:], strict=False)):
        raise ValueError("prime anchors must be strictly increasing")
    if not primes:
        raise ValueError("D11 prime anchor population is empty")

    counters: dict[str, Counter[Signature]] = {family: Counter() for family in FAMILY_ORDER}
    per_family_signatures: dict[str, list[Signature]] = {family: [] for family in FAMILY_ORDER}
    residues: list[int] = []
    for prime in primes:
        counts = factor_counts(int(prime))
        signatures = signatures_from_counts(counts)
        residues.append(int(prime) % Q)
        for family in FAMILY_ORDER:
            signature = signatures[family]
            counters[family][signature] += 1
            per_family_signatures[family].append(signature)

    population = len(primes)
    family_rows: list[dict[str, Any]] = []
    unique_modes: dict[str, Signature | None] = {}
    support_sets: dict[str, frozenset[int] | None] = {}
    for family in FAMILY_ORDER:
        row, unique, support, _ = _family_row(
            family=family,
            counter=counters[family],
            signatures=per_family_signatures[family],
            residues=residues,
            population=population,
        )
        family_rows.append(row)
        unique_modes[family] = unique
        support_sets[family] = support

    promotions = apply_duplicate_suppression(family_rows, unique_modes, support_sets)
    validation = {key: 0 for key in sorted(VALIDATION_KEYS)}
    payload = {
        "experiment": EXPERIMENT_ID,
        "implementation_commit": code_commit,
        "band": {"name": band_name, "range": [start, stop], "interval_semantics": "half-open"},
        "partition": [
            {"name": name, "role": role, "range": list(interval)}
            for name, role, interval in FROZEN_PARTITION
        ],
        "parameters": _parameters(),
        "generation_plan": plan,
        "anchor_summary": {
            "prime_count": population,
            "first_prime": int(primes[0]),
            "last_prime": int(primes[-1]),
        },
        "validation": validation,
        "families": family_rows,
        "promotions": promotions,
    }
    validate_payload_allowlist(payload)
    return payload


def h11_criterion_fields(
    *,
    observation_id: str,
    family: str,
    target: Signature,
    counter: Mapping[Signature, int],
    signatures: Sequence[Signature],
    residues: Sequence[int],
    population: int,
    validation: Mapping[str, int],
) -> dict[str, Any]:
    """Evaluate exactly one precommitted E011 H11 criterion."""
    if (observation_id, family, target) not in H11_TARGETS:
        raise ValueError("H11 target does not match a frozen observation")
    signature_sort_key(family, target)
    if sum(int(count) for count in counter.values()) != population:
        raise ValueError(f"H11 {family} frequency table does not exhaust prime anchors")
    if len(signatures) != population or len(residues) != population:
        raise ValueError("H11 criterion vectors do not exhaust prime anchors")
    if frozenset(validation) != VALIDATION_KEYS:
        raise ValueError("H11 mandatory validation aggregate changed")
    if any(
        not isinstance(value, int) or isinstance(value, bool) or value < 0
        for value in validation.values()
    ):
        raise ValueError("H11 validation aggregates must be nonnegative integers")

    target_count = int(counter.get(target, 0))
    highest_competing_count = max(
        (int(count) for signature, count in counter.items() if signature != target),
        default=0,
    )
    mixed = mixed_residue_count(target, signatures, residues)
    population_ok = population >= POPULATION_FLOOR
    occurrence_ok = target_count >= OCCURRENCE_FLOOR
    strict_unique_ok = target_count > highest_competing_count
    residue_ok = mixed >= MIXED_RESIDUE_FLOOR
    validation_ok = all(int(value) == 0 for value in validation.values())
    replication_ok = bool(
        population_ok
        and occurrence_ok
        and strict_unique_ok
        and residue_ok
        and validation_ok
    )
    fields = {
        "target_signature": signature_to_json(family, target),
        "target_count": target_count,
        "highest_competing_count": highest_competing_count,
        "mixed_residue_count": mixed,
        "prime_population": population,
        "population_floor_passed": population_ok,
        "occurrence_floor_passed": occurrence_ok,
        "strict_unique_mode_passed": strict_unique_ok,
        "mixed_residue_floor_passed": residue_ok,
        "validation_passed": validation_ok,
        "replication_passed": replication_ok,
    }
    if frozenset(fields) != H11_CRITERION_KEYS:
        raise ValueError("H11 criterion record escaped frozen allowlist")
    return fields


def summarise_h11_replication(
    *, code_commit: str, plan: list[dict[str, Any]], primes: Sequence[int]
) -> dict[str, Any]:
    validate_generation_plan(plan, band_name="H11")
    start, stop = BANDS["H11"]
    if any(prime < start or prime >= stop for prime in primes):
        raise ValueError("prime anchors escaped exact H11 band")
    if any(a >= b for a, b in zip(primes, primes[1:], strict=False)):
        raise ValueError("H11 prime anchors must be strictly increasing")
    if not primes:
        raise ValueError("H11 prime anchor population is empty")

    selected_families = tuple(family for _, family, _ in H11_TARGETS)
    counters: dict[str, Counter[Signature]] = {
        family: Counter() for family in selected_families
    }
    per_family_signatures: dict[str, list[Signature]] = {
        family: [] for family in selected_families
    }
    residues: list[int] = []
    for prime in primes:
        counts = factor_counts(int(prime))
        signatures = signatures_from_counts(counts)
        residues.append(int(prime) % Q)
        for family in selected_families:
            signature = signatures[family]
            counters[family][signature] += 1
            per_family_signatures[family].append(signature)

    population = len(primes)
    validation = {key: 0 for key in sorted(VALIDATION_KEYS)}
    for family in selected_families:
        if sum(int(count) for count in counters[family].values()) != population:
            validation["family_frequency_total_failure_count"] += 1

    criteria: dict[str, dict[str, Any]] = {}
    for observation_id, family, target in H11_TARGETS:
        criteria[observation_id] = h11_criterion_fields(
            observation_id=observation_id,
            family=family,
            target=target,
            counter=counters[family],
            signatures=per_family_signatures[family],
            residues=residues,
            population=population,
            validation=validation,
        )

    payload = {
        "experiment": EXPERIMENT_ID,
        "implementation_commit": code_commit,
        "band": {"name": "H11", "range": [start, stop], "interval_semantics": "half-open"},
        "generation_plan": plan,
        "validation": validation,
        "criteria": criteria,
    }
    validate_h11_payload_allowlist(payload)
    return payload


def build_payload(*, band_name: str, code_commit: str) -> dict[str, Any]:
    if band_name != "H11":
        raise ValueError("D1-34 build path authorizes H11 only")
    plan = generation_plan("H11")
    validate_generation_plan(plan, band_name="H11")
    _, primes = execute_generation_plan(plan, band_name="H11")
    return summarise_h11_replication(code_commit=code_commit, plan=plan, primes=primes)


def serialise_payload(payload: Mapping[str, Any]) -> bytes:
    return (json.dumps(payload, sort_keys=True, indent=2) + "\n").encode("utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--band", choices=("H11",), required=True)
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
