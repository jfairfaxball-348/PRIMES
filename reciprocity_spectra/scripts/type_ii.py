"""RS-S013 EXPLORATORY squarefree Type II kernels, run locally.

M,N denote lower norm endpoints; the supports are (M,2M] and (N,2N].
No finite measurement is a theorem or a registered conjecture test.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import platform
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

os.environ.setdefault('OPENBLAS_NUM_THREADS', '2')
os.environ.setdefault('OMP_NUM_THREADS', '2')

import numpy as np
import scipy
from scipy.linalg import svd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from reciprocity_spectra.bilinear import (  # noqa: E402
    kernel_exponent,
    normalized_gauss_sum,
    squarefree_moduli,
)


def conjugation_map(moduli):
    by_element = {m.element: i for i, m in enumerate(moduli)}
    return [by_element[(m.element[0] - m.element[1], -m.element[1])] for m in moduli]


def matched_control(exponents, rows, cols, seed):
    """Randomize conjugation/transpose orbits, preserving support and quadratic sign.

    This is the squarefree product-kernel counterpart of structured_random.
    A raw prime-symbol null is not applicable to composite reciprocal products.
    The sixth-root exponent parity is the quadratic reciprocity sign; choose
    uniformly among its three compatible roots. Self-conjugate orbits are forced.
    """
    rng = np.random.default_rng(seed)
    ri, cj = conjugation_map(rows), conjugation_map(cols)
    rlookup = {m.element: i for i, m in enumerate(rows)}
    clookup = {m.element: j for j, m in enumerate(cols)}
    out = np.full(exponents.shape, -1, dtype=np.int8)
    for i, m in enumerate(rows):
        for j, n in enumerate(cols):
            if exponents[i, j] < 0 or out[i, j] >= 0:
                continue
            orbit = {(i, j, 1), (ri[i], cj[j], -1)}
            if n.element in rlookup and m.element in clookup:
                ti, tj = rlookup[n.element], clookup[m.element]
                orbit |= {(ti, tj, 1), (ri[ti], cj[tj], -1)}
            parity = int(exponents[i, j] % 2)
            positive = {(a, b) for a, b, s in orbit if s == 1}
            negative = {(a, b) for a, b, s in orbit if s == -1}
            k = 3 * parity if positive & negative else parity + 2 * int(rng.integers(3))
            for a, b, sign in orbit:
                assert exponents[a, b] >= 0 and exponents[a, b] % 2 == parity
                out[a, b] = sign * k % 6
    assert np.array_equal(out < 0, exponents < 0)
    assert np.array_equal(out[np.ix_(ri, cj)], np.where(out < 0, -1, -out % 6))
    if [m.element for m in rows] == [m.element for m in cols]:
        assert np.array_equal(out, out.T)
    return np.where(out < 0, 0, np.exp(1j * np.pi * out / 3))


def measure(moduli, m_lower, n_lower, phases, seed):
    start = time.perf_counter()
    rows = [m for m in moduli if m_lower < m.norm <= 2 * m_lower]
    cols = [n for n in moduli if n_lower < n.norm <= 2 * n_lower]
    exponents = np.array([[(-1 if (k := kernel_exponent(m, n)) is None else k)
                           for n in cols] for m in rows], dtype=np.int8)
    symbol = np.where(exponents < 0, 0, np.exp(1j * np.pi * exponents / 3))
    gp = np.array([phases[m] for m in rows])
    gq = np.array([phases[n] for n in cols])
    kernel = gp[:, None] * symbol * gq[None, :]
    u, singular, vh = svd(kernel, full_matrices=False, check_finite=False)
    sigma = float(singular[0])
    v = vh[0].conj()
    r, c = kernel.shape
    alpha, beta = u[:, 0].conj() * math.sqrt(r), v * math.sqrt(c)
    extremal = abs(alpha @ kernel @ beta)
    assert abs(extremal / (sigma * math.sqrt(r * c)) - 1) < 1e-10
    symbol_sigma = float(svd(symbol, compute_uv=False, check_finite=False)[0])
    assert abs(sigma / symbol_sigma - 1) < 1e-10
    phase_alpha = np.exp(-1j * np.angle(u[:, 0]))
    phase_beta = np.exp(1j * np.angle(v))
    rng = np.random.default_rng(seed)
    random_values = [float(abs(np.exp(2j * np.pi * rng.random(r)) @ kernel
                              @ np.exp(2j * np.pi * rng.random(c)))) for _ in range(8)]
    controls = []
    for control_seed in (0, 1, 2):
        null = matched_control(exponents, rows, cols, control_seed)
        controls.append({'seed': control_seed,
                         'operator_norm': float(svd(null, compute_uv=False)[0])})
    # Epsilon factor and implicit constant are deliberately NOT assigned values.
    sieve_shape = 2 * m_lower + 2 * n_lower + (4 * m_lower * n_lower) ** (2 / 3)
    x = 4 * m_lower * n_lower
    target = x ** (2 / 3) / math.log(x)
    count = int(np.sum(exponents >= 0))
    lower_bound = math.sqrt(count / min(r, c))
    mu_rows = np.array([(-1) ** len(m.factors) for m in rows])
    mu_cols = np.array([(-1) ** len(n.factors) for n in cols])
    return {
        'M_lower': m_lower, 'N_lower': n_lower, 'X_product_upper': x,
        'D': [r, c], 'frequency_c': [1, 0], 'coprime_pairs': count,
        'matrix_exponent_sha256': hashlib.sha256(exponents.tobytes()).hexdigest(),
        'operator_norm': sigma, 'symbol_operator_norm': symbol_sigma,
        'gauss_phase_norm_max_error': float(max(np.max(abs(abs(gp) - 1)), np.max(abs(abs(gq) - 1)))),
        'frobenius_rank_lower_bound': lower_bound,
        'sieve_shape_without_constant_or_epsilon': sieve_shape,
        'operator_norm_over_sqrt_sieve_shape': sigma / math.sqrt(sieve_shape),
        'target_X_two_thirds_over_log_X': target,
        'l2_extremal_form': float(extremal),
        'l2_extremal_over_target': float(extremal / target),
        'l2_extremal_max_abs_coefficients': [float(max(abs(alpha))), float(max(abs(beta)))],
        'phase_projected_unimodular_form': float(abs(phase_alpha @ kernel @ phase_beta)),
        'random_unimodular_forms': random_values, 'coefficient_seed': seed,
        'constant_coefficient_form': float(abs(np.ones(r) @ kernel @ np.ones(c))),
        'mobius_coefficient_form': float(abs(mu_rows @ kernel @ mu_cols)),
        'matched_controls': controls,
        'wall_seconds': time.perf_counter() - start,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--seed', type=int, default=23)
    args = parser.parse_args()
    pairs = [(32, 32), (64, 64), (128, 128), (256, 256), (512, 512),
             (32, 256), (64, 512), (32, 1024)]
    paths = [Path(__file__), ROOT / 'reciprocity_spectra/bilinear.py',
             ROOT / 'reciprocity_spectra/arith.py']
    doc = {
        'session': 'RS-S013', 'stage': 'EXPLORATORY', 'date': '2026-10-26',
        'created_utc': datetime.now(UTC).isoformat(), 'execution': 'local Windows',
        'code_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        'source_sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
        'command': subprocess.list2cmdline([sys.executable, *sys.argv]),
        'versions': {'python': platform.python_version(), 'numpy': np.__version__, 'scipy': scipy.__version__},
        'parameters': {'norm_intervals': '(M,2M], (N,2N]', 'pairs': pairs,
                       'support': 'all squarefree ideals of Z[omega] coprime to 6; canonical prime-factor products',
                       'noncoprime_pairs': 'zero (restricted Type II form)', 'frequency_c': [1, 0],
                       'coefficient_seed': args.seed, 'control_seeds': [0, 1, 2]},
        'limitations': [
            'Approximate complex128 spectra; exact integer character exponents.',
            'The sieve expression omits its unknown constant and epsilon; it is not a numerical upper bound.',
            'L2 extremizers are data-dependent and need not be bounded by one or arise in a prime decomposition.',
            'No bound uniform in moving frequency c, no prime asymptotic, and no conjecture status promotion.',
            'The product-kernel control preserves coprimality zeros, transpose, conjugation, quadratic signs and forced entries.',
        ],
        'runs': [],
    }
    moduli = squarefree_moduli(2048)
    used = {m for m in moduli if any(a < m.norm <= 2*a for pair in pairs for a in pair)}
    phases = {m: normalized_gauss_sum((1, 0), m) for m in used}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    for m_lower, n_lower in pairs:
        run = measure(moduli, m_lower, n_lower, phases, args.seed)
        doc['runs'].append(run)
        temp = args.output.with_suffix('.tmp')
        temp.write_text(json.dumps(doc, indent=2) + '\n', encoding='utf-8')
        temp.replace(args.output)
        print(json.dumps({k: run[k] for k in ('M_lower', 'N_lower', 'D', 'operator_norm',
                                             'l2_extremal_over_target', 'wall_seconds')}), flush=True)


if __name__ == '__main__':
    main()
