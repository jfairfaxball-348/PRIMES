"""Squarefree Eisenstein moduli and the trace-form Type II kernel.

Elements, norms, characters, CRT representatives and phase exponents are exact.
Functions returning ``complex`` evaluate roots of unity in floating point. The
moduli here are products of distinct primary prime elements, prime to 6; an
inert rational prime q has norm q**2. In particular, conjugate split primes are
distinct factors, whereas two copies of the same prime ideal are forbidden.

The kernel is restricted to coprime pairs. A zero at a noncoprime pair encodes
that restriction and is NOT an assertion about a nonsquarefree Gauss sum.
"""
from __future__ import annotations

import cmath
import math
from dataclasses import dataclass
from functools import cache, cached_property
from itertools import product

from reciprocity_spectra.arith import (
    DegreeOnePrime,
    _mul_w,
    eisenstein_trace,
    kubota_g6_prime,
    mod4_class_coordinates,
    primary_eisenstein_primes,
    primes_upto,
    sextic_symbol_at,
)

Element = tuple[int, int]
PrimeFactor = DegreeOnePrime | int
ZETA6 = cmath.exp(1j * math.pi / 3)


def factor_element(factor: PrimeFactor) -> Element:
    """The chosen primary generator of a split or inert prime ideal."""
    return (factor, 0) if isinstance(factor, int) else (factor.a, factor.b)


def factor_norm(factor: PrimeFactor) -> int:
    return factor * factor if isinstance(factor, int) else factor.p


@cache
def _validate_factor(factor: PrimeFactor) -> None:
    q = factor if isinstance(factor, int) else factor.p
    if q <= 3 or any(q % d == 0 for d in range(2, math.isqrt(q) + 1)):
        raise ValueError("factors must be primes away from 2 and 3")
    if isinstance(factor, int):
        if q % 3 != 2:
            raise ValueError("integer factors must be inert rational primes")
    elif (factor.n != 3 or q % 3 != 1 or factor.a % 3 != 2 or factor.b % 3
          or factor.a**2 - factor.a * factor.b + factor.b**2 != q):
        raise ValueError("split factors must be primary Eisenstein primes")


@dataclass(frozen=True)
class SquarefreeModulus:
    """A squarefree ideal together with its canonical product of generators.

    The empty tuple represents 1. Generators are multiplied without a further
    unit adjustment, so the product is congruent to +1 or -1 modulo 3.
    """

    factors: tuple[PrimeFactor, ...]

    def __post_init__(self) -> None:
        for factor in self.factors:
            _validate_factor(factor)
        factors = tuple(sorted(self.factors, key=lambda f: (factor_norm(f), factor_element(f))))
        if len(set(factors)) != len(factors):
            raise ValueError("repeated prime ideal: modulus is not squarefree")
        object.__setattr__(self, "factors", factors)

    @cached_property
    def element(self) -> Element:
        value = (1, 0)
        for factor in self.factors:
            value = _mul_w(value, factor_element(factor))
        return value

    @cached_property
    def norm(self) -> int:
        return math.prod(factor_norm(factor) for factor in self.factors)


def squarefree_moduli(limit: int) -> list[SquarefreeModulus]:
    """All squarefree ideals prime to 6 of norm <= limit, including the unit.

    Each ideal occurs once. Split conjugates and inert primes are both included;
    "squarefree" refers to prime ideals, not squarefree rational norms.
    """
    if limit < 1:
        return []
    factors: list[PrimeFactor] = list(primary_eisenstein_primes(limit))
    factors.extend(q for q in primes_upto(math.isqrt(limit)) if q > 2 and q % 3 == 2)
    factors.sort(key=lambda f: (factor_norm(f), factor_element(f)))
    out = []

    def visit(start: int, chosen: tuple[PrimeFactor, ...], norm: int) -> None:
        out.append(SquarefreeModulus(chosen))
        for i in range(start, len(factors)):
            next_norm = norm * factor_norm(factors[i])
            if next_norm > limit:
                break
            visit(i + 1, (*chosen, factors[i]), next_norm)

    visit(0, (), 1)
    return sorted(out, key=lambda m: (m.norm, m.element))


def symbol_exponent(alpha: Element, modulus: SquarefreeModulus) -> int | None:
    """k with (alpha/modulus)_6 = zeta6**k; None means a zero symbol."""
    exponent = 0
    for factor in modulus.factors:
        local = sextic_symbol_at(*alpha, factor)
        if local is None:
            return None
        exponent += local
    return exponent % 6


def coprime(m: SquarefreeModulus, n: SquarefreeModulus) -> bool:
    return not set(m.factors).intersection(n.factors)


def kernel_exponent(m: SquarefreeModulus, n: SquarefreeModulus) -> int | None:
    """Exponent of (m/n)_6(n/m)_6, or None outside the coprime restriction."""
    if not coprime(m, n):
        return None
    return (symbol_exponent(m.element, n) + symbol_exponent(n.element, m)) % 6


def reciprocity_sign(m: SquarefreeModulus, n: SquarefreeModulus) -> int:
    """The local quadratic reciprocity sign epsilon(m,n), determined modulo 4.

    Write m = omega**i (-1)**k (1+2 omega)**l mod 4, and similarly n.
    The dyadic quadratic Hilbert pairing is (-1)**(k*l' + l*k' + l*l').
    For our generators and coprime m,n, (n/m)_6 = epsilon(m,n)(m/n)_6.
    """
    if not coprime(m, n):
        raise ValueError("reciprocity identity requires coprime moduli")
    _, k, ell = mod4_class_coordinates(*m.element)
    _, k2, ell2 = mod4_class_coordinates(*n.element)
    return -1 if (k * ell2 + ell * k2 + ell * ell2) % 2 else 1


def cubic_kernel_exponent(m: SquarefreeModulus, n: SquarefreeModulus) -> int | None:
    """Exponent in omega of the cubic symbol (m/n)_3, with zero on noncoprime pairs.

    Cubic reciprocity and quadratic reciprocity give the EXACT reduction
    (m/n)_6(n/m)_6 = epsilon(m,n) * omega**cubic_kernel_exponent(m,n).
    This is a signed cubic kernel, not a generic sextic symbol matrix.
    """
    if not coprime(m, n):
        return None
    return symbol_exponent(m.element, n) % 3


@cache
def _normalized_prime_gauss(factor: PrimeFactor) -> complex:
    return kubota_g6_prime((1, 0), factor) / math.sqrt(factor_norm(factor))


@cache
def normalized_gauss_sum(c: Element, modulus: SquarefreeModulus) -> complex:
    """Floating evaluation of g6_trace(c,modulus)/sqrt(N(modulus)).

    Uses exact twisted multiplicativity and a cached direct prime Gauss sum.
    If a factor divides c the primitive local character sums to zero, so the
    squarefree Gauss sum is zero. No inverse symbol is used in that case.
    """
    twist = symbol_exponent(c, modulus)
    if twist is None:
        return 0j
    result = ZETA6 ** (-twist)
    prefix = SquarefreeModulus(())
    for factor in modulus.factors:
        single = SquarefreeModulus((factor,))
        result *= ZETA6 ** kernel_exponent(prefix, single) * _normalized_prime_gauss(factor)
        prefix = SquarefreeModulus((*prefix.factors, factor))
    return result


def bilinear_kernel(c: Element, m: SquarefreeModulus, n: SquarefreeModulus) -> complex:
    """Restricted kernel 1_(m,n)=1 * g6_trace(c,mn)/sqrt(N(mn)).

    For coprime m,n this equals the reciprocal-symbol product times the two
    normalized Gauss sums. A noncoprime pair is omitted, even if a Gauss sum
    at the nonsquarefree product could be nonzero.
    """
    exponent = kernel_exponent(m, n)
    if exponent is None:
        return 0j
    return ZETA6 ** exponent * normalized_gauss_sum(c, m) * normalized_gauss_sum(c, n)


def _inverse_at(alpha: Element, factor: PrimeFactor) -> Element:
    if isinstance(factor, int):
        a, b = alpha
        inverse_norm = pow((a * a - a * b + b * b) % factor, -1, factor)
        return ((a - b) * inverse_norm % factor, -b * inverse_norm % factor)
    return (pow((alpha[0] + alpha[1] * factor.root) % factor.p, -1, factor.p), 0)


def crt_representatives(modulus: SquarefreeModulus):
    """Yield exactly N(modulus) representatives using prime-field CRT.

    This constructs residue classes independently of the Gauss product formula.
    Representatives are reduced coordinatewise modulo N(modulus), which does
    not change their class modulo the ideal (modulus.element).
    """
    idempotents, residue_lists = [], []
    for i, factor in enumerate(modulus.factors):
        complement = SquarefreeModulus(modulus.factors[:i] + modulus.factors[i + 1:]).element
        idempotents.append(_mul_w(complement, _inverse_at(complement, factor)))
        if isinstance(factor, int):
            residue_lists.append([(a, b) for a in range(factor) for b in range(factor)])
        else:
            residue_lists.append([(a, 0) for a in range(factor.p)])
    for residues in product(*residue_lists):
        x = [0, 0]
        for residue, idempotent in zip(residues, idempotents, strict=True):
            term = _mul_w(residue, idempotent)
            x[0] += term[0]
            x[1] += term[1]
        yield (x[0] % modulus.norm, x[1] % modulus.norm)


def direct_gauss_sum(c: Element, modulus: SquarefreeModulus) -> complex:
    """Direct floating residue sum g6_trace(c,modulus), for small test moduli.

    Symbol exponents and Tr(c*x*conj(modulus))/N(modulus) are computed exactly;
    only the final roots of unity and summation use complex floating point.
    Neither prime Gauss sums nor twisted multiplicativity are used here.
    """
    a, b = modulus.element
    c_conjugate = _mul_w(c, (a - b, -b))
    total = 0j
    for x in crt_representatives(modulus):
        exponent = symbol_exponent(x, modulus)
        if exponent is not None:
            numerator = eisenstein_trace(_mul_w(c_conjugate, x)) % modulus.norm
            total += ZETA6 ** exponent * cmath.exp(2j * math.pi * numerator / modulus.norm)
    return total
