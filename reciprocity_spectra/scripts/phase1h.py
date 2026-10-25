"""RS-S010: Astra's decisive test (Q5) -- Kubota partial sums of sextic Gauss sums by unit class.

T_j(X) = sum over squarefree n in Z[w], (n, 6) = 1, N(n) <= X, of g6(zeta6^j, n) / sqrt(N n),
with n a product of primary primes (split primary pi; inert rational q = 2 mod 3, q > 2) and the
trace-form Gauss sum g6(c, n) = sum_{x mod n} (x/n)_6 e(Tr(c x / n)) (arith.kubota_g6_prime;
twisted multiplicativity g6(c, n1 n2) = (n1/n2)_6 (n2/n1)_6 g6(c, n1) g6(c, n2), tested).
For a unit c, g6(c, n) = conj((c/n)_6) g6(1, n), and (zeta6/pi)_6 = zeta6^((N pi - 1)/6).
Split-prime sums come from the native engine (RS_NO_MATRIX=1): g_ours = (conj pi/pi)_6 g6(1, pi).
"""
from __future__ import annotations

import argparse
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
    primes_upto,
    sextic_residue_exponent,
    sextic_symbol_at,
)

DATA, ROOT = phase1c.DATA, phase1c.ROOT
RESULT = ROOT / 'reciprocity_spectra/results/phase1h_2026-10-25.json'
Z6 = np.exp(1j * np.pi / 3) ** np.arange(6)


def split_primes(x):
    """Primary split primes with normalized trace-form Gauss sums g6(1, pi)/sqrt(p)."""
    meta_path, g_path = DATA / f'kubota_meta_{x}.bin', DATA / f'kubota_g_{x}.bin'
    subprocess.run([str(DATA / 'residue_engine'), 'sextic', str(x), str(meta_path), str(g_path)],
                   check=True, env=os.environ | {'RS_NO_MATRIX': '1'}, timeout=2700)
    with meta_path.open('rb') as f:
        d = int(np.fromfile(f, np.int32, 1)[0])
        meta = np.fromfile(f, np.int64, 3 * d).reshape(d, 3)
    g = np.fromfile(g_path, np.complex128)
    meta_path.unlink()
    g_path.unlink()
    out = []
    for (p, a, b), gv in zip(meta.tolist(), g, strict=True):
        pi = DegreeOnePrime(3, p, a, b)
        k = sextic_residue_exponent(a - b, -b, pi)  # (conj pi / pi)_6
        out.append({'norm': p, 'elem': (a, b), 'prime': pi, 'g': complex(gv * Z6[(-k) % 6]),
                    'unit': ((p - 1) // 6) % 6})
    return out


def inert_gauss(q):
    """Normalized trace-form g6(1, q)/q for inert q, vectorized over F_{q^2} = F_q[w]."""
    s, t = np.meshgrid(np.arange(q), np.arange(q), indexing='ij')
    s, t = s.ravel().astype(np.int64), t.ravel().astype(np.int64)
    nz = (s != 0) | (t != 0)
    s, t = s[nz], t[nz]

    def mul(x0, x1, y0, y1):
        return (x0 * y0 - x1 * y1) % q, (x0 * y1 + x1 * y0 - x1 * y1) % q

    r0, r1 = np.ones_like(s), np.zeros_like(s)
    b0, b1, e = s.copy(), t.copy(), (q * q - 1) // 6
    while e:
        if e & 1:
            r0, r1 = mul(r0, r1, b0, b1)
        b0, b1 = mul(b0, b1, b0, b1)
        e >>= 1
    k = np.full(len(s), -1)
    p0, p1 = 1, 0
    for j in range(6):  # powers of zeta6 = 1 + w
        k[(r0 == p0) & (r1 == p1)] = j
        p0, p1 = (p0 - p1) % q, p0 % q
    assert (k >= 0).all()
    return complex(np.sum(Z6[k] * np.exp(2j * np.pi * (2 * s - t) / q)) / q)


def build_primes(x, psi=False, split_only=False):
    """psi: multiply each split g6(1, pi) by (conj pi / pi)_6, the factor relating the trace form to
    the matrix normalization g_ours (RS-S010 finding; Astra check 3). Inert q keep psi(q) = 1."""
    primes = split_primes(x)
    if psi:
        for r in primes:
            a, b = r['elem']
            r['g'] *= Z6[sextic_symbol_at(a - b, -b, r['prime'])]
    for q in ([] if split_only else primes_upto(math.isqrt(x))):
        if q % 3 == 2 and q > 2:
            primes.append({'norm': q * q, 'elem': (q, 0), 'prime': q, 'g': inert_gauss(q),
                           'unit': ((q * q - 1) // 6) % 6})
    primes.sort(key=lambda r: r['norm'])
    return primes


def mul_w(x, y):
    return (x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0] - x[1] * y[1])


def kubota_sums(x, grid, psi=False, split_only=False):
    """Accumulate g6(zeta6^j, n)/sqrt(N n) over squarefree n by depth-first products of primes."""
    primes = build_primes(x, psi, split_only)
    norms = np.array([r['norm'] for r in primes])
    sums = np.zeros((len(grid), 6), complex)
    count = np.zeros(len(grid), int)
    grid_arr = np.array(grid)
    stack = [(1, (1, 0), 1 + 0j, 0, [], -1)]  # norm, element, g(1,n)/sqrt(N), unit exponent, factors, last index
    nodes = 0
    while stack:
        norm, elem, g, unit, factors, last = stack.pop()
        if norm > 1:
            nodes += 1
            vals = g * np.conj(Z6[(np.arange(6) * unit) % 6])
            idx = np.searchsorted(grid_arr, norm)
            sums[idx:] += vals
            count[idx:] += 1
        limit = x // norm
        hi = int(np.searchsorted(norms, limit, side='right'))
        for i in range(last + 1, hi):
            pr = primes[i]
            k = sextic_symbol_at(*elem, pr['prime']) if factors else 0  # (n / pi)_6
            if k is None:
                continue
            for f in factors:  # (pi / n)_6 = prod (pi / f)_6
                kf = sextic_symbol_at(*pr['elem'], f)
                if kf is None:
                    k = None
                    break
                k += kf
            if k is None:
                continue
            stack.append((norm * pr['norm'], mul_w(elem, pr['elem']), g * pr['g'] * Z6[k % 6],
                          (unit + pr['unit']) % 6, factors + [pr['prime']], i))
    return sums, count, nodes, len(primes)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('label', choices=['EXPLORATORY', 'REGISTERED'])
    parser.add_argument('--x', type=int, required=True)
    parser.add_argument('--psi', action='store_true')
    parser.add_argument('--split-only', action='store_true')
    args = parser.parse_args()
    phase1c.legacy.compile_engine()
    doc = json.loads(RESULT.read_text()) if RESULT.exists() else {
        'session': 'RS-S010', 'date': '2026-10-25', 'source': 'ASTRA_RESPONSE_2026-10-25.md, Q5',
        'definition': __doc__, 'predictions': [], 'prediction_commit': None, 'runs': []}
    if args.label == 'REGISTERED':
        assert doc['prediction_commit'] and args.x == 1280000 and not args.psi and not args.split_only, 'register first'
    grid = [int(1000 * 2 ** k) for k in range(40) if 1000 * 2 ** k <= args.x]
    if grid[-1] != args.x:
        grid.append(args.x)
    started = time.monotonic()
    sums, count, nodes, nprimes = kubota_sums(args.x, grid, args.psi, args.split_only)
    row = {'X': args.x, 'classification': args.label, 'psi': args.psi, 'split_only': args.split_only, 'grid': grid, 'count': count.tolist(),
           'abs_T': np.abs(sums).T.tolist(), 'T_re': sums.real.T.tolist(), 'T_im': sums.imag.T.tolist(),
           'nodes': nodes, 'primes': nprimes, 'seconds': time.monotonic() - started,
           'command': 'python ' + ' '.join(sys.argv), 'code_commit': phase1c.legacy.shell('git', 'rev-parse', 'HEAD'),
           'started_at': datetime.now(UTC).isoformat()}
    if args.label == 'REGISTERED':
        score(doc, row)
    doc['runs'].append(row)
    phase1c.phase1b.RESULT, phase1c.phase1b.BRANCH = RESULT, phase1c.BRANCH
    phase1c.phase1b.save(doc, f'RS-S010: {args.label} Kubota sums X={args.x} psi={args.psi} split_only={args.split_only}')
    for gx, c, t in zip(grid, count, np.abs(sums), strict=True):
        print(gx, c, ' '.join(f'{v:9.1f}' for v in t), flush=True)
    print('nodes', nodes, 'seconds', round(row['seconds'], 1), row.get('prediction_outcomes'))


def primes_only_matrix_norm(x):
    """|sum over split primes of g_ours(zeta6^j, rho)/sqrt(p)| / sqrt(count), g_ours = (conj rho/rho)_6 g6."""
    primes = build_primes(x, psi=True, split_only=True)
    t = np.zeros(6, complex)
    for r in primes:
        t += r['g'] * np.conj(Z6[(np.arange(6) * r['unit']) % 6])
    return (np.abs(t) / math.sqrt(len(primes))).tolist(), len(primes)


def score(doc, row):
    xs, n = np.array(row['grid'], float), np.array(row['count'], float)
    m = xs >= 128000
    slope = [float(np.polyfit(np.log(xs[m]), np.log(np.array(row['abs_T'][j])[m]), 1)[0]) for j in range(6)]
    ratio = [row['abs_T'][j][-1] / math.sqrt(n[-1]) for j in range(6)]
    prime_ratio, nprimes = primes_only_matrix_norm(row['X'])
    row.update(slopes_from_128000=slope, ratio_to_sqrt_count=ratio, primes_only_matrix_norm=prime_ratio,
               primes_only_count=nprimes)
    out = [
        {'id': 'RS-S010-ASTRA-Q5', 'value': [slope[0], slope[1]],
         'outcome': 'PASS' if 0.5667 <= slope[0] <= 0.7667 and slope[1] <= 0.6 else 'FAIL'},
        {'id': 'RS-S010-K1-trace', 'value': [slope[1], ratio[1], ratio[0]],
         'outcome': 'PASS' if 0.55 <= slope[1] <= 0.85 and ratio[1] >= 3.0 and ratio[0] <= 2.0 else 'FAIL'},
        {'id': 'RS-S010-K2-primes-matrix-norm', 'value': prime_ratio,
         'outcome': 'PASS' if prime_ratio[0] >= 2.0 and max(prime_ratio[j] for j in (1, 2, 4, 5)) <= 1.5 else 'FAIL'}]
    row['prediction_outcomes'] = out


if __name__ == '__main__':
    main()
