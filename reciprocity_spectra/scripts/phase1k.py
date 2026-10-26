"""RS-S015: registered sixth-power-class tests of PROV-RS14 at X = 10^6 (sextic, D = 78462).

w_kappa = conj(g6~) * prod_pi (pi/.)_6^(e_pi), built from prime symbol exponents
(arith.sextic_class_exponents at scale); r = ||C w|| / (||w|| sqrt(D)); forward products only.
eps = (r^2 - 1)/(r_1^2 - 1); s = eps * N6^(1/6), N6 = prod N(pi)^e.

  validate        engine-port check (MSVC on Windows) against stored Linux digests and r values
  register        write the predictions and class list (commit and push before any X = 10^6 data)
  run --part P    P = singles (with u = 1 and controls) or pairs; appends to the results JSON
  score           verbatim scoring of the registered criteria
"""
from __future__ import annotations

import argparse
import gc
import json
import math
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import phase1 as legacy  # noqa: E402
import phase1d  # noqa: E402

ROOT, DATA = legacy.ROOT, legacy.DATA
sys.path.insert(0, str(ROOT))
from reciprocity_spectra.arith import (  # noqa: E402
    DegreeOnePrime,
    sextic_residue_exponent,
    smallest_primary_primes,
)

RESULTS = ROOT / 'reciprocity_spectra/results'
RESULT = RESULTS / 'rs_s015_class_tests_2026-10-26.json'
X = 1_000_000
SEED = 15


def norm(pi):
    return pi[0] ** 2 - pi[0] * pi[1] + pi[1] ** 2


def classes():
    small = smallest_primary_primes(20)
    out = [{'part': 'singles', 'kappa': [[list(pi), k]]} for pi in small for k in range(1, 6)]
    pairs = [(i, j) for i in range(4) for j in range(i + 1, 4)]
    out += [{'part': 'pairs', 'kappa': [[list(small[i]), e1], [list(small[j]), e2]]}
            for i, j in pairs for e1 in range(1, 6) for e2 in range(1, 6)]
    for c in out:
        c['exponents'] = sorted(e for _, e in c['kappa'])
        c['N6'] = math.prod(norm(pi) ** e for pi, e in c['kappa'])
    return out


def save(doc, message=None):
    temp = RESULT.with_suffix('.tmp')
    temp.write_text(json.dumps(doc, indent=2, allow_nan=False) + '\n')
    temp.replace(RESULT)
    if message:
        legacy.shell('git', 'add', str(RESULT))
        legacy.shell('git', 'commit', '-m', message)
        print(legacy.shell('git', 'push', '-u', 'origin', legacy.shell('git', 'branch', '--show-current')))


def build(x):
    path, gpath = DATA / f'sextic_{x}.bin', DATA / f'sexticg_{x}.bin'
    if not (path.exists() and gpath.exists()):
        subprocess.run([str(DATA / 'residue_engine'), 'sextic', str(x), str(path), str(gpath)],
                       check=True, timeout=5400)
    a = legacy.Engine('cubic', x, path)
    a.n = 6
    return a, np.fromfile(gpath, np.complex128)


def rayleigh(a, w):
    return float(np.linalg.norm(a.apply(w / np.linalg.norm(w))) / math.sqrt(a.d))


def digest(path):
    with path.open('rb') as f:
        return legacy.hashlib.file_digest(f, 'sha256').hexdigest()


def release(*paths):
    gc.collect()  # drop the memmap first: Windows cannot delete a mapped file
    for p in paths:
        p.unlink(missing_ok=True)


def stored_digest(x):
    doc = json.loads((RESULTS / 'phase1e_2026-10-25.json').read_text())
    return next(r['matrix_sha256'] for r in doc['rayleigh_runs'] if r['X'] == x and 'matrix_sha256' in r)


def validate():
    legacy.compile_engine()
    out = {'command': 'python ' + ' '.join(sys.argv), 'code_commit': legacy.shell('git', 'rev-parse', 'HEAD'),
           'platform': sys.platform, 'started_at': datetime.now(UTC).isoformat()}
    stored = next(r for r in json.loads((RESULTS / 'phase1e_2026-10-25.json').read_text())['rayleigh_runs']
                  if r['X'] == 320000)
    checks = []
    for x in (320000, 640000):
        a, g = build(x)
        row = {'X': x, 'D': a.d, 'matrix_sha256': digest(a.path), 'stored_sha256': stored_digest(x)}
        row['byte_identical'] = row['matrix_sha256'] == row['stored_sha256']
        if x == 320000:
            rel = []
            for t in stored['twists'][:40]:
                sym = phase1d.sextic_symbol(a.meta, *t['u'])
                r = rayleigh(a, g.conj() * (sym if t['sign'] == '+' else sym.conj()))
                rel.append(abs(r - t['r']) / t['r'])
            rng = np.random.default_rng(13)
            for k in range(2):
                r = rayleigh(a, np.exp(2j * np.pi * rng.random(a.d)))
                rel.append(abs(r - stored['random_phase_r'][k]) / stored['random_phase_r'][k])
            row.update(r_values_compared=len(rel), max_relative_r_difference=max(rel))
        checks.append(row)
        del a
        release(DATA / f'sextic_{x}.bin', DATA / f'sexticg_{x}.bin')
    out['checks'] = checks
    out['pass'] = all(c['byte_identical'] for c in checks) and checks[0]['max_relative_r_difference'] < 1e-8
    doc = json.loads(RESULT.read_text()) if RESULT.exists() else {'session': 'RS-S015', 'runs': []}
    doc['engine_validation'] = out
    save(doc)
    print(json.dumps(out, indent=1))


def exponent_vector(meta, pi):
    out = np.empty(len(meta), np.int8)
    for j, (p, a, b) in enumerate(meta.tolist()):
        k = sextic_residue_exponent(pi[0], pi[1], DegreeOnePrime(3, p, a, b))
        out[j] = -1 if k is None else k
    return out


def run(part):
    doc = json.loads(RESULT.read_text())
    assert doc.get('prediction_commit') and doc['engine_validation']['pass']
    legacy.compile_engine()
    started = time.monotonic()
    row = {'part': part, 'X': X, 'command': 'python ' + ' '.join(sys.argv),
           'code_commit': legacy.shell('git', 'rev-parse', 'HEAD'), 'platform': sys.platform,
           'started_at': datetime.now(UTC).isoformat()}
    a, g = build(X)
    row.update(D=a.d, matrix_sha256=digest(a.path), gauss_sha256=digest(DATA / f'sexticg_{X}.bin'),
               build_seconds=time.monotonic() - started)
    base = g.conj()
    row['r_u1'] = rayleigh(a, base)
    todo = [c for c in classes() if c['part'] == part]
    symbols = {}
    for c in todo:
        for pi, _ in c['kappa']:
            if tuple(pi) not in symbols:
                symbols[tuple(pi)] = exponent_vector(a.meta, pi)
    z6 = np.exp(1j * np.pi / 3 * np.arange(6))
    rows = []
    for c in todo:
        total, zero = np.zeros(a.d, np.int64), np.zeros(a.d, bool)
        for pi, e in c['kappa']:
            v = symbols[tuple(pi)]
            zero |= v < 0
            total += e * v.astype(np.int64)
        w = np.where(zero, 0, base * z6[total % 6])
        rows.append({k: c[k] for k in ('kappa', 'exponents', 'N6')} |
                    {'zero_rows': int(zero.sum()), 'r': rayleigh(a, w)})
    row['classes'] = rows
    if part == 'singles':
        rng = np.random.default_rng(SEED)
        row['control_seed'] = SEED
        row['random_phase_r'] = [rayleigh(a, np.exp(2j * np.pi * rng.random(a.d))) for _ in range(10)]
        row['conj_g6_random_roots_r'] = [rayleigh(a, base * z6[rng.integers(0, 6, a.d)]) for _ in range(10)]
    row['seconds'] = time.monotonic() - started
    doc['runs'].append(row)
    save(doc, f'RS-S015: registered class-twist run X={X} part={part}')
    print(json.dumps({k: row[k] for k in ('part', 'D', 'r_u1', 'seconds')}))


def stat(c, r1):
    eps = (c['r'] ** 2 - 1) / (r1 ** 2 - 1)
    return eps, eps * c['N6'] ** (1 / 6)


def score():
    doc = json.loads(RESULT.read_text())
    runs = {r['part']: r for r in doc['runs']}
    r1 = runs['singles']['r_u1']
    allc = [c | {'part': p} for p in ('singles', 'pairs') for c in runs[p]['classes']]
    for c in allc:
        c['eps'], c['s'] = stat(c, r1)
    low = [c for c in allc if set(c['exponents']) <= {1, 2, 3}]
    has5 = [c for c in allc if 5 in c['exponents']]
    single5 = [c for c in allc if c['part'] == 'singles' and c['exponents'] == [5]]
    s_low = np.array([c['s'] for c in low])
    b_band = [c for c in single5 if 19 <= norm(c['kappa'][0][0]) <= 61]
    b_mean = float(np.mean([c['s'] for c in single5 if norm(c['kappa'][0][0]) >= 19]))

    def worst(cs, key, sign):
        c = max(cs, key=lambda t: sign * t[key])
        return {'kappa': c['kappa'], 'r': c['r'], 's': c['s']}

    out = {
        'r_u1_singles': r1, 'r_u1_pairs': runs['pairs']['r_u1'],
        'P1': {'n': len(low), 'mean_s': float(s_low.mean()), 'sd_s': float(s_low.std()),
               'pass': bool(0.90 <= s_low.mean() <= 1.00 and s_low.std() <= 0.05)},
        'P2': {'n_band': len(b_band), 'max_r_band': max(c['r'] for c in b_band),
               'worst_band': worst(b_band, 'r', 1), 'mean_s_N_ge_19': b_mean,
               'pass': bool(all(c['r'] < 1 for c in b_band) and -1.30 <= b_mean <= -0.80)},
        'P3': {'n_with_5': len(has5), 'max_r_with_5': max(c['r'] for c in has5),
               'worst_with_5': worst(has5, 'r', 1), 'n_low': len(low),
               'min_r_low': min(c['r'] for c in low), 'worst_low': worst(low, 'r', -1),
               'low_failures_at_1.05': [c['kappa'] for c in low if c['r'] <= 1.05],
               'clause_5_pass': bool(all(c['r'] < 1.02 for c in has5)),
               'clause_low_pass': bool(all(c['r'] > 1.05 for c in low))},
    }
    out['P3']['pass'] = out['P3']['clause_5_pass'] and out['P3']['clause_low_pass']
    failing = sorted((c for c in low if c['r'] <= 1.05), key=lambda t: t['N6'])
    out['P3']['smallest_failing_low'] = failing and {k: failing[0][k] for k in ('kappa', 'N6', 'r', 's')}
    by_pattern = {}
    for c in allc:
        by_pattern.setdefault(str(c['exponents']), []).append(c)
    out['by_pattern'] = {k: {'n': len(v), 'mean_s': float(np.mean([c['s'] for c in v])),
                             'min_r': min(c['r'] for c in v), 'max_r': max(c['r'] for c in v)}
                         for k, v in sorted(by_pattern.items())}
    out['P4_exploratory'] = {k: v for k, v in out['by_pattern'].items() if '4' in k}
    out['controls'] = {'random_phase_max': max(runs['singles']['random_phase_r']),
                       'random_phase_sd': float(np.std(runs['singles']['random_phase_r'])),
                       'conj_g6_roots_max': max(runs['singles']['conj_g6_random_roots_r'])}
    gate = out['P1']['pass'] and out['P2']['pass'] and out['P3']['pass']
    out['cand_002_gate'] = {'rule': doc['decision_rule'], 'pass': bool(gate)}
    doc['score'] = out
    save(doc)
    print(json.dumps({k: (v if k != 'by_pattern' else '...') for k, v in out.items()}, indent=1))


def register():
    doc = json.loads(RESULT.read_text())
    assert 'predictions' not in doc, 'predictions are frozen once written'
    r1_stored = 1.4342110940043258  # phase1j sextic X = 10^6 (RS-S012)
    cs = classes()
    expected = sorted(({'kappa': c['kappa'], 'expected_r_under_A': math.sqrt(
        1 + 0.95 * (r1_stored ** 2 - 1) / c['N6'] ** (1 / 6))} for c in cs if set(c['exponents']) <= {1, 2, 3}),
        key=lambda t: t['expected_r_under_A'])[:5]
    doc.update(
        date='2026-10-26', X=X, D_expected=78462,
        class_list={'singles': '20 smallest primary primes (inert (2,0),(5,0) included; norms 4..73) x k=1..5',
                    'pairs': 'all 6 pairs among the 4 smallest primary primes x (e1,e2) in {1..5}^2',
                    'count': len(cs), 'classes': [c['kappa'] for c in cs]},
        controls={'seed': SEED, 'random_phase': 10, 'conj_g6_random_sixth_roots': 10},
        power='sd(r_random) ~ 0.003 at D = 78462; sigma_eps ~ 2 sigma_r/(r_1^2 - 1) ~ 0.006 (RS-S014 section 6)',
        predictions=[
            {'id': 'RS-S015-P1', 'text': 'over single-prime k in {1,2,3} and pair classes with exponents in {1,2,3}, '
                                         'mean eps*N6^(1/6) in [0.90, 1.00] and sd <= 0.05'},
            {'id': 'RS-S015-P2', 'text': 'every single-prime k = 5 class with 19 <= N(pi) <= 61 has r < 1, and over '
                                         'N(pi) >= 19 the mean eps*N^(5/6) in [-1.30, -0.80]'},
            {'id': 'RS-S015-P3', 'text': 'every class containing an exponent 5 has r < 1.02; every class with '
                                         'exponents in {1,2,3} has r > 1.05 (verbatim draft)'},
            {'id': 'RS-S015-P4', 'text': 'EXPLORATORY: report eps*N6^(1/6) for k = 4 and pairs containing 4'},
        ],
        pre_data_note=('Before any X = 10^6 class data: under PROV-RS14 (A) with s = 0.95 and stored r_1 = '
                       '1.4342, the smallest expected r among {1,2,3} classes is listed in lowest_expected_r; '
                       'the P3 threshold 1.05 has a thin margin there (about 1.051 for (3,3) on N = 7 x 13). '
                       'Criteria are registered verbatim from RS_S014_INVARIANCE_AUDIT.md section 6.'),
        lowest_expected_r=expected,
        decision_rule=('Freeze CAND-002 only if P1, P2 and P3 all PASS. A failure of P1 or P3 refutes PROV-RS14 '
                       'as stated; record the smallest failing class.'),
        prediction_commit=None)
    save(doc)
    print(len(cs), 'classes; lowest expected r under (A):', expected[0]['expected_r_under_A'])


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('step', choices=['validate', 'register', 'run', 'score'])
    parser.add_argument('--part', choices=['singles', 'pairs'])
    args = parser.parse_args()
    if args.step == 'run':
        run(args.part)
    else:
        {'validate': validate, 'register': register, 'score': score}[args.step]()


if __name__ == '__main__':
    main()
