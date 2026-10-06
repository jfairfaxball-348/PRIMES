# PRIMES

A long-horizon experimental mathematics programme for discovering, stress-testing, and eventually proving genuinely interesting structure in the primes.

**Current stage: BOOTSTRAP / DISCOVERY-0. No novelty claim, conjecture claim, or theorem claim is currently active.**

Start every serious session at [START_HERE.md](START_HERE.md), then read [PROJECT_CHARTER.md](PROJECT_CHARTER.md) and [AGENTS.md](AGENTS.md).

## Mission

The aim is not to make another catalogue of known facts about primes. The aim is to build a disciplined discovery system that can:

1. generate exact prime data and derived structures;
2. search for reproducible patterns across many representations and scales;
3. turn persistent patterns into sharply stated candidate conjectures;
4. attack those candidates with adversarial computation and proof attempts;
5. only then perform bounded prior-art and novelty audits;
6. preserve failures, collisions, and counterexamples as research outputs; and
7. graduate the rare surviving candidate into a separate theorem/proof programme.

The desired endpoint is a mathematically meaningful contribution that was *found*, not selected in advance.

## The core idea: discovery before recognition

Prime research is saturated with deep theory. That creates a serious methodological danger: if we begin by reading the famous results and then search nearby, we are likely to rediscover their neighbourhood rather than find white space.

PRIMES therefore separates two activities.

### Blind discovery mode

During candidate generation we deliberately emphasize observations that can be defined directly from the prime sequence, arithmetic operations, finite combinatorial transforms, local statistics, and exact computation. Famous theories may be used as controls, but they do not define the search direction.

The question is:

> If the existing conceptual map were hidden, what regularities would force us to invent new objects, transforms, or language?

### Collision mode

Once a candidate survives internal falsification, we stop treating ignorance as evidence. We search the literature and databases for:

- the exact statement;
- equivalent formulations;
- stronger results implying it;
- the same invariant under different terminology;
- the same phenomenon in a broader theory;
- known counterexamples;
- proof mechanisms that make the candidate routine.

A negative search is never a novelty proof. Search scope and uncertainty are recorded.

## Riemann as a methodological case study, not a destination

We do **not** set out to reproduce Riemann's work.

Instead we ask what discovery process could have made a leap of that kind possible if the answer were unknown:

- measure the object at increasing scales;
- compare raw counts with simple baselines;
- study the residual/error rather than only the leading trend;
- invent transforms that compress arithmetic structure into analyzable structure;
- look for dual descriptions of the same data;
- notice when a representation exposes hidden regularity;
- formulate a structural conjecture only after the phenomenon survives changes of scale and representation;
- use computation to seek the mechanism, not merely more confirming examples.

See [docs/RIEMANN_AS_METHOD.md](docs/RIEMANN_AS_METHOD.md).

## Research architecture

The programme treats each promising observation as moving through a one-way evidence pipeline:

```text
raw primes
   -> derived representations
   -> pattern observations
   -> replicated phenomena
   -> candidate conjectures
   -> adversarial falsification
   -> mechanism search
   -> prior-art collision audit
   -> graduate / collide / refute / archive
```

Candidate history is append-only. Failed ideas are not deleted.

## Initial search atlas

The first phase deliberately spans multiple views of the primes rather than betting on one fashionable area.

### A. Local geometry of the prime sequence

Gap words, higher finite differences, runs, reversals, motifs, record events, dense and sparse windows, and scale-normalized local signatures.

### B. Cross-scale structure

How local prime configurations change as the observation window, normalization, or coarse-graining scale changes. We will look for features that are stable under scale changes rather than artifacts of a fixed cutoff.

### C. Residue dynamics

Not merely prime counts in residue classes, but transition structure, motif structure, conditional behaviour, and changing-modulus fingerprints of consecutive primes.

### D. Index/value duality

Patterns created by treating prime index and prime value symmetrically: derived subsequences, inverse lookup structure, compositions, and iterated transforms. These are high-collision-risk areas and must be novelty-audited aggressively.

### E. Error and residual structure

Whenever a simple baseline captures a first-order trend, study the residual as a first-class object: sign patterns, excursions, extrema, recurrence, local predictability, spectral or combinatorial structure, and cross-scale dependencies.

### F. Prime configurations as finite objects

Represent bounded prime neighbourhoods as words, graphs, point clouds, occupancy vectors, or finite metric objects, then search for invariants and forbidden/rare configurations.

### G. Description-length and predictability tests

Use compression, entropy, symbolic complexity, and out-of-sample prediction only as *pattern detectors*. Apparent predictability is not treated as mathematics until translated into an exact statement.

The atlas will grow only when a new representation is mathematically distinct.

## What counts as a useful pattern?

A pattern becomes interesting only if it clears several filters:

- **exactly definable** — it can be stated without relying on a plot;
- **replicable** — it persists on unseen ranges or independent samples;
- **nontrivial** — it is not an immediate parity/residue/sieving artifact;
- **stable** — it survives reasonable changes of cutoff, binning, and normalization;
- **compressive** — it reduces many observations to a smaller structural rule;
- **falsifiable** — there is a clear way to search for counterexamples;
- **mechanism-bearing** — it suggests a mathematical reason, not just a fitted curve;
- **collision-resistant** — after promotion, it survives a serious prior-art audit.

## Evidence discipline

Finite computation can refute universal statements but does not prove them.

Every promoted candidate must record:

- exact statement and definitions;
- discovery data range;
- holdout range;
- tests performed;
- smallest known counterexample search bound;
- known equivalent forms;
- suspected trivial explanations;
- provenance of every external fact;
- novelty-search queries and sources;
- lifecycle status.

See [docs/DISCOVERY_PROTOCOL.md](docs/DISCOVERY_PROTOCOL.md) and [docs/NOVELTY_PROTOCOL.md](docs/NOVELTY_PROTOCOL.md).

## Repository map

```text
PRIMES/
├── README.md
├── START_HERE.md
├── PROJECT_CHARTER.md
├── PROGRAM_STATUS.md
├── ROADMAP.md
├── AGENTS.md
├── docs/
│   ├── DISCOVERY_PROTOCOL.md
│   ├── NOVELTY_PROTOCOL.md
│   ├── RIEMANN_AS_METHOD.md
│   └── RESEARCH_ATLAS.md
├── research/
│   ├── OBSERVATION_LEDGER.md
│   ├── CONJECTURE_REGISTER.md
│   └── FAILURE_LEDGER.md
├── experiments/
│   ├── README.md
│   └── E000_baseline_scan.py
├── src/primes_lab/
│   ├── __init__.py
│   ├── core.py
│   └── patterns.py
├── tests/
├── pyproject.toml
└── .github/workflows/ci.yml
```

## Reproducible baseline

After installation:

```bash
python -m pip install -e ".[dev]"
pytest
python experiments/E000_baseline_scan.py --limit 100000
```

The baseline experiment is intentionally elementary. Its purpose is to validate the data path and generate a first exact observation bundle, not to claim discovery.

## Graduation rule

This repository owns discovery, falsification, provenance, and novelty triage.

If a candidate becomes a serious theorem project, freeze its exact statement and evidence bundle and graduate it to a dedicated repository for proof development, formalisation where useful, manuscript preparation, and publication work. PRIMES keeps the discovery record.

## Current status

The programme is at **DISCOVERY-0**:

- architecture: being bootstrapped;
- computational core: being bootstrapped;
- observation ledger: empty by design;
- active conjectures: none;
- novelty claims: none;
- theorem claims: none.

The first objective is not "find a theorem". It is to build a research machine trustworthy enough that an unexpected pattern has somewhere rigorous to go.
