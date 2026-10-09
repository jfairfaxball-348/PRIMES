#!/bin/sh
set -eu
cd "$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)"
python experiments/E021_fixed_block_set_partition_residue_shapes.py --code-commit 3272bb793cece4d5083e492e6abe9268129a5d70 --output /tmp/e021-d21-discovery.json
