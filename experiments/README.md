# Experiments

Experiments are bounded, reproducible questions. They are not informal scratchpads.

Each promoted experiment should declare:

- ID and question;
- stage;
- primitive objects and transforms;
- discovery range;
- holdout/adversarial ranges where relevant;
- command and parameters;
- generated artifacts;
- interpretation limits.

## E000 — Baseline scan

`E000_baseline_scan.py` validates the core pipeline and prints an exact JSON summary containing:

- prime count;
- gap extrema;
- common gap motifs;
- small-modulus residue transition counts;
- fixed-block occupancy extrema.

It is a plumbing and observation-baseline experiment, not a novelty experiment.
