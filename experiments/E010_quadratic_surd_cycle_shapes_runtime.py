"""Exact integer runtime for frozen E010 quadratic-surd cycle shapes."""
from __future__ import annotations

from collections import Counter
import ctypes
import fcntl
import hashlib
import subprocess
import tempfile
from collections.abc import Mapping, Sequence
from math import isqrt
from pathlib import Path
from typing import Any, TypeAlias

FAMILY_ORDER = ("L1", "L2", "L3", "L4")
POPULATION_FLOOR = 1_000
OCCURRENCE_FLOOR = 32
PROMOTION_CAP = 4
NATIVE_PROFILE_CAP = 32_768
_NATIVE_LIBRARY: ctypes.CDLL | None = None

ScalarSignature: TypeAlias = int
ProfileSignature: TypeAlias = tuple[int, ...]
Signature: TypeAlias = ScalarSignature | ProfileSignature


class IntegerRootDomainError(ValueError):
    pass


class RecurrenceArithmeticError(ValueError):
    pass


class RecurrenceQuotientError(ValueError):
    pass


class PrematureRepeatError(ValueError):
    pass


class TerminalStateError(ValueError):
    pass


class CycleProfileError(ValueError):
    pass


def exact_nonsquare_root(value: int) -> int:
    if value < 0:
        raise IntegerRootDomainError("quadratic-surd anchor must be nonnegative")
    root = isqrt(value)
    if root * root == value:
        raise IntegerRootDomainError("quadratic-surd anchor must be nonsquare")
    if not (root * root < value < (root + 1) * (root + 1)):
        raise IntegerRootDomainError("exact isqrt bracket failed")
    return root


def validate_quotient_bounds(*, numerator: int, denominator: int, quotient: int) -> None:
    if denominator <= 0:
        raise RecurrenceQuotientError("recurrence denominator must be positive")
    if not quotient * denominator <= numerator < (quotient + 1) * denominator:
        raise RecurrenceQuotientError("exact recurrence quotient bounds failed")


def recurrence_step(*, x: int, a0: int, m: int, d: int, a: int) -> tuple[int, int, int]:
    if d <= 0:
        raise RecurrenceArithmeticError("recurrence input denominator must be positive")
    next_m = d * a - m
    remainder = x - next_m * next_m
    if remainder <= 0:
        raise RecurrenceArithmeticError("recurrence remainder must be positive")
    if remainder % d:
        raise RecurrenceArithmeticError("recurrence remainder must be divisible by prior d")
    next_d = remainder // d
    if next_d <= 0:
        raise RecurrenceArithmeticError("recurrence denominator must remain positive")
    numerator = a0 + next_m
    next_a = numerator // next_d
    validate_quotient_bounds(numerator=numerator, denominator=next_d, quotient=next_a)
    return next_m, next_d, next_a


def record_nonterminal_state(seen: set[tuple[int, int]], *, m: int, d: int) -> None:
    state = (m, d)
    if state in seen:
        raise PrematureRepeatError("nonterminal recurrence state repeated before termination")
    seen.add(state)


def denominator_cycle(x: int) -> tuple[int, ...]:
    a0 = exact_nonsquare_root(x)
    m, d, a = 0, 1, a0
    seen = {(m, d)}
    denominators: list[int] = []
    terminal = (a0, 1, 2 * a0)
    while True:
        m, d, a = recurrence_step(x=x, a0=a0, m=m, d=d, a=a)
        denominators.append(d)
        if (m, d, a) == terminal:
            break
        record_nonterminal_state(seen, m=m, d=d)
    if not denominators or denominators[-1] != 1 or (m, d, a) != terminal:
        raise TerminalStateError("canonical terminal state was not reached")
    return tuple(denominators)


def multiplicity_profile(denominators: Sequence[int]) -> tuple[int, ...]:
    if not denominators or any(value <= 0 for value in denominators):
        raise CycleProfileError("denominator cycle must be nonempty and positive")
    multiplicities = Counter(int(value) for value in denominators)
    maximum = max(multiplicities.values())
    by_multiplicity = Counter(multiplicities.values())
    profile = tuple(by_multiplicity.get(j, 0) for j in range(1, maximum + 1))
    if not profile or profile[-1] <= 0:
        raise CycleProfileError("multiplicity profile may not have trailing zero")
    if sum((j + 1) * count for j, count in enumerate(profile)) != len(denominators):
        raise CycleProfileError("period-length/profile identity failed")
    if sum(profile) != len(multiplicities):
        raise CycleProfileError("distinct-denominator/profile identity failed")
    if len(profile) != maximum:
        raise CycleProfileError("peak-multiplicity/profile identity failed")
    return profile


def cycle_signatures_from_denominators(denominators: Sequence[int]) -> dict[str, Signature]:
    profile = multiplicity_profile(denominators)
    signatures: dict[str, Signature] = {
        "L1": len(denominators),
        "L2": sum(profile),
        "L3": len(profile),
        "L4": profile,
    }
    if int(signatures["L1"]) != sum((j + 1) * c for j, c in enumerate(profile)):
        raise CycleProfileError("L1 profile identity failed")
    if int(signatures["L2"]) != sum(profile):
        raise CycleProfileError("L2 profile identity failed")
    if int(signatures["L3"]) != max(j + 1 for j, c in enumerate(profile) if c):
        raise CycleProfileError("L3 profile identity failed")
    return signatures


def _native_library() -> ctypes.CDLL:
    global _NATIVE_LIBRARY
    if _NATIVE_LIBRARY is not None:
        return _NATIVE_LIBRARY
    source = Path(__file__).with_name("e010_cycle_runtime.c")
    source_bytes = source.read_bytes()
    digest = hashlib.sha256(source_bytes).hexdigest()[:20]
    output = Path(tempfile.gettempdir()) / f"primes-e010-{digest}.so"
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
    function = library.e010_cycle_signatures
    function.argtypes = [
        ctypes.c_uint64, ctypes.c_uint64,
        ctypes.POINTER(ctypes.c_uint32), ctypes.POINTER(ctypes.c_uint32),
        ctypes.POINTER(ctypes.c_uint32), ctypes.POINTER(ctypes.c_uint32), ctypes.c_uint32,
    ]
    function.restype = ctypes.c_int
    _NATIVE_LIBRARY = library
    return library


def cycle_signatures(x: int) -> dict[str, Signature]:
    a0 = exact_nonsquare_root(x)
    l1 = ctypes.c_uint32()
    l2 = ctypes.c_uint32()
    l3 = ctypes.c_uint32()
    profile_buffer = (ctypes.c_uint32 * NATIVE_PROFILE_CAP)()
    result = _native_library().e010_cycle_signatures(
        ctypes.c_uint64(x), ctypes.c_uint64(a0),
        ctypes.byref(l1), ctypes.byref(l2), ctypes.byref(l3),
        profile_buffer, ctypes.c_uint32(NATIVE_PROFILE_CAP),
    )
    if result == 1:
        raise RecurrenceArithmeticError("native recurrence positivity/divisibility failure")
    if result == 2:
        raise RecurrenceQuotientError("native recurrence quotient-bound failure")
    if result == 3:
        raise PrematureRepeatError("native nonterminal recurrence state repeated")
    if result == 4:
        raise TerminalStateError("native canonical terminal-state failure")
    if result == 5:
        raise CycleProfileError("native denominator profile identity failure")
    if result == 7:
        raise IntegerRootDomainError("native exact isqrt bracket failure")
    if result != 0:
        raise CycleProfileError(f"native E010 runtime capacity/build failure: {result}")
    maximum = int(l3.value)
    profile = tuple(int(profile_buffer[i]) for i in range(maximum))
    signatures: dict[str, Signature] = {
        "L1": int(l1.value), "L2": int(l2.value), "L3": maximum, "L4": profile,
    }
    reference_identities = cycle_signatures_from_denominators
    if signatures["L1"] != sum((j + 1) * c for j, c in enumerate(profile)):
        raise CycleProfileError("native L1 profile identity failed")
    if signatures["L2"] != sum(profile):
        raise CycleProfileError("native L2 profile identity failed")
    if maximum != max(j + 1 for j, c in enumerate(profile) if c):
        raise CycleProfileError("native L3 profile identity failed")
    _ = reference_identities
    return signatures


def signature_sort_key(family: str, signature: Signature) -> Any:
    if family in {"L1", "L2", "L3"} and isinstance(signature, int):
        return signature
    if family == "L4" and isinstance(signature, tuple):
        return signature
    raise ValueError(f"invalid signature for frozen family {family}")


def signature_to_json(family: str, signature: Signature) -> int | list[int]:
    signature_sort_key(family, signature)
    return signature if isinstance(signature, int) else list(signature)


def frequency_table(family: str, counter: Mapping[Signature, int]) -> list[dict[str, Any]]:
    return [
        {"signature": signature_to_json(family, sig), "count": int(counter[sig])}
        for sig in sorted(counter, key=lambda value: signature_sort_key(family, value))
    ]


def mode_summary(family: str, counter: Mapping[Signature, int]) -> dict[str, Any]:
    if not counter:
        return {
            "prime_mode_count": 0,
            "prime_maximizing_signatures": [],
            "runner_up_count": None,
            "strict_unique_prime_mode": False,
        }
    ranking = sorted(counter.items(), key=lambda item: (-int(item[1]), signature_sort_key(family, item[0])))
    maximum = int(ranking[0][1])
    maximizers = [signature_to_json(family, sig) for sig, count in ranking if int(count) == maximum]
    return {
        "prime_mode_count": maximum,
        "prime_maximizing_signatures": maximizers,
        "runner_up_count": int(ranking[1][1]) if len(ranking) >= 2 else None,
        "strict_unique_prime_mode": len(maximizers) == 1,
    }


def enrichment_numerator(*, n_prime: int, n_composite: int, N_prime: int, N_composite: int) -> int:
    return n_prime * N_composite - n_composite * N_prime


def family_row(
    *, family: str, prime_counter: Counter[Signature], composite_counter: Counter[Signature],
    N_prime: int, N_composite: int,
) -> tuple[dict[str, Any], Signature | None]:
    mode = mode_summary(family, prime_counter)
    unique: Signature | None = None
    n_composite: int | None = None
    enrichment: int | None = None
    occurrence_passed = enrichment_passed = False
    if mode["strict_unique_prime_mode"]:
        unique = min(
            prime_counter,
            key=lambda sig: (-prime_counter[sig], signature_sort_key(family, sig)),
        )
        n_prime = int(prime_counter[unique])
        n_composite = int(composite_counter.get(unique, 0))
        enrichment = enrichment_numerator(
            n_prime=n_prime, n_composite=n_composite,
            N_prime=N_prime, N_composite=N_composite,
        )
        occurrence_passed = n_prime >= OCCURRENCE_FLOOR
        enrichment_passed = enrichment > 0
    population_passed = N_prime >= POPULATION_FLOOR and N_composite >= POPULATION_FLOOR
    return ({
        "family": family,
        "prime_frequency_table": frequency_table(family, prime_counter),
        "composite_frequency_table": frequency_table(family, composite_counter),
        **mode,
        "unique_mode_composite_count": n_composite,
        "unique_mode_enrichment_numerator": enrichment,
        "population_floor_passed": population_passed,
        "occurrence_floor_passed": occurrence_passed,
        "enrichment_passed": enrichment_passed,
        "mechanically_eligible": False,
    }, unique)


def apply_duplicate_suppression(
    rows: Sequence[dict[str, Any]], mode_anchor_sets: Mapping[str, frozenset[int]]
) -> list[dict[str, Any]]:
    retained_sets: list[frozenset[int]] = []
    promotions: list[dict[str, Any]] = []
    for row in rows:
        family = str(row["family"])
        pre_duplicate = bool(
            row["population_floor_passed"] and row["strict_unique_prime_mode"]
            and row["occurrence_floor_passed"] and row["enrichment_passed"]
        )
        target_set = mode_anchor_sets.get(family, frozenset())
        duplicate = pre_duplicate and any(target_set == prior for prior in retained_sets)
        row["mechanically_eligible"] = pre_duplicate and not duplicate
        if row["mechanically_eligible"]:
            retained_sets.append(target_set)
            promotions.append({
                "family": family,
                "target_signature": row["prime_maximizing_signatures"][0],
                "prime_count": int(row["prime_mode_count"]),
                "composite_count": int(row["unique_mode_composite_count"]),
                "enrichment_numerator": int(row["unique_mode_enrichment_numerator"]),
            })
    return promotions[:PROMOTION_CAP]
