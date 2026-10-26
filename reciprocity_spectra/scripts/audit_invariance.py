"""RS-S014: sixth-power-class audit of the sextic twist evidence (no new matrices).

Every stored sextic twist (u, sign) is mapped to its exact twist class: the exponent vector mod 6 of
(u/.)_6^sign over primary primes (arith.sextic_twist_class). This is legitimate because
(u v^6/rho)_6 = (u/rho)_6 away from rho | v, (u^5/rho)_6 = conj((u/rho)_6), and (-1/rho)_6 leaves r
unchanged (all exact). For single-prime classes pi^k the statistic is
eps * N(pi)^(k/6), eps = (r^2 - 1)/(r_1^2 - 1); the sixth-power-free-norm law predicts +1 for every k.
Writes (or with --check verifies) results/rs_s014_invariance_2026-10-26.json.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from reciprocity_spectra.arith import sextic_twist_class  # noqa: E402

SOURCES = [ROOT / 'reciprocity_spectra/results/phase1e_2026-10-25.json',
           ROOT / 'reciprocity_spectra/results/phase1j_2026-10-25.json']
RESULT = ROOT / 'reciprocity_spectra/results/rs_s014_invariance_2026-10-26.json'


def lf_sha256(path):
    return hashlib.sha256(path.read_bytes().replace(b'\r\n', b'\n')).hexdigest()


def stats(values):
    n = len(values)
    mean = sum(values) / n
    return {'n': n, 'mean': mean, 'sd': math.sqrt(sum((v - mean) ** 2 for v in values) / n),
            'min': min(values), 'max': max(values)}


def runs():
    phase1e = json.loads(SOURCES[0].read_text(encoding='utf-8'))
    phase1j = json.loads(SOURCES[1].read_text(encoding='utf-8'))
    out = []
    for run in phase1e['runs'] + phase1e['rayleigh_runs']:
        out.append(('phase1e', run['X'], run['norm_max'], [(t['u'], t['sign'], t['r']) for t in run['twists']]))
    for run in phase1j['runs']:
        if run['mode'] == 'sextic':
            out.append(('phase1j', run['X'], 100, [(t['u'], '+', t['r']) for t in run['twists']]))
    return sorted(out, key=lambda r: (r[1], r[0]))


def audit():
    rows = []
    for source, x, norm_max, twists in runs():
        r1 = next(r for u, s, r in twists if u == [1, 0] and s == '+')
        base = r1 * r1 - 1
        by_pattern, single = collections.defaultdict(list), collections.defaultdict(list)
        r_inverse_of_2 = None
        for u, sign, r in twists:
            c, d = u
            if d % 3 or (c + d) % 3 == 0:
                continue  # +-primary twists coprime to 3 only
            cls = sextic_twist_class(c, d, 1 if sign == '+' else -1)
            by_pattern[str(tuple(sorted(e for _, e in cls)))].append(r)
            if len(cls) == 1:
                (pi, k), = cls
                norm = pi[0] ** 2 - pi[0] * pi[1] + pi[1] ** 2
                single[str(k)].append((r * r - 1) / base * norm ** (k / 6))
            if u == [2, 0] and sign == '-':
                r_inverse_of_2 = r  # = r_32 exactly, since 32 = 2^5 and 2 divides no indexed prime
        rows.append({'source': source, 'X': x, 'norm_max': norm_max, 'r_1': r1,
                     'r_by_exponent_pattern': {k: stats(v) for k, v in sorted(by_pattern.items())},
                     'single_prime_scaled_excess': {k: stats(v) for k, v in sorted(single.items())},
                     'r_32_equals_conjugate_twist_of_2': r_inverse_of_2})
    return {'session': 'RS-S014', 'date': '2026-10-26', 'classification': 'AUDIT of stored evidence (no new matrices)',
            'definition': __doc__,
            'sources': [{'path': p.relative_to(ROOT).as_posix(), 'sha256_lf': lf_sha256(p)} for p in SOURCES],
            'runs': rows}


def compare(a, b, label):
    if isinstance(a, float):
        assert isinstance(b, (int, float)) and math.isclose(a, b, rel_tol=1e-12, abs_tol=1e-14), label
    elif isinstance(a, dict):
        assert isinstance(b, dict) and a.keys() == b.keys(), label
        for k in a:
            compare(a[k], b[k], f'{label}.{k}')
    elif isinstance(a, list):
        assert isinstance(b, list) and len(a) == len(b), label
        for i, (x, y) in enumerate(zip(a, b, strict=True)):
            compare(x, y, f'{label}[{i}]')
    else:
        assert a == b, label


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    doc = audit()
    if args.check:
        compare(doc, json.loads(RESULT.read_text(encoding='utf-8')), 'record')
        print('RS-S014 invariance audit record verified')
    else:
        RESULT.write_text(json.dumps(doc, indent=2) + '\n', encoding='utf-8')
    for row in doc['runs']:
        sp = row['single_prime_scaled_excess']
        print(row['source'], row['X'], 'r_32 =', row['r_32_equals_conjugate_twist_of_2'],
              {k: (v['n'], round(v['mean'], 3), round(v['sd'], 3)) for k, v in sp.items()})


if __name__ == '__main__':
    main()
