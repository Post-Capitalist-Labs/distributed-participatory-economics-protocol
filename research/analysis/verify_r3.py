#!/usr/bin/env python3
"""Third-refinement numerical checks for the DPEP monograph.

Run from the repository root (standard library only):

    python3 research/analysis/verify_r3.py

Writes research/analysis/r3_verification_results.json and prints a summary.
If research/analysis/bench_prio3/results_m4pro.jsonl exists, predicted
Prio3SumVec sizes are checked byte-for-byte against the libprio measurements.

Sections
  A  one-sided vs two-sided success measures (single plant, staggered plants, Scarf)
  B  Algorithm 3b as printed vs Deng et al. (2017) Algorithm 4 with a slack block
  C  Table 6.1 cells parsed from the .tex, rescoring and score-perturbation sensitivity
  D  household report sizes, reporting unit, coarse baseline, per-year uploads
  E  council proposal sizes, leaf archive, signature counts (Table 9.2 rows)
  F  Layer-1 block and unit conventions
  G  budget per FTE-year
"""
from __future__ import annotations

import json
import math
import os
import random
import re
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)

import parameters as P  # noqa: E402
from verify_economics import pequod_price_step  # noqa: E402

TAU = 0.05          # two-sided clearing tolerance (book: tau in [0.01, 0.05])
U_MAX = 0.05        # proposed maximum unused-output share (value-weighted)


# ---------------------------------------------------------------------------
# A. Success measures beyond one-sided feasibility (R3-02)
# ---------------------------------------------------------------------------
def classify(s, d, p):
    """Return feasible / cleared flags and value-weighted unused and unmet shares."""
    feasible = all(di <= si + 1e-12 for si, di in zip(s, d))
    val_s = sum(pi * si for pi, si in zip(p, s))
    val_d = sum(pi * di for pi, di in zip(p, d))
    unused = sum(pi * max(0.0, si - di) for pi, si, di in zip(p, s, d))
    unmet = sum(pi * max(0.0, di - si) for pi, si, di in zip(p, s, d))
    rho = [2 * abs(si - di) / (si + di) if si + di > 0 else 0.0 for si, di in zip(s, d)]
    u_share = unused / val_s if val_s > 0 else 0.0
    m_share = unmet / val_d if val_d > 0 else 0.0
    cleared = feasible and max(rho) <= TAU and u_share <= U_MAX
    return {"feasible": feasible, "cleared": cleared, "max_rho": max(rho),
            "unused_share": u_share, "unmet_share": m_share}


def run_plants(thresholds, cap, a=70.0, p0=8.0, rounds=500):
    p, pd = [p0], [0.25]
    hist = []
    for t in range(1, rounds + 1):
        s = [sum(cap for th in thresholds if p[0] >= th)]
        d = [max(0.0, a - p[0])]
        c = classify(s, d, p)
        c.update(round=t, price=p[0], S=s[0], D=d[0])
        hist.append(c)
        p, pd, _ = pequod_price_step(s, d, pd, p)
    first_feas = next((h for h in hist if h["feasible"]), None)
    first_clear = next((h for h in hist if h["cleared"]), None)
    last = hist[-100:]
    return {
        "first_feasible": {k: round(v, 4) if isinstance(v, float) else v for k, v in first_feas.items()} if first_feas else None,
        "first_cleared_round": first_clear["round"] if first_clear else None,
        "share_of_rounds_feasible": round(sum(h["feasible"] for h in hist) / rounds, 4),
        "share_of_rounds_cleared": round(sum(h["cleared"] for h in hist) / rounds, 4),
        "last100_feasible_unused_share_max": round(max((h["unused_share"] for h in last if h["feasible"]), default=float("nan")), 4),
        "last100_unmet_share_max": round(max(h["unmet_share"] for h in last), 4),
    }


def scarf_metrics(rounds=3000):
    supply = [1.0, 1.0, 1.0]
    prices, pd = [1.3, 1.0, 0.8], [0.25] * 3
    hist = []
    for t in range(1, rounds + 1):
        dem = [0.0, 0.0, 0.0]
        for i in range(3):
            j = (i + 1) % 3
            q = prices[i] / (prices[i] + prices[j])
            dem[i] += q
            dem[j] += q
        hist.append(classify(supply, dem, prices))
        prices, pd, _ = pequod_price_step(supply, dem, pd, prices)
    feas = [h for h in hist if h["feasible"]]
    return {
        "share_rounds_feasible": round(len(feas) / rounds, 4),
        "first_feasible_round": next((i + 1 for i, h in enumerate(hist) if h["feasible"]), None),
        "unused_share_when_feasible_min": round(min((h["unused_share"] for h in feas), default=float("nan")), 4),
        "unused_share_when_feasible_median": round(statistics.median([h["unused_share"] for h in feas]), 4) if feas else None,
        "share_rounds_cleared": round(sum(h["cleared"] for h in hist) / rounds, 4),
        "min_max_rho": round(min(h["max_rho"] for h in hist), 4),
    }


def section_a():
    K = 20
    stag = [8.5 + 3.0 * i / (K - 1) for i in range(K)]
    return {
        "definitions": {
            "feasible": "D_g <= S_g for every good and every hard cap (one-sided)",
            "cleared": f"feasible and max_rho <= {TAU} and value-weighted unused output <= {U_MAX}",
            "socially_acceptable": "cleared, unmet need below a ratified threshold, and welfare gap to an oracle below a ratified threshold (requires an oracle; not computable for these toy cases)",
        },
        "single_plant": run_plants([10.0], 100.0),
        "K20_staggered_a70": run_plants(stag, 100.0 / K),
        "K20_identical_a70": run_plants([10.0] * K, 100.0 / K),
        "scarf": scarf_metrics(),
    }


# ---------------------------------------------------------------------------
# B. Algorithm 3b vs Deng et al. (2017) Algorithm 4 (R3-12)
# ---------------------------------------------------------------------------
def argmin_box(grad_fn, lo=0.0, hi=10.0):
    """Minimise a strictly convex 1-D function on [lo, hi] given its derivative."""
    if grad_fn(lo) >= 0:
        return lo
    if grad_fn(hi) <= 0:
        return hi
    a, b = lo, hi
    for _ in range(80):
        m = 0.5 * (a + b)
        if grad_fn(m) > 0:
            b = m
        else:
            a = m
    return 0.5 * (a + b)


def deng_alg4(welfare, rho=1.0, gamma=1.0, rounds=20000, b=1.0):
    """Two councils + one slack block s >= 0 for x1 + x2 <= b, i.e. x1 + x2 + s = b.

    Deng et al. Algorithm 4 (proximal Jacobian ADMM), standard proximal P_i = tau I,
    with tau > rho * (N / (2 - gamma) - 1) * ||A_i||^2 and N = 3 blocks (eq. 2.11).
    Lagrangian sign follows the paper: L = f - lambda^T (Ax - c).
    """
    N = 3
    tau = rho * (N / (2 - gamma) - 1) + 0.01
    x, s, lam = [0.0, 0.0], 0.0, 0.0
    dw = (lambda v: 1.0) if welfare == "linear" else (lambda v: 1.0 / (1.0 + v))
    tail = []
    for t in range(rounds):
        r_old = x[0] + x[1] + s - b
        new = []
        for i in range(2):
            others = r_old - x[i]
            g = lambda v, xi=x[i], o=others: -dw(v) + rho * (v + o - lam / rho) + tau * (v - xi)
            new.append(argmin_box(g))
        others_s = r_old - s
        gs = lambda v: rho * (v + others_s - lam / rho) + tau * (v - s)
        s_new = argmin_box(gs, 0.0, 100.0)
        x, s = new, s_new
        lam = lam - gamma * rho * (x[0] + x[1] + s - b)
        if t >= rounds - 2000:
            tail.append((abs(x[0] + x[1] - b) if x[0] + x[1] > b else 0.0, -lam, x[0] + x[1]))
    return {
        "tau": round(tau, 3),
        "max_violation_last2000": round(max(v for v, _, _ in tail), 6),
        "price_range_last2000": [round(min(p for _, p, _ in tail), 4), round(max(p for _, p, _ in tail), 4)],
        "sum_x_final": round(tail[-1][2], 6),
    }


def printed_3b(welfare, rho=1.0, rounds=20000, b=1.0):
    """Algorithm 3b exactly as printed (no augmented/residual term)."""
    prox = rho * 2 + 1e-3
    x, lam = [0.0, 0.0], 0.0
    dw = (lambda v: 1.0) if welfare == "linear" else (lambda v: 1.0 / (1.0 + v))
    tail = []
    for t in range(rounds):
        x = [argmin_box(lambda v, xi=xi: -dw(v) + lam + prox * (v - xi)) for xi in x]
        lam = max(0.0, lam + rho * (sum(x) - b))
        if t >= rounds - 2000:
            tail.append((abs(sum(x) - b), lam))
    return {
        "max_abs_resid_last2000": round(max(a for a, _ in tail), 4),
        "lambda_range_last2000": [round(min(c for _, c in tail), 4), round(max(c for _, c in tail), 4)],
    }


def section_b():
    out = {}
    for w in ("linear", "log"):
        out[w] = {"as_printed": printed_3b(w), "deng_alg4_slack": deng_alg4(w)}
    out["condition_note"] = (
        "Deng et al. (2.8)/(2.11): P_i > rho*(N/(2-gamma) - 1)*A_i^T A_i (strict), N = number of "
        "blocks including any slack block; standard proximal P_i = tau I needs "
        "tau > rho*(N/(2-gamma)-1)*||A_i||^2, prox-linear P_i = tau I - rho A_i^T A_i needs "
        "tau > rho*N/(2-gamma)*||A_i||^2. The book's P_c >= rho*N*A_c^T A_c is sufficient for "
        "gamma = 1 only when A_c has full column rank (strictness)."
    )
    return out


# ---------------------------------------------------------------------------
# C. Table 6.1 (R3-18)
# ---------------------------------------------------------------------------
REFERENCE = {  # Test C rows as supplied by the reviewer
    "w": [9, 10, 8, 8, 7, 8, 9, 8, 9, 6, 6, 4, 4, 4],
    "A": [2, 2, 2, 5, 4.5, 4.5, 1.5, 1, 2.5, 4, 5, 4, 4.5, 4],
    "B": [5, 3, 4.5, 4, 2.5, 3.5, 5, 2.5, 2, 3.5, 3, 4.5, 4, 3.5],
    "C": [3, 4.5, 4, 2, 1.5, 1.5, 1, 5, 1, 2, 2.5, 2, 2.5, 2],
    "D": [4.5, 4, 4.5, 5, 4.5, 4.5, 5, 4, 4, 4, 3.5, 4.5, 4, 4],
}
# Third-pass rescore of D (rows 4, 5, 6, 9, 12) after the libprio benchmark,
# the proposal-size rework and the VDAF once-only finding. Rationale in the book.
RESCORE_D = [4.5, 4.0, 4.5, 4.0, 3.5, 4.0, 5.0, 4.0, 3.5, 4.0, 3.5, 4.0, 4.0, 4.0]


def parse_table61(tex):
    block = tex.split(r"\label{tab:arch-comp}", 1)[1].split(r"\midrule", 1)[1].split(r"\midrule", 1)[0]
    rows = []
    for line in block.strip().splitlines():
        m = re.match(r"\s*(\d+)\.\s.*?&\s*(\d+)\\%\s*&\s*([\d.]+)\s*&\s*([\d.]+)\s*&\s*([\d.]+)\s*&\s*(?:\\textbf\{)?([\d.]+)", line)
        if m:
            rows.append([int(m.group(2))] + [float(m.group(i)) for i in range(3, 7)])
    return rows


def score(w, s):
    return sum(a * b for a, b in zip(w, s)) / sum(w)


def section_c(tex):
    """Table 6.1: reviewer's reference cells (pre-rescore) and the book's current cells."""
    rows = parse_table61(tex)
    book = {"w": [r[0] for r in rows], "A": [r[1] for r in rows], "B": [r[2] for r in rows],
            "C": [r[3] for r in rows], "D": [r[4] for r in rows]} if len(rows) == 14 else None
    ref = {k: [float(x) for x in v] for k, v in REFERENCE.items()}
    w = ref["w"]

    def scores(ws, tab):
        return {k: round(score(ws, tab[k]), 3) for k in "ABCD"}

    focus = {3, 10, 11}
    rest = sum(w[i] for i in range(14) if i not in focus)
    w70 = [0.7 / 3 if i in focus else 0.3 * w[i] / rest for i in range(14)]

    def crossover(tab):
        for k in range(0, 101):
            a = k / 100
            ws = [a / 3 if i in focus else (1 - a) * w[i] / rest for i in range(14)]
            if score(ws, tab["A"]) > score(ws, tab["D"]):
                return a
        return None

    def harsh(tab):
        t = dict(tab)
        h = list(tab["D"])
        h[1], h[4], h[5], h[8] = 3.5, 2.5, 3, 3
        t["D"] = h
        return t

    rescored = dict(ref)
    rescored["D"] = RESCORE_D
    rng = random.Random(20261104)
    wins = {k: 0 for k in "ABCD"}
    lead = []
    for _ in range(20000):
        sc = {k: score(w, [min(5, max(1, v + rng.uniform(-1, 1))) for v in rescored[k]]) for k in "ABCD"}
        wins[max(sc, key=sc.get)] += 1
        lead.append(sc["D"] - max(v for k, v in sc.items() if k != "D"))
    lead.sort()
    out = {
        "reviewer_reference": {
            "baseline": scores(w, ref), "seventy_pct_4_11_12": scores(w70, ref),
            "harsher_D": scores(w, harsh(ref)),
            "A_beats_D_on": [i + 1 for i in range(14) if ref["A"][i] > ref["D"][i]],
            "D_ge_A_count": sum(ref["D"][i] >= ref["A"][i] for i in range(14)),
        },
        "rescored_D_row": RESCORE_D,
        "rescored": {
            "baseline": scores(w, rescored), "equal_weights": scores([1] * 14, rescored),
            "seventy_pct_4_11_12": scores(w70, rescored), "harsher_D": scores(w, harsh(rescored)),
            "A_overtakes_D_at_focus_weight": crossover(rescored),
            "A_beats_D_on": [i + 1 for i in range(14) if rescored["A"][i] > RESCORE_D[i]],
            "D_ge_A_count": sum(RESCORE_D[i] >= rescored["A"][i] for i in range(14)),
            "perturbation_U(-1,1)_wins_share": {k: round(v / 20000, 4) for k, v in wins.items()},
            "perturbation_D_lead_p05_p50": [round(lead[1000], 3), round(lead[10000], 3)],
        },
        "book_table_rows_parsed": len(rows),
        "book_table_matches_rescored": bool(book) and book["D"] == RESCORE_D
        and all(book[k] == ref[k] for k in "wABC"),
    }
    return out


# ---------------------------------------------------------------------------
# D. Household reports (R3-04, R3-05, R3-06, R3-08)
# ---------------------------------------------------------------------------
def section_d():
    configs = [(3000, 20), (3000, 64), (10000, 64), (230, 20), (100, 32),
               (100, 20), (230, 32), (3000, 32), (100, 64), (230, 64),
               (100, 16), (150, 16), (200, 16), (250, 16), (200, 20), (3000, 16)]
    sizes = {}
    for length, bits in configs:
        r = P.prio3_report_bytes(length, bits)
        sizes[f"{length}x{bits}"] = {
            "encoded_measurement_bytes": length * bits * P.FIELD128_ENCODED_SIZE,
            "leader_share_bytes": r["leader_share_bytes"],
            "client_upload_bytes": r["client_upload_bytes"],
            "fits_75kB_leader": r["leader_share_bytes"] <= 75_000,
            "chunk_length": P.optimal_chunk_length(length * bits),
        }
    bench_path = os.path.join(HERE, "bench_prio3", "results_m4pro.jsonl")
    bench_check = None
    if os.path.exists(bench_path):
        bench_check = []
        with open(bench_path) as f:
            for line in f:
                b = json.loads(line)
                pred = P.prio3_report_bytes(b["length"], b["bits"])
                bench_check.append({
                    "length": b["length"], "bits": b["bits"],
                    "measured_leader": b["leader_input_share_bytes"],
                    "predicted_leader": pred["leader_share_bytes"],
                    "match": b["leader_input_share_bytes"] == pred["leader_share_bytes"],
                    "measured_upload": b["client_upload_bytes"],
                    "predicted_upload": pred["client_upload_bytes"],
                    "verify_init_leader_ms": b["verify_init_leader_ms_median"],
                    "verify_init_helper_ms": b["verify_init_helper_ms_median"],
                    "shard_ms": b["shard_ms_median"],
                })
    max_units_at_micro = {b: (2 ** b - 1) / P.PROTOCOL_SCALE for b in (16, 20, 32, 64)}
    # aggregator CPU per round at N = 10^6 reports, single core, from bench medians
    agg_cpu = {}
    if bench_check:
        for row in bench_check:
            key = f"{row['length']}x{row['bits']}"
            agg_cpu[key] = {
                "core_minutes_per_aggregator_1e6": round(row["verify_init_helper_ms"] * 1e6 / 60000, 1),
                "minutes_on_16_cores": round(row["verify_init_helper_ms"] * 1e6 / 60000 / 16, 1),
            }
    per_year = {}
    for key in ("3000x20", "200x16"):
        up = sizes[key]["client_upload_bytes"]
        per_year[key] = {
            "per_fresh_report_bytes": up,
            "per_year_10_rounds_MB": round(10 * up / 1e6, 2),
            "per_year_3_milestones_MB": round(P.ROUNDS_FRESH_REPORT * up / 1e6, 2),
        }
    rounding = {
        "s_g=100000 micro (0.1 unit), N=200": P.hru_rounding(200, 100_000),
        "s_g=100000 micro (0.1 unit), N=10^6": P.hru_rounding(10 ** 6, 100_000),
    }
    return {
        "sizes": sizes,
        "bench_check": bench_check,
        "max_quantity_at_1e-6_scale_by_bits": max_units_at_micro,
        "aggregator_cpu_1e6_reports_desktop": agg_cpu,
        "per_year_upload": per_year,
        "hru_rounding": {k: {kk: round(vv, 1) for kk, vv in v.items()} for k, v in rounding.items()},
        "sparse_note": "Prio3SumVec sums fixed coordinates (VDAF-22 s7.4.3); a 50-coordinate "
                       "vector cannot encode 50 items chosen from 3,000 without revealing which.",
    }


# ---------------------------------------------------------------------------
# E. Proposals, archive, signature counts (R3-10, R3-11, R3-18 Table 9.2)
# ---------------------------------------------------------------------------
def section_e():
    sig = P.ML_DSA_65_SIG_BYTES
    hyb = P.HYBRID_SIG_BYTES
    checks = {
        "book_5200_minus_one_sig": 5200 - sig,
        "items_in_remainder": (5200 - sig) // P.SPARSE_ITEM_BYTES,
        "neighbourhood_dense_3000_items_bytes": 3000 * P.SPARSE_ITEM_BYTES,
    }
    types = {
        "worker_council_150_items_1sig": P.proposal_bytes(150, 1, hyb),
        "worker_council_150_items_5sig": P.proposal_bytes(150, 5, hyb),
        "consumer_council_coarse200_1sig": P.proposal_bytes(200, 1, hyb),
        "consumer_council_coarse200_5sig": P.proposal_bytes(200, 5, hyb),
        "consumer_council_3000_items_1sig": P.proposal_bytes(3000, 1, hyb),
        "consumer_council_3000_items_5sig": P.proposal_bytes(3000, 5, hyb),
    }
    # 40,000 proposals at N = 10^6: half worker, half consumer
    scen = {}
    for name, wc, cc, signers in [
        ("coarse200_single_key", 150, 200, 1),
        ("coarse200_5_signers", 150, 200, 5),
        ("dense3000_single_key", 150, 3000, 1),
        ("dense3000_5_signers", 150, 3000, 5),
    ]:
        per_round = 20_000 * P.proposal_bytes(wc, signers, hyb) + 20_000 * P.proposal_bytes(cc, signers, hyb)
        scen[name] = {
            "raw_MB_per_round": round(per_round / 1e6, 1),
            "raw_GB_per_year_10_rounds": round(10 * per_round / 1e9, 2),
            "signature_verifications_per_round": 40_000 * signers,
        }
    # Table 9.2 Layer-2 rows recomputed from the book's own 5.2 KB leaf and proposals/round
    props = {100: 20, 1000: 40, 10_000: 400, 100_000: 4_000, 1_000_000: 40_000}
    zstd_ratio = 60 / 208
    t92 = {str(n): {"raw_MB_per_year": round(10 * k * 5200 / 1e6, 2),
                    "zstd_MB_per_year": round(10 * k * 5200 * zstd_ratio / 1e6, 2)}
           for n, k in props.items()}
    light = {
        "fetch_all_86_sigs_bytes": 86 * sig,
        "fetch_all_86_hybrid_sigs_bytes": 86 * hyb,
        "coordinator_attestation_bytes": hyb,
        "sample_8_of_86_bytes": 8 * hyb,
    }
    return {"checks": checks, "proposal_types": types, "archive_scenarios_1e6": scen,
            "table92_layer2_recomputed": t92, "light_client_options": light}


# ---------------------------------------------------------------------------
# F. Layer-1 block and units (R3-18)
# ---------------------------------------------------------------------------
def section_f():
    blk = P.layer1_block_bytes()
    total = blk["total_bytes"]
    sigs = blk["sigs_bytes"]
    return {
        "block_bytes": total,
        "block_kB": round(total / 1e3, 1),
        "block_KiB": round(total / 1024, 1),
        "sigs_bytes": sigs,
        "sigs_kB": round(sigs / 1e3, 1),
        "sigs_KiB": round(sigs / 1024, 1),
        "year_425_MB": round(425 * total / 1e6, 1),
        "year_425_MiB": round(425 * total / 2 ** 20, 1),
        "year_435_MB": round(435 * total / 1e6, 1),
        "convention": "SI units (kB = 1,000 B, MB = 10^6 B) throughout the book; KiB only where libprio prints them",
    }


# ---------------------------------------------------------------------------
# G. Budget (R3-03)
# ---------------------------------------------------------------------------
def section_g():
    out = {}
    for name, (f_lo, f_hi, m_lo, m_hi, l_lo, l_hi, n_lo, n_hi) in P.BUDGET_ROWS.items():
        fy_lo, fy_hi = f_lo * m_lo / 12, f_hi * m_hi / 12
        out[name] = {
            "fte_years": [round(fy_lo, 3), round(fy_hi, 3)],
            "implied_labour_per_fte_year_at_matched_ends": [round(l_lo / fy_lo), round(l_hi / fy_hi)],
        }
    # Table 9.1 assigns $25k-$45k to Phase 1 alone at 1.0 FTE, 2-3 months.
    out["Phase 1 per Table 9.1"] = {"fte_years": [2 / 12, 3 / 12],
                                    "implied_per_fte_year": [round(25_000 / (2 / 12)), round(45_000 / (3 / 12))]}
    out["Phase 3 incl. audit and hosting"] = {"implied_per_fte_year": [round(250_000 / 2), round(950_000 / 8)]}
    # Proposed reconciliation at one assumed loaded rate band (author to replace).
    rate = (120_000, 180_000)
    plan = {
        "Phase 1": (1.0, 4, 6, 1_000, 3_000),
        "Phase 1H": (1.0, 3, 4, 8_000, 25_000),     # ethics review, consent, compensation, DPIA
        "Phase 2": (2.5, 4, 6, 2_000, 5_000),
        "Phase 3": (4.0, 9, 12, 80_000, 230_000),   # audit, hosting, pilot ethics/data protection
    }
    rec = {}
    tot_lo = tot_hi = 0
    for k, (fte, mlo, mhi, nlo, nhi) in plan.items():
        lo = fte * mlo / 12 * rate[0] + nlo
        hi = fte * mhi / 12 * rate[1] + nhi
        rec[k] = [round(lo, -3), round(hi, -3)]
        tot_lo += lo
        tot_hi += hi
    rec["Programme total"] = [round(tot_lo, -3), round(tot_hi, -3)]
    out["proposed_reconciliation_at_120k_180k"] = rec
    return out


def main():
    with open(os.path.join(ROOT, "book", "dpep_book.tex"), encoding="utf-8") as f:
        tex = f.read()
    out = {
        "A_success_measures": section_a(),
        "B_algorithm_3b": section_b(),
        "C_table_6_1": section_c(tex),
        "D_household_reports": section_d(),
        "E_proposals_archive": section_e(),
        "F_layer1_units": section_f(),
        "G_budget": section_g(),
    }
    dest = os.path.join(HERE, "r3_verification_results.json")
    with open(dest, "w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))
    print(f"\nWrote {dest}", file=sys.stderr)


if __name__ == "__main__":
    main()
