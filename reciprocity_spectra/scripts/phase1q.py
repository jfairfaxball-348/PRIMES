"""RS-S021: larger-X evidence with the matrix-free engine (native/residue_free.c).

Metadata and Gauss sums come from residue_engine with RS_NO_MATRIX=1 (no D x D matrix); products Y = R W
come from rs_free_apply, which evaluates each symbol by Euler's criterion. Rational normalization, prime
moduli, the RS-S015 singles (pi^k, k = 1..5, 20 smallest primary primes), r = ||R w|| / (||w|| sqrt(D)).

  validate          free engine reproduces stored r values (RS-S016 X = 3.2e5 singles; RS-S015 r_1 at X = 1e6)
  register          H+ and the new-scale holdout at X = 2e6 and 4e6 (commit before data)
  run --x X         one registered scale
  score             verbatim scoring
"""
from __future__ import annotations

import argparse
import ctypes as ct
import json
import math
import os
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import phase1k as k1  # noqa: E402
import phase1l  # noqa: E402

legacy, DATA, ROOT = k1.legacy, k1.DATA, k1.ROOT
RESULT = k1.RESULTS / 'rs_s021_large_x_2026-10-26.json'
THREADS = os.cpu_count() or 4
SEED = 21
SCALES = (2_000_000, 4_000_000)
Z6 = np.exp(1j * np.pi / 3 * np.arange(6))


_COMPILED = []


def compile_free():
    if _COMPILED:  # a loaded DLL cannot be replaced on Windows; build once per process
        return
    _COMPILED.append(True)
    source = ROOT / 'reciprocity_spectra/native/residue_free.c'
    if sys.platform == 'win32':
        build = DATA / 'msvc_build'
        build.mkdir(parents=True, exist_ok=True)
        cl = f'cl /nologo /O2 /openmp:llvm /std:c11 /LD "{source}" /Fe"{build / "libfree.so"}"'
        subprocess.run(f'call "{legacy.VCVARS}" >nul && {cl}', shell=True, cwd=build, check=True,
                       stdout=subprocess.DEVNULL)
        (build / 'libfree.so').replace(DATA / 'libfree.so')
    else:
        legacy.shell('cc', '-O3', '-fopenmp', '-shared', '-fPIC', '-o', str(DATA / 'libfree.so'), str(source), '-lm')


class Free:
    def __init__(self, x):
        if not _COMPILED:
            legacy.compile_engine()
        compile_free()
        self.x = x
        meta_path, g_path = DATA / f'free_meta_{x}.bin', DATA / f'free_gauss_{x}.bin'
        env = dict(os.environ, RS_NO_MATRIX='1', RS_THREADS=str(THREADS))
        started = time.monotonic()
        subprocess.run([str(DATA / 'residue_engine'), 'sextic', str(x), str(meta_path), str(g_path)],
                       check=True, env=env, timeout=4 * 3600)
        self.build_seconds = time.monotonic() - started
        with meta_path.open('rb') as f:
            self.d = int(np.fromfile(f, np.int32, 1)[0])
            self.meta = np.fromfile(f, np.int64, 3 * self.d).reshape(self.d, 3)
        self.g = np.fromfile(g_path, np.complex128)
        meta_path.unlink()
        g_path.unlink()
        self.lib = ct.CDLL(str(DATA / 'libfree.so'))
        self.lib.rs_free_apply.argtypes = [ct.c_int, ct.c_void_p, ct.c_int, ct.c_void_p, ct.c_void_p, ct.c_int]
        self.lib.rs_free_apply.restype = ct.c_int

    def apply(self, w):
        w = np.ascontiguousarray(w, dtype=np.complex128)
        y = np.empty_like(w)
        meta = np.ascontiguousarray(self.meta)
        if self.lib.rs_free_apply(self.d, meta.ctypes.data, w.shape[1], w.ctypes.data, y.ctypes.data, THREADS):
            raise ValueError('prime too large for the free engine')
        return y

    def ratios(self, w):
        y = self.apply(w)
        return np.linalg.norm(y, axis=0) / (np.linalg.norm(w, axis=0) * math.sqrt(self.d))

    def class_vectors(self, kappas):
        base = self.g.conj()
        cols = []
        for kappa in kappas:
            if not kappa:
                cols.append(base)
                continue
            (pi, e), = kappa
            v = k1.exponent_vector(self.meta, pi)
            cols.append(np.where(v < 0, 0, base * Z6[(e * v.astype(np.int64)) % 6]))
        return np.array(cols).T


def save(doc):
    RESULT.write_text(json.dumps(doc, indent=2, allow_nan=False) + '\n')


def load():
    return json.loads(RESULT.read_text()) if RESULT.exists() else {'session': 'RS-S021', 'runs': []}


def validate():
    doc = load()
    out = {'threads': THREADS, 'platform': sys.platform}
    stored = next(r for r in phase1l.load()['runs'] if r['X'] == 320000)
    f = Free(320000)
    kappas = [[]] + [c['kappa'] for c in stored['classes']]
    started = time.monotonic()
    r = f.ratios(f.class_vectors(kappas))
    ref = np.array([stored['r_u1']] + [c['r'] for c in stored['classes']])
    out['X320000'] = {'n': len(ref), 'max_relative_r_difference': float(np.max(np.abs(r - ref) / ref)),
                      'apply_seconds': time.monotonic() - started, 'build_seconds': f.build_seconds}
    f = Free(1_000_000)
    started = time.monotonic()
    r1 = float(f.ratios(f.class_vectors([[]]))[0])
    out['X1000000'] = {'r_u1': r1, 'stored': 1.4342110940043258, 'relative_difference': abs(r1 / 1.4342110940043258 - 1),
                       'apply_seconds_V1': time.monotonic() - started, 'build_seconds': f.build_seconds}
    out['pass'] = out['X320000']['max_relative_r_difference'] < 1e-8 and out['X1000000']['relative_difference'] < 1e-8
    doc['validation'] = out
    save(doc)
    print(json.dumps(out, indent=1))


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('step', choices=['validate', 'register', 'run', 'score'])
    parser.add_argument('--x', type=int)
    args = parser.parse_args()
    if args.step == 'validate':
        validate()
    elif args.step == 'run':
        run(args.x)
    else:
        {'register': register, 'score': score}[args.step]()


def norm(pi):
    return pi[0] ** 2 - pi[0] * pi[1] + pi[1] ** 2


K1_STORED_1E6 = 0.9612  # mean s, k = 1 singles with N <= 43, RS-S015 run at X = 1e6 (phase1l.table)


def register():
    doc = load()
    assert doc['validation']['pass'] and 'predictions' not in doc
    doc.update(
        date='2026-10-26', scales=list(SCALES), control_seed=SEED, threads=THREADS,
        classes='RS-S015 singles (pi^k, k = 1..5, 20 smallest primary primes); rational normalization; prime moduli',
        frozen_F='results/rs_s016_x_dependence_2026-10-26.json analysis.collapse_bins_t_eq_N6_over_X.k234',
        stored_trend_K1={'1.6e5': 0.9319, '3.2e5': 0.9534, '6.4e5': 0.9632, '1e6': 0.9612},
        predictions=[
            {'id': 'RS-S021-H+', 'text': (
                'K1 = mean s over k = 1 singles with N <= 43 (14 classes). Strong form (F(0+) = 1): K1(4e6) > '
                'K1(1e6) + 0.01 = 0.9712 and K1(4e6) > K1(2e6), with K1(4e6) <= 1.05: RISING. Plateau alternative: '
                '|K1(4e6) - 0.9612| <= 0.01: LEVEL. Otherwise UNDECIDED.')},
            {'id': 'RS-S021-A', 'text': (
                'New-scale holdout of the crossover law: for every half-decade bin of log10 t (pooled over both X) '
                'with >= 4 singles having k <= 4 and an F prediction, |mean s - mean F| <= 0.12.')},
            {'id': 'RS-S021-B', 'text': 'At each X, mean s over pi^5 singles with t >= 3 lies in [-1.15, -0.85].'},
        ],
        power_note=('Random-phase sd of r scales as D^(-1/2): about 0.0011 at X = 2e6 and 0.0008 at 4e6, so sigma_eps '
                    'about 0.002 and sigma_s about 0.002-0.003 for k = 1 (SE of K1 about 0.001); pi^5 classes with '
                    't >= 3 have sigma_s about 0.03-0.07 each.'),
        prediction_commit=None)
    save(doc)
    print('registered')


def run(x):
    doc = load()
    assert doc.get('prediction_commit') and x in SCALES
    started = time.monotonic()
    f = Free(x)
    kappas = [[]] + [c['kappa'] for c in k1.classes() if c['part'] == 'singles']
    w = f.class_vectors(kappas)
    rng = np.random.default_rng(SEED)
    controls = np.exp(2j * np.pi * rng.random((f.d, 10)))
    apply_started = time.monotonic()
    r = f.ratios(np.concatenate([w, controls], axis=1))
    r1 = float(r[0])
    cls = []
    for kappa, rk in zip(kappas[1:], r[1:len(kappas)], strict=True):
        (pi, e), = kappa
        n6 = norm(pi) ** e
        eps = (rk ** 2 - 1) / (r1 ** 2 - 1)
        cls.append({'kappa': kappa, 'N': norm(pi), 'k': e, 'r': float(rk), 's': float(eps * n6 ** (1 / 6)),
                    't': n6 / x})
    row = {'X': x, 'D': f.d, 'r_u1': r1, 'classes': cls, 'random_phase_r': r[len(kappas):].tolist(),
           'build_seconds': f.build_seconds, 'apply_seconds': time.monotonic() - apply_started,
           'seconds': time.monotonic() - started, 'threads': THREADS, 'platform': sys.platform,
           'command': 'python ' + ' '.join(sys.argv), 'code_commit': legacy.shell('git', 'rev-parse', 'HEAD'),
           'started_at': datetime.now(UTC).isoformat()}
    doc = load()
    doc['runs'] = sorted([q for q in doc['runs'] if q['X'] != x] + [row], key=lambda q: q['X'])
    save(doc)
    print(json.dumps({k: row[k] for k in ('X', 'D', 'r_u1', 'build_seconds', 'apply_seconds')}))


def score():
    doc = load()
    runs = {q['X']: q for q in doc['runs']}
    out = {}
    k1m = {x: float(np.mean([c['s'] for c in runs[x]['classes'] if c['k'] == 1 and c['N'] <= 43])) for x in SCALES}
    a, b = k1m[SCALES[0]], k1m[SCALES[1]]
    if b > K1_STORED_1E6 + 0.01 and b > a and b <= 1.05:
        h = 'RISING'
    elif abs(b - K1_STORED_1E6) <= 0.01:
        h = 'LEVEL'
    else:
        h = 'UNDECIDED'
    out['H+'] = {'K1': {str(x): v for x, v in k1m.items()}, 'K1_1e6_stored': K1_STORED_1E6, 'outcome': h}
    f = json.loads((k1.RESULTS / 'rs_s016_x_dependence_2026-10-26.json').read_text())
    pts = [(b_['log10_t_lo'] + 0.25, b_['mean_s']) for b_ in f['analysis']['collapse_bins_t_eq_N6_over_X']['k234']]
    xs, ys = zip(*pts, strict=True)
    bins = {}
    for x in SCALES:
        for c in runs[x]['classes']:
            lt = math.log10(c['t'])
            if c['k'] <= 4 and xs[0] <= lt <= xs[-1]:
                bins.setdefault(math.floor(lt * 2) / 2, []).append((c['s'], float(np.interp(lt, xs, ys))))
    rows = []
    for lo, v in sorted(bins.items()):
        if len(v) >= 4:
            ms, mf = float(np.mean([q[0] for q in v])), float(np.mean([q[1] for q in v]))
            rows.append({'log10_t_lo': lo, 'n': len(v), 'mean_s': ms, 'mean_F': mf, 'diff': ms - mf,
                         'ok': abs(ms - mf) <= 0.12})
    out['A'] = {'bins': rows, 'outcome': 'PASS' if rows and all(q['ok'] for q in rows) else 'FAIL'}
    p5 = {str(x): float(np.mean([c['s'] for c in runs[x]['classes'] if c['k'] == 5 and c['t'] >= 3])) for x in SCALES}
    out['B'] = {'mean_s_pi5_t_ge_3': p5, 'outcome': 'PASS' if all(-1.15 <= v <= -0.85 for v in p5.values()) else 'FAIL'}
    out['controls'] = {str(x): {'max': max(runs[x]['random_phase_r']), 'sd': float(np.std(runs[x]['random_phase_r']))}
                       for x in SCALES}
    out['r_u1'] = {str(x): runs[x]['r_u1'] for x in SCALES}
    doc['score'] = out
    save(doc)
    print(json.dumps(out, indent=1))


if __name__ == '__main__':
    main()
