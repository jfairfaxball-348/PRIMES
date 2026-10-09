"""Generator-free independent E025 synthetic, algebraic and poison tests."""
from __future__ import annotations

from functools import cache
from math import factorial, gcd, isqrt
from pathlib import Path

import pytest

from experiments import e025_three_row_young_tableau_linear_extension_remainder_octiles as e


def independent_poset_extensions(k: int) -> int:
    """Independent box-poset predecessor subset DP, not ballot words."""
    boxes = [(i, j) for i in range(3) for j in range(k)]
    ix = {b: n for n, b in enumerate(boxes)}
    before = []
    for i, j in boxes:
        pred = 0
        if j:
            pred |= 1 << ix[(i, j - 1)]
        if i:
            pred |= 1 << ix[(i - 1, j)]
        before.append(pred)

    @cache
    def extensions(mask: int) -> int:
        if mask == (1 << len(boxes)) - 1:
            return 1
        total = 0
        for n, requirements in enumerate(before):
            if not mask & (1 << n) and mask & requirements == requirements:
                total += extensions(mask | (1 << n))
        return total

    return extensions(0)


def test_independent_ballot_poset_hook_recurrence() -> None:
    # Three independent representations: poset order ideals, chamber words,
    # factorial quotient, plus exact checked adjacent recurrence.
    for k, expected in enumerate((1, 1, 5, 42, 462)):
        assert independent_poset_extensions(k) == expected
        assert e.ballot_reference(k) == expected
        assert e.hook_quotient(k) == expected
        assert e.tableau_window(k, k)[k] == expected
    assert factorial(0) == 1
    assert e.tableau_window(0, 4) == dict(enumerate((1, 1, 5, 42, 462)))
    e.independent_small_checks()


def test_octile_fixtures_exact_boundaries_and_types() -> None:
    examples = ((1, 1, 4), (3, 1, 2), (4, 5, 0), (8, 5, 4),
                (9, 42, 1), (15, 42, 5), (16, 462, 1))
    for x, t, expected in examples:
        assert e.signature(x, t) == expected
    for m in range(1, 101):
        for r in range(m):
            value = e.octile_from_remainder(r, m)
            assert 0 <= value <= 7
            assert value == sum(8 * r >= i * m for i in range(1, 8))
            if 8 * r % m == 0:
                assert value == 8 * r // m
    for pair in ((-1, 7), (7, 7), (8, 7), (1, 0), (True, 10), (1, False)):
        with pytest.raises(ValueError):
            e.octile_from_remainder(*pair)
    with pytest.raises(ValueError):
        e.ballot_reference(5)
    with pytest.raises(ValueError):
        e.hook_quotient(-1)
    for invalid in ((-1, 1), (2, 1), (2.0, 2), (False, 2)):
        with pytest.raises(ValueError):
            e.tableau_window(*invalid)


def design() -> str:
    return Path("experiments/E025_THREE_ROW_YOUNG_TABLEAU_LINEAR_EXTENSION_REMAINDER_OCTILES.md").read_text()


def test_integer_named_exclusion_full_counts() -> None:
    old = e.audit_named_intervals(design())
    assert len(old) == 149
    maximum = {n: b for n, b in old.items() if n.endswith("-maximum")}
    nested = {n: b for n, b in old.items() if "-nested-" in n}
    prior = {n: b for n, b in old.items() if n not in nested}
    assert len(prior) == 119 and len(nested) == 30 and len(maximum) == 6
    assert len(prior) * (len(prior) - 1) // 2 == 7021
    assert len(prior) * 5 == 595
    assert 5 * len(nested) == 150
    assert (len(prior) - 6) * len(nested) == 3390
    assert len(e.PARTITION) * (len(e.PARTITION) - 1) // 2 == 10
    overlap = e.overlaps
    assert all(not overlap(a, b) for i, a in enumerate(prior.values())
               for b in list(prior.values())[i + 1:])
    assert all(not overlap((a, b), ob) for _, a, b, _ in e.PARTITION for ob in old.values())
    assert all(not overlap((a, b), (c, d)) for i, (_, a, b, _) in enumerate(e.PARTITION)
               for _, c, d, _ in e.PARTITION[i + 1:])
    nest_pairs = list(nested.items())
    assert sum(overlap(a, b) for i, (_, a) in enumerate(nest_pairs)
               for _, b in nest_pairs[i + 1:]) == 60
    assert sum(not overlap(a, b) for i, (_, a) in enumerate(nest_pairs)
               for _, b in nest_pairs[i + 1:]) == 375
    assert all(maximum[n.split("-nested-")[0] + "-maximum"][0] <= a
               < b <= maximum[n.split("-nested-")[0] + "-maximum"][1]
               for n, (a, b) in nested.items())
    assert isqrt(e.HIGH - 1) == 14560
    assert 14560**2 <= e.HIGH - 1 < 14561**2
    assert e.RESIDUES == tuple(x for x in range(210) if gcd(x, 210) == 1)


def test_whole_plan_poisons_before_any_generator(monkeypatch: pytest.MonkeyPatch) -> None:
    calls = []
    real_low = e.low_base_sieve
    real_direct = e.direct_target_mask
    monkeypatch.setattr(e, "low_base_sieve", lambda *args: calls.append(args))
    monkeypatch.setattr(e, "direct_target_mask", lambda *args: calls.append(args))
    source = design()
    e.assert_plan(e.PLAN, source)
    for i in (0, 1):
        e.generation_entry(i, e.PLAN, source, "D25")
    bad = [
        (), (e.PLAN[0],), (e.PLAN[1],), tuple(reversed(e.PLAN)),
        e.PLAN + (e.PLAN[1],), [*e.PLAN],
        (("base_sieve_support", 0, 14560, "whole_prefix"), e.PLAN[1]),
        (("base_sieve_support", 0, 14562, "whole_prefix"), e.PLAN[1]),
        (("base_sieve_support", 1, 14561, "whole_prefix"), e.PLAN[1]),
        (("base_sieve_support", 0, 14561, "direct_segmented"), e.PLAN[1]),
        (("whole_prefix", 0, e.HIGH, "whole_prefix"), e.PLAN[1]),
        (e.PLAN[0], ("segmented_target", e.LOW, e.HIGH, "whole_prefix")),
        (e.PLAN[0], ("segmented_target", e.LOW, e.HIGH, "filtered_whole_prefix")),
        (e.PLAN[0], ("segmented_target", 0, e.HIGH, "direct_segmented")),
        (e.PLAN[0], ("segmented_target", e.LOW + 1, e.HIGH, "direct_segmented")),
        (e.PLAN[0], ("segmented_target", e.LOW - 1, e.HIGH, "direct_segmented")),
        (e.PLAN[0], ("segmented_target", e.LOW, e.HIGH - 1, "direct_segmented")),
        (e.PLAN[0], ("segmented_target", e.LOW, e.HIGH + 1, "direct_segmented")),
        (e.PLAN[0], ("segmented_target", 214_000_000, 216_000_000, "direct_segmented")),
        (e.PLAN[0], ("segmented_target", 184_000_000, 186_000_000, "direct_segmented")),
        (e.PLAN[0], ("segmented_target", 128_000_000, 128_004_096, "direct_segmented")),
        (e.PLAN[0], ("segmented_target", 420_000_000, 422_000_000, "direct_segmented")),
    ]
    for plan in bad:
        with pytest.raises(PermissionError):
            e.assert_plan(plan, source)
    for phase in ("H25", "A25", "G25-pre", "D24", "D23", "D19", ""):
        with pytest.raises(PermissionError):
            e.assert_plan(e.PLAN, source, phase)
    for bad_index in (-1, 2, 3, 1.0, True):
        with pytest.raises(PermissionError):
            e.generation_entry(bad_index, e.PLAN, source, "D25")
    # Helpers cannot run on any nonexact range, even without plan callback.
    with pytest.raises(PermissionError):
        real_low(14562)
    with pytest.raises(PermissionError):
        real_direct(e.LOW, e.HIGH + 1, [])
    assert calls == []


def test_independent_triviality_counterexamples() -> None:
    assert e.independent_triviality_veto()


def test_strict_selector_signed_classes_no_fallback() -> None:
    prime = [[0] * 8 for _ in range(48)]
    comp = [[0] * 8 for _ in range(48)]
    for i in range(48):
        prime[i][0], prime[i][1] = 30, 10
        comp[i][0], comp[i][1] = 20, 30
    f, promotions = e.candidate_analysis(prime, comp)
    assert f["candidate_signature"] == 0 and f["strict_unique_prime_mode"]
    assert f["prime_mode_count"] == 1440 and f["highest_competing_prime_count"] == 480
    assert f["mixed_class_count"] == 48 and f["positive_class_count"] == 48
    assert f["target_enrichment_numerator"] > 0
    assert not f["population_floor_passed"]  # 1920 primes, before floor
    assert f["triviality_veto_passed"] and not f["mechanically_eligible"]
    assert promotions == []
    for row in prime:
        row[1] = row[0]
    f, promotions = e.candidate_analysis(prime, comp)
    assert f["candidate_signature"] is None
    assert f["evaluated_signature"] is None and not f["strict_unique_prime_mode"]
    assert f["target_enrichment_numerator"] is None
    assert f["target_prime_count"] is None and f["positive_class_count"] is None
    assert promotions == []


def test_canonical_bytes_reject_noninteger_nonascii_and_nested_schema() -> None:
    sample = {
        "experiment": "E025", "implementation_commit": "a" * 40,
        "band": {"name": "D25", "range": [e.LOW, e.HIGH], "interval_semantics": "half-open"},
        "partition": [{"name": n, "range": [a, b], "role": role} for n, a, b, role in e.PARTITION],
        "generation_plan": [{"purpose": p, "start": a, "stop": b, "strategy": s}
                            for p, a, b, s in e.PLAN],
        "parameters": {
            "width": 2_000_000, "wheel": 210, "residues_R210": list(e.RESIDUES),
            "rows": 3, "index_rule": "isqrt_x",
            "object": "three_row_rectangular_standard_young_tableau_linear_extensions",
            "modulus": "anchor_plus_one", "feature": "tableau_remainder_octile",
            "signature_domain": list(e.STATES), "selector": "strict_unique_prime_frequency_mode",
            "population_floor": 2000, "class_floor": 20, "occurrence_floor": 64,
            "mixed_class_floor": 36, "positive_class_floor": 36,
            "support_cap": 1, "full_mixed_required": True,
        },
        "anchor_summary": {"wheel_anchor_count": 0, "prime_count": 0,
                           "composite_count": 0, "prime_counts_by_R210": [0] * 48,
                           "composite_counts_by_R210": [0] * 48},
        "families": [{
            "family": "F1", "prime_mode_count": 0,
            "highest_competing_prime_count": 0, "strict_unique_prime_mode": False,
            "candidate_signature": None, "evaluated_signature": None,
            "target_prime_count": None, "target_composite_count": None,
            "population_floor_passed": False, "class_floor_passed": False,
            "occurrence_floor_passed": False, "mixed_class_count": None,
            "mixed_class_floor_passed": False, "positive_class_count": None,
            "positive_class_floor_passed": False, "target_enrichment_numerator": None,
            "target_enrichment_positive": False, "triviality_veto_passed": False,
            "mechanically_eligible": False,
        }], "promotions": [], "validation": {k: 0 for k in e.VALIDATORS},
    }
    e.payload_schema(sample)
    raw = e.canonical(sample)
    assert raw[-1:] == b"\n" and raw.count(b"\r") == 0
    assert e.canonical(__import__("json").loads(raw)) == raw
    sample["validation"]["plan_failure_count"] = False
    with pytest.raises(ValueError):
        e.payload_schema(sample)
    sample["validation"]["plan_failure_count"] = 0
    sample["parameters"]["rows"] = True
    with pytest.raises(ValueError):
        e.payload_schema(sample)
    sample["parameters"]["rows"] = 3
    sample["anchor_summary"]["prime_counts_by_R210"][0] = 0.0
    with pytest.raises(ValueError):
        e.payload_schema(sample)
    sample["anchor_summary"]["prime_counts_by_R210"][0] = 0
    sample["families"][0]["extra_key"] = 1
    with pytest.raises(ValueError):
        e.payload_schema(sample)
