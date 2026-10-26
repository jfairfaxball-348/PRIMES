"""Exact checks for the Reciprocity Spectra arithmetic core (pure Python, no numpy)."""
import cmath
import math

from reciprocity_spectra.arith import (
    DegreeOnePrime,
    gauss_sum,
    jacobi_sum,
    legendre,
    primary_eisenstein_primes,
    primary_gaussian_primes,
    primes_upto,
    reciprocity_sign,
    residue_exponent,
    residue_matrix,
    sextic_reciprocity_sign,
    sextic_residue_exponent,
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
    lib.rs_apply_sym.argtypes = [ct.c_void_p, ct.c_int, ct.c_int, ct.c_void_p,
                                ct.c_void_p, ct.c_void_p, ct.c_int]
    lib.rs_random.argtypes = [ct.c_void_p, ct.c_int, ct.c_int, ct.c_void_p, ct.c_uint64]
    lib.rs_pair_signs.argtypes = [ct.c_void_p, ct.c_void_p, ct.c_int, ct.c_int]
    lib.rs_pair_signs.restype = ct.c_uint64
    lib.rs_apply_signed.argtypes = [ct.c_void_p, ct.c_void_p, ct.c_int, ct.c_int,
                                   ct.c_void_p, ct.c_void_p, ct.c_int]
    lib.rs_random_signed.argtypes = [ct.c_void_p, ct.c_void_p, ct.c_int, ct.c_int, ct.c_uint64]
    for n, mode in [(2, 'quad'), (3, 'cubic'), (4, 'quartic'), (6, 'sextic')]:
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
        signs = (ct.c_uint8 * (d*d))()
        assert lib.rs_pair_signs(e, signs, d, n) == 0
        for i in range(d):
            for j in range(d):
                if i != j:
                    sign = reciprocity_sign(n, index[lookup[meta[i]]], index[lookup[meta[j]]])
                    assert signs[i*d+j] == (sign == -1)
        z = [complex(i % 5 - 2, i % 7 - 3) for i in range(d)]
        xv = array('d', [t for v in z for t in (v.real, v.imag)])
        yv = array('d', [0.] * (2*d))
        roots = [cmath.exp(2j * math.pi * k / n) for k in range(n)] + [0j] * (256-n)
        odd = array('B', [int(p % 4 == 3 if n == 2 else p % 8 == 5 if n == 4 else False)
                          for p, _, _ in meta])
        for adjoint in [False, True]:
            for symmetric in [False, True]:
                if symmetric and n == 6:
                    lib.rs_apply_signed(e, signs, d, n, xv.buffer_info()[0],
                                        yv.buffer_info()[0], adjoint)
                elif symmetric:
                    lib.rs_apply_sym(e, d, n, odd.buffer_info()[0], xv.buffer_info()[0],
                                     yv.buffer_info()[0], adjoint)
                else:
                    lib.rs_apply(e, d, n, xv.buffer_info()[0], yv.buffer_info()[0], adjoint)
                for i in range(d):
                    want = sum((roots[e[j*d+i]].conjugate() if adjoint else roots[e[i*d+j]]) * z[j]
                               for j in range(d))
                    assert abs(complex(yv[2*i], yv[2*i+1]) - want) < 1e-10
        primes = array('q', [p for p, _, _ in meta])
        if n == 6:
            lib.rs_random_signed(e, signs, d, n, 0)
        else:
            lib.rs_random(e, d, n, primes.buffer_info()[0], 0)
        first = bytes(e)
        if n == 6:
            lib.rs_random_signed(e, signs, d, n, 0)
        else:
            lib.rs_random(e, d, n, primes.buffer_info()[0], 0)
        assert first == bytes(e)
        for i in range(d):
            assert e[i*d+i] == 255
            for j in range(i+1, d):
                s = reciprocity_sign(n, index[lookup[meta[i]]], index[lookup[meta[j]]])
                assert e[j*d+i] == (e[i*d+j] + (n//2 if s == -1 else 0)) % n



def test_sextic_normalization_and_multiplicativity():
    for prime in primary_eisenstein_primes(300):
        for c, d in [(1, 0), (-1, 0), (0, 1), (1, 1), (2, -1), (-3, 2)]:
            k6 = sextic_residue_exponent(c, d, prime)
            k3 = residue_exponent(c, d, prime)
            q = legendre(c + d * prime.root, prime.p)
            if k6 is None:
                assert k3 is None and q == 0
            else:
                assert k6 % 3 == k3
                assert (-1)**k6 == q
                assert k6 == (4*k3 + 3*(q == -1)) % 6
        assert sextic_residue_exponent(-1, 0, prime) == (3*((prime.p-1)//6)) % 6
        assert sextic_residue_exponent(1, 1, prime) == ((prime.p-1)//6) % 6
        for c, d in [(2, 1), (-1, 2), (3, -2)]:
            for a, b in [(1, 1), (2, -1), (-2, 3)]:
                left = sextic_residue_exponent(c, d, prime)
                right = sextic_residue_exponent(a, b, prime)
                product = sextic_residue_exponent(c*a-d*b, c*b+d*a-d*b, prime)
                if None in (left, right):
                    assert product is None
                else:
                    assert product == (left + right) % 6


def test_sextic_reciprocity_uses_field_quadratic_pair_signs():
    index, matrix = residue_matrix(6, 400)
    seen = set()
    for i, x in enumerate(index):
        assert matrix[i][i] is None
        for j, y in enumerate(index):
            if i == j:
                continue
            sign = sextic_reciprocity_sign(x, y)
            seen.add(sign)
            assert sign in (-1, 1)
            assert matrix[j][i] == (matrix[i][j] + (3 if sign == -1 else 0)) % 6
    assert seen == {-1, 1}


def _conjugation_index(n, index):
    from reciprocity_spectra.arith import conjugate_prime
    lookup = {(p.p, p.a, p.b): i for i, p in enumerate(index)}
    return [lookup[(c.p, c.a, c.b)] for c in map(conjugate_prime, index)]


def test_conjugation_identity_and_forced_conjugate_pairs():
    """(conj x/conj y)_n = conj((x/y)_n); (pi/conj pi)_n lies in the reflection-fixed set."""
    from reciprocity_spectra.arith import conjugate_pair_exponents, conjugate_prime

    for n in (3, 4, 6):
        index, mat = residue_matrix(n, 600)
        conj = _conjugation_index(n, index)
        for i, x in enumerate(index):
            c = conjugate_prime(x)
            assert c.p == x.p and conj[i] != i and conj[conj[i]] == i
            for j in range(len(index)):
                if i == j:
                    continue
                assert mat[conj[i]][conj[j]] == (-mat[i][j]) % n
                assert reciprocity_sign(n, index[conj[i]], index[conj[j]]) == \
                    reciprocity_sign(n, x, index[j])
            sign = reciprocity_sign(n, x, index[conj[i]])
            assert mat[i][conj[i]] in conjugate_pair_exponents(n, sign)
            if n == 3:
                assert mat[i][conj[i]] == 0
            if n == 6:
                assert sign == 1


def test_cubic_matrix_times_conjugation_is_hermitian():
    """C symmetric and C[conj, conj] = conj(C) imply that H = C P is Hermitian, H_ij = C_{i,conj j}."""
    index, mat = residue_matrix(3, 600)
    conj = _conjugation_index(3, index)
    for i in range(len(index)):
        for j in range(len(index)):
            hij, hji = mat[i][conj[j]], mat[j][conj[i]]
            if hij is None:
                assert hji is None
            else:
                assert hij == (-hji) % 3


def _splitmix_exponent(seed, a, b, d, n):
    mask = (1 << 64) - 1

    def mix(x):
        x = ((x ^ (x >> 30)) * 0xbf58476d1ce4e5b9) & mask
        x = ((x ^ (x >> 27)) * 0x94d049bb133111eb) & mask
        return x ^ (x >> 31)

    state = (seed + a * d + b) & mask
    while True:
        state = (state + 0x9e3779b97f4a7c15) & mask
        u = mix(state)
        if u >= ((1 << 64) - n) % n:
            return u % n


def test_native_conjugation_orbit_control(tmp_path):
    """rs_random_conj: exact identities, copied conjugate pairs, and a pure-Python reference."""
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
    lib.rs_pair_signs.argtypes = [ct.c_void_p, ct.c_void_p, ct.c_int, ct.c_int]
    lib.rs_pair_signs.restype = ct.c_uint64
    lib.rs_random_conj.argtypes = [ct.c_void_p, ct.c_void_p, ct.c_void_p, ct.c_void_p,
                                   ct.c_int, ct.c_int, ct.c_uint64]
    lib.rs_random_conj.restype = ct.c_uint64
    for n, mode in [(3, 'cubic'), (4, 'quartic'), (6, 'sextic')]:
        path = tmp_path / f'{mode}.bin'
        subprocess.run([str(exe), mode, '400', str(path)], check=True)
        raw = path.read_bytes()
        d = struct.unpack_from('=i', raw)[0]
        meta = [struct.unpack_from('=qqq', raw, 4 + 24 * j) for j in range(d)]
        e = (ct.c_uint8 * (d*d)).from_buffer_copy(raw[4+24*d:])
        signs = (ct.c_uint8 * (d*d))()
        assert lib.rs_pair_signs(e, signs, d, n) == 0
        key = {m: i for i, m in enumerate(meta)}
        conj = array('i', [key[(p, a - b, -b) if n != 4 else (p, a, -b)] for p, a, b in meta])
        forced = array('B', [e[i*d + conj[i]] for i in range(d)])
        out = (ct.c_uint8 * (d*d))()
        for seed in (0, 7):
            assert lib.rs_random_conj(out, signs, conj.buffer_info()[0],
                                      forced.buffer_info()[0], d, n, seed) == 0
            h = n // 2
            for i in range(d):
                assert out[i*d+i] == 255
                for j in range(d):
                    if i == j:
                        continue
                    v = out[i*d+j]
                    assert out[j*d+i] == (v + signs[i*d+j] * h) % n
                    assert out[conj[i]*d + conj[j]] == (-v) % n
                    if j == conj[i]:
                        assert v == forced[i]
                    elif i < j and (i, j) <= tuple(sorted((conj[i], conj[j]))):
                        assert v == _splitmix_exponent(seed, i, j, d, n)
            if seed == 0:
                differs = sum(out[k] != e[k] for k in range(d*d))
                assert differs > d * d // 2


def test_sextic_gauss_sum_identities():
    """|g6|^2 = p and g6^2 = J(chi6, chi6) g3, since chi6^2 is the cubic character."""
    from reciprocity_spectra.arith import sextic_gauss_sum, sextic_jacobi_sum

    for prime in primary_eisenstein_primes(400):
        g6, g3 = sextic_gauss_sum(prime), gauss_sum(prime)
        assert abs(abs(g6) ** 2 - prime.p) < 1e-8 * prime.p
        assert abs(g6 * g6 - sextic_jacobi_sum(prime) * g3) < 1e-8 * prime.p


def test_native_sextic_gauss_sums(tmp_path):
    import shutil
    import struct
    import subprocess
    from pathlib import Path

    import pytest

    from reciprocity_spectra.arith import sextic_gauss_sum

    if not shutil.which('cc'):
        pytest.skip('C compiler unavailable')
    source = Path(__file__).resolve().parents[1] / 'reciprocity_spectra/native/residue_engine.c'
    exe = tmp_path / 'engine'
    subprocess.run(['cc', '-O2', '-fopenmp', '-o', str(exe), str(source), '-lm'], check=True)
    subprocess.run([str(exe), 'sextic', '400', str(tmp_path / 'm.bin'), str(tmp_path / 'g.bin')],
                   check=True)
    raw, g = (tmp_path / 'm.bin').read_bytes(), (tmp_path / 'g.bin').read_bytes()
    d = struct.unpack_from('=i', raw)[0]
    for j in range(d):
        p, a, b = struct.unpack_from('=qqq', raw, 4 + 24 * j)
        re, im = struct.unpack_from('=dd', g, 16 * j)
        want = sextic_gauss_sum(DegreeOnePrime(3, p, a, b)) / math.sqrt(p)
        assert abs(complex(re, im) - want) < 1e-9


def test_sextic_unit_symbols_are_characters_of_the_norm():
    """(zeta6^j / pi)_6 = zeta6^(j(p-1)/6): a character of p mod 36, equal to (-1/p) for j = 3.

    So for an associate u' = zeta6^j u, (u'/pi)_6 = zeta6^(j(p-1)/6) (u/pi)_6. The extra factor is
    unramified at 3 (it depends on p mod 4 only) exactly for j in {0, 3}, i.e. u' = +-u.
    """
    primes = primary_eisenstein_primes(2000)
    units = [(1, 0), (1, 1), (0, 1), (-1, 0), (-1, -1), (0, -1)]  # zeta6^j = (1 + w)^j
    for prime in primes:
        p = prime.p
        for j, (c, d) in enumerate(units):
            assert sextic_residue_exponent(c, d, prime) == (j * (p - 1) // 6) % 6
        assert (-1) ** ((p - 1) // 6) == legendre(-1, p)
    # multiplicativity in p of e(p) = (p - 1)/6 mod 6 on p = 1 mod 6, and its 3-part dependence
    for p in range(7, 400, 6):
        for q in range(7, 400, 6):
            assert ((p * q - 1) // 6) % 6 == ((p - 1) // 6 + (q - 1) // 6) % 6
    by_class = {}
    for p in range(7, 2000, 6):
        by_class.setdefault(p % 36, set()).add(((p - 1) // 6) % 6)
    assert all(len(v) == 1 for v in by_class.values())
    assert {p % 36 for p in range(7, 2000, 6) if ((p - 1) // 6) % 6 in (0, 3)} == {1, 19}
    assert {p % 36 for p in range(7, 2000, 6) if ((p - 1) // 6) % 2 == 0} == {1, 13, 25}


def test_note_tables_match_results():
    """NOTE_DRAFT.md tables are regenerated verbatim from the committed results JSONs."""
    import subprocess
    import sys
    from pathlib import Path

    script = Path(__file__).resolve().parents[1] / 'reciprocity_spectra/scripts/note_tables.py'
    subprocess.run([sys.executable, str(script), '--check'], check=True)


def test_sextic_gauss_sum_hasse_davenport_factorization():
    """g6~(rho) = conj((2/rho)_3) (rho/|rho|) g2~(p) conj(g3~(rho)) (Astra referee, 2026-10-25).

    g2~ = 1 for p = 1 (mod 4) and i for p = 3 (mod 4); our e(t/p) normalization throughout.
    """
    from reciprocity_spectra.arith import sextic_gauss_sum

    w = cmath.exp(2j * math.pi / 3)
    for rho in primary_eisenstein_primes(1500):
        p = rho.p
        g6, g3 = sextic_gauss_sum(rho) / math.sqrt(p), gauss_sum(rho) / math.sqrt(p)
        g2 = 1 if p % 4 == 1 else 1j
        phase = rho.complex_value() / abs(rho.complex_value())
        chi = w ** residue_exponent(2, 0, rho)
        assert abs(g6 - chi.conjugate() * phase * g2 * g3.conjugate()) < 1e-9


def test_kubota_sextic_gauss_sums_and_twisted_multiplicativity():
    """Trace-form g6(c, n): |g6(1, pi)|^2 = N(pi); relation to our e(t/p) sum; CRT multiplicativity.

    g_ours(pi) = (conj(pi)/pi)_6 g6(1, pi) (Astra referee check 3), and for coprime n1, n2:
    g6(c, n1 n2) = (n1/n2)_6 (n2/n1)_6 g6(c, n1) g6(c, n2), verified by direct summation.
    """
    from reciprocity_spectra.arith import (
        _mul_w,
        eisenstein_trace,
        kubota_g6_prime,
        sextic_gauss_sum,
        sextic_symbol_at,
    )

    z6 = cmath.exp(1j * math.pi / 3)
    primes = primary_eisenstein_primes(120)
    for pi in primes:
        g = kubota_g6_prime((1, 0), pi)
        assert abs(abs(g) ** 2 - pi.p) < 1e-8 * pi.p
        k = sextic_residue_exponent(pi.a - pi.b, -pi.b, pi)  # (conj pi / pi)_6
        assert abs(sextic_gauss_sum(pi) - z6 ** k * g) < 1e-8 * pi.p
        for c in [(0, 1), (1, 1), (-1, 0)]:  # g6(u, pi) = conj((u/pi)_6) g6(1, pi) for units u
            assert abs(kubota_g6_prime(c, pi) - z6 ** (-sextic_residue_exponent(*c, pi)) * g) < 1e-8 * pi.p
    for q in (5, 11):
        assert abs(abs(kubota_g6_prime((1, 0), q)) - q) < 1e-8 * q

    def symbol(x, factors):
        ks = [sextic_symbol_at(*x, f) for f in factors]
        return None if None in ks else sum(ks) % 6

    def element(f):
        return (f, 0) if isinstance(f, int) else (f.a, f.b)

    def direct(c, factors, reps, n):
        nbar = (n[0] - n[1], -n[1])
        norm = n[0] ** 2 - n[0] * n[1] + n[1] ** 2
        total = 0j
        for x in reps:
            k = symbol(x, factors)
            if k is not None:
                total += z6 ** k * cmath.exp(2j * math.pi * eisenstein_trace(_mul_w(_mul_w(c, x), nbar)) / norm)
        return total

    cases = [(primes[0], primes[2]), (primes[0], primes[1]), (primes[2], 5)]
    for f1, f2 in cases:
        n = _mul_w(element(f1), element(f2))
        norm = n[0] ** 2 - n[0] * n[1] + n[1] ** 2
        if isinstance(f2, int) or f1.p == f2.p:  # Z[w]/n is not cyclic: residues s + t w modulo m
            m = f2 if isinstance(f2, int) else f1.p
            m = m * (f1.p if isinstance(f2, int) else 1)
            reps = [(s_, t) for s_ in range(m) for t in range(norm // m)]
        else:
            reps = [(s_, 0) for s_ in range(norm)]
        for c in [(1, 0), (0, 1), (1, 1)]:
            want = direct(c, [f1, f2], reps, n)
            twist = z6 ** (sextic_symbol_at(*element(f1), f2) + sextic_symbol_at(*element(f2), f1))
            got = twist * kubota_g6_prime(c, f1) * kubota_g6_prime(c, f2)
            assert abs(want - got) < 1e-7 * norm


def test_squarefree_moduli_include_inert_and_conjugate_split_factors():
    """Ideal-squarefreeness permits norm p^2 from conjugate split factors."""
    from collections import Counter

    import pytest

    from reciprocity_spectra.bilinear import SquarefreeModulus, squarefree_moduli

    moduli = squarefree_moduli(500)
    assert squarefree_moduli(0) == []
    assert squarefree_moduli(1) == [SquarefreeModulus(())]
    assert len(set(moduli)) == len(moduli)
    assert Counter(m.norm for m in moduli if m.norm <= 49) == Counter(
        [1, 7, 7, 13, 13, 19, 19, 25, 31, 31, 37, 37, 43, 43, 49])
    # Independent rational-norm Euler factors: split (1+2t+t^2), inert (1+t^2).
    counts = {1: 1}
    for p in primes_upto(500):
        terms = [(1, 1)]
        if p > 3 and p % 3 == 1:
            terms += [(p, 2), (p * p, 1)]
        elif p > 3 and p % 3 == 2:
            terms += [(p * p, 1)]
        updated = Counter()
        for norm, count in counts.items():
            for factor, multiplicity in terms:
                if norm * factor <= 500:
                    updated[norm * factor] += count * multiplicity
        counts = updated
    assert Counter(m.norm for m in moduli) == counts
    for m in moduli:
        a, b = m.element
        assert m.norm == a * a - a * b + b * b
        assert a % 3 in (1, 2) and b % 3 == 0
    pi, conjugate = primary_eisenstein_primes(7)
    assert SquarefreeModulus((pi, conjugate)).norm == 49
    assert SquarefreeModulus((pi, 5)) == SquarefreeModulus((5, pi))
    for factors in ((pi, pi), (5, 5), (2,), (3,), (7,), (35,), (DegreeOnePrime(3, 7, 1, 3),)):
        with pytest.raises(ValueError):
            SquarefreeModulus(factors)


def test_squarefree_kernel_reduces_to_cubic_with_local_sign():
    """Exact character exponents, including inert and composite moduli, norm <= 300."""
    from reciprocity_spectra.arith import _mul_w
    from reciprocity_spectra.bilinear import (
        coprime,
        cubic_kernel_exponent,
        kernel_exponent,
        squarefree_moduli,
        symbol_exponent,
    )
    from reciprocity_spectra.bilinear import reciprocity_sign as local_sign

    def independent_cubic(alpha, modulus):
        exponent = 0
        for factor in modulus.factors:
            if not isinstance(factor, int):
                exponent += residue_exponent(*alpha, factor)
                continue
            # Direct cubic Euler criterion in F_(q^2), not a sextic exponent reduction.
            e, base, power = (factor * factor - 1) // 3, alpha, (1, 0)
            while e:
                if e & 1:
                    power = tuple(v % factor for v in _mul_w(power, base))
                base = tuple(v % factor for v in _mul_w(base, base))
                e //= 2
            roots = ((1, 0), (0, 1), (factor - 1, factor - 1))
            exponent += roots.index(power)
        return exponent % 3

    moduli = squarefree_moduli(300)
    signs = set()
    for m in moduli:
        for n in moduli:
            exponent = kernel_exponent(m, n)
            if not coprime(m, n):
                assert exponent is None
                assert cubic_kernel_exponent(m, n) is None
                continue
            forward, backward = symbol_exponent(m.element, n), symbol_exponent(n.element, m)
            sign = local_sign(m, n)
            signs.add(sign)
            shift = 3 if sign == -1 else 0
            assert backward == (forward + shift) % 6
            cubic = independent_cubic(m.element, n)
            assert cubic_kernel_exponent(m, n) == cubic
            assert exponent == (2 * cubic + shift) % 6
    assert signs == {-1, 1}


def test_squarefree_gauss_product_against_independent_crt_residue_sum():
    """Float Gauss values validate exact CRT identities; c may share a prime factor."""
    from reciprocity_spectra.bilinear import (
        SquarefreeModulus,
        bilinear_kernel,
        crt_representatives,
        direct_gauss_sum,
        normalized_gauss_sum,
    )

    pi, conjugate, rho, _ = primary_eisenstein_primes(13)
    cases = [(), (pi,), (5,), (pi, conjugate), (pi, rho), (pi, 5),
             (5, 11), (pi, rho, 5), (pi, conjugate, rho)]

    def residue_signature(x, factors):
        return tuple((x[0] % f, x[1] % f) if isinstance(f, int)
                     else ((x[0] + x[1] * f.root) % f.p,)
                     for f in factors)

    for factors in cases:
        modulus = SquarefreeModulus(factors)
        residues = list(crt_representatives(modulus))
        assert len(residues) == modulus.norm
        assert len({residue_signature(x, modulus.factors) for x in residues}) == modulus.norm
        left = SquarefreeModulus(modulus.factors[:1])
        right = SquarefreeModulus(modulus.factors[1:])
        for c in [(1, 0), (0, 1), (2, -1), (pi.a, pi.b), (5, 0), (0, 0)]:
            direct = direct_gauss_sum(c, modulus) / math.sqrt(modulus.norm)
            assert abs(normalized_gauss_sum(c, modulus) - direct) < 1e-9
            assert abs(bilinear_kernel(c, left, right) - direct) < 1e-9


def test_bilinear_kernel_coprime_restriction_and_ramified_frequency():
    """A noncoprime pair is excluded; a factor dividing c gives an actual zero."""
    import pytest

    from reciprocity_spectra.bilinear import (
        SquarefreeModulus,
        bilinear_kernel,
        direct_gauss_sum,
        kernel_exponent,
        normalized_gauss_sum,
        symbol_exponent,
    )
    from reciprocity_spectra.bilinear import reciprocity_sign as local_sign

    pi, conjugate = primary_eisenstein_primes(7)
    m, n = SquarefreeModulus((pi,)), SquarefreeModulus((conjugate, 5))
    shared = SquarefreeModulus((pi, 5))
    assert kernel_exponent(m, shared) is None
    assert bilinear_kernel((1, 0), m, shared) == 0j
    with pytest.raises(ValueError, match="coprime"):
        local_sign(m, shared)
    assert symbol_exponent(m.element, shared) is None
    assert normalized_gauss_sum(m.element, shared) == 0j
    assert abs(direct_gauss_sum(m.element, shared)) < 1e-9
    assert bilinear_kernel(m.element, m, n) == 0j
    assert abs(abs(normalized_gauss_sum((1, 0), shared)) - 1) < 1e-10


def test_conjugate_ratio_symbol_is_two_adic():
    """(conj pi / pi)_6 = +-1 is a function of (a, b) mod 4 only, and +1 when p = 3 (mod 4)."""
    table = {}
    for pi in primary_eisenstein_primes(20000):
        k = sextic_residue_exponent(pi.a - pi.b, -pi.b, pi)
        assert k in (0, 3)
        if pi.p % 4 == 3:
            assert k == 0
        assert table.setdefault((pi.a % 4, pi.b % 4), k) == k


def test_sixth_power_twist_invariance_refutes_unreduced_strength_norm():
    """u=64 is a sixth power with no prime divisor in the matrix index.

    Character equality gives vector/Rayleigh equality at every scale; the
    unreduced norm law instead requires relative excess 1/4. The general
    identity is tested away from prime divisors of the sixth-power base.
    """
    from fractions import Fraction

    from reciprocity_spectra.arith import _mul_w

    for rho in primary_eisenstein_primes(1000):
        assert sextic_residue_exponent(64, 0, rho) == 0
        for base in [(2, 0), (1, -1), (-1, -3)]:
            if sextic_residue_exponent(*base, rho) is None:
                continue
            power = (1, 0)
            for _ in range(6):
                power = _mul_w(power, base)
            for u in [(1, 0), (0, 1), (2, 0), (rho.a, rho.b)]:
                assert sextic_residue_exponent(*_mul_w(u, power), rho) == sextic_residue_exponent(*u, rho)
    assert 64**2 == 4**6
    assert Fraction(1, 4) != 1


def test_mod4_unit_group_and_two_adic_characters():
    """(Z[w]/4)^x = <w> x <-1> x <1+2w>; (2/rho)_3 = chi(1,0,0); (-1/p) = chi(0,0,1);
    (conj rho/rho)_6 is a class function mod 4 but not a character."""
    import itertools

    from reciprocity_spectra.arith import _mul_w, mod4_character, mod4_class_coordinates

    units = [(a, b) for a in range(4) for b in range(4) if (a % 2, b % 2) != (0, 0)]
    coords = {u: mod4_class_coordinates(*u) for u in units}
    assert len(set(coords.values())) == 12
    for u in units:
        for v in units:
            uv = tuple(c % 4 for c in _mul_w(u, v))
            assert coords[uv] == tuple((x + y) % n for x, y, n in zip(coords[u], coords[v], (3, 2, 2), strict=True))
    w = cmath.exp(2j * math.pi / 3)
    primes = primary_eisenstein_primes(5000)
    assert len({coords[(p.a % 4, p.b % 4)] for p in primes}) == 12
    for p in primes:
        assert abs(w ** residue_exponent(2, 0, p) - mod4_character(1, 0, 0, p.a, p.b)) < 1e-12
        assert abs((-1) ** ((p.p - 1) // 2) - mod4_character(0, 0, 1, p.a, p.b)) < 1e-12
    psi = {p: (-1) ** (sextic_residue_exponent(p.a - p.b, -p.b, p) // 3) for p in primes}
    for chi in itertools.product(range(3), range(2), range(2)):
        assert any(abs(psi[p] - mod4_character(*chi, p.a, p.b)) > 1e-9 for p in primes)


def test_twist_norm_equals_sum_of_twisted_prime_gauss_sums():
    """||C w_u||^2 = sum_pi |S(pi u)|^2, S(c) = sum_{rho != pi} conj((c/rho)_6) g~(rho) (exact), with
    diagonal part sum_pi sum_{rho != pi, rho prime to u} 1 (= D(D-1) for u prime to the index)."""
    from reciprocity_spectra.arith import sextic_gauss_sum

    z6 = cmath.exp(1j * math.pi / 3)
    index, mat = residue_matrix(6, 400)
    g = [sextic_gauss_sum(p) / math.sqrt(p.p) for p in index]
    for c, d in [(2, 0), (-1, -3), (1, 1), (0, 1), (5, 0)]:
        sym = [sextic_residue_exponent(c, d, p) for p in index]
        w = [0j if k is None else g[i].conjugate() * z6 ** k for i, k in enumerate(sym)]
        lhs = sum(abs(sum(z6 ** mat[i][j] * w[j] for j in range(len(index)) if j != i)) ** 2
                  for i in range(len(index)))
        rhs, diag = 0.0, 0
        for i, pi in enumerate(index):
            total = 0j
            for j, rho in enumerate(index):
                if j == i:
                    continue
                k = sextic_residue_exponent(pi.a * c - pi.b * d, pi.a * d + pi.b * c - pi.b * d, rho)  # (pi u / rho)
                if k is not None:
                    total += z6 ** (-k) * g[j]
                    diag += 1
            rhs += abs(total) ** 2
        assert abs(lhs - rhs) < 1e-8 * rhs
        assert diag == sum(1 for i in range(len(index)) for j in range(len(index))
                           if j != i and sym[j] is not None)


def test_sextic_twist_classes_sixth_powers_and_inversion():
    """Exact twist-class identities behind RS-S014.

    (u v^6 / rho)_6 = (u/rho)_6 for rho not dividing v, and 0 if rho | v; (u^5/rho)_6 = conj((u/rho)_6),
    so the "+" twist by u^5 is exactly the conjugate twist by u. The factorization reconstructs u,
    and the sixth-power-free norm and twist class are invariant under u -> -u, conj(u), u v^6.
    """
    from reciprocity_spectra.arith import (
        _mul_w,
        eisenstein_factorization,
        sextic_twist_class,
        sixth_power_free_norm,
    )

    def power(x, k):
        out = (1, 0)
        for _ in range(k):
            out = _mul_w(out, x)
        return out

    primes = primary_eisenstein_primes(1500)
    us = [(2, 0), (-1, -3), (5, 0), (4, 3), (7, 0), (2, 3)]
    vs = [(2, 0), (primes[0].a, primes[0].b), (5, 0)]
    for u in us:
        u5 = power(u, 5)
        for v in vs:
            uv6 = _mul_w(u, power(v, 6))
            for rho in primes:
                k, k5, k6 = (sextic_residue_exponent(*x, rho) for x in (u, u5, uv6))
                divides_v = sextic_residue_exponent(*v, rho) is None
                assert k6 == (None if divides_v or k is None else k)
                assert k5 == (None if k is None else (-k) % 6)
        j, factors = eisenstein_factorization(*u)
        rebuilt = power((1, 1), j)
        for pi, e in factors:
            rebuilt = _mul_w(rebuilt, power(pi, e))
        assert rebuilt == u
        conj = (u[0] - u[1], -u[1])
        for w in [(-u[0], -u[1]), conj, _mul_w(u, power((2, 0), 6))]:
            assert sixth_power_free_norm(*w) == sixth_power_free_norm(*u)
        assert sextic_twist_class(*u5) == sextic_twist_class(*u, sign=-1)
        assert sextic_twist_class(*_mul_w(u, power((2, 0), 6))) == sextic_twist_class(*u)
    assert sixth_power_free_norm(64, 0) == 1 and sixth_power_free_norm(8, 0) == 64
    assert sixth_power_free_norm(128, 0) == 4


def test_sextic_class_exponents_match_direct_symbols():
    """RS-S015: the product of prime symbol vectors equals (u/.)_6 for u = prod pi^e, exactly.

    Covers inert 2 and 5, conjugate split pairs, exponents 1..5 and indexed primes dividing u.
    """
    from reciprocity_spectra.arith import (
        class_element,
        sextic_class_exponents,
        smallest_primary_primes,
    )

    small = smallest_primary_primes(20)
    assert small[:3] == [(2, 0), (-1, -3), (2, 3)] and (5, 0) in small and len(small) == 20
    norms = [a * a - a * b + b * b for a, b in small]
    assert norms == sorted(norms) and max(norms) == 73
    index = primary_eisenstein_primes(400)
    kappas = [[(pi, k)] for pi in small[:8] for k in range(1, 6)]
    kappas += [[(small[i], e1), (small[j], e2)] for i, j in [(0, 1), (1, 2), (2, 4)]
               for e1 in range(1, 6) for e2 in (1, 4, 5)]
    for kappa in kappas:
        u = class_element(kappa)
        direct = [sextic_residue_exponent(*u, rho) for rho in index]
        assert sextic_class_exponents(kappa, index) == direct
        assert any(k is None for k in direct) == any(
            sextic_residue_exponent(*pi, rho) is None for pi, _ in kappa for rho in index)


def test_trace_gauss_sums_twisted_multiplicativity():
    """RS-S019: composite trace-normalized sextic Gauss sums, exactly as used for unrestricted moduli.

    Checks, by brute force over Z[w]/(c): |g(1, c)|^2 = N(c) for squarefree c; twisted multiplicativity
    g(c1 c2) = (c1/c2)(c2/c1) g(c1) g(c2) (split, inert 5 and 11, conjugate pairs, three factors); and the
    prime relation g_trace(sigma) = conj(((2a - b)/sigma)_6) * g_rational(sigma), g_rational = sum_t (t/sigma)_6 e(t/p).
    """
    import cmath
    import math

    from reciprocity_spectra.arith import (
        conjugate_prime,
        trace_gauss_sum,
        twisted_gauss_product,
    )

    primes = primary_eisenstein_primes(80)
    for s in primes[:6]:
        rational = sum(cmath.exp(2j * math.pi * (sextic_residue_exponent(t, 0, s) / 6 + t / s.p))
                       for t in range(1, s.p))
        k = sextic_residue_exponent(2 * s.a - s.b, 0, s)
        assert abs(trace_gauss_sum([s]) - cmath.exp(-2j * math.pi * k / 6) * rational) < 1e-8
    cases = [[primes[0], primes[2]], [primes[1], 5], [primes[0], conjugate_prime(primes[0])],
             [5, 11], [primes[0], primes[3], 5], [primes[2], primes[4]]]
    for factors in cases:
        brute = trace_gauss_sum(factors)
        norm = math.prod(p * p if isinstance(p, int) else p.p for p in factors)
        assert abs(abs(brute) ** 2 - norm) < 1e-6 * norm
        formula = twisted_gauss_product(factors, [trace_gauss_sum([p]) for p in factors])
        assert abs(brute - formula) < 1e-6 * math.sqrt(norm)


def test_trace_normalization_factor_and_unit_twist_by_norm():
    """RS-S020 exact lemmas.

    (1) ((2a - b)/rho)_6 = (-1/rho)_6 (sqrt(-3)/rho)_6 (3/rho)_6 (b'/rho)_6 with b = 3 b', and it equals
        (conj rho / rho)_6, the factor between rational and trace prime Gauss sums.
    (2) (zeta6/sigma)_6 = zeta6^((p - 1)/6) at split primes; multiplicativity makes (zeta6/c)_6 = zeta6^((N(c)-1)/6)
        for squarefree products c of split primes, because (N - 1)/6 is additive mod 6 on N = 1 mod 6.
    (3) at inert q, (zeta6/q)_6 = zeta6^((q^2 - 1)/6).
    """
    from reciprocity_spectra.arith import (
        inert_sextic_exponent,
        trace_normalization_factor,
        unit_twist_exponent_from_norm,
    )

    primes = primary_eisenstein_primes(3000)
    for rho in primes:
        f = trace_normalization_factor(rho)
        assert f['total'] == (f['minus_one'] + f['sqrt_minus_3'] + f['three'] + f['b_prime']) % 6
        assert f['total'] == sextic_residue_exponent(rho.a - rho.b, -rho.b, rho)
        assert sextic_residue_exponent(1, 1, rho) == unit_twist_exponent_from_norm(rho.p)
    for i, s1 in enumerate(primes[:25]):
        for s2 in primes[i + 1:25]:
            k = (sextic_residue_exponent(1, 1, s1) + sextic_residue_exponent(1, 1, s2)) % 6
            assert k == unit_twist_exponent_from_norm(s1.p * s2.p)
    for q in (5, 11, 17, 23):
        assert inert_sextic_exponent(1, 1, q) == ((q * q - 1) // 6) % 6
