#!/usr/bin/env bash
# Exactly one separately precommitted complete D20 invocation. Run this file unchanged twice.
set -euo pipefail
cd "$(dirname "$0")/../.."
PYTHONPATH=.:src python experiments/E020_s3_generator_word_endpoint_residue_shapes.py \
  --band D20 \
  --code-commit ff17721ddebdc309e9927e619786bc163cfed3f1 \
  --output /tmp/e020-d20-discovery.json
