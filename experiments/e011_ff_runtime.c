#include <stdint.h>
#include <stddef.h>

#define MAX_DEG 10

typedef struct {
    uint64_t c[MAX_DEG + 1];
    int deg;
} poly_t;

static uint64_t addm(uint64_t a, uint64_t b, uint64_t p) {
    uint64_t x = a + b;
    return x >= p ? x - p : x;
}

static uint64_t subm(uint64_t a, uint64_t b, uint64_t p) {
    return a >= b ? a - b : p - (b - a);
}

static uint64_t mulm(uint64_t a, uint64_t b, uint64_t p) {
    return (uint64_t)((__uint128_t)a * (__uint128_t)b % p);
}

static uint64_t powm(uint64_t a, uint64_t e, uint64_t p) {
    uint64_t r = 1 % p;
    uint64_t x = a % p;
    while (e) {
        if (e & 1) r = mulm(r, x, p);
        e >>= 1;
        if (e) x = mulm(x, x, p);
    }
    return r;
}

static void norm(poly_t *a, uint64_t p) {
    for (int i = 0; i <= MAX_DEG; ++i) a->c[i] %= p;
    while (a->deg >= 0 && a->c[a->deg] == 0) a->deg--;
}

static poly_t poly_zero(void) {
    poly_t r = {{0}, -1};
    return r;
}

static poly_t poly_f(uint64_t p) {
    poly_t r = poly_zero();
    r.deg = 5;
    r.c[0] = 1 % p;
    r.c[1] = 1 % p;
    r.c[5] = 1 % p;
    return r;
}

static poly_t poly_x(void) {
    poly_t r = poly_zero();
    r.deg = 1;
    r.c[1] = 1;
    return r;
}

static poly_t poly_sub(poly_t a, poly_t b, uint64_t p) {
    poly_t r = poly_zero();
    int d = a.deg > b.deg ? a.deg : b.deg;
    r.deg = d;
    for (int i = 0; i <= d; ++i) {
        uint64_t av = i <= a.deg ? a.c[i] : 0;
        uint64_t bv = i <= b.deg ? b.c[i] : 0;
        r.c[i] = subm(av, bv, p);
    }
    norm(&r, p);
    return r;
}

static poly_t poly_divrem(poly_t num, poly_t den, uint64_t p, poly_t *quot) {
    poly_t q = poly_zero();
    if (den.deg < 0) return num;
    norm(&num, p);
    norm(&den, p);
    if (num.deg >= den.deg) q.deg = num.deg - den.deg;
    uint64_t inv = powm(den.c[den.deg], p - 2, p);
    while (num.deg >= den.deg && num.deg >= 0) {
        int shift = num.deg - den.deg;
        uint64_t coeff = mulm(num.c[num.deg], inv, p);
        q.c[shift] = coeff;
        for (int i = 0; i <= den.deg; ++i) {
            num.c[shift + i] = subm(num.c[shift + i], mulm(coeff, den.c[i], p), p);
        }
        norm(&num, p);
    }
    norm(&q, p);
    if (quot) *quot = q;
    return num;
}

static poly_t poly_monic(poly_t a, uint64_t p) {
    norm(&a, p);
    if (a.deg < 0) return a;
    uint64_t inv = powm(a.c[a.deg], p - 2, p);
    for (int i = 0; i <= a.deg; ++i) a.c[i] = mulm(a.c[i], inv, p);
    norm(&a, p);
    return a;
}

static poly_t poly_gcd(poly_t a, poly_t b, uint64_t p) {
    norm(&a, p);
    norm(&b, p);
    while (b.deg >= 0) {
        poly_t r = poly_divrem(a, b, p, NULL);
        a = b;
        b = r;
    }
    return poly_monic(a, p);
}

/* Multiply degree<5 polynomials modulo F=x^5+x+1. */
static poly_t mul_mod_f(poly_t a, poly_t b, uint64_t p) {
    uint64_t tmp[9] = {0};
    for (int i = 0; i <= a.deg; ++i) {
        for (int j = 0; j <= b.deg; ++j) {
            uint64_t term = mulm(a.c[i], b.c[j], p);
            tmp[i + j] = addm(tmp[i + j], term, p);
        }
    }
    for (int d = 8; d >= 5; --d) {
        uint64_t coeff = tmp[d] % p;
        if (!coeff) continue;
        tmp[d] = 0;
        tmp[d - 5] = subm(tmp[d - 5], coeff, p);
        tmp[d - 4] = subm(tmp[d - 4], coeff, p);
    }
    poly_t r = poly_zero();
    r.deg = 4;
    for (int i = 0; i < 5; ++i) r.c[i] = tmp[i] % p;
    norm(&r, p);
    return r;
}

static poly_t pow_mod_f(poly_t base, uint64_t exponent, uint64_t p) {
    poly_t r = poly_zero();
    r.deg = 0;
    r.c[0] = 1 % p;
    poly_t x = base;
    while (exponent) {
        if (exponent & 1) r = mul_mod_f(r, x, p);
        exponent >>= 1;
        if (exponent) x = mul_mod_f(x, x, p);
    }
    return r;
}

int e011_factor_counts(uint64_t p, uint32_t *out_counts) {
    if (p < 2 || out_counts == NULL) return 9;
    poly_t f = poly_f(p);
    poly_t deriv = poly_zero();
    deriv.deg = 4;
    deriv.c[0] = 1 % p;
    deriv.c[4] = 5 % p;
    poly_t squarefree = poly_gcd(f, deriv, p);
    if (!(squarefree.deg == 0 && squarefree.c[0] == 1)) return 1;

    poly_t x = poly_x();
    poly_t r = x;
    int s[5] = {0};
    for (int k = 0; k < 5; ++k) {
        r = pow_mod_f(r, p, p);
        poly_t diff = poly_sub(r, x, p);
        poly_t g = poly_gcd(f, diff, p);
        if (g.deg < 0 || g.deg > 5) return 2;
        s[k] = g.deg;
    }

    int c[5] = {0};
    int n1 = s[0];
    if (n1 < 0) return 3;
    c[0] = n1;
    int n2 = s[1] - c[0];
    if (n2 < 0 || n2 % 2 != 0) return 3;
    c[1] = n2 / 2;
    int n3 = s[2] - c[0];
    if (n3 < 0 || n3 % 3 != 0) return 3;
    c[2] = n3 / 3;
    int n4 = s[3] - c[0] - 2 * c[1];
    if (n4 < 0 || n4 % 4 != 0) return 3;
    c[3] = n4 / 4;
    int n5 = s[4] - c[0];
    if (n5 < 0 || n5 % 5 != 0) return 3;
    c[4] = n5 / 5;
    int rec[5] = {
        c[0],
        c[0] + 2 * c[1],
        c[0] + 3 * c[2],
        c[0] + 2 * c[1] + 4 * c[3],
        c[0] + 5 * c[4],
    };
    for (int i = 0; i < 5; ++i) if (rec[i] != s[i]) return 4;
    int total = c[0] + 2*c[1] + 3*c[2] + 4*c[3] + 5*c[4];
    if (total != 5) return 5;
    for (int i = 0; i < 5; ++i) out_counts[i] = (uint32_t)c[i];
    return 0;
}
