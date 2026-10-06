# E005 Historical-Theory Unblinding Comparison — 2026-10-06

**Lane:** historical rediscovery calibration (permanently quarantined from novelty)  
**Queue item:** SQ-005  
**Related task:** D1-13 / SQ-005  
**Frozen benchmark:** `experiments/E005_PRIME_COUNT_SCALE_CALIBRATION.md`  
**Blinded execution:** `experiments/E005_BLINDED_EXECUTION_2026-10-06.md`  
**Required pre-unblinding checkpoint:** `experiments/E005_PRE_UNBLINDING_SUMMARY_2026-10-06.md`  
**Pre-unblinding checkpoint commit:** `8187a5a2021c124860848da39fc53702eac73921`

The historical comparison below began only after the source-free blinded summary above was committed. E005 design choices and D1-12 outputs remain frozen; no calibration result is novelty evidence.

## Bounded source list

### Primary historical source

1. Bernhard Riemann, *On the Number of Prime Numbers less than a Given Quantity* (1859), English translation by David R. Wilkins, hosted by the Clay Mathematics Institute: https://www.claymath.org/wp-content/uploads/2023/04/Wilkins-translation.pdf

Direct statements used from the paper:

- Riemann begins from Euler's prime product and introduces `ζ(s)` as a function of a complex variable.
- He expands `log ζ(s)` as a sum over prime powers.
- He replaces the raw prime-count step function by the weighted prime-power count `f(x)=F(x)+1/2 F(x^(1/2))+1/3 F(x^(1/3))+...`.
- He represents that counting object through an integral transform involving `log ζ(s)/s` and invokes Fourier inversion.
- He obtains an explicit expression with a leading `Li(x)` term and correction terms indexed by zeros of the transformed zeta function; the resulting density expression has leading term `1/log x` plus zero-dependent oscillatory corrections.

### Authoritative modern references

2. NIST Digital Library of Mathematical Functions, §27.2, especially Eq. 27.2.3: https://dlmf.nist.gov/27.2  
   This records the prime number theorem `π(x) ~ x/ln x`, and attributes the historical conjecture to Gauss and Legendre and the first proofs to Hadamard and de la Vallée Poussin.

3. NIST Digital Library of Mathematical Functions, §25.16, especially Eqs. 25.16.1–25.16.3: https://dlmf.nist.gov/25.16  
   This defines the weighted prime-power function `ψ(x)`, gives an explicit formula with correction terms from nontrivial zeros of `ζ(s)`, and records `ψ(x)=x+o(x)` as equivalent to the prime number theorem.

4. Clay Mathematics Institute, *Riemann's 1859 Manuscript*: https://www.claymath.org/collections/riemanns-1859-manuscript/  
   Used only as authoritative expository context: it describes the prime number theorem as the average prime distribution and Riemann's zero-based formula as describing deviations from that average.

No broader literature survey or negative-source inference was used.

## Section 18 comparison

### 1. Selected leading normalization

The historical leading density scale implied by `π(x) ~ x/ln x` is `1/ln x`. In E005 notation, the direct elementary normalization corresponding to that leading scale is therefore `N01 = d * ln(s)`, not the selected `N03 = d * sqrt(ln(s))`.

The frozen tournament did contain N01 and ranked it second on development, immediately behind N03. This shows that the blinded elementary palette reached the correct logarithmic neighbourhood. But the frozen selector did not identify the historical leading normalization: N03 still carries an expected factor of approximately `1/sqrt(ln s)` under the prime-number-theorem scale and therefore tends in the wrong leading direction.

Calibration labels:

- selected N03 as a historical leading description: **DESCRIPTIVE_ONLY**;
- N01's presence in the frozen palette, considered as an object-level overlap only: **DIRECT_HISTORICAL_MATCH**;
- the blinded scale-search process overall: **USEFUL_PARTIAL_REDISCOVERY**.

The assessment behaviour helps explain the miss without changing it: the max-over-width score was vulnerable to the shortest fixed windows, where count noise is proportionally largest. N03 retained the frozen M2 width-specific compression result, but that empirical compression is not the historical leading law.

### 2. Leading/residual separation

E005 did separate a selected leading transform from a residual, which is methodologically aligned with the historical average-versus-deviation split. However its residual

`r(a,w) = T_N03(a,w) / B_w - 1`

is centred on a five-width collection of development means `B_w`. It is not the historical error after subtracting a mathematically defined leading counting term such as `Li(x)`, nor the modern weighted-prime-power residual `ψ(x)-x`.

Riemann's primary construction instead changes the counting object before studying the remainder: weighted prime powers are encoded through `log ζ(s)`, inverted, and decomposed into a leading `Li(x)` contribution plus zero-dependent corrections. The modern DLMF formula for `ψ(x)` makes the same structural point explicitly: the residual is attached to a globally defined counting function and its zeta zeros, not to a width-specific empirical baseline.

Calibration label: **DESCRIPTIVE_ONLY**.

### 3. Residual transform search

The frozen R0–R4 family retained raw residual words, signs, first differences, first-difference signs, and a second difference. The only development compression target was the R1 sign word `(1,-1,-1)`; it failed assessment completely, while `(-1,-1,-1)` occurred at all five assessment widths.

No member of the frozen residual transform family corresponds to the historically structural transform in Riemann's argument. The historically productive transformation is from prime counts to a weighted prime-power counting object, then to `log ζ(s)` in the complex domain, followed by inversion; the zeros supply the oscillatory correction terms.

Calibration label: **DESCRIPTIVE_ONLY**.

### 4. Cross-width compression

N03 did compress several count/scale observations in the limited frozen sense measured by M2: it beat raw density width-by-width at 5/5 development widths and 4/5 assessment widths. That is a meaningful process success because a single non-identity scale correction worked across several window sizes without refitting.

Historically, however, the correct leading correction is the full logarithm, not its square root, and the selected normalization failed M1 on the assessment global score. The compression therefore points in the right kind of direction but stops short of the historically useful leading object.

Calibration label: **USEFUL_PARTIAL_REDISCOVERY**.

### 5. Missing historical representation change

The crucial absent move was a change from local elementary functions of interval density to a global multiplicative/analytic encoding of the primes.

Riemann's paper directly:

1. passes from primes to the Euler product / Dirichlet series `ζ(s)`;
2. takes `log ζ(s)`, which naturally introduces weighted prime powers;
3. converts the resulting weighted counting function into an integral transform;
4. uses complex/Fourier inversion;
5. expresses the counting object as a leading logarithmic-integral term plus contributions from zeros.

E005 explicitly forbade the series, integral, complex-valued transform, zero set, and equivalent mature object needed for that move. No amount of further search inside frozen R0–R4 could have reached it.

Calibration label: **STALLED_BEFORE_KEY_IDEA**.

### 6. Q1–Q3 in hindsight

**Q1.** As instantiated with N03, the finite-nonzero-limit question points at the right general idea—seek scale-normalized stability—but at the wrong normalization and on fixed short windows. The historically matched elementary candidate would have been N01, and the historically stronger formulation concerns a cumulative or suitably averaged counting object rather than persistence of fixed-width local counts.

Calibration label: **DESCRIPTIVE_ONLY**.

**Q2.** Asking whether one normalization coherently improves several widths was productive as a methodological compression test. It successfully detected that one scale correction can unify several observations, even though the selected correction was not the historical one.

Calibration label: **USEFUL_PARTIAL_REDISCOVERY**.

**Q3.** Persistent residual-sign words were not historically productive. Riemann's residual structure is oscillatory and is encoded through zero contributions after a representation change; a stable three-anchor sign word is not the relevant invariant. The frozen assessment failure was therefore informative rather than a near-miss.

Calibration label: **DESCRIPTIVE_ONLY**.

## Final calibration judgement

**Overall E005 historical-theory label: STALLED_BEFORE_KEY_IDEA.**

Supporting component labels:

- elementary scale search: **USEFUL_PARTIAL_REDISCOVERY**;
- direct historical scale object present in the palette but not selected (N01): **DIRECT_HISTORICAL_MATCH**;
- selected N03 leading description: **DESCRIPTIVE_ONLY**;
- empirical residual and R0–R4 residual transforms: **DESCRIPTIVE_ONLY**;
- missing multiplicative/complex representation shift: **STALLED_BEFORE_KEY_IDEA**.

This is not a reinterpretation of the frozen mechanical `PARTIAL_PASS`. The two judgements answer different questions: `PARTIAL_PASS` rates the blinded frozen milestones; `STALLED_BEFORE_KEY_IDEA` rates the post-unblinding historical comparison.

## What the blinded process found, missed, and would have needed next

### Found

- absolute scale matters for prime-count density;
- logarithmic elementary transforms are useful enough to sit at the top of the development ranking;
- one nontrivial normalization can compress several window scales at once;
- leading behaviour and a residual can be separated procedurally;
- exact structural questions can be generated without importing mature terminology;
- holdout/firewall discipline can be preserved through the calibration.

### Missed

- selection of the full logarithmic leading normalization N01;
- the logarithmic-integral/cumulative form of the leading description;
- a globally defined weighted prime-power counting object;
- the multiplicative encoding of primes by the Euler product / zeta function;
- the use of `log ζ` to linearize prime-power contributions;
- complex/Fourier inversion and zero-dependent residual structure.

### What would have been needed next inside the historical benchmark

A successful continuation would have required a predeclared representation-switch stage, not retuning N03 or extending R0–R4. The necessary historical move is from pointwise elementary normalization of short interval densities to a global weighted counting object with a transform that respects multiplicative structure, followed by inversion and analysis of its residual terms.

That statement is calibration-only. It must not be imported as a novelty candidate, feature, prior-art result, or justification for inspecting A1/H3/A3/H4/A4.

## Quarantine

D1-13 generated no prime-derived data, changed no E005 score/selection/residual/question/milestone semantics, allocated no `OBS-###` or `CAND-###`, changed no novelty status, and ran no novelty collision audit.

A1=`[33_000_000,34_000_000)`, H3=`[37_000_000,38_000_000)`, H4=`[41_000_000,42_000_000)`, A3=`[70_000_000,71_000_000)`, and A4=`[78_000_000,79_000_000)` remain untouched/uninspected.
