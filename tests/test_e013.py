"""E013 frozen D13 pre-generation semantics, guard, and serializer tests."""
import copy
import importlib.util
from collections import Counter
from math import gcd, isqrt
from pathlib import Path

import pytest

SOURCE = Path(__file__).resolve().parents[1] / "experiments/E013_modular_quadratic_orbit_shapes.py"
spec = importlib.util.spec_from_file_location("e013", SOURCE)
e = importlib.util.module_from_spec(spec)
spec.loader.exec_module(e)


def test_frozen_metadata_and_disjointness():
    e.metadata_check()
    assert len(e.OLD_MILLIONS) == 53 and len(e.E005) == 6
    assert isqrt(72_999_999) == 8544
    assert isqrt(74_999_999) == 8660
    assert isqrt(144_999_999) == 12041
    assert (e.W, e.Q, e.K, e.R30) == (1_000_000, 30, 10, (1, 7, 11, 13, 17, 19, 23, 29))
    assert e.overlap((1, 2), (2, 3)) is False
    assert e.overlap((1, 3), (2, 4)) is True


def test_common_anchor_wheel_and_manual_partition():
    domain = [x for x in range(31, 68) if gcd(x, 30) == 1]
    assert domain == [31, 37, 41, 43, 47, 49, 53, 59, 61, 67]
    prime_labels = {31, 37, 41, 43, 47, 53, 59, 61, 67}  # invented/manual
    p = [x for x in domain if x in prime_labels]
    c = [x for x in domain if x not in prime_labels]
    assert len(p) == 9 and c == [49]
    assert set(p).isdisjoint(c) and set(p) | set(c) == set(domain)
    assert len({x % 30 for x in domain}) == 8


def test_toy_orbit_recurrence_and_tail():
    # Toy modulus 7: 2 -> 5 -> 5 -> 5 etc.; not a generation/primality query.
    ys = e.orbit(7)
    assert ys == (2, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5)
    assert ys[4:11] == (5,) * 7
    assert e.shapes(ys[4:11]) == ("COLLISION",) * 4
    assert e.orbit(11)[:5] == (2, 5, 4, 6, 4)
    assert all(0 <= y < 11 for y in e.orbit(11)[1:])
    assert e.orbit(500_000)[:5] == (2, 5, 26, 677, 458330)
    assert len(e.orbit(500_000)[4:]) == 7


def test_hand_chosen_shapes_and_distinctness():
    assert e.shapes((1, 2, 3, 4, 5, 6, 7)) == (0, 6, (0, 0, 0, 0, 0, 0), 7)
    assert e.shapes((7, 6, 5, 4, 3, 2, 1)) == (6, 0, (1, 1, 1, 1, 1, 1), 1)
    tail = (4, 1, 6, 2, 7, 3, 5)
    assert e.shapes(tail) == (3, 2, (1, 0, 1, 0, 1, 0), 2)
    assert e.shapes((1, 2, 3, 4, 5, 6, 1)) == ("COLLISION",) * 4
    assert e.shapes((1, 3, 2, 5, 4, 7, 6))[0] == 3
    assert e.shapes((2, 3, 1, 5, 4, 7, 6))[0] == 3
    # Same adjacent-comparison word, different nonadjacent record-high count.
    assert e.shapes((1, 4, 2, 5, 3, 6, 0))[2] == e.shapes((3, 4, 1, 5, 2, 6, 0))[2]


def test_mode_tie_strictness_ranking_and_collision():
    assert e.mode_info(Counter({1: 9, 2: 9})) == (None, 9, 2, 9)
    assert e.mode_info(Counter({"COLLISION": 10, 0: 9})) == ("COLLISION", 10, 1, 9)
    assert e.mode_info(Counter({1: 11, 2: 10})) == (1, 11, 1, 10)
    assert e.mode_info(Counter()) == (None, 0, 0, 0)
    assert e.signature_json((1, 0, 1, 0, 1, 0)) == [1, 0, 1, 0, 1, 0]


def test_mixing_four_counts_and_exact_integer_enrichment():
    ppop = Counter({r: 100 for r in e.R30})
    cpop = Counter({r: 100 for r in e.R30})
    pc = {r: Counter({"t": 1}) for r in e.R30}
    cc = {r: Counter({"t": 99}) for r in e.R30}
    assert e.mixed_count("t", pc, cc, ppop, cpop) == 8
    cc[e.R30[0]]["t"] = 100
    cc[e.R30[1]]["t"] = 0
    assert e.mixed_count("t", pc, cc, ppop, cpop) == 6
    cc[e.R30[2]]["t"] = 0
    assert e.mixed_count("t", pc, cc, ppop, cpop) == 5
    assert e.enrichment(5, 4, 100, 100) == 100
    assert e.enrichment(4, 4, 100, 100) == 0
    assert e.enrichment(3, 4, 100, 100) == -100
    assert e.enrichment(8, 3, 50, 100) == 650


def fabricated(mode_supports=None):
    modes = [1, 2, (0, 1, 0, 1, 0, 1), 3]
    pc, cc, pby, cby, support = [], [], [], [], []
    for i, mode in enumerate(modes):
        pc.append(Counter({mode: 800, "COLLISION": 500, -1: 300}))
        cc.append(Counter({mode: 160, "COLLISION": 1000, -1: 440}))
        pby.append({r: Counter({mode: 100, "COLLISION": 60, -1: 40}) for r in e.R30})
        cby.append({r: Counter({mode: 20, "COLLISION": 125, -1: 55}) for r in e.R30})
        support.append({mode: set(range(1000 * i, 1000 * i + 800)) if mode_supports is None else mode_supports[i]})
    pop = Counter({r: 200 for r in e.R30})
    return pc, cc, pby, cby, pop, pop.copy(), support, {k: 0 for k in e.VALIDATION_KEYS}


def test_floors_duplicate_suppression_cap_and_failure_injection():
    args = fabricated()
    rows, promoted = e.choose_rows(*args)
    assert len(rows) == len(promoted) == 4
    assert [v["family"] for v in promoted] == list(e.FAMILIES)
    dup = [set(range(800)), set(range(800)), set(range(2000, 2800)), set(range(3000, 3800))]
    rows, promoted = e.choose_rows(*fabricated(dup))
    assert [v["family"] for v in promoted] == ["O1", "O3", "O4"]
    assert rows[1]["mechanically_eligible"] is False
    args = list(fabricated())
    args[-1]["family_identity_failure_count"] = 1
    rows, promoted = e.choose_rows(*args)
    assert promoted == [] and all(not r["mechanically_eligible"] for r in rows)
    args = list(fabricated())
    args[4][1] = 99
    with pytest.raises(AssertionError, match="conservation"):
        e.choose_rows(*args)
    args = list(fabricated())
    args[0][0] = Counter({"COLLISION": 900, 1: 700})
    assert [v["family"] for v in e.choose_rows(*args)[1]] == ["O2", "O3", "O4"]
    args = list(fabricated())
    args[0][0] = Counter({1: 800, 2: 800})
    assert [v["family"] for v in e.choose_rows(*args)[1]] == ["O2", "O3", "O4"]


def test_poison_generators_every_negative_plan():
    valid = e.plan_d13()
    touched = []
    def poison(*args):
        touched.append(args)
        raise AssertionError("generator reached")
    e.authorize(valid, "D13")
    invalid = []
    for entry in range(2):
        for field, value in (("start", -1), ("stop", valid[entry]["stop"] - 1),
                             ("stop", valid[entry]["stop"] + 1), ("strategy", "whole_prefix" if entry else "segmented")):
            changed = copy.deepcopy(valid)
            changed[entry][field] = value
            invalid.append(changed)
    invalid.extend([[], valid[:1], valid[::-1], valid + [valid[-1]],
                    [valid[0], valid[1], valid[1]],
                    [{**valid[0], "stop": 73_000_000}, valid[1]],
                    [valid[0], {**valid[1], "extra": 1}]])
    excluded = list(e.PARTITION[i][1] for i in (0, 2, 3, 4))
    excluded += [(a * e.W, b * e.W) for a, b in e.OLD_MILLIONS]
    excluded += list(e.E005)
    excluded += [(start, start + 4_096) for start, _ in e.E005]
    excluded += [(69_000_000, 70_000_000), (134_000_000, 135_000_000),
                 (66_000_000, 67_000_000), (70_000_000, 71_000_000),
                 (90_000_000, 91_000_000)]
    for start, stop in excluded:
        invalid.append([valid[0], {**valid[1], "start": start, "stop": stop}])
    for bad in invalid:
        with pytest.raises(ValueError):
            e.generate(bad, "D13", poison, poison)
    for phase in ("H13", "A13", "G13-pre", "D12", "OTHER"):
        with pytest.raises(ValueError):
            e.generate(valid, phase, poison, poison)
    assert touched == []
    with pytest.raises(AssertionError, match="generator reached"):
        e.generate(valid, "D13", poison, poison)
    assert len(touched) == 1


def test_narrow_json_and_byte_determinism():
    args = fabricated()
    rows, promotions = e.choose_rows(*args)
    payload = {
        "experiment": "E013", "implementation_commit": "a" * 40,
        "band": {"name": "D13", "range": [72_000_000, 73_000_000], "interval_semantics": "half-open"},
        "partition": [{"name": n, "range": list(b), "role": role} for n, b, role in e.PARTITION],
        "parameters": {"width": e.W, "wheel": e.Q, "reduced_residues": list(e.R30),
                       "seed": 2, "polynomial_map": "y^2+1 mod x", "steps": 10,
                       "tail_start": 4, "tail_length": 7, "population_floor": 1000,
                       "class_floor": 100, "occurrence_floor": 32, "mixed_class_floor": 6},
        "generation_plan": e.plan_d13(),
        "anchor_summary": {"anchor_count": 3200, "prime_count": 1600, "composite_count": 1600,
                           "first_prime": None, "last_prime": None,
                           "prime_counts_by_R30": [200] * 8, "composite_counts_by_R30": [200] * 8,
                           "collision_prime_count": 0, "collision_composite_count": 0},
        "validation": {k: 0 for k in e.VALIDATION_KEYS}, "families": rows,
        "promotions": promotions,
    }
    output = e.canonical_json(payload)
    assert output == e.canonical_json(copy.deepcopy(payload)) and output.endswith(b"\n")
    assert b"\"raw_orbits\"" not in output
    forbidden = {
        "": ("prime_list", "timings", "complete_frequency_table", "per_anchor_x"),
        "band": ("timestamp", "host", "non_modes"),
        "partition": ("guard_primes", "paths"),
        "parameters": ("alternate_seed", "factorization"),
        "generation_plan": ("extra_support",),
        "anchor_summary": ("per_anchor_orbits", "prime_list", "per_residue_target_counts"),
        "validation": ("diagnostics",),
        "families": ("second_mode_signature", "support_set", "residue_target_counts"),
        "promotions": ("anchor_set", "rank_words"),
    }
    for section, names in forbidden.items():
        for name in names:
            changed = copy.deepcopy(payload)
            obj = changed if not section else changed[section]
            (obj[0] if isinstance(obj, list) else obj)[name] = 123
            with pytest.raises(ValueError):
                e.canonical_json(changed)
    changed = copy.deepcopy(payload)
    changed["families"][2]["unique_mode_signature"] = [0, 1, 0]
    with pytest.raises(ValueError):
        e.canonical_json(changed)
    changed = copy.deepcopy(payload)
    changed["validation"]["plan_failure_count"] = 1
    with pytest.raises(ValueError):
        e.canonical_json(changed)