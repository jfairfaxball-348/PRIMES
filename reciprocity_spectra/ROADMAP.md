# Roadmap

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
