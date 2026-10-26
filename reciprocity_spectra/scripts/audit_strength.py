"""Recompute the original 80-twist sextic criterion and the exact u=64 sanity check.

Read-only, local, standard-library audit of frozen RS-S012 evidence. No matrices are
generated and no new statistical scale is tested. Use --check to compare the
recomputation with the recorded RS-S013 audit (or --check PATH for another record).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import statistics
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from reciprocity_spectra.arith import (  # noqa: E402
    primary_eisenstein_primes,
    sextic_residue_exponent,
)

SOURCE = ROOT / 'reciprocity_spectra/results/phase1j_2026-10-25.json'
AUDIT = ROOT / 'reciprocity_spectra/results/rs_s013_candidate_audit_2026-10-26.json'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def compare(actual, recorded, label):
    """Check complete structures, allowing only float-rounding differences."""
    if isinstance(actual, float):
        require(isinstance(recorded, (int, float)) and
                math.isclose(actual, recorded, rel_tol=1e-12, abs_tol=1e-14), label)
    elif isinstance(actual, dict):
        require(isinstance(recorded, dict) and actual.keys() == recorded.keys(), label)
        for key, value in actual.items():
            compare(value, recorded[key], f'{label}.{key}')
    elif isinstance(actual, list):
        require(isinstance(recorded, list) and len(actual) == len(recorded), label)
        for i, (left, right) in enumerate(zip(actual, recorded, strict=True)):
            compare(left, right, f'{label}[{i}]')
    else:
        require(actual == recorded, label)


def recompute():
    source = json.loads(SOURCE.read_text(encoding='utf-8'))
    predictions = [p for p in source['predictions'] if p['id'] == 'RS-S012-LAW-SEXTIC']
    require(len(predictions) == 1, 'Expected one original sextic prediction')
    prediction = predictions[0]
    runs = [r for r in source['runs'] if r['mode'] == 'sextic' and
            r['X'] == prediction['X']]
    require(len(runs) == 1, 'Expected one matching frozen sextic run')
    run = runs[0]
    norm_max = prediction['norm_max']
    require(norm_max == 100, 'Unexpected registered norm cutoff')

    # Enumerate the whole eligible family independently of the historical filter.
    bound = math.isqrt(4 * norm_max // 3) + 1
    expected = {(a, b) for a in range(-bound, bound + 1)
                for b in range(-bound, bound + 1)
                if 1 < a*a - a*b + b*b <= norm_max and b % 3 == 0 and (a+b) % 3}
    require(len(expected) == 80, 'Unexpected eligible family size')
    selected = []
    seen = set()
    for row in run['twists']:
        a, b = row['u']
        require((a, b) not in seen, 'Duplicate stored twist')
        seen.add((a, b))
        require(row['norm'] == a*a - a*b + b*b, 'Incorrect stored norm')
        require(row['pm_primary'] == (b % 3 == 0), 'Incorrect primary-class flag')
        require((a+b) % 3 != 0 and math.isfinite(row['r']), 'Invalid stored twist')
        if (a, b) in expected:
            selected.append(row)
    require({tuple(row['u']) for row in selected} == expected, 'Incomplete eligible family')
    r1 = next(row['r'] for row in run['twists'] if row['u'] == [1, 0])
    compare(r1, run['r_u1'], 'stored r_1')
    denominator = r1*r1 - 1
    require(denominator != 0, 'Strength ratio has a zero denominator')

    def ratio(row):
        return (row['r']*row['r'] - 1) * row['norm']**(1/6) / denominator

    ratios = [ratio(row) for row in selected]
    mean, sd = statistics.mean(ratios), statistics.pstdev(ratios)
    others = [row for row in run['twists'] if not row['pm_primary'] and row['norm'] <= 13]
    require(bool(others), 'Missing other-associate checks')
    criteria = {
        'mean_in_registered_interval': prediction['mean_min'] <= mean <= prediction['mean_max'],
        'population_sd_at_most_registered_max': sd <= prediction['sd_max'],
        'all_pm_primary_r_gt_1': all(row['r'] > 1 for row in run['twists'] if row['pm_primary']),
        'all_tested_other_associates_norm_le_13_r_lt_1': all(row['r'] < 1 for row in others),
    }
    corrected = {'ratio_n': len(ratios), 'ratio_mean': mean, 'ratio_sd': sd,
                 'criteria': criteria, 'outcome': 'PASS' if all(criteria.values()) else 'FAIL'}
    omitted = [{'u': row['u'], 'norm': row['norm'], 'r': row['r'], 'correct_ratio': ratio(row)}
               for row in selected if row['u'] in ([8, 0], [-8, 0])]
    primes = primary_eisenstein_primes(1000)
    exponents = [sextic_residue_exponent(64, 0, prime) for prime in primes]
    require(all(exponent == 0 for exponent in exponents), 'u=64 symbol sanity check failed')
    sanity = {'X': 1000, 'prime_ideal_count': len(primes),
              'exponents_observed': sorted(set(exponents)), 'all_zero': True}
    return prediction, run, corrected, omitted, sanity


def check_record(path, prediction, run, corrected, omitted, sanity):
    record = json.loads(path.read_text(encoding='utf-8'))
    for source in record['sources']:
        if 'git_ref' in source:
            content = subprocess.check_output(
                ['git', 'show', f"{source['git_ref']}:{source['path']}"], cwd=ROOT)
            expected = source['git_blob_sha256']
        else:
            content = (ROOT / source['path']).read_bytes()
            expected = source['sha256']
        digest = hashlib.sha256(content).hexdigest()
        # RS-S014: the RS-S013 record hashed a Windows CRLF checkout. Also accept the same content
        # with normalized line endings, so the check is platform independent.
        lf = content.replace(b'\r\n', b'\n')
        candidates = {digest, hashlib.sha256(lf).hexdigest(),
                      hashlib.sha256(lf.replace(b'\n', b'\r\n')).hexdigest()}
        require(expected in candidates or source.get('sha256_lf') in candidates,
                f"Source hash mismatch: {source['path']}")
    compare(prediction, record['registration']['prediction'], 'registered prediction')
    finite = record['finite_recomputation']
    for key in ('X', 'D'):
        compare(run[key], finite[key], key)
    compare(run['code_commit'], finite['source_code_commit'], 'source code commit')
    for key, value in finite['original'].items():
        compare(run[key], value, f'original.{key}')
    compare(corrected, finite['corrected'], 'corrected')
    compare(omitted, finite['omitted_rows'], 'omitted rows')
    exact = record['exact_obstruction']
    compare([64, 0], exact['u'], 'counterexample u')
    compare(64**2, exact['norm_u'], 'counterexample norm')
    require(64 == 2**6 and 4096 == 4**6, 'Exact sixth-power arithmetic failed')
    for key, numerator, denominator in (
        ('actual_relative_strength', 1, 1),
        ('statement_3_required_relative_strength_limit', 1, 4),
        ('actual_rescaled_ratio', 4, 1),
        ('statement_3_required_rescaled_ratio_limit', 1, 1),
    ):
        compare({'numerator': numerator, 'denominator': denominator}, exact[key], key)
    for key, value in sanity.items():
        compare(value, exact['bounded_sanity_check'][key], f'symbol sanity.{key}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', nargs='?', const=AUDIT, type=Path,
                        help='Verify the recorded audit; defaults to the RS-S013 record')
    args = parser.parse_args()
    prediction, run, corrected, omitted, sanity = recompute()
    if args.check is not None:
        check_record(args.check, prediction, run, corrected, omitted, sanity)
    print(json.dumps({'source': str(SOURCE.relative_to(ROOT)), 'X': run['X'], 'D': run['D'],
                      'corrected': corrected, 'u64_symbol_sanity': sanity,
                      'checked_record': str(args.check) if args.check is not None else None}, indent=2))


if __name__ == '__main__':
    main()
