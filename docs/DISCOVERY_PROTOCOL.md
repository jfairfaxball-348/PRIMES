# Discovery Protocol

## 1. Purpose

This protocol is designed to reduce two common failure modes in computational mathematics:

1. overfitting a pattern to the range on which it was noticed;
2. unconsciously steering the search toward known theory and then mistaking rediscovery for novelty.

## 2. Data partition

Every promoted experiment must identify three disjoint numerical regions before result inspection:

- **discovery range** — feature generation and candidate noticing;
- **holdout range** — one-shot replication;
- **adversarial range** — a later and/or structurally chosen range used to attack surviving claims.

Because prime statistics change with scale, contiguous later ranges are usually more meaningful than random row splits.

The exact boundaries belong in the experiment record.

## 3. Representation declaration

Before a blind scan, list the allowed primitive objects and transforms.

Example primitives:

- prime values `p_n`;
- indices `n`;
- gaps `p_{n+1}-p_n`;
- finite differences;
- residues modulo declared moduli;
- occupancy of declared intervals;
- local windows of declared length.

Derived features may be composed only according to the predeclared grammar for that experiment.

If a new transform is invented after seeing the holdout, the holdout is contaminated for that transform.

## 4. Pattern classes

A scan may search for:

- exact equalities or inequalities;
- forbidden finite configurations;
- repeated symbolic motifs;
- monotone/extremal behaviour;
- recurrence;
- invariance under a transform;
- conditional distribution shifts;
- cross-scale persistence;
- unexpectedly low description complexity.

Statistical signals are observation generators only. Promotion requires a mathematical translation.

## 5. Null and artifact checks

Before promotion, test whether the feature is explained by:

- parity;
- residues modulo small primes;
- the wheel used by the prime generator;
- fixed-window edge effects;
- sorting or rank effects;
- duplicated information in correlated features;
- a deterministic consequence of definitions;
- finite sample sparsity.

Where useful, compare against synthetic controls that preserve obvious constraints, such as a shuffled gap multiset. Such controls diagnose artifacts; they are not number-theoretic models.

## 6. Observation promotion

An observation gets an `OBS-###` ID only if:

- it has an exact definition;
- the generating experiment is reproducible;
- the discovery range is recorded;
- the holdout was not used to tune it;
- it is not immediately trivial.

Replicated observations may later seed candidates.

## 7. Candidate promotion

A candidate gets a `CAND-###` ID only if it is a falsifiable mathematical statement and survives at least one untouched holdout.

Candidates should normally be phrased at multiple strengths:

- minimal statement supported by evidence;
- natural structural statement;
- strongest tempting statement.

This helps detect where the real boundary lies.

## 8. Falsification first

For each candidate, spend computational effort first on the range or construction most likely to break it, not on accumulating easy confirmations.

Record the first counterexample exactly.

## 9. Mechanism requirement

A candidate that survives computation but has no plausible mathematical mechanism is not ready for proof-scale investment.

The mechanism may be incomplete, but it should identify what structural constraint could make the phenomenon true.

## 10. Reproducibility

Promoted results must record:

- code commit;
- command;
- parameters;
- environment assumptions;
- exact range;
- output artifact or digest;
- interpretation;
- known limitations.
