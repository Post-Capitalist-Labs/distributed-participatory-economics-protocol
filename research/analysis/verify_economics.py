#!/usr/bin/env python3
"""
Reproducible Verification Script for Economic & Algorithmic Findings (R-ECON-01 to R-ECON-10)
Part of DPEP Working Draft Technical Validation.
"""
import json
import math

def pequod_price_step(supply, demand, prev_pd, prices):
    new_prices = []
    new_pd = []
    rhos = []
    for s, d, pd_prev, p in zip(supply, demand, prev_pd, prices):
        surplus = s - d
        denom = s + d
        rho = (2.0 * abs(surplus) / denom) if denom > 0 else 0.0
        rhos.append(rho)
        tilde_delta = 1.05 - (0.5 ** rho)
        delta = max(0.001, min(tilde_delta, tilde_delta * pd_prev))
        if surplus > 0:
            p_next = p * (1.0 - delta)
        elif surplus < 0:
            p_next = p * (1.0 + delta)
        else:
            p_next = p
        new_prices.append(p_next)
        new_pd.append(min(0.25, rho))
    return new_prices, new_pd, rhos

def test_r_econ_03_scarf():
    """
    R-ECON-03: Test Scarf (1960) 3-good Leontief cyclic example under Pequod price rule
    and multiplicative trust-region damping.
    """
    schedules = {
        "no_damping": lambda t: None,
        "beta_0.25": lambda t: 0.25,
        "beta_0.10": lambda t: 0.10,
        "beta_0.02": lambda t: 0.02,
        "beta_0.25_decay_0.99": lambda t: 0.25 * (0.99 ** t),
    }
    results = {}
    supply = [1.0, 1.0, 1.0]
    for name, beta_fn in schedules.items():
        prices = [1.3, 1.0, 0.8]
        prev_pd = [0.25, 0.25, 0.25]
        prev_c_demands = None
        min_max_rho = 999.0
        final_max_rho = None
        converged_round = None
        for t in range(1, 3001):
            # Consumer i owns 1 unit of good i (income = p_i) and demands min(x_i, x_{i+1})
            # Unconstrained Leontief demand of consumer i for good i and i+1 is p_i / (p_i + p_{i+1})
            c_demands = [[0.0, 0.0, 0.0] for _ in range(3)]
            for i in range(3):
                j = (i + 1) % 3
                q = prices[i] / (prices[i] + prices[j])
                c_demands[i][i] = q
                c_demands[i][j] = q
            if t >= 3 and prev_c_demands is not None:
                beta = beta_fn(t)
                if beta is not None:
                    for i in range(3):
                        for g in range(3):
                            prev_q = prev_c_demands[i][g]
                            target_q = c_demands[i][g]
                            lo = prev_q * (1.0 - beta)
                            hi = prev_q * (1.0 + beta)
                            c_demands[i][g] = max(lo, min(hi, target_q))
            prev_c_demands = [row[:] for row in c_demands]
            agg_demand = [sum(c_demands[i][g] for i in range(3)) for g in range(3)]
            prices, prev_pd, rhos = pequod_price_step(supply, agg_demand, prev_pd, prices)
            max_rho = max(rhos)
            if max_rho < min_max_rho:
                min_max_rho = max_rho
            if max_rho <= 0.05 and converged_round is None:
                converged_round = t
            if t == 3000:
                final_max_rho = max_rho
        results[name] = {
            "min_max_rho_over_3000_rounds": round(min_max_rho, 6),
            "final_max_rho_at_3000": round(final_max_rho, 6),
            "converged_to_5pct": converged_round is not None,
            "final_prices": [round(p, 4) for p in prices],
        }
    return results

def test_r_econ_03b_scarf_fixed_budgets():
    """
    R-ECON-03b: Control for R-ECON-03. Same three Leontief consumers, same goods,
    same starting prices and same price rule, but each consumer's budget is one third
    of the value of total supply instead of the market value of their own endowment.
    Relative incomes then do not move with relative prices (a Fisher market with equal
    budgets, homogeneous of degree zero as under a numeraire). This isolates whether
    the cycle in R-ECON-03 comes from Leontief complementarity or from endowment income.
    """
    supply = [1.0, 1.0, 1.0]
    out = {}
    for mode in ("endowment_income", "fixed_equal_budgets"):
        prices = [1.3, 1.0, 0.8]
        prev_pd = [0.25, 0.25, 0.25]
        min_max_rho = 999.0
        first_5pct = None
        last100 = []
        for t in range(1, 3001):
            agg = [0.0, 0.0, 0.0]
            for i in range(3):
                j = (i + 1) % 3
                income = prices[i] if mode == "endowment_income" else sum(p * s for p, s in zip(prices, supply)) / 3.0
                q = income / (prices[i] + prices[j])
                agg[i] += q
                agg[j] += q
            prices, prev_pd, rhos = pequod_price_step(supply, agg, prev_pd, prices)
            m = max(rhos)
            min_max_rho = min(min_max_rho, m)
            if m <= 0.05 and first_5pct is None:
                first_5pct = t
            if t > 2900:
                last100.append(m)
        out[mode] = {
            "min_max_rho_over_3000_rounds": round(min_max_rho, 6),
            "max_rho_last_100_rounds": round(max(last100), 6),
            "first_round_max_rho_le_5pct": first_5pct,
        }
    return out

def test_r_econ_04_nonconvex_plant():
    """
    R-ECON-04: Single indivisible plant with S(p) = 100 if p >= 10 else 0,
    D(p) = max(0, 70 - p), starting at p = 8 for 500 rounds.
    Also tests Shapley-Folkman effect with K smaller plants with staggered thresholds
    in [8.5, 11.5] summing to capacity 100.
    """
    prices = [8.0]
    prev_pd = [0.25]
    min_rho = 999.0
    for t in range(1, 501):
        p = prices[0]
        s = [100.0 if p >= 10.0 else 0.0]
        d = [max(0.0, 70.0 - p)]
        prices, prev_pd, rhos = pequod_price_step(s, d, prev_pd, prices)
        min_rho = min(min_rho, rhos[0])
    single_plant = {
        "min_rho_over_500_rounds": round(min_rho, 6),
        "final_price": round(prices[0], 4),
        "theoretical_min_imbalance_at_p10": round(2.0 * abs(100.0 - 60.0) / (100.0 + 60.0), 6),
    }

    # Shapley-Folkman comparison: K plants each of capacity 100/K with thresholds evenly in [8.5, 11.5]
    sf_results = {}
    for K in [1, 5, 20, 100]:
        p_k = [8.0]
        pd_k = [0.25]
        min_r = 999.0
        thresholds = [10.0] if K == 1 else [8.5 + 3.0 * i / (K - 1) for i in range(K)]
        for t in range(1, 501):
            p = p_k[0]
            s = [sum((100.0 / K) for th in thresholds if p >= th)]
            d = [max(0.0, 70.0 - p)]
            p_k, pd_k, rhos = pequod_price_step(s, d, pd_k, p_k)
            min_r = min(min_r, rhos[0])
        sf_results[f"K={K}"] = {"min_rho": round(min_r, 6), "final_price": round(p_k[0], 4)}

    return {"single_indivisible_plant": single_plant, "shapley_folkman_multi_plant": sf_results}

def test_r_econ_05_numeraire():
    """
    R-ECON-05: 2 goods with fixed outputs (60, 20), Cobb-Douglas shares (0.6, 0.4),
    H = 100, and Eq. 4.16 with alpha = 0.5, initial w_base = 700.
    Compare starting prices [700, 700] vs [1400, 1400].
    """
    supply = [60.0, 20.0]
    shares = [0.6, 0.4]
    H = 100.0
    runs = {}
    for init_p in [700.0, 1400.0]:
        prices = [init_p, init_p]
        prev_pd = [0.25, 0.25]
        w_base = 700.0
        alpha = 0.5
        for t in range(1, 201):
            # Eq 4.16 update (with sigma_inv = 0, Y_allow = 0)
            y_gdp = prices[0] * supply[0] + prices[1] * supply[1]
            w_base = (1.0 - alpha) * w_base + alpha * (y_gdp / H)
            budget = w_base * H
            demand = [budget * shares[0] / prices[0], budget * shares[1] / prices[1]]
            prices, prev_pd, rhos = pequod_price_step(supply, demand, prev_pd, prices)
            if all(r <= 0.03 for r in rhos):
                break
        runs[f"init_p_{int(init_p)}"] = {
            "converged_round": t,
            "final_p1": round(prices[0], 2),
            "final_p2": round(prices[1], 2),
            "price_ratio_p1_over_p2": round(prices[0] / prices[1], 6),
            "final_w_base": round(w_base, 2),
        }
    return runs

if __name__ == "__main__":
    out = {
        "R_ECON_03_scarf": test_r_econ_03_scarf(),
        "R_ECON_03b_scarf_fixed_budgets": test_r_econ_03b_scarf_fixed_budgets(),
        "R_ECON_04_nonconvex": test_r_econ_04_nonconvex_plant(),
        "R_ECON_05_numeraire": test_r_econ_05_numeraire(),
    }
    print(json.dumps(out, indent=2))
    with open("research/analysis/econ_verification_results.json", "w") as f:
        json.dump(out, f, indent=2)
