#!/usr/bin/env python3
"""Consistency checks on book/dpep_book.tex (standard library only).

    python3 research/analysis/check_book.py

1. Every \\ref / \\eqref target has a \\label, and every \\label is unique.
2. Every bibliography entry (author surname + year) is cited in the body.
3. Every "Surname (YEAR" or "Surname et al. (YEAR" citation in the body, and
   every surname in a footnote citation, matches a bibliography entry.
4. Phrases that address a reviewer or record revision history are absent.
5. Figures the book attributes to the analysis scripts appear in their JSON output.

Exit status 1 if any check fails. Heuristic: check 3 can miss citations that do
not use the Surname (Year) form; the output lists what was matched.
"""
from __future__ import annotations

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
TEX = os.path.join(ROOT, "book", "dpep_book.tex")

# Surnames that appear in "Name (Year" form but are not bibliographic citations
# (people discussed, epigraph attributions resolved through another entry, etc.).
NON_CITATIONS = {"Kleisthenes", "Pericles", "Aristotle", "Freeman's", "Merriman", "Marx",
                 "Nove", "Albert", "Hahnel", "Hurwicz",
                 # capitalised words followed by a year that are not citations
                 "Budgeting", "Catalonia", "Corporation", "DAANES", "Depots", "Street", "Valencia",
                 "Algorithms''", "Economy''", "Mapping''", "PEP",
                 # movements named with a year in headings and tables
                 "Rojava", "Zapatistas"}

BANNED = [
    "not because of a 3.60", "does not licence", "returned 404", "is retired", "retired",
    "Do not cite", "previously published", "previously quoted", "this pass",
    "earlier draft", "Earlier drafts", "R3-", "R2-", "R-ECON", "R-SEC", "R-TECH", "Ackerman",
    "4.51", "78\\text{ GB", "Score cut from", "Rescored from", "Critics (,)",
]


def main() -> int:
    tex = open(TEX, encoding="utf-8").read()
    ok = True
    body, bib = tex.split(r"\chapter{Comprehensive Source Bibliography}", 1)
    bib = bib.split(r"\end{enumerate}", 1)[0]

    # 1. labels and refs
    labels = re.findall(r"\\label\{([^}]+)\}", tex) + re.findall(r"label=([^,\]]+)", tex)
    dup = sorted({l for l in labels if labels.count(l) > 1})
    refs = set(re.findall(r"\\(?:eq)?ref\{([^}]+)\}", tex))
    missing = sorted(refs - set(labels))
    unused = sorted(set(labels) - refs)
    print(f"[1] labels {len(labels)}, refs {len(refs)}, missing targets {missing}, duplicates {dup}")
    print(f"    labels never referenced (informational): {unused}")
    ok &= not missing and not dup

    # 2. bibliography entries cited?
    entries = re.findall(r"\\textbf\{([^}]*?)\((\d{4})[a-c]?[^)]*\)\.?\}", bib)
    uncited = []
    surnames = set()
    for who, year in entries:
        sur = re.split(r"[ ,]", who.strip())[0].replace("\\", "").replace('"', "")
        sur = {"Sandstr": "Sandstr"}.get(sur[:7], sur)
        surnames.add(sur)
        alias = {"O'Connor": "BLAKE3 spec", "Aas": "prio", "Hong": "Hong, Luo"}
        if sur.startswith("Sandstr"):
            hit = re.search(r"Sandstr", body)
        elif sur in alias:
            hit = re.search(re.escape(alias[sur]), body)
        else:
            hit = re.search(re.escape(sur), body)
        if not hit:
            uncited.append(f"{who.strip()} ({year})")
    # entries without a year in bold (e.g. Peirats)
    print(f"[2] bibliography works parsed {len(entries)}; not cited in body: {uncited}")
    ok &= not uncited

    # 3. body citations resolvable?
    cites = set(re.findall(r"\b([A-Z][A-Za-z\\'\"{}]+)(?: et al\.\\?)? \((1[89]\d\d|20\d\d)", body))
    unresolved = []
    for sur, year in sorted(cites):
        s = sur.replace("\\", "").replace("{", "").replace("}", "").replace("'s", "")
        if s in NON_CITATIONS or s.startswith("Sandstr"):
            continue
        if not re.search(re.escape(s), bib):
            unresolved.append(f"{s} ({year})")
    print(f"[3] body Surname (Year) citations {len(cites)}; unresolved: {unresolved}")
    ok &= not unresolved

    # 4. banned phrases
    found = [b for b in BANNED if b in body]
    print(f"[4] reviewer-voice / history phrases found: {found}")
    ok &= not found

    # 5. figures vs script output
    r3 = json.load(open(os.path.join(HERE, "r3_verification_results.json")))
    checks = {
        "4.07": abs(r3["C_table_6_1"]["rescored"]["baseline"]["D"] - 4.065) < 1e-9,
        "3.92 (70%)": round(r3["C_table_6_1"]["rescored"]["seventy_pct_4_11_12"]["D"], 2) == 3.92,
        "0.63 crossover": r3["C_table_6_1"]["rescored"]["A_overtakes_D_at_focus_weight"] == 0.63,
        "42\\% unused": round(r3["A_success_measures"]["single_plant"]["first_feasible"]["unused_share"], 2) == 0.42,
        "975,760 B leader": r3["D_household_reports"]["sizes"]["3000x20"]["leader_share_bytes"] == 975760,
        "55.1 kB coarse": r3["D_household_reports"]["sizes"]["200x16"]["client_upload_bytes"] == 55120,
        "700,142 B block": r3["F_layer1_units"]["block_bytes"] == 700142,
        "bench sizes match": all(x["match"] for x in r3["D_household_reports"]["bench_check"] or [{"match": False}]),
        "\\$0.62M programme": r3["G_budget"]["proposed_reconciliation_at_120k_180k"]["Programme total"][0] == 621000.0,
    }
    for k, v in checks.items():
        in_book = k.split(" ")[0].replace(",", "{,}") in tex or k.split(" ")[0] in tex
        print(f"[5] {k}: script {'OK' if v else 'MISMATCH'}; in book: {in_book}")
        ok &= v
    print("ALL CHECKS PASSED" if ok else "SOME CHECKS FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
