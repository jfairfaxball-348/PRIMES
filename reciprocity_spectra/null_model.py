"""Exact structural null specification and independent small-matrix BFS sampler.

No numpy dependency. See NULL_CERTIFICATION.md for the conditional measure and
its scope. Production generation uses the native orbit sampler.
"""
from __future__ import annotations

from math import gcd

from reciprocity_spectra.arith import DegreeOnePrime, legendre, reciprocity_sign


def conjugate_label(n: int, value):
    if n == 2:
        return value
    if n in (3, 6) and value.n == 3:
        return DegreeOnePrime(3, value.p, value.a-value.b, -value.b)
    if n == 4 and value.n == 4:
        return DegreeOnePrime(4, value.p, value.a, -value.b)
    raise ValueError('Character order and index ring disagree')


def conjugate_permutation(n: int, index: list) -> list[int]:
    lookup = {value: i for i, value in enumerate(index)}
    if len(lookup) != len(index):
        raise ValueError('Duplicate index')
    bar = [lookup[conjugate_label(n, value)] for value in index]
    if any(bar[bar[i]] != i for i in range(len(index))):
        raise ValueError('Conjugation must be an involution')
    return bar


def conjugate_pair_phase(n: int, prime) -> int | None:
    """One-prime trace formula; never reads an arithmetic matrix entry."""
    if n == 2:
        return None  # the conjugation orbit is the zero diagonal
    if n == 3:
        return 0
    if n == 6:
        q = legendre(2*prime.a-prime.b, prime.p)
        if q == 0:
            raise ArithmeticError('Ramified trace is outside the split-prime index set')
        return 0 if q == 1 else 3
    if n == 4:
        p = prime.p
        root_at_conjugate = prime.a * pow(prime.b % p, -1, p) % p
        target = pow(2*prime.a % p, (p-1)//4, p)
        power = 1
        for k in range(4):
            if power == target:
                return k
            power = power * root_at_conjugate % p
        raise ArithmeticError('Trace character is not a fourth root')
    raise ValueError('Unsupported character order')


def unit_multiple(n: int, label, power: int):
    """Multiply by (-1)^power, (1+omega)^power or i^power in the label ring."""
    if n == 2:
        return label * (-1 if power % 2 else 1)
    order = 4 if n == 4 else 6
    a, b = label.a, label.b
    for _ in range(power % order):
        a, b = (-b, a) if n == 4 else (a-b, a)
    return DegreeOnePrime(label.n, label.p, a, b)


def is_primary(n: int, label) -> bool:
    if n == 2:
        return label > 0 and label % 2 == 1
    if n in (3, 6):
        return label.n == 3 and label.a % 3 == 2 and label.b % 3 == 0
    if n == 4:
        return label.n == 4 and label.b % 2 == 0 and (label.a+label.b) % 4 == 1
    raise ValueError('Unsupported character order')


def unit_character_phase(n: int, prime, power: int) -> int:
    p = prime if n == 2 else prime.p
    denominator = 6 if n in (3, 6) else n
    return power * ((p-1)//denominator) % n


def root_galois_powers(n: int) -> list[int]:
    return [k for k in range(1, n) if gcd(k, n) == 1]


def counter_choice(seed: int, leader: int, count: int) -> int:
    """SplitMix64 counter/rejection specification, independent of orbit propagation."""
    if count <= 0:
        raise ValueError('Empty phase set')
    mask = (1 << 64)-1
    state = (seed+leader) & mask
    threshold = (1 << 64) % count
    while True:
        state = (state+0x9E3779B97F4A7C15) & mask
        z = state
        z = ((z ^ (z >> 30))*0xBF58476D1CE4E5B9) & mask
        z = ((z ^ (z >> 27))*0x94D049BB133111EB) & mask
        z ^= z >> 31
        if z >= threshold:
            return z % count


def reference_control(n: int, index: list, seed: int = 0) -> list[list[int | None]]:
    """Exact BFS reference for small matrices; no closed four-position formula."""
    d = len(index)
    bar = conjugate_permutation(n, index)
    matrix = [[None for _ in range(d)] for _ in range(d)]
    done = {(i, i) for i in range(d)}
    shifts = {}

    def shift(i, j):
        if (i, j) not in shifts:
            sign = reciprocity_sign(n, index[i], index[j])
            if sign not in (-1, 1):
                raise ArithmeticError('Nonzero reversal must be a sign')
            shifts[i, j] = n//2 if sign == -1 else 0
        return shifts[i, j]

    def propagate(i, j, phase):
        assigned = {(i, j): phase}
        pending = [(i, j)]
        while pending:
            a, b = pending.pop()
            v = assigned[a, b]
            for position, value in [((b, a), (v+shift(a, b)) % n),
                                    ((bar[a], bar[b]), -v % n)]:
                if position in assigned:
                    if assigned[position] != value:
                        return None
                else:
                    assigned[position] = value
                    pending.append(position)
        return assigned

    for i in range(d):
        for j in range(i+1, d):
            if (i, j) in done:
                continue
            candidates = [conjugate_pair_phase(n, index[i])] if j == bar[i] else range(n)
            allowed = [values for k in candidates if (values := propagate(i, j, k)) is not None]
            if not allowed:
                raise ArithmeticError('Incompatible orbit stabilizer or boundary')
            chosen = allowed[counter_choice(seed, i*d+j, len(allowed))]
            if min(chosen) != (i, j):
                raise ArithmeticError('Leader is not canonical')
            for (a, b), value in chosen.items():
                matrix[a][b] = value
                done.add((a, b))
    return matrix
