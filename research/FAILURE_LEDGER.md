# Failure and Lesson Ledger

Failures are research outputs. Preserve them so the project does not repeatedly rediscover the same dead ends.

### FAIL-001

**Date:** 2026-10-06  
**Related observation/candidate/experiment:** D0-02 / E000 preflight  
**Idea attempted:** Reproduce the repository's CI validation path in an isolated local runner after reconstructing the exact committed E000/core/test sources.  
**Why it looked plausible:** The repository declares Ruff and pytest as development dependencies, and the bounded task required validation in addition to checking the committed CI record.  
**Failure mode:** other — execution-environment plumbing  
**Exact evidence:** Direct `git clone` from the isolated runner failed because that runner could not resolve `github.com`; the source was therefore reconstructed through the GitHub repository API. In the reconstructed tree, `ruff --version` and `ruff check .` failed with `ruff: command not found` (exit status 127). GitHub programme authority already records Ruff, pytest, package installation, and the E000 smoke run as passed at validated CI head `e47b272b6e3867fb10d0eefc199b1231557659da`. Local `pytest` still passed 9/9 tests, repeated E000 outputs at limits 10,000 and 100,000 were byte-identical, and an independent trial-division generator exactly matched the repository sieve at both limits.  
**Lesson:** Connector-backed research sessions must not assume that a detached execution runner has network access or every repository dev tool installed. Separate session-environment failures from repository/data failures, and preserve the authoritative CI evidence when local reproduction is partial.  
**What remains valid:** No E000 data-quality defect was found. The exact committed Python sources execute correctly under pytest and produce deterministic E000 summaries at both declared preflight limits.  
**Do-not-repeat condition:** Check runner network/tool availability before chaining validation commands; when Ruff is absent, do not misclassify that as a code failure, and use the committed GitHub Actions Ruff result unless a runnable lint environment is available.

### FAIL-002

**Date:** 2026-10-06  
**Related observation/candidate/experiment:** D0-03 / E001 discovery execution  
**Idea attempted:** Reproduce the repository's full lint/test validation path locally for the new E001 implementation and retrieve current-head CI evidence through the available GitHub connector.  
**Why it looked plausible:** E001 adds new Python experiment and test files, and the repository declares Ruff and pytest as development dependencies with a push-triggered CI workflow.  
**Failure mode:** other — execution-environment / CI-observability plumbing  
**Exact evidence:** The detached runner uses Python 3.13.5. `PYTHONPATH=src pytest -q` passed 14/14 tests and `python -m compileall -q src experiments tests` succeeded. `ruff --version` failed with `ruff: command not found` (exit 127), repeating the local-tool limitation seen in FAIL-001. For implementation commit `beab213501dab318075199c3fcac6d5501d0b9d3`, the available GitHub connector returned `statuses: []` from combined-status retrieval and `workflow_runs: []` from its commit-workflow wrapper, which is documented as exposing pull-request-triggered runs only. Those empty responses do not establish either a CI pass or CI failure for the push commit. The last independently recorded green CI head remains `e47b272b6e3867fb10d0eefc199b1231557659da`, predating E001.  
**Lesson:** Do not infer current-head CI state from an empty connector response, and do not misclassify a missing local linter as a repository defect. State exactly which validation was reproduced locally and which CI evidence is unavailable.  
**What remains valid:** All 14 local tests pass; byte-deterministic E001 D0 generation passes; Python compilation succeeds; an independent SymPy prime list exactly matches the repository sieve on D0; no implementation or data-quality failure was found.  
**Do-not-repeat condition:** Unless the runner gains Ruff or the connector exposes push/check-run status, reuse this limitation rather than treating absent objects as CI evidence.

**D1-01 recurrence:** During E001 H0 replication, the detached runner again returned `ruff: command not found` (exit 127). The connector again returned empty combined-status and PR-triggered workflow-run collections for both the frozen E001 implementation commit `beab213501dab318075199c3fcac6d5501d0b9d3` and then-current main head `d087f332239817b128d810c08a75057ffcc1572b`. The exact reconstructed E001 source matched the committed blob, pytest passed 14/14, and compilation succeeded before H0 generation. This is a recurrence of FAIL-002, not a new failure ID or repository defect.

## Template

### FAIL-###

**Date:**  
**Related observation/candidate/experiment:**  
**Idea attempted:**  
**Why it looked plausible:**  
**Failure mode:** counterexample / trivial consequence / artifact / prior-art collision / computational flaw / non-reproducible / no mechanism / other  
**Exact evidence:**  
**Lesson:**  
**What remains valid:**  
**Do-not-repeat condition:**
