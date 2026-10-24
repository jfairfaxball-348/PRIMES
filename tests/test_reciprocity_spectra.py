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


def test_native_byte_engine_against_exact_core(tmp_path):
    """No numpy dependency: check symbols, complex adjoints and control signs."""
    import ctypes as ct
    import shutil
    import struct
    import subprocess
    from array import array
    from pathlib import Path

    import pytest

    if not shutil.which('cc'):
        pytest.skip('C compiler unavailable')
    source = Path(__file__).resolve().parents[1] / 'reciprocity_spectra/native/residue_engine.c'
    exe, libpath = tmp_path / 'engine', tmp_path / 'engine.so'
    for flags, target in [([], exe), (['-shared', '-fPIC'], libpath)]:
        subprocess.run(['cc', '-O2', '-fopenmp', *flags, '-o', str(target),
                        str(source), '-lm'], check=True)
    lib = ct.CDLL(str(libpath))
    lib.rs_apply.argtypes = [ct.c_void_p, ct.c_int, ct.c_int, ct.c_void_p,
                            ct.c_void_p, ct.c_int]
    lib.rs_random.argtypes = [ct.c_void_p, ct.c_int, ct.c_int, ct.c_void_p, ct.c_uint64]
    for n, mode in [(2, 'quad'), (3, 'cubic'), (4, 'quartic')]:
        path = tmp_path / f'{mode}.bin'
        subprocess.run([str(exe), mode, '100', str(path)], check=True)
        raw = path.read_bytes()
        d = struct.unpack_from('=i', raw)[0]
        meta = [struct.unpack_from('=qqq', raw, 4 + 24 * j) for j in range(d)]
        index, expected = residue_matrix(n, 100)
        lookup = {((p, p, 0) if n == 2 else (p.p, p.a, p.b)): i
                  for i, p in enumerate(index)}
        e = (ct.c_uint8 * (d*d)).from_buffer_copy(raw[4+24*d:])
        for i in range(d):
            for j in range(d):
                want = expected[lookup[meta[i]]][lookup[meta[j]]]
                assert e[i*d+j] == (255 if want is None else want)
        z = [complex(i % 5 - 2, i % 7 - 3) for i in range(d)]
        xv = array('d', [t for v in z for t in (v.real, v.imag)])
        yv = array('d', [0.] * (2*d))
        roots = [cmath.exp(2j * math.pi * k / n) for k in range(n)] + [0j] * (256-n)
        for adjoint in [False, True]:
            lib.rs_apply(e, d, n, xv.buffer_info()[0], yv.buffer_info()[0], adjoint)
            for i in range(d):
                want = sum((roots[e[j*d+i]].conjugate() if adjoint else roots[e[i*d+j]]) * z[j]
                           for j in range(d))
                assert abs(complex(yv[2*i], yv[2*i+1]) - want) < 1e-10
        primes = array('q', [p for p, _, _ in meta])
        lib.rs_random(e, d, n, primes.buffer_info()[0], 0)
        first = bytes(e)
        lib.rs_random(e, d, n, primes.buffer_info()[0], 0)
        assert first == bytes(e)
        for i in range(d):
            assert e[i*d+i] == 255
            for j in range(i+1, d):
                s = reciprocity_sign(n, index[lookup[meta[i]]], index[lookup[meta[j]]])
                assert e[j*d+i] == (e[i*d+j] + (n//2 if s == -1 else 0)) % n
