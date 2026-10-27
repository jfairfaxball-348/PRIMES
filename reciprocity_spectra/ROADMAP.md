> **CURRENT RS-S042 (2026-10-27):** Internally audited 13-page paper candidate, 12 displayed of 14 reproducibly generated figures, eleven corrected bibliographic entries and full numerical/JSON-key provenance in `paper/NUMERICAL_SOURCE_AUDIT.md`; copy-ready `paper/ARXIV_METADATA.md`. Critical RS-S021 pre-registration correction: registered A-bin ±0.12, observed maximum residual 0.0494578894 (not registered ±0.05). Pinned code-head [paper 40591098532](https://github.com/jfairfaxball-348/PRIMES/actions/runs/40591098532), [scoped Lean/pytest/evidence 40591098569](https://github.com/jfairfaxball-348/PRIMES/actions/runs/40591098569), [independent 26-theorem Comparator/NanoDa 40591098652](https://github.com/jfairfaxball-348/PRIMES/actions/runs/40591098652) all PASS at `c7e87a3f`. Final docs-head still requires validation before merge. **RS-S043:** purely INTERNAL standalone arXiv-source-package rehearsal; owner retains all release decisions. CAND-002(1)–(3) remain unproved; prior failures and H_P erratum retained. No arXiv or journal submission.

> **HISTORICAL RS-S041 (2026-10-27):** Figure-rich experimental-mathematics paper drafted in `paper/`; fourteen vector+PNG pairs and the full LaTeX first-draft PDF build PASSED in [workflow 40587444244](https://github.com/jfairfaxball-348/PRIMES/actions/runs/40587444244). CAND-002(1)–(3) remain conjectures; the exact finite Lean corpus is a verification artefact only. No Palomar registration or external publication; owner route paper → arXiv → journal. **Next RS-S042:** internal layout, source-number and bibliography audit, then arXiv metadata/owner decision list. Historical sections below are superseded, not erased.

> **RS-S039 CURRENT CHECKPOINT (2026-10-27):** The genuine 26-finite-theorem independent Comparator+NanoDa+Lean kernel accepted the proof at 4cb25de8 (workflow 40564457111). Matching scoped full cloud passed (40564457029). Complete final-docs-head checks and merge stacked PR #14 through #18 in order. All exact finite E4/E7, Eisenstein class and frozen row theorems remain unchanged. No Palomar ID. Only owner-reviewed AI-use disclosure remains before actual registry submission: automation.methods [] is pending, NOT an assertion of no AI assistance. CAND-002 asymptotics remain unproved, D1 unchanged.

> **ACTIVE CHECKPOINT (RS-S035, 2026-10-27):** Exact finite Palomar packaging expanded to a 26-theorem independent Mathlib-only Challenge, including specialized sextic E4/E7 and full frozen matrix row identity. Initial independent Comparator run 40520302610 rejected the `res_mul` statement owing to an extra implicit Challenge assumption; the code-head Lean suite 40522609418 is green, but Comparator 40522609498 now fails on the frozen shiftedGauss definition comparison. RS-S036 must repair exact exported-constant fidelity; no package merge. AI disclosure remains explicitly pending owner review; no submission or Palomar ID. CAND-002(1)–(3) stays conjectural. Do not replace verification with Lake green alone.

> **RS-S034 DRAFT CHECKPOINT (2026-10-27):** Palomar packaging has begun under the current official source-policy requirements. All 17 original Lean files successfully passed module-format compilation at code head 42d0607, cloud run 40516664832; Apache-2.0 is the chosen root licence. An initial Challenge/Solution comparator selects 15 exact elementary and generic character statements only; the specialised E7/E4 and full finite row theorem are not yet in the independent statement surface. The automation disclosure is explicitly pending human completion and therefore the metadata is not submission-valid. No Palomar ID, manuscript or conjectural proof is claimed. RS-S035 must finish the independent Challenge and Comparator verification before submission.

> **ACTIVE CHECKPOINT (2026-10-27, RS-S033):** The actual finite Eisenstein class product and frozen `shiftedGauss(ρ * classNumerator κ, σ)` matrix-row identity are now kernel-proved in `ClassProduct.lean`. Pinned workflow [40511639019](https://github.com/jfairfaxball-348/PRIMES/actions/runs/40511639019) passed Lean library, Checks, standard-axiom audit, 1764/1764 exponents, 366 pytest, 42 Gauss values, Ruff and two frozen audits. Group (A′) items 1–3 are complete; RS-S034 is narrowly scoped to Palomar packaging of these **finite proved lemmas only** after final closeout validation and merge. CAND-002 (1)–(3) remains conjectural and optional; paused D1 untouched. No Palomar ID exists yet.

> **ACTIVE CHECKPOINT (2026-10-27, RS-S032):** The actual finite `residueMatVec` row identity is kernel-proved with all indexed split-prime hypotheses derived from membership; exact periodicity also identifies frozen `shiftedGauss u σ` with the reduced direct sum for every true Eisenstein u (including zero). Pinned workflow 40505888940 succeeded. The remaining bridge is one column-independent finite Eisenstein product representing arbitrary `TwistClass` reductions (`rowShift`); the attempted uncompiled construction was removed. RS-S033 finishes only that finite bridge; Palomar packaging stays gated until it passes. CAND-002 remains unproved, optional; no asymptotic/prior-art work.

> **ACTIVE CHECKPOINT (2026-10-27, RS-S030):** pinned Lean/Mathlib GitHub Actions run 40489442361 PASS. The actual rational direct Gauss sum is now identified with Mathlib's sextic gaussSum by a proved finite reindexing and positive-sign exponential bridge; specialized sextic E7 `Gσ·conj(Gσ)=Nσ` is kernel checked. Group (A′) items 1–2 are complete. **RS-S031** must finish the direct shifted E4 (including zero shift) and `residueMatVec` row orientation before Palomar packaging. CAND-002 is still conjectural and optional research; no novelty/external-review work in this release pipeline.

# Roadmap

> **ACTIVE CHECKPOINT (2026-10-27, RS-S029):** Lean v4.35.0 / pinned Mathlib cloud verification PASS (run 40485959252). The sextic exponent-based `MulChar`, its nontriviality and rational-symbol agreement, the split-prime residue-root polynomial and the generic zero-shift Gauss identity are kernel checked. The `rawGauss` sum identification, sextic E7/E4 and the `residueMatVec` row-orientation identity remain **OPEN**. **Next RS-S030:** finish those identities before Palomar packaging. CAND-002 proof work is optional and out of the release pipeline under PROTOCOL §9.6; all asymptotic claims stay conjectural. The historical checkpoints below are superseded by this plan of record.

> **Active mathematical checkpoint (2026-10-27, RS-S028):** CAND-002(3) remains **OPEN**; mathematics-first, with no further Lean/Palomar work. RS-S028 gives an exact ideal prime projection (including rational/trace correction, inert ideals and excluded prime powers), an ideal Vaughan I/II decomposition with genuine Möbius/Λ coefficients, and a rigorous Dirichlet-series counterexample to transfer from an all-moduli **pole residue alone** to a prime coefficient. None yields a sextic prime-asymptotic coefficient or the signed endpoint estimates. See \`RS_S028_PRIME_PROJECTION_VAUGHAN.md\`. **Next:** RS-S029, arithmetic local factors and signed Type II main term (or a narrow, proved obstruction) for moving shifts \(u=\rho\kappa\). The Phase-1 headings below are historical.

> **Active mathematical checkpoint (2026-10-27, RS-S027):** Proof-first CAND-002(3) bridge remains **OPEN**. RS-S027 proves an exact signed-kernel reciprocity transfer and a genuinely uniform *upper-tail* Abel lemma under raw H_P, but no moving-row full estimate, signed two-point asymptotic, or fixed-class implication. See `RS_S027_SIGNED_KERNEL_TAIL.md`. Next: RS-S028, explicit arithmetic coefficient/Type II obstruction. Phase-1 headings below are historical planning, not the active stage. No Lean work until the mathematical gap is resolved (PROTOCOL §9.6).

**Current checkpoint: RS-S026 (2026-10-27), mathematics-first.** The exact rational sextic row orientation, signed two-point prime-correlation expansion (including diagonal correction), and fixed-shift Abelian transport under the stated H_P (leading coefficient 4) are proved **on paper** in `RS_S026_PRIME_MOMENT_BRIDGE.md`. The proof obligation CAND-002(3) remains **OPEN**: H_P is raw and one-point, lacks moving-shift normalised uniformity, and does not give coefficient signs/averaged squares or the t→0 boundary. Next is RS-S027 (signed two-point prime kernel and moving-shift asymptotics). **Do not resume Lean, Palomar or paper work while this owner-specified proof-first gate remains open.**

**Owner priority (2026-10-26): MATHEMATICS FIRST. RS-S026 is a prime-level/matrix-level proof-obligation session, not Lean work. The compact-t and large-t regimes in CAND-002 do not entail their fixed-class t→0 consequences without additional argument. Resolve H_P weighting/coefficients and prove or properly repair the mathematical implication before more Lean or Palomar preparation; see RS_CAND002_LOGICAL_BRIDGE_AUDIT.md.**

**Historical checkpoint: RS-S025 (2026-10-26): pinned cloud Lean builds and Checks PASS; the rational positive-sign AddChar and its primitivity/value theorems are proved with standard axioms. Sextic MulChar, symbol equality, E4/E7 specialization and zero shifts remain OPEN. 1764/1764 matrix, 42 Gauss, 366 tests, targeted Ruff and both audits pass. Historical Lean handoff to RS-S026 was superseded by the owner's 2026-10-26 mathematics-first directive.** **Current checkpoint: RS-S024 (2026-10-26): cloud Lean builds green; E0–E3, E5–E6 remain proved; generic-character E4/E7 proved but actual sextic MulChar bridge remains open; CAND-002 Prop and finite model defined; 1764/1764 exponent and 42 native/Python Gauss checks pass; next RS-S025.** Earlier: RS-S022, CAND-002 frozen. Earlier: RS-S021, new-scale holdouts PASS. Earlier: RS-S020, H− PASSES on fresh primes. Earlier: RS-S019, π⁵ deficit intrinsic. Earlier: external review received (anonymous), CAND-002 freeze deferred. Earlier: RS-S018, collision audit done, crossover-law candidate drafted. Earlier: RS-S017, (A″) PASSES on fresh classes. Earlier: RS-S016, finite-X crossover in N₆/X. Earlier: RS-S015, PROV-RS14 refuted at X = 10⁶. Previous: RS-S013 (2026-10-26), local execution. The Type II
product is exactly a locally signed cubic kernel. Generic large-sieve and
unrestricted operator-norm approaches cannot reach the proposed sextic target;
the route using actual arithmetic coefficients remains unresolved. CAND-001's
frozen three-statement package is REFUTED by sixth-power invariance of u=64.
Its matrix and prime-bias components are not refuted, and the corrected finite
80-row test still passes. Historical checkpoints below are preserved.
Next: RS-S014, a bounded invariant-formulation audit of the strength law.
No automatic fallback, theorem graduation, or new candidate is authorized by
this checkpoint; see `PROOF_ROUTE.md` section 7 and `NEXT_SESSION_PROMPT.md`.

**Route revised (owner, 2026-10-27, after the Palomar review).** The route is now: **paper →
arXiv preprint → journal**.

- Lean formalisation is done and is a verification artefact, cited in the paper.
- Palomar is optional: its editorial review declined the 26 finite identities on research interest,
  not correctness.
- Next session: **RS-S041, paper drafting, figure-rich** (`NEXT_SESSION_PROMPT.md`).

**Plan of record (owner, 2026-10-27).** Proof work is out of the pipeline and parked as optional
research (PROTOCOL §9.6). Formalise what is exact; everything else stays conjecture.

- Stage 1 next: RS-S029, the Lean sextic character bridge (E7/E4 sextic cases).
- Then RS-S030, Palomar packaging.
- The classification of claims is in `RELEASE_INVENTORY.md`, "Plan of record".

## Route to publication (owner, 2026-10-26; replaces the earlier six-phase route)

Phase 1, settling the science, is complete: CAND-002 was frozen in RS-S022. Novelty assessment and
external review are done independently by the owner and are not stages or gates. The route has five
stages, in order:

1. **Formalise in Lean** (`formalisation/` in this repository; PROTOCOL §10):
   - the exact-identity inventory E1–E9;
   - Lean 4 + Mathlib definitions and proofs;
   - CAND-002 as a Lean `Prop`;
   - the byte-for-byte faithfulness check against the engine.
2. **Palomar register** the proved lemmas from a fixed public commit. **Owner action:** the
   repository must be public on GitHub, with write-access proof.
3. **Write the paper** (experimental mathematics):
   - definitions;
   - every registered prediction and its outcome;
   - Palomar IDs;
   - the formal conjecture;
   - the mechanism, labelled heuristic;
   - a reproducibility archive;
   - an AI-use disclosure.
4. **arXiv preprint:** math.NT. **Owner action:** an endorsement if needed.
5. **Journal submission:** Experimental Mathematics first. Mathematics of Computation, Research in
   Number Theory or JTNB are alternatives.

Each phase ends with:

- updated `results/`;
- an updated `CONJECTURES.md`;
- one concrete next step.

Kills are recorded, not hidden (`LESSONS.md` R6).

## Phase 0: triage and pilot (done 2026-10-24)

- Exit: lead area chosen (`AREA_TRIAGE.md`).
- Exit: collision audit recorded (`PRIOR_ART.md`).
- Exit: pilot data up to D ≈ 14,600 (`results/`).
- Exit: six working conjectures (`CONJECTURES.md`).

## Phase 1: scale with pre-registered predictions

1. **Memory and compute.** Store the matrix as uint8 exponents (D² bytes). Do matrix–vector
   products blockwise in C or numba, and run Lanczos on `C*C`. This reaches D ≈ 5·10⁴ (X ≈ 6·10⁵)
   on this machine, and more with out-of-core storage.
2. **Pre-register, then run X = 3.2·10⁵ and 6.4·10⁵.** Predictions:
   - κ₃ ∈ [1.38, 1.47];
   - cubic overlap within 0.03 of the BBP value `√(1 − D/θ²)`;
   - quartic θ_n ≈ 0.166·log X − 0.18 (± 0.05);
   - quadratic `(2 − m₄)·log D ∈ [1.0, 1.4]`.
3. **Test RS-5.** Run sextic matrices over `Z[ω]`: the sextic symbol is the product of the
   quadratic and cubic symbols in the right normalization. Run quintic matrices over `Z[ζ₅]`,
   which is a PID.
4. **Local statistics (RS-6).**
   - singular-value spacings after deflating the outliers;
   - fluctuations of the first bulk singular value;
   - eigenvalues of the complex symmetric `C_X` (circular law?).

Exit: each of RS-1, RS-3, RS-4 becomes STRESSED or REFUTED.

**RS-S002 checkpoint:** the scalable byte engine is validated, and the required X = 320000
comparisons all PASS; RS-1, RS-3 and RS-4 are STRESSED at this scale. X = 640000 remains untested
because measured runtime projections exceed the per-run budget (see LEDGER.md and the Phase-1
results JSON). The subsequent Phase 1b outcomes are recorded below.

**RS-S003 checkpoint:** all eight registered finite sextic/local comparisons FAIL. The RS-5
finite formulation and RS-6 finite local extension are REFUTED; eventual asymptotic limits
remain unresolved and the original RS-6 bulk claim remains PILOT. Phase 1c next certifies
additional exact identities required of the null ensemble, followed by qualified-model tests
at fresh scales. Old outcomes and predictions stay unchanged. See the ledger and Phase-1b JSON.

**RS-S004 checkpoint (Phase 1c):** the conjugation-matched null is certified with exact tests.
All five registered fresh-scale predictions PASS:

- bulk gap ratios match the corrected null (RS-6C, X = 80000);
- the cubic and quartic outliers stay above it;
- the sextic excess persists at X = 320000 (RS-7).

Phase 1d next characterises the sextic outlier cluster.

**RS-S005 checkpoint (Phase 1d):** the sextic excess is a growing cluster: 7, 22 and 34
singular values above the corrected null at X = 40000, 160000 and 320000. Its delocalized
vectors are increasingly enriched in twisted conj(g̃6) spans (registered PASS). The
identification is partial (RS-7a). Next: measure the per-twist strengths against N(u).

**RS-S006 checkpoint:**

- The sextic twist strengths obey an exact-looking primary-class dichotomy (RS-7b). It is
  registered PASS at X = 320000 and 640000.
- No twist is individually supercritical below X ≈ 6·10⁵.
- Two simple models of the cluster multiplicity fail.

Next: the mechanism stage for RS-7b, which opens Phase 2 for the sextic family.

**RS-S007 checkpoint:** RS-7b has been reformulated exactly: twists are enhanced iff their
unit-class factor is unramified at 3. Its strength mechanism is UNEXPLAINED, and the naive
theta-coefficient heuristic fails. Next: the Phase-5 external note, starting early, because the
open questions are theoretical.

**RS-S008 checkpoint:**

- The collision audit has been refreshed.
- The expert-review note (`NOTE_DRAFT.md`) and the Astra referee prompt (`ASTRA_PROMPT.md`) are
  prepared.
- Blocked on an owner action: send the prompt and commit the reply.

**RS-S009 checkpoint:**

- Astra's reply has been evaluated. Its exact symmetry and Hasse–Davenport factorization are
  verified.
- Its cubic calibration was registered and FAILED as stated. A squarefree correction was then
  registered and PASSES at X = 160000 (RS-8).
- Next: Astra's decisive Kubota-sum test (Q5).

**RS-S010 checkpoint:**

- Astra's Q5 FAILED as stated.
- The trace-form Kubota sums carry main terms in the ω-rotated classes (RS-9, PASS at
  X = 1.28·10⁶).
- A purely 2-adic sign moves the prime-level bias to classes 0 and 3, which explains the side of
  the matrix dichotomy.
- Next: map the full 2-adic × unit-class selection table.

**RS-S011 checkpoint:**

- The 2-adic character selection rule FAILED twice in fresh windows, with underpowered
  statistics; it is not established.
- CAND-001 is frozen: the matrix dichotomy plus the prime-level unit-class bias.
- The proof stage begins on the hard version (`PROOF_ROUTE.md`).

**RS-S012 checkpoint:**

- The dispersion reduction is exact.
- The cubic Patterson law is calibrated (PASS at X = 3.2·10⁵).
- The sextic strength law θ_u² ∝ N(u)^{−1/6} holds (PASS at X = 10⁶), and is added to CAND-001.
- Next: T2, the Type II crux.

**RS-S014 checkpoint:**

- The strength law and the dichotomy must be stated on sixth-power twist classes.
- Exponents 1–3 follow N₆^{−1/6}; exponent 4 is open; exponent 5 has a negative excess.
- CAND-001 statement 1's universal form is withdrawn.
- PROV-RS14 awaits registered class tests at X = 10⁶.

**RS-S015 checkpoint:**

- PROV-RS14 is REFUTED at X = 10⁶ (P1 and P3 FAIL; P2 PASS).
- Exponents 3 and 4 decay faster than N₆^{−1/6}.
- Next: RS-S016, exploratory X-dependence.

**RS-S016 checkpoint:**

- The decay is finite-X: the excess collapses in N₆/X.
- PROV-RS16 is recorded.
- Next: RS-S017, registered fresh-class tests.

**RS-S017 checkpoint:**

- (A″) is STRESSED: Q1, Q2 and Q4 pass on 440 unseen classes.
- (B″) is refuted as stated; its mean form survives.
- Next: RS-S018, collision-audit of the surviving core.

**RS-S018 checkpoint:**

- Statement 2 is mostly theory-implied.
- (A″) and the π⁵ constant have no collision; the excess is not a naive τ₆ readout.
- The candidate is drafted.

## Phase 2: mechanisms (heuristic derivations, then comparison)

1. **κ₃ (RS-1).** Heuristic: let `w = conj(g̃)`. By cubic reciprocity and twisted multiplicativity
   of Gauss sums, `(C w)_ρ` is a twisted Gauss-sum average with main term `≍ τ(ρ) X^{5/6}/log X`.
   Here `τ(ρ)` are cubic theta coefficients with `|τ(ρ)| ≍ N(ρ)^{-1/6}` (Patterson). So
   `‖Cw‖² ≈ Σ_ρ |τ(ρ)|² X^{5/3}/log²X ≈ X^{7/3}/log³X` and `‖w‖² = D ≈ X/log X`. Together these
   give `θ ≍ X^{2/3}/log X`. Make the constant explicit and compare with 1.42.
2. **The outlier family (RS-2).** Predict `θ_u/θ_1` from Patterson's formula for `τ(u)`, and
   predict the near-orthogonality of the twisted vectors (a Rankin–Selberg computation, as in
   de Faveri–Dunn–Hoffstein).
3. **The quartic growth law (RS-3).** Derive `θ_n ∝ log X` from the X^{3/4} bias conjecture of
   David–Dunn–Hamieh–Lin, or explain the discrepancy.
4. **c₄ (RS-4).** Write `m₄ − 2` as a mean square of real character sums over primes (see
   `CONJECTURES.md`). Derive its 1/log term from a Hardy–Littlewood / Montgomery–Hooley heuristic
   with secondary terms. Run the explicit-formula variance model numerically. Check the
   prediction by restricting the index set (primes ≡ 1 mod 4 only; excluding small primes).

Exit: each conjecture either has a quantitative mechanism that matches the data within error, or
is marked UNEXPLAINED with a precise residual.

## Phase 3: quartic theta coefficients (highest-upside branch)

- Extract the top singular vectors of `Q_X` for growing X and track their stability.
- Compare with Eckhardt–Patterson numerics and with Suzuki's values at squares (for a
  rectangular variant indexed by squares).
- If the vectors stabilize, formulate numerical conjectures for the quartic theta coefficients at
  primes. These coefficients are not known in closed form.

## Phase 4: theorems in reach

1. **Quarter-circle law for the Legendre matrix of primes.** Moment method plus Heath-Brown's
   quadratic large sieve; moments reduce to multilinear character sums over primes.
2. **At least one outlier for n = 3 under GRH**, with spike `≍ X^{2/3}/log X`. This should follow
   from the Dunn–Radziwiłł dispersion estimate. Check against de Faveri–Dunn–Hoffstein, who prove
   the operator-norm version unconditionally.
3. **Function-field analogues over `F_q[t]`**, where RH holds and Hoffstein–Patterson theta
   functions are explicit: residue matrices of monic irreducibles.

## Phase 5: expert review and graduation

Write a short note: "Spectra of power-residue matrices: random bulk and metaplectic outliers".
Contact:

- D. Dummit / H. Kisilevsky (residue matrices);
- A. Dunn / A. de Faveri / J. Hoffstein / C. David (metaplectic);
- a random-matrix theorist, for the spiked-model analysis.

Graduate any proved statement to its own repository, following the PRIMES graduation rule.

## Release verification checkpoint — RS-S036 (2026-10-27)

The 26 finite exact theorem statements are still proven in the library, but their independent Palomar Challenge/Solution fidelity is not certified. RS-S036 isolated the automatic `shiftedGauss._proof_1` numeral witness as the next strict Comparator obligation (see `LEDGER.md`). CAND-002(1)–(3) stay separate conjectures and outside the release proof pipeline; do not broaden this verification session to numerical discovery or asymptotic proofs. No paper or registration before the explicit release gate.

**RS-S036 failed-closeout recovery (2026-10-27):** comparator #44 and cloud #133 originally failed to compile a Challenge-only raw-numeral witness (`omega` at line 228), not an established mathematical theorem. The repair now compiles and scoped cloud validation is green at [40534020351](https://github.com/jfairfaxball-348/PRIMES/actions/runs/40534020351); independent Comparator [40534020098](https://github.com/jfairfaxball-348/PRIMES/actions/runs/40534020098) has passed the original `shiftedGauss` witness mismatch and found its *next* exact-source mismatch at `sexticCharacter`, involving autogenerated `_proof_2/_proof_3` names. The required 26 statement surface is unchanged; no independent acceptance or Palomar ID. Root Apache-2.0 and owner-pending AI declaration unchanged. The final diagnostic run at code head `43c5ff5` must be checked in RS-S037. See `LEDGER.md` for full evidence.


**RS-S037 (2026-10-27):** the true independent Comparator has cleared the exact `sexticCharacter` exported source mismatch and now stops at `directShiftedGauss` (run 40542225202). The complete scoped Lean/Python/evidence cloud suite passed at the same code head (run 40542225221). Verification of all 26 remains OPEN; no merge or Palomar registration. RS-S038 is restricted to the next exact exported-definition dependency, not CAND-002 proof or numerical exploration.
