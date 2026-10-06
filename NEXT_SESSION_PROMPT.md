Read "PROGRAM_STATUS.md", "PROJECT_CHARTER.md", "AGENTS.md", "docs/SESSION_PROTOCOL.md", "research/SESSION_LEDGER.md", "research/SEARCH_QUEUE.md", "research/OBSERVATION_LEDGER.md", "research/CONJECTURE_REGISTER.md", "research/FAILURE_LEDGER.md", "experiments/E000_PREFLIGHT_2026-10-06.md", and "experiments/E001_REPRESENTATION_GRID.md" before changing anything.

Continue PRIMES at DISCOVERY-0.

Your bounded task is D0-03 / SQ-001 E001 discovery execution:

1. Treat "experiments/E001_REPRESENTATION_GRID.md" as frozen. Do not change its representation parameters, ranking rules, event definitions, or numerical ranges after inspecting any E001 output.
2. Implement E001 from that frozen specification using exact arithmetic and deterministic serialization.
3. Add tests for band-boundary exclusion, globally anchored occupancy blocks, strict global record-gap event selection, deterministic counter ordering, and byte-deterministic output.
4. Run the appropriate validation suite. If a local tool is unavailable, record the exact environment failure without misclassifying it as a repository/data defect, and use available GitHub CI evidence where appropriate.
5. Execute E001 on discovery D0 = [0, 1_000_000) only, repeat it to verify byte determinism, and record a SHA-256 digest of the discovery artifact.
6. Inspect the D0 artifact only. You may promote at most 10 exact, reproducible, non-immediately-trivial observations to "research/OBSERVATION_LEDGER.md". For every promoted observation, freeze its exact definition, discovery evidence, triviality checks, and one-shot H0 replication criterion before any holdout execution.
7. Do not generate or inspect H0 = [1_000_000, 2_000_000) or A0 = [10_000_000, 11_000_000) in this session.
8. Do not create a conjecture or candidate. A candidate remains forbidden until an exact observation has survived an untouched holdout.
9. Record implementation/data/plumbing failures in "research/FAILURE_LEDGER.md" and update "research/SEARCH_QUEUE.md" and authoritative programme state to match the actual result.

At the natural completion of this bounded unit, follow "docs/SESSION_PROTOCOL.md": validate and checkpoint useful work, update the session ledger, and automatically finish.

If unblocked, replace "NEXT_SESSION_PROMPT.md" with exactly one immediately runnable next-session prompt consistent with the new committed state and include that same prompt in the closeout. If a genuine owner decision blocks continuation, suppress/delete the live prompt and ask only for the exact decision required.