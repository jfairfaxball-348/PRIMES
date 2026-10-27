# RS-S028 — Prime projection, ideal Vaughan blocks and the residue-transfer obstruction

**Date:** 2026-10-27. **Stage:** mathematics-first, hard prime-level/matrix-level route. **Outcome:** exact prime projection, an ideal-theoretic Vaughan decomposition and a counterexample to *residue-only* prime transfer are proved on paper; **CAND-002(3) remains OPEN**. No sextic prime asymptotic, signed moment law or Kubota-to-prime coefficient identification is claimed. No Lean, Palomar, publication or discovery-scale computation.

## 0. Input and notation

Use the frozen definitions in \`research/CONJECTURE_REGISTER.md\` (CAND-002), RS-S026 (row and signed Gram identities), RS-S027 (mod-4 kernel and H_P upper tail), RS-S013 (composite trace-Gauss reciprocity) and RS-S019/020 (rational-to-trace conversion). All prime-indexed sums below are over *ideals*, not arbitrary associates of generators.

Let \(K=\mathbb Q(\omega)\), \(\mathcal O=\mathbb Z[\omega]\) and \(N\mathfrak a=|\mathcal O/\mathfrak a|\). For every nonzero integral ideal prime to \((3)\), write \(a_*\) for its unique generator congruent to \(-1\bmod3\). Uniqueness uses the six units, whose images are the six units of \(\mathcal O/(3)\). Thus \((\mathfrak a\mathfrak b)_*=-a_*b_*\). As before, \(\chi_a(u)=(u/a)_6\) is zero if \((u,a)\ne1\). For squarefree \(a\) prime to \((6)\), put
\[
 G^{\rm tr}_u(a)=\frac{1}{\sqrt{Na}}
 \sum_{z\bmod a}(z/a)_6\exp(2\pi i\operatorname{Tr}_{K/\mathbb Q}(uz/a)).
\]
The residue symbol belongs to the **ideal** \((a)\); the trace additive phase depends on the chosen generator. The composite trace sums and their CRT rule are those of RS-S013/019. Standard finite Gauss orthogonality gives \(|G^{\rm tr}_u(a)|=1\) for \((u,a)=1\) and zero otherwise on this squarefree support; the conductor of the additive character is understood as in RS-S019.

At a degree-one ideal \(\mathfrak p=(\sigma)\), \(\sigma=a+b\omega\), define the **rational/trace correction**
\[
 d(\mathfrak p)=\chi_\sigma(2a-b)=\chi_\sigma(\bar\sigma),\quad |d(\mathfrak p)|=1.
\]
RS-S019/020 give the *exact* prime identity, with zero cases,
\[
 \frac{g^{\rm rat}_\sigma(u)}{\sqrt{N\sigma}}
       =d(\mathfrak p)G^{\rm tr}_u(\sigma).                \tag{1}
\]
For degree-two inert primes set \(d(\mathfrak p)=1\). For a squarefree ideal coprime to 6, extend \(d\) by the finite product over **its prime-ideal factors**. This is an explicitly defined multiplicative function on coprime squarefree ideals, **not** an identified fixed-conductor Hecke character. The factor \(d(\mathfrak p)\), particularly its \(\bar\sigma\) dependence, must not be erased when replacing rational prime weights by trace weights.

Define the independent arithmetic weight (not a spectral statistic)
\[
 b_u(\mathfrak a)=
 \begin{cases}
  d(\mathfrak a)G^{\rm tr}_u(a_*),&
     \mathfrak a\ {\rm squarefree},\;(\mathfrak a,6)=1,\\
  0,&\text{otherwise}.
 \end{cases}                                           \tag{2}
\]
Then \(|b_u|\le1\). This is a **composite extension** of the required prime weights, not a proposed asymptotic model \(B_6(\rho\kappa;X)\); it is defined without referencing \(R_X\) or its measured row sums. The additional factor \(d\) means that a standard trace-only Kubota residue does not automatically describe the resulting series.

## 1. Proposition A — exact prime sieve, including inert and prime-power terms

Let \(\Lambda_K(\mathfrak a)=\log N\mathfrak p\) when \(\mathfrak a=\mathfrak p^j\), \(j\ge1\), and zero otherwise; \(\mu_K\) is the ideal Möbius function. For every \(X\ge7\) and nonzero shift \(u\),
\[
 \boxed{\;
 M_u(X):=\sum_{\sigma\in P_X}
       \frac{g^{\rm rat}_\sigma(u)}{\sqrt{N\sigma}}
 =\sum_{N\mathfrak a\le X}
      \frac{\Lambda_K(\mathfrak a)}{\log N\mathfrak a}
                   b_u(\mathfrak a)
  -\sum_{\substack{q\le\sqrt X\\q\equiv2\ (3),\ q>2}}
                   b_u((q)).\;}                       \tag{3}
\]
The \(\mathfrak a=1\) summand is defined to be zero. The second sum is \(O(\sqrt X)\), **uniformly in u**. The ramified prime above 3 and the inert prime above 2 are already removed by \((\mathfrak a,6)=1\); do not hide them inside a generic \(O(1)\) local factor when claiming an Euler product.

**Proof.** \(\Lambda_K(\mathfrak a)/\log N\mathfrak a\) vanishes off prime powers, and equals \(1/j\) at \(\mathfrak p^j\). For \(j\ge2\), \(b_u(\mathfrak p^j)=0\) by its **squarefree** support. Thus the rightmost unrestricted sum is exactly the sum over prime ideals away from 2 and 3, each once. In \(K\), these are the two degree-one prime ideals over each \(p\equiv1\bmod3\), represented by the two primary conjugate generators, plus the inert ideals \((q)\) of norm \(q^2\) for \(q\equiv2\bmod3\). The latter give the displayed subtraction. Equation (1) identifies both degree-one weights with those in \(M_u\). Finally each inert term has modulus at most one and there are at most \(\sqrt X\) such q. QED.

**Why this is not yet a prime theorem.** Equation (3) is an exact von-Mangoldt sieve of an explicitly chosen *composite* weight. It is not a justified equality between a **Kubota-series residue** and a **prime first-moment coefficient**. The rational/trace factor \(d\), squarefree restriction, the prime sieve, and the local 2/3 exclusions all affect that question. Formally one may write
\[
 \mathcal K^{\rm test}_u(s)=
   \sum_{\mathfrak a}b_u(\mathfrak a)(N\mathfrak a)^{-s},
 \qquad
 \mathcal P^{\rm test}_u(s)=
   \sum_{\mathfrak a}\frac{\Lambda_K(\mathfrak a)}
                     {\log N\mathfrak a}
                     b_u(\mathfrak a)(N\mathfrak a)^{-s},\quad \Re s>1,
                                                            \tag{4}
\]
but neither series is here identified with a specific metaplectic Kubota
series, nor is any continuation, functional equation or residue claimed
for \(\mathcal P^{\rm test}\). Their absolute convergence in \(\Re s>1\) follows from \(|b_u|\le1\) and the ideal-counting bound. In particular \(\mathcal P^{\rm test}\ne\mathcal K^{\rm test}\): a Dirichlet coefficient projector onto primes is **not** an operation that preserves a pole coefficient without a separate analytic theorem.

Define \(\Psi_u(X)=\sum_{N\mathfrak a\le X}\Lambda_K(\mathfrak a)b_u(\mathfrak a)\).
Because the squarefree support kills every prime power with \(j\ge2\), ordinary Stieltjes partial summation gives the **exact** further identity
\[
 M_u(X)=\frac{\Psi_u(X)}{\log X}
       +\int_2^X\frac{\Psi_u(t)}{t(\log t)^2}\,dt
       -E_u^{\rm inert}(X),\quad |E_u^{\rm inert}|\le\sqrt X .   \tag{5}
\]
No error term has been absorbed into a conjectural main term. For raw Gauss
weights one must instead insert \(\sqrt{N\mathfrak a}\) into (2); the
power scale of the raw H_P is **not** interchangeable with the normalised
prime scale in (3).

## 2. Proposition B — exact ideal Vaughan identity and the actual Type II range

For ideal arithmetic functions, write convolution \((f*g)(\mathfrak n)=
\sum_{\mathfrak d\mathfrak e=\mathfrak n}f(\mathfrak d)g(\mathfrak e)\);
\(1(\mathfrak n)=1\), \(L(\mathfrak n)=\log N\mathfrak n\), and
\(f_{\le U}(\mathfrak n)=1_{N\mathfrak n\le U}f(\mathfrak n)\).
The standard unique factorization of *ideals* gives
\(\mu_K*1=\varepsilon\), \(L=\Lambda_K*1\),
\(\Lambda_K=\mu_K*L\). It follows, with no analytic hypotheses, that
\[
 \boxed{\Lambda_K=
   \mu_{\le U}*L
  -\mu_{\le U}*\Lambda_{\le V}*1
  +\Lambda_{\le V}
  +\mu_{>U}*\Lambda_{>V}*1.}                         \tag{6}
\]
**Proof.** Split \(\mu=\mu_{\le U}+\mu_{>U}\) in \(\mu*L\);
substitute \(L=\Lambda*1\) in the second term, then split
\(\Lambda=\Lambda_{\le V}+\Lambda_{>V}\).
As \(\mu_{>U}*1=\varepsilon-\mu_{\le U}*1\), the
\(\Lambda_{\le V}\) term is exactly as displayed. This is a finite
convolution identity at each ideal; in particular there is no unproved
assumption about the distribution of prime ideals.

For any smooth compactly supported cutoff \(W\), and a dyadic shell \(Y\)
(\(W(N\mathfrak n/Y)\) supported on \(Y\le N\mathfrak n\le2Y\)),
the exact weighted sum
\(T_u(Y)=\sum_{\mathfrak n}\Lambda_K(\mathfrak n)b_u(\mathfrak n)
W(N\mathfrak n/Y)\) is \(I_1-I_2+I_0+II\), where

\[
\begin{aligned}
 I_1&=\sum_{N\mathfrak d\le U}\mu_K(\mathfrak d)
  \sum_{\mathfrak m} \log N\mathfrak m\,
       b_u(\mathfrak d\mathfrak m)W(N\mathfrak d\mathfrak m/Y),\\
 I_2&=\sum_{\substack{N\mathfrak d\le U\\N\mathfrak e\le V}}
  \mu_K(\mathfrak d)\Lambda_K(\mathfrak e)
  \sum_{\mathfrak h}b_u(\mathfrak d\mathfrak e\mathfrak h)
     W(N\mathfrak d\mathfrak e\mathfrak h/Y),\\
 I_0&=\sum_{N\mathfrak e\le V}
    \Lambda_K(\mathfrak e)b_u(\mathfrak e)W(N\mathfrak e/Y),\\
 II&=\sum_{\substack{N\mathfrak m>U\\N\mathfrak n>V}}
     \alpha_U(\mathfrak m)\Lambda_K(\mathfrak n)
     b_u(\mathfrak m\mathfrak n)W(N\mathfrak m\mathfrak n/Y),\\
 \alpha_U(\mathfrak m)&=
     \sum_{\substack{\mathfrak d\mid\mathfrak m\\N\mathfrak d>U}}
                        \mu_K(\mathfrak d).
\end{aligned}                                                    \tag{7}
\]
These coefficients are **fixed arithmetically by Möbius and von
Mangoldt** before any matrix product or test; they cannot be replaced
by arbitrary extremising \(\ell^2\) vectors. No claim is made that the
resulting bilinear sum is small.

For a top-scale shell \(X/2\le N\mathfrak m\mathfrak n\le X\), choose
\(U=V=X^{1/3+\delta}\), \(0<\delta<1/6\). Every **nonzero**
Type II summand obeys
\[
 X^{1/3+\delta}<N\mathfrak m,N\mathfrak n
                    \le X^{2/3-\delta}.              \tag{8}
\]
Both factor ideals must be coprime and squarefree if
\(b_u(\mathfrak m\mathfrak n)\ne0\); since
\(\Lambda_K(\mathfrak n)\ne0\), this forces \(\mathfrak n\)
to be a genuine prime ideal, **not a higher prime power**.
At other shells, using the same global U,V may make II empty or
shorten its factor ranges. I1/I2 and the short \(I_0\) term cannot be
discarded on the grounds that II is central.

The trace-Gauss CRT multiplication introduces its **real phase
correction**, not ordinary multiplicativity. On coprime squarefree
primary generators \(a,b\) away from 6, \(c_*=-ab\), and
\[
 G^{\rm tr}_u(c_*)=
 \chi_a(-1)\chi_b(-1)\,
 (a/b)_6(b/a)_6\,
 G^{\rm tr}_u(a)G^{\rm tr}_u(b).                       \tag{9}
\]
Indeed, \(g_u(-ab)=g_{-u}(ab)\), apply the exact CRT formula
\(g_{-u}(ab)=(a/b)_6(b/a)_6g_{-u}(a)g_{-u}(b)\),
then \(g_{-u}(a)=\chi_a(-1)g_u(a)\) and similarly for b.
The two signs \(\chi_a(-1),\chi_b(-1)\) are \(\pm1\).
Equation (9) is valid also when a local factor vanishes. Since \(d\)
was defined multiplicatively on squarefree coprime ideals, it follows that
\(b_u(\mathfrak m\mathfrak n)\) contains the **same signed cubic
kernel**, up to the explicitly shown extra \(-1\) factors.
The mod-4 reduction of \((a/b)_6(b/a)_6\) is recorded in RS-S013;
it requires **both** local 2-adic classes, not just a generic cubic
symbol. When ideals have common factors the weight is zero, rather
than a primitive Gauss sum of a nonsquarefree modulus.

**Logarithmic budget and the unproved estimate.** In the sum \(II\),
\(|\alpha_U(\mathfrak m)|\le d_K(\mathfrak m)\) and
\(|\Lambda_K(\mathfrak n)|\le\log X\), with O(log X) dyadic
splits. Even the generic cubic/sextic large sieve of RS-S013 has a
balanced arbitrary-coefficient envelope \(X^{5/6+\epsilon}\)
for **unit-sized normalized Gauss weights with divisor-sized
coefficients**, before such logarithmic losses. It neither delivers
the needed signed arithmetic main term nor controls the
row-varying \(u=\rho\kappa\). In particular, the raw H_P scale
\(X^{2/3}/\log X\), the *fixed-shift* normalized H_P scale
\(X^{1/6}/\log X\), and the *moving-row L2* requirement in RS-S027
are **three different targets**; no single unexplained power
saving proves them all.

For example, if a proposed independently derived row model
\(B_6(\rho\kappa;X)\) is eventually specified, to reach RS-S027's
\(\sum_\rho|M_{\rho\kappa}(X)-B_6(\rho\kappa;X)|^2
\ll D^2(\log X)^{-A}\), one sufficient **UNPROVED**
allocation across J=O(log X) dyadic block errors \(e_j(\rho)\) is
\[
 \sum_\rho |e_j(\rho)|^2
       \ll_{\kappa,A}D^2(\log X)^{-A-4}
 \quad\text{uniformly in }j;                            \tag{10}
\]
the triangle inequality in \(\ell^2(P_X)\) gives a total
\(\ll D^2(\log X)^{-A-2}\) after summing J blocks. The I/II
main terms must be assembled *with* the proper weights in (5).
Equation (10) is an error **budget**, not a proven estimate.

## 3. Proposition C — a pole residue does not determine the prime coefficient

**Rigorous counterexample to a proposed analytic inference; NOT a
counterexample to the actual sextic matrix or a Kubota theorem.**
For \(n\ge1\) put \(a_n=n^{-1/3}\), and for each **odd rational
prime** \(p\) modify two coefficients:
\[
 a'_p=a_p+p^{-1/3}=2p^{-1/3},\qquad
 a'_{p+1}=a_{p+1}-(p+1)^{-1/3}=0.                     \tag{11}
\]
All other \(a'_n=a_n\). Every \(p+1\) is a distinct even
composite, so this is unambiguous; \(a'_n\) remains nonnegative.

The two Dirichlet series
\[
 F(s)=\sum_{n\ge1}a_n n^{-s}=\zeta(s+1/3),\quad
 F'(s)=F(s)+H(s),
\quad H(s)=\sum_{\substack{p\ \mathrm{odd}\\p\ \mathrm{prime}}}
       \left(p^{-s-1/3}-(p+1)^{-s-1/3}\right)           \tag{12}
\]
have **the same pole and residue 1 at \(s=2/3\)**.
Indeed the mean value theorem, uniformly on compact subsets,
bounds each bracket by \(C_s p^{-\Re(s)-4/3}\), whose sum converges
locally uniformly for \(\Re(s)>-1/3\). Thus H is holomorphic
in a neighbourhood of \(2/3\), whereas F has a simple pole
of residue 1 there.

But the *prime-sieved* sums differ on the main scale:
\[
 \sum_{p\le X}a'_p-\sum_{p\le X}a_p
     =\sum_{3\le p\le X}p^{-1/3}
     \sim\frac{3}{2}\frac{X^{2/3}}{\log X},
                                                        \tag{13}
\]
using the classical rational prime number theorem and partial
summation. Consequently **even a meromorphic pole/residue plus
nonnegative coefficients does not fix a prime first-moment
constant**. Nearby composite coefficients can compensate while
preserving the pole. No direct inference of the prime coefficient
\(c(u)\) from a full-moduli theta/Kubota residue is valid without
a separate prime-sieve argument. This result does **not** rule out
a stronger, arithmetic-specific identity for the actual sextic
Gauss coefficients. It isolates the missing analytic transfer
rather than claiming that all hard routes are exhausted.

## 4. Fixed-class signs are separate and still open

The exact signed dispersion identity of RS-S026 is
\[
 r_\kappa^2=1-\frac1D+\frac{O_\kappa}{DD_\kappa}.
\]
For **fixed non-five** \(\kappa\), one needs a genuine positive
lower bound \(O_\kappa/(DD_\kappa)\ge a_\kappa+o(1)\)
(\(a_\kappa>0\)); for **fixed fifth** class \(\pi^5\), one needs
\(O_{\pi^5}/(DD_{\pi^5})\le o(1)\). Zeros where
\(\sigma\mid\kappa\) are removed via \(D_\kappa\);
\(D_\kappa=D-O_\kappa(1)\) for fixed \(\kappa\), but it must not
be replaced by D inside an **exact** finite identity.
The denominator \(r_1^2-1\) has only a positive lower bound in
the frozen conditional formulation, not an upper bound; its
appearance in \(s_\kappa\) does not remove the fifth-class
error budget.

The model built in (2) is an exact composite extension and
**does not** supply the row model or signed coefficients required
by either inequality. A zero local theta coefficient at \(\pi^5\)
would not by itself force a nonpositive *signed two-point energy*.
For any proposed model B whose energy is \(O(D^2)\), the elementary
inequality
\[
 |\|M\|_2^2-\|B\|_2^2|
 \le 2\|B\|_2\|M-B\|_2+\|M-B\|_2^2
\]
transfers a proved \(o(D^2)\) squared-error estimate to energy,
but **cannot give its sign**. Both sign conditions remain
distinct unproved arithmetic obligations.

## 5. Independent checks, limitations and next dependency

- The convolution derivation of (6) uses only ideal Möbius
  inversion and \(L=\Lambda_K*1\). Independent integer-monoid
  enumeration checked the same algebraic identity for
  \(n=2,\ldots,299\), \(U=11,V=13\) (all cases matched to
  floating error <1e-8). This checks the convolution signs, **not**
  the Eisenstein analytic problem.
- For (11), enumeration of the 167 odd primes below 1000
  confirms that all the compensators \(p+1\) are distinct
  composites; the proof is the elementary parity argument.
  Holomorphy follows from the displayed absolute difference
  estimate, not from this finite check.
- Literature used for context, **not as a purported sextic
  prime theorem**: Brubaker–Bump, *On Kubota's Dirichlet Series*
  (2006), https://citeseerx.ist.psu.edu/document?doi=f15ee63ef8a2a074ddc455da19e127e0c7563b1e ;
  Vaughan's convolution identity (see
  https://encyclopediaofmath.org/wiki/Vaughan_identity );
  exact cubic/sextic large-sieve domains are documented
  in RS-S013_LITERATURE.md. No new novelty claim.
- No Kubota series with the *required* rational correction and
  prime projector has been analytically continued; no Type II
  main term, uniform moving-shift error, bounded prefix or
  coefficient sign has been proved. No prime-moment coefficient
  was identified with a theta residue.
- No .lean, pins, workflows, comparator, registration, papers,
  frozen candidate, original evidence or paused D1 files changed.

**Checkpoint:** the missing step is now an **explicit prime sieve
with rational/trace local factors and an arithmetic-weighted
signed Type II estimate**, not just a generic appeal to a
Kubota residue. In RS-S029, determine whether the exact
factors in (7)–(9) admit a suitable **prime-ideal analytic
main term** at moving shifts \(u=\rho\kappa\) (including the
\(2\)- and \(3\)-local factors); otherwise prove a narrower
obstruction. Do not graduate CAND-002, resume Lean or use
fallback routes merely because this subproblem is open.
