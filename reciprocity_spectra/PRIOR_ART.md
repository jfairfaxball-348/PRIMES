# Prior-art and collision audit: spectra of power-residue matrices

Audit date: 2026-10-24.
Tools: web search (Parallel Search) and the arXiv, journal and OEIS pages it surfaced.
Status vocabulary: the PRIMES `docs/NOVELTY_PROTOCOL.md` statuses.

A negative search is not a novelty proof. This area sits next to an active research group: Dunn,
de Faveri, Hoffstein, David, Hamieh and Lin. Expert review is required before any external claim.

## Object

Let `n ∈ {2, 3, 4}` and let `P_n(X)` be one of:

- the odd rational primes `≤ X` (n = 2);
- the primary degree-one primes of `Z[ω]` with norm `≤ X` (n = 3);
- the primary degree-one primes of `Z[i]` with norm `≤ X` (n = 4).

The *power-residue matrix* is `R_n(X) = ((π/ρ)_n)_{π,ρ ∈ P_n(X)}`, with zero diagonal.
The programme studies its singular values, eigenvalues, outliers and singular vectors as X → ∞.

## Collision ladder

| Step | Query family | Closest hits | Relation |
|---|---|---|---|
| 1 Exact language | "quadratic/cubic/quartic residue matrix", "Legendre symbol matrix eigenvalues primes" | D. Dummit, E. Dummit, H. Kisilevsky, *Characterizations of quadratic, cubic, and quartic residue matrices*, J. Number Theory 168 (2016) 167–179 (arXiv 1512.06480). E. Dummit, *Characterizations of the dth-power residue matrices over finite fields* (arXiv 1809.10225). E. Dummit, *The number of quadratic, cubic, and quartic residue matrices* (submitted) | **Same matrices, different questions.** These papers characterize which sign or root-of-unity matrices occur (block skew/symmetric structure from reciprocity) and count them. Nothing on spectra, outliers or limit laws. Their characterization is our null-model symmetry. |
| 1′ | "determinant Legendre symbols" | Z.-W. Sun, Chapman, Wu, Ren–Sun (2018–2025) | Different object: matrices indexed by residues mod a *fixed* prime. |
| 2 Synonyms | "large sieve real characters", "cubic large sieve", "quartic large sieve" | Heath-Brown, *A mean value estimate for real character sums* (Acta Arith. 72, 1995); Heath-Brown, *Kummer's conjecture for cubic Gauss sums* (Israel J. Math. 2000); Gao–Zhao, *Large sieve inequalities for quartic characters* (Q. J. Math. 2012); Blomer–Goldmakher–Louvel; Goldmakher–Louvel (number fields) | **Operator-norm bounds only.** A large-sieve inequality is an upper bound for `‖R_n(X)‖` and its rectangular blocks. Heath-Brown's quadratic bound is `(MN)^ε (M+N)`; removing the ε is conjectured. |
| 3 Equivalent forms | "Patterson conjecture", "cubic large sieve sharp", "non-orthogonality large sieve" | Patterson (1978); Heath-Brown–Patterson (1979); Dunn–Radziwiłł, *Bias in cubic Gauss sums: Patterson's conjecture* (Annals 200 (2024), arXiv 2109.07463): the cubic large sieve is sharp up to `X^{o(1)}` under GRH; **de Faveri–Dunn–Hoffstein, *Non-orthogonality of the cubic and quartic large sieves via Rankin–Selberg* (arXiv 2607.07911, July 2026)**: unconditional, and the obstruction is the bias of Gauss sums | **KNOWN: the operator-norm shadow of the n = 3, 4 outliers.** The top singular value of `R_3`, `R_4` exceeds the orthogonal benchmark because of Gauss-sum bias. Our cubic finding that the top singular vector is the Gauss-sum vector is very likely implicit in these proofs: **POSSIBLE_OVERLAP**. |
| 3′ | "quartic theta function Fourier coefficients" | Suzuki (coefficients at squares); Eckhardt–Patterson, *On the Fourier coefficients of biquadratic theta series* (Proc. LMS 1992); David–Dunn–Hamieh–Lin (arXiv 2306.11875), who note that the quartic theta coefficients "are in general not all determined" | Background for conjecture RS-3: the quartic outlier vectors are a candidate numerical proxy for these coefficients. |
| 4 Stronger theorems | spiked random matrices; BBP; quarter-circle law for arithmetic matrices | Baik–Ben Arous–Péché (2005); Benaych-Georges–Nadakuditi (2012); Knill, *Some experiments in number theory* (arXiv 1606.05971: circular law for some Gaussian-prime matrices, not residue symbols) | No theorem found that implies the spike law, the outlier family, or the quadratic 1/log D bulk law. |
| 5 Sequence/data | OEIS for spectral constants | none | — |
| 6 Citation chain | DDK → Dummit–Granville–Kisilevsky, *Big biases amongst products of two primes* (Mathematika 2016) | Biases with a `log log x` scale for `pq` with prescribed `χ(p), χ(q)` | Possibly related to the slow quadratic corrections, but not the same statement. |
| 7 Expert translation | — | "Spectral statistics of power-residue symbol matrices on degree-one primes. The cubic case is a BBP spiked model whose spike is the Kubota–Patterson theta function. The quadratic case follows the quarter-circle law with a 1/log D Montgomery–Hooley-type correction." | For contacts: Kisilevsky/Dummit, Dunn/de Faveri/Hoffstein, David. |

## Conclusions by statement

| Statement | Status |
|---|---|
| `‖R_3(X)‖`, `‖R_4(X)‖` exceed the orthogonal (large-sieve diagonal) benchmark because of Gauss-sum bias | **KNOWN** (Dunn–Radziwiłł under GRH; de Faveri–Dunn–Hoffstein unconditionally) |
| Patterson bias `Σ_{N(π)≤X} g̃(π) ~ c X^{5/6}/log X` | **KNOWN** (Dunn–Radziwiłł under GRH) |
| The cubic top singular vector is (conjugate) normalized cubic Gauss sums | **POSSIBLE_OVERLAP** (implicit in the sharpness and non-orthogonality mechanisms) |
| Quantitative spike law: `σ₁ = θ + D/θ`, `θ ≈ κ₃ X^{2/3}/log X`, `κ₃ ≈ 1.42`, overlap `= √(1 − D/θ²)` | **SEARCHED_NO_COLLISION_FOUND** |
| Outlier *family* labelled by small `u`, with singular vectors `conj(g̃)·(u/·)₃` | **SEARCHED_NO_COLLISION_FOUND** (de Faveri–Dunn–Hoffstein's Rankin–Selberg input may contain the Gram-matrix information) |
| Quartic outliers exist but their vectors are not twisted Gauss sums; slowly growing strength | **SEARCHED_NO_COLLISION_FOUND** (outlier existence is known at norm level) |
| The quadratic Legendre matrix of primes has a compressed bulk and edge: `m₄ = 2 − c₄/log D`, `c₄ ≈ 1.2` | **SEARCHED_NO_COLLISION_FOUND** |
| Bulk quarter-circle universality for n = 3, 4 after removing outliers | **SEARCHED_NO_COLLISION_FOUND** |

## Search log (2026-10-24)

- Periodic points of `x²−1` mod p; post-critically finite proportion; Fariña-Asategui; Radi. Area B.
- Lemke Oliver–Soundararajan for Chebotarev classes; consecutive primes in cubic fields. Area C.
  Nothing found, then tested computationally.
- Apéry numbers mod p, `e^{-1/2}`; Malik–Straub; Rowland–Yassawi. Area G.
- Roots of polynomial congruences modulo primes; Hooley; Marklof–Welsh. Area H.
- Murmurations: families surveyed for 2025–2026. Area E.
- Artin conjecture error term; Chebyshev bias for primitive roots; Fiorilli–Jouve radical
  extensions. Area F.
- Quartic Gauss sums bias; Dunn–Radziwiłł; David–Dunn–Hamieh–Lin. Area D.
- Legendre symbol matrix eigenvalues; cubic residue matrix; reciprocity graph. Found DDK and Knill.
- Extremal vectors of the cubic large sieve; Baier–Young; Heath-Brown sharpness. Found
  de Faveri–Dunn–Hoffstein 2607.07911.
- Quadratic large sieve optimal constant; Heath-Brown ε-removal. No numerical study found.

## RS-S008 refresh (2026-10-25)

The searches used Parallel Search; the queries are listed below.

**New relevant sources:**

- G. Chinta, S. Friedberg, J. Hoffstein, *Double Dirichlet series and theta functions* (2011).
  It makes a conjecture on the Fourier coefficients of the theta function on the 6-fold cover of
  GL(2), and notes that for n = 3 the coefficients are essentially cubic Gauss sums (Patterson).
  https://gchinta.github.io/assets/pdfs/doubledirichlet.pdf
- R. Bröker, J. Hoffstein, *Fourier coefficients of sextic theta series*, Math. Comp. (2015),
  DOI 10.1090/mcom3044, arXiv 1312.0568. It gives partially proven and partially conjectured
  values of τ(π)², τ(π²) and τ(π⁴) at primes.
- S. Friedberg, D. Ginzburg, *Descent and theta functions for metaplectic groups*,
  arXiv 1403.3930. A descent framework consistent with the Patterson and Chinta–Friedberg–Hoffstein
  conjectures.
- *Vanishing of quartic and sextic twists of L-functions*, arXiv 2301.05329. It introduces
  "totally order-ℓ" characters, and finds that sextic Gauss sums equidistribute much more slowly
  in the full family than in the totally sextic subfamily. This is possibly related to our
  unit-class dichotomy, but it concerns Dirichlet characters, not our matrices.
- arXiv 2607.27131: second moments of Hecke L-functions of r-th order characters, citing the
  X^{5/6} Patterson barrier and the de Faveri–Dunn–Hoffstein result.

**Not peer-reviewed, different object:**

- Notes from October 2026 on a "quasi-Riemann hypothesis" use sextic symbols, sextic Gauss sums
  and the cubic theta function to bound Möbius sums:
  - https://www.math.uwaterloo.ca/~mrubinst/quasi_rh_notes/zeta_7_8_guide.pdf
  - https://www.emergentmind.com/openai-math-explorer/papers/6.pdf
- They do not study residue matrices. They are recorded because they use the same
  sextic-to-cubic Gauss-sum mechanism.

**Status by finding:**

| Statement | Status |
|---|---|
| Conjugation-matched null; cubic `C·P` Hermitian (exact identities) | KNOWN_IMPLIED (direct consequences of Galois equivariance and cubic reciprocity; no spectral use found) |
| RS-6C: bulk gap ratios match the symmetry-matched null | SEARCHED_NO_COLLISION_FOUND |
| RS-7/RS-7a: sextic cluster above the null, enriched in twisted conj(g̃6) spans | SEARCHED_NO_COLLISION_FOUND |
| RS-7b: twist enhanced iff unit-class factor unramified at 3 | POSSIBLE_OVERLAP: 3-adic and unit normalization is intrinsic to the coefficients of the sextic theta function (Chinta–Friedberg–Hoffstein; Bröker–Hoffstein), but no statement about these twists or matrices was found. NOVELTY_REQUIRES_EXPERT_REVIEW |
| Earlier statuses (RS-1 to RS-4) | unchanged from the 2026-10-24 audit |

**Queries:** sextic Gauss sums distribution; sextic theta function metaplectic; bias sextic Gauss
sums primes; residue matrix eigenvalues primes; large sieve sextic characters; cubic Gauss sums
twisted Hecke character primes; de Faveri Dunn Hoffstein non-orthogonality; Gauss sums primary
normalization ramified at 3; Chinta Friedberg Hoffstein sextic theta conjecture; Bröker Hoffstein
sextic theta series.
