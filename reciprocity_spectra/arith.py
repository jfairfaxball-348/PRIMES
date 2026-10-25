"""Exact arithmetic core for power-residue matrices of degree-one primes.

Conventions
-----------
* ``n = 6``: the same Eisenstein indices as n=3, with coefficients still in the omega
  basis and ``prime.n == 3``. Use ``sextic_residue_exponent`` with ``zeta6 = 1 + omega``;
  the metadata ring and the character order are deliberately distinct.
* ``n = 2``: odd rational primes ``p``; the symbol is the Legendre symbol ``(p_i / p_j)``.
* ``n = 3``: primary primes ``pi = a + b*w`` of ``Z[w]``, ``w = exp(2 pi i / 3)``, with
  ``a = 2 (mod 3)``, ``b = 0 (mod 3)`` and norm ``p = a^2 - a*b + b^2 = 1 (mod 3)``
  (Ireland--Rosen, Ch. 9).  Each such ``p`` gives two primary primes ``pi`` and ``conj(pi)``.
* ``n = 4``: primary primes ``pi = a + b*i`` of ``Z[i]`` with ``b`` even, ``a + b = 1 (mod 4)``
  and norm ``p = a^2 + b^2 = 1 (mod 4)``.

For a degree-one prime ``pi`` of norm ``p`` the residue field is ``F_p`` and the root of unity
(``w`` or ``i``) maps to ``r = -a/b (mod p)``.  The power-residue symbol of ``alpha = c + d*zeta``
is ``zeta^k`` where ``(c + d*r)^((p-1)/n) = r^k (mod p)``; functions return the exponent ``k``
(``None`` when ``pi`` divides ``alpha``).  Gauss sums use the rational additive character:
``g(pi) = sum_{t=1}^{p-1} (t/pi)_n e(t/p)``.
"""
from __future__ import annotations

import cmath
import math
from dataclasses import dataclass


def primes_upto(limit: int) -> list[int]:
    """All primes ``<= limit`` (sieve of Eratosthenes)."""
    if limit < 2:
        return []
    sieve = bytearray([1]) * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for i in range(2, math.isqrt(limit) + 1):
        if sieve[i]:
            sieve[i * i :: i] = bytearray(len(sieve[i * i :: i]))
    return [i for i in range(limit + 1) if sieve[i]]


@dataclass(frozen=True)
class DegreeOnePrime:
    """A degree-one prime ``a + b*zeta`` of norm ``p`` in ``Z[zeta_n]`` (``n`` in {3, 4})."""

    n: int
    p: int
    a: int
    b: int

    @property
    def root(self) -> int:
        """Image of ``zeta_n`` (``w`` for n=3, ``i`` for n=4) in the residue field ``F_p``."""
        return (-self.a * pow(self.b % self.p, -1, self.p)) % self.p

    def complex_value(self) -> complex:
        zeta = cmath.exp(2j * math.pi / self.n)
        return self.a + self.b * zeta


def primary_eisenstein_primes(limit: int) -> list[DegreeOnePrime]:
    """Primary primes of ``Z[w]`` with norm ``p <= limit``, ``p = 1 (mod 3)``, sorted by norm."""
    out: list[DegreeOnePrime] = []
    for p in primes_upto(limit):
        if p % 3 != 1:
            continue
        found = set()
        bmax = math.isqrt(4 * p // 3) + 3
        for b in range(-(bmax // 3 + 1) * 3, bmax + 1, 3):
            disc = 4 * p - 3 * b * b
            if disc < 0:
                continue
            s = math.isqrt(disc)
            if s * s != disc:
                continue
            for root in (s, -s):
                if (b + root) % 2:
                    continue
                a = (b + root) // 2
                if a % 3 == 2 and a * a - a * b + b * b == p:
                    found.add((a, b))
        if len(found) != 2:
            raise ArithmeticError(f"expected two primary primes above {p}, found {sorted(found)}")
        out.extend(DegreeOnePrime(3, p, a, b) for a, b in sorted(found))
    return out


def primary_gaussian_primes(limit: int) -> list[DegreeOnePrime]:
    """Primary primes of ``Z[i]`` with norm ``p <= limit``, ``p = 1 (mod 4)``, sorted by norm."""
    out: list[DegreeOnePrime] = []
    for p in primes_upto(limit):
        if p % 4 != 1:
            continue
        found = set()
        for b in range(-math.isqrt(p), math.isqrt(p) + 1):
            if b % 2:
                continue
            a2 = p - b * b
            a0 = math.isqrt(a2)
            if a0 * a0 != a2:
                continue
            for a in (a0, -a0):
                if (a + b) % 4 == 1:
                    found.add((a, b))
        if len(found) != 2:
            raise ArithmeticError(f"expected two primary primes above {p}, found {sorted(found)}")
        out.extend(DegreeOnePrime(4, p, a, b) for a, b in sorted(found))
    return out


def legendre(a: int, p: int) -> int:
    """Legendre symbol ``(a/p)`` for an odd prime ``p``: returns 1, -1 or 0."""
    t = pow(a % p, (p - 1) // 2, p)
    return -1 if t == p - 1 else t


def residue_exponent(c: int, d: int, prime: DegreeOnePrime) -> int | None:
    """Exponent ``k`` with ``((c + d*zeta)/prime)_n = zeta^k``; ``None`` if ``prime`` divides it."""
    p, r, n = prime.p, prime.root, prime.n
    v = (c + d * r) % p
    if v == 0:
        return None
    t = pow(v, (p - 1) // n, p)
    power = 1
    for k in range(n):
        if t == power:
            return k
        power = power * r % p
    raise ArithmeticError("power-residue symbol is not an n-th root of unity")


def symbol_between(alpha: DegreeOnePrime, prime: DegreeOnePrime) -> int | None:
    """Exponent of ``(alpha / prime)_n`` for two degree-one primes of the same ring."""
    return residue_exponent(alpha.a, alpha.b, prime)


def gauss_sum(prime: DegreeOnePrime) -> complex:
    """``g(pi) = sum_{t=1}^{p-1} (t/pi)_n e(t/p)`` (Ireland--Rosen normalization)."""
    p, n = prime.p, prime.n
    zeta_n = cmath.exp(2j * math.pi / n)
    total = 0j
    for t in range(1, p):
        k = residue_exponent(t, 0, prime)
        total += zeta_n ** k * cmath.exp(2j * math.pi * t / p)
    return total


def jacobi_sum(prime: DegreeOnePrime) -> complex:
    """``J(chi, chi) = sum_t chi(t) chi(1 - t)`` for ``chi = (./pi)_n``."""
    p, n = prime.p, prime.n
    zeta_n = cmath.exp(2j * math.pi / n)
    total = 0j
    for t in range(2, p):
        k1 = residue_exponent(t, 0, prime)
        k2 = residue_exponent(1 - t, 0, prime)
        total += zeta_n ** (k1 + k2)
    return total


def residue_matrix(n: int, limit: int) -> tuple[list, list[list[int | None]]]:
    """Index set and exponent matrix ``E[i][j]`` with ``(x_i/x_j)_n = zeta_n^E[i][j]``.

    For ``n = 2`` the index set is the odd primes ``<= limit`` and the entry is 0 for ``+1``
    and 1 for ``-1``.  Intended for small ``limit`` (tests); use ``native/residue_matrix.c`` at scale.
    """
    if n == 6:
        index = primary_eisenstein_primes(limit)
        return index, [[sextic_residue_exponent(x.a, x.b, y) for y in index] for x in index]
    if n == 2:
        index: list = [q for q in primes_upto(limit) if q > 2]
        mat = [
            [None if i == j else (0 if legendre(qi, qj) == 1 else 1) for j, qj in enumerate(index)]
            for i, qi in enumerate(index)
        ]
        return index, mat
    if n == 3:
        index = primary_eisenstein_primes(limit)
    elif n == 4:
        index = primary_gaussian_primes(limit)
    else:
        raise ValueError("n must be 2, 3, 4 or 6")
    mat = [[symbol_between(x, y) for y in index] for x in index]
    return index, mat


def reciprocity_sign(n: int, x, y) -> int:
    """Sign ``s`` in the reciprocity law ``(y/x) = s (x/y)`` for the conventions above."""
    if n == 2:
        return -1 if (x % 4 == 3 and y % 4 == 3) else 1
    if n == 3:
        return 1
    if n == 6:
        return sextic_reciprocity_sign(x, y)
    if n == 4:
        return -1 if ((x.p - 1) // 4) * ((y.p - 1) // 4) % 2 else 1
    raise ValueError("n must be 2, 3, 4 or 6")



def conjugate_prime(prime: DegreeOnePrime) -> DegreeOnePrime:
    """Complex conjugate of a primary degree-one prime; it is again primary with the same norm.

    ``conj(a + b*w) = (a - b) - b*w`` (``w^2 = -1 - w``) and ``conj(a + b*i) = a - b*i``.
    Galois equivariance of the power-residue symbol gives
    ``(conj alpha / conj pi)_n = conj((alpha / pi)_n)``; for n = 6 the same holds because
    complex conjugation also sends ``zeta6 = 1 + w`` to ``zeta6^-1``.
    """
    if prime.n == 3:
        return DegreeOnePrime(3, prime.p, prime.a - prime.b, -prime.b)
    if prime.n == 4:
        return DegreeOnePrime(4, prime.p, prime.a, -prime.b)
    raise ValueError("conjugation is defined for Eisenstein and Gaussian primes")


def conjugate_pair_exponents(n: int, sign: int) -> set[int]:
    """Exponents allowed at ``(pi / conj pi)_n`` by reciprocity plus conjugation alone.

    Both identities give ``x = sign * conj(x)`` for that entry, so ``x`` lies on the line
    fixed by this reflection: ``{0}`` for n = 3, ``{0, n/2}`` for ``sign = 1`` and
    ``{n/4, 3n/4}`` for ``sign = -1`` (empty for n = 6, so the sign must be +1 there).
    """
    if sign == -1 and n % 2:
        return set()
    return {k for k in range(n) if (2 * k + (n // 2 if sign == -1 else 0)) % n == 0}


def sextic_residue_exponent(c: int, d: int, prime: DegreeOnePrime) -> int | None:
    """Sextic exponent for c+d*omega; zeta6=1+omega, on the cubic primary index set.

    Keep prime.n=3: (a,b) are coefficients in the omega basis, not zeta6.
    Direct Euler exponentiation independently determines the sixth root.
    """
    if prime.n != 3:
        raise ValueError("sextic characters require a primary Eisenstein prime")
    p, omega = prime.p, prime.root
    value = (c + d * omega) % p
    if not value:
        return None
    target = pow(value, (p - 1) // 6, p)
    zeta6, power = (1 + omega) % p, 1
    for k in range(6):
        if target == power:
            return k
        power = power * zeta6 % p
    raise ArithmeticError("sextic symbol is not a sixth root of unity")


def sextic_gauss_sum(prime: DegreeOnePrime) -> complex:
    """``g6(pi) = sum_{t=1}^{p-1} (t/pi)_6 e(t/p)`` with ``zeta6 = 1 + w`` (sextic convention)."""
    p = prime.p
    zeta6 = cmath.exp(1j * math.pi / 3)
    return sum(zeta6 ** sextic_residue_exponent(t, 0, prime) * cmath.exp(2j * math.pi * t / p)
               for t in range(1, p))


def sextic_jacobi_sum(prime: DegreeOnePrime) -> complex:
    """``J(chi6, chi6) = sum_t chi6(t) chi6(1 - t)``."""
    zeta6 = cmath.exp(1j * math.pi / 3)
    return sum(zeta6 ** (sextic_residue_exponent(t, 0, prime) + sextic_residue_exponent(1 - t, 0, prime))
               for t in range(2, prime.p))


def _mul_w(x, y):
    """(x0 + x1 w)(y0 + y1 w) with w^2 = -1 - w."""
    return (x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0] - x[1] * y[1])


def eisenstein_trace(x) -> int:
    """Tr(x0 + x1 w) = 2 x0 - x1."""
    return 2 * x[0] - x[1]


def inert_sextic_exponent(c: int, d: int, q: int) -> int | None:
    """Exponent k with ((c + d w)/q)_6 = zeta6^k for an inert rational prime q = 2 (mod 3), q > 2.

    The residue field is F_{q^2} = F_q[w]; the symbol is x^((q^2 - 1)/6), and zeta6 = 1 + w.
    """
    x = (c % q, d % q)
    if x == (0, 0):
        return None
    e, result, base = (q * q - 1) // 6, (1, 0), x
    while e:
        if e & 1:
            result = tuple(v % q for v in _mul_w(result, base))
        base = tuple(v % q for v in _mul_w(base, base))
        e >>= 1
    power = (1, 0)
    for k in range(6):
        if result == power:
            return k
        power = tuple(v % q for v in _mul_w(power, (1, 1)))
    raise ArithmeticError("inert sextic symbol is not a sixth root of unity")


def sextic_symbol_at(c: int, d: int, prime) -> int | None:
    """Sextic exponent of c + d w at a split DegreeOnePrime or an inert rational prime q."""
    return inert_sextic_exponent(c, d, prime) if isinstance(prime, int) else sextic_residue_exponent(c, d, prime)


def kubota_g6_prime(c, prime) -> complex:
    """g6(c, pi) = sum_{x mod pi} (x/pi)_6 e(Tr(c x / pi)) (Heath-Brown--Patterson trace form).

    Split pi = a + b w: residues t = 0..p-1 and Tr(c t / pi) = t Tr(c conj(pi)) / p.
    Inert q: residues s + t w with s, t mod q and Tr(c x / q) = Tr(c x) / q.
    """
    z6 = cmath.exp(1j * math.pi / 3)
    total = 0j
    if isinstance(prime, int):
        q = prime
        for s_ in range(q):
            for t in range(q):
                k = inert_sextic_exponent(s_, t, q)
                if k is not None:
                    total += z6 ** k * cmath.exp(2j * math.pi * eisenstein_trace(_mul_w(c, (s_, t))) / q)
        return total
    p = prime.p
    tr = eisenstein_trace(_mul_w(c, (prime.a - prime.b, -prime.b)))  # c * conj(pi)
    for t in range(1, p):
        total += z6 ** sextic_residue_exponent(t, 0, prime) * cmath.exp(2j * math.pi * t * tr / p)
    return total


def sextic_reciprocity_sign(x: DegreeOnePrime, y: DegreeOnePrime) -> int:
    """Exact pairwise reversal sign from the two field-quadratic symbols.

    Cubic reciprocity fixes the quotient's square to one; its cube is the
    quotient of the quadratic characters, equal to their product. This is an
    implementation identity, not an asymptotic spectral mechanism.
    """
    if x.n != 3 or y.n != 3:
        raise ValueError("sextic characters require primary Eisenstein primes")
    return legendre(x.a + x.b * y.root, y.p) * legendre(y.a + y.b * x.root, x.p)
