# Proof route for CAND-001: hard version first

Status: **RS-S013 audit complete (2026-10-26)**. The frozen CAND-001 package is
**REFUTED** by its unreduced strength law; its matrix dichotomy and prime-bias
components are not refuted. The unrestricted Type II operator route is ruled
out; the arithmetic-coefficient route is unresolved. See section 7 before
using the historical plan below. Nothing here is proved unless it is marked
*exact* or *known*.

Order of attack (PROTOCOL §9):

1. the prime-level and matrix-level statements;
2. only after documented exhaustion of the first: all-n Kubota-series, function-field, or
   conditional fallbacks.

## 1. Target statements (hard version)

### Notation

- ρ runs over primary split primes of ℤ[ω] with p = N(ρ) ≤ X.
- g̃(c, ρ) = g6_trace(c, ρ)/√p, where g6_trace(c, ρ) = Σ_{x mod ρ} (x/ρ)₆ e(Tr(cx/ρ)).
- χ runs over the 12 characters (m, s1, s2) of (ℤ[ω]/4)^× (`arith.mod4_character`).
- j indexes the unit classes, via ζ₆ʲ.

### H1, prime-level unit-class bias (CAND-001, statement 2)

In the matrix normalization g̃_ours = (ρ̄/ρ)₆·g̃_trace:

```
S_j(X) = Σ_{N ρ ≤ X} g̃_ours(ρ) conj((ζ₆ʲ/ρ)₆) = c_j X^{2/3}/log X + o(X^{2/3}/log X),
with c_j ≠ 0  ⟺  j ∈ {0, 3}.
```

- The exponent 2/3 = 1/2 + 1/6 is the location of the pole of the sextic Kubota series. This is
  heuristic; the cubic analogue is Patterson's X^{5/6}, proved under GRH by Dunn–Radziwiłł.
- Numerical status: registered PASS at X = 1.28·10⁶ (RS-S010-K2).
- **Refuted refinements.** A finer rule by 2-adic characters χ of (ℤ[ω]/4)^× failed twice in fresh
  windows (RS-S011-SEL, RS-S011-M0). Window statistics were probably underpowered: the main-term
  increment per window is comparable to the noise. A theoretical derivation of the 2-adic
  structure (T1 below) should come before any further numerical refinement.

### H2, matrix dichotomy (RS-7b)

For u coprime to 3, let w_u = conj(g̃₆)·(u/·)₆ and r_u = ‖C w_u‖/(√D ‖w_u‖). Then, as X → ∞:

- r_u ≥ 1 + δ(u) > 1 if u is ±primary;
- lim sup r_u < 1 otherwise.

### H3, cubic calibration (RS-8)

This is the analogous statement for n = 3, with the squarefree condition. It should follow from
Patterson's explicit coefficients. It is the testbed for the method.

## 2. Reduction of H2 to twisted prime sums

*Exact algebraic identity; checked independently in RS-S012* (Astra, Q1):

```
‖C w_u‖² = Σ_π |S(πu)|²,   S(c) = Σ_{ρ ≠ π} conj((c/ρ)₆) g̃_ours(ρ),
```

- The diagonal ρ₁ = ρ₂ contributes (D − 1)D_u exactly, where D_u counts indexed
  primes not dividing u. This equals D(D − 1) only when u is coprime to the
  entire index. RS-S013 corrects the earlier unrestricted diagonal claim.
- Everything else is the off-diagonal "dispersion" term.

So H2 is a statement about S(c) for frequencies c = πu, with N(c) up to about X. It needs:

- **(R1) Main term.** S(c) ≈ M(c), with M(c) ∝ τ₆-type coefficient · N(c)^{−1/12} · X^{2/3}/log X
  (Astra Q2). This holds on average over c.
- **(R2) Dispersion bound.**
  Σ_π |S(πu)|² = D(D − 1) + Σ_π |M(πu)|² + o(Σ_π |M(πu)|²).

**RS-S013 correction:** R2 is a positive-excess proposal for primary classes
only, not an equivalent formulation of the full H2 dichotomy. The nonprimary
limsup r_u < 1 requires a negative off-diagonal contribution of order D D_u,
which a nonnegative sum of squared main terms cannot supply. The exact identity
above survives; R1/R2 are unproved ansatzes. Dunn–Radziwiłł's cubic dispersion
estimate is a methodological model, not an existing sextic theorem.

## 3. Method template: Dunn–Radziwiłł for n = 3, adapted to n = 6

1. **Combinatorial decomposition.** Apply Heath-Brown's identity, or Vaughan's, to the sum over
   primes ρ. This splits it into Type I sums (one long smooth variable) and Type II sums
   (bilinear).
2. **Type I.** Sums of g̃(c, n)·χ(n) over all n with smooth weights are controlled by the twisted
   sextic Kubota Dirichlet series:

   ```
   ψ(s; c, χ, j) = Σ_n g6(ζ₆ʲ c, n) χ(n) N(n)^{−s}
   ```

   - **Needed (T1):** its pole at s = 1/2 + 1/6 (in normalized g̃) and the residue, as a function
     of (c, χ, j).
   - The selection rule says which (χ, j) have a nonzero residue. Theory: Kubota and Patterson
     (metaplectic Eisenstein series on the 6-fold cover), Kazhdan–Patterson, and
     Chinta–Friedberg–Hoffstein (Fourier coefficients of the sextic theta function; their
     G⁽⁶⁾ = (G⁽³⁾)² relation ignores characters ramified at 2n, which is exactly where our 2-adic
     χ lives).
   - Local computation needed: the residue's dependence on the classes of n at the primes above
     2 and 3.
   - **Numerical support:** RS-9 (trace form, all squarefree n) and RS-S011 (primes).
3. **Type II.** Bilinear sums Σ_{m~M, n~N} α_m β_n g̃(c, mn) χ(mn). By twisted multiplicativity
   (*exact*, tested) these become bilinear forms in sextic symbols (m/n)₆(n/m)₆.
   - **Needed (T2):** a bound o(X^{2/3}/log X) in the range the decomposition leaves.
   - Tools: the sextic and n-th order large sieves, i.e. Heath-Brown's method extended in
     Blomer–Goldmakher–Louvel and Goldmakher–Louvel. Their exact exponents are still to be
     extracted from the papers.
   - **This is the expected crux.** The sextic main term X^{2/3} beats square-root cancellation
     X^{1/2} by only X^{1/6}. The cubic case had X^{1/3} of room, and even there Dunn–Radziwiłł
     needed GRH plus sharp large-sieve input.
4. **Hypotheses.** Expect GRH for Hecke L-functions over ℚ(ω), at least to control error terms,
   as in Dunn–Radziwiłł. A conditional theorem under GRH would still be a theorem on the hard
   version.
5. **Uniformity in c (needed for H2, not for H1).** The main term and the Type II bound must hold
   uniformly for N(c) ≤ X, in mean square over c = πu. Dunn–Radziwiłł's level-aspect Voronoi
   formula for cubic Gauss sums is the model; we need its sextic analogue.

## 4. Inputs: known, conditional, open

| Input | Status |
|---|---|
| Hasse–Davenport factorization of g̃₆ at primes; unit and 2-adic characters; conjugation and r_u = r_{−ū}; associate sum rule | *exact*, tested in this repository |
| Twisted multiplicativity of g6_trace | *exact*, tested by direct summation |
| Sextic theta function and Kubota series: existence, meromorphy, location of the pole | known (Kubota; Patterson; Kazhdan–Patterson) |
| Explicit sextic theta coefficients at primes | partially conjectural (Bröker–Hoffstein, Math. Comp. 2015/16) |
| Residue selection by (χ, j), i.e. 2-adic and 3-adic local factors (T1) | **open**; numerical support (RS-9, RS-S011) |
| Type II bound for sextic bilinear forms below X^{2/3} (T2) | **open**; expected crux |
| Sextic level-aspect Voronoi formula (uniformity in c) | **open**; cubic analogue known (Dunn–Radziwiłł) |
| GRH for Hecke L-functions over ℚ(ω) | conjectural hypothesis (as in Dunn–Radziwiłł) |

## 5. Next bounded actions (hard route)

1. **Verify the reduction exactly.** Check the formula for ‖C w_u‖² and its diagonal/off-diagonal
   split to machine precision at small X. Confirm numerically that the off-diagonal term is
   carried by the S(πu) main terms.
2. **Type I, local theory (T1).** Derive the selection rule (m = 0, s1 = 1, with the j-pattern)
   from the local behaviour of the twisted sextic Kubota series at 2 and 3. Start by reproducing
   the cubic case (H3) from Patterson's explicit formula, as a check on the method.
3. **Type II, measurement then theory (T2).**
   - Compute the sizes of bilinear sextic sums over the ranges a Heath-Brown decomposition needs.
     This shows how much cancellation is actually present beyond the large sieve.
   - Extract the precise sextic large-sieve exponents from the literature, and state the gap.
4. **Conditional theorem attempt.** Under GRH, plus the best available Type II input, determine
   how far H1 can be proved. For example: a main term for some (χ, j), and absence for others.
   Record exactly what is achieved.

**Fallbacks.** Use these only after the hard route above is documented as exhausted:

- all-n Kubota residues (T1 alone, as a theorem in its own right);
- the function-field analogue over 𝔽_q[t];
- a cubic-only theorem.

## 6. Progress (RS-S012)

**Step 1: done (exact).** The identity ‖C w_u‖² = Σ_π |S(πu)|² is verified, with diagonal
D(D − 1) (`test_twist_norm_equals_sum_of_twisted_prime_gauss_sums`). So H2 is exactly a
statement about the off-diagonal (dispersion) part of twisted prime sums of g̃₆.

**Step 2, cubic calibration of T1.** Patterson's coefficients (Pat77 Thm 8.1; Dunn–Radziwiłł
(5.7)–(5.8)) have three properties:

- τ is supported on ±ζλ^{3n−4}cd³ with c squarefree and c, d ≡ 1 (mod 3);
- they are unimodular in c;
- they carry a factor |d| on cubes.

Dunn–Radziwiłł's main-term mechanism sieves to S = {λ⁻³cd³}. Under that mechanism, the twisted
prime sum for a frequency in the ±1 class mod 3 has main term ∝ τ·N^{−1/6}. That predicts every
feature of RS-8:

- the N(u)^{−1/3} profile;
- the squarefree condition;
- cube invariance (u = 8 behaves like u = 1);
- associate suppression.

The predicted constant ratio holds to 2–4% and converges toward 1: 0.881 → 0.921 → 0.942 at
X = 4·10⁴, 1.6·10⁵, 3.2·10⁵ (registered PASS at 3.2·10⁵). The prime-level cubic statement for a
fixed twist appears accessible to the Dunn–Radziwiłł method under GRH, which already carries a
twist r in its Type I proposition (Prop. 8.1). This is to be verified as a separate,
known-method-implied statement. It is the calibration, not the target.

**Sextic T1 (the target).** The same architecture predicts θ_u² ∝ |τ₆-type coefficient|²·N(u)^{−1/6}.

- The data show that the relevant mean-square coefficient is **independent of u**, including at
  squares. This was registered PASS at X = 10⁶, with ratio 0.943 ± 0.022.
- So the main term behaves as if the sextic coefficients (on average over the rows πu) had
  constant modulus on the ±1 class mod 3, and vanished, or were depleted, on the ω-rotated
  classes.
- What is needed for a proof:
  1. the residue of the twisted sextic Kubota series and its size as a function of u, which is
     the sextic analogue of Patterson's Thm 8.1 on average;
  2. the local factor at 2 that explains why the matrix normalization (ρ̄/ρ)₆ moves the main
     term (RS-9).
- Status: **open**. The literature (Bröker–Hoffstein; Chinta–Friedberg–Hoffstein) gives τ₆(π)²
  at primes, partly conjectured, but not mean squares at πu.

**Step 3 (T2, the crux): not started.** Next, measure the actual size of the bilinear sextic sums
that a Heath-Brown decomposition needs. Compare with the sextic large-sieve exponents, extracted
exactly from the literature, and state the gap to o(X^{2/3}/log X).

## 7. RS-S013: exact kernel, measured norms, and the actual obstruction

Stages: **mechanism, certification, exploratory measurement, falsification**.
Executed locally on Windows. Entry authority was main/origin/main `68d19bd`;
the handoff's claim that RS-S012 was unmerged was stale. Session branch:
`codex/rs-s013-type-ii`; no merge is authorized by this session.

### Exact building blocks

For squarefree coprime m,n prime to 6, define the trace-form normalized Gauss
sum G_c(m)=g6(c,m)/sqrt(Nm). The Chinese remainder theorem gives

```text
G_c(mn) = (m/n)_6 (n/m)_6 G_c(m)G_c(n).
```

Indeed, representing a residue modulo mn by nx+my factors its additive
character as e(Tr(cx/m))e(Tr(cy/n)), and its multiplicative character as
(n/m)_6(m/n)_6(x/m)_6(y/n)_6. Multiplying the two finite sums proves the
identity. If c shares a prime factor, the corresponding primitive local sum
is zero. Noncoprime m,n are excluded rather than assigned an asserted
nonsquarefree Gauss value.

The reciprocal-symbol factor Q is cubic with a local sign:

```text
Q(m,n) = epsilon(m,n) (m/n)_3,
epsilon = (-1)^(k*l' + l*k' + l*l'),
m mod4 = omega^i (-1)^k (1+2omega)^l.
```

The exact transport from E-primary reciprocity to our prime-product generators
is derived in `RS_S013_LITERATURE.md` section 2. `bilinear.py` implements it
with integer exponent arithmetic. Independent CRT residue summation checks
the Gauss factorization on split, conjugate, inert and mixed composites;
independent Euler exponentiation checks the cubic reduction. These finite
checks certify implementations of the algebraic derivations, not asymptotic
claims.

For fixed c coprime to the supports, G_c has modulus one. Its row and column
factors therefore leave every singular value unchanged. Operator norms discard
the special Gauss phases that the arithmetic-coefficient problem needs.

### Literature and precise exponent gap

`RS_S013_LITERATURE.md` records source URLs, theorem numbers, coefficient
hypotheses and domains. Heath-Brown's cubic sieve and BGL's higher-order sieve
give, after the finite local class partition,

```text
|B| << (MN)^epsilon ||alpha||_2 ||beta||_2
       sqrt(M + N + (MN)^(2/3)).
```

For divisor-bounded dense coefficients and MN=X, the exponent is
`1/2 + max(a,1-a,2/3)/2`, where M=X^a. It is 5/6 throughout
1/3 <= a <= 2/3 and worse outside. The gap to X^(2/3)/log X is a power
X^(1/6), plus logarithms and epsilon losses. GL's stronger quadratic bound
does not apply to this cubic product kernel.

Dunn–Radziwill Proposition 10.1 treats a **corrected cubic main term**, with
special coefficient cancellation conditions supplied by GRH in their
application; its dense broad range is X^(1/3+xi) <= B <= X^(1/2-xi).
It is not an assertion that every Type II block is negligible. Neither this
theorem nor ordinary Hecke GRH as used there supplies the missing
sextic-weighted residual estimate. No complete sextic prime decomposition or
its total logarithmic error budget has been proved here.

### Local measurements and their scope

The pre-run specification is `RS_S013_EXPERIMENT.md`; the implementation/design
checkpoint is `b6556f7`. `results/type_ii_2026-10-26.json` contains all eight
supports, exact exponent hashes, coefficients, matched controls and provenance.
Supports include **every squarefree ideal prime to 6**, not only prime pairs.
Here M,N are lower dyadic endpoints and X=4MN is the product upper bound.

| M,N | matrix dimensions | norm | matched control norms (seeds 0,1,2) | L2 extremal form / (X^(2/3)/log X) |
|---|---|---:|---|---:|
| 32,32 | 7 x 7 | 3.9004 | 4.1623, 3.9004, 4.5955 | 0.8871 |
| 64,64 | 19 x 19 | 8.3772 | 7.3973, 8.3788, 9.0731 | 2.3944 |
| 128,128 | 37 x 37 | 11.1526 | 12.5518, 11.4453, 10.7449 | 2.8154 |
| 256,256 | 74 x 74 | 16.5505 | 17.5758, 16.3257, 16.8774 | 3.7306 |
| 512,512 | 139 x 139 | 22.4568 | 23.4257, 22.5973, 23.2687 | 4.1926 |
| 32,256 | 7 x 74 | 10.6273 | 9.7281, 11.0156, 9.9449 | 2.4559 |
| 64,512 | 19 x 139 | 14.9406 | 14.6732, 15.0751, 15.9426 | 3.5063 |
| 32,1024 | 7 x 294 | 18.8082 | 18.5240, 18.4830, 18.4301 | 3.8965 |

At (512,512), the extremal L2 form is 3121.50 versus target 744.52; even its
unimodular phase projection gives 2562.47. Eight random unimodular coefficient
pairs have maximum 189.34. The coefficients make a decisive difference.
The finite sieve-shape ratios are recorded without interpreting an unspecified
theorem constant as one. These are exploratory examples, not an asymptotic
exponent fit, a new spectral conjecture, or a prime-weight estimate.

### What can and cannot close

**Unconditional obstruction to the proposed unrestricted route.** The Frobenius
norm implies sigma_max >= sqrt(number of nonzero entries / min(R,S)).
Even arbitrary pointwise-bounded coefficients admit a balanced prime-band
bilinear value of order X^(3/4)/(log X)^(3/2): random column phases followed
by row alignment prove this via second/fourth moments. The derivation is in
`RS_S013_CANDIDATE_AUDIT.md`. Thus an all-coefficient o(X^(2/3)/log X) theorem
is impossible. More operator-norm measurements cannot remove that obstruction.

**Unresolved arithmetic route.** One must specify the actual prime-decomposition
coefficients, identify any Type II main term/correction, and bound the residual
below the required total error. H2 additionally needs a frequency average for
c=pi*u and a negative off-diagonal mechanism for nonprimary u. T1 residues and
local factors remain unresolved. Conditional statements must explicitly assume
the missing sextic coefficient estimate as well as any Hecke hypothesis; this
session proves no such estimate. Viability is not established.

**Disposition.** This exhausts the generic large-sieve/operator-norm approach
proposed for this unit, not every hard-route method. It does not authorize an
automatic all-n or function-field fallback under PROTOCOL section 9.

### Candidate correction encountered during the audit

The frozen CAND-001 conjunction is **REFUTED**: u=64=2^6 has w_64=w_1 exactly,
but its statement 3 predicts excess ratio N(64)^(-1/6)=1/4. Statements 1 and
2 are not refuted. The norm-100 finite test remains PASS after independently
restoring the two omitted sextic rows u=+/-8 (80 rows, mean 0.9426271,
population SD 0.0214900). Old evidence and original statements are preserved;
the current scoring script now limits its cube special case to cubic mode.
See `RS_S013_CANDIDATE_AUDIT.md` and its JSON for the exact proof and rescore.

The immediate next bounded unit is an invariant formulation audit and explicit
repair decision for the strength statement; a sixth-power-free norm is only a
possible repair, not an established law. CAND-001 must not be silently revived
or renumbered. No theorem export or publication is justified by this session.


## 8. RS-S014 consequence for the targets

- H2, the matrix dichotomy, must be stated on **twist classes**: exponent vectors mod 6. It cannot
  be stated on "±primary u", because u⁵ is ±primary and its twist is the conjugate twist, which is
  not enhanced.
- Any dispersion target has to produce three behaviours:
  - a positive main term for exponents 1–3, with ε ∝ N₆^{−1/6};
  - a **negative** excess of size about N^{−5/6} for exponent 5;
  - the depletion of the non-primary associates.

  This reinforces the RS-S013 finding that a positive squared-main-term ansatz (R2) cannot be the
  whole story. A signed dispersion formula is required.
- The cubic analogue of the exponent-5 behaviour is Patterson's τ₃(π²) = 0, at exponent n − 1.
  Whether the sextic exponent-(n − 1) excess is a nonzero negative constant is a precise question
  for T1. See `RS_S014_INVARIANCE_AUDIT.md`.
