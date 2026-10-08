# E016 — Frozen Central-Binomial Odd-Valuation Carry Shapes

**Stage:** DISCOVERY-1 / blind novelty lane  
**Queue:** SQ-016  
**Design:** D1-48 / S050, 2026-10-08  
**State:** DESIGN FROZEN ONLY; D16/H16/A16 UNGENERATED; BOTH G16 GUARDS PROTECTED

## 1. Firewall, provenance, and a single independent primitive family

Freeze exactly **one** prospective target-agnostic arithmetic family: the **three-coordinate odd-prime valuation profile of the central binomial coefficient** attached to an individual integer anchor x, with only the three exact capped coarsenings specified below. Every primitive feature is constructed without knowing whether x is prime; segmented prime membership supplies only the final binary label for a common, predeclared set of anchors. There is no fitted quantity, random seed, target signature, selected prior observation, or historical source.

This is a qualitatively different primitive from every E001–E015 family: E001/E002 gaps/differences, occupancy, residue transitions and persistence; E003 event-centred local neighbourhoods; E004 residue-transition refinements; E006 prime-indicator translation overlaps; E007 factorization of x−1 and x+1; E008 low binary positional words; E009 multiplicative unit orders and covering antichains; E010 quadratic-surd continued-fraction cycles; E011 irreducible finite-field polynomial degree partitions; E012 nearby lattice-norm brackets; E013 modular-polynomial short orbit comparisons; E014 primitive three-cube representations and summand incidence; E015 near-isqrt Euclidean-division remainder quartiles. E016 instead measures divisibility of **one combinatorial integer** C(2x,x) by the fixed odd bases 3,5,7 using finite Legendre floor sums over *all their powers*. It never computes the binomial integer or an integer factorization, an x-digit word, a gap/neighbour, norm representation, modular orbit, order, continued fraction, additive triple, or near-square denominator. The 3/5/7 profile may be independently checked via carries in those odd bases, but digit words, their positions and runs cannot be promoted. The only shared framework with earlier work is the generic fixed-width band / exact prime-vs-composite control.

**Theory-informed generic conventions, not experimental discoveries:** central binomial coefficients and factorial valuations are elementary combinatorics; the three smallest odd primes 3,5,7 and avoidance of direct 2/3/5/7 divisibility through Q=210 are fixed structural controls; cap 4, width one million, strict mode and signed enrichment are methodological conventions. No choice was made using D12/D13/H13, D14/H14 or D15/H15 outcomes, signatures, frequencies or failures. SQ-005 remains permanently CLOSED/QUARANTINED; no unblinded calibration object, historical target or source-derived mechanism is imported. This family is **UNAUDITED**, not claimed mathematically novel, and no collision/prior-art work occurs here.

## 2. Complete provenance-only frozen partition

All intervals are half-open and W=1_000_000. Scan by increasing W-aligned intervals from the end of E015 H15, rejecting every historical generated/consumed/contaminated, held-back, reserve, guard and calibration interval. Historic protected A6=[84_000_000,85_000_000) is not available; the next four clean units are assigned preguard, D16, midguard and one-shot H16, respectively. As in prior frozen designs, the later A16 lower endpoint is exactly twice D16's: 2*86_000_000=172_000_000. This placement uses **only numerical metadata**, never prime outcomes.

| Role | Immutable interval | Permission |
|---|---|---|
| G16-pre | [85_000_000,86_000_000) | untouched permanent non-target guard |
| D16 | [86_000_000,87_000_000) | future D1-49 discovery only, NOT this design session |
| G16-mid | [87_000_000,88_000_000) | untouched permanent non-target guard |
| H16 | [88_000_000,89_000_000) | one-shot untouched holdout, separately authorized only if an OBS and unchanged criterion are committed after D16 |
| A16 | [172_000_000,173_000_000) | untouched adversarial reserve; no automatic access |

**Exact historical inventory:** E013's 53 individually named early bands consist of 22 generated/consumed/retired (including contaminated A0), 14 held-back/adversarial/holdout and 17 guards. Add all 15 role bands of E013/E014/E015 (five each), including consumed D/H, guarded G and untouched A roles, plus the six disjoint quarantined E005 maximum calibration segments:
[128_000_000,129_048_576), [256_000_000,257_048_576), [512_000_000,513_048_576), [1_024_000_000,1_025_048_576), [2_048_000_000,2_049_048_576), [4_096_000_000,4_097_048_576).
Every calibration maximum contains five nested widths 4_096, 16_384, 65_536, 262_144 and 1_048_576 beginning at that anchor.

**Metadata arithmetic actually performed at D1-48:** 53+15+6=74 named historical exclusions. With exact integer overlap predicate ([a,b) intersects [c,d) iff a<d AND c<b), all 5*74=370 new/history comparisons and 10 new-role pairs were checked: **380/380, zero overlaps**. All **30/30** E005 nested ranges were separately checked for containment in their respective six maxima, and all 5*30=150 explicit new-role/nested comparisons were checked: **150/150, zero overlaps**. In addition 2*lower(D16)=lower(A16) holds exactly. No protected range was generated, traversed, queried or inspected. A0 stays contaminated/retired; A15, G15 guards, A14/A13, H12/A12/A8/A3, A6/A7 and every earlier protected/reserved/calibration interval keep their original states. A future newly found provenance collision fails closed; do not quietly move a frozen band.

## 3. Exact independent anchor primitive and controls

For any **authorized phase's single target** B=[L,U), let R210 be the ascending list of all integers 0<=r<210 with gcd(r,210)=1; exactly 48 classes:
[1,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,121,127,131,137,139,143,149,151,157,163,167,169,173,179,181,187,191,193,197,199,209].

The common complete population is X_B={x integer: L<=x<U, gcd(x,210)=1}; each x>1. It must be constructed **label-blind** and is never post-selected. Prime-labelled P_B and composite-labelled C_B are the disjoint exhaustive partition of X_B, with labels supplied **only** by membership in a separately authorized *directly segmented B prime set*. No extra primality testing of x or other high values is permitted. Q=210 removes the immediate 2/3/5/7-divisibility artefact from the control comparison; R210 residue classes are diagnostic only, never promoted.

For every x in X_B and each q in the **ordered fixed tuple (3,5,7)** define

  V_q(x) = sum over k>=1 with q^k<=2*x of (floor(2*x/q^k) − 2*floor(x/q^k)).

All terms are exactly 0 or 1; the sum is the nonnegative integer v_q((2x)!/(x!)²) and is exactly the number of carries in adding x+x in base q. Calculate only with integer products, comparisons, powers, quotients and sums; stop when next q-power exceeds 2*x. Do not create a factorial/binomial integer, factor it, scan x's binary coordinates, approximate with logarithms or query a prime oracle. The carry equivalence is an independent **validation identity only**. An independent base-q addition check on synthetic integers must agree, but no per-digit carry sequence may be mined, emitted or promoted.

For each q set c_q(x)=min(4,V_q(x)), an exact integer in 0..4. Cap 4 is a small fixed finite-state convenience, not fitted to an inspected frequency; values 4 include all higher valuations. The only internal ordered primitive vector is (c_3,c_5,c_7). Exact uncapped valuations, individual q-power terms, base-q digits and carry locations are strictly non-promotable.

## 4. Exactly three promotable transforms and finite domains

In this **fixed** family order:
- **T1 — total capped odd valuation:** c_3+c_5+c_7, integer 0..12 inclusive (13 signatures).
- **T2 — number of active odd valuation coordinates:** 1[c_3>0]+1[c_5>0]+1[c_7>0], integer 0..3 inclusive (4 signatures).
- **T3 — ordered capped valuation triple:** [c_3,c_5,c_7], each integer 0..4, all 125 lexicographically ascending triples admitted, including zero-frequency possibilities.

No alternative q, exponent, factorial ratio, cap, source integer, bit mask, subset, sorting, reordering, entropy, per-q marginal, carry-run, signature join, conditional anchor subset, normalization or additional feature is admitted. The T1/T2 mappings from T3 and each bound are validation/coarsening identities, **not** observations. In all families enumerate the **entire domain**, including signatures with zero observed frequency, for strict-mode competitor checks. Canonical signature order is ascending integer for T1/T2 and lexicographic on three integers for T3. Prime and composite tables use the same fixed X_B.

## 5. Frozen target-selection gates, confounder controls and duplicates

For F=T1,T2,T3, let n_P(t),n_C(t) be the exact signature t frequencies; N_P=|P_B|, N_C=|C_B|. For every one of 48 R210 classes r, use N_{P,r},N_{C,r},n_{P,r}(t),n_{C,r}(t). All tests are integer only. Define a mixed class by strict positivity of **all four** counts n_{P,r}, N_{P,r}-n_{P,r}, n_{C,r}, N_{C,r}-n_{C,r}. Define signed enrichment E(t)=n_P(t)*N_C−n_C(t)*N_P and per-class E_r(t)=n_{P,r}(t)*N_{C,r}−n_{C,r}(t)*N_{P,r}. No floating effect sizes, p-values, adjusted controls or weight fitting.

Freeze these **generic pre-result gates** for each eligible t:
1. Entire phase population: both N_P,N_C >= W/1000=1000; every one of the 48 R210 classes has **at least 10 of each label** (W/100000); no class may be omitted.
2. Target t is the **strict unique** prime count maximum against every full-domain signature; ties, null modes and equal competitors fail. Deterministic frequency display sorting cannot rescue a tie.
3. Target prime frequency n_P(t)>=ceil(sqrt(1000))=32.
4. At least 3*48/4=**36 mixed R210 classes**.
5. Overall E(t)>0 **and** at least ceil(5*48/8)=**30 classes** have E_r(t)>0; zero counts as nonpositive.
6. All ten mandatory validation-failure counters are exactly zero, including duplicate/support/serializer and generator guards.

These thresholds depend on W and number of wheel classes, **not** on any E012–E015 output, previous successful target or holdout failure. The wheel/congruence restrictions, exact factorial identity, nonnegative carry terms, cap, support conservation, coarsening identities, primality-label partition and modal sorting are artefact controls rather than promotable mathematical claims. A significant-looking pattern is never a proof.

Rank full finite tables by prime count descending, signature ascending solely to determine a strict unique mode; if no strict unique mode there is no candidate for that family, **no runner-up**. Evaluate all six gates exactly once for its unique target. For each eligible (F,t) collect internally its **exact set of prime anchors** S_F(t); if two eligible sets are **identical as integer sets**, keep the first in T1<T2<T3 and suppress the later, without substitution. Mere equal cardinality or formatting is not duplicate proof. At most three observations can arise, and none is allocated at design freeze. Unpromotable failed families remain failed; no tuning after reading results.

## 6. Immutable one-shot H16 criterion and A16 lock

After one separately authorized D16 discovery execution, if no family passes, record **NO ELIGIBLE OBSERVATION**, close SQ-016 and leave H16/A16 untouched. Otherwise assign OBS IDs and commit for each survivor its exact T-family and integer/three-integer-array target, unchanged T1/T2/T3 primitive, Q210 domain, all population/class/mixing/positive-sign/generator/serializer gates and H16 same-family strict-unique-mode criterion **before H16 generation**. On a separately authorized one-shot H16, pass iff the **same exact target** satisfies all six criteria against the **same complete finite signature domain** on H16 alone. Missing targets, ties, higher competitors, any failed population/32-occurrence/36-mixed/30-positive-class/total-positive or validation gate **REFUTE** mechanically. No altered wheel, valuation base, cap, mode target, alternative family, second H16 attempt or retarget. H16 is never an extra discovery band. A16 always requires separate later adversarial authorization, even after replication.

## 7. Narrow deterministic aggregate-only future serializer

Freeze D16 JSON **top-level exact keys**, no extensions: experiment, implementation_commit, band, partition, parameters, generation_plan, anchor_summary, validation, families, promotions.

- **experiment:** literal E016; **implementation_commit:** exact precommitted source commit string; **band:** object with only name,range=[L,U],interval_semantics="half-open".
- **partition:** ordered five objects G16-pre,D16,G16-mid,H16,A16, each containing exactly name,range,role. **parameters:** object with only width=1000000,wheel=210,residues_R210=the above 48,valuation_bases=[3,5,7],valuation_cap=4,population_floor=1000,class_floor=10,occurrence_floor=32,mixed_class_floor=36,positive_class_floor=30,strict_global_enrichment=true.
- **generation_plan:** exactly two ordered objects, keys only purpose,start,stop,strategy, equal to the phase allowlist in §8.
- **anchor_summary:** only wheel_anchor_count,prime_count,composite_count,prime_counts_by_R210 (48 ascending integers),composite_counts_by_R210 (48 ascending integers).
- **validation:** exactly ten nonnegative integer keys plan_failure_count,domain_partition_failure_count,factorial_valuation_failure_count,digit_carry_identity_failure_count,cap_signature_failure_count,support_identity_failure_count,class_label_failure_count,frequency_mode_failure_count,gate_duplicate_failure_count,serializer_failure_count; all MUST equal zero to inspect or promote.
- **families:** precisely three objects in T1,T2,T3 order; each has only family,prime_mode_count,highest_competing_count,strict_unique_prime_mode,unique_mode_signature (int for T1/T2; length-three int array for T3; null for tie),target_composite_count (null on tie),population_floor_passed,class_floor_passed,occurrence_floor_passed,mixed_class_count (null on tie),mixed_class_floor_passed,positive_class_count (null on tie),positive_class_floor_passed,aggregate_enrichment_numerator (null on tie),aggregate_enrichment_positive,mechanically_eligible (post duplicate suppression). Exact booleans, integers or null only.
- **promotions:** zero to three objects T1,T2,T3 order, keys only family,target_signature,target_prime_count,target_composite_count,mixed_class_count,positive_class_count,aggregate_enrichment_numerator. No OBS ID until an observation is separately frozen.

The only disclosed descriptive values are these strictly whitelisted aggregates. Prohibit individual x, primes, composite examples, valuation/q-power/carry traces, raw/truncated per-anchor triples, full T1/T2/T3 frequency tables, competitor identity, per-class target counts or signs, support sets, alternative target signatures, arbitrary diagnostics, timestamps/hostnames/environment, prime list, calibration outputs or noncanonical keys. Canonical bytes are UTF-8 of Python json.dumps(payload,sort_keys=True,indent=2,ensure_ascii=True)+"\n"; exact ordered lists; compute SHA-256. Future D16 must execute the **entire identical pinned command twice** at the same output path, seal the first raw bytes, and prove complete raw-byte and SHA equality **before inspecting any descriptive field**. Reject extra, missing or mistyped fields and any nonzero validation.

## 8. Two-entry generator *positive allowlists* — phase-specific

At each authorized phase target B=[L,U), the only permitted ordered generator calls are (1) base_sieve_support, **whole_prefix** [0,isqrt(U−1)+1); (2) segmented_target, **direct segmented** B. Exact independently checked integer square roots are:

| Phase | First and only low whole-prefix call | Second and only high segmented call |
|---|---|---|
| D16 (future D1-49 only) | [0,9328), since isqrt(86_999_999)=9327 | [86_000_000,87_000_000) |
| H16 (later separate one-shot if OBS) | [0,9434), since isqrt(88_999_999)=9433 | [88_000_000,89_000_000) |
| A16 (later separate adversarial permission only) | [0,13153), since isqrt(172_999_999)=13152 | [172_000_000,173_000_000) |

**Validate the complete list of exactly two (purpose,start,stop,strategy) tuples before entering either generator, and recheck at each generator boundary.** Fail closed on wrong phase, high whole-prefix, direct high primality helper, any other high traversal, off-phase H16/A16, guards, consumed D16 after use, malformed/split/expanded/shortened/shifted/duplicated/reordered/extra calls, alternate low prefix, all 74 historical exclusions, E005 six maxima and 30 nested calibration intervals, or implicit prime enumeration in a factorial/binomial helper. The negative-list checks supplement but never replace the exact **positive** allowlist. No generator call was made in D1-48.

## 9. Mandatory D1-49 pre-generation obligations, not performed at design freeze

Implement exactly this primitive and D16-only evaluator, generator-boundary checks and narrow serializer; do not add features. Before the first prime generation, separately **commit and independently remote-byte-verify** exact source and tests and a complete pinned full-run command, the latter in its own pre-generation command checkpoint. Focused synthetic hand checks must include Legendre vs independent base-q x+x carry count at tiny fabricated x, q-power cutoff, each term 0/1, cap at 4, zero/nonzero and full 13/4/125 domains, exact T1/T2 coarsening, lexical ordering, strict unique mode/tie and no fallback, integer aggregate and all 48 class sign tests, class mixture, every floor, exact duplicate prime-support set equality and inequality, canonical serializer fields/types and forbidden extras, and empty promotion case. Synthetic labels are invented and no prime/primality generator may enter.

Poison a generator that raises immediately if called; prove **all malformed/off-phase/protected/nested E005 and all 74 named exclusion plans** are rejected before generator entry. Verify 380/380 historical/new pairs, 30/30 calibration nesting checks and 150/150 explicit new/nested pairs again from frozen metadata, with zero overlaps, before any valid prime call. Use exact integer root arithmetic; tests may **not** traverse future high bands. Focused pytest and Python compilation mandatory; Ruff if available, otherwise record that limitation without claiming pass. Check source/test/pinned command Git blobs before generation. Only then a **separate D1-49 session** may execute D16 twice using the identical fixed complete command and two-entry positive plan, compare all raw bytes/SHA first, and mechanically promote at most three observations with H16 criterion frozen before any separate replication or close SQ-016. Never run H16/A16/guards as part of D1-49.

## 10. D1-48 strict design-only checkpoint

Only documentary family choice and exact interval/grammar metadata arithmetic were performed. **No evaluator/code/tests were created or run, no prime number generated, queried or inspected, no D16/H16/A16/G16 traversal, no D12/D13/H13, D14/H14 or D15/H15 target/frequency/result mining, no calibration transfer, no H15 retarget, no OBS/CAND allocation, no mechanism, proof, candidate synthesis, adversarial, literature, collision, novelty or prior-art work.** OBS-018/019 remain REPLICATED, OBS-020/021 REFUTED; totals stay 13 REPLICATED / 0 OBSERVED / 8 REFUTED; SQ-005 CLOSED/QUARANTINED, SQ-014/015 CLOSED, zero active candidates. This is a frozen design, not computation or evidence of a prime phenomenon. Natural stop here; next independent unit is D1-49 D16-only implementation/execution under the frozen pre-generation constraints.
