# RS-S004: structural null certification

This certifies a stated conditional null ensemble. It is not a claim that every arithmetic
correlation has been removed, a universality theorem, or an explanation of the spectral spikes.
The classical primary-prime reciprocity conventions are those already used by `arith.py` and
its exact tests (Ireland–Rosen, chapter 9; Dummit–Dummit–Kisilevsky, listed in `PRIOR_ART.md`).
The finite conjugation, boundary and unit calculations below follow directly from the character
definitions. They are independent of the owner's exploratory control implementation.

## Conjugation and closure of the index set

Write omega for the Eisenstein root and zeta6 = 1 + omega. Conjugation sends
(a,b) to (a-b,-b) in the Eisenstein basis, and to (a,-b) in the Gaussian basis.
Both maps preserve the specified primary condition and norm, are involutions, and have no fixed
indices among the odd degree-one split primes. For rational quadratic indices the map is identity.

If r is the image of omega or i at rho, the image at conjugate(rho) is r^(-1).
Consequently the reduction of conjugate(alpha) at conjugate(rho) equals the reduction of alpha
at rho, while the chosen root of unity is inverted. Euler exponentiation therefore gives

    e_n(conjugate(alpha), conjugate(rho)) = -e_n(alpha,rho) mod n.

For sextic characters, (1+r)(1+r^(-1)) = 1, so the same argument applies to zeta6.
In matrix form C[bar(i),bar(j)] = conjugate(C[i,j]); there is no renormalizing unit because
conjugation already preserves the primary generators.

Reciprocity gives e[j,i] = e[i,j] + t[i,j] mod n. Here t is zero for cubic, half a turn
for the familiar quadratic/quartic parity cases, and for sextic it is half a turn precisely
when the product of the two field-quadratic symbols is negative. The sextic assertion follows
because the square of the reversal quotient is one by cubic reciprocity, while its cube is
that quadratic product. These shifts are symmetric and invariant under simultaneous conjugation.

## Conjugate-pair entries from one-prime data

These entries are computed from metadata, never copied from the arithmetic matrix.

* Cubic: reciprocity and conjugation make v = C[i,bar(i)] real; its nonzero cubic-root value is 1.
* Gaussian quartic: reducing a+b*i at the conjugate prime gives 2a. If u=a/b mod p is the image
  of i at the conjugate prime, solve (2a)^((p-1)/4)=u^k for k. This also obeys 2k=t mod 4.
  Reciprocity/conjugation alone allow two phases; the one-prime trace calculation fixes which.
* Sextic: reducing a+b*omega at the conjugate prime gives 2a-b. The square of the entry is
  the cubic conjugate-pair value 1, so the entry is the quadratic character of 2a-b in F_p.
  Its exponent is zero or three. Its reversal shift is zero.
* Rational quadratic: conjugate pairs are diagonal, already fixed to zero.

The conjugate-prime root and trace formulas also provide direct Euler checks of these rules.

## Galois and unit audit

The root fields for orders 3, 4 and 6 are quadratic; their nontrivial field automorphism is the
conjugation just treated. The ring-unit generator maps (a,b) to (a-b,a) in the Eisenstein ring
and to (-b,a) in the Gaussian ring. Among all unit multiples of a chosen primary generator,
only the original generator satisfies the selected primary condition. Thus unit multiplication
does not give another permutation of this index set. Multiplicativity still prescribes the
character of a unit times a numerator: the exponent increments are t*(p-1)/6 modulo 3 or 6
for Eisenstein characters, and t*(p-1)/4 modulo 4 for Gaussian characters. Exact tests check
these identities against direct Euler characters.

Characters of products or rational norms introduce character evaluations outside the chosen
prime index set. Conditioning on their numerical two-prime values would import additional
arithmetic data and can eliminate the randomness being used as a benchmark. This ensemble
conditions on the stated closed index symmetries, reciprocity shifts and one-prime boundary
values; it does not claim to preserve all such external arithmetic correlations.

## Exact orbit sampler and its measure

For a generic ordered pair the commuting index actions transpose and simultaneous conjugation
produce at most four positions. A leader exponent k propagates to

    k, k+t, -k, -k+t mod n

at (i,j), (j,i), (bar(i),bar(j)), (bar(j),bar(i)). All duplicate-position constraints must agree.
The diagonal is zero; conjugate-pair leaders use the metadata-derived phase above. On every
remaining orbit draw uniformly from the phases consistent with its stabilizer, independently
in the mathematical null measure. This is uniform on all matrices satisfying these specified
constraints. The native sampler uses unbiased rejection sampling with SplitMix64 counters keyed
by seed and the smallest row-major orbit position, and four OpenMP threads. A pure-Python BFS
reference propagates the generators instead of using the native four-position formula.

For rational quadratic matrices conjugation adds no constraint, and this sampler is
byte-identical to the old seed-matched control. Thus the quadratic null law is unchanged.

RS-S003's reciprocity-only comparisons remain FAIL. Fresh qualified-model comparisons use
separate RS-S004 prediction IDs. The owner's diagnostic used a different bulk window and RNG;
its rounded values are exploratory input, not this session's validation targets or status drivers.
