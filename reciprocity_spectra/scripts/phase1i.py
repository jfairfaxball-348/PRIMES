"""RS-S011: selection table of the sextic Gauss-sum main term over primes.

B(j, chi)(window) = |sum_rho g6_trace(zeta6^j, rho) chi(rho) / sqrt(p)| / sqrt(count) over primary split
primes rho with p in the window, for the six unit classes j and the twelve characters chi = (m, s1, s2)
of (Z[w]/4)^x (arith.mod4_character). g6_trace = trace-form (Heath-Brown--Patterson) Gauss sum;
g6_trace(zeta6^j, rho) = conj((zeta6^j/rho)_6) g6_trace(1, rho). Also the Fourier expansion of the
matrix-normalization sign psi(rho) = (conj rho/rho)_6 over the twelve characters. Ratios (not slopes)
are the statistic; random-walk size is 1.
"""
from __future__ import annotations

import argparse
import itertools
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
import phase1c  # noqa: E402

from reciprocity_spectra.arith import (  # noqa: E402
    DegreeOnePrime,
    mod4_class_coordinates,
    sextic_residue_exponent,
)

DATA, ROOT = phase1c.DATA, phase1c.ROOT
RESULT = ROOT / 'reciprocity_spectra/results/phase1i_2026-10-25.json'
Z6 = np.exp(1j * np.pi / 3) ** np.arange(6)
CHARS = list(itertools.product(range(3), range(2), range(2)))


def char_table(coords):
    """Values chi_(m,s1,s2) on rows with coordinates (i, k, l): shape (12, len)."""
    i, k, l2 = coords.T
    return np.array([np.exp(2j * np.pi * m * i / 3) * (-1.0) ** (s1 * k + s2 * l2) for m, s1, s2 in CHARS])


def primes_with_gauss(x, xmin=0):
    """Primary split primes with trace-form g6(1, rho)/sqrt(p), class coordinates, unit and psi."""
    meta_path, g_path = DATA / f'sel_meta_{x}.bin', DATA / f'sel_g_{x}.bin'
    env = os.environ | {'RS_NO_MATRIX': '1', 'RS_GAUSS_MIN': str(xmin)}
    subprocess.run([str(DATA / 'residue_engine'), 'sextic', str(x), str(meta_path), str(g_path)],
                   check=True, env=env, timeout=2700)
    with meta_path.open('rb') as f:
        d = int(np.fromfile(f, np.int32, 1)[0])
        meta = np.fromfile(f, np.int64, 3 * d).reshape(d, 3)
    g = np.fromfile(g_path, np.complex128)
    meta_path.unlink()
    g_path.unlink()
    keep = meta[:, 0] > xmin
    meta, g = meta[keep], g[keep]
    psi = np.empty(len(meta))
    coords = np.empty((len(meta), 3), int)
    for idx, (p, a, b) in enumerate(meta.tolist()):
        k = sextic_residue_exponent(a - b, -b, DegreeOnePrime(3, p, a, b))
        psi[idx] = 1 - 2 * (k == 3)
        coords[idx] = mod4_class_coordinates(a, b)
    g_trace = g * psi  # g_ours = psi * g_trace and psi = +-1
    unit = ((meta[:, 0] - 1) // 6) % 6
    return meta, g_trace, coords, unit, psi


def table(g_trace, coords, unit, mask):
    chars = char_table(coords[mask])
    n = int(mask.sum())
    out = np.zeros((6, 12))
    for j in range(6):
        twisted = g_trace[mask] * np.conj(Z6[(j * unit[mask]) % 6])
        out[j] = np.abs(chars @ twisted) / math.sqrt(n)
    return out, n


def psi_expansion(coords, psi):
    """Coefficients c_chi with psi = sum c_chi chi on the twelve classes (exact class function)."""
    values = {}
    for c, v in zip(map(tuple, coords), psi, strict=True):
        assert values.setdefault(c, v) == v
    classes = sorted(values)
    chars = char_table(np.array(classes))
    vec = np.array([values[c] for c in classes])
    coef = chars.conj() @ vec / len(classes)
    return {f'{m}{s1}{s2}': [round(float(z.real), 12), round(float(z.imag), 12)]
            for (m, s1, s2), z in zip(CHARS, coef, strict=True)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('label', choices=['EXPLORATORY', 'REGISTERED'])
    parser.add_argument('--x', type=int, required=True)
    parser.add_argument('--xmin', type=int, default=0)
    args = parser.parse_args()
    phase1c.legacy.compile_engine()
    doc = json.loads(RESULT.read_text()) if RESULT.exists() else {
        'session': 'RS-S011', 'date': '2026-10-25', 'definition': __doc__,
        'characters': ['m s1 s2 = ' + ''.join(map(str, c)) for c in CHARS],
        'predictions': [], 'prediction_commit': None, 'runs': []}
    started = time.monotonic()
    meta, g_trace, coords, unit, psi = primes_with_gauss(args.x, args.xmin)
    windows = {}
    for lo, hi in ([(0, 80000), (0, 320000), (0, 1280000), (320000, 1280000)] if args.label == 'EXPLORATORY'
                   else [(args.xmin, args.x)]):
        mask = (meta[:, 0] > lo) & (meta[:, 0] <= hi)
        if mask.sum() and hi <= args.x and lo >= args.xmin:
            t, n = table(g_trace, coords, unit, mask)
            windows[f'{lo}-{hi}'] = {'count': n, 'B': t.tolist()}
    row = {'X': args.x, 'xmin': args.xmin, 'classification': args.label, 'windows': windows,
           'psi_expansion': psi_expansion(coords, psi), 'seconds': time.monotonic() - started,
           'command': 'python ' + ' '.join(sys.argv), 'code_commit': phase1c.legacy.shell('git', 'rev-parse', 'HEAD'),
           'started_at': datetime.now(UTC).isoformat()}
    if args.label == 'REGISTERED':
        assert doc['prediction_commit'] and (args.x, args.xmin) == (1920000, 1280000)
        score(doc, row)
    doc['runs'].append(row)
    phase1c.phase1b.RESULT, phase1c.phase1b.BRANCH = RESULT, phase1c.BRANCH
    phase1c.phase1b.save(doc, f'RS-S011: {args.label} selection table X={args.x} xmin={args.xmin}')
    for name, w in windows.items():
        print('window', name, 'count', w['count'])
        print('      ' + ' '.join(f'{"".join(map(str, c)):>6}' for c in CHARS))
        for j in range(6):
            print(f'j={j}  ' + ' '.join(f'{v:6.2f}' for v in w['B'][j]))
    print('psi expansion', {k: v for k, v in row['psi_expansion'].items() if abs(complex(*v)) > 1e-9})
    print('outcomes', row.get('prediction_outcomes'), 'seconds', round(row['seconds']))


def score(doc, row):
    """Pooled mean of B^2 over the rule pairs (m = 0, s1 = 1) and over the two complementary groups."""
    b2 = np.array(next(iter(row['windows'].values()))['B']) ** 2
    groups = {'rule': [], 'cubic_nontrivial': [], 'even_trivial_cubic': []}
    for j in range(6):
        for c, (m, s1, _) in enumerate(CHARS):
            key = 'rule' if m == 0 and s1 == 1 else 'cubic_nontrivial' if m else 'even_trivial_cubic'
            groups[key].append(b2[j, c])
    means = {k: float(np.mean(v)) for k, v in groups.items()}
    p = doc['predictions'][0]
    ok = means['rule'] >= p['rule_min'] and max(means['cubic_nontrivial'], means['even_trivial_cubic']) <= p['other_max']
    row['prediction_outcomes'] = [{'id': p['id'], 'means': means, 'outcome': 'PASS' if ok else 'FAIL'}]


if __name__ == '__main__':
    main()
