"""RS-S005 / Phase 1d: identify the sextic outlier cluster (RS-7).

Multiplicity above conjugation-matched controls, and projections of Gauss-sum
candidate vectors onto the top singular subspace. Right singular vectors are
the eigenvectors of C*C returned by Engine.top. Candidate w and its conjugation
image conj(w)[c] project equally (C[c,c] = conj C), so images are not listed.
Use OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4; 2700-second alarm per job.
"""
from __future__ import annotations

import argparse
import json
import math
import signal
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import phase1c  # noqa: E402

legacy, DATA, ROOT = phase1c.legacy, phase1c.DATA, phase1c.ROOT
RESULT = ROOT / 'reciprocity_spectra/results/phase1d_2026-10-25.json'
TWISTS = {'1': (1, 0), '-1': (-1, 0), 'w': (0, 1), '1+w': (1, 1), '2': (2, 0), '1-w': (1, -1),
          '3': (3, 0), 'N7': None, 'N7c': None, 'N13': None, 'N13c': None}


def command():
    return 'OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 python ' + ' '.join(sys.argv)


def save(doc, message=None):
    phase1c.phase1b.RESULT, phase1c.phase1b.BRANCH = RESULT, phase1c.BRANCH
    phase1c.phase1b.save(doc, message)


def build(x):
    """Sextic matrix plus normalized sextic and cubic Gauss sums on the same index order."""
    for mode in ('cubic', 'sextic'):
        subprocess.run([str(DATA / 'residue_engine'), mode, str(x), str(DATA / f'{mode}_{x}.bin'),
                        str(DATA / f'{mode}g_{x}.bin')], check=True, timeout=2700)
    meta3 = np.fromfile(DATA / f'cubic_{x}.bin', np.int64, 3 * 10**6, offset=4)
    a = phase1c.ConjEngine('sextic', x)
    assert np.array_equal(meta3[:3 * a.d].reshape(a.d, 3), a.meta)
    (DATA / f'cubic_{x}.bin').unlink()
    g6 = np.fromfile(DATA / f'sexticg_{x}.bin', np.complex128)
    g3 = np.fromfile(DATA / f'cubicg_{x}.bin', np.complex128)
    return a, g6, g3


def sextic_symbol(meta, c, d):
    """((c + d w)/pi)_6 as complex numbers (0 when pi divides it)."""
    z6 = np.exp(1j * np.pi / 3)
    out = np.zeros(len(meta), complex)
    for j, (p, a, b) in enumerate(meta.tolist()):
        r = (-a * pow(b % p, -1, p)) % p
        v = (c + d * r) % p
        if v:
            t, unit, power = pow(v, (p - 1) // 6, p), (1 + r) % p, 1
            for k in range(6):
                if t == power:
                    out[j] = z6 ** k
                    break
                power = power * unit % p
    return out


def candidates(meta, g6, g3):
    twists = dict(TWISTS)
    small = [(p, a, b) for p, a, b in meta.tolist() if p in (7, 13)]
    for (_p, a, b), name in zip(small, ['N7', 'N7c', 'N13', 'N13c'], strict=True):
        twists[name] = (a, b)
    out = {}
    for base, vec in [('g6', g6), ('conj g6', g6.conj()), ('g3', g3), ('conj g3', g3.conj())]:
        for name, (c, d) in twists.items():
            sym = np.ones(len(meta), complex) if name == '1' else sextic_symbol(meta, c, d)
            for sign, tw in (('+', sym), ('-', sym.conj())):
                if name == '1' and sign == '-':
                    continue
                out[f'{base} * ({name}/pi)_6^{sign}1'] = vec * tw
    return out


def projections(v, vectors, m):
    rows = {}
    for name, w in vectors.items():
        w = w / np.linalg.norm(w)
        coef = v.conj().T @ w
        rows[name] = {'proj_top_m': float(np.linalg.norm(coef[:m])),
                      'proj_top_k': float(np.linalg.norm(coef)),
                      'dominant_index': int(np.argmax(abs(coef)))}
    return rows


def explore(doc, x, k, seeds):
    signal.alarm(2700)
    started = time.monotonic()
    row = {'X': x, 'k': k, 'control_seeds': seeds, 'solver_seed': 2, 'command': command(),
           'code_commit': legacy.shell('git', 'rev-parse', 'HEAD'),
           'started_at': datetime.now(UTC).isoformat(),
           'classification': 'EXPLORATORY'}
    a, g6, g3 = build(x)
    edge = 2 * math.sqrt(a.d)
    s, v, res = a.top(k)
    row.update(D=a.d, top_k=s.tolist(), gram_relative_residuals=res,
               matrix_sha256=phase1c.digest(a.path))
    vectors = candidates(a.meta, g6, g3)
    rng = np.random.default_rng(11)
    for i in range(20):
        vectors[f'random phase {i}'] = np.exp(2j * np.pi * rng.random(a.d))
    for i in range(10):
        vectors[f'conj g6 * random sixth roots {i}'] = g6.conj() * np.exp(1j * np.pi / 3 * rng.integers(0, 6, a.d))
    rayleigh = {}
    for name, w in vectors.items():
        if not name.startswith(('random', 'conj g6 * random')):
            w = w / np.linalg.norm(w)
            rayleigh[name] = float(np.linalg.norm(a.apply(w)) / edge)
    controls = {}
    for seed in seeds:
        a.control(seed)
        c, _, cres = a.top(2)
        controls[str(seed)] = {'top2': c.tolist(), 'gram_relative_residuals': cres,
                               'sigma1_over_edge': float(c[0] / edge)}
        a.path.unlink()
    cmax = max(c['top2'][0] for c in controls.values())
    m = int(np.sum(s > cmax))
    row.update(controls=controls, max_control_sigma1=cmax, multiplicity_above_max_control=m,
               top_k_over_edge=(s / edge).tolist(),
               projections=projections(v, vectors, max(m, 1)), rayleigh_over_edge=rayleigh,
               total_seconds=time.monotonic() - started)
    signal.alarm(0)
    doc.setdefault('exploratory', []).append(row)
    save(doc, f'RS-S005: EXPLORATORY sextic cluster X={x}')
    best = sorted(((r['proj_top_k'], n) for n, r in row['projections'].items()), reverse=True)[:8]
    print(json.dumps({'X': x, 'D': a.d, 'multiplicity': m, 'top_over_edge': [round(t, 4) for t in row['top_k_over_edge'][:8]],
                      'control_max_over_edge': cmax / edge, 'best': best,
                      'seconds': row['total_seconds']}), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['explore'])
    parser.add_argument('--x', type=int, required=True)
    parser.add_argument('--k', type=int, default=24)
    parser.add_argument('--seeds', type=int, nargs='+', default=[0, 1, 2])
    args = parser.parse_args()
    legacy.compile_engine()
    doc = json.loads(RESULT.read_text()) if RESULT.exists() else {
        'session': 'RS-S005', 'phase': '1d', 'date': '2026-10-25',
        'control': 'rs_random_conj (RS-S004), seeds as listed', 'predictions': [],
        'prediction_commit': None}
    explore(doc, args.x, args.k, args.seeds)


if __name__ == '__main__':
    main()
