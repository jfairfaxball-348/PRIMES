/*
 * residue_matrix.c -- build power-residue-symbol matrices of degree-one primes.
 *
 *   ./residue_matrix quad|cubic|quartic X matrix.bin [gauss.bin]
 *
 * quad    : odd rational primes p <= X;            E[i][j] = 0 if (p_i/p_j) = +1, 1 if -1.
 * cubic   : primary pi = a + b w in Z[w], N(pi) <= X; E[i][j] = k with (pi_i/pi_j)_3 = w^k.
 * quartic : primary pi = a + b i in Z[i], N(pi) <= X; E[i][j] = k with (pi_i/pi_j)_4 = i^k.
 * Diagonal (and any zero symbol) is stored as 255.  Conventions match reciprocity_spectra/arith.py.
 *
 * matrix.bin : int32 D, then D records of int64 (p, a, b), then D*D uint8 row-major E[i][j].
 * gauss.bin  : D complex doubles g(pi)/sqrt(p), g(pi) = sum_{t=1}^{p-1} (t/pi)_n e(t/p).
 *
 * Build: cc -O2 -o residue_matrix residue_matrix.c -lm
 */
#include <math.h>
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
    if (argc < 4) { fprintf(stderr, "usage: %s quad|cubic|quartic X matrix.bin [gauss.bin]\n", argv[0]); return 1; }
    int n = !strcmp(argv[1], "cubic") ? 3 : !strcmp(argv[1], "quartic") ? 4 : !strcmp(argv[1], "quad") ? 2 : 0;
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
            if (n == 3) {
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

    uint8_t *E = malloc((size_t)D * D);
    for (int j = 0; j < D; j++) {
        ll p = P[j].p, r = P[j].r, e = (p - 1) / n, rp[4] = {1, 1, 1, 1};
        for (int k = 1; k < n; k++) rp[k] = (__int128)rp[k - 1] * r % p;
        for (int i = 0; i < D; i++) {
            uint8_t code = 255;
            if (i != j) {
                ll t = (n == 2) ? pw(P[i].p, e, p) : pw(mod(P[i].a + P[i].b * r, p), e, p);
                if (n == 2) code = (t == 1) ? 0 : 1;
                else if (t) for (int k = 0; k < n; k++) if (t == rp[k]) { code = (uint8_t)k; break; }
            }
            E[(size_t)i * D + j] = code;
        }
    }
    FILE *f = fopen(argv[3], "wb");
    int32_t D32 = D; fwrite(&D32, 4, 1, f);
    for (int i = 0; i < D; i++) { int64_t rec[3] = {P[i].p, P[i].a, P[i].b}; fwrite(rec, 8, 3, f); }
    fwrite(E, 1, (size_t)D * D, f);
    fclose(f);

    if (argc > 4) {
        FILE *g = fopen(argv[4], "wb");
        for (int j = 0; j < D; j++) {
            ll p = P[j].p, r = P[j].r, e = (p - 1) / n, gen = 2;
            for (;; gen++) { /* primitive root mod p */
                ll m = p - 1, ok = 1;
                for (ll q = 2; q * q <= m; q++) if (m % q == 0) { if (pw(gen, (p - 1) / q, p) == 1) ok = 0; while (m % q == 0) m /= q; }
                if (m > 1 && pw(gen, (p - 1) / m, p) == 1) ok = 0;
                if (ok) break;
            }
            int kg = 1; /* chi(gen) = zeta_n^kg */
            if (n > 2) { ll ge = pw(gen, e, p), rr = 1; for (int k = 0; k < n; k++) { if (rr == ge) { kg = k; break; } rr = (__int128)rr * r % p; } }
            double re = 0, im = 0; ll x = 1;
            for (ll s = 0; s < p - 1; s++) {
                double ang = 2 * M_PI * ((double)((s * kg) % n) / n + (double)x / p);
                re += cos(ang); im += sin(ang);
                x = (__int128)x * gen % p;
            }
            double v[2] = {re / sqrt((double)p), im / sqrt((double)p)};
            fwrite(v, 8, 2, g);
        }
        fclose(g);
    }
    return 0;
}
