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
