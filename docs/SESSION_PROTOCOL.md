# Autonomous Session Protocol

This protocol governs how PRIMES research sessions start, execute, checkpoint, and finish.

The goal is for each session to behave like a bounded autonomous research unit rather than an open-ended chat.

## 1. Enter from committed authority

At the start of every serious session:

1. read `PROGRAM_STATUS.md`;
2. read `PROJECT_CHARTER.md`;
3. read `AGENTS.md`;
4. read `research/SESSION_LEDGER.md`;
5. read the active observation/candidate/search records relevant to the task;
6. read `NEXT_SESSION_PROMPT.md` if it exists.

The committed repository is authoritative. Conversation history can help interpret intent, but it is not the project state.

If the kickoff prompt disagrees with newer committed authority, reconcile the mismatch explicitly and follow the newer valid state.

## 2. Run one bounded research unit

A session should have one primary bounded objective.

Examples include:

- run one frozen discovery sweep;
- replicate one observation on untouched data;
- falsify one candidate family;
- derive one mechanism lemma;
- perform one bounded prior-art collision audit;
- design and freeze one experiment;
- resolve one computational or methodological dependency.

Do not manufacture extra work merely because time remains.

Use reasonable judgement for implementation, computation, documentation, and research decisions that are already within the agreed scope. Do not repeatedly ask the owner to authorize routine reversible steps.

## 3. Natural completion rule

A session ends when the bounded objective has reached a natural checkpoint.

A natural checkpoint is one where the next useful action is materially different from the current unit, for example:

- an experiment has been run and interpreted;
- an observation has been promoted, refuted, or explained;
- a candidate has survived or failed its assigned stress test;
- a representation grid has been frozen;
- a proof route has reached a clearly stated lemma or obstruction;
- a prior-art audit has reached a bounded conclusion;
- a blocker has been isolated precisely.

Do not continue indefinitely into the next research unit simply because it is possible.

## 4. Blocker classification

Before closing, classify any unresolved dependency.

### Ordinary blocker

An ordinary blocker is something the session can resolve within its existing authority, such as:

- a code defect;
- a missing test;
- a reproducibility issue;
- a source that can be checked directly;
- a failed experiment requiring a revised but still in-scope test;
- a routine methodological choice already governed by project rules.

Resolve ordinary blockers before closing whenever practical.

### Owner decision blocker

An owner decision blocker exists only when meaningful continuation requires a genuine choice or authorization that the project rules do not determine.

Examples:

- choose between materially different research targets;
- approve a change to the project charter or discovery firewall;
- decide whether to abandon, pause, or graduate a major direction when evidence supports multiple reasonable paths;
- authorize an external action outside the standing project scope;
- supply unavailable information that cannot be inferred safely.

Do not label ordinary uncertainty as an owner blocker.

## 5. Closeout obligations

Before a session finishes, update the durable project state as applicable:

- `PROGRAM_STATUS.md`;
- `research/SESSION_LEDGER.md`;
- `research/OBSERVATION_LEDGER.md`;
- `research/CONJECTURE_REGISTER.md`;
- `research/FAILURE_LEDGER.md`;
- `research/SEARCH_QUEUE.md`;
- experiment records and generated evidence;
- relevant documentation.

Record:

- what bounded task was attempted;
- what changed mathematically or computationally;
- what was validated;
- what failed;
- what remains uncertain;
- the exact next dependency.

A large quantity of notes is not a progress claim. State the actual research result.

## 6. Automatic next-session prompt

If the session is unblocked and there is a clear next bounded research unit, the session must automatically:

1. update `NEXT_SESSION_PROMPT.md` with exactly one immediately runnable prompt;
2. ensure that prompt is consistent with the newly committed state;
3. include the same prompt in the conversational closeout;
4. finish without waiting for the owner to say "wrap up", "finish", or "what next?".

The prompt must contain enough context for a fresh session to begin from the repository alone.

It should specify:

- files to read first;
- current programme stage;
- one bounded objective;
- constraints and stop rules;
- validation requirements;
- expected closeout behaviour.

It must not depend on unstated approval.

## 7. Decision-blocker suppression rule

If an owner decision blocker is active:

1. checkpoint all useful work first;
2. update `PROGRAM_STATUS.md` with the blocker;
3. record the blocker in `research/SESSION_LEDGER.md`;
4. delete or suppress the live `NEXT_SESSION_PROMPT.md`;
5. do **not** provide a conditional, placeholder, or "after you decide" next-session prompt;
6. end by asking for exactly the decision or information required.

The closeout should make the available options and consequences clear enough for the owner to decide without reconstructing the session.

Once the owner resolves the blocker, the next session may restore `NEXT_SESSION_PROMPT.md`.

## 8. Natural programme-completion rule

If a programme stage or the entire programme has genuinely completed and there is no justified next research unit, close cleanly.

Do not invent a new task merely to satisfy the automatic-prompt rule.

Record the completion state and leave no live next-session prompt unless a real continuation has been defined.

## 9. Validation before close

Run checks appropriate to the work performed.

For code changes, this normally includes:

```bash
ruff check .
pytest
```

and the relevant experiment smoke or reproduction command.

For mathematical or literature work, validate definitions, source boundaries, computations, and consistency with the authoritative records.

Documentation checks do not validate mathematical truth.

## 10. Final conversational closeout

After a useful checkpoint has been committed, finish automatically.

The closeout should be concise and include:

- session outcome;
- important mathematical/computational result;
- validation performed;
- commit or repository state;
- remaining limitation.

Then:

- **if unblocked:** include exactly one copyable next-session prompt;
- **if owner-blocked:** include only the exact owner decision request and no next-session prompt;
- **if naturally complete:** state completion and do not manufacture a prompt.

This is a conversational handover protocol, not a background automation. The next research session begins when the owner opens or pastes the emitted prompt.

## 11. Observation-to-synthesis disposition links

When a bounded synthesis-only triage ends, keep the frozen representation, observation definition, holdout target and criterion unchanged. Record the candidate disposition in the conjecture register (including **NO CANDIDATE CREATED** when appropriate) and link each considered observation's **Candidate link** field to that synthesis result without changing its REPLICATED status unless a separately justified lifecycle transition has actually occurred. Documentation links are not new evidence or permission to reuse a consumed holdout.

The D1-41 / SQ-013 example is `OBS-018` and `OBS-019` in `research/OBSERVATION_LEDGER.md`, both retaining REPLICATED and linking to `experiments/E013_D1_41_SYNTHESIS_2026-10-08.md` and `research/CONJECTURE_REGISTER.md`. This cross-reference does not authorize further D13/H13 analysis, A13 execution or an E013 criterion change.
