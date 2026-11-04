# Proof-of-Concept Specification, Benchmark Programme, and Implementation Roadmap

**Deliverable:** `reports/POC_SPECIFICATION.md`  
**Phase:** 5 — Proof-of-Concept Design, Benchmarking & Roadmap  
**Scope:** Sections 12 (Proof-of-Concept Proposal), 13 (Benchmark and Simulation Programme), and 15 (Implementation Roadmap and Budget).

---

## 1. Proof-of-Concept (PoC) Design and Scenario Specification (Section 12)

### 1.1 Architectural Justification: Is a Decentralised Ledger Necessary in the PoC?

**Explicit Answer:** **A full transaction-level blockchain is unnecessary and counterproductive, both in the PoC and at scale.**  
Instead, DPEP uses **Architecture D**:
1. **99% of data and computation** (household consumption drafting, local budget proofs, workplace input-output optimization, intra-year delivery tracking, and qualitative `Lists`) stays **off-chain** in local SQLite/CRDT stores (`Role-LP`, `Role-CC`) and federated BLAKE3 Merkle-Sum Trees (`Role-PCW`).
2. **Where a decentralized ledger *is* justified:** A minimal **Epoch Checkpoint Log** (an append-only hash-chain of threshold-signed `RoundAggregationAndPrices` roots and `SocietyAccount` settlement roots) is used **solely** to:
   - Lock the global Merkle-Sum root `H_root` at the close of each planning round $t$ (preventing equivocation or retroactive proposal tampering).
   - Anchor the deterministic WASM code hash `wasm_rule_hash` of the IFB price-update rule.
   - Anchor the final ratified annual plan root (`State S6`) and year-end Society Account reconciliation (`State S9`).
   In the PoC, this Epoch Checkpoint Log is implemented as a lightweight **3-of-4 Federation Threshold-Signed Checkpoint Chain** (under 500 lines of Rust), with a clean trait interface (`EpochFinalityProvider`) that can wrap a CometBFT validator cluster in larger deployments.

---

### 1.2 Baseline PoC Simulated Economy Parameters

We treat the following figures as **initial experimental parameters** designed to exercise every institutional and mathematical feature of Albert & Hahnel (1991a, 1991b), Hahnel (2021), and Sandström (2020) on modest hardware:

| Parameter Category | PoC Experimental Configuration | Economic & Structural Details |
| :--- | :--- | :--- |
| **Total Simulated Participants ($\mathcal{I}$)** | **1,000 participants** (750 working adults, 250 dependents/retirees) | Partitioned into 400 households across 20 neighborhoods; 996 simulated via autonomous local solver processes + **4 interactive human/device seats**. |
| **Consumer Councils ($\mathcal{H}$) & Federations ($\mathcal{F}^C$)** | **20 Neighborhood Consumer Councils ($CC_1 \dots CC_{20}$)** | 50 participants (20 households) per $CC_h$, nested into **4 Ward Federations ($CF^{\text{ward}}_1 \dots CF^{\text{ward}}_4$)** (5 $CC$s each) and **1 City Federation ($CF^{\text{city}}_1$)**. |
| **Worker Councils ($\mathcal{J}$) & Federations ($\mathcal{F}^W$)** | **20 Worker Councils ($WC_1 \dots WC_{20}$)** | Averaging 37.5 workers per $WC_j$, grouped into **4 Industry Federations**: $IF_1$ (Agriculture & Food, 5 WCs), $IF_2$ (Manufacturing & Clothing, 5 WCs), $IF_3$ (Energy, Intermediate Inputs & Utilities, 5 WCs), $IF_4$ (Public Services, Construction & Transit, 5 WCs), plus **2 Regional Worker Federations**. |
| **Communities of Affected Parties ($\mathcal{C}^{\text{CAP}}$)** | **2 CAPs ($CAP_1, CAP_2$)** | $CAP_1$ (Watershed Zone A, 10 $CC$s affected by industrial effluent $z_1$); $CAP_2$ (Airshed Zone B, 20 $CC$s affected by particulate/$\text{NO}_x$ emissions $z_2$). |
| **Priced Economic Catalog ($\Omega$)** | **80 Total Categories across all 7 Classes** | - **30 Private Goods ($\mathcal{G}^{\text{priv}}$):** Food staples, apparel, electronics, household goods, cultural/recreation items.<br>- **10 Public/Collective Goods ($\mathcal{G}^{\text{pub}}$):** 4 Ward-level goods (parks, local clinics, community kitchens, libraries) + 6 City-level goods (public transit, water treatment, grid maintenance, schools, cultural center, sports complex).<br>- **15 Intermediate Inputs ($\mathcal{G}^{\text{int}}$):** Grain, textiles, steel, lumber, semiconductors, electricity, freight transport, chemical reagents, etc.<br>- **8 Natural Resources ($\mathcal{R}$):** Arable land, freshwater extraction, timber quota, solar/wind land leases, mineral ores (with hard ecological caps $r^*$).<br>- **7 Labor Categories ($\mathcal{L}$):** Agronomy, mechanical/electrical engineering, fabrication/assembly, software/administration, healthcare/caregiving, construction, logistics (organized into Balanced Job Complexes within each $WC_j$).<br>- **5 Capital Asset Stocks ($\mathcal{K}$):** Heavy machinery, transport fleet, compute/server infrastructure, industrial buildings, agricultural equipment (held in Sandström Stand-Alone Capital Asset Entities).<br>- **5 Regulated Pollutants ($\mathcal{Z}$):** Watershed nitrogen runoff ($z_1$), urban $\text{PM}_{2.5}$/$\text{NO}_x$ ($z_2$), industrial noise ($z_3$), solid waste ($z_4$), GHG carbon equivalent ($z_5$, governed by a hard environmental cap $E_{z_5}^{\max}$). |
| **Planned Slack Buffer ($SL^E$)** | **$\eta_i = 4.0\%$** for produced private and intermediate goods | Pre-planned excess supply cushion to absorb intra-year demand variance (PEPE Ch. 4 p. 67, Ch. 6 p. 113). |

---

### 1.3 End-to-End Walkthrough of the 12 Mandatory PoC Capabilities

The PoC executes a deterministic, reproducible 12-stage state machine matching `reports/ECONOMIC_MODEL.md`:

1. **Stage 1 — Council Formation and Membership (`S0`):**
   - Generates hybrid post-quantum keys (`Ed25519 + ML-DSA-65`) for all 20 $CC$s, 20 $WC$s, 4 Ward Federations, 4 Industry Federations, 2 CAPs, and the interactive participant nodes.
   - Issues `PQ-UCAN` membership credentials binding participants to their $CC_h$ and $WC_j$, initializes Balanced Job Complex (BJC) empowerment/desirability scores across the 7 labor categories, and loads initial capital endowments $k_j^0$ into Stand-Alone Capital Asset Entities.
2. **Stage 2 — Collective & Private Consumption Proposals (`S1 -> S2`):**
   - City and Ward Consumer Federations first ratify collective good bundles $y_f^{\text{pub}}$, computing per-capita budget deductions.
   - Households formulate private consumption vectors $y_u^{\text{priv}}$ using the local quadratic/conic utility solver (`Clarabel.rs` / `HiGHS`), generate a local budget compliance proof ($p^{\text{priv}} \cdot y_u^{\text{priv}} + \text{PubShare}_u \le B_u$), and aggregate them via pairwise additive masking into $CC_h$'s signed proposal $\pi_h^{(t)}$ with attached qualitative annotations.
3. **Stage 3 — Worker Council Production Proposals (`S2`):**
   - Each $WC_j$ evaluates current indicative prices $P^{(t)}$ against its multi-input production recipe (combining Leontief minimum input ratios with smooth input substitution across intermediate goods, labor categories, capital user-rights, natural resources, and pollution abatement), solving for outputs $\bar{a}_j$ and inputs $(\underline{a}_j, r_j, \Delta l_j, \Delta k_j, e_j)$ that satisfy $SB_j(P)/SC_j(P) \ge 1$.
4. **Stage 4 — Distributed Federated Aggregation (`S3`):**
   - Proposals propagate up the Ward $\to$ City and Industry Federation **BLAKE3 Sparse Merkle-Sum Trees (MST)** over QUIC (`quinn`).
   - Each council receives and verifies its compact MST inclusion proof ($O(\log M)$ hashes + vector sums) against the global round root `H_root`.
5. **Stage 5 — Indicative Price & Coordination-Signal Updates (`S4`):**
   - The IFB node executes the compiled deterministic fixed-point WASM module (`dpep_ifb_rule.wasm` in `Wasmtime`), computing aggregate excess demands $ED_i^{(t)}$, relative imbalances $\rho_i^{(t)}$, updated Society Account base wage $w_{\text{base}}^{(t+1)}$, and updated indicative prices $P^{(t+1)}$ using the safeguarded damped rule + ecological barrier constraints.
6. **Stage 6 — Iterative Plan Revision (`S2 <-> S4` Loop):**
   - Starting from an intentionally imbalanced Round 1 state (where initial consumer "wish lists" and worker comfort proposals create $>35\%$ excess demand on 60% of goods), the PoC iterates through Rounds $t = 1, 2, \dots, R$, applying proximal damping trust regions in Round $t \ge 3$ until $\max_{i \in \Omega} \rho_i^{(R)} \le 0.03$ (3% threshold).
7. **Stage 7 — Plan Feasibility & Invariant Checks (`S4 -> S6`):**
   - Automatically verifies that: (a) $\forall i \in \Omega: \rho_i^{(R)} \le 0.03$; (b) hard ecological caps $\sum_j r_j \le r^*$ and $\sum_j e_{j,z} \le E_z^{\max}$ hold with zero violation; (c) every $CC_h$ satisfies $SC_h \le B_h$ (except $CC_7$, which tests a Ward-approved special medical/accessibility need exception); and (d) every $WC_j$ satisfies $SB_j/SC_j \ge 1$ (except $WC_{14}$, which tests an Industry Federation appeal for transitional retooling).
8. **Stage 8 — Democratic Approval (`S6`):**
   - Each council casts a threshold-signed ratification ballot over the converged plan (or tests the Round-5 vote over 5 IFB-extrapolated feasible boundary plans; PEPE Ch. 4 p. 71).
9. **Stage 9 — Cryptographically Verifiable Commitments (`S6`):**
   - The 4 Federation validator nodes co-sign the `AnnualPlanCommitment` block containing the final MST root, price vector $P^*$, council allocation roots, and Society Account balance sheet.
10. **Stage 10 — Publication of the Final Plan (`S6`):**
    - Publishes the complete verifiable plan bundle to content-addressed storage and renders an interactive balance sheet of Sandström's four accounting entities (Consumers, Producers, Capital Asset Sets, Society & CAP Accounts).
11. **Stage 11 — Simulated Intra-Year Production and Consumption (`S7`):**
    - Simulates 12 monthly ticks of production deliveries and household consumption drawdowns. Demonstrates how a $\pm 12\%$ random preference shift between specific food/apparel items within $CC_1 \dots CC_5$ cancels out at Ward Federation $CF^{\text{ward}}_1$ and is absorbed within the 4% planned slack buffer $SL^E$ *without* altering any Worker Council's production target.
12. **Stage 12 — Unexpected Supply Shortage and Scoped Replanning (`S8`):**
    - In Month 6, injects an exogenous **30% supply shock** to an intermediate input (e.g., transformer/semiconductor outage at $WC_{11}$ due to storm damage), exceeding the 4% slack buffer.
    - Demonstrates the Updating Facilitation Board ($\text{UFB}$) and Industry Federation $IF_3$ running a **Scoped Sub-Graph Replanning Iteration** (`State S8`) that reallocates reserve capacity across $WC_{12}, WC_{13}$, credits overtime effort to volunteering workers, and adjusts downstream deliveries in 2 rapid sub-rounds without restarting the entire economy's annual plan.

---

### 1.4 Mandatory Multi-Device, Mobile, Offline, and Adversarial Test Suite

| Test ID | Mandatory Requirement (Section 12) | Concrete Test Execution Procedure | Pass / Acceptance Criterion |
| :--- | :--- | :--- | :--- |
| **TEST-E2E-01 (Multi-Device)** | At least two council participants operate on separate devices. | Run Coordinator + 38 councils on Device A (workstation/laptop) and `WC_1` + `CC_1` on Device B (Raspberry Pi or second computer) over LAN/WAN QUIC. | Full 12-stage planning cycle converges to identical `H_root` and $P^*$ across both physical machines. |
| **TEST-E2E-02 (Mobile Client)** | At least one participant uses a smartphone or mobile-compatible client. | Connect a real smartphone (Android/iOS running the Local-First PWA / WASM client `Role-LP`) as a member of `CC_1` over Wi-Fi/cellular. | Mobile client computes local budget optimization, generates budget compliance proof in $<250\text{ ms}$, signs ballot with hybrid PQ key, and verifies MST inclusion proof. |
| **TEST-E2E-03 (Offline & Resync)** | Demonstrate temporary disconnection and successful resynchronisation. | Sever network connection of `CC_2` (or mobile client) during Round 2; draft proposal updates and qualitative `List` edits offline in local SQLite/Loro CRDT; restore connection before Round 3 aggregation window closes. | Client syncs CRDT deltas automatically in $<2\text{ s}$ with zero data loss, submits signed Round 3 proposal, and verifies inclusion in Round 3 `H_root`. |
| **TEST-SEC-04 (Adversarial / Tampered Proposal Rejection)** | Demonstrate rejection of an unauthorised or tampered proposal. | Inject four adversarial payloads: (4a) Proposal signed by an unaccredited/revoked key; (4b) Bit-flipped quantity vector after council signature; (4c) Consumer proposal with $SC_h = 1.25 B_h$ and `requests_exception = false`; (4d) Worker proposal with negative input quantity $-50$. | Aggregator and deterministic WASM validator deterministically reject all 4 payloads with explicit cryptographic/invariant error codes (`ERR_INVALID_PQ_SIG`, `ERR_BUDGET_EXCEEDED`, `ERR_NEGATIVE_QUANTITY`) and exclude them from `H_root`. |
| **TEST-SEC-05 (Censorship Detection)** | Verify protection against malicious aggregator omission. | Configure Ward Aggregator 1 in fault-injection mode to silently drop `CC_3`'s signed proposal despite returning a receipt. | `CC_3` detects failed MST inclusion verification against `H_root`, submits its signed receipt to the Epoch Checkpoint nodes, and triggers automatic re-aggregation including `CC_3`. |

---

## 2. Benchmark and Simulation Programme (Section 13)

### 2.1 Scaling Projections Across Five Population Scales ($10^2$ to $10^6$ Participants)

The table below separates **demonstrated empirical benchmarks** (from `pequod-cljs` / Hahnel et al. 2021) from **analytical engineering projections** for the full cryptographic DPEP stack across the five required population scales.

*Assumptions for DPEP Analytical Projections:*
- Average council size: 50 participants per $CC_h$, 35 workers per $WC_j$ (at scales $\ge 1,000$; 10 per council at scale $100$).
- Active sparsity $s$: Each household/council proposal has $s = 60$ non-zero entries (out of $G$ total categories), encoded as `SparseItemVector` ($12\text{ B}$ per entry) + $3,373\text{ B}$ hybrid `Ed25519 + ML-DSA-65` signature + $1\text{ KB}$ compressed qualitative metadata $\approx \mathbf{5.2\text{ KB}}$ per signed council proposal.
- Annual planning takes $R = 10$ iterations.

| Metric | Scale 1: **100 Participants** | Scale 2: **1,000 Participants (PoC)** | Scale 3: **10,000 Participants** | Scale 4: **100,000 Participants** | Scale 5: **1,000,000 Participants** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Economic Entities ($CC_h + WC_j + \text{Fed/CAP}$)** | $10\ CC + 10\ WC + 4\text{ Fed} = \mathbf{24}$ | $20\ CC + 20\ WC + 11\text{ Fed} = \mathbf{51}$ | $200\ CC + 200\ WC + 30\text{ Fed} = \mathbf{430}$ | $2,000\ CC + 2,000\ WC + 120\text{ Fed} = \mathbf{4,120}$ | $20,000\ CC + 20,000\ WC + 600\text{ Fed} = \mathbf{40,600}$ |
| **Priced Categories ($G = |\Omega|$)** | $30$ categories | $80$ categories | $500$ categories | $2,000$ categories | $10,000$ categories |
| **Council Proposals per Round / per 10-Round Plan** | $20$ /round ($200$ /plan) | $40$ /round ($400$ /plan) | $400$ /round ($4,000$ /plan) | $4,000$ /round ($40,000$ /plan) | $40,000$ /round ($400,000$ /plan) |
| **Total Signed Messages per Round (Incl. Household $\to CC$ + MST Receipts)** | $\sim 150$ msgs/round | $\sim 1,150$ msgs/round | $\sim 11,200$ msgs/round | $\sim 112,000$ msgs/round | $\sim 1,120,000$ msgs/round |
| **Aggregate Network Traffic per Round (All Nodes Combined)** | $\sim \mathbf{0.8\text{ MB}}$ /round | $\sim \mathbf{6.5\text{ MB}}$ /round | $\sim \mathbf{68\text{ MB}}$ /round | $\sim \mathbf{720\text{ MB}}$ /round | $\sim \mathbf{7.8\text{ GB}}$ /round (across 600 federated relays $\approx 13\text{ MB}$/relay!) |
| **Bandwidth per Mobile Client (`Role-LP`) per Round** | $\sim 12\text{ KB}$ /round | $\sim 18\text{ KB}$ /round | $\sim 35\text{ KB}$ /round | $\sim 65\text{ KB}$ /round | $\sim 140\text{ KB}$ /round |
| **Total Storage Growth per Annual Plan (Full Archival Node `Role-SR`)** | $\sim \mathbf{10\text{ MB}}$ /year | $\sim \mathbf{75\text{ MB}}$ /year | $\sim \mathbf{750\text{ MB}}$ /year | $\sim \mathbf{7.5\text{ GB}}$ /year | $\sim \mathbf{78\text{ GB}}$ /year (compressed MST + qualitative blobs) |
| **Storage on Mobile Client (`Role-LP`)** | $< 5\text{ MB}$ | $< 10\text{ MB}$ | $< 20\text{ MB}$ | $< 35\text{ MB}$ | $< 60\text{ MB}$ |
| **Pure Economic Solver + Aggregation CPU Time per Round (Parallel across Federations)** | $< \mathbf{5\text{ ms}}$ (1 core) | $< \mathbf{25\text{ ms}}$ (4 cores) | $\sim \mathbf{120\text{ ms}}$ (8 cores) | $\sim \mathbf{0.6\text{ s}}$ (across 10 federation servers) | $\sim \mathbf{2.4\text{ s}}$ (across 50 federation servers; cf. 2.5s for 60k councils on 1 JVM in `pequod-cljs`) |
| **Cryptographic Overhead per Round (Hybrid PQ Verify + MST + ZK Budget Proofs)** | $\sim \mathbf{15\text{ ms}}$ aggregate CPU | $\sim \mathbf{110\text{ ms}}$ aggregate CPU | $\sim \mathbf{1.1\text{ s}}$ aggregate CPU | $\sim \mathbf{11\text{ s}}$ total CPU ($\sim 1.1\text{ s}$ wall-clock across 10 servers) | $\sim \mathbf{110\text{ s}}$ total CPU ($\sim 2.2\text{ s}$ wall-clock across 50 servers; plus $180\text{ ms}$ local proof on each phone) |
| **Epoch BFT Consensus Overhead per Round Checkpoint** | $< 50\text{ ms}$ (3-of-4 threshold sig) | $< 100\text{ ms}$ (4-node local BFT) | $\sim 0.8\text{ s}$ (16-validator CometBFT) | $\sim 2.0\text{ s}$ (32-validator CometBFT) | $\sim 3.5\text{ s}$ (64-validator CometBFT, 1 checkpoint block of $<500\text{ KB}$) |
| **Total End-to-End Automated Wall-Clock Time per Round (Excl. Human Deliberation)** | **$< 0.1\text{ seconds}$** | **$< 0.4\text{ seconds}$** | **$\sim 1.5\text{ seconds}$** | **$\sim 4.0\text{ seconds}$** | **$\sim 9.0\text{ seconds}$** |
| **Estimated Infrastructure Cost of Operation (Community / Cloud Equivalent)** | **$0–$5 / month** (runs on existing laptops/Pi) | **$10–$25 / month** (2 Raspberry Pis + 1 entry VPS) | **$80–$150 / month** (8 community mini-PCs/VPS) | **$400–$800 / month** (~20 federation servers) | **$3,000–$6,000 / month** (~100 community servers; $\approx \$0.005$ per citizen/year!) |

---

### 2.2 Decoupling Economic Algorithm Scaling from Infrastructure Scaling

To rigorously separate **economic convergence behavior** from **distributed systems overhead**, the benchmark programme runs two orthogonal tracks:

1. **Track 1 — Pure Economic Convergence Scaling (`dpep-sim-fast`):**
   - Runs the exact fixed-point council solvers (`Clarabel.rs` / closed-form + proximal trust regions) and IFB price-update WASM module in a single multi-threaded Rust process (`rayon`) with cryptographic signatures disabled.
   - Measures the **iteration count $R(\tau, G, M, \kappa)$** required to reach $\tau \in \{0.05, 0.03, 0.01\}$ as a function of:
     - Number of priced categories $G \in \{80, 500, 2000, 10000\}$.
     - Input-output network depth and cyclicity (Leontief spectral radius).
     - Elasticity of substitution $\sigma_{\text{CES}} \in \{0.1 \text{ (near-Leontief)}, 0.5, 1.0 \text{ (Cobb-Douglas)}, 2.0\}$.
     - Fraction of worker councils with fixed setup costs / minimum efficient scale ($\kappa \in \{0\%, 10\%, 25\%, 50\%\}$).
     - Endogenous income feedback relaxation parameter $\alpha_w \in \{0.0 \text{ (Pequod baseline)}, 0.5, 1.0\}$.
2. **Track 2 — Distributed vs. Centralised Baseline Overhead (`dpep-bench-net`):**
   - Compares four configurations on identical hardware and identical economic inputs:
     - **Baseline C0 (Centralised Cleartext):** Single Rust HTTP/PostgreSQL server, no per-proposal signatures, cleartext household proposals.
     - **Config D1 (Federated Classical Crypto):** Architecture D with classical Ed25519 signatures and BLAKE3 Merkle-Sum Trees.
     - **Config D2 (Federated Hybrid Post-Quantum):** Architecture D with hybrid `Ed25519 + ML-DSA-65` signatures and `X25519MLKEM768` transport.
     - **Config D3 (Full DPEP: Federated Hybrid PQC + Private Household Masking & STARK Budget Proofs):** Adds pairwise additive masking and `Plonky3` budget compliance proofs.
   - Quantifies the exact **Decentralisation Multiplier** ($\text{Time}_{D1}/\text{Time}_{C0}$), **PQC Multiplier** ($\text{Bytes}_{D2}/\text{Bytes}_{D1}$), and **Privacy Multiplier** ($\text{CPU}_{D3}/\text{CPU}_{D2}$).

---

## 3. Implementation Roadmap and Budget Scenarios (Section 15)

In accordance with Section 15, we provide three realistic development scenarios. All figures below **explicitly distinguish engineering estimates from verified 2026 market rates** (cloud/hardware pricing verified against Hetzner/AWS/Raspberry Pi retail prices; security audit rates based on published 2025–2026 Trail of Bits / Least Authority / Oak Security engagement brackets).

### Scenario A — Solo Developer with AI-Assisted Coding
*Profile:* One senior systems/cryptography engineer with solid mathematical optimization literacy, using Cursor, Claude Code, and mature Rust/TypeScript open-source crates (`quinn`, `rusqlite`, `clarabel`, `wasmtime`, `ml-dsa`, `ml-kem`, `loro`).

| Dimension | Estimate & Specification |
| :--- | :--- |
| **Development Duration** | **4 to 6 months** (Full-time equivalent, ~700–1,000 engineering hours across 4 milestones). |
| **Staffing Requirements** | 1.0 FTE Principal Engineer (Full-stack Rust + TypeScript PWA + Applied Crypto/OR). |
| **Infrastructure Costs** | **$150 – $300 total (Verified Hardware/Cloud Costs):** 2x Raspberry Pi 5 (8GB) @ $80 each for local multi-device testing + 3x Hetzner Cloud ARM/x86 VPS instances (€4.50–€8/mo each) for 6 months of WAN federation testing. |
| **Security Review Costs** | **$0 external audit** (Self-audited via property-based fuzzing with `proptest`/`cargo-fuzz`, formal invariant assertions, and using audited upstream `RustCrypto` crates rather than rolling custom crypto primitives). *Caveat: Not suitable for high-stakes adversarial production without external review.* |
| **Research Dependencies** | Relies on existing `pequod-cljs` datasets and the formal model in `reports/ECONOMIC_MODEL.md`; uses pairwise masking + Pedersen/Bulletproofs (or off-the-shelf `Plonky3` example circuits) rather than custom lattice ZK research. |
| **Main Risks** | 1. Single-person bus factor and UI polish bottlenecks. 2. Scope creep if attempting to build custom P2P NAT traversal instead of using `iroh`/`quinn`. 3. Lack of real human-factors validation beyond developer self-testing. |
| **Expected Deliverables** | Complete open-source PoC repository (`dpep-poc`) passing all 12 Section-12 capabilities and `TEST-E2E-01` through `TEST-SEC-05`, including the 1,000-participant simulator, deterministic WASM IFB engine, CLI + mobile-compatible PWA client, and reproducible benchmark suite up to 100,000 simulated participants. |

---

### Scenario B — Small Research and Engineering Team (Recommended Initial Launch)
*Profile:* 3 to 5 contributors combining distributed systems/Rust engineering, computational economics/OR modeling, and local-first mobile/UX development.

| Dimension | Estimate & Specification |
| :--- | :--- |
| **Development Duration** | **6 to 9 months** (2 phases: Months 1–4 Core Protocol & Simulation Suite; Months 5–9 Interactive Mobile/Desktop Apps, PQC/ZK Privacy Layer, and Human-in-the-Loop Workshop Pilot with 40–100 live participants). |
| **Staffing Requirements** | **3.5 – 4.5 FTEs** (*Estimated compensation: $350k – $650k total* depending on academic/cooperative vs. commercial grant rates, or open-source fellowship stipends):<br>- 1x Lead Distributed Systems & Rust Protocol Engineer (1.0 FTE)<br>- 1x Applied Cryptographer / Privacy Engineer (0.5–1.0 FTE)<br>- 1x Computational Economist / Operations Research Scientist (1.0 FTE)<br>- 1x Local-First Frontend / Mobile & Accessibility Engineer (1.0 FTE) |
| **Infrastructure Costs** | **$2,500 – $5,000 total:** Dedicated 20-node multi-region testbed (Hetzner/AWS spot cluster for 1,000,000-participant scale benchmarks) + hardware test lab (5x Raspberry Pi appliances, 4x low-end/legacy Android test phones, iOS test device). |
| **Security Review Costs** | **$25,000 – $45,000 (Estimated Market Rate):** Targeted 2–3 auditor-week review by a specialized cryptography/systems consultancy focusing on the MST aggregation verifier, `PQ-UCAN` capability validation, and WASM sandbox determinism. |
| **Research Dependencies** | Convergence tuning of Algorithm 3 (ADMM/proximal damping) under Leontief + non-convex setup costs; UX user-testing with cooperative members to keep household planning under 30 minutes/round. |
| **Main Risks** | Coordination overhead between economic modeling and UX simplification; potential latency on legacy Android devices for post-quantum STARK proofs (mitigated by hybrid Pedersen/masking fallback). |
| **Expected Deliverables** | Production-grade PoC + Scale-4/5 distributed benchmark suite + peer-reviewed paper on non-convex participatory planning convergence + live human-in-the-loop workshop software used by 50–100 real participants across worker/consumer councils. |

---

### Scenario C — Funded Interdisciplinary Research Programme & Real-World Cooperative Pilot
*Profile:* Multi-year institutional research programme (university consortium, solidarity-economy foundation, or cooperative federation such as Mondragón / Cecosesola / CoopCycle network).

| Dimension | Estimate & Specification |
| :--- | :--- |
| **Development Duration** | **24 to 36 months** (Year 1: Core Protocol, Formal Verification & Large-Scale Simulation; Year 2: Field Pilot with 10–30 real worker cooperatives and consumer buying clubs / participatory budgeting municipalities; Year 3: Multi-Region Federation & Security Hardening). |
| **Staffing Requirements** | **10 to 14 FTEs** (*Estimated budget: $2.2M – $4.0M over 2.5–3 years*):<br>- 4x Core Rust / P2P / Consensus Engineers<br>- 2x Post-Quantum & Zero-Knowledge Cryptographers<br>- 2x Mechanism Design / Ecological & Computational Economists<br>- 2x Mobile, Accessibility & HCI Researchers<br>- 2x Cooperative Field Coordinators / Institutional Sociologists |
| **Infrastructure Costs** | **$35,000 – $75,000 over 3 years:** Community server appliances deployed at 30+ pilot cooperatives and neighborhood centers + continuous large-scale simulation cluster + LoRa/mesh offline field kits. |
| **Security Review & Formal Verification Costs** | **$120,000 – $200,000:** Two comprehensive third-party security audits (core crypto/protocol + mobile/web clients), penetration testing of federation relays, and formal verification (TLA+ / Lean 4) of the state-machine accounting invariants (`INV-1` through `INV-5`). |
| **Research Dependencies** | Real-world legal/accounting bridging for pilot cooperatives operating inside a surrounding capitalist economy ("Parallel Economy" Experiment 2, PEPE Ch. 6 p. 129; Sandström 2020); longitudinal study of BJC and effort-rating dynamics. |
| **Main Risks** | Real-world institutional friction (participant turnover, legal/tax constraints on inter-cooperative non-market clearing, cultural resistance to peer effort ratings). |
| **Expected Deliverables** | Audited v1.0 Open Protocol Specification + Multi-platform client/server suite + Empirical field data from a live parallel participatory economy pilot involving 1,000–10,000 real workers and consumers. |

---

## 4. PoC Milestone Schedule and Acceptance Criteria Checklist

To ensure disciplined engineering execution (under Scenario A or B), the PoC is divided into **five sequential milestones**:

- **Milestone M1 (Weeks 1–3): Deterministic Economic Core & Sandström Ledger (`dpep-core`)**
  - *Deliverable:* Pure Rust crate implementing `FixedDecimal`, the 7-category catalog $\Omega$, Sandström's 4 accounting entities, local council `Clarabel.rs` optimization, and the deterministic WASM IFB price-update rule.
  - *Acceptance Criterion:* Reproduces `pequod-cljs` convergence in $\le 12$ rounds on cold start and $\le 7$ rounds on warm start while enforcing exact Society Account conservation ($\text{Discrepancy} = 0\text{ micro-units}$) and hard ecological ceilings.
- **Milestone M2 (Weeks 4–6): Hybrid PQC Identity, `PQ-UCAN` Capabilities & BLAKE3 Merkle-Sum Trees (`dpep-crypto`)**
  - *Deliverable:* `Ed25519 + ML-DSA-65` signing, `PQ-UCAN` council/delegate certificates with 1-step revocation, Sparse Merkle-Sum Tree builder/verifier, and pairwise additive masking + budget compliance proofs.
  - *Acceptance Criterion:* Passes `TEST-SEC-04` (100% rejection of tampered/unauthenticated/out-of-budget proposals) and `TEST-SEC-05` (censorship detection via MST inclusion proof) with $<1\text{ ms}$ per-proposal verification on ARMv8.
- **Milestone M3 (Weeks 7–10): Local-First Storage, QUIC Federation Transport & Epoch Checkpoint Log (`dpep-node`)**
  - *Deliverable:* SQLite + Loro CRDT council state engine, QUIC (`quinn`) federated tree sync, threshold-signed Epoch Checkpoint log, and intra-year UFB scoped replanning (`State S7–S8`).
  - *Acceptance Criterion:* Passes `TEST-E2E-01` (multi-device execution) and `TEST-E2E-03` (offline disconnect, local edit, and resynchronization in $<2\text{ s}$) plus Stage 11–12 intra-year 30% supply shock recovery.
- **Milestone M4 (Weeks 11–14): Mobile-Compatible Local-First PWA & Council Deliberation UI (`dpep-ui`)**
  - *Deliverable:* Accessible TypeScript + WASM Progressive Web App supporting household proposal drafting ("what-if" sliders + diff view), qualitative `List` browser, and council voting on mobile and desktop.
  - *Acceptance Criterion:* Passes `TEST-E2E-02` on a real smartphone with $<50\text{ KB}$ bandwidth per round and $<250\text{ ms}$ local proof generation.
- **Milestone M5 (Weeks 15–16): Multi-Scale Benchmark Suite & Reproducible Evaluation Report (`dpep-bench`)**
  - *Deliverable:* Automated benchmark harness executing Track 1 and Track 2 experiments from $10^2$ to $10^5+$ participants against the centralized baseline `C0`.
  - *Acceptance Criterion:* Generates reproducible CSV/JSON performance profiles and plots verifying all latency, bandwidth, and convergence targets.
