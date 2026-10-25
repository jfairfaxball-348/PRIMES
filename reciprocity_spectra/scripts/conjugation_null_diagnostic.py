"""EXPLORATORY diagnostic (2026-10-25): does the conjugation identity explain RS-6's gap-ratio FAIL?

For n = 3, 4 the arithmetic matrices satisfy (conj(pi)/conj(rho))_n = conj((pi/rho)_n) exactly,
and the entries (pi/conj(pi))_n are forced.  The RS-S003 controls matched reciprocity only.
This script builds a control that also imposes the conjugation identity (copying the forced
(pi/conj pi) entries) and compares bulk gap ratios (central 60% of singular values).
Usage: python scripts/conjugation_null_diagnostic.py X   (needs data/{cubic,quartic}_X.bin)
Not a status driver: RS-S003's registered FAIL outcomes are immutable.
"""
from __future__ import annotations

import json
import sys

import numpy as np
from spectra import load_matrix, reciprocity_signs


def gap_ratio(sv: np.ndarray) -> float:
    s = np.sort(sv)
    n = len(s)
    s = s[int(0.2 * n) : int(0.8 * n)]
    g = np.diff(s)
    return float((np.minimum(g[1:], g[:-1]) / np.maximum(g[1:], g[:-1])).mean())


def conjugate_index(mode: str, meta) -> np.ndarray:
    key = {tuple(int(v) for v in row): i for i, row in enumerate(meta)}
    if mode == "cubic":  # conj(a + b w) = (a - b) - b w
        return np.array([key[(p, a - b, -b)] for p, a, b in meta.tolist()])
    return np.array([key[(p, a, -b)] for p, a, b in meta.tolist()])


def symmetric_control(mode: str, meta, mat, seed: int) -> np.ndarray:
    n = {"cubic": 3, "quartic": 4}[mode]
    d = len(meta)
    cj = conjugate_index(mode, meta)
    s = reciprocity_signs(mode, meta)
    rng = np.random.default_rng(seed)
    roots = np.exp(2j * np.pi * np.arange(n) / n)
    draw = roots[rng.integers(0, n, (d, d))]
    out = np.zeros((d, d), complex)
    done = np.eye(d, dtype=bool)
    for j in range(d):
        for k in range(j + 1, d):
            if done[j, k]:
                continue
            v = mat[j, k] if k == cj[j] else draw[j, k]
            out[j, k], out[k, j] = v, s[j, k] * v
            out[cj[j], cj[k]], out[cj[k], cj[j]] = np.conj(v), s[j, k] * np.conj(v)
            done[j, k] = done[k, j] = done[cj[j], cj[k]] = done[cj[k], cj[j]] = True
    return out


def main() -> None:
    x = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
    rows = []
    for mode in ("cubic", "quartic"):
        _, meta, mat = load_matrix(mode, x)
        cj = conjugate_index(mode, meta)
        row = {"mode": mode, "X": x, "D": len(meta),
               "conjugation_identity_max_err": float(np.max(np.abs(mat[np.ix_(cj, cj)] - mat.conj()))),
               "arithmetic_gap_ratio": round(gap_ratio(np.linalg.svd(mat, compute_uv=False)), 4)}
        for seed in (0, 1):
            ctrl = symmetric_control(mode, meta, mat, seed)
            sv = np.linalg.svd(ctrl, compute_uv=False)
            row[f"control_seed{seed}_gap_ratio"] = round(gap_ratio(sv), 4)
            row[f"control_seed{seed}_s1_over_edge"] = round(float(sv.max() / (2 * np.sqrt(len(meta)))), 4)
        rows.append(row)
    print(json.dumps(rows, indent=1))


if __name__ == "__main__":
    main()
