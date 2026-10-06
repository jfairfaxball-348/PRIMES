Read "PROGRAM_STATUS.md", "PROJECT_CHARTER.md", "AGENTS.md", "docs/SESSION_PROTOCOL.md", "research/SESSION_LEDGER.md", "research/SEARCH_QUEUE.md", "research/OBSERVATION_LEDGER.md", "research/CONJECTURE_REGISTER.md", "research/FAILURE_LEDGER.md", "experiments/E001_REPRESENTATION_GRID.md", "experiments/E001_D0_DISCOVERY_2026-10-06.md", and "research/evidence/E001_D0_observations.json" before changing anything.

Continue PRIMES at DISCOVERY-1.

Your bounded task is D1-01 / SQ-001 one-shot E001 H0 replication:

1. Treat "experiments/E001_REPRESENTATION_GRID.md" and the exact definitions/replication criteria of OBS-001 through OBS-004 in "research/OBSERVATION_LEDGER.md" as frozen. Do not tune any definition, threshold, ranking rule, modulus, occupancy width, or criterion after seeing H0.
2. Use the exact E001 implementation semantics from commit "beab213501dab318075199c3fcac6d5501d0b9d3". Before generating H0, verify that the executable E001 source you run is byte-equivalent to that committed implementation or reconstruct it directly from that ref.
3. Run the appropriate validation suite before holdout generation. If an implementation-semantic defect is discovered, do not generate H0; record the defect and close on a correction task. If only the known local Ruff/CI-observability limitation recurs, record/reuse it without misclassifying it as a repository defect.
4. Generate E001 only for untouched H0 = [1_000_000, 2_000_000). You may repeat the identical H0 command solely to verify byte determinism. Record the H0 artifact SHA-256 digest.
5. Inspect H0 only against the four frozen criteria:
   - OBS-001 replicates iff third forward difference value 0 is the unique modal value.
   - OBS-002 replicates iff width-2 gap motif [6, 6] is the unique modal motif.
   - OBS-003 replicates iff directed reduced-residue transition support is complete for every frozen modulus, with support sizes 4, 16, 16, 64, and 256 for moduli 6, 10, 12, 30, and 60.
   - OBS-004 replicates iff every globally anchored width-100 H0 block has occupancy at least 1.
6. Do not mine H0 for new observations or inspect unrelated H0 rankings/extrema beyond what is necessary to evaluate those criteria. Do not generate or inspect A0 = [10_000_000, 11_000_000).
7. Update each observation to REPLICATED or REFUTED with exact H0 evidence. For any failed criterion, record the exact competing mode, missing transition pair(s), or first empty block as applicable.
8. Do not create a conjecture/candidate, perform a prior-art search, or start mechanism work in this session even if an observation replicates. Candidate synthesis, if justified, is a separate later bounded unit.
9. Update "research/SEARCH_QUEUE.md", "PROGRAM_STATUS.md", "research/FAILURE_LEDGER.md" as applicable, and add a bounded H0 replication record plus compact machine-readable evidence.

At the natural completion of this bounded unit, follow "docs/SESSION_PROTOCOL.md": validate and checkpoint useful work, update the session ledger, and automatically finish.

If unblocked, replace "NEXT_SESSION_PROMPT.md" with exactly one immediately runnable next-session prompt consistent with the new committed state and include that same prompt in the closeout. If a genuine owner decision blocks continuation, suppress/delete the live prompt and ask only for the exact decision required.
