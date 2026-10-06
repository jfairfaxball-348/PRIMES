# E001 — Frozen Baseline Representation Grid

**Stage:** discovery  
**Queue item:** SQ-001  
**Status:** FROZEN / NOT YET EXECUTED  
**Freeze date:** 2026-10-06

This file freezes the E001 search grammar and numerical partition before any E001 result is generated or inspected. Any later change to a representation, parameter, range, ranking rule, or event definition creates a new experiment/version and cannot reuse the untouched E001 holdout for that changed feature.

## Purpose

Run a broad exact descriptive sweep over several primitive representations of the prime sequence without selecting a known theorem or conjecture in advance.

E001 is an observation generator only. It may produce exact observations. It must not directly produce a conjecture.

## Frozen numerical partition

All ranges are half-open value intervals.

- **Discovery D0:** `[0, 1_000_000)`
- **Untouched holdout H0:** `[1_000_000, 2_000_000)`
- **Reserved adversarial A0:** `[10_000_000, 11_000_000)`

The next E001 execution unit may generate and inspect **D0 only**. H0 must not be generated or inspected until any proposed observation has been stated exactly, with its replication criterion frozen in the observation ledger. A0 remains reserved for later hostile testing.

For band-local sequential representations, only primes inside the selected band participate. Gaps, finite-difference windows, motifs, and residue transitions that would cross a band boundary are excluded.

## Frozen representation grid

### G1 — Gap motifs

Primitive: consecutive prime gaps within the band.

Widths:

`2, 3, 4, 5, 6`

For each width, record the complete exact motif-count table and a deterministic top-20 convenience ranking. Complete tables are sorted lexicographically by motif. Rankings are sorted by descending count and then by the repository's deterministic representation-key rule.

No normalization or thresholding is permitted in E001.

### G2 — Higher finite differences

Primitive: prime values in the band.

Forward-difference orders:

`1, 2, 3, 4`

For each order, record:

- sequence length;
- minimum and maximum value;
- zero count;
- complete exact value-frequency table;
- deterministic top-20 value ranking.

No fitted trend, scaling law, smoothing, or magnitude binning is permitted in E001.

### G3 — Residue transitions

Primitive: directed transitions between residues of consecutive in-band primes.

Frozen moduli:

`6, 10, 12, 30, 60`

For each modulus, use `reduced_residues_only=True`: prime divisors of the modulus are excluded before residues are formed. Record the complete directed transition-count table and deterministic top-20 ranking.

The modulus family is a fixed search grid, not a claim of special significance.

### G4 — Occupancy scales

Primitive: exact counts of primes in globally anchored half-open value blocks.

Frozen block widths:

`100, 1_000, 10_000, 100_000`

Blocks are `[k*w, (k+1)*w)`. The frozen band boundaries are multiples of every declared width, so E001 contains no partial edge blocks.

For each width, record the complete ordered occupancy vector plus the first minimum and first maximum block under the repository's deterministic tie rule.

### G5 — Event-centred neighbourhoods

E001 event class: **strict global record prime gaps only**.

A gap is a strict global record if it is larger than every earlier prime gap in the full prime sequence. Select an event into a band only when both endpoints of the record gap lie inside that band.

Frozen neighbourhood radii in gap coordinates:

`2, 4, 8`

For radius `r`, serialize the raw gap word containing `r` gaps before the record gap, the record gap itself, and `r` gaps after it. The record gap occupies the unique centre position. Omit an event at a band edge if the full neighbourhood is not contained in the band, and record the omission count.

Prime-dense and prime-sparse occupancy events are deliberately deferred to SQ-003; they are not part of E001 and cannot be introduced after D0 inspection.

## Determinism and artifact rules

1. Exact integer arithmetic only.
2. No randomness.
3. JSON output must use stable key ordering.
4. Complete counter tables must use a frozen deterministic serialization order.
5. Repeating the same command on the same commit must produce byte-identical output.
6. The generated artifact must include the experiment ID, code commit, band name, exact half-open range, and all grid parameters.
7. A SHA-256 digest of each generated artifact must be recorded.

## Discovery and promotion firewall

The first execution of E001 must be limited to D0.

After D0 inspection, a possible phenomenon can receive an `OBS-###` entry only when its exact definition, discovery evidence, triviality checks, and one-shot H0 replication criterion are frozen. Only then may H0 be generated for that observation.

No feature may be tuned using H0. If a definition changes after H0 is inspected, H0 is contaminated for that changed definition.

No `CAND-###` may be created unless an exact observation has already survived an untouched holdout.

## Stop rule for this preflight

This preflight ends when this representation grid and partition are committed. It does **not** execute E001 and does **not** inspect D0, H0, or A0 E001 results.
