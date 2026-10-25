# Sextic Theta Function: Checks, Questions, and Findings

The derivable parts all point to the sextic theta function. Finding 1 is known in substance. Findings 2–5 look new to me, and most of their structure has a derivable explanation. One piece, the sum rule in finding 5, I can't explain. First, three things to check.

## Checks before the questions

### 1. An exact symmetry: r_v = r_{−v̄}

Since (t/ρ̄)₆ = conj((t/ρ)₆) for rational t, you get g̃₆(ρ̄) = (−1/ρ)₆·conj(g̃₆(ρ)).

Hence conj(w_u(ρ̄)) = w_{−ū}(ρ).

With C[π̄,ρ̄] = conj C[π,ρ], this gives (Cw_u)π̄ = conj((Cw{−ū})π), so ‖Cw_u‖ = ‖Cw{−ū}‖.

For u = 1−ω you have ū = ζ₆(1−ω), so r_ū must equal r_{−u}. If only one associate of 1−ω is enhanced in your data, there's a bug, or I've misread "conjugate twist."

### 2. The cubic case should have many outliers, not one

Patterson's τ₃ is unimodular at squarefree arguments.

The same theta argument that gives your sextic twists (Q2) predicts cubic twists w_u = ḡ̃₃·(u/·)₃ with θ_u² ≈ θ₁²·N(u)^{−1/3}.

At X = 4·10⁴ your fit gives θ₁ ≈ 157, so θ₁²/D ≈ 5.9. Every ±primary u with N(u) ≲ 200 would then be individually supercritical: dozens of outliers.

Please check σ₂, σ₃, … for the cubic matrix. If they really sit in the bulk, my scaling below is wrong.

### 3. Your g̃₆ is not the Kubota-normalized Gauss sum

With e(t/p), compared with Heath-Brown–Patterson's e(Tr(x/π)), g_yours = (π̄/π)ₙ·g_HBP.

For n = 3 this factor is 1 (by reciprocity plus conjugation).

For n = 6 it is (π̄/π)₂ = ((2a−b)/p). Using 4p = (2a−b)² + 27(b/3)² and 2a−b ≡ 1 (mod 3), this depends only on 2-adic data.

So it can't create a 3-adic effect, but it does mix the mod-4 classes. Use the standard normalization for anything involving composite moduli.

## Q1: The dichotomy

**Exact formula for ‖Cw_u‖².** By the twist identity conj((c/ρ)₆)·g̃₆(ρ) = g̃₆(c,ρ):

‖Cw_u‖² = Σ_π |S(πu)|², where S(c) = Σ_{ρ≠π} g̃₆(c,ρ).

Expanding, the diagonal ρ₁ = ρ₂ gives exactly D(D−1). The off-diagonal part is Σ_{ρ₁≠ρ₂} g̃₆(ρ₁)·conj(g̃₆(ρ₂))·conj((u/ρ₁)₆)·(u/ρ₂)₆·Σ_π conj((π/ρ₁)₆)·(π/ρ₂)₆. All of the effect is in this off-diagonal term. Heuristically it equals Σ_π |M(πu)|², where M is the theta main term of S.

**Hasse–Davenport identity (derivable).** Use the duplication formula with Ireland–Rosen's g(χ_ρ)³ = pρ, which holds in your normalization. At primes this gives:

> g̃₆(ρ) = conj((2/ρ)₃) · (ρ/|ρ|) · g̃₂(ρ) · conj(g̃₃(ρ)), with g̃₂ ∈ {1, i} according to p mod 4.

Twisting by c then gives g̃₆(c,ρ) = conj(g̃₃(4c,ρ)) · (c/ρ)₂ · (ρ/|ρ|) · g̃₂(ρ). This agrees with Chinta–Friedberg–Hoffstein's G⁽⁶⁾ = (G⁽³⁾)², which they state while ignoring characters ramified at 2n and the quadratic Gauss sum. (cuny)

**The unit twist ζ₆ʲ now becomes transparent:**

- It multiplies the cubic Gauss sum by (ω/ρ)₃^{2j}, a character ramified at 3 that is trivial iff 3 | j.
- It multiplies the quadratic factor by (−1/p)ʲ.

So j ∈ {0, 3} only flips a 2-adic sign. For the other j, the frequency of the cubic Gauss sum is rotated by ω^{±1}, which is a non-cube at λ = 1−ω.

**Why +u and −u agree (derivable).** The classes p ≡ 1 and p ≡ 3 (mod 4) enter with phases 1 and −i (from g̃₂). Suppose their main terms are otherwise equal. Then S₁ and S₃ are orthogonal in the real inner product, so ‖S₁ + S₃‖ = ‖S₁ − S₃‖. Prediction: the inner product of the images of the two mod-4 restrictions of w_u is nearly purely imaginary.

**Why the ω-rotated twists lose the main term (my guess).** I think the residue of the twisted Kubota series at s = 2/3 behaves like a local Whittaker functional at λ:

- Rotating the frequency by a cube (±1) preserves |τ₆|.
- Rotating it by a non-cube kills it.

I know no reference for this at n = 6. Patterson's explicit cubic coefficients would show whether the same thing happens at n = 3, which makes the cubic twists in check 2 a calibration.

**Why the others fall below random (partly derivable).**

Write w_u^(a) for w_u restricted to the class p ≡ a (mod 36). The six associate twists are the discrete Fourier transform of these restrictions, so Σⱼ ‖Cw_{ζʲu}‖² = 6·Σ_a ‖C w_u^(a)‖².

If the noise were independent of the main term, Σⱼ(rⱼ² − 1) would be at least (r₀² − 1) + (r₃² − 1) ≈ 2(r_u² − 1).

You observe ≈ 0 at 4·10⁴. So the class-restricted noise must be anti-correlated with the main term.

Since Tr C*C = D(D−1) exactly, any enhancement is paid for somewhere. At small X it is paid inside the associate orbit, which forces r < 1 for j ∉ {0, 3}.

I can't explain the anti-correlation itself. If it is a finite-X secondary term, the six-sum should climb toward 2·mean(r_u² − 1). Your drift from 0.04 to 0.75 is in that direction.

## Q2: Scaling

**Size of the theta residue.** CFH normalize so that the residue of the k-fold Kubota series at s = 1/2 + 1/k is a constant times τ⁽ᵏ⁾(m)/Nm^{1/(2k)}. Check this against n = 3: the residue's mean square is ~N^{−1/3}. That is exactly what reproduces your θ ∝ X^{2/3}/log X. (cuny)

**Prediction for n = 6.** Assume a Patterson-type main term over primes, K·τ₆(c)·N(c)^{−1/12}·X^{2/3}/log X. Then:

> r_u² − 1 ≈ A·κ_u·N(u)^{−1/6}·X^{1/6}/log X.

**N(u) dependence.**

The predicted exponent is −1/6 ≈ −0.17. You see −0.19.

Your naive −2/3 uses the pole location as if it were the decay rate of the coefficients.

A cubic effect in disguise (via χ₆ = χ̄₃χ₂) would give −1/3, which your data disfavour.

**u = 1 against the formula.** The ratio (r₁² − 1)·log X / X^{1/6} at your six values of X is 1.42, 1.51, 1.47, 1.47, 1.45, 1.46. That is remarkably flat.

**Caveat:** r₁² − 1 ≈ 0.076·log X fits equally well, because the two curves have the same local slope near log X ≈ 12. They separate only at larger X:

| X | r₁ if X^{1/6}/log X | r₁ if log X |
|---|---:|---:|
| 10⁷ | 1.53 | 1.49 |
| 10⁸ | 1.65 | 1.55 |

You don't need the whole matrix for this. Sample a few thousand rows π.

**Unbounded growth.** If the formula holds, r₁ ~ X^{1/12}/√(log X), so it grows without bound but very slowly.

**Interpretation.** r_u = √2 is exactly θ_u = √D. The u = 1 spike therefore only reaches threshold near 6·10⁵, and even at 10⁸ it would sit at about 1.04 × 2√D. So your σ₁/2√D ≈ 1.05 at 3.2·10⁵ is collective, not this one spike.

Also note what r_u² − 1 measures: the mean square of τ₆(πu) over primes π. These coefficients are not fixed by the Hecke relations, so your experiment is a numerical probe of them.

## Q3: Random-matrix model

This isn't finite-rank BBP. Use Benaych-Georges–Nadakuditi (2012): the outliers are set by the singular values of the perturbation P, not by the individual spikes. Coherent subcritical spikes add in quadrature: k spikes sharing a left vector give a singular value of √(Σθ²). Since the rank here is hundreds, the information-plus-noise model (Dozier–Silverstein 2007) or rectangular free convolution is the right tool.

**What to measure:**

**Excess spectrum.** Orthonormalize the twist basis Q and compute QCCQ/D, along with the null model compressed to the same span. The span has dimension ~D/25 to D/8, so the null spreads in Marchenko–Pastur fashion and individual r-values can't be compared directly. The excess eigenvalues t_k² > 1 predict outliers at √D(t_k + 1/t_k). Check whether this reproduces 7, 22, 34.

**Image correlations.** Compute these within the orbits {u, −u, ū, −ū} and among Hecke-related u. If two twists share their main term, |corr| = √((r_u² − 1)(r_v² − 1))/(r_u·r_v). For r = 1.28 that gives 0.39, against your observed maximum of 0.37. That is suggestive.

## Q4: Prior art

**Finding 1.** It is essentially a matrix restatement of the following:

- Heath-Brown's cubic large sieve, with its (MN)^{2/3} term.
- Dunn–Radziwiłł, cited for the X^{5/6} main term in the cubic case. (arxiv)
- de Faveri–Dunn–Hoffstein (arXiv 2607.07911, July 2026). They prove unconditionally that the cubic and quartic large sieves fail to be perfectly orthogonal, with the Gauss-sum bias as the main obstruction. That is your outlier, stated as a norm bound. The BBP form and the constant 1.42 aren't in any of them, as far as I know. (arxiv)

**Sextic theta function.** Your Bröker–Hoffstein reference is Math. Comp. 85 (2016), 1901–1927, which gives partially proven, partially conjectured values of τ(π)², τ(π²) and τ(π⁴) at primes π. The CFH conjecture relates the sextic coefficients at squares to cubic Gauss sums, and is proved over a rational function field. Neither addresses unit or 3-adic dependence at squarefree arguments, as far as I know. Compare your per-row main terms with their τ(π)² tables. (Fourier coefficients of sextic theta series +2)

**Quartic analogue.** David–Dunn–Hamieh–Lin conjecture an X^{3/4} bias for quartic Gauss sums over primes, which they say is out of reach even under GRH. (arxiv)

**Spectra of power-residue matrices over primes.** I know of no such study, for n = 3, 4 or 6. Findings 2–5 look new.

## Q5: Decisive computation

Drop the primes and the random-matrix layer, and compute Kubota partial sums at the six unit frequencies:

> Tⱼ(X) = Σ_{N(n)≤X, (n,6)=1} g̃₆(ζ₆ʲ, n), for j = 0, …, 5.

Use the HBP normalization and twisted multiplicativity for composite n. g̃₆ vanishes at non-squarefree n coprime to the frequency.

**Prediction:** |T₀| ≈ |T₃| grow like X^{2/3}, while T₁, T₂, T₄, T₅ stay O(X^{1/2+ε}). On a log-log plot that is slope ≈ 0.67 against ≈ 0.5. Your existing data reach 6.4·10⁵, which should separate the two.

**What would kill my explanation:**

- If T₁ or T₂ also has slope 2/3, the dichotomy is not a theta-residue effect.
- If T₀ doesn't have slope 2/3, findings 2–4 need a different source.

## Summary lists

### (a) Known, with references

- Your outlier is the Gauss-sum bias: Patterson 1977, Heath-Brown–Patterson 1979, Heath-Brown 2000, Dunn–Radziwiłł, de Faveri–Dunn–Hoffstein 2026.
- For n ≥ 4, the theta coefficients at squarefree arguments are not determined by the Hecke relations (CFH, Kazhdan–Patterson).
- Bröker–Hoffstein give conjectural values of τ₆ at primes.

### (b) Derivable (sketched above)

- At primes, g̃₆ = conj((2/ρ)₃)·(ρ/|ρ|)·g̃₂·ḡ̃₃.
- A unit twist rotates the cubic frequency by ω^{2j} and adds a factor (−1/p)ʲ.
- r_v = r_{−v̄} exactly.
- The Parseval and trace sum rules.
- The mod-4 phase explanation of r_u ≈ r_{−u}.
- The predicted N(u)^{−1/6}·X^{1/6}/log X scaling.

### (c) Open or doubtful

- That non-cube rotations kill the residue at λ: my guess.
- The source of the anti-correlation behind finding 5.
- Whether the cubic matrix really has a single outlier, which would contradict (b).
- X^{1/6}/log X versus log X growth: undecided below 10⁸.
