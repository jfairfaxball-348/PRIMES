from __future__ import annotations

from collections import Counter
from decimal import Decimal
from pathlib import Path

import pytest

from experiments.E005_prime_count_scale_calibration import (
    ASSESSMENT_ANCHORS,
    CANDIDATES,
    DEVELOPMENT_ANCHORS,
    WIDTHS,
    _strict_target,
    build_assessment_checkpoint,
    build_development_checkpoint,
    count_half_open,
    decimal_string,
    eligible_questions,
    evaluate_milestones,
    execute_generation_plan,
    generation_plan,
    nested_interval_counts,
    rational_pair,
    residual_objects,
    score_candidates,
    select_residual_target,
    serialise_payload,
    transform_density,
    validate_generation_plan,
    verify_development_record,
)


def test_half_open_and_nested_interval_counting() -> None:
    values = [100, 103, 107, 109, 113, 127, 131, 151]
    assert count_half_open(values, 103, 113) == 3
    assert count_half_open(values, 103, 114) == 4
    counts = nested_interval_counts(values, 100)
    assert counts["W0"] == len(values)


def test_rational_serialization_is_reduced_with_positive_denominator() -> None:
    assert rational_pair(6) == [6, 1]
    from fractions import Fraction

    assert rational_pair(Fraction(6, -8)) == [-3, 4]


def test_frozen_orders_and_decimal_transform_semantics() -> None:
    assert [name for name, _ in WIDTHS] == ["W0", "W1", "W2", "W3", "W4"]
    assert [name for name, _ in DEVELOPMENT_ANCHORS] == ["D5-0", "D5-1", "D5-2"]
    assert [name for name, _ in ASSESSMENT_ANCHORS] == ["H5-0", "H5-1", "H5-2"]
    assert CANDIDATES == tuple(f"N{i:02d}" for i in range(13))
    identity = transform_density("N00", 1, 128_000_000, 4)
    assert decimal_string(identity) == "2.500000000000000000000000000000000000000000000000000000000000E-1"
    first = decimal_string(transform_density("N01", 100, 128_000_000, 4096))
    second = decimal_string(transform_density("N01", 100, 128_000_000, 4096))
    assert first == second
    assert "E" in first and len(first.split("E")[0].split(".")[1]) == 60


def _synthetic_transformed() -> dict[str, dict[str, dict[str, Decimal]]]:
    transformed: dict[str, dict[str, dict[str, Decimal]]] = {}
    for index, candidate in enumerate(CANDIDATES):
        transformed[candidate] = {}
        for anchor_index, (anchor_name, _) in enumerate(DEVELOPMENT_ANCHORS):
            transformed[candidate][anchor_name] = {}
            for width_name, _ in WIDTHS:
                if candidate == "N03":
                    value = Decimal("1") + Decimal(anchor_index) / Decimal("100")
                elif candidate == "N00":
                    value = Decimal("1") + Decimal(anchor_index) / Decimal("10")
                else:
                    value = Decimal("1") + Decimal(anchor_index * (index + 2)) / Decimal("10")
                transformed[candidate][anchor_name][width_name] = value
    return transformed


def test_candidate_scores_ranking_and_development_selection() -> None:
    scores = score_candidates(_synthetic_transformed(), DEVELOPMENT_ANCHORS)
    assert scores["candidate_ranking"][0] == "N03"
    assert Decimal(scores["candidate_scores"]["N03"]) < Decimal(
        scores["candidate_scores"]["N00"]
    )
    assert all(ranking[0] == "N03" for ranking in scores["width_rankings"].values())


def test_baselines_residual_objects_and_sign_target_rules() -> None:
    transformed = _synthetic_transformed()
    baselines, objects, counters = residual_objects(
        "N03", transformed, DEVELOPMENT_ANCHORS
    )
    assert set(baselines) == {name for name, _ in WIDTHS}
    assert set(objects["W0"]) == {"R0", "R1", "R2", "R3", "R4"}
    target, tables = select_residual_target(counters)
    assert isinstance(target, dict)
    assert target["family"] == "R1"
    assert target["development_count"] == 5
    assert len(tables["R1"]) == 1

    tie = Counter({(-1, 1, 1): 2, (-1, -1, 1): 2, (1, -1, 1): 1})
    assert _strict_target(tie) is None
    below_floor = Counter({(-1, 1, 1): 2, (1, -1, 1): 1})
    assert _strict_target(below_floor) is None


def test_q1_q2_q3_eligibility_is_mechanical() -> None:
    scores = score_candidates(_synthetic_transformed(), DEVELOPMENT_ANCHORS)
    questions = eligible_questions(
        "N03",
        scores,
        {"family": "R1", "word": [-1, 0, 1], "development_count": 3},
    )
    assert [row["id"] for row in questions] == ["Q1", "Q2", "Q3"]
    assert eligible_questions("N00", scores, "NO_RESIDUAL_SIGN_TARGET") == []


def test_milestone_and_outcome_encoding() -> None:
    conditions = {
