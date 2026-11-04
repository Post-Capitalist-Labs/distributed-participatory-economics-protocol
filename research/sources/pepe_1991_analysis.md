# Source Analysis: *The Political Economy of Participatory Economics* (1991)

**Authors:** Michael Albert and Robin Hahnel  
**Publisher:** Princeton University Press, Princeton, NJ (1991), 132 pp.  
**Identifiers:** ISBN 978-0-691-00384-9 (pbk) / 978-0-691-04274-9 (hbk) / DOI `10.2307/j.ctv131bvr2` / `10.1515/9780691216003`  
**Source Verification:** Print pagination verified via `pepe_dandelon.pdf` (pp. 1–132); full text read via ZNetwork online edition (`https://znetwork.org/wp-content/uploads/zbooks/htdocs/books/intro.htm` and `1.htm`–`6.htm`), accessed November 4, 2026.

---

## 1. Structural Overview and Pagination Map

| Chapter | Title | Print Pages | ZNetwork Source File | Core Subject Matter |
| :--- | :--- | :--- | :--- | :--- |
| Intro | Introduction | pp. 3–6 | `intro.htm` | Critique of market vs. command dichotomy; overview of participatory economics (PE) and its formal model (FMPE). |
| Ch. 1 | Traditional Economies | pp. 7–22 | `1.htm` | Valuative criteria (equity, self-management, solidarity, variety, efficiency); endogenous preference theorems; critique of markets, central planning, private ownership, and hierarchical production ("coordinatorism"). |
| Ch. 2 | Production | pp. 23–38 | `2.htm` | Workers' councils, proportional decision-making, formal partition of tasks into Balanced Job Complexes (BJCs) within and across workplaces, Job Complex Committees, efficiency and technology choice. |
| Ch. 3 | Consumption | pp. 39–56 | `3.htm` | Nested consumers' councils and federations, collective vs. private consumption, incentive compatibility for public goods, the four distributive maxims, remuneration for effort and sacrifice ("report cards"). |
| Ch. 4 | Allocation | pp. 57–72 | `4.htm` | Decentralized participatory planning: three communicative tools (indicative prices, measures of work, qualitative activity descriptions), Iteration Facilitation Boards (IFBs), 5-iteration convergence example, intra-year flexible updating and slack planning. |
| Ch. 5 | Welfare | pp. 73–106 | `5.htm` | Formal Model of a Participatory Economy (FMPE): mathematical specification of consumer and worker council optimization problems, primal/dual shadow prices, Lange-Arrow-Hurwicz gradient procedure, convexity conditions, public goods and externalities. |
| Ch. 6 | Feasibility | pp. 107–130 | `6.htm` | Computational data structures (vectors, lists, unit/industry/economy input-output matrices), simulation methodology, statistical aggregation of consumer demand and industry responses, and parallel economy experiments. |
| Conc. | Conclusion | pp. 131–132 | `6.htm` (end) | Synthesis of theoretical and experimental agenda. |

---

## 2. Detailed Chapter-by-Chapter Technical Extraction

### Chapter 1: Traditional Economies (pp. 7–22)
- **Five Valuative Criteria (pp. 8–9):**
  1. *Equity:* Evaluated across four mutually exclusive distributive maxims:
     - Maxim 1: Payment according to personal contribution and contribution of property owned (capitalism).
     - Maxim 2: Payment according to personal contribution / human capital (market socialism / coordinatorism).
     - Maxim 3: Payment according to effort and personal sacrifice (participatory economics).
     - Maxim 4: Payment according to need (full communism / humane solidarity, applied to free public goods and special-need exceptions in PE).
  2. *Self-Management:* Decision-making input in proportion to the degree one is affected by the outcome (distinct from both laissez-faire "economic freedom" and simple economy-wide majority rule).
  3. *Solidarity:* Granting others equal consideration in their endeavors (positive-sum social esteem vs. zero/negative-sum invidious comparison).
  4. *Variety:* Diversity of economic lifestyles and outcomes.
  5. *Efficiency:* Pareto optimality extended to account for endogenous human characteristics and preferences.
- **Welfare Theorems with Endogenous Preferences (pp. 9–11, citing Hahnel & Albert 1990, *Quiet Revolution in Welfare Economics*, Chs. 4, 6, 7):**
  - Human beings are conscious agents who account for both *preference fulfillment* effects and *preference development* effects ($\Delta C$) when making choices.
  - **Snowballing Non-Optimality Theorem:** If an economic institution systematically biases the relative terms of supply of two activities (charging more or less than true social opportunity cost), rational individuals will mold their future preferences away from overpriced activities and toward underpriced ones. Consequently: (1) static welfare losses understate true non-optimality, which snowballs over time; (2) human development trajectories are systematically warped; and (3) the bias becomes invisible to participants ex post.
  - **Application to Markets (pp. 12–15):** Markets systematically underprice goods with negative externalities and overprice public goods / goods with positive externalities, inducing a snowballing anti-social, individualistic bias. Market competition also forces democratic worker cooperatives (as in Yugoslavia, p. 14) to hire managers/experts who prioritize bottom-line survival over workplace quality, degenerating into a ruling "coordinator class."
  - **Application to Central Planning (pp. 15–17):** Even if planners know technologies and maximize a democratically voted social welfare function, central planning uses top-down command relations ("down-go-questions, up-come-answers; down-go-orders, up-comes-obedience") that systematically under-supply self-managed work roles, inducing worker apathy and coordinator class rule.

### Chapter 2: Production (pp. 23–38)
- **Workers' Councils (pp. 23–25):** Every workplace is governed by a democratic council (one worker, one vote as final arbiter, with subgroup autonomy and weighted/consensus procedures where impacts differ).
- **Formal Partition for Balanced Job Complexes (pp. 25–27):**
  - Let $\{PA\}$ be the set of all single productive tasks/activities in economy $E$.
  - Partition $\{PA\}$ into subsets of "practically identical production activities" $\{PIPA\}_i$, ordered along a spectrum of qualitative empowerment and desirability effects.
  - Construct the menu of available job complexes by combining tasks across different $\{PIPA\}_i$ subsets such that each worker's primary job complex has a comparable empowerment and desirability rating.
- **Balancing Across Workplaces (pp. 27–30):**
  - Because some industries (e.g., coal mining vs. book publishing) have inherently below- or above-average empowerment/desirability even after internal balancing, economy-wide **Job Complex Committees** rate workplaces and assign workers in above-average primary workplaces offsetting time in below-average workplaces (and vice versa).
  - Empirical check on ratings: Workers are free to apply to any council with openings ("voting with their feet," p. 28). Excess applications to particular councils signal that their job complexes are under-rated in desirability, prompting recalibration of rotation times.

### Chapter 3: Consumption (pp. 39–56)
- **Nested Consumers' Councils and Federations (pp. 40–42):**
  - Individuals/households belong to neighborhood councils, which federate into ward, city/county, state, and national consumption councils.
  - Subsidiarity rule: Collective goods are requested at the federation level corresponding to the population affected (block shrubbery $\to$ neighborhood park $\to$ ward library $\to$ city transit $\to$ watershed waste $\to$ national/global public goods).
  - Privacy & non-veto guarantee for private consumption (p. 41): While neighborhood councils discuss consumption implications, **individual requests whose total social cost does not exceed the individual's warranted consumption allowance (effort-rated budget) cannot be vetoed by the neighborhood council.**
- **Incentive Compatibility for Public Goods (pp. 43–44):**
  - Because member councils are automatically charged their proportionate share of approved federation collective consumption requests out of their total consumption budgets, members cannot "free ride."
  - Councils can optionally implement demand-revealing or pivot mechanisms (Groves-Ledyard / Clarke-Groves variants) to compensate or charge preference outliers.
- **Remuneration and Effort "Report Cards" (pp. 50–55):**
  - Rejects Maxims 1 and 2 (genetic lottery, inheritance, luck, and publicly funded training do not merit unequal consumption).
  - Adopts Maxim 3 (effort and sacrifice) tempered by Maxim 4 (free public goods like healthcare/education plus discretionary special-need allowances).
  - Workers receive an effort rating ("report card," p. 52) from their workers' council—either a finely scaled index around the workplace average or a coarse scale ("superior, average, below average")—which determines their consumption budget at their neighborhood council, along with saving/borrowing across years.

### Chapter 4: Allocation (pp. 57–72)
- **Three Communicative Tools (pp. 59–62):**
  1. *Indicative Prices:* Quantitative estimates of full social costs and benefits (including ecological and human effects), iteratively updated.
  2. *Measures of Work:* Labor hours worked at balanced job complexes, adjusted by peer effort intensity ratings.
  3. *Qualitative Information:* Concise descriptive accounts attached to production and consumption proposals detailing work conditions and special consumption needs.
- **Iterative Planning Lifecycle (pp. 63–71):**
  - Pre-planning: Iteration Facilitation Boards (IFBs) publish last year's final data, completed long-term investment commitments, demographic projections, and initial indicative prices.
  - Early iterations (Rounds 1–2): Individuals propose personal consumption and work plans; neighborhood and workplace councils sum/average proposals; IFBs aggregate global supply and demand, compute percentage excess demand/supply for every good category, and update indicative prices.
  - Middle iterations (Rounds 3–4, pp. 69–70): Proposals shift from individual averages to coherent unit-wide council proposals. Convergence-hastening rules may restrict proposal changes (e.g., capping demand increases for goods in excess demand or capping supply reductions). Workers' councils with benefit-to-cost ratios ($SB/SC$) below industry average must improve efficiency/effort or justify special circumstances; consumer councils above warranted per-capita cost must whittle down or shift toward excess-supply goods.
  - Late iterations (Round 5+, p. 71): IFBs can extrapolate from prior rounds to present ~5 feasible macro-plans (differing slightly in total output/work/consumption/investment) for council voting, followed by micro-adjustments.
- **Flexible Intra-Year Updating & Slack Planning (pp. 66–67):**
  - Consumer federation boards clear canceling adjustments at the lowest possible level (neighborhood $\to$ ward $\to$ city) without disrupting production.
  - Non-canceling demand shifts are tracked via computerized consumption records ("credit card computers" / inventory terminals) and negotiated between consumer federations, industry councils, and workplaces.
  - **Slack Planning (p. 67):** To prevent a "taut" plan where minor shocks cascade across the input-output network, the approved plan intentionally incorporates a buffer of planned excess supply ("slack," e.g., ~5% in Ch. 6, p. 122) in shock-prone industries.

### Chapter 5: Welfare — The Formal Model (FMPE) (pp. 73–106)
- **Explicit Simplifications in FMPE vs. PE (pp. 74–77):**
  1. No interpersonal empathy assumed (pure self-interested *homo economicus*).
  2. No "global awareness" linking a person's consumer and worker identities.
  3. Federations are not modeled as separate structural types, but represented by interpreting subset indices $CC(w), CC(s), CC(n)$ and $WC(r), WC(ind)$ as federations.
  4. Non-discretionary mechanical percentage price adjustments instead of discretionary IFB rules.
  5. Qualitative information omitted.
- **Primal and Dual Economy-Wide Reference Problem (pp. 78–79):**
  - Activity vector $x$; produced input matrix $A$; capital stock coefficient matrix $K$ (available $k^*$); nonproducible scarce resource matrix $R$ (available $r^*$); direct labor input matrix $L$ (available $l^*$); social value row vector $v$.
  - Primal: $\max_x v(I - A)x$ subject to $Kx \le k^*$, $Rx \le r^*$, $Lx \le l^*$, $x \ge 0$.
  - Dual: $\min_{P_k, P_r, P_l} (P_k k^* + P_r r^* + P_l l^*)$ subject to $P_k K + P_r R + P_l L \ge v(I - A)$.
  - Crucial distinction (p. 79): Dual programming shadow prices $P_l$ reflect only marginal physical productivities of labor, *not* differential disutilities/desirabilities of work. FMPE's iterative procedure generates indicative prices that incorporate worker disutility of effort and workplace conditions.
- **Consumer Council Problem in FMPE (pp. 79–80, 88):**
  - Each consumer council $CC(h)$ ($h = 1,\dots,H$) chooses consumption request vector $y(h)$ to maximize total well-being (immediate fulfillment $U(h)$ plus preference development $\Delta C(h)$):
    $$\max_{y(h)} W(h) = W(U(h), \Delta C(h)) \quad \text{s.t.} \quad P \cdot (y(h) - \bar{y}) \le 0$$
    where $P$ is the indicative price vector of produced goods and $\bar{y} = \frac{1}{H}\sum_{h=1}^H y(h)$ is the average consumption bundle (assuming equal council sizes and average effort; otherwise scaled by effort rating).
- **Worker Council Problem in FMPE (pp. 85–88):**
  - Each worker council $WC(j)$ ($j = 1,\dots,J$) begins with initial labor endowment $l_j$ ($\sum_j l_j = l^*$) and initial capital endowment $k_j$ ($\sum_j k_j = k^*$), for which it is charged $P_l l_j + P_k k_j$.
  - In iteration $t$, $WC(j)$ proposes produced outputs $\bar{a}(j)$, produced intermediate inputs $\underline{a}(j)$, natural resource inputs $r(j)$, net labor additions/releases $\Delta l(j)$, and net capital additions/releases $\Delta k(j)$.
  - Social cost of inputs and endowments: $SC(j) = P \cdot \underline{a}(j) + P_r \cdot r(j) + P_l \cdot (l_j + \Delta l(j)) + P_k \cdot (k_j + \Delta k(j))$.
  - Social benefit of outputs: $SB(j) = P \cdot \bar{a}(j)$.
  - $WC(j)$ maximizes worker well-being and development subject to the "socially non-abusive" constraint ($SB(j) \ge SC(j)$):
    $$\max W(j) = W(U(j), \Delta C(j)) \quad \text{s.t.} \quad P \cdot \bar{a}(j) - \left[ P \cdot \underline{a}(j) + P_r \cdot r(j) + P_l \cdot (l_j + \Delta l(j)) + P_k \cdot (k_j + \Delta k(j)) \right] \ge 0$$
- **FMPE Iterative Algorithm (Lange-Arrow-Hurwicz Gradient Procedure, pp. 89–93):**
  - Step 1–2: $CC(h)$ and $WC(j)$ submit initial proposals ($t = 0$).
  - Step 3: Planning Bureau (PB / IFB) quotes initial price vector $P^0 = (P, P_r, P_l, P_k)$.
  - Step 4: Each $CC(h)$ adjusts consumption request $y_i(h)$ proportionally to the difference between its marginal social benefit and its shadow-priced budget cost (with step size $0 < \alpha < 1$, projected onto $y_i(h) \ge 0$).
  - Step 5: Each $WC(j)$ adjusts outputs $\bar{a}(j)$ and inputs $(\underline{a}(j), r(j), \Delta l(j), \Delta k(j))$ proportionally to the marginal net social benefit plus marginal worker well-being (with step size $0 < \beta < 1$).
  - Step 6: PB adjusts prices proportionally to aggregate excess demand (with step size $0 < \gamma < 1$, projected onto $P \ge 0$):
    $$\Delta P_i = \gamma \left( \sum_{h=1}^H y_i(h) + \sum_{j=1}^J \underline{a}_i(j) - \sum_{j=1}^J \bar{a}_i(j) \right)$$
    and analogously for resource, labor, and capital prices based on $\sum_j r(j) - r^*$, $\sum_j \Delta l(j)$, and $\sum_j \Delta k(j)$.
  - **Convergence & Optimality Proof Reference (p. 93 & Notes 3–4, p. 105):** Equivalent to the Arrow-Hurwicz-Uzawa (1958) / Heal (1973, Ch. 4) price-guided gradient procedure; converges to a saddle point (feasible and Pareto optimal plan) under standard convexity of council well-being functions and production possibility sets, extended to boundary discontinuities via Champsaur, Dreze, & Henry / Henry (1972).

### Chapter 6: Feasibility and Computational Formalism (pp. 107–130)
- **Data Structures (pp. 109–111):**
  - Quantitative proposals represented as $n$-dimensional vectors: consumer input $C_j$, consumer output $\bar{C}_j$, producer input $P_j$, producer output $\bar{P}_j$.
  - Qualitative data represented as hierarchical `Lists` paired with each vector entry, summarized upward by IFBs while preserving full drill-down access to raw council/individual text.
  - Unit production matrices $M_j$ ($n \times n$) where $P_j \cdot M_j = \bar{P}_j$; aggregated via output-weighted averages into industry matrices $M_{\text{Industry}(k)}$ and economy matrix $M^E$.
- **Global Feasibility Equation with Slack (p. 113):**
  $$\bar{P}^E = C^E + P^E + SL^E$$
  where $\bar{P}^E$ is gross economy output, $C^E$ is total final consumption demand, $P^E$ is total intermediate/productive input demand, and $SL^E$ is planned slack (e.g., $SL^E(G) = 0.05 \cdot S^I(G)$, p. 122).
- **Proposed Experiments (pp. 114–130):**
  1. Micro-simulations with a small number of explicit councils and goods.
  2. Macro-simulations representing consumer demands as normal distributions $(\mu, \sigma)$ shifting across iterations, with interactive human-in-the-loop terminals ("game format," p. 117, 128).
  3. Parallel "shadow" participatory economy run alongside an existing economy or sector (pp. 129–130).
