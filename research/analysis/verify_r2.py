#!/usr/bin/env python3
"""
Second-refinement numerical checks (R2-03, R2-11, R2-18, R2-19, R2-20, R2-21).

Run from the repository root:
    python3 research/analysis/verify_r2.py

Writes research/analysis/r2_verification_results.json
"""
from __future__ import annotations
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)

from parameters import (
    G_CATALOGUE,
    G_PRIV,
    N_PARTICIPANTS,
    N_VALIDATORS,
    binomial_tail,
    layer1_block_bytes,
    prio3_report_bytes,
    quorum_sig_bytes,
)
from verify_economics import pequod_price_step


def shapley_folkman_sweep() -> dict:
    """Reproduce R2-11 against the book's 0.40% K=20 claim."""

    def run(K, a, thresholds, rounds=500, p0=8.0):
        p_k = [p0]
        pd_k = [0.25]
        rhos = []
        for _ in range(rounds):
            p = p_k[0]
            s = [sum((100.0 / K) for th in thresholds if p >= th)]
            d = [max(0.0, a - p)]
            p_k, pd_k, r = pequod_price_step(s, d, pd_k, p_k)
            rhos.append(r[0])
        last100_max = max(rhos[-100:])
        return {
            "min_over_rounds": round(min(rhos), 6),
            "last100_max": round(last100_max, 6),
            "final_rho": round(rhos[-1], 6),
            "final_price": round(p_k[0], 4),
        }

    K = 20
    staggered = [8.5 + 3.0 * i / (K - 1) for i in range(K)]
    identical = [10.0] * K

    a70 = run(K, 70.0, staggered)
    identical_a70 = run(K, 70.0, identical)

    sweep = []
    a = 60.0
    while a <= 80.0001:
        r = run(K, a, staggered)
        # best-achievable imbalance at any price (not via the price rule)
        best = 1.0
        for p in [x / 10.0 for x in range(50, 201)]:
            s = sum((100.0 / K) for th in staggered if p >= th)
            d = max(0.0, a - p)
            denom = s + d
            rho = (2.0 * abs(s - d) / denom) if denom > 0 else 0.0
            best = min(best, rho)
        sweep.append({"a": a, **r, "best_achievable": round(best, 6)})
        a += 0.5

    last100s = [x["last100_max"] for x in sweep]
    bests = [x["best_achievable"] for x in sweep]
    return {
        "K20_a70_staggered": a70,
        "K20_a70_identical_thresholds": identical_a70,
        "sweep_n": len(sweep),
        "sweep_median_last100_max": round(sorted(last100s)[len(last100s) // 2], 6),
        "sweep_worst_last100_max": round(max(last100s), 6),
        "sweep_share_last100_max_le_5pct": round(
            sum(1 for x in last100s if x <= 0.05) / len(last100s), 4
        ),
        "sweep_worst_best_achievable": round(max(bests), 6),
        "note": "One-good staggered-threshold test; says nothing about interdependent Leontief markets.",
    }


def prio3_sizes() -> dict:
    out = {}
    for length, bits in [
        (G_PRIV, 20),
        (10_000, 20),
        (230, 20),
        (50, 20),
        (G_PRIV, 64),
        (50, 64),
    ]:
        key = f"len{length}_bits{bits}"
        out[key] = prio3_report_bytes(length, bits)
    # items that fit in 75 KB leader share at 20 bits: 75*1024 / (20*16)
    out["items_fitting_75kib_leader_meas_only_20bit"] = int((75 * 1024) / (20 * 16))
    out["book_75kb_claim_fits_full_G_priv"] = (
        out[f"len{G_PRIV}_bits20"]["client_upload_bytes"] <= 75 * 1024
    )
    return out


def committee() -> dict:
    rows = {}
    for n in (64, 128):
        k_fail = n // 3 + 1  # >= n/3 + epsilon; for n=64, 22; n=128, 43
        rows[n] = {}
        for p in (0.10, 0.15, 0.20, 0.25, 0.30):
            single = binomial_tail(n, k_fail, p)
            rows[n][f"p{int(p*100)}"] = {
                "k_fail": k_fail,
                "single_draw": single,
                "single_draw_pct": round(single * 100, 8),
                "annual_if_435_independent_pct": round((1 - (1 - single) ** 435) * 100, 4),
            }
    return rows


def architecture_sensitivity() -> dict:
    # (name, baseline_w, A, B, C, D)
    criteria = [
        ("1. Decentralisation", 0.09, 2.0, 5.0, 3.0, 4.5),
        ("2. Trust Assumptions", 0.10, 2.0, 3.0, 4.5, 4.5),
        ("3. Censorship Resistance", 0.08, 2.0, 4.5, 4.0, 4.5),
        ("4. Throughput & Latency", 0.08, 5.0, 4.0, 2.0, 5.0),
        ("5. Network Bandwidth", 0.07, 4.5, 2.5, 1.5, 4.5),
        ("6. Hardware Requirements", 0.08, 4.5, 3.5, 1.5, 4.5),
        ("7. Offline Capability", 0.09, 1.5, 5.0, 1.0, 5.0),
        ("8. Byzantine Fault Tolerance", 0.08, 1.0, 2.5, 5.0, 4.5),
        ("9. Privacy", 0.09, 2.5, 2.0, 1.0, 4.5),
        ("10. Post-Quantum Readiness", 0.06, 4.0, 3.5, 2.0, 4.5),
        ("11. Implementation Simplicity", 0.06, 5.0, 3.0, 2.5, 3.5),
        ("12. Operational Cost", 0.04, 4.0, 4.5, 2.0, 4.5),
        ("13. Energy Efficiency", 0.04, 4.5, 4.0, 2.5, 4.5),
        ("14. Maintainability", 0.04, 4.0, 3.5, 2.0, 4.0),
    ]

    def score(weights):
        s = [0.0, 0.0, 0.0, 0.0]
        for w, c in zip(weights, criteria):
            for i in range(4):
                s[i] += w * c[2 + i]
        return {k: round(v, 4) for k, v in zip("ABCD", s)}

    base_w = [c[1] for c in criteria]
    equal_w = [1 / 14] * 14

    # Reviewer's 70% split equally across criteria 4, 11, 12; rest proportional
    focus = {3, 10, 11}  # 0-indexed 4, 11, 12
    rest_sum = sum(base_w[i] for i in range(14) if i not in focus)
    w70 = []
    for i, w in enumerate(base_w):
        if i in focus:
            w70.append(0.70 / 3)
        else:
            w70.append(0.30 * w / rest_sum)

    # Theoretical floor for D: 0.7*3.5 + 0.3*4.0 = 3.65 if 70% on its lowest score
    d_scores = [c[5] for c in criteria]
    d_min, d_next = sorted(set(d_scores))[:2]
    theoretical_floor = round(0.70 * d_min + 0.30 * d_next, 4)

    wins = sum(1 for c in criteria if c[5] >= c[2])  # D vs A

    return {
        "baseline": score(base_w),
        "equal_weights": score(equal_w),
        "seventy_pct_on_4_11_12": score(w70),
        "D_theoretical_floor_70pct_on_lowest": theoretical_floor,
        "D_lowest_score": d_min,
        "D_beats_or_equals_A_on": wins,
        "book_claimed_A_4.65_D_3.60_reproducible": False,
        "note": "Weight changes alone cannot make D score 3.60; D's minimum cell is 3.5.",
    }


def pequod_csv_subsets() -> dict:
    """R2-18: subset means the book actually cites."""
    import glob
    import statistics

    pequod = os.environ.get(
        "PEQUOD_DIR",
        "/tmp/pequod_audit/pequod-cljs/src/clj/pequod_cljs",
    )
    if not os.path.isdir(pequod):
        return {"error": f"pequod dir not found: {pequod}"}

    def parse_csv(path):
        with open(path) as f:
            lines = [line.split(",", 2)[:2] for line in f]
        sections, cur = [], []
        for row in lines[1:]:
            if not row:
                continue
            if row[0] == "exponent-sum":
                sections.append(cur)
                cur = []
            else:
                cur.append((int(row[0]), row[1].strip()))
        if cur:
            sections.append(cur)

        def first(section, colours):
            hits = [it for it, col in section if col in colours]
            return hits[0] if hits else None

        y1g = first(sections[0], (":green", ":blue")) if sections else None
        y1b = first(sections[0], (":blue",)) if sections else None
        y2g = first(sections[1], (":green", ":blue")) if len(sections) > 1 else None
        y2b = first(sections[1], (":blue",)) if len(sections) > 1 else None
        # exponent-sum jump between year sections if present
        return y1g, y1b, y2g, y2b

    def subset(lo, hi):
        y1g, y1b, y2g, y2b = [], [], [], []
        missing = []
        for i in range(lo, hi + 1):
            path = os.path.join(pequod, f"dep1ex{i:02d}.csv" if i < 100 else f"dep1ex{i}.csv")
            if not os.path.exists(path):
                missing.append(os.path.basename(path))
                continue
            a, b, c, d = parse_csv(path)
            if a is not None:
                y1g.append(a)
            if b is not None:
                y1b.append(b)
            if c is not None:
                y2g.append(c)
            if d is not None:
                y2b.append(d)
        mean = lambda xs: round(statistics.mean(xs), 3) if xs else None
        return {
            "n": hi - lo + 1 - len(missing),
            "missing": missing,
            "Y1_5pct": mean(y1g),
            "Y1_3pct": mean(y1b),
            "Y2_5pct": mean(y2g),
            "Y2_3pct": mean(y2b),
        }

    clj = sorted(glob.glob(os.path.join(pequod, "dep1ex*.clj")))
    lfs, real = [], []
    for p in clj:
        with open(p, "rb") as f:
            head = f.read(80)
        if head.startswith(b"version https://git-lfs.github.com"):
            lfs.append(os.path.basename(p))
        else:
            real.append(os.path.basename(p))

    # exponent-sum jumps in CSVs (dep1ex and dep2ex)
    def exponent_jumps(pattern):
        jumps = []
        for path in sorted(glob.glob(os.path.join(pequod, pattern))):
            with open(path) as f:
                rows = [line.strip().split(",") for line in f]
            sums = []
            for row in rows:
                if row and row[0] == "exponent-sum":
                    try:
                        sums.append(float(row[1]))
                    except (ValueError, IndexError):
                        pass
            if len(sums) >= 2:
                jumps.append(abs(sums[1] - sums[0]))
        return {
            "n": len(jumps),
            "max_abs_jump": round(max(jumps), 4) if jumps else None,
            "mean_abs_jump": round(sum(jumps) / len(jumps), 4) if jumps else None,
        }

    return {
        "clj_real": real,
        "clj_lfs_pointers": lfs,
        "clj_real_count": len(real),
        "clj_lfs_count": len(lfs),
        "dep1ex01_50": subset(1, 50),
        "dep1ex51_90": subset(51, 90),
        "dep1ex61_100": subset(61, 100),
        "dep1ex01_99_excluding_100": subset(1, 99),
        "dep1ex_exponent_sum_jumps": exponent_jumps("dep1ex*.csv"),
        "dep2ex_exponent_sum_jumps": exponent_jumps("dep2ex*.csv"),
        "dep2ex_csv_count": len(glob.glob(os.path.join(pequod, "dep2ex*.csv"))),
        "dep2ex_clj_count": len(glob.glob(os.path.join(pequod, "dep2ex*.clj"))),
    }


def derived_figures() -> dict:
    q64 = quorum_sig_bytes(64)
    q128 = quorum_sig_bytes(128)
    b64 = layer1_block_bytes(64)
    b128 = layer1_block_bytes(128)
    prio = prio3_report_bytes(G_PRIV, 20)
    prio_sparse = prio3_report_bytes(50, 20)
    # mobile round with n=128, using ceil(2n/3) sigs + 15-40 KB deltas + prio sparse + 512 B
    sigs = q128["bytes_ceil_2n3"]
    return {
        "n_participants": N_PARTICIPANTS,
        "G_catalogue": G_CATALOGUE,
        "G_priv": G_PRIV,
        "quorum_64": q64,
        "quorum_128": q128,
        "block_64": b64,
        "block_128": b128,
        "layer1_year_10rounds_n128_mb": round(
            (10 + 365 + 50) * b128["total_bytes"] / (1024 * 1024), 1
        ),
        "layer1_year_20rounds_n128_mb": round(
            (20 + 365 + 50) * b128["total_bytes"] / (1024 * 1024), 1
        ),
        "prio3_full_G_priv_20bit": prio,
        "prio3_sparse_50_20bit": prio_sparse,
        "mobile_round_n128_if_prio_were_75kb": {
            "sigs_kib": q128["kib_ceil_2n3"],
            "deltas_kib": "15-40",
            "prio_claimed_kib": 75,
            "merkle_b": 512,
            "low_kib": round(q128["kib_ceil_2n3"] + 15 + 75 + 0.5, 1),
            "high_kib": round(q128["kib_ceil_2n3"] + 40 + 75 + 0.5, 1),
        },
        "leaf_archive_10rounds_raw_gb": round(10 * 40_000 * 5_200 / 1e9, 3),
        "leaf_archive_10rounds_zstd_gb": round(10 * 60e6 / 1e9, 3),
    }


def main():
    out = {
        "R2_03_prio3_sizes": prio3_sizes(),
        "R2_11_shapley_folkman": shapley_folkman_sweep(),
        "R2_18_pequod_subsets": pequod_csv_subsets(),
        "R2_19_architecture_sensitivity": architecture_sensitivity(),
        "R2_20_committee": committee(),
        "R2_21_derived": derived_figures(),
    }
    dest = os.path.join(HERE, "r2_verification_results.json")
    with open(dest, "w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))
    print(f"\nWrote {dest}", file=sys.stderr)


if __name__ == "__main__":
    main()
