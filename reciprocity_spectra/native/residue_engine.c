/*
 * residue_engine.c -- OpenMP byte engine, based on residue_matrix.c; build power-residue-symbol matrices of degree-one primes.
 *
 *   ./residue_matrix quad|cubic|quartic|sextic X matrix.bin [gauss.bin]
 *
 * quad    : odd rational primes p <= X;            E[i][j] = 0 if (p_i/p_j) = +1, 1 if -1.
 * cubic   : primary pi = a + b w in Z[w], N(pi) <= X; E[i][j] = k with (pi_i/pi_j)_3 = w^k.
 * quartic : primary pi = a + b i in Z[i], N(pi) <= X; E[i][j] = k with (pi_i/pi_j)_4 = i^k.
 * sextic  : same Eisenstein indices; zeta6 = 1+w, exponents of exp(pi*i/3).
 * Diagonal (and any zero symbol) is stored as 255.  Conventions match reciprocity_spectra/arith.py.
 *
 * matrix.bin : int32 D, then D records of int64 (p, a, b), then D*D uint8 row-major E[i][j].
 * gauss.bin  : D complex doubles g(pi)/sqrt(p), g(pi) = sum_{t=1}^{p-1} (t/pi)_n e(t/p).
 *
 * Build: cc -O2 -o residue_matrix residue_matrix.c -lm
 */
#include <math.h>
#include <complex.h>
#include <omp.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef long long ll;
typedef struct { ll p, a, b, r; } prime_t; /* r = image of the root of unity in F_p */

static ll mod(ll a, ll m) { a %= m; return a < 0 ? a + m : a; }
static ll pw(ll a, ll e, ll m) {
    ll r = 1; a = mod(a, m);
    while (e) { if (e & 1) r = (__int128)r * a % m; a = (__int128)a * a % m; e >>= 1; }
    return r;
}
static ll inv(ll a, ll m) { return pw(a, m - 2, m); }

static char *sieve(ll n) {
    char *c = calloc(n + 1, 1); /* c[k] = 1 if composite */
    c[0] = c[1] = 1;
    for (ll i = 2; i * i <= n; i++) if (!c[i]) for (ll j = i * i; j <= n; j += i) c[j] = 1;
    return c;
}

static int add_primary(prime_t *P, int D, int first, ll p, ll a, ll b) {
    for (int k = first; k < D; k++) if (P[k].a == a && P[k].b == b) return D;
    P[D].p = p; P[D].a = a; P[D].b = b; P[D].r = mod(-a * inv(mod(b, p), p), p);
    return D + 1;
}

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: %s quad|cubic|quartic|sextic X matrix.bin [gauss.bin]\n", argv[0]); return 1; }
    int n = !strcmp(argv[1], "sextic") ? 6 : !strcmp(argv[1], "cubic") ? 3 : !strcmp(argv[1], "quartic") ? 4 : !strcmp(argv[1], "quad") ? 2 : 0;
    if (!n) { fprintf(stderr, "unknown mode %s\n", argv[1]); return 1; }
    ll X = atoll(argv[2]);
    char *comp = sieve(X);
    prime_t *P = malloc(sizeof(prime_t) * (X + 2));
    int D = 0;
    for (ll p = 3; p <= X; p++) {
        if (comp[p]) continue;
        if (n == 2) { P[D].p = p; P[D].a = p; P[D].b = 0; P[D].r = 0; D++; continue; }
        if (p % n != 1) continue;
        int first = D;
        ll bmax = (ll)sqrt((double)(4 * p)) + 2;
        for (ll b = -bmax; b <= bmax; b++) {
            if (n == 3 || n == 6) {
                if (mod(b, 3)) continue;
                ll disc = 4 * p - 3 * b * b; if (disc < 0) continue;
                ll s = llround(sqrt((double)disc)); if (s * s != disc) continue;
                for (int sg = -1; sg <= 1; sg += 2) {
                    ll t = b + sg * s; if (t % 2) continue;
                    ll a = t / 2;
                    if (mod(a, 3) == 2 && a * a - a * b + b * b == p) D = add_primary(P, D, first, p, a, b);
                }
            } else {
                if (mod(b, 2)) continue;
                ll disc = p - b * b; if (disc < 0) continue;
                ll s = llround(sqrt((double)disc)); if (s * s != disc) continue;
                for (int sg = -1; sg <= 1; sg += 2) if (mod(sg * s + b, 4) == 1) D = add_primary(P, D, first, p, sg * s, b);
            }
        }
        if (D - first != 2) { fprintf(stderr, "p=%lld: found %d primary primes\n", p, D - first); return 2; }
    }
    fprintf(stderr, "mode=%s X=%lld D=%d\n", argv[1], X, D);

    omp_set_num_threads(4);
    /* RS_NO_MATRIX: write header and index metadata only (Gauss sums at scales beyond the matrix). */
    int nomatrix = getenv("RS_NO_MATRIX") != NULL;
    uint8_t *E = nomatrix ? NULL : malloc((size_t)D * D);
    if (!nomatrix && !E) { fprintf(stderr, "matrix allocation failed\n"); return 3; }
    #pragma omp parallel for schedule(dynamic, 1)
    for (int j = 0; j < (nomatrix ? 0 : D); j++) {
        ll p = P[j].p, r = P[j].r, e = (p - 1) / n;
        ll unit = n == 6 ? mod(1 + r, p) : r;
        /* Build the character table in O(p), rather than D modular powers. */
        ll gen = 2;
        for (;; gen++) {
            ll m = p - 1; int ok = 1;
            for (ll q = 2; q * q <= m; q++) if (m % q == 0) {
                if (pw(gen, (p - 1) / q, p) == 1) ok = 0;
                while (m % q == 0) m /= q;
            }
            if (m > 1 && pw(gen, (p - 1) / m, p) == 1) ok = 0;
            if (ok) break;
        }
        int kg = 1;
        if (n > 2) {
            ll ge = pw(gen, e, p), rr = 1;
            for (int k = 0; k < n; k++) {
                if (rr == ge) { kg = k; break; }
                rr = rr * unit % p;
            }
        }
        uint8_t *table = malloc(p);
        if (!table) abort();
        table[0] = 255;
        ll t = 1;
        for (ll k = 0; k < p - 1; k++) {
            table[t] = (k * kg) % n;
            t = t * gen % p;
        }
        for (int i = 0; i < D; i++) {
            ll v = n == 2 ? P[i].p % p : mod(P[i].a + P[i].b * r, p);
            E[(size_t)i * D + j] = i == j ? 255 : table[v];
        }
        free(table);
    }
    FILE *f = fopen(argv[3], "wb");
    int32_t D32 = D; fwrite(&D32, 4, 1, f);
    for (int i = 0; i < D; i++) { int64_t rec[3] = {P[i].p, P[i].a, P[i].b}; fwrite(rec, 8, 3, f); }
    if (!nomatrix) fwrite(E, 1, (size_t)D * D, f);
    fclose(f);

    if (argc > 4) {
        FILE *g = fopen(argv[4], "wb");
        double *G = malloc((size_t)D * 2 * sizeof(double));
        if (!G) abort();
        #pragma omp parallel for schedule(dynamic, 1)
        for (int j = 0; j < D; j++) {
            ll p = P[j].p, r = P[j].r, e = (p - 1) / n, gen = 2;
            ll unit = n == 6 ? mod(1 + r, p) : r;
            for (;; gen++) { /* primitive root mod p */
                ll m = p - 1, ok = 1;
                for (ll q = 2; q * q <= m; q++) if (m % q == 0) { if (pw(gen, (p - 1) / q, p) == 1) ok = 0; while (m % q == 0) m /= q; }
                if (m > 1 && pw(gen, (p - 1) / m, p) == 1) ok = 0;
                if (ok) break;
            }
            int kg = 1; /* chi(gen) = zeta_n^kg */
            if (n > 2) { ll ge = pw(gen, e, p), rr = 1; for (int k = 0; k < n; k++) { if (rr == ge) { kg = k; break; } rr = (__int128)rr * unit % p; } }
            double re = 0, im = 0; ll x = 1;
            for (ll s = 0; s < p - 1; s++) {
                double ang = 2 * M_PI * ((double)((s * kg) % n) / n + (double)x / p);
                re += cos(ang); im += sin(ang);
                x = (__int128)x * gen % p;
            }
            double v[2] = {re / sqrt((double)p), im / sqrt((double)p)};
            G[2*j] = v[0]; G[2*j+1] = v[1];
        }
        fwrite(G, sizeof(double), (size_t)D * 2, g);
        free(G);
        fclose(g);
    }
    free(E); free(P); free(comp);
    return 0;
}

/* ctypes ABI: interleaved complex128 vectors; no dense floating matrix.
 * 64-row blocks, 256-column blocks; adjoint uses transposed byte accesses.
 * Each output row belongs to one thread, so reductions are deterministic.
 */
void rs_apply(const uint8_t *E, int D, int n, const double complex *x,
              double complex *y, int adjoint) {
    double complex roots[256] = {0};
    for (int k = 0; k < n; k++) roots[k] = cexp(2 * M_PI * I * k / n);
    omp_set_num_threads(4);
    #pragma omp parallel for schedule(static)
    for (int ib = 0; ib < D; ib += 64) {
        int end = ib + 64 < D ? ib + 64 : D;
        for (int i = ib; i < end; i++) y[i] = 0;
        for (int jb = 0; jb < D; jb += 256) {
            int je = jb + 256 < D ? jb + 256 : D;
            if (!adjoint) {
                for (int i = ib; i < end; i++) {
                    double complex sum = 0;
                    const uint8_t *row = E + (size_t)i * D;
                    for (int j = jb; j < je; j++) sum += roots[row[j]] * x[j];
                    y[i] += sum;
                }
            } else {
                for (int j = jb; j < je; j++) {
                    const uint8_t *row = E + (size_t)j * D;
                    for (int i = ib; i < end; i++) y[i] += conj(roots[row[i]]) * x[j];
                }
            }
        }
    }
}

/* Counter-based SplitMix64: each independent upper pair has a fixed draw.
 * Rejection removes modulo bias (notably n=3). Same signs as structured_random.
 * The seed-0 stream is specified here, distinct from numpy's PCG64 stream.
 */
static uint64_t mix64(uint64_t x) {
    x = (x ^ (x >> 30)) * UINT64_C(0xbf58476d1ce4e5b9);
    x = (x ^ (x >> 27)) * UINT64_C(0x94d049bb133111eb);
    return x ^ (x >> 31);
}
void rs_random(uint8_t *E, int D, int n, const int64_t *primes, uint64_t seed) {
    if (n == 6) abort(); /* Sextic controls require the full pairwise mask API below. */
    omp_set_num_threads(4);
    #pragma omp parallel for schedule(static)
    for (int i = 0; i < D; i++) {
        E[(size_t)i * D + i] = 255;
        for (int j = i+1; j < D; j++) {
            uint64_t state = seed + (uint64_t)i * D + j;
            uint64_t u;
            do { state += UINT64_C(0x9e3779b97f4a7c15); u = mix64(state); }
            while (u < (uint64_t)(-((uint64_t)n)) % n);
            int k = u % n;
            int neg = n == 2 ? (primes[i]%4 == 3 && primes[j]%4 == 3)
                    : n == 4 && primes[i]%8 == 5 && primes[j]%8 == 5;
            E[(size_t)i * D + j] = k;
            E[(size_t)j * D + i] = (k + (neg ? n/2 : 0)) % n;
        }
    }
}

/* Reciprocity-aware adjoint: C_ji = sign_ij C_ij, sign=-1 only
 * when both metadata parity bits are set. This keeps byte reads contiguous.
 * The generic transpose kernel above remains available for independent checks.
 */
void rs_apply_sym(const uint8_t *E, int D, int n, const uint8_t *odd,
                  const double complex *x, double complex *y, int adjoint) {
    if (!adjoint) { rs_apply(E, D, n, x, y, 0); return; }
    double complex roots[256] = {0};
    for (int k = 0; k < n; k++) roots[k] = conj(cexp(2 * M_PI * I * k / n));
    omp_set_num_threads(4);
    #pragma omp parallel for schedule(static)
    for (int ib = 0; ib < D; ib += 64) {
        int end = ib + 64 < D ? ib + 64 : D;
        for (int i = ib; i < end; i++) {
            double complex sum = 0;
            const uint8_t *row = E + (size_t)i * D;
            for (int jb = 0; jb < D; jb += 256) {
                int je = jb + 256 < D ? jb + 256 : D;
                double complex part = 0;
                if (odd[i]) {
                    for (int j = jb; j < je; j++)
                        part += (odd[j] ? -roots[row[j]] : roots[row[j]]) * x[j];
                } else {
                    for (int j = jb; j < je; j++) part += roots[row[j]] * x[j];
                }
                sum += part;
            }
            y[i] = sum;
        }
    }
}

/* Extract the full exact +/- reciprocity mask from exponents. Returns the
 * number of invalid pairs (nonzero/half-turn phase, or off-diagonal zero).
 * For sextic characters, cubic reciprocity makes this ratio a sign.
 */
uint64_t rs_pair_signs(const uint8_t *E, uint8_t *S, int D, int n) {
    uint64_t errors = 0;
    omp_set_num_threads(4);
    #pragma omp parallel for schedule(static) reduction(+:errors)
    for (int ib = 0; ib < D; ib += 64) {
        int ie = ib + 64 < D ? ib + 64 : D;
        for (int jb = 0; jb < D; jb += 256) {
            int je = jb + 256 < D ? jb + 256 : D;
            for (int i = ib; i < ie; i++) for (int j = jb; j < je; j++) {
                size_t ij = (size_t)i * D + j, ji = (size_t)j * D + i;
                if (i == j) { S[ij] = 0; continue; }
                int a = E[ij], b = E[ji];
                int shift = (b + n - a) % n;
                if (a >= n || b >= n || (shift != 0 && shift != n/2)) errors++;
                S[ij] = shift == n/2;
            }
        }
    }
    return errors;
}

void rs_random_signed(uint8_t *E, const uint8_t *S, int D, int n, uint64_t seed) {
    omp_set_num_threads(4);
    #pragma omp parallel for schedule(static)
    for (int i = 0; i < D; i++) {
        E[(size_t)i * D + i] = 255;
        for (int j = i+1; j < D; j++) {
            uint64_t state = seed + (uint64_t)i * D + j, u;
            do { state += UINT64_C(0x9e3779b97f4a7c15); u = mix64(state); }
            while (u < (uint64_t)(-((uint64_t)n)) % n);
            int k = u % n;
            E[(size_t)i * D + j] = k;
            E[(size_t)j * D + i] = (k + S[(size_t)i * D + j] * (n/2)) % n;
        }
    }
}

/* Contiguous adjoint with a full pairwise sign mask, rather than odd[i]*odd[j]. */
void rs_apply_signed(const uint8_t *E, const uint8_t *S, int D, int n,
                     const double complex *x, double complex *y, int adjoint) {
    if (!adjoint) { rs_apply(E, D, n, x, y, 0); return; }
    double complex roots[256] = {0};
    for (int k = 0; k < n; k++) roots[k] = conj(cexp(2 * M_PI * I * k / n));
    omp_set_num_threads(4);
    #pragma omp parallel for schedule(static)
    for (int ib = 0; ib < D; ib += 64) {
        int ie = ib + 64 < D ? ib + 64 : D;
        for (int i = ib; i < ie; i++) {
            double complex sum = 0;
            const uint8_t *row = E + (size_t)i * D, *signs = S + (size_t)i * D;
            for (int jb = 0; jb < D; jb += 256) {
                int je = jb + 256 < D ? jb + 256 : D;
                double complex part = 0;
                for (int j = jb; j < je; j++)
                    part += (signs[j] ? -roots[row[j]] : roots[row[j]]) * x[j];
                sum += part;
            }
            y[i] = sum;
        }
    }
}

/* RS-S004 control: draws are constant on the orbits of the exact identities
 * E[j][i] = E[i][j] + S[i][j]*(n/2) (reciprocity) and E[c[i]][c[j]] = -E[i][j]
 * (complex conjugation, c = conjugate-prime index). The draw for an orbit uses
 * the rs_random counter of its smallest ordered representative (a < b). The
 * pair (i, c[i]) is fixed by both identities; its exponent is copied from
 * forced[i]. Each row is written by one thread, so the result is deterministic.
 * Returns the number of rows whose mask is not conjugation-invariant.
 */
uint64_t rs_random_conj(uint8_t *E, const uint8_t *S, const int32_t *c,
                        const uint8_t *forced, int D, int n, uint64_t seed) {
    uint64_t errors = 0;
    int h = n / 2;
    omp_set_num_threads(4);
    #pragma omp parallel for schedule(static) reduction(+:errors)
    for (int i = 0; i < D; i++) {
        E[(size_t)i * D + i] = 255;
        int ci = c[i];
        for (int j = 0; j < D; j++) {
            if (j == i) continue;
            if (j == ci) { E[(size_t)i * D + j] = forced[i]; continue; }
            int cj = c[j];
            if (S[(size_t)i * D + j] != S[(size_t)ci * D + cj]) errors++;
            int a = i < j ? i : j, b = i < j ? j : i;
            int a2 = ci < cj ? ci : cj, b2 = ci < cj ? cj : ci;
            int conjugated = a2 < a || (a2 == a && b2 < b);
            if (conjugated) { a = a2; b = b2; }
            uint64_t state = seed + (uint64_t)a * D + b, u;
            do { state += UINT64_C(0x9e3779b97f4a7c15); u = mix64(state); }
            while (u < (uint64_t)(-((uint64_t)n)) % n);
            int k = u % n;                       /* exponent at (a, b) */
            int ri = conjugated ? ci : i;
            if (ri != a) k = (k + S[(size_t)a * D + b] * h) % n;  /* transpose */
            if (conjugated) k = (n - k) % n;
            E[(size_t)i * D + j] = k;
        }
    }
    return errors;
}
