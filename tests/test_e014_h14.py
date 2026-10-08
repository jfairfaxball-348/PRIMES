"""E014 H14 pre-generation synthetic, poison, target-only schema tests."""
import copy
import sys
from collections import Counter
from math import gcd, isqrt
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiments"))
import E014_h14_primitive_three_cube_replication as h  # noqa: E402


def fixture():
    ppop = Counter({r: 100 for r in h.R90})
    cpop = Counter({r: 100 for r in h.R90})
    pf = Counter({1: 960, 2: 240, 3: 200, 4: 200})
    cf = Counter({1: 320, 2: 400, 3: 440, 4: 440})
    pby = {r: Counter({1: 60, 2: 15, 3: 12, 4: 13}) for r in h.R90}
    cby = {r: Counter({1: 20, 2: 25, 3: 27, 4: 28}) for r in h.R90}
    # Exact class rows conserve 100, aggregate all frequency totals conserved.
    pf = Counter({t: sum(pby[r][t] for r in h.R90) for t in range(1, 5)})
    cf = Counter({t: sum(cby[r][t] for r in h.R90) for t in range(1, 5)})
    return pf, cf, pby, cby, ppop, cpop, {k: 0 for k in h.VALIDATION_KEYS}


def sample():
    t = h.frozen_gates(*fixture())
    return {"experiment": "E014-H14-OBS020", "implementation_commit": "a" * 40,
            "band": {"name": "H14", "range": list(h.H14), "interval_semantics": "half-open"},
            "partition": [{"name": name, "range": list(bounds), "role": role}
                          for name, bounds, role in h.frozen.PARTITION],
            "parameters": h.frozen.parameters(), "generation_plan": h.plan_h14(),
            "anchor_summary": {"wheel_anchor_count": 3200, "represented_anchor_count": 3200,
                               "unrepresented_anchor_count": 0, "prime_count": 1600,
                               "composite_count": 1600, "prime_counts_by_R90": [100] * 16,
                               "composite_counts_by_R90": [100] * 16},
            "validation": {k: 0 for k in h.VALIDATION_KEYS}, "target": t}


def test_cubes_gcd_graph_mod9_r90_and_metadata():
    assert h.frozen.metadata_check() == 330
    assert len(h.frozen.OLD_MILLIONS) == 53
    assert len(h.R90) == 16 and h.R90 == tuple(sorted(h.R90))
    assert all(gcd(r, 30) == 1 and r % 9 in (1, 2, 7, 8) for r in h.R90)
    assert {x**3 % 9 for x in range(9)} == {0, 1, 8}
    assert {sum(z**3 for z in t) % 9 for t in ((a, b, c) for a in range(9) for b in range(9) for c in range(9))} == {0, 1, 2, 3, 6, 7, 8}
    assert [(sum(a**3 for a in t), h.frozen.primitive(t)) for t in ((1, 1, 1), (1, 1, 2), (1, 2, 2), (1, 2, 3), (2, 2, 2))] == [(3, True), (10, True), (17, True), (36, True), (24, False)]
    assert h.frozen.primitive((1, 2, 3)) and not h.frozen.primitive((2, 1, 3))
    assert h.frozen.incidence_shapes([]) is None
    assert h.frozen.incidence_shapes([(1, 1, 1)]) == (1, 1)
    assert h.frozen.incidence_shapes([(1, 2, 3), (4, 5, 6)]) == (2, 1)
    assert h.frozen.incidence_shapes([(1, 2, 3), (3, 4, 5), (5, 6, 7)]) == (3, 3)
    assert h.frozen.incidence_shapes([(1, 2, 3), (3, 4, 5), (5, 6, 7), (7, 8, 9), (9, 10, 11)]) == (4, 4)
    with pytest.raises(AssertionError):
        h.frozen.incidence_shapes([(1, 2, 3), (1, 2, 3)])
    for n in (0, 1, 7, 8, 27, 430**3, 431**3 - 1):
        k = h.frozen.icbrt(n)
        assert k**3 <= n < (k + 1)**3
    assert [isqrt(u - 1) + 1 for _, (l, u), role in h.frozen.PARTITION if role != "guard"] == [8775, 8945, 12370]
    assert h.frozen.icbrt(h.H14[1] - 3) == 430


def test_target_exact_gates_and_ties_and_no_fallback():
    args = fixture()
    target = h.frozen_gates(*args)
    assert target["replicated"] and target["family"] == "I2" and target["signature"] == 1
    assert target["mixed_class_count"] == 16 and target["positive_class_count"] == 16
    assert target["aggregate_enrichment_numerator"] == 960 * 1600 - 320 * 1600
    tied = list(fixture())
    tied[0] = Counter({1: 800, 2: 800})
    assert not h.frozen_gates(*tied)["strict_unique_prime_mode"]
    assert not h.frozen_gates(*tied)["replicated"]
    above = list(fixture())
    above[0] = Counter({1: 700, 2: 900})
    assert not h.frozen_gates(*above)["replicated"]
    missing = list(fixture())
    missing[0] = Counter({2: 1600})
    assert not h.frozen_gates(*missing)["replicated"]


def test_target_mixed_class_and_positive_per_class_and_aggregate():
    args = list(fixture())
    for r in h.R90[:5]:
        args[2][r] = Counter({1: 100})
    args[0] = Counter({t: sum(args[2][r][t] for r in h.R90) for t in range(1, 5)})
    a = h.frozen_gates(*args)
    assert a["mixed_class_count"] == 11 and not a["replicated"]
    args = list(fixture())
    for r in h.R90[:7]:
        args[3][r] = Counter({1: 80, 2: 10, 3: 5, 4: 5})
    args[1] = Counter({t: sum(args[3][r][t] for r in h.R90) for t in range(1, 5)})
    a = h.frozen_gates(*args)
    assert a["positive_class_count"] == 9 and not a["replicated"]
    args = list(fixture())
    for r in h.R90:
        args[3][r] = Counter({1: 80, 2: 10, 3: 5, 4: 5})
    args[1] = Counter({t: sum(args[3][r][t] for r in h.R90) for t in range(1, 5)})
    assert h.frozen_gates(*args)["aggregate_enrichment_numerator"] < 0


def test_invalid_conservation_validation_and_json():
    base = sample()
    assert h.canonical_json(base) == h.canonical_json(copy.deepcopy(base))
    assert b'"prime_list"' not in h.canonical_json(base)
    for sect, name in (("", "raw_triples"), ("target", "competing_signatures"),
                       ("anchor_summary", "anchor_ids"), ("parameters", "unfrozen"),
                       ("partition", "hidden"), ("generation_plan", "helper"),
                       ("validation", "extra")):
        bad = copy.deepcopy(base)
        obj = bad if not sect else bad[sect]
        if type(obj) is list:
            obj[0][name] = 1
        else:
            obj[name] = 1
        with pytest.raises(ValueError):
            h.canonical_json(bad)
    for mutate in (
        lambda d: d["validation"].update(plan_failure_count=1),
        lambda d: d["target"].update(signature=2),
        lambda d: d["target"].update(aggregate_enrichment_numerator=0),
        lambda d: d["target"].update(replicated=False),
        lambda d: d["target"].update(prime_target_count=True),
        lambda d: d["anchor_summary"].update(prime_count=-1),
        lambda d: d["anchor_summary"].update(prime_counts_by_R90=[100] * 15),
        lambda d: d.update(implementation_commit="none"),
    ):
        bad = copy.deepcopy(base)
        mutate(bad)
        with pytest.raises(ValueError):
            h.canonical_json(bad)
    args = list(fixture())
    args[-1]["incidence_graph_failure_count"] = 1
    with pytest.raises(ValueError):
        h.frozen_gates(*args)
    args = list(fixture())
    args[4][h.R90[0]] = 99
    with pytest.raises(ValueError):
        h.frozen_gates(*args)


def test_exact_poison_plan_historical_nested_protected_offphase_highprefix():
    good = h.plan_h14()
    h.authorize(good, "H14")
    entered = []

    def poison(*args):
        entered.append(args)
        raise AssertionError("poison generator entered")

    invalid = [[], good[:1], good[::-1], good + [good[-1]],
               [good[0], good[1], good[1]],
               [dict(good[0], extra=1), good[1]],
               [dict(good[0], stop=8944), good[1]],
               [dict(good[0], stop=8946), good[1]],
               [dict(good[0], purpose="other"), good[1]],
               [good[0], dict(good[1], purpose="other")],
               [good[0], dict(good[1], strategy="whole_prefix")],
               [good[0], {**good[1], "stop": h.H14[1] - 1}],
               [good[0], {**good[1], "start": h.H14[0] + 1}],
               [good[0], {**good[1], "start": h.H14[0], "stop": h.H14[0] + 500000}],
               [good[0], {**good[1], "start": h.H14[0] + 500000}],
               [good[0], {**good[1], "start": h.H14[0] - 1}],
               [good[0], {**good[1], "stop": h.H14[1] + 1}],
               [good[0], {**good[1], "start": -1}],
               [good[0], {**good[1], "stop": float(h.H14[1])}],
               [dict(good[0], stop=True), good[1]],
               [good[0], {**good[1], "start": 10_000_000_000, "stop": 10_001_000_000}]]
    protected = [(a * h.frozen.W, b * h.frozen.W)
                 for a, b in (*h.frozen.OLD_MILLIONS, *h.frozen.E013_ROLES)]
    protected += list(h.frozen.E005)
    protected += [(start, start + width) for start, _ in h.frozen.E005
                  for width in (4096, 16384, 65536, 262144, 1048576)]
    protected += [bounds for name, bounds, role in h.frozen.PARTITION if name != "H14"]
    assert len(protected) == 98
    for lo, hi in protected:
        invalid.append([good[0], {**good[1], "start": lo, "stop": hi}])
    for plan in invalid:
        with pytest.raises(ValueError):
            h.generate(plan, "H14", poison, poison)
    for phase in ("D14", "A14", "G14-pre", "G14-mid", "D12", "H12", "D13", "H13", "A13", "other"):
        with pytest.raises(ValueError):
            h.generate(good, phase, poison, poison)
    assert entered == []
    with pytest.raises(AssertionError, match="poison generator entered"):
        h.generate(good, "H14", poison, poison)
    assert len(entered) == 1
