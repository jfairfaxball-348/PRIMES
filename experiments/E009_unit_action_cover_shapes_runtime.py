#!/usr/bin/env python3
"""E009 committed runtime for the frozen unit-action cover-shape evaluator."""
from __future__ import annotations

import argparse
from collections import Counter
from collections.abc import Sequence
from math import gcd, isqrt
from pathlib import Path
from typing import Any

import experiments.E009_unit_action_cover_shapes as frozen


def factor_exact_runtime(
    value: int, base_primes: Sequence[int], support_limit: int
) -> tuple[tuple[tuple[int, int], ...], bool, bool]:
    """Ascending trial division with reconstruction/canonical witnesses retained in one pass."""
    if value < 1:
        raise ValueError("exact factorization input must be positive")
    remainder = value
    factors: list[tuple[int, int]] = []
    residual_prime_proven = remainder == 1

    for prime in base_primes:
        if prime * prime > remainder:
            residual_prime_proven = True
            break
        if remainder % prime:
            continue
        exponent = 0
        while remainder % prime == 0:
            remainder //= prime
            exponent += 1
        factors.append((int(prime), exponent))
        if remainder == 1:
            residual_prime_proven = True
            break
    else:
        # The validated E009 plan provides every prime through floor(sqrt(U-1)).
        residual_prime_proven = support_limit >= isqrt(value)

    if remainder > 1:
        factors.append((int(remainder), 1))

    reconstruction_ok = frozen.reconstruct_factors(factors) == value
    canonical_ok = residual_prime_proven and all(
        exponent >= 1 and (i == 0 or factors[i - 1][0] < prime)
        for i, (prime, exponent) in enumerate(factors)
    )
    return tuple(factors), reconstruction_ok, canonical_ok


def summarise_band(
    *,
    band_name: str,
    code_commit: str,
    plan: list[dict[str, Any]],
    base_primes: Sequence[int],
    target_primes: Sequence[int],
) -> dict[str, Any]:
    frozen.validate_generation_plan(plan, band_name=band_name)
    start, stop = frozen.BANDS[band_name]
    if any(prime < start or prime >= stop for prime in target_primes):
        raise ValueError("target prime input contains value outside the selected band")
    if any(not frozen.is_q_admissible(prime) for prime in target_primes):
        raise ValueError("every high-band prime must belong to the Q-admissible domain")

    base_request = next(row for row in plan if row["purpose"] == "base_sieve_support")
    support_limit = int(base_request["stop"]) - 1
    if support_limit < isqrt(stop - 1):
        raise ValueError("base support is insufficient for exact runtime factorization")

    prime_set = frozenset(target_primes)
    prime_counters = {family: Counter() for family in frozen.FAMILY_ORDER}
    composite_counters = {family: Counter() for family in frozen.FAMILY_ORDER}
    prime_signature_members: dict[str, dict[Any, set[int]]] = {
        family: {} for family in frozen.FAMILY_ORDER
    }
    validation = {key: 0 for key in frozen.VALIDATION_KEYS}
    admissible_count = 0
    N_prime = 0
    N_composite = 0

    for anchor in range(start, stop):
        if not frozen.is_q_admissible(anchor):
            continue
        admissible_count += 1
        is_prime = anchor in prime_set
        if is_prime:
            N_prime += 1
            counters = prime_counters
        else:
            N_composite += 1
            counters = composite_counters

        factors, reconstruction_ok, canonical_ok = factor_exact_runtime(
            anchor, base_primes, support_limit
        )
        if not reconstruction_ok:
            validation["factorization_reconstruction_failure_count"] += 1
        if not canonical_ok:
            validation["nonprime_factor_or_canonical_order_failure_count"] += 1

        terms = frozen.lambda_terms(factors)
        lambda_value = frozen.unit_group_exponent(factors)
        if lambda_value != frozen.lcm_many(terms):
            validation["lambda_construction_failure_count"] += 1
        if any(gcd(base, anchor) != 1 for base in frozen.BASIS):
            validation["basis_unit_gcd_failure_count"] += 1

        lambda_factors, lambda_reconstruction_ok, lambda_canonical_ok = factor_exact_runtime(
            lambda_value, base_primes, support_limit
        )
        if not lambda_reconstruction_ok:
            validation["factorization_reconstruction_failure_count"] += 1
        if not lambda_canonical_ok:
            validation["nonprime_factor_or_canonical_order_failure_count"] += 1

        orders: list[int] = []
        for base in frozen.BASIS:
            order = frozen.multiplicative_order(base, anchor, lambda_value, lambda_factors)
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

        sigs, flags, minimal = frozen.cover_shape(tuple(orders), lambda_value)
        if not frozen.cover_monotonicity_holds(flags):
            validation["cover_monotonicity_failure_count"] += 1
        if not frozen.minimal_antichain_is_exact(flags, minimal):
            validation["minimal_antichain_failure_count"] += 1

        for family in frozen.FAMILY_ORDER:
            signature = sigs[family]
            counters[family][signature] += 1
            if is_prime:
                bucket = prime_signature_members[family].get(signature)
                if bucket is None:
                    bucket = set()
                    prime_signature_members[family][signature] = bucket
                bucket.add(anchor)

    if N_prime != len(prime_set) or N_prime + N_composite != admissible_count:
        raise ValueError("Q-admissible prime/composite partition failed")
    if any(validation.values()):
        raise ValueError("validation aggregate failure detected during E009 evaluation")

    family_rows: list[dict[str, Any]] = []
    mode_anchor_sets: dict[str, frozenset[int]] = {}
    for family in frozen.FAMILY_ORDER:
        if sum(prime_counters[family].values()) != N_prime:
            raise ValueError("prime frequency table does not exhaust prime anchors")
        if sum(composite_counters[family].values()) != N_composite:
            raise ValueError("composite frequency table does not exhaust composite anchors")
        row, unique_signature = frozen._family_row(
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

    promotions = frozen.apply_duplicate_suppression(family_rows, mode_anchor_sets)
    target_primes_sorted = sorted(target_primes)
    payload = {
        "experiment": frozen.EXPERIMENT_ID,
        "implementation_commit": code_commit,
        "band": {
            "name": band_name,
            "range": [start, stop],
            "interval_semantics": "half-open",
        },
        "partition": [
            {"name": name, "role": role, "range": list(interval)}
            for name, role, interval in frozen.FROZEN_PARTITION
        ],
        "parameters": frozen._parameters(),
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
    if frozenset(payload) != frozen.PAYLOAD_KEYS:
        raise ValueError("E009 payload escaped the frozen descriptive allowlist")
    if frozenset(payload["anchor_summary"]) != frozen.ANCHOR_SUMMARY_KEYS:
        raise ValueError("E009 anchor summary escaped the frozen descriptive allowlist")
    if frozenset(payload["validation"]) != frozen.VALIDATION_KEYS:
        raise ValueError("E009 validation escaped the frozen descriptive allowlist")
    if any(frozenset(row) != frozen.FAMILY_ROW_KEYS for row in family_rows):
        raise ValueError("E009 family row escaped the frozen descriptive allowlist")
    return payload


def build_payload(*, band_name: str, code_commit: str) -> dict[str, Any]:
    plan = frozen.generation_plan(band_name)
    frozen.validate_generation_plan(plan, band_name=band_name)
    base_primes, target_primes = frozen.execute_generation_plan(plan, band_name=band_name)
    return summarise_band(
        band_name=band_name,
        code_commit=code_commit,
        plan=plan,
        base_primes=base_primes,
        target_primes=target_primes,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--band", choices=tuple(frozen.BANDS), required=True)
    parser.add_argument("--code-commit", required=True)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_payload(band_name=args.band, code_commit=args.code_commit)
    rendered = frozen.serialise_payload(payload)
    if args.output is None:
        print(rendered.decode("utf-8"), end="")
    else:
        args.output.write_bytes(rendered)


if __name__ == "__main__":
    main()
