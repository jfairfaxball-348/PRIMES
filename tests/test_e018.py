"""Synthetic-only E018 independent references; NEVER generate a high prime here."""
import copy
import importlib.util
import json
import sys
from itertools import combinations
from math import gcd, isqrt
from pathlib import Path

import pytest

S = Path(__file__).resolve().parents[1] / 'experiments' / 'E018_monomer_domino_tromino_tiling_residue_shapes.py'
spec=importlib.util.spec_from_file_location('e018_frozen',S)
e=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=e
spec.loader.exec_module(e)


def enumerate_tilings(n):
    if n == 0:
        return [()]
    return [(k,)+row for k in (1,2,3) if k<=n for row in enumerate_tilings(n-k)]


def reference_direct(n):
    if n<0:
        return 0
    return len(enumerate_tilings(n)) if n<=10 else (
        reference_recurrence(n))


def reference_recurrence(n):
    t=[1,0,0]
    for _ in range(n):
        t=[sum(t),t[0],t[1]]
    return t[0]


def independent_matrix_n(n):
    v=[2,1,1]
    for _ in range(n):
        v=[v[0]+v[1]+v[2],v[0],v[1]]
    return v


def test_exact_tilings_recurrence_matrix_all_small():
    assert [len(enumerate_tilings(n)) for n in range(4)]==[1,1,2,4]
    for n in range(11):
        assert len(enumerate_tilings(n))==reference_recurrence(n)
    for n in range(1,80):
        v=independent_matrix_n(n)
        assert v==[reference_recurrence(n+2),reference_recurrence(n+1),reference_recurrence(n)]
        assert e.tiling_remainder(n)==v[2]%n
    e._reference_checks()


def test_mod_exponent_boundaries_and_large_integer_safety():
    assert e.tiling_remainder(1)==0
    assert e.tiling_remainder(2)==0
    assert e.tiling_remainder(3)==1
    for n in (4,7,8,16,31,32,33,64,127,128,129,257,1024):
        assert e.tiling_remainder(n)==reference_recurrence(n)%n
    # No floating-point is permitted even when square/power is too large for machine ints.
    for n in (10**30+19,2**128+51):
        r=e.tiling_remainder(n)
        assert type(r) is int and 0<=r<n
    for n in (0,-1,1.0,True):
        with pytest.raises(ValueError):
            e.tiling_remainder(n)


def test_signature_full_domains_coarsening_and_type_rejection():
    n=997
    pairs=[e.binned(n,r) for r in range(n)]
    assert {a for a,_ in pairs}==set(range(4))
    assert {b for _,b in pairs}==set(range(8))
    assert all(a==b//2 for a,b in pairs)
    assert e.binned(2,0)==(0,0)
    assert e.binned(2,1)==(2,4)
    for x,r in ((1,0),(0,0),(2,2),(5,-1),(5,2.0),(5,True)):
        with pytest.raises(ValueError):
            e.binned(x,r)


def test_complete_unique_mode_including_zeros_and_ties():
    assert e.strict_mode([13,0,0,0])==(13,0,0)
    assert e.strict_mode([0,1,7,2])==(7,2,2)
    assert e.strict_mode([0,2,2,0])==(2,2,None)
    assert e.strict_mode([0]*8)==(0,0,None)
    with pytest.raises(ValueError):
        e.strict_mode([])
    with pytest.raises(ValueError):
        e.strict_mode([True,0,0,0])


def test_signed_exact_enrichment_and_strict_class_mix():
    assert e.signed_enrichment(2,10,4,10)==-20
    assert e.signed_enrichment(5,10,5,10)==0
    assert e.signed_enrichment(7,10,1,10)==60
    assert e.fully_mixed(1,2,1,2)
    assert not e.fully_mixed(0,2,1,2)
    assert not e.fully_mixed(2,2,1,2)
    assert not e.fully_mixed(1,2,0,2)
    assert not e.fully_mixed(1,2,2,2)
    with pytest.raises(ValueError):
        e.signed_enrichment(True,10,2,10)
    with pytest.raises(ValueError):
        e.fully_mixed(4,3,1,2)


def test_exact_integer_sets_duplicate_cap_and_zero_promotions():
    assert e.select_supports([])==[]
    rows=[('L1',1,{101,211}),('L2',3,{101,211})]
    assert e.select_supports(rows)==[rows[0]]
    same_cardinality_distinct=[('L1',1,{101,211}),('L2',3,{101,223})]
    assert e.select_supports(same_cardinality_distinct)==same_cardinality_distinct
    with pytest.raises(ValueError):
        e.select_supports([('L2',3,{101}),('L1',1,{211})])
    with pytest.raises(ValueError):
        e.select_supports([('L1',1,{101}),('L2',3,{211}),('L2',4,{307})])
    with pytest.raises(ValueError):
        e.select_supports([('L1',1,{True})])


def test_complete_wheel_48_reduced_classes_and_partition():
    assert len(e.R210)==48
    assert tuple(i for i in range(210) if gcd(i,210)==1)==e.R210
    for left in (0,1,209,210,211,419,420,421,499):
        right=left+1000
        anchor=[x for x in range(left,right) if gcd(x,210)==1]
        partition=[x for x in range(left,right) if x%210 in e.R210]
        assert anchor==partition
    assert e.R210[0]==1 and e.R210[-1]==209


def test_named_interval_metadata_audit_and_containments():
    assert e.interval_audit()==(3486,430,30,150)
    assert len(e.EARLY)==53 and len(e.LATE)==25
    assert len(e.HISTORIC)==84 and len(e.NESTED)==30
    assert len({x[0] for x in e.HISTORIC})==84
    assert len(set((x[1],x[2]) for x in e.HISTORIC))==84
    assert sum(1 for a,b in combinations(e.HISTORIC,2) if e._overlap(a,b))==0
    assert sum(1 for a in e.ROLES for b in e.HISTORIC if e._overlap(a,b))==0
    assert sum(1 for a,b in combinations(e.ROLES,2) if e._overlap(a,b))==0
    for i,s in enumerate(e.CAL_STARTS):
        maximum=e.HISTORIC[78+i]
        assert maximum==(f'E005-max-{i+1}',s,s+1048576)
        assert all(s <= q[1] < q[2] <= maximum[2] for q in e.NESTED if q[1]==s)
    assert isqrt(95_999_999)==9797
    assert e.ROLES[4][1]==2*e.ROLES[1][1]


def poison():
    raise AssertionError('generator entered on poison')


def poison_base(stop):
    return poison()


def poison_segment(start,stop,base):
    return poison()


def test_positive_full_plan_boundaries_with_fakes_only():
    calls=[]
    def fakebase(stop):
        calls.append(('base_sieve_support',0,stop,'whole_prefix'))
        return [2,3,5]
    def fakesegment(start,stop,base):
        assert base==[2,3,5]
        calls.append(('segmented_target',start,stop,'direct_segmented'))
        return set()
    assert e.execute_plan('D18',[dict(x) for x in e.D18_PLAN],fakebase,fakesegment)==set()
    assert calls==[('base_sieve_support',0,9798,'whole_prefix'),
                   ('segmented_target',95_000_000,96_000_000,'direct_segmented')]


def test_all_historic_nested_and_off_phase_poison_never_enters_either_generator():
    for name,l,u in e.HISTORIC+e.NESTED+tuple(r for r in e.ROLES if r[0]!='D18'):
        plan=[dict(x) for x in e.D18_PLAN]
        plan[1]['start']=l
        plan[1]['stop']=u
        with pytest.raises(ValueError,match='plan|allowlist|square root|support'):
            e.execute_plan('D18',plan,poison_base,poison_segment)


def test_malformed_extra_split_shift_high_prefix_indirect_reorder_poison():
    base=[dict(x) for x in e.D18_PLAN]
    bad=[]
    bad.append([base[1],base[0]])
    bad.append([base[0]])
    bad.append([*base,dict(base[1])])
    bad.append([*base,{'purpose':'segmented_target','start':96_000_000,
                      'stop':97_000_000,'strategy':'direct_segmented'}])
    bad.append([base[0],dict(base[1],start=95_000_001)])
    bad.append([base[0],dict(base[1],stop=95_999_999)])
    bad.append([dict(base[0],stop=9797),base[1]])
    bad.append([dict(base[0],stop=9799),base[1]])
    bad.append([dict(base[0],stop=96_000_000),base[1]])
    bad.append([dict(base[0],strategy='direct_segmented'),base[1]])
    bad.append([base[0],dict(base[1],strategy='whole_prefix')])
    bad.append([base[0],dict(base[1],strategy='indirect_segmented')])
    bad.append([base[0],dict(base[1],purpose='primality_helper')])
    bad.append([base[0],dict(base[1],extra=1)])
    bad.append([dict(base[0],start=True),base[1]])
    bad.append([dict(base[0],stop=9798.0),base[1]])
    bad.append((dict(base[0]),dict(base[1],start=94_999_999)))
    bad.append('indirect generator plan')
    for plan in bad:
        with pytest.raises(ValueError):
            e.execute_plan('D18',plan,poison_base,poison_segment)
    for phase in ('H18','A18','G18-pre','D17','D18 ',''):
        with pytest.raises(ValueError):
            e.execute_plan(phase,base,poison_base,poison_segment)


def fixture_payload():
    popP=[20]*48
    popC=[30]*48
    def fam(name,domain,unique=True):
        return dict(family=name,prime_mode_count=300,highest_competing_count=220,
                    strict_unique_prime_mode=unique,unique_mode_signature=1 if unique else None,
                    target_composite_count=100 if unique else None,
                    population_floor_passed=False,class_floor_passed=True,
                    occurrence_floor_passed=unique,mixed_class_count=48 if unique else None,
                    mixed_class_floor_passed=unique,positive_class_count=35 if unique else None,
                    positive_class_floor_passed=unique,
                    aggregate_enrichment_numerator=100 if unique else None,
                    aggregate_enrichment_positive=unique,mechanically_eligible=False)
    names=('non-target guard','discovery','non-target guard','one-shot holdout',
           'independently locked adversarial reserve')
    return {'experiment':'E018','implementation_commit':'a'*40,
            'band':{'name':'D18','range':[95000000,96000000],
                    'interval_semantics':'half-open'},
            'partition':[{'name':x,'range':[l,u],'role':v}
                         for (x,l,u),v in zip(e.ROLES,names)],
            'parameters':copy.deepcopy(e.PARAMETERS),
            'generation_plan':[dict(x) for x in e.D18_PLAN],
            'anchor_summary':{'wheel_anchor_count':2400,'prime_count':960,
                              'composite_count':1440,
                              'prime_counts_by_R210':popP,'composite_counts_by_R210':popC},
            'validation':{k:0 for k in e.VALIDATORS},
            'families':[fam('L1',4),fam('L2',8,False)],'promotions':[]}


def test_canonical_serializer_strict_allowlists_types_bytes_empty_promos():
    p=fixture_payload()
    b=e.canonical_bytes(p)
    assert b==(json.dumps(p,sort_keys=True,indent=2,ensure_ascii=True)+'\n').encode()
    assert b.endswith(b'\n') and not b.endswith(b'\n\n')
    assert json.loads(b)==p
    assert e.canonical_bytes(p)==b


def test_serialize_rejects_forbidden_data_nested_extras_and_ties():
    modifications=[
      lambda p:p.update({'prime_anchor_ids':[11,13]}),
      lambda p:p['band'].update({'clock':'never'}),
      lambda p:p['partition'][0].update({'timestamp':'now'}),
      lambda p:p['parameters'].update({'source':'calibration'}),
      lambda p:p['parameters'].update({'population_floor':True}),
      lambda p:p['parameters'].update({'tile_lengths':[1,2,4]}),
      lambda p:p['generation_plan'][0].update({'stop':9799}),
      lambda p:p['anchor_summary'].update({'prime_counts_by_R210':[20]*47}),
      lambda p:p['anchor_summary'].update({'full_frequency_table':[1,2]}),
      lambda p:p['validation'].update({'serializer_failure_count':1}),
      lambda p:p['validation'].update({'serializer_failure_count':False}),
      lambda p:p['families'][0].update({'support_set':[101]}),
      lambda p:p['families'][0].update({'prime_mode_count':300.0}),
      lambda p:p['families'][0].update({'strict_unique_prime_mode':1}),
      lambda p:p['families'][0].update({'strict_unique_prime_mode':False}),
      lambda p:p['families'][0].update({'unique_mode_signature':4}),
      lambda p:p['families'][0].update({'aggregate_enrichment_numerator':'100'}),
      lambda p:p.update({'promotions':[{'family':'L2'}]}),
      lambda p:p['partition'].reverse(),
      lambda p:p['families'].reverse(),
    ]
    for mutation in modifications:
        p=fixture_payload()
        mutation(p)
        with pytest.raises(ValueError):
            e.canonical_bytes(p)


def test_serializer_rejects_fake_promotion_and_accepts_consistent_one():
    p=fixture_payload()
    p['families'][0]['mechanically_eligible']=True
    with pytest.raises(ValueError):
        e.canonical_bytes(p)
    f=p['families'][0]
    p['promotions']=[dict(family='L1',target_signature=f['unique_mode_signature'],
                          target_prime_count=f['prime_mode_count'],
                          target_composite_count=f['target_composite_count'],
                          mixed_class_count=f['mixed_class_count'],
                          positive_class_count=f['positive_class_count'],
                          aggregate_enrichment_numerator=f['aggregate_enrichment_numerator'])]
    assert e.canonical_bytes(p)
    p['promotions'][0]['target_prime_count']+=1
    with pytest.raises(ValueError):
        e.canonical_bytes(p)


def test_no_prime_or_high_helper_from_tiling_path():
    import ast
    tree=ast.parse(S.read_text())
    defs={n.name:n for n in tree.body if isinstance(n,ast.FunctionDef)}
    for name in ('tiling_remainder','matrix_product','binned'):
        content=ast.unparse(defs[name]).lower()
        for forbidden in ('_segmented_target','_base_sieve_support',
                          'is_prime(', 'prime_test(', 'sympy', 'primepi'):
            assert forbidden not in content
