"""RS-S018: stored-data consistency check of the theta-coefficient reading of the class excess.

Broker-Hoffstein (arXiv 1312.0568, Lemma 5.3): for |pi| = 1 mod 12, tau_6(pi^2) != 0 forces
(pi/pibar)_6 = 1. If the matrix excess were s = |tau_6(u)/tau_6(1)|^2 (suitably normalized), k = 2
classes with N = 1 mod 12 and (pi/pibar)_6 != 1 would show no enhancement at small t = N6/X.
Uses stored single-prime classes from RS-S015/16/17 (split primes only), t < 1e-2.
"""
from __future__ import annotations

import json
import statistics as st
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from reciprocity_spectra.arith import (  # noqa: E402
    DegreeOnePrime,
    conjugate_prime,
    sextic_residue_exponent,
)

RESULTS = ROOT / 'reciprocity_spectra/results'
RESULT = RESULTS / 'rs_s018_collision_checks_2026-10-26.json'
SOURCES = ['rs_s015_class_tests_2026-10-26.json', 'rs_s016_x_dependence_2026-10-26.json',
           'rs_s017_fresh_classes_2026-10-26.json']


def points():
    out = []
    for name in SOURCES:
        runs = json.loads((RESULTS / name).read_text())['runs']
        if name.startswith('rs_s015'):
            runs = [dict(runs[0], X=1000000)]
        for run in runs:
            r1 = run['r_u1']
            for c in run['classes']:
                if len(c['kappa']) != 1:
                    continue
                (pi, e), = c['kappa']
                a, b = pi
                n = a * a - a * b + b * b
                if b == 0 or n ** e / run['X'] >= 1e-2:
                    continue
                eps = (c['r'] ** 2 - 1) / (r1 ** 2 - 1)
                prime = DegreeOnePrime(3, n, a, b)
                k = sextic_residue_exponent(a, b, conjugate_prime(prime))
                out.append({'k': e, 'N': n, 'X': run['X'], 'N_mod_12': n % 12, 'pi_over_pibar_exp': k,
                            's': eps * n ** (e / 6), 'source': name})
    return out


def main():
    pts = points()
    groups = {}
    for p in pts:
        key = f"k={p['k']} N%12={p['N_mod_12']} pi_over_pibar_trivial={p['pi_over_pibar_exp'] == 0}"
        groups.setdefault(key, []).append(p['s'])
    summary = {k: {'n': len(v), 'mean_s': st.mean(v), 'sd_s': st.pstdev(v)} for k, v in sorted(groups.items())}
    doc = {'session': 'RS-S018', 'date': datetime.now(UTC).date().isoformat(), 'stage': 'collision-audit',
           'check': __doc__.strip(), 'sources': SOURCES, 'groups': summary, 'points': pts}
    RESULT.write_text(json.dumps(doc, indent=2) + '\n')
    print(json.dumps(summary, indent=1))


if __name__ == '__main__':
    main()
