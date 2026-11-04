# Formal Economic Model and Computational Requirements

**Deliverable:** `reports/ECONOMIC_MODEL.md`  
**Phase:** 2 — Economic and Institutional Analysis  
**Grounded Sources:** Albert & Hahnel (1991a [PEPE], Chs. 2–6; 1991b [LF], Chs. 1–9); Hahnel (2021 [DEP], Chs. 5–15); Sandström (2020, 2023); Szczepanczyk (2023) & `pequod-cljs` (`csvgen.clj`).

---

## 1. Scope and Fidelity to Primary Sources

This document translates the economic theory of Participatory Economics (Parecon) into a formal mathematical and computational specification suitable for distributed systems engineering.

### 1.1 Verification and Correction of the 10-Stage Planning Lifecycle
Section 4 of the Research Brief outlines a 10-step planning lifecycle. Comparing that sequence against the primary texts (Albert & Hahnel 1991a, Chs. 4–5; 1991b, Chs. 6–9; Hahnel 2021, Chs. 7–15) confirms that the 10 steps capture the core annual loop, **subject to five critical refinements required for fidelity to the original model**:

1. **Pre-Annual Multi-Horizon Conditioning (LF Ch. 9, `lf9_1.htm`; DEP Chs. 11–14):** Annual planning does *not* start in a vacuum. Aggregate Investment Planning (determining the share of GDP devoted to capital formation), Comprehensive Investment Planning, Long-Run Educational Planning (determining the vector of available labor categories $l^*$), and Long-Run Environmental Planning (setting biophysical extraction caps $r^*$ and non-negotiable emissions bans) **precede** annual planning and fix its boundary constraints and pre-committed multi-year project demands.
2. **Collective-Before-Personal Consumption Ordering (PEPE Ch. 3, p. 41; LF Ch. 3 `lf3_2.htm`, Ch. 8 `lf8_1.htm`):** National, state, county/city, and ward collective consumption requests are proposed, deliberated, and settled *prior to or in the initial stages of* individual household consumption planning, because each household's available budget for private goods is net of its proportionate share of approved federation collective consumption.
3. **Shift from Individual Proposals to Coherent Council Proposals in Mid-Rounds (PEPE Ch. 4, pp. 64–65, 70; Ch. 6, p. 111):** In Rounds 1–2, individual workers submit personal work-hour/effort proposals that are averaged into an indicative plant proposal, even though team production requires synchronized schedules. By Round 3–4, workplace councils deliberate and submit unified, technically implementable unit-wide production proposals.
4. **Dual Approval Mechanism — Quantitative Social Cost/Benefit + Peer Council Veto/Exceptions (PEPE Ch. 4, p. 66; Ch. 5, pp. 80, 86–88; DEP Ch. 7, pp. 130–133):** Iteration Facilitation Boards (IFBs) **never** approve or veto proposals. Instead:
   - Consumer councils approve or contest peer consumption proposals based on whether per-capita social cost exceeds warranted effort-rated income ($P \cdot y(h) \le B(h)$), with qualitative petitions required for special-need exceptions.
   - Worker councils and industry federations approve or contest production proposals based on whether the Social Benefit to Social Cost ratio satisfies $SB(j) / SC(j) \ge 1$ (or meets the industry average), with qualitative petitions where accounting prices misrepresent local conditions.
5. **Slack Planning and Hierarchical Intra-Year Adjustment (PEPE Ch. 4, pp. 66–67; Ch. 6, p. 113; DEP Ch. 8, pp. 167–170):** Annual planning deliberately targets a non-zero buffer of planned excess supply ("slack" $SL^E$, e.g., 3–5%) rather than a "taut" zero-surplus plan. During the year, individual consumer substitutions cancel out across neighborhood, ward, and city consumer federations; only net non-canceling shifts that breach slack buffers trigger Updating Facilitation Board (UFB) and industry federation renegotiation.

---

## 2. Formal Ontology: Actors, Institutions, and Economic Objects

### 2.1 Sets of Economic Actors and Institutions

Let the economy $\mathcal{E}$ over planning period (year) $T$ consist of the following finite sets of actors and institutional entities:

1. **Individuals ($\mathcal{I} = \{1, \dots, N_{\text{ind}}\}$):** Natural persons participating as consumers, workers (if of working age/ability), and citizens. Each individual $u \in \mathcal{I}$ has:
   - Primary neighborhood membership $h(u) \in \mathcal{H}$.
   - Primary worker council membership $j(u) \in \mathcal{J}$ (and optional secondary rotation council $j'(u) \in \mathcal{J}$ for cross-workplace BJC balancing; PEPE Ch. 2, pp. 27–30).
2. **Households / Living Units ($\mathcal{U}$):** Co-housing units, families, or single-person households partitioning $\mathcal{I}$, assisted by **Household Facilitation Boards ($\text{HFB}$)**.
3. **Neighborhood Consumer Councils ($\mathcal{H} = \{CC_1, \dots, CC_H\}$):** Base geographic councils of ~50–500 households.
4. **Nested Consumer Federations ($\mathcal{F}^C = \mathcal{F}^C_1 \cup \dots \cup \mathcal{F}^C_L$):** A rooted tree of geographic federations of depth $L$ (typically $L = 5$: Level 1 = Ward, Level 2 = City/County, Level 3 = State/Province, Level 4 = Region, Level 5 = National/Coalition; PEPE Ch. 3, p. 40). For any federation $f \in \mathcal{F}^C_\ell$, let $\text{children}(f)$ be its member councils/sub-federations and $\text{pop}(f) \subseteq \mathcal{I}$ be all individuals nested within $f$.
5. **Worker Councils ($\mathcal{J} = \{WC_1, \dots, WC_J\}$):** Democratic workplace collectives (internally structured into work teams $WT_{j,m}$ for large plants; LF Ch. 2).
6. **Worker Federations ($\mathcal{F}^W = \mathcal{F}^{W,\text{ind}} \cup \mathcal{F}^{W,\text{reg}}$):**
   - **Industry Federations ($\mathcal{F}^{W,\text{ind}} = \{IF_1, \dots, IF_K\}$):** Partitioning or grouping $\mathcal{J}$ by primary product/sector $k$ to manage sector-wide capacity, R&D, scale economies, council accreditation/dissolution, and $SB/SC$ benchmarking (PEPE Ch. 4, pp. 62, 70; DEP Ch. 6, p. 104).
   - **Regional Worker Federations ($\mathcal{F}^{W,\text{reg}}$):** Grouping $\mathcal{J}$ geographically to coordinate local production externalities and shared infrastructure (PEPE Ch. 5, p. 97).
7. **Communities of Affected Parties ($\mathcal{C}^{\text{CAP}} = \{CAP_1, \dots, CAP_Z\}$):** Ecological/geographic collectives defined for each regulated pollutant/emission $z \in \mathcal{Z}$ in a specific airshed/watershed, comprising affected residents $\text{pop}(CAP_z) \subseteq \mathcal{I}$ (DEP Ch. 7, pp. 140–148).
8. **Six Functional Facilitation Boards ($\mathcal{B} = \{\text{IFB}, \text{CFB}, \text{PFB}, \text{EFB}, \text{HFB}, \text{UFB}\}$):** Informational calculation and mediation services (LF Ch. 6, `lf6_1.htm`).
9. **Stand-Alone Capital Asset Entities ($\mathcal{A}^{\text{cap}}$), Society Account ($\mathcal{A}^{\text{soc}}$), and Audit/Environmental Courts ($\mathcal{D}$):** Accounting and adjudication institutions (Sandström 2020, 2023; PEP 2023).

---

### 2.2 Sets of Economic Objects and Priced Categories

Following Albert & Hahnel (1991a, Chs. 5–6), Hahnel (2021, Chs. 7–9), and Szczepanczyk (2023, Sec. 4), the economy tracks **seven disjoint categories of goods, resources, labor, capital, and emissions**, indexed over the master catalog $\Omega$:

$$\Omega = \mathcal{G}^{\text{priv}} \sqcup \mathcal{G}^{\text{pub}} \sqcup \mathcal{G}^{\text{int}} \sqcup \mathcal{R} \sqcup \mathcal{L} \sqcup \mathcal{K} \sqcup \mathcal{Z}$$

| Symbol | Category Name | Cardinality | Economic Role & Valuation Semantics |
| :--- | :--- | :--- | :--- |
| $\mathcal{G}^{\text{priv}}$ | Private Consumption Goods | $N_{\text{priv}}$ | Coarse resource-equivalent product classes (e.g., "winter coat," "laptop Type B") requested by individuals/households via $CC_h$; granular SKU attributes (size/color) resolved at fulfillment (DEP Ch. 8, pp. 163–167). Priced at $p_g^{\text{priv}} \ge 0$. |
| $\mathcal{G}^{\text{pub}}$ | Collective / Public Goods | $N_{\text{pub}}$ | Goods and services jointly consumed by a neighborhood council $CC_h$ or consumer federation $f \in \mathcal{F}^C_\ell$ (e.g., local park equipment, municipal transit, regional hospital capacity). Priced at $p_g^{\text{pub}} \ge 0$. |
| $\mathcal{G}^{\text{int}}$ | Intermediate Produced Inputs | $N_{\text{int}}$ | Goods and services produced by some $WC_j$ and used as inputs by other $WC_{j'}$ (steel, electricity, semiconductors, freight). Priced at $p_g^{\text{int}} \ge 0$. |
| $\mathcal{R}$ | Non-Producible Natural Resources | $N_{\text{res}}$ | Virgin resource flows and land/water usage rights subject to total ecological sustainability bound $r^* \in \mathbb{R}_+^{N_{\text{res}}}$ set by Long-Run Environmental Planning. Priced at opportunity cost $p_r^{\text{res}} \ge 0$. |
| $\mathcal{L}$ | Labor Categories | $N_{\text{lab}}$ | Distinct skill/training categories of labor (engineers, machinists, caregivers, agronomists) with total available economy supply $l^* \in \mathbb{R}_+^{N_{\text{lab}}}$ set by Educational Planning and demographics. Priced at opportunity cost $p_\ell^{\text{lab}} \ge 0$ (paid by WCs to $\mathcal{A}^{\text{soc}}$; *distinct* from worker effort remuneration!). |
| $\mathcal{K}$ | Capital Goods / Productive Assets | $N_{\text{cap}}$ | Plant, machinery, and fixed equipment stocks available at start of year $k^* \in \mathbb{R}_+^{N_{\text{cap}}}$ (plus newly produced investment goods $\Delta K^{\text{inv}}$). WCs pay user-right rental price $p_\kappa^{\text{cap}} \ge 0$ to $\mathcal{A}^{\text{soc}}$ (PEPE Ch. 5, p. 85; DEP Ch. 12, p. 244; Sandström 2023). |
| $\mathcal{Z}$ | Regulated Pollutants / Emissions | $N_{\text{pol}}$ | Harmful emissions indexed by substance and airshed/watershed $z \in \mathcal{Z}$, subject to hard biophysical ceiling $E_z^{\max}$ (from Environmental Planning) and soft victim-tolerance supply $E_z \le E_z^{\max}$ proposed by $CAP_z$. Priced at damage fee $p_z^{\text{pol}} \ge 0$ (DEP Ch. 7, pp. 139–148). |

Let $P = \left(p^{\text{priv}}, p^{\text{pub}}, p^{\text{int}}, p^{\text{res}}, p^{\text{lab}}, p^{\text{cap}}, p^{\text{pol}}\right) \in \mathbb{R}_+^{|\Omega|}$ denote the complete vector of indicative prices at iteration $t$.

---

## 3. Mathematical Formulation of the Participatory Planning Model

### 3.1 Society Account, Warranted Income, and Effort Remuneration (Sandström 2020/2023; DEP Ch. 6)

A crucial contribution of Sandström (2020, Ch. 3; 2023) and Hahnel (2021, Ch. 6) is clarifying the exact mathematical relationship between **opportunity-cost charges paid by Worker Councils** and **effort-based income received by Consumers**:

1. **Total Social Value of Final Net Product (GDP) at Indicative Prices $P$:**
   In any feasible plan, the value of net final output equals the sum of private consumption, public consumption, and aggregate gross investment $\mathcal{I}^{\text{inv}}$:
   $$Y^{\text{GDP}}(P) = p^{\text{priv}} \cdot D^{\text{priv}} + p^{\text{pub}} \cdot D^{\text{pub}} + p^{\text{cap,new}} \cdot D^{\text{inv}}$$
   By dual accounting conservation in the **Society Account** ($\mathcal{A}^{\text{soc}}$), this also equals total user-right fees paid by WCs for primary factors (labor $p^{\text{lab}} \cdot L$, natural resources $p^{\text{res}} \cdot R$, capital stocks $p^{\text{cap}} \cdot K$) plus net WC operating surpluses $\sum_j (SB_j - SC_j^{\text{excl. pol}})$.

2. **Aggregate Consumption Pool ($Y^{\text{cons}}$) and Base Hourly Remuneration ($w_{\text{base}}$):**
   Let $\sigma_{\text{inv}} \in (0, 1)$ be the share of GDP allocated to aggregate investment (determined by Aggregate Investment Planning, DEP Ch. 11), and let $Y^{\text{allow}}$ be the politically ratified budget for non-working allowances (children, retirees, disability) and universal free public services (healthcare, education; Maxim 4, Sandström 2023 Arrows 2 & 5). Then the total pool available for effort-rated worker remuneration is:
   $$Y^{\text{work}}(P) = (1 - \sigma_{\text{inv}}) Y^{\text{GDP}}(P) - Y^{\text{allow}}$$
   For a total planned socially valued work-hour supply $H^{\text{tot}} = \sum_{u \in \mathcal{I}^{\text{work}}} h_u$, the base income per standard effort-adjusted hour is:
   $$w_{\text{base}}(P) = \frac{Y^{\text{work}}(P)}{H^{\text{tot}}}$$

3. **Worker Effort Rating Cap and Individual Warranted Budget ($B_u$):**
   Inside worker council $WC_j$, each worker $u \in WC_j$ works $h_u$ hours at a balanced job complex and receives a peer-evaluated effort multiplier $\epsilon_u \ge 0$. To prevent collective grade inflation, the council's hours-weighted average effort multiplier is capped by its social benefit-to-cost ratio (DEP Ch. 6, p. 117):
   $$\frac{\sum_{u \in WC_j} h_u \epsilon_u}{\sum_{u \in WC_j} h_u} \le \min\left(\bar{\epsilon}_{\max}, \frac{SB_j(P)}{SC_j(P)}\right)$$
   (where $\bar{\epsilon}_{\max} = 1.0$ if excess social surplus is attributed to unpriced technological/endowment advantages rather than worker sacrifice, or $>1.0$ only upon industry federation validation).
   Then individual $u$'s **warranted annual consumption budget** $B_u(P)$ is the sum of four components (Sandström 2023, Arrows 1–4):
   $$B_u(P) = \underbrace{w_{\text{base}}(P) \cdot h_u \cdot \epsilon_u}_{\text{Work Effort Income}} + \underbrace{A_u^{\text{social}}}_{\text{Age/Disability Allowance}} + \underbrace{\sum_{z: u \in CAP_z} \frac{p_z^{\text{pol}} E_z}{|\text{pop}(CAP_z)|}}_{\text{CAP Pollution Compensation}} + \underbrace{\Delta S_u}_{\text{Approved Borrowing } (>0) \text{ or Saving } (<0) + \text{ Special Need}}$$

---

### 3.2 Consumer Council and Federation Optimization Problem

For each neighborhood consumer council $CC_h \in \mathcal{H}$ with member set $\text{pop}(CC_h)$, let:
- $y_u^{\text{priv}} \in \mathbb{R}_+^{N_{\text{priv}}}$ be member $u$'s personal consumption request vector.
- $y_h^{\text{priv}} = \sum_{u \in \text{pop}(CC_h)} y_u^{\text{priv}}$ be the aggregated private consumption vector of $CC_h$.
- $y_h^{\text{pub,loc}} \in \mathbb{R}_+^{N_{\text{pub}}}$ be $CC_h$'s local neighborhood collective consumption request.
- For each higher-level consumer federation $f \in \mathcal{F}^C_\ell$ containing $CC_h$ ($CC_h \prec f$), let $y_f^{\text{pub}} \in \mathbb{R}_+^{N_{\text{pub}}}$ be federation $f$'s collective consumption request, of which each citizen bears a proportionate share $\frac{1}{|\text{pop}(f)|}$ (or a Groves-Ledyard / pivot adjusted share $\theta_{u,f}$; PEPE Ch. 3, pp. 43–44).

**Individual Budget Constraint (Protected Private Sphere, PEPE Ch. 3, p. 41):**
$$p^{\text{priv}} \cdot y_u^{\text{priv}} + \frac{p^{\text{pub}} \cdot y_h^{\text{pub,loc}}}{|\text{pop}(CC_h)|} + \sum_{f \succ CC_h} \frac{p^{\text{pub}} \cdot y_f^{\text{pub}}}{|\text{pop}(f)|} \le B_u(P)$$

**Neighborhood Council Budget Constraint (FMPE Ch. 5, p. 80, 88):**
Summing over $u \in \text{pop}(CC_h)$ defines the council's aggregate warranted budget $B(CC_h, P) = \sum_{u \in \text{pop}(CC_h)} B_u(P)$:
$$SC(CC_h, P) \triangleq p^{\text{priv}} \cdot y_h^{\text{priv}} + p^{\text{pub}} \cdot y_h^{\text{pub,loc}} + |\text{pop}(CC_h)| \sum_{f \succ CC_h} \frac{p^{\text{pub}} \cdot y_f^{\text{pub}}}{|\text{pop}(f)|} \le B(CC_h, P)$$

Each consumer council $CC_h$ (and nested federation $f$) maximizes its members' immediate fulfillment $U_h$ and endogenous preference development $\Delta C_h$:
$$\max_{y_h^{\text{priv}}, y_h^{\text{pub,loc}} \ge 0} W_h\left(U_h(y_h^{\text{priv}}, y^{\text{pub}}), \Delta C_h(y_h^{\text{priv}}, y^{\text{pub}})\right) \quad \text{s.t.} \quad SC(CC_h, P) \le B(CC_h, P)$$

---

### 3.3 Community of Affected Parties (CAP) Optimization Problem (DEP Ch. 7, pp. 139–148)

For each pollutant $z \in \mathcal{Z}$ governed by $CAP_z$ with biophysical sustainability ceiling $E_z^{\max}$ (fixed by Long-Run Environmental Planning):
Given indicative damage price $p_z^{\text{pol}}$ announced by the IFB, $CAP_z$ chooses the total permissible emission level $E_z \in [0, E_z^{\max}]$ to maximize member well-being (trading off the health/aesthetic disutility of pollution $D_{CAP_z}(E_z)$ against the consumption utility gained from the compensation credit $p_z^{\text{pol}} E_z$):
$$\max_{0 \le E_z \le E_z^{\max}} W_{CAP_z}\left(\text{Compensation Credit } p_z^{\text{pol}} E_z, \, -D_{CAP_z}(E_z)\right)$$
At an interior optimum, $CAP_z$ proposes $E_z$ such that the sum of members' marginal damage equals $p_z^{\text{pol}}$ (Lindahl-Pigou condition; DEP Ch. 7, Appendix pp. 159–162).

---

### 3.4 Worker Council Optimization Problem (PEPE Ch. 5, pp. 85–88; DEP Ch. 7, pp. 152–156)

Each worker council $WC_j \in \mathcal{J}$ begins the annual planning cycle with:
- Initial labor endowment vector $l_j^0 \in \mathbb{R}_+^{N_{\text{lab}}}$ ($\sum_{j=1}^J l_j^0 = l^*$).
- Initial capital stock endowment vector $k_j^0 \in \mathbb{R}_+^{N_{\text{cap}}}$ ($\sum_{j=1}^J k_j^0 = k^*$).
- Access to the public book of technological blueprints (represented as a production possibility set $\mathcal{T}_j$ or input-output technology matrix $M_j$; PEPE Ch. 5, p. 84; Ch. 6, p. 111).

In iteration $t$, $WC_j$ submits a production proposal tuple:
$$\pi_j^{(t)} = \left(\bar{a}_j, \, \underline{a}_j, \, r_j, \, \Delta l_j, \, \Delta k_j, \, e_j, \, \xi_j, \, \text{QualList}_j\right)$$
where:
- $\bar{a}_j = (\bar{a}_j^{\text{priv}}, \bar{a}_j^{\text{pub}}, \bar{a}_j^{\text{int}}, \bar{a}_j^{\text{inv}}) \in \mathbb{R}_+^{N_{\text{priv}} + N_{\text{pub}} + N_{\text{int}} + N_{\text{cap}}}$ is the vector of proposed outputs.
- $\underline{a}_j \in \mathbb{R}_+^{N_{\text{int}}}$ is the vector of requested intermediate produced inputs.
- $r_j \in \mathbb{R}_+^{N_{\text{res}}}$ is the vector of requested natural resource inputs.
- $l_j = l_j^0 + \Delta l_j \in \mathbb{R}_+^{N_{\text{lab}}}$ is the net labor vector requested ($\Delta l_{j,\ell} > 0$ additions, $\Delta l_{j,\ell} < 0$ releases).
- $k_j = k_j^0 + \Delta k_j \in \mathbb{R}_+^{N_{\text{cap}}}$ is the net capital user-right vector requested.
- $e_j \in \mathbb{R}_+^{N_{\text{pol}}}$ is the vector of proposed pollutant emissions.
- $\xi_j \in \mathbb{R}_+$ is the council's aggregate work effort/intensity commitment.
- $\text{QualList}_j$ is the structured qualitative justification list.

**Social Benefit ($SB_j$) and Social Cost ($SC_j$) at Indicative Prices $P$:**
$$SB_j(P) = p^{\text{priv}} \cdot \bar{a}_j^{\text{priv}} + p^{\text{pub}} \cdot \bar{a}_j^{\text{pub}} + p^{\text{int}} \cdot \bar{a}_j^{\text{int}} + p^{\text{cap,new}} \cdot \bar{a}_j^{\text{inv}}$$
$$SC_j(P) = p^{\text{int}} \cdot \underline{a}_j + p^{\text{res}} \cdot r_j + p^{\text{lab}} \cdot (l_j^0 + \Delta l_j) + p^{\text{cap}} \cdot (k_j^0 + \Delta k_j) + p^{\text{pol}} \cdot e_j$$

**Worker Council Optimization Problem:**
$$WC_j \text{ solves:} \quad \max_{\pi_j \in \mathcal{T}_j} W_j\left(U_j(\pi_j), \Delta C_j(\pi_j)\right)$$
subject to the **Socially Non-Abusive Production Constraint** (PEPE Ch. 5, p. 87, 88):
$$\text{Constraint (WC-1):} \quad SB_j(P) - SC_j(P) \ge 0 \quad \left(\text{equivalently, } \frac{SB_j(P)}{SC_j(P)} \ge 1\right)$$
(unless $WC_j$ files a qualitative appeal $\text{Appeal}_j$ ratified by its Industry Federation $IF_k$ due to transitional retooling or unpriced handicap).

---

### 3.5 Global Supply, Demand, Slack, and Market-Clearing Invariants

At iteration $t$, aggregating across all $\mathcal{H}, \mathcal{F}^C, \mathcal{J}, \mathcal{C}^{\text{CAP}}$ yields total demand $D_i^{(t)}$, total supply $S_i^{(t)}$, planned slack $SL_i^{(t)} = \eta_i S_i^{(t)}$ (where $\eta_i \in [0, 0.05]$ is the slack buffer coefficient for produced goods; PEPE Ch. 6, p. 113, 122), and net excess demand $ED_i^{(t)} = D_i^{(t)} + SL_i^{(t)} - S_i^{(t)}$ for every category $i \in \Omega$:

1. **Private Goods ($g \in \mathcal{G}^{\text{priv}}$):**
   $$D_g^{\text{priv}} = \sum_{h=1}^H y_{h,g}^{\text{priv}}, \quad S_g^{\text{priv}} = \sum_{j=1}^J \bar{a}_{j,g}^{\text{priv}}, \quad ED_g^{\text{priv}} = D_g^{\text{priv}} + SL_g^{\text{priv}} - S_g^{\text{priv}}$$
2. **Public / Collective Goods ($g \in \mathcal{G}^{\text{pub}}$):**
   Note a subtle distinction between the **quantity of a public good produced** and **individual councils' expressions of demand**:
   - For a public good $g$ scoped to a specific federation or neighborhood $f(g)$, the collective demand $D_g^{\text{pub}}$ is either ratified by federation vote prior to the round ($y_{f(g), g}^{\text{pub}}$; LF Ch. 8) or, in the simultaneous FMPE/Pequod formulation (Szczepanczyk 2023, `csvgen.clj` lines 443–447), averaged across the member councils sharing the good:
     $$D_g^{\text{pub}} = \frac{1}{|\text{members}(f(g))|} \sum_{h \in \text{members}(f(g))} y_{h,g}^{\text{pub}}, \quad S_g^{\text{pub}} = \sum_{j=1}^J \bar{a}_{j,g}^{\text{pub}}, \quad ED_g^{\text{pub}} = D_g^{\text{pub}} + SL_g^{\text{pub}} - S_g^{\text{pub}}$$
3. **Intermediate Inputs ($g \in \mathcal{G}^{\text{int}}$):**
   $$D_g^{\text{int}} = \sum_{j=1}^J \underline{a}_{j,g} + D_g^{\text{inv,int}}, \quad S_g^{\text{int}} = \sum_{j=1}^J \bar{a}_{j,g}^{\text{int}}, \quad ED_g^{\text{int}} = D_g^{\text{int}} + SL_g^{\text{int}} - S_g^{\text{int}}$$
4. **Natural Resources ($r \in \mathcal{R}$):**
   $$D_r^{\text{res}} = \sum_{j=1}^J r_{j,r}, \quad S_r^{\text{res}} = r_r^* \text{ (fixed ecological cap)}, \quad ED_r^{\text{res}} = D_r^{\text{res}} - r_r^*$$
5. **Labor Categories ($\ell \in \mathcal{L}$):**
   $$D_\ell^{\text{lab}} = \sum_{j=1}^J (l_{j,\ell}^0 + \Delta l_{j,\ell}), \quad S_\ell^{\text{lab}} = l_\ell^* = \sum_{j=1}^J l_{j,\ell}^0, \quad ED_\ell^{\text{lab}} = \sum_{j=1}^J \Delta l_{j,\ell}$$
6. **Capital Asset User Rights ($\kappa \in \mathcal{K}$):**
   $$D_\kappa^{\text{cap}} = \sum_{j=1}^J (k_{j,\kappa}^0 + \Delta k_{j,\kappa}), \quad S_\kappa^{\text{cap}} = k_\kappa^* = \sum_{j=1}^J k_{j,\kappa}^0, \quad ED_\kappa^{\text{cap}} = \sum_{j=1}^J \Delta k_{j,\kappa}$$
7. **Pollutant Emissions ($z \in \mathcal{Z}$):**
   $$D_z^{\text{pol}} = \sum_{j=1}^J e_{j,z} \text{ (polluter demand for emission rights)}, \quad S_z^{\text{pol}} = E_z \le E_z^{\max} \text{ (CAP tolerance)}, \quad ED_z^{\text{pol}} = \sum_{j=1}^J e_{j,z} - E_z$$

**Convergence / Feasibility Criterion ($\tau$-Feasibility):**
Define the symmetric normalized relative imbalance for each item $i \in \Omega$ (Hahnel 2021, p. 178; `csvgen.clj` line 602):
$$\rho_i^{(t)} = \frac{2 \left| ED_i^{(t)} \right|}{D_i^{(t)} + SL_i^{(t)} + S_i^{(t)} + \varepsilon}$$
A plan is **$(\tau, \text{eco})$-feasible** if and only if:
1. $\forall i \in \Omega: \rho_i^{(t)} \le \tau$ (where $\tau \in [0.01, 0.05]$, typically $\tau = 0.03$ or $0.05$).
2. **Hard Ecological Invariant:** $\forall r \in \mathcal{R}: D_r^{\text{res}} \le r_r^*$ and $\forall z \in \mathcal{Z}: D_z^{\text{pol}} \le E_z^{\max}$ (biophysical ceilings cannot be violated even within the $\tau$ tolerance band!).
3. **Council Constraint Invariant:** Every active $CC_h$ satisfies $SC(CC_h, P) \le B(CC_h, P)$ (or holds a federation-ratified need exception) and every active $WC_j$ satisfies $SB_j(P)/SC_j(P) \ge 1$ (or holds an industry-federation-ratified appeal).

---

## 4. State-Machine Specification of the Planning Protocol

```
+-----------------------------------------------------------------------------------+
|                        ANNUAL & OPERATIONAL STATE MACHINE                         |
+-----------------------------------------------------------------------------------+

  [S0: PRE_PLAN_PARAMETERS]
     |  Inputs: Long-run Education (l*), Environment (r*, E_max), Aggregate Investment (sigma_inv),
     |          Prior Year Final Prices P^(0), Demographic & BJC Rosters.
     v
  [S1: COLLECTIVE_GOODS_PHASE]
     |  Consumer Federations (National -> State -> County/City -> Ward) deliberate & vote
     |  provisional collective consumption bundles y_f^pub; per-capita deductions locked.
     v
  [S2: ROUND_OPEN (t = 1..T_max)] <-----------------------------------------+
     |  IFB publishes P^(t), w_base^(t), macro projections, & prior surpluses.|
     |  Councils (CC_h, WC_j, CAP_z) compute & sign proposals pi^(t).        |
     v                                                                        |
  [S3: FEDERATED_AGGREGATION]                                                 |
     |  Neighborhood -> Ward -> City -> Regional -> Global Merkle-Sum Tree    |
     |  aggregates D^(t), S^(t), ED^(t), and Qualitative Summary Lists.      |
     v                                                                        |
  [S4: FEASIBILITY_AND_PRICE_UPDATE]                                          |
     |  Check if max_i rho_i^(t) <= tau AND ecological/council invariants hold|
     +--- If NO and t < T_switch: Apply Price Update Rule -> P^(t+1), t++ ----+
     |
     +--- If NO and t >= T_switch (Optional Late-Round Acceleration, PEPE p.71):
     |       v
     |    [S5: MACRO_PLAN_SYNTHESIS_AND_VOTE]
     |       IFB generates K=5 feasible boundary plans; Councils vote or reject to resume S2.
     |
     +--- If YES (Converged):
             v
  [S6: DEMOCRATIC_RATIFICATION_AND_COMMITMENT]
     |  Councils & Federations verify final constraints, sign cryptographic
     |  Production & Consumption Commitments; Job Complex Committees finalize
     |  cross-workplace rotation schedules (PEPE Ch. 5, p. 83) & EFB labor transfers.
     v
  [S7: INTRA_YEAR_EXECUTION_AND_CLEARING]
     |  Continuous recording of deliveries, inventory drawdowns, and effort hours.
     |  Local demand substitutions clear inside Neighborhood/Ward/City buffers.
     |  If shock > Slack SL^E: transition to [S8: SCOPED_REPLANNING] via UFB & IF_k.
     v
  [S9: YEAR_END_RECONCILIATION_AND_AUDIT (EUTHYNAI)]
        Society Account & CAP Accounts reconciled; savings/borrowing carried forward;
        Audit Panels verify IFB/UFB logs; seed P^(0) for Year T+1.
```

---

## 5. Planning-Round Algorithms and Mathematical Convergence Analysis

We specify three algorithmic variants for the core iterative loop (`S2 -> S3 -> S4`):

### Algorithm 1: Classical Lange-Arrow-Hurwicz Gradient Tâtonnement (PEPE Ch. 5, pp. 89–93)
- **Price Update:**
  $$P_i^{(t+1)} = \max\left(0, \, P_i^{(t)} + \gamma \cdot ED_i^{(t)}\right), \quad 0 < \gamma < 1$$
- **Properties:** Proven to converge to a Pareto-optimal saddle point in continuous time under strict convexity of council well-being functions and production sets (Arrow, Hurwicz, & Uzawa 1958; Heal 1973, Ch. 4; Henry 1972).
- **Practical Defect:** In discrete rounds with heterogeneous good scales, a uniform linear step $\gamma$ either oscillates wildly ("overshooting," PEPE Ch. 4, p. 67) or converges in hundreds of iterations.

### Algorithm 2: Hahnel-Weisdorf-Szczepanczyk Damped Exponential Rule (DEP Ch. 9, p. 179; `pequod-cljs`)
- **Price Update:** Uses the scale-invariant relative imbalance $\rho_i^{(t)} = \frac{2|S_i^{(t)} - D_i^{(t)}|}{S_i^{(t)} + D_i^{(t)}}$:
  $$\tilde{\delta}_i^{(t)} = 1.05 - 0.5^{\rho_i^{(t)}}, \qquad \delta_i^{(t)} = \max\left(0.001, \, \min\left(\tilde{\delta}_i^{(t)}, \, \tilde{\delta}_i^{(t)} \cdot \min\left(0.25, \rho_i^{(t-1)}\right)\right)\right)$$
  $$P_i^{(t+1)} = P_i^{(t)} \cdot \left(1 + \text{sign}\left(D_i^{(t)} - S_i^{(t)}\right) \delta_i^{(t)}\right)$$
- **Properties:** Scale-invariant multiplicative update; damps step sizes automatically as $\rho_i^{(t-1)}$ shrinks, preventing late-round oscillation. Converges in ~6–12 rounds for smooth Cobb-Douglas agents.
- **Practical Defect Identified in Our Source Audit (`research/sources/hahnel_2021_dep_analysis.md`):** Purely diagonal (ignores input-output cross-price Jacobian $I - A$), does not enforce hard ecological caps ($D_r \le r^*$) as barrier constraints, and can chatter if production technologies are piecewise linear (Leontief/activity analysis) rather than smooth Cobb-Douglas.

### Algorithm 3: Proposed DPEP Safeguarded Primal-Dual / Augmented-Lagrangian Protocol (Technical Extension)
To handle realistic input-output coupling, discrete activity bounds, endogenous income updates, and hard ecological ceilings without granting discretionary power to IFB staff, DPEP pairs the transparent multiplicative update rule with **Augmented Lagrangian proximal regularization (ADMM-style damping)**:
1. **Local Council Proximal Regularization (Anti-Oscillation Rule, formalizing PEPE Ch. 4, p. 70):**
   When worker council $WC_j$ optimizes its proposal in round $t \ge 3$, its local decision-support solver adds a small quadratic proximal penalty $\frac{\mu^{(t)}}{2} \|\pi_j - \pi_j^{(t-1)}\|^2$ (or explicit percentage trust-region bounds $|\Delta \pi_{j,i}| \le \beta^{(t)} \pi_{j,i}^{(t-1)}$, exactly as described in PEPE Ch. 4, p. 70!). This makes the council's supply response strictly Lipschitz-continuous even when its underlying technology is linear or piecewise-linear!
2. **Endogenous Income Fixed-Point Update:**
   In each round $t$, $w_{\text{base}}^{(t)}$ and $B_h^{(t)}$ are updated via damped relaxation:
   $$w_{\text{base}}^{(t)} = (1 - \alpha_w) w_{\text{base}}^{(t-1)} + \alpha_w \frac{(1 - \sigma_{\text{inv}}) Y^{\text{GDP}}(P^{(t)}) - Y^{\text{allow}}}{H^{\text{tot}}}, \quad \alpha_w \in (0.3, 0.7)$$
3. **Hard Ecological Barrier Pricing:**
   For natural resources $r \in \mathcal{R}$ and pollutants $z \in \mathcal{Z}$ approaching their hard biophysical cap $E_z^{\max}$, the price update incorporates an asymmetric barrier multiplier when $D_z^{(t)} > E_z^{\max}$ so biophysical limits are strictly respected before termination.

---

## 6. Canonical Data Schemas and Message Specifications

Below are the language-agnostic canonical data schemas (expressible in Protobuf / CBOR / JSON-Schema) required for the protocol.

```protobuf
syntax = "proto3";
package dpep.v1;

// Fixed-point decimal representation for deterministic cross-platform arithmetic
// (Avoids IEEE-754 floating-point non-determinism across x86, ARM, and WASM)
message FixedDecimal {
  int64 mantissa = 1; // Value = mantissa * 10^(-scale), default scale = 6 (micro-units)
  uint32 scale = 2;
}

enum CategoryType {
  CATEGORY_PRIVATE_GOOD = 0;
  CATEGORY_PUBLIC_GOOD = 1;
  CATEGORY_INTERMEDIATE_INPUT = 2;
  CATEGORY_NATURAL_RESOURCE = 3;
  CATEGORY_LABOR_CATEGORY = 4;
  CATEGORY_CAPITAL_ASSET = 5;
  CATEGORY_POLLUTANT = 6;
}

message SparseItemVector {
  repeated uint32 item_ids = 1;          // Sorted catalog indices in Omega
  repeated FixedDecimal quantities = 2;  // Strictly non-negative quantities
}

// Qualitative List entry (PEPE Ch. 6, pp. 110-112)
message QualitativeAnnotation {
  uint32 item_id = 1;                    // 0 for council-wide narrative, >0 for specific item
  string summary_code = 2;               // Standardized taxonomy tag (e.g., "MEDICAL_NEED", "HAZARD_REDUCTION")
  string narrative_text = 3;             // Concise human-readable explanation
  bytes content_cid = 4;                 // BLAKE3 content-addressed hash of extended documentation
}

// Consumer Council Proposal (Neighborhood CC_h or Federation CF_f)
message ConsumerCouncilProposal {
  uint32 plan_year = 1;
  uint32 round_number = 2;
  bytes council_id = 3;
  uint32 member_population = 4;
  SparseItemVector private_demand = 5;           // Aggregated over members (individual bundles stay private!)
  SparseItemVector local_public_demand = 6;      // Council-level collective goods
  FixedDecimal total_social_cost = 7;            // SC(CC_h, P^(t))
  FixedDecimal warranted_budget_allowance = 8;   // B(CC_h, P^(t))
  bool requests_exception = 9;                   // True if SC > B
  repeated QualitativeAnnotation qualitative_list = 10;
  bytes member_commitments_merkle_root = 11;     // Root of individual members' signed private budget proofs
  bytes council_threshold_signature = 12;        // Post-quantum / hybrid council signature
}

// Worker Council Proposal (WC_j)
message WorkerCouncilProposal {
  uint32 plan_year = 1;
  uint32 round_number = 2;
  bytes council_id = 3;
  uint32 industry_federation_id = 4;
  uint32 worker_count = 5;
  SparseItemVector proposed_outputs = 6;         // bar{a}_j
  SparseItemVector intermediate_inputs = 7;      // underline{a}_j
  SparseItemVector natural_resources = 8;        // r_j
  SparseItemVector total_labor_requested = 9;    // l_j^0 + Delta l_j
  SparseItemVector total_capital_requested = 10; // k_j^0 + Delta k_j
  SparseItemVector pollutant_emissions = 11;     // e_j
  FixedDecimal aggregate_effort_hours = 12;
  FixedDecimal social_benefit = 13;              // SB_j(P^(t))
  FixedDecimal social_cost = 14;                 // SC_j(P^(t))
  FixedDecimal sb_sc_ratio = 15;                 // SB_j / SC_j
  bool requests_appeal = 16;                     // True if SB_j / SC_j < 1.0
  repeated QualitativeAnnotation qualitative_list = 17;
  bytes council_threshold_signature = 18;
}

// Iteration Facilitation Board (IFB) Round Summary & Price Vector
message RoundAggregationAndPrices {
  uint32 plan_year = 1;
  uint32 round_number = 2;
  repeated FixedDecimal indicative_prices = 3;   // P^(t+1) for all |Omega| items
  repeated FixedDecimal total_supply = 4;        // S^(t)
  repeated FixedDecimal total_demand = 5;        // D^(t)
  repeated FixedDecimal planned_slack = 6;       // SL^(t)
  repeated FixedDecimal relative_imbalance = 7;  // rho_i^(t)
  FixedDecimal base_hourly_remuneration = 8;     // w_base^(t)
  FixedDecimal max_imbalance = 9;                // max_i rho_i^(t)
  bool threshold_met = 10;
  bytes proposals_merkle_sum_root = 11;          // Cryptographic commitment to all council proposals
  bytes deterministic_wasm_code_hash = 12;       // Hash of the price-update rule executed
  bytes ifb_attestation_signature = 13;
}
```

---

## 7. Invariants, Safety Properties, and Complexity Estimates

### 7.1 Protocol Safety Invariants
1. **INV-1 (No Unbacked Consumption Credit Creation):** For every neighborhood council $CC_h$, the sum of individual members' committed budgets equals the council's warranted budget $B(CC_h, P)$, and $\sum_{h \in \mathcal{H}} B(CC_h, P) + I^{\text{inv}}(P) \equiv Y^{\text{GDP}}(P)$ in the Society Account.
2. **INV-2 (Non-Negative Quantities and Prices):** $\forall i \in \Omega: P_i^{(t)} \ge 0, S_i^{(t)} \ge 0, D_i^{(t)} \ge 0$.
3. **INV-3 (Deterministic Fixed-Point Reproducibility):** Given the Merkle-Sum Tree root `proposals_merkle_sum_root` of round $t$ and prior state `RoundAggregationAndPrices(t-1)`, any node executing the price-update state transition produces the exact bit-for-bit identical `RoundAggregationAndPrices(t)`.
4. **INV-4 (Effort-Cap Soundness):** No Worker Council can issue individual effort certificates $\epsilon_u$ whose hours-weighted mean exceeds its ratified cap $\min(\bar{\epsilon}_{\max}, SB_j/SC_j)$.
5. **INV-5 (Individual Private Consumption Non-Veto):** If an individual $u$'s private consumption vector $y_u^{\text{priv}}$ satisfies $p^{\text{priv}} \cdot y_u^{\text{priv}} + \text{PublicShare}_u \le B_u$ and contains no banned items, no neighborhood council node can block its inclusion in $y_h^{\text{priv}}$ (PEPE Ch. 3, p. 41).

### 7.2 Computational and Communication Complexity
Let:
- $N_{\text{ind}} = |\mathcal{I}|$ be total population.
- $M = |\mathcal{H}| + |\mathcal{J}| + |\mathcal{F}^C| + |\mathcal{C}^{\text{CAP}}|$ be total councils and federations.
- $G = |\Omega|$ be the number of coarse priced categories in annual planning (typically $500 \le G \le 50,000$).
- $s \ll G$ be the average sparsity (number of non-zero items per council proposal; typically $s \in [20, 500]$).
- $R$ be the number of planning iterations ($R \approx 6\text{–}15$ for annual planning).

| Operation | Per-Round Computational Complexity | Per-Round Communication Complexity | Bottleneck Analysis |
| :--- | :--- | :--- | :--- |
| **1. Local Council Proposal Optimization** | $O(s^2)$ to $O(s^3)$ per council (completely parallel across $M$ councils) | $0$ (computed locally on council/member devices) | **Embarrassingly parallel.** Even for a 500-input LP/QP, takes $<5\text{ ms}$ on a smartphone or laptop. |
| **2. Proposal Submission & Federated Aggregation** | $O(M \cdot s)$ vector additions across a federation tree of branching factor $b$ and depth $L = \lceil \log_b M \rceil$ | $O(M \cdot s)$ total signed sparse entries across the network; $O(b \cdot G_{\text{active}})$ per federation aggregator node | With $M = 60,000$ councils and $s = 100$, total raw payload per round is $\sim 6 \times 10^6 \times 12\text{ B} \approx \mathbf{72\text{ MB}}$ economy-wide! |
| **3. IFB Price & Surplus Calculation** | $O(G)$ arithmetic operations once aggregated vectors $S^{(t)}, D^{(t)}$ are summed | $O(G)$ broadcast of new price vector $P^{(t+1)}$ ($G = 10,000 \implies \sim 160\text{ KB}$ per round) | **Trivial ($<1\text{ ms}$ CPU).** High TPS blockchain consensus is *not* needed for price computation. |
| **4. Intra-Year Fulfillment & Inventory Updates** | $O(1)$ per drawdown event | Local to consumer council & distribution point; federated rollups $O(G_{\text{SKU}})$ periodically | Handled via local-first CRDTs/double-entry channels, not global consensus. |

---

## 8. Distributed Execution Model: Consistency and Privacy Partition

A central requirement of Section 4 is to identify **what must be globally consistent, what can be federated, what can be locally computed, and what must remain private**.

| Data / Operation | Required Consistency Scope | Required Privacy Scope | Why Global Blockchain Consensus Is (or Is Not) Needed |
| :--- | :--- | :--- | :--- |
| **1. Individual Private Consumption Bundles ($y_u^{\text{priv}}$) & Medical/Personal Needs** | **Local / Household + Neighborhood Commitment** | **Strictly Private to Individual/Household** (unless requesting a special-need exception above $B_u$) | Never broadcast globally or even in plaintext to neighbors; only the sum $y_h^{\text{priv}} = \sum_u y_u^{\text{priv}}$ and a ZK/Pedersen proof that $\forall u: P \cdot y_u^{\text{priv}} \le B_u^{\text{priv}}$ are needed by $CC_h$. |
| **2. Internal Workplace Task Balancing (BJCs) & Individual Effort Ratings ($\epsilon_u$)** | **Local to Worker Council ($WC_j$)** (with summary cap proof to Industry Federation / Society Account) | **Council-Internal** (individual received allowance $B_u$ is shared only between worker $u$, $WC_j$, and $CC_h$ via blinded credential) | Internal work-team scheduling and peer effort deliberation affect only $WC_j$ members; only the aggregate cap invariant ($\bar{\epsilon}_j \le SB_j/SC_j$) requires external verification. |
| **3. Council Proposal Drafting & Local What-If Simulation** | **Local-First (CRDT / Offline-Capable)** | **Council-Internal until Round Submission** | Members draft, debate, and amend proposals offline or on a local council LAN/peer group before co-signing the council's round submission. |
| **4. Federated Aggregation of Supply/Demand & Intra-Year Variance Cancellation** | **Federated (Hierarchical Merkle-Sum Tree across Ward $\to$ City $\to$ Region / Industry)** | **Public at Council-Aggregate Level** (PEPE Ch. 4, p. 65) | Intermediate sums are computed and verified along the federation tree; intra-year consumer swaps that cancel within a ward or city never touch the global state. |
| **5. Round Price Vectors ($P^{(t)}$), Global Supply/Demand Totals ($S^{(t)}, D^{(t)}$), Final Ratified Plan Root, and Macro Society Account** | **Globally Consistent (Epoch-Based Checkpoint once per Round / Plan Approval)** | **100% Public and Auditable** | All councils in the economy must see the *same* indicative price vector $P^{(t)}$ at the start of round $t$ and the *same* ratified plan root at the end of planning. However, this requires **only ~10–20 global state checkpoints per year** during annual planning (plus periodic macro-settlement checkpoints)—not a 100,000 TPS per-transaction global blockchain! |
