#!/usr/bin/env bash
# Reproduce the 2026-10-24 pilot.  Needs a C compiler, python3 with numpy and scipy.
# Usage: scripts/run_pilot.sh [Xmax]   (default 40000; the recorded pilot went to 160000)
set -euo pipefail
here="$(cd "$(dirname "$0")/.." && pwd)"
xmax="${1:-40000}"
mkdir -p "$here/data"
cc -O2 -o "$here/data/residue_matrix" "$here/native/residue_matrix.c" -lm
xs=()
for x in 5000 10000 20000 40000 80000 160000; do
  if [ "$x" -le "$xmax" ]; then xs+=("$x"); fi
done
for x in "${xs[@]}"; do
  "$here/data/residue_matrix" cubic "$x" "$here/data/cubic_$x.bin" "$here/data/cubicg_$x.bin"
  "$here/data/residue_matrix" quartic "$x" "$here/data/quartic_$x.bin" "$here/data/quarticg_$x.bin"
  "$here/data/residue_matrix" quad "$x" "$here/data/quad_$x.bin"
done
cd "$here"
python3 scripts/spectra.py spike "${xs[@]}"
python3 scripts/spectra.py family "${xs[-1]}"
python3 scripts/spectra.py bulk quad "${xs[@]}"
for x in "${xs[@]}"; do python3 scripts/spectra.py summary quartic "$x"; done
