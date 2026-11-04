# Open Theoretical, Institutional, Economic, and Technical Questions

**Deliverable:** `reports/OPEN_QUESTIONS.md`  
**Phase:** 5 — Proof-of-Concept Design & Open Research Agenda  
**Scope:** Section 14 (Unresolved theoretical, institutional, economic, and technical questions, ranked by importance).

---

## Ranking Methodology

Questions are ranked from **Priority 1 (Most Critical / Existential to System Viability)** to **Priority 15**, scored along three dimensions:
1. **Existential Impact:** If unresolved, could this issue cause the economic plan to diverge, stall, or degenerate into authoritarian/market hierarchy?
2. **Evidence Gap:** How wide is the gap between existing theoretical claims (Albert & Hahnel 1991a; Hahnel 2021) and demonstrated empirical or mathematical proof?
3. **Actionability:** Can this question be investigated directly via the proposed simulation programme (`[SIM]`) or human-in-the-loop pilot (`[HUMAN]`)?

---

## Tier 1: Critical Economic & Algorithmic Questions (Priorities 1–5)

### Priority 1: Convergence Under Genuine Non-Convexities, Fixed Setup Costs, and Complementarities (`[ECON / ALGORITHMIC]`)
- **The Unresolved Problem:** As established in our code audit of `pequod-cljs` (`research/sources/hahnel_2021_dep_analysis.md`), the 2021 computer simulations of Participatory Economics tested only smooth, strictly interior Cobb-Douglas production and utility functions where even the "increasing returns to scale" test (`toothaches?`) remained convexified by a steep effort-disutility exponent $k$. In a real industrial economy, production involves:
  1. **Strict input complementarities** (Leontief fixed proportions: a bicycle requires 2 wheels and 1 frame regardless of relative price changes).
  2. **Indivisibilities and minimum efficient scale** (opening a second shift or a new semiconductor fab is a discrete mixed-integer jump, not a continuous derivative).
  3. **Multi-output joint production** (refineries, chemical plants, agriculture).
  Under pure unregularized price tâtonnement, non-convex sets and linear segments cause supply proposals to jump discontinuously between extreme corners ("bang-bang oscillation") as prices cross critical thresholds.
- **How to Investigate (`[SIM]`):** Implement mixed-integer / piecewise-linear Leontief production sets in the DPEP simulator and compare three coordination mechanisms: (a) Hahnel's heuristic multiplicative rule, (b) Proximal / Augmented Lagrangian (ADMM) quadratic regularization with round-to-round trust regions, and (c) Industry Federation multi-unit capacity smoothing.

### Priority 2: Stability of Coupled Endogenous Income Feedback During Planning Iterations (`[ECON / ALGORITHMIC]`)
- **The Unresolved Problem:** In `pequod-cljs`, each Consumer Council's budget `(:income cc)` was held fixed as an exogenous constant across all planning iterations (`util.cljc` line 48). In real Participatory Economics and in Sandström's (2020) accounting system, aggregate consumer budgets depend dynamically on the Society Account's valuation of net output $Y^{\text{GDP}}(P^{(t)})$, workers' proposed effort hours $H^{\text{tot}}$, and CAP pollution compensation credits $p_z^{\text{pol}} E_z$. When consumer income changes every round as a function of factor and output prices, standard general-equilibrium theory (Sonnenschein-Mantel-Debreu theorem) warns that strong income effects can violate gross substitutability and induce multiple equilibria or limit cycles.
- **How to Investigate (`[SIM]`):** Run comparative convergence experiments in Milestone M1 comparing exogenous budgets against coupled endogenous Society Account budgets under varying relaxation parameters $\alpha_w \in (0, 1]$.

### Priority 3: Deliberative Complexity and Participation Fatigue in Multi-Round Planning (`[INSTITUTIONAL / HCI]`)
- **The Unresolved Problem:** Even if DPEP reduces automated computational round times to under 5 seconds, human beings must still deliberate on collective neighborhood/city consumption, workplace BJC schedules, qualitative appeals, and personal trade-offs. If annual planning requires citizens to attend 10 sequential rounds of council meetings over two months, participation attrition (as seen in Occupy 2011 and historical council movements) could hand de facto control to a small minority of "meeting athletes."
- **How to Investigate (`[HUMAN]`):** Conduct human-in-the-loop experiments using the DPEP PWA client to test a **"3-Milestone Hybrid Schedule"** (where humans deliberate at Round 1 [Initial Priorities & Collective Goods], Round 4 [Mid-Course Tradeoff Review], and Round 8 [Final Plan Ratification], while local council OR solvers execute intermediate price-clearing sub-iterations automatically within council-approved bounds). Measure participant time spent and NASA-TLX cognitive load scores.

### Priority 4: Enforcing Biophysical Ecological Limits Without Reductionist Commensurability (`[ECOLOGICAL / ECON]`)
- **The Unresolved Problem:** In the 2024 *Erasmus Journal for Philosophy and Economics* symposium, John O'Neill demonstrated a fundamental tension in Hahnel's (2021, Ch. 7) Pollution Demand-Revealing Mechanism (PDRM): PDRM prices pollution by asking local Communities of Affected Parties (CAPs) how much emission $E_z$ they are willing to tolerate in exchange for extra consumption allowances ($p_z^{\text{pol}} E_z$). This creates two dangers: (1) poorer or less risk-averse communities might accept toxic exposure for higher material consumption; and (2) cumulative, irreversible, or planetary-boundary pollutants ($\text{CO}_2$, PFAS, biodiversity loss) cannot be traded off against consumer goods (*value incommensurability*).
- **How to Investigate (`[ECON / GOVERNANCE]`):** Formalize the mathematical boundary between **inviolable *in natura* biophysical caps** ($r^*, E_z^{\max}$ determined by scientific/intergenerational Environmental Planning) and **PDRM damage pricing**. Verify in simulation how hard shadow-price barriers behave when aggregate demand hits an absolute biophysical ceiling.

### Priority 5: Coarse-to-Granular Product Disaggregation and Intra-Year Buffer Sizing (`[ECON / OR]`)
- **The Unresolved Problem:** Annual planning operates over coarse product categories ($G \sim 10^3\text{–}10^4$), whereas actual production and consumption occur over millions of granular SKUs ($G_{\text{SKU}} \sim 10^7$, Hahnel's "size 6 purple shoe" problem, DEP Ch. 8; Sandström 2025). If statistical disaggregation from coarse categories to specific SKUs has high variance, or if intra-year consumer preferences drift faster than the 3–5% planned slack buffer $SL^E$, chronic local stockouts and surpluses will occur.
- **How to Investigate (`[SIM]`):** Simulate a 2-tier inventory cascade with 50 coarse categories mapped to 2,000 granular SKUs under realistic non-stationary consumer preference drift, measuring stockout rates and UFB replanning frequency as a function of planned slack $\eta \in [1\%, 10\%]$.

---

## Tier 2: Institutional Governance & Mechanism Design Questions (Priorities 6–10)

### Priority 6: Workplace Effort-Rating Dynamics — Solidarity vs. Surveillance or Flattening (`[INSTITUTIONAL]`)
- **The Unresolved Problem:** Parecon ties individual consumption allowances to peer-assessed work effort and sacrifice (PEPE Ch. 3). Critics (O'Neill 2024; Schweickart 1993; Burczak) argue that grading coworkers' effort invites intrusive mutual surveillance, resentment, or strategic gaming ("handicap racing"), while empirical experience in many worker cooperatives (e.g., Suma in the UK) shows workers often prefer a flat equal hourly rate once job complexes are balanced, using peer accountability only for attendance and good-faith effort.
- **How to Investigate (`[HUMAN]`):** Survey and pilot with existing worker cooperatives to test whether councils prefer fine-grained numerical effort multipliers ($\epsilon_u \in [0.7, 1.3]$), coarse 3-tier ratings, or flat hourly parity ($\epsilon_u \equiv 1.0$) combined with BJC task rotation and graduated peer mediation.

### Priority 7: Preventing Industry Federation Cartelization and Gatekeeping Against Innovation (`[INSTITUTIONAL / ECON]`)
- **The Unresolved Problem:** As Hannes Kuch (2024) points out, Industry Federations ($IF_k$) wield immense institutional power: they accredit new worker councils, allocate R&D capacity, adjudicate $SB_j/SC_j < 1$ appeals, and can recommend dissolving persistently low-$SB/SC$ workplaces. What stops incumbent worker councils in an industry federation from acting like a guild—blocking a group of innovators who want to launch a new worker council with a disruptive technology that would force existing councils to retool?
- **How to Investigate (`[INSTITUTIONAL DESIGN]`):** Design and test a **"Dual-Path Startup Accreditation Rule"** where a rejected startup council can appeal an Industry Federation denial to a cross-industry Innovation Jury (selected by sortition and co-ratified by the National Consumer Federation) backed by a dedicated small-scale R&D/experimentation resource pool.

### Priority 8: Calibrating Balanced Job Complexes Across Radically Different Industries (`[INSTITUTIONAL]`)
- **The Unresolved Problem:** Balancing tasks for empowerment and desirability *within* a single workplace (e.g., Northstart publishing) is straightforward. Balancing *across* workplaces (e.g., comparing deep-sea fishing, semiconductor lithography, pediatric nursing, and sewage treatment; PEPE Ch. 2, pp. 27–30) relies on economy-wide Job Complex Committees and worker transfer queues ("voting with their feet"). How quickly and practically can cross-workplace rotation schedules (working 4 days/week in an empowering office and 1 day/week in arduous civic maintenance) be coordinated without high commuting and context-switching costs?
- **How to Investigate (`[SIM]` + `[HUMAN]`):** Model multi-workplace rotation matching as a constrained bipartite assignment problem in the EFB module, accounting for geographic travel time and minimum skill-certification requirements.

### Priority 9: Inter-Regional and International Economic Coordination Across Unequal Endowments (`[ECON / POLITICAL]`)
- **The Unresolved Problem:** Hahnel (2021, Ch. 15, p. 272) proposes that trade between participatory economies and lower-income regions follow comparative social opportunity cost while allocating $>50\%$ of the efficiency gains to the poorer region. However, within a federated economy spanning regions with vastly different climates, infrastructure, and historical wealth, how are Society Account investment funds ($\sigma_{\text{inv}} Y^{\text{GDP}}$) apportioned geographically without triggering regional secessionist friction (as seen between rich and poor collectives in 1936 Spain and 1970s Yugoslavia)?
- **How to Investigate (`[ECON / SIM]`):** Simulate multi-region investment allocation rules (per-capita parity vs. Porto Alegre-style need-weighted development matrices) over 10-year horizons.

### Priority 10: Reproductive, Domestic, and In-Home Care Labor Integration (`[INSTITUTIONAL / FEMINIST ECON]`)
- **The Unresolved Problem:** In *Democratic Economic Planning* Ch. 10 (pp. 195–210), Hahnel, Bohmer, and Chowdhury analyze reproductive and caring labor, noting that while public childcare, eldercare, and healthcare are organized as standard worker councils, **in-home domestic and caring labor inside households** poses difficult choices: should in-home care be remunerated from the Society Account as socially valued labor (risking reinforcing gendered specialization inside the home) or socialized primarily through public care councils and household BJC norms?
- **How to Investigate (`[INSTITUTIONAL / HUMAN]`):** Require Women's and Caregivers' Caucuses (DEP Ch. 10, p. 200) in the governance design of any pilot community to determine how care allowances and parental/caregiver effort credits are accounted for in the protocol.

---

## Tier 3: Distributed Systems, Cryptography, and Transition Questions (Priorities 11–15)

### Priority 11: Byzantine Resilience During Prolonged Regional Network Partitions (`[DISTRIBUTED SYSTEMS]`)
- **The Unresolved Problem:** During an annual planning cycle, if a region of 500 councils loses external internet connectivity for 5 days due to a natural disaster or state censorship, holding up the entire national planning iteration violates liveness, whereas proceeding without them violates their self-management rights.
- **How to Investigate (`[SIM / SW-ARCH]`):** Test the accuracy of **Automated Regional Proxy Extrapolation** (where the last known regional Merkle-Sum node and local price elasticities are used as a temporary proxy in global rounds $t+1, t+2$, reconciled via local UFB slack adjustments when the partition heals).

### Priority 12: Post-Quantum Threshold Signatures and Lattice ZK Proof Standardization (`[CRYPTOGRAPHY]`)
- **The Unresolved Problem:** While NIST standardized single-signer `ML-DSA` (FIPS 204) and `SLH-DSA` (FIPS 205) in 2024, compact post-quantum **threshold signatures** (e.g., threshold ML-DSA without interactive round explosion or large signature sizes) and standardized compact **lattice-based zero-knowledge proofs** are still undergoing NIST Call for Multi-Party Threshold Schemes evaluation as of 2026.
- **How to Investigate (`[CRYPTOGRAPHY]`):** Use deterministic $k$-of-$n$ multi-signatures (or classical FROST + concatenated ML-DSA signer bitmaps for small council quorums) and hash-based `Plonky3` STARKs today, while maintaining cryptographic agility (`CryptoSuiteId` header) to drop in standardized threshold ML-DSA once finalized.

### Priority 13: Privacy vs. Accountability in Small Rural Councils ($m < 20$ Households) (`[PRIVACY / CRYPTO]`)
- **The Unresolved Problem:** In a 200-household urban neighborhood council, aggregating private consumption via pairwise masking ($y_h^{\text{priv}} = \sum_{u=1}^{200} y_u^{\text{priv}}$) provides strong $k$-anonymity. In a tiny 12-household rural hamlet, if the hamlet's aggregate demand vector shows 1 unit of a rare item, neighbors can trivially deduce that someone in the 12-household hamlet ordered it.
- **How to Investigate (`[SW-ARCH]`):** Allow small councils ($m < 50$) to merge their *private consumption aggregation anonymity set* at the **Ward Federation level** ($m \ge 250$) while keeping collective neighborhood good deliberation at the local hamlet level!

### Priority 14: Hardware Endpoint Security vs. Open Modifiability on User Devices (`[SECURITY]`)
- **The Unresolved Problem:** Protecting against compromised mobile devices (`Threat T13`) favors hardware remote attestation (Android Play Integrity / Apple App Attest), *but* relying on proprietary Big Tech attestation APIs violates requirement 9 ("Resistance to platform lock-in" and open-source software freedom).
- **How to Investigate (`[SECURITY]`):** Rely on local hardware keystore PIN/biometric unlocking + council-level social verification and statistical outlier prompts rather than mandatory proprietary OS remote attestation.

### Priority 15: Bootstrapping a "Parallel Participatory Economy" Within a Capitalist Market Environment (`[ADOPTION / TRANSITION]`)
- **The Unresolved Problem:** As Albert & Hahnel (1991a, Ch. 6, pp. 129–130) propose in "Experiment 2: Developing a Parallel Economy," the most realistic path to testing and adopting DPEP is within networks of existing worker cooperatives, consumer co-ops / community-supported agriculture (CSAs), and municipal participatory budgets. However, these entities must pay taxes, buy external raw materials, and service external debts in fiat currency.
- **How to Investigate (`[ECON / ADOPTION]`):** Design a **Boundary Reserve & Dual-Price Bridge Module** in Sandström's Society Account that treats the external capitalist market as a "rest-of-world trading partner" (DEP Ch. 15), clearing internal cooperative labor and goods via participatory indicative prices while pooling external fiat revenues/inputs across the federation.
