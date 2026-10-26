Run RS-S024 as a CLOUD session (not local) on a new branch from main of jfairfaxball-348/PRIMES. Read `reciprocity_spectra/PROTOCOL.md` section 10, `reciprocity_spectra/RELEASE_INVENTORY.md`, CAND-002 in `research/CONJECTURE_REGISTER.md`, `formalisation/README.md` and `formalisation/ReciprocitySpectra/Sextic.lean`. CLOUD EXECUTION NOTES (this session is not local; same methodology as the owner's Almost-Stacked-Proof `formal/`):
- Toolchain from scratch: run `bash formalisation/cloud_setup.sh`. It installs elan, then the pinned toolchain from `formalisation/lean-toolchain` (leanprover/lean4:v4.35.0). It runs `lake exe cache get` for prebuilt Mathlib oleans at the pinned commit 56a005855ea17e0b0958f73ec801ae140b0a1679 (tag v4.35.0; the manifest is committed), then builds `ReciprocitySpectra` and `Checks`. Expect several GB of download and a few minutes. Never commit `.lake/`, and never run `lake update`: keep the Mathlib pin.
- Expected baseline: the build succeeds; every theorem depends only on [propext, Classical.choice, Quot.sound]; faithfulness reports "entries: 1764, mismatches: 0". If the baseline fails, fix the environment first and record it.
- Ephemeral container (PROTOCOL section 8; typically 4 cores, ~15 GB RAM, ~29 GB disk): commit and push small checkpoints often. Anything not pushed is lost.
- Linux host: the numerical engine compiles with cc/gcc through `reciprocity_spectra/scripts/phase1.compile_engine` (the non-Windows path), so new fixtures (for example normalized Gauss sums at X = 200) can be exported in-session. Full pytest runs on Linux with no fcntl exclusions and no PYTHONUTF8. The MSVC notes in the records apply only to the owner's local Windows machine.
- Palomar readiness, to adopt in this session or the packaging session, following Almost-Stacked `formal/` (Challenge.lean, Solution.lean, comparator.json, formalization.yaml, FROZEN_MODULES.md, README):
  - convert every .lean file to the module system (`module` header, `public import`), as Palomar requires;
  - keep the toolchain and Mathlib pin exactly;
  - plan a self-contained orphan branch `palomar/submission` for the owner to upload (PRIMES is ~14 MB, well under Palomar's 500 MiB limit, but the snapshot keeps the submission clean).
  - Do not submit to Palomar; the owner uploads.
- Merge to main, push and delete the branch at closeout without asking (PROTOCOL section 9 item 4).

Novelty assessment and external review are owner-run and are not gates. Route: formalise in Lean -> Palomar -> paper -> arXiv -> journal.

STATE: proved with no sorry: E0, E1, E2, E3, E5 and E6. Faithfulness: 1764/1764 at X = 200.

ONE BOUNDED UNIT, RS-S024 (Lean):
1. Build the sextic character chi_rho as a `MulChar (ZMod p) ℂ` from `sexticExp` (multiplicativity from E3; zero at 0). Prove it nontrivial (order 6).
2. E7: |gaussSum chi psi|^2 = p for the primitive additive character psi(t) = e(t/p), using Mathlib's `gaussSum_mul_gaussSum_eq_card` (or `gaussSum_sq`) and the character's conjugation. Record the normalisation g~ = g/sqrt p.
3. E4: the shifted Gauss-sum identity g(r, chi) = conj(chi(r)) g(1, chi) (`gaussSum_mulShift`), and the matrix-orientation identity as a finite-sum lemma.
4. Define the finite index set of primary split primes with N <= X, the matrix R_X, the class vectors w_kappa and the statistics r, eps and s (computable where possible). Extend the faithfulness check to the normalized Gauss sums at X = 200, against an exported fixture, to a stated tolerance.
5. State CAND-002 (1) and (2) as Lean `Prop`s, with every interpretive choice documented. State the conditional (3) with an abstract hypothesis H_P.
Update `RELEASE_INVENTORY.md` status, `formalisation/README.md`, and the LEDGER. Run `lake build` (both targets), full pytest (Linux; no exclusions expected), and both audit checkers. Close out under PROTOCOL section 7: merge to main, push and delete the branch without asking, with exactly one justified next prompt.
