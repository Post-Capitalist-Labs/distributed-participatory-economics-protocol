#!/usr/bin/env python3
"""
Reproducible Audit of Upstream `msszczep/pequod-cljs` @ 8bd46b5c233f0e48c767ad6d5069b9437a67c38b
Verifies R-ECON-06 (concavity / toothache exponents across all dep1ex*.clj datasets)
and R-ECON-12 (CSV iteration counts at 5% [:green] and 3% [:blue] thresholds across Year 1 and Year 2).
"""
import glob
import json
import os
import re
import statistics

PEQUOD_ROOT = os.environ.get("PEQUOD_DIR", "/tmp/pequod_audit/pequod-cljs")
PEQUOD_DIR = os.path.join(PEQUOD_ROOT, "src/clj/pequod_cljs")
TABLES_TXT = os.path.join(PEQUOD_ROOT, "resources/tables.txt")
TABLES2_TXT = os.path.join(PEQUOD_ROOT, "resources/tables2.txt")

def audit_clj_datasets():
    clj_files = sorted(glob.glob(os.path.join(PEQUOD_DIR, "dep1ex*.clj")))
    wc_pattern = re.compile(
        r":c\s+([0-9.]+).*?:input-exponents\s+\[([0-9.\s]+)\].*?:nature-exponents\s+\[([0-9.\s]+)\].*?:labor-exponents\s+\[([0-9.\s]+)\].*?:du\s+([0-9.]+)",
        re.DOTALL,
    )
    # Faster line/record parser for WC maps
    total_wcs = 0
    base_concavity_min = 999.0
    base_concavity_max = -999.0
    toothache_concavity_min = 999.0
    toothache_concavity_max = -999.0
    toothache_violations = 0

    for path in clj_files:
        if os.path.getsize(path) < 1000:
            continue  # Git LFS pointer; not fetched
        text = open(path).read()
        # Extract each WC map in wcs vector
        wcs_pos = text.find("(def wcs")
        if wcs_pos == -1:
            continue
        wcs_text = text[wcs_pos:]
        for m in re.finditer(r"\{[^{}]*:input-exponents[^{}]*\}", wcs_text):
            rec = m.group(0)
            c_m = re.search(r":c\s+([0-9.eE+-]+)", rec)
            du_m = re.search(r":du\s+([0-9.eE+-]+)", rec)
            ie_m = re.search(r":input-exponents\s+\[([^\]]+)\]", rec)
            ne_m = re.search(r":nature-exponents\s+\[([^\]]+)\]", rec)
            le_m = re.search(r":labor-exponents\s+\[([^\]]+)\]", rec)
            if not (c_m and du_m and ie_m and ne_m and le_m):
                continue
            c = float(c_m.group(1))
            k = float(du_m.group(1))
            b_vals = [float(x) for x in (ie_m.group(1) + " " + ne_m.group(1) + " " + le_m.group(1)).split()]
            n_inputs = len(b_vals)
            sum_b = sum(b_vals)
            base_idx = sum_b + (c / k)
            tooth_idx = sum_b + 0.1 * n_inputs + (c / k)
            total_wcs += 1
            base_concavity_min = min(base_concavity_min, base_idx)
            base_concavity_max = max(base_concavity_max, base_idx)
            toothache_concavity_min = min(toothache_concavity_min, tooth_idx)
            toothache_concavity_max = max(toothache_concavity_max, tooth_idx)
            if tooth_idx >= 1.0:
                toothache_violations += 1

    return {
        "clj_dataset_files_count": len(clj_files),
        "total_wc_records_audited": total_wcs,
        "baseline_sum_b_plus_c_over_k_range": [round(base_concavity_min, 4), round(base_concavity_max, 4)],
        "toothache_sum_b_plus_c_over_k_range": [round(toothache_concavity_min, 4), round(toothache_concavity_max, 4)],
        "toothache_concavity_violations": toothache_violations,
        "toothache_violation_rate": round(toothache_violations / total_wcs, 6) if total_wcs else None,
    }

def audit_csv_files():
    csv_files = sorted(glob.glob(os.path.join(PEQUOD_DIR, "dep1ex*.csv")))
    # Exclude dep1ex100.csv if we also check standard 1..40 or 51..90
    y1_green = []
    y1_blue = []
    y2_green = []
    y2_blue = []
    naive_line_counts = []

    for path in csv_files:
        bn = os.path.basename(path)
        if bn == "dep1ex100.csv":
            continue
        with open(path) as f:
            lines = [line.split(",", 2)[:2] for line in f]
        naive_line_counts.append(len(lines))
        # Split into sections separated by ['exponent-sum', '']
        sections = []
        cur = []
        for row in lines[1:]:  # skip header
            if not row:
                continue
            if row[0] == "exponent-sum":
                sections.append(cur)
                cur = []
            else:
                cur.append((int(row[0]), row[1].strip()))
        if cur:
            sections.append(cur)
        if len(sections) >= 1 and sections[0]:
            g1 = [it for it, col in sections[0] if col in (":green", ":blue")]
            b1 = [it for it, col in sections[0] if col == ":blue"]
            if g1:
                y1_green.append(g1[0])
            if b1:
                y1_blue.append(b1[0])
        if len(sections) >= 2 and sections[1]:
            g2 = [it for it, col in sections[1] if col in (":green", ":blue")]
            b2 = [it for it, col in sections[1] if col == ":blue"]
            if g2:
                y2_green.append(g2[0])
            if b2:
                y2_blue.append(b2[0])

    # Also parse tables2.txt (which tracks dep2ex01..50 for toothaches / IRS experiments!)
    t2_y1_green = []
    t2_y2_green = []
    if os.path.exists(TABLES2_TXT):
        by_file = {}
        for line in open(TABLES2_TXT):
            line = line.strip()
            if not line:
                continue
            fname, rest = line.split(":", 1)
            it_str = rest.split()[0]
            by_file.setdefault(fname, []).append(int(it_str))
        for fname, its in sorted(by_file.items()):
            # First sequence is Year 1, second sequence (after drop in iteration number) is Year 2
            y1_first = its[0]
            y2_first = None
            for prev, curr in zip(its, its[1:]):
                if curr < prev:
                    y2_first = curr
                    break
            t2_y1_green.append(y1_first)
            if y2_first is not None:
                t2_y2_green.append(y2_first)

    return {
        "csv_files_audited_count": len(y1_blue),
        "naive_line_count_mean": round(statistics.mean(naive_line_counts), 2),
        "dep1ex_year1_first_green_5pct_mean": round(statistics.mean(y1_green), 3),
        "dep1ex_year1_first_green_5pct_range": [min(y1_green), max(y1_green)],
        "dep1ex_year1_first_blue_3pct_mean": round(statistics.mean(y1_blue), 3),
        "dep1ex_year1_first_blue_3pct_range": [min(y1_blue), max(y1_blue)],
        "dep1ex_year2_first_green_5pct_mean": round(statistics.mean(y2_green), 3),
        "dep1ex_year2_first_green_5pct_range": [min(y2_green), max(y2_green)],
        "dep1ex_year2_first_blue_3pct_mean": round(statistics.mean(y2_blue), 3),
        "dep1ex_year2_first_blue_3pct_range": [min(y2_blue), max(y2_blue)],
        "tables2_dep2ex_year1_first_green_mean": round(statistics.mean(t2_y1_green), 3) if t2_y1_green else None,
        "tables2_dep2ex_year2_first_green_mean": round(statistics.mean(t2_y2_green), 3) if t2_y2_green else None,
    }

if __name__ == "__main__":
    res = {
        "R_ECON_06_clj_audit": audit_clj_datasets(),
        "R_ECON_12_csv_audit": audit_csv_files(),
    }
    print(json.dumps(res, indent=2))
    with open("research/analysis/pequod_dataset_audit.json", "w") as f:
        json.dump(res, f, indent=2)
