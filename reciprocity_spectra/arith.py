"""Exact arithmetic core for power-residue matrices of degree-one primes.

Conventions
-----------
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
        raise ValueError("n must be 2, 3 or 4")
    mat = [[symbol_between(x, y) for y in index] for x in index]
    return index, mat


def reciprocity_sign(n: int, x, y) -> int:
    """Sign ``s`` in the reciprocity law ``(y/x) = s (x/y)`` for the conventions above."""
    if n == 2:
        return -1 if (x % 4 == 3 and y % 4 == 3) else 1
    if n == 3:
        return 1
    if n == 4:
        return -1 if ((x.p - 1) // 4) * ((y.p - 1) // 4) % 2 else 1
    raise ValueError("n must be 2, 3 or 4")
