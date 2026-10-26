#!/usr/bin/env bash
# Fresh-clone / cloud setup for the Lean formalisation (same method as Almost-Stacked-Proof `formal/`):
# install elan if missing, fetch the prebuilt Mathlib cache for the pinned commit, build, run the checks.
# Usage (from the repository root or formalisation/):  bash formalisation/cloud_setup.sh
set -euo pipefail

cd "$(dirname "$0")"

if ! command -v lake >/dev/null 2>&1; then
  if [ ! -x "$HOME/.elan/bin/lake" ]; then
    curl -sSfL https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh \
      | sh -s -- -y --default-toolchain none
  fi
  export PATH="$HOME/.elan/bin:$PATH"
fi

echo "toolchain: $(cat lean-toolchain)"
lake --version

# Prebuilt Mathlib oleans for the pinned commit (several GB; avoids rebuilding Mathlib).
lake exe cache get

# Library, then the checks (axiom audit + faithfulness against the engine fixture).
lake build ReciprocitySpectra
lake build Checks 2>&1 | grep -E "depends on axioms|mismatches|error" || true
