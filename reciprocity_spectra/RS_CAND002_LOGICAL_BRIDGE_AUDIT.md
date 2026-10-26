# CAND-002 mathematical implication audit (owner priority, 2026-10-26)

**Status:** proof obligation OPEN; formalisation paused pending mathematical resolution.
**Authority:** the exact CAND-002 statement remains frozen in `research/CONJECTURE_REGISTER.md`.
This note is a logical diagnosis and an **abstract countermodel to a claimed implication**,
not a counterexample to the particular sextic residue matrix and not a refutation of CAND-002.
No novelty or external-review claim is made.

## 1. The two noncommuting limiting regimes

Put `n = N_6(κ)` and `t = n/X`.

- **CAND-002(1)** controls `s_κ(X) - F(t)` uniformly only for
  `a <= t <= b` with each fixed `a > 0`. For fixed κ, n is fixed,
  so `t -> 0` as `X -> infinity`. The small-`t` positivity of
  `F(t)` does not establish positivity of `s_κ(X)` unless the
  approximation error is controlled **jointly at the boundary** `t -> 0`.
- **CAND-002(2)** controls `s_{π^5}(X)` when the norm of π is large
  *and* `N(π)^5/X >= T`. For fixed π and `X -> infinity`,
  this ratio tends to zero. The large-`t` bound gives no information
  about the fixed-prime limit.

In particular, the conditional fixed-class conclusions (3) do not follow
*from statements (1) and (2) alone*. Whether the separately assumed
analytic hypothesis H_P supplies enough to bridge this gap is a distinct,
unproved mathematical question, not resolved by stating H_P.

## 2. Rigorous abstract countermodel to (1)+(2) => (3)

The following scalar values satisfy **every asymptotic regime specified in
(1) and (2), including the normalization gap**, but violate both
fixed-class conclusions. They need not arise from a residue matrix; that
is precisely why they show that an additional structural/analytic
argument is necessary, without refuting CAND-002 itself.

Take `X >= 2`, let `F(t) = 1/(1+t)` for `t > 0`, and fix
`r_1(X) = sqrt(2)`. Thus the normalization gap
`r_1(X)^2 - 1 = 1` holds identically. Define
`s_κ(X) = (r_κ(X)^2 - 1) n^(1/6)` using `n = N_6(κ)`.

For every admissible **non-unit class without exponent five**, define

    r_κ(X) = 1                                    when n <= sqrt(X),
    r_κ(X) = sqrt(1 + n^(-1/6) F(n/X))            when n > sqrt(X).

For the unit class `κ=1`, retain `r_1(X)=sqrt(2)`, hence
`s_1(X)=1`. Its `t=1/X` eventually leaves every fixed compact
subinterval `[a,b]` of `(0,infinity)`.

For any fixed compact `[a,b]` with `a>0`, if
`t=n/X >= a` and `X > a^(-2)`, then
`n >= a X > sqrt(X)`. Consequently
`s_κ(X)=F(t)` **exactly** throughout that compact aspect range;
compact-uniform convergence holds with zero error. Also
`F(0+)=1`, `F` decreases on `[0.01,1]`, and `F(infinity)=0`.

But for each fixed non-unit κ, eventually `n <= sqrt(X)`,
so `r_κ(X)=1` identically, contradicting the proposed
`liminf_X r_κ(X)>1`.

For every admissible single-prime exponent-five class
`κ=π^5` with `n=N(π)^5>1`, define

    r_{π^5}(X) = sqrt(1 - n^(-1/6))    when n/X >= 1,
    r_{π^5}(X) = 6/5                   when n/X < 1.

For `n/X >= 1`, the normalized statistic is exactly
`s_{π^5}(X)=-1`: it satisfies (2) for every δ>0 by taking
`T=1`, `N0=2` and `X0=2`. But at every fixed π,
eventually `n/X<1`, so `r_{π^5}(X)=6/5`,
contradicting `limsup_X r_{π^5}(X)<=1`.

All displayed strengths are nonnegative reals. The example is not a
sextic-residue-matrix realization and does not model or satisfy the
separate arithmetic H_P; it establishes only the non-implication
of the two quantified asymptotic regimes plus the positive baseline.

## 3. What would actually suffice (but is NOT proved)

For fixed κ with no exponent five, the normalization gap gives
`r_1(X)^2 - 1 >= η > 0` for all large X. If an independently
proved *boundary-aspect estimate* gives
`liminf_{X->infinity} s_κ(X) >= c_κ > 0`,
then for `n=N_6(κ)>0`,

    r_κ(X)^2 - 1
       = (r_1(X)^2 - 1) * s_κ(X) / n^(1/6)
       >= η * c_κ / (2*n^(1/6))

eventually, whence
`liminf_X r_κ(X) >= sqrt(1 + η*c_κ/(2*n^(1/6))) > 1`.
For the unit class, the baseline gap alone already gives enhancement.

For fixed π, a sufficient (stronger) statement is
`s_{π^5}(X) <= 0` eventually, since the denominator is
eventually positive: then `r_{π^5}(X) <= 1`.
A weaker asymptotic condition on the positive part of the
*unnormalized excess* could also suffice, but cannot be replaced
by the large-t claim (2).

These are **requirements / conditional deductions**, not newly proved
claims for the actual matrix.

## 4. H_P and normalization obligations

The Lean `AbstractPrimeMomentHP` quantifies an unspecified
coefficient function `c(u)` in a **raw, unnormalised** shifted
Gauss first moment `shiftedFirstMoment`. The matrix orientation
identity uses sums of **normalised** Gauss values
`g(shift,σ)/sqrt(Nσ)`. Therefore a proof of an implication
from H_P to matrix-strength bounds needs, separately:

1. A rigorous passage from unnormalised to normalised prime sums,
   with uniform weighted error bounds, not an informal deletion
   of the `1/sqrt(Nσ)` factor.
2. The precise coefficient/sign/support or second-moment information
   that makes fixed non-five strengths stay above one, and fixed
   fifth strengths stay at or below one.
3. Uniformity in shifts of size `N(ρ κ)` as ρ ranges with X,
   and a treatment of the boundary `N_6(κ)/X -> 0`.
4. An explicit check of the quantifier order and whether `H_P`
   as currently stated actually contains these ingredients.

An unspecified complex `c(u)` is not automatically nonzero or
positive in the sense required by the norm inequalities.
No theorem supplying these missing ingredients is established here.

## 5. Decision and next task

**Owner decision:** mathematical proof first; pause all further Lean
sextic-bridge work and Palomar packaging. The previously verified Lean
lemmas remain valid and retained.

**RS-S026 is now MATHEMATICS-FIRST.** Its next-session prompt must
attempt the actual prime-level/matrix-level analytic implication
(hard version first, per PROTOCOL §9); prove it with precise estimates,
or give a rigorous counterargument and specify the minimum repair.
Neither frozen CAND-002 wording nor numerical results are to be silently
changed. The conjecture remains unproved, and its conditional
corollary is marked LOGICAL_BRIDGE_OPEN pending mathematical work.
