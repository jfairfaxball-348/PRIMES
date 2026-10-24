"""RS-S003 registered sextic spectra and bulk gap-ratio tests.

Use OPENBLAS_NUM_THREADS=2 OMP_NUM_THREADS=4. Each job has a 2700-second
alarm; checkpoints push only this session's results to rs-s003-phase1b.
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

from reciprocity_spectra.arith import residue_matrix, sextic_reciprocity_sign  # noqa: E402

DATA = legacy.DATA
RESULT = ROOT / 'reciprocity_spectra/results/phase1b_2026-10-24.json'
BRANCH = 'rs-s003-phase1b'
PREDICTION_COMMIT = '4ae9c7a'


def digest(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def command():
    return 'OPENBLAS_NUM_THREADS=2 OMP_NUM_THREADS=4 python ' + ' '.join(sys.argv)


def save(doc, message=None):
    temp = RESULT.with_suffix('.tmp')
    temp.write_text(json.dumps(doc, indent=2, allow_nan=False) + '\n')
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


class SexticEngine(legacy.Engine):
    """Inherit the byte-file/Lanczos machinery, with explicit sextic kernels.

    The superclass reads the cubic-format Eisenstein metadata only. The sextic
    phase order and full pairwise sign mask replace its cubic kernel choices.
    """
    def __init__(self, x):
        super().__init__('cubic', x, DATA / f'sextic_{x}.bin')
        self.mode, self.n = 'sextic', 6
        self.lib.rs_pair_signs.argtypes = [ct.c_void_p, ct.c_void_p, ct.c_int, ct.c_int]
        self.lib.rs_pair_signs.restype = ct.c_uint64
        self.lib.rs_apply_signed.argtypes = [ct.c_void_p, ct.c_void_p, ct.c_int, ct.c_int,
                                            ct.c_void_p, ct.c_void_p, ct.c_int]
        self.lib.rs_apply_signed.restype = None
        self.lib.rs_random_signed.argtypes = [ct.c_void_p, ct.c_void_p, ct.c_int, ct.c_int,
                                             ct.c_uint64]
        self.lib.rs_random_signed.restype = None
        self.mask_path = DATA / f'sextic_signs_{x}.bin'
        self.signs = np.memmap(self.mask_path, dtype=np.uint8, mode='w+',
                               shape=(self.d, self.d))
        errors = self.lib.rs_pair_signs(self.e.ctypes.data, self.signs.ctypes.data,
                                        self.d, self.n)
        if errors:
            raise ValueError(f'{errors} invalid sextic reciprocity pairs')
        self.signs.flush()

    def apply(self, x, adjoint=False):
        x = np.ascontiguousarray(x, dtype=np.complex128).reshape(self.d)
        y = np.empty(self.d, dtype=np.complex128)
        self.lib.rs_apply_signed(self.e.ctypes.data, self.signs.ctypes.data, self.d,
                                 self.n, x.ctypes.data, y.ctypes.data, adjoint)
        self.calls += 1
        return y

    def control(self, seed=0):
        self.e = np.memmap(DATA / f'control_sextic_{self.x}.bin', dtype=np.uint8,
                           mode='w+', shape=(self.d, self.d))
        self.lib.rs_random_signed(self.e.ctypes.data, self.signs.ctypes.data,
                                  self.d, self.n, seed)
        self.e.flush()


def build_sextic(x):
    subprocess.run([str(DATA / 'residue_engine'), 'sextic', str(x),
                    str(DATA / f'sextic_{x}.bin')], check=True, timeout=2700)
    return SexticEngine(x)


def gap_ratio(values, d):
    values = np.sort(values)
    remaining = values[values <= 2 * math.sqrt(d)]
    m = len(remaining)
    lo, hi = math.ceil(.2 * m), math.floor(.8 * m)
    gaps = np.diff(remaining[lo:hi])
    if len(gaps) < 2:
        raise ValueError('Registered window contains too few gaps')
    numerator = np.minimum(gaps[:-1], gaps[1:])
    denominator = np.maximum(gaps[:-1], gaps[1:])
    ratios = np.divide(numerator, denominator, out=np.zeros_like(numerator),
                       where=denominator > 0)
    return {'mean_bulk_gap_ratio': float(np.mean(ratios)), 'deflated_count': d - m,
            'remaining_m': m, 'window_lo': lo, 'window_hi_exclusive': hi,
            'ratio_count': len(ratios), 'zero_denominator_count': int(np.sum(denominator == 0))}


def validate():
    # Legacy validate() returns a dictionary; it never writes the RS-S002 JSON.
    out = {'classification': 'VALIDATION; sextic small-scale values are EXPLORATORY, not status drivers',
           'legacy': legacy.validate()}
    a = build_sextic(2000)
    index, pure = residue_matrix(6, 2000)
    lookup = {(p.p, p.a, p.b): i for i, p in enumerate(index)}
    order = [lookup[tuple(row)] for row in a.meta.tolist()]
    expected = np.array([[255 if pure[i][j] is None else pure[i][j] for j in order]
                         for i in order], dtype=np.uint8)
    assert np.array_equal(a.e, expected)
    expected_signs = np.array([[0 if i == j else
                               int(sextic_reciprocity_sign(index[i], index[j]) == -1)
                               for j in order] for i in order], dtype=np.uint8)
    assert np.array_equal(a.signs, expected_signs)
    dense = a.dense()
    s, _, residuals = a.top(8)
    ref = np.sort(svds(dense, k=8, tol=1e-12, return_singular_vectors=False,
                       rng=np.random.default_rng(2)))[::-1]
    error = float(np.max(abs(s/ref - 1)))
    assert error < 1e-8
    z = np.random.default_rng(3).normal(size=a.d) + 1j*np.random.default_rng(4).normal(size=a.d)
    product_errors = [float(np.linalg.norm(a.apply(z)-dense@z)/np.linalg.norm(dense@z)),
                      float(np.linalg.norm(a.apply(z, True)-dense.conj().T@z)
                            / np.linalg.norm(dense.conj().T@z))]
    assert max(product_errors) < 1e-12
    out['sextic_2000'] = {'D': a.d, 'matrix_byte_exact_against_python': True,
                          'full_sign_mask_exact_against_quadratic_symbols': True,
                          'top8': s.tolist(), 'reference_svds_top8': ref.tolist(),
                          'max_relative_error': error, 'gram_relative_residuals': residuals,
                          'complex_matvec_relative_errors': product_errors,
                          'matrix_sha256': digest(a.path), 'mask_sha256': digest(a.mask_path)}
    a.control(0)
    control = a.dense()
    sign = 1 - 2*np.asarray(a.signs, dtype=np.int16)
    assert np.allclose(control.T, sign*control, atol=1e-14)
    for adj, want in [(False, control@z), (True, control.conj().T@z)]:
        assert np.linalg.norm(a.apply(z, adj)-want)/np.linalg.norm(want) < 1e-12
    out['sextic_2000']['control_reciprocity_and_complex_products_checked'] = True
    # Prespecified window, strict deflation and tie conventions on known arrays.
    test = gap_ratio(np.arange(20)*.4, 20)
    assert abs(test['mean_bulk_gap_ratio'] - 1) < 1e-12
    assert (test['window_lo'], test['window_hi_exclusive'], test['ratio_count']) == (4, 16, 10)
    assert gap_ratio(np.zeros(20), 20)['mean_bulk_gap_ratio'] == 0
    assert gap_ratio(np.r_[np.arange(20)*.4, 100.], 21)['deflated_count'] == 1
    out['registered_window_and_tie_semantics_checked'] = True
    out['passed'] = True
    return out


def sextic(doc, x, resume=False):
    signal.alarm(2700)
    started = time.monotonic()
    previous = next((r for r in doc['sextic_runs'] if r['X'] == x), None)
    resumed = bool(resume and previous and 'arithmetic_seconds' in previous)
    if resume and previous and previous.get('complete'):
        signal.alarm(0)
        return
    if resumed:
        row = previous
        a = SexticEngine(x)
        row.update(control_code_commit=legacy.shell('git', 'rev-parse', 'HEAD'),
                   control_command=command(), resumed_control=True)
    else:
        row = {'X': x, 'mode': 'sextic', 'command': command(),
               'code_commit': legacy.shell('git', 'rev-parse', 'HEAD'),
               'seeds': {'control': 0, 'solver': 2}, 'started_at': datetime.now(UTC).isoformat()}
        doc['sextic_runs'].append(row)
        a = build_sextic(x)
        row.update(D=a.d, matrix_sha256=digest(a.path), mask_sha256=digest(a.mask_path),
                   build_seconds=time.monotonic()-started)
        save(doc)
        s, _, residuals = a.top(12)
        row.update(top12=s.tolist(), gram_relative_residuals=residuals,
                   sigma1_over_edge=float(s[0]/(2*math.sqrt(a.d))),
                   arithmetic_seconds=time.monotonic()-started)
        save(doc, f'RS-S003: sextic X={x} arithmetic spectrum')
        print('arithmetic sextic', x, row['sigma1_over_edge'], flush=True)
    a.control(0)
    s, _, residuals = a.top(12)
    excess = row['sigma1_over_edge'] - s[0]/(2*math.sqrt(a.d))
    row.update(control_top12=s.tolist(), control_gram_relative_residuals=residuals,
               control_sigma1_over_edge=float(s[0]/(2*math.sqrt(a.d))),
               normalized_excess=float(excess), control_sha256=digest(DATA/f'control_sextic_{x}.bin'),
               predictions=[{'id': 'RS-S003-P5-E', 'prediction': doc['predictions'][0]['prediction'],
                             'outcome': 'PASS' if row['sigma1_over_edge'] <= 1.02 else 'FAIL'},
                            {'id': 'RS-S003-P5-N', 'prediction': doc['predictions'][1]['prediction'],
                             'outcome': 'PASS' if excess <= .02 else 'FAIL'}],
               total_seconds=time.monotonic()-started + (row['arithmetic_seconds'] if resumed else 0),
               matvec_calls=a.calls, complete=True)
    signal.alarm(0)
    save(doc, f'RS-S003: sextic X={x} matched control and prediction outcomes')
    print('complete sextic', x, row['normalized_excess'], row['total_seconds'], flush=True)


def local(doc, mode, x):
    signal.alarm(2700)
    started = time.monotonic()
    row = {'mode': mode, 'X': x, 'command': command(), 'control_seed': 0,
           'code_commit': legacy.shell('git', 'rev-parse', 'HEAD'),
           'started_at': datetime.now(UTC).isoformat()}
    doc['local_runs'].append(row)
    a = legacy.build(mode, x)
    row.update(D=a.d, matrix_sha256=digest(a.path))
    values = svdvals(a.dense(), overwrite_a=True, check_finite=False)
    row.update(arithmetic=gap_ratio(values, a.d), singular_values_desc=values.tolist(),
               arithmetic_seconds=time.monotonic()-started)
    if x == 40000:
        ref = np.array(doc['validation']['legacy']['spectra_40000'][mode]['top8'])
        error = float(np.max(abs(values[:8]/ref - 1)))
        assert error < 1e-8
        row['full_svd_top8_max_relative_error'] = error
    save(doc, f'RS-S003: {mode} X={x} arithmetic bulk gap ratio')
    print('arithmetic local', mode, x, row['arithmetic'], flush=True)
    a.control(0)
    values = svdvals(a.dense(), overwrite_a=True, check_finite=False)
    row.update(control=gap_ratio(values, a.d), control_singular_values_desc=values.tolist(),
               control_sha256=digest(DATA/f'control_{mode}_{x}.bin'))
    delta = abs(row['arithmetic']['mean_bulk_gap_ratio'] - row['control']['mean_bulk_gap_ratio'])
    row.update(absolute_gap_ratio_difference=delta,
               prediction={'id': 'RS-S003-P6-R', 'prediction': doc['predictions'][2]['prediction'],
                           'outcome': 'PASS' if delta <= .03 else 'FAIL'},
               total_seconds=time.monotonic()-started, complete=True)
    signal.alarm(0)
    save(doc, f'RS-S003: {mode} X={x} matched bulk gap ratio and outcome')
    print('complete local', mode, x, delta, row['total_seconds'], flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['validate', 'sextic', 'local'])
    parser.add_argument('--resume', action='store_true')
    parser.add_argument('--x', type=int, nargs='+')
    parser.add_argument('--mode', choices=['cubic', 'quartic'], nargs='+', default=['cubic', 'quartic'])
    args = parser.parse_args()
    legacy.compile_engine()
    doc = json.loads(RESULT.read_text())
    doc['prediction_commit'] = PREDICTION_COMMIT
    if args.action == 'validate':
        doc['validation'] = validate()
        doc['validation'].update(code_commit=legacy.shell('git', 'rev-parse', 'HEAD'), command=command())
        save(doc, 'RS-S003: validate sextic extension and legacy overlap before stress tests')
    else:
        assert doc['validation']['passed'], 'Validation is required before stress tests'
        if args.action == 'sextic':
            for x in args.x or [40000, 160000]:
                assert x in [40000, 160000], 'Only registered scales in this unit'
                sextic(doc, x, args.resume)
        else:
            for mode in args.mode:
                for x in args.x or [20000, 40000]:
                    assert x in [20000, 40000], 'Only registered scales in this unit'
                    local(doc, mode, x)


if __name__ == '__main__':
    main()
