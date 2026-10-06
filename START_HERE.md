# START HERE

PRIMES is currently in **DISCOVERY-0**.

The immediate objective is to establish a trustworthy observation pipeline before making any mathematical claim.

## Session protocol

The controlling closeout rules are in `docs/SESSION_PROTOCOL.md`. Each session runs one bounded research unit and finishes automatically at a natural checkpoint.

For each bounded research session:

1. Read `PROGRAM_STATUS.md` and the ledgers.
2. State one exact question.
3. Classify the session stage.
4. Freeze the input range, transforms, parameters, and holdout before inspecting results.
5. Run the smallest experiment that can answer the question.
6. Record observations, including negative ones.
7. Try the obvious triviality/sieve explanations.
8. If the observation is interesting, replicate it on untouched data.
9. Promote only exact, falsifiable statements.
10. Update the authoritative ledgers before ending.
11. If unblocked, write one immediately runnable `NEXT_SESSION_PROMPT.md` and include it in the closeout.
12. If an owner decision is required, suppress the next-session prompt and ask only for that decision.

## DISCOVERY-0 task sequence

The first programme sequence is:

- **D0-01** — validate prime generation and elementary transforms;
- **D0-02** — run E000 baseline scan and record the first observation bundle;
- **D0-03** — define a controlled representation grid for the initial search atlas;
- **D0-04** — run independent discovery/holdout scans across that grid;
- **D0-05** — promote at most five observations for hostile falsification.

No conjecture should be created merely to fill the register.

## What to run locally

```bash
python -m pip install -e ".[dev]"
pytest
python experiments/E000_baseline_scan.py --limit 100000
```

For a larger baseline, increase `--limit`, but do not confuse scale with novelty.

## Current gates

- Discovery gate: **OPEN**
- Replication gate: **OPEN** once an observation exists
- Conjecture gate: **CLOSED until an observation survives holdout**
- Collision-audit gate: **CLOSED until a candidate exists**
- Proof gate: **CLOSED**
- Publication gate: **CLOSED**

See `ROADMAP.md` for the graduation criteria.
