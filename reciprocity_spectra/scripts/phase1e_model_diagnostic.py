"""RS-S006 EXPLORATORY: collective subcritical-spike model and left-image alignment at X=40000.

Synthetic model: seed-0 conjugation-matched control plus sum_u theta_u y_u w_u*, with w_u the
orthonormalized twists (r_u > cut, strongest first), theta_u = sqrt(r_u^2 - 1) sqrt(D) and
random orthonormal left directions y_u (seeds 100+s, 200+s). Counts singular values above the
control sigma1. Also: |corr| of left images C w_u for the 60 strongest twists, arithmetic vs control.
Needs data/sextic_40000.bin and sexticg_40000.bin from phase1e explore --x 40000.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import phase1c  # noqa: E402
import phase1e  # noqa: E402


def main():
    x = 40000
    doc = json.loads(phase1e.RESULT.read_text())
    run = [t for t in doc['runs'] if t['X'] == x][-1]
    a = phase1c.ConjEngine('sextic', x)
    d = a.d
    g6 = np.fromfile(phase1c.DATA / f'sexticg_{x}.bin', np.complex128)
    fam = phase1e.twists(a.meta, run['norm_max'])
    r = np.array([t['r'] for t in run['twists']])
    c = a.dense()
    a.control(0)
    c0 = a.dense()
    a.path.unlink()
    s0 = np.linalg.svd(c0, compute_uv=False)
    out = {'X': x, 'D': d, 'command': 'python ' + ' '.join(sys.argv),
           'code_commit': phase1c.legacy.shell('git', 'rev-parse', 'HEAD'),
           'arithmetic_multiplicity_vs_max_of_3_controls': run['cluster_multiplicity'],
           'arithmetic_sigma1_over_edge': run['top_k'][0] / (2 * math.sqrt(d)), 'model': []}
    for cut in (1.024, 1.05, 1.1):
        idx = [i for i in np.argsort(-r) if r[i] > cut]
        w, _ = np.linalg.qr(np.column_stack([g6.conj() * fam[i]['vector'] for i in idx]))
        theta = np.sqrt(r[idx] ** 2 - 1) * math.sqrt(d)
        for ys in range(3):
            g = np.random.default_rng(100 + ys).standard_normal((d, len(idx)))
            h = np.random.default_rng(200 + ys).standard_normal((d, len(idx)))
            y, _ = np.linalg.qr(g + 1j * h)
            s = np.linalg.svd(c0 + (y * theta) @ w.conj().T, compute_uv=False)
            out['model'].append({'cut': cut, 'rank': len(idx), 'left_seed': ys,
                                 'multiplicity_above_control_seed0': int(np.sum(s > s0[0])),
                                 'sigma1_over_edge': float(s[0] / (2 * math.sqrt(d)))})
    top = np.argsort(-r)[:60]
    w = np.column_stack([g6.conj() * fam[i]['vector'] for i in top])
    w /= np.linalg.norm(w, axis=0)
    for label, m in (('arithmetic', c), ('control_seed0', c0)):
        y = m @ w
        y /= np.linalg.norm(y, axis=0)
        corr = abs(y.conj().T @ y) - np.eye(60)
        out[f'left_image_abs_corr_{label}'] = {'mean': float(corr.mean()), 'max': float(corr.max())}
    doc['exploratory_model_diagnostic'] = out
    phase1e.save(doc, 'RS-S006: EXPLORATORY collective-spike model and left-image alignment')
    print(json.dumps(out, indent=1))


if __name__ == '__main__':
    main()
