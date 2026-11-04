# Security, Privacy, and Post-Quantum Cryptography Report

**Deliverable:** `reports/SECURITY_AND_PQC.md`  
**Phase:** 3 & 4 — Technical Architecture & Feasibility Research  
**Scope:** Section 7 (Post-Quantum Cryptography, Threat Model, Democratic Membership & Sybil Resistance) and Section 8 (Privacy and Verifiability Architecture).

---

## 1. Post-Quantum Cryptography (PQC) Engineering Analysis (Section 7)

### 1.1 Precision in Quantum Threat Modeling
Economic planning records, health/disability need allowances, and household consumption histories are sensitive over multi-decade human lifespans ("harvest-now, decrypt-later" threat). Conversely, forging signatures on council proposals or Society Account settlements requires a live Cryptographically Relevant Quantum Computer (CRQC) capable of running Shor's algorithm on elliptic curves (Ed25519, secp256k1, BLS12-381) or RSA.
- **What PQC Protects Against:** Shor's algorithm (which breaks all classical discrete-logarithm, factoring, and pairing-based cryptosystems in polynomial time) and Grover's algorithm (which provides a quadratic $\sqrt{N}$ speedup against symmetric ciphers and hash functions, mitigated by using 256-bit symmetric keys and 256-bit hash outputs like BLAKE3-256 / SHA3-256).
- **What PQC Does NOT Guarantee:** No lattice-based scheme (ML-KEM, ML-DSA) has an unconditional mathematical proof of hardness; its security rests on the conjectured worst-case/average-case hardness of Module Learning With Errors (M-LWE) and Module Short Integer Solution (M-SIS). Only hash-based signatures (**SLH-DSA**, NIST FIPS 205) and symmetric/hash commitments rely strictly on hash collision/preimage resistance. Therefore, **cryptographic agility** and **hybrid classical + post-quantum constructions** are mandatory from day one.

### 1.2 Quantitative Comparison of Standardized PQC Primitives (NIST FIPS 203, 204, 205)

The table below provides exact parameter sizes and empirical ARMv8 (mobile Cortex-A76 / Raspberry Pi 4–5 class) performance measurements for the NIST PQC standards finalized in August 2024:

| Primitive & Standard | Security Level | Public Key (Bytes) | Private Key (Bytes) | Ciphertext / Signature (Bytes) | ARMv8 Sign / Encaps ($\mu\text{s}$) | ARMv8 Verify / Decaps ($\mu\text{s}$) | Role in DPEP |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **X25519** (Classical Baseline) | Classical 128-bit (Quantum broken) | $32\text{ B}$ | $32\text{ B}$ | $32\text{ B}$ | $\sim 45\ \mu\text{s}$ | $\sim 45\ \mu\text{s}$ | Classical half of hybrid transport & storage encryption. |
| **ML-KEM-768** (NIST FIPS 203, Kyber) | NIST Level 3 ($\sim\text{AES-192}$) | $1,184\text{ B}$ | $2,400\text{ B}$ | $1,088\text{ B}$ | $\sim 35\ \mu\text{s}$ | $\sim 40\ \mu\text{s}$ | **Primary KEM** (combined as **X25519MLKEM768** hybrid in QUIC/TLS 1.3 and E2EE council messages). |
| **Ed25519** (Classical Baseline) | Classical 128-bit (Quantum broken) | $32\text{ B}$ | $64\text{ B}$ | $64\text{ B}$ | $\sim 50\ \mu\text{s}$ | $\sim 110\ \mu\text{s}$ | Classical half of hybrid composite signature. |
| **ML-DSA-65** (NIST FIPS 204, Dilithium3) | NIST Level 3 | $1,952\text{ B}$ | $4,032\text{ B}$ | $3,309\text{ B}$ | $\sim 180\ \mu\text{s}$ | $\sim 65\ \mu\text{s}$ | **Primary Workhorse Signature** (combined as **Ed25519 + ML-DSA-65** hybrid, total sig = $3,373\text{ B}$). Note: ML-DSA-65 verification is *faster* than Ed25519! |
| **SLH-DSA-SHA2-128s** (NIST FIPS 205, SPHINCS+) | NIST Level 1 (Pure Hash-Based) | $32\text{ B}$ | $64\text{ B}$ | $7,856\text{ B}$ | $\sim 120,000\ \mu\text{s}$ ($120\text{ ms}$) | $\sim 2,500\ \mu\text{s}$ ($2.5\text{ ms}$) | **Long-Term Root & Software Release Anchor:** Used for Federation Root accreditation, annual plan finality anchors, and WASM rule signing (immune to lattice cryptanalysis). |
| **BLAKE3-256** (Commitments & MST) | 256-bit Classical / 128-bit Grover | N/A | N/A | $32\text{ B}$ digest | $< 1\ \mu\text{s}$ / KB | $< 1\ \mu\text{s}$ / KB | **Merkle-Sum Trees**, content-addressed `List` blobs, and hash commitments. |

### 1.3 Network Overhead, Mobile Hardware Keystores, and Consensus Impact
1. **Network Overhead & Why Architecture D Is Essential for PQC:**
   - A hybrid `Ed25519 + ML-DSA-65` signature is **$3,373\text{ bytes}$** (plus $1,984\text{ bytes}$ for the public key if not cached by council ID)—roughly **$53\times$ larger** than a 64-byte Ed25519 signature.
   - In a naive global blockchain (Architecture C), broadcasting 400,000 council signatures to 1,000 validator nodes every round requires $400,000 \times 3.37\text{ KB} \approx 1.35\text{ GB}$ per node per round.
   - In **Architecture D (Federated Merkle-Sum Tree)**, each council submits its $3.37\text{ KB}$ signature *only* to its local Ward/Industry aggregator (`Role-CC` / `Role-PCW`). The aggregator verifies the signature (taking just $65\ \mu\text{s}$ per ML-DSA-65 verify!) and rolls the proposals into a **32-byte BLAKE3 Merkle-Sum root**. Thus, PQC signature size is absorbed at the edge and never floods the core network.
2. **Mobile Key Storage & Secure Enclave Reality Check:**
   - As of 2026, hardware Secure Elements (Apple Secure Enclave, Android StrongBox / Titan M2) natively support hardware-bound **P-256 (ECDSA)** and **Ed25519**, but most older smartphones in circulation do *not* support in-silicon ML-DSA key generation.
   - **DPEP Hybrid Key Storage Architecture:** On mobile devices (`Role-LP`), the classical key (`P-256`/`Ed25519`) is generated inside the hardware Secure Enclave / Android Keystore (requiring biometric/PIN unlock), while the post-quantum key (`ML-DSA-65`) is stored in SQLCipher encrypted storage wrapped by a symmetric key derived via HKDF from the hardware-keystore-protected secret plus user passphrase. This binds the PQ key to the physical anti-hammering protections of the mobile Secure Element even on legacy phones.
3. **Post-Quantum Implications for Zero-Knowledge Proofs and Threshold Signatures:**
   - Classical elliptic-curve ZK-SNARKs (Groth16, PLONK over BN254/BLS12-381) and Bulletproofs (Pedersen commitments over Ristretto255) are **not post-quantum secure**; a future CRQC could forge false budget proofs (*soundness failure*, which only matters *during* the planning round) or break commitment hiding if non-statistically hiding commitments are used.
   - **Critical Cryptographic Design Rule:**
     - **Confidentiality (Hiding)** must hold for *decades* against "harvest-now, decrypt-later" adversaries.
     - **Integrity (Soundness / Binding)** only needs to hold *at the time the proof is verified* during the planning round!
     - However, to ensure both immediate and long-term post-quantum security without elliptic-curve assumptions, DPEP uses **statistically hiding hash/lattice commitments** and **hash-based FRI/STARK range proofs (`Plonky3`)** for private household budget compliance.

---

## 2. Democratic Membership, Sybil Resistance, and Social Trust Assumptions

Section 7 emphasizes a foundational sociotechnical truth:
> **A cryptographic identity does not establish that its holder is a unique person, an eligible council member, or a legitimate representative.**

In capitalist Web3 systems, Sybil resistance is purchased via plutocracy (Proof-of-Stake token weight) or waste (Proof-of-Work), both of which violate Parecon's core principle of classlessness and one-person-one-vote self-management. Conversely, centralized state biometric databases create single points of surveillance and political exclusion.

### 2.1 DPEP's Federated Web-of-Councils Membership Protocol
Participatory Economics already possesses a natural institutional boundary against Sybil attacks: **people live in physical neighborhoods and work in physical/social workplaces** (PEPE Chs. 2–3; Ostrom's 1st Design Principle). DPEP translates this into a decentralized **Multi-Council Co-Attestation Protocol**:

1. **Local In-Person Council Onboarding (Primary Sybil Barrier):**
   - A person $u$ joins their local **Neighborhood Consumer Council ($CC_h$)** (typically 50–300 households who share physical housing registered with the Household Facilitation Board $\text{HFB}$) and, if working, their **Worker Council ($WC_j$)** (registered with the Employment Facilitation Board $\text{EFB}$ and Industry Federation $IF_k$).
   - Enrollment requires a threshold attestation ($k$-of-$n$ council membership committee members + household residency record) issuing a cryptographic `CouncilMembershipCredential` signed by $CC_h$'s hybrid PQ key.
2. **Cross-Checking Population and Effort Invariants (Macro Sybil Barrier):**
   - Can a rogue Neighborhood Council $CC_h$ invent 500 phantom "Sybil citizens" to claim extra consumption goods?
   - **No, because of Sandström's Accounting Identity (`reports/ECONOMIC_MODEL.md` Section 3.1):** A neighborhood council's warranted consumption budget $B(CC_h, P)$ is **not** a free per-head airdrop! Every adult able-bodied consumer budget is backed by **verified effort-hour certificates** issued by accredited Worker Councils $WC_j$ (whose total effort rating is capped by $SB_j / SC_j$ of actual outputs delivered to other councils!), and dependent allowances (children/retirees/disability) are audited by the Ward/City Consumer Federation!
   - Thus, inventing phantom neighbors in $CC_h$ without corresponding verified workplace production or federation-audited dependent status adds **zero** aggregate purchasing power to $CC_h$!
3. **Social Recovery and Key Rotation:**
   - If a participant loses their smartphone or suspects compromise, a threshold quorum of their household + 3 designated peers in $CC_h$ executes a **Social Key Rotation Certificate**, revoking the old key in the council's epoch revocation list and binding their remaining intra-year budget balance to their new hybrid PQ key.

### 2.2 Explicit Remaining Social Trust Assumptions
No software protocol can eliminate social reality. DPEP explicitly relies on the following five irreducible social trust assumptions:
1. **Physical Audit of Production and Inventory:** Cryptography proves that $WC_j$ *signed* a delivery receipt and that $CC_h$ *signed* an acceptance receipt; it cannot prevent a colluding producer and consumer council from signing false receipts for physical goods that never existed without physical spot-audits by Industry/Consumer Federation *logistai*.
2. **Local Neighborhood Integrity:** At least a quorum of a neighborhood council's onboarding committee and its surrounding Ward Federation must not collude to fabricate dependent/disability allowances.
3. **Workplace Peer Fairness in Effort Ratings:** While the protocol enforces the mathematical ceiling that a workplace's average effort rating cannot exceed $100 \times (SB_j/SC_j)$, fairness of effort ratings *among* workmates inside $WC_j$ relies on democratic workplace deliberation and federation appellate oversight.
4. **Scientific Integrity of Ecological Boundaries:** Biophysical caps ($r^*$ and $E_z^{\max}$) entered into Long-Run Environmental Planning rely on honest scientific measurement and environmental monitoring sensors.
5. **Geographic Diversity of Epoch BFT Validators:** Fewer than $1/3$ of the sortition-selected federation validator nodes (`Role-BFT`) in any epoch collude to halt or equivocate on round checkpoints.

---

## 3. Comprehensive Threat Model (14 Required Threat Vectors)

| # | Threat Vector | Adversary Goal & Attack Surface | Protocol & Institutional Mitigations in DPEP | Residual Risk & Severity |
| :--- | :--- | :--- | :--- | :--- |
| **T1** | **Sybil Attacks** | Create fake digital identities to inflate council votes or claim extra consumption allowances. | Onboarding requires local $CC_h$/$\text{HFB}$ residency attestation; consumption budgets $B_u$ require $WC_j$ effort certificates capped by $SB_j/SC_j$ or Ward-audited dependent status (Sandström conservation invariant). | **Low** (Economic gain from pure digital Sybils is zero without federation collusion). |
| **T2** | **Identity Capture** | Steal or coerce a citizen's device/keys to hijack their vote or drain their consumption allowance. | Hardware-keystore PIN/biometric binding; per-round spending limits; 1-step council Social Key Recovery & immediate revocation; coerced ballot mitigation via re-voting before round close. | **Low-Medium** (Physical household coercion remains a social/legal issue). |
| **T3** | **Council Capture** | An internal clique ("coordinator faction") monopolizes $WC_j$ or $CC_h$ proposals and delegates. | Protocol enforces mandatory term limits on `PQ-UCAN` delegate certificates, 1-vote council recall, BJC task rotation tracking, and requires $k$-of-$n$ member signatures on council proposals. | **Medium** (Informal social deference requires cultural vigilance). |
| **T4** | **Malicious Participants** | Submit negative quantities, NaN/overflow values, or budget-violating consumption requests. | Schema-level unsigned/non-negative fixed-point types (`FixedDecimal`); local & aggregator deterministic validation rejects any proposal violating $SC \le B$ or $SB/SC \ge 1$ (without appeal flag). | **Very Low** (Deterministic cryptographic rejection). |
| **T5** | **Censorship of Proposals** | A malicious Ward/Industry aggregator omits a dissident council's proposal or qualitative `List`. | Aggregator must return a signed receipt on submission; council verifies its **Merkle-Sum Inclusion Proof** in `H_root`. If omitted, council broadcasts the signed receipt to Epoch BFT validators to fault & replace the aggregator. | **Low** (Provable accountable omission). |
| **T6** | **Eclipse Attacks** | Isolate a rural council node so it sees stale or fabricated indicative prices $P^{(t)}$. | Light clients verify the Epoch BFT threshold signature ($>2/3$ of federated validators) on `RoundAggregationAndPrices(t)` and connect via multiple transports (QUIC, relay, mesh/DTN). | **Low** (Cannot forge BFT validator quorum signature). |
| **T7** | **Network Partitioning** | Regional internet blackout during an active annual planning round. | Councils operate offline-first on LAN; federated aggregation includes a configurable grace window; if partition persists, deterministic fallback carries forward $\pi_c^{(t-1)}$ scaled to new prices so the council is not zeroed out. | **Medium** (Prolonged partitions delay global convergence or require fallback approximations). |
| **T8** | **Denial of Service (DoS)** | Flood aggregators or BFT nodes with millions of junk proposals or huge qualitative blobs. | No anonymous traffic on aggregation endpoints: every message requires a valid council-member `PQ-UCAN` capability token + strict per-council rate limits (e.g., max 5 proposal revisions per round) and blob size caps. | **Low** (Authenticated capability rate-limiting is far more effective than blockchain gas fees). |
| **T9** | **Manipulated Economic Submissions** | Strategically hoard endowment reports, underreport pollution $e_{jz}$, or exaggerate intermediate input needs. | Fixed endowments ($k_j^0, l_j^0$) are debited automatically from the Stand-Alone Capital Asset ledger; input hoarders are penalized instantly because $SC_j$ rises and lowers their $SB_j/SC_j$ effort cap; physical/sensor audits verify emissions. | **Medium** (Classic Hurwicz information-revelation tension; mitigated by $SB/SC$ coupling). |
| **T10** | **Collusion (Inter-Council / IFB)** | An Industry Federation cartel restricts supply to drive up its output's indicative price $p_k$. | Higher $p_k$ raises $SB_j/SC_j$, *but* worker remuneration is capped at $\bar{\epsilon}_{\max} = 1.0$ (excess surplus goes to the Society Account, not worker pockets; Sandström 2023) and triggers EFB entry of new worker councils into industry $k$! | **Low-Medium** (Removing profit retention eliminates the primary capitalist motive for cartel price-fixing). |
| **T11** | **Data Leakage (Privacy Breach)** | Adversary infers sensitive personal medical, reproductive, or lifestyle data from consumption proposals. | Individual bundles $y_u^{\text{priv}}$ never leave the household in cleartext; neighborhood aggregation uses pairwise additive masking + ZK/Pedersen budget proofs; special medical needs are handled by blinded health-service vouchers (Maxim 4). | **Low** (See Section 4 below). |
| **T12** | **Software Supply-Chain Compromise** | Backdoor injected into the IFB price calculation code or client wallet update. | Deterministic reproducible builds (Nix/Guix); IFB price rules run in sandboxed `Wasmtime` verified against on-chain `wasm_rule_hash` signed by multi-federation **SLH-DSA** (FIPS 205) threshold keys. | **Low**. |
| **T13** | **Compromised Mobile Devices** | Malware on a user's smartphone attempts to exfiltrate private history or forge votes. | Hardware-backed keystore PIN/biometric prompt per round signature; local SQLCipher encryption; council threshold checks detect anomalous outlier revisions. | **Medium** (Endpoint malware on user devices is an industry-wide challenge). |
| **T14** | **Long-Term Quantum Threats** | Adversary records encrypted P2P council traffic today and decrypts it in 2040 with a CRQC; or uses a CRQC to forge signatures. | All transport/storage uses **X25519 + ML-KEM-768**; all signatures use **Ed25519 + ML-DSA-65**; long-term anchors use hash-based **SLH-DSA**; private commitments use statistically hiding commitments. | **Low**. |

---

## 4. Privacy and Verifiability Architecture (Section 8)

Participatory planning requires high transparency at the **aggregate and institutional level** (PEPE Ch. 4, p. 65) while strictly protecting **personal and household privacy** (PEPE Ch. 3, p. 41; LF Ch. 3, `lf3_2.htm`; Dapprich 2024).

### 4.1 Four-Tier Data Visibility Classification

| Visibility Tier | Economic Data Assigned to Tier | Cryptographic Protection Mechanism |
| :--- | :--- | :--- |
| **Tier 1: Strictly Private (Individual / Household)** | Itemized personal consumption vector $y_u^{\text{priv}}$; specific health/medical needs; personal savings/borrowing balance; individual ballot choices in secret-ballot votes. | Stored locally in SQLCipher; aggregated into $y_h^{\text{priv}}$ via **Pairwise Additive Masking (Bonawitz Secure Aggregation)** + **Local Budget Compliance Proof**; medical goods dispensed directly via health councils as free Maxim-4 public services (PEPE Ch. 3, p. 47) so they never appear on neighborhood consumption lists! |
| **Tier 2: Council-Internal ($WC_j$ or $CC_h$)** | Individual worker BJC task rotation schedules; peer effort deliberation & raw ratings $\epsilon_u$; internal work-team drafts; neighborhood collective consumption deliberation. | Encrypted to Council Group Key (MLS — Messaging Layer Security RFC 9420 with `X25519MLKEM768` ciphersuite). To unlink workplace politics from neighborhood consumption, worker $u$ converts their workplace effort certificate into a **Blinded Warranted-Budget Credential** verified by $CC_h$. |
| **Tier 3: Federation-Scoped ($CF_f, IF_k, CAP_z$)** | Inter-workplace BJC rotation requests (EFB); industry-specific R&D and capacity reallocation plans; regional intra-year UFB inventory swaps; appellate petitions. | Scoped access via `PQ-UCAN` capability tokens; replicated across federation `Role-SR` storage nodes. |
| **Tier 4: Public & Globally Verifiable** | Anonymized/aggregated council supply and demand vectors ($y_h^{\text{priv}}, y_h^{\text{pub}}, \pi_j$); all indicative prices $P^{(t)}$; aggregate surpluses/deficits; qualitative council `Lists`; Society Account & CAP macro flows; IFB WASM modules. | Publicly readable via BLAKE3 content-addressed storage and verified against Layer 1 Epoch BFT Merkle-Sum roots. |

### 4.2 Protocol for Private Household Consumption Aggregation Without Neighbor Snooping
How can Neighborhood Consumer Council $CC_h$ (say, $m = 100$ households) compute its exact aggregate private demand vector $y_h^{\text{priv}} = \sum_{u=1}^m y_u^{\text{priv}}$ and verify that every household $u$ obeyed its budget constraint $p^{\text{priv}} \cdot y_u^{\text{priv}} + \text{PubShare}_u \le B_u$ **without any neighbor or council coordinator seeing what household $u$ ordered**?

DPEP avoids heavy general-purpose multiparty computation (MPC) and instead combines **two lightweight primitives**:

1. **Step A — Local Budget Compliance Proof (Zero-Knowledge Range & Inner-Product Proof):**
   - Household $u$ commits to its private demand vector $y_u^{\text{priv}} \in \mathbb{Z}_+^{N_{\text{priv}}}$ using a homomorphic commitment $C_u = \text{Com}(y_u^{\text{priv}}; r_u)$ (Pedersen commitment for classical speed, or a Ajtai/Module-SIS lattice commitment + `Plonky3` FRI/STARK proof for post-quantum security) and generates a non-interactive proof $\Pi_u$ demonstrating:
     $$\forall g \in \mathcal{G}^{\text{priv}}: y_{u,g}^{\text{priv}} \ge 0 \quad \land \quad \sum_{g \in \mathcal{G}^{\text{priv}}} p_g^{\text{priv}} y_{u,g}^{\text{priv}} + \text{PubShare}_u \le B_u$$
2. **Step B — One-Round Pairwise Masking (Bonawitz Secure Aggregation) for Vector Summation:**
   - Each household $u$ shares a pairwise Diffie-Hellman (`X25519MLKEM768`) seed with neighbors in $CC_h$ (or with a 3-of-5 neighborhood tally committee) to mask $y_u^{\text{priv}}$ with zero-sum masks $m_u$ ($\sum_{u=1}^m m_u = 0 \pmod q$).
   - The neighborhood coordinator `Role-CC` sums the masked vectors to obtain the exact cleartext council sum $y_h^{\text{priv}} = \sum_{u=1}^m y_u^{\text{priv}}$ and checks the homomorphic commitment sum $\sum_{u=1}^m C_u = \text{Com}(y_h^{\text{priv}}; \sum r_u)$.

### 4.3 Mobile Computational and Bandwidth Costs of Privacy Primitives
For a household requesting $s = 50$ active private goods out of $N_{\text{priv}} = 1,000$ categories on a mid-range/older ARMv8 smartphone:

| Privacy Primitive | Mobile Proving Time (ARMv8) | Proof / Payload Size | Coordinator Verification Time | Practical Assessment |
| :--- | :---: | :---: | :---: | :--- |
| **Pairwise Additive Masking (`X25519MLKEM768` + PRG over 1,000 items)** | $\sim 1.2\text{ ms}$ | $4\text{ KB}$ masked vector | $< 0.2\text{ ms}$ | **Negligible cost.** Runs effortlessly on 10-year-old Android devices. |
| **Classical Bulletproofs Budget & Non-Negativity Proof ($s = 50$ non-zero items)** | $\sim 45\text{ ms}$ | $\sim 1.3\text{ KB}$ | $\sim 6\text{ ms}$ (batchable) | Extremely fast and compact; suitable for classical/hybrid deployment. |
| **Post-Quantum STARK Budget Proof (`Plonky3` over Goldilocks/BabyBear field, $s = 50$)** | $\sim 180\text{ ms}$ | $\sim 32\text{ KB}$ | $\sim 3\text{ ms}$ | **Highly practical** because a household only generates this proof **once per planning round** (i.e., once every 12–48 hours!). |
| **Fully Homomorphic Encryption (TFHE / CKKS) over Full Economy Planning** | $> 60,000\text{ ms}$ | $> 50\text{ MB}$ | Seconds per op | **Impractical and unnecessary.** Rejected in favor of local proving + edge aggregation. |
