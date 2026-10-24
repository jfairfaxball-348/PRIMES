"""Exact checks for the Reciprocity Spectra arithmetic core (pure Python, no numpy)."""
import cmath
import math

from reciprocity_spectra.arith import (
    gauss_sum,
    jacobi_sum,
    legendre,
    primary_eisenstein_primes,
    primary_gaussian_primes,
    primes_upto,
    reciprocity_sign,
    residue_exponent,
    residue_matrix,
)


def test_primary_prime_enumeration():
    eis = primary_eisenstein_primes(500)
    gau = primary_gaussian_primes(500)
    assert len(eis) == 2 * sum(1 for p in primes_upto(500) if p % 3 == 1)
    assert len(gau) == 2 * sum(1 for p in primes_upto(500) if p % 4 == 1)
    for x in eis:
        assert x.a * x.a - x.a * x.b + x.b * x.b == x.p
        assert x.a % 3 == 2 and x.b % 3 == 0
        assert (x.root * x.root + x.root + 1) % x.p == 0
    for x in gau:
        assert x.a * x.a + x.b * x.b == x.p
        assert x.b % 2 == 0 and (x.a + x.b) % 4 == 1
        assert (x.root * x.root + 1) % x.p == 0


def test_cubic_gauss_sum_cube_is_p_times_pi():
    # Ireland--Rosen: for primary pi of norm p, g(chi_pi)^3 = p * pi.
    for x in primary_eisenstein_primes(200):
        g = gauss_sum(x)
        assert abs(abs(g) ** 2 - x.p) < 1e-8 * x.p
        assert abs(g ** 3 - x.p * x.complex_value()) < 1e-7 * x.p ** 1.5


def test_quartic_jacobi_and_gauss_sum_identities():
    # Ireland--Rosen 9.9.4: -chi(-1) J(chi, chi) = pi; consequently g(chi)^4 = p * pi^2.
    for x in primary_gaussian_primes(150):
        chi_m1 = 1j ** residue_exponent(-1, 0, x)
        assert abs(-chi_m1 * jacobi_sum(x) - x.complex_value()) < 1e-8 * x.p
        g = gauss_sum(x)
        assert abs(g ** 4 - x.p * x.complex_value() ** 2) < 1e-7 * x.p ** 2


def test_reciprocity_laws_hold_on_matrices():
    for n, limit in ((2, 300), (3, 400), (4, 400)):
        index, mat = residue_matrix(n, limit)
        size = len(index)
        assert size > 20
        for i in range(size):
            assert mat[i][i] is None
            for j in range(i + 1, size):
                kij, kji = mat[i][j], mat[j][i]
                assert kij is not None and kji is not None
                sign = reciprocity_sign(n, index[i], index[j])
                # (x_j/x_i) = sign * (x_i/x_j) translated to exponents of zeta_n
                shift = 0 if sign == 1 else n // 2
                assert kji == (kij + shift) % n


def test_symbols_are_multiplicative_characters():
    for x in primary_eisenstein_primes(150)[:10] + primary_gaussian_primes(150)[:10]:
        for s in range(2, 12):
            for t in range(2, 12):
                ks, kt = residue_exponent(s, 0, x), residue_exponent(t, 0, x)
                kst = residue_exponent(s * t, 0, x)
                if None not in (ks, kt, kst):
                    assert kst == (ks + kt) % x.n
    for p in primes_upto(200)[1:]:
        for a in range(1, 30):
            assert legendre(a * a, p) in (0, 1)


def test_cubic_matrix_is_symmetric_and_unimodular():
    index, mat = residue_matrix(3, 300)
    zeta = cmath.exp(2j * math.pi / 3)
    for i in range(len(index)):
        for j in range(len(index)):
            if i != j:
                assert mat[i][j] == mat[j][i]
                assert abs(abs(zeta ** mat[i][j]) - 1) < 1e-12
