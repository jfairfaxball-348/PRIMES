"""E015 integer-only synthetic tests: never generate primes or query primality."""
import copy
import importlib.util
from collections import Counter
from pathlib import Path

import pytest

MODULE = Path(__file__).resolve().parents[1] / 'experiments' / 'E015_square_shell_euclidean_remainder_quartile_shapes.py'
spec = importlib.util.spec_from_file_location('e015', MODULE)
e = importlib.util.module_from_spec(spec)
spec.loader.exec_module(e)


def test_metadata_exact_355_and_69():
    assert len(e.HISTORICAL_MILLIONS)==63
    assert len(e.historical_intervals())==69
    assert e.audit_partition()==355
    assert e.ROLES[1][1:3]==(81_000_000,82_000_000)
    assert e.PLANS['D15']==(('base_sieve_support',0,9056,'whole_prefix'),('segmented_target',81_000_000,82_000_000,'segmented'))
    assert len(set(n for n,*_ in e.historical_intervals()))==69


def test_isqrt_shell_and_zero_condition():
    for x in (100,101,120,121,122,224,225,226):
        s=e.isqrt(x)
        assert s*s<=x<(s+1)**2
        assert [s+j for j in e.OFFSETS]==list(range(s-4,s+5))
        for d in range(s-4,s+5):
            q,r=divmod(x,d)
            assert x==q*d+r and 0<=r<d
    assert e.shape(100) is None
    found=next(x for x in range(200,1500) if e.shape(x) is not None)
    assert sum(e.shape(found)[2])==9
    assert list(e.shape(found)[1])==sorted(e.shape(found)[2],reverse=True)


def test_quartile_exact_boundaries_and_invalid():
    assert [e.quartile(r,8) for r in (0,1,2,3,4,5,6,7)]==[0,0,1,1,2,2,3,3]
    assert e.quartile(3,12)==1 and e.quartile(6,12)==2 and e.quartile(9,12)==3
    for args in ((-1,8),(8,8),(1,0),(0,-1)):
        with pytest.raises(ValueError): e.quartile(*args)


def test_bin_counts_coarsenings_domains_zeros():
    words=((0,)*9,(0,0,0,1,1,2,2,3,3),(0,1,2,3,0,1,2,3,0))
    for word in words:
        c=tuple(word.count(i) for i in range(4))
        assert sum(c)==9
        assert max(c)==sorted(c,reverse=True)[0]
        assert tuple(sorted(c,reverse=True)) in e.domains()[1]
        assert c in e.domains()[2]
    assert (9,0,0,0) in e.domains()[1]
    assert (0,0,0,9) in e.domains()[2]
    assert e.domains()[0]==tuple(range(3,10))
    assert len(e.domains()[2])==220
    assert len(e.domains()[1])==18
    assert len(set(e.domains()[2]))==len(e.domains()[2])


def test_mode_tie_and_no_fallback():
    domain=e.domains()[0]
    assert e.strict_mode(Counter({3:12,4:11}),domain)==(3,12,11)
    assert e.strict_mode(Counter({3:12,4:12,5:10}),domain)==(None,12,12)
    assert e.strict_mode(Counter(),domain)==(None,0,0)
    assert e.strict_mode(Counter({4:1}),domain)==(4,1,0)


def test_mixed_classes_and_signed_enrichment():
    p=[Counter({'t':3,'other':1}) for _ in range(8)]
    c=[Counter({'t':2,'other':2}) for _ in range(8)]
    np=[4]*8;nc=[4]*8
    assert e.mixed_classes(p,c,np,nc,'t')==8
    c[0]['t']=4
    assert e.mixed_classes(p,c,np,nc,'t')==7
    p[1]['t']=0
    assert e.mixed_classes(p,c,np,nc,'t')==6
    assert e.exact_enrichment(1000,2000,40,70)==10000
    assert e.exact_enrichment(1000,2000,40,90)==-10000
    assert e.exact_enrichment(1000,2000,40,80)==0
    assert 999<1000 and 99<100 and 31<32 and 5<6


def test_duplicate_sets_not_counts_or_shapes():
    pairs=[('R1',{1,2}),('R2',{2,1}),('R3',{1,3})]
    assert e.select_duplicates(pairs)==['R1','R3']
    assert e.select_duplicates([('R1',{1}),('R2',{2}),('R3',{3})])==['R1','R2','R3']
    assert e.select_duplicates([])==[]
    with pytest.raises(ValueError): e.select_duplicates([('a',{1}),('b',{2}),('c',{3}),('d',{4})])


def _payload():
    fam=[]
    for f in ('R1','R2','R3'):
        fam.append(dict(family=f,prime_mode_count=0,highest_competing_count=0,strict_unique_prime_mode=False,unique_mode_signature=None,target_composite_count=None,population_floor_passed=False,class_floor_passed=False,occurrence_floor_passed=False,mixed_class_count=None,mixed_class_floor_passed=False,aggregate_enrichment_numerator=None,aggregate_enrichment_positive=False,mechanically_eligible=False))
    return dict(experiment='E015',implementation_commit='a'*40,band=dict(name='D15',range=[81_000_000,82_000_000],interval_semantics='half-open'),partition=[dict(name=n,range=[a,b],role=r) for n,a,b,r in e.ROLES],parameters=dict(width=1_000_000,wheel=30,residues_R30=list(e.R30),denominator_offsets=list(e.OFFSETS),quartile_edges_num=[0,1,2,3,4],quartile_denominator=4,zero_remainder_excluded=True,population_floor=1000,class_floor=100,occurrence_floor=32,mixed_class_floor=6),generation_plan=e.expected_plan('D15'),anchor_summary=dict(wheel_anchor_count=0,conditioned_anchor_count=0,excluded_zero_remainder_count=0,prime_count=0,composite_count=0,prime_counts_by_R30=[0]*8,composite_counts_by_R30=[0]*8),validation=dict.fromkeys(e.VALIDATION_KEYS,0),families=fam,promotions=[])


def test_canonical_schema_and_forbidden_fields():
    p=_payload()
    b=e.serialize(p)
    assert b.endswith(b'\n') and e.json.loads(b)==p
    assert b==e.serialize(e.json.loads(b))
    for key, value in (('prime_list',[]),('unblinded',1),('per_anchor',{})):
        q=copy.deepcopy(p);q[key]=value
        with pytest.raises(ValueError): e.serialize(q)
    for branch,key,value in (('anchor_summary','excluded_prime_count',0),('parameters','other',0),('validation','extra',0)):
        q=copy.deepcopy(p);q[branch][key]=value
        with pytest.raises(ValueError): e.serialize(q)
    q=copy.deepcopy(p);q['validation'][e.VALIDATION_KEYS[0]]=1
    with pytest.raises(ValueError): e.serialize(q)
    q=copy.deepcopy(p);q['families'][0]['unique_mode_signature']=3
    with pytest.raises(ValueError): e.serialize(q)


def test_poison_generator_all_metadata_exclusions_and_bad_calls():
    calls=[]
    def poison(_):
        calls.append('entered')
        raise AssertionError('poison generator entered')
    good=e.expected_plan('D15')
    assert e.validate_plan('D15',good)
    for role,lo,hi in e.historical_intervals():
        bad=copy.deepcopy(good);bad[1]['start']=lo;bad[1]['stop']=hi
        with pytest.raises(ValueError,match='plan denied'):
            e.generator_entry('D15',bad,0,poison)
    # E005 nested calibration widths, though maximum segments are already covered.
    for lo in e.CALIBRATION_STARTS:
        for width in (4096,16384,65536,262144,1048576):
            bad=copy.deepcopy(good);bad[1].update(start=lo,stop=lo+width)
            with pytest.raises(ValueError): e.generator_entry('D15',bad,0,poison)
    for lo,hi in ((80_000_000,81_000_000),(82_000_000,83_000_000),(83_000_000,84_000_000),(162_000_000,163_000_000),(86_000_000,87_000_000)):
        bad=copy.deepcopy(good);bad[1].update(start=lo,stop=hi)
        with pytest.raises(ValueError): e.generator_entry('D15',bad,0,poison)
    for phase in ('H15','A15','UNKNOWN'):
        with pytest.raises(ValueError): e.generator_entry(phase,e.expected_plan(phase) if phase!='UNKNOWN' else good,0,poison)
    changes=((0,'stop',9055),(0,'stop',9057),(0,'start',1),(0,'strategy','segmented'),(1,'start',80_999_999),(1,'stop',82_000_001),(1,'stop',81_999_999),(1,'strategy','whole_prefix'),(1,'purpose','base_sieve_support'))
    for i,key,value in changes:
        bad=copy.deepcopy(good);bad[i][key]=value
        with pytest.raises(ValueError): e.generator_entry('D15',bad,0,poison)
    for plan in (good[::-1],good+[good[1]],good[:1],good[1:],[],[good[0],good[0]],good+[dict(good[1],purpose='hidden_helper')]):
        with pytest.raises(ValueError): e.generator_entry('D15',plan,0,poison)
    for plan in ([dict(good[0],helper='primality_query'),good[1]],[good[0],dict(good[1],oracle=True)]):
        with pytest.raises(ValueError): e.generator_entry('D15',plan,0,poison)
    assert calls==[]


def test_guard_rechecks_phase_and_entry():
    calls=[]
    def fake(call):
        calls.append(call)
        return ()
    good=e.expected_plan('D15')
    assert e.generator_entry('D15',good,0,fake)==()
    assert e.generator_entry('D15',good,1,fake)==()
    assert calls==good
    with pytest.raises(ValueError): e.generator_entry('D15',good,2,fake)
    assert calls==good
