from collections import Counter

import pytest

from experiments.E004_residue_transition_factorization import (
    BANDS,
    FAMILY_ORDER,
    MODULI,
    RELATIONS,
    _execute_generation_plan,
    _matrix_objects,
    _mode_stats,
    _relation_summary,
    _sort_promotion_pool,
    generation_plan,
    lift_set,
    project_counts,
    reduced_residues,
    serialise_payload,
    transition_counts,
    validate_generation_plan,
)


def _common_high_primes() -> list[int]:
    return [61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127]


def test_exact_reduced_residue_enumeration() -> None:
    assert MODULI == (6, 10, 12, 30, 60)
    assert reduced_residues(6) == (1, 5)
    assert reduced_residues(10) == (1, 3, 7, 9)
    assert reduced_residues(12) == (1, 5, 7, 11)
    assert reduced_residues(30) == (1, 7, 11, 13, 17, 19, 23, 29)
    assert reduced_residues(60) == (
        1, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 49, 53, 59
    )


def test_reduced_residue_filtering_removes_prime_divisors() -> None:
    primes = [2, 3, 5, 7, 11, 13, 17, 19]
    assert transition_counts(primes, 6) == Counter({(5, 1): 3, (1, 5): 2})


def test_band_boundary_exclusion() -> None:
    primes = [99_983, 100_003, 100_019, 100_043, 100_049, 100_057, 100_069, 200_003]
    selected = [p for p in primes if 100_000 <= p < 200_000]
    assert transition_counts(
        primes, 6, start=100_000, stop=200_000
    ) == transition_counts(selected, 6)
    assert sum(
        transition_counts(primes, 6, start=100_000, stop=200_000).values()
    ) == 5


def test_exact_directed_transition_counts() -> None:
    primes = [5, 7, 11, 13, 17, 19]
    assert transition_counts(primes, 6) == Counter({(5, 1): 3, (1, 5): 2})


def test_frozen_relation_order_and_lift_semantics() -> None:
    assert RELATIONS == ((6, 12), (6, 30), (10, 30), (12, 60), (30, 60))
    for coarse, fine in RELATIONS:
        expected_h = len(reduced_residues(fine)) // len(reduced_residues(coarse))
        for residue in reduced_residues(coarse):
            lifts = lift_set(coarse, fine, residue)
            assert lifts == tuple(sorted(lifts))
            assert len(lifts) == expected_h
            assert all(value % coarse == residue for value in lifts)
            assert all(value in reduced_residues(fine) for value in lifts)


def test_exact_projection_and_composite_path_consistency() -> None:
    primes = _common_high_primes()
    counts = {m: transition_counts(primes, m) for m in MODULI}
    for coarse, fine in RELATIONS:
        projected = project_counts(
            counts[fine], fine_modulus=fine, coarse_modulus=coarse
        )
        assert projected == counts[coarse]

    direct = project_counts(counts[60], fine_modulus=60, coarse_modulus=6)
    via_12 = project_counts(
        project_counts(counts[60], fine_modulus=60, coarse_modulus=12),
        fine_modulus=12,
        coarse_modulus=6,
    )
    via_30 = project_counts(
        project_counts(counts[60], fine_modulus=60, coarse_modulus=30),
        fine_modulus=30,
        coarse_modulus=6,
    )
    assert direct == via_12 == via_30 == counts[6]


def test_refinement_order_balance_and_rank_one_classification() -> None:
    objects = _matrix_objects(((1, 2), (3, 4)), coarse_count=10)
    assert objects["forbidden_lift_mask"] == (0, 0, 0, 0)
    assert objects["balance_vector"] == (-6, -2, 2, 6)
    assert sum(objects["balance_vector"]) == 0
    assert objects["determinant_vector"] == (-2,)
    assert objects["minor_zero_mask"] == (0,)
    assert objects["uniform"] is False
    assert objects["positive_rank_one"] is False

    uniform = _matrix_objects(((2, 2), (2, 2)), coarse_count=8)
    assert uniform["balance_vector"] == (0, 0, 0, 0)
    assert uniform["determinant_vector"] == (0,)
    assert uniform["uniform"] is True
    assert uniform["positive_rank_one"] is True

    rank_one = _matrix_objects(((1, 2), (2, 4)), coarse_count=9)
    assert rank_one["uniform"] is False
    assert rank_one["positive_rank_one"] is True

    nonpositive = _matrix_objects(((1, 2), (0, 0)), coarse_count=3)
    assert nonpositive["determinant_vector"] == (0,)
    assert nonpositive["positive_rank_one"] is False


def test_exact_2x2_minor_ordering_for_3x3_matrix() -> None:
    matrix = ((1, 2, 3), (4, 5, 6), (7, 8, 10))
    objects = _matrix_objects(matrix, coarse_count=sum(map(sum, matrix)))
    expected = []
    for i1, i2 in ((0, 1), (0, 2), (1, 2)):
        for j1, j2 in ((0, 1), (0, 2), (1, 2)):
            expected.append(
                matrix[i1][j1] * matrix[i2][j2]
                - matrix[i1][j2] * matrix[i2][j1]
            )
    assert objects["determinant_vector"] == tuple(expected)


def _uniform_counts_6_12() -> dict[int, Counter[tuple[int, int]]]:
    fine = Counter(
        {
            (left, right): 1
            for left in reduced_residues(12)
            for right in reduced_residues(12)
        }
    )
    coarse = project_counts(fine, fine_modulus=12, coarse_modulus=6)
    return {6: coarse, 12: fine}


def _rank_one_counts_6_12() -> dict[int, Counter[tuple[int, int]]]:
    fine: Counter[tuple[int, int]] = Counter()
    pattern = ((1, 2), (2, 4))
    for left in reduced_residues(6):
        left_lifts = lift_set(6, 12, left)
        for right in reduced_residues(6):
            right_lifts = lift_set(6, 12, right)
            for i, fine_left in enumerate(left_lifts):
                for j, fine_right in enumerate(right_lifts):
                    fine[(fine_left, fine_right)] = pattern[i][j]
    coarse = project_counts(fine, fine_modulus=12, coarse_modulus=6)
    return {6: coarse, 12: fine}


def test_p1_suppresses_p2_duplicate_and_p2_nonuniform_case() -> None:
    uniform_relation = _relation_summary(6, 12, _uniform_counts_6_12())
    records = {
        row["family"]: row for row in uniform_relation["promotion_records"]
    }
    assert uniform_relation["complete_positive_uniform_refinement"] is True
    assert uniform_relation["complete_positive_rank_one_refinement"] is True
    assert records["P1"]["mechanical_eligible"] is True
    assert records["P2"]["mechanical_eligible"] is False
    assert records["P2"]["suppressed_by_P1"] is True

    rank_relation = _relation_summary(6, 12, _rank_one_counts_6_12())
    records = {row["family"]: row for row in rank_relation["promotion_records"]}
    assert rank_relation["complete_positive_uniform_refinement"] is False
    assert rank_relation["complete_positive_rank_one_refinement"] is True
    assert records["P1"]["mechanical_eligible"] is False
    assert records["P2"]["mechanical_eligible"] is True


def test_p3_p4_p5_occurrence_floor_and_tie_rejection() -> None:
    unique = _mode_stats([(1, 0), (1, 0), (0, 1), (1, 1)])
    assert unique["coarse_pair_floor_passed"] is True
    assert unique["occurrence_floor_passed"] is True
    assert unique["strict_unique_mode"] is True
    assert unique["mechanical_eligible"] is True

    tie = _mode_stats([(1, 0), (1, 0), (0, 1), (0, 1)])
    assert tie["strict_unique_mode"] is False
    assert tie["mechanical_eligible"] is False

    too_few_pairs = _mode_stats([(1,), (1,), (2,)])
    assert too_few_pairs["coarse_pair_floor_passed"] is False
    assert too_few_pairs["mechanical_eligible"] is False

    too_few_target = _mode_stats([(1,), (2,), (3,), (4,)])
    assert too_few_target["occurrence_floor_passed"] is False
    assert too_few_target["mechanical_eligible"] is False


def _synthetic_relation(
    edge: tuple[int, int], records: list[dict[str, object]]
) -> dict[str, object]:
    return {"edge": list(edge), "promotion_records": records}


def test_deterministic_promotion_family_relation_and_target_order() -> None:
    assert FAMILY_ORDER == ("P1", "P2", "P3", "P4", "P5")
    relations = [
        _synthetic_relation(
            edge,
            [
                {
                    "family": "P1",
                    "mechanical_eligible": edge == (6, 30),
                    "target": None,
                },
                {"family": "P2", "mechanical_eligible": False, "target": None},
                {
                    "family": "P3",
                    "mechanical_eligible": True,
                    "target": [edge[0]],
                    "dominance_margin": 2 if edge == (10, 30) else 1,
                    "mode_count": 3,
                },
                {
                    "family": "P4",
                    "mechanical_eligible": False,
                    "target": [1],
                    "dominance_margin": 0,
                    "mode_count": 0,
                },
                {
                    "family": "P5",
                    "mechanical_eligible": False,
                    "target": [1],
                    "dominance_margin": 0,
                    "mode_count": 0,
                },
            ],
        )
        for edge in RELATIONS
    ]
    pool = _sort_promotion_pool(relations)
    assert [row["family"] for row in pool[:5]] == ["P1"] * 5
    p1_rows = [row for row in pool if row["family"] == "P1"]
    assert [tuple(row["edge"]) for row in p1_rows] == list(RELATIONS)
    p3_rows = [row for row in pool if row["family"] == "P3"]
    assert tuple(p3_rows[0]["edge"]) == (10, 30)


def test_byte_deterministic_serialization() -> None:
    payload = {
        "experiment": "E004",
        "relation_graph": [[6, 12], [6, 30]],
        "x": {"b": 2, "a": 1},
    }
    assert serialise_payload(payload) == serialise_payload(payload)


def test_fail_closed_generation_plan_rejection_before_prime_generation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    plan = generation_plan("D4")
    validate_generation_plan(plan, band_name="D4")
    assert plan[0]["start"] == 0
    assert plan[0]["stop"] < 100_000
    assert (plan[1]["start"], plan[1]["stop"]) == BANDS["D4"]

    called = False

    def forbidden_sieve(_: int) -> list[int]:
        nonlocal called
        called = True
        return []

    monkeypatch.setattr(
        "experiments.E004_residue_transition_factorization.sieve",
        forbidden_sieve,
    )

    bad_prefix = [
        {
            "purpose": "base_sieve_support",
            "strategy": "whole_prefix",
            "start": 0,
            "stop": 200_000,
        },
        plan[1],
    ]
    with pytest.raises(ValueError, match="whole-prefix"):
        _execute_generation_plan(bad_prefix, band_name="D4")
    assert called is False

    forbidden_intervals = (
        (33_000_000, 33_100_000),
        (34_000_000, 34_100_000),
        (35_000_000, 35_100_000),
        (36_000_000, 36_100_000),
        (37_000_000, 37_100_000),
        (38_000_000, 38_100_000),
        (40_000_000, 40_100_000),
        (41_000_000, 41_100_000),
        (70_000_000, 70_100_000),
        (78_000_000, 78_100_000),
    )
    for start, stop in forbidden_intervals:
        bad = [
            plan[0],
            {
                "purpose": "segmented_target",
                "strategy": "segmented",
                "start": start,
                "stop": stop,
            },
        ]
        with pytest.raises(ValueError):
            _execute_generation_plan(bad, band_name="D4")
        assert called is False
