"""Source-free synthetic graph checks and fail-before-generator poisons for H19."""
import copy
from math import gcd, isqrt
import pytest

from experiments import E019_H19_fixed_two_row_ladder_spanning_forest as e


def test_tiny_forest_independent_enumeration():
    assert [e.tiny_graph_states(n) for n in range(1, 5)] == [
        (1, 1), (4, 3), (15, 11), (56, 41)]
    for n in range(1, 5):
        assert e.tiny_graph_states(n) == e.direct_states(n)
        assert e.forest_mod(n) == tuple(v % n for v in e.tiny_graph_states(n))
    with pytest.raises(ValueError): e.tiny_graph_states(5)
    with pytest.raises(ValueError): e.forest_mod(0)


def test_transfer_modular_bins():
    for n in range(1, 17):
        c, d = e.direct_states(n)
        assert e.forest_mod(n) == (c % n, d % n)
        assert e.signature(n) == 2*(2*(c % n)//n) + (2*(d % n)//n)
    for n in (1, 2, 3, 7, 31, 101, 65537, 10**12+39):
        a, b = e.forest_mod(n)
        assert 0 <= a < n and 0 <= b < n
        assert 0 <= e.signature(n) <= 3
    for x in (10, 12, 100):
        assert [(2*r)//x for r in range(x)] == [int(r >= (x+1)//2) for r in range(x)]
    assert e.product_mod(((1,0),(0,1)), e.M, 101) == e.M


def test_wheel_and_inventory():
    assert e.Q == 210 and len(e.R210) == 48 and e.R210 == tuple(r for r in range(210) if gcd(r,210)==1)
    assert e.audit_intervals() == dict(old_pairs=3916, old_new=445, new_pairs=10, nested_contained=30, new_nested=150)
    assert len(e.inventories()[0]) == 89 and len(e.inventories()[2]) == 30
    assert isqrt(101_999_999) == 10099
    assert e.validate_plan(e.positive_plan())


def test_poison_all_named_and_nested():
    old, new, nested = e.inventories()
    for name, a, b in old + nested + [z for z in new if z[0] != 'H19']:
        plan = e.positive_plan()
        plan[1]['start'], plan[1]['stop'] = a, b
        try: e.validate_plan(plan)
        except (ValueError, AssertionError): pass
        else: pytest.fail(f'accepted forbidden {name}')


def test_poison_complete_plan_before_any_generator(tmp_path):
    calls=[]
    def poison(*args):
        calls.append(args)
        raise AssertionError('generator entered')
    good=e.positive_plan()
    bad=[]
    for idx in (0,1):
        for k in ('start','stop'):
            for delta in (-1,1):
                p=copy.deepcopy(good);p[idx][k]+=delta;bad.append(p)
        for k in ('purpose','strategy'):
            p=copy.deepcopy(good);p[idx][k]='indirect_helper';bad.append(p)
        p=copy.deepcopy(good);p[idx]['extra']='x';bad.append(p)
    bad.extend([good[:1],good+[copy.deepcopy(good[-1])], list(reversed(good)),
                [], [None,good[-1]], [{**good[0], 'start': False},good[1]],
                [good[0],{**good[1], 'stop': True}],
                [good[0], {**good[1], 'start': 0, 'stop': 102_000_000,
                           'strategy':'whole_prefix'}],
                [good[0], {**good[1], 'start': 101_000_000, 'stop': 101_500_000}],
                [good[0], {**good[1], 'start': 101_500_000, 'stop':102_000_000}]])
    for p in bad:
        with pytest.raises((ValueError, AssertionError)):
            e.run(tmp_path/'forbidden.json','a'*40,plan=p,
                  low_generator=poison,high_generator=poison)
    for phase, entry in [('D19','direct'),('A19','direct'),('H19','per_anchor_prime'),
                         ('H19','high_whole_prefix'),('H19','indirect')]:
        with pytest.raises((ValueError, AssertionError)):
            e.run(tmp_path/'forbidden.json','a'*40,plan=good,phase=phase,entry=entry,
                  low_generator=poison,high_generator=poison)
    assert not calls
    assert not (tmp_path/'forbidden.json').exists()


def test_synthetic_mode_positive_and_negative(tmp_path):
    # Fabricate fully controlled labels: NO prime generator and NO high anchor scan.
    p=e.positive_plan(); fake_commit='a'*40
    def build(p_hist, c_hist):
        obj={
            'experiment':'E019','implementation_commit':fake_commit,
            'band':{'name':'H19','range':[101_000_000,102_000_000], 'interval_semantics':'half-open'},
            'partition':[{'name':n,'range':[a,b],'role':r} for n,a,b,r in e.ROLES],
            'parameters':copy.deepcopy(e.PARAMETERS), 'generation_plan':p,
            'anchor_summary':{'wheel_anchor_count':sum(p_hist)+sum(c_hist),
                'prime_count':sum(p_hist),'composite_count':sum(c_hist),
                'prime_counts_by_R210':[sum(p_hist)//48]*48,
                'composite_counts_by_R210':[sum(c_hist)//48]*48},
            'validation':dict.fromkeys(e.VALIDATORS,0), 'families':[], 'promotions':[]}
        obj['anchor_summary']['prime_counts_by_R210'][0] += sum(p_hist)%48
        obj['anchor_summary']['composite_counts_by_R210'][0] += sum(c_hist)%48
        return obj
    obj=build([100]*4,[200]*4)
    f={k: (False if k.endswith('passed') or k in ('strict_unique_prime_mode','aggregate_enrichment_positive','mechanically_eligible') else None) for k in e.FAMILY_KEYS}
    f.update(family='B1', prime_mode_count=100, highest_competing_count=100,
             population_floor_passed=False, class_floor_passed=False)
    obj['families']=[f]
    assert e.validate_payload(obj)
    assert e.canonical(obj) == e.canonical(copy.deepcopy(obj))
    bad=copy.deepcopy(obj);bad['families'][0]['unique_mode_signature']=0
    with pytest.raises(ValueError): e.validate_payload(bad)
    good=build([400,150,150,150],[100,300,300,300])
    # Correct the synthetic population to match the declared label vector.
    good['anchor_summary']['prime_counts_by_R210']=[18]*48
    good['anchor_summary']['prime_counts_by_R210'][0]=850-18*47
    good['anchor_summary']['composite_counts_by_R210']=[21]*48
    good['anchor_summary']['composite_counts_by_R210'][0]=1000-21*47
    gf={'family':'B1','prime_mode_count':400,'highest_competing_count':150,
        'strict_unique_prime_mode':True,'unique_mode_signature':2,
        'target_composite_count':100,'population_floor_passed':False,
        'class_floor_passed':False, 'occurrence_floor_passed':True,
        'mixed_class_count':48,'mixed_class_floor_passed':True,
        'positive_class_count':48,'positive_class_floor_passed':True,
        'aggregate_enrichment_numerator':400*1000-100*850,
        'aggregate_enrichment_positive':True, 'mechanically_eligible':False}
    good['families']=[gf]
    assert e.validate_payload(good)
    gf['aggregate_enrichment_numerator']=0
    gf['aggregate_enrichment_positive']=False
    assert e.validate_payload(good)
    for k in e.VALIDATORS:
        invalid=copy.deepcopy(obj);invalid['validation'][k]=1
        with pytest.raises(ValueError): e.canonical(invalid)


def test_payload_strict_types_and_forbidden_fields():
    # Small consistent schematic empty mode artifact, with no primes generated.
    a={'wheel_anchor_count':0,'prime_count':0,'composite_count':0,
       'prime_counts_by_R210':[0]*48,'composite_counts_by_R210':[0]*48}
    f={'family':'B1','prime_mode_count':0,'highest_competing_count':0,
       'strict_unique_prime_mode':False,'unique_mode_signature':None,
       'target_composite_count':None,'population_floor_passed':False,
       'class_floor_passed':False,'occurrence_floor_passed':False,
       'mixed_class_count':None,'mixed_class_floor_passed':False,
       'positive_class_count':None,'positive_class_floor_passed':False,
       'aggregate_enrichment_numerator':None,'aggregate_enrichment_positive':False,
       'mechanically_eligible':False}
    o={'experiment':'E019','implementation_commit':'a'*40,
       'band':{'name':'H19','range':[101_000_000,102_000_000],'interval_semantics':'half-open'},
       'partition':[{'name':n,'range':[l,u],'role':r} for n,l,u,r in e.ROLES],
       'parameters':copy.deepcopy(e.PARAMETERS),'generation_plan':e.positive_plan(),
       'anchor_summary':a,'validation':dict.fromkeys(e.VALIDATORS,0),
       'families':[f],'promotions':[]}
    assert e.canonical(o).endswith(b'\n')
    checks=[('extra',42),('anchor_ids',[99_000_001]),('prime_list',[3]),('time','now')]
    for k,v in checks:
        q=copy.deepcopy(o);q[k]=v
        with pytest.raises(ValueError): e.canonical(q)
    q=copy.deepcopy(o);q['anchor_summary']['prime_count']=True
    with pytest.raises(ValueError): e.canonical(q)
    q=copy.deepcopy(o);q['families'][0]['prime_mode_count']=1.0
    with pytest.raises(ValueError): e.canonical(q)
    q=copy.deepcopy(o);q['parameters']['strict_global_enrichment']=1
    with pytest.raises(ValueError): e.canonical(q)
    q=copy.deepcopy(o);q['validation']['serializer_failure_count']=True
    with pytest.raises(ValueError): e.canonical(q)
    q=copy.deepcopy(o);q['parameters']['residues_R210'][0]=True
    with pytest.raises(ValueError): e.canonical(q)
    q=copy.deepcopy(o);q['band']['range'][0]=True
    with pytest.raises(ValueError): e.canonical(q)
    q=copy.deepcopy(o);q['partition'][0]['range'][0]=True
    with pytest.raises(ValueError): e.canonical(q)
    q=copy.deepcopy(o);q['promotions']=[{'family':'B1'}]
    with pytest.raises(ValueError): e.canonical(q)


def test_fixed_integer_two_no_search_or_fallback():
    assert e.fixed_target_mode({0: 4, 1: 3, 2: 7, 3: 6}) == (7,6,True)
    assert e.fixed_target_mode({0: 8, 1: 0, 2: 7, 3: 0}) == (7,8,False)
    assert e.fixed_target_mode({0: 8, 1: 0, 2: 8, 3: 0}) == (8,8,False)
    assert e.fixed_target_mode({0: 8, 1: 0, 3: 1}) == (0,8,False)
    assert e.fixed_target_mode({2: 32}) == (32,0,True)
    with pytest.raises(ValueError): e.fixed_target_mode({2: True})
    with pytest.raises(ValueError): e.fixed_target_mode({4: 1})


def test_one_support_duplicate_and_cap():
    s={11,31,41}; equal={41,11,31}; same_count={13,19,29}
    assert s == equal and s != same_count
    kept=[]
    for incoming in (s,equal):
        if not any(incoming==other for other in kept):kept.append(incoming)
    assert len(kept)==1
