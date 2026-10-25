Continue from the committed RS-S010 handover (main = `18bb011`). Read `reciprocity_spectra/PROTOCOL.md` (including section 9, owner decisions of 2026-10-25), `reciprocity_spectra/LEDGER.md`, `reciprocity_spectra/CONJECTURES.md` (RS-7b, RS-8, RS-9 and the RS-S010 correction), `reciprocity_spectra/ASTRA_RESPONSE_2026-10-25.md` and this prompt. Work on `ccr-c363c6bb-0zejeu`; do not merge without owner instruction.

ONE BOUNDED UNIT: RS-S011, the selection table, then freeze CAND-001 and draft the hard-version proof route.

1. Exact: (Z[w]/4)^x (order 12, = F4^x x C2 x C2) restricted to the classes of primary rho; enumerate its 12 characters; test exactly that (conj rho/rho)_6, (2/rho)_3 and g2~ are functions of rho mod 4 and which characters they are.
2. EXPLORATORY: prime-level biases B(j, chi) = |sum_rho g6_trace(zeta6^j, rho) chi(rho)/sqrt(p)| / sqrt(count) for all 6 x 12 pairs, at X = 8e4 .. 1.28e6 (magnitude ratios, not slopes); identify the main-term pairs and the exact rule.
3. Register the table, then test it at a fresh norm window (e.g. primes with 1.28e6 < p <= 1.92e6 via an engine minimum-norm option), within ~45 minutes per job.
4. Freeze CAND-001 in `research/CONJECTURE_REGISTER.md` (first CAND ever allocated; use the template): the prime-level selection rule and its matrix consequence (RS-7b), with exact statement, definitions, evidence, triviality checks and prior-art status.
5. Write `reciprocity_spectra/PROOF_ROUTE.md` for the HARD version first (PROTOCOL section 9): reduce the matrix dichotomy to prime-level twisted sextic Gauss-sum asymptotics (Astra's exact formula ||C w_u||^2 = sum_pi |S(pi u)|^2); a Heath-Brown/Vaughan decomposition into Type I (twisted Kubota series residues; the selection rule) and Type II (bilinear sextic sums; compare the sextic large sieve with what Dunn-Radziwill needed for n = 3); list every required input, which are known (with citations), conditional, or open. The tractable versions are fallbacks only.

Keep jobs within about 45 minutes, push checkpoints serially, never commit large data, run Ruff on touched files and pytest. Close out under PROTOCOL section 7 with exactly one justified next prompt.
