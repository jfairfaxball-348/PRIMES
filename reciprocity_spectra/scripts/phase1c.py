"""RS-S004 / Phase 1c: conjugation-matched null controls and fresh-scale tests.

The control keeps the exact reciprocity mask and also the conjugation identity
E[c(i)][c(j)] = -E[i][j]; the conjugate-pair entries (i, c(i)) are copied (see
native rs_random_conj and arith.conjugate_pair_exponents). Use
OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4. Each job has a 2700-second alarm;
checkpoints push only this session's results to the session branch.
"""
from __future__ import annotations

import argparse
import ctypes as ct
import json
import math
import signal
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
import phase1b  # noqa: E402

DATA = legacy.DATA
RESULT = ROOT / 'reciprocity_spectra/results/phase1c_2026-10-25.json'
BRANCH = 'ccr-c363c6bb-0zejeu'
ORDER = {'cubic': 3, 'quartic': 4, 'sextic': 6}
gap_ratio, digest = phase1b.gap_ratio, phase1b.digest


def command():
    return 'OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 python ' + ' '.join(sys.argv)


def save(doc, message=None):
    phase1b.RESULT, phase1b.BRANCH = RESULT, BRANCH
    phase1b.save(doc, message)


class ConjEngine(legacy.Engine):
    """Arithmetic matrix with full sign mask, conjugate index and orbit control."""

    def __init__(self, mode, x):
        super().__init__('cubic' if mode == 'sextic' else mode, x, DATA / f'{mode}_{x}.bin')
        self.mode, self.n = mode, ORDER[mode]
        lib = self.lib
        lib.rs_pair_signs.argtypes = [ct.c_void_p, ct.c_void_p, ct.c_int, ct.c_int]
        lib.rs_pair_signs.restype = ct.c_uint64
        lib.rs_apply_signed.argtypes = [ct.c_void_p, ct.c_void_p, ct.c_int, ct.c_int,
                                        ct.c_void_p, ct.c_void_p, ct.c_int]
        lib.rs_apply_signed.restype = None
        lib.rs_random_conj.argtypes = [ct.c_void_p, ct.c_void_p, ct.c_void_p, ct.c_void_p,
                                       ct.c_int, ct.c_int, ct.c_uint64]
        lib.rs_random_conj.restype = ct.c_uint64
        self.mask_path = DATA / f'{mode}_signs_{x}.bin'
        self.signs = np.memmap(self.mask_path, dtype=np.uint8, mode='w+', shape=(self.d, self.d))
        if lib.rs_pair_signs(self.e.ctypes.data, self.signs.ctypes.data, self.d, self.n):
            raise ValueError('invalid reciprocity pairs')
        key = {tuple(r): i for i, r in enumerate(self.meta.tolist())}
        self.conj = np.array([key[(p, a - b, -b) if self.n != 4 else (p, a, -b)]
                              for p, a, b in self.meta.tolist()], dtype=np.int32)
        self.forced = np.ascontiguousarray(self.e[np.arange(self.d), self.conj])
        self.arith_path = self.path

    def apply(self, x, adjoint=False):
        x = np.ascontiguousarray(x, dtype=np.complex128).reshape(self.d)
        y = np.empty(self.d, dtype=np.complex128)
        self.lib.rs_apply_signed(self.e.ctypes.data, self.signs.ctypes.data, self.d,
                                 self.n, x.ctypes.data, y.ctypes.data, adjoint)
        self.calls += 1
        return y

    def control(self, seed=0):
        self.path = DATA / f'conjcontrol_{self.mode}_{self.x}_{seed}.bin'
        self.e = np.memmap(self.path, dtype=np.uint8, mode='w+', shape=(self.d, self.d))
        if self.lib.rs_random_conj(self.e.ctypes.data, self.signs.ctypes.data,
                                   self.conj.ctypes.data, self.forced.ctypes.data,
                                   self.d, self.n, seed):
            raise ValueError('reciprocity mask is not conjugation-invariant')
        self.e.flush()

    def arithmetic(self):
        self.path = self.arith_path
        self.e = np.memmap(self.path, dtype=np.uint8, mode='r', offset=4 + 24 * self.d,
                           shape=(self.d, self.d))

    def identity_errors(self):
        """Exact exponent-level violations of reciprocity and conjugation (off-diagonal)."""
        e = np.asarray(self.e, dtype=np.int16)
        s = np.asarray(self.signs, dtype=np.int16)
        off = ~np.eye(self.d, dtype=bool)
        recip = (e.T - e - s * (self.n // 2)) % self.n
        conj = (e[np.ix_(self.conj, self.conj)] + e) % self.n
        return {'reciprocity': int(np.count_nonzero(recip[off])),
                'conjugation': int(np.count_nonzero(conj[off])),
                'diagonal_not_255': int(np.count_nonzero(np.diag(e) != 255))}


def build(mode, x):
    legacy.subprocess.run([str(DATA / 'residue_engine'), mode, str(x),
                           str(DATA / f'{mode}_{x}.bin')], check=True, timeout=2700)
    return ConjEngine(mode, x)


def validate():
    out = {'classification': 'VALIDATION of the conjugation-matched control and engine path'}
    old = json.loads((ROOT / 'reciprocity_spectra/results/phase1_2026-10-24.json').read_text())
    for mode in ORDER:
        a = build(mode, 20000)
        row = {'D': a.d, 'matrix_sha256': digest(a.path),
               'arithmetic_identity_errors': a.identity_errors()}
        if mode != 'sextic':
            row['matrix_sha256_matches_RS-S002'] = \
                row['matrix_sha256'] == old['validation']['matrix_20000'][mode]['sha256']
            assert row['matrix_sha256_matches_RS-S002']
        assert not any(row['arithmetic_identity_errors'].values())
        dense = a.dense()
        s, _, residuals = a.top(8)
        ref = np.sort(svds(dense, k=8, tol=1e-12, return_singular_vectors=False,
                           rng=np.random.default_rng(2)))[::-1]
        row.update(top8=s.tolist(), reference_svds_top8=ref.tolist(),
                   max_relative_error=float(np.max(abs(s / ref - 1))))
        assert row['max_relative_error'] < 1e-8
        a.control(0)
        row['control_identity_errors'] = a.identity_errors()
        assert not any(row['control_identity_errors'].values())
        assert np.array_equal(a.e[np.arange(a.d), a.conj], a.forced)
        ctrl = a.dense()
        rng = np.random.default_rng(3)
        z = rng.standard_normal(a.d) + 1j * rng.standard_normal(a.d)
        errors = [float(np.linalg.norm(a.apply(z) - ctrl @ z) / np.linalg.norm(ctrl @ z)),
                  float(np.linalg.norm(a.apply(z, True) - ctrl.conj().T @ z)
                        / np.linalg.norm(ctrl.conj().T @ z))]
        assert max(errors) < 1e-12
        s, _, _ = a.top(8)
        ref = np.sort(svds(ctrl, k=8, tol=1e-12, return_singular_vectors=False,
                           rng=np.random.default_rng(2)))[::-1]
        row.update(control_top8=s.tolist(), control_reference_svds_top8=ref.tolist(),
                   control_max_relative_error=float(np.max(abs(s / ref - 1))),
                   control_complex_matvec_relative_errors=errors,
                   control_sha256=digest(a.path))
        assert row['control_max_relative_error'] < 1e-8
        upper = ctrl[np.triu_indices(a.d, 1)]
        exps = np.rint(np.angle(upper) / (2 * np.pi / a.n)).astype(int) % a.n
        row['control_upper_exponent_counts'] = np.bincount(exps, minlength=a.n).tolist()
        if mode == 'cubic':
            h = ctrl[:, a.conj]
            row['control_times_conjugation_hermitian_max_error'] = float(np.max(abs(h - h.conj().T)))
            assert row['control_times_conjugation_hermitian_max_error'] < 1e-12
        out[mode] = row
        print('validated', mode, row['max_relative_error'], row['control_max_relative_error'], flush=True)
    out['passed'] = True
    return out


def spectrum_row(a, seeds, full):
    """Full SVD gap ratios (dense) or top-12 Lanczos values for arithmetic and controls."""
    edge = 2 * math.sqrt(a.d)
    a.arithmetic()
    t = time.monotonic()
    if full:
        v = svdvals(a.dense(), overwrite_a=True, check_finite=False)
        row = {'arithmetic': gap_ratio(v, a.d), 'singular_values_desc': v.tolist()}
    else:
        v, _, res = a.top(12)
        row = {'top12': v.tolist(), 'gram_relative_residuals': res}
    row.update(sigma1_over_edge=float(v[0] / edge), arithmetic_seconds=time.monotonic() - t,
               matrix_sha256=digest(a.path), controls={})
    for seed in seeds:
        t = time.monotonic()
        a.control(seed)
        if full:
            c = svdvals(a.dense(), overwrite_a=True, check_finite=False)
            ctl = {'gap': gap_ratio(c, a.d), 'singular_values_desc': c.tolist()}
        else:
            c, _, res = a.top(12)
            ctl = {'top12': c.tolist(), 'gram_relative_residuals': res}
        ctl.update(sigma1_over_edge=float(c[0] / edge), sha256=digest(a.path),
                   seconds=time.monotonic() - t)
        row['controls'][str(seed)] = ctl
        a.path.unlink()
    return row


def run(doc, section, mode, x, seeds, full, message):
    signal.alarm(2700)
    started = time.monotonic()
    row = {'mode': mode, 'X': x, 'command': command(), 'control_seeds': seeds,
           'solver_seed': None if full else 2,
           'code_commit': legacy.shell('git', 'rev-parse', 'HEAD'),
           'started_at': datetime.now(UTC).isoformat()}
    a = build(mode, x)
    row.update(D=a.d, mask_sha256=digest(a.mask_path), **spectrum_row(a, seeds, full))
    row['total_seconds'] = time.monotonic() - started
    signal.alarm(0)
    doc.setdefault(section, []).append(row)
    if section == 'registered':
        score(doc, row)
    save(doc, message)
    summary = {k: row[k] for k in ('mode', 'X', 'D', 'sigma1_over_edge', 'total_seconds')}
    summary['controls'] = {s: c['sigma1_over_edge'] for s, c in row['controls'].items()}
    if full:
        summary['gap'] = row['arithmetic']['mean_bulk_gap_ratio']
        summary['control_gap'] = {s: c['gap']['mean_bulk_gap_ratio'] for s, c in row['controls'].items()}
    print(json.dumps(summary), flush=True)
    return row


def score(doc, row):
    """Apply the committed RS-S004 predictions verbatim (see doc['predictions'])."""
    ctrl = row['controls']['0']
    outcomes = []
    for p in doc['predictions']:
        if p['mode'] != row['mode'] or p['X'] != row['X']:
            continue
        if p['statistic'] == 'abs_gap_ratio_difference':
            value = abs(row['arithmetic']['mean_bulk_gap_ratio'] - ctrl['gap']['mean_bulk_gap_ratio'])
        else:  # 'sigma1_over_edge_excess'
            value = row['sigma1_over_edge'] - ctrl['sigma1_over_edge']
        ok = (p.get('min') is None or value >= p['min']) and (p.get('max') is None or value <= p['max'])
        outcomes.append({'id': p['id'], 'value': value, 'outcome': 'PASS' if ok else 'FAIL'})
    row['prediction_outcomes'] = outcomes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['validate', 'explore', 'registered'])
    parser.add_argument('--mode', choices=sorted(ORDER), required=False)
    parser.add_argument('--x', type=int)
    parser.add_argument('--seeds', type=int, nargs='+', default=[0])
    parser.add_argument('--full', action='store_true', help='dense full SVD (gap ratios)')
    args = parser.parse_args()
    legacy.compile_engine()
    doc = json.loads(RESULT.read_text())
    if args.action == 'validate':
        doc['validation'] = validate()
        doc['validation'].update(code_commit=legacy.shell('git', 'rev-parse', 'HEAD'),
                                 command=command())
        save(doc, 'RS-S004: validate conjugation-matched control and engine path')
        return
    assert doc['validation']['passed'], 'Validation is required first'
    if args.action == 'explore':
        run(doc, 'exploratory', args.mode, args.x, args.seeds, args.full,
            f'RS-S004: EXPLORATORY {args.mode} X={args.x} against conjugation-matched controls')
    else:
        assert doc.get('prediction_commit'), 'Predictions must be committed and pushed first'
        reg = [p for p in doc['predictions'] if p['mode'] == args.mode and p['X'] == args.x]
        assert reg, 'Only registered mode/scale pairs'
        assert args.seeds == [0] and args.full == (reg[0]['statistic'] == 'abs_gap_ratio_difference')
        run(doc, 'registered', args.mode, args.x, [0], args.full,
            f'RS-S004: registered {args.mode} X={args.x} outcome')


if __name__ == '__main__':
    main()
