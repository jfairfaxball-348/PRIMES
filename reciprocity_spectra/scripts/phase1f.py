"""RS-S007 EXPLORATORY: Patterson-type bias of twisted sextic Gauss sums, associate sum rule,
and strength profile of the RS-7b dichotomy.

bias_j(X) = |sum_pi conj(g6~(pi)) zeta6^(j(p-1)/6)| / sqrt(D) (random-walk scale ~ 1), for the
six unit classes j, and the same with g6~ instead of conj(g6~); also twisted by (u/pi)_6 for
small u. Uses the sextic Gauss-sum files and index metadata already in data/ (no matrices are
built); twist Rayleigh data come from results/phase1e_2026-10-25.json.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import phase1c  # noqa: E402
import phase1d  # noqa: E402

ROOT = phase1c.ROOT
DATA = phase1c.DATA
RESULT = ROOT / 'reciprocity_spectra/results/phase1f_2026-10-25.json'
E = ROOT / 'reciprocity_spectra/results/phase1e_2026-10-25.json'


def meta_for(x):
    """Index metadata (p, a, b) in engine order, rebuilt cheaply with a 1-prime-per-row stub."""
    path = DATA / f'sextic_meta_{x}.bin'
    if not path.exists():
        phase1c.legacy.subprocess.run([str(DATA / 'residue_engine'), 'sextic', str(x), str(path)],
                                      check=True, timeout=2700)
    with path.open('rb') as f:
        d = int(np.fromfile(f, np.int32, 1)[0])
        meta = np.fromfile(f, np.int64, 3 * d).reshape(d, 3)
    path.unlink()
    return meta


def bias(x):
    g = np.fromfile(DATA / f'sexticg_{x}.bin', np.complex128)
    meta = meta_for(x)
    assert len(meta) == len(g)
    d, p = len(g), meta[:, 0]
    z = np.exp(1j * np.pi / 3) ** (((p - 1) // 6) % 6)
    row = {'X': x, 'D': d, 'unit_class': {}, 'twists': {}}
    for j in range(6):
        t = z ** j
        row['unit_class'][str(j)] = {'conj_g6': float(abs(np.sum(g.conj() * t)) / math.sqrt(d)),
                                     'g6': float(abs(np.sum(g * t)) / math.sqrt(d))}
    for name, (c, e) in {'2': (2, 0), '-2': (-2, 0), '2w': (0, 2), 'N7 primary': (-1, -3),
                         'N7 other': (-3, -2), 'N13 primary': (1, -3), 'N13 other': (-3, 1)}.items():
        sym = phase1d.sextic_symbol(meta, c, e)
        row['twists'][name] = float(abs(np.sum(g.conj() * sym)) / math.sqrt(d))
    rng = np.random.default_rng(17)
    row['random_phase_twist'] = [float(abs(np.sum(g.conj() * np.exp(2j * np.pi * rng.random(d)))) / math.sqrt(d))
                                 for _ in range(20)]
    return row


def associates(c, d):
    out, (x, y) = [], (c, d)
    for _ in range(6):  # multiply by zeta6 = 1 + w: (x + y w)(1 + w) = (x - y) + x w
        out.append((x, y))
        x, y = x - y, x
    return out


def sum_rule():
    doc = json.loads(E.read_text())
    rows = []
    for run in doc['runs'] + doc['rayleigh_runs']:
        r = {(tuple(t['u']), t['sign']): t['r'] for t in run['twists']}
        groups = []
        for (u, sign) in r:
            if sign != '+' or (u[0] + u[1]) % 3 == 0 or u[1] % 3 or u[0] % 3 != 2:
                continue  # one primary representative per class, coprime to 3
            vals = [r.get((v, '+')) for v in associates(*u)]
            if None in vals:
                continue
            groups.append({'u': list(u), 'norm': u[0] ** 2 - u[0] * u[1] + u[1] ** 2,
                           'sum_r2_minus_1': float(sum(v * v - 1 for v in vals)),
                           'pm_mean_r2_minus_1': float(np.mean([vals[0] ** 2 - 1, vals[3] ** 2 - 1])),
                           'other_mean_r2_minus_1': float(np.mean([vals[k] ** 2 - 1 for k in (1, 2, 4, 5)]))})
        s = np.array([g['sum_r2_minus_1'] for g in groups])
        pm = np.array([g['pm_mean_r2_minus_1'] for g in groups])
        ot = np.array([g['other_mean_r2_minus_1'] for g in groups])
        n = np.array([g['norm'] for g in groups])
        fit = np.polyfit(np.log(n[n > 1]), np.log(pm[n > 1]), 1) if (n > 1).sum() > 2 else [None, None]
        rows.append({'X': run['X'], 'D': run['D'], 'classes': len(groups),
                     'mean_sum_r2_minus_1': float(s.mean()), 'sd_sum_r2_minus_1': float(s.std()),
                     'mean_pm_r2_minus_1': float(pm.mean()), 'mean_other_r2_minus_1': float(ot.mean()),
                     'ratio_other_to_pm': float(ot.mean() / pm.mean()),
                     'pm_powerlaw_exponent_in_N': None if fit[0] is None else float(fit[0]),
                     'groups': groups})
    return rows


def sum_rule_identity(x=20000):
    """Exact identity: sum_j ||C D_j w||^2 = 6 sum_c ||C (w restricted to p = c mod 36)||^2,
    with D_j = diag(zeta6^(j(p-1)/6)), by orthogonality of the six unit characters."""
    a = phase1c.build('sextic', x)
    c = a.dense()
    g = np.fromfile(DATA / f'sexticg_{x}.bin', np.complex128)
    p = a.meta[:, 0]
    w = g.conj() * phase1d.sextic_symbol(a.meta, 2, 0)
    z = np.exp(1j * np.pi / 3) ** (((p - 1) // 6) % 6)
    left = sum(np.linalg.norm(c @ (w * z ** j)) ** 2 for j in range(6))
    right = 6 * sum(np.linalg.norm(c @ (w * (p % 36 == k))) ** 2 for k in np.unique(p % 36))
    a.path.unlink()
    a.mask_path.unlink()
    return {'X': x, 'u': '2', 'left': float(left), 'right': float(right),
            'relative_error': float(abs(left - right) / right)}


def main():
    out = {'session': 'RS-S007', 'classification': 'EXPLORATORY', 'command': 'python ' + ' '.join(sys.argv),
           'code_commit': phase1c.legacy.shell('git', 'rev-parse', 'HEAD'),
           'bias': [bias(x) for x in (20000, 40000, 80000, 160000, 320000, 640000)
                    if (DATA / f'sexticg_{x}.bin').exists()],
           'sum_rule': sum_rule(), 'sum_rule_identity': sum_rule_identity()}
    RESULT.write_text(json.dumps(out, indent=2) + '\n')
    for b in out['bias']:
        print(b['X'], b['D'], {j: round(v['conj_g6'], 2) for j, v in b['unit_class'].items()},
              'g6:', {j: round(v['g6'], 2) for j, v in b['unit_class'].items()},
              {k: round(v, 2) for k, v in b['twists'].items()}, 'rand max', round(max(b['random_phase_twist']), 2))
    print('identity', out['sum_rule_identity'])
    for s in out['sum_rule']:
        print('sum rule X', s['X'], 'classes', s['classes'], 'mean sum', round(s['mean_sum_r2_minus_1'], 3),
              'sd', round(s['sd_sum_r2_minus_1'], 3), 'pm', round(s['mean_pm_r2_minus_1'], 3),
              'other', round(s['mean_other_r2_minus_1'], 3), 'ratio', round(s['ratio_other_to_pm'], 3),
              'exp', s['pm_powerlaw_exponent_in_N'])


if __name__ == '__main__':
    main()
