# Observation Ledger

Permanent append-only register of reproducible phenomena.

## Template

### OBS-###

**Title:**  
**Status:** OBSERVED / REPLICATED / PROMOTED / REFUTED / EXPLAINED / DORMANT  
**Date:**  
**Experiment:**  
**Exact definition:**  
**Discovery range:**  
**Holdout range:**  
**Observation:**  
**Triviality checks:**  
**Replication result:**  
**Possible mechanism:**  
**Candidate link:**  
**Notes:**
### OBS-001

**Title:** Zero is the unique modal third forward difference on D0  
**Status:** REPLICATED  
**Date:** 2026-10-06  
**Experiment:** E001 / SQ-001  
**Exact definition:** For the ordered primes `q_1 < ... < q_n` lying inside a band, form the exact third forward differences `Δ^3 q_i = q_{i+3} - 3q_{i+2} + 3q_{i+1} - q_i`, with no cross-boundary windows. The observation is that value 0 has strictly greater frequency than every other third-difference value.  
**Discovery range:** D0 = `[0, 1_000_000)`  
**Holdout range:** H0 = `[1_000_000, 2_000_000)`, untouched at promotion  
**Observation:** In D0, `Δ^3 = 0` occurs 4,656 times. The runner-up value is 6 with 4,241 occurrences; 12 has 4,198. Therefore 0 is the unique modal third-difference value.  
**Triviality checks:** Parity forces most post-boundary finite differences into even classes but does not force 0 to dominate. `Δ^3 = 0` is equivalent to three consecutive in-band prime gaps forming an arithmetic progression, so the count is not a serializer identity. The 4,656 zeroes are distributed across 131 distinct width-3 gap motifs; the largest single contributing motif, `[6, 4, 2]`, contributes only 306, so the observation is not a one-motif artifact. No small-modulus forcing of the modal rank was identified.  
**Replication result:** REPLICATED on untouched H0 = `[1_000_000, 2_000_000)`. Value 0 occurs 3,764 times and is the unique modal third-forward-difference value; the runner-up is value 12 with 3,408 occurrences. Frozen criterion satisfied without tuning. H0 artifact SHA-256 `80c8c49f1845e941764b31471404a8e674fa794394687cb6502dbd2eca980254`.  
**Possible mechanism:** Unknown; arithmetic-progression structure among consecutive gap triples is the immediate exact reformulation.  
**Candidate link:** none — D1-02 triage retained OBS-001 as REPLICATED without promotion.  
**Notes:** Discovery artifact SHA-256 `822431d664d5a35949abdf230a1b8abb41afa1f97511b7c129e5d18779f2e284`; compact evidence in `research/evidence/E001_D0_observations.json`. D1-02 synthesis found that the two adjacent million-wide bands establish replication but do not justify choosing a universal/eventual quantifier over band origin, width, or scale; a D0+H0-only candidate would merely restate finite evidence. D1-03/E002 preflight froze this exact definition unchanged for the five fresh bands S1=[2,000,000,3,000,000), S2=[4,000,000,5,000,000), S3=[8,000,000,9,000,000), S4=[16,000,000,17,000,000), and S5=[32,000,000,33,000,000). D1-04 E002 result: **NOT PERSISTENT**. The frozen criterion fails in S1 (zero 3,292 vs value 12 at 3,323) and S3 (zero 2,839 vs value 12 at 2,881), while passing S2, S4, and S5. This does not rewrite the historical E001 REPLICATED status. Valid E002 artifact SHA-256 `32d24d5ea2417b1fdbf02b0787e6a616170162e0f7373dae32cf6906f19d37d5`.

### OBS-002

**Title:** `[6, 6]` is the unique modal width-2 prime-gap motif on D0  
**Status:** REPLICATED  
**Date:** 2026-10-06  
**Experiment:** E001 / SQ-001  
**Exact definition:** For consecutive in-band prime gaps `g_i`, count every width-2 word `(g_i, g_{i+1})` wholly contained in the band. The observation is that motif `[6, 6]` has strictly greater frequency than every other width-2 motif.  
**Discovery range:** D0 = `[0, 1_000_000)`  
**Holdout range:** H0 = `[1_000_000, 2_000_000)`, untouched at promotion  
**Observation:** `[6, 6]` occurs 1,929 times in D0. The next two motifs are `[4, 6]` with 1,771 and `[6, 4]` with 1,766, so `[6, 6]` is the unique mode.  
**Triviality checks:** Gap 6 is itself the modal single gap in D0 (13,549 occurrences), but that marginal fact does not force two consecutive 6-gaps to be the modal pair. Parity does not distinguish `[6, 6]` from several even-gap competitors, and small-modulus admissibility also permits the leading competitors. No encoding identity forces the observed rank.  
**Replication result:** REPLICATED on untouched H0 = `[1_000_000, 2_000_000)`. Motif `[6, 6]` occurs 1,409 times and is the unique modal width-2 motif; runner-up `[6, 4]` occurs 1,335 times. Frozen criterion satisfied without tuning. H0 artifact SHA-256 `80c8c49f1845e941764b31471404a8e674fa794394687cb6502dbd2eca980254`.  
**Possible mechanism:** Unknown; could reflect an interaction between the marginal abundance of gap 6 and local admissibility/correlation, to be investigated only after replication.  
**Candidate link:** none — D1-02 and D1-06 triages retained OBS-002 as REPLICATED without promotion; D1-06 additionally records E002 PERSISTENT.  
**Notes:** Discovery artifact SHA-256 `822431d664d5a35949abdf230a1b8abb41afa1f97511b7c129e5d18779f2e284`; compact evidence in `research/evidence/E001_D0_observations.json`. D1-02 synthesis found that the two adjacent million-wide bands establish replication of the modal pair but do not justify a universal/eventual modal-rank claim across arbitrary or chosen scales; a D0+H0-only candidate would not extend beyond the evidence. D1-03/E002 preflight froze this exact definition unchanged for the same five fresh scale bands. D1-04 E002 result: **PERSISTENT**. `[6, 6]` remains the strict unique width-2 motif mode in every band: S1 1,273 vs 1,161, S2 1,140 vs 1,077, S3 1,003 vs 940, S4 924 vs 824, and S5 831 vs 745. No motif width/value was retuned. Historical E001 status remains REPLICATED. Valid E002 artifact SHA-256 `32d24d5ea2417b1fdbf02b0787e6a616170162e0f7373dae32cf6906f19d37d5`. D1-06 synthesis again made no candidate: seven successful fixed-width bands strengthen persistence but do not justify a non-arbitrary quantifier over untested origins, widths, later scales, or infinitely many scale-ladder members; a seven-band statement would only restate finite computation.

### OBS-003

**Title:** Complete directed reduced-residue transition support across the frozen modulus grid  
**Status:** REPLICATED  
**Date:** 2026-10-06  
**Experiment:** E001 / SQ-001  
**Exact definition:** For each frozen modulus `m ∈ {6, 10, 12, 30, 60}`, remove prime divisors of `m`, reduce the remaining in-band consecutive primes modulo `m`, and take directed transitions between consecutive residues. Let `R_m` be the reduced residue system. The observation is that the transition support equals the full Cartesian product `R_m × R_m` for every frozen modulus.  
**Discovery range:** D0 = `[0, 1_000_000)`  
**Holdout range:** H0 = `[1_000_000, 2_000_000)`, untouched at promotion  
**Observation:** D0 realizes 4/4 possible directed pairs for `m=6`, 16/16 for `m=10`, 16/16 for `m=12`, 64/64 for `m=30`, and 256/256 for `m=60`.  
**Triviality checks:** The reduced-residue filter defines which endpoint residues are allowed, but it does not force a finite consecutive-prime sequence to realize every allowed ordered pair. The observation is therefore not a consequence of serialization or merely of excluding non-coprime residues. No stronger mechanism is claimed.  
**Replication result:** REPLICATED on untouched H0 = `[1_000_000, 2_000_000)`. Directed reduced-residue transition support is complete at every frozen modulus: 4/4 for 6, 16/16 for 10, 16/16 for 12, 64/64 for 30, and 256/256 for 60; no allowed directed pair is missing. Frozen criterion satisfied without tuning. H0 artifact SHA-256 `80c8c49f1845e941764b31471404a8e674fa794394687cb6502dbd2eca980254`.  
**Possible mechanism:** Unknown; later SQ-004 may test exact projection/refinement structure if this coverage property survives holdout.  
**Candidate link:** none — D1-02 and D1-06 triages retained OBS-003 as REPLICATED without promotion; D1-06 additionally records E002 PERSISTENT.  
**Notes:** Discovery artifact SHA-256 `822431d664d5a35949abdf230a1b8abb41afa1f97511b7c129e5d18779f2e284`; compact evidence in `research/evidence/E001_D0_observations.json`. D1-02 synthesis found that exact complete support on the five frozen moduli in D0+H0 is not yet enough to justify an all-moduli and/or infinite-occurrence statement; restricting a candidate to the finite modulus grid would largely restate finite coverage. D1-03/E002 preflight froze this exact definition and the modulus family {6,10,12,30,60} unchanged for the same five fresh scale bands. D1-04 E002 result: **PERSISTENT**. Every S1-S5 band has complete directed transition support at every frozen modulus: 4/4, 16/16, 16/16, 64/64, and 256/256, with no missing allowed pair. No modulus was added or removed. Historical E001 status remains REPLICATED. Valid E002 artifact SHA-256 `32d24d5ea2417b1fdbf02b0787e6a616170162e0f7373dae32cf6906f19d37d5`. D1-06 synthesis again made no candidate: full support across the five frozen moduli in seven tested bands still does not justify an all-moduli, broader-family, all-band/eventual, or infinite-occurrence quantifier; restricting a statement to the tested finite grid would only restate committed evidence.

### OBS-004

**Title:** No empty globally anchored width-100 block on D0  
**Status:** REFUTED  
**Date:** 2026-10-06  
**Experiment:** E001 / SQ-001  
**Exact definition:** Partition value space into globally anchored blocks `[100k, 100(k+1))`. Restrict to blocks wholly inside the band and count in-band primes exactly. The observation is that every such block has occupancy at least 1.  
**Discovery range:** D0 = `[0, 1_000_000)`  
**Holdout range:** H0 = `[1_000_000, 2_000_000)`, untouched at promotion  
**Observation:** All 10,000 width-100 D0 blocks are nonempty. The minimum occupancy is 1, attained first at `[155900, 156000)` and also at `[268300, 268400)` and `[413300, 413400)`.  
**Triviality checks:** This is not forced merely by the maximum prime gap: D0 contains a maximum in-band gap of 114, larger than the block width 100, yet the fixed global block alignment still produces no empty block. Parity and residue encoding do not force nonemptiness of each anchored interval.  
**Replication result:** REFUTED on untouched H0 = `[1_000_000, 2_000_000)`. Exactly one globally anchored width-100 H0 block is empty: `[1_671_800, 1_671_900)`, occupancy 0. This is the first and only empty H0 block and is an exact counterexample to the frozen criterion. H0 artifact SHA-256 `80c8c49f1845e941764b31471404a8e674fa794394687cb6502dbd2eca980254`.  
**Possible mechanism:** Unknown; global alignment relative to large gaps is the immediate structural issue.  
**Candidate link:** none — REFUTED; excluded from D1-02 candidate synthesis.  
**Notes:** Discovery artifact SHA-256 `822431d664d5a35949abdf230a1b8abb41afa1f97511b7c129e5d18779f2e284`; compact evidence in `research/evidence/E001_D0_observations.json`. D1-02 preserved the refutation exactly; no width, alignment, range, or criterion change was considered.

### OBS-005

**Title:** Shift 900 uniquely maximizes D6 translation overlap within odd-radical class 15  
**Status:** REFUTED  
**Date:** 2026-10-06  
**Experiment:** E006 / SQ-006  
**Exact definition:** Under the frozen E006 semantics, let C_B(h) count all prime pairs (p,p+h) with even h in {2,4,...,1000} and common left anchor p in [L,U-1000). Let rho(h) be the odd radical. On D6, among exactly the frozen shifts with rho(h)=15, h=900 has strictly greater C_D6(h) than every other class member.  
**Discovery range:** D6 = [42_000_000, 43_000_000)  
**Holdout range:** H6 = [44_000_000, 45_000_000), untouched at promotion  
**Observation:** The rho=15 class has 19 members. C_D6(900)=11,503; the deterministic runner-up count is 11,440, so the strict dominance margin is 63.  
**Triviality checks:** Parity is fixed by the all-even shift set and the odd-radical class fixes the frozen deterministic two-point modular-admissibility profile. The claim compares counts only within that control class; it is not a parity/radical identity, common-anchor/boundary consequence, serialization/tie-break consequence, cross-class comparison, or consecutive-gap statement. The maximum is strict by exact counts.  
**Replication result:** REFUTED on one-shot H6 = `[44_000_000, 45_000_000)`. `C_H6(900)=11,397`, satisfying the occurrence floor, but same-class shift 90 has count 11,456. The frozen strict-maximum criterion therefore fails by 59; no retargeting was performed.
**Possible mechanism:** Unknown; no mechanism work performed in D1-16.  
**Candidate link:** none  
**Notes:** Selected first by the frozen E006 promotion ranking. D6 artifact: 111,534 bytes, SHA-256 0e3e1565f3d26b221ffc17ecd8e550db445390e210213aaa27c77045e339a23c. H6 has now been executed once for frozen-criterion replication; A6 remains ungenerated. H6 artifact SHA-256 `be1694f488777be97202d9ccb047d56ba97a2d8fe087bab968090837dfc6ca3e`; compact criterion evidence in `research/evidence/E006_H6_replication.json`.

### OBS-006

**Title:** Shift 280 uniquely maximizes D6 translation overlap within odd-radical class 35  
**Status:** REFUTED  
**Date:** 2026-10-06  
**Experiment:** E006 / SQ-006  
**Exact definition:** Under the frozen E006 semantics, among exactly the frozen shifts h in {2,4,...,1000} with rho(h)=35, h=280 has strictly greater C_D6(h) than every other class member, where C_B uses the common [L,U-1000) anchor and counts all prime pairs without an adjacency requirement.  
**Discovery range:** D6 = [42_000_000, 43_000_000)  
**Holdout range:** H6 = [44_000_000, 45_000_000), untouched at promotion  
**Observation:** The rho=35 class has 8 members. C_D6(280)=6,905; runner-up 6,852; strict margin 53.  
**Triviality checks:** Same frozen exclusions as OBS-005: parity and deterministic two-point modular admissibility are controlled within class; the result is not an anchor, encoding, ordering, cross-class, or consecutive-gap consequence. The maximum is strict by exact counts.  
**Replication result:** REFUTED on one-shot H6 = `[44_000_000, 45_000_000)`. `C_H6(280)=6,776`, satisfying the occurrence floor, but same-class shift 560 has count 6,855. The frozen strict-maximum criterion therefore fails by 79; no retargeting was performed.
**Possible mechanism:** Unknown; no mechanism work performed.  
**Candidate link:** none  
**Notes:** Selected second by the frozen ranking. D6 artifact SHA-256 0e3e1565f3d26b221ffc17ecd8e550db445390e210213aaa27c77045e339a23c. H6 has now been executed once for frozen-criterion replication; A6 remains ungenerated. H6 artifact SHA-256 `be1694f488777be97202d9ccb047d56ba97a2d8fe087bab968090837dfc6ca3e`; compact criterion evidence in `research/evidence/E006_H6_replication.json`.

### OBS-007

**Title:** Shift 56 uniquely maximizes D6 translation overlap within odd-radical class 7  
**Status:** REFUTED  
**Date:** 2026-10-06  
**Experiment:** E006 / SQ-006  
**Exact definition:** Under frozen E006, among exactly the frozen shifts with rho(h)=7, h=56 has strictly greater D6 common-anchor all-pairs translation-overlap count than every other class member.  
**Discovery range:** D6 = [42_000_000, 43_000_000)  
**Holdout range:** H6 = [44_000_000, 45_000_000), untouched at promotion  
**Observation:** The rho=7 class has 12 members. C_D6(56)=5,225; runner-up 5,184; strict margin 41.  
**Triviality checks:** Same frozen within-class parity/radical, anchor/boundary, encoding/ordering, cross-class, and adjacency exclusions as OBS-005. The maximum is strict by exact counts.  
**Replication result:** REFUTED on one-shot H6 = `[44_000_000, 45_000_000)`. `C_H6(56)=5,047`, satisfying the occurrence floor, but same-class shift 28 has count 5,179. The frozen strict-maximum criterion therefore fails by 132; no retargeting was performed.
**Possible mechanism:** Unknown; no mechanism work performed.  
**Candidate link:** none  
**Notes:** Selected third by the frozen ranking. D6 artifact SHA-256 0e3e1565f3d26b221ffc17ecd8e550db445390e210213aaa27c77045e339a23c. H6 has now been executed once for frozen-criterion replication; A6 remains ungenerated. H6 artifact SHA-256 `be1694f488777be97202d9ccb047d56ba97a2d8fe087bab968090837dfc6ca3e`; compact criterion evidence in `research/evidence/E006_H6_replication.json`.

### OBS-008

**Title:** Shift 294 uniquely maximizes D6 translation overlap within odd-radical class 21  
**Status:** REPLICATED  
**Date:** 2026-10-06  
**Experiment:** E006 / SQ-006  
**Exact definition:** Under frozen E006, among exactly the frozen shifts with rho(h)=21, h=294 has strictly greater D6 common-anchor all-pairs translation-overlap count than every other class member.  
**Discovery range:** D6 = [42_000_000, 43_000_000)  
**Holdout range:** H6 = [44_000_000, 45_000_000), untouched at promotion  
**Observation:** The rho=21 class has 13 members. C_D6(294)=10,373; runner-up 10,333; strict margin 40.  
**Triviality checks:** Same frozen within-class parity/radical, anchor/boundary, encoding/ordering, cross-class, and adjacency exclusions as OBS-005. The maximum is strict by exact counts.  
**Replication result:** REPLICATED on one-shot H6 = `[44_000_000, 45_000_000)`. `C_H6(294)=10,305`, and the highest same-class competitor is shift 126 at 10,301, so target 294 remains the strict unique maximum with margin 4 and satisfies the occurrence floor without tuning.
**Possible mechanism:** Unknown; no mechanism work performed.  
**Candidate link:** none — D1-18 synthesis triage found no non-arbitrary candidate statement beyond the committed D6+H6 finite evidence.  
**Notes:** Selected fourth by the frozen ranking. D1-18 considered OBS-008 alone for candidate synthesis and retained it as REPLICATED: restricting a statement to D6+H6 would only restate finite computation, while extending to any untested band/origin/width/later scale/infinite family or broader shift/class family would add an unsupported quantifier. A6 remains untouched. D6 artifact SHA-256 0e3e1565f3d26b221ffc17ecd8e550db445390e210213aaa27c77045e339a23c. H6 has now been executed once for frozen-criterion replication; A6 remains ungenerated. H6 artifact SHA-256 `be1694f488777be97202d9ccb047d56ba97a2d8fe087bab968090837dfc6ca3e`; compact criterion evidence in `research/evidence/E006_H6_replication.json`.

### OBS-009

**Title:** Shift 324 uniquely maximizes D6 translation overlap within odd-radical class 3  
**Status:** REFUTED  
**Date:** 2026-10-06  
**Experiment:** E006 / SQ-006  
**Exact definition:** Under frozen E006, among exactly the frozen shifts with rho(h)=3, h=324 has strictly greater D6 common-anchor all-pairs translation-overlap count than every other class member.  
**Discovery range:** D6 = [42_000_000, 43_000_000)  
**Holdout range:** H6 = [44_000_000, 45_000_000), untouched at promotion  
**Observation:** The rho=3 class has 24 members. C_D6(324)=8,675; runner-up 8,643; strict margin 32.  
**Triviality checks:** Same frozen within-class parity/radical, anchor/boundary, encoding/ordering, cross-class, and adjacency exclusions as OBS-005. The maximum is strict by exact counts.  
**Replication result:** REFUTED on one-shot H6 = `[44_000_000, 45_000_000)`. `C_H6(324)=8,527`, satisfying the occurrence floor, but same-class shift 216 has count 8,667. The frozen strict-maximum criterion therefore fails by 140; no retargeting was performed.
**Possible mechanism:** Unknown; no mechanism work performed.  
**Candidate link:** none  
**Notes:** Selected fifth by the frozen ranking. D6 artifact SHA-256 0e3e1565f3d26b221ffc17ecd8e550db445390e210213aaa27c77045e339a23c. H6 has now been executed once for frozen-criterion replication; A6 remains ungenerated. H6 artifact SHA-256 `be1694f488777be97202d9ccb047d56ba97a2d8fe087bab968090837dfc6ca3e`; compact criterion evidence in `research/evidence/E006_H6_replication.json`.

### OBS-010

**Title:** `[3,3]` is the unique F2 distinct-factor-count pair mode on D7  
**Status:** REPLICATED  
**Date:** 2026-10-06  
**Experiment:** E007 / SQ-007  
**Exact definition:** Under frozen E007, for every prime anchor `x` in the common odd-anchor domain of D7, remove the complete power of two from `x-1` and `x+1`, canonically align the v2=1 neighbour as thin `T` and the other as thick `K`, and let `F2(x)=(omega(o_T),omega(o_K))`. The observation is that exact signature `[3,3]` has strictly greater D7 prime-anchor frequency than every other F2 signature, occurs at least 32 times, and has strictly positive exact relative-frequency enrichment against the odd composite-anchor controls.  
**Discovery range:** D7 = `[46_000_000, 47_000_000)`  
**Holdout range:** H7 = `[48_000_000, 49_000_000)`, untouched at promotion  
**Observation:** D7 has 56,640 prime anchors and 443,359 composite controls. F2 target `[3,3]` occurs 7,740 times among prime anchors; the deterministic runner-up count is 6,364. The same target occurs 52,501 times among composite controls. Its exact enrichment numerator is `7,740*443,359 - 52,501*56,640 = 457,942,020 > 0`.  
**Triviality checks:** The claim is not the forced 2-adic thin/thick orientation, the odd-core coprimality identity, factorization reconstruction, a serialization/ranking rule, or a composite-control fact by itself. F2 is a frozen predeclared coarsening of F1; separate F2 eligibility was frozen before D7. The target survived the exact cross-family duplicate-suppression rule.  
**Replication result:** REPLICATED on one-shot H7 = `[48_000_000, 49_000_000)`. H7 has 56,387 prime anchors and 443,612 composite controls. Exact F2 target `[3,3]` occurs 7,917 times among prime anchors and remains the strict unique H7 prime-anchor mode; highest competitor `[3,2]` occurs 6,404 times. The target occurs 52,339 times among composite controls. Its exact enrichment numerator is `7,917*443,612 - 52,339*56,387 = 560,837,011 > 0`. Both population floors and the occurrence floor pass. The frozen criterion is satisfied without tuning or fallback.

**Possible mechanism:** Unknown; no mechanism work performed.  
**Candidate link:** none — D1-22 synthesis triage found no exact non-arbitrary candidate beyond the committed D7+H7 finite evidence.  
**Notes:** D7 artifact: 448,997 bytes, SHA-256 `dde63c44ed6090c0dbdd7897e440b7cbd642336c82dbc126c513acc1357f4635`; compact discovery evidence in `research/evidence/E007_D7_discovery.json`. H7 artifact: 450,687 bytes, SHA-256 `6a25381c7430a6e720e619fb27696ec75e8696514d72a8f7a26398f616d85ced`; compact criterion evidence in `research/evidence/E007_H7_replication.json`. H7 was inspected only for the frozen criterion; A7 remains ungenerated. D1-22 retained OBS-010 as REPLICATED with no candidate link: an exact D7+H7-only statement is a finite restatement, while extending F2 target `[3,3]` to untested bands, origins, widths, scales, anchors, factorization families, or infinitely many values would add an unsupported quantifier. A7 remains untouched.


### OBS-011

**Title:** `[3,3]` is the unique F3 total-multiplicity pair mode on D7  
**Status:** REPLICATED  
**Date:** 2026-10-06  
**Experiment:** E007 / SQ-007  
**Exact definition:** Under frozen E007, for every prime anchor `x` in the common odd-anchor domain of D7, remove the complete power of two from `x-1` and `x+1`, canonically align the v2=1 neighbour as thin `T` and the other as thick `K`, and let `F3(x)=(Omega(o_T),Omega(o_K))`. The observation is that exact signature `[3,3]` has strictly greater D7 prime-anchor frequency than every other F3 signature, occurs at least 32 times, and has strictly positive exact relative-frequency enrichment against the odd composite-anchor controls.  
**Discovery range:** D7 = `[46_000_000, 47_000_000)`  
**Holdout range:** H7 = `[48_000_000, 49_000_000)`, untouched at promotion  
**Observation:** D7 has 56,640 prime anchors and 443,359 composite controls. F3 target `[3,3]` occurs 5,009 times among prime anchors; the deterministic runner-up count is 3,958. The same target occurs 39,183 times among composite controls. Its exact enrichment numerator is `5,009*443,359 - 39,183*56,640 = 1,460,111 > 0`.  
**Triviality checks:** The claim is not the forced 2-adic thin/thick orientation, the odd-core coprimality identity, factorization reconstruction, a serialization/ranking rule, or a composite-control fact by itself. F3 is a frozen predeclared coarsening of F1; separate F3 eligibility was frozen before D7. Although OBS-010 and OBS-011 have the same displayed integer pair, they are different frozen families and select different D7 prime-anchor subsets, so the exact duplicate-suppression rule removes neither.  
**Replication result:** REPLICATED on one-shot H7 = `[48_000_000, 49_000_000)`. H7 has 56,387 prime anchors and 443,612 composite controls. Exact F3 target `[3,3]` occurs 5,106 times among prime anchors and remains the strict unique H7 prime-anchor mode; highest competitor `[3,2]` occurs 3,977 times. The target occurs 38,940 times among composite controls. Its exact enrichment numerator is `5,106*443,612 - 38,940*56,387 = 69,373,092 > 0`. Both population floors and the occurrence floor pass. The frozen criterion is satisfied without tuning or fallback.

**Possible mechanism:** Unknown; no mechanism work performed.  
**Candidate link:** none — D1-22 synthesis triage found no exact non-arbitrary candidate beyond the committed D7+H7 finite evidence.  
**Notes:** D7 artifact: 448,997 bytes, SHA-256 `dde63c44ed6090c0dbdd7897e440b7cbd642336c82dbc126c513acc1357f4635`; compact discovery evidence in `research/evidence/E007_D7_discovery.json`. H7 artifact: 450,687 bytes, SHA-256 `6a25381c7430a6e720e619fb27696ec75e8696514d72a8f7a26398f616d85ced`; compact criterion evidence in `research/evidence/E007_H7_replication.json`. H7 was inspected only for the frozen criterion; A7 remains ungenerated. D1-22 retained OBS-011 as REPLICATED with no candidate link: an exact D7+H7-only statement is a finite restatement, while extending F3 target `[3,3]` to untested bands, origins, widths, scales, anchors, factorization families, or infinitely many values would add an unsupported quantifier. The exact F2+F3 conjunction was also rejected as only a repackaging of the two finite observations. A7 remains untouched.

## OBS-012

**Title:** `[2,0,0,0]` is the unique C2 minimal-cover-size-profile mode on D9  
**Status:** REPLICATED  
**Date:** 2026-10-07  
**Experiment:** E009 / SQ-009  
**Exact definition:** Under frozen E009, for each Q=210-admissible prime anchor `x` in D9, compute the exact odd-anchor unit-group exponent Lambda(x), exact multiplicative orders of the ordered basis A=(2,3,5,7), all 15 nonempty basis-subset order-lcms, and the inclusion-minimal cover antichain M(x). Let C2(x)=(m1,m2,m3,m4), where mk is the number of members of M(x) of cardinality k. The observation is that exact C2 signature `[2,0,0,0]` is the strict unique D9 prime-anchor mode, occurs at least 32 times, and has strictly positive exact relative-frequency enrichment against Q-admissible composite controls.  
**Discovery range:** D9 = `[54_000_000,55_000_000)`  
**Holdout range:** H9 = `[56_000_000,57_000_000)`, untouched at promotion  
**Observation:** D9 has 55,997 prime anchors and 172,574 composite controls. C2 target `[2,0,0,0]` occurs 13,849 times among prime anchors; the deterministic runner-up count is 11,341. The same target occurs 35,767 times among composite controls. Its exact enrichment numerator is `13,849*172,574 - 35,767*55,997 = 387,132,627 > 0`.  
**Triviality checks:** The claim is not factorization reconstruction, Lambda construction, a basis-unit gcd fact, an order-divides-Lambda/minimality witness, upward cover monotonicity, minimal-antichain construction, a serialization/ranking consequence, a population/floor consequence, or a composite-control fact by itself. C2 is a frozen predeclared promotable family. C3 selected the identical D9 prime-anchor subset and was therefore suppressed mechanically in favour of lower-numbered C2; there is no fallback.  
**Frozen one-shot H9 replication criterion:** With unchanged E009 definitions and C2 semantics, H9 must have at least 1,000 prime anchors and 1,000 composite controls; exact C2 signature `[2,0,0,0]` must occur at least 32 times among H9 prime anchors and have strictly greater frequency than every competing C2 signature; and its exact H9 enrichment numerator `n_P*N_C - n_C*N_P` must be strictly positive. A tie, any higher-frequency competitor, either population-floor failure, target count below 32, or nonpositive enrichment is a mechanical failure. No fallback, retargeting, or changed semantics is permitted.  
**H9 replication result:** REPLICATED. H9 has 56,105 prime anchors and 172,466 composite controls. Frozen C2 target `[2,0,0,0]` occurs 13,900 times among H9 prime anchors, strictly above the highest competing C2 count 11,411; it occurs 35,726 times among H9 composite controls. Exact enrichment numerator: `13,900*172,466 - 35,726*56,105 = 392,870,170 > 0`. Both population floors and the 32-occurrence floor pass. No fallback or retargeting was used.  

**Possible mechanism:** Unknown; no mechanism work performed.  
**Candidate link:** none — D1-28 synthesis triage found no exact non-arbitrary candidate beyond the committed D9+H9 finite evidence.  
**Notes:** D9 artifact: 82,398 bytes, SHA-256 `a157a7b62667a76fee741db33e1cbf60594cb83aa17c54c4cbf57eb399b7cde9`; compact discovery evidence in `research/evidence/E009_D9_discovery.json`. H9 artifact: 85,386 bytes, SHA-256 `9fccccd71c49983870e226f6f03ab80bff60820874edc2fe09cfbc6fdd361126`; compact replication evidence in `research/evidence/E009_H9_replication.json`. H9 was inspected only for the frozen criterion; A9 remains ungenerated and untouched. D1-28 retained OBS-012 as REPLICATED with no candidate link: a statement confined to D9 and H9 is a finite restatement, while extending C2 target `[2,0,0,0]` to untested bands, origins, widths, scales, bases, wheels, anchor populations, representation families, or infinitely many values would add an unsupported quantifier.

## OBS-013

**Title:** the empty minimal-cover antichain is the unique C4 mode on D9  
**Status:** REPLICATED  
**Date:** 2026-10-07  
**Experiment:** E009 / SQ-009  
**Exact definition:** Under frozen E009, for each Q=210-admissible prime anchor `x` in D9, compute the exact odd-anchor unit-group exponent Lambda(x), exact multiplicative orders of A=(2,3,5,7), and the exact canonical inclusion-minimal cover antichain M(x). C4(x) is M(x) itself. The observation is that the empty antichain signature `[]`—meaning no nonempty subset of the frozen basis has order-lcm equal to Lambda(x)—is the strict unique D9 prime-anchor C4 mode, occurs at least 32 times, and has strictly positive exact relative-frequency enrichment against Q-admissible composite controls.  
**Discovery range:** D9 = `[54_000_000,55_000_000)`  
**Holdout range:** H9 = `[56_000_000,57_000_000)`, untouched at promotion  
**Observation:** D9 has 55,997 prime anchors and 172,574 composite controls. C4 target `[]` occurs 3,797 times among prime anchors; the deterministic runner-up count is 3,078. The same target occurs 5,003 times among composite controls. Its exact enrichment numerator is `3,797*172,574 - 5,003*55,997 = 375,110,487 > 0`.  
**Triviality checks:** The claim is not factorization reconstruction, Lambda construction, a basis-unit gcd fact, an order-divides-Lambda/minimality witness, upward cover monotonicity, minimal-antichain construction, a combinatorial bound, a serialization/ranking consequence, a population/floor consequence, or a composite-control fact by itself. The empty antichain is an allowed predeclared C4 signature, not a post-result exception, and the target survives exact cross-family duplicate suppression.  
**Frozen one-shot H9 replication criterion:** With unchanged E009 definitions and C4 semantics, H9 must have at least 1,000 prime anchors and 1,000 composite controls; exact C4 signature `[]` must occur at least 32 times among H9 prime anchors and have strictly greater frequency than every competing C4 signature; and its exact H9 enrichment numerator `n_P*N_C - n_C*N_P` must be strictly positive. A tie, any higher-frequency competitor, either population-floor failure, target count below 32, or nonpositive enrichment is a mechanical failure. No fallback, retargeting, or changed semantics is permitted.  
**H9 replication result:** REPLICATED. H9 has 56,105 prime anchors and 172,466 composite controls. Frozen C4 target `[]` occurs 3,869 times among H9 prime anchors, strictly above the highest competing C4 count 3,089; it occurs 5,075 times among H9 composite controls. Exact enrichment numerator: `3,869*172,466 - 5,075*56,105 = 382,538,079 > 0`. Both population floors and the 32-occurrence floor pass. No fallback or retargeting was used.  

**Possible mechanism:** Unknown; no mechanism work performed.  
**Candidate link:** none — D1-28 synthesis triage found no exact non-arbitrary candidate beyond the committed D9+H9 finite evidence.  
**Notes:** D9 artifact: 82,398 bytes, SHA-256 `a157a7b62667a76fee741db33e1cbf60594cb83aa17c54c4cbf57eb399b7cde9`; compact discovery evidence in `research/evidence/E009_D9_discovery.json`. H9 artifact: 85,386 bytes, SHA-256 `9fccccd71c49983870e226f6f03ab80bff60820874edc2fe09cfbc6fdd361126`; compact replication evidence in `research/evidence/E009_H9_replication.json`. H9 was inspected only for the frozen criterion; A9 remains ungenerated and untouched. D1-28 retained OBS-013 as REPLICATED with no candidate link: a statement confined to D9 and H9 is a finite restatement, while extending C4 target `[]` to persistence, eventuality, universality, untested bands/scales/bases/wheels, broader families, or infinitely many values would add unsupported structure. The permitted C2+C4 conjunction was also rejected as only a packaging of the two finite observations.

## OBS-014

**Title:** `1487` is the unique L2 distinct-denominator-count mode on D10  
**Status:** REFUTED  
**Date:** 2026-10-07  
**Experiment:** E010 / SQ-010  
**Exact definition:** Under frozen E010, for every Q=210-admissible nonsquare prime anchor `x` in D10, compute the exact integer quadratic-surd recurrence for `sqrt(x)` through the first canonical terminal state `(a0,1,2*a0)`, form the exact denominator cycle `D(x)=(d_1,...,d_ell)` including terminal denominator 1, and let `L2(x)` be the number of distinct denominator values appearing in that cycle. The observation is that exact L2 signature `1487` is the strict unique D10 prime-anchor mode, occurs at least 32 times, and has strictly positive exact relative-frequency enrichment against Q=210-admissible nonsquare composite controls.  
**Discovery range:** D10 = `[58_000_000,59_000_000)`  
**Holdout range:** H10 = `[60_000_000,61_000_000)`, untouched at promotion  
**Observation:** D10 has 55,978 prime anchors and 172,580 composite controls after the common Q-admissible nonsquare filter. L2 target `1487` occurs 44 times among prime anchors; the deterministic runner-up count is 40. The same target occurs 53 times among composite controls. Its exact enrichment numerator is `44*172,580 - 53*55,978 = 4,626,686 > 0`. Both population floors and the 32-occurrence floor pass.  
**Triviality checks:** The claim is not the Q=210 admissibility condition, perfect-square exclusion, exact isqrt bracket, recurrence positivity/divisibility or quotient identity, canonical termination, nonterminal-repeat exclusion, terminal denominator identity, a denominator-profile identity, a serialization/ranking consequence, a population/floor consequence, or a composite-control fact by itself. L2 is a frozen predeclared promotable family. L1 and L4 fail the frozen occurrence floor and L3 fails positive enrichment, so no cross-family duplicate suppresses L2 and no fallback target is used.  
**Frozen one-shot H10 replication criterion:** With unchanged E010 definitions and L2 semantics, H10 must have at least 1,000 prime anchors and 1,000 Q-admissible nonsquare composite controls; exact L2 signature `1487` must occur at least 32 times among H10 prime anchors and have strictly greater frequency than every competing L2 signature; and its exact H10 enrichment numerator `n_P*N_C - n_C*N_P` must be strictly positive. A tie, any higher-frequency competitor, either population-floor failure, target count below 32, or nonpositive enrichment is a mechanical failure. No fallback, retargeting, family replacement, threshold or normalization change, recurrence change, or control-population change is permitted.  
**Replication result:** **REFUTED.** H10 has 55,930 prime anchors and 172,626 Q-admissible nonsquare composite controls. Frozen L2 target `1487` occurs 20 times among H10 prime anchors, below the frozen 32-occurrence floor, and the highest competing L2 prime count is 41, so `1487` is not the strict unique H10 L2 prime-anchor mode. The target occurs 50 times among H10 composite controls. Exact enrichment remains positive: `20*172626 - 50*55930 = 656,020 > 0`. Population floors and enrichment pass, but occurrence and strict-unique-mode fail; the conjunctive frozen criterion therefore fails mechanically. No competing signature identity was inspected or serialized; no fallback or retargeting was used.  
**Possible mechanism:** Unknown; no mechanism work performed.  
**Candidate link:** none — OBS-014 failed its frozen one-shot H10 criterion, so it is ineligible to seed candidate synthesis.  
**Notes:** D10 artifact: 52,653,877 bytes, SHA-256 `52c7be1bd4ba53eb78596fa7a0738a412742d10d31583a574901d47f1915ce74`; compact discovery evidence in `research/evidence/E010_D10_discovery.json`. The identical complete D10 command ran twice on implementation checkpoint `e9ab511a06e612792cbf95953d2e1b71307fb40f` before descriptive inspection. H10 replication artifact: 1,003 bytes, SHA-256 `8730125952a015951d4e2fa698e3e354ba59b03b0d5d1d3f29fb93c2f5d88ad9`; compact criterion-only evidence in `research/evidence/E010_H10_replication.json` and execution record in `experiments/E010_H10_REPLICATION_2026-10-07.md`. H10 is now consumed replication evidence. A10 remains ungenerated, untouched, uninspected, and unexecuted; A9 and every historical protected range retain their prior frozen roles.
