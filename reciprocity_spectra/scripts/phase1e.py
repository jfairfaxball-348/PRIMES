"""RS-S006: per-twist sextic spike strengths and a twist-count model of the RS-7a cluster.

For w_u = conj(g6~) * (u/pi)_6^{+-1}, normalized, r_u = ||C w_u|| / sqrt(D). In the square spiked
model C = R + theta x w*, ||C w||^2 ~ D + theta^2, so theta_u / sqrt(D) = sqrt(r_u^2 - 1) and a
spike is supercritical (an outlier) iff r_u > sqrt(2). A collective check compresses C onto the
family span W: eigenvalues of W* C* C W / D against the same compression of matched controls.
Use OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4; 2700-second alarm per job.
"""
from __future__ import annotations

import argparse
import json
import math
import signal
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import phase1c  # noqa: E402
import phase1d  # noqa: E402

legacy, ROOT = phase1c.legacy, phase1c.ROOT
RESULT = ROOT / 'reciprocity_spectra/results/phase1e_2026-10-25.json'


def command():
    return 'OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 python ' + ' '.join(sys.argv)


def save(doc, message=None):
    phase1c.phase1b.RESULT, phase1c.phase1b.BRANCH = RESULT, phase1c.BRANCH
    phase1c.phase1b.save(doc, message)


def twists(meta, norm_max):
    """Distinct symbol vectors (u/pi)_6 and their conjugates, with the smallest-norm label."""
    elems = sorted((c * c - c * d + d * d, c, d) for c in range(-25, 26) for d in range(-25, 26)
                    if 0 < c * c - c * d + d * d <= norm_max)
    seen, out = set(), []
    for n, c, d in elems:
        sym = phase1d.sextic_symbol(meta, c, d)
        for sign, v in (('+', sym), ('-', sym.conj())):
            key = tuple(np.round(v[:60], 6))
            if key not in seen:
                seen.add(key)
                out.append({'u': [c, d], 'norm': n, 'sign': sign, 'vector': v})
    return out


def rayleigh(a, w):
    w = w / np.linalg.norm(w)
    return float(np.linalg.norm(a.apply(w)) / math.sqrt(a.d))


def compressed(a, basis):
    """Eigenvalues (descending) of B* B / D with B = C Q, Q an orthonormal basis of the span."""
    b = np.column_stack([a.apply(basis[:, j]) for j in range(basis.shape[1])])
    return np.sort(np.linalg.eigvalsh(b.conj().T @ b / a.d))[::-1]


def run(doc, x, norm_max, k, seeds, label):
    signal.alarm(2700)
    started = time.monotonic()
    row = {'X': x, 'norm_max': norm_max, 'k': k, 'control_seeds': seeds, 'solver_seed': 2,
           'command': command(), 'code_commit': legacy.shell('git', 'rev-parse', 'HEAD'),
           'started_at': datetime.now(UTC).isoformat(), 'classification': label}
    a, g6, _ = phase1d.build(x)
    base = g6.conj()
    family = twists(a.meta, norm_max)
    rows = [{'u': f['u'], 'norm': f['norm'], 'sign': f['sign'],
             'r': rayleigh(a, base * f['vector'])} for f in family]
    for f in rows:
        f['theta_over_sqrtD'] = math.sqrt(max(f['r'] ** 2 - 1, 0.0))
    rng = np.random.default_rng(13)
    rand = [rayleigh(a, np.exp(2j * np.pi * rng.random(a.d))) for _ in range(40)]
    roots = [rayleigh(a, base * np.exp(1j * np.pi / 3 * rng.integers(0, 6, a.d))) for _ in range(40)]
    q, _ = np.linalg.qr(np.column_stack([base * f['vector'] for f in family]))
    gram = np.column_stack([base * f['vector'] for f in family[:200]])
    gram /= np.linalg.norm(gram, axis=0)
    g = abs(gram.conj().T @ gram) - np.eye(gram.shape[1])
    arith_eigs = compressed(a, q)
    s, v, res = a.top(k) if k else (None, None, None)
    row.update(D=a.d, family_size=len(family), twists=rows,
               random_phase_r=rand, conj_g6_random_roots_r=roots,
               gram_first200_max_offdiag=float(g.max()), gram_first200_mean_offdiag=float(g.mean()),
               supercritical_count=int(sum(f['r'] > math.sqrt(2) for f in rows)),
               compressed_top40=arith_eigs[:40].tolist())
    if k:
        coef = q.conj().T @ v
        rq, _ = np.linalg.qr(np.exp(2j * np.pi * rng.random((a.d, q.shape[1]))))
        row.update(top_k=s.tolist(), gram_relative_residuals=res,
                   family_capture_top_k=np.linalg.norm(coef, axis=0).tolist(),
                   random_capture_top_k=np.linalg.norm(rq.conj().T @ v, axis=0).tolist())
    controls = {}
    for seed in seeds:
        a.control(seed)
        ce = compressed(a, q)
        c, _, _ = a.top(2)
        controls[str(seed)] = {'compressed_top40': ce[:40].tolist(), 'top2': c.tolist(),
                               'family_r_max': max(rayleigh(a, base * f['vector']) for f in family[:200])}
        a.path.unlink()
    a.arithmetic()
    cmax = max(c['compressed_top40'][0] for c in controls.values())
    row.update(controls=controls, compressed_count_above_control=int(np.sum(arith_eigs > cmax)),
               total_seconds=time.monotonic() - started)
    if k:
        smax = max(c['top2'][0] for c in controls.values())
        row['cluster_multiplicity'] = int(np.sum(np.array(row['top_k']) > smax))
    signal.alarm(0)
    doc.setdefault('runs', []).append(row)
    save(doc, f'RS-S006: {label} sextic twist strengths X={x}')
    top = sorted(rows, key=lambda f: -f['r'])[:8]
    print(json.dumps({'X': x, 'D': a.d, 'family': len(family), 'supercritical': row['supercritical_count'],
                      'top_r': [(f['u'], f['norm'], f['sign'], round(f['r'], 3)) for f in top],
                      'random_r_max': max(rand), 'roots_r_max': max(roots),
                      'compressed_above_control': row['compressed_count_above_control'],
                      'compressed_top5': [round(t, 3) for t in arith_eigs[:5]],
                      'control_compressed_top1': cmax, 'multiplicity': row.get('cluster_multiplicity'),
                      'gram_max': row['gram_first200_max_offdiag'], 'seconds': row['total_seconds']}),
          flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['explore'])
    parser.add_argument('--x', type=int, required=True)
    parser.add_argument('--norm-max', type=int, default=300)
    parser.add_argument('--k', type=int, default=0)
    parser.add_argument('--seeds', type=int, nargs='+', default=[0, 1, 2])
    args = parser.parse_args()
    legacy.compile_engine()
    doc = json.loads(RESULT.read_text()) if RESULT.exists() else {
        'session': 'RS-S006', 'date': '2026-10-25', 'predictions': [], 'prediction_commit': None,
        'model': __doc__}
    assert args.x <= 160000, 'EXPLORATORY scales only before registration'
    run(doc, args.x, args.norm_max, args.k, args.seeds, 'EXPLORATORY')


if __name__ == '__main__':
    main()
