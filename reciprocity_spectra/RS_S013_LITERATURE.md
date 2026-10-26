# RS-S013: Type II literature extraction

Stage: **collision-audit / mechanism**. Local session, 2026-10-26.
This is an input audit, not a sextic prime theorem or a novelty claim.
Page numbers below refer to the linked arXiv/preprint PDFs, not journal pagination.

## 1. Large-sieve statements and domains

Write `Nm` for the absolute norm. All implied constants may depend on the fixed
number field, bad-prime set/conductor, and epsilon. Neither theorem below supplies
an explicit numerical constant for comparison against a finite matrix norm.

**Heath-Brown, Theorem 2, preprint pp. 3–4.** For arbitrary complex coefficients,

```text
sum*_{Nm<=M} |sum*_{Nn<=N} a_n (n/m)_3|^2
  <<_eps (MN)^eps [M+N+(MN)^(2/3)] sum* |a_n|^2.
```

Both stars mean squarefree elements of Z[omega] congruent to 1 modulo 3. The
statement is unconditional. Source: [author-uploaded preprint, Kummer's
conjecture for cubic Gauss sums](https://www.researchgate.net/publication/254847691_Kummer%27s_conjecture_for_cubic_Gauss_sums)
(Israel J. Math. 120 (2000), 97–124, DOI 10.1007/s11856-000-1273-y).

**Blomer–Goldmakher–Louvel, Theorem 1.3, p. 4.** For their n-th order Hecke family
over a number field containing the n-th roots of unity, n>=3, M,N>=1/2,

```text
sum*_{Na<=M} |sum*_{Nb<=N} lambda_b chi_a(b)|^2
  << (MN)^eps [M+N+(MN)^(2/3)] sum* |lambda_b|^2.
```

The stars restrict BOTH ideal variables to squarefree ideals coprime to the
fixed bad-prime set S. Their family, including its finite ray-class choices, is
defined in section 2; Lemma 2.1 gives the conductor and reciprocity properties.
Taking n=6 and K=Q(omega) is admissible. A raw element convention must first be
matched to this ideal family; it is not legitimate to suppress bad-prime/unit
factors. Source: [BGL, arXiv:1112.1650v1](https://arxiv.org/pdf/1112.1650v1).

**Goldmakher–Louvel, Theorem 1.1 and Corollary 1.2, p. 2.** For a quadratic Hecke
family as in their Definition 1, the preceding squared norm is bounded by
`(MN)^eps(M+N) sum* |lambda_b|^2`. Both variables are squarefree ideals prime to
the fixed ideal c. Corollary 1.2 applies this to `chi_b^(n/2)` for even n. For
n=6 that is the quadratic character `chi_b^3`; it does **not** assert this bound
for `chi_b` or `chi_b^2`. Source: [GL,
arXiv:1112.1642v2](https://arxiv.org/pdf/1112.1642v2).

## 2. The reciprocal sextic product has cubic order

[Gao–Zhao, arXiv:2306.10726v3](https://arxiv.org/pdf/2306.10726v3), p. 4 and
p. 6, equation (2.10), supplies the following conventions and reciprocity law.
For n=a+b*omega prime to 6, E-primary means n congruent to +/-1 modulo 3 and:
`a+b=1 mod4` if b is even; `b=1 mod4` if a is even; `a=3 mod4` otherwise.
For coprime E-primary m,n prime to 6,

```text
(n/m)_6 = (m/n)_6 (-1)^[((Nn-1)/2)((Nm-1)/2)].
```

Since `(m/n)_6^2=(m/n)_3`, our algebraic deduction is

```text
Q(m,n) := (m/n)_6 (n/m)_6
        = epsilon(m,n) (m/n)_3,
epsilon(m,n) := (-1)^[((Nn-1)/2)((Nm-1)/2)].
```

Here is the transport to the repository's convention, derived from that law.
For elements congruent to +/-1 modulo 3, write their classes modulo 4 as

```text
m = omega^i (-1)^k lambda^l, lambda=1+2*omega,
n = omega^i'(-1)^k'lambda^l'.
```

The exponents k,l,k',l' lie in {0,1}; i,i' lie in {0,1,2}. Since
`lambda^2=-3=1 mod4`, cubing removes omega^i and preserves the other two
factors modulo 4. The E-primary cube criterion above becomes `k+l=0 mod2`.
Thus `m_E=(-1)^(k+l)m` and `n_E=(-1)^(k'+l')n` are E-primary. Norms give
`(Nm-1)/2=l mod2` and `(Nn-1)/2=l' mod2`. The residue-symbol definition,
extended multiplicatively, gives `(-1/m)_6=(-1)^l`, while `(-1/m)_3=1`.
Denominator symbols depend on the ideal, so replacing its generator by its
negative does not change them. It follows that

```text
Q(m_E,n_E)=(-1)^[(k+l)l'+(k'+l')l] Q(m,n),
Q(m_E,n_E)=(-1)^(ll') (m/n)_3,
Q(m,n)=(-1)^(k*l'+l*k'+l*l') (m/n)_3.
```

This proves the finite-local-block formula for coprime m,n prime to 6 and
congruent to +/-1 modulo 3, including the repository's factor products. Passing
from -1 to +1 modulo 3 also leaves cubic symbols unchanged. Therefore each
fixed pair of modulo-4 classes gives a constant-sign cubic block to which the
Heath-Brown theorem applies. The large-sieve exponent does not improve merely
because the original Gauss sum is sextic.

## 3. What Dunn–Radziwill actually assume and achieve

Source: [Dunn–Radziwill, arXiv:2109.07463v3](https://arxiv.org/pdf/2109.07463v3),
Definition 3.1 (p. 11), Proposition 10.1/Remark 10.1 (p. 61), section 1.5
(pp. 8–10), Theorem 1.4 (p. 7).

`C_eta(B,w)` requires bounded coefficients on squarefree w-rough primary b,
`Nb~B`, and, for every epsilon,t,ell,k,u with k,u primary,

```text
sum_{u|b} beta_b (b/|b|)^ell (Nb)^(it) (k/b)_3
 <<_eps (1+|ell|)^eps (Nk)^eps (1+|t|)^eps
          (B/Nu)^(1/2+eta+eps),
```

when ell!=0 or k is not a cube. GRH supplies this property for their
prime-generated coefficients.

Proposition 10.1, specialized to pi=1: let X=AB, A,B>=10, 0<eta<=1/4,
0<eps<1/10000, w>(log X)^10, beta in C_eta(B,w), alpha supported on squarefree
primary a with Na in [A/10,10A], and W smooth supported in [1,2]. Then

```text
sum alpha_a beta_b g3~(ab) W(N(ab)/X)
 = kappa sum alpha_a beta_b mu^2(ab) N(ab)^(-1/6) W(N(ab)/X)
   + O_eps(||alpha||_2 E),
kappa=(2*pi)^(2/3)/(3*Gamma(2/3)),
E=A^(1/3)B^(5/6)[w^(-9/20)+X^(-rho/2)]
  + A^(1/12+eps/2)B^(5/6)
  + X^(eps/2)[B^(29/24)A^(-1/24)+B^(1+eta)
              +X^(1/2)(1+(B^2/A)^(-500))],
rho=rho(eps) in (0,1/10000).
```

Its dense-coefficient range is `X^(1/3+xi)<=B<=X^(1/2-xi)`. Narrow
balanced/Type III ranges use Proposition 7.1 and logarithmic savings. Theorem
1.4 conditionally proves cubic large-sieve sharpness. None is a generic
sextic-weight cancellation theorem.

## 4. Consequences for the proposed sextic target (our deductions)

For a squarefree coprime family away from the bad primes, absorb the normalized
Gauss factors and fixed twists into the coefficients. Their moduli are one on
the primitive support. After the finite local class decomposition above,
Cauchy–Schwarz and the cubic large sieve give

```text
|B(alpha,beta)|
 << (MN)^eps ||alpha||_2 ||beta||_2
            [M+N+(MN)^(2/3)]^(1/2).
```

This step is a bound for arbitrary coefficients, not a claim that the
coefficients supplied by a prime decomposition are worst cases. For divisor
bounded dense coefficients, `||alpha||_2 ||beta||_2 <= X^(1/2+eps)` with MN=X.
Putting M=X^a and N=X^(1-a) gives the exponent

```text
e(a)=1/2 + (1/2) max(a,1-a,2/3).
```

For `1/3<=a<=2/3`, this is 5/6, exceeding 2/3 by 1/6. Outside that interval,
the exponent is larger. Thus the generic inequality never attains the required
sextic target in any factorization range. Relative to the unweighted prime
target `X^(2/3)/log X`, the central-range envelope has gap
`X^(1/6+eps) log X`. Heath-Brown/Vaughan logarithmic coefficients and the number
of dyadic blocks require additional log savings, or a fixed power saving, when
reassembling the prime sum. The exact log budget depends on the decomposition
and has not been frozen here.

Even the hypothetical removal of the `(MN)^(2/3)` term would give only
`X^(3/4+eps)` at M=N=sqrt(X), still larger than X^(2/3). This matters when
interpreting numerical operator norms: demonstrating square-root sized random
matrix norms cannot prove the desired prime-weighted cancellation by a uniform
operator estimate.

The obstruction is stronger at the operator level. For an R-by-S matrix whose
coprime entries have modulus one,

```text
sigma_max >= ||K||_F/sqrt(min(R,S)).
```

For positive-density squarefree norm shells, R~M, S~N and a positive proportion
of entries are coprime, hence `sigma_max` is at least a constant multiple of
`sqrt(max(M,N))`. An all-coefficient sufficient condition
`sigma_max=o(X^(1/6)/log X)` is already incompatible with this lower bound in
balanced dense families. Prime-only shells change logarithms, not these powers.
This rejects the unrestricted operator-norm route; it does not refute the
special arithmetic prime coefficients.

Dunn–Radziwill's broad estimate contains a nonzero main term. It cannot be
transplanted as an assertion that all Type II sums are small. To adapt it here,
one must identify a sextic correction/main term and prove residual cancellation
for the actual decomposition coefficients, possibly after comparison with the
cubic Gauss phase. GRH for ordinary Hecke L-functions alone does not, from the
statements audited here, supply that additional sextic-weighted estimate.
Furthermore, H2 needs a frequency-averaged result for c=pi*u, not merely a
fixed-c bound for H1.

**Checkpoint.** The available generic large sieves and this operator-norm route
are insufficient. A route using the actual arithmetic coefficients, an explicit
dispersion correction, and separately proved twist-uniform estimates remains a
possible research dependency. This audit neither proves that route viable nor
exhausts every hard-route method. Numerical kernel measurements can document the
finite-size norm gap, but cannot close this analytic gap or change CAND-001's
proof status.
