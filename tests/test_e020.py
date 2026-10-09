"""E020 D20 strict synthetic/poison tests: no prime-generation entry."""
from __future__ import annotations

import copy
import json
from itertools import product
from pathlib import Path
from unittest.mock import patch

import pytest

from experiments import E020_s3_generator_word_endpoint_residue_shapes as e


def synthetic_tables(kind="pass"):
    if kind == "pass":
        p, c = [18,4,4,4], [3,9,9,9]
    elif kind == "tie":
        p, c = [8,8,7,7], [3,9,9,9]
    elif kind == "negative":
        p, c = [18,4,4,4], [25,2,2,1]
    elif kind == "no_mix":
        p, c = [30,0,0,0], [3,9,9,9]
    else:
        raise ValueError(kind)
    pr, cr = [p[:] for _ in range(48)], [c[:] for _ in range(48)]
    pc = [48*t for t in p]
    cc = [48*t for t in c]
    return pc, cc, pr, cr, [sum(p)]*48, [sum(c)]*48, list(range(pc[0]))


def sample_payload():
    pc,cc,pr,cr,pclass,cclass,support=synthetic_tables()
    row, promotions = e.select_w1(pc,cc,pr,cr,pclass,cclass,support)
    return dict(experiment="E020", implementation_commit="a"*40,
        band=dict(name="D20",range=[103*e.M,104*e.M],interval_semantics="half-open"),
        partition=[dict(name=n,range=[lo,hi],role=role) for n,lo,hi,role in e.PARTITION],
        parameters=e.parameters(),
        generation_plan=[dict(purpose=p,start=s,stop=t,strategy=q) for p,s,t,q in e.PLAN],
        anchor_summary=dict(wheel_anchor_count=sum(pclass)+sum(cclass),
             prime_count=sum(pclass),composite_count=sum(cclass),
             prime_counts_by_R210=pclass, composite_counts_by_R210=cclass),
        validation={key:0 for key in e.VALIDATORS},
        families=[row], promotions=promotions)


def test_six_state_multiplication_noncommutative_associative():
    assert e.STATES == tuple(sorted(e.STATES))
    assert len(e.STATES) == len(set(e.STATES)) == 6
    assert e.compose(e.A,e.B) != e.compose(e.B,e.A)
    for g,h,k in product(e.STATES, repeat=3):
        assert e.compose(e.compose(g,h),k) == e.compose(g,e.compose(h,k))
        assert e.MUL[e.INDEX[g]][e.INDEX[h]] == e.INDEX[e.compose(g,h)]


def test_tiny_words_direct_and_right_append_recurrence():
    for n in range(5):
        direct = [0]*6
        for letters in product((e.A,e.B),repeat=n):
            g=e.IDENTITY
            for letter in letters:
                g=e.compose(g,letter)
            direct[e.INDEX[g]] += 1
        assert tuple(direct) == e.word_power(n)
        assert sum(direct) == 2**n
        for mod in (1,2,3,4,7,11,19):
            assert e.word_power(n,mod)==tuple(t%mod for t in direct)
            assert sum(e.word_power(n,mod))%mod==pow(2,n,mod)
        if n<4:
            nxt = [0]*6
            for j,g in enumerate(e.STATES):
                for h in (e.A,e.B):
                    nxt[e.INDEX[e.compose(g,h)]] += direct[j]
            assert tuple(nxt) == e.word_power(n+1)


def test_remainders_bins_small_synthetic():
    assert e.signature(1)==0
    assert all(e.signature(n) in (0,1,2,3) for n in range(1,35))
    for n in range(1,35):
        q=e.word_power(n,n)
        assert all(0<=v<n for v in q)
        aa,bb=q[e.INDEX[e.A]],q[e.INDEX[e.B]]
        assert e.signature(n)==2*((2*aa)//n)+(2*bb)//n
    assert (2*(10//2))//10 == 1


def test_full_wheel_and_metadata_disjointness():
    assert e.R210 == tuple(n for n in range(210) if __import__('math').gcd(n,210)==1)
    assert (len(e.EARLY),len(e.old_roles()),len(e.NEW))==(53,94,5)
    assert e.audit_intervals()
    old=e.old_roles(); new=e.NEW
    assert sum(e.overlap(a,b) for i,a in enumerate(old) for b in old[i+1:])==0
    assert sum(e.overlap(a,b) for a in new for b in old)==0
    assert sum(e.overlap(a,b) for i,a in enumerate(new) for b in new[i+1:])==0
    assert len(old)*(len(old)-1)//2==4371
    assert len(old)*len(new)==470
    assert len(new)*(len(new)-1)//2==10
    assert e.isqrt(103_999_999)==10198


def test_poison_plan_before_any_generator_entry():
    positive=e.PLAN
    negatives=[positive[::-1], positive[:1], positive+(positive[-1],),
       (("base_sieve_support",0,104*e.M,"whole_prefix"),positive[1]),
       (("base_sieve_support",0,10198,"whole_prefix"),positive[1]),
       (("base_sieve_support",0,10200,"whole_prefix"),positive[1]),
       (positive[0],("segmented_target",104*e.M,105*e.M,"direct_segmented")),
       (positive[0],("segmented_target",103*e.M,103*e.M+1,"direct_segmented")),
       (positive[0],("segmented_target",103*e.M-1,104*e.M,"direct_segmented")),
       (positive[0],("segmented_target",103*e.M,104*e.M+1,"direct_segmented")),
       (positive[0],("segmented_target",105*e.M,106*e.M,"direct_segmented")),
       (positive[0],("segmented_target",206*e.M,207*e.M,"direct_segmented")),
       (positive[0],("segmented_target",128*e.M,128*e.M+4096,"direct_segmented")),
       (positive[0],("segmented_target",99*e.M,100*e.M,"direct_segmented")),
       (positive[0],("segmented_target",103*e.M,104*e.M,"whole_prefix"))]
    with patch.object(e,"base_sieve",side_effect=AssertionError("prime generator entered")), \
         patch.object(e,"segmented_target",side_effect=AssertionError("prime generator entered")):
        for plan in negatives:
            with pytest.raises(ValueError):
                e.GeneratorFirewall(plan)
        for phase in ("H20","A20","D19","G20-pre"):
            with pytest.raises(ValueError): e.validate_plan(positive,phase)
        fw=e.GeneratorFirewall(positive)
        with pytest.raises(ValueError): fw.enter(*positive[1])
        fw.enter(*positive[0])
        with pytest.raises(ValueError): fw.enter(*positive[0])
        fw.enter(*positive[1]);fw.complete()
        with pytest.raises(ValueError): fw.enter(*positive[1])


def test_synthetic_unique_tie_signed_and_mixing_gates():
    for name,ok in (("pass",True),("tie",False),("negative",False),("no_mix",False)):
        row,promo=e.select_w1(*synthetic_tables(name))
        assert row["mechanically_eligible"] is ok
        assert bool(promo) is ok
        if name=="tie":
            assert row["unique_mode_signature"] is None
            assert row["aggregate_enrichment_numerator"] is None
            assert row["mixed_class_count"] is None
            assert row["positive_class_count"] is None
    args=list(synthetic_tables("pass"))
    args[6]=[5]*len(args[6])
    with pytest.raises(ValueError):e.select_w1(*args)
    args=list(synthetic_tables("pass"))
    args[6]=[True]+args[6][1:]
    with pytest.raises(ValueError):e.select_w1(*args)


def test_strict_full_json_canonical_and_poison_types():
    d=sample_payload()
    raw=e.canonical(d)
    assert raw.endswith(b"\n") and not raw.endswith(b"\n\n")
    assert json.loads(raw)==d
    assert raw== (json.dumps(d,sort_keys=True,indent=2,ensure_ascii=True)+"\n").encode("ascii")
    mutants=[]
    x=copy.deepcopy(d);x["unknown"]=0;mutants.append(x)
    x=copy.deepcopy(d);del x["validation"]["serializer_failure_count"];mutants.append(x)
    x=copy.deepcopy(d);x["validation"]["plan_failure_count"]=True;mutants.append(x)
    x=copy.deepcopy(d);x["validation"]["plan_failure_count"]=1;mutants.append(x)
    x=copy.deepcopy(d);x["anchor_summary"]["prime_count"]=True;mutants.append(x)
    x=copy.deepcopy(d);x["parameters"]["width"]=True;mutants.append(x)
    x=copy.deepcopy(d);x["families"][0]["strict_unique_prime_mode"]=1;mutants.append(x)
    x=copy.deepcopy(d);x["families"][0]["unique_mode_signature"]=True;mutants.append(x)
    x=copy.deepcopy(d);x["promotions"].append(x["promotions"][0]);mutants.append(x)
    x=copy.deepcopy(d);x["promotions"][0]["per_anchor_support"]=[13];mutants.append(x)
    x=copy.deepcopy(d);x["parameters"]["residues_R210"].append(211);mutants.append(x)
    x=copy.deepcopy(d);x["anchor_summary"]["prime_counts_by_R210"][0]=1.0;mutants.append(x)
    x=copy.deepcopy(d);x["partition"][1]["range"][0]=True;mutants.append(x)
    for x in mutants:
        with pytest.raises((ValueError,TypeError,AssertionError)):
            e.canonical(x)


def test_no_generation_on_synthetic_preflight():
    with patch.object(e,"base_sieve",side_effect=AssertionError("unexpected entry")), \
         patch.object(e,"segmented_target",side_effect=AssertionError("unexpected entry")):
        assert e.self_check()
