"""RS-S009: cubic twist strengths (Astra calibration, check 2) and outlier count.

r_u = ||C w_u|| / (sqrt(D) ||w_u||), w_u = conj(g3~) (u/pi)_3 for u coprime to 3, N(u) <= 200;
'+-primary' means d = 0 mod 3. Outliers: cubic singular values above the seed-0
conjugation-matched control sigma1 (dense SVD). Scores the RS-S009 registered predictions.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import phase1c  # noqa: E402
from spectra import cubic_symbol_vector  # noqa: E402

RESULT = phase1c.ROOT / 'reciprocity_spectra/results/phase1g_2026-10-25.json'


def quotient(c, d, a, b):
    """(c + d w)/(a + b w) in Z[w], or None if not integral."""
    n = a * a - a * b + b * b
    re, im = c * (a - b) + d * b, d * a - c * b  # (c + d w)((a - b) - b w), using w^2 = -1 - w
    return (re // n, im // n) if re % n == 0 and im % n == 0 else None


def prime_elements(limit):
    """Prime elements of Z[w] up to units with norm <= limit (split, inert; 1 - w excluded)."""
    out = []
    for a in range(-30, 31):
        for b in range(-30, 31):
            m = a * a - a * b + b * b
            if 1 < m <= limit and b % 3 == 0 and a % 3 == 2:
                q = int(round(m ** .5))
                if all(m % k for k in range(2, int(m ** .5) + 1)) or (q * q == m and q % 3 == 2 and b == 0
                                                                      and all(q % k for k in range(2, q))):
                    out.append((a, b))
    return out


def squarefree(c, d):
    """Cube-free part of u = c + d w (coprime to 3) is squarefree: every v_pi(u) mod 3 is 0 or 1.

    Cubic twists depend on u only modulo cubes, so this is the relevant notion for (u/pi)_3.
    """
    n = c * c - c * d + d * d
    for a, b in prime_elements(n):
        v, cur = 0, (c, d)
        while (q := quotient(*cur, a, b)) is not None:
            v, cur = v + 1, q
        if v % 3 == 2:
            return False
    return True


def score160(row, preds):
    pm = [t for t in row['twists'] if t['class'] == 'pm-primary' and t['norm'] > 1]
    sf = [t for t in pm if t['squarefree']]
    nsf = [t for t in pm if not t['squarefree']]
    other = [t['r'] for t in row['twists'] if t['class'] == 'other']
    slope = float(np.polyfit(np.log([t['norm'] for t in sf]), np.log([t['r'] ** 2 - 1 for t in sf]), 1)[0]) \
        if all(t['r'] > 1 for t in sf) else None
    row.update(slope_squarefree=slope, min_r_squarefree=min(t['r'] for t in sf),
               max_r_nonsquarefree=max(t['r'] for t in nsf), max_r_other=max(other))
    p = {q['id']: q for q in preds}
    a = p['RS-S009-C1-slope']
    row['prediction_outcomes'] = [
        {'id': a['id'], 'value': slope, 'outcome': 'PASS' if slope is not None and a['min'] <= slope <= a['max'] else 'FAIL'},
        {'id': 'RS-S009-C2-squarefree', 'value': [row['min_r_squarefree'], row['max_r_nonsquarefree']],
         'outcome': 'PASS' if row['min_r_squarefree'] > 1.05 and row['max_r_nonsquarefree'] < 1.0 else 'FAIL'},
        {'id': 'RS-S009-C3-associates', 'value': row['max_r_other'],
         'outcome': 'PASS' if row['max_r_other'] < 1.0 else 'FAIL'}]


def main():
    x = int(sys.argv[1]) if len(sys.argv) > 1 else 40000
    phase1c.legacy.compile_engine()
    doc = json.loads(RESULT.read_text())
    assert doc['prediction_commit']
    data = phase1c.DATA
    phase1c.legacy.subprocess.run([str(data / 'residue_engine'), 'cubic', str(x), str(data / f'cubic_{x}.bin'),
                                   str(data / f'cubicg_{x}.bin')], check=True)
    a = phase1c.ConjEngine('cubic', x)
    g3 = np.fromfile(data / f'cubicg_{x}.bin', np.complex128)
    dense = x <= 40000
    c = a.dense() if dense else None
    apply = (lambda v: c @ v) if dense else a.apply
    twists = []
    for cc in range(-16, 17):
        for dd in range(-16, 17):
            n = cc * cc - cc * dd + dd * dd
            if 0 < n <= 200 and (cc + dd) % 3:
                w = g3.conj() * (np.ones(a.d) if (cc, dd) == (1, 0) else cubic_symbol_vector(a.meta, cc, dd))
                w /= np.linalg.norm(w)
                twists.append({'u': [cc, dd], 'norm': n, 'class': 'pm-primary' if dd % 3 == 0 else 'other',
                               'squarefree': squarefree(cc, dd),
                               'r': float(np.linalg.norm(apply(w)) / math.sqrt(a.d))})
    edge = 2 * math.sqrt(a.d)
    if not dense:
        row = {'X': x, 'D': a.d, 'code_commit': phase1c.legacy.shell('git', 'rev-parse', 'HEAD'),
               'command': 'python ' + ' '.join(sys.argv), 'twists': twists, 'classification': 'REGISTERED',
               'r_u1': next(t['r'] for t in twists if t['u'] == [1, 0])}
        score160(row, doc['predictions'])
        doc.setdefault('runs', []).append(row)
        phase1c.phase1b.RESULT, phase1c.phase1b.BRANCH = RESULT, phase1c.BRANCH
        phase1c.phase1b.save(doc, f'RS-S009: REGISTERED cubic twist dichotomy X={x}')
        print(json.dumps({k: row[k] for k in ('X', 'D', 'r_u1', 'slope_squarefree', 'min_r_squarefree',
                                              'max_r_nonsquarefree', 'max_r_other', 'prediction_outcomes')}))
        return
    s = np.linalg.svd(c, compute_uv=False)
    a.control(0)
    s0 = np.linalg.svd(a.dense(), compute_uv=False)
    a.path.unlink()
    pm = [t for t in twists if t['class'] == 'pm-primary' and t['norm'] > 1]
    ok = all(t['r'] > 1 for t in pm)
    slope = float(np.polyfit(np.log([t['norm'] for t in pm]), np.log([t['r'] ** 2 - 1 for t in pm]), 1)[0]) if ok else None
    count = int(np.sum(s > s0[0]))
    row = {'X': x, 'D': a.d, 'code_commit': phase1c.legacy.shell('git', 'rev-parse', 'HEAD'),
           'command': 'python ' + ' '.join(sys.argv), 'twists': twists, 'slope_pm': slope,
           'r_u1': next(t['r'] for t in twists if t['u'] == [1, 0]),
           'supercritical_pm_twists': sum(t['r'] > math.sqrt(2) for t in pm),
           'top40_over_edge': (s[:40] / edge).tolist(), 'control_sigma1_over_edge': float(s0[0] / edge),
           'outliers_above_control': count}
    if x == 40000:
        lo, hi = doc['predictions'][0]['min'], doc['predictions'][0]['max']
        row['prediction_outcomes'] = [
            {'id': 'RS-S009-A2-exponent', 'value': slope,
             'outcome': 'PASS' if slope is not None and lo <= slope <= hi else 'FAIL'},
            {'id': 'RS-S009-A2-count', 'value': count, 'outcome': 'PASS' if count >= 24 else 'FAIL'}]
        row['classification'] = 'REGISTERED'
    else:
        row['classification'] = 'EXPLORATORY'
    doc.setdefault('runs', []).append(row)
    phase1c.phase1b.RESULT, phase1c.phase1b.BRANCH = RESULT, phase1c.BRANCH
    phase1c.phase1b.save(doc, f'RS-S009: {row["classification"]} cubic twist strengths X={x}')
    print(json.dumps({k: row[k] for k in ('X', 'D', 'slope_pm', 'r_u1', 'supercritical_pm_twists',
                                          'outliers_above_control', 'control_sigma1_over_edge')}
                     | {'top12': [round(v, 3) for v in row['top40_over_edge'][:12]],
                        'outcomes': row.get('prediction_outcomes')}))


if __name__ == '__main__':
    main()
