# RS-S013: exact candidate and finite-evidence audit

Date: 2026-10-26. Stages: **falsification / certification**. Executed locally.
Machine record: `results/rs_s013_candidate_audit_2026-10-26.json`.

## Frozen strength statement is incompatible with sixth-power invariance

The frozen CAND-001 package contains both the positive excess in statement 1 and
the strength law in statement 3 for **every** fixed coprime-to-3, ±primary u.
Take u = 64 = 2^6. Its omega coefficient is zero, it is coprime to 3, and
N(u) = 4096. Every prime rho in the index has odd norm p = 1 modulo 3, so rho
does not divide 2. Multiplicativity gives the exact identity

```text
(64/rho)_6 = (2/rho)_6^6 = 1,
w_64 = w_1,
r_64(X) = r_1(X).
```

Consequently, whenever r_1(X)^2 - 1 is nonzero,

```text
(r_64(X)^2 - 1)/(r_1(X)^2 - 1) = 1,
```

whereas statement 3 requires this ratio to tend to 4096^(-1/6) = 1/4.
Statement 1 ensures that the denominator is eventually bounded away from zero.
Even convergence to zero through nonzero values would leave the ratio equal to
one. The possible vacuity of a strength law with an identically zero excess is
therefore unavailable to the frozen package.

The corresponding rescaled strength statistic is exactly 4, instead of tending
to 1. This is an algebraic contradiction, independent of a numerical cutoff or
an extrapolated fit. Exact integer Euler exponentiation additionally confirms
the symbol equals one at all 160 indexed primes of norm at most 1000; this
finite check supports the implementation and is not the proof.

The smallest nonunit Eisenstein norm coprime to 3 is 4. Thus 64 is a
smallest-norm nontrivial integral sixth power coprime to 3, with norm 4^6. This
does not claim to identify the smallest counterexample to every possible
reformulation.

**Disposition:** the frozen three-statement CAND-001 package is **REFUTED**.
Statements 1 and 2 are not refuted by this audit. Preserve their evidence and
the original statement history. A replacement requires an explicit statement
with its own lifecycle treatment; replacing N(u) by a sixth-power-free norm
without further analysis would be an untested repair. In general, multiplication
by a sixth power preserves twist symbols only away from its prime divisors;
u = 64 avoids this qualification because the index contains no prime above 2.

## Recomputed registered finite test still passes

The prediction at commit `0971270` explicitly specifies all 80 eligible
±primary twists with 1 < N(u) <= 100, at X = 1,000,000. The frozen run stores
all their individual rows. Its summary has only 78 entries because
`scripts/phase1j.py` applies the cubic special case N_cf(±8) = 1 in sextic mode
as well, excluding those two rows from its ratio aggregate.

Recomputing the originally registered statistic from all 80 stored rows gives:

| Statistic | Frozen 78-row summary | Correct 80-row summary | Registered criterion |
|---|---:|---:|---|
| Mean | 0.9426628358681987 | 0.9426270885607334 | 0.90 <= mean <= 1.00 |
| Population standard deviation | 0.02176255398638871 | 0.0214899598426770 | sd <= 0.035 |

Each of the two omitted rows has ratio 0.9412329435695991. The other registered
conditions also pass: every stored ±primary r_u is greater than one, and every
tested other associate of norm at most 13 has r_u less than one. The corrected
finite verdict remains **PASS**. No new scale or fresh twist matrix was run;
the frozen source JSON is unchanged. The historical script remains available
at its recorded commit; RS-S013 fixes the current script so that the cubic
special case applies only in cubic mode.

To reproduce, select `pm_primary` rows with `1 < norm <= 100` from the sextic
run in `results/phase1j_2026-10-25.json`; calculate
`(r*r - 1) * norm**(1/6) / (r_u1*r_u1 - 1)` for each row, then take their mean
and population standard deviation. Source SHA-256 hashes, the original
registration, run commit, dimension, exact rational obstruction, and every
rechecked criterion are in the audit JSON.

The norm-4096 sixth-power obstruction lies outside this finite norm-100 family.
The finite PASS and the refutation of the universally quantified statement are
therefore distinct results.

## Consequence for an unrestricted Type II target

For an R-by-S matrix K with unit-modulus entries, write its largest singular
value as sigma. Frobenius norm and rank give

```text
sigma >= ||K||_F / sqrt(min(R,S)) = sqrt(max(R,S)).
sup_{||alpha||_2=sqrt(R), ||beta||_2=sqrt(S)} |alpha^* K beta|
    = sqrt(R*S) sigma
    >= sqrt(R*S*max(R,S)).
```

There is also a floor for arbitrary pointwise-bounded coefficients. Choose
independent uniform complex phases beta_j, set Z_i = sum_j K_ij beta_j, and
align alpha_i with Z_i. Then the resulting bilinear magnitude is sum_i |Z_i|.
Here E|Z_i|^2 = S and E|Z_i|^4 = 2S^2 - S. The elementary interpolation
inequality E|Z| >= (E|Z|^2)^(3/2)/(E|Z|^4)^(1/2) implies

```text
sup_{|alpha_i|,|beta_j|<=1} |sum_ij alpha_i K_ij beta_j|
    >= R sqrt(S/2),
```

and transposition supplies the analogous S sqrt(R/2) floor. Disjoint prime
bands have no shared-prime zero entries, so the argument applies directly.
In balanced bands with norm product X, prime counts of order
R,S ~ sqrt(X)/log X give a floor of order
X^(3/4)/(log X)^(3/2). This exceeds X^(2/3)/log X by an unbounded factor.
Thus a blanket uniform o(X^(2/3)/log X) estimate for arbitrary bounded
coefficients cannot be the required theorem. Specific coefficients arising
from a fully specified prime-sum decomposition may have additional structure;
this argument neither bounds their sums nor exhausts that route.

Measuring finitely many coefficient vectors gives examples and lower bounds,
not a uniform coefficient bound or an asymptotic exponent. Any numerical
operator estimate should be accompanied by this unavoidable floor.

Finally, cubic reciprocity gives an exact algebraic simplification for coprime
primary m,n. Set a = (m/n)_6 and b = (n/m)_6. Since a^2 = b^2, write
b = epsilon a, epsilon in {+1,-1}. Then

```text
(m/n)_6 (n/m)_6 = epsilon (m/n)_3,
epsilon = (m/n)_2 (n/m)_2.
```

The Type II kernel is consequently a cubic-symbol kernel multiplied by the
quadratic reciprocity sign. Extracting any usable analytic bound must retain
that sign and all indexing, coprimality, and coefficient restrictions.

## Scope of the proposed dispersion formula

Let D_u count indexed primes not dividing u. The exact diagonal term is
(D-1)D_u, and ||w_u||^2 = D_u. Thus

```text
r_u^2 = (D-1)/D + off_diagonal(u)/(D*D_u).
```

The simpler D(D-1) diagonal is exact only when u is coprime to every indexed
prime, as the existing reduction test already specifies. For fixed u,
D_u = D - O_u(1), so this distinction does not alter the limiting baseline.

The proposed R2 in `PROOF_ROUTE.md` adds a positive sum of squared main terms
to the diagonal, with error smaller than that positive sum. Such a formula
cannot establish the nonprimary half of H2, whose limiting ratio is bounded
strictly below one: that half requires a negative off-diagonal contribution
of order D*D_u. R2 must therefore be restricted to an appropriate positive
class or replaced with a signed dispersion statement. This is a defect in
the proposed reduction target, not a refutation of the dichotomy itself.
