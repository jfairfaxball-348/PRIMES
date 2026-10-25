# Expert-review prompt for OpenAI's Astra agent (RS-S008)

**Instructions for the owner.** This prompt is ready to paste. Nothing has been sent; you decide
whether and when to send it. If Astra can read attachments, attach `reciprocity_spectra/NOTE_DRAFT.md`
(and the repository, if you choose to share it). Paste Astra's full reply into
`reciprocity_spectra/ASTRA_RESPONSE_<date>.md` and commit it. The next session (RS-S009) starts
from that reply.

Everything below the line is the prompt.

---

You are being consulted as an expert in analytic number theory and metaplectic forms: Gauss sums,
Kubota–Patterson theta functions, and large sieves for n-th order residue symbols. Below are
finite numerical findings about matrices of power-residue symbols between primes, followed by
precise questions. Please answer as a referee would.

**How to answer:**

- Distinguish what is **known** (give a citation: authors, title, venue or arXiv number), what
  **follows from** known results (sketch the argument), and what is **your conjecture or
  heuristic**.
- Do not call anything new or open unless you can point to evidence. "I don't know" is a useful
  answer.
- Where you propose an explanation, give a concrete numerical test that could falsify it (a
  quantity, its predicted value or scaling, and the expected size of the deviation).
- Point out any error in our conventions or reasoning.
- If you cannot access attachments, answer from this text alone.

## Setup

- **Index set.** π = a + bω runs over the primary degree-one primes of ℤ[ω]: a ≡ 2 (mod 3),
  b ≡ 0 (mod 3), N(π) = p ≡ 1 (mod 6), p ≤ X. Both π and π̄ are included.
- **Matrix.** For n = 6, C = ((π/ρ)₆) has dimension D ≈ X/log X and a zero diagonal.
  (π/ρ)₆ is the sixth root of unity ≡ π^{(N(ρ)−1)/6} mod ρ, with ζ₆ = 1 + ω.
  Exactly: ((·)/ρ)₆² is the cubic symbol and ((·)/ρ)₆³ is the quadratic symbol.
  Analogous matrices exist for n = 2, 3 and 4.
- **Gauss sums.** g̃₆(π) = Σ_{t mod p} (t/π)₆ e(t/p)/√p, which is unimodular.
- **Null model.** The control is a random matrix that satisfies exactly the reciprocity relation
  C_ρπ = s(π, ρ)·C_πρ (s a ±1 class function mod 4) and the conjugation identity
  C[π̄, ρ̄] = conj C[π, ρ]. It is uniform on the orbits of those two identities, with the forced
  (π, π̄) entries copied. Random matrices of this kind have their largest singular value at about
  2√D.

## Findings

All of these are reproducible. Pre-registered tests were committed before the data were
computed. Each has a PASS/FAIL record, and failures are kept.

**(F1) Cubic spike.** For n = 3 there is one large outlier:

- σ₁ = θ + D/θ with θ ≈ κ₃ X^{2/3}/log X, κ₃ ≈ 1.42 (stable for X from 5·10³ to 3.2·10⁵);
- the top singular vector has overlap √(1 − D/θ²) with conj(g̃₃), as in a BBP spiked model.

We understand this as the matrix form of the Patterson bias (Dunn–Radziwiłł; de Faveri–Dunn–
Hoffstein).

**(F2) Sextic cluster.** The sextic matrix has a growing cluster of singular values above the null:

| X | values above the null |
|---:|---:|
| 4·10⁴ | 7 |
| 1.6·10⁵ | 22 |
| 3.2·10⁵ | 34 |

- σ₁/(2√D) is 1.030, 1.042 and 1.050 at those scales, against about 1.000 for the null.
- The cluster vectors are delocalized, with no concentration on small primes or residue classes.
- They are increasingly enriched in the span of the twists w_u = conj(g̃₆)·(u/π)₆ over small u:
  2.96 times a random span of equal dimension at X = 3.2·10⁵.

**(F3) The dichotomy (main finding).** Let r_u = ‖C w_u‖/(√D‖w_u‖); random unit vectors give
r ≈ 1.000 ± 0.005. For u ∈ ℤ[ω] coprime to 3:

- if u ≡ ±(primary), i.e. u ≡ ±1 or ±2 mod 3 with zero ω-coefficient mod 3, then r_u ≥ 1.11;
- for each of the other four associates ζ₆ʲu (j = 1, 2, 4, 5), r_u ≤ 0.98, below the random
  level.

This held without exception:

- for 492 to 2094 twists per scale;
- with N(u) ≤ 100 or ≤ 300;
- at X = 2·10⁴, 4·10⁴, 8·10⁴, 1.6·10⁵, 3.2·10⁵ and 6.4·10⁵;
- including pre-registered tests at the last two scales.

Example at N(u) = 7, X = 1.6·10⁵: the two ±primary associates give r = 1.28; the other four give
0.96. For the ramified u = 1 − ω, only the conjugate twist conj(g̃₆)·conj((u/π)₆) is enhanced
(r ≈ 1.15).

**Exact reformulation (we checked this).** (ζ₆ʲ/π)₆ = ζ₆^{j(p−1)/6}. So
(ζ₆ʲu/π)₆ = ζ₆^{j(p−1)/6}·(u/π)₆, and p ↦ ζ₆^{j(p−1)/6} is a Dirichlet character mod 36. It is
unramified at 3, equal to (−1/p), exactly for j ∈ {0, 3}. Empirically, a twist is enhanced iff
its unit-class factor is unramified at 3.

**(F4) Strength profile.** In the spiked-model reading, θ_u²/D = r_u² − 1.

- For ±primary u, θ_u²/D decays like N(u)^{−0.19}. The exponent is stable for X from 2·10⁴ to
  6.4·10⁵.
- At u = 1, r₁ = 1.322, 1.354, 1.362, 1.379, 1.396 and 1.418 at X = 2·10⁴, 4·10⁴, 8·10⁴,
  1.6·10⁵, 3.2·10⁵ and 6.4·10⁵. At the largest X it just exceeds √2, the threshold for an
  individual BBP outlier.
- A naive guess that the strengths follow sextic theta coefficients, |τ(u)|² ∝ N(u)^{−2/3}, does
  not fit.

**(F5) Associate sum rule.**

- Exact: Σ_{j=0}^{5} ‖C D_j w‖² = 6 Σ_{c mod 36} ‖C (w restricted to p ≡ c mod 36)‖², by
  orthogonality of the unit characters.
- Numerically, the sum over the six associates of (r²−1) is about 0 at small X (0.04 ± 0.11 at
  X = 4·10⁴). It drifts upward to 0.75 ± 0.29 at X = 6.4·10⁵.

**(F6) Failed models.**

- Counting individually supercritical twists predicts 0 outliers below X ≈ 6·10⁵, but there are 7
  to 34.
- A model of independent subcritical spikes (strengths from F4, random left directions) predicts
  about 16 weak outliers at X = 4·10⁴, against 7 stronger ones observed.
- The images C w_u of the strongest twists are partly aligned: maximum |correlation| 0.37,
  against 0.05 for the null.

## Questions

**Q1 (mechanism of F3).** Why are twists of conj(g̃₆) by (u/π)₆ enhanced exactly when the twist's
unit-class factor is unramified at 3, and suppressed below the random level otherwise?

- Is this a known property of the sextic theta function on the 6-fold cover of GL₂ (Chinta–
  Friedberg–Hoffstein 2011; Bröker–Hoffstein, Math. Comp. 2015) or of Kubota's sextic Dirichlet
  series?
- For example: do Fourier coefficients, or the residues of Σ g₆(π)ψ(π)N(π)^{−s}, vanish or change
  for characters ψ ramified at 3?
- Please write ‖C w_u‖² as a double sum of twisted Gauss sums. Identify which term produces the
  enhancement for unramified twists and the depletion for ramified ones.

**Q2 (strength law F4).** What does theory predict for the size of the enhancement r_u² − 1 as a
function of N(u) and X?

- Is the slow decay N(u)^{−0.19}, rather than N(u)^{−2/3}, plausible? For example, if τ₆ at
  non-squarefree or non-prime u behaves differently, or if the relevant coefficients are those of
  the cubic theta function at related arguments (via χ₆ = conj(χ₃)·χ₂).
- Should r₁ grow without bound in X (so that the u = 1 twist becomes a genuine BBP outlier, as at
  X = 6.4·10⁵), or converge? At what rate?

**Q3 (cluster F2/F6).** Given many correlated, individually subcritical twisted spikes, what is the
right random-matrix model for the number and positions of outliers above 2√D? Is there a known
result on finite-rank-per-scale but growing-rank deformations with structured left vectors that
predicts 7, 22 and 34 at D = 4178, 14640 and 27554? Which quantity should we measure to pin down
the left-vector correlation structure?

**Q4 (prior art).** Have spectra, singular values or outliers of power-residue matrices
((π/ρ)ₙ) over primes, for n = 3, 4 or 6, been studied? Is our cubic statement F1 (top singular
vector is the conjugate Gauss-sum vector, with BBP overlap) implicit in Dunn–Radziwiłł or
de Faveri–Dunn–Hoffstein? Is anything in F2–F5 known? Please give references.

**Q5 (the best next test).** What single computation would most sharply confirm or refute your
explanation of F3? Examples: a different index normalization; twists by characters of conductor
9 versus 4; restriction to p in a fixed class mod 36; the cubic or quartic analogue of the
dichotomy; or a function-field analogue over 𝔽_q[t]. Please state the predicted outcome.

Please end with a short list: (a) statements you consider known, with references; (b) statements
you can derive or sketch; (c) statements you believe are open or doubtful.
