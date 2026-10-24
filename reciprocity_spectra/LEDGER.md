# Reciprocity Spectra: programme ledger

This ledger is append-only. Session IDs are `RS-S###`.

## Current state

- **Phase:** 1 (scaling with pre-registered predictions). Not started.
- **Conjectures:** RS-1, RS-2, RS-3, RS-4 and RS-6 are PILOT. RS-5 is UNTESTED.
- **Committed predictions:** written in `CONJECTURES.md` and `ROADMAP.md` at commit `0b77769`.
  That is before any run at X > 1.6·10⁵. For X = 3.2·10⁵ and 6.4·10⁵:
  - κ₃ ∈ [1.38, 1.47];
  - cubic overlap within 0.03 of `√(1 − D/θ²)`;
  - quartic `θ_n = 0.166·ln X − 0.18 ± 0.05`, which is 1.924 at 3.2·10⁵ and 2.039 at 6.4·10⁵;
  - quadratic `(2 − m₄)·ln D ∈ [1.0, 1.4]`.
- **Owner decision blocker:** none.
- **Next unit:** RS-S002, Phase 1a (see `NEXT_SESSION_PROMPT.md`).

---

### RS-S001 (2026-10-24): area triage, pilot, and opening of the programme

**Stage:** area selection, collision audit, and pilot computation.

**Bounded task:** find an unsaturated, genuinely interesting research area in primes, given the
failure modes of PRIMES D0–D1 and Pointed Order Zeta. Pilot it, and set up a programme.

**What was done:**

- Read both repositories and diagnosed their failure modes (`LESSONS.md`).
- Checked eight candidate areas against the literature (`AREA_TRIAGE.md`).
- Killed one candidate computationally: there is no consecutive-prime bias in the non-abelian part
  of an S3 Frobenius, to 10⁹ (`scripts/consecutive_frobenius_s3.c`).
- Chose spectra of power-residue matrices.
- Recorded the collision audit (`PRIOR_ART.md`). The closest prior art is at operator-norm level
  only: Dunn–Radziwiłł (2024) and de Faveri–Dunn–Hoffstein (July 2026). The matrices themselves come
  from Dummit–Dummit–Kisilevsky (2016).

**Results (pilot, D ≤ 14,682):**

- **RS-1.** The cubic spike law holds with κ₃ = 1.419–1.434 for X from 5·10³ to 1.6·10⁵. The
  overlap with conjugate Gauss sums is 0.936, against a BBP prediction of 0.939.
- **RS-2.** The cubic outlier family is identified with twisted Gauss sums for u = 2, 1−ω, and the
  primes of norm 7, 13, 19, 31, 37, 43.
- **RS-3.** Quartic outliers have θ_n = 1.461, 1.574, 1.690, 1.810, and their vectors are not
  Gauss sums.
- **RS-4.** The quadratic compression gives `(2 − m₄)·ln D` = 1.248 down to 1.196 for D from 668 to
  14,682.
- Symmetry-matched random controls give `σ₁/edge = 0.997–1.000` and `m₄ ≈ 1.997`.

**Validation:**

- 6 new exact tests: reciprocity laws for n = 2, 3, 4; `g³ = pπ`; `g⁴ = pπ²`; `−χ(−1)J = π`;
  multiplicativity.
- The full pytest suite passes.
- `ruff check` is clean on all new files.
- The C builder is byte-identical to the pilot builds.
- `scripts/run_pilot.sh 10000` reproduces the recorded numbers.

**Commits:**

- PRIMES `0b77769`: programme opened.
- pointed-order-zeta `b7dd2b8`: successor pointer.
- Follow-up commit: this ledger, `PROTOCOL.md`, and the switch of the active programme.

**Owner decision (recorded from the 2026-10-24 conversation):**

- Merge the work.
- Start investigating under a new authoritative next-session prompt.
- Implemented as follows. Reciprocity Spectra is the active PRIMES programme. The DISCOVERY-1 chain
  is **paused** at D1-72/S074, with 16 REPLICATED / 0 OBSERVED / 9 REFUTED and zero candidates.
  SQ-037 is deferred, not started. The previous D1-73 prompt is preserved in git history at
  `8bbaeee:NEXT_SESSION_PROMPT.md`.

**Failures and limitations:**

- Novelty status is search-based only. The area is adjacent to an active group (Dunn, de Faveri,
  Hoffstein, David), and expert review is needed before any claim.
- Mechanisms are hypotheses. κ₃ and c₄ are not derived.
- The repository-wide ruff step was already failing on frozen D1 files. That is unchanged.

**Outgoing state:** Phase 1 ready. One prompt has been written (RS-S002).
