# Lessons from PRIMES and Pointed Order Zeta

This file explains why the two earlier programmes produced no novel candidate. It then lists the
design rules Reciprocity Spectra adopts so it does not repeat their failures. The diagnosis comes
from reading both repositories in full on 2026-10-24.

## 1. PRIMES (DISCOVERY-0/1, sessions S001–S074)

### Aim

Find structure in the primes by *blind discovery*:

- start from exact prime data and declared transforms;
- hide the existing conceptual map;
- replicate on untouched holdouts;
- run a prior-art audit only after a candidate exists.

### What happened

- 25 experiment families (E001–E025) produced 25 observations: 16 replicated, 9 refuted,
  and **zero candidates**.
- Every observation was a *modal fact in a fixed numerical band*. Examples:
  - `[6,6]` is the unique modal width-2 gap motif in a million-wide band;
  - every reduced-residue transition occurs for the moduli {6, 10, 12, 30, 60};
  - the modal residue of an arbitrary combinatorial function evaluated at primes in two bands.
    The functions included Josephus survivors, Young-tableau linear extensions, Grassmannian
    ranks, spanning forests of ladder graphs and proper cycle colourings.
- Every synthesis triage ended "NO CANDIDATE CREATED". The register gives the same reason each
  time: a finite modal fact cannot be extrapolated without an unsupported quantifier over bands,
  widths or scales. This is the *quantifier-selection problem*.
- Process cost grew to dominate the work. By D1-72 a session handoff required, among other things:
  - reconstructing 124 named interval roles plus 30 nested protected roles;
  - AST guards;
  - "poison" preflights;
  - one-shot workflows.

### Diagnosis

1. **Local statistics of the prime sequence are already predicted.**
   - Hardy–Littlewood k-tuple singular series (Gallagher; Montgomery–Soundararajan) give the
     leading terms.
   - Lemke Oliver–Soundararajan (2016) give the lower-order biases.
   - The `[6,6]` mode is the largest singular series among short admissible patterns.
   - Complete transition support follows from Shiu's strings of congruent primes and Maynard's
     theorem.

   Blind search in this space can only rediscover Hardy–Littlewood or record noise.
2. **Arbitrary primitives carry no prime structure.** A combinatorial function evaluated at a
   prime differs from its value at a composite only through divisibility by small primes. Once
   controls are wheel-matched, nothing structural remains, so there was no mechanism and no
   natural quantifier.
3. **The firewall banned the productive move.** `docs/RIEMANN_AS_METHOD.md` says "promote the
   residual". But the protocol never allowed an explicit model whose residual could be measured.
   New phenomena in modern prime research appear exactly as residuals from a strong model:
   - Chebyshev bias, against the explicit formula;
   - Lemke Oliver–Soundararajan, against Hardy–Littlewood;
   - Patterson bias, against equidistribution;
   - murmurations, against root-number averages.
4. **Holdout discipline was applied to the wrong objects.** Pre-registering a modal residue in a
   band is rigorous but empty. Pre-registering a *predicted constant of a limit law* is both
   rigorous and informative.
5. **The novelty audit came too late.** It was gated behind candidate promotion, which never
   happened. So the programme never learned that its observations were classical.

## 2. Pointed Order Zeta (Sessions 1–6)

### Aim

Study the residual index `I_a(p) = (p-1)/ord_p(a)` through the Euler product
`Z_a(s,z) = prod (1 - I_a(p)^(-z) p^(-s))^(-1)` and its singularity spectrum.

### What happened

- Foundations passed. The prior-art gate then showed the object is standard generalized-Artin
  theory: Felix–Murty Thm 1.7 gives `Delta_a(z)` immediately, and Wagstaff gives the Kummer
  degrees.
- Analytic continuation reduced to a power-saving effective Chebotarev theorem in the growing
  nested Kummer tower. That is a recognized barrier, and nothing in the project made it easier.
- The project was closed with the verdict PILOT_KILL.

### Diagnosis

1. **Packaging is not novelty.** A new Euler product over a classical density is equivalent
   mathematics.
2. **The hard step was a known barrier.** The project's strongest structure was a profinite Haar
   L² covariance. It already exists at the classical primitive-root endpoint, so it supplied no
   new leverage.
3. **What went right:** an early prior-art gate and an honest kill after six sessions. Keep both.
4. **Its exact missing lemma** (`notes/session6-go-no-go.md` §14) is a prime-side L² equidistribution
   estimate for the full Kummer observable. It must hold uniformly up to a power-sized level and have
   a controlled infinite tail. Session 6 checked the Frobenius large sieves (Zywina; Kowalski) and
   found no match. Those sieves average over independent representations or geometric families.
   The large sieves relevant to Reciprocity Spectra (Heath-Brown's quadratic and cubic, Gao–Zhao's
   quartic) average over the *base* of the residue symbol. That is a different technology, and it
   does not supply Pointed Order Zeta's missing lemma.

### Thematic link to the new programme

Pointed Order Zeta studied one row of a power-residue table: whether a fixed `a` is an n-th power
mod `p` as `p` varies. Along a single row everything is Chebotarev, so the object collapsed.
Reciprocity Spectra studies the whole matrix of symbols between primes. There, reciprocity fixes
a symmetry type, random-matrix theory supplies a null model, and the deviations are new.

## 3. Design rules for Reciprocity Spectra

| Rule | Statement | Failure it prevents |
|---|---|---|
| R1 Model first | Every observable is compared with an explicit null model encoding the known structure. Here the null model is a random matrix with the exact reciprocity symmetry. Discoveries are residuals from it. | PRIMES §1.3 |
| R2 Natural quantifiers | Observables are limit laws as `X → ∞`: spectral distributions, scaling exponents, constants. Each conjecture carries its own quantifier. | quantifier-selection problem |
| R3 Mechanism or kill | Within a few sessions, each deviation is matched to a candidate mechanism (theta functions, variance of primes in progressions, …). Otherwise it is recorded as unexplained with exact data. | PRIMES §1.2 |
| R4 Collision audit before investment | Prior art is searched when an area is chosen, and the search scope is recorded (see `PRIOR_ART.md`). | PRIMES §1.5, POZ §2.1 |
| R5 Predict, then compute | Before scaling a computation, write down the predicted value (κ₃, BBP overlap, c₄). This is the holdout discipline that carries information. | PRIMES §1.4 |
| R6 Fast kills are outputs | A candidate that fails its test is recorded with code and numbers, then dropped. Example: `scripts/consecutive_frobenius_s3.c`. | sunk-cost drift |
| R7 Exact core in CI, exploration in scripts | Pure-Python exact arithmetic is tested in CI. Floating-point spectral work lives in scripts with recorded parameters. | unverifiable numerics |
| R8 Lightweight process | Each session ends with: updated results, updated conjecture table, and one next step. No interval-role bureaucracy. | PRIMES §1 process cost |
