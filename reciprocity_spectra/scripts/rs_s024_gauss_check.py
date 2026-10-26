"""RS-S024: cross-check normalized sextic Gauss sums at X=200.

The native C engine exports 42 complex128 values g(p)/sqrt(p). Independently
recompute from the Python Euler-criterion implementation and compare components
with tolerance 2e-12. The saved JSON fixture is produced by the native engine.

Run from repository root:
  python reciprocity_spectra/scripts/rs_s024_gauss_check.py --export
  python reciprocity_spectra/scripts/rs_s024_gauss_check.py --check
"""
from __future__ import annotations

import argparse
import json
import math
import struct
from pathlib import Path

from reciprocity_spectra.arith import primary_eisenstein_primes, sextic_gauss_sum
from reciprocity_spectra.scripts.phase1 import DATA, build, compile_engine

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "formalisation/fixtures/sextic_gauss_200.json"
X = 200
TOL = 2e-12


def native_values():
    compile_engine()
    engine = build("sextic", X, gauss=True)
    path = DATA / f"sexticg_{X}.bin"
    raw = path.read_bytes()
    if len(raw) != engine.d * 16:
        raise AssertionError(f"Incorrect native Gauss length: {len(raw)}")
    vals = [complex(*struct.unpack_from("dd", raw, 16 * j)) for j in range(engine.d)]
    index = [(int(p), int(a), int(b)) for p, a, b in engine.meta]
    return index, vals


def generate():
    index, g = native_values()
    primes = primary_eisenstein_primes(X)
    assert index == [(p.p, p.a, p.b) for p in primes], "Native/Python index mismatch"
    rows = []
    max_diff = 0.0
    for item, z in zip(primes, g, strict=True):
        independently = sextic_gauss_sum(item) / math.sqrt(item.p)
        delta = abs(z - independently)
        max_diff = max(max_diff, delta)
        assert delta <= TOL, f"Gauss mismatch at ({item.a},{item.b}): {delta}"
        rows.append({"p": item.p, "a": item.a, "b": item.b,
                     "real": z.real, "imag": z.imag})
    return {"X": X, "D": len(rows), "engine": "native/residue_engine.c sextic",
            "method": "native complex128 vs independent arith.sextic_gauss_sum",
            "absolute_tolerance": TOL, "maximum_observed_difference": max_diff,
            "entries": rows}


def check(record):
    current = generate()
    assert record["X"] == current["X"] and record["D"] == current["D"]
    assert len(record["entries"]) == len(current["entries"])
    for a, b in zip(record["entries"], current["entries"], strict=True):
        assert [a[k] for k in ("p", "a", "b")] == [b[k] for k in ("p", "a", "b")]
        assert abs(complex(a["real"], a["imag"]) -
                   complex(b["real"], b["imag"])) <= TOL
    return current


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--export", action="store_true")
    p.add_argument("--check", action="store_true")
    args = p.parse_args()
    if args.export and args.check:
        p.error("Choose export or check")
    if args.check:
        report = check(json.loads(FIXTURE.read_text(encoding="utf8")))
    else:
        report = generate()
    print(f"Gauss X={X}, D={report['D']}, max error={report['maximum_observed_difference']:.3g}")
    if args.export:
        print("FIXTURE_JSON_BEGIN")
        print(json.dumps(report, indent=2))
        print("FIXTURE_JSON_END")


if __name__ == "__main__":
    main()
