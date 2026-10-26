"""RS-S017: registered fresh-class tests of PROV-RS16 (RS_S016_CROSSOVER.md section 5).

Fresh classes use only primary primes with 79 <= N <= 400 (none used in RS-S015/16):
singles pi^k (k = 1..5) over all 58 such primes, and pairs (e1, e2) in {1..5}^2 over the 6 pairs
of the 4 smallest. Same construction as phase1k; s = eps * N6^(1/6), t = N6 / X.
F is frozen from the RS-S016 k234 bin table (bin centres, linear interpolation in log10 t).

  register        write class list, frozen F, per-class predictions and Q1-Q4 (commit before data)
  run --x X       X in {640000, 1000000}; appends to the results JSON (no git operations)
  score           verbatim scoring
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import phase1k as k1  # noqa: E402
import phase1l  # noqa: E402

RESULT = k1.RESULTS / 'rs_s017_fresh_classes_2026-10-26.json'
SCALES = (640000, 1000000)
SEED = 17
SIGMA_EPS = 0.004  # RS-S016 section 5 power estimate: sigma_s ~ 0.004 * N6^(1/6)


def save(doc):
    temp = RESULT.with_suffix('.tmp')
    temp.write_text(json.dumps(doc, indent=2, allow_nan=False) + '\n')
    temp.replace(RESULT)


def fresh_primes():
    return [p for p in k1.smallest_primary_primes(90) if 79 <= k1.norm(p) <= 400]


def classes():
    fresh = fresh_primes()
    out = [{'kappa': [[list(pi), k]]} for pi in fresh for k in range(1, 6)]
    out += [{'kappa': [[list(fresh[i]), e1], [list(fresh[j]), e2]]}
            for i in range(4) for j in range(i + 1, 4) for e1 in range(1, 6) for e2 in range(1, 6)]
    for c in out:
        c['exponents'] = sorted(e for _, e in c['kappa'])
        c['N6'] = math.prod(k1.norm(pi) ** e for pi, e in c['kappa'])
    return out


def frozen_f():
    bins = json.loads(phase1l.RESULT.read_text())['analysis']['collapse_bins_t_eq_N6_over_X']['k234']
    return [(b['log10_t_lo'] + 0.25, b['mean_s']) for b in bins]


def predict(f, log_t):
    xs, ys = zip(*f, strict=True)
    if not xs[0] <= log_t <= xs[-1]:
        return None
    return float(np.interp(log_t, xs, ys))


def register():
    doc = {'session': 'RS-S017', 'date': '2026-10-26', 'scales': list(SCALES), 'control_seed': SEED,
           'controls_per_X': {'random_phase': 10, 'conj_g6_random_sixth_roots': 10}, 'runs': []}
    f = frozen_f()
    rows = []
    for c in classes():
        sigma = SIGMA_EPS * c['N6'] ** (1 / 6)
        pred = {}
        for x in SCALES:
            lt = math.log10(c['N6'] / x)
            pred[str(x)] = {'log10_t': lt, 'F': None if 5 in c['exponents'] else predict(f, lt)}
        rows.append(c | {'sigma_s': sigma, 'powered': sigma <= 0.05, 'predictions': pred})
    doc.update(
        frozen_F={'source': 'results/rs_s016_x_dependence_2026-10-26.json analysis.collapse_bins_t_eq_N6_over_X.k234',
                  'points_log10t_centre_mean_s': f, 'interpolation': 'linear in log10 t; none outside the table'},
        classes=rows,
        predictions=[
            {'id': 'RS-S017-Q1', 'text': 'every fresh no-5 class with t <= 1e-2 (powered: sigma_s <= 0.05) has '
                                         's in [0.70, 1.00], at each X'},
            {'id': 'RS-S017-Q2', 'text': 'for every half-decade bin of log10 t (bins as in frozen F, pooled over '
                                         'both X) with >= 4 powered fresh no-5 classes, |mean s - mean F| <= 0.12'},
            {'id': 'RS-S017-Q3', 'text': 'every fresh class containing a 5 has r < 1 (each X), and the fresh pi^5 '
                                         'singles with t >= 3 have mean s in [-1.25, -0.85] (each X)'},
            {'id': 'RS-S017-Q4', 'text': 'at least 80% of powered fresh no-5 classes with 10^-1.5 <= t(1e6) <= 10 '
                                         'have s(1e6) > s(6.4e5)'},
        ],
        decision_rule=('Failure of Q1, Q2 or Q4 refutes (A") as stated; failure of Q3 refutes (B"). If Q1-Q4 all '
                       'PASS, draft (do not freeze) a replacement candidate for collision-audit with CAND-001 '
                       'statement 2. Otherwise record the smallest failing class and begin the owner-agreed '
                       'fallback (prior-art audit of statement 2 plus law (B)).'),
        scale_note='X = 1.28e6 (D = 98512, 9.7 GB matrix) skipped: 6.2 GB free RAM on this machine at registration.',
        prediction_commit=None)
    save(doc)
    no5 = [r for r in rows if 5 not in r['exponents']]
    print(len(rows), 'classes;', len(no5), 'without 5;', sum(r['powered'] for r in no5), 'powered')


def run(x):
    doc = json.loads(RESULT.read_text())
    assert doc['prediction_commit']
    k1.legacy.compile_engine()
    started = time.monotonic()
    row = {'X': x, 'command': 'python ' + ' '.join(sys.argv), 'platform': sys.platform,
           'code_commit': k1.legacy.shell('git', 'rev-parse', 'HEAD'), 'started_at': datetime.now(UTC).isoformat()}
    a, g = k1.build(x)
    base = g.conj()
    row.update(D=a.d, matrix_sha256=k1.digest(a.path), r_u1=k1.rayleigh(a, base))
    z6 = np.exp(1j * np.pi / 3 * np.arange(6))
    symbols, out = {}, []
    for c in doc['classes']:
        total, zero = np.zeros(a.d, np.int64), np.zeros(a.d, bool)
        for pi, e in c['kappa']:
            if tuple(pi) not in symbols:
                symbols[tuple(pi)] = k1.exponent_vector(a.meta, pi)
            v = symbols[tuple(pi)]
            zero |= v < 0
            total += e * v.astype(np.int64)
        out.append({'kappa': c['kappa'], 'r': k1.rayleigh(a, np.where(zero, 0, base * z6[total % 6]))})
    rng = np.random.default_rng(SEED)
    row.update(classes=out, control_seed=SEED,
               random_phase_r=[k1.rayleigh(a, np.exp(2j * np.pi * rng.random(a.d))) for _ in range(10)],
               conj_g6_random_roots_r=[k1.rayleigh(a, base * z6[rng.integers(0, 6, a.d)]) for _ in range(10)],
               seconds=time.monotonic() - started)
    del a
    k1.release(k1.DATA / f'sextic_{x}.bin', k1.DATA / f'sexticg_{x}.bin')
    doc['runs'] = sorted([r for r in doc['runs'] if r['X'] != x] + [row], key=lambda r: r['X'])
    save(doc)
    print(json.dumps({k: row[k] for k in ('X', 'D', 'r_u1', 'seconds')}))


def score():
    doc = json.loads(RESULT.read_text())
    meta = {json.dumps(c['kappa']): c for c in doc['classes']}
    obs = {}
    for run_ in doc['runs']:
        x, r1 = run_['X'], run_['r_u1']
        for c in run_['classes']:
            m = meta[json.dumps(c['kappa'])]
            eps = (c['r'] ** 2 - 1) / (r1 ** 2 - 1)
            p = m['predictions'][str(x)]
            obs.setdefault(json.dumps(c['kappa']), {})[x] = {
                'r': c['r'], 's': eps * m['N6'] ** (1 / 6), 'log10_t': p['log10_t'], 'F': p['F']}
    no5 = [k for k, m in meta.items() if 5 not in m['exponents']]
    powered = [k for k in no5 if meta[k]['powered']]
    out = {}
    # Q1
    q1 = [(k, x, obs[k][x]) for k in powered for x in SCALES if obs[k][x]['log10_t'] <= -2]
    q1_fail = [(k, x, v['s']) for k, x, v in q1 if not 0.70 <= v['s'] <= 1.00]
    out['Q1'] = {'n': len(q1), 'min_s': min(v['s'] for _, _, v in q1), 'max_s': max(v['s'] for _, _, v in q1),
                 'failures': q1_fail, 'pass': not q1_fail and len(q1) > 0}
    # Q2
    bins = {}
    for k in powered:
        for x in SCALES:
            v = obs[k][x]
            if v['F'] is not None:
                lo = math.floor(v['log10_t'] * 2) / 2
                bins.setdefault(lo, []).append(v)
    q2 = []
    for lo, vs in sorted(bins.items()):
        if len(vs) >= 4:
            ms, mf = float(np.mean([v['s'] for v in vs])), float(np.mean([v['F'] for v in vs]))
            q2.append({'log10_t_lo': lo, 'n': len(vs), 'mean_s': ms, 'mean_F': mf, 'diff': ms - mf,
                       'ok': abs(ms - mf) <= 0.12})
    out['Q2'] = {'bins': q2, 'pass': bool(q2) and all(b['ok'] for b in q2)}
    # Q3
    has5 = [k for k, m in meta.items() if 5 in m['exponents']]
    r_fail = [(k, x, obs[k][x]['r']) for k in has5 for x in SCALES if obs[k][x]['r'] >= 1]
    single5 = [k for k in has5 if meta[k]['exponents'] == [5]]
    means = {str(x): float(np.mean([obs[k][x]['s'] for k in single5 if obs[k][x]['log10_t'] >= math.log10(3)]))
             for x in SCALES}
    out['Q3'] = {'n_with_5': len(has5), 'max_r': max(obs[k][x]['r'] for k in has5 for x in SCALES),
                 'r_failures': r_fail, 'mean_s_pi5_t_ge_3': means,
                 'pass': not r_fail and all(-1.25 <= m <= -0.85 for m in means.values())}
    # Q4
    q4 = [k for k in powered if -1.5 <= obs[k][1000000]['log10_t'] <= 1]
    up = [k for k in q4 if obs[k][1000000]['s'] > obs[k][640000]['s']]
    out['Q4'] = {'n': len(q4), 'n_increasing': len(up), 'fraction': len(up) / len(q4) if q4 else None,
                 'pass': bool(q4) and len(up) >= 0.8 * len(q4)}
    out['controls'] = {str(r['X']): {'random_phase_max': max(r['random_phase_r']),
                                     'random_phase_sd': float(np.std(r['random_phase_r'])),
                                     'conj_g6_roots_max': max(r['conj_g6_random_roots_r'])} for r in doc['runs']}
    out['all_pass'] = all(out[q]['pass'] for q in ('Q1', 'Q2', 'Q3', 'Q4'))
    doc['score'], doc['observed'] = out, obs
    save(doc)
    print(json.dumps({q: {k: v for k, v in out[q].items() if k not in ('failures', 'r_failures')}
                      for q in ('Q1', 'Q2', 'Q3', 'Q4', 'controls')} | {'all_pass': out['all_pass']}, indent=1))


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('step', choices=['register', 'run', 'score'])
    parser.add_argument('--x', type=int, choices=SCALES)
    args = parser.parse_args()
    if args.step == 'run':
        run(args.x)
    else:
        {'register': register, 'score': score}[args.step]()


if __name__ == '__main__':
    main()
