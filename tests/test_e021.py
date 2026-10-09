"""Independent E021 source-free semantics and poison-before-generator checks only."""
import importlib.util
import json
from math import gcd
from pathlib import Path

import pytest

SOURCE = Path(__file__).resolve().parents[1] / 'experiments' / 'E021_fixed_block_set_partition_residue_shapes.py'
spec = importlib.util.spec_from_file_location('e021', SOURCE)
e = importlib.util.module_from_spec(spec)
spec.loader.exec_module(e)


def test_independent_synthetic_stirling_and_modular_integer_quotient():
    # Build whole Stirling triangle from zero, not the source's recursive function.
    rows=[[1]]
    for n in range(1,19):
        prev=rows[-1]
        rows.append([0]+[k*(prev[k] if k<len(prev) else 0)+prev[k-1] for k in range(1,n+1)])
    for n in range(1,19):
        expected=tuple(rows[n][k]%(n+1) if k<=n else 0 for k in (3,4))
        assert e.residues(n)==expected
        for k,d in ((3,6),(4,24)):
            val=sum((-1)**(k-j)*__import__('math').comb(k,j)*j**n for j in range(k+1))
            assert val%d==0
            assert val//d==(rows[n][k] if n>=k else 0)
            mod=d*(n+1)
            assert all(pow(j,n,mod)==j**n%mod for j in range(k+1))


def test_quartiles_boundaries_complete_joint_and_bad_values():
    n=19;m=n+1
    assert {e.signature(n,a,b) for a in range(m) for b in range(m)}==set(range(16))
    for q in range(4):
        assert e.signature(n,q*m//4,0)//4==q
        assert e.signature(n,0,q*m//4)%4==q
    assert e.signature(3,1,2)==6
    for bad in ((0,0,0),(5,6,0),(5,0,6),(5,True,0)):
        with pytest.raises(ValueError):e.signature(*bad)


def test_wheel_classes_and_roles_from_metadata_only():
    assert e.R210==tuple(i for i in range(210) if gcd(i,210)==1)
    assert len(e.R210)==48
    assert e.audit_intervals()==(4851,495,10,150,30)
    assert len(e.old_intervals())==99
    assert len(e.EARLY)==53
    assert len({name for name,_,_ in e.old_intervals()})==99
    assert len([q for q in e.old_intervals() if q[0].startswith('E005-')])==6
    assert e.PLAN==(('base_sieve_support',0,11833,'whole_prefix'),('segmented_target',138000000,140000000,'direct_segmented'))


def test_enrichment_selector_is_signed_not_prime_mode_and_tie_fails():
    a=[-10]*16;a[7]=4;a[3]=3
    assert e.select(a)==(7,4,3)
    a[3]=4
    assert e.select(a)==(None,4,4)
    a=[-1]*16
    assert e.select(a)==(None,-1,-1)
    a[2]=0
    assert e.select(a)==(None,0,-1)
    with pytest.raises(ValueError):e.select([False]+[1]*15)
    # Prime-count mode of state 1 versus signed E maximum of state 2.
    np=[0]*16;nc=[0]*16
    np[1]=20;np[2]=15;nc[1]=45;nc[2]=2
    np[0]=5;nc[0]=53
    NP=sum(np);NC=sum(nc)
    assert max(range(16),key=lambda t:np[t])==1
    E=[np[t]*NC-nc[t]*NP for t in range(16)]
    assert e.select(E)[0]==2


def test_exact_support_equality_and_cap_one():
    old=[]
    assert e.dedup_support({5,11},old)
    assert not e.dedup_support({11,5},old)
    assert not e.dedup_support({5,13},old) # different set but cap one
    assert old==[{5,11}]
    with pytest.raises(ValueError):e.dedup_support({True},[])


def test_poisoned_whole_plans_and_off_phase_before_any_sieve(monkeypatch):
    def forbidden(*a,**kw): raise AssertionError('PRIME GENERATOR ENTERED')
    monkeypatch.setattr(e,'base_sieve',forbidden)
    monkeypatch.setattr(e,'target_segment',forbidden)
    legitimate=e.PLAN
    invalid=[]
    invalid += [(legitimate[1],legitimate[0]),(legitimate[0],),(legitimate[0],legitimate[1],legitimate[1])]
    for i in range(2):
        for slot in (1,2):
            for delta in (-1,1):
                plan=[tuple(x) for x in legitimate]
                x=list(plan[i]);x[slot]+=delta;plan[i]=tuple(x);invalid.append(tuple(plan))
    for item in e.old_intervals()+[(n,a,b) for n,a,b,_ in e.ROLES]:
        name,start,stop=item
        if (start,stop)!=(138000000,140000000):
            invalid.append((legitimate[0],('segmented_target',start,stop,'direct_segmented')))
    for a in e.E005_STARTS:
        for w in e.E005_WIDTHS:
            invalid.append((legitimate[0],('segmented_target',a,a+w,'direct_segmented')))
    invalid += [(('base_sieve_support',0,140000000,'whole_prefix'),legitimate[1]),
                (legitimate[0],('segmented_target',138000000,139999999,'direct_segmented')),
                (legitimate[0],('segmented_target',138000000,140000000,'whole_prefix'))]
    for plan in invalid:
        with pytest.raises((ValueError,AssertionError)):
            e.GeneratorGate(plan)
    for phase in ('H21','A21','G21-pre','D20','D19','D21-split'):
        with pytest.raises(ValueError):e.GeneratorGate(legitimate,phase=phase)
    for kw in ({'indirect':True},{'per_anchor':True}):
        with pytest.raises(ValueError):e.GeneratorGate(legitimate,**kw)
    assert len(invalid)>=140


def test_generator_entry_order_and_hidden_alteration_fails_before_call():
    g=e.GeneratorGate()
    with pytest.raises(ValueError):g.enter(1,*e.PLAN[1])
    with pytest.raises(ValueError):g.enter(0,'base_sieve_support',0,11834,'whole_prefix')
    with pytest.raises(ValueError):g.enter(0,'base_sieve_support',0,11833,'direct_segmented')
    assert g.cursor==0
    g.enter(0,*e.PLAN[0]);assert g.cursor==1
    with pytest.raises(ValueError):g.enter(0,*e.PLAN[0])
    g.enter(1,*e.PLAN[1]);assert g.cursor==2
    with pytest.raises(ValueError):g.enter(1,*e.PLAN[1])


def _payload():
    f=dict.fromkeys(e.FAMILY_KEYS,None)
    f.update(family='F1',candidate_signature=None,evaluated_signature=None,
             highest_enrichment_numerator=0,highest_competing_enrichment_numerator=0,
             strict_unique_positive_enrichment_max=False,population_floor_passed=False,class_floor_passed=False,
             occurrence_floor_passed=False,mixed_class_floor_passed=False,positive_class_floor_passed=False,
             target_enrichment_positive=False,mechanically_eligible=False)
    return dict(experiment='E021',implementation_commit='0'*40,band=dict(name='D21',range=[138000000,140000000],interval_semantics='half-open'),
        partition=[dict(name=n,range=[a,b],role=r) for n,a,b,r in e.ROLES],
        parameters=e.PARAMS,generation_plan=[dict(purpose=a,start=b,stop=c,strategy=d) for a,b,c,d in e.PLAN],
        anchor_summary=dict(wheel_anchor_count=0,prime_count=0,composite_count=0,
            prime_counts_by_R210=[0]*48,composite_counts_by_R210=[0]*48),
        validation={k:0 for k in e.COUNTERS},families=[f],promotions=[])


def test_strict_typed_canonical_ten_key_aggregate_and_poison():
    p=_payload()
    raw=e.canonical(p)
    assert raw.endswith(b'\n') and not raw.endswith(b'\n\n')
    assert raw== (json.dumps(p,sort_keys=True,indent=2,ensure_ascii=True)+'\n').encode('ascii')
    for key in e.COUNTERS:
        altered=_payload();altered['validation'][key]=True
        with pytest.raises(ValueError):e.canonical(altered)
        altered=_payload();altered['validation'][key]=1
        with pytest.raises(ValueError):e.canonical(altered)
    altered=_payload();altered['unexpected_histogram']=[0]*16
    with pytest.raises(ValueError):e.canonical(altered)
    altered=_payload();altered['anchor_summary']['prime_counts_by_R210'][0]=True
    with pytest.raises(ValueError):e.canonical(altered)
    altered=_payload();altered['families'][0]['target_prime_count']=0
    with pytest.raises(ValueError):e.canonical(altered)
    altered=_payload();altered['promotions']=[{},{}]
    with pytest.raises(ValueError):e.canonical(altered)
