#include <stdint.h>
#include <stddef.h>
#include <string.h>

#define E010_TABLE_SIZE 65536u
#define E010_TABLE_MASK (E010_TABLE_SIZE - 1u)
#define E010_PROFILE_CAP 32768u

static _Thread_local uint64_t denom_keys[E010_TABLE_SIZE];
static _Thread_local uint32_t denom_counts[E010_TABLE_SIZE];
static _Thread_local uint32_t denom_stamps[E010_TABLE_SIZE];
static _Thread_local uint32_t denom_generation = 1u;

static _Thread_local uint64_t state_keys[E010_TABLE_SIZE];
static _Thread_local uint32_t state_stamps[E010_TABLE_SIZE];
static _Thread_local uint32_t state_generation = 1u;

static uint64_t mix64(uint64_t x) {
    x ^= x >> 30;
    x *= UINT64_C(0xbf58476d1ce4e5b9);
    x ^= x >> 27;
    x *= UINT64_C(0x94d049bb133111eb);
    x ^= x >> 31;
    return x;
}

static void next_generations(void) {
    ++denom_generation;
    if (denom_generation == 0u) {
        memset(denom_stamps, 0, sizeof(denom_stamps));
        denom_generation = 1u;
    }
    ++state_generation;
    if (state_generation == 0u) {
        memset(state_stamps, 0, sizeof(state_stamps));
        state_generation = 1u;
    }
}

static int denom_increment(uint64_t key) {
    uint32_t slot = (uint32_t)(mix64(key) & E010_TABLE_MASK);
    for (uint32_t probes = 0; probes < E010_TABLE_SIZE; ++probes) {
        if (denom_stamps[slot] != denom_generation) {
            denom_stamps[slot] = denom_generation;
            denom_keys[slot] = key;
            denom_counts[slot] = 1u;
            return 0;
        }
        if (denom_keys[slot] == key) {
            ++denom_counts[slot];
            return 0;
        }
        slot = (slot + 1u) & E010_TABLE_MASK;
    }
    return 6;
}

static int state_insert(uint64_t m, uint64_t d) {
    uint64_t key = (m << 32) ^ d;
    if (key == 0u) {
        key = UINT64_C(0x9e3779b97f4a7c15);
    }
    uint32_t slot = (uint32_t)(mix64(key) & E010_TABLE_MASK);
    for (uint32_t probes = 0; probes < E010_TABLE_SIZE; ++probes) {
        if (state_stamps[slot] != state_generation) {
            state_stamps[slot] = state_generation;
            state_keys[slot] = key;
            return 0;
        }
        if (state_keys[slot] == key) {
            return 3;
        }
        slot = (slot + 1u) & E010_TABLE_MASK;
    }
    return 6;
}

int e010_cycle_signatures(
    uint64_t x,
    uint64_t a0,
    uint32_t *out_l1,
    uint32_t *out_l2,
    uint32_t *out_l3,
    uint32_t *out_profile,
    uint32_t profile_cap
) {
    if (profile_cap < E010_PROFILE_CAP) {
        return 6;
    }
    if (!(a0 * a0 < x && x < (a0 + 1u) * (a0 + 1u))) {
        return 7;
    }

    next_generations();
    uint64_t m = 0u;
    uint64_t d = 1u;
    uint64_t a = a0;
    uint32_t length = 0u;

    if (state_insert(m, d) != 0) {
        return 6;
    }

    for (;;) {
        uint64_t next_m = d * a - m;
        if (next_m * next_m >= x) {
            return 1;
        }
        uint64_t remainder = x - next_m * next_m;
        if (remainder == 0u || remainder % d != 0u) {
            return 1;
        }
        uint64_t next_d = remainder / d;
        if (next_d == 0u) {
            return 1;
        }
        uint64_t numerator = a0 + next_m;
        uint64_t next_a = numerator / next_d;
        if (!(next_a * next_d <= numerator && numerator < (next_a + 1u) * next_d)) {
            return 2;
        }
        if (denom_increment(next_d) != 0) {
            return 6;
        }
        ++length;
        if (length >= E010_PROFILE_CAP) {
            return 6;
        }

        m = next_m;
        d = next_d;
        a = next_a;
        if (m == a0 && d == 1u && a == 2u * a0) {
            break;
        }
        int state_result = state_insert(m, d);
        if (state_result != 0) {
            return state_result;
        }
    }

    if (length == 0u || d != 1u || m != a0 || a != 2u * a0) {
        return 4;
    }

    uint32_t distinct = 0u;
    uint32_t maximum = 0u;
    for (uint32_t slot = 0; slot < E010_TABLE_SIZE; ++slot) {
        if (denom_stamps[slot] != denom_generation) {
            continue;
        }
        ++distinct;
        if (denom_counts[slot] > maximum) {
            maximum = denom_counts[slot];
        }
    }
    if (maximum == 0u || maximum > profile_cap) {
        return 5;
    }
    memset(out_profile, 0, (size_t)maximum * sizeof(uint32_t));
    for (uint32_t slot = 0; slot < E010_TABLE_SIZE; ++slot) {
        if (denom_stamps[slot] != denom_generation) {
            continue;
        }
        uint32_t count = denom_counts[slot];
        if (count == 0u || count > maximum) {
            return 5;
        }
        ++out_profile[count - 1u];
    }

    uint64_t recovered_length = 0u;
    uint64_t recovered_distinct = 0u;
    for (uint32_t j = 0; j < maximum; ++j) {
        recovered_length += (uint64_t)(j + 1u) * out_profile[j];
        recovered_distinct += out_profile[j];
    }
    if (recovered_length != length || recovered_distinct != distinct || out_profile[maximum - 1u] == 0u) {
        return 5;
    }

    *out_l1 = length;
    *out_l2 = distinct;
    *out_l3 = maximum;
    return 0;
}
