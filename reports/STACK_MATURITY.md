# Technology Stack Maturity Dossier

**Deliverable:** `reports/STACK_MATURITY.md` (companion register: [`research/stack_maturity_register.csv`](../research/stack_maturity_register.csv))
**Scope:** Every component named in Architecture D (book Chapters 5–8: Fig. 5.1, Tables 6.2, 7.1, 7.2, 7.3, 8.1), with the cryptographic and post-quantum layer treated in most depth.
**Date of evidence:** 5 November 2026.
**Status:** Working draft for author review. Book table numbers refer to the 105-page build of 5 November 2026. Ratings are judgements against the rubric below, not measurements.

---

## 0. How to read this dossier

### 0.1 Three different things can be "mature"

A component can be mature at one level and immature at another. The dossier rates each separately, because conflating them is the most common error in feasibility claims:

| Level | Question | Example |
|---|---|---|
| **Primitive / protocol** | Is the mathematics or protocol standardised, analysed and trusted? | ML-KEM-768 (FIPS 203) |
| **Named implementation** | Is the specific library the book names production-grade, audited, maintained? | RustCrypto `ml-kem` crate |
| **DPEP composition** | Has anyone deployed this component *in the way DPEP combines it*? | Prio3 with a custom budget-predicate circuit and price constants |

Almost every DPEP *composition* is original and therefore research-grade (M1), even where the primitive is M5. Section 9 lists them.

### 0.2 Maturity scale

| Level | Name | Criteria (all should hold) |
|---|---|---|
| **M5** | Ubiquitous | Final standard (RFC / FIPS / ISO) or universal de facto standard; several independent implementations; deployed to billions of users or devices; ≥10 years of public analysis. |
| **M4** | Production-proven | Final standard or stable 1.x+ release; several major organisations run it in production; independent audits or formal verification exist for at least one implementation. |
| **M3** | Early production | Final standard *or* stable release, but deployment is limited to one or a few significant operators, or the standard is new (<3 years), or the specification is still an Internet-Draft. |
| **M2** | Pre-production | Implementations exist but are unaudited, pre-1.0, beta, or follow a draft that is still changing; little or no production use. |
| **M1** | Research | Papers and prototypes only; no standard; parameters or security proofs still moving. |
| **M0** | Unspecified | DPEP needs the function but has not chosen a construction. |

### 0.3 Evidence tags

- **[V]** checked on the web on 5 November 2026; the source is linked.
- **[K]** background knowledge of the authors of this dossier, not re-checked in this pass. Each [K] item should be confirmed before it is cited in the book.
- **[B]** taken from the book or its verification scripts (already audited in earlier refinement passes).

---

## 1. Summary matrix

| # | Layer | Component (as named in the book) | Primitive | Named impl. | DPEP composition | Main gap |
|---|---|---|:-:|:-:|:-:|---|
| 1 | Crypto | X25519 / Ed25519 (classical half of hybrids) | **M5** | M4–M5 | M4 | None material |
| 2 | Crypto | ML-KEM-768 in hybrid X25519MLKEM768 | **M4** | **M2** (RustCrypto) / M4 (libcrux, AWS-LC) | M2 | Book names an unaudited crate |
| 3 | Crypto | ML-DSA-65 in hybrid Ed25519+ML-DSA-65 | **M3** | M2 | M2 | Composite format still a draft; heavy at scale |
| 4 | Crypto | SLH-DSA-SHA2-192s (root / WASM signing) | **M3** | M2–M3 | M3 | Little production use; fine for rare signing |
| 5 | Crypto | BLAKE3 (Merkle roots, content IDs) | **M3** | M4 | M3 | Not NIST/IETF-standardised; 128-bit target |
| 6 | Crypto | SHA3-256 / TurboSHAKE128 (VDAF XOF) | **M5** / M3 | M4 | M3 | — |
| 7 | Privacy | Prio3 VDAF + DAP (household aggregation) | **M3** | M3 (`prio` crate) | **M1** | Custom budget circuit unspecified; draft-version drift |
| 8 | Privacy | PQ encryption of DAP report shares (HPKE) | M2 | M2 | M1 | No standard PQ HPKE suite in DAP yet |
| 9 | Integrity | Two-Root BLAKE3 Merkle aggregation | **M5** (Merkle/CT) | M4 | **M1** | DPEP-original protocol |
| 10 | Integrity | k-of-n hybrid multi-signature | M4 | M3 | M2 | Size; no PQ threshold scheme |
| 11 | Integrity | PQ threshold signatures (open question P12) | **M1** | — | M0 | NIST call opened Jan 2026 |
| 12 | Identity | PQ anonymous budget credentials | **M1** | — | **M0** | Lattice credentials 80 kB–900 kB, no standard |
| 13 | Identity | PQ-UCAN capability certificates | UCAN M2; PQ-UCAN **M0** | M2 | M0 | Does not exist; must be specified |
| 14 | Governance | Sortition beacon (VRF / VDF) | Classical M4; PQ **M1** | — | **M0** | Book already marks unresolved |
| 15 | Keys | Hardware key storage for PQ keys | M2–M3 | — | M0 | Android has no PQ keystore profile [K] |
| 16 | Transport | QUIC (`quinn`) + TLS 1.3 (`rustls`) | **M5** | M4 | M3 | PQ group must be enabled explicitly |
| 17 | Transport | `iroh` P2P (relays, hole-punching, BLAKE3 streaming) | M3 | **M3** (1.0, June 2026) | M2 | Young stable release; relay dependency |
| 18 | Transport | Delay-tolerant gateways (`Role-GW`) | M3–M4 (BPv7) | — | M1 | Not designed |
| 19 | State | SQLite + SQLCipher | **M5** / M4 | M5 / M4 | M4 | None material |
| 20 | State | CRDTs: Loro / Automerge (Yjs alternative) | M4 (theory) | M3 | M3 | Schema evolution, metadata growth |
| 21 | Consensus | CometBFT (Tendermint) epoch checkpoints | **M4–M5** | M4; PQ keys M2 | M2 | PQ is pure ML-DSA, not hybrid; 331 kB/block |
| 22 | Consensus | Simplex / HotStuff / Malachite (alternatives) | M2–M4 | M2–M3 | M1 | Simplex libs in beta |
| 23 | Execution | Deterministic fixed-point WASM on Wasmtime | **M4** | M4 | M2 | Pin LTS; NaN/fuel config must be fixed |
| 24 | Encoding | Canonical CBOR, Zstd, proto3 | **M5** | M4–M5 | M3 | Deterministic-CBOR profile to choose |
| 25 | Clients | Rust core + UniFFI + WASM/TypeScript PWA | M5 (Rust/TS) | M3–M4 (UniFFI) | M2 | UniFFI maintainers warn of "sharp edges" |
| 26 | Solvers | HiGHS, Clarabel (native + WASM), PATH | **M4** | M4 native / **M2** WASM-on-phone | M2 | No phone benchmark yet [B] |
| 27 | Research | Python (NumPy/SciPy, highspy, Clarabel-py) | **M5** | M5 | M4 | — |
| 28 | Edge AI | ETS/ARIMA forecasting; local NMT/TTS | M5 / M4 | M4 | M3 | Translation quality for low-resource languages |

**Reading the matrix.** The *primitives* are, with the four exceptions in rows 11–14, standardised and widely deployed. The *named Rust implementations* are uneven: several of the book's specific picks are less mature than readily available alternatives (rows 2, 3, 13). The *compositions* are almost all DPEP-original, which is expected for a research programme and is already reflected in the kill-gate design.

---

## 2. Cryptographic primitives (post-quantum and classical)

### 2.1 Context: where the PQ transition stands (November 2026)

- NIST published FIPS 203 (ML-KEM), 204 (ML-DSA) and 205 (SLH-DSA) on 13 August 2024 [B]. FN-DSA (FIPS 206, Falcon) is still a draft, with final publication expected late 2026 or early 2027 [V](https://www.encryptionconsulting.com/education-center/fn-dsa-fips-206/). HQC was selected in March 2025 as a code-based backup KEM; a final standard is expected in 2027 [V](https://csrc.nist.gov/News/2025/hqc-announced-as-a-4th-round-selection).
- **Key exchange has crossed into mass deployment; signatures have not.** Hybrid ML-KEM now protects most browser traffic, while PQ signatures are mostly at the library and certificate-format stage. DPEP's design leans heavily on signatures (proposals, quorum certificates, UCANs, receipts), so it sits on the less mature half of the transition.

### 2.2 X25519 and Ed25519 (classical half of every hybrid) — M5

- **Designers:** Daniel J. Bernstein (Curve25519, 2006); Bernstein, Niels Duif, Tanja Lange, Peter Schwabe and Bo-Yin Yang (Ed25519, 2011) [K].
- **Standards:** RFC 7748, RFC 8032; EdDSA is in FIPS 186-5 [K].
- **Deployment:** TLS 1.3, SSH, Signal, WireGuard, Tor and nearly every modern protocol [K].
- **Implementations:** `curve25519-dalek` / `ed25519-dalek` (audited by Quarkslab, 2019 [K]), `ring`, `aws-lc-rs`.
- **DPEP note:** keeping a classical half is the correct hedge while lattice assumptions are younger.

### 2.3 ML-KEM-768 in hybrid X25519MLKEM768 — primitive M4, deployment near M5

**Cryptographers.** CRYSTALS-Kyber team: Roberto Avanzi, Joppe Bos, Léo Ducas, Eike Kiltz, Tancrède Lepoint, Vadim Lyubashevsky, John M. Schanck, Peter Schwabe, Gregor Seiler, Damien Stehlé [K]. The security assumption (Module-LWE) builds on Regev (2005) and Langlois–Stehlé (2015) [K]. Kyber was public from 2017 and went through all three NIST rounds [K].

**Production deployments.**

| Operator / product | What it uses | Tag |
|---|---|---|
| Cloudflare edge | X25519MLKEM768 on more than two-thirds of human TLS traffic (April 2026), and opportunistically on origin connections (45 bn connections/day) | [V](https://blog.cloudflare.com/post-quantum-visibility/), [V](https://www.sdxcentral.com/news/cloudflare-45-billion-daily-connections-see-automated-post-quantum-key-exchange/) |
| Apple (iOS/macOS 26) | Quantum-secure TLS on by default in URLSession and Network.framework; CryptoKit ML-KEM-768/1024 and X-Wing HPKE | [V](https://support.apple.com/guide/security/secc7c82e533/web), [V](https://wwdcnotes.com/documentation/wwdc25-314-get-ahead-with-quantumsecure-cryptography/) |
| OpenSSH 10.0 (April 2025) | `mlkem768x25519-sha256` is the default key exchange | [V](https://www.phoronix.com/news/OpenSSH-10.0-Released) |
| Signal (Oct 2025) | SPQR "Triple Ratchet" with ML-KEM-768, formally verified with Cryspen (adds to PQXDH, 2023) | [V](https://signal.org/blog/spqr/) |
| Chrome, Firefox, Edge | X25519MLKEM768 on by default (Chrome since v131, Nov 2024) | [K] |
| Go 1.24+, OpenSSL 3.5+, BoringSSL, Java 24+ | ML-KEM in the standard library / default TLS group | [K] |
| AWS-LC FIPS 3.0 | First FIPS 140-3 validated module to include ML-KEM (all three sets) | [V](https://aws.amazon.com/blogs/security/aws-lc-fips-3-0-first-cryptographic-library-to-include-ml-kem-in-fips-140-3-validation) |

**Assurance and formal verification.**
- Cryspen's `libcrux-ml-kem` is verified with hax and F\*, and its generated C is vendored in Mozilla NSS (`security/nss/lib/freebl/verified/`) [V](https://searchfox.org/firefox-main/source/security/nss/lib/freebl/verified/internal/libcrux_mlkem_portable.h), [V](https://docs.rs/libcrux-ml-kem). OpenSSH's ML-KEM code is also understood to derive from libcrux [K, not confirmed this pass].
- Formosa Crypto (Jasmin/EasyCrypt) and `mlkem-native` (PQ Code Package, with CBMC and HOL Light proofs) provide further verified implementations [K].
- **Implementation lesson:** the 2024 "KyberSlash" timing flaws affected many early Kyber implementations [K]. Primitive maturity did not imply implementation maturity.

**The book's named implementation.** §6.2 names `RustCrypto` FIPS 203/204/205. The RustCrypto `ml-kem` crate states that it "has never been independently audited" [V](https://docs.rs/ml-kem). A July 2025 review on the NIST PQC forum said that no audited Rust crate covers all three FIPS algorithms [V](https://groups.google.com/a/list.nist.gov/g/pqc-forum/c/94RfGMmFqt0).
→ **Recommendation:** for ML-KEM, use `libcrux-ml-kem` (formally verified) or `aws-lc-rs` (FIPS-validated). For TLS/QUIC, enable `rustls`'s `prefer-post-quantum` feature with the `aws-lc-rs` provider, which makes X25519MLKEM768 the top key-exchange group [V](https://docs.rs/rustls-post-quantum/latest/rustls_post_quantum/). Keep RustCrypto as a WASM fallback only.

### 2.4 ML-DSA-65 in hybrid Ed25519+ML-DSA-65 — primitive M3

**Cryptographers.** CRYSTALS-Dilithium team: Shi Bai, Léo Ducas, Eike Kiltz, Tancrède Lepoint, Vadim Lyubashevsky, Peter Schwabe, Gregor Seiler, Damien Stehlé [K]. Assumptions: Module-LWE and Module-SIS; Fiat–Shamir with aborts (Lyubashevsky 2009/2012) [K].

**Standards.**
- FIPS 204 (final, Aug 2024) [B].
- RFC 9881, *ML-DSA in X.509 certificates*, Proposed Standard, October 2025 [V](https://www.rfc-editor.org/rfc/rfc9881.html).
- **Composite (hybrid) ML-DSA** including an Ed25519 combination: `draft-ietf-lamps-pq-composite-sigs-19` (April 2026), still an Internet-Draft [V](https://datatracker.ietf.org/doc/html/draft-ietf-lamps-pq-composite-sigs-19). DPEP's "hybrid signature" therefore has no final wire format to adopt yet.

**Deployments.**

| Operator / product | Use | Tag |
|---|---|---|
| CometBFT v0.40 + Cosmos SDK v0.55 | ML-DSA-65 consensus and account keys, **pure (not hybrid)**; validators rotate from Ed25519 | [V](https://docs.cosmos.network/sdk/latest/keys/post-quantum-keys.md) |
| Apple CryptoKit (OS 26) | ML-DSA-65 and ML-DSA-87, including Secure Enclave keys | [V](https://developer.apple.com/tutorials/data/documentation/cryptokit/enhancing-your-app-s-privacy-and-security-with-quantum-secure-workflows.md) |
| AWS KMS, Google Cloud KMS, OpenSSL 3.5, Java 24, Windows CNG | ML-DSA keys / APIs | [K] |
| Web PKI | Not yet issuing ML-DSA certificates to browsers | [K] |

**Cost signal.** Cosmos's own documentation estimates that moving a 100-validator chain to ML-DSA-65 raises signature data from about 6 kB to about 331 kB per block [V](https://docs.cosmos.network/sdk/latest/keys/post-quantum-keys.md). This independently confirms the book's 290–296 kB per 86-signature checkpoint (Table 7.8) [B].

**Named implementation.** RustCrypto `ml-dsa` carries a security warning; no audit was found [V](https://docs.rs/ml-dsa). Alternatives: `aws-lc-rs` ML-DSA [K]; `libcrux-ml-dsa` (Cryspen, verification in progress) [K].

**Rating rationale.** The standard is final and the primitive is well studied, but production deployment is about two years behind ML-KEM, and the hybrid format is unfinished. **M3** primitive, **M2** for the hybrid as DPEP uses it.

### 2.5 SLH-DSA-SHA2-192s (federation root and WASM-rule signing) — M3

- **Cryptographers.** SPHINCS+ team, including Jean-Philippe Aumasson, Daniel J. Bernstein, Ward Beullens, Christoph Dobraunig, Maria Eichlseder, Scott Fluhrer, Stefan-Lukas Gazdag, Andreas Hülsing, Panos Kampanakis, Stefan Kölbl, Tanja Lange, Martin M. Lauridsen, Florian Mendel, Ruben Niederhagen, Christian Rechberger, Joost Rijneveld, Peter Schwabe and Bas Westerbaan [K]. Descends from SPHINCS (Bernstein et al., Eurocrypt 2015) [K].
- **Security basis:** hash-function properties only. This is the most conservative assumption in the stack [B].
- **Deployment:** in OpenSSL 3.5, AWS-LC and BoringSSL [K]. Production use is mostly firmware and code signing. There, *stateful* hash-based schemes (LMS/XMSS, RFC 8554/8391, NIST SP 800-208, required for firmware under CNSA 2.0) are more widely deployed [K].
- **DPEP fit:** good. Signatures are rare (rule ratification, root accreditation), so the 16 kB size and slow signing do not matter. Consider LMS/XMSS only if the signers can be trusted to manage state; the stateless scheme is the safer default for a federated, volunteer-run setting.

### 2.6 BLAKE3 — primitive M3, implementation M4

- **Designers.** Jack O'Connor, Jean-Philippe Aumasson, Samuel Neves, Zooko Wilcox-O'Hearn (2020) [K]. It inherits analysis of BLAKE (SHA-3 finalist, 2008–2012) and BLAKE2 (RFC 7693) [K].
- **Margin.** It uses 7 rounds against BLAKE2s's 10. A designer reports no non-trivial attacks on reduced versions, and that boomerang distinguishers up to 7.5 rounds, at astronomical cost, have not improved since 2014 [V](https://bfswa.substack.com/p/6-years-after-too-much-crypto) (designer commentary, not independent review). The 128-bit target is already stated in the book [B].
- **Standards.** None from NIST, IETF or ISO [K]. This is the main maturity gap for a component that roots every checkpoint.
- **Users.** `iroh` (verified streaming), OpenZFS (checksum option), Bazel (digest function), ccache [K].
- **Recommendation.** Keep BLAKE3 for content addressing and performance-critical hashing. Register SHA3-256 or SHA-256 under `CryptoSuiteId` as a standards-track alternative for checkpoint roots, so a compliance-driven pilot can switch without a protocol fork.

### 2.7 SHA-3 / TurboSHAKE128 — M5 / M3

- Keccak team: Guido Bertoni, Joan Daemen, Michaël Peeters, Gilles Van Assche; FIPS 202 (2015) [K]. TurboSHAKE (reduced-round Keccak, with Ronny Van Keer) is specified in an RFC (RFC 9861) [K, confirm number]. VDAF-22 uses it for its XOF [B].

---

## 3. Privacy layer: Prio3 / VDAF / DAP

### 3.1 Primitive and protocol — M3

- **Cryptographers.** Henry Corrigan-Gibbs and Dan Boneh (Prio, NSDI 2017). Dan Boneh, Elette Boyle, Henry Corrigan-Gibbs, Niv Gilboa and Yuval Ishai (fully linear PCPs, CRYPTO 2019) [B].
- **Specification authors.** VDAF: Richard L. Barnes, David Cook, Christopher Patton, Phillipp Schoppmann. DAP: Tim Geoghegan, Christopher Patton, Brandon Pitman, Eric Rescorla, Christopher A. Wood [K].
- **Status.** VDAF-22 is an Informational IRTF CFRG draft (14 Aug 2026) [B]; DAP is a standards-track IETF PPM draft [K].
- **Formal analysis.** Davis, Patton, Rosulek and Schoppmann, *Verifiable Distributed Aggregation Functions*, PoPETs 2023(4). The paper proves Prio3 secure with minor changes. Its robustness proof (Theorem 1) was corrected in a 2024 revision, giving a weaker bound and a larger PRG seed [V](https://eprint.iacr.org/2023/130). **Cite the corrected ePrint version, not the proceedings version.**

### 3.2 Deployments

| Deployment | Scale / arrangement | Tag |
|---|---|---|
| Apple–Google Exposure Notifications Private Analytics (ENPA) | Prio-based; ISRG and NIH as aggregators, MITRE combining for public-health authorities; ISRG reports over 2 bn device metrics | [V](https://isrg.org/post/prio-services-for-covid-en/), [V](https://mpc.cs.berkeley.edu/posts/Privacy-Preserving-COVID-19-Exposure-Notifications) |
| Mozilla Firefox telemetry | DAP with ISRG's Divvi Up as an aggregator and Fastly running an Oblivious HTTP relay | [V](https://blog.mozilla.org/en/products/firefox/partnership-ohttp-prio/) |
| Divvi Up (ISRG) | DAP aggregator as a service, in production for more than three years | [V](https://blog.mozilla.org/en/products/firefox/partnership-ohttp-prio/) |
| Cloudflare Daphne | DAP helper implementation | [K] |

**Teams with operating experience:** ISRG/Divvi Up (also runs Let's Encrypt), Mozilla, Cloudflare Research, Apple, Google. They are natural reviewers for a DPEP custom circuit.

### 3.3 Implementation — M3

The `prio` crate (libprio-rs, ISRG/Mozilla) is production code behind Divvi Up. The book's benchmark found that version 0.18.1 implements VDAF draft 18, not 22 [B]. **Draft-version drift is a live risk:** the wire format and validity circuits can still change before an RFC.

### 3.4 DPEP composition — M1

Production deployments aggregate small telemetry vectors, such as counts and histograms, with simple validity circuits. DPEP's use differs in four ways, none with a precedent:
1. A **custom budget-predicate circuit** with prices as per-round constants (Eq. 7.1) is unspecified [B].
2. **Vectors of 200 × 16 bits per person, re-submitted at milestones,** go well beyond typical telemetry [B].
3. **Non-nested, adversarial aggregators** are run by federations with opposed interests. Production deployments use cooperating, contractually bound operators.
4. **PQ share encryption** (row 8) applies. DAP encrypts shares with HPKE (RFC 9180), which is classical. A post-quantum HPKE ciphersuite (ML-KEM or X-Wing) is still in IETF drafting [K], although Apple already ships X-Wing HPKE [V](https://wwdcnotes.com/documentation/wwdc25-314-get-ahead-with-quantumsecure-cryptography/).

---

## 4. Integrity layer: Merkle aggregation, multi-signatures, threshold signatures

### 4.1 Two-Root BLAKE3 aggregation — primitive M5, composition M1

- Merkle trees (Merkle, 1979). The closest production analogue is **Certificate Transparency** (RFC 6962 → RFC 9162; Ben Laurie, Adam Langley, Emilia Kasper). It uses signed tree heads, inclusion proofs and public auditors, and logs are run by Google, Cloudflare, Let's Encrypt, DigiCert and others [K]. The Go checksum database (`sum.golang.org`) and Sigsum are further transparency-log deployments [K].
- Merkle-*sum* trees (Maxwell, 2013) are used in exchange proof-of-reserves [K]. The book's Two-Root design replaced them [B].
- **DPEP composition (M1):** the combination of the proposals root, the totals root, the participation bitmap and the receipt challenge window is original. **Recommendation:** borrow CT's tooling (Trillian/Tessera log design, witness co-signing, gossip of tree heads) rather than writing a log from scratch.

### 4.2 k-of-n hybrid multi-signatures — M2 composition

These are concatenated signatures plus a signer bitmap, which is straightforward [B]. The issue is size, not maturity: 3,437 B per signer [B].

### 4.3 Post-quantum threshold signatures (P12) — M1

NIST published IR 8214C, *First Call for Multi-Party Threshold Schemes*, in January 2026. It is a reference-material process, not a standards competition, and preview talks of planned submissions were still under way in September–October 2026 [V](https://csrc.nist.gov/News/2026/nist-and-multi-party-threshold-schemes), [V](https://www.nist.gov/news-events/news/2026/09/nist-threshold-call-preview-talks-3-virtual). No threshold ML-DSA is standardised. The book's choice of k-of-n multi-signatures is the right one until this matures (likely 2028 or later).

---

## 5. Identity, credentials and governance randomness

### 5.1 Post-quantum anonymous budget credentials — M1 (DPEP: M0)

| Construction | Status | Tag |
|---|---|---|
| BBS signatures (IETF CFRG draft) | Classical, pairing-based; **not PQ** | [B], [K] |
| Privacy Pass (RFC 9576–9578), Apple Private Access Tokens | Deployed at scale; RSA blind signatures / VOPRF; **not PQ** | [K] |
| Bootle, Lyubashevsky, Nguyen, Sorniotti, lattice credential framework (CRYPTO 2023) | Research; IBM Research Zurich | [V](https://research.ibm.com/publications/a-framework-for-practical-anonymous-credentials-from-lattices) |
| Argo, Güneysu, Jeudy et al. (ePrint 2024/131) | Credentials under 80 kB | [V](https://eprint.iacr.org/2024/131) |
| Kemmoe, Lysyanskaya, Nguyen, PQ rate-limited tokens (NIST WPEC 2026) | 899 kB at a rate limit of 256 (prior: 3 MB) | [V](https://csrc.nist.gov/presentations/2026/wpec2026-3b3) |
| Lattice blind signatures (state of the art) | At least 20 kB per showing | [V](https://eprint.iacr.org/2024/131) |

**Assessment.** A 55 kB Prio3 report plus an 80–900 kB credential per milestone would break the ≤150 kB per round mobile target in Kill Gate 3 [B]. The book's council-accreditation fallback is the only workable early-pilot option. **Watch:** IBM Zurich (Lyubashevsky, Nguyen), Brown (Lysyanskaya) and the NIST privacy-enhancing-cryptography (PEC) workshops.

### 5.2 PQ-UCAN capability certificates — UCAN M2, PQ-UCAN M0

- The UCAN specification is at **1.0.0-rc.1** under the UCAN Working Group (spun out of Fission) [V](https://github.com/ucan-wg/spec). Its main users have been in the IPFS/Filecoin ecosystem (e.g. Storacha / web3.storage) [K]. Fission, UCAN's originator, has wound down [K, not confirmed this pass].
- **"PQ-UCAN" does not exist.** UCANs are signed with Ed25519 / P-256 / RSA via DIDs; there is no ML-DSA profile. It is a DPEP-original specification task.
- **More mature alternatives for chained capabilities:** Biscuit (Eclipse Foundation, originated at Clever Cloud; Datalog policies) [K]; macaroons (Birgisson et al., NDSS 2014; used at Google) [K]. Neither is PQ, but both are easier to re-sign with ML-DSA than inventing a format.
- **Recommendation:** rename it to "capability certificate (format TBD)" in the book until a format is chosen, and evaluate Biscuit and UCAN 1.0 against Phase 2 needs.

### 5.3 Sortition beacon — classical M4, PQ M1

Classical public randomness is mature: drand / League of Entropy (threshold BLS; Cloudflare, Protocol Labs, EPFL and others), the NIST Randomness Beacon, and ECVRF (RFC 9381) [K]. All rely on pairings or elliptic curves, or on a trusted operator. No PQ VRF or VDF is standardised [K]. The book already marks the beacon unresolved [B]; this dossier concurs.

### 5.4 Key storage on devices — M2–M3

Apple's Secure Enclave can hold ML-DSA and ML-KEM keys from OS 26 [V](https://developer.apple.com/tutorials/data/documentation/cryptokit/enhancing-your-app-s-privacy-and-security-with-quantum-secure-workflows.md). No equivalent Android Keystore/StrongBox PQ profile is known [K]. On Android, hybrid keys would sit in software, wrapped by a hardware-held classical key. That is an asymmetry worth stating in the threat model (key compromise, §7.5).

---

## 6. Networking, storage and state

| Component | Maturity | Teams / users | Notes |
|---|---|---|---|
| **QUIC** (RFC 9000, 2021) | M5 | Google, Meta, Cloudflare, Apple (HTTP/3) [K] | — |
| **`quinn`** | M4 | Underpins `iroh` and much of the Rust QUIC ecosystem [K] | PQ comes from the TLS provider (`rustls` + `aws-lc-rs`), not from `quinn` itself. |
| **`rustls`** | M4 | ISRG Prossimo funding; Cure53 audit (2020) [K] | X25519MLKEM768 available; top priority with `prefer-post-quantum` [V](https://docs.rs/rustls-post-quantum/latest/rustls_post_quantum/) |
| **`iroh`** (n0, Inc.) | M3 | 1.0.0 shipped 15 June 2026, with a supported-version policy; 1.0.3 by July 2026 [V](https://iroh.computer/blog/iroh-1-0-0-rc-1), [V](https://alternativeto.net/news/2026/6/iroh-1-0-launches-with-stable-key-based-addressing-and-broad-language-support/). Delta Chat uses iroh for real-time peer channels [K]. | Stable but young. Default relays are run by n0, so DPEP should self-host relays (`Role-SR`). |
| **`libp2p`** (alternative) | M4 | Ethereum consensus clients (Lighthouse, Prysm), Filecoin, Polkadot, IPFS [K] | A heavier but more battle-tested fallback. |
| **Delay-tolerant networking** | BPv7 M3–M4; DPEP gateway M1 | RFC 9171 (BPv7); NASA ION; Briar (Tor/Bluetooth/Wi-Fi); Meshtastic (LoRa) [K] | `Role-GW` is unspecified; evaluate BPv7 or Briar's mailbox model. |
| **SQLite** | M5 | Ubiquitous (every phone and browser) [K] | — |
| **SQLCipher** (Zetetic) | M4 | Signal Android and Desktop [K] | AES-256; data at rest is symmetric, so Grover only halves the margin. |
| **CRDT theory** | M4 | Shapiro, Preguiça, Baquero, Zawirski (2011); Kleppmann et al.; Isabelle-verified CRDTs (Gomes et al., OOPSLA 2017) [K] | — |
| **Yjs** (not named, strongest alternative) | M4 | Kevin Jahns; JupyterLab collaboration and many editors [K] | The most deployed CRDT library. |
| **Automerge** (Ink & Switch) | M3 | Kleppmann, van Hardenberg et al.; 3.0 (July 2025) reports 10× or more memory reduction [V secondary](https://handbook-hld.pages.dev/curriculum/architecture-patterns/crdt-applications/) | Production use small but growing. |
| **Loro** | M3 | 1.0 released; Rust/JS/Swift bindings; Fugue text, movable tree [V](https://github.com/loro-dev/loro/wiki) | Young; small team. |

---

## 7. Consensus and deterministic execution

### 7.1 CometBFT (Tendermint) — M4–M5 core, M2 with PQ keys

- **Researchers:** Jae Kwon, Ethan Buchman, Zarko Milosevic ("The latest gossip on BFT consensus", 2018) [B]. Maintained by Informal Systems and the Cosmos ecosystem. Formal specification and model checking in TLA+/Apalache [K].
- **Deployment:** the Cosmos Hub since 2019 and well over a hundred production chains [K].
- **PQ status:** CometBFT v0.40 with Cosmos SDK v0.55 supports **ML-DSA-65 consensus keys** [V](https://docs.cosmos.network/sdk/latest/keys/post-quantum-keys.md). This is a significant positive finding for DPEP: an off-the-shelf BFT engine now accepts PQ validator keys. Caveats:
  - The scheme is **pure ML-DSA-65, not hybrid**. DPEP's Ed25519+ML-DSA-65 hybrid would need a custom key type, or the book should accept pure ML-DSA at Layer 1.
  - About 331 kB of signature data per block at 100 validators [V].
  - Old IBC light clients cannot verify ML-DSA headers [V].
  - The implementation library is said to be Cloudflare CIRCL [V secondary](https://github.com/DoraFactory/doravota/blob/pqc-auth/x/pqcauth/pqc-migration.md).
  - Release dates and maturity of v0.40 were not confirmed in this pass.

### 7.2 Alternatives

| Engine | Researchers | Maturity | Tag |
|---|---|---|---|
| HotStuff family | Maofan Yin, Dahlia Malkhi, Michael K. Reiter, Guy Golan Gueta, Ittai Abraham (PODC 2019) | M4 via derivatives (DiemBFT/Jolteon in Aptos) | [K] |
| Simplex | Benjamin Y. Chan, Rafael Pass (2023) | M2: Commonware's `simplex` module is marked BETA | [V](https://docs.rs/crate/commonware-consensus/latest/source/src/lib.rs), [V](https://decentralizedthoughts.github.io/2025-06-18-simplex) |
| Malachite (Rust Tendermint) | Informal Systems team, now at Circle | M2: "alpha software", "not externally audited", no formal releases; parts co-designed with Quint specifications; only production user is Circle's Arc | [V](https://github.com/circlefin/malachite) |

**Malachite and the hybrid question.** Malachite takes the signature scheme as a plug-in (a `SigningScheme` interface in its core types, with Ed25519 as a separate crate) [V](https://docs.rs/informalsystems-malachitebft-core-types/latest/informalsystems_malachitebft_core_types/). An Ed25519 + ML-DSA-65 hybrid would therefore be one new crate rather than a change to CometBFT's Go code. It does not change checkpoint size: commit certificates carry one signature per validator, and neither scheme aggregates, so the book's ~290 kB per 86-signature checkpoint holds for any engine. It also brings maturity and governance costs: alpha status, no external audit, and a single corporate steward.

**Decision (provisional, 5 November 2026; not locked in).** CometBFT remains the Layer 1 reference engine. Malachite is the fallback if a hybrid consensus signature becomes a hard requirement. Simplex is not yet a responsible default. Revisit at Kill Gate 2.

### 7.3 Wasmtime deterministic fixed-point execution — M4

- **Team:** Bytecode Alliance (Mozilla, Fastly, Intel, Microsoft and others); Cranelift code generator [K]. Wasmtime 1.0 shipped in September 2022 [K]. **LTS policy:** every 12th release gets two years of security fixes [V](https://bytecodealliance.org/articles/wasmtime-lts).
- **Active scrutiny:** 12 advisories fixed on 9 April 2026, found jointly by Mozilla, UCSD, Akamai and F5 using LLM-assisted tools [V](https://bytecodealliance.org/articles/wasmtime-security-advisories). That signals an actively audited, actively attacked runtime, so DPEP must track LTS patch releases.
- **Determinism:** Wasmtime documents the controls needed (NaN canonicalisation, fuel metering, no threads or relaxed-SIMD) [V](https://docs.wasmtime.dev/examples-deterministic-wasm-execution.html). Substrate/Polkadot enables NaN canonicalisation for consensus-critical parachain validation [V](https://crates.parity.io/sc_executor_wasmtime/struct.Semantics.html). DPEP's integer-only fixed-point rule removes most float risk anyway [B].
- **Production users:** Fastly Compute, Shopify Functions, Fermyon/Akamai, and Polkadot's executor [K].

---

## 8. Clients, encodings, solvers and edge AI

| Component | Maturity | Teams / users / people | Notes |
|---|---|---|---|
| **Rust** | M5 | Linux kernel, Android, Windows, AWS, Cloudflare [K] | — |
| **UniFFI** (Mozilla) | M3–M4 | Firefox Android/iOS Application Services [V](https://firefox-source-docs.mozilla.org/rust-components/developing-rust-components/uniffi.html); matrix-rust-sdk behind Element X iOS/Android [V](https://git.oss.uzinfocom.uz/uchar/matrix-rust-sdk) | Its maintainers warn that it "is changing rapidly and has a number of sharp edges" [V]. |
| **TypeScript PWA** | M5 | — | iOS PWA storage eviction and background limits affect offline-first use [K]. |
| **CBOR** (RFC 8949) / COSE (RFC 9052) | M5 | WebAuthn/FIDO2, Matter, IoT [K] | Pick a deterministic profile (RFC 8949 §4.2 core deterministic, or dCBOR) [K]. |
| **Zstd** (RFC 8878) | M5 | Meta; Linux kernel [K] | Signatures do not compress [B]. |
| **HiGHS** | M4 | Julian Hall and the Edinburgh team; bundled in SciPy (LP from 1.6.1, MIP from 1.9.0) [V](https://cvxpy.readthedocs.io/en/latest/install/index.html); JuMP; energy-system models such as PyPSA [K] | **WASM-on-phone M2:** not benchmarked [B]. |
| **Clarabel** (Oxford) | M4 | Paul J. Goulart and Yuwen Chen; CVXPY's default solver since 1.5 [V](https://cvxpy.readthedocs.io/en/functions-table/updates/index.html); *Math. Prog. Computation* 2026 [B] | Pure Rust, so a WASM build is plausible; unbenchmarked on phones [B]. |
| **PATH** (MCP solver) | M4 | Michael Ferris, Todd Munson, Steven Dirkse [K] | Proprietary licence (book caveat) [B]. |
| **Python scientific stack** | M5 | NumPy, SciPy, `highspy` | — |
| **ETS/ARIMA** | M5 | Hyndman's methods; `statsmodels` [K] | — |
| **Local NMT** | M4 | Firefox Translations (Bergamot project: University of Edinburgh with Mozilla and partners) [K] | Weak for low-resource languages [K]. |

---

## 9. Where DPEP is original: no maturity to inherit

These are the components no outside team has deployed. Their maturity can come only from DPEP's own Phases 1–3:

1. Prio3 **budget-predicate validity circuit** with per-round price constants (§7.4) — M0/M1.
2. **Two-Root aggregation** with participation bitmap and receipt challenge (§5.3.1) — M1.
3. **Hybrid Ed25519+ML-DSA-65 wire format** for proposals, receipts and checkpoints — M1, until the composite RFC lands.
4. **PQ capability certificates** ("PQ-UCAN") — M0.
5. **PQ anonymous budget credentials with nullifiers** — M0.
6. **PQ sortition beacon** — M0.
7. **Light-client attestation policy** (Table 7.8) — M1.
8. **Non-nested adversarial aggregator governance** — M1 (an institutional design question, not a technical one).
9. **IFB price-update and Society Account rules as ratified WASM modules** — M1.

Each one either sits behind a kill gate or is explicitly marked open in the book. **No change to the gates is required by this dossier.**

---

## 10. Findings and recommended actions

| # | Finding | Severity | Recommended action | Where in the book |
|---|---|---|---|---|
| F1 | The book names **RustCrypto** for FIPS 203/204/205. Its ML-KEM crate says it has never been audited; no audited Rust crate covers all three. | Medium | Name `libcrux-ml-kem` (verified) or `aws-lc-rs` (FIPS 140-3) for ML-KEM; `aws-lc-rs` or `libcrux-ml-dsa` for ML-DSA. Use `rustls` + `aws-lc-rs` with `prefer-post-quantum` for QUIC. | §6.2 item 2; Table 6.2 row 2 |
| F2 | **CometBFT v0.40 supports ML-DSA-65 validator keys** (pure, not hybrid). | Positive / Medium | State that Layer 1 can use an off-the-shelf PQ BFT engine. Decide between pure ML-DSA at Layer 1 and a custom hybrid key type. Cite Cosmos's 331 kB/block figure as corroboration of Table 7.8. Provisional decision: CometBFT retained (§7.2). | §5.4 Table 5.3; §7.2 Table 7.1; §7.6 |
| F3 | **Hybrid signature format is not standardised** (composite ML-DSA is draft-19). | Medium | Add a sentence: DPEP will adopt `draft-ietf-lamps-pq-composite-sigs` once it is an RFC. Until then, the format is DPEP-defined under `CryptoSuiteId`. | §7.2 |
| F4 | **"PQ-UCAN" does not exist** as a specification. | Medium | Re-label it "capability certificates (format to be chosen; UCAN 1.0-rc and Biscuit are candidates, re-signed with ML-DSA)". | List of abbreviations; §1.4 Layer 3; Table 2.2; Fig. 5.1; Table 7.1 |
| F5 | **PQ share encryption for DAP** has no standard HPKE suite. | Low–Medium | Note that DAP's HPKE is classical today; name X-Wing or ML-KEM HPKE drafts as the path. | §7.4 VDAF paragraph; Table 7.2 row 1 |
| F6 | **Prio3 robustness proof was corrected** (ePrint 2023/130, 2024 revision). | Low | Cite the corrected ePrint version alongside VDAF-22. | §7.4 footnote |
| F7 | **BLAKE3 is not standardised.** | Low | Register SHA3-256 under `CryptoSuiteId` as a standards-track alternative for checkpoint roots. | §7.2 Table 7.2 |
| F8 | **Android has no known PQ hardware keystore.** | Low–Medium | Add to the key-compromise entry in the threat model. | §7.5 |
| F9 | **`iroh` 1.0 is now released** (June 2026), so maturity improved. Default relays are third-party. | Low | Update the maturity wording; specify self-hosted relays. | Table 6.2 row 3 |
| F10 | `reports/TECHNOLOGY_COMPARISON.md` §2 still recommends Pedersen commitments, Bulletproofs-era reasoning, `Plonky3` budget proofs and Bonawitz masking. The book has since replaced these with Prio3. | Medium (consistency) | Regenerate or retire that report section so it matches the book. | `reports/TECHNOLOGY_COMPARISON.md`; `README.md` "About the Book" |

Findings F11–F14, from the risk ranking, are in §11.4. **Applied on 5 November 2026:** all of F1–F14 (see `research/STACK_MATURITY_DISPOSITIONS.md`).

---

## 11. Risk ranking and mature substitution paths

This section asks which maturity gaps matter most, and whether a more mature substitute exists that keeps DPEP's core properties: decentralisation, distribution, censorship resistance, minimal trust, and no new intermediaries.

### 11.1 Which properties need post-quantum protection now

The urgency of post-quantum protection differs by property. That changes how several M0/M1 gaps should be read.

- **Confidentiality must be post-quantum now.** Ciphertext captured today can be decrypted once a cryptographically relevant quantum computer (CRQC) exists ("harvest now, decrypt later") [B]. DPEP covers this with hybrid ML-KEM, which is mature (§2.3).
- **Authenticity, Sybil resistance and randomness need post-quantum protection only before a CRQC exists.** A future CRQC can forge future signatures and bias future draws. It cannot retroactively change a finalised election or a past committee draw. Nor can it undo anonymity that rested on information-theoretic blinding: blind RSA blindness (RFC 9474) is unconditional, and statistically zero-knowledge credential proofs leak nothing a later adversary can extract [K; confirm per scheme before relying on it].
- **Two conditions apply.** These mechanisms need (i) crypto agility, so suites can be replaced before a CRQC arrives (`CryptoSuiteId`) [B], and (ii) re-anchoring of historical checkpoint archives under a hash-based signature, so old authenticity claims survive. SLH-DSA is already the book's root anchor [B].

Under those conditions, several gaps can use **mature classical schemes now with a planned migration**, without weakening any core property today. Confidentiality is the exception: it is never downgraded.

### 11.2 Ranked risks

Ranking weighs (a) how directly the gap threatens a core property, (b) how immature the best available option is, and (c) whether a fallback exists.

| Rank | Gap (dossier row) | Core property at risk | Why it ranks here |
|---|---|---|---|
| R1 | One report per person with private budgets: PQ anonymous credentials (row 12) | Privacy; minimal trust; Sybil resistance | Without it, reports are either linked to identities or vouched for by councils, which reintroduces councils as intermediaries. |
| R2 | Prio3 correctness requires **all** aggregators honest (row 7) | Minimal trust | Any one aggregator can shift demand between categories undetected and so move prices [B]. No mature construction fixes this while keeping privacy. |
| R3 | Sortition beacon (row 14) | Decentralisation; capture resistance | Committee selection is the capture point. A biasable draw undermines every later safeguard. |
| R4 | Phone clients trust their coordinator by default (Table 7.8) | Minimal trust | Most participants verify nothing themselves. |
| R5 | Key custody: no Android PQ keystore; appliance hosts hold validator keys (row 15) | Decentralisation | Whoever hosts the appliance is effectively the validator [B]. |
| R6 | Hybrid signature size and unfinished wire format (rows 3, 10) | Censorship resistance; low-end hardware | Bandwidth excludes weak links. This is mostly a size problem, not a maturity problem. |
| R7 | Unaudited RustCrypto crates, the "PQ-UCAN" format and default iroh relays (rows 2, 13, 17) | Integrity; decentralisation | Each can be fixed today with mature components. |

### 11.3 Substitution paths

| Rank | Mature substitute available now | Keeps core properties? | What remains open | Path rating |
|---|---|---|---|---|
| R1 | **Classical anonymous tokens:** Privacy Pass (RFC 9576–9578) with blind RSA (RFC 9474), deployed by Apple and Cloudflare; BBS (IETF CFRG draft). **Threshold issuance** across k-of-n councils, so no single council can mint or link credentials: Coconut (Sonnino et al., NDSS 2019), in production in Nym [K]. | Yes for anonymity (see §11.1) and decentralised issuance. Forgery becomes possible only after a CRQC, so migration is required. | Binding a secret-shared budget $B_u$ to the credential inside the Prio3 circuit (§7.4.4) has no mature path. Interim: council-attested budget bands, or the early-pilot council-trust default [B]. | **Partly credible.** Anonymity and Sybil resistance can be solved now; budget binding cannot. |
| R2 | None that is trustless. Deployed practice (ENPA, Firefox/Divvi Up) relies on **institutional independence** of the aggregator operators; DPEP adds **detection**: three non-nested aggregators with opposed interests [B]; published commitments to each aggregate share; **canary batches**: whole batches with known totals submitted by an independent auditor, which detect indiscriminate tampering with aggregate shares (not tampering aimed at batches known to be real); the public budget check [B]. | Partly. Privacy is cryptographic; correctness rests on institutions. | Robust, maliciously secure aggregation at DPEP scale is not mature. **Avoid** trusted execution environments (TEEs): they look mature but make the chip vendor the intermediary. | **No trustless path.** The book should say plainly that correctness depends on institutional independence. |
| R3 | **A drand network run by the federations themselves**: open-source threshold-BLS randomness, as used by the League of Entropy [K], with the federations holding the threshold key shares. Do not depend on the public League of Entropy network, which is a set of external operators. | Yes: distributed, no last-revealer problem, no outside operator. A CRQC could bias only future draws, so migration covers it (§11.1). | Distributed key generation ceremony and share custody across federations; migration to a PQ beacon once one exists. | **Credible.** |
| R4 | **Sync-committee pattern** (Ethereum Altair: 512-validator committee, BLS-aggregated [K]). Adapted: a small, rotating, beacon-drawn subset signs headers for phones. 24 members with quorum 16 ≈ 55 kB per round, capture probability 0.017% per draw with 42 of 128 validators faulty (16 members, quorum 11: ≈ 38 kB, 0.19%; `research/analysis/verify_sync_committee.py`). | Mostly: an explicit, rotating trust assumption replaces trust in a member's own coordinator. | Fully trustless PQ light clients (hash-based signatures aggregated with STARK proofs) are research [K]. | **Credible** as an improvement on the current default. |
| R5 | **Split hybrid custody:** the classical half of each hybrid key in hardware (Android StrongBox / Apple Secure Enclave), the ML-DSA half in software. Until a CRQC exists, a forger needs both, so the hybrid inherits hardware protection. Apple already holds both halves in hardware from OS 26 (§5.4). Validators use citizen-held tokens rather than host-held keys. | Yes. | Android PQ hardware support; a recovery UX [B]; the "host is the validator" problem is solved procedurally, not cryptographically. | **Credible.** |
| R6 | Adopt `draft-ietf-lamps-pq-composite-sigs` once published as an RFC (§2.4). Move to **FN-DSA** once FIPS 206 is final: signatures are roughly 0.7–1.3 kB against 3.3 kB for ML-DSA-65 [K], cutting checkpoint size by roughly 3–4×. Keep committees as small as the binomial tables allow [B]. | Yes. | Timing of FIPS 206 and the composite RFC; FN-DSA's floating-point signing is harder to implement safely [K]. | **Credible**, on a 1–2 year horizon. |
| R7 | `libcrux` (formally verified) or `aws-lc-rs` (FIPS 140-3) instead of RustCrypto (§2.3); Biscuit, UCAN 1.0 or COSE/CWT tokens re-signed with ML-DSA instead of "PQ-UCAN" (§5.2); self-hosted iroh relays with libp2p as fallback (§6). All are open-source libraries with no runtime dependency on their vendors. | Yes. | Engineering only. | **Credible now.** |

### 11.4 Summary

- **R3–R7** have credible mature paths that keep the core properties.
- **R1** is about half solvable today: classical credentials with threshold issuance cover anonymity and Sybil resistance; budget binding stays open.
- **R2** has no trustless answer at any maturity level. Aggregate correctness rests on institutional independence plus detection, and the book should state that explicitly rather than imply cryptography removes the trust (see F11 below).

**Additional findings for §10:**

| # | Finding | Severity | Recommended action | Where in the book |
|---|---|---|---|---|
| F11 | Prio3 aggregate correctness rests on institutions, not cryptography, and no mature trustless alternative exists. | Medium | State this in §7.4 and in Table 6.1 row 2. Add canary batches to the proposed correctness model. | §7.4; Table 7.4; Table 6.1 |
| F12 | Several M0/M1 gaps (credentials, beacon) can use mature classical schemes now, because only confidentiality needs PQ protection before a CRQC exists. | Medium | Add the §11.1 distinction to §7.2. Name federation-run drand as the interim beacon candidate and threshold-issued classical tokens as the interim credential candidate, each with a migration trigger. | §7.2; §7.4.4; §7.6 |
| F13 | The light-client default trusts a member's own coordinator. | Low–Medium | Add a rotating sortition-drawn sync committee as an option in Table 7.8. | Table 7.8 |
| F14 | Extends F8: Android has no hardware home for PQ keys. | Low | Specify split hybrid custody (classical half in hardware). | §7.5 key compromise |

---

## 12. People and organisations to approach for review

Grouped by the DPEP component each could review. Listing is for outreach planning only; no endorsement is implied.

| Component | Research groups / people | Operating teams |
|---|---|---|
| ML-KEM / ML-DSA implementations | Cryspen (Karthikeyan Bhargavan et al.); Formosa Crypto; PQ Code Package (Linux Foundation) [K] | AWS Cryptography (AWS-LC); Cloudflare Research; Google BoringSSL [K] |
| PQ protocol design | Douglas Stebila (Open Quantum Safe); Signal (Rolfe Schmidt, Graeme Connell) [K]/[V] | Signal; Apple CoreCrypto [K] |
| Prio3 / DAP | Henry Corrigan-Gibbs (MIT); Dan Boneh (Stanford); Christopher Patton; Phillipp Schoppmann; Mike Rosulek [B]/[V] | ISRG / Divvi Up; Mozilla; Cloudflare Research [V] |
| Lattice credentials | Vadim Lyubashevsky, Ngoc Khanh Nguyen (IBM Research Zurich); Anna Lysyanskaya (Brown) [V] | — |
| Hash-based signatures | Andreas Hülsing (TU Eindhoven); Daniel J. Bernstein; Tanja Lange [K] | — |
| BFT consensus | Informal Systems (CometBFT, Malachite); Rafael Pass (Cornell Tech); Ittai Abraham, Dahlia Malkhi [K]/[V] | Cosmos ecosystem validators |
| Transparency logs | Certificate Transparency team (Google); Sigsum project [K] | Let's Encrypt; Cloudflare |
| CRDTs / local-first | Martin Kleppmann (Cambridge); Ink & Switch; Kevin Jahns (Yjs) [K] | — |
| WASM determinism | Bytecode Alliance (Wasmtime/Cranelift); Parity (Substrate executor) [K] | Fastly; Polkadot |
| Optimisation | Paul Goulart (Oxford); Julian Hall (Edinburgh / HiGHS) [B]/[K] | — |

---

## 13. Method and limits

- **Sources.** Web checks on 5 November 2026 (marked [V]); the book and its verification scripts ([B]); otherwise background knowledge ([K]). Several [V] items come from secondary reporting: the Cloudflare share figures, the Automerge 3.0 memory figure, and CometBFT's use of CIRCL. Each is marked where it occurs.
- **Not done.** No source code audits; no benchmarks; no contact with maintainers; NIST CMVP certificates and IETF datatracker states were not checked live; Release dates for CometBFT v0.40 / Cosmos SDK v0.55 and the current Wasmtime LTS line were not confirmed.
- **Re-check cadence.** PQ deployment is moving quickly. Rows 2, 3, 7, 8, 11, 12, 17 and 21 should be re-checked before each phase gate.
- **Machine-readable copy.** [`research/stack_maturity_register.csv`](../research/stack_maturity_register.csv) has one row per component with ratings, evidence URLs and tags, for regeneration or filtering.
