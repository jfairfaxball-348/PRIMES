# Instructions for PRIMES agents

This file governs automated and human-assisted work in PRIMES.

## First action in every serious session

Read, in order:

1. `PROGRAM_STATUS.md`
2. `PROJECT_CHARTER.md`
3. `research/CONJECTURE_REGISTER.md`
4. `research/OBSERVATION_LEDGER.md`
5. the experiment or candidate record being continued.

## Stage discipline

Label substantive work as one of:

- **discovery** — generate representations and observations;
- **replication** — test an observation on untouched data;
- **falsification** — seek counterexamples or trivial explanations;
- **mechanism** — derive an exact mathematical reason;
- **collision-audit** — check prior art and equivalent formulations;
- **proof** — prove a frozen statement;
- **certification** — independently verify a proof/computation.

Do not blur discovery and collision-audit in a way that lets literature silently steer a supposedly blind experiment.

## Discovery firewall

During a declared blind-discovery experiment:

- start only from the explicitly listed primitive objects and transforms;
- do not choose a feature because it is known to connect to a famous theorem;
- do not inspect the holdout range;
- do not tune thresholds on the holdout range;
- do not rewrite a failed observation out of history;
- label any unavoidable theory-informed choice.

The firewall is methodological, not psychological. It does not claim that an agent has forgotten mathematics.

## Candidate discipline

Every candidate receives a permanent ID of the form `CAND-###`.

A candidate record must include:

- exact statement;
- definitions;
- discovery provenance;
- discovery range;
- untouched holdout range;
- falsification strategy;
- current evidence;
- triviality checks;
- mechanism notes;
- prior-art status;
- lifecycle status.

Allowed lifecycle statuses:

`OBSERVED -> REPLICATED -> CANDIDATE -> STRESSED -> COLLISION_AUDIT -> GRADUATED`

and terminal/side statuses:

`REFUTED`, `TRIVIAL`, `KNOWN`, `DUPLICATE`, `DORMANT`.

Never recycle an ID.

## Evidence rules

1. Prefer exact integer and rational arithmetic.
2. Record random seeds for stochastic controls.
3. Distinguish discovery data from holdout and adversarial data.
4. A chart is supporting evidence only; commit machine-readable outputs for promoted observations.
5. Record the smallest counterexample found, not merely that a run failed.
6. Preserve code and parameters sufficient to reproduce promoted evidence.
7. Never report a computational bound without stating precisely what was checked.

## Novelty rules

Do not say "new", "novel", "open", "unknown", or "first" from memory or from a failed search.

Use the statuses:

- `UNAUDITED`
- `SEARCHED_NO_COLLISION_FOUND`
- `POSSIBLE_OVERLAP`
- `KNOWN_EQUIVALENT`
- `KNOWN_IMPLIED`
- `NOVELTY_REQUIRES_EXPERT_REVIEW`

A candidate can graduate with the last status, but the uncertainty must remain explicit.

## Pattern-mining rules

When a pattern is found, ask in this order:

1. Is it forced by parity?
2. Is it forced by small-modulus sieving?
3. Is it forced by the way the feature was encoded?
4. Does it survive a disjoint numerical range?
5. Does it survive a much later range?
6. Does it survive a reasonable normalization change?
7. Can it be stated exactly?
8. What would a counterexample look like?
9. What mechanism could produce it?
10. Only after those checks: has it already been studied?

## Graduation rule

PRIMES is discovery infrastructure. A serious surviving theorem candidate should be frozen and exported to a dedicated proof repository rather than allowing this repository to become an unbounded proof-development tree.
