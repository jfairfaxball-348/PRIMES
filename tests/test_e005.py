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
        "a": True,
        "b": True,
    }
    result = evaluate_milestones(
        selected="N03",
        development_selected_score=Decimal("1.01"),
        development_identity_score=Decimal("1.10"),
        assessment_selected_score=Decimal("1.02"),
        assessment_identity_score=Decimal("1.11"),
        development_width_wins=5,
        assessment_width_wins=4,
        development_target={"family": "R1", "word": [-1, 0, 1], "development_count": 3},
        assessment_target_passed=False,
        questions=[{"id": "Q1", "text": "x"}],
        m5_conditions=conditions,
        deterministic_reproduction=True,
        guard_validation=True,
    )
    assert result["M1"] is True
    assert result["M2"] is True
    assert result["M3"] is False
    assert result["M4"] is True
    assert result["M5"] is True
    assert result["overall_outcome"] == "STRONG_PASS"

    invalid = evaluate_milestones(
        selected="N03",
        development_selected_score=Decimal("1"),
        development_identity_score=Decimal("2"),
        assessment_selected_score=Decimal("1"),
        assessment_identity_score=Decimal("2"),
        development_width_wins=5,
        assessment_width_wins=5,
        development_target="NO_RESIDUAL_SIGN_TARGET",
        assessment_target_passed=False,
        questions=[{"id": "Q1", "text": "x"}],
        m5_conditions={"guard": False},
        deterministic_reproduction=True,
        guard_validation=True,
    )
    assert invalid["overall_outcome"] == "INVALID"


def test_byte_deterministic_serialization() -> None:
    payload = {"z": 2, "a": {"y": [2, 1], "x": 3}}
    assert serialise_payload(payload) == serialise_payload(payload)
    assert serialise_payload(payload).endswith(b"\n")


def test_development_plan_is_exact_and_assessment_requires_checkpoint() -> None:
    plan = generation_plan("development")
    validate_generation_plan(plan, phase="development")
    assert plan[0]["start"] == 0
    assert plan[0]["stop"] < 100_000
    assert [(row["start"], row["stop"]) for row in plan[1:]] == [
        (128_000_000, 129_048_576),
        (256_000_000, 257_048_576),
        (512_000_000, 513_048_576),
    ]
    with pytest.raises(ValueError, match="verified committed development checkpoint"):
        generation_plan("assessment")


def test_guard_rejects_before_any_prime_generation(monkeypatch: pytest.MonkeyPatch) -> None:
    called = False

    def forbidden_base(_: int) -> tuple[int, ...]:
        nonlocal called
        called = True
        return ()

    monkeypatch.setattr(
        "experiments.E005_prime_count_scale_calibration._base_primes", forbidden_base
    )
    good = generation_plan("development")

    bad_prefix = [dict(row) for row in good]
    bad_prefix[0]["stop"] = 200_000
    with pytest.raises(ValueError, match="base support|whole-prefix"):
        execute_generation_plan(bad_prefix, phase="development")
    assert called is False

    bad_target_strategy = [dict(row) for row in good]
    bad_target_strategy[1]["strategy"] = "whole_prefix"
    with pytest.raises(ValueError, match="whole-prefix"):
        execute_generation_plan(bad_target_strategy, phase="development")
    assert called is False

    for start, stop in (
        (33_000_000, 34_000_000),
        (37_000_000, 38_000_000),
        (41_000_000, 42_000_000),
        (70_000_000, 71_000_000),
        (78_000_000, 79_000_000),
        (38_000_000, 39_000_000),
        (40_000_000, 41_000_000),
    ):
        bad = [dict(row) for row in good]
        bad[1] = {
            "anchor_name": "D5-0",
            "purpose": "segmented_target",
            "strategy": "segmented",
            "start": start,
            "stop": stop,
        }
        with pytest.raises(ValueError):
            execute_generation_plan(bad, phase="development")
        assert called is False

    widened = [dict(row) for row in good]
    widened[1]["stop"] += 1
    with pytest.raises(ValueError, match="undeclared or widened"):
        execute_generation_plan(widened, phase="development")
    assert called is False

    undeclared = [dict(row) for row in good]
    undeclared[1]["anchor_name"] = "D5-X"
    with pytest.raises(ValueError, match="undeclared or duplicate"):
        execute_generation_plan(undeclared, phase="development")
    assert called is False

    with pytest.raises(ValueError, match="raw-prime serialization"):
        execute_generation_plan(good, phase="development", serialize_raw_primes=True)
    assert called is False


def test_assessment_plan_rejection_precedes_generation(monkeypatch: pytest.MonkeyPatch) -> None:
    called = False

    def forbidden_base(_: int) -> tuple[int, ...]:
        nonlocal called
        called = True
        return ()

    monkeypatch.setattr(
        "experiments.E005_prime_count_scale_calibration._base_primes", forbidden_base
    )
    plan = generation_plan("assessment", development_checkpoint_verified=True)
    with pytest.raises(ValueError, match="verified committed development checkpoint"):
        execute_generation_plan(plan, phase="assessment")
    assert called is False



def test_compact_checkpoint_records_bind_full_artifact_digest() -> None:
    development = {
        "experiment": "E005",
        "lane": "historical_rediscovery_calibration",
        "phase": "development",
        "implementation_commit": "a" * 40,
        "candidate_order": list(CANDIDATES),
        "candidate_scores": {candidate: decimal_string(Decimal(index + 1)) for index, candidate in enumerate(CANDIDATES)},
        "candidate_ranking": list(CANDIDATES),
        "width_spreads": {candidate: {name: decimal_string(Decimal(1)) for name, _ in WIDTHS} for candidate in CANDIDATES},
        "selection": {
            "normalization": "N01",
            "development_width_wins_over_N00": 5,
            "baselines": {name: decimal_string(Decimal(1)) for name, _ in WIDTHS},
            "residual_sign_target": "NO_RESIDUAL_SIGN_TARGET",
            "eligible_questions": [{"id": "Q1", "text": "x"}],
        },
    }
    full = serialise_payload(development)
    checkpoint = build_development_checkpoint(development, full)
    assert checkpoint["phase"] == "development_selection_checkpoint"
    assert checkpoint["development_artifact"]["bytes"] == len(full)
    assert checkpoint["selection"]["normalization"] == "N01"

    assessment = {
        "experiment": "E005",
        "lane": "historical_rediscovery_calibration",
        "phase": "assessment",
        "implementation_commit": "a" * 40,
        "development_checkpoint": {"record_sha256": "0" * 64},
        "candidate_scores": development["candidate_scores"],
        "candidate_ranking": development["candidate_ranking"],
        "width_spreads": development["width_spreads"],
        "selected_normalization_assessment": {
            "normalization": "N01",
            "assessment_width_wins_over_N00": 4,
            "residual_target_evaluation": None,
        },
        "milestones": {"M1": True, "M2": True, "M3": False, "M4": True, "M5": True, "overall_outcome": "STRONG_PASS"},
    }
    assessment_full = serialise_payload(assessment)
    assessment_checkpoint = build_assessment_checkpoint(assessment, assessment_full)
    assert assessment_checkpoint["phase"] == "assessment_checkpoint"
    assert assessment_checkpoint["assessment_artifact"]["bytes"] == len(assessment_full)
    assert assessment_checkpoint["milestones"]["overall_outcome"] == "STRONG_PASS"

def test_development_record_verification(tmp_path: Path) -> None:
    record = {
        "experiment": "E005",
        "phase": "development_selection_checkpoint",
        "implementation_commit": "a" * 40,
        "selection": {
            "normalization": "N01",
            "baselines": {name: "1.000000000000000000000000000000000000000000000000000000000000E+0" for name, _ in WIDTHS},
            "eligible_questions": [],
        },
    }
    data = serialise_payload(record)
    path = tmp_path / "development.json"
    path.write_bytes(data)
    import hashlib

    digest = hashlib.sha256(data).hexdigest()
    loaded = verify_development_record(
        path,
        expected_sha256=digest,
        development_record_commit="b" * 40,
        code_commit="a" * 40,
    )
    assert loaded["selection"]["normalization"] == "N01"
    with pytest.raises(ValueError, match="SHA-256"):
        verify_development_record(
            path,
            expected_sha256="0" * 64,
            development_record_commit="b" * 40,
            code_commit="a" * 40,
        )
