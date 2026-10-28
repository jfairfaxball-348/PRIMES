# RS-S042 numerical and figure-source audit (2026-10-28)

**Status:** Source-key audit of committed data at the RS-S041 merged baseline `309654671e536fc97e20d2cfef4d643d463e7026` (parent of main `0d81d79271d62771fcf956ef3dcb9656ad294691`). No new computations were performed. Plotting script: `paper/figures/make_all.py`. All source paths below begin `reciprocity_spectra/results/`. Data records have embedded `prediction_commit`, `runs[].code_commit`, commands, seeds and validation data where applicable. Figure PDF and PNG files are *derived display products*, not primary evidence.

## Figure-by-figure provenance

| File stem (vector PDF and PNG) | JSON file(s) | Exact JSON keys / interpretation | In manuscript? |
|---|---|---|---|
| `visual_abstract` | none (paper definitions; register CAND-002) | conceptual diagram; no numeric input | no: box-heavy redundancy |
| `crossover` | `rs_s016_x_dependence_2026-10-26.json`, `rs_s015_class_tests_2026-10-26.json`, `rs_s021_large_x_2026-10-26.json` | `runs[].{X,classes[].{k,exponents,N6,s,r}}`; S016 `analysis.r_u1`, `analysis.collapse_bins_t_eq_N6_over_X.k234[].{log10_t_lo,mean_s}`; S021 `score.r_u1` | yes; finite discovery and data points, not a fit |
| `primary_lattice` | `rs_s019_moduli_2026-10-26.json` | `runs[0].prime.classes[].kappa[0][0]` representative integer pair | yes; illustrative |
| `prereg_timeline` | `rs_s015_class_tests_2026-10-26.json`, `rs_s016_x_dependence_2026-10-26.json`, `rs_s017_fresh_classes_2026-10-26.json`, `rs_s019_moduli_2026-10-26.json`, `rs_s020_h_minus_2026-10-26.json`, `rs_s021_large_x_2026-10-26.json` | `score.P1/P2/P3.pass`; `analysis.verdict`; `score.Q1/Q2/Q3/Q4.pass`; `score.P.outcome`, `score.Q.prediction_met`; `score.outcome`; `score.A/B/H+.outcome` | yes; schematic, not quantitative plot |
| `r1_growth` | S016, S021 JSON | `analysis.r_u1` and `score.r_u1` | yes |
| `exponent_profiles` | S016 JSON | `analysis.collapse_bins_t_eq_N6_over_X.{k2,k3,k4,k5}[].{log10_t_lo,mean_s}` | yes; exploratory discovery |
| `holdout_residuals` | S021 JSON | `score.A.bins[].{log10_t_lo,n,mean_s,mean_F,diff,ok}`; `predictions[id=RS-S021-A].text` fixes acceptance at **±0.12**, not ±0.05 | yes |
| `exponent_five` | S021 JSON | `runs[].{X,classes[].{N,k,s}}`, select `k=5`; reference -1 is conjectural | yes |
| `moduli` | S019 JSON | `runs[0].prime.classes[].{k,t,s}`, `runs[0].unrestricted.classes[].{k,t,s}`; ***trace*** normalization | yes |
| `rho_parity` | `rs_s020_rho_partition_2026-10-26.json` | `settings.rational.classes[].{k,N_mod_12,s_by_part}`; grouped by row residue class; no significance test | yes; exploratory |
| `plateau` | S021 JSON | `stored_trend_K1`, `score.H+.K1`, `score.H+.outcome` | yes |
| `normalisation` | `rs_s022_cand002_audit_2026-10-26.json` | `normalizations.{frozen,control,raw}.median_across_X_spread_of_bin_means` | yes |
| `regime_map` | none (CAND-002 quantifiers) | conceptual boundary diagram, no numeric measurement | yes |
| `verification` | `formalisation/README.md`, `PROGRAM_STATUS.md`, Comparator run 40569785577 | schematic evidence path, no numeric measurement | no: box-heavy redundancy |

The regeneration command makes **fourteen** vector-PDF/PNG pairs (including two excluded schematic plates); the manuscript references twelve figures. The LaTeX build now hard-fails on a missing referenced PDF rather than silently creating a placeholder.

## Quantitative statements and frozen scoring

| Manuscript numerical claim | Committed evidence and exact keys | Audit interpretation |
|---|---|---|
| Engine relative discrepancy `5.27e-15` | `rs_s021_large_x_2026-10-26.json`: `validation.X320000.max_relative_r_difference` | engine-overlap agreement, not proof |
| S015 P1 / P2 / P3 = FAIL / PASS / FAIL | S015: `score.P1.pass=false`, `score.P2.pass=true`, `score.P3.pass=false`, `score.cand_002_gate.pass=false` | preserved precursor rejection; prereg `prediction_commit=552f5b7f0c7c5583b5a3158632299f920c2e5022` |
| S017 Q1 / Q2 / Q4 PASS; Q3 FAIL | S017: `score.Q1.pass`, `score.Q2.pass`, `score.Q4.pass` true; `score.Q3.pass=false`, `score.all_pass=false` | prereg `df8f889d5e246bc6da15040bfc235a2f3344e2e6` |
| `30` of `224` class-scale failures of Q3 universal clause | S017: `score.Q3.r_failures` has 30 entries; `score.Q3.n_with_5=112` per scale, `scales=[640000,1000000]` | finite and not every fifth-power class negative |
| S019 trace prime `-1.0812` vs unrestricted `-1.2224` | S019: `score.prime.pi5_mean_s`, `score.unrestricted.pi5_mean_s`, `score.P.outcome=INTRINSIC` | no rational/trace equation; prereg `d915b4decab333ad8f54823e14a8cac175258ed6` |
| S020 `-0.9188 ± 0.0828` over 88 | `rs_s020_h_minus_2026-10-26.json`: `score.mean_s=-0.9188132889`, `score.se=0.0828324667`, `score.n=88`, `score.outcome=PASS` | prereg `0efc29bdcacefa15a4360a6b8b3002e5b4517133` |
| S021 at X=2,000,000 / 4,000,000 | S021: `scales`, `runs[].X`, `runs[].code_commit=86a869114251b75e19b510cd843a6292747c3a4b` | largest observed cutoffs, no later extrapolation |
| S021 12 score bins pass | S021: `score.A.bins` length 12, all `ok=true`, `score.A.outcome=PASS`; observed maximum `abs(diff)=0.04945788945` | **critical correction:** registration `predictions[id=RS-S021-A].text` is **±0.12**. All 12 happened to satisfy the stricter observed ±0.05, but ±0.05 was *not* the registered tolerance. Prereg `2717a1301ef995fc32ef6a544fbe6669b29652b3` |
| S021 fifth-power means -1.0581, -1.0469 | S021: `score.B.mean_s_pi5_t_ge_3.2000000`, `score.B.mean_s_pi5_t_ge_3.4000000`, `score.B.outcome=PASS` | prereg acceptance interval [-1.15,-0.85], not a limit |
| Small-aspect `0.9612`, `0.9701`, `0.9747` | S021: `score.H+.K1_1e6_stored`, `score.H+.K1.2000000`, `score.H+.K1.4000000`, `score.H+.outcome=RISING` | finite pattern; F(0+) unresolved |
| Frozen, control-referenced and raw spreads | S022: `normalizations.frozen.median_across_X_spread_of_bin_means=0.02187259`, `normalizations.control...=0.02113255`, `normalizations.raw...=0.06705786`, `n_points=600` | raw spread larger; not an asymptotic claim |
| `1764/1764` formal faithfulness | `formalisation/Checks/Faithfulness.lean` and `formalisation/fixtures/sextic_200.json`; scoped workflow 40569785692 | fixture, not proof of conjectures |
| `26` selected exact Lean results | `formalisation/README.md` items 1–26, `formalisation/comparator.json`, Comparator/NanoDa workflow 40569785577 | finite identity claims only |

## Evidence and interpretation boundaries

The matrix has numerator rows / denominator columns, zero diagonal; prime-rational additive characters in the frozen matrix and distinct trace-normalized S019 comparisons. The H_P scaling correction is authoritative at `reciprocity_spectra/RS_HP_SCALE_ERRATUM.md`. The independently tested finite Lean identities are not asymptotic CAND-002(1)–(3) proofs. Fixed-class (3) does not follow from compact positive-aspect (1), large-aspect (2), or the corrected abstract H_P; see `RS_CAND002_LOGICAL_BRIDGE_AUDIT.md`. Row-prime parity is exploratory. No frozen prediction, output JSON, registered tolerance or conjecture status has been modified in RS-S042.
