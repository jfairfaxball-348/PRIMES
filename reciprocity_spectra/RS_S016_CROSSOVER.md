# RS-S016: X-dependence of the sixth-power-class excess (EXPLORATORY)

**Date:** 2026-10-26. **Stage:** discovery and falsification (exploratory; no registration, no CAND).
**Execution:** local Windows; MSVC engine port (validated in RS-S015).

**Machine record:** `results/rs_s016_x_dependence_2026-10-26.json`. Regenerate with
`scripts/phase1l.py run --x X` for X in {1.6·10⁵, 3.2·10⁵, 6.4·10⁵}, then `scripts/phase1l.py analyse`.
The X = 10⁶ values are read from the RS-S015 record.

## 1. Question and decision rule

RS-S015 refuted PROV-RS14 at X = 10⁶, because exponent-3 and exponent-4 classes lose their
enhancement as N grows. The question is whether this is a finite-X effect or a different class law.

The decision rule was committed in `4cf7c60`, before any lower-X run. Its statistic T is the mean s
over the k = 3 singles with N ≥ 37 (10 classes):

- **finite-X:** T increases monotonically and gains at least 0.15 in total;
- **X-stable:** |ΔT| ≤ 0.05;
- **otherwise:** undecided.

The classes are the RS-S015 singles (π^k, k = 1–5, 20 smallest primary primes). The same
construction is used at every X, with 10 + 10 controls per X (seed 16). The random-phase maximum
is 1.0056, 1.0051 and 1.0024 at the three lower X.

## 2. Outcome: finite-X

| X | 1.6·10⁵ | 3.2·10⁵ | 6.4·10⁵ | 10⁶ |
|---|---:|---:|---:|---:|
| r₁ | 1.379 | 1.396 | 1.418 | 1.434 |
| T (k = 3, N ≥ 37) | 0.022 | 0.129 | 0.250 | 0.342 |
| k = 4, N ≥ 31 | −0.174 | −0.106 | −0.078 | −0.071 |
| k = 1, N ≥ 37 | 0.887 | 0.906 | 0.929 | 0.941 |
| k = 2, N ≥ 37 | 0.753 | 0.821 | 0.853 | 0.852 |
| k = 5, N ≥ 37 | −1.034 | −1.020 | −1.070 | −1.043 |

T is monotone and gains 0.32. **Verdict: finite-X.** At every fixed (N, k = 3), s rises with X. For
example, at N = 31 it goes 0.29 → 0.43 → 0.61 → 0.68.

## 3. Collapse in t = N₆/X

Sorting all (class, X) points by log N₆ − a·log X, the scan over a finds the following.

| Pattern | Best a | Roughness at a = 0 | Roughness at best a |
|---|---:|---:|---:|
| exponents 2, 3, 4 pooled | 1.00 | 0.0153 | 0.0055 |
| exponent 3 | 0.9 | 0.024 | 0.0033 |
| exponent 5 | 1.45 | 0.039 | 0.025 (weaker collapse) |

The binned curve at a = 1 is below; the full table is in the JSON.

| log₁₀ t | exponents {2,3,4}: mean s (n) | exponent 5: mean s (n) |
|---:|---:|---:|
| −4.5 | 0.940 (6) | — |
| −3.0 | 0.847 (28) | −0.207 (2) |
| −2.0 | 0.760 (26) | −0.274 (4) |
| −1.5 | 0.561 (20) | −0.448 (2) |
| −1.0 | 0.282 (18) | −0.601 (2) |
| −0.5 | 0.071 (24) | −0.956 (4) |
| 0.0 | −0.066 (18) | −1.130 (6) |
| 1.0 | −0.102 (16) | −1.086 (6) |

**Reading.**

- For exponents in {2, 3, 4}, the excess is approximately a single function F(N₆/X):
  - a plateau of about 0.85 for t ≲ 10⁻², and about 0.94 below 10⁻⁴;
  - a crossover to about 0 near t ≈ 1;
  - slightly negative (about −0.1) for t ≫ 1.
- The exponent-3 and exponent-4 bins agree within about 0.08 wherever both have data.
- Exponent-1 classes stay at t ≤ 10⁻³·³ here, so they never enter the crossover.
- Exponent 5 has the opposite profile. Its law (B), s ≈ −1.05 to −1.1, is the **large-t** regime;
  every N ≥ 19 has t ≥ 2.5 at these X. At small t, the excess is weakly negative: π = 2 (N = 4,
  t ≈ 10⁻³) sits at −0.17 to −0.21 at every X, and π₇⁵ rises from −0.62 to −0.24 as X grows.

**Consequences for RS-S015.**

- The P1 and P3 failures are crossover effects: the class list put exponent-3 and exponent-4
  classes at t between 10⁻¹ and 10².
- RS-S015-P2's (B) is real, but as written it is a statement about t ≫ 1. It is not a fixed-class
  limit.

## 4. Provisional statement PROV-RS16 (not a CAND; not frozen)

**Definitions.** As in PROV-RS14:

- s_κ(X) = ε_κ(X)·N₆(κ)^{1/6};
- ε_κ = (r_κ² − 1)/(r₁² − 1);
- t = N₆(κ)/X.

**(A″) Crossover law, no exponent 5.** If every exponent of κ lies in {1, …, 4}, then
s_κ(X) = F(N₆(κ)/X) + o(1). Here F is a single decreasing function, independent of the exponent
pattern, with:

- F(0⁺) = c ∈ [0.80, 1.00];
- F(t) ≈ 0 near t ≈ 1;
- F(t) ≤ 0 for t ≫ 1.

**Fixed-class corollary.** For fixed κ, lim s_κ = c > 0, so κ is enhanced.

**(B″) Exponent 5.** If κ = π⁵, then:

- s_κ ≈ −1.05 to −1.1 for t ≫ 1;
- |s_κ| decreases as t → 0. Whether the fixed-class limit is about −0.2 (as at π = 2) or 0 is open.

In all cases lim sup r ≤ 1.

**Consequence for the dichotomy.** (D) is restored as a fixed-class statement: classes without
exponent 5 are enhanced in the limit, and classes with exponent 5 are not. At any finite X, only
classes with N₆ ≪ X show it.

**Status of the evidence.** This is fitted on the same 400 (class, X) points that suggested it. It
is a hypothesis, not a confirmed law. The value of c is uncertain because the plateau sits at
0.85 for 10⁻³·⁵ ≤ t ≤ 10⁻² but at about 0.94 below 10⁻⁴, and only small N reaches the latter.

**Mechanism hypothesis (not derived).**

- (π/·)₆^k = (π^k/·)₆, and its conductor is set by π. The collapse in N₆/X, rather than N/X,
  points to the theta-coefficient size at the sixth-power-free part N₆ as the relevant length. This
  is the Patterson-type main term ∝ τ(u)·X^{5/6}, which dominates only when the twisted series is
  long compared with N₆.
- π⁵ and π⁴ are the conjugate twists of π and π². Their large-t values (−1.1 and −0.1) differ, so
  conjugation alone does not set the sign.

These are analogies to evaluate against Patterson and Bröker–Hoffstein, not derivations.

## 5. Falsification plan, for a later registered session

**Design.** Use fresh classes (primes not in the RS-S015 list) at X = 10⁶ and 6.4·10⁵. Both scales
are feasible locally. X = 1.28·10⁶ has D = 98512, a 9.7 GB matrix, which exceeds what this 15.7 GB
machine can hold safely, so it is optional and depends on memory.

- Freeze F as the {2,3,4} bin table above (JSON `collapse_bins_t_eq_N6_over_X.k234`), with linear
  interpolation in log₁₀ t.
- Fresh singles: k = 2, 3 and 4 over the primary primes with 79 ≤ N ≤ about 400. These give t
  from about 10⁻² to 10³.
- Fresh pairs: mixed patterns built from those primes.
- Fresh k = 5 classes across t ∈ [10⁻², 10³], using the small-norm primes where needed.
- Controls: 10 + 10 per X, seeded.

**Power.** The control sd in r is about 0.002 (at X ≥ 6.4·10⁵), so σ_ε ≈ 0.004 and
σ_s ≈ 0.004·N₆^{1/6}. That is below 0.05 for N₆^{1/6} ≤ 12. Classes with larger N₆^{1/6} are
group-averaged only.

**Draft criteria (to register verbatim before data).**

- **Q1:** every fresh no-5 class with t ≤ 10⁻² has s ∈ [0.70, 1.00].
- **Q2:** for every half-decade bin with at least 4 fresh no-5 classes, the mean s is within 0.12
  of frozen F.
- **Q3:** every fresh class containing a 5 has r < 1, and the fresh π⁵ classes with t ≥ 3 have
  mean s ∈ [−1.25, −0.85].
- **Q4 (direction of the limit):** at 6.4·10⁵ versus 10⁶, at least 80% of fresh no-5 classes with
  10⁻¹·⁵ ≤ t ≤ 10 have larger s at the larger X.

Failure of Q1, Q2 or Q4 refutes (A″) as stated. Failure of Q3 refutes (B″). Only if Q1–Q4 pass
would a replacement candidate be considered. That candidate would cover the fixed-class dichotomy
with crossover, together with CAND-001 statement 2, after the prior-art audit agreed for that
branch.

## 6. Outcome (RS-S017, registered)

Q1, Q2 and Q4 PASS on 440 fresh classes, so (A″) is STRESSED. Q3 FAILS on its per-class r < 1
clause; that clause was underpowered at large N₆. Its mean clause passes. See the RS-S017 entries
in `LEDGER.md` and `CONJECTURES.md`.
