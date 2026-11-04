# Source Analysis: Subsequent Developments, Accounting, Simulations, and Critiques (2020–2024)

**Sources Covered:**
1. Robin Hahnel (with contributions by Peter Bohmer, Savvina Chowdhury, Allison Kerkhoff, Mitchell Szczepanczyk, and Michael Weisdorf), *Democratic Economic Planning*, Routledge, 2021 (ISBN 978-1-032-00332-0, DOI `10.4324/9781003173700`).
2. Robin Hahnel, *A Participatory Economy*, AK Press, 2022 (ISBN 978-1-84935-484-4).
3. Anders Sandström, *Anarchist Accounting: Accounting Principles for a Democratic Economy*, Routledge, 2020 (ISBN 978-0-367-47703-5, DOI `10.4324/9781003036005`) and "An Accounting System for a Libertarian Socialist Economy" (`participatoryeconomy.org`, Feb 14, 2023).
4. Mitchell Szczepanczyk, "Pseudocode and Algorithms for Computer Simulations of Democratically Planned Economies," *Journal of Information Economics* 1(3), 43–54, 2023 (`doi:10.58567/jie01030004`), and `pequod-cljs` open-source repository (`https://github.com/msszczep/pequod-cljs`).
5. *Erasmus Journal for Philosophy and Economics* (EJPE), Vol. 17, Issue 2 (Winter 2024), Special Issue on Robin Hahnel's *Democratic Economic Planning* (papers by John O'Neill, Hannes Kuch, Jan Philipp Dapprich, and replies by Robin Hahnel).

---

## 1. Key Theoretical & Procedural Advances in Hahnel (2021), *Democratic Economic Planning*

### A. Explicit Ownership Doctrine: The "Productive Commons" (Ch. 6, pp. 98–102)
- Replaces vague notions of "public ownership" with a formal **Productive Commons**: all natural resources (land, water, ecosystems, atmospheric sinks) and produced capital goods (factories, machinery, infrastructure) belong jointly to all citizens.
- Worker councils do **not** own their factories or equipment; they acquire temporary **user rights** during the annual planning process and are charged the opportunity cost (indicative rental price) of every natural resource, capital asset, and category of labor they utilize (pp. 101–102, 244–245).

### B. Capping Average Effort Ratings (Ch. 6, pp. 109–117)
- To prevent "grade inflation" (where every worker council rates all its members 150% of average to inflate their consumption allowances), each worker council's **average effort rating across its members is capped** at $100 \times (SB_j / SC_j)$ (or fixed at 100 if councils must meet $SB_j / SC_j \ge 1$, with industry federations adjudicating appeals when accounting prices mismeasure true effort, pp. 117–118).

### C. The Pollution Demand-Revealing Mechanism (PDRM) & Communities of Affected Parties (CAPs) (Ch. 7, pp. 138–149, 159–162)
- Solves a major gap in the 1991 books (which only treated production externalities between worker federations):
  1. **Communities of Affected Parties (CAPs):** Geographic/ecological collectives comprising all citizens impacted by a specific pollutant in a specific watershed/airshed (e.g., VOC/$\text{NO}_x$ smog in Los Angeles vs. particulate matter in Kansas City, p. 140).
  2. **Iterative Pricing of Emissions:** In each round, the IFB quotes an indicative damage price $p_z$ per unit of pollutant $z$.
  3. **Polluter Side:** Each worker council proposes emissions $e_{jz}$ and is charged $p_z e_{jz}$ as part of its social cost $SC_j$.
  4. **Victim Side (CAP):** The CAP proposes a total permissive emission level $E_z$ ("supply of permission to pollute") and receives total credit $p_z E_z$, which is distributed as additional consumption income allowances to CAP members (or spent on collective remediation).
  5. **Equilibrium & Incentive Compatibility (pp. 141–148):** Under proportional cost/credit sharing within the CAP, individual members face a standard public-bad pricing problem; the IFB adjusts $p_z$ upward when $\sum_j e_{jz} > E_z$ and downward when $\sum_j e_{jz} < E_z$, converging to Pigouvian/Lindahl efficiency where marginal abatement cost equals sum of marginal victim damages.
  6. **Important Caveat (p. 149):** Hahnel explicitly acknowledges that PDRM requires knowing *who* belongs to a CAP and relies on victim perception of harm; for long-lived, intergenerational, or scientifically complex ecological thresholds (e.g., $\text{CO}_2$, biodiversity loss), PDRM in annual planning is insufficient and must be governed by **Participatory Environmental Planning** (Ch. 14, pp. 261–267) using scientific expert testimony and intergenerational constraints.

### D. Multi-Horizon Planning Integration (Parts IV & V, Chs. 11–15, pp. 215–292)
- **Aggregate Investment Planning (Ch. 11, pp. 219–237, with Allison Kerkhoff):** Determines the intertemporal division of GDP between current consumption and aggregate investment over a multi-year horizon via consumer federation delegates, investment facilitation boards, and updated social discount/return estimates, with annual re-optimization ("updating investment plans," pp. 232–236) as future preferences and technologies become known.
- **Comprehensive Investment Planning (Ch. 12, pp. 238–245):** Industry federations and worker councils translate aggregate investment allocations into specific demands for capital goods $k_i$ where marginal social return of expanding stock $k_i$ exceeds its marginal social production cost.
- **Long-Run Development Planning (Chs. 13–15, pp. 249–292):** Participatory Educational Planning (human capital / labor categories $l^*$), Participatory Environmental Planning (natural resource extraction caps $r^*$ and sink limits), and Participatory International Economic Planning (trade based on comparative social opportunity cost with a " >50% of benefits to lower-income trading partners" equity rule, p. 272).

---

## 2. Algorithmic & Code Audit of the Computer Simulations (Hahnel et al. 2021, Ch. 9; Szczepanczyk 2023; `pequod-cljs`)

### A. Reported Simulation Design and Results (Hahnel 2021, pp. 173–194; Szczepanczyk 2023, pp. 43–54)
- **Scale:** 40 experiments, each with **30,000 Worker Councils (WCs)** (10,000 private goods producers, 10,000 intermediate goods producers, 10,000 public goods producers), **30,000 Consumer Councils (CCs)**, and **500 distinct priced categories** (100 private goods, 100 public goods, 100 intermediate goods, 100 natural resources, 100 labor categories).
- **Price Adjustment Rule ("Convex/Exponential Damped Rule," Hahnel 2021, p. 179; Szczepanczyk 2023, Eq. 9; `csvgen.clj` lines 383–463):**
  Let $S_i$ be total supply, $D_i$ be total demand, and $\text{surplus}_i = S_i - D_i$. Define the normalized relative imbalance:
  $$r_i = \frac{2 |S_i - D_i|}{S_i + D_i}$$
  The raw price adjustment factor is:
  $$\tilde{\delta}_i = 1.05 - 0.5^{r_i}$$
  This is multiplied by a capped prior-round relative surplus factor $\text{pdlist}_i = \min(0.25, r_i^{\text{prev}})$ and floored at $0.001$:
  $$\delta_i = \max\left(0.001, \min\left(\tilde{\delta}_i, \tilde{\delta}_i \cdot \text{pdlist}_i\right)\right)$$
  Price update:
  $$P_i^{(t+1)} = \begin{cases} P_i^{(t)} (1 - \delta_i) & \text{if } S_i > D_i \\ P_i^{(t)} (1 + \delta_i) & \text{if } S_i < D_i \\ P_i^{(t)} & \text{if } S_i = D_i \end{cases}$$
- **Convergence Findings:**
  - Starting from arbitrary uniform prices ($P_i^{(0)} = 700$ for all 500 categories):
    - **5% threshold** ($r_i < 0.05$ for all 500 categories): **11.85 iterations** on average (range 11–13, Table 9.1, p. 178).
    - **3% threshold** ($r_i < 0.03$ for all 500 categories): **19.20 iterations** on average (range 18–22, Table 9.2, p. 179).
  - Starting Year 2 from Year 1's final prices after random technological/preference shocks (`augment-exponents` in `util.cljc` lines 25–43):
    - **5% threshold:** **6.5 iterations** on average (6.25 iterations when 20% of WCs have input elasticities increased by $+0.1$, labeled `toothaches?` in `csvgen.clj`).

### B. Critical Algorithmic Audit of `pequod-cljs` (`csvgen.clj`)
Direct inspection of `research/sources/pequod_cljs_csvgen_apache2.clj` reveals four critical discrepancies between the theoretical FMPE/PE model and what `pequod-cljs` actually simulated:
1. **Unconstrained Cobb-Douglas Interior Solutions:** Each WC solves $\max_{y, x, e} [\lambda y - \sum p_i x_i - s e^k]$ analytically via closed-form logarithmic formulas (`solution-1` through `solution-8`, lines 209–376). It does *not* enforce the Parecon constraint $SB_j / SC_j \ge 1$ nor the labor/capital stock conservation constraints $\sum \Delta l_j = 0, \sum \Delta k_j = 0$; instead it treats labor and natural resources as elastically purchased spot inputs against fixed global supplies (`1000` units each, lines 162–163).
2. **Why "Increasing Returns to Scale" (`toothaches?`) Did Not Diverge:** In `solution-1..8`, the denominator of the log-linear solution is $c - k + k \sum b_i = k\left(\sum b_i + \frac{c}{k} - 1\right)$. Even when `create-toothache` (lines 667–672) makes $\sum b_i + c > 1$ (increasing physical returns to scale in $(x, e)$), as long as the disutility of effort exponent $k$ is sufficiently large that $\sum b_i + \frac{c}{k} < 1$, the objective function remains strictly concave in $(x, e)$! Thus, the simulation did *not* test genuine non-convexity (such as fixed setup costs, minimum efficient scale, or discrete plant openings/closings).
3. **Decoupled Consumer Income:** In `consume` (lines 176–192), each CC's budget `(:income cc)` is held constant across iterations rather than being recalculated from WC effort ratings and social product value.
4. **Sparsity Assumption:** Each WC uses at most 8 inputs (`solution-1` to `solution-8`) and produces exactly 1 output (`:product`).

---

## 3. Anders Sandström's Accounting Framework (*Anarchist Accounting*, 2020; Sandström 2023)

Sandström translates Parecon's economic flows into a rigorous double-entry/entity accounting architecture without private equity or debt markets:
1. **Four Core Accounting Entities:**
   - **Consumer Entities:** Individuals, Neighborhood Consumer Councils, and Consumer Federations.
   - **Producer Entities:** Worker Councils and Industry/Regional Federations.
   - **Capital Asset Entities ("Stand-Alone Asset Sets"):** Because productive capital belongs to the Productive Commons rather than individual WCs, capital assets are held in stand-alone accounting entities that track both (a) historical social production cost and (b) annual user-right rental fees ($P_k$) paid by WCs during annual planning.
   - **Society Account & CAP Accounts:** The central macro-reconciliation accounts.
2. **Macro-Accounting Identity (Closed Clearing Loop):**
   - **Credits to Society Account (Social Income Supply):** User-right fees paid by WCs for labor categories ($\sum P_l L$), natural resources ($\sum P_r R$), and capital assets ($\sum P_k K$), plus consumer council depreciation/discount charges on public consumer assets, plus WC operating surpluses/deficits.
   - **Debits to Society Account (Social Income Allocation):** Aggregate Investment Expenditure (paid to capital-goods-producing WCs) + Public Service/Benefit Programs (children, retirees, disability, public healthcare/education) + Base Effort-Rated Worker Compensation Pool.
   - **CAP Reconciliation Accounts:** Collect pollutant emission fees ($\sum_j p_z e_{jz}$) from WCs and disburse compensation credits ($p_z E_z$) to CAP members.

---

## 4. Major Peer Critiques in the Literature (incl. EJPE 2024 Special Issue)

1. **John O'Neill (2002; EJPE 2024, pp. 29–48) — Value Incommensurability, Ecological Limits, and Effort Surveillance:**
   - Draws on Otto Neurath and K. William Kapp to argue that reducing multi-dimensional ecological and human values to a single scalar shadow price ("market-mimicking shadow price socialism") violates value incommensurability; ecological sustainability requires biophysical *in natura* boundaries (non-substitutable planetary limits), not victim willingness-to-accept compensation in CAPs.
   - Critiques peer effort rating as requiring intrusive mutual surveillance and risking workplace humiliation or strategic gaming ("handicap racing").
2. **Hannes Kuch (EJPE 2024) — Hidden Centralization in Federations:**
   - Argues that industry and consumer federations exercise substantial centralized gatekeeping power (accrediting/dissolving worker councils, adjudicating $SB/SC < 1$ appeals, managing intra-year adjustments), creating risks of bureaucratic centralization.
3. **Jan Philipp Dapprich (EJPE 2024) & Paul Cockshott / Allin Cottrell (*Towards a New Socialism*, 1993) — Democratic Theory & Algorithmic Planning:**
   - Dapprich argues that democratic self-government requires citizens to vote on general planning *rules* and macroeconomic parameters, not to subject individual/council concrete plans to neighbor or federation vetoes.
   - Cockshott & Cottrell argue that iterativecouncil-by-council bargaining over millions of products is computationally inferior to direct high-dimensional input-output linear programming using labor-time accounting and revealed consumer clearing.
4. **David Schweickart (*Against Capitalism*, 1993) & Seth Ackerman (*Jacobin* / *Science & Society*, 2014) — Participation Burden & Walrasian Formalism:**
   - Critique the cognitive and time burden placed on households to forecast annual consumption and attend council meetings, and note that FMPE relies on Walrasian/Arrow-Debreu convexity assumptions that struggle with dynamic product innovation and increasing returns.
