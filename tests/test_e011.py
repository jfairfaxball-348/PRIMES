from __future__ import annotations

from copy import deepcopy
from math import gcd

import pytest

from experiments import E011_finite_field_factor_degree_shapes as e011


def test_frozen_metadata_partition_polynomial_and_floors() -> None:
    e011.validate_frozen_metadata()
    assert e011.BANDS == {
        "D11": (62_000_000, 63_000_000),
        "H11": (64_000_000, 65_000_000),
        "A11": (124_000_000, 125_000_000),
    }
    assert e011.POLYNOMIAL == (1, 1, 0, 0, 0, 1)
    assert e011.DISCRIMINANT == 3381 == 3 * 7 * 7 * 23
    assert e011.POPULATION_FLOOR == 1000
    assert e011.OCCURRENCE_FLOOR == 32
    assert e011.MIXED_RESIDUE_FLOOR == 8
    assert e011.FAMILY_ORDER == ("K1", "K2", "K3", "K4")


def test_partition_is_disjoint_from_all_historical_and_calibration_ranges() -> None:
    rows = [interval for _, _, interval in e011.FROZEN_PARTITION]
    for i, left in enumerate(rows):
        for right in rows[i + 1 :]:
            assert not e011._intersects(left, right)
        for prior in e011.HISTORICAL_RANGES.values():
            assert not e011._intersects(left, prior)
        for prior in e011.E005_CALIBRATION_RANGES:
            assert not e011._intersects(left, prior)


def test_exact_polynomial_normalization_add_multiply_divide_gcd_and_power() -> None:
    p = 5
    assert e011.poly_normalize([1, -1, 0, 0], p) == (1, 4)
    assert e011.poly_add((1, 1), (4, 2), p) == (0, 3)
    assert e011.poly_sub((1, 1), (4, 2), p) == (2, 4)
    square = e011.poly_mul((1, 1), (1, 1), p)
    assert square == (1, 2, 1)
    quotient, remainder = e011.poly_divmod(square, (1, 1), p)
    assert quotient == (1, 1)
    assert remainder == ()
    left = e011.poly_mul((1, 1), (2, 1), p)
    right = e011.poly_mul((1, 1), (3, 1), p)
    assert e011.poly_gcd(left, right, p) == (1, 1)
    assert e011.poly_pow_mod((0, 1), 5, e011.POLYNOMIAL, p) == (4, 4)


def test_squarefree_validation_matches_discriminant_small_fields() -> None:
    for p in (3, 7, 23):
        with pytest.raises(ValueError, match="squarefree"):
            e011.factor_counts_reference(p)
        with pytest.raises(ValueError, match="squarefree"):
            e011.factor_counts(p)
    for p in (2, 5, 11, 13, 19):
        assert e011.factor_counts_reference(p) == e011.factor_counts(p)


@pytest.mark.parametrize(
    ("p", "counts", "k1", "k2", "k3", "k4"),
    [
        (2, (0, 1, 1, 0, 0), (3, 2), 2, 0, 3),
        (5, (1, 2, 0, 0, 0), (2, 2, 1), 3, 1, 2),
        (13, (2, 0, 1, 0, 0), (3, 1, 1), 3, 2, 3),
        (19, (3, 1, 0, 0, 0), (2, 1, 1, 1), 4, 3, 2),
        (29, (0, 1, 1, 0, 0), (3, 2), 2, 0, 3),
    ],
)
def test_hand_checkable_factor_counts_and_k_families(
    p: int,
    counts: tuple[int, ...],
    k1: tuple[int, ...],
    k2: int,
    k3: int,
    k4: int,
) -> None:
    assert e011.factor_counts_reference(p) == counts
    assert e011.factor_counts(p) == counts
    assert e011.signatures_from_counts(counts) == {"K1": k1, "K2": k2, "K3": k3, "K4": k4}


def test_all_seven_frozen_k1_partitions_and_coarsenings() -> None:
    vectors = [
        (0, 0, 0, 0, 1),
        (1, 0, 0, 1, 0),
        (0, 1, 1, 0, 0),
        (2, 0, 1, 0, 0),
        (1, 2, 0, 0, 0),
        (3, 1, 0, 0, 0),
        (5, 0, 0, 0, 0),
    ]
    assert {e011.signatures_from_counts(v)["K1"] for v in vectors} == e011.ALLOWED_K1
    for vector in vectors:
        signatures = e011.signatures_from_counts(vector)
        assert signatures["K2"] == len(signatures["K1"])
        assert signatures["K3"] == vector[0]
        assert signatures["K4"] == max(signatures["K1"])


def test_signature_order_and_strict_tie_handling() -> None:
    assert e011.signature_sort_key("K1", (3, 1, 1)) < e011.signature_sort_key("K1", (4, 1))
    unique = e011.mode_summary("K2", {1: 9, 2: 7, 3: 2})
    assert unique == {
        "prime_mode_count": 9,
        "maximizer_count": 1,
        "highest_competing_count": 7,
        "strict_unique_prime_mode": True,
        "unique_mode": 1,
    }
    tied = e011.mode_summary("K2", {1: 9, 2: 9, 3: 2})
    assert tied["strict_unique_prime_mode"] is False
    assert tied["maximizer_count"] == 2
    assert tied["highest_competing_count"] == 9
    assert tied["unique_mode"] is None


def test_mixed_residue_control_boundary_at_seven_and_eight() -> None:
    reduced = [r for r in range(210) if gcd(r, 210) == 1]
    target = 2
    signatures7 = []
    residues7 = []
    for residue in reduced[:7]:
        signatures7.extend([target, 3])
        residues7.extend([residue, residue])
    assert e011.mixed_residue_count(target, signatures7, residues7) == 7
    signatures8 = signatures7 + [target, 3]
    residues8 = residues7 + [reduced[7], reduced[7]]
    assert e011.mixed_residue_count(target, signatures8, residues8) == 8


def _eligible_row(family: str, signature: int | list[int], count: int = 40) -> dict[str, object]:
    return {
        "family": family,
        "prime_mode_count": count,
        "maximizer_count": 1,
        "highest_competing_count": count - 1,
        "strict_unique_prime_mode": True,
        "unique_mode_signature": signature,
        "population_floor_passed": True,
        "occurrence_floor_passed": True,
        "unique_mode_mixed_residue_count": 8,
        "residue_control_passed": True,
        "mechanically_eligible": True,
    }


def test_duplicate_suppression_uses_frozen_family_order_and_cap() -> None:
    rows = [
        _eligible_row("K1", [3, 2]),
        _eligible_row("K2", 2),
        _eligible_row("K3", 0),
        _eligible_row("K4", 3),
    ]
    unique = {"K1": (3, 2), "K2": 2, "K3": 0, "K4": 3}
    supports = {
        "K1": frozenset({1, 2, 3}),
        "K2": frozenset({1, 2, 3}),
        "K3": frozenset({4, 5, 6}),
        "K4": frozenset({7, 8, 9}),
    }
    promotions = e011.apply_duplicate_suppression(rows, unique, supports)
    assert [row["family"] for row in promotions] == ["K1", "K3", "K4"]
    assert rows[1]["mechanically_eligible"] is False
    assert len(promotions) <= 4


def test_family_frequency_total_is_mandatory() -> None:
    with pytest.raises(ValueError, match="does not exhaust"):
        e011._family_row(
            family="K2",
            counter={2: 9},
            signatures=[2] * 9,
            residues=[1] * 9,
            population=10,
        )


def test_d11_generation_plan_is_exact() -> None:
    assert e011.generation_plan("D11") == [
        {"purpose": "base_sieve_support", "strategy": "whole_prefix", "start": 0, "stop": 7938},
        {"purpose": "segmented_target", "strategy": "segmented", "start": 62_000_000, "stop": 63_000_000},
    ]
    e011.validate_generation_plan(e011.generation_plan("D11"), band_name="D11")


def test_fail_closed_plan_rejection_precedes_prime_generators(monkeypatch: pytest.MonkeyPatch) -> None:
    called = False

    def forbidden(*args: object, **kwargs: object) -> object:
        nonlocal called
        called = True
        raise AssertionError("prime generator must not be reached")

    monkeypatch.setattr(e011, "sieve", forbidden)
    monkeypatch.setattr(e011, "_segmented_target_prime_flags", forbidden)
    canonical = e011.generation_plan("D11")
    invalid_plans = []
    for stop in (7937, 7939, 100_001):
        plan = deepcopy(canonical)
        plan[0]["stop"] = stop
        invalid_plans.append(plan)
    for interval in [
        (61_000_000, 62_000_000),
        (62_000_001, 63_000_000),
        (62_000_000, 63_000_001),
        (62_000_001, 63_000_001),
        (63_000_000, 64_000_000),
        (64_000_000, 65_000_000),
        (124_000_000, 125_000_000),
        (58_000_000, 59_000_000),
        (60_000_000, 61_000_000),
        (116_000_000, 117_000_000),
        (54_000_000, 55_000_000),
        (56_000_000, 57_000_000),
        (108_000_000, 109_000_000),
        (52_000_000, 53_000_000),
        (66_000_000, 67_000_000),
        (39_000_000, 40_000_000),
        (128_000_000, 129_048_576),
        (90_000_000, 91_000_000),
    ]:
        plan = deepcopy(canonical)
        plan[1]["start"], plan[1]["stop"] = interval
        invalid_plans.append(plan)
    split = deepcopy(canonical) + [
        {"purpose": "segmented_target", "strategy": "segmented", "start": 62_500_000, "stop": 63_000_000}
    ]
    invalid_plans.append(split)
    reordered = [canonical[1], canonical[0]]
    invalid_plans.append(reordered)
    whole_prefix_high = deepcopy(canonical)
    whole_prefix_high[1]["strategy"] = "whole_prefix"
    whole_prefix_high[1]["start"] = 0
    invalid_plans.append(whole_prefix_high)
    for plan in invalid_plans:
        with pytest.raises(ValueError):
            e011.execute_generation_plan(plan, band_name="D11")
    assert called is False
    with pytest.raises(ValueError):
        e011.execute_generation_plan(canonical, band_name="H11")
    assert called is False


def test_payload_allowlist_and_deterministic_serialization() -> None:
    family_rows = [
        _eligible_row("K1", [3, 2]),
        _eligible_row("K2", 2),
        _eligible_row("K3", 0),
        _eligible_row("K4", 3),
    ]
    payload = {
        "experiment": "E011",
        "implementation_commit": "checkpoint",
        "band": {"name": "D11", "range": [62_000_000, 63_000_000], "interval_semantics": "half-open"},
        "partition": [],
        "parameters": {},
        "generation_plan": e011.generation_plan("D11"),
        "anchor_summary": {"prime_count": 1001, "first_prime": 62_000_003, "last_prime": 62_999_999},
        "validation": {key: 0 for key in e011.VALIDATION_KEYS},
        "families": family_rows,
        "promotions": [
            {"family": "K1", "target_signature": [3, 2], "target_prime_count": 40, "target_mixed_residue_count": 8}
        ],
    }
    e011.validate_payload_allowlist(payload)
    first = e011.serialise_payload(payload)
    second = e011.serialise_payload(deepcopy(payload))
    assert first == second
    assert first.endswith(b"\n")
    contaminated = deepcopy(payload)
    contaminated["prime_list"] = [62_000_003]
    with pytest.raises(ValueError, match="allowlist"):
        e011.validate_payload_allowlist(contaminated)
    contaminated = deepcopy(payload)
    contaminated["families"][0]["frequency_table"] = []
    with pytest.raises(ValueError, match="allowlist"):
        e011.validate_payload_allowlist(contaminated)


def test_native_and_reference_exact_equivalence_on_additional_small_primes() -> None:
    for p in (31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97):
        assert e011.factor_counts(p) == e011.factor_counts_reference(p)
