# RS-S013 local Type II diagnostic

Stage: **EXPLORATORY**, specified before running the numerical diagnostic. This
does not register a prediction or change a conjecture status. The execution host
is the owner's local Windows workspace; no cloud job is requested.

Use every squarefree ideal of Z[omega] coprime to 6 in the norm intervals
`M < N(m) <= 2M`, `N < N(n) <= 2N`, with canonical prime-factor-product
generators. Include inert primes and both split conjugates. Set noncoprime
pairs to zero: this is a restricted Type II form, not a formula for a Gauss
sum at a nonsquarefree modulus. Fix frequency c=1.

Pairs (M,N): (32,32), (64,64), (128,128), (256,256), (512,512),
(32,256), (64,512), (32,1024). These small balanced and unbalanced supports
give directly checkable dense matrices. They are not a claimed complete
Heath-Brown decomposition. X in numerical comparisons is the product upper
bound 4MN; both lower endpoints are recorded.

Measure the operator norm of

`K(m,n) = (m/n)_6 (n/m)_6 g6~(1,m) g6~(1,n)`

and its reciprocal-symbol factor. The Gauss factors have modulus one, so
the two norms agree by unitary diagonal multiplication. Record that check,
the Frobenius/rank lower bound, and the comparison with
`sqrt(2M+2N+(4MN)^(2/3))`. The latter omits the theorem's unspecified constant
and epsilon factor and is **not** a numerical upper bound.

Coefficient diagnostics: eight independent random unimodular pairs (seed 23),
constant and ideal-Mobius coefficients, the exact L2 singular-vector extremizer
scaled to norms sqrt(row count) and sqrt(column count), and its componentwise
unimodular projection. Record maximum extremizer coefficients: L2 extremizers
need not satisfy a pointwise bound and are not the arithmetic weights of a
prime decomposition. No empirical fitted exponent will be promoted.

Each support has three matched random controls (seeds 0,1,2). The prime-matrix
`structured_random` implementation does not apply to composite reciprocal
products. Its counterpart here randomizes transpose/conjugation orbits among
the three sixth roots with the same exponent parity, retaining the coprimality
mask, quadratic reciprocity signs, and forced self-conjugate entries. The
null's Gauss phases are omitted because unitary diagonal multiplication
leaves its operator norm unchanged.

Save compact JSON after every support. It records the command, code commit,
source hashes, dimensions, X, seeds, versions, and floating-point limitations.
No matrices are committed. No fresh-scale conjecture test is performed.
