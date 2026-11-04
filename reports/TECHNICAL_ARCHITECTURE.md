# Technical Architecture Report: Distributed Participatory Economics Protocol (DPEP)

**Deliverable:** `reports/TECHNICAL_ARCHITECTURE.md`  
**Phase:** 3 & 4 — Technical Architecture & Feasibility Research  
**Scope:** Sections 5 (Distributed Systems Architecture), 6 (Consensus, Consistency, and Performance), and 9 (Mobile and Low-Power Participation).

---

## 1. Architectural Thesis: Why Participatory Economics Is Not a High-TPS Blockchain Problem

A foundational requirement of this study is to let **economic and institutional requirements precede technology selection** and to avoid assuming that every economic operation requires a global blockchain transaction.

When we examine the computational structure of Participatory Economics formalized in `reports/ECONOMIC_MODEL.md`, three architectural facts emerge immediately:

1. **Participatory Planning Is an Epoch-Synchronized Bulk-Synchronous Parallel (BSP) / Hierarchical MapReduce Process, Not a Continuous Stream of Atomic Global Transfers:**
   - During the annual planning cycle (10–20 iterations over several weeks), millions of individuals and tens of thousands of councils draft proposals locally, aggregate them up nested geographic and industrial federation trees, and compute updated indicative prices $P^{(t+1)}$ once per iteration.
   - Global state agreement is required **only at iteration boundaries** (to lock the Merkle-Sum root of round-$t$ proposals and ratify the deterministic computation of $P^{(t+1)}$) and **at plan ratification / year-end settlement**.
2. **Intra-Year Execution Is Hierarchically Scoped:**
   - As Albert & Hahnel (1991a, Ch. 4, pp. 66–67) specify, 90%+ of intra-year consumer preference shifts cancel out at the neighborhood, ward, or city federation level without altering aggregate production plans. Requiring global Byzantine consensus across millions of nodes every time a household swaps apples for oranges at a neighborhood distribution center would be an absurd architectural anti-pattern.
3. **Participation Must Work Offline and on Low-Power Devices:**
   - Workers and consumers in rural collectives, factory floors, or intermittently connected regions must be able to inspect prices, deliberate in council work-groups, run local budget/recipe optimizations, and sign proposals offline, synchronizing opportunistically when connectivity resumes.

Consequently, **Architecture D — a Local-First, Peer-to-Peer Federated Architecture with Selective Epoch-Based Byzantine Fault-Tolerant (BFT) Checkpoint Finality**—is overwhelmingly superior to a monolithic database (Architecture A), an unstructured P2P gossip network without finality guarantees (Architecture B), or a per-transaction global blockchain (Architecture C).

---

## 2. High-Level System Architecture (Architecture D)

DPEP is structured into **four decoupled horizontal layers** operating across **six distinct node roles**:

```
+===================================================================================+
| LAYER 4: HUMAN DELIBERATION, ACCESSIBILITY & DECISION-SUPPORT INTERFACE           |
|  - Local-First Mobile/Desktop/Web UI (Offline PWA / Native Kotlin & Swift + WASM) |
|  - Deterministic Council LP/QP Proposal Solver (HiGHS-WASM) + Forecasting Assist  |
|  - Qualitative Annotation ('List') Browser & Accessible Deliberation Workspaces   |
+===================================================================================+
                                        |
                                        v
+===================================================================================+
| LAYER 3: LOCAL-FIRST COUNCIL & HOUSEHOLD STATE LAYER (ASYNC / OFFLINE-CAPABLE)    |
|  - Embedded SQLite + Automerge/Loro CRDT Document Store for Council Drafts        |
|  - Private Household Budget Ledger & ZK/Pedersen Budget Compliance Prover         |
|  - Scoped Capability Authorization (PQ-UCAN / Revocable Delegate Certificates)    |
+===================================================================================+
                                        |
                                        v
+===================================================================================+
| LAYER 2: FEDERATED AGGREGATION & CONTENT-ADDRESSED DATA PLANE (P2P / HIERARCHICAL)|
|  - libp2p / Quinn (QUIC) Transport with Store-and-Forward Relay / DTN Sync        |
|  - BLAKE3 Content-Addressed Storage (Iroh-style) for Recipes & Qualitative Lists  |
|  - Verifiable Merkle-Sum Trees (MST) for Ward -> City -> Region / Industry Sums   |
+===================================================================================+
                                        |
                                        v
+===================================================================================+
| LAYER 1: SELECTIVE EPOCH-BFT CHECKPOINT & DETERMINISTIC IFB ENGINE                |
|  - Lightweight Rotating BFT Committee (CometBFT / Simplex-style Epoch Consensus)  |
|    elected via Federated Council Sortition (commits ~1-20 checkpoints per round)  |
|  - Deterministic Sandboxed WASM Runtime executing IFB Price-Update Rules          |
|  - Society Account & CAP Macro-Reconciliation State Roots (Sandström Model)       |
+===================================================================================+
```

---

## 3. Component Boundaries and Protocol Workflows

### 3.1 Layer 1: Selective Epoch-BFT Checkpoint & Deterministic IFB Engine
Instead of processing individual economic actions on a blockchain, Layer 1 acts strictly as a **verifiable public bulletin board and deterministic state-transition notary** for macro-planning epochs.
- **What Layer 1 Stores:**
  1. The **Federation & Council Registry Root** (accreditation certificates of active $CC_h, WC_j, CF_f, IF_k, CAP_z$ and rotating sortition committees).
  2. The **Pre-Plan Boundary Commitments** ($l^*, r^*, E^{\max}, \sigma_{\text{inv}}$ from Long-Run and Investment Planning).
  3. One **Epoch Checkpoint Block per Annual Planning Iteration $t$**, containing:
     - `proposals_merkle_sum_root`: The 32-byte BLAKE3 Merkle-Sum Tree root of all council supply/demand vectors submitted in Round $t$.
     - `wasm_rule_hash`: The hash of the ratified deterministic WASM module implementing the IFB price-update rule.
     - `RoundAggregationAndPrices(t)`: The resulting aggregate supply $S^{(t)}$, demand $D^{(t)}$, slack $SL^{(t)}$, imbalance vector $\rho^{(t)}$, base wage $w_{\text{base}}^{(t)}$, and new indicative prices $P^{(t+1)}$.
  4. The **Ratified Annual Plan Root** (`S6`) and **Periodic Macro-Accounting Checkpoints** (`S7–S9`) for the Society Account and CAP Accounts.
- **Why IFBs Cannot Cheat:** Because the IFB price-update algorithm is compiled to a **deterministic, floating-point-free (64-bit fixed-point) WebAssembly (WASM) module**, any council laptop or Raspberry Pi that downloads the top-level federation Merkle-Sum nodes (~a few megabytes per round) can re-execute the WASM module locally in $<10\text{ ms}$ and verify that the IFB's published price vector $P^{(t+1)}$ is mathematically exact.

### 3.2 Layer 2: Federated Aggregation via Verifiable Merkle-Sum Trees (MST)
In Participatory Economics, aggregation follows the nested structure of consumer and worker federations (PEPE Ch. 4, p. 64; Ch. 6, pp. 111–112). DPEP implements this directly using **Sparse Merkle-Sum Trees (MST)**:

```
                       [Global Round-t MST Root]
                      Hash: H_root | Vectors: (S^E, D^E)
                             /                  \
          [Consumer Federation Root]        [Worker Federation Root]
          Hash: H_C | Vector: D^final       Hash: H_W | Vectors: (S^gross, D^int)
               /              \                    /                \
      [Region CF_1]        [Region CF_2]     [Industry IF_1]    [Industry IF_2]
         /      \                                /      \
   [City CF]   [City CF]                    [WC_1]     [WC_2]
     /    \
 [CC_1]  [CC_2]
```

- **How MST Verification Works:**
  1. Each leaf node is a council's signed proposal $\pi_c^{(t)}$, containing a sparse vector of non-negative fixed-point quantities and its PQC/hybrid threshold signature.
  2. Each internal node (Ward $\to$ City $\to$ State $\to$ Region, or Industry Sub-Sector $\to$ Industry Federation) computes:
     $$\text{Hash}(\text{Parent}) = \text{BLAKE3}\left(\text{Hash}(\text{Left}) \parallel \text{VectorSum}(\text{Left}) \parallel \text{Hash}(\text{Right}) \parallel \text{VectorSum}(\text{Right})\right)$$
     $$\text{VectorSum}(\text{Parent}) = \text{VectorSum}(\text{Left}) + \text{VectorSum}(\text{Right})$$
  3. **Cryptographic Non-Inclusion / Non-Tampering Proof:** Every council $CC_h$ or $WC_j$ receives a compact **Merkle-Sum Inclusion Proof** ($O(\log M)$ hashes and sparse vector sums) proving that its exact signed proposal was included without modification or negative-quantity injection in the global round root `H_root`!
  4. **Qualitative `List` Aggregation:** Qualitative annotations (`QualitativeAnnotation` in `reports/ECONOMIC_MODEL.md`) are stored in content-addressed BLAKE3 blobs (via an Iroh/IPFS-compatible data plane) referenced by CID inside the MST leaves, allowing any citizen to read high-level IFB summaries while drilling down to the original signed narrative of any workplace or neighborhood council (PEPE Ch. 6, p. 112).

### 3.3 Layer 3: Local-First Council & Household State Layer
- **Intra-Council Deliberation (CRDTs + SQLite):** Within a workplace council $WC_j$ (say, 20 to 500 workers) or neighborhood council $CC_h$, members collaborate on draft production recipes, balanced job complex schedules, and collective neighborhood projects using **conflict-free replicated data types (CRDTs)** (specifically operation/state-based delta CRDTs such as Automerge or Loro persisted to local SQLite).
- **Offline-First Synchronization:** When a rural collective or factory subnet is disconnected from the wider internet, workers continue deliberating, voting on work-team schedules, and recording local deliveries over local Wi-Fi/LAN (via mDNS/Bluetooth/QUIC peer discovery). Once a gateway node regains connectivity, delta-state sync merges local updates and submits the council's threshold-signed round proposal.

---

## 4. Consensus, Consistency, and Performance Analysis (Section 6)

### 4.1 Granular Consistency Mapping by Economic Subsystem

Different economic operations have fundamentally different consistency, latency, and fault-tolerance requirements. Applying a single consistency model to the entire economy is both unnecessary and harmful.

| Economic Subsystem | Required Consistency Model | Finality Latency Target | Partition Behavior (CAP Theorem Tradeoff) | Justification |
| :--- | :--- | :--- | :--- | :--- |
| **1. Individual & Council Proposal Drafting (`S1–S2`)** | **Strong Eventual Consistency (SEC)** via causal delta-CRDTs + local SQLite | Real-time local ($<50\text{ ms}$); async sync on reconnect | **AP (Available under Partition):** Disconnected households and councils continue drafting and deliberating offline. | No external actor relies on unsubmitted drafts; availability and offline usability are paramount. |
| **2. Council Vote & Proposal Ratification** | **Council-Scoped Quorum Consensus** ($k$-of-$n$ threshold signature / recorded tally) | Seconds to hours (human deliberation bound) | **Locally CP within Council LAN:** Requires council quorum to sign official proposal $\pi_c^{(t)}$, but independent of global internet. | Only eligible members of $WC_j$ or $CC_h$ have authority over their council's proposal. |
| **3. Authentication, Membership & Role Delegation** | **Causal Consistency + Epoch Revocation Lists** (Capability certificates anchored to Council Roots) | Verification: $<5\text{ ms}$ local; Revocation propagation: $<1\text{ min}$ (or next epoch) | **AP for local verification** using cached council public keys; **CP for accrediting new councils** at federation level. |Recallable delegates (Spain 1936 / Paris 1871) require fast revocation propagation across federation relays. |
| **4. Federated Round Aggregation (`S3`)** | **Deterministic Convergent Tree Reduction** (Merkle-Sum Tree) | $1\text{–}10\text{ minutes}$ per global planning round | **Bounded-Wait CP with Grace Window:** If a regional subnet is partitioned during a 24-hour planning round, relays buffer until the round deadline; if prolonged, fallback rules use the council's prior-round proposal $\pi_c^{(t-1)}$. | Prevents a single offline neighborhood from halting national annual planning while preserving verifiable inclusion. |
| **5. IFB Price Update & Plan Publication (`S4, S6`)** | **Global Total Order / Linearizable State Machine Replication (Epoch BFT)** | $2\text{–}15\text{ seconds}$ per BFT checkpoint block | **CP (Safety over Liveness):** Requires $\ge 2f+1$ of $3f+1$ geographically diverse federation validators to finalize $P^{(t+1)}$ and the final plan root. | All councils must compute round $t+1$ against the *exact same* indicative price vector $P^{(t+1)}$. |
| **6. Intra-Year Delivery & Consumption Clearing (`S7`)** | **Counterparty Bilateral Finality + Periodic Federated Rollup** | Point-of-service: $<500\text{ ms}$ (offline-capable with bounded credit); Rollup: hourly/daily | **AP with Bounded Exposure Offline:** "Credit-card computer" (PEPE Ch. 4, p. 66) signs bilateral receipts locally against cached budget allowance; syncs upward to Ward/City UFB. | A consumer picking up groceries at a neighborhood depot must not wait for global consensus; double-spending beyond warranted budget $B_u$ is prevented by hardware-bound counters and daily council reconciliation. |
| **7. Conflict Resolution, Appeals & Audit Trails (`S8–S9`)** | **Tamper-Evident Append-Only Log (Merkle Hash-Chain) + Court Quorum** | Hours to days (deliberative adjudication) | **CP for final ruling:** Requires signed quorum of the Industry Federation appellate board or Environmental Court. | Audit trails (*euthynai*) must be non-repudiable and permanently verifiable. |

---

### 4.2 Is High Transaction Throughput (TPS) the Principal Scaling Constraint?

**No.** Quantitative analysis of the economic model proves that **global consensus TPS is not the scaling bottleneck** of participatory planning:
- Even in a large national economy of **100 million participants**, **200,000 Worker Councils**, **200,000 Neighborhood Consumer Councils**, and **10,000 coarse product categories**:
  - Each planning round occurs over a human deliberation window of **12 to 48 hours** (or in automated sub-iterations, several minutes).
  - The 400,000 councils submit **one signed sparse vector per round**.
  - Aggregated hierarchically across 100 regional/industrial federations, each regional aggregator verifies ~4,000 signatures and sums ~4,000 sparse vectors per round—a workload that a single modern 8-core server completes in **under 0.5 seconds**!
  - The global BFT checkpoint layer only needs to commit **one summary state root and 10,000 updated prices per round** ($\sim 200\text{ KB}$).
- **What ARE the real scaling constraints?**
  1. **Human Cognitive and Deliberative Bandwidth:** How workers and consumers meaningfully review qualitative `Lists`, evaluate collective goods, and revise proposals without coordination fatigue (addressed in `reports/AI_AND_OPTIMISATION.md`).
  2. **Algorithmic Convergence Rate ($R$) Under Input-Output Coupling and Non-Convexities:** Ensuring the iterative procedure reaches $\tau \le 5\%$ across thousands of intermediate goods in $R \le 10\text{–}15$ rounds without oscillation.
  3. **Byzantine Fault Tolerance of Federated Aggregators:** Preventing a malicious or compromised federation coordinator from omitting valid council proposals (censorship) or injecting phantom demand/supply (addressed via Merkle-Sum inclusion proofs and BFT threshold witnessing).
  4. **Post-Quantum Signature & Proof Bandwidth on Constrained Links:** Keeping round synchronization payloads small enough for low-end smartphones on 2G/3G or community mesh networks (addressed in `reports/SECURITY_AND_PQC.md`).

### 4.3 Measurable Performance Objectives (Distinguishing Targets from Proven Results)

In compliance with Section 6, the table below defines concrete, measurable engineering targets for DPEP across hardware tiers, explicitly distinguishing **analytical targets** from **already demonstrated simulation results** (`pequod-cljs` / Szczepanczyk 2023):

| Metric | Demonstrated Baseline in Literature (`pequod-cljs`, Single JVM Node) | DPEP PoC Target (1,000 Participants, 40 Councils, 100 Goods) | DPEP Regional Target (100,000 Participants, 1,000 Councils, 1,000 Goods) | DPEP National Target (1,000,000+ Participants, 10,000 Councils, 5,000 Goods) |
| :--- | :--- | :--- | :--- | :--- |
| **Economic Convergence ($\tau \le 5\%$)** | **Demonstrated:** 11.85 rounds (Year 1 cold start), 6.5 rounds (Year 2 warm start) for 60k councils, 500 goods | $\le 12$ rounds (cold start), $\le 7$ rounds (warm start) with endogenous income active | $\le 15$ rounds (cold start), $\le 8$ rounds (warm start) | $\le 18$ rounds (cold start), $\le 10$ rounds (warm start) |
| **Cryptographic Proposal Verification Rate (per Coordinator Node)** | *Not implemented in `pequod-cljs`* (in-memory Clojure maps without signatures) | $\ge 500$ hybrid PQ signatures/sec (Raspberry Pi 4 / entry server) | $\ge 5,000$ hybrid PQ signatures/sec (8-core community server) | $\ge 50,000$ hybrid PQ signatures/sec across 10 federated aggregators |
| **Compute Time per Automated Planning Iteration (Excl. Human Deliberation)** | **Demonstrated:** ~2.5s per iteration for 60,000 councils on 1 JVM laptop | $< 500\text{ ms}$ end-to-end across distributed nodes | $< 3\text{ seconds}$ end-to-end (federated MST + BFT checkpoint) | $< 15\text{ seconds}$ end-to-end across 2-tier federation tree |
| **Bandwidth per Mobile Participant per Planning Round** | *N/A* | $< 50\text{ KB}$ / round (delta prices + sparse proposal + MST proof) | $< 150\text{ KB}$ / round | $< 500\text{ KB}$ / round (compressed sparse price deltas) |
| **Offline Resynchronization Latency (After 48h Disconnect)** | *N/A* | $< 2\text{ seconds}$ on reconnect | $< 5\text{ seconds}$ on reconnect | $< 10\text{ seconds}$ on reconnect |
| **Energy Consumption per Planning Round** | *N/A* | $< 0.01\text{ Wh}$ per mobile client; $< 0.5\text{ Wh}$ total server compute | $< 50\text{ Wh}$ total federation compute per round | $< 500\text{ Wh}$ total federation compute per round ($\sim 10^{-7}\times$ Proof-of-Work) |

---

## 5. Mobile, Low-Power, and Offline-First Participation Architecture (Section 9)

To prevent a "digital coordinator class" where only participants with high-end workstations and fiber connections can participate, DPEP strictly separates **six node roles** mapped to hardware capabilities:

### 5.1 Taxonomy of Node Roles and Hardware Realism

| Node Role | Core Responsibilities | Realistic on Entry Smartphone (e.g., 3GB RAM Android, ARM Cortex-A53)? | Realistic on Raspberry Pi 4/5 (4–8GB RAM)? | Realistic on Community Server / Desktop (8+ Cores, 16–64GB RAM)? |
| :--- | :--- | :--- | :--- | :--- |
| **1. Lightweight Participant Node (`Role-LP`)** | Stores personal/household consumption draft, effort certificate, local council CRDT state; runs local household budget LP/QP solver; generates ZK/Pedersen budget proof; verifies MST inclusion proofs & BFT checkpoint headers; signs ballots. | **YES (Primary Target).** Uses $< 50\text{ MB}$ RAM, $< 100\text{ MB}$ SQLite storage, $< 1\%$ battery per day. | **YES.** | **YES.** |
| **2. Council Coordinator Node (`Role-CC`)** | Hosts workplace ($WC_j$) or neighborhood ($CC_h$) CRDT sync relay on local LAN/Wi-Fi; aggregates member drafts; runs workplace input-output optimization (`HiGHS-WASM`); assembles council threshold signature. | **YES (Emergency/Ad-hoc failover).** A smartphone hotspot can coordinate a 50-person council offline. | **YES (Ideal Primary Appliance).** A $50 Raspberry Pi in a workplace or neighborhood center runs `Role-CC` 24/7 at 5W. | **YES.** |
| **3. Storage & Qualitative Replica Node (`Role-SR`)** | Pins content-addressed BLAKE3 blobs for regional qualitative `Lists`, product catalogs, and historical audit logs; serves range queries to light clients. | **NO** (Flash wear and cellular bandwidth limits make phones unsuitable as public archive servers). | **YES** (with external USB SSD, up to 1–2 TB regional archive). | **YES.** |
| **4. Planning Computation Worker (`Role-PCW`)** | Executes federated Merkle-Sum Tree reductions, deterministic WASM price updates, cross-industry input-output feasibility checks, and optional forecasting/scenario simulations. | **NO** (Full federation matrix inversions and Monte Carlo simulations exceed mobile thermal/battery budgets). | **PARTIAL** (Can easily compute MST reductions and IFB price updates for $\le 5,000$ councils). | **YES (Primary Target for Federation IFBs).** |
| **5. Consensus Participant / Epoch Validator (`Role-BFT`)** | Participates in the rotating Federation BFT committee (e.g., 21–100 nodes) to finalize round checkpoints, Society Account roots, and accreditation updates. | **NO** (Consensus validators require high uptime and stable routing; mobile phones can *verify* light-client BFT headers but should not be active BFT block proposers). | **YES** (For PoC / local federations with $\le 32$ validators). | **YES (Primary Target).** |
| **6. Gateway / Delay-Tolerant Relay (`Role-GW`)** | Bridges intermittently connected mesh networks (LoRa, community Wi-Fi,sneakernet USB bundles) to the wider federation P2P network via store-and-forward bundles. | **YES (As "Data Mule").** A smartphone moving between a disconnected village and town can carry signed council CRDT/proposal bundles! | **YES (Community Wi-Fi / Mesh Box).** | **YES.** |

### 5.2 Offline-First Synchronisation and Conflict Resolution Protocol
1. **Local Encrypted Storage:** Every `Role-LP` client stores its state in an encrypted local **SQLite (SQLCipher)** database containing:
   - Cached product catalog $\Omega$ and latest known indicative price vector $P^{(t)}$.
   - The council's Automerge/Loro CRDT document for shared deliberation and BJC task schedules.
   - An outbound queue of signed, idempotent intent bundles (`SignedProposalIntent`).
2. **Opportunistic Sync & Bandwidth Compression:**
   - Price vectors $P^{(t)}$ are transmitted as **Zstandard-compressed delta-encoded varints** relative to $P^{(t-1)}$. Because most prices change by $<15\%$ per round and only active goods need full precision, a 1,000-good price update compresses to **$< 4\text{ KB}$**.
   - After a temporary disconnection, the client exchanges a 32-byte CRDT sync bloom filter / heads vector with its `Role-CC` coordinator and downloads only missing causal operations plus the latest `RoundAggregationAndPrices` header (~10–30 KB).
3. **Platform Independence & Anti-Lock-In:**
   - The core protocol engine (`dpep-core`) is compiled to both **native C-ABI libraries (for Android JNI / iOS Swift FFI / Linux CLI)** and **WebAssembly (`wasm32-unknown-unknown`)** for Progressive Web Apps (PWAs), ensuring that participants on old Android phones without Google Play Services (via F-Droid APK or local HTTP PWA hosted on the neighborhood Raspberry Pi `Role-CC`!) have 100% feature parity.
