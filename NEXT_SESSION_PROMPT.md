Run RS-S030 as a CLOUD Lean-formalisation session on a fresh branch from the latest main of jfairfaxball-348/PRIMES. Read the committed repo as authority; never read or touch the paused D1 machinery.

OWNER PLAN (2026-10-27, PROTOCOL §9.6): Formalise what is exact; CAND-002 proof is parked as optional, and the conjecture remains unproved. Route: Lean -> Palomar -> paper -> arXiv -> journal. Do NOT attempt asymptotic proof, novelty audit or expert review.

READ FIRST: reciprocity_spectra/PROTOCOL.md §§7–10, reciprocity_spectra/RELEASE_INVENTORY.md (RS-S029 checkpoint and (A′) items 2–3), formalisation/README.md, formalisation/ReciprocitySpectra/{Sextic,Model,Gauss,CharacterBridge,SexticCharacter,Conjecture}.lean, formalisation/Checks/{Axioms,Faithfulness}.lean, and this prompt. Context: RS_S026_PRIME_MOMENT_BRIDGE.md §§1–2. Run bash formalisation/cloud_setup.sh to install pinned Lean 4.35.0 and Mathlib 56a005855ea17e0b0958f73ec801ae140b0a1679. Do not lake update, change pins or commit .lake/.

BASELINE: GitHub workflow 40485959252 passed two Lean targets, standard axiom audit, 1764/1764 faithfulness, 42 Gauss comparisons, full pytest, touched Ruff and both historical evidence audits. Verify baseline independently before edits.

ONE BOUNDED UNIT — COMPLETE THE EXACT SEXTIC GAUSS BRIDGE, NOT PALOMAR PACKAGING:

1. Prove the equality between Model.rawGauss σ (direct sum over t in Finset.range p of Model.complexSymbol at rational t times positive exponential) and Mathlib.gaussSum (sexticCharacter (residueRoot σ) ...) (rationalAddChar p). The sextic MulChar and symbol bridge are already kernel checked. Prove the finite ZMod/range reindexing exactly, match the positive additive character using rationalAddChar_apply. Expose explicit conditions for primary split prime, prime p=Nσ, nonzero σ.d, 2≠0, 3≠0, 6∣p−1. Do not assume the equality as a new hypothesis.
2. Use sexticCharacter_ne_one, rationalAddChar_primitive and Gauss.gauss_modulus_sq to prove the sextic rawGauss E7: rawGauss σ * star (rawGauss σ) = p (and derive normSq if desired).
3. Formalise shiftedGauss (with direct positive-sign Gauss convention), prove E4 using gauss_shift_all, including zero residue shifts. Tie the per-column identity to Model.classVector and Model.residueMatrix and prove the finite residueMatVec row orientation identity with all conjugations and the square-root normalisation correct. If the sum step is a separate obligation, prove the per-sigma statement and say what remains.
4. Only stretch after 1–3: finite Gram identity for imageNormSq.

RULES: No sorry/admit/new axiom or placeholder proof; add new theorems to Checks/Axioms.lean. Keep Conjecture.lean unchanged, especially CAND002 = (1) ∧ (2) ∧ (3). The residue-field quotient remains a modelling convention, not a proved Eisenstein quotient identification. If a theorem is blocked, retain only proved lemmas and document the exact missing obligation; do not advertise generic E7/E4 as specialized.

CLOSEOUT: both Lean targets and Checks axioms green, 1764/1764; Gauss fixture python -m reciprocity_spectra.scripts.rs_s024_gauss_check --check; full pytest; Ruff on touched Python; python scripts/audit_strength.py --check and scripts/audit_invariance.py --check. Update RELEASE_INVENTORY.md, formalisation/README.md, LEDGER.md, PROGRAM_STATUS.md and ROADMAP.md. Replace this file with exactly one correct next prompt (Palomar packaging ONLY if A′ items 1–3 are finished; otherwise remaining bridge). Push checkpoints, PR, merge validated branch to main without asking, delete branch if supported; disclose tool limitations.
