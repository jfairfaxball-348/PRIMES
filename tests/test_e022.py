"""Independent bounded E022 synthetic evaluator, poison and strict-schema checks."""
import copy
import importlib.util
import json
from itertools import product
from math import gcd
from pathlib import Path

import pytest

SOURCE = Path(__file__).resolve().parents[1] / "experiments" / "E022_proper_cycle_colouring_residue_order_shapes.py"
spec = importlib.util.spec_from_file_location("e022", SOURCE)
e = importlib.util.module_from_spec(spec)
spec.loader.exec_module(e)


def test_independent_direct_cycle_colouring_trace_and_modular_pow():
    for n in range(3, 7):
        for q in (3, 4):
            # Enumerate independently: all q-labelled vertex assignments,
            # explicitly including closing edge n-1 -> 0.
            direct = 0
            for words in product(range(q), repeat=n):
                if all(words[i] != words[(i + 1) % n] for i in range(n)):
                    direct += 1
            trace = e.closed_walk_trace(n, q)
            formula = (q - 1)**n + (q - 1) * (-1)**n
            assert direct == trace == formula
            assert e.colour_remainder(n, q) == direct % (n + 1)
    assert e.synthetic_failures() == (0, 0, 0)


def test_three_way_order_and_boundaries_and_validation_errors():
    assert {e.signature_from_remainders(7, a, b)
            for a in range(8) for b in range(8)} == {0, 1, 2}
    assert e.signature_from_remainders(7, 1, 3) == 0
    assert e.signature_from_remainders(7, 3, 3) == 1
    assert e.signature_from_remainders(7, 3, 1) == 2
    for x, a, b in ((2, 0, 1), (3, 0, 4), (3, -1, 0), (3, True, 0)):
        with pytest.raises(ValueError):
            e.signature_from_remainders(x, a, b)
    assert e.triviality_clear()
    for x in (3, 4, 13, 17):
        assert e.signature(x) in e.SIGNATURES


def test_role_exclusion_is_reconstructed_and_exhaustive():
    assert len(e.EARLY.strip().splitlines()) == 53
    assert len(e.old_intervals()) == 104
    assert len(e.E005_STARTS) * len(e.E005_WIDTHS) == 30
    assert e.audit_intervals() == dict(
        old_old=5356, new_old=520, new_new=10, new_nested=150,
        old_non_e005_nested=2940, nested_contained=30,
        nested_within=60, nested_across=375,
    )
    assert e.R210 == tuple(i for i in range(210) if gcd(i, 210) == 1)
    assert e.PLAN == (
        ("base_sieve_support", 0, 12570, "whole_prefix"),
        ("segmented_target", 156000000, 158000000, "direct_segmented"),
    )


def test_mode_strict_ties_and_one_set_support_cap():
    assert e.mode([9, 7, 8]) == (0, 9, 8)
    assert e.mode([8, 8, 4]) == (None, 8, 8)
    assert e.mode([2, 1, 9]) == (2, 9, 2)
    assert e.mode([0, 0, 0]) == (None, 0, 0)
    already = []
    assert e.dedup_support({11, 19}, already)
    assert not e.dedup_support({19, 11}, already)
    assert not e.dedup_support({11, 21}, already)
    assert already == [{11, 19}]
    with pytest.raises(ValueError):
        e.dedup_support({True}, [])


def test_negative_whole_plan_poison_before_any_generator(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("prime generator entered on negative plan")
    monkeypatch.setattr(e, "base_sieve", forbidden)
    monkeypatch.setattr(e, "target_segment", forbidden)
    allowed = e.PLAN
    poisons = [
        allowed[::-1], allowed[:1], allowed + (allowed[1],),
        (("base_sieve_support", 0, 158000000, "whole_prefix"), allowed[1]),
        (("base_sieve_support", 0, 12570, "direct_segmented"), allowed[1]),
        (allowed[0], ("segmented_target", 156000000, 158000000, "whole_prefix")),
        (allowed[0], ("segmented_target", 156000000, 157999999, "direct_segmented")),
        (allowed[0], ("segmented_target", 156000001, 158000000, "direct_segmented")),
        (allowed[0], ("segmented_target", 160000000, 162000000, "direct_segmented")),
        (allowed[0], ("segmented_target", 312000000, 314000000, "direct_segmented")),
        (allowed[0], ("segmented_target", True, 158000000, "direct_segmented")),
    ]
    for i in range(2):
        for slot in (1, 2):
            for delta in (-1, 1):
                copy_plan = [list(row) for row in allowed]
                copy_plan[i][slot] += delta
                poisons.append(tuple(map(tuple, copy_plan)))
    for _, a, b in e.old_intervals():
        poisons.append((allowed[0], ("segmented_target", a, b, "direct_segmented")))
    for n, a, b, _ in e.ROLES:
        if n != "D22":
            poisons.append((allowed[0], ("segmented_target", a, b, "direct_segmented")))
    for s in e.E005_STARTS:
        for w in e.E005_WIDTHS:
            poisons.append((allowed[0], ("segmented_target", s, s+w, "direct_segmented")))
    for plan in poisons:
        with pytest.raises(ValueError):
            e.GeneratorGate(plan)
    for phase in ("H22", "A22", "G22-pre", "E021", "D21", "H19"):
        with pytest.raises(ValueError):
            e.GeneratorGate(allowed, phase=phase)
    for opts in ({"indirect": True}, {"per_anchor": True}):
        with pytest.raises(ValueError):
            e.GeneratorGate(allowed, **opts)
    assert len(poisons) >= 145


def test_ordered_generator_entries_and_replay_poison():
    gate = e.GeneratorGate()
    with pytest.raises(ValueError):
        gate.enter(1, *e.PLAN[1])
    with pytest.raises(ValueError):
        gate.enter(0, "base_sieve_support", 0, 12571, "whole_prefix")
    gate.enter(0, *e.PLAN[0])
    with pytest.raises(ValueError):
        gate.enter(0, *e.PLAN[0])
    gate.enter(1, *e.PLAN[1])
    gate.finished()
    with pytest.raises(ValueError):
        gate.enter(1, *e.PLAN[1])
    with pytest.raises(ValueError):
        e.GeneratorGate((e.PLAN[0], e.PLAN[1][:3]))


def test_synthetic_direct_segmented_equivalence_unprotected_toy_only():
    # Verify the arithmetical sieve formula with independent trial division;
    # none of these integers is in or near a protected high role.
    from primes_lab.core import sieve
    low = sieve(14)
    a, b = 103, 201
    marks = e.target_segment(a, b, low)
    expected = [n >= 2 and all(n % p for p in range(2, int(n**0.5)+1))
                for n in range(a, b)]
    assert list(map(bool, marks)) == expected


def test_typed_schema_and_canonical_rejection_without_prime_labels():
    # Synthetic small count cells only, not a D22 or historical result.
    f = dict(
        family="R1", prime_mode_count=144, highest_competing_prime_count=96,
        strict_unique_prime_mode=True, candidate_signature=2,
        evaluated_signature=2, target_prime_count=144, target_composite_count=288,
        population_floor_passed=False, class_floor_passed=False,
        occurrence_floor_passed=True, mixed_class_count=48,
        mixed_class_floor_passed=True, positive_class_count=0,
        positive_class_floor_passed=False, target_enrichment_numerator=-6912,
        target_enrichment_positive=False, mechanically_eligible=False,
    )
    data = dict(
        experiment="E022", implementation_commit="1"*40,
        band=dict(name="D22", range=[156000000, 158000000],
                  interval_semantics="half-open"),
        partition=[dict(name=n, range=[a, b], role=role) for n, a, b, role in e.ROLES],
        parameters=e.PARAMETERS, generation_plan=e.plan_dicts(),
        anchor_summary=dict(
            wheel_anchor_count=1008, prime_count=288, composite_count=720,
            prime_counts_by_R210=[6]*48, composite_counts_by_R210=[15]*48,
        ), validation=dict.fromkeys(e.VALIDATORS, 0), families=[f], promotions=[],
    )
    # Adjustment: synthetic signed E(2) = 144*720 - 288*288 = 20736.
    data["families"][0]["target_enrichment_numerator"] = 20736
    data["families"][0]["target_enrichment_positive"] = True
    assert e.validate_payload(data)
    raw = e.canonical(data)
    assert raw == e.canonical(json.loads(raw))
    assert raw.endswith(b"\n") and not raw.endswith(b"\n\n")
    bad = copy.deepcopy(data)
    bad["unexpected"] = 0
    assert not e.validate_payload(bad)
    bad = copy.deepcopy(data)
    bad["validation"]["serializer_failure_count"] = False
    assert not e.validate_payload(bad)
    bad = copy.deepcopy(data)
    bad["parameters"]["population_floor"] = True
    assert not e.validate_payload(bad)
    bad = copy.deepcopy(data)
    bad["parameters"]["residues_R210"][0] = True
    assert not e.validate_payload(bad)
    bad = copy.deepcopy(data)
    bad["band"]["range"][0] = True
    assert not e.validate_payload(bad)
    bad = copy.deepcopy(data)
    bad["anchor_summary"]["prime_count"] = 288.0
    assert not e.validate_payload(bad)
    bad = copy.deepcopy(data)
    bad["families"][0]["candidate_signature"] = True
    assert not e.validate_payload(bad)
    bad = copy.deepcopy(data)
    bad["families"][0]["extra"] = 0
    assert not e.validate_payload(bad)
    bad = copy.deepcopy(data)
    bad["promotions"] = [{}]
    assert not e.validate_payload(bad)
