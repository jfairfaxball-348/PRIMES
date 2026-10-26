"""RS-S022: normalization-artefact check for CAND-002 on stored single-class data (six scales).

Single-prime classes pi^k (RS-S015 singles) at X = 1.6e5, 3.2e5, 6.4e5 (RS-S016), 1e6 (RS-S015),
2e6, 4e6 (RS-S021). Three normalizations of the class excess:
  frozen      s   = (r^2 - 1)/(r_1^2 - 1) * N6^(1/6)
  raw         u   = (r^2 - 1) * N6^(1/6)                (no r_1 normalization)
  control     s_c = (r^2 - c0)/(r_1^2 - c0) * N6^(1/6), c0 = mean r^2 of the random-phase controls
For each: collapse roughness in t = N6/X for exponents {2,3,4} (mean squared step after sorting by log t),
the spread across X of half-decade bin means, and the pi^5 mean for t >= 3.
"""
from __future__ import annotations

import argparse
import json
import math
from datetime import UTC, datetime
from pathlib import Path

import numpy as np

RESULTS = Path(__file__).resolve().parents[1] / 'results'
RESULT = RESULTS / 'rs_s022_cand002_audit_2026-10-26.json'


def runs():
    out = []
    for r in json.loads((RESULTS / 'rs_s016_x_dependence_2026-10-26.json').read_text())['runs']:
        out.append((r['X'], r['r_u1'], r['random_phase_r'], r['classes']))
    r = json.loads((RESULTS / 'rs_s015_class_tests_2026-10-26.json').read_text())['runs'][0]
    out.append((1_000_000, r['r_u1'], r['random_phase_r'], r['classes']))
    for r in json.loads((RESULTS / 'rs_s021_large_x_2026-10-26.json').read_text())['runs']:
        out.append((r['X'], r['r_u1'], r['random_phase_r'], r['classes']))
    return sorted(out, key=lambda t: t[0])


def norm(pi):
    return pi[0] ** 2 - pi[0] * pi[1] + pi[1] ** 2


def points():
    pts = []
    for x, r1, ctrl, classes in runs():
        c0 = float(np.mean(np.square(ctrl)))
        for c in classes:
            (pi, k), = c['kappa']
            n6 = norm(pi) ** k
            r2 = c['r'] ** 2
            pts.append({'X': x, 'k': k, 'N': norm(pi), 't': n6 / x,
                        'frozen': (r2 - 1) / (r1 ** 2 - 1) * n6 ** (1 / 6),
                        'raw': (r2 - 1) * n6 ** (1 / 6),
                        'control': (r2 - c0) / (r1 ** 2 - c0) * n6 ** (1 / 6)})
    return pts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true',
                        help='Compare against the committed RS-S022 record without writing it')
    args = parser.parse_args()
    pts = points()
    out = {'date': datetime.now(UTC).date().isoformat(), 'scales': sorted({p['X'] for p in pts}),
           'n_points': len(pts), 'normalizations': {}}
    for key in ('frozen', 'raw', 'control'):
        mid = sorted((p for p in pts if p['k'] in (2, 3, 4)), key=lambda p: math.log(p['t']))
        rough = float(np.mean(np.diff([p[key] for p in mid]) ** 2))
        bins = {}
        for p in mid:
            bins.setdefault(math.floor(math.log10(p['t']) * 2) / 2, {}).setdefault(p['X'], []).append(p[key])
        spreads = [float(np.std([np.mean(v) for v in per_x.values()]))
                   for per_x in bins.values() if len(per_x) >= 3]
        p5 = [p[key] for p in pts if p['k'] == 5 and p['t'] >= 3]
        out['normalizations'][key] = {'collapse_roughness_k234': rough,
                                      'median_across_X_spread_of_bin_means': float(np.median(spreads)),
                                      'pi5_mean_t_ge_3': float(np.mean(p5)), 'pi5_n': len(p5)}
    if args.check:
        recorded = json.loads(RESULT.read_text(encoding='utf-8'))
        assert out['scales'] == recorded['scales']
        assert out['n_points'] == recorded['n_points']
        assert out['normalizations'].keys() == recorded['normalizations'].keys()
        for key, fields in out['normalizations'].items():
            expected = recorded['normalizations'][key]
            assert fields.keys() == expected.keys()
            for name, actual in fields.items():
                target = expected[name]
                assert (math.isclose(actual, target, rel_tol=1e-12, abs_tol=1e-14)
                        if isinstance(actual, float) else actual == target), (key, name)
        print('RS-S022 CAND-002 audit: PASS (read-only)')
    else:
        RESULT.write_text(json.dumps(out, indent=2) + '\n')
        print(json.dumps(out, indent=1))


if __name__ == '__main__':
    main()
