# Area triage (2026-10-24)

The goal was an area of prime-number research that meets all four of these conditions:

- it is *genuinely interesting*: deep structure and a real mechanism;
- it is *not saturated*: little or no current work on the specific questions;
- it is *computationally accessible*: the PRIMES lab can generate decisive data;
- it has *natural quantifiers*: limit laws, not modal facts.

Each candidate was checked against the literature with web searches on 2026-10-24. Where cheap,
it was also tested with a pilot computation. A negative search is not a novelty proof. The
verdicts record the scope that was actually checked.

| # | Area | Verdict | Key evidence |
|---|---|---|---|
| A | Spectra of power-residue matrices of primes ("Reciprocity Spectra") | **LEAD** | Pilot: three distinct regimes (cubic metaplectic outliers obeying an exact spike law; quartic outliers that are not Gauss sums; quadratic compression with a 1/log D law). Closest prior art is at operator-norm level only; see `PRIOR_ART.md`. |
| B | Proportion of periodic points of polynomial maps mod p (post-critically finite maps, basilica `x²−1`) | **SATURATING** | The qualitative question (Juul–Kurlberg–Madhu–Tucker 2014) was settled in 2026. Fariña-Asategui–Radi, *Fixed-point proportion of geometric iterated Galois groups* (arXiv 2601.16173). Radi, *Proportion of periodic points in reduction of polynomials* (arXiv 2603.21620; Acta Arith. 2026). Radi, arXiv 2608.14524 (rational functions). Also Penkov–Stoll, *Prime numbers and dynamics of x²−1* (arXiv 2502.11929). Only quantitative rates remain, and this group is actively working. |
| C | Lemke Oliver–Soundararajan biases in non-abelian Frobenius classes of consecutive primes | **KILLED (computed null)** | Splitting field of `x³−2` (S3), all primes to 10⁹. The abelian part shows the expected bias (same class mod 3: 0.4451 vs 0.5). The cube-residue bit of the next prime is independent of the previous class: z = −1.52, −0.06, +1.30. This matches the Hardy–Littlewood prediction that consecutive-prime correlations factor through the maximal abelian quotient. Code: `scripts/consecutive_frobenius_s3.c`. |
| D | Bias of quartic and higher-order Gauss sums at primes | **ACTIVE EXPERT FRONT** | Dunn–Radziwiłł, *Bias in cubic Gauss sums: Patterson's conjecture* (Annals 200 (2024); arXiv 2109.07463). David–Dunn–Hamieh–Lin, *Quartic Gauss sums over primes and metaplectic theta functions* (arXiv 2306.11875; to appear in ANT), which states the X^{3/4} conjecture. |
| E | Murmurations | **CROWDED** | He–Lee–Oliver–Pozdnyakov; Zubrilina; Sawin–Sutherland (arXiv 2504.12295); Lee–Oliver–Pozdnyakov (Dirichlet characters, arXiv 2307.00256); Maass forms; depth aspect (arXiv 2606.08353); function fields (arXiv 2603.13802). |
| F | True size and sign bias of the error term `N_a(x) − A·li(x)` in Artin's primitive-root conjecture | **OPEN, kept in reserve** | No numerical study of the error term's distribution was found. Neighbours: Fiorilli–Jouve on biases in radical extensions (arXiv 2001.05428); Goldmakher–Martin–Péringuey, *Refinements of Artin's conjecture* (arXiv 2502.19601); Fan–Pollack (arXiv 2505.05601). Not chosen as lead because it sits on the Kummer-tower barrier that killed Pointed Order Zeta. It is the natural second programme, and Pointed Order Zeta already supplies two assets for it. First, its Session-6 profinite lcm-covariance theorem (`notes/session6-go-no-go.md`) gives the exact Haar variance of the Artin indicator, which is the null model for the error term's size. Second, its exact `src/residual_index.py` engine, with pre-factored `p−1` support, computes the data. |
| G | Primes dividing no Apéry-like number (`e^{-1/2}` heuristics) | **PARTLY DONE** | Malik–Straub (Res. Number Theory 2016) give the `e^{-1/2}` heuristic; OEIS A133370, A260793; Caruso–Fürnsinn–Vargas-Montoya–Zudilin (arXiv 2510.23298). |
| H | Equidistribution and fine-scale statistics of roots of cubic congruences mod primes | **OPEN BUT HARD** | Kowalski–Soundararajan (arXiv 2003.12965) call degree ≥ 3 for prime moduli "an outstanding open problem". Marklof–Welsh (arXiv 2105.02854) treat fine-scale statistics for quadratic congruences over all moduli. |

Also considered briefly but not searched in depth:

- the density of `p + 2^k` (Romanoff);
- Paley-graph clique numbers;
- the Jacobsthal function of primorials;
- "hidden signals" in greedy prime-defined sequences, in the style of Ulam numbers.

## Why A wins

1. **New object, classical ingredients.** Dummit–Dummit–Kisilevsky define quadratic, cubic and
   quartic residue matrices and classify which ±1 matrices arise, but say nothing about spectra.
   The large-sieve literature bounds operator norms only.
2. **The null model is exact.** Reciprocity fixes the symmetry type of the matrix. A uniformly
   random matrix with the same symmetry is a parameter-free baseline.
3. **The deviations have deep mechanisms.**
   - n = 3: the Kubota–Patterson cubic theta function.
   - n = 4: the quartic theta function, whose Fourier coefficients at primes are *not known in
     closed form*.
   - n = 2: mean squares of real character sums over primes, a Montgomery–Hooley-type secondary
     term.
4. **Natural quantifiers.** X → ∞ limits, scaling exponents, and constants (κ₃, c₄).
5. **Cheap, decisive computation.** The pilot reached dimension 14,642 in minutes on four cores.
