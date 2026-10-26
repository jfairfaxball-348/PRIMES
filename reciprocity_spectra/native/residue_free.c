/*
 * residue_free.c -- matrix-free sextic residue products (RS-S021).
 *
 * Y = R W for R[i][j] = (pi_i/pi_j)_6 (zero diagonal), with the same index order and conventions as
 * residue_engine.c, without storing R: each symbol is Euler's criterion x^((p-1)/6) mod p, matched against
 * the powers of the image of zeta6 = 1 + w (identical to the engine's generator-table exponents).
 * Memory O(D * V); time O(D^2 (log p + V)). Threads own blocks of rows, and each output row accumulates
 * over j in increasing order, so results do not depend on the thread count.
 *
 * Requires p < 2^22 (products of residues stay below 2^44, exact in int64 and in the double estimate).
 * Build (MSVC): cl /O2 /openmp:llvm /std:c11 /LD residue_free.c ; (gcc): cc -O3 -fopenmp -shared -fPIC.
 */
#ifdef _MSC_VER
#define _USE_MATH_DEFINES
#endif
#include <math.h>
#include <omp.h>
#include <stdint.h>
#include <stdlib.h>

#ifdef _MSC_VER
#define RS_EXPORT __declspec(dllexport)
#else
#define RS_EXPORT
#endif

typedef long long ll;

static ll mulmod(ll x, ll y, ll p, double pinv) {
    ll q = (ll)((double)x * (double)y * pinv);
    ll r = x * y - q * p;
    while (r < 0) r += p;
    while (r >= p) r -= p;
    return r;
}

static ll powmod(ll x, ll e, ll p, double pinv) {
    ll r = 1;
    while (e) {
        if (e & 1) r = mulmod(r, x, p, pinv);
        x = mulmod(x, x, p, pinv);
        e >>= 1;
    }
    return r;
}

/* meta: D records (p, a, b); W, Y: D x V complex, row-major, interleaved (re, im). Returns 0, or 1 if p too large. */
RS_EXPORT int rs_free_apply(int D, const int64_t *meta, int V, const double *W, double *Y, int threads) {
    ll *P = malloc(sizeof(ll) * D), *Rw = malloc(sizeof(ll) * D), *E = malloc(sizeof(ll) * D);
    ll *U = malloc(sizeof(ll) * 6 * (size_t)D);
    double *Pinv = malloc(sizeof(double) * D);
    double cr[6], ci[6];
    int bad = 0, j;
    for (int k = 0; k < 6; k++) { cr[k] = cos(M_PI * k / 3); ci[k] = sin(M_PI * k / 3); }
    for (j = 0; j < D; j++) {
        ll p = meta[3 * j], a = meta[3 * j + 1], b = meta[3 * j + 2];
        if (p >= (1LL << 22)) bad = 1;
        double pinv = 1.0 / (double)p;
        ll bm = ((b % p) + p) % p, am = ((a % p) + p) % p;
        ll r = mulmod((p - am) % p, powmod(bm, p - 2, p, pinv), p, pinv); /* w = -a/b mod pi */
        ll unit = (1 + r) % p, u = 1;
        P[j] = p; Rw[j] = r; E[j] = (p - 1) / 6; Pinv[j] = pinv;
        for (int k = 0; k < 6; k++) { U[6 * (size_t)j + k] = u; u = mulmod(u, unit, p, pinv); }
    }
    if (bad) { free(P); free(Rw); free(E); free(U); free(Pinv); return 1; }
    for (size_t t = 0; t < (size_t)D * V * 2; t++) Y[t] = 0;
    omp_set_num_threads(threads);
    int ib;
    #pragma omp parallel for schedule(dynamic, 1)
    for (ib = 0; ib < D; ib += 128) {
        int ie = ib + 128 < D ? ib + 128 : D;
        for (int jj = 0; jj < D; jj++) {
            ll p = P[jj], r = Rw[jj], e = E[jj];
            double pinv = Pinv[jj];
            const ll *u = U + 6 * (size_t)jj;
            const double *w = W + 2 * (size_t)V * jj;
            for (int i = ib; i < ie; i++) {
                if (i == jj) continue;
                ll v = (meta[3 * i + 1] + meta[3 * i + 2] * r) % p;
                if (v < 0) v += p;
                if (v == 0) continue;
                ll t = powmod(v, e, p, pinv);
                int k = 0;
                while (k < 6 && u[k] != t) k++;
                if (k == 6) continue; /* unreachable for valid input */
                double c = cr[k], s = ci[k];
                double *y = Y + 2 * (size_t)V * i;
                for (int q = 0; q < V; q++) {
                    double xr = w[2 * q], xi = w[2 * q + 1];
                    y[2 * q] += c * xr - s * xi;
                    y[2 * q + 1] += c * xi + s * xr;
                }
            }
        }
    }
    free(P); free(Rw); free(E); free(U); free(Pinv);
    return 0;
}
