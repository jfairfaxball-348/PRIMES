"""E014 D14 pre-generation-only tests: invented labels, no primality or prime generation."""
import copy
import importlib.util
from collections import Counter
from math import gcd, isqrt
from pathlib import Path

import pytest

SOURCE = Path(__file__).resolve().parents[1] / "experiments/E014_primitive_three_cube_incidence_shapes.py"
spec = importlib.util.spec_from_file_location("e014", SOURCE)
e = importlib.util.module_from_spec(spec)
spec.loader.exec_module(e)


def fabricated(supports=None):
    ppop = Counter({r: 100 for r in e.R90})
    cpop = Counter({r: 100 for r in e.R90})
    modes = (1, 2)
    pf, cf, pb, cb, supp = [], [], [], [], []
    for j, t in enumerate(modes):
        pf.append(Counter({t: 960, 3: 320, 4: 320}))
        cf.append(Counter({t: 320, 3: 640, 4: 640}))
        pb.append({r: Counter({t: 60, 3: 20, 4: 20}) for r in e.R90})
        cb.append({r: Counter({t: 20, 3: 40, 4: 40}) for r in e.R90})
        supp.append({t: set(range(960 * j, 960 * (j + 1))) if supports is None else supports[j]})
    return pf, cf, pb, cb, ppop, cpop, supp, {k: 0 for k in e.VALIDATION_KEYS}


def test_metadata_partition_and_exact_square_cube_bounds():
    assert e.metadata_check() == 330
    assert (len(e.OLD_MILLIONS), len(e.E013_ROLES), len(e.E005)) == (53, 5, 6)
    assert [name for name, _, _ in e.PARTITION] == ["G14-pre", "D14", "G14-mid", "H14", "A14"]
    assert [isqrt(u - 1) + 1 for _, (l, u), role in e.PARTITION if role != "guard"] == [8775, 8945, 12370]
    assert [e.icbrt(u - 3) for _, (l, u), role in e.PARTITION if role != "guard"] == [425, 430, 534]
    assert e.overlap((0, 2), (2, 4)) is False
    assert e.overlap((1, 3), (2, 4)) is True
    assert len(e.R90) == 16 and e.R90 == tuple(sorted(set(e.R90)))
    assert all(gcd(r, 30) == 1 and r % 9 in (1, 2, 7, 8) for r in e.R90)
    assert {v**3 % 9 for v in range(9)} == {0, 1, 8}
    assert {sum(x**3 for x in (a, b, c)) % 9 for a in range(9) for b in range(9) for c in range(9)} == {0, 1, 2, 3, 6, 7, 8}
    for value in (0, 1, 7, 8, 26, 27, 28, 425**3, 426**3 - 1):
        k = e.icbrt(value)
        assert k**3 <= value < (k + 1)**3
    with pytest.raises(ValueError):
        e.icbrt(-1)
    with pytest.raises(ValueError):
        e.icbrt(2.5)


def test_hand_cubes_positive_primitive_and_canonical_permutations():
    examples = [((1, 1, 1), 3), ((1, 1, 2), 10), ((1, 2, 2), 17), ((1, 2, 3), 36)]
    for triple, x in examples:
        assert e.primitive(triple)
        assert sum(k**3 for k in triple) == x
        assert e.primitive(tuple(sorted(reversed(triple))))
    assert sum(t**3 for t in (2, 2, 2)) == 24
    assert not e.primitive((2, 2, 2))
    assert not e.primitive((0, 1, 2))
    assert not e.primitive((2, 1, 3))
    assert not e.primitive((1, -1, 4))
    with pytest.raises(ValueError, match="D14"):
        e.enumerate_representations(79_000_000, 80_000_000)


def test_incidence_component_paths_disjoint_and_caps():
    assert e.incidence_shapes([]) is None
    assert e.incidence_shapes([(1, 1, 1)]) == (1, 1)
    assert e.incidence_shapes([(1, 2, 3), (4, 5, 6)]) == (2, 1)
    assert e.incidence_shapes([(1, 2, 3), (3, 4, 5)]) == (2, 2)
    # First/third don't share directly, but a two-edge path joins all three.
    assert e.incidence_shapes([(1, 2, 3), (3, 4, 5), (5, 6, 7)]) == (3, 3)
    reps = [(1, 2, 3), (3, 4, 5), (5, 6, 7), (8, 9, 10), (11, 12, 13)]
    assert e.incidence_shapes(reps) == (4, 3)
    chain = [(1, 2, 3), (3, 4, 5), (5, 6, 7), (7, 8, 9), (9, 10, 11)]
    assert e.incidence_shapes(chain) == (4, 4)
    with pytest.raises(AssertionError, match="noncanonical"):
        e.incidence_shapes([(1, 2, 3), (1, 2, 3)])
    with pytest.raises(AssertionError, match="noncanonical"):
        e.incidence_shapes([(2, 2, 2)])


def test_strict_mode_no_runner_up_no_tie_break():
    assert e.mode_info(Counter({1: 9, 2: 9})) == (None, 9, 9)
    assert e.mode_info(Counter({1: 9, 2: 8})) == (1, 9, 8)
    assert e.mode_info(Counter()) == (None, 0, 0)
    assert e.mode_info(Counter({4: 10, 1: 9})) == (4, 10, 9)
    with pytest.raises(AssertionError):
        e.mode_info(Counter({1: -1}))


def test_selection_exact_mixing_signed_class_aggregate_enrichment_and_duplicate():
    args = fabricated()
    rows, promoted = e.choose_rows(*args)
    assert [v["family"] for v in promoted] == ["I1", "I2"]
    assert all(row["mechanically_eligible"] and row["mixed_class_count"] == 16 and row["positive_class_count"] == 16 for row in rows)
    assert all(row["aggregate_enrichment_numerator"] == 960 * 1600 - 320 * 1600 for row in rows)
    same = set(range(960))
    rows, promoted = e.choose_rows(*fabricated([same, same.copy()]))
    assert [v["family"] for v in promoted] == ["I1"]
    assert not rows[1]["mechanically_eligible"]
    # Same cardinality, different *integer support*, never a duplicate.
    rows, promoted = e.choose_rows(*fabricated([same, set(range(1, 961))]))
    assert len(promoted) == 2
    args = list(fabricated())
    args[0][0] = Counter({1: 800, 2: 800})
    args[2][0] = {r: Counter({1: 50, 2: 50}) for r in e.R90}
    rows, promoted = e.choose_rows(*args)
    assert rows[0]["unique_mode_signature"] is None and not rows[0]["mechanically_eligible"]
    assert [v["family"] for v in promoted] == ["I2"]
    args = list(fabricated())
    args[2][0][e.R90[0]] = Counter({1: 100})  # No mixed target/control there.
    args[0][0][1] += 40
    args[0][0][3] -= 20
    args[0][0][4] -= 20
    args[6][0][1].update(range(100000, 100040))
    # Class totals maintain 100, counts are uneven but permitted as a synthetic test.
    rows, _ = e.choose_rows(*args)
    assert rows[0]["mixed_class_count"] == 15
    args = list(fabricated())
    for r in e.R90[:7]:
        args[3][0][r] = Counter({1: 80, 3: 10, 4: 10})
        args[1][0][1] += 60
        args[1][0][3] -= 30
        args[1][0][4] -= 30
    rows, promoted = e.choose_rows(*args)
    assert rows[0]["positive_class_count"] == 9
    assert not rows[0]["positive_class_floor_passed"]
    assert [v["family"] for v in promoted] == ["I2"]
    args = list(fabricated())
    args[-1]["serializer_or_duplicate_failure_count"] = 1
    assert e.choose_rows(*args)[1] == []
    args = list(fabricated())
    args[4][e.R90[0]] = 9
    with pytest.raises(AssertionError, match="conservation"):
        e.choose_rows(*args)
    args = list(fabricated())
    args[6][0][1].remove(0)
    with pytest.raises(AssertionError, match="support"):
        e.choose_rows(*args)


def test_poison_generator_all_out_of_phase_historical_calibration_nested_and_mutants():
    valid = e.plan_d14()
    e.authorize(valid, "D14")
    touched = []

    def poison(*args):
        touched.append(args)
        raise AssertionError("poison generator entered")

    invalid = [[], valid[:1], valid[::-1], valid + [valid[-1]],
               [valid[0], valid[1], valid[1]],
               [dict(valid[0], extra=1), valid[1]],
               [valid[0], dict(valid[1], extra=1)],
               [dict(valid[0], stop=77_000_000), valid[1]],
               [dict(valid[0], start=76_000_000), valid[1]],
               [valid[0], dict(valid[1], strategy="whole_prefix")],
               [valid[0], dict(valid[1], strategy="segmented-different")],
               [valid[0], {**valid[1], "start": 76_000_000, "stop": 76_500_000}],
               [valid[0], {**valid[1], "start": 76_500_000, "stop": 77_000_000}],
               [valid[0], {**valid[1], "start": 76_000_000, "stop": 78_000_000}],
               [valid[0], {**valid[1], "start": -20}],
               [valid[0], {**valid[1], "stop": 77_000_000.0}],
               [valid[0], {**valid[1], "start": True}],
               [dict(valid[0], stop=8774), valid[1]],
               [dict(valid[0], stop=8776), valid[1]],
               [dict(valid[0], purpose="other"), valid[1]],
               [valid[0], dict(valid[1], purpose="other")]]
    excluded = [(a * e.W, b * e.W) for a, b in (*e.OLD_MILLIONS, *e.E013_ROLES)]
    excluded += list(e.E005)
    excluded += [(start, start + width) for start, _ in e.E005
                 for width in (4096, 16384, 65536, 262144, 1048576)]
    excluded += [bounds for name, bounds, role in e.PARTITION if name != "D14"]
    excluded += [(200_000_000, 201_000_000), (10_000_000_000, 10_001_000_000)]
    for lo, hi in excluded:
        invalid.append([valid[0], {**valid[1], "start": lo, "stop": hi}])
    for plan in invalid:
        with pytest.raises(ValueError):
            e.generate(plan, "D14", poison, poison)
    for phase in ("H14", "A14", "G14-pre", "G14-mid", "D13", "H13", "D12", "A13", "OTHER"):
        with pytest.raises(ValueError):
            e.generate(valid, phase, poison, poison)
    assert touched == []
    with pytest.raises(AssertionError, match="poison generator entered"):
        e.generate(valid, "D14", poison, poison)
    assert len(touched) == 1


def sample_payload():
    rows, promotions = e.choose_rows(*fabricated())
    return {"experiment": "E014", "implementation_commit": "a" * 40,
            "band": {"name": "D14", "range": [76_000_000, 77_000_000], "interval_semantics": "half-open"},
            "partition": [{"name": n, "range": list(b), "role": role} for n, b, role in e.PARTITION],
            "parameters": e.parameters(), "generation_plan": e.plan_d14(),
            "anchor_summary": {"wheel_anchor_count": 3200, "represented_anchor_count": 3200,
                               "unrepresented_anchor_count": 0, "prime_count": 1600,
                               "composite_count": 1600, "prime_counts_by_R90": [100] * 16,
                               "composite_counts_by_R90": [100] * 16},
            "validation": {k: 0 for k in e.VALIDATION_KEYS},
            "families": rows, "promotions": promotions}


def test_exact_json_allowlist_types_null_canonical_bytes_and_failure_suppression():
    payload = sample_payload()
    raw = e.canonical_json(payload)
    assert raw == e.canonical_json(copy.deepcopy(payload)) and raw.endswith(b"\n")
    assert b'"prime_list"' not in raw and b'"support_set"' not in raw
    forbidden = {"": ["timings", "raw_triples"], "band": ["first_prime"],
                 "partition": ["extra"], "parameters": ["alternate_cap"],
                 "generation_plan": ["high_helper"], "anchor_summary": ["unrepresented_prime_count"],
                 "validation": ["debug"], "families": ["support_set"],
                 "promotions": ["anchor_ids"]}
    for section, keys in forbidden.items():
        for key in keys:
            changed = copy.deepcopy(payload)
            obj = changed if not section else changed[section]
            (obj[0] if isinstance(obj, list) else obj)[key] = 1
            with pytest.raises(ValueError):
                e.canonical_json(changed)
    variants = []
    changed = copy.deepcopy(payload)
    changed["validation"]["plan_failure_count"] = 1
    variants.append(changed)
    changed = copy.deepcopy(payload)
    changed["anchor_summary"]["prime_counts_by_R90"] = [100] * 15
    variants.append(changed)
    changed = copy.deepcopy(payload)
    changed["families"][0]["strict_unique_prime_mode"] = False
    variants.append(changed)
    changed = copy.deepcopy(payload)
    changed["families"][0]["unique_mode_signature"] = None
    variants.append(changed)
    changed = copy.deepcopy(payload)
    changed["promotions"] = changed["promotions"][::-1]
    variants.append(changed)
    changed = copy.deepcopy(payload)
    changed["anchor_summary"]["prime_count"] = True
    variants.append(changed)
    changed = copy.deepcopy(payload)
    changed["implementation_commit"] = "unversioned"
    variants.append(changed)
    for changed in variants:
        with pytest.raises(ValueError):
            e.canonical_json(changed)
    args = list(fabricated())
    args[0][0] = Counter({1: 800, 2: 800})
    args[2][0] = {r: Counter({1: 50, 2: 50}) for r in e.R90}
    rows, promotions = e.choose_rows(*args)
    tied = sample_payload()
    tied["families"], tied["promotions"] = rows, promotions
    assert b'"unique_mode_signature": null' in e.canonical_json(tied)
