# E018 — Frozen Monomer–Domino–Tromino Tiling Residue Shapes

**Stage:** DISCOVERY-1 / blind novelty lane  
**Queue:** SQ-018  
**Design unit:** D1-52 / S054, 2026-10-08  
**Status at freeze:** DESIGN ONLY; D18/H18/A18 NOT GENERATED; G18 GUARDS UNTOUCHED  
**Epistemic status:** UNAUDITED representation, not a prime observation, conjecture, claim of novelty, or prior-art assessment

## 1. Exactly one source-free mathematical primitive and independence boundary

Freeze the exact number **T(n)** of ordered tilings of a row of **n** unit cells by one available tile of each length 1, 2, and 3 (monomer, domino, tromino); tiles do not carry colours, orientations, weights, or labels. The empty row has exactly one tiling. This is a pure combinatorial object defined without prime labels. The tile set, length parameter, and target-free residue transforms below are immutable. No source, historical outcome, prime support, hidden target, calibration object, literature or prior-art result was consulted to choose it.

For all integers n>=0 set T(0)=1, T(n)=0 for n<0, and for n>=1
`T(n)=T(n-1)+T(n-2)+T(n-3)`.
Equivalently a tiling is classified by its first tile, yielding the same recursion. In particular T(1)=1, T(2)=2, T(3)=4. The **sole primitive per anchor x** is the exact self-length tiling count reduced to its canonical remainder `r(x)=T(x) mod x`, `0<=r(x)<x`. The modulus x is the same anchor used for both labels, not a selected modulus search. Compute no new quantity conditional on primality.

**Theory-informed generic choices, disclosed:** counting one-dimensional compositions/tilings using three smallest positive tile lengths is an elementary combinatorial recurrence; reduction modulo the row length, the Q210 wheel, uniform four/eight residue-rank bins and million-width range convention are fixed source-free choices. Nothing here claims a historically new tiling identity or a known link to prime theorems. Modular reduction is an encoding/control convention, not a claim that a residue mode is intrinsically informative.

**Qualitative distinction from every frozen E001–E017 primitive:** E001/E002 concern prime gaps/residue transitions/occupancy and persistence; E003 event-selected prime neighbourhoods; E004 refinement fibres of prime residue transitions; E006 translated prime-indicator pair overlaps; E007 factorization of neighbours x-1 and x+1; E008 a short positional binary word of x; E009 unit-group multiplicative orders and cover antichains modulo x; E010 variable quadratic-surd continued-fraction denominator **cycles**; E011 polynomial factor-degree partitions over finite fields; E012 near lattice-norm bracketing; E013 short **nonlinear quadratic polynomial** orbits modulo x; E014 primitive positive three-cube incidence; E015 near-square Euclidean division remainders; E016 factorial odd-prime valuations of central binomial coefficients; E017 fixed-step circular Josephus **elimination survivor**. E018 instead counts all finite tilings of the full **x-cell row** by a fixed finite tile alphabet using a homogeneous three-term **linear counting recurrence**, then reduces that count modulo x. It has no gap, prime pair, prime-index neighbour, digit word, factorization, unit action/order, continued-fraction cycle, finite-field polynomial factorization, lattice support, additive cube representation, shell division, valuation/carry, quadratic polynomial trajectory or circular deletion. In particular E018's logarithmic-time transfer-matrix evaluation of the x-th *count* is not E010's periodic quadratic-surd state or E013's fixed-length quadratic orbit. Reuse of exact generic wheel/bin/strict-mode controls is **not** a second mathematical primitive or a retune of E017.

One source of risk is that any remainder-based signature could be forced by algebra or congruences rather than prime structure. Such identities, if found later, are controls/limitations only and never eligible for OBS solely by encoding. No mechanism, prior-art or mathematical novelty analysis is authorised by this design.

## 2. Exact fresh interval roles from named provenance only

All intervals are half-open, W=1_000_000. Start the W-aligned free-band scan at 94_000_000, the exclusive end of permanently protected H17=[93M,94M). Select in order the first free units for G18-pre, D18, G18-mid and one-shot H18. Separately set lower(A18)=2*lower(D18)=190_000_000; the A18 width is W and its placement must independently pass all exclusion checks. No empirical data entered the scan.

| Role | Frozen exact interval | Protection/permission |
|---|---|---|
| G18-pre | [94_000_000,95_000_000) | untouched, permanent non-target guard |
| D18 | [95_000_000,96_000_000) | discovery only in a **future separate D1-53**, after pre-generation checkpoints |
| G18-mid | [96_000_000,97_000_000) | untouched, permanent non-target guard |
| H18 | [97_000_000,98_000_000) | untouched one-shot holdout, only after a D18 OBS and immutable criterion are committed |
| A18 | [190_000_000,191_000_000) | untouched separately locked adversarial reserve; no automatic access |

The historical inventory comprises the exactly **53 individually named** early generated/consumed/retired/protected/guard intervals listed in E013 section "Provenance-only partition and exact disjointness"; **25 distinct named** G/D/G/H/A roles of E013–E017, including all consumed D/H bands and all untouched guards/holdouts/reserves; and the **six E005 quarantined maximum calibration segments**. That is **84 distinct named historical exclusions**, not a merged cover and not merely the nearest adjacent exclusions. A0 remains contaminated/retired, not untouched. The six E005 maxima are exactly [128_000_000,129_048_576), [256_000_000,257_048_576), [512_000_000,513_048_576), [1_024_000_000,1_025_048_576), [2_048_000_000,2_049_048_576), and [4_096_000_000,4_097_048_576). Their 30 nested calibration intervals have the same six starts and five widths 4_096, 16_384, 65_536, 262_144, 1_048_576.

**D1-52 independent arithmetic audit using named interval metadata only:** `[a,b)` overlaps `[c,d)` iff `a<d && c<b`. Exactly 84*83/2=**3,486** historical/historical pairs, **5*84=420** new/historical pairs, and **5*4/2=10** new/new pairs were compared and all are disjoint (**430/430** comparisons involving new roles). All **30/30** E005 nested widths are contained in their maximum; **5*30=150/150** new/nested pairs are disjoint. `2*95_000_000=190_000_000` and all five intervals are W-aligned. This is interval arithmetic, not numerical data access, high-band traversal or a prime-generation step. Any newly discovered conflict must halt, never quietly relocate an interval.

H17/A17/G17, A7, H16/A16/G16, A15/A14/A13, H12/A12/A8/A3, all earlier guarded, consumed, held-back, adversarial and calibration intervals remain barred. The two new guards are never targets. A18 cannot be run as part of D18 or H18.

## 3. Exact common label-blind anchor population and implementation grammar

Freeze Q=210=2*3*5*7 and its complete ordered 48 reduced residues
`R210=(1,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,121,127,131,137,139,143,149,151,157,163,167,169,173,179,181,187,191,193,197,199,209)`.

For a **separately authorised single phase** B=[L,U), define `X_B={x integer | L<=x<U, gcd(x,210)=1}` independently of prime labels and of r(x). Every such x>1. After label-blind domain construction, partition exactly into `P_B={x in X_B | x is prime}` and `C_B=X_B\P_B`, with all composites included and no drop/rebalancing by feature. The only prime oracle is membership in the **single directly segmented authorised high target**; no per-anchor external primality helper or other high-region generation. Every R210 class is retained for both populations.

The conceptual recurrence defining T(n) must **not** be iterated n times for production x. Freeze the exact transfer matrix

`M=[[1,1,1],[1,0,0],[0,1,0]]`,
`v_0=[T(2),T(1),T(0)]^T=[2,1,1]^T`,
`M^x v_0 = [T(x+2),T(x+1),T(x)]^T`.

The production value r(x) is the third entry of `(M^x mod x)*(v_0 mod x) mod x`, with every matrix/vector operation in the integers and all remainders canonical. Matrix exponentiation is by deterministic binary repeated squaring in O(log x) 3-by-3 modular matrix products, with identity exponent-zero base, no floating-point, machine-word overflow, randomised short-circuit, high-anchor precomputed table, or call to any primality function. This is exactly equivalent to the combinatorial recurrence by induction. A separately implemented bounded direct counting recurrence and tiny explicit tiling enumerations are **synthetic validation references only**, never a high-range production fallback. The same finite definition applies to every integer x>=1; the production wheel and phases restrict which x may be evaluated.

## 4. Complete finite transforms and signatures

For every x in the complete X_B, calculate only `r=r(x)`. Freeze `b4(x)=(4*r)//x` in {0,1,2,3} and `b8(x)=(8*r)//x` in {0,1,2,3,4,5,6,7}. Use arbitrary-precision exact integer multiplication and quotient; a floating ratio is prohibited. Exactly two promotable families, ordered permanently:

- **L1 — tiling-remainder quartile:** target signature b4, full domain 0,1,2,3, ascending.
- **L2 — tiling-remainder octile:** target signature b8, full domain 0,1,2,3,4,5,6,7, ascending.

The forced coarsening `b4=floor(b8/2)` is a **nonpromotable invariant/control**, not a third feature. All zero-count signatures remain in their complete domain and compete. No row tiles of other lengths, coloured variants, alternate recurrences/initial values, extra powers, alternative modulo, digits/quotients of T(x), x±1 tiling signatures, nested interval selection, custom bins, changing the wheel, order statistics over other tiling counts or conditional anchor filtering may be introduced. Exactly one mathematical source and two fixed coarsenings: no target selected at design.

## 5. Strict signed controls, promotion and duplicate grammar

For F in (L1,L2), each complete-domain signature t has exact nonnegative integer frequencies nP(t),nC(t); NP=|P_B| and NC=|C_B|. Each ordered r0 in R210 also has NP,r0,NC,r0,nP,r0(t),nC,r0(t). Exact signed enrichment: `E(t)=nP(t)*NC - nC(t)*NP` and `E_r0(t)=nP,r0(t)*NC,r0 - nC,r0(t)*NP,r0`. A class is **fully mixed** only if its prime target, prime nontarget, composite target, composite nontarget counts are **all >0**. A zero signed numerator is not positive; no decimal estimate, smoothing, statistical fitting or omitted class.

For each F separately, and **only its strict unique prime-count mode among every signature in its full domain**, promote if and only if **all**:
1. NP>=1000 and NC>=1000, plus NP,r0>=10 and NC,r0>=10 in **each of all 48** R210 classes;
2. strict unique prime-count mode: any tie or empty-mode ambiguity fails; deterministic signature ordering may be used only to print, **never as fallback**;
3. target nP(t)>=32 (ceil sqrt(1000), fixed);
4. at least **36/48** classes fully mixed for t;
5. **E(t)>0** and at least **30/48** individually positive E_r0(t);
6. every one of the ten section-7 mandatory validation counters exactly zero, with no forbidden plan/schema field;
7. the signature is not merely a proven definitional/encoding identity (all matrix, domain, bin/coarsening and counting tautologies are nonpromotable).

No lower-ranked alternative, family/target switch, targeted class split, post-hoc criterion amendment or threshold relaxation. For each initially eligible (F,t), retain the exact *integer anchor ID set* `S_F(t)={x in P_B | F(x)=t}` internally. Compare the sets themselves, not merely frequencies, digest, signatures, ranks, or sample rows. If `S_L1(t1)=S_L2(t2)`, keep L1 and suppress L2, **without replacement**; equal-size unequal sets are not duplicates. Fixed promotion cap **two**, at most one per family, in L1 then L2 order. No OBS/CAND ID is created by this design.

These gates diagnose basic wheel, coarsening, support and signed-enrichment artefacts, but do not prove nontriviality or any general theorem.

## 6. One-shot unchanged H18 and independent A18 lock

Only if **separate authorised D18 execution** yields an eligible nonduplicate family may an OBS ID and its exact family/signature with **this identical full criterion** be permanently committed *before* a later H18 generator entry. A D18 closure with zero survivors closes SQ-018 **NO ELIGIBLE OBSERVATION**, leaving H18/A18/guards ungenerated. H18 never selects targets.

For an OBS whose frozen D18 family is L1 or L2 and signature is exact integer t, the **sole one-shot H18** test on X_H18 requires t to be the **strict unique prime-count mode in precisely the same complete domain and same family** on H18, with >=1000 each label, >=10 each label in each of all 48 classes, >=32 target primes, >=36 fully mixed classes, E(t)>0, >=30 positive E_r0(t), all ten zero validators and identical exact-support duplicate handling. An absent t, a tie or greater competitor, any deficient gate, corrupted schema or forbidden generator call mechanically **REFUTES**; there is no second H18 discovery scan, retarget, change of bins, different modulus/wheel, step/tile set, target, or fallback. Each observation has exactly this one attempt. A18 is not unlocked by H18 outcomes and requires an independently authorised later adversarial unit. Guards never become execution targets.

## 7. Ten validators and strict narrow canonical serializer

Authorised future phase JSON has **exactly** the top-level keys `experiment`, `implementation_commit`, `band`, `partition`, `parameters`, `generation_plan`, `anchor_summary`, `validation`, `families`, `promotions`, and no other keys.

- `experiment` is "E018"; `implementation_commit` is the actual pinned, previously committed source/test SHA. `band` has exactly `name`, `range` (two integer bounds) and `interval_semantics`="half-open". `partition` contains exactly the five ordered role objects G18-pre,D18,G18-mid,H18,A18, each with only `name`, `range`, `role`.
- `parameters` has exactly `width`=1000000, `wheel`=210, `residues_R210`=the fixed 48-order list, `tile_lengths`=[1,2,3], `tiling_seed`=[2,1,1], `transfer_matrix`=[[1,1,1],[1,0,0],[0,1,0]], `remainder_modulus`="anchor", `residue_bin_counts`=[4,8], `population_floor`=1000, `class_floor`=10, `occurrence_floor`=32, `mixed_class_floor`=36, `positive_class_floor`=30 and `strict_global_enrichment`=true.
- `generation_plan` is exactly the two ordered allowlist entries of section 8, each with only `purpose`, `start`, `stop`, `strategy`.
- `anchor_summary` has exactly `wheel_anchor_count`, `prime_count`, `composite_count`, `prime_counts_by_R210` and `composite_counts_by_R210` (48 nonnegative integer entries each).
- `validation` has exactly these **ten** nonnegative integer counters, each required to be zero: `plan_failure_count`, `domain_partition_failure_count`, `tiling_recurrence_failure_count`, `transfer_matrix_failure_count`, `residue_bin_failure_count`, `support_identity_failure_count`, `class_label_failure_count`, `frequency_mode_failure_count`, `gate_duplicate_failure_count`, `serializer_failure_count`.
- `families` has exactly two objects in L1,L2 order, each with only `family`, `prime_mode_count`, `highest_competing_count`, `strict_unique_prime_mode`, `unique_mode_signature` (0..3 or 0..7, or null on tie), `target_composite_count` (nonnegative integer, null on tie), `population_floor_passed`, `class_floor_passed`, `occurrence_floor_passed`, `mixed_class_count` (null on tie), `mixed_class_floor_passed`, `positive_class_count` (null on tie), `positive_class_floor_passed`, `aggregate_enrichment_numerator` (null on tie), `aggregate_enrichment_positive`, `mechanically_eligible`. All booleans are actual JSON booleans. An absent or tied target must have null target-specific fields and fail eligibility; never serialize a fallback.
- `promotions` contains zero to two objects in L1,L2 order and exactly the keys `family`, `target_signature` (integer), `target_prime_count`, `target_composite_count`, `mixed_class_count`, `positive_class_count`, `aggregate_enrichment_numerator`, only for eligible and nondeduplicated signatures. No OBS number appears before a separate committed observation freeze.

Every map rejects missing/unknown keys; integer values must not be booleans, floating-point values or strings; null is permitted only where specified. Never serialize individual anchor IDs/prime values, tiling counts or remainders, row tilings, full signatures or frequency tables, per-class target counts/enrichment signs, exact support sets, competitor identity, failed or alternative targets, sources, timestamps, environmental metadata or E005 objects. Internally needed exact support sets are discarded without serialization.

Canonical bytes are UTF-8 `json.dumps(payload, sort_keys=True, indent=2, ensure_ascii=True)+"\n"` with one terminal LF, no extra whitespace or metadata. At future D18, checkpoint the *complete identical actual pinned command* separately before entry, run it exactly twice against the same output path, seal first full raw bytes, and prove **whole-file byte equality and identical SHA-256** before inspecting any descriptive aggregate. Any schema/type mismatch, nonzero validation counter or replay mismatch is fail-closed.

Validator responsibilities: (1) exact phase-positive plan and exclusions; (2) complete wheel partition/label conservation; (3) bounded independent exact count/tiling enumeration semantics; (4) exact M/recurrence agreement and power/modular arithmetic; (5) canonical r bounds, complete bin domains and b4=floor(b8/2); (6) per-family support/count partition identities; (7) all 48 residue/label class conservation; (8) full-domain mode/tie/no-fallback semantics; (9) exact signed gates, exact set equality and cap; (10) strict schema, field/type/byte and forbidden-data checks. Synthetic reference tests are not prime computations.

## 8. Future exact two-entry positive prime-generation allowlists — NOT executed

For a separately authorised phase B=[L,U), prevalidate the **whole ordered generation plan** before generator entry and again at each boundary. Its *only* two calls are `(base_sieve_support,0,isqrt(U-1)+1,whole_prefix)`, then `(segmented_target,L,U,direct_segmented)`. No third call, high whole-prefix, high primality query, indirect traversal, extra/split/reordered/expanded/shrunken target, alternative strategy or protected/guard/calibration segment is permitted. Exact integer `s=isqrt(U-1)` must satisfy `s*s<=U-1<(s+1)*(s+1)`.

| Separate possible phase | Sole safe low support | Sole directly segmented high target |
|---|---|---|
| D18 (only future D1-53) | [0,9798), isqrt(95_999_999)=9797 | [95_000_000,96_000_000) |
| H18 (future, only after committed D18 OBS) | [0,9900), isqrt(97_999_999)=9899 | [97_000_000,98_000_000) |
| A18 (future, independent adversarial approval) | [0,13821), isqrt(190_999_999)=13820 | [190_000_000,191_000_000) |

The positive plan is authoritative; a historical negative exclusion inventory is necessary as an extra guard but never sufficient on its own. Any plan overlapping any of **84** named historical exclusions, any of the **30** nested E005 bands, any E018 off-phase role, or an undeclared segment must fail *before even the low support generator*. Entire low support is well below protected high roles. No E018 generator was entered in D1-52.

## 9. Strict D1-52 stop and next distinct bounded unit

This is an exact mathematical/documentary **DESIGN-ONLY** freeze. There was no new E018 source code, test, evaluator, test execution, run-command file, prime generation, primality query, numerical high-anchor traversal, E017 result mining, old-family target/signature/frequency/failure inspection, calibration unblinding, prior-art/source/literature search, candidate synthesis, mechanism/proof, adversarial execution, collision/novelty assessment, OBS/CAND allocation or criterion retune. All previously committed evidence and observation/conjecture/failure statuses stay immutable. SQ-005 and SQ-014–017 remain CLOSED; D17 consumed with no eligible OBS; H17/A17/G17 untouched; 13 REPLICATED / 0 OBSERVED / 8 REFUTED; zero active CAND.

The **only distinct next bounded unit**, D1-53 / SQ-018, may implement and checkpoint the *already frozen* D18 evaluator, exact semantics and poison tests, and separately checkpoint the complete exact D18 command **before any generator**. The future unit must independently verify 3,486 historic/historic, 430 new-role and 150 nested intersections plus 30 containments, source/test/command blobs, all 84 role negative plans, all 30 E005 nested poisons, and all malformed whole-plan poisons; conduct only the exact D18 allowlisted generation twice and validate complete byte equality before narrow aggregate interpretation; either freeze 0–2 OBS/unchanged H18 criteria or close without H18. **Do not run D18, H18 or A18 in D1-52.**
