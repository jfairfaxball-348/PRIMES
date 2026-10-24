"""Spectral analysis of power-residue matrices built by ``native/residue_matrix.c``.

Requires numpy and scipy (not needed by the test suite).  Matrices are read from
``reciprocity_spectra/data/{mode}_{X}.bin`` and Gauss sums from ``{mode}g_{X}.bin``.

Sub-commands
------------
summary MODE X        top singular values, reciprocity-structured random control, Gauss overlap
spike X [X ...]       cubic spike law: BBP-inverted strength theta vs kappa * X^(2/3) / log X
family X              identify cubic outliers with twisted Gauss-sum vectors conj(g) * (u/pi)_3
bulk MODE X [X ...]   normalized singular-value moments m4, m6 and edge (full SVD)
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
from scipy.sparse.linalg import svds

DATA = Path(__file__).resolve().parent.parent / "data"
ORDER = {"quad": 2, "cubic": 3, "quartic": 4}


def load_matrix(mode: str, x: int):
    """Return (D, meta, C) with C the complex (real for quad) residue-symbol matrix."""
    n = ORDER[mode]
    with open(DATA / f"{mode}_{x}.bin", "rb") as f:
        d = int(np.frombuffer(f.read(4), np.int32)[0])
        meta = np.frombuffer(f.read(24 * d), np.int64).reshape(d, 3)
        exps = np.frombuffer(f.read(d * d), np.uint8).reshape(d, d)
    lut = np.zeros(256, np.complex128)
    lut[:n] = np.exp(2j * np.pi * np.arange(n) / n) if n > 2 else np.array([1.0, -1.0])
    mat = lut[exps]
    return d, meta, (mat.real.copy() if n == 2 else mat)


def load_gauss(mode: str, x: int, d: int) -> np.ndarray:
    g = np.fromfile(DATA / f"{mode}g_{x}.bin", np.float64).reshape(d, 2)
    return g[:, 0] + 1j * g[:, 1]


def top_singular(mat, k: int):
    u, s, vh = svds(mat, k=k)
    order = np.argsort(-s)
    return u[:, order], s[order], vh[order]


def reciprocity_signs(mode: str, meta) -> np.ndarray:
    """s_ij with C_ji = s_ij C_ij (Legendre: both p = 3 mod 4; quartic: both N = 5 mod 8)."""
    p = meta[:, 0]
    if mode == "quad":
        odd = p % 4 == 3
    elif mode == "quartic":
        odd = p % 8 == 5
    else:
        odd = np.zeros(len(p), bool)
    return np.where(np.outer(odd, odd), -1.0, 1.0)


def structured_random(mode: str, meta, seed: int = 0):
    """Uniform random symbol matrix with exactly the same reciprocity structure (null model)."""
    n = ORDER[mode]
    d = len(meta)
    rng = np.random.default_rng(seed)
    roots = np.exp(2j * np.pi * np.arange(n) / n) if n > 2 else np.array([1.0, -1.0])
    upper = np.triu(roots[rng.integers(0, n, size=(d, d))], 1)
    return upper + (reciprocity_signs(mode, meta) * upper).T


def bbp_strength(s1: float, d: int) -> float:
    """Invert s1 = theta + d / theta (square spiked model); nan below threshold."""
    disc = s1 * s1 - 4 * d
    return (s1 + math.sqrt(disc)) / 2 if disc > 0 else float("nan")


def cmd_summary(mode: str, x: int) -> dict:
    d, meta, mat = load_matrix(mode, x)
    edge = 2 * math.sqrt(d)
    _, s, vh = top_singular(mat, 8)
    ctrl = np.sort(svds(structured_random(mode, meta), k=4, return_singular_vectors=False))[::-1]
    out = {"mode": mode, "X": x, "D": d, "top_sv_over_edge": [round(v / edge, 4) for v in s],
           "control_top_sv_over_edge": [round(v / edge, 4) for v in ctrl]}
    gpath = DATA / f"{mode}g_{x}.bin"
    if gpath.exists():
        g = load_gauss(mode, x, d)
        v = vh[0].conj()
        out["overlap_top_right_sv_conj_gauss"] = round(abs(np.vdot(g.conj(), v)) / np.linalg.norm(g), 4)
        out["rayleigh_conj_gauss_over_sqrtD"] = round(float(np.linalg.norm(mat @ g.conj()) / np.linalg.norm(g) / math.sqrt(d)), 4)
    return out


def cmd_spike(xs: list[int]) -> list[dict]:
    rows = []
    for x in xs:
        d, _, mat = load_matrix("cubic", x)
        g = load_gauss("cubic", x, d)
        _, s, vh = top_singular(mat, 2)
        theta = bbp_strength(s[0], d)
        tn = theta / math.sqrt(d)
        rows.append({"X": x, "D": d, "s1": round(float(s[0]), 2), "s1_over_edge": round(s[0] / (2 * math.sqrt(d)), 4),
                     "theta": round(theta, 2), "kappa3": round(theta / (x ** (2 / 3) / math.log(x)), 4),
                     "overlap_conj_gauss": round(abs(np.vdot(g.conj(), vh[0].conj())) / np.linalg.norm(g), 4),
                     "bbp_predicted_overlap": round(math.sqrt(1 - 1 / tn**2), 4)})
        del mat
    return rows


def cubic_symbol_vector(meta, c: int, e: int) -> np.ndarray:
    """((c + e*w)/pi)_3 over the index set, as complex numbers."""
    w = np.exp(2j * np.pi / 3)
    out = np.zeros(len(meta), complex)
    for j, (p, a, b) in enumerate(meta.tolist()):
        r = (-a * pow(b % p, -1, p)) % p
        v = (c + e * r) % p
        if v:
            t = pow(v, (p - 1) // 3, p)
            out[j] = 1 if t == 1 else (w if t == r else w * w)
    return out


def cmd_family(x: int, k: int = 24) -> list[dict]:
    d, meta, mat = load_matrix("cubic", x)
    g = load_gauss("cubic", x, d)
    _, s, vh = top_singular(mat, k)
    basis = vh.conj().T
    elems = [("1", 1, 0), ("2 (inert)", 2, 0), ("1-w (ramified)", 1, -1)]
    seen = set()
    for p, a, b in meta.tolist():
        if p not in seen and len(seen) < 6:
            seen.add(p)
            elems.append((f"pi=({a}{b:+d}w), N={p}", a, b))
    rows = []
    for name, c, e in elems:
        sym = np.ones(d, complex) if (c, e) == (1, 0) else cubic_symbol_vector(meta, c, e)
        for sign, tw in (("+", sym), ("-", sym.conj())):
            vec = g.conj() * tw
            vec /= np.linalg.norm(vec)
            coef = basis.conj().T @ vec
            top = int(np.argmax(np.abs(coef)))
            rows.append({"u": name, "twist": sign, "proj_norm_topk": round(float(np.linalg.norm(coef)), 3),
                         "dominant_index": top, "dominant_sigma_over_edge": round(s[top] / (2 * math.sqrt(d)), 4),
                         "rayleigh_over_sqrtD": round(float(np.linalg.norm(mat @ vec) / math.sqrt(d)), 3)})
    return rows


def cmd_bulk(mode: str, xs: list[int]) -> list[dict]:
    rows = []
    for x in xs:
        d, _, mat = load_matrix(mode, x)
        sv = np.linalg.svd(mat, compute_uv=False) / math.sqrt(d)
        m4, m6 = float(np.mean(sv**4)), float(np.mean(sv**6))
        rows.append({"mode": mode, "X": x, "D": d, "m4": round(m4, 4), "m6": round(m6, 4),
                     "edge": round(float(sv.max()), 4), "(2-m4)logD": round((2 - m4) * math.log(d), 3),
                     "(1-edge/2)logD": round((1 - sv.max() / 2) * math.log(d), 3)})
        del mat
    return rows


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("summary")
    a.add_argument("mode", choices=sorted(ORDER))
    a.add_argument("X", type=int)
    b = sub.add_parser("spike")
    b.add_argument("X", type=int, nargs="+")
    c = sub.add_parser("family")
    c.add_argument("X", type=int)
    e = sub.add_parser("bulk")
    e.add_argument("mode", choices=sorted(ORDER))
    e.add_argument("X", type=int, nargs="+")
    args = ap.parse_args()
    if args.cmd == "summary":
        res = cmd_summary(args.mode, args.X)
    elif args.cmd == "spike":
        res = cmd_spike(args.X)
    elif args.cmd == "family":
        res = cmd_family(args.X)
    else:
        res = cmd_bulk(args.mode, args.X)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
