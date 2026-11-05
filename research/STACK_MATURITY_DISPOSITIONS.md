# Stack maturity pass: dispositions

**Start state:** commit `bd14ddb` (branch `third-refinement`) plus the uncommitted `reports/STACK_MATURITY.md` and `research/stack_maturity_register.csv`.
**Date:** 5 November 2026.
**Source of findings:** `reports/STACK_MATURITY.md` §10 (F1–F10) and §11.4 (F11–F14).
**Result:** `book/dpep_book.tex` rebuilt with tectonic to 106 pages (was 99; 105 after the first batch) and copied to both PDF locations. `research/analysis/check_book.py` passes. There are no undefined references and no overfull box over 10 pt. The only log warnings are the existing font-substitution notices.

## Author decisions recorded (5 November 2026)

1. **Interim classical credentials and beacon adopted**, on condition that they are crypto-agile, so post-quantum primitives can replace them easily later. In the book: design rule "Interim Classical Constructions Under Crypto Agility (adopted)" in §7.2.1, with four conditions: suite inside the signature, no downgrade below a ratified floor, published migration triggers, and history re-anchored under SLH-DSA.
2. **No commitment to pure ML-DSA at the consensus layer.** The validator suite is the strongest the engine supports at deployment. It moves to ML-DSA by key rotation, and to the hybrid once a composite standard and engine support exist. CometBFT remains the provisional reference engine; Malachite is the fallback. Book sizes still assume the hybrid (worst case).

## Findings applied in this pass

| ID | Edit | Location in book |
|---|---|---|
| F1 | RustCrypto replaced by `libcrux` / `aws-lc-rs`; RustCrypto kept as a WASM fallback; footnote with sources; `rustls` hybrid key exchange named. | §6.2 item 2; Table 6.2 row 2 |
| F2 | CometBFT v0.40 ML-DSA-65 keys (pure), the Cosmos 331 kB/block estimate as corroboration, and the Malachite fallback. | §7.2.1 "Layer 1"; Table 7.3; Table 6.3 |
| F3, F5 | Paragraph on formats still in standardisation (composite ML-DSA draft; RFC 9881; classical HPKE in DAP). | §7.2, after the opening paragraph |
| F4 | "PQ-UCAN" renamed CapCert ("format to be chosen; signed under the active `CryptoSuiteId`"). | Abbreviations; §1.4; Table 2.2; Fig. 5.1; Table 7.1 |
| F6 | Davis et al. (2023) security analysis cited, with the corrected full version (ePrint 2023/130). | §7.4 footnote; bibliography |
| F7 | SHA3-256 registered as an alternative to BLAKE3 for checkpoint roots. | Table 7.2 |
| F9 | `iroh` 1.0 (June 2026) and self-hosted relays. | Table 6.3 |
| F12 | New §7.2.1: which properties need post-quantum protection now; design rule; Table 7.3 (urgency, construction now, upgrade trigger); credential selection criterion (unlinkability must not rest on a CRQC-breakable assumption); interim beacon; Layer 1. Pointers added in §7.4.4 and §7.6, and §1.4 Layer 1 reworded. The credentials/beacon row of Table 7.2 changed from "Unspecified" to "Interim classical". | §7.2.1; §7.4.4; §7.6; §1.4; Table 7.2 |
| — | New §6.3 Component Maturity: three-level rating, scale, Table 6.3 (18 rows), nine original combinations mapped to Kill Gates 2/3, re-check rule. | §6.3 |

New bibliography entries: Davis et al. (2023), Massimo et al. (2025, RFC 9881), Ounsworth et al. (2026, composite draft-19), Sonnino et al. (2019, Coconut), Bootle et al. (2023), Argo et al. (2024). Each was checked against its publisher, RFC Editor, Datatracker or IBM Research page on 5 November 2026. `audit_bibliography.py` was not re-run.

## Second batch (same day): remaining findings

| ID | Edit | Location in book / repository |
|---|---|---|
| F8 / F14 | Split hybrid custody in the key-compromise entry: classical half in the platform keystore, ML-DSA half in software encrypted under a hardware key; Apple Secure Enclave holds ML-DSA from OS 26; no Android equivalent found. P14 row points to it. | §7.5 Key compromise; open-questions table, P14 (Ch. 10) |
| F11 | Correctness model: canary batches added; explicit statement that cryptography guarantees privacy, not correct totals; TEEs rejected. New canary-batch row in the aggregator-options table. Table 6.1 row 2 rationale extended. | §7.4; Table 7.4; Table 6.1 |
| F13 | Sync-committee row in the light-client table (24 members, quorum 16, ≈55 kB, capture 0.017% per draw at 42/128 faulty; 16 members, quorum 11, ≈38 kB, 0.19%); paragraph and Ethereum spec footnote. Figures from new `research/analysis/verify_sync_committee.py` (output `sync_committee_results.json`). | Table 7.8; §7.6 |
| Register | Appendix A: CLM-TECH-07, CLM-SEC-09, CLM-SEC-10, CLM-SEC-11 added; CLM-SEC-06 evidence and limitations updated. `research/CLAIMS_REGISTER.md` updated to match. | Appendix A |
| Open questions | P12 cites NIST IR 8214C (January 2026). Weakness-table rows for the beacon and credentials name the interim constructions. | Open-questions table (Ch. 10); weaknesses table (Ch. 12) |
| Ch. 9 | Pre-registration paragraph: re-check the fast-moving maturity rows before each gate. | §9.1 |
| §1.3 | Plain statement: names the functions without a standardised, deployed primitive and notes that most combinations are original. | §1.3 |
| F10 | `reports/TECHNOLOGY_COMPARISON.md`: status note marking §1 scores and earlier mechanisms as superseded by the book; §2 rewritten to match the book; language-table PQ row updated. `README.md`: page count (105→106 after rebuild) and the "About the Book" stack line. | Outside the book |

The dossier was corrected to match: canary *batches* (not individual canary reports, which cannot reveal tampering with a secret-shared sum), the sync-committee figures from the script, and the statement that ENPA and Firefox rely on institutional independence (detection is DPEP's addition).

## Third batch (same day): protocol diagrams

Eight TikZ figures were added in the existing figure style. Shared styles (`dbox`, `dhead`, `dcrypto`, `dinst`, `dwarn`, `darr`, `dlab`, `dlife`) are defined in the preamble. The book is now 111 pages, `check_book.py` passes, there are no undefined references and no overfull box over 10 pt. The last two rows of the open-questions table (P14, P15) are kept together so P15 no longer sits alone on a page.

| Figure | Label | Location |
|---|---|---|
| 5.2 One planning round as a message sequence (12 steps, 5 lanes) | `fig:round-seq` | §5.2, after Fig. 5.1 |
| 5.3 Two-Root aggregation, inclusion path, bitmap, censorship challenge | `fig:two-root` | §5.2.1 |
| 5.4 Federation topology and node placement; non-nested aggregators | `fig:topology` | §5.3 (new label `sec:roles`) |
| 7.1 Crypto-agility lanes and four-step migration | `fig:agility` | §7.2.1 |
| 7.2 Identity separation and the two credential paths | `fig:identity` | §7.3 (new label `sec:membership`) |
| 7.3 Household report flow; privacy/correctness asymmetry | `fig:privacy-flow` | §7.4 |
| 7.4 Annual calendar: milestones, automated rounds, 425 blocks/year | `fig:calendar` | §7.4.3 |
| 7.5 Trust map: guaranteed, detected, institutional | `fig:trust-map` | §7.5 |

Known limitation: bold text does not render in the tectonic build (Palladio bold shapes are substituted, as noted in the third-refinement dispositions). This affects the existing figures and design-principle headings in the same way.

## Fourth batch (same day): repository paths moved to footnotes

At the author's request, references to scripts and files in this repository were moved out of running text into footnotes giving the full path: colophon source list; executive-summary Table 1.1 (one footnote via mark and note, as the table already did for Hurwicz); §4.4 audit, stress-test and reference-test results; §6.1.1 sensitivity analysis; §6.3 maturity dossier; §7.6 binomial tails; §9.1 pre-registration directory; Table 9.3 methodological note; Appendix A evidence fields (ten footnotes); bibliography introduction. Book now 112 pages; checks pass.

Deliberately left in place:
- Table notes below Tables 1.2, 5.1, 6.1 and 7.5 ("Source: …"). These already sit outside the running text as each table's own note.
- Upstream `pequod-cljs` file names (`dep1ex*.csv`, `csvgen.clj`, `wcs.clj`). They name the external material audited, not this repository's scripts.
- Bibliography entries that say where a source copy is preserved in `research/sources/`.
- `council_participation_bitmap`, a protocol field name.

## Fifth batch (same day): list of abbreviations

The author noted that NIST was missing. A scripted comparison of capitalised tokens in the body against both abbreviation lists found more. Added to list A: CLT, DAANES, GDPR, SDF, TFEU. Added to list B: AI, BBS, BHT, BLS, CFRG, CPU / RAM, CSV, DAP, DP, FN-DSA, FOC, GC, HCI, HPKE, HQC, IDL, IETF / IRTF, IIS, KEM, LAN / WAN, LFS, LLM, LWE / SIS, M0–M5, MCP, NIST, PQ, PRG, RFC, SDK, SHA-2 / SHA-3, SQL / REST, TLS, UCAN, UI / UX, VRF / VDF, X25519 / Ed25519, XOF. Both lists are now sorted alphabetically (they were partly unsorted). Book is 113 pages; checks pass.

Not added: units (kB, MB, GB), country and region codes (EU, UK, US), publisher and venue names in citations (ACM, IACR, USENIX), requirement, claim and question identifiers (REQ-…, CLM-…, P1–P15), source-classification tags ([ORIGINAL-1991] and similar, defined in Chapter 3), and protocol names that are not abbreviations (STIR, WHIR).

## Corrections to the dossier made during this pass

- Bootle, Lyubashevsky, Nguyen and Sorniotti is CRYPTO 2023, not PKC 2025. Corrected in the dossier §5.1.
- The Prio3 proof correction is dated to a 2024 revision; the ePrint page's last revision is 25 September 2024. The dossier now says "2024 revision".
- RFC 9474 does not state that blind-RSA blindness is unconditional. The book therefore treats statistical blinding / zero-knowledge as a selection criterion to verify, not as a fact about classical credentials.
- Dossier references to book Tables 7.3–7.7 renumbered to 7.4–7.8 after the new Table 7.3.
