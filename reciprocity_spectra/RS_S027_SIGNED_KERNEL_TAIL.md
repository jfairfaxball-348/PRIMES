# RS-S027 — Reciprocity transfer, conductor and uniform-tail checkpoint

> **Erratum (2026-10-27).** The H_P used here applied the X^(2/3)/log X scale to raw Gauss sums. The correct scale is normalised X^(2/3)/log X (raw X^(7/6)/log X). See `RS_HP_SCALE_ERRATUM.md` for which statements are unaffected and which rates change.

**Date:** 2026-10-27. **Stage:** mathematics-first hard prime/matrix route.
**Status:** a finite reciprocity transformation and a uniform upper-tail consequence
of abstract H_P are proved on paper. The fixed-class implication in frozen
CAND-002(3) is **NOT PROVED**. No Lean, registration, publication or new
numerical conjecture test took place.

## 1. Conventions and the exact reciprocal kernel

Write \(K=\mathbf Q(\omega)\), \(\omega^2+\omega+1=0\), \(\zeta_6=1+\omega\),
and \(P_X\) for the **two primary degree-one prime elements above each**
rational \(p\equiv1\bmod3\), with \(a\equiv2\bmod3\), \(b\equiv0\bmod3\).
Let \(\chi_\sigma(z)=(z/\sigma)_6\) and set it to zero at multiples of \(\sigma\).
For \(\sigma\ne\tau\) in \(P_X\), the existing Gram kernel is
\[
 K_X(\sigma,\tau)=\sum_{\rho\in P_X}
              \chi_\sigma(\rho)\overline{\chi_\tau(\rho)}.
\]
The diagonal contribution is treated separately in RS-S026; it is NOT included
in the following off-diagonal reciprocity proposition.

For a primary prime \(v=a+b\omega\) away from 2 and 3, write
\(v\equiv \omega^{i_v}(-1)^{k_v}(1+2\omega)^{l_v}\pmod4\)
with \(k_v,l_v\in\{0,1\}\). This is the exact finite-local coordinate system
derived in \`RS_S013_LITERATURE.md\`, §2. Put
\[
 \eta_{v}(\rho)=(-1)^{k_v l_\rho+
                              l_v k_\rho+l_v l_\rho},\qquad
 h_{\sigma,\tau}(\rho)=\eta_\sigma(\rho)\eta_\tau(\rho).
\]

**Proposition 1 (exact, including zeros).** For every distinct
\(\sigma,\tau\in P_X\),
\[
 \boxed{\ K_X(\sigma,\tau)=
 \sum_{\rho\in P_X}h_{\sigma,\tau}(\rho)
                     \left(\frac{\sigma\tau^5}{\rho}\right)_6.\ } \tag{1}
\]
In particular, if \(k_*=k_\sigma+k_\tau\bmod2\) and
\(l_*=l_\sigma+l_\tau\bmod2\), then
\[
 h_{\sigma,\tau}(\rho)
  =(-1)^{\,l_*k_\rho+(k_*+l_*)l_\rho}.                 \tag{2}
\]
It is a **quadratic local character of the primary generator mod 4**, not a
constant sign in general.

**Proof.** For coprime primary elements, transporting the standard
E-primary sextic reciprocity formula to the repository's \(-1\bmod3\)
convention (RS-S013, §2) gives
\((\rho/v)_6=\eta_v(\rho)(v/\rho)_6\). The sign is real and its square is one.
Therefore when \(\rho\notin\{\sigma,\tau\}\),
\[
  (\rho/\sigma)_6\overline{(\rho/\tau)_6}
  =\eta_\sigma(\rho)\eta_\tau(\rho)
   (\sigma/\rho)_6(\tau/\rho)_6^5
  =h_{\sigma,\tau}(\rho)(\sigma\tau^5/\rho)_6.
\]
At \(\rho=\sigma\) or \(\rho=\tau\), **both sides are zero** under the
extended-symbol convention, so the equality holds on the full index set.
Collecting mod-2 exponents proves (2). QED.

**Primitive-conductor lemma.** The element-character
\(f_{\sigma,\tau}(z)=\chi_\sigma(z)\overline{\chi_\tau(z)}\), considered on
\((\mathcal O_K/(\sigma\tau))^\times\), is nontrivial and primitive at **each**
of the distinct prime-ideal factors \((\sigma)\), \((\tau)\): each local
sextic residue character has order six on its residue field, and CRT
permits independent variation at the two primes. Hence the complete-unit
sum vanishes:
\[
 \sum_{z\in(\mathcal O_K/(\sigma\tau))^\times}
                  f_{\sigma,\tau}(z)=0.             \tag{3}
\]
This is finite orthogonality, **not** a cancellation bound over primes.

There is an exact ideal-character realization, with a unit-normalization
caveat worth making explicit. For every ideal \(\mathfrak a\) prime to 3,
let \(a_*\equiv-1\bmod3\) be its unique primary generator
(\(\mathbb Z[\omega]\) has class number one and units map bijectively to
\((\mathcal O_K/(3))^\times\)). Set
\(\lambda=f_{\sigma,\tau}(-1)\in\{\pm1\}\) and
\(\Phi_{\sigma,\tau}(\mathfrak a)=\lambda f_{\sigma,\tau}(a_*)\).
As \((\mathfrak a\mathfrak b)_*\!= -a_*b_*\), this is **multiplicative**:
\(\Phi(\mathfrak a\mathfrak b)=\Phi(\mathfrak a)\Phi(\mathfrak b)\).
It is a nonprincipal finite-order Hecke character with conductor
dividing \((3\sigma\tau)\) and with both \(\sigma,\tau\) present in its
conductor. The factor \(\lambda\) is necessary; simply declaring
\(f(a_*)\) multiplicative would be wrong when \(\lambda=-1\).

**Fixed-pair consequence (using a classical external theorem).** The Hecke
prime-ideal theorem for each **fixed nonprincipal character** gives
\(K_X(\sigma,\tau)=o_{\sigma,\tau}(X/\log X)=o_{\sigma,\tau}(D)\)
when \(\sigma,\tau\) are fixed and X grows. The inert degree-two prime
ideals with norm \(\le X\) contribute at most \(O(\sqrt X)\) and can be
removed. This corollary **invokes the classical Hecke prime-ideal theorem**;
we are not claiming a new proof of that analytic theorem. Its implicit
threshold depends on \(\sigma,\tau\). In the actual contraction the two
conductors move with X and can have norm on the order of \(X^2\).
Consequently no uniform, signed, averaged estimate follows from the
fixed-conductor theorem.

**Conductor-aspect obstruction.** Formula (1) involves numerator shift
\(u=\sigma\tau^5\), of norm \(N\sigma(N\tau)^5\), on the order of
\(X^6\) when both primes have norm comparable to X. The abstract H_P
only covers \(N(u)\le B y\) for each **fixed** B at prime-summation scale
\(y\le X\). Applying H_P to the transformed kernel therefore requires
\(B\gg X^5\), which its quantifiers do not permit. The \(\bmod4\)
quadratic factor \(h_{\sigma,\tau}(\rho)\) is also not automatically
accounted for by untwisted H_P.

## 2. The strongest uniform Abel consequence available on an upper slice

Use the **raw** H_P exactly as declared in
\`formalisation/ReciprocitySpectra/Conjecture.lean\` (read only).
Let \(A_u(y)=\sum_{N\sigma\le y}g_\sigma(u)\),
\(f(y)=y^{2/3}/\log y\), and
\(M_u(a,b)=\sum_{a<N\sigma\le b}g_\sigma(u)/\sqrt{N\sigma}\).
The coefficient \(c(u)\in\mathbb C\) is *unrestricted* in H_P.

**Proposition 2 (genuine uniform moving-shift tail).** Fix
\(0<\lambda<1\) and B>0. Uniformly over **all** nonzero shifts u with
\(N(u)\le B\lambda X\), H_P implies
\[
 M_u(\lambda X,X)=c(u)H_\lambda(X)
             +o_{B,\lambda}(X^{1/6}/\log X),       \tag{4}
\]
where the deterministic coefficient, with **no approximation**, is
\[
 H_\lambda(X)=
 {f(X)\over\sqrt X}-{f(\lambda X)\over\sqrt{\lambda X}}
 +{1\over2}\int_{\lambda X}^{X} f(y)y^{-3/2}\,dy .
                                                        \tag{5}
\]
For fixed \(\lambda\),
\(H_\lambda(X)\sim4(1-\lambda^{1/6})X^{1/6}/\log X\).

**Proof.** We first handle a small but essential quantifier detail:
Lean H_P is stated at **integer** cutoffs, whereas the following Abel
integral uses real y. For any y in [\(\lambda X,X\)], put \(n=\lfloor
y\rfloor\). For sufficiently large X, \(n\ge\lambda X/2\);
thus \(N(u)\le B\lambda X\le 2Bn\), and H_P applies at n
uniformly in u with the **fixed** constant \(2B\).
We must also justify replacing \(f(n)\) by \(f(y)\) despite the
possibly growing coefficient c(u). Apply H_P with error tolerance 1 at
one integer \(n\asymp X\) in the interval: from the trivial
\(|A_u(n)|\le\sum_{N\sigma\le n}\sqrt{N\sigma}
\ll n^{3/2}/\log n\), we obtain uniformly
\(|c(u)|\ll_{B,\lambda} X^{5/6}\).
Since \(f(y)-f(\lfloor y\rfloor)
=O_\lambda(X^{-1/3}/\log X)\), the coefficient rounding error is
\(O_{B,\lambda}(X^{1/2}/\log X)=o(X^{2/3}/\log X)\).
Thus the integer H_P yields, for every \(\epsilon>0\) and X large,
\(|A_u(y)-c(u)f(y)|\le(\epsilon+o(1))f(y)\) at **every**
real \(y\in[\lambda X,X]\), uniformly in eligible u.
Stieltjes/Abel summation gives the exact identity
\[
 M_u(\lambda X,X)
  ={A_u(X)\over\sqrt X}
  -{A_u(\lambda X)\over\sqrt{\lambda X}}
  +{1\over2}\int_{\lambda X}^{X} A_u(y)y^{-3/2}dy .
\]
The error has modulus at most
\(\epsilon[f(X)/\sqrt X+f(\lambda X)/\sqrt{\lambda X}
+\tfrac12\int_{\lambda X}^X f(y)y^{-3/2}dy]\),
which is \(O_\lambda(\epsilon X^{1/6}/\log X)\). Uniformity and arbitrary
\(\epsilon\) prove (4). Elementary substitution \(y=Xt\) yields the
asymptotic for (5). QED.

**Do not silently strengthen (4).** For moving u, one cannot uniformly
replace \(c(u)H_\lambda(X)\) by
\(4c(u)(1-\lambda^{1/6})X^{1/6}/\log X\) with an **additive**
little-o error without a uniform bound on the growth of \(c(u)\).
The exact H is deliberately retained. If u is fixed, c(u) is fixed;
letting the lower cutoff be fixed recovers RS-S026's coefficient 4.

For a fixed class \(\kappa\), a row shift \(u=\rho\kappa\) has
\(N(u)=N\rho\,N\kappa\le N\kappa X\); (4) applies on **every fixed
upper slice** \((\lambda X,X]\) by taking \(B\ge N\kappa/\lambda\).
But the missing prefix below \(\lambda X\) obeys only the unconditional
trivial bound
\[
 |M_{\rho\kappa}(0,\lambda X)|
 \le\#P_{\lambda X}\ll {\lambda X\over\log(\lambda X)}
 \quad (X\to\infty,\ \lambda>0\text{ fixed}),       \tag{6}
\]
since \(|g_\sigma(u)/\sqrt{N\sigma}|\le1\), including zero shifts.
Relative to the scale \(X^{1/6}/\log X\), (6) allows
\(O_\lambda(X^{5/6})\); it does **not** tend to zero. Each fixed
\(\lambda\) requires its own fixed B, and H_P does not give the
threshold control for \(B=B(X)\to\infty\). Equation (4) therefore does
not provide a uniform **full-row** first-moment asymptotic.

## 3. Signed contraction and the two different endpoints

By RS-S026's exact zero-diagonal Gram identity, with
\(q_\kappa(\sigma)=\overline{G_\sigma}\chi_\sigma(\kappa)\),
\[
 r_\kappa^2=1-\frac1D+\frac{O_\kappa}{D D_\kappa},\qquad
 O_\kappa=\sum_{\substack{\sigma,\tau\in U_\kappa\\\sigma\ne\tau}}
   q_\kappa(\sigma)\overline{q_\kappa(\tau)}
   \sum_{\rho\in P_X}h_{\sigma,\tau}(\rho)
                       (\sigma\tau^5/\rho)_6 .     \tag{7}
\]
The sum is real by the Hermitian partner \((\tau,\sigma)\).
Equation (7) is an exact arithmetic transformation, **not** a bound.

- **Fixed non-five \(\kappa\):** strict enhancement requires, for some
  \(a_\kappa>0\), \(O_\kappa/(D D_\kappa)\ge a_\kappa+o(1)\);
  the unit class follows separately from the already-assumed
  positive normalization gap. Neither the compact-aspect law (1) nor
  fixed-pair cancellation proves this.
- **Fixed \(\pi^5\):** mere nonenhancement is implied by
  \(O_{\pi^5}/(D D_{\pi^5})\le o(1)\); a *negative* constant limit would
  prove a stronger deficit. The large-aspect law (2) concerns
  \(N(\pi)^5/X\ge T\), not fixed \(\pi\) and X increasing.
  A vanishing sextic-theta coefficient at \(\pi^5\) would at most
  remove one candidate positive main term. It does **not** establish
  the sign of the complete off-diagonal expression (7).

The denominator \(r_1^2-1\) has only a **positive lower** bound in the
frozen statement; converting small normalized fifth-class \(s_\kappa\)
to an absolute error also needs upper control, as RS-S026 explains.
One must not infer either endpoint by interchanging nonuniform limits.

## 4. Concrete non-circular hard-route target (UNPROVED)

The following specifies an arithmetic programme rather than renaming
(7) as an assumption.

1. **Arithmetic model first, independently of R.** Define candidate
   coefficients \(C_6(u)\) from *explicitly identified* sextic
   Kubota-series residues, **including** the rational-versus-trace
   change and local factors at 2 and 3. Identify and justify the
   prime-modulus projection; the all-squarefree residue is **not**
   automatically the prime coefficient, and the abstract c(u) in H_P
   is not assumed equal to any theta coefficient.
2. **Uniform error at the actual shift aspect.** For each fixed
   admissible \(\kappa\), each \(A>2\), and every \(X\ge X_0(A,\kappa)\),
   target an independently derived model \(B_6(\rho\kappa;X)\), built
   exclusively from those explicit arithmetic coefficients and
   analytic weights, such that
   \[
     \sum_{\rho\in P_X}
       \left|\sum_{\sigma\in P_X}
            {g_\sigma(\rho\kappa)\over\sqrt{N\sigma}}
             -B_6(\rho\kappa;X)\right|^2
       \ll_{\kappa,A}D^2(\log X)^{-A}.              \tag{8}
   \]
   The range is \(0<N(\rho\kappa)\le N(\kappa)X\), including the
   initial portion of the prime-modulus sum, not merely
   \(N\sigma\ge\lambda X\). \(B_6\) must be specified **before**
   comparison and cannot be defined by the measured row sum.
   Equation (8) is a proposed **unproved** mean-square estimate,
   not a theorem; it does not itself settle the endpoint signs.
3. **Separate coefficient arithmetic.** Prove a signed local
   coefficient moment for this independent model:
   for a fixed no-five \(\kappa\),
   \(\sum_\rho|B_6(\rho\kappa;X)|^2
       \ge (1+a_\kappa)DD_\kappa+o(D^2)\),
   with \(a_\kappa>0\); for fixed \(\pi^5\), prove
   \(\sum_\rho|B_6(\rho\pi^5;X)|^2
       \le DD_{\pi^5}+o(D^2)\).
   With (8) and Cauchy–Schwarz, these imply the two endpoints
   **if** the model energies are \(O(D^2)\) where needed and the
   error is \(o(D^2)\). The two different signs are explicit
   separate obligations. These are unproved coefficient laws,
   not interchangeable with a vanishing \(\tau_6(\pi^5)\).
4. **Plausible proof architecture and Type II crux.** Start with a
   prime-modulus Vaughan/Heath-Brown decomposition, an exact
   rational-to-trace character transport (RS-S020), and the
   squarefree composite Gauss-factorization with its local
   reciprocal cubic kernel (RS-S013). For \(MN\asymp X\) and the
   hard bilinear range
   \(X^{1/3+\delta}\le M,N\le X^{2/3-\delta}\)
   (\(0<\delta<1/6\)), extract any **explicit arithmetic main
   term** rather than assuming all Type II contributions are
   negligible. The needed log-power saving is over the actual
   Möbius/von-Mangoldt-derived coefficients and row shifts
   \(N(\rho\kappa)\le N\kappa X\), **averaged in \(\rho\)**,
   not over arbitrary L2 coefficients. Record the Type I and
   short-endpoint blocks separately, including prime powers,
   inert ideals and the 2/3 and 2-adic local cases. The existing
   generic cubic/sextic sieve gives an \(X^{5/6+\epsilon}\)
   envelope on balanced arbitrary-coefficient blocks against the
   \(X^{2/3}/\log X\) prime-first-moment scale
   (RS-S013): a gap of \(X^{1/6}\), before logs. Such a
   sieve alone cannot prove (8) or either signed coefficient law.

This target is **non-circular in specification** only when
\(B_6\) and its coefficients are independently and explicitly
defined from analytic objects. At present they have **not** been
derived. It is therefore a dependency and a possible route,
not a claim of a viable, proven estimate or of progress beyond
the exact identities and uniform-tail lemma established above.
The generic all-coefficient route is already ruled out in
RS-S013; the arithmetic-coefficient hard route is not exhausted.

## 5. Validation and disposition

- Proof of (1): documented E-primary transfer, multiplicative
  symbols, explicit treatment of \(\rho=\sigma,\tau\).
- Independent, freshly written pure-Python modular check (not an
  asymptotic experiment): 32 primary split primes through norm 151,
  all 992 ordered unequal pairs and 31,744 ordered triples
  including zero cases. Direct Euler sixth-residue exponents
  agree with (1) and the mod-4 sign. These are algebra checks,
  not a proof of an analytic estimate.
- Proof of (4): exact complex Abel summation and the fixed-B
  quantifiers; the deterministic H retains the coefficient's
  possible u-dependence.
- External mathematical input distinguished: sextic reciprocity
  (as cited in RS-S013, Gao–Zhao arXiv:2306.10726v3, (2.10))
  and the *classical* Hecke prime-ideal theorem for a fixed
  nonprincipal character; no new proof of either theorem.
- No discovery-scale test, status change, or evidence JSON.
  CAND-002 (1)–(3), its frozen register, and H_P remain
  **conjectural/conditional** as before. No Lean/Palomar/paper
  or paused D1 material was changed.

**Natural checkpoint:** exact sign and conductor identified;
fixed-pair cancellation and a uniform moving-shift **upper
slice** established, but endpoint implication remains OPEN.
**Next dependency:** RS-S028 should make the proposed analytic
model \(B_6\) genuinely explicit (or rigorously falsify that
route) and audit the Type II/logarithmic obligations without
renaming the matrix conclusion as a hypothesis.
