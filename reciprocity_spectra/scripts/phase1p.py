"""RS-S020: registered test of H- (pi^5 coefficient -> -1) on fresh primes, X = 10^6, prime moduli.

Classes: pi^5 for every primary prime (split or inert (q, 0)) with 400 < N(pi) <= 1000; none was used before.
Exploratory alongside (no prediction): pi^1 for the same primes. Rational normalization, as in RS-S015..17.
s = eps * N6^(1/6), eps = (r^2 - 1)/(r_1^2 - 1).

  register | run | score
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

RESULT = k1.RESULTS / 'rs_s020_h_minus_2026-10-26.json'
X = 1_000_000
SEED = 20


def save(doc):
    RESULT.write_text(json.dumps(doc, indent=2, allow_nan=False) + '\n')


def fresh():
    return [p for p in k1.smallest_primary_primes(400) if 400 < k1.norm(p) <= 1000]


def register():
    assert not RESULT.exists()
    primes = fresh()
    sd_r = 0.0016  # RS-S017 random-phase sd at X = 1e6
    sig = [2 * sd_r / (1.4342 ** 2 - 1) * k1.norm(p) ** (5 / 6) for p in primes]
    se = math.sqrt(sum(v * v for v in sig)) / len(primes)
    doc = {'session': 'RS-S020', 'date': '2026-10-26', 'X': X, 'control_seed': SEED,
           'primes': [list(p) for p in primes], 'n_classes': len(primes),
           'predictions': [{'id': 'RS-S020-H-', 'text': (
               'mean s over the fresh pi^5 singles (400 < N <= 1000, all t >> 1) lies in [-1.15, -0.85] (about +-2 SE)')}],
           'power': {'per_class_sigma_s_range': [min(sig), max(sig)], 'se_of_mean': se,
                     'basis': 'sigma_eps = 2 sd_r / (r_1^2 - 1), sd_r = 0.0016 (RS-S017, X = 1e6)'},
           'exploratory': 'pi^1 singles of the same primes (no prediction)',
           'H_plus_design': ('H+: F(0+) = 1 needs t <= 1e-6, i.e. X >= 4e6 for N = 4 classes; not feasible on the '
                             'local machine (matrix > 9.7 GB at X = 1.28e6). Deferred to a large-RAM or cloud session '
                             '(owner decision on compute).'),
           'prediction_commit': None, 'runs': []}
    save(doc)
    print(len(primes), 'classes; SE of mean', round(se, 3))


def run():
    doc = json.loads(RESULT.read_text())
    assert doc['prediction_commit']
    k1.legacy.compile_engine()
    started = time.monotonic()
    a, g = k1.build(X)
    base = g.conj()
    row = {'X': X, 'D': a.d, 'matrix_sha256': k1.digest(a.path), 'r_u1': k1.rayleigh(a, base),
           'command': 'python ' + ' '.join(sys.argv), 'platform': sys.platform,
           'code_commit': k1.legacy.shell('git', 'rev-parse', 'HEAD'), 'started_at': datetime.now(UTC).isoformat()}
    z6 = np.exp(1j * np.pi / 3 * np.arange(6))
    cls = []
    for p in doc['primes']:
        v = k1.exponent_vector(a.meta, p)
        for k in (5, 1):
            w = np.where(v < 0, 0, base * z6[(k * v.astype(np.int64)) % 6])
            r = k1.rayleigh(a, w)
            n = k1.norm(p)
            eps = (r ** 2 - 1) / (row['r_u1'] ** 2 - 1)
            cls.append({'pi': p, 'N': n, 'k': k, 'r': r, 's': eps * n ** (k / 6), 't': n ** k / X})
    rng = np.random.default_rng(SEED)
    row.update(classes=cls, random_phase_r=[k1.rayleigh(a, np.exp(2j * np.pi * rng.random(a.d))) for _ in range(10)],
               seconds=time.monotonic() - started)
    del a
    k1.release(k1.DATA / f'sextic_{X}.bin', k1.DATA / f'sexticg_{X}.bin')
    doc['runs'].append(row)
    save(doc)
    print(json.dumps({k: row[k] for k in ('D', 'r_u1', 'seconds')}))


def score():
    doc = json.loads(RESULT.read_text())
    row = doc['runs'][-1]
    p5 = [c for c in row['classes'] if c['k'] == 5]
    s = np.array([c['s'] for c in p5])
    n = np.array([c['N'] for c in p5], float)
    b, c5 = np.polyfit(1 / n, s, 1)
    mean = float(s.mean())
    k1s = [c['s'] for c in row['classes'] if c['k'] == 1]
    doc['score'] = {'n': len(p5), 'mean_s': mean, 'se': float(s.std() / math.sqrt(len(s))), 'fit_c5': float(c5),
                    'fit_b': float(b), 'max_r_pi5': max(c['r'] for c in p5),
                    'random_phase_max': max(row['random_phase_r']),
                    'random_phase_sd': float(np.std(row['random_phase_r'])),
                    'outcome': 'PASS' if -1.15 <= mean <= -0.85 else 'FAIL',
                    'exploratory_k1_mean_s': float(np.mean(k1s)), 'exploratory_k1_n': len(k1s)}
    save(doc)
    print(json.dumps(doc['score'], indent=1))


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('step', choices=['register', 'run', 'score'])
    {'register': register, 'run': run, 'score': score}[parser.parse_args().step]()


if __name__ == '__main__':
    main()
