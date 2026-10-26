"""RS-S019: twist-class excess with prime versus unrestricted (squarefree) moduli.

Rows are the primary degree-one primes rho with N(rho) <= X (as in R_6). Columns are moduli c:
  prime:        the split primes sigma with N(sigma) <= X (the RS-S015..17 object);
  unrestricted: every squarefree c = product of distinct primary primes coprime to 6 (split, or inert q),
                N(c) <= X.
Entry (rho/c)_6 = prod_{p | c} (rho/p)_6. Column weight conj(G(c)) (kappa/c)_6 (zeta6^j/c)_6, where
  trace normalization: G(c) = g(1,c)/sqrt(N c), g(1,c) = sum_{x mod c} (x/c)_6 e(Tr(x/c)), assembled by
                       twisted multiplicativity from prime values (arith.twisted_gauss_product; tested);
  rational (prime columns only, for validation): G(sigma) = engine g~6(sigma) (e(t/p) form).
r = ||A w|| / (||w|| sqrt(D)); eps = (r^2 - 1)/(r_1^2 - 1) with r_1 the kappa = 1 vector of the same setting;
s = eps * N6(kappa)^(1/6); t = N6/X.

  validate --x 160000     rational/prime mode reproduces stored RS-S016 r values
  explore --x X           unit twist j = 0..5 for kappa = 1, trace mode, prime and unrestricted (EXPLORATORY)
  run --x X               registered run (all classes, both column sets, controls)
  score                   verbatim scoring
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

from reciprocity_spectra.arith import (  # noqa: E402
    DegreeOnePrime,
    inert_sextic_exponent,
    kubota_g6_prime,
    primes_upto,
    sextic_residue_exponent,
)

RESULT = k1.RESULTS / 'rs_s019_moduli_2026-10-26.json'
Z6 = np.exp(1j * np.pi / 3 * np.arange(6))
SEED = 19


def save(doc):
    temp = RESULT.with_suffix('.tmp')
    temp.write_text(json.dumps(doc, indent=2, allow_nan=False) + '\n')
    temp.replace(RESULT)


def load():
    return json.loads(RESULT.read_text()) if RESULT.exists() else {'session': 'RS-S019', 'runs': []}


class Setting:
    """Rows, primes (split indices 0..D-1, then inert), moduli and all exponent tables at one X."""

    def __init__(self, x):
        self.x = x
        self.a, g_rat = k1.build(x)
        a = self.a
        self.d = a.d
        self.meta = a.meta
        self.et = np.ascontiguousarray(np.asarray(a.e).T)  # et[sigma, rho] = (rho/sigma)_6, 255 on diagonal
        self.g_rat = g_rat
        self.split = [DegreeOnePrime(3, p, a_, b) for p, a_, b in self.meta.tolist()]
        self.inert = [q for q in primes_upto(math.isqrt(x)) if q % 3 == 2 and q > 2]
        rows = self.meta[:, 1:]
        # (rho/q)_6 for inert q, as extra "prime columns" of exponents (rows rho)
        self.e_inert = np.array([[inert_sextic_exponent(int(r0), int(r1), q) for r0, r1 in rows]
                                 for q in self.inert], dtype=np.uint8)
        # trace-normalized prime Gauss sums, unimodular
        tr_fix = np.array([sextic_residue_exponent(2 * s.a - s.b, 0, s) for s in self.split])
        self.g_tr_split = g_rat * np.exp(-2j * np.pi * tr_fix / 6)
        self.g_tr_inert = np.array([kubota_g6_prime((1, 0), q) / q for q in self.inert])
        # (q/sigma)_6 and (q1/q2)_6 for twisted multiplicativity
        self.q_at_split = np.array([[sextic_residue_exponent(q, 0, s) for s in self.split] for q in self.inert],
                                   dtype=np.int64)
        self.q_at_q = np.array([[inert_sextic_exponent(q1, 0, q2) if q1 != q2 else 0 for q2 in self.inert]
                                for q1 in self.inert], dtype=np.int64)
        self.norms = np.concatenate([self.meta[:, 0], np.array(self.inert, dtype=np.int64) ** 2])
        self.moduli = self.enumerate_moduli()

    def enumerate_moduli(self):
        """Squarefree moduli as tuples of prime indices (split i < D, inert D + k), N(c) <= X, sorted."""
        order = np.argsort(self.norms, kind='stable')
        norms = self.norms[order]
        out = []

        def grow(start, prod, idx):
            for pos in range(start, len(order)):
                n = prod * int(norms[pos])
                if n > self.x:
                    break
                cur = idx + (int(order[pos]),)
                out.append(cur)
                grow(pos + 1, n, cur)

        grow(0, 1, ())
        return out

    def exponent(self, prime_index, rows=None):
        """Row exponent vector (rho/p)_6 for a prime column index (255 where rho = p)."""
        if prime_index < self.d:
            return self.et[prime_index]
        return self.e_inert[prime_index - self.d]

    def pair_exponent(self, i, j):
        """(p_i/p_j)_6 + (p_j/p_i)_6 for distinct prime indices."""
        d = self.d
        if i < d and j < d:
            return int(self.et[j, i]) + int(self.et[i, j])  # et[j, i] = (pi_i / pi_j)
        if i >= d and j >= d:
            return int(self.q_at_q[i - d, j - d] + self.q_at_q[j - d, i - d])
        s, q = (i, j - d) if j >= d else (j, i - d)
        return int(self.e_inert[q, s]) + int(self.q_at_split[q, s])  # (sigma/q) + (q/sigma)

    def columns(self, moduli, mode):
        """Exponent matrix (len(moduli) x D, uint8, 255 = zero) and unimodular weights G(c)."""
        ec = np.empty((len(moduli), self.d), np.uint8)
        g = np.empty(len(moduli), complex)
        for n, c in enumerate(moduli):
            acc = np.zeros(self.d, np.int16)
            zero = np.zeros(self.d, bool)
            w = complex(1)
            for i in c:
                v = self.exponent(i)
                zero |= v == 255
                acc += v
                if mode == 'rational':
                    w *= self.g_rat[i]
                else:
                    w *= self.g_tr_split[i] if i < self.d else self.g_tr_inert[i - self.d]
            for a_, i in enumerate(c):
                for j in c[a_ + 1:]:
                    w *= Z6[self.pair_exponent(i, j) % 6]
            col = (acc % 6).astype(np.uint8)
            col[zero] = 255
            ec[n] = col
            g[n] = w
        return ec, g

    def class_exponents(self, kappa, moduli):
        """(kappa/c)_6 exponents per modulus; -1 where gcd(kappa, c) > 1 (vectorized over moduli)."""
        n = self.d + len(self.inert)
        per = np.array([self.prime_class_exponent(kappa, i) for i in range(n)], dtype=object)
        per = np.array([-10**6 if v is None else v for v in per] + [0], dtype=np.int64)  # last = padding
        width = max(len(c) for c in moduli)
        idx = np.full((len(moduli), width), n, dtype=np.int64)
        for r, c in enumerate(moduli):
            idx[r, :len(c)] = c
        tot = per[idx].sum(axis=1)
        return np.where(tot < 0, -1, tot % 6)

    def prime_class_exponent(self, kappa, i):
        tot = 0
        for (a_, b), e in kappa:
            if i < self.d:
                k = sextic_residue_exponent(a_, b, self.split[i])
            else:
                k = inert_sextic_exponent(a_, b, self.inert[i - self.d])
            if k is None:
                return None
            tot += e * k
        return tot % 6


def apply(ec, w):
    """Y = A W with A[rho, c] = zeta6^ec[c, rho] (0 where 255); W is (M x V)."""
    roots = np.zeros(256, complex)
    roots[:6] = Z6
    y = np.zeros((ec.shape[1], w.shape[1]), complex)
    for start in range(0, ec.shape[0], 800):
        y += roots[ec[start:start + 800]].T @ w[start:start + 800]
    return y


def ratios(ec, w):
    y = apply(ec, w)
    return np.linalg.norm(y, axis=0) / (np.linalg.norm(w, axis=0) * math.sqrt(ec.shape[1]))


def vectors(st, moduli, g, kappas, unit_j):
    unit = st.class_exponents([((1, 1), unit_j)], moduli) if unit_j else np.zeros(len(moduli), np.int64)
    cols = []
    for kappa in kappas:
        e = st.class_exponents(kappa, moduli) if kappa else np.zeros(len(moduli), np.int64)
        cols.append(np.where(e < 0, 0, np.conj(g) * Z6[(e + unit) % 6]))
    return np.array(cols).T


def singles():
    return [c['kappa'] for c in k1.classes() if c['part'] == 'singles']


def validate(x):
    st = Setting(x)
    prime_moduli = [(i,) for i in range(st.d)]
    ec, g = st.columns(prime_moduli, 'rational')
    stored = next(r for r in phase1l.load()['runs'] if r['X'] == x)
    kappas = [[]] + [c['kappa'] for c in stored['classes']]
    r = ratios(ec, vectors(st, prime_moduli, g, kappas, 0))
    ref = np.array([stored['r_u1']] + [c['r'] for c in stored['classes']])
    doc = load()
    doc['validation'] = {'X': x, 'n': len(ref), 'max_relative_r_difference': float(np.max(np.abs(r - ref) / ref)),
                         'pass': bool(np.max(np.abs(r - ref) / ref) < 1e-8), 'platform': sys.platform}
    save(doc)
    print(doc['validation'])


def explore(x):
    st = Setting(x)
    out = {'X': x, 'D': st.d, 'n_unrestricted_moduli': len(st.moduli), 'classification': 'EXPLORATORY'}
    for name, moduli in (('prime', [(i,) for i in range(st.d)]), ('unrestricted', st.moduli)):
        ec, g = st.columns(moduli, 'trace')
        w = np.concatenate([vectors(st, moduli, g, [[]], j) for j in range(6)], axis=1)
        out[name] = {f'j={j}': float(v) for j, v in enumerate(ratios(ec, w))}
    doc = load()
    doc.setdefault('explore', []).append(out)
    save(doc)
    print(json.dumps(out, indent=1))


X_RUN = 200000
UNIT_J = 0


def norm(pi):
    return pi[0] ** 2 - pi[0] * pi[1] + pi[1] ** 2


def register():
    doc = load()
    assert 'predictions' not in doc and doc['validation']['pass']
    doc.update(
        date='2026-10-26', X=X_RUN, unit_j=UNIT_J, control_seed=SEED,
        unit_j_basis='EXPLORATORY scan at X = 50000 (explore): trace/prime r is maximal for j in {0, 3}',
        classes='RS-S015 singles: pi^k, k = 1..5, over the 20 smallest primary primes (k1.classes singles)',
        settings={'prime': 'columns = split primes sigma, N <= X, trace-normalized G',
                  'unrestricted': 'columns = all squarefree primary c coprime to 6 (split and inert factors), '
                                  'N(c) <= X, trace-normalized G by twisted multiplicativity'},
        statistic='s = eps * N6^(1/6), eps = (r^2 - 1)/(r_1^2 - 1), r_1 = kappa = 1 vector in the same setting',
        predictions=[
            {'id': 'RS-S019-P', 'text': (
                'B = mean s over pi^5 singles with t >= 3 (prime setting), U = same (unrestricted). If B > -0.6: '
                'BASELINE_ABSENT. Else SIEVE_SUPPORTED if U - B >= 0.5 or U > 0; INTRINSIC if |U - B| <= 0.25; '
                'otherwise UNDECIDED. The reviewer-suggested sieve hypothesis predicts SIEVE_SUPPORTED.')},
            {'id': 'RS-S019-Q', 'text': (
                'In each setting, plateau Pl = mean s over k in {1..4} singles with t <= 1e-2, crossover C = mean s '
                'over k in {1..4} singles with 10^-0.5 <= t <= 10^0.5. PROFILE_PRESENT iff Pl in [0.5, 1.3] and '
                'C <= Pl - 0.3. Predicted: PRESENT in both settings (crossover is a shift-aspect property of the '
                'Gauss-sum first moment); ABSENT in the unrestricted setting would make it prime-specific.')},
        ],
        power_note=('Class counts at X = 2e5: P uses 15 pi^5 singles (N = 19..73); Q plateau 38 classes, crossover '
                    '11 classes (k = 3, N = 43..73; k = 4, N = 19, 25). Random-phase sd of r about 0.003 at D ~ 1.8e4, '
                    'so sigma_eps ~ 0.007 and sigma_s(pi^5) ~ 0.08-0.25 per class; SE of B, U about 0.05.'),
        prediction_commit=None)
    save(doc)
    print('registered')


def run(x):
    doc = load()
    assert doc.get('prediction_commit')
    started = time.monotonic()
    st = Setting(x)
    kappas = [[]] + singles()
    row = {'X': x, 'D': st.d, 'n_unrestricted_moduli': len(st.moduli), 'command': 'python ' + ' '.join(sys.argv),
           'code_commit': k1.legacy.shell('git', 'rev-parse', 'HEAD'), 'platform': sys.platform,
           'started_at': datetime.now(UTC).isoformat(), 'unit_j': UNIT_J}
    rng = np.random.default_rng(SEED)
    for name, moduli in (('prime', [(i,) for i in range(st.d)]), ('unrestricted', st.moduli)):
        ec, g = st.columns(moduli, 'trace')
        r = ratios(ec, vectors(st, moduli, g, kappas, UNIT_J))
        m = len(moduli)
        controls = np.concatenate([np.exp(2j * np.pi * rng.random((m, 10))),
                                   np.conj(g)[:, None] * Z6[rng.integers(0, 6, (m, 10))]], axis=1)
        rc = ratios(ec, controls)
        r1 = float(r[0])
        cls = []
        for kappa, rk in zip(kappas[1:], r[1:], strict=True):
            (pi, e), = kappa
            n6 = norm(pi) ** e
            eps = (rk ** 2 - 1) / (r1 ** 2 - 1)
            cls.append({'kappa': kappa, 'N': norm(pi), 'k': e, 'N6': n6, 'r': float(rk),
                        's': float(eps * n6 ** (1 / 6)), 't': n6 / x})
        row[name] = {'n_moduli': m, 'r_u1': r1, 'classes': cls, 'random_phase_r': rc[:10].tolist(),
                     'conj_G_random_roots_r': rc[10:].tolist()}
        del ec
    row['seconds'] = time.monotonic() - started
    del st
    k1.release(k1.DATA / f'sextic_{x}.bin', k1.DATA / f'sexticg_{x}.bin')
    doc['runs'] = [r_ for r_ in doc['runs'] if r_['X'] != x] + [row]
    save(doc)
    print(json.dumps({k: row[k] for k in ('X', 'D', 'n_unrestricted_moduli', 'seconds')} |
                     {n: row[n]['r_u1'] for n in ('prime', 'unrestricted')}))


def score():
    doc = load()
    row = next(r for r in doc['runs'] if r['X'] == doc['X'])
    out = {}
    for name in ('prime', 'unrestricted'):
        cls = row[name]['classes']
        p5 = [c['s'] for c in cls if c['k'] == 5 and c['t'] >= 3]
        plateau = [c['s'] for c in cls if c['k'] <= 4 and c['t'] <= 1e-2]
        cross = [c['s'] for c in cls if c['k'] <= 4 and 10 ** -0.5 <= c['t'] <= 10 ** 0.5]
        pl, cr = float(np.mean(plateau)), float(np.mean(cross))
        out[name] = {'r_u1': row[name]['r_u1'], 'pi5_mean_s': float(np.mean(p5)), 'pi5_n': len(p5),
                     'pi5_sd_s': float(np.std(p5)), 'plateau_mean_s': pl, 'plateau_n': len(plateau),
                     'crossover_mean_s': cr, 'crossover_n': len(cross),
                     'profile_present': bool(0.5 <= pl <= 1.3 and cr <= pl - 0.3),
                     'random_phase_max': max(row[name]['random_phase_r']),
                     'random_phase_sd': float(np.std(row[name]['random_phase_r'])),
                     'conj_G_roots_max': max(row[name]['conj_G_random_roots_r'])}
    b, u = out['prime']['pi5_mean_s'], out['unrestricted']['pi5_mean_s']
    if b > -0.6:
        p = 'BASELINE_ABSENT'
    elif u - b >= 0.5 or u > 0:
        p = 'SIEVE_SUPPORTED'
    elif abs(u - b) <= 0.25:
        p = 'INTRINSIC'
    else:
        p = 'UNDECIDED'
    out['P'] = {'B': b, 'U': u, 'U_minus_B': u - b, 'outcome': p}
    q = {n: 'PROFILE_PRESENT' if out[n]['profile_present'] else 'PROFILE_ABSENT' for n in ('prime', 'unrestricted')}
    out['Q'] = q | {'prediction_met': q['prime'] == q['unrestricted'] == 'PROFILE_PRESENT'}
    doc['score'] = out
    save(doc)
    print(json.dumps(out, indent=1))


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('step', choices=['validate', 'explore', 'register', 'run', 'score', 'fits'])
    parser.add_argument('--x', type=int)
    args = parser.parse_args()
    k1.legacy.compile_engine()
    if args.step in ('register', 'score', 'fits'):
        {'register': register, 'score': score, 'fits': exploratory_fits}[args.step]()
    else:
        {'validate': validate, 'explore': explore, 'run': run}[args.step](args.x)



def exploratory_fits():
    """EXPLORATORY (RS-S019 item 4): 1/log X fit of the plateau, and the pi^5 coefficient against N(pi).

    Uses stored rational-normalization prime-moduli runs: RS-S016 singles (X = 1.6e5..6.4e5), RS-S015 (1e6),
    RS-S017 fresh singles (6.4e5, 1e6).
    """
    tab = phase1l.table()  # {X: (r1, D, sd, [(N, k, r, s)])}, RS-S015/16 singles
    groups = {'k1_t<=1e-3.5': lambda n, k, x: k == 1 and n / x <= 10 ** -3.5,
              'k2,3_1e-3.5<t<=1e-2': lambda n, k, x: k in (2, 3) and 10 ** -3.5 < n ** k / x <= 1e-2}
    fits = {}
    for name, sel in groups.items():
        xs, ms = [], []
        for x, (_, _, _, rows) in tab.items():
            v = [s for n, k, _, s in rows if sel(n, k, x)]
            if v:
                xs.append(x)
                ms.append(float(np.mean(v)))
        inv = 1 / np.log(np.array(xs, float))
        slope, icept = np.polyfit(inv, ms, 1)
        fits[name] = {'X': xs, 'mean_s': ms, 'fit': 's = c - a/log X', 'c_infinity': float(icept),
                      'a': float(-slope), 'max_abs_residual': float(np.max(np.abs(np.polyval([slope, icept], inv) - ms)))}
    pts = []
    for x, (_, _, _, rows) in tab.items():
        pts += [(n, s, x) for n, k, _, s in rows if k == 5 and n ** 5 / x >= 3]
    fresh = json.loads((k1.RESULTS / 'rs_s017_fresh_classes_2026-10-26.json').read_text())
    for key, o in fresh['observed'].items():
        kappa = json.loads(key)
        if len(kappa) == 1 and kappa[0][1] == 5:
            for x, v in o.items():
                if v['log10_t'] >= math.log10(3):
                    pts.append((norm(kappa[0][0]), v['s'], int(x)))
    bands = [(19, 43), (61, 73), (79, 150), (151, 250), (251, 400)]
    trend = []
    for lo, hi in bands:
        v = [s for n, s, _ in pts if lo <= n <= hi]
        trend.append({'N_range': [lo, hi], 'n': len(v), 'mean_s': float(np.mean(v)),
                      'se': float(np.std(v) / math.sqrt(len(v)))})
    nn = np.array([p[0] for p in pts], float)
    ss = np.array([p[1] for p in pts])
    b1, b0 = np.polyfit(1 / nn, ss, 1)
    doc = load()
    doc['exploratory_fits'] = {'classification': 'EXPLORATORY', 'plateau_log_fits': fits,
                               'pi5_trend_by_N': trend, 'pi5_fit': {'model': 's = c5 + b/N', 'c5': float(b0),
                                                                    'b': float(b1), 'n': len(pts)}}
    save(doc)
    print(json.dumps(doc['exploratory_fits'], indent=1))


if __name__ == '__main__':
    main()
