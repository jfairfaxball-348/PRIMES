"""Reproducible byte-engine validation and Phase-1 runs (four OpenMP threads).

Run from the repository root with OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=4.
The native control uses SplitMix64 pair counters, rather than numpy's PCG64;
its law and reciprocity signs match spectra.structured_random.
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
from scipy.sparse.linalg import LinearOperator, eigsh, svds

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'reciprocity_spectra' / 'scripts'))
from spectra import ORDER, bbp_strength  # noqa: E402

DATA = ROOT / 'reciprocity_spectra/data'
RESULT = ROOT / 'reciprocity_spectra/results/phase1_2026-10-24.json'


def shell(*args):
    return subprocess.check_output(args, cwd=ROOT, text=True).strip()


VCVARS = Path('C:/Program Files (x86)/Microsoft Visual Studio/2022/BuildTools/VC/Auxiliary/Build/vcvars64.bat')


def compile_engine_msvc(source):
    """Windows-local build (RS-S015): MSVC with OpenMP; validated against stored Linux digests."""
    build = DATA / 'msvc_build'
    build.mkdir(exist_ok=True)
    for flags, output in [([], 'residue_engine.exe'), (['/LD'], 'libresidue.so')]:
        cl = ' '.join(['cl', '/nologo', '/O2', '/openmp:llvm', '/std:c11', *flags, f'"{source}"',
                       f'/Fe"{build / output}"'])
        subprocess.run(f'call "{VCVARS}" >nul && {cl}', shell=True, cwd=build, check=True,
                       stdout=subprocess.DEVNULL)
        (build / output).replace(DATA / output)


def compile_engine():
    DATA.mkdir(exist_ok=True)
    source = ROOT / 'reciprocity_spectra/native/residue_engine.c'
    if sys.platform == 'win32':
        compile_engine_msvc(source)
        return
    for flags, output in [([], 'residue_engine'), (['-shared', '-fPIC'], 'libresidue.so')]:
        temp = DATA / (output + '.tmp')
        shell('cc', '-O3', '-fopenmp', *flags, '-o', str(temp), str(source), '-lm')
        temp.replace(DATA / output)
    shell('cc', '-O2', '-o', str(DATA / 'residue_matrix'),
          str(ROOT / 'reciprocity_spectra/native/residue_matrix.c'), '-lm')


class Engine:
    def __init__(self, mode, x, path=None):
        self.mode, self.x, self.n = mode, x, ORDER[mode]
        self.path = path or DATA / f'{mode}_{x}.bin'
        with self.path.open('rb') as f:
            self.d = int(np.fromfile(f, np.int32, 1)[0])
            self.meta = np.fromfile(f, np.int64, 3 * self.d).reshape(self.d, 3)
        self.e = np.memmap(self.path, dtype=np.uint8, mode='r',
                           offset=4 + 24 * self.d, shape=(self.d, self.d))
        self.lib = ct.CDLL(str(DATA / 'libresidue.so'))
        self.lib.rs_apply.argtypes = [ct.c_void_p, ct.c_int, ct.c_int,
                                     ct.c_void_p, ct.c_void_p, ct.c_int]
        self.lib.rs_apply.restype = None
        self.lib.rs_random.argtypes = [ct.c_void_p, ct.c_int, ct.c_int,
                                      ct.c_void_p, ct.c_uint64]
        self.lib.rs_random.restype = None
        self.lib.rs_apply_sym.argtypes = [ct.c_void_p, ct.c_int, ct.c_int, ct.c_void_p,
                                         ct.c_void_p, ct.c_void_p, ct.c_int]
        self.lib.rs_apply_sym.restype = None
        p = self.meta[:, 0]
        self.odd = np.ascontiguousarray(p % 4 == 3 if mode == 'quad' else
                                       p % 8 == 5 if mode == 'quartic' else
                                       np.zeros(self.d, bool), dtype=np.uint8)
        self.calls = 0

    def apply(self, x, adjoint=False):
        x = np.ascontiguousarray(x, dtype=np.complex128).reshape(self.d)
        y = np.empty(self.d, dtype=np.complex128)
        self.lib.rs_apply_sym(self.e.ctypes.data, self.d, self.n, self.odd.ctypes.data,
                              x.ctypes.data, y.ctypes.data, adjoint)
        self.calls += 1
        return y

    def operator(self):
        return LinearOperator((self.d, self.d), matvec=self.apply,
                              rmatvec=lambda x: self.apply(x, True), dtype=np.complex128)

    def control(self, seed=0):
        # A separate disk-backed byte array; no floating-point matrix.
        self.e = np.memmap(DATA / f'control_{self.mode}_{self.x}.bin', dtype=np.uint8,
                           mode='w+', shape=(self.d, self.d))
        primes = np.ascontiguousarray(self.meta[:, 0])
        self.lib.rs_random(self.e.ctypes.data, self.d, self.n, primes.ctypes.data, seed)
        self.e.flush()

    def dense(self):
        roots = np.zeros(256, complex)
        roots[:self.n] = np.exp(2j * np.pi * np.arange(self.n) / self.n)
        return roots[self.e]

    def top(self, k):
        op = self.operator()
        gram = LinearOperator(op.shape, matvec=lambda v: op.rmatvec(op.matvec(v)),
                              dtype=np.complex128)
        rng = np.random.default_rng(2)
        w, v = eigsh(gram, k=k, which='LA', tol=1e-11, ncv=max(64, 4 * k + 1),
                     v0=rng.standard_normal(self.d) + 1j * rng.standard_normal(self.d))
        order = np.argsort(-w)
        s, v = np.sqrt(w[order]), v[:, order]
        residual = [float(np.linalg.norm(gram @ v[:, j] - s[j]**2 * v[:, j]) / s[j]**2)
                    for j in range(k)]
        return s, v, residual

    def m4(self, probes=128, seed=1):
        rng = np.random.default_rng(seed)
        values = []
        for _ in range(probes):
            z = 2 * rng.integers(0, 2, self.d) - 1
            gz = self.apply(self.apply(z), True)
            values.append(float(np.vdot(gz, gz).real / self.d**3))
        return {'method': 'Hutchinson real Rademacher on (C*C)^2', 'probes': probes,
                'seed': seed, 'estimate': float(np.mean(values)),
                'standard_error': float(np.std(values, ddof=1) / math.sqrt(probes)),
                'probe_values': values}


def build(mode, x, reference=False, gauss=False):
    name = 'residue_matrix' if reference else 'residue_engine'
    path = DATA / f'{"reference_" if reference else ""}{mode}_{x}.bin'
    args = [str(DATA / name), mode, str(x), str(path)]
    if gauss:
        args.append(str(DATA / f'{mode}g_{x}.bin'))
    subprocess.run(args, check=True, timeout=2700)
    return Engine(mode, x, path)


def save(doc, message=None):
    temp = RESULT.with_suffix('.tmp')
    temp.write_text(json.dumps(doc, indent=2, allow_nan=False) + '\n')
    temp.replace(RESULT)
    if message:
        shell('git', 'add', str(RESULT))
        shell('git', 'commit', '-m', message)
        print(shell('git', 'push', '-u', 'origin', 'rs-s002-phase1a'), flush=True)


def validate():
    out = {'matrix_20000': {}, 'spectra_40000': {}}
    for mode in ORDER:
        a = build(mode, 20000)
        b = build(mode, 20000, reference=True)
        identical = a.path.read_bytes() == b.path.read_bytes()
        assert identical
        out['matrix_20000'][mode] = {'byte_identical': identical, 'D': a.d,
                                    'sha256': hashlib.sha256(a.path.read_bytes()).hexdigest()}
        a = build(mode, 40000, gauss=(mode == 'cubic'))
        mat = a.dense()
        s, _, residual = a.top(8)
        ref = np.sort(svds(mat, k=8, tol=1e-12, return_singular_vectors=False,
                           rng=np.random.default_rng(2)))[::-1]
        err = float(np.max(np.abs(s / ref - 1)))
        assert err < 1e-8
        # Complex adjoint and reciprocity signs are checked independently.
        rng = np.random.default_rng(3)
        z = rng.standard_normal(a.d) + 1j * rng.standard_normal(a.d)
        errors = [float(np.linalg.norm(a.apply(z) - mat @ z) / np.linalg.norm(mat @ z)),
                  float(np.linalg.norm(a.apply(z, True) - mat.conj().T @ z)
                        / np.linalg.norm(mat.conj().T @ z))]
        assert max(errors) < 1e-12
        out['spectra_40000'][mode] = {'D': a.d, 'top8': s.tolist(),
                                    'reference_svds_top8': ref.tolist(),
                                    'max_relative_error': err, 'gram_residuals': residual,
                                    'complex_matvec_relative_errors': errors}
        if mode == 'quad':
            m = a.m4()
            gram = mat.conj().T @ mat
            exact_dense = float(np.vdot(gram, gram).real / a.d**3)
            m['dense_value'] = exact_dense
            m['within_2_standard_errors'] = abs(m['estimate'] - exact_dense) <= 2 * m['standard_error']
            assert m['within_2_standard_errors']
            out['m4_40000'] = m
        if mode == 'cubic':
            # Compare parallel sums with the previous serial builder at the byte-test scale.
            refpath = DATA / 'reference_gauss.bin'
            subprocess.run([str(DATA / 'residue_matrix'), mode, '20000',
                            str(DATA / 'reference_cubic_20000.bin'), str(refpath)], check=True)
            build(mode, 20000, gauss=True)
            out['gauss_20000_byte_identical'] = refpath.read_bytes() == (DATA / 'cubicg_20000.bin').read_bytes()
            assert out['gauss_20000_byte_identical']
        a.control()
        ctrl = a.dense()
        p = a.meta[:, 0]
        odd = p % 4 == 3 if mode == 'quad' else p % 8 == 5 if mode == 'quartic' else np.zeros(a.d, bool)
        signs = np.where(np.outer(odd, odd), -1, 1)
        assert np.allclose(ctrl.T, signs * ctrl, atol=1e-14)
        out['spectra_40000'][mode]['control_reciprocity_checked'] = True
        print('validated', mode, err, flush=True)
    out['passed'] = True
    return out


def run(doc, mode, x, resume=False):
    signal.alarm(2700)
    t = time.monotonic()
    previous = next((r for r in doc['runs'] if r['mode'] == mode and r['X'] == x), None)
    if resume and previous and previous.get('complete'):
        signal.alarm(0)
        return
    if resume and previous and 'arithmetic_seconds' in previous:
        row = previous
        a = Engine(mode, x)
        row['control_code_commit'] = shell('git', 'rev-parse', 'HEAD')
        row['control_command'] = 'OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=4 python ' + ' '.join(sys.argv)
    else:
        row = {'mode': mode, 'X': x, 'code_commit': shell('git', 'rev-parse', 'HEAD'),
               'command': ' '.join(sys.argv), 'seeds': {'control': 0, 'probes': 1, 'solver': 2}}
        doc['runs'].append(row)
        save(doc)
        a = build(mode, x, gauss=(mode == 'cubic'))
        row.update(D=a.d, build_seconds=time.monotonic() - t)
        save(doc)
        print('built', mode, x, a.d, row['build_seconds'], flush=True)
        s, v, residual = a.top(12)
        theta = bbp_strength(float(s[0]), a.d)
        row.update(top12=s.tolist(), gram_relative_residuals=residual,
                   theta=theta if math.isfinite(theta) else None,
                   sigma1_over_edge=float(s[0] / (2 * math.sqrt(a.d))))
        if mode == 'cubic':
            g = np.fromfile(DATA / f'cubicg_{x}.bin', np.complex128)
            row.update(kappa3=theta * math.log(x) / x**(2/3),
                       overlap_conj_gauss=float(abs(np.vdot(g.conj(), v[:, 0])) / np.linalg.norm(g)),
                       bbp_predicted_overlap=math.sqrt(1 - a.d / theta**2))
            row['predictions'] = [
                {'prediction': 'kappa3 in [1.38, 1.47]', 'outcome': 'PASS' if 1.38 <= row['kappa3'] <= 1.47 else 'FAIL'},
                {'prediction': 'cubic top-singular-vector overlap with conj(g~) within 0.03 of sqrt(1 - D/theta^2)',
                 'outcome': 'PASS' if abs(row['overlap_conj_gauss'] - row['bbp_predicted_overlap']) <= .03 else 'FAIL'}]
        elif mode == 'quartic':
            row['theta_normalized'] = theta / math.sqrt(a.d)
            row['predicted_theta_normalized'] = .166 * math.log(x) - .18
            row['predictions'] = [{'prediction': 'quartic theta_n = 0.166*ln X - 0.18 +- 0.05',
                                   'outcome': 'PASS' if abs(row['theta_normalized'] - row['predicted_theta_normalized']) <= .05 else 'FAIL'}]
        else:
            row['m4'] = a.m4()
            row['quadratic_correction'] = (2 - row['m4']['estimate']) * math.log(a.d)
            row['quadratic_correction_standard_error'] = row['m4']['standard_error'] * math.log(a.d)
            row['predictions'] = [{'prediction': 'quadratic (2 - m4)*ln D in [1.0, 1.4]',
                                   'outcome': 'PASS' if 1 <= row['quadratic_correction'] <= 1.4 else 'FAIL'}]
        row['arithmetic_seconds'] = time.monotonic() - t
        save(doc, f'RS-S002: checkpoint {mode} X={x} arithmetic results')
        print('arithmetic', mode, row, flush=True)
    a.control(seed=0)
    s, _, residual = a.top(12)
    row.update(control_top12=s.tolist(), control_gram_relative_residuals=residual,
               control_rng='SplitMix64 rejection-sampled upper-pair counters; seed 0',
               total_seconds=time.monotonic() - t + (row['arithmetic_seconds'] if resume and previous else 0),
               control_seconds=time.monotonic() - t if resume and previous else time.monotonic() - t - row['arithmetic_seconds'],
               matvec_calls=a.calls, complete=True)
    signal.alarm(0)
    save(doc, f'RS-S002: checkpoint {mode} X={x} matched control')
    print('complete', mode, x, row['total_seconds'], flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['validate', 'run', 'control-m4'])
    parser.add_argument('--resume', action='store_true', help='Keep completed rows and resume saved arithmetic at its control')
    parser.add_argument('--x', type=int, default=320000)
    parser.add_argument('--mode', choices=list(ORDER), nargs='+', default=['cubic', 'quartic', 'quad'])
    args = parser.parse_args()
    compile_engine()
    doc = json.loads(RESULT.read_text()) if RESULT.exists() else {
        'session': 'RS-S002', 'date': datetime.now(UTC).isoformat(),
        'base_commit': shell('git', 'rev-parse', 'HEAD'), 'prediction_commit': '0b77769',
        'threads': 4, 'command': ' '.join(sys.argv), 'runs': []}
    if args.action == 'validate':
        if 'validation' in doc:
            doc.setdefault('validation_history', []).append(doc['validation'])
        doc['validation'] = validate()
        doc['validation']['code_commit'] = shell('git', 'rev-parse', 'HEAD')
        doc['validation']['command'] = 'OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=4 python ' + ' '.join(sys.argv)
        save(doc, 'RS-S002: validate byte engine before scaling')
    elif args.action == 'control-m4':
        assert doc.get('validation', {}).get('passed')
        assert args.mode == ['quad'], 'control-m4 requires --mode quad'
        row = next(r for r in doc['runs'] if r['mode'] == 'quad' and r['X'] == args.x)
        assert row.get('complete'), 'Finish arithmetic and control spectra first'
        signal.alarm(2700)
        started = time.monotonic()
        a = Engine('quad', args.x)
        a.e = np.memmap(DATA / f'control_quad_{args.x}.bin', dtype=np.uint8,
                        mode='r', shape=(a.d, a.d))
        row['control_m4'] = a.m4()
        row['control_m4'].update(code_commit=shell('git', 'rev-parse', 'HEAD'),
                                 command='OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=4 python ' + ' '.join(sys.argv),
                                 elapsed_seconds=time.monotonic() - started,
                                 role='Matched null diagnostic; not a separate conjecture prediction')
        signal.alarm(0)
        save(doc, f'RS-S002: checkpoint quadratic X={args.x} matched-control fourth moment')
    else:
        assert doc.get('validation', {}).get('passed'), 'Validation must pass before scaling'
        for mode in args.mode:
            run(doc, mode, args.x, args.resume)


if __name__ == '__main__':
    main()
