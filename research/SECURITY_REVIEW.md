# Security, Privacy, Membership, and Post-Quantum Cryptography Review

**Deliverable:** `research/SECURITY_REVIEW.md`
**Status:** Working Draft (fourth refinement: technology stack, 7 November 2026)
**Canonical text:** `book/dpep_book.tex` Chapters 5 and 7. Earlier passes are kept below as a historical record.

---

## Fourth refinement (technology stack)

Dispositions: `research/FOURTH_REFINEMENT_DISPOSITIONS.md`. Scripts: `research/analysis/verify_signature_suites.py`, `verify_r3.py` §H, `verify_sync_committee.py`, `bench_signatures/`.

### Signature sizes (corrected)

ML-DSA-65 signatures are 3,309 B (FIPS 204; confirmed by `libcrux-ml-dsa` 0.0.11). The hybrid Ed25519 + ML-DSA-65 composite of RFC 10073 concatenates the two: 3,373 B. Council-proposal sizes previously used 3,437 B per signer, which added a second Ed25519 signature; corrected throughout (Table 5.2, Table 7.9, P12, `verify_sync_committee.py`). Checkpoint figures already used 3,373 B and are unchanged.

### Tiered signature policy (proposed)

| Object class | Construction | Rationale |
|---|---|---|
| Confidentiality (transport, Prio3 shares) | Hybrid X25519 + ML-KEM-768 | Harvest-now-decrypt-later; unchanged |
| Per-round objects (council proposals, receipts, round checkpoints) | Ed25519; aggregated BLS12-381 or 86 Ed25519 for validators/witnesses; roots anchored post-quantum within 24 h of round close by 3-of-5 federation SLH-DSA signatures (BFT: 48.7 kB per block, 20.7 MB/yr) or 11-of-16 ML-DSA-44 witness cosignatures (log: 26.8 kB, 11.4 MB/yr, plus an annual 3-of-5 SLH-DSA backstop) | Matter only for one round and its challenge window; anchoring bounds rewriting of history |
| Long-lived objects (accreditation, CapCerts, roster roots, WASM hashes, annual ratification) | Hybrid (RFC 10073) or SLH-DSA | Long validity |

Effects (`verify_signature_suites.py`): phone full checkpoint check 290 kB → 5.5 kB (Ed25519) / 112 B (BLS, only where the engine or log aggregates; CometBFT does not); checkpoint block 700 kB → 416 kB / 410 kB; Layer 1 298 → 177 / 174 MB/yr; coarse archive with five signers 775 MB → 113 MB per round. Phone traffic per round: 21–46 kB automated, 76–101 kB milestone (was 306–386 kB with hybrid full checks).

Residual risk: a covert CRQC before a migration trigger could forge live round objects; migration of many devices needs rehearsal. All-hybrid would resist the first.

### Follow-up fixes (7 November 2026)

- **Distributed anchor.** A single federation SLH-DSA key replaced by k-of-n anchoring (Table 7.3 in the book): BFT design 3-of-5 federation SLH-DSA (48,673 B per block, 20.7 MB/yr); log design 11-of-16 ML-DSA-44 witness cosignatures (26,752 B, 11.4 MB/yr) plus an annual 3-of-5 SLH-DSA backstop over the year's log root (0.05 MB/yr). Anchor-key custody added to §7.7 and to the trust map; unspecified.
- **S7 overspend bound.** Per-depot caps would give cap × depots visited. Pilot design now: rationed goods checked online when possible, offline only at the home depot, so the bound is one cap per person per day. A secure-hardware spend counter is left for later study (vendor trust; phones without secure hardware).

### Verification load (measured)

Apple M4 Pro, one core: ML-DSA-65 verify 32.2 µs; Ed25519 17.3 µs (8.7 µs in batches of 64); hybrid 49.5 µs; aggregated BLS of 86 signers 0.45 ms. 200,000 hybrid verifications: 9.9 s; ML-DSA alone on 14 threads: 0.66 s. On a desktop, size rather than CPU is the cost; Raspberry Pi and community-server timings remain a Kill Gate 2 measurement and could change this for small federations.

### Layer 1

Witnessed log (C2SP) added as an option beside BFT checkpoints; both tested at Kill Gate 2. Log liveness rests on one operator per round (institutional replacement). CometBFT v0.40.0 offers a BLS key type only behind a build flag and does not aggregate votes.

### Aggregators

DAP draft-20 requires exactly two aggregators; K = 3 means a DPEP-original protocol (+$40k–$95k, wider audit). Proposed: K = 2 on DAP (Janus) for pilots; K = 3 only if a governance case is shown. Privacy needs one of two honest; correctness needs both. A custom budget circuit needs server changes either way; libprio 0.18.1 supports user-defined circuits.

### Intra-year fulfilment (S7)

New §7.5: requirements, three candidate designs (attributed receipts with credit cap; anonymous tokens; council-level allocation for staples), daily rollup, and a pilot recommendation. **The household privacy claim is narrowed to annual requests**; point-of-use privacy is open (P16, Kill Gate 3(d), CLM-SEC-13). GNU Taler's offline design was abandoned, so offline anonymous tokens remain research-grade.

### Clients, distribution, notifications

A PWA cannot reach hardware keystores; WebCrypto PQ is a WICG draft (Chrome experiment only); Safari lacks Background Sync. Native Kotlin/Swift clients over the Rust core are proposed as primary. App-store removal and push metadata added to the threat model; mitigations: F-Droid and direct APK, reproducible client builds, content-free notifications.

---

# Historical record (earlier passes)

## Third refinement

### R3-08: Prio3 benchmark (run)

`research/analysis/bench_prio3/` uses `prio` 0.18.1, which implements **VDAF draft 18** (crate README), not draft 22; the `Prio3SumVec` encoding is the same layout. Prio3SumVec, 3 aggregators, Field128, `chunk_length` from libprio's `optimal_chunk_length`. Medians of 30 runs on one core of an Apple M4 Pro (macOS 26.6.2, rustc/cargo 1.98.1, `--release`, thin LTO).

| Length × bits | Leader share | Upload | Shard | verify_init leader | verify_init helper |
|---|---|---|---|---|---|
| 100×20 | 35,088 B | 35,312 B | 0.55 ms | 0.21 ms | 0.23 ms |
| 100×32 | 54,896 B | 55,120 B | 0.65 ms | 0.21 ms | 0.22 ms |
| 100×64 | 107,728 B | 107,952 B | 1.13 ms | 0.30 ms | 0.32 ms |
| 230×20 | 78,032 B | 78,256 B | 0.81 ms | 0.23 ms | 0.25 ms |
| 230×32 | 123,568 B | 123,792 B | 1.28 ms | 0.33 ms | 0.35 ms |
| 230×64 | 243,344 B | 243,568 B | 2.52 ms | 0.82 ms | 0.86 ms |
| 3000×20 | 975,760 B | 975,984 B | 10.6 ms | 3.46 ms | 3.64 ms |
| 3000×32 | 1,556,272 B | 1,556,496 B | 16.2 ms | 4.85 ms | 5.21 ms |
| 3000×64 | 3,100,432 B | 3,100,656 B | 33.3 ms | 12.0 ms | 12.7 ms |

Helper shares 64 B; public share 96 B; combining verifier shares and `verify_next` take under 5 µs. `parameters.py` now predicts all nine leader and upload sizes **byte-for-byte**. The second-pass formula used gadget arity 2 instead of `2·chunk_length` and understated sizes by about 1%. The book's "1 ms per report" illustration was optimistic for dense reports even on a desktop: $10^6$ dense reports cost about 61 core-minutes per aggregator, and helpers cost as much as the leader. These are desktop numbers, not phone or Raspberry Pi results.

### R3-04: sparse row

VDAF-22 §7.4.3: "Each measurement is a vector of positive integers with length equal to the length parameter. Each element of the measurement is an integer in the range [0, max_measurement]." Coordinates are fixed, so a 50-coordinate report cannot carry 50 items chosen from 3,000 without revealing which. The row and the "fits a sparse report" claim are removed.

### R3-05: units

At the fixed $10^{-6}$ scale, $b$ bits express at most $(2^b-1)/10^6$ units: 0.066 (16 bits), 1.05 (20 bits), 4,295 (32 bits). The book now defines a per-category Household Reporting Unit (HRU, 16 bits, integer scale $s_g$ micro-units per HRU). Conversion to protocol totals is exact; rounding happens once at the client (≤ ½ HRU per category per person; aggregate s.d. $s_g\sqrt{N/12}$). Size tables now come from the benchmark. Per-year upload: 9.8 MB for ten dense reports against 0.17 MB for three coarse milestone reports.

### R3-06: privacy baseline (recommendation for author ratification)

Coarse `Prio3SumVec`, 200 categories × 16-bit HRU, 55,120 B upload, about 0.25 ms per verification, as the household-crypto baseline. Council-level trust (no household cryptography) for Phase 1H and the first Phase 3 pilots. Dense 3,000 is not a baseline. This is tied to P5, P13 and Kill Gate 3 in the book.

### R3-07: prices, carry-forward, replay

- The budget predicate depends on $P^{(t)}$, which must be circuit constants, so there is one VDAF instance per price vector. `ctx` binds epoch, round, price hash and aggregator set, but does not enter the arithmetic.
- **VDAF-22 §7.2.3: "Prio3 only permits a report to be aggregated once"; §9.4: re-aggregation "risks re-using correlated randomness, which might compromise confidentiality".** Carrying individual reports into later rounds, and re-running a round from stored reports with a replacement aggregator, are therefore not available as specified. The reviewer did not raise this; it is the strongest reason to change the carry-forward design.
- Proposed rule: fresh budget-checked reports at milestone rounds (t = 1, 4, 8); between milestones, aggregate shares are reused as constants and an aggregate check is applied at current prices with tolerance κ = 5%; offline people are counted at their council's per-capita average and flagged. Nonces are retained per epoch for replay rejection (§9.2). Input shares are retained encrypted until $T_{challenge}$ (proposed 14 days), then deleted. This reconciles "ephemeral shares" (§11.2) with retention (§7.5).

### R3-09: credentials and correctness

- Present-tense credential claims (§7.3) are reworded as an unbuilt design goal. The only other present-tense instance found was §11.2 GDPR ("using ephemeral Prio3 shares"), which is reworded.
- BBS signatures are pairing-based, so a "post-quantum adaptation of BBS-style" credential is not an established object. Lattice-based anonymous credentials are research without a standard. Checking a credential inside an FLP circuit is unrealistic (signature or hash verification is a large circuit, and the credential would have to be secret-shared). Proposed: verify at upload outside the VDAF with a per-epoch nullifier, bound to the report by nonce/`ctx`; binding the secret-shared $B_u$ remains open.
- The public check $p\cdot\sum y\le\sum B_u$ cannot detect category shifting, permits inflation up to unspent budget, and cannot detect deflation at all.
- Recommended for Phase 3 (proposed): three **non-nested** aggregators from organisations with different interests, plus the public check and published aggregate-share commitments. Nested CC/Ward/Federation should not be the default. Robust MPC is deferred.
- Individual wallets versus household reports: $u$ is now defined as one budget-holding person throughout.

### R3-10 / R3-11: proposal sizes and light clients

The 5.2 kB proposal minus one 3,373 B signature leaves 1,827 B, about 152 items at 12 B. A neighbourhood's sum over 3,000 goods is about 36 kB, and each extra multi-signature signer adds 3,437 B (hybrid). Councils use k-of-n multi-signatures until a PQ threshold scheme exists (Table 7.1 note; P12). Round archive at $10^6$: 0.24-1.46 GB raw; 40k-200k signature verifications per round; per-signature time not benchmarked here, so the old 9-27 s figure is withdrawn and Kill Gate 2 measures it. Light-client options are tabulated (all 86 signatures at 296 kB; coordinator attestation at 3.4 kB; sampling 8 at 27 kB, with an all-pass probability of (42/86)^8 ≈ 0.3% if only the corrupt minority really signed; full checks at milestones). Proposed mobile cap: ≤150 kB per ordinary round and ≤450 kB per full-verification round.

### Table 7.1

The caption now says the latency columns are placeholders; they are marked ᵖ, and the ~80 µs hybrid KEM figure is flagged as optimistic. No device benchmark was run; ML-KEM and ML-DSA were not benchmarked in this pass.

---

# Historical record (earlier passes)

# Security, Privacy, Membership, and Post-Quantum Cryptography Review

**Deliverable:** `research/SECURITY_REVIEW.md`  
**Status:** Working Draft (corrected 4 November 2026, second refinement)  
**Canonical text:** `book/dpep_book.tex` Chapters 5 and 7. This file is a working note; where it conflicts with the book, the book wins.

**Withdrawn figures in this note:** “100% Binding / 100% Post-Quantum / zero lattice”; “18–35 KB” and “<15 ms” `Prio3` costs; “uniform NIST Level 3” including BLAKE3; VDAF-16 as a Category A standard; 1-of-3 privacy as if it were correctness; n=64 / 145 KB / 616 KB after n=128. See `research/analysis/parameters.py`, `verify_r2.py`, and `SECOND_REFINEMENT_DISPOSITIONS.md` (R2-01–R2-08, R2-20, R2-22).

**VDAF-22 §9 (HTML, IETF Datatracker, accessed this pass):** privacy needs one honest aggregator; an aggregator can modify its aggregate share undetected; DP and Sybil/rate-limits are out of scope; no post-quantum claim. Report sizes: Field128 `Prio3SumVec`, `MEAS_LEN = length × bits`; leader share is the full measurement, helpers are seeds.

**Threat model, equivocation, recovery, ballots, sortition beacon, and $B_u$ credentials** are now in the monograph (§7). They remain largely **Open**.

---

# Historical note (first-pass text below; do not quote the 18–35 KB / 100% rows)

---

## 1. Critical Cryptographic Vulnerabilities in Naive Privacy Sketches and Their Remediation

### 1.1 The Unbound Commitment-to-Mask Flaw (`R-SEC-01` — Most Serious Cryptographic Bug)
- **The Flaw in an Unbound Sketch:** In an initial sketch of Chapter 7 (Section 7.3), each household $u$ generated a zero-knowledge proof $\Pi_u$ that its committed consumption vector $C_u = \text{Com}(y_u^{\text{priv}}; r_u)$ satisfied $y_{u,g}^{\text{priv}} \ge 0$ and $p^{\text{priv}} \cdot y_u^{\text{priv}} + \text{PubShare}_u \le B_u$, while separately submitting a pairwise-masked vector $\tilde{y}_u = y_u^{\text{priv}} + m_u \pmod q$ to the neighbourhood coordinator. **Nothing bound the committed vector inside $C_u$ to the masked vector $\tilde{y}_u$!** A malicious household could commit to $y_u^{\text{priv}} = \mathbf{0}$ (trivially passing the budget proof $\Pi_u$) while submitting $\tilde{y}_u = 10^6 \cdot \mathbf{1} + m_u$, injecting arbitrary unbacked demand into the council sum $y_h^{\text{priv}} = \sum_{u=1}^m \tilde{y}_u$ undetected!
- **Why Simple Sum-of-Commitments Fails Under Pairwise Masking unless Masks Are Also Committed:** If $\tilde{y}_u = y_u^{\text{priv}} + \sum_{v \ne u} s_{u,v} \mathbf{r}_{u,v}$ (where $s_{u,v} = -s_{v,u}$), the coordinator only learns the sum $y_h^{\text{priv}} = \sum_u \tilde{y}_u$ after all $m$ masked vectors are summed, and if the sum fails to match $\sum_u C_u$, the coordinator **cannot identify which household cheated** ("cheater identification / blame attribution failure")!
- **Remediation Comparison (Four Validated-Aggregation Architectures):**

| Validated-Aggregation Architecture | How Input Validity Is Bound to the Counted Share | Dropout Resilience | Post-Quantum Status | Bandwidth & Prover Cost ($G_{\text{priv}} = 3,000, s = 50$) | Trust Assumption |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Option A: IETF CFRG `Prio3` / VDAF (`draft-irtf-cfrg-vdaf-16`)** (Corrigan-Gibbs & Boneh 2017; Boneh et al. 2019) | Household splits $y_u^{\text{priv}}$ into $K \ge 2$ additive secret shares $y_u = y_{u,1} + \dots + y_{u,K} \pmod q$ sent to $K$ non-colluding Council/Ward Aggregators, accompanied by a **Fully Linear Proof (FLP)** (information-theoretic PCP over finite fields) verifying $y_{u,g} \in [0, Y_{\max}]$ and $p \cdot y_u \le B_u$ directly on the shares! | **100% Dropout Resilient:** Each household submission is verified and summed independently; if household $u$ is offline, other households' shares still sum cleanly! | **100% Post-Quantum:** Relies *only* on finite-field secret sharing, PRGs (AES/SHAKE256), and authenticated channels (`X25519MLKEM768`). Zero lattice/pairing/FRI conjectures needed! | Share + FLP proof size: **$\sim 18\text{–}35\text{ KB}$**; mobile proving time: **$< 15\text{ ms}$** (pure finite-field arithmetic); rejects malformed inputs *before* aggregation. | **Any-1-of-$K$ Honest Aggregator ($1$-out-of-$K$ privacy):** Privacy holds as long as at least 1 of the $K$ (e.g., $K=3$: Neighbourhood, Ward, and Consumer Federation) aggregators does not collude to reconstruct $y_u$. |
| **Option B: RoFL / EIFFeL / ACORN** (Lycklama et al. 2023; Chowdhury et al. 2022; Bell et al. 2023) | Binds pairwise masks $m_u = \sum_{v} \text{PRG}(k_{u,v})$ to homomorphic Pedersen/lattice commitments $C_u^{\text{mask}}$ so the coordinator verifies $C_u^{\text{masked\_input}} = C_u \cdot C_u^{\text{mask}}$ before summing, plus Bulletproofs/lattice range proofs. | Requires multi-round Shamir key-share recovery (Bonawitz et al. 2017, 4 rounds) whenever any peer drops out mid-round (`R-SEC-02`). | Classical Pedersen/Bulletproofs broken by CRQC; lattice-based ACORN requires heavy Module-SIS proofs (~100–300 KB). | Dense vector + commitments + range proofs: **$\sim 95\text{–}250\text{ KB}$** per household per round; multi-round interactive dropout recovery. | $t$-of-$m$ honest peers in neighbourhood council. |

- **Architectural Decision:** We replace the unbound 1-round pairwise-masking + unlinked STARK sketch with **Option A (`Prio3` / VDAF over $K=3$ Federated Aggregators)** as the **primary baseline privacy architecture** (because it is 100% post-quantum, non-interactive/single-message for offline-first clients, identifies and drops invalid submissions individually, and avoids Reed-Solomon proximity-gap conjectures), while retaining **Option B (ACORN/RoFL commitment-bound masking)** as an optional research track for communities that reject the 1-of-3 non-colluding aggregator assumption.

### 1.2 Correction of Pairwise Masking & Zero-Knowledge Cost Understatements (`R-SEC-02`, `R-SEC-03`, `R-SEC-05`)
1. **Why Pairwise Masking Conflicts with Single-Round Offline-First Sync (`R-SEC-02`, `R-SEC-03`):**
   - If household $u$ masks its vector with pairwise seeds shared with 99 neighbours, and even **one** neighbour goes offline during the round, the sum $\sum \tilde{y}_u$ remains masked by random noise and is unusable unless surviving nodes execute Bonawitz et al.'s (2017) interactive 4-round Shamir secret-share recovery protocol.
   - Furthermore, `ML-KEM-768` is an interactive Key Encapsulation Mechanism (not a static Diffie-Hellman group), so establishing fresh post-quantum pairwise seeds with 99 neighbours requires $99 \times 1,120\text{ B} = \mathbf{110.9\text{ KB}}$ of ciphertexts and $\sim 8\text{ ms}$ of KEM decapsulation before PRG expansion, and the masked vector must be **dense** over all $G_{\text{priv}}$ private goods ($3,000 \times 8\text{ B} = 24\text{ KB}$, or $80\text{ KB}$ at $G_{\text{priv}} = 10,000$) because a sparse masked vector leaks the exact support of which goods household $u$ ordered!
2. **Correction of Zero-Knowledge Proof Claims and the Crites–Stewart (2025) Proximity-Gap Result (`R-SEC-05`):**
   - **Bulletproofs** rely on the discrete logarithm assumption (broken by Shor's algorithm on a CRQC) and require 64 range-proof bit commitments per item ($50 \text{ items} \times 64\text{ bits} = 3,200$ Pedersen gates, taking ~150–400 ms on mobile ARM rather than 45 ms).
   - **FRI / STARK Proximity Gaps (`Crites & Stewart, IACR ePrint 2025/2046`):** In December 2025, Elizabeth Crites and Alistair Stewart disproved the **up-to-capacity correlated agreement, mutual correlated agreement, and list-decodability conjectures** for Reed–Solomon codes (Ben-Sasson et al., *J. ACM* 2023) that underpinned aggressive parameterisations of FRI, DEEP-FRI, STIR, and WHIR. Consequently, any FRI/STARK proof used in DPEP must be parameterised strictly within the **proven Johnson / unique-decoding bound** ($\delta < 1 - \sqrt{\rho_{\text{rate}}}$ rather than the falsified up-to-capacity bound $\delta < 1 - \rho_{\text{rate}}$), which roughly doubles the number of FRI query rounds and increases STARK proof sizes from ~32 KB to **~65–110 KB**.
   - By contrast, **`Prio3` Fully Linear Proofs (FLPs)** over secret shares do not use Reed–Solomon codes or proximity-gap conjectures at all!

### 1.3 Residual Privacy Leakage Vectors (`R-SEC-04`)
Even with cryptographically sound `Prio3` VDAF aggregation, four structural privacy leaks remain and are explicitly documented in the DPEP threat model:
1. **Sybil Stuffing / Coordinator Isolation Attack:** If a malicious neighbourhood coordinator stuffs $m-1$ controlled accounts with known zero vectors into a batch, the aggregate sum reveals the single target household's vector. *Mitigation:* Aggregators enforce a minimum batch quorum ($m_{\min} \ge 30$ distinct hardware/residency-attested council members) before releasing any aggregate sum.
2. **Differential Round-to-Round Dropout Inference:** If 100 households participate in Round 1 and 99 in Round 2, differencing $y_h^{(2)} - y_h^{(1)}$ leaks information about the dropped household. *Mitigation:* If a registered household does not submit an update in Round $t$, its prior-round secret shares are automatically carried forward (adjusted proportionally to price changes) so the active anonymity set remains constant across rounds.
3. **Rare / Niche Goods in Small Councils:** If only 1 person in a 50-household council orders a specialized item, the cleartext neighbourhood sum reveals that someone in the neighbourhood ordered it. *Mitigation:* Items with low historical frequency (or all private goods in small councils $m < 50$) are aggregated at the **Ward Federation level ($m \ge 500$)** rather than the neighbourhood level.
4. **Budget Allowance ($B_u$) Linkability & Physical Depot Pickups:** Because $B_u$ reflects effort rating $\epsilon_u$, CAP compensation, and social allowances, proving $p \cdot y_u \le B_u$ requires $B_u$ to be committed inside the `Prio3` circuit via an aggregator-blinded credential rather than published in cleartext; and physical pickups at distribution depots use **category-level unlinkable blind tokens** rather than item-level identity logs.

---

## 2. Rigorous Protocol for Distributed Aggregation & Censorship Resistance (Section 5; `R-SEC-06`, `R-SEC-09`, `R-SEC-11`)

### 2.1 Separating Seven Distinct Security Properties (`R-SEC-06`)
Rather than conflating distinct properties under the label "Merkle-Sum Tree verification," DPEP strictly separates them:

| Property | Precise Definition | What Provides It (or Cannot Provide It) in DPEP |
| :--- | :--- | :--- |
| **1. Authenticity** | A proposal $\pi_c^{(t)}$ was signed by an authorised quorum of council $c$'s registered keys for round $t$. | Hybrid `Ed25519 + ML-DSA-65` council signature over canonical domain-separated bytes. |
| **2. Data Integrity** | Once included in a committed tree root `H_root`, no quantity in $\pi_c^{(t)}$ can be altered without changing `H_root`. | `BLAKE3-256` collision resistance. |
| **3. Inclusion Verification** | Council $c$ can verify that its specific proposal $\pi_c^{(t)}$ was included at leaf $c$ of `H_root`. | Merkle inclusion path of sibling hashes from leaf $c$ to `H_root`. |
| **4. Arithmetic Conservation (No Phantom Negative/Positive Injection)** | The root vector $S^E, D^E$ equals the exact sum of the leaves in the tree, with no negative quantities injected at hidden sibling leaves. | **Critical Distinction (`R-SEC-06`):** A local Merkle-Sum inclusion path only checks the nodes *along council $c$'s path to the root*—it does **not** prove that two sibling subtrees off-path weren't fabricated or inflated by a dishonest aggregator unless the internal sums are verified from the leaves up! |
| **5. Completeness (Non-Omission)** | *Every* eligible council that submitted a valid proposal before the round deadline is included in `H_root`. | An inclusion proof for council $c$ says nothing about whether council $c'$ was omitted; completeness requires **Accredited Council Roster Bitmaps + Signed Submission Receipts + Challenge Windows**. |
| **6. Data Availability** | Any auditor or council node can fetch the underlying council proposals that produced `H_root` to verify the sum independently. | Requires **Data Availability (DA) sampling / full leaf broadcast** across `Role-SR` federation replicas ($40,000 \text{ councils} \times 5.2\text{ KB} \approx 208\text{ MB}$ total per round—small enough that *every* regional `Role-SR` and `Role-BFT` node downloads and verifies all leaf proposals directly!). |
| **7. Economic & Physical Truthfulness (`R-SEC-11`)** | Reported capacities, effort hours, deliveries, and emissions match physical reality. | **Cannot be proven by cryptography.** Requires physical inventory spot-checks (*euthynai*), sensor cross-audits, and counterparty mass-balance reconciliation. |

### 2.2 Why Naive Merkle-Sum Proofs Bloated to 1.28 MB—and the Simpler Authenticated Structure (`R-SEC-06`)
In `R-SEC-06`, our byte script (`verify_security_and_scoring.py`) confirmed a major flaw in naive Sparse Merkle-Sum Tree (MST) constructions:
- If every internal node of a depth-16 binary tree contains the dense 10,000-category vector sum ($10,000 \times 8\text{ B} = 80\text{ KB}$), then sending the sibling vector at each of the 16 levels of an inclusion proof requires $16 \times 80\text{ KB} = \mathbf{1.28\text{ MB}}$ per proof—violating the mobile bandwidth target by $10\times$!
- Even worse, if the total raw size of all 40,000 council proposals in a round is only $40,000 \times 5.2\text{ KB} \approx \mathbf{208\text{ MB}}$ (or $\sim 60\text{ MB}$ compressed), then **every `Role-PCW` and `Role-BFT` server can simply download all 40,000 signed sparse council proposals, verify every signature, and sum the vectors directly in $< 0.2\text{ seconds}$!**
- **How Light Clients (`Role-LP` on Mobile Phones) Verify Inclusion in $< 1\text{ KB}$:**
  We replace the heavy multi-vector MST node format with a **Two-Root Authenticated Aggregation Structure**:
  1. **`proposals_merkle_root` ($32\text{ B}$ standard BLAKE3 Merkle Tree over sorted `(council_id, Hash(canonical_proposal_bytes))`):** A mobile client verifies that its council's proposal was included using a standard 16-level BLAKE3 Merkle proof of **$16 \times 32\text{ B} = \mathbf{512\text{ bytes}}$**!
  2. **`category_totals_merkle_root` ($32\text{ B}$ Merkle Tree over the $G = 10,000$ category totals `(item_id, S_i, D_i, P_i)`):** Any `Role-PCW`, `Role-SR`, or `Role-BFT` node (or any citizen's laptop) downloads the compressed $60\text{ MB}$ round archive, verifies all 40,000 leaf signatures against `proposals_merkle_root`, and checks that their sum equals `category_totals_merkle_root`. If an aggregator miscomputes a sum, any full node publishes a **1-step Fraud Proof** (or the BFT validators refuse to sign the checkpoint block).

### 2.3 Complete 12-Step Anti-Censorship & Partition-Resilient Submission Protocol
To address all 12 requirements of Section 5:
1. **Accredited Council Roster (`R_epoch`):** At the start of each planning year, the active roster of $M$ accredited council IDs and their public keys is committed in `R_epoch`.
2. **Canonical Proposal Encoding (`R-SEC-08`):** Rather than non-canonical `proto3` wire encoding with variable `scale`, all signed messages use **RFC 8949 Canonical CBOR (CDE)** with a **fixed global scale $10^{-6}$** (`int64` micro-units, no variable `scale` field) and explicit domain-separation tags (`"DPEP-v1-PROPOSAL"`).
3. **Dual-Path Submission & Signed Receipts:** Each council submits its signed proposal $\pi_c^{(t)}$ to its primary Ward/Industry aggregator *and* gossips it to at least 2 independent `Role-SR` relays before deadline $T_{\text{submit}}$, receiving a timestamped `SubmissionReceipt` signed by any receiving relay.
4. **Explicit Participation Bitmap (`B_active` vs. `B_partitioned`):** Rather than silently carrying forward $\pi_c^{(t-1)}$ (which would make censorship indistinguishable from a network partition!), the round checkpoint header must include a $M$-bit participation bitmap classifying every council into: `01 = Fresh Signed Round-t Proposal Included`, `10 = Timeout/Partition Fallback Carry-Forward Applied`, or `00 = Missing/Excluded`.
5. **Challenge Window ($T_{\text{challenge}}$) Before Finality:** If a council sees itself marked `10` (Partitioned) or `00` when it actually submitted before $T_{\text{submit}}$, any node broadcasts its signed `SubmissionReceipt` + $\pi_c^{(t)}$ during the challenge window, forcing inclusion and slashing/rotating the censoring aggregator.

---

## 3. Validator Sortition, Security Levels, and Mobile Bandwidth (`R-SEC-08`, `R-SEC-09`, `R-SEC-10`, `R-TECH-02`)

### 3.1 Validator Committee Sortition Math and Rotation Frequency (`R-SEC-09`)
Our script `research/analysis/verify_security_and_scoring.py` confirmed that for a committee of $n = 64$ validators drawn uniformly from a pool with corrupt fraction $f_{\text{pool}}$, the probability of drawing $\ge 22$ corrupt validators ($\ge n/3$, violating BFT safety) in a **single draw** is:
- $f_{\text{pool}} = 10\%$: **`0.000012%`** ($1.2 \times 10^{-7}$)
- $f_{\text{pool}} = 20\%$: **`0.5086%`**
- $f_{\text{pool}} = 25\%$: **`5.9623%`**
- $f_{\text{pool}} = 30\%$: **`26.1727%`**

Crucially, if the committee were redrawn independently on *every* block across 435 blocks/year, a $20\%$ corrupt pool would have a $1 - (1 - 0.005086)^{435} = \mathbf{89.12\%}$ chance of corrupting at least one block during the year!
- **Remediation in DPEP:**
  1. **Annual / Per-Plan-Cycle Committee Rotation (1–4 Draws/Year, Not Per-Block):** A single sortition-elected committee serves for the entire annual planning cycle, with **ephemeral forward-secure key erasure** upon epoch handoff to prevent long-range key compromise.
  2. **Larger Committee Size ($n = 128$, fault threshold $43$) Stratified Across Regional & Industry Federations:** Increasing $n$ from $64$ to $128$ reduces the single-draw failure probability at $f_{\text{pool}} = 15\%$ from $0.017\%$ to **$0.00015\%$** while stratifying seats across geographic regions so no single captured regional federation can exceed $1/3$.
  3. **Post-Quantum VRF / Commit-Reveal Sortition (`R-SEC-08`):** Because classical elliptic-curve VRFs (ECVRF, RFC 9381) are broken by quantum computers and lattice VRFs (e.g., LB-VRF) are not yet NIST-standardised, DPEP uses a **Hash-Based Commit-Reveal + VDF/Beacon Protocol** anchored by the outgoing federation councils' `SLH-DSA` signatures, preventing last-revealer grinding.

### 3.2 Aligning NIST Security Levels and Correcting Mobile Checkpoint Bandwidth (`R-SEC-10`, `R-TECH-02`)
1. **NIST Security Level Alignment (`R-SEC-10`):**
   - To avoid mixing NIST Level 3 workhorse signatures (`ML-DSA-65`) with a Level 1 root anchor (`SLH-DSA-SHA2-128s`), DPEP uses **`SLH-DSA-SHA2-192s` (NIST FIPS 205 Level 3**: $48\text{ B}$ public key, $16,224\text{ B}$ signature), so the entire signature hierarchy achieves **uniform NIST Security Level 3**.
   - We also clarify that **BLAKE3-256** is a non-NIST cryptographic hash function (providing 256-bit classical preimage security, 128-bit classical collision security, and $\sim 128$-bit Grover preimage / $\sim 85$-bit Brassard-Høyer-Tapp quantum collision resistance), and provide **SHA3-256 / SHAKE256 (NIST FIPS 202)** as the strict FIPS-compliant hash profile.
2. **Realistic Mobile Bandwidth Budget (`R-TECH-02`):**
   - As `R-TECH-02` proved, downloading 43 individual hybrid validator signatures on every round checkpoint costs $43 \times 3,373\text{ B} = \mathbf{145.0\text{ KB}}$ before any price or proposal data is even counted!
   - Accounting honestly for: (a) 43 validator checkpoint signatures ($145\text{ KB}$), (b) Zstd-compressed price/imbalance deltas ($15\text{–}40\text{ KB}$), (c) three `Prio3` VDAF shares + FLP proofs ($3 \times 25\text{ KB} = 75\text{ KB}$), and (d) the 512-byte Merkle inclusion proof, the realistic mobile bandwidth per planning round at $N = 10^6, G = 10,000$ is **`250–400 KB / round`** (`2.5–4.0 MB` over a 10-round annual plan)—which is still effortlessly supported on 2G/3G/community Wi-Fi, without relying on false under-counting.

---

## 4. Democratic Identity, Sybil Resistance, and Constitutional Protocol Governance (Section 7; `R-SEC-07`, `R-POL-01`, `R-POL-02`, `R-POL-05`, `R-POL-06`)

### 4.1 Closing the Four Sybil Attack Vectors (`R-SEC-07`)
While phantom digital accounts in a consumer council $CC_h$ cannot mint adult work income without $WC_j$ effort certificates capped by $SB_j/SC_j$, four deeper attack vectors must be closed (`R-SEC-07`):
1. **Hours Inflation Inside a Worker Council:** Equation 4.7 caps the hours-weighted *mean* effort multiplier $\frac{\sum h_u \epsilon_u}{\sum h_u} \le \frac{SB_j}{SC_j}$, **not** total hours $\sum h_u$! If a $WC_j$ invents phantom workers to claim $2\times$ more hours $h_u$, its labour user-right charge $p^{\text{lab}} \cdot l_j$ in $SC_j$ doubles—**provided** that the labour category charge $p^{\text{lab}}_\ell$ is at least equal to the base hourly consumption payout $w_{\text{base}}$! We therefore add **Protocol Invariant `INV-4B` (Labour Endowment & Hours Conservation):** a Worker Council's total credited standard effort-hours $\sum_{u \in WC_j} h_u \epsilon_u$ cannot exceed its ratified labour endowment $\sum_\ell l_{j,\ell} \cdot (SB_j / SC_j)$, and $p^{\text{lab}}_\ell$ is floored at $w_{\text{base}}$ unless an explicit underemployment rebate is authorised by the EFB.
2. **Colluding Producer–Consumer "Carousel Fraud":** If a fake $WC_j$ and fake $CC_h$ collude, $WC_j$ could claim to deliver fictitious services to $CC_h$, inflating $SB_j$ to mint effort certificates that $CC_h$ then spends on real food and energy produced by honest councils! *Mitigation:* Cross-council bilateral clearing anomaly detection (flagging closed-loop or low-input-ratio service claims) combined with mandatory **Industry Federation physical/random *euthynai* audits** before accrediting any new $WC_j$'s output capacity.
3. **CAP & Social Allowance Inflation:** Because CAP pollution compensation $p_z^{\text{pol}} E_z$ is a **fixed lump-sum pool** for the airshed (`R-ECON-07`), adding phantom members to $CAP_z$ dilutes each member's payout $\frac{p_z^{\text{pol}} E_z}{|\text{pop}(CAP_z)|}$ rather than increasing total payout from the Society Account; however, inflating a specific neighborhood's headcount $|\text{pop}(CC_h)|$ inside a multi-neighborhood CAP or claiming fake dependent allowances ($A_u^{\text{social}}$) steals shares from neighboring councils. This requires **cross-neighborhood Ward Federation mutual audit** of residency rolls.
4. **Governance & Sortition Capture:** Even without extra consumption credits, phantom accounts would dilute 1-person-1-vote referenda and sortition pools. Therefore, sortition and federation votes are weighted by **verified council accreditation quotas** bounded by physical housing/workplace audits rather than raw unverified public keys.

### 4.2 Civil Liberties & Protection Against a Surveillance Population Register (`R-POL-06`)
Linking physical housing records (`HFB`), workplace rosters (`EFB`), public keys, and consumption allowances risks creating a coercive population register that excludes undocumented migrants, informal/transient workers, or people fleeing domestic abuse.
- **Civil-Liberties Safeguards:**
  1. **Unlinkable Credential Separation:** A citizen's residency attestation in $CC_h$ and work attestation in $WC_j$ are converted locally via blind signatures into **unlinkable epoch budget credentials**—no central database links a person's physical dwelling address to their workplace or consumption vector.
  2. **Universal Baseline Provisioning for Transients & Non-Members:** Unaffiliated residents, migrants, and individuals in transition between households receive unconditional baseline Maxim-4 allowances through autonomous community clinics and neighbourhood hospitality centres without requiring household head co-signature (preventing intra-household domestic coercion).

### 4.3 Constitutional Governance of Protocol Parameters (`R-POL-01`, `R-POL-02`)
"Verifiable neutrality" of a WASM module only proves that *a given piece of code ran faithfully*—it does not prevent a technical elite from exercising coordinator-class power by controlling *which* WASM code, product catalogue $\Omega$, ecological caps $E^{\max}$, default solver weights, or root keys are canonical!

| Protocol Lever | Who Proposes Changes | Constitutional Ratification Rule | Right of Challenge, Fork & Exit |
| :--- | :--- | :--- | :--- |
| **1. IFB WASM Price & Clearing Code (`wasm_rule_hash`)** | Open-source Technical Maintenance Worker Councils (operating under BJCs). | Dual supermajority ($\ge 2/3$) of National Consumer Federation + Congress of Industry Federations, with 60-day reproducible-build audit window. | Cannot be changed mid-planning-cycle; any regional federation can reject an unratified binary. |
| **2. Biophysical Caps ($r^*, E_z^{\max}$)** | Scientific Environmental Panels + Communities of Affected Parties ($CAP_z$). | Lexicographic Precautionary Rule: ratified in Long-Run Environmental Planning; any affected CAP can petition an Environmental Court to tighten local caps. | Explicit feasibility check detects if caps conflict with baseline human needs (`R-ECON-10`). |
| **3. Product Catalogue ($\Omega$) & Coarse Categories** | Consumer Federation R&D Task Forces + Industry Federations (Sandström 2025). | Annual pre-planning ratification (`State S0`); any council group representing $\ge 0.1\%$ of population can petition to split a coarse category. | Prevents incumbents from hiding neglected consumer needs inside coarse averages. |
| **4. Default Drafting Weights & 5-Plan Grid (`State S5`)** | Published as open protocol constants; local client defaults require **explicit user opt-in** per round (`R-POL-03`). | The 5 boundary plans in `State S5` must span a fixed symmetric grid $(\pm \Delta H^{\text{tot}}, \pm \Delta \sigma_{\text{inv}})$; councils can reject all 5 plans by simple majority to continue iterating. | Eliminates agenda-setting manipulation of late-round votes. |
| **5. Hardware-Decoupled Sortition (`R-POL-02`)** | All accredited council members are eligible for sortition regardless of whether their council owns a server. | Sortition selects **human citizen delegates/auditors first**; selected citizens are provisioned with community-hosted `Role-BFT` hardware appliances operated under their personal signing keys. | Prevents server-owning councils from monopolising BFT validator seats. |
