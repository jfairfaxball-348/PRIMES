"""RS-S012: registered tests of the twist-strength scaling laws (Patterson calibration and sextic law).

ratio_u = (r_u^2 - 1) N_cf(u)^(1/k) / (r_1^2 - 1), with k = 3 (cubic, w_u = conj(g3~)(u/.)_3, u +-primary with
squarefree cube-free part, N_cf = norm of the cube-free part) or k = 6 (sextic, w_u = conj(g6~)(u/.)_6, every
+-primary u coprime to 3). Forward matrix-vector products only (byte engine), so D up to ~8e4 fits.
"""
from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import phase1c  # noqa: E402
import phase1d  # noqa: E402
from phase1g import squarefree  # noqa: E402
from spectra import cubic_symbol_vector  # noqa: E402

DATA, ROOT, legacy = phase1c.DATA, phase1c.ROOT, phase1c.legacy
RESULT = ROOT / 'reciprocity_spectra/results/phase1j_2026-10-25.json'


def engine(mode, x):
    path, gpath = DATA / f'{mode}_{x}.bin', DATA / f'{mode}g_{x}.bin'
    subprocess.run([str(DATA / 'residue_engine'), mode, str(x), str(path), str(gpath)], check=True, timeout=2700)
    a = legacy.Engine('cubic', x, path)
    a.n = 6 if mode == 'sextic' else 3
    return a, np.fromfile(gpath, np.complex128), path, gpath


def run(mode, x, norm_max):
    a, g, path, gpath = engine(mode, x)
    k = 6 if mode == 'sextic' else 3
    rows = []
    for c in range(-12, 13):
        for d in range(-12, 13):
            n = c * c - c * d + d * d
            if not (0 < n <= norm_max and (c + d) % 3):
                continue
            pm = d % 3 == 0
            if mode == 'cubic' and pm and not squarefree(c, d) and n > 1:
                continue  # cubic law is stated on squarefree cube-free parts only
            if mode == 'sextic' and not pm and n > 13:
                continue  # sextic: all +-primary u, plus the non-primary associates at small norm
            if (c, d) == (1, 0):
                sym = np.ones(a.d)
            elif mode == 'sextic':
                sym = phase1d.sextic_symbol(a.meta, c, d)
            else:
                sym = cubic_symbol_vector(a.meta, c, d)
            w = g.conj() * sym
            w /= np.linalg.norm(w)
            rows.append({'u': [c, d], 'norm': n, 'pm_primary': pm,
                         'r': float(np.linalg.norm(a.apply(w)) / math.sqrt(a.d))})
    rng = np.random.default_rng(23)
    rand = [float(np.linalg.norm(a.apply(np.exp(2j * np.pi * rng.random(a.d)))) / a.d) for _ in range(5)]
    path.unlink()
    gpath.unlink()
    r1 = next(t['r'] for t in rows if t['u'] == [1, 0])
    law = []
    for t in rows:
        if t['pm_primary'] and t['norm'] > 1:
            ncf = 1 if t['u'] in ([8, 0], [-8, 0]) else t['norm']
            if ncf > 1:
                law.append(((t['r'] ** 2 - 1) * ncf ** (1 / k) / (r1 ** 2 - 1), ncf))
    ratio = np.array([v for v, _ in law])
    norms = np.array([n for _, n in law])
    other = [t['r'] for t in rows if not t['pm_primary']]
    return {'D': a.d, 'twists': rows, 'r_u1': r1, 'random_r': rand, 'ratio_n': len(ratio),
            'ratio_mean': float(ratio.mean()), 'ratio_sd': float(ratio.std()),
            'ratio_residual_slope': float(np.polyfit(np.log(norms), np.log(ratio), 1)[0]),
            'max_r_other_associates': max(other) if other else None,
            'min_r_pm_primary': min(t['r'] for t in rows if t['pm_primary'])}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['cubic', 'sextic'])
    parser.add_argument('--x', type=int, required=True)
    args = parser.parse_args()
    legacy.compile_engine()
    doc = json.loads(RESULT.read_text())
    pred = next(p for p in doc['predictions'] if p['mode'] == args.mode and p['X'] == args.x)
    assert doc['prediction_commit']
    started = time.monotonic()
    row = {'mode': args.mode, 'X': args.x, 'command': 'python ' + ' '.join(sys.argv),
           'code_commit': legacy.shell('git', 'rev-parse', 'HEAD'), 'started_at': datetime.now(UTC).isoformat(),
           **run(args.mode, args.x, pred['norm_max'])}
    ok = pred['mean_min'] <= row['ratio_mean'] <= pred['mean_max'] and row['ratio_sd'] <= pred['sd_max']
    if args.mode == 'sextic':
        ok = ok and row['max_r_other_associates'] < 1.0 and row['min_r_pm_primary'] > 1.0
    row.update(seconds=time.monotonic() - started,
               prediction_outcomes=[{'id': pred['id'], 'outcome': 'PASS' if ok else 'FAIL'}])
    doc['runs'].append(row)
    phase1c.phase1b.RESULT, phase1c.phase1b.BRANCH = RESULT, phase1c.BRANCH
    phase1c.phase1b.save(doc, f'RS-S012: registered {args.mode} twist-law test X={args.x}')
    print(json.dumps({k: row[k] for k in ('mode', 'X', 'D', 'r_u1', 'ratio_n', 'ratio_mean', 'ratio_sd',
                                          'ratio_residual_slope', 'max_r_other_associates', 'min_r_pm_primary',
                                          'seconds', 'prediction_outcomes')}))


if __name__ == '__main__':
    main()
