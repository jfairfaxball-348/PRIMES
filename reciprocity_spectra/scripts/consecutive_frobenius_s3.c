/*
 * consecutive_frobenius_s3.c -- recorded KILLED candidate (see AREA_TRIAGE.md, item C).
 *
 * Question: do consecutive primes show Lemke Oliver--Soundararajan-type biases in the
 * NON-abelian part of a Frobenius class?  Test field: splitting field of x^3 - 2 (group S3).
 * Classes: T (p = 2 mod 3), I (p = 1 mod 3 and 2 is a cube), C (p = 1 mod 3, 2 not a cube).
 * Prediction (Hardy--Littlewood heuristic): bias only through the abelian quotient (p mod 3);
 * conditional on p = 1 mod 3 the cube bit of the next prime is independent of the previous class.
 * Result to 1e9: abelian same-class fraction 0.4451 (strong bias); non-abelian z-scores within
 * +-1.6 (no bias).  Verdict: null, as predicted -- killed in one session.
 *
 * Build: cc -O2 -o consecutive_frobenius_s3 consecutive_frobenius_s3.c -lm ; run: ./a.out 1000000000
 */
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static uint64_t powmod(uint64_t a, uint64_t e, uint64_t m) {
    uint64_t r = 1; a %= m;
    while (e) { if (e & 1) r = (unsigned __int128)r * a % m; a = (unsigned __int128)a * a % m; e >>= 1; }
    return r;
}

int main(int argc, char **argv) {
    uint64_t N = argc > 1 ? strtoull(argv[1], 0, 10) : 100000000ULL;
    uint64_t r = (uint64_t)sqrt((double)N) + 2, ns = 0, M[3][3] = {{0}}, cnt[3] = {0};
    char *small = calloc(r + 1, 1);
    uint64_t *sp = malloc(sizeof(uint64_t) * (r + 1));
    for (uint64_t i = 2; i <= r; i++) if (!small[i]) { sp[ns++] = i; for (uint64_t j = i * i; j <= r; j += i) small[j] = 1; }
    const uint64_t S = 1 << 22;
    char *seg = malloc(S);
    int prev = -1;
    for (uint64_t L = 5; L < N; L += S) {
        uint64_t H = L + S < N ? L + S : N;
        memset(seg, 0, H - L);
        for (uint64_t k = 0; k < ns && sp[k] * sp[k] < H; k++) {
            uint64_t q = sp[k], st = (L + q - 1) / q * q;
            if (st < q * q) st = q * q;
            for (uint64_t j = st; j < H; j += q) seg[j - L] = 1;
        }
        for (uint64_t p = L; p < H; p++) {
            if (seg[p - L]) continue;
            int c = (p % 3 == 2) ? 0 : (powmod(2, (p - 1) / 3, p) == 1 ? 1 : 2);
            cnt[c]++;
            if (prev >= 0) M[prev][c]++;
            prev = c;
        }
    }
    const char *nm[3] = {"T", "I", "C"};
    double tot = 0, same = M[0][0] + M[1][1] + M[1][2] + M[2][1] + M[2][2];
    for (int i = 0; i < 3; i++) for (int j = 0; j < 3; j++) tot += M[i][j];
    printf("N=%llu counts T=%llu I=%llu C=%llu; abelian same-class fraction %.4f\n", (unsigned long long)N,
           (unsigned long long)cnt[0], (unsigned long long)cnt[1], (unsigned long long)cnt[2], same / tot);
    for (int i = 0; i < 3; i++) {
        double a = M[i][1], b = M[i][2], f = a / (a + b);
        printf("P(next=I | next=1 mod 3, prev=%s) = %.6f (pred 1/3), z = %+.2f\n", nm[i], f,
               (f - 1.0 / 3) / sqrt((2.0 / 9) / (a + b)));
    }
    return 0;
}
