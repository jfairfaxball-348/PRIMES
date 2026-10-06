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

