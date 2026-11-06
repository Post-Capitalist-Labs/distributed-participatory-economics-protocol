# Executive Summary: Distributed Participatory Economics Protocol (DPEP)

**Deliverable:** `reports/EXECUTIVE_SUMMARY.md`
**Imprint:** Post-Capitalist Labs Imprint (`https://github.com/Post-Capitalist-Labs`)
**Status:** Working Draft Monograph (November 2026), third refinement
**Canonical text:** `book/dpep_book.tex` (PDF: `Distributed_Participatory_Economics_Protocol_Book.pdf`, 99 pages). Where this summary and the book differ, the book wins.

---

## 1. Purpose

DPEP is an open-source research programme asking whether distributed computing, applied cryptography and optimisation can support democratic, non-market, non-command economic coordination, as proposed by Albert and Hahnel's participatory economics. Architecture D (local-first clients, Two-Root BLAKE3 aggregation, selective BFT checkpoints) is the **leading hypothesis**, not a demonstrated system. Nothing has been implemented.

## 2. What is established, estimated and unknown

- **Established.** The 1991 model and its formalisations are coherent at the level of accounting identities. `pequod-cljs` Cobb–Douglas runs (`dep1ex61–100`, fixed incomes) reach 5% imbalance in 11.85 rounds. The price rule fails Scarf's cycle, where incomes move with prices (min imbalance 10.5%), and a single lumpy plant (50.4%); with fixed budgets it clears Scarf's consumers (below 0.02%). NIST FIPS 203–205 are standards. `Prio3SumVec` sizes and desktop timings are **measured** with libprio 0.18.1: a dense 3,000-category, 20-bit report is 975,760 B to the leader and about 3.5 ms to verify per aggregator on one desktop core. A coarse 200-category, 16-bit report is 55,120 B and about 0.25 ms.
- **Estimated, not measured at scale.** Round time, archive sizes (0.24–1.46 GB raw per round at $10^6$), mobile traffic, hosting (\$3k–\$6k/month for 100 servers), and aggregator CPU at $10^6$ participants (about 4 coarse to 61 dense desktop core-minutes per aggregator per fresh-report round).
- **Unknown.** Whether any solver clears Leontief, lumpy, endogenous-income and strategic economies. Whether ordinary people sustain multi-round planning without a technical elite forming. How household budgets can be checked privately when prices change between rounds. Whether one-report-per-person can be enforced without a population register.

## 3. Most consequential changes in this pass

1. **The gates can now fail.** Each kill gate has pre-registered pass and fail conditions, a consequence (proceed / narrow / redesign and rerun / stop) and a reason. Thresholds are proposed for author ratification (book Table 9.2). Pre-registration lives in `research/preregistration/` with a signed tag deposited externally.
2. **Success is no longer one-sided feasibility.** The single-plant case was "feasible" at round 3 with 42% of output unused. The book now distinguishes *feasible*, *cleared* and *socially acceptable* (Definition 4.2), and Gate 1 requires clearing.
3. **Algorithm 3b is corrected.** The printed form was an Arrow–Hurwicz-type iteration that oscillates on linear welfare. It is now Deng et al.'s Algorithm 4 with a slack block and the correct proximal condition. Algorithm 3d is added as a candidate endogenous-income solver (a damped budget fixed point; no convergence theorem).
4. **A privacy baseline that can work.** The coarse `Prio3` mode (200 categories, 16-bit Household Reporting Units, 55 kB) replaces the impossible "50 sparse items" row. Council-level trust with no household cryptography is proposed for early pilots.
5. **Carry-forward is redesigned.** VDAF-22 permits each Prio3 report to be aggregated only once. Fresh budget-checked reports are therefore taken at milestone rounds, with aggregates carried between them, and rounds cannot be re-run from stored reports.
6. **Sources.** The *Science & Society* critique is by **David Laibman**, not Seth Ackerman (pp. 207–234; response by Hahnel, 78(3) 379–389). Kuch's title was wrong. Caspe figures are now a sourced range dated February 1937. Levy (1991) and Freundlich (2015) are removed. 72 bibliography entries were audited: 39 confirmed, 9 corrected, 9 partially confirmed, 12 not confirmed, 3 removed.
7. **Architecture comparison is honest about A.** After rescoring against measured costs, D scores 4.07 against A 3.10 at baseline weights. **A overtakes D once simplicity, throughput and cost carry ≥63% of the weight**, which supports using A for Phase 1H and the first pilots.

## 4. Gates (proposed thresholds, for ratification)

| Gate | Pass (abridged) | Fail (abridged) | Consequence |
|---|---|---|---|
| 1 Economic | ≥90% of convex and Leontief instances cleared in ≤25 rounds; ≥70% of staggered-lumpy; 100% of infeasible instances detected; ≥70% of endogenous-income instances; median welfare gap ≤5% | <50% convex and Leontief cleared, any infeasible instance reported feasible, or median gap >15% | Proceed / narrow to passing classes / rerun once / stop |
| 1H Human | ≥80% completion; median comprehension ≥70%; ≤25% drafts accepted unopened; ≥50% substantive override reasons; top 20% originate ≤60% of adopted amendments | <60% completion, comprehension <50%, >50% unopened, or top 20% >80% | Proceed / redesign once / stop human-facing claims |
| 2 Distributed | 100% tamper detection over ≥1,000 trials; p95 round ≤10 min at ≥$10^4$, ≤60 min extrapolated to $10^6$; ≤10× an Architecture A baseline | Any miss; p95 >30 min; >50× overhead | Proceed / narrow / stop and pilot on A |
| 3 Crypto, mobile, pilot | Audit with no open critical or high findings; ≤150 kB ordinary round, ≤450 kB full-check round, RAM ≤150 MB; pilot retention ≥70% | Open critical finding; any device metric >2× cap; retention <40% | Proceed / council-level trust only / stop custom circuits |

## 5. Budget (proposed; assumed \$120k–\$180k loaded per FTE-year)

| Phase | Staff, time | Estimate |
|---|---|---|
| 1 | 1.0 FTE, 4–6 months | \$41k–\$93k |
| 1H | 1.0 FTE, 3–4 months, plus ethics, consent, compensation, data protection | \$38k–\$85k |
| 2 | 2.5 FTE, 4–6 months | \$102k–\$230k |
| 3 | 4.0 FTE, 9–12 months, plus audit and pilot data protection | \$440k–\$950k (Phase 3 alone) |
| Programme | if every gate passes | \$0.62M–\$1.36M |

The previous table's implied rates were inconsistent (about \$150k–\$180k per FTE-year in Phase 1, \$280k–\$300k in Phase 2, about \$120k in Phase 3), and its "2026 Verified Rates" label had no source; both are replaced.

## 6. Decisions for the author (recommendations in the book, labelled "proposed")

1. **Gate thresholds and consequences:** as in section 4.
2. **Privacy baseline:** coarse `Prio3` (200 × 16-bit) for household cryptography; council-level trust (no household crypto) for Phase 1H and the first Phase 3 pilots.
3. **Aggregator correctness:** three non-nested aggregators from organisations with different interests, plus the public budget check and aggregate-share commitments; not nested CC/Ward/Federation. Robust MPC deferred.
4. **Effort rating:** $\bar\epsilon_{\max}=1.0$; individual spread $\epsilon_{\max}=0$ (flat pay per accredited hour) unless a council votes for peer-rated spread capped at 0.15. This honours Maxim 3 through hours and job balancing but not, by default, through intensity.
5. **Subtitle:** recommend replacing "A Rigorous, Source-Grounded Feasibility Study and Post-Quantum Technical Architecture…" with "A Source-Grounded Research Programme and Post-Quantum Technical Architecture…". The cover is unchanged pending the author's decision.

## 7. Strongest remaining criticisms (severity)

- **Critical:** participation at scale; a technical elite forming around the software; no solver shown to clear full DPEP instances; no credential construction for household cryptography.
- **Major:** federations as hidden central authorities (Kuch); round cost at $10^6$; aggregator correctness; one-good results not transferring; ratchet and incentive limits; foreign trade and defence unspecified.

---

# Superseded second-refinement summary (kept for the record; do not quote)


**Deliverable:** `reports/EXECUTIVE_SUMMARY.md`  
**Imprint:** Post-Capitalist Labs Imprint (`https://github.com/Post-Capitalist-Labs`)  
**Status:** Working Draft Monograph (November 2026)  
**Canonical text:** `book/dpep_book.tex`

---

## 1. Purpose and Scope

The **Distributed Participatory Economics Protocol (DPEP)** is an open-source research and systems-architecture programme investigating whether contemporary distributed computing, applied cryptography, and mathematical optimisation can provide a practical technical foundation for democratic, non-market, non-command economic coordination.

Its intellectual foundation is **Participatory Economics (Parecon)** (Albert and Hahnel 1991a, 1991b, 2003; Hahnel 2021), combined with Anders Sandström's double-entry social accounting and historical experiences of worker and community self-management.

This working draft separates **what has been empirically demonstrated**, **what has been analytically estimated**, and **what remains open**. Architecture D is the **leading long-term hypothesis**, not a commitment demonstrated at scale.

### Central finding

The principal bottleneck is **economic, algorithmic, cryptographic, and institutional**, not raw compute:

1. **`pequod-cljs` CSVs** (`dep1ex61–100`, n=40) reach 5% imbalance in 11.85 Year-1 rounds and 6.58 Year-2 rounds under unconstrained Cobb–Douglas with **fixed** incomes. That is not a non-convex or endogenous-income result. The toothache construction predicts unbounded/saddle supply on the 20% of councils it selects in the 50 real `.clj` files; that perverse supply is **not** observed in committed CSVs. Heuristic tâtônnement fails Scarf (min ρ 10.5%) and a single lumpy plant (50.4%). One-good Shapley–Folkman at K=20 has a **best-round** 0.40% and a **last-100-round max** of 8.4% at a=70.
2. **`Prio3` / VDAF-22** (Informational draft, 14 August 2026) gives measurement **privacy if ≥1 aggregator is honest** and **correct totals only if all are honest**. Nested CC/Ward/Federation aggregators are a weak independence story. Dense reports at $G_{\mathrm{priv}}=3{,}000$ and 20 bits are ≈946 KiB to the leader, not 75 KB. There is no “100% post-quantum / zero lattice” claim: ML-KEM is lattice; BLAKE3 is specified at 128-bit security for all goals.
3. Cryptography does not prove physical output, honest labour rosters, or that a federation MILP is politically legitimate.

Phase 1 (economic coordination) and Phase 1H (30–60 self-selected volunteers on Architecture A) are kill gates. They cannot, by themselves, underwrite a protocol.

---

## 2. Three-tier classification

| Tier A (CSV / Python stress tests) | Tier B (schema estimates; unbenchmarked) | Tier C (open) |
| :--- | :--- | :--- |
| `dep1ex61–100.csv`: 11.85 / 19.20 / 6.58 rounds. `dep1ex01–50.csv`: 11.18 Year-1 5%. | Leaf transport + BFT 9–27 s **omits** `Prio3` verify-share. | Algorithms 3a–3c on pre-registered Scarf, lumpy, endogenous, ecological instances. |
| Scarf min ρ 10.5% (endowment incomes; fixed budgets < 0.02%); single plant 50.4%. | n=128 quorum signatures ≈ 283 KB. Dense `Prio3` ≈ 946 KiB; sparse 50-item ≈ 18 KiB. | Budget credentials, sortition beacon, aggregator correctness beyond VDAF. |
| K=20 one-good: min 0.40%; last-100 max 8.4%; sweep median 6.0%. | Layer-1 ≈ 284 MB/year at 10 rounds. Leaf archive ≈ 0.6 GB Zstd / 2.1 GB raw. | Phase 1H agency; ratchet; labour floor; foreign trade and defence. |

---

## 3. Architecture D (leading hypothesis)

Four-layer hybrid: local-first councils, Two-Root BLAKE3 aggregation, epoch BFT with **n=128**. Weighted score in Table 6.1 is **4.32** after privacy/trust/BFT/PQ/energy rescores — expert judgement, not a measurement. D equals or beats A on 13 of 14 cells, so weight changes test little. The previously published A 4.65 / D 3.60 pair is **unreproducible** (D cannot fall below 3.65 at any 70% weighting of its weakest cell). Architecture A is used for Phase 1H because a disclosed trusted server matches a small probe.

Algorithms 3a–3c are **research candidates**. Deng et al. (2017) do not give a rate for endogenous-income DPEP.

---

## 4. Kill gates (summary)

| Phase | Gate | Cost (labour + hosting; audit separate) |
| :--- | :--- | :--- |
| 1 | Pre-registered instances including Scarf, infeasible caps, strategic behaviour, endogenous income. Report failures. 1,000 councils do not imply $10^6$. | \$25k–\$45k labour; \$0–\$100 compute |
| 1H | Completion, override **and** comprehension **and** reasons. n=30–60 cannot speak to democratic agency. | \$50 hosting + 1 FTE |
| 2 | Detection of omission; latency **including** report verification. | \$150k–\$280k |
| 3 | Mandatory \$50k–\$150k external audit. `<400 KB/round` **reopened** (283 KB signatures already). | \$250k–\$950k programme |

---

## 5. Strongest remaining criticisms (six audiences)

See Chapter 12. All listed rows are **Open**: aggregator correctness; $B_u$ credentials and sortition beacon; endogenous-income solver; Shapley–Folkman overclaim withdrawn; 30–60 volunteer probe; Maxim 3 vs $\epsilon=1$; ratchet; labour floor; consumption invisibility vs 1991 criticism; foreign trade and defence.
