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

The D0-02 preflight reproduction, deterministic output digests, and independent sieve cross-check are recorded in `E000_PREFLIGHT_2026-10-06.md`.

## E001 — Frozen baseline representation grid

`E001_REPRESENTATION_GRID.md` freezes the SQ-001 search grammar before any E001 result is generated or inspected.

It covers:

- gap motifs of widths 2 through 6;
- finite differences through order 4;
- residue transitions for moduli 6, 10, 12, 30, and 60;
- occupancy widths 100, 1,000, 10,000, and 100,000;
- strict global record-gap neighbourhoods at radii 2, 4, and 8.

Its discovery range is `[0, 1_000_000)`; its untouched holdout is `[1_000_000, 2_000_000)`; and its reserved adversarial range is `[10_000_000, 11_000_000)`.

E001 has not yet been executed. The first execution unit may inspect the discovery range only.
