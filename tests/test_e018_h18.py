"""Pure synthetic E018 H18 tests. No high target generator or traversal."""
import copy
import importlib.util
import json
import sys
from itertools import combinations
from math import gcd, isqrt
from pathlib import Path

import pytest

SOURCE = Path(__file__).resolve().parents[1] / 'experiments/E018_H18_fixed_replication.py'
spec = importlib.util.spec_from_file_location('e018_h18_fixed', SOURCE)
h = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = h
spec.loader.exec_module(h)


def test_tiling_first_values_independent_count_and_modular_identity():
    h.reference_checks()
    t = [1, 1, 2]
    for _ in range(1100):
        t.append(sum(t[-3:]))
    assert t[:4] == [1, 1, 2, 4]
    for n in (1, 2, 3, 4, 5, 8, 32, 128, 1024):
        assert h.tiling_mod(n) == t[n] % n
    for n in (10**30+19, 2**128+51):
        r = h.tiling_mod(n)
        assert type(r) is int and 0 <= r < n
    for n in (0, -5, 2.0, True):
        with pytest.raises(ValueError):
            h.tiling_mod(n)


def test_full_signature_domain_and_coarsening():
    assert len(h.RESIDUES) == 48
    assert h.RESIDUES == tuple(r for r in range(210) if gcd(r, 210) == 1)
    b = [h.bins(997, r) for r in range(997)]
    assert {p for p, _ in b} == set(range(4))
    assert {q for _, q in b} == set(range(8))
    assert all(p == q//2 for p, q in b)
    for args in ((1, 0), (2, 2), (11, -1), (11, 0.5), (True, 0)):
        with pytest.raises(ValueError):
            h.bins(*args)


def test_interval_named_inventory_and_roots():
    assert h.interval_audit() == (3486, 430, 30, 150)
    assert len(h.EARLY) == 53 and len(h.LATE) == 25
    assert len(h.HISTORY) == 84 and len(h.NESTED) == 30
    assert all(not h.intersects(a, b) for a, b in combinations(h.HISTORY, 2))
    assert all(not h.intersects(a, b) for a in h.ROLES for b in h.NESTED)
    for s in h.CAL_STARTS:
        assert len([n for n in h.NESTED if n[1] == s]) == 5
    assert isqrt(97_999_999) == 9899


def reject_base(*_):
    raise AssertionError('poison passed the base boundary')


def reject_segment(*_):
    raise AssertionError('poison passed the high boundary')


def test_positive_full_plan_fake_generators_exact_order():
    calls = []

    def base(stop):
        calls.append(('base_sieve_support', 0, stop, 'whole_prefix'))
        return (2, 3, 5)

    def segment(a, b, small):
        assert small == (2, 3, 5)
        calls.append(('segmented_target', a, b, 'direct_segmented'))
        return set()

    assert h.run_plan('H18', [dict(z) for z in h.PLAN], base, segment) == set()
    assert calls == [('base_sieve_support', 0, 9900, 'whole_prefix'),
                     ('segmented_target', 97_000_000, 98_000_000, 'direct_segmented')]


def test_all_84_historic_30_nested_and_offphase_poison():
    excluded = h.HISTORY+h.NESTED+tuple(z for z in h.ROLES if z[0] != 'H18')
    assert len(excluded) == 118
    for _, a, b in excluded:
        entries = [dict(z) for z in h.PLAN]
        entries[1]['start'], entries[1]['stop'] = a, b
        with pytest.raises(ValueError):
            h.run_plan('H18', entries, reject_base, reject_segment)


def test_malformed_indirect_split_reorder_shift_highprefix_and_phase_poison():
    good = [dict(z) for z in h.PLAN]
    bad = [[], [good[0]], [good[1], good[0]], [*good, good[1]],
           [dict(good[0], stop=9901), good[1]],
           [dict(good[0], stop=9899), good[1]],
           [dict(good[0], stop=98_000_000), good[1]],
           [dict(good[0], strategy='segmented_target'), good[1]],
           [good[0], dict(good[1], start=97_000_001)],
           [good[0], dict(good[1], stop=97_999_999)],
           [good[0], dict(good[1], stop=98_000_001)],
           [good[0], dict(good[1], start=96_999_999)],
           [good[0], dict(good[1], strategy='whole_prefix')],
           [good[0], dict(good[1], strategy='indirect_segmented')],
           [good[0], dict(good[1], purpose='prime_test')],
           [good[0], dict(good[1], extra=True)],
           [dict(good[0], start=True), good[1]],
           [dict(good[0], stop=9900.0), good[1]],
           'high-prefix']
    for entry in bad:
        with pytest.raises(ValueError):
            h.run_plan('H18', entry, reject_base, reject_segment)
    for phase in ('D18', 'A18', 'H17', 'G18-pre', 'H18 ', None):
        with pytest.raises(ValueError):
            h.run_plan(phase, good, reject_base, reject_segment)


def case(domain=4, prime_target=600, composite_target=450, other=360):
    # Equal 48-class totals, exact positive E and positive signed strata.
    pp = [20]*48
    pc = [30]*48
    tp = [prime_target//48]*48
    tc = [composite_target//48]*48
    for i in range(prime_target % 48):
        tp[i] += 1
    for i in range(composite_target % 48):
        tc[i] += 1
    counts_p = [prime_target, other]+[0]*(domain-2)
    counts_c = [composite_target, 1440-composite_target]+[0]*(domain-2)
    # Preserve full-domain conservation for prime population 960.
    assert prime_target+other == 960
    return counts_p, counts_c, pp, pc, tp, tc, set(range(101, 101+prime_target))


def test_fixed_target_unique_positive_and_all_negative_gates():
    args = case()
    f = h.fixed_zero_gate('L1', *args)
    assert f['strict_unique_prime_mode'] and f['unique_mode_signature'] == 0
    assert not f['population_floor_passed'] and not f['mechanically_eligible']
    # A full synthetic above-total-floor case on 48 classes.
    freq_p = [1200, 720, 0, 0]
    freq_c = [600, 2280, 0, 0]
    pp = [40]*48
    pc = [60]*48
    tp = [25]*48
    tc = [12]*48  # 576 class target, reconcile to 600 below
    for k in range(24):
        tc[k] += 1
    f = h.fixed_zero_gate('L1', freq_p, freq_c, pp, pc, tp, tc, set(range(1200)))
    assert f['mechanically_eligible'] and f['mixed_class_count'] == 48
    assert f['positive_class_count'] == 48 and f['aggregate_enrichment_numerator'] > 0
    tie = h.fixed_zero_gate('L1', [960, 960, 0, 0], freq_c, pp, pc,
                            [20]*48, tc, set(range(960)))
    assert not tie['strict_unique_prime_mode'] and tie['unique_mode_signature'] is None
    assert not tie['mechanically_eligible']
    greater = h.fixed_zero_gate('L1', [480, 1440, 0, 0], freq_c, pp, pc,
                                [10]*48, tc, set(range(480)))
    assert not greater['mechanically_eligible']
    no_target = h.fixed_zero_gate('L1', [0, 1920, 0, 0], freq_c, pp, pc,
                                  [0]*48, tc, set())
    assert not no_target['mechanically_eligible']
    with pytest.raises(ValueError):
        h.fixed_zero_gate('L2', freq_p, freq_c, pp, pc, tp, tc, set(range(1200)))


def test_signed_mix_support_equality_and_cap():
    assert h.difference(7, 10, 1, 10) == 60
    assert h.difference(5, 10, 5, 10) == 0
    assert h.difference(2, 10, 4, 10) == -20
    assert h.mix(1, 2, 1, 2)
    assert not h.mix(0, 2, 1, 2) and not h.mix(2, 2, 1, 2)
    with pytest.raises(ValueError):
        h.difference(True, 10, 2, 10)
    a = ('L1', 0, {101, 211})
    b = ('L2', 0, {101, 211})
    c = ('L2', 0, {101, 223})
    assert h.retain([]) == [] and h.retain([a, b]) == [a]
    assert h.retain([a, c]) == [a, c]
    with pytest.raises(ValueError):
        h.retain([b, a])
    with pytest.raises(ValueError):
        h.retain([a, b, c])


def fixture():
    counts = [20]*48
    comps = [30]*48
    def fam(name):
        return dict(family=name, prime_mode_count=300, highest_competing_count=280,
                    strict_unique_prime_mode=False, unique_mode_signature=None,
                    target_composite_count=None, population_floor_passed=False,
                    class_floor_passed=True, occurrence_floor_passed=False,
                    mixed_class_count=None, mixed_class_floor_passed=False,
                    positive_class_count=None, positive_class_floor_passed=False,
                    aggregate_enrichment_numerator=None, aggregate_enrichment_positive=False,
                    mechanically_eligible=False)
    return {'experiment': 'E018', 'implementation_commit': 'a'*40,
            'band': {'name': 'H18', 'range': [h.LOW, h.HIGH], 'interval_semantics': 'half-open'},
            'partition': [dict(name=n, range=[a, b], role=r)
                          for (n, a, b), r in zip(h.ROLES, h.ROLE_LABELS)],
            'parameters': copy.deepcopy(h.PARAMS),
            'generation_plan': [dict(z) for z in h.PLAN],
            'anchor_summary': dict(wheel_anchor_count=2400, prime_count=960,
                                   composite_count=1440, prime_counts_by_R210=counts,
                                   composite_counts_by_R210=comps),
            'validation': {k: 0 for k in h.VALIDATION_KEYS},
            'families': [fam('L1'), fam('L2')], 'promotions': []}


def test_both_serializer_outcomes_and_canonical_bytes():
    payload = fixture()
    raw = h.canonical(payload)
    assert raw == (json.dumps(payload, sort_keys=True, indent=2, ensure_ascii=True)+'\n').encode()
    assert raw.endswith(b'\n') and not raw.endswith(b'\n\n')
    f = payload['families'][0]
    f.update(strict_unique_prime_mode=True, unique_mode_signature=0,
             target_composite_count=100, occurrence_floor_passed=True,
             mixed_class_count=40, mixed_class_floor_passed=True,
             positive_class_count=35, positive_class_floor_passed=True,
             aggregate_enrichment_numerator=1000, aggregate_enrichment_positive=True,
             mechanically_eligible=True)
    payload['promotions'] = [dict(family='L1', target_signature=0,
                                   target_prime_count=f['prime_mode_count'],
                                   target_composite_count=f['target_composite_count'],
                                   mixed_class_count=40, positive_class_count=35,
                                   aggregate_enrichment_numerator=1000)]
    assert h.canonical(payload)
    payload['promotions'][0]['target_signature'] = 1
    with pytest.raises(ValueError):
        h.canonical(payload)


def test_strict_nested_schema_zero_validators_and_no_leaks():
    changes = [lambda p: p.update(prime_anchor_ids=[1]),
               lambda p: p['band'].update(clock='now'),
               lambda p: p['partition'][0].update(extra='x'),
               lambda p: p['parameters'].update(tile_lengths=[1, 2, 4]),
               lambda p: p['parameters'].update(population_floor=True),
               lambda p: p['generation_plan'][1].update(stop=97_999_999),
               lambda p: p['validation'].update(plan_failure_count=1),
               lambda p: p['validation'].update(plan_failure_count=False),
               lambda p: p['families'][0].update(prime_mode_count=True),
               lambda p: p['families'][0].update(target_composite_count=5),
               lambda p: p['families'][0].update(unique_mode_signature=1),
               lambda p: p['families'][0].update(per_class_support=[1]),
               lambda p: p['anchor_summary'].update(prime_count=961),
               lambda p: p['anchor_summary'].update(composite_counts_by_R210=[30]*47),
               lambda p: p['partition'].reverse(),
               lambda p: p['families'].reverse(),
               lambda p: p.update(promotions=[{'family':'L1'}])]
    for change in changes:
        p = fixture()
        change(p)
        with pytest.raises(ValueError):
            h.canonical(p)
