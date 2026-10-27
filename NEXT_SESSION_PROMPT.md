Run RS-S029 as a CLOUD Lean-formalisation session on a fresh branch from main of jfairfaxball-348/PRIMES. Authoritative main overrides chat history. Do not inspect or modify the paused D1 records.

PLAN OF RECORD (owner, 2026-10-27): proof work on CAND-002 is OUT of the pipeline (parked, optional, not a gate). Formalise what is exact; everything else stays conjecture. Route: Lean -> Palomar -> paper -> arXiv -> journal. Novelty and external review are owner-run and not gates. Do NOT attempt to prove CAND-002 or its asymptotics.

READ FIRST: reciprocity_spectra/PROTOCOL.md sections 7-10 (section 9.6 is revised); reciprocity_spectra/RELEASE_INVENTORY.md, section "Plan of record" (the work list for this session is (A')); formalisation/README.md; all formalisation/ReciprocitySpectra/*.lean (Sextic, Gauss, CharacterBridge, Model, Conjecture); formalisation/Checks/*.lean. Context only: RS_HP_SCALE_ERRATUM.md and RS_S026_PRIME_MOMENT_BRIDGE.md sections 1-2 (the paper statements of the row and Gram identities).

SETUP (cloud; same method as the owner's Almost-Stacked-Proof formal/):
- Run `bash formalisation/cloud_setup.sh`. It installs elan and the pinned toolchain leanprover/lean4:v4.35.0, runs `lake exe cache get` for Mathlib 56a005855ea17e0b0958f73ec801ae140b0a1679, and builds ReciprocitySpectra and Checks.
- Never run `lake update`, never change the pins, never commit `.lake/`.
- BASELINE before any edit:
  - both targets build;
  - Checks prints only [propext, Classical.choice, Quot.sound] (res_mul uses fewer);
  - faithfulness prints "entries: 1764, mismatches: 0";
  - `python -m reciprocity_spectra.scripts.rs_s024_gauss_check --check` passes.
  If the baseline fails, fix the environment first and record it.
- The container is ephemeral: push small checkpoints often. CI (.github/workflows/rs_s024_cloud.yml) runs the Lean build and checks on pull requests to main.

ONE BOUNDED UNIT, RS-S029: the sextic character bridge (RELEASE_INVENTORY (A') items 1-3).

1. Sextic MulChar. For a primary split prime sigma (p = N sigma prime, p = 1 mod 6, r = residueRoot sigma, so r^2 + r + 1 = 0 in ZMod p), build chi_sigma : MulChar (ZMod p) ℂ from sexticExp: x -> complexZeta6^k when sexticExp r x = some k, and 0 at x = 0. Multiplicativity comes from sexticExp_mul (E3) and exp_unique (E0); the map is determined by the unit hom (ZMod p)^x -> ℂ^x (MulChar.ofUnitHom may help). Prove chi_sigma ≠ 1 (for example, x -> x^((p-1)/6) maps the cyclic group (ZMod p)^x onto the 6th roots of unity, so some x has exponent 1). Prove chi_sigma agrees with Model.complexSymbol on residues of rational integers, including the zero case. State the hypotheses you need on sigma explicitly (primary, prime norm, p ≠ 2, 3), with a lemma deriving r^2 + r + 1 = 0 from them.
2. E7, sextic case: ‖rawGauss sigma‖^2 = p. Identify rawGauss sigma with gaussSum chi_sigma (rationalAddChar p): the sum over Finset.range p versus over ZMod p, and the positive sign convention, both via rationalAddChar_apply. Then apply gauss_modulus_sq with rationalAddChar_primitive and chi_sigma ≠ 1.
3. E4, sextic case: shiftedGauss u sigma = conj(chi_sigma(res r u)) * rawGauss sigma when sigma does not divide u (res ≠ 0), and = 0 when res r u = 0. Then the per-sigma row term and the row orientation identity for Model.residueMatVec (RS-S026 Prop 1): (R w_kappa)_rho = conj(sum_sigma g_sigma(rho*kappa)/sqrt(N sigma)), matching Model's definitions of classVector and residueMatVec exactly. If the full row identity is too long, prove the per-sigma identity and record the summation step as the remaining obligation.
4. Stretch, only if 1-3 are done: (A') item 4, the finite Gram identity for imageNormSq.

RULES: no sorry, admit or new axiom. Add every new theorem to Checks/Axioms.lean. Keep the faithfulness check passing. Keep Conjecture.lean's statements unchanged (CAND002 = (1) ∧ (2) ∧ (3)), except for definitional refactors needed by the bridge; document any. If an item cannot be finished, checkpoint what is proved, state the exact remaining Lean obligation, and continue with the next item where possible.

CLOSEOUT:
- Both Lean targets build; axioms print; 1764/1764; the gauss fixture check passes; full pytest (Linux, no exclusions expected); both audit checkers (scripts/audit_strength.py --check, scripts/audit_invariance.py --check).
- Update RELEASE_INVENTORY.md status, formalisation/README.md, LEDGER.md, PROGRAM_STATUS.md and ROADMAP.md.
- Replace NEXT_SESSION_PROMPT.md with exactly one next unit. If (A') items 1-3 are done, that unit is RS-S030 PALOMAR PACKAGING (module system in every file; Challenge.lean/Solution.lean for the proved lemmas; comparator.json; a formalization.yaml draft, flagging owner fields such as licence, authors and automation disclosure; an orphan palomar/submission snapshot; Palomar's mechanical pre-checks and lake comparator; the owner uploads; follow palomar-registry.org/how-to-submit and the PalomarPolicy CONTRIBUTING). If items 1-3 are not done, the next unit is the remaining (A') obligations.
- Merge to main without asking (PROTOCOL section 9.4), push, and delete the session branch. Disclose explicitly anything that could not be done.
