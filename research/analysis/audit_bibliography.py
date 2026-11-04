#!/usr/bin/env python3
"""Audit every bibliography entry in book/dpep_book.tex against Crossref.

For each `\\item` in the back-matter bibliography (entries that bundle several
works with `;` are split on the bold author/year markers), the script:

  * resolves any DOI given in the entry via api.crossref.org/works/<doi>;
  * otherwise runs a Crossref bibliographic query and reports the best match.

It does not decide whether an entry is correct. It prints the evidence and
writes `bibliography_audit.json`; dispositions are recorded by hand in
`research/SOURCE_AUDIT.md`. Network access is required. Standard library only.

    python3 research/analysis/audit_bibliography.py [path/to/dpep_book.tex]
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
TEX = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "book", "dpep_book.tex")
UA = "dpep-source-audit/0.3 (research script; no contact address)"


def get(url: str) -> dict | None:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except Exception as exc:  # noqa: BLE001
            if attempt == 2:
                return {"error": str(exc)}
            time.sleep(2)
    return None


def clean(s: str) -> str:
    s = re.sub(r"\\(?:emph|textbf|texttt|url|path)\{([^}]*)\}", r"\1", s)
    s = re.sub(r"\\[a-zA-Z]+\s*", " ", s)
    s = s.replace("{", "").replace("}", "").replace("~", " ").replace("--", "-")
    return re.sub(r"\s+", " ", s).strip()


def entries(tex: str) -> list[str]:
    body = tex.split(r"\chapter{Comprehensive Source Bibliography}", 1)[1]
    body = body.split(r"\end{enumerate}", 1)[0]
    items = [i.strip() for i in body.split(r"\item")[1:]]
    out = []
    for it in items:
        # split bundled entries at "; \textbf{" boundaries
        parts = re.split(r";\s*(?=\\textbf\{)", it)
        out.extend(p.strip() for p in parts if p.strip())
    return out


def summarise(m: dict) -> dict:
    return {
        "doi": m.get("DOI"),
        "title": (m.get("title") or [""])[0],
        "authors": [f"{a.get('given', '')} {a.get('family', '')}".strip() for a in m.get("author", [])][:6],
        "container": (m.get("container-title") or [""])[0],
        "publisher": m.get("publisher"),
        "year": (m.get("issued", {}).get("date-parts") or [[None]])[0][0],
        "volume": m.get("volume"),
        "issue": m.get("issue"),
        "page": m.get("page"),
        "type": m.get("type"),
    }


def main() -> None:
    with open(TEX, encoding="utf-8") as f:
        tex = f.read()
    results = []
    for raw in entries(tex):
        text = clean(raw)
        head = re.match(r"\\textbf\{([^}]*)\}", raw)
        label = clean(head.group(1)) if head else text[:60]
        doi_m = re.search(r"doi\.org/([^\s}]+)", raw)
        rec = {"label": label, "entry": text[:300]}
        if doi_m:
            doi = doi_m.group(1).rstrip(".")
            data = get("https://api.crossref.org/works/" + urllib.parse.quote(doi))
            rec["method"] = "doi"
            rec["given_doi"] = doi
            rec["crossref"] = summarise(data["message"]) if data and "message" in data else data
        else:
            q = urllib.parse.quote(text[:250])
            data = get(f"https://api.crossref.org/works?rows=3&query.bibliographic={q}")
            rec["method"] = "query"
            items = (data or {}).get("message", {}).get("items", []) if data else []
            rec["crossref_top"] = [summarise(i) | {"score": i.get("score")} for i in items]
        results.append(rec)
        print(f"\n### {label}\n  entry: {text[:200]}")
        if rec["method"] == "doi":
            print(f"  DOI {rec['given_doi']} -> {rec['crossref']}")
        else:
            for c in rec["crossref_top"][:2]:
                print(f"  match({c['score']:.0f}): {c['authors'][:3]} | {c['title'][:90]} | "
                      f"{c['container'][:40]} {c['year']} {c['volume']}({c['issue']}) {c['page']} | {c['doi']}")
        time.sleep(0.4)
    dest = os.path.join(HERE, "bibliography_audit.json")
    with open(dest, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n{len(results)} works audited; wrote {dest}", file=sys.stderr)


if __name__ == "__main__":
    main()
