"""Focused H13 frozen semantics, serializer and poison-generator preflight tests."""
import copy
import importlib.util
from collections import Counter
from math import isqrt
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location(
    "h13", Path(__file__).resolve().parents[1] / "experiments/E013_h13_replication.py"
)
e = importlib.util.module_from_spec(spec)
spec.loader.exec_module(e)


def test_metadata_and_plan():
    e.metadata_check()
    assert e.plan_h13() == [
        {"purpose": "base_sieve_support", "start": 0, "stop": 8661, "strategy": "whole_prefix"},
        {"purpose": "segmented_target", "start": 74_000_000, "stop": 75_000_000, "strategy": "segmented"},
    ]
    assert isqrt(74_999_999) == 8660
    assert e.TARGETS == (("OBS-018", "O1", 3), ("OBS-019", "O2", 2))


def test_manual_orbit_and_collision():
    assert e.orbit_signatures(7) == ("COLLISION", "COLLISION")
    assert e.shapes((1, 2, 3, 4, 5, 6, 7)) == (0, 6)
    assert e.shapes((7, 6, 5, 4, 3, 2, 1)) == (6, 0)
    assert e.shapes((4, 1, 6, 2, 7, 3, 5)) == (3, 2)
    assert e.shapes((1, 2, 3, 4, 5, 6, 1)) == ("COLLISION", "COLLISION")
    assert e.orbit_signatures(500_000)[0] in range(7)
    assert e.orbit_signatures(500_000)[1] in range(7)
    with pytest.raises(ValueError):
        e.orbit_signatures(2)


def test_criterion_all_gates_and_failures():
    pp, cp = Counter({r: 200 for r in e.R30}), Counter({r: 200 for r in e.R30})
    pc, cc = Counter({3: 900, 1: 700}), Counter({3: 200, 1: 1400})
    pby = {r: Counter({3: 112, 1: 88}) for r in e.R30}
    cby = {r: Counter({3: 25, 1: 175}) for r in e.R30}
    fail = {key: 0 for key in e.VALIDATION_KEYS}
    result = e.criterion(pc, cc, pby, cby, pp, cp, 3, "OBS-018", "O1", fail)
    assert result["status"] == "REPLICATED"
    assert result["mixed_class_count"] == 8
    assert result["aggregate_enrichment_numerator"] == 1_120_000
    pc[1] = 900
    assert e.criterion(pc, cc, pby, cby, pp, cp, 3, "OBS-018", "O1", fail)["status"] == "REFUTED"
    pc[1] = 700
    cby[e.R30[0]][3] = 0
    cby[e.R30[1]][3] = 200
    cby[e.R30[2]][3] = 0
    assert e.criterion(pc, cc, pby, cby, pp, cp, 3, "OBS-018", "O1", fail)["status"] == "REFUTED"
    for r in e.R30[:3]:
        cby[r][3] = 25
    fail["family_identity_failure_count"] = 1
    assert e.criterion(pc, cc, pby, cby, pp, cp, 3, "OBS-018", "O1", fail)["status"] == "REFUTED"
    fail["family_identity_failure_count"] = 0
    cc[3] = 900
    assert e.criterion(pc, cc, pby, cby, pp, cp, 3, "OBS-018", "O1", fail)["status"] == "REFUTED"
    cc[3] = 200
    pp[1] = 99
    assert e.criterion(pc, cc, pby, cby, pp, cp, 3, "OBS-018", "O1", fail)["status"] == "REFUTED"


def test_poison_generator_before_entry():
    valid = e.plan_h13()
    touched = []
    def poison(*args):
        touched.append(args)
        raise AssertionError("generator reached")
    e.authorize(valid, "H13")
    bad = [[], valid[:1], valid[::-1], valid + [valid[1]],
           [{**valid[0], "stop": 75_000_000}, valid[1]],
           [valid[0], {**valid[1], "strategy": "whole_prefix"}],
           [valid[0], {**valid[1], "extra": True}]]
    for index in (0, 1):
        for field, change in (("start", -1), ("stop", -1), ("stop", 1)):
            altered = copy.deepcopy(valid)
            altered[index][field] += change
            bad.append(altered)
    excluded = [r[1] for i, r in enumerate(e.PARTITION) if i != 3]
    excluded += [(a * e.W, b * e.W) for a, b in e.OLD_MILLIONS]
    excluded += list(e.E005)
    excluded += [(a, a + 4096) for a, _ in e.E005]
    excluded += [(69_000_000, 70_000_000), (134_000_000, 135_000_000),
                 (66_000_000, 67_000_000), (70_000_000, 71_000_000),
                 (90_000_000, 91_000_000)]
    for a, b in excluded:
        bad.append([valid[0], {**valid[1], "start": a, "stop": b}])
    for plan in bad:
        with pytest.raises(ValueError):
            e.generate(plan, "H13", poison, poison)
    for phase in ("D13", "A13", "G13-pre", "G13-mid", "H12", "OTHER"):
        with pytest.raises(ValueError):
            e.generate(valid, phase, poison, poison)
    assert touched == []
    with pytest.raises(AssertionError, match="generator reached"):
        e.generate(valid, "H13", poison, poison)
    assert len(touched) == 1


def test_serializer_strict_allowlist_and_determinism():
    p = {
        "experiment": "E013", "implementation_commit": "a" * 40,
        "band": {"name": "H13", "range": list(e.H13), "interval_semantics": "half-open"},
        "partition": [{"name": n, "range": list(b), "role": role} for n, b, role in e.PARTITION],
        "parameters": {"width": e.W, "wheel": e.Q, "reduced_residues": list(e.R30),
                       "seed": 2, "polynomial_map": "y^2+1 mod x", "steps": 10,
                       "tail_start": 4, "tail_length": 7, "population_floor": 1000,
                       "class_floor": 100, "occurrence_floor": 32, "mixed_class_floor": 6},
        "generation_plan": e.plan_h13(),
        "anchor_summary": {"anchor_count": 266666, "prime_count": 1000,
                           "composite_count": 265666, "prime_counts_by_R30": [125] * 8,
                           "composite_counts_by_R30": [33208] * 8},
        "validation": {key: 0 for key in e.VALIDATION_KEYS},
        "replications": [
            {"observation": obs, "family": fam, "frozen_target": target,
             "target_prime_count": 500, "highest_competing_prime_count": 100,
             "target_composite_count": 200, "population_floor_passed": True,
             "class_floor_passed": True, "strict_unique_target_mode": True,
             "occurrence_floor_passed": True, "mixed_class_count": 8,
             "mixed_class_floor_passed": True, "aggregate_enrichment_numerator": 10,
             "aggregate_enrichment_positive": True, "status": "REPLICATED"}
            for obs, fam, target in e.TARGETS],
    }
    a = e.canonical_json(p)
    assert a == e.canonical_json(copy.deepcopy(p)) and a.endswith(b"\n")
    for key, subsection in (("rogue", None), ("prime_list", "anchor_summary"),
                            ("target_counts_by_class", "replications"),
                            ("alternate_seed", "parameters"), ("extra", "generation_plan")):
        altered = copy.deepcopy(p)
        obj = altered if subsection is None else altered[subsection]
        (obj[0] if isinstance(obj, list) else obj)[key] = 123
        with pytest.raises(ValueError):
            e.canonical_json(altered)
    altered = copy.deepcopy(p)
    altered["validation"]["plan_failure_count"] = 1
    with pytest.raises(ValueError):
        e.canonical_json(altered)
    altered = copy.deepcopy(p)
    altered["replications"][1]["frozen_target"] = 3
    with pytest.raises(ValueError):
        e.canonical_json(altered)
