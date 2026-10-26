"""RS-S016 (EXPLORATORY): X-dependence of the single-prime class excesses.

Reruns the RS-S015 single-prime classes pi^k (k = 1..5, 20 smallest primary primes) at smaller X,
with the same construction (phase1k) and 10 + 10 seeded controls per X. s = eps * N6^(1/6).

Decision rule (written before any lower-X run; recorded in the JSON as `decision_rule`):
  T = mean s over the k = 3 singles with N >= 37 (10 classes).
  - finite-X: T increases monotonically with X over 1.6e5, 3.2e5, 6.4e5, 1e6 and gains >= 0.15 in total;
  - X-stable: |T(1e6) - T(1.6e5)| <= 0.05;
  - otherwise: undecided.
The same statistic for k = 4 (N >= 31, 12 classes) is reported alongside.

  run --x X    one scale; appends to the results JSON (no git operations)
  analyse      tables of s by (N, k, X), the decision statistic, and simple fits
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import phase1k as k1  # noqa: E402

RESULT = k1.RESULTS / 'rs_s016_x_dependence_2026-10-26.json'
SCALES = (160000, 320000, 640000)
DECISION = __doc__.split('Decision rule')[1].split('\n\n')[0]


def save(doc):
    temp = RESULT.with_suffix('.tmp')
    temp.write_text(json.dumps(doc, indent=2, allow_nan=False) + '\n')
    temp.replace(RESULT)


def load():
    if RESULT.exists():
        return json.loads(RESULT.read_text())
    return {'session': 'RS-S016', 'classification': 'EXPLORATORY', 'date': '2026-10-26',
            'decision_rule': 'Decision rule' + DECISION, 'runs': []}


def run(x):
    doc = load()
    k1.legacy.compile_engine()
    started = time.monotonic()
    row = {'X': x, 'command': 'python ' + ' '.join(sys.argv), 'platform': sys.platform,
           'code_commit': k1.legacy.shell('git', 'rev-parse', 'HEAD'),
           'started_at': datetime.now(UTC).isoformat()}
    a, g = k1.build(x)
    base = g.conj()
    row.update(D=a.d, matrix_sha256=k1.digest(a.path), r_u1=k1.rayleigh(a, base))
    z6 = np.exp(1j * np.pi / 3 * np.arange(6))
    symbols, rows = {}, []
    for c in (c for c in k1.classes() if c['part'] == 'singles'):
        (pi, e), = c['kappa']
        if tuple(pi) not in symbols:
            symbols[tuple(pi)] = k1.exponent_vector(a.meta, pi)
        v = symbols[tuple(pi)]
        w = np.where(v < 0, 0, base * z6[(e * v.astype(np.int64)) % 6])
        rows.append({'kappa': c['kappa'], 'N6': c['N6'], 'zero_rows': int((v < 0).sum()), 'r': k1.rayleigh(a, w)})
    rng = np.random.default_rng(16)
    row.update(classes=rows, control_seed=16,
               random_phase_r=[k1.rayleigh(a, np.exp(2j * np.pi * rng.random(a.d))) for _ in range(10)],
               conj_g6_random_roots_r=[k1.rayleigh(a, base * z6[rng.integers(0, 6, a.d)]) for _ in range(10)],
               seconds=time.monotonic() - started)
    del a
    k1.release(k1.DATA / f'sextic_{x}.bin', k1.DATA / f'sexticg_{x}.bin')
    doc['runs'] = [r for r in doc['runs'] if r['X'] != x] + [row]
    doc['runs'].sort(key=lambda r: r['X'])
    save(doc)
    print(json.dumps({k: row[k] for k in ('X', 'D', 'r_u1', 'seconds')}))


def table():
    """{X: (r1, D, controls_sd, [(N, k, r, s)])} including the stored RS-S015 X = 10^6 singles."""
    out = {}
    s15 = json.loads(k1.RESULT.read_text())['runs'][0]
    for r in load()['runs'] + [dict(s15, X=k1.X)]:
        r1 = r['r_u1']
        rows = []
        for c in r['classes']:
            (pi, e), = c['kappa']
            eps = (c['r'] ** 2 - 1) / (r1 ** 2 - 1)
            rows.append((k1.norm(pi), e, c['r'], eps * c['N6'] ** (1 / 6)))
        out[r['X']] = (r1, r['D'], float(np.std(r['random_phase_r'])), rows)
    return dict(sorted(out.items()))


def analyse():
    doc, tab = load(), table()
    xs = list(tab)
    stats = {}
    for k, nmin in ((1, 37), (2, 37), (3, 37), (4, 31), (5, 37)):
        series = [float(np.mean([s for n, e, _, s in tab[x][3] if e == k and n >= nmin])) for x in xs]
        stats[f'k{k}_N>={nmin}'] = dict(zip(map(str, xs), series, strict=True))
    t = list(stats['k3_N>=37'].values())
    mono = all(b > a for a, b in zip(t, t[1:], strict=False))
    verdict = ('finite-X' if mono and t[-1] - t[0] >= 0.15 else
               'X-stable' if abs(t[-1] - t[0]) <= 0.05 else 'undecided')
    # Per-(N, k) series and simple fits: log eps against log N at each X and k (eps > 0 only).
    per = {}
    for x in xs:
        for n, e, _, s in tab[x][3]:
            per.setdefault(f'{e}', {}).setdefault(str(n), {})[str(x)] = round(s, 4)
    fits = {}
    for x in xs:
        r1, _, _, rows = tab[x]
        for k in range(1, 5):
            pts = [(n, s / n ** (k / 6)) for n, e, _, s in rows if e == k and s > 0.05]
            if len(pts) >= 6:
                slope, icept = np.polyfit(np.log([p[0] for p in pts]), np.log([p[1] for p in pts]), 1)
                fits[f'k{k}_X{x}'] = {'n': len(pts), 'eps_power_of_N': float(slope),
                                      'const': float(np.exp(icept))}
    # Collapse in t = N6 / X^a: roughness = mean squared step of s after sorting by log t (a-scan),
    # and half-decade bins of log10(N6/X) for exponents {2,3,4} pooled and for exponent 5.
    def points(ks):
        return [(n ** e, x, s) for x in xs for n, e, _, s in tab[x][3] if e in ks]

    def rough(p, a):
        z = sorted(p, key=lambda t: np.log(t[0]) - a * np.log(t[1]))
        return float(np.mean(np.diff([t[2] for t in z]) ** 2))

    grid = [round(v, 2) for v in np.linspace(0, 2, 41)]
    scan = {}
    for name, ks in (('k2', [2]), ('k3', [3]), ('k4', [4]), ('k234', [2, 3, 4]), ('k5', [5])):
        v = [rough(points(ks), a) for a in grid]
        scan[name] = {'best_a': grid[int(np.argmin(v))], 'roughness_best': min(v),
                      'roughness_a0': v[0], 'roughness_a1': v[20]}
    bins = {}
    for name, ks in (('k234', [2, 3, 4]), ('k2', [2]), ('k3', [3]), ('k4', [4]), ('k5', [5])):
        z = np.array([(np.log10(t / x), s) for t, x, s in points(ks)])
        rows = []
        for lo in np.arange(-6.0, 4.5, 0.5):
            m = (z[:, 0] >= lo) & (z[:, 0] < lo + 0.5)
            if m.sum():
                rows.append({'log10_t_lo': float(lo), 'n': int(m.sum()), 'mean_s': float(z[m, 1].mean()),
                             'sd_s': float(z[m, 1].std())})
        bins[name] = rows
    doc['analysis'] = {'collapse_a_scan': scan, 'collapse_bins_t_eq_N6_over_X': bins,'scales': xs, 'r_u1': {str(x): tab[x][0] for x in xs},
                       'D': {str(x): tab[x][1] for x in xs},
                       'random_phase_sd': {str(x): tab[x][2] for x in xs},
                       'group_mean_s': stats, 'decision_statistic_T': t, 'verdict': verdict,
                       's_by_k_N_X': per, 'eps_power_fits': fits}
    save(doc)
    print(json.dumps({k: doc['analysis'][k] for k in ('r_u1', 'group_mean_s', 'verdict', 'eps_power_fits')},
                     indent=1))


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('step', choices=['run', 'analyse'])
    parser.add_argument('--x', type=int)
    args = parser.parse_args()
    if args.step == 'run':
        run(args.x)
    else:
        analyse()


if __name__ == '__main__':
    main()
