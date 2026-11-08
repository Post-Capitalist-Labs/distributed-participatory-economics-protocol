# Initial Editorial Audit

**Manuscript:** `book/dpep_book.tex` (3,159 lines; LaTeX), commit `c578ba8`, examined on branch `editorial`. **No manuscript changes have been made.**
**Built PDF:** 149 pages (6.5 × 9.5 in). No undefined references; `check_book.py` passes.
**Date:** 7 November 2026.

**Method.** I read the preamble, the front matter, the bibliography and Chapter 2 in full, and sampled every other chapter. I then ran automated surveys of the body text with maths, code, TikZ and comments stripped, and cross-checked footnote sources against the bibliography. The quotations were checked against the repository's source notes and, where reachable, against the online sources. Line numbers (L…) refer to `book/dpep_book.tex` at `c578ba8`.

**Scope limits** (repository rules): technical, cryptographic and economic claims were **not** re-verified. Mathematics, code, identifiers and every number are protected.

**Classes:**
- **C** (Critical): citations, quotations, permissions and legal matters, internal inconsistency.
- **M** (Major): affects readiness for production.
- **m** (Minor): mechanical.
- **D** (Editorial decision): the author's call.

---

## 1. Current structure

| Part | Content | Notes |
|---|---|---|
| Cover (PDF p. 1) | TikZ full-bleed cover: title, subtitle, author, "three audiences" badges, imprint footer | Not part of a submission manuscript (M-1) |
| Imprint page (p. 2) | "Post-Capitalist Labs Imprint · Open-Source Research Monograph Series"; title block; "About Post-Capitalist Labs" (mission, vision, approach, URLs) | Promotional; uses "we" (D-5) |
| Copyright and publication details (p. 3) | Metadata, version, status, **CC BY-SA 4.0 licence**, "Cite as", source-access tiers | Licence is a legal question for any publisher (C-6) |
| Reader's guide (p. 4) | "How to Read This Book Across Disciplines": three reading paths | Hard-coded chapter and section numbers, all correct today (m-9) |
| Contents | `\tableofcontents`, depth 2 | PDF bookmarks show raw `` `` '' `` (m-10) |
| List of Abbreviations and Mathematical Notation | Three uncaptioned longtables | Says "Chapters 1--10"; the book has 12 chapters and an appendix (m-8) |
| Chapters 1–12 | 1 Executive Summary; 2 Historical and Institutional Inspirations; 3 Source-Grounded Requirements; 4 Formal Economic Model; 5 Distributed Systems Architecture; 6 Weighted Architecture and Stack Comparison; 7 Post-Quantum Cryptography, Membership and Privacy; 8 Accountable AI; 9 Experimental Programme; 10 Open Questions; 11 Practical Adoption; 12 Critical Examination | Chapters 10 and 12 have no numbered sections. Chapter 1 is titled as a report's "Executive Summary" (D-6). 11 chapters carry epigraphs; Chapter 12 has none. |
| Appendix A | Scientific Claims Register (longtable) | |
| Bibliography | "Comprehensive Source Bibliography": 92 numbered entries in author–date form, grouped by topic | C-4, M-3 |
| Closing panel | Imprint banner with GitHub URLs | Promotional (P-5) |

**Apparatus:**
- 97 headings (12 chapters, 50 sections, 34 subsections, plus starred headings).
- 152 notes: 133 `\footnote` and 19 `\footnotemark`/`\footnotetext` pairs, numbered by chapter.
- 41 numbered tables, 10 numbered figures (all TikZ), 3 uncaptioned abbreviation tables.
- 11 epigraphs and 3 block quotations.
- Definitions, design principles, invariants and algorithm listings.
- No preface, acknowledgements, dedication, list of figures, list of tables, glossary (the abbreviation list partly serves) or index.

---

## 2. Applicable requirements (summary; detail in `STYLE_GUIDE.md`)

- **Until the publisher question is answered:** CMOS 18 with British -ise spelling, and the manuscript's own consistent conventions.
- **Press-level requirements that will apply to any submission** (University of Chicago Press guidelines, and Bloomsbury 2015 where it agrees):
  - a complete manuscript, with title page, contents and full text;
  - one documentation system;
  - double-numbered tables and figures, with matching callouts;
  - art supplied as separate, final, legible files;
  - alt text for every image;
  - documentation backing every credit line;
  - the author clears permissions;
  - an index, prepared by the author or at the author's cost (Bloomsbury 2015).
- **Format:** Word is preferred by both presses. LaTeX is accepted by the University of Chicago Press after checking with the editor. Bloomsbury's position is unknown (P-1).

---

## 3. Findings

### Critical

| ID | Location | Finding | Proposed action |
|---|---|---|---|
| **C-1** | Epigraph, Ch. 1 (L560) | **Quotation spelling altered.** The book prints "A decentralised, social, iterative, communication process". The source (*Looking Forward*, Ch. 6, ZNetwork edition) reads "decentralized", as confirmed by a search-engine extract on 7 November 2026. The quotation has been made British. | Restore "decentralized". Check every quotation from an American source the same way (Q-1). |
| **C-2** | Epigraphs, Ch. 8 (L2478) and Ch. 9 (L2543) | Same risk. "computer programmes" (*Looking Forward*, US edition) and "actors' behaviours" (*PEPE*, Princeton) are probably "programs" and "behaviors" in the originals. ZNetwork blocked automated access, so these could not be checked. | Author checks against print or online copies and restores the source spelling (Q-1). |
| **C-3** | Block quotation, §1.2 (L580–581) | **Quotation text disagrees with the record.** The book's interpolation reads "[i.e., command planning]". `research/SOURCE_AUDIT.md` §2 records the verified text as "[i.e., central planning]". The quotation is from Nove (1983), via *PEPE*. | Author confirms which wording appears in the source and whether the bracket belongs to Albert and Hahnel or was added in this book (Q-2). |
| **C-4** | Epigraph, Ch. 3 (L980) | **Attribution.** The epigraph ("Until now, however, descriptions of alternatives have been unconvincing. Here Michael Albert and Robin Hahnel support …") is publisher's blurb from the front flap or JSTOR abstract, yet it is attributed to Albert and Hahnel as authors. Its wording refers to them in the third person. | Re-attribute it ("Princeton University Press, jacket copy for …") or replace the epigraph (Q-3). |
| **C-5** | Epigraph, Ch. 9 (L2543) | Spliced quotation. One epigraph joins text from p. 108 and p. 129 with an ellipsis, across 21 pages. | Split it into two quotations or cite "pp. 108, 129" with the splice made explicit. Author to decide (Q-4). |
| **C-6** | Copyright page (L340ff.) | **Licence and prior publication.** The text and figures are released under CC BY-SA 4.0 and published openly on GitHub. A commercial publisher's standard contract takes exclusive rights. A ShareAlike licence already granted cannot be withdrawn for existing copies. Any quoted material must also be compatible with an openly licensed work, which the notice partly addresses ("Quoted material remains under its owners' copyright"). | Raise with the commissioning editor before submission: open-access edition, licence terms, and the status of the public repository (P-6). Not an editing matter. |
| **C-7** | Epigraphs and long quotations (see `PERMISSIONS_LOG.md`) | **Permissions not cleared.** 11 epigraphs, nine of them from two Albert and Hahnel books, plus three block quotations of 59–84 words, are reproduced without recorded permission. Many publishers require permission for epigraphs whatever their length. | Author requests permissions or confirms fair dealing with the publisher. The log gives the status of each item. |
| **C-8** | Notes vs. bibliography | **Sources cited in notes but missing from the bibliography** (13 found automatically): Bookchin, "Introductory Essay" (L768, in Dolgoff); Souchy, "Collectivizations in Catalonia" (L777, in Dolgoff); Subcomandante Insurgente Moisés (L824); Radio Dabanga (L851); McGranaghan (L1483); Zawirski (L1725); WICG (L1794); Chromium (L1794); Cosmos SDK documentation (L2102); Apple (L2426); Eckstein (L2485). | Add to the bibliography or justify leaving them out (web sources, chapters inside a collected volume). To be completed in `CITATION_AUDIT.md` (Phase 5). |
| **C-9** | Bibliography | **Entries recorded as not confirmed or only partly confirmed** in `research/SOURCE_AUDIT.md`. Not confirmed: Hahnel 2022; Sandström 2023; PEP 2023; Heal 1973; Leval 1971; Mintz 2013; BLAKE3 spec; FIPS 203/204/205; Buchman et al. 2018; Kornai 1980; Corrigan-Gibbs and Boneh 2017; Crites and Stewart 2025. Partly confirmed: Sandström 2025 (Crossref dates it 2026), Hurwicz 1973, Hayek 1945, Devine 1988, Leval 1975, Peirats, Marx 1871, Freeman 1972, Casanova 2005 (Crossref 2004). | Verify the metadata in Phase 5. Uncertain corrections go to the author. |

### Major

| ID | Location | Finding | Proposed action |
|---|---|---|---|
| **M-1** | Front matter (L190–368) | **Not in manuscript form.** The full-bleed cover, the "About Post-Capitalist Labs" panel, the audience badges and the closing imprint banner are design elements. Missing: a plain title page and a half title (Bloomsbury 2015 prelims order: half title, title, imprint, dedication, contents, illustrations, acknowledgements, foreword, preface). | Propose a plain manuscript title page. Keep the cover and branding out of the submission build (a LaTeX switch, so the public draft is unaffected). Needs approval (P-5). |
| **M-2** | Whole book | **Blended documentation system:** full footnote citations plus 75 author–date citations plus an author–date reference list. | Choose a system (P-3), then convert in Phase 5. |
| **M-3** | Bibliography (L3047–3144) | **Not in CMOS form.** Numbered labels; grouped by topic, not alphabetised; "(Year)" placed after the name in bold; page counts and ISBNs included; notes on source access and preservation inside entries ("Full text analyzed via ZNetwork", "Print TOC/pagination scan preserved at research/sources/…"). US-style dates in two entries (L3059, L3117). Two entries without dates (Ounsworth et al.; Peirats). Title: "Comprehensive Source Bibliography". | Restyle once P-3 is decided. Move the access notes to a "Note on Sources" or to `research/SOURCE_AUDIT.md` (P-4). |
| **M-4** | Figures | **Art production.** All 10 figures are TikZ, set at `\tiny` and `\scriptsize` (about 5–7 pt at this trim size). Several captions rely on colour, such as Figure 5.2 (L1563): "Teal steps carry private household data …; the dashed crimson step …". | Ask whether the interior will be in colour. Export each figure as a separate vector PDF and supply it with the submission. Make the captions work in greyscale (by pattern or label, not colour alone). Raise the minimum font size. All of this is production work and needs approval. |
| **M-5** | Figures | **No alt text or long descriptions** for any of the 10 figures. The University of Chicago Press requires alt text of 150 characters or fewer. Accessibility law (European Accessibility Act, June 2025) affects e-book editions. | Draft alt text and long descriptions in Phase 5 for author review. |
| **M-6** | Running text | **Bold used for emphasis about 980 times; colour boxes** (`\audiencebox`, coloured "Methodological note" blocks). The University of Chicago Press says only italics survive processing. CMOS advises against bold for emphasis. | Remove bold from running prose, but keep it in table column heads and run-in labels such as "**Lesson carried forward.**". Defined terms at first use go to italics. **Approval needed**, because bold is part of how the author signals key claims (D-1). |
| **M-7** | Captions (45) | Inconsistent capitalisation of captions (headline style vs. sentence style, about half each); some captions are several sentences long. | Sentence style throughout (STYLE_GUIDE §7). No wording changes. |
| **M-8** | Front matter, copyright page | **Source-access tiers** printed on the copyright page (L345). They are useful but unusual there. | Move them to a "Note on Sources" (P-4). |
| **M-9** | Missing components | No acknowledgements, preface, list of figures or list of tables. No index or index plan. | Author supplies acknowledgements (not to be drafted for them). The lists can be generated (`\listoffigures`, `\listoftables`). An index term list is offered as Phase 5 work. |
| **M-10** | Notes | 19 `\footnotemark`/`\footnotetext` pairs inside tables and epigraphs, with manual counter adjustments (`\addtocounter{footnote}{-1}`). These are fragile when content moves and will not survive conversion to Word. | Leave as they are in LaTeX. Flag them for production. |

### Minor (mechanical; will be fixed in Phase 4 after approval)

| ID | Finding | Count and location |
|---|---|---|
| m-1 | American spellings in the author's own prose (quotations, titles and proper names excluded) | 31; Appendix A |
| m-2 | US-style dates in the author's prose | 6 in §2.3 Paris Commune (L719 heading, L734–742); 2 in the bibliography (L3059, L3117) |
| m-3 | Dash style mixed: spaced em dash (15), unspaced em dash (18) | Throughout (spaced dashes inside quotations are left as they are) |
| m-4 | Serial comma mixed (about 121 with, 79 without) | Throughout |
| m-5 | Comma after *e.g.* and *i.e.* inconsistent | 9 and 3 instances |
| m-6 | "toward" (2) vs. "towards" (4) | L1004 |
| m-7 | "vs." in running prose and captions | 14 (keep in tables) |
| m-8 | Abbreviations list says "Chapters 1--10" | L379 |
| m-9 | Reader's guide hard-codes numbers ("Section 4.4", "Chapter 4 (Section 4.5 …)"). All correct at present; label wording differs slightly ("6-Role Mobile Taxonomy" vs. the heading "Node Role Taxonomy"). | L357–366; replace with `\ref` |
| m-10 | PDF bookmarks show raw LaTeX quotation marks (`` ``No Third Way'' ``) | Heading of §1.2; fix with `\texorpdfstring` |
| m-11 | Access-date phrasing: "(checked November 2026)" vs. "(checked 7 November 2026)" | 16; keep both forms, as the day is not always known |
| m-12 | Punctuation outside closing quotation marks (5) vs. inside (76) | L1664, L1798, L2360, L2379, L2855 (pending P-2) |

### Editorial decisions (the author's call)

| ID | Question |
|---|---|
| D-1 | Bold for emphasis (M-6): remove, reduce, or keep? |
| D-2 | Subtitle: "A Rigorous, Source-Grounded Feasibility Study and Post-Quantum Technical Architecture for …". "Rigorous" is self-description, which reviewers and publishers often ask authors to drop, and the subtitle runs to 25 words. |
| D-3 | Several chapter titles are long and in the style of a report ("Six-Discipline Critical Examination and Remaining Weaknesses"; "Three-Phase Experimental Programme, Kill Gates, and Benchmarks"). Keep, or shorten? Titles are not changed without approval. |
| D-4 | Section headings that state a position ("Why We Reject a Global Blockchain") use "we", while the book has a single author. |
| D-5 | Authorial voice: "we" or "our" appears 23 times, mostly in the front matter and Chapter 1, and "this book" or "this monograph" 19 times. Keep "we" (as the authorial plural or as Post-Capitalist Labs), or use "I"? |
| D-6 | Chapter 1 as "Executive Summary" (with "Five Key Decisions" and budget tables) versus a scholarly "Introduction". A monograph publisher may expect an Introduction. The content would be kept either way. |
| D-7 | The Reader's guide's audience boxes and the cover's "Designed for three interdisciplinary audiences": keep as a preface-style "How to Read This Book", or drop? |
| D-8 | Notes on verification inside notes ("cited at bibliographic level" 12×; "Neither book was read in full…"; "read in full"). These are honest but unusual. Keep them in the notes (recommended), or collect them in a "Note on Sources"? |

---

## 4. Cross-references

- 103 labels and 76 `\ref` targets. No missing targets and no duplicate labels (`check_book.py` [1]).
- Unreferenced labels are harmless.
- Hard-coded references: m-8 and m-9. No other "Section N.N" strings in the body.
- The external reference "PEPE Chapter 5 (pp. 73–106)" (L408) is to a source, not this book.
- "Table above" or "below" phrasing: none found.

---

## 5. Proposed correction plan (once approved)

**Phase 4 (mechanical; chapter by chapter, rebuild and run checks after each):**
1. Spelling (m-1, m-6).
2. Dates (m-2).
3. Dashes (m-3).
4. Serial comma (m-4).
5. *e.g.* and *i.e.* (m-5).
6. "vs." in prose (m-7).
7. Hard-coded references (m-8, m-9).
8. Bookmarks (m-10).
9. Caption case (M-7).

Each change is logged in `editorial/CHANGELOG.md`. Quotations, titles, code and numbers are excluded by rule.

**Phase 5 (apparatus):**
1. The citation system as decided (M-2, M-3).
2. Missing and unverified bibliography entries (C-8, C-9) → `CITATION_AUDIT.md`.
3. Quotation checks (C-1 to C-5).
4. Alt text (M-5).
5. Index term list (M-9).

**Phase 6:** substantive queries only, with no silent rewriting.

**Phase 7:**
1. Diff against `c578ba8`.
2. Full rebuild.
3. `FINAL_QA_REPORT.md`.

**Not proposed:** reorganising chapters, changing the argument or terminology, or touching protected technical content.

---

## Appendix A. American spellings in the author's own prose (m-1)

These are in running text, tables, notes or the bibliography's descriptive remarks. Quotations, titles of works, proper names, code and TikZ keys are excluded.

| Line | Word | Line | Word |
|---|---|---|---|
| L323 | Analyzing | L912 | neighborhood |
| L328 | Organization | L920 | Equalization |
| L357 | Organizers | L987 | analyzed (×2) |
| L379 | labor | L988 | formalizations |
| L408 | analyzed | L1000 | equalization |
| L429 | color | L1004 | toward (×2) |
| L548 | Normalized | L1046 | colors |
| L561 | authorized | L1483 | optimize |
| L624 | localized | L2486 | color |
| L641 | color | L2706 | Cartelization |
| L705 | analyzed | L3052 | analyzed |
| L710 | favoring | L3053 | analyzed |
| L740 | realized, socializing | L3055 | analyzed |
| L768 | specialized | | |
| L773 | Reorganization (heading) | | |
| L776 | standardize | | |
| L898 | synthesizes, analyzed | | |

**Kept as they are:**
- L526 "User Controlled Authorization Network" (a proper name, UCAN);
- L687 Leval epigraph (quotation);
- L1422 "computerized" (quotation);
- all titles (*Decolonizing*, "Decentralized Planning", "Optimization", "Characterize", "Collectivizations", "Systematizing", "Centralization", "Self-Stabilizing").
