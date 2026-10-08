"""One-shot H15 synthetic/poison tests; no real prime generation or primality queries."""
import copy
import importlib.util
from collections import Counter
from pathlib import Path

import pytest

PATH = Path(__file__).resolve().parents[1] / "experiments" / "E015_H15_replication.py"
spec = importlib.util.spec_from_file_location("h15", PATH)
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)
e = h.e
OTHER = (0, 0, 0, 9)


def fabricated(prime_target=120, prime_other=80, composite_target=60, composite_other=140):
    p_by = [Counter({h.TARGET: prime_target, OTHER: prime_other}) for _ in range(8)]
    c_by = [Counter({h.TARGET: composite_target, OTHER: composite_other}) for _ in range(8)]
    return (sum(p_by, Counter()), sum(c_by, Counter()),
            [prime_target + prime_other] * 8, [composite_target + composite_other] * 8,
            p_by, c_by)


def test_exact_metadata_exclusions_and_original_blob_behaviour():
    assert len(e.historical_intervals()) == 69
    assert h.plan_checked("H15", e.expected_plan("H15"))
    assert e.audit_partition() == 355
    assert len(e.domains()[2]) == 220 and h.TARGET in e.domains()[2]
    assert e.PLANS["H15"] == (("base_sieve_support", 0, 9166, "whole_prefix"),
                             ("segmented_target", 83_000_000, 84_000_000, "segmented"))


def test_exact_euclidean_shell_quartiles_and_coarsening():
    for x in (100, 101, 120, 121, 122, 224, 225, 226, 1000, 1001):
        s = e.isqrt(x)
        assert s*s <= x < (s+1)**2
        assert [s+j for j in e.OFFSETS] == list(range(s-4, s+5))
        for d in range(s-4, s+5):
            q, r = divmod(x, d)
            assert x == q*d+r and 0 <= r < d
    assert e.shape(100) is None
    assert [e.quartile(r, 8) for r in range(8)] == [0, 0, 1, 1, 2, 2, 3, 3]
    assert [e.quartile(i, 12) for i in (3,6,9)] == [1,2,3]
    found = next(x for x in range(200, 1500) if e.shape(x) is not None)
    r1, r2, r3 = e.shape(found)
    assert sum(r3) == 9 and r1 == max(r3) and r2 == tuple(sorted(r3, reverse=True))


def test_strict_220_domain_target_and_enrichment_signed():
    t = h.target_metrics(*fabricated())
    assert t["criterion_passed"] and t["prime_count"] == 960
    assert t["highest_competing_prime_count"] == 640 and t["mixed_class_count"] == 8
    assert t["aggregate_enrichment_numerator"] == 960*1600-480*1600
    tie = h.target_metrics(*fabricated(100,100,60,140))
    assert not tie["strict_unique_prime_mode"] and not tie["criterion_passed"]
    beaten = h.target_metrics(*fabricated(80,120,60,140))
    assert not beaten["strict_unique_prime_mode"] and not beaten["criterion_passed"]
    absent = h.target_metrics(*fabricated(0,200,60,140))
    assert not absent["strict_unique_prime_mode"] and not absent["criterion_passed"]
    assert not h.target_metrics(*fabricated(120,80,160,40))["aggregate_enrichment_positive"]
    assert not h.target_metrics(*fabricated(120,80,120,80))["aggregate_enrichment_positive"]
    assert h.target_metrics(*fabricated(120,80,0,200))["aggregate_enrichment_positive"]


def test_mixed_and_floors_no_extra_positive_class_gate():
    p, c, np, nc, pb, cb = fabricated()
    for i in range(3):
        pb[i] = Counter({OTHER: 200})
    p = sum(pb, Counter())
    t = h.target_metrics(p,c,np,nc,pb,cb)
    assert t["mixed_class_count"] == 5 and not t["criterion_passed"]
    p,c,np,nc,pb,cb = fabricated(50,49,20,79)
    t = h.target_metrics(p,c,np,nc,pb,cb)
    assert not t["population_floor_passed"] and not t["class_floor_passed"]
    p,c,np,nc,pb,cb = fabricated(3,197,2,198)
    assert not h.target_metrics(p,c,np,nc,pb,cb)["occurrence_floor_passed"]


def test_invalid_frequencies_and_domain():
    p,c,np,nc,pb,cb = fabricated()
    with pytest.raises(ValueError):
        h.target_metrics(Counter({(10,0,0,0):1600}), c, np, nc, pb, cb)
    with pytest.raises(ValueError):
        h.target_metrics(p, c, [199]*8, nc, pb, cb)


def test_poison_all_69_history_and_nested_calibration_and_e015_guards():
    called=[]
    def poison(_):
        called.append(True)
        raise AssertionError("generator must not be entered")
    good=e.expected_plan("H15")
    negatives=[]
    for _,lo,hi in e.historical_intervals():
        bad=copy.deepcopy(good);bad[1].update(start=lo,stop=hi);negatives.append(bad)
    for lo in e.CALIBRATION_STARTS:
        for w in (4096,16384,65536,262144,1048576):
            bad=copy.deepcopy(good);bad[1].update(start=lo,stop=lo+w);negatives.append(bad)
    for lo,hi in ((80_000_000,81_000_000),(81_000_000,82_000_000),
                  (82_000_000,83_000_000),(162_000_000,163_000_000),
                  (79_000_000,80_000_000),(84_000_000,85_000_000),
                  (86_000_000,87_000_000)):
        bad=copy.deepcopy(good);bad[1].update(start=lo,stop=hi);negatives.append(bad)
    for i,k,v in ((0,"stop",9165),(0,"stop",9167),(0,"start",1),
                  (0,"strategy","segmented"),(1,"start",82_999_999),
                  (1,"stop",84_000_001),(1,"stop",83_999_999),
                  (1,"strategy","whole_prefix"),(1,"purpose","base_sieve_support")):
        bad=copy.deepcopy(good);bad[i][k]=v;negatives.append(bad)
    negatives += [good[::-1],good+[good[1]],good[:1],good[1:],[],
                  [good[0],good[0]],good+[dict(good[1],purpose="helper")],
                  [dict(good[0],helper="primality_query"),good[1]],
                  [good[0],dict(good[1],oracle=True)]]
    assert len(negatives) >= 120
    for bad in negatives:
        with pytest.raises(ValueError):
            e.generator_entry("H15",bad,0,poison,authorized="H15")
        with pytest.raises(ValueError):
            h.plan_checked("H15",bad)
    for phase in ("D15","A15","UNKNOWN"):
        with pytest.raises(ValueError):
            h.plan_checked(phase,good)
        with pytest.raises(ValueError):
            e.generator_entry(phase,good,0,poison,authorized="H15")
    assert not called


def test_exact_two_boundary_rechecks_without_real_generator():
    calls=[]
    def fake(entry):
        calls.append(entry)
        return ()
    good=e.expected_plan("H15")
    assert e.generator_entry("H15",good,0,fake,authorized="H15")==()
    assert e.generator_entry("H15",good,1,fake,authorized="H15")==()
    assert calls==good
    with pytest.raises(ValueError):
        e.generator_entry("H15",good,2,fake,authorized="H15")
    assert calls==good


def synthetic_schema():
    target=h.target_metrics(*fabricated())
    plan=e.expected_plan("H15")
    return dict(experiment="E015",implementation_commit="a"*40,
                band=dict(name="H15",range=[h.LOW,h.HIGH],interval_semantics="half-open"),
                partition=[dict(name=n,range=[lo,hi],role=r) for n,lo,hi,r in e.ROLES],
                parameters=dict(width=1_000_000,wheel=30,residues_R30=list(e.R30),
                                denominator_offsets=list(e.OFFSETS),quartile_edges_num=[0,1,2,3,4],
                                quartile_denominator=4,zero_remainder_excluded=True,
                                population_floor=1000,class_floor=100,occurrence_floor=32,mixed_class_floor=6),
                generation_plan=plan,
                anchor_summary=dict(wheel_anchor_count=3200,conditioned_anchor_count=3200,
                                    excluded_zero_remainder_count=0,prime_count=1600,composite_count=1600,
                                    prime_counts_by_R30=[200]*8,composite_counts_by_R30=[200]*8),
                validation=dict.fromkeys(e.VALIDATION_KEYS,0),target=target)


def test_strict_canonical_schema_forbidden_field_and_zero_counters():
    p=synthetic_schema()
    data=h.serialize(p)
    assert data.endswith(b"\n") and h.serialize(h.json.loads(data))==data
    for path,k,v in (((),"primes",[]),(("target",),"competitor_signature",[0,0,0,9]),
                     (("anchor_summary",),"examples",[]),(("parameters",),"other",0),
                     (("validation",),"extra",0)):
        q=copy.deepcopy(p)
        node=q
        for component in path:node=node[component]
        node[k]=v
        with pytest.raises(ValueError):h.serialize(q)
    q=copy.deepcopy(p);q["validation"][e.VALIDATION_KEYS[0]]=1
    with pytest.raises(ValueError):h.serialize(q)
    q=copy.deepcopy(p);q["target"]["signature"]=[0,0,0,9]
    with pytest.raises(ValueError):h.serialize(q)
    q=copy.deepcopy(p);q["target"]["criterion_passed"]=False
    with pytest.raises(ValueError):h.serialize(q)


def test_frozen_source_untouched_by_h15_tests():
    # No test calls e.guarded_primes, e._generate, or primality functions.
    assert h.ORIGINAL_PATH.name=="E015_square_shell_euclidean_remainder_quartile_shapes.py"
    assert e.shape(100) is None
