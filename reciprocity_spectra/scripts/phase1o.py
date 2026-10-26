"""RS-S020 (EXPLORATORY): the reviewer's rho-partition test of the tau_6(pi^2) vanishing condition.

For single-prime classes kappa = pi^k (prime moduli; rational and trace normalization), split the rows rho by
the residue exponent j = (rho/pi)_6 and compute, within each part,
  s_j = (mean_{rho in part j} |(A w)_rho|^2 / ||w||^2 - 1) / (r_1^2 - 1) * N6^(1/6),
with r_1 the kappa = 1 ratio of the same setting (so the row-average of s_j is the usual s).
Broker-Hoffstein Lemma 5.3: for N(pi) = 1 mod 12, tau_6(pi^2) != 0 forces (pi/pibar)_6 = 1. The question is
whether the k = 2 excess concentrates in particular parts j differently for (pi/pibar)_6 = 1 and != 1.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import phase1k as k1  # noqa: E402
import phase1n as k2  # noqa: E402

from reciprocity_spectra.arith import (  # noqa: E402
    DegreeOnePrime,
    conjugate_prime,
    sextic_residue_exponent,
)

RESULT = k1.RESULTS / 'rs_s020_rho_partition_2026-10-26.json'


def norm(p):
    return p[0] ** 2 - p[0] * p[1] + p[1] ** 2


def run(x, nmax):
    st = k2.Setting(x)
    index = {(int(a), int(b)): i for i, (_, a, b) in enumerate(st.meta.tolist())}
    primes = [(a, b) for (a, b), i in index.items() if norm((a, b)) <= nmax]
    kappas = [[[list(p), k]] for p in sorted(primes, key=norm) for k in (1, 2, 4)]
    moduli = [(i,) for i in range(st.d)]
    out = {'X': x, 'D': st.d, 'nmax': nmax, 'classification': 'EXPLORATORY', 'platform': sys.platform,
           'code_commit': k1.legacy.shell('git', 'rev-parse', 'HEAD'),
           'started_at': datetime.now(UTC).isoformat(), 'settings': {}}
    for mode in ('rational', 'trace'):
        ec, g = st.columns(moduli, mode)
        w = k2.vectors(st, moduli, g, [[]] + kappas, 0)
        y = k2.apply(ec, w)
        wn2 = np.linalg.norm(w, axis=0) ** 2
        r1sq = float(np.sum(np.abs(y[:, 0]) ** 2) / (wn2[0] * st.d))
        rows = []
        for v, kappa in enumerate(kappas, start=1):
            (pi, k), = kappa
            n = norm(pi)
            part = st.et[index[tuple(pi)]]  # (rho/pi)_6 for every row rho; 255 at rho = pi
            prime = DegreeOnePrime(3, n, *pi)
            conj_exp = sextic_residue_exponent(*pi, conjugate_prime(prime))
            rel = np.abs(y[:, v]) ** 2 / wn2[v]
            sj = {}
            for j in range(6):
                m = part == j
                sj[str(j)] = float((rel[m].mean() - 1) / (r1sq - 1) * n ** (k / 6))
            s_all = float((rel[part != 255].mean() - 1) / (r1sq - 1) * n ** (k / 6))
            rows.append({'kappa': kappa, 'N': n, 'k': k, 'N_mod_12': n % 12, 'pi_over_pibar_exp': conj_exp,
                         's': s_all, 's_by_part': sj})
        out['settings'][mode] = {'r_u1': r1sq ** 0.5, 'classes': rows}
        del ec
    del st
    k1.release(k1.DATA / f'sextic_{x}.bin', k1.DATA / f'sexticg_{x}.bin')
    RESULT.write_text(json.dumps(out, indent=2) + '\n')
    summarize(out)


def summarize(out):
    for mode, d in out['settings'].items():
        print(mode, 'r1 =', round(d['r_u1'], 4))
        for k in (1, 2, 4):
            for label, sel in (('N=1(12), (pi/pibar)=1', lambda c: c['N_mod_12'] == 1 and c['pi_over_pibar_exp'] == 0),
                               ('N=1(12), (pi/pibar)!=1', lambda c: c['N_mod_12'] == 1 and c['pi_over_pibar_exp'] != 0),
                               ('N=7(12)', lambda c: c['N_mod_12'] == 7)):
                cs = [c for c in d['classes'] if c['k'] == k and sel(c)]
                if cs:
                    prof = np.array([[c['s_by_part'][str(j)] for j in range(6)] for c in cs])
                    print(f'  k={k} {label:24s} n={len(cs):2d} s={np.mean([c["s"] for c in cs]):.3f} '
                          f'by part j=0..5: ' + ' '.join(f'{v:+.2f}' for v in prof.mean(axis=0)))


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--x', type=int, default=320000)
    parser.add_argument('--nmax', type=int, default=200)
    args = parser.parse_args()
    k1.legacy.compile_engine()
    run(args.x, args.nmax)


if __name__ == '__main__':
    main()
