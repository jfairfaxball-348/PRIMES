# Historical Rediscovery Calibration

PRIMES needs a way to test whether its discovery machinery is capable of finding deep structure at all.

This lane is separate from the novelty lane.

## Principle

Take a phenomenon that is already understood, hide the mature terminology and solution from the active experiment specification, and ask whether the same discovery pipeline would generate useful intermediate objects from raw prime data.

After the experiment is frozen, unblind the historical theory and compare:

- what was noticed;
- which representation changes were invented;
- where the pipeline stalled;
- which missing idea would have been needed;
- whether the discovered object was genuinely compressive or merely descriptive.

## Generic process hardening

These rules apply to future calibration designs only. They do not reopen or retrofit a completed benchmark.

### Representation-switch trigger

A calibration specification should make the boundary of each representation family explicit. If a frozen family produces nontrivial compression on development data but then fails one or more predeclared assessment, holdout, or residual-persistence criteria intended to test generalization, freeze that family as failed or partial at the declared criterion. Do not repair it using inspected assessment output by changing transforms, coefficients, thresholds, residual grammar, aggregation rules, or targets.

If further calibration work is justified, continue only through a separately frozen stage using a qualitatively different representation family, with its primitive objects, transform grammar, selection rules, diagnostics, and untouched assessment data declared before execution. The reason for the switch must be target-agnostic: failure of the existing representation to generalize is enough; the hidden historical solution is not.

Once a benchmark has been historically unblinded, no newly invented target-specific stage on that benchmark counts as blinded rediscovery. Only target-agnostic process lessons may transfer to later calibration tasks or to the novelty methodology.

### Scoring-design safeguards

Whenever a calibration selector aggregates performance across multiple widths, scales, strata, views, or other subproblems, the specification must predeclare both the per-subscale metric and the global aggregation rule.

The committed calibration record must expose enough diagnostics that one subscale cannot silently determine the winner:

- serialize each candidate's per-subscale score or contribution, not only the aggregate;
- identify the subscale or subscales that attain a worst-case/max aggregate or otherwise contribute most strongly under the frozen rule;
- predeclare at least one influence diagnostic that is not used to retune the winner, such as leave-one-subscale-out re-ranking, or an equivalent contribution-share diagnostic for an additive score;
- explicitly flag a selection as subscale-sensitive when removing one subscale changes the winner or when the declared aggregate advantage is supported only by one subscale.

These diagnostics describe selector fragility; they do not change the frozen winner unless the selection rule itself said so before assessment. After assessment inspection, removing, reweighting, normalizing, or replacing a subscale creates a new calibration design/version and requires fresh untouched assessment data.

## Riemann-style benchmark

The benchmark is not "rediscover the zeta function."

Instead, beginning from prime counts and elementary derived data, ask whether the process naturally learns to:

1. compare counts across scale;
2. separate leading behaviour from residual behaviour;
3. seek transforms or alternative representations of the residual;
4. prefer representations that unify several observations;
5. formulate exact structural questions from those representations.

Any known result used in this calibration lane is permanently excluded from novelty promotion.

## Other calibration tasks

Later calibration tasks may use known prime phenomena with very different signatures: local residue structure, gap phenomena, arithmetic progressions, or extremal events.

The calibration suite should remain small. Its purpose is to test the method, not consume the research programme.
