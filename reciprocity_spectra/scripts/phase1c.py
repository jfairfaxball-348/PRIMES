"""RS-S004: certify a conditional structural null and run frozen comparisons.

OPENBLAS_NUM_THREADS=2 OMP_NUM_THREADS=4. Each spectrum/moment component
has its own 2700-second alarm and incremental checkpoint. --resume is implicit:
completed components are retained, never duplicated. Pushes are serialized.
"""
from __future__ import annotations

import argparse
import ctypes as ct
import hashlib
import json
import math
import signal
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

import numpy as np
from scipy.linalg import svdvals
from scipy.sparse.linalg import svds

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import phase1 as legacy  # noqa: E402
import phase1b as previous  # noqa: E402

from reciprocity_spectra.arith import DegreeOnePrime  # noqa: E402
from reciprocity_spectra.null_model import (  # noqa: E402
    conjugate_pair_phase,
    conjugate_permutation,
    reference_control,
)

DATA = legacy.DATA
RESULT = ROOT/'reciprocity_spectra/results/phase1c_2026-10-25.json'
BRANCH = 'rs-s004-phase1c'
REGISTRATION = '5502ba3'
ORDER = {'quad': 2, 'cubic': 3, 'quartic': 4, 'sextic': 6}


def digest(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def command():
    return 'OPENBLAS_NUM_THREADS=2 OMP_NUM_THREADS=4 python '+' '.join(sys.argv)


def save(doc, message=None):
    temp = RESULT.with_suffix('.tmp')
    temp.write_text(json.dumps(doc, indent=2, allow_nan=False)+'\n')
    temp.replace(RESULT)
    if message:
        assert legacy.shell('git', 'branch', '--show-current') == BRANCH
        legacy.shell('git', 'add', str(RESULT))
        legacy.shell('git', 'commit', '-m', message)
        for attempt in range(3):
            try:
                print(legacy.shell('git', 'push', '-u', 'origin', BRANCH), flush=True)
                break
            except subprocess.CalledProcessError:
                if attempt == 2:
                    raise
                time.sleep(1)


def metadata(a):
    if hasattr(a, 'certified_metadata'):
        return a.certified_metadata
    ring = 3 if a.n == 6 else a.n
    index = [int(p) if a.n == 2 else DegreeOnePrime(ring, int(p), int(u), int(v))
             for p, u, v in a.meta.tolist()]
    bar = np.ascontiguousarray(conjugate_permutation(a.n, index), dtype=np.int32)
    forced = np.ascontiguousarray([255 if a.n == 2 else conjugate_pair_phase(a.n, x)
                                  for x in index], dtype=np.uint8)
    primes = np.ascontiguousarray(a.meta[:, 0], dtype=np.int64)
    neg = np.arange(256, dtype=np.uint8)
    neg[:a.n] = (-np.arange(a.n)) % a.n
    neg[255] = 255
    assert np.array_equal(forced[bar], neg[forced])
    a.certified_metadata = (bar, forced, primes, index)
    return a.certified_metadata


def certified_control(a, seed):
    bar, forced, primes, _ = metadata(a)
    outpath = DATA/f'certified_{a.mode}_{a.x}_seed{seed}.bin'
    output = np.memmap(outpath, dtype=np.uint8, mode='w+', shape=(a.d, a.d))
    a.lib.rs_certified_random.argtypes = [ct.c_void_p]*5+[ct.c_int, ct.c_int, ct.c_uint64]
    a.lib.rs_certified_random.restype = ct.c_uint64
    signs = a.signs.ctypes.data if a.n == 6 else 0
    errors = a.lib.rs_certified_random(output.ctypes.data, signs, bar.ctypes.data,
                                       forced.ctypes.data, primes.ctypes.data, a.d, a.n, seed)
    if errors:
        raise ArithmeticError(f'{errors} inconsistent certified-control orbits')
    output.flush()
    a.e = output
    a.certified_path = outpath
    return outpath


def audit(a):
    """All-entry exact audit using bounded uint8/int16 blocks, never dense floats."""
    bar, forced, _, _ = metadata(a)
    neg = np.arange(256, dtype=np.uint8)
    neg[:a.n] = (-np.arange(a.n)) % a.n
    neg[255] = 255
    diag = np.asarray(a.e[np.arange(a.d), np.arange(a.d)])
    counts = {'diagonal_mismatches': int(np.sum(diag != 255)),
              'conjugation_mismatches': 0, 'reciprocity_mismatches': 0,
              'boundary_mismatches': int(np.sum(a.e[np.arange(a.d), bar] != forced)),
              'invalid_exponents': 0, 'off_diagonal_zeros': 0,
              'sextic_mask_conjugation_mismatches': 0}
    zero_count = 0
    for lo in range(0, a.d, 64):
        hi = min(a.d, lo+64)
        raw = np.asarray(a.e[lo:hi])
        zero_count += int(np.sum(raw == 255))
        counts['invalid_exponents'] += int(np.sum((raw >= a.n) & (raw != 255)))
        conjugated = a.e[bar[lo:hi, None], bar[None, :]]
        counts['conjugation_mismatches'] += int(np.sum(conjugated != neg[raw]))
        if a.n == 6:
            turn = a.signs[lo:hi]*3
            counts['sextic_mask_conjugation_mismatches'] += int(np.sum(
                a.signs[bar[lo:hi, None], bar[None, :]] != a.signs[lo:hi]))
        elif a.n in (2, 4):
            turn = a.odd[lo:hi, None]*a.odd[None, :]*(a.n//2)
        else:
            turn = 0
        reversed_codes = (raw.astype(np.int16)+turn) % a.n
        reversed_codes[raw == 255] = 255
        counts['reciprocity_mismatches'] += int(np.sum(a.e[:, lo:hi].T != reversed_codes))
    counts['off_diagonal_zeros'] = zero_count-int(np.sum(diag == 255))
    if any(counts.values()):
        raise ArithmeticError(f'Structural audit failed: {counts}')
    return {'checked_entries': a.d*a.d, 'counts': counts, 'all_exact': True}


def build(mode, x):
    return previous.build_sextic(x) if mode == 'sextic' else legacy.build(mode, x)


def read(mode, x):
    path = DATA/f'{mode}_{x}.bin'
    if not path.exists():
        return build(mode, x)
    return previous.SexticEngine(x) if mode == 'sextic' else legacy.Engine(mode, x)


def stamp():
    return {'code_commit': legacy.shell('git', 'rev-parse', 'HEAD'), 'command': command(),
            'at_utc': datetime.now(UTC).isoformat()}


def outcome(doc, identity, passed, values):
    prediction = next(p for p in doc['predictions'] if p['id'] == identity)
    return {'id': identity, 'prediction': prediction['prediction'],
            'role': prediction['role'], 'outcome': 'PASS' if passed else 'FAIL', **values}


def validate():
    out = {'classification': 'VALIDATION; old-scale spectra are EXPLORATORY and not status drivers',
           'legacy_and_sextic_overlap': previous.validate(), 'reference_controls_500': {},
           'numerical_controls_2000': {}}
    for mode, n in ORDER.items():
        a = build(mode, 500)
        out['reference_controls_500'][mode] = {'arithmetic_audit': audit(a), 'seeds': {}}
        for seed in (0, 1):
            certified_control(a, seed)
            expected = reference_control(n, metadata(a)[3], seed)
            expected = np.array([[255 if v is None else v for v in row] for row in expected], dtype=np.uint8)
            assert np.array_equal(a.e, expected)
            item = {'byte_identical_to_python_BFS': True, 'audit': audit(a),
                    'sha256': digest(a.certified_path)}
            if n == 2:
                old = np.empty((a.d, a.d), dtype=np.uint8)
                a.lib.rs_random(old.ctypes.data, a.d, a.n, metadata(a)[2].ctypes.data, seed)
                assert np.array_equal(old, a.e)
                item['byte_identical_to_old_quadratic_null'] = True
            out['reference_controls_500'][mode]['seeds'][str(seed)] = item
        a = build(mode, 2000)
        out['numerical_controls_2000'][mode] = {}
        for seed in (0, 1):
            certified_control(a, seed)
            structural = audit(a)
            dense = a.dense()
            s, _, residuals = a.top(8)
            ref = np.sort(svds(dense, k=8, tol=1e-12, return_singular_vectors=False,
                               rng=np.random.default_rng(2)))[::-1]
            error = float(np.max(abs(s/ref-1)))
            assert error < 1e-8
            rng = np.random.default_rng(3)
            z = rng.normal(size=a.d)+1j*rng.normal(size=a.d)
            errors = [float(np.linalg.norm(a.apply(z)-dense@z)/np.linalg.norm(dense@z)),
                      float(np.linalg.norm(a.apply(z, True)-dense.conj().T@z)
                            / np.linalg.norm(dense.conj().T@z))]
            assert max(errors) < 1e-12
            out['numerical_controls_2000'][mode][str(seed)] = {
                'D': a.d, 'structural_audit': structural, 'top8': s.tolist(),
                'reference_top8': ref.tolist(), 'max_relative_error': error,
                'complex_product_relative_errors': errors, 'gram_relative_residuals': residuals}
        print('certified validation', mode, flush=True)
    out.update(passed=True, native_source_sha256=digest(ROOT/'reciprocity_spectra/native/residue_engine.c'),
               null_source_sha256=digest(ROOT/'reciprocity_spectra/null_model.py'), **stamp())
    return out


def local(doc, mode):
    x = 80000
    row = next((r for r in doc['local_runs'] if r['mode'] == mode), None)
    if row and row.get('complete'):
        return
    if row is None:
        row = {'mode': mode, 'X': x, 'controls': {}}
        doc['local_runs'].append(row)
    if 'arithmetic' not in row:
        signal.alarm(2700)
        started = time.monotonic()
        a = build(mode, x)
        row.update(D=a.d, matrix_sha256=digest(a.path))
        structural = audit(a)
        values = svdvals(a.dense(), overwrite_a=True, check_finite=False)
        row['arithmetic'] = {**stamp(), 'audit': structural, 'singular_values_desc': values.tolist(),
                             'statistic': previous.gap_ratio(values, a.d),
                             'sigma1_over_edge': float(values[0]/(2*math.sqrt(a.d))),
                             'seconds': time.monotonic()-started}
        signal.alarm(0)
        save(doc, f'RS-S004: {mode} X={x} arithmetic full spectrum')
    else:
        a = read(mode, x)
        assert digest(a.path) == row['matrix_sha256']
    for seed in (0, 1):
        if str(seed) in row['controls']:
            continue
        signal.alarm(2700)
        started = time.monotonic()
        certified_control(a, seed)
        structural = audit(a)
        values = svdvals(a.dense(), overwrite_a=True, check_finite=False)
        stats = previous.gap_ratio(values, a.d)
        delta = abs(row['arithmetic']['statistic']['mean_bulk_gap_ratio']-stats['mean_bulk_gap_ratio'])
        excess = row['arithmetic']['sigma1_over_edge']-values[0]/(2*math.sqrt(a.d))
        row['controls'][str(seed)] = {**stamp(), 'seed': seed, 'audit': structural,
             'sha256': digest(a.certified_path), 'singular_values_desc': values.tolist(), 'statistic': stats,
             'sigma1_over_edge': float(values[0]/(2*math.sqrt(a.d))), 'seconds': time.monotonic()-started,
             'outcomes': [outcome(doc, f'RS-S004-L-{mode}-{seed}', delta <= .03, {'absolute_difference': delta}),
                          outcome(doc, f'RS-S004-O-{mode}-{seed}', excess >= .05, {'normalized_excess': float(excess)})]}
        row['complete'] = len(row['controls']) == 2
        signal.alarm(0)
        save(doc, f'RS-S004: {mode} X={x} certified control seed {seed} and outcomes')
        print('local', mode, seed, delta, excess, flush=True)


def sextic(doc):
    x = 320000
    row = doc['sextic_run']
    if row and row.get('complete'):
        return
    if row is None:
        row = {'mode': 'sextic', 'X': x, 'controls': {}}
        doc['sextic_run'] = row
    if 'arithmetic' not in row:
        signal.alarm(2700)
        started = time.monotonic()
        a = build('sextic', x)
        row.update(D=a.d, matrix_sha256=digest(a.path), sign_mask_sha256=digest(a.mask_path))
        structural = audit(a)
        s, _, residuals = a.top(12)
        row['arithmetic'] = {**stamp(), 'audit': structural, 'top12': s.tolist(),
             'gram_relative_residuals': residuals, 'solver_seed': 2,
             'sigma1_over_edge': float(s[0]/(2*math.sqrt(a.d))), 'seconds': time.monotonic()-started}
        signal.alarm(0)
        save(doc, 'RS-S004: sextic X=320000 arithmetic spectrum')
    else:
        a = read('sextic', x)
        assert digest(a.path) == row['matrix_sha256']
    for seed in (0, 1):
        if str(seed) in row['controls']:
            continue
        signal.alarm(2700)
        started = time.monotonic()
        certified_control(a, seed)
        structural = audit(a)
        s, _, residuals = a.top(12)
        excess = row['arithmetic']['sigma1_over_edge']-s[0]/(2*math.sqrt(a.d))
        row['controls'][str(seed)] = {**stamp(), 'audit': structural, 'seed': seed,
             'sha256': digest(a.certified_path), 'top12': s.tolist(), 'gram_relative_residuals': residuals,
             'sigma1_over_edge': float(s[0]/(2*math.sqrt(a.d))), 'seconds': time.monotonic()-started,
             'outcomes': [outcome(doc, f'RS-S004-S-{seed}', excess <= .02, {'normalized_excess': float(excess)})]}
        row['complete'] = len(row['controls']) == 2
        signal.alarm(0)
        save(doc, f'RS-S004: sextic X=320000 certified control seed {seed} and outcome')
        print('sextic', seed, excess, flush=True)


def quadratic(doc):
    x = 80000
    row = doc['quadratic_run']
    if row and row.get('complete'):
        return
    if row is None:
        row = {'mode': 'quad', 'X': x, 'controls': {}}
        doc['quadratic_run'] = row
    if 'arithmetic' not in row:
        signal.alarm(2700)
        started = time.monotonic()
        a = build('quad', x)
        row.update(D=a.d, matrix_sha256=digest(a.path))
        structural = audit(a)
        row['arithmetic'] = {**stamp(), 'audit': structural, 'm4': a.m4(128, 1),
                             'seconds': time.monotonic()-started}
        signal.alarm(0)
        save(doc, 'RS-S004: quadratic X=80000 arithmetic fourth moment')
    else:
        a = read('quad', x)
        assert digest(a.path) == row['matrix_sha256']
    for seed in (0, 1):
        if str(seed) in row['controls']:
            continue
        signal.alarm(2700)
        started = time.monotonic()
        certified_control(a, seed)
        structural = audit(a)
        m = a.m4(128, 3+seed)
        arithmetic = row['arithmetic']['m4']
        delta = m['estimate']-arithmetic['estimate']
        se = math.sqrt(m['standard_error']**2+arithmetic['standard_error']**2)
        threshold = max(.05, 5*se)
        row['controls'][str(seed)] = {**stamp(), 'audit': structural, 'seed': seed,
             'sha256': digest(a.certified_path), 'm4': m, 'seconds': time.monotonic()-started,
             'outcomes': [outcome(doc, f'RS-S004-Q-{seed}', delta >= threshold,
                                  {'m4_difference': delta, 'combined_standard_error': se, 'required_margin': threshold})]}
        row['complete'] = len(row['controls']) == 2
        signal.alarm(0)
        save(doc, f'RS-S004: quadratic X=80000 certified control seed {seed} and retention')
        print('quad', seed, delta, threshold, flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['validate', 'local', 'sextic', 'quad', 'run'])
    args = parser.parse_args()
    legacy.compile_engine()
    doc = json.loads(RESULT.read_text())
    doc['prediction_commit'] = REGISTRATION
    if args.action == 'validate':
        doc['validation'] = validate()
        save(doc, 'RS-S004: certify corrected null controls and numerical overlap before fresh data')
        return
    assert doc['validation']['passed']
    assert doc['validation']['native_source_sha256'] == digest(ROOT/'reciprocity_spectra/native/residue_engine.c')
    assert doc['validation']['null_source_sha256'] == digest(ROOT/'reciprocity_spectra/null_model.py')
    doc['classification'] = 'REGISTERED QUALIFIED-MODEL TEST RESULTS'
    if args.action in ('local', 'run'):
        for mode in ('cubic', 'quartic'):
            local(doc, mode)
    if args.action in ('quad', 'run'):
        quadratic(doc)
    if args.action in ('sextic', 'run'):
        sextic(doc)


if __name__ == '__main__':
    main()
