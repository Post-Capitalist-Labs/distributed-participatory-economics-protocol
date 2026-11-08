# Editorial Change Record

**Branch:** `editorial`. Base commit: `c578ba8` (the recoverable original; compare with `git diff c578ba8 -- book/dpep_book.tex`).
**File:** `book/dpep_book.tex` unless stated otherwise. Line numbers (L…) are approximate, because earlier edits shift later lines.
**Authority:** the author's decisions of November 7, 2026 (`STYLE_GUIDE.md`, top section): CMOS 18; US spelling; CMOS punctuation; author–date citations.
**Never touched:**
- mathematics, code, schema fragments, TikZ path syntax;
- identifiers (labels such as `sec:fulfilment` keep their old spelling as keys);
- names of standards and software;
- numbers and table values;
- titles of published works.

**Approval:**
- "No" means the change carries out an approved rule.
- "Yes" means the change needs the author's sign-off: it touches a quotation, a heading's wording, or meaning.

---

## Phase 4: mechanical copyediting

### 4.1 US spelling (305 replacements, plus 2 by hand)

- **Method.** A script masked protected zones before replacing: maths, code, `\texttt`/`\path`/`\url`/`\label`/`\ref` arguments, TikZ options, quotations, epigraphs and titles of works. It then replaced British forms in the unprotected text only. I vetted the candidate list by hand, and excluded words that only look British (*exercise, premise, promise, enterprise, advise, revise, comprise, uprising, pairwise, franchised*).
- **Rule.** Author decision 2 (US spelling throughout). CMOS follows *Merriam-Webster*.
- **Approval:** No.

| Change | Count |
|---|---|
| labour → labor (including the author's translated names: "National Confederation of Labor", "Commission of Labor and Exchange") | 50 |
| neighbourhood/neighbour(s) → neighborhood/neighbor(s) | 37 |
| fulfilment → fulfillment | 20 |
| -ise/-isation → -ize/-ization (standardized, decentralized, organized, optimization, minimization and so on) | about 140 |
| centre → center; defence → defense; licence → license (noun) | 7; 4; 3 |
| programme → program (plan sense; "Experimental Program") | 12 |
| catalogue(s) → catalog(s) | 8 |
| judgement → judgment | 4 |
| behaviour → behavior (incl. misbehavior) | 4 |
| favour/favoured/favours → favor…; honours → honors | 3; 2 |
| towards → toward; downwards → downward (L765, by hand) | 3; 1 |
| modelled → modeled; labelled → labeled; practised → practiced; analysed → analyzed; sceptical → skeptical | 1 each |
| Tradeoff → Trade-off (L2517); Tradeoffs → trade-offs (caption, L1713) (*Merriam-Webster* hyphenates) | 2 |

- **Chapter titles affected:** Ch. 8 "…Mathematical Optimization…"; Ch. 9 "Three-Phase Experimental Program…"; §7.5 "Intra-Year Fulfillment…"; Ch. 2 subsection "Kerala's People's Campaign for Decentralized Planning".
- **Kept as they are:**
  - titles of works: *Towards a New Socialism*; "Reproductive Labour" (chapter title in Hahnel 2021); the Wikipedia article title "Regional Defence Council of Aragon"; "Decentralised" and others inside quoted titles;
  - the RFC title;
  - comments in the LaTeX source.

### 4.2 Quotations restored to their source spelling (author decision 7)

| Location | Original in the manuscript | Revised | Reason | Approval |
|---|---|---|---|---|
| Ch. 1 epigraph (L560) | "A decentralised, social, iterative…" | "A decentralized, social, iterative…" | Source reads "decentralized" (*Looking Forward*, ch. 6; confirmed November 7, 2026) | Approved by the author |
| Ch. 8 epigraph (L2478) | "the computer programmes are human products" | "the computer programs are human products" | American source; restored at the author's instruction (not verified online: ZNetwork blocked access) | Approved by the author |
| Ch. 9 epigraph (L2543) | "actors' behaviours" | "actors' behaviors" | American source (Princeton); as above | Approved by the author |
| §2.1 (L693) | ``decentralised governance'' | ``decentralized governance'' | The author's own scare-quoted term, not a quotation | No |

### 4.3 Dates (50 conversions)

- **Rule.** Author decision 4: month day, year, with a comma after the year when the sentence continues (CMOS 6.41).
- **Examples:**
  - "On 9 December 1956 the government" → "On December 9, 1956, the government";
  - "17--22 October 1917" → "October 17--22, 1917";
  - "(checked 7 November 2026)" → "(checked November 7, 2026)";
  - "19--20 December" → "December 19--20".
- **One reordering:** "the \textbf{30 January 2026 SDF--Damascus integration agreement}" → "the \textbf{SDF--Damascus integration agreement of January 30, 2026}" (§2.11). This avoids a date used as an adjective (CMOS advice). **Approval: Yes** (minor rewording).
- The six dates already in US form in §2.3 (Paris Commune) are unchanged. The §2.3 heading range "March 18 -- May 28, 1871" → "March 18--May 28, 1871" (see 4.4).

### 4.4 Dashes

- **Rule.** CMOS: unspaced em dash; unspaced en dash for ranges. **Approval:** No.

| Location | Before | After |
|---|---|---|
| L626, 1232, 1239, 1254, 1265, 1860, 1861, 2531 | `X --- Y` (spaced em dash) | `X---Y` |
| §2.2 heading (L702) | `508/7 -- 322 BCE` | `508/7--322 BCE` |
| §2.3 heading (L719) | `March 18 -- May 28, 1871` | `March 18--May 28, 1871` |
| Castoriadis quotation (L801) | `anything -- except` (spaced en dash) | `anything---except` (typographic regularization only, which CMOS permits in quotations) |
| L1870–1871 | `)---Python`, `)---Rust` | `\allowbreak` added after the dash to restore a line break |

- Table placeholders ("& --- &", "& -- &") are unchanged.

### 4.5 Punctuation at quotation marks (CMOS US style)

| Location | Before | After |
|---|---|---|
| L1664 | `` ``…new deployments''.} `` | `` ``…new deployments.''} `` |
| L1798 | `` ``something changed'', `` | `` ``something changed,'' `` |
| L2360 | `` ``clothing'', `` | `` ``clothing,'' `` |
| L2379 | `` ``Offline payments'', `` | `` ``Offline payments,'' `` |
| L2855 | `` ``Why Build on Circles?'', `` | `` ``Why Build on Circles?'' `` (no comma after a question mark) |

**Approval:** No.

### 4.6 *e.g.* and *i.e.* (6)

- `e.g.\ ` / `i.e.\ ` → `e.g., ` / `i.e., ` at L489, 518, 519, 532, 1571 and 2426.
- **Rule:** CMOS (comma after them).
- **Approval:** No.

### 4.7 Serial comma (145 insertions)

- **Method.** 277 candidate "A, B and C" patterns were reviewed one by one. The comma was inserted only in genuine lists of three or more.
- **Excluded:**
  - introductory phrases ("In 1936, workers and peasants");
  - compound items ("formal welfare and planning economics");
  - nested lists;
  - lists already serial;
  - titles of works ("Pluralism, Ecology and Planning").
- **Corrected:** 7 insertions that the script placed after the wrong conjunction were fixed by hand ("§§ 3, 7, and 9"; "Cairo, Alexandria, Suez, and many Delta towns"; "surveil, coerce, or shut down"; "in the stack, and, at present,"; "criteria 4, 11, and 12"; "(a), (d), and (f)"). One asyndetic list ("billions of users, ten or more years") was restored unchanged.
- **Also changed:** the heading "Client Platform, Distribution, and Notifications" (§5.5) and two captions ("…, current construction, and upgrade path…"; "…, consequences, and reasons…").
- **Approval:** No.

### 4.8 Cross-references

| Location | Before | After | Note |
|---|---|---|---|
| L588, L914 | `Section~2.5` | `Section~\ref{sec:hist-uprisings}` | **Corrects a broken reference.** §2.5 had been "Occupy" before the Chapter 2 reorder; Occupy is now in §2.10. |
| L1235 | `Section~4.4.3` | `Section~\ref{sec:convergence-limits}` (new label) | Same target |
| L2170 | `Section~7.3` | `Section~\ref{sec:membership}` | Same target |
| L2970 | `Section~4.2` | `Section~\ref{sec:primal-dual}` (new label) | Same target |
| Reader's guide (L357–366) | 11 hard-coded "Chapter N" / "Section 4.4" / "Section 4.5" | `\ref` to new labels `ch:exec` … `ch:critique`, `sec:pequod-audit`, `sec:cbor-schemas` | Same targets |
| L379 | "used across Chapters 1--10" | "used in this book" | The book has 12 chapters and an appendix |
| L470, 523, 535, 627, 993, 1486 | "Chapter 2/5/4/6/10/4" | `Chapter~\ref{…}` | Same targets |
| §1.2 heading | PDF bookmark showed raw `` `` '' `` | `\texorpdfstring` with typographic quotation marks | Bookmark only |

- **Not changed:** L2360 "what ``ephemeral shares'' means in Section~11.2". The phrase occurs nowhere else in the book, so the target is unknown (query X-1).
- **Approval:** No (targets are certain), except X-1.

### 4.9 Block quotations and epigraphs (CMOS treatment; author decision 5)

- The three `quote` environments (Nove L581, Bookchin L771, Brinton L938) are now set in roman type without enclosing quotation marks. Brinton's emphasized "*Meaningful action*" now prints in italic, as an emphasized phrase should, where before it was inverted to roman inside the italic block.
- `\chapterepigraph` no longer adds enclosing quotation marks. Single quotation marks inside three epigraphs became double ("experiments", "shadow" ×2).
- **Approval:** No.

### 4.10 Caption capitalization (12 captions to sentence style)

- **Changed:** Tables 1.1, 2.1, 2.2, 3.1, 5.4, 5.5, 6.2, 10.1, 11.1 and A.1; Figures 4.1 and 5.1.
- Proper nouns are kept: Paris Commune, DPEP, Distributed Participatory Economics Protocol, Architecture D, Raspberry Pis.
- **Wording changes:** Table 2.1 "Actually Implemented Institutions vs. Proposals \& Extrapolations" → "institutions actually implemented vs.\ proposals and extrapolations" (word order; "&" → "and"); "Tradeoffs" → "trade-offs". **Approval: Yes** (minor).

---

## Not changed in Phase 4 (by decision or rule)

- Bold emphasis and branding (author decision 8).
- "vs." in table labels, titles and technical comparisons (allowed by CMOS).
- `%` with numerals (technical exception).
- `$\sim$` for "approximately" (technical notation; protected).
- "Ch." in citations: decided in Phase 5 under author–date.

---

## Phase 5: scholarly apparatus

### 5.1 Citation system: author–date (author decision 6)

- **Approach.** Notes stay where they are, with their numbering and their remarks on how each source was accessed. The full citations inside them become CMOS author–date references: "Albert and Hahnel 1991a, chap.~4, 66--67"; "Marx 1871, sec.~III"; "Hansen 1991, chap.~9, 230--245". CMOS allows author–date citations in notes. Moving citation-only notes into the running text is a possible later step; it is not done here.
- **Scope:** 115 of the 152 notes were rewritten (Ch.~1: 16; Ch.~2: 42; Chs.~3--4: 28; Chs.~5--7: 15; Chs.~8--12 and App.~A: 14). The other 37 cite only repository scripts or web pages and are unchanged.
- **Locators:** "Ch." becomes "chap."; "pp." is dropped; "Sec." becomes "sec."; "Arrows" becomes "arrows".
- **Kept in the notes:** web documentation, software release pages, standards drafts and news items (C2SP, WICG, Chromium, MDN, RustCrypto, drand, Cosmos SDK, Apple, Ethereum specifications, IETF DAP, Janus, Quint, Valueflows and others, Circles, Radio Dabanga), each with its URL and "checked" date. CMOS permits citing such sources in the notes alone.
- **Wording changes in notes:** none beyond the citation forms. Every remark such as "cited at bibliographic level", "read in full" or "not read in full" is kept verbatim.
- **Approval:** No (carries out decision 6).

### 5.2 In-text citations

- Locators normalized: "(1991a, Ch.~5, pp.~84--87)" → "(1991a, chap.~5, 84--87)"; the same for 13 other citations (Albert 2003; Hahnel 2021; Leval 1975; Sandstr\"om 2020 and 2023; Szczepanczyk 2023).
- "(2020/2023)" → "(2020, 2023)".
- **O'Neill.** "O'Neill (2024)" and "(O'Neill 2024)" (5 instances) → "2024a", for "Pluralism, Ecology and Planning". The 2024 entry has been split into 2024a and 2024b (the response to Hahnel). **Approval: Yes**: I assigned 2024a on the evidence of the context; see query X-3.
- **Short titles:** the abbreviation list entries for PEPE, LF, DEP and PLAC now end "cited as Albert and Hahnel 1991a" (or 1991b, Hahnel 2021, Albert 2003). The short titles stay in the dense tables (query X-4).

### 5.3 Reference list (replaces "Comprehensive Source Bibliography")

- **Title and form:** "References". Alphabetized and unnumbered (hanging indent), in CMOS author–date form ("Surname, First. Year. *Title*. Place: Publisher. URL.").
- **Split:** combined entries became separate ones (Lessig 1999 and 2000; Mattsson 2022 and 2023; Boyd 2011, Deng 2017 and Hong 2016; Scarf 1960 and Sonnenschein 1973; Weitzman 1974 and 1980; Kornai 1980 and 1986; Seidman 1991 and 2002; Finley 1981 and Ste.~Croix 1981; Mansbridge 1980 and Dahl and Tufte 1973; Corrigan-Gibbs and Boneh 2017, Boneh et al. 2019 and Barnes et al. 2026; O'Neill 2024a and 2024b; NIST 2024a, b and c; Castoriadis 1972 and 1988).
- **Added** (cited in the notes, missing from the list): Bookchin 1974; Souchy 1974; Mois\'es 2023; Yin et al. 2019 (HotStuff).
- **Completed:** full author lists for Kleppmann et al. 2019 and Shapiro et al. 2011, taken from the existing notes. Peirats is dated 1974 (via Dolgoff).
- **Removed** (not CMOS elements): page counts ("132 pp.") and ISBNs, and the "DOI:" prefix (DOIs are given as URLs).
- **Kept:** every remark on how a source was accessed or preserved (query P-4 is still open).
- **Reprints:** dated in CMOS form: Castoriadis (1957) 1972; Lange and Taylor (1938) 1964. Mintz 2013 now reads "First published 1970; revised 1977."
- **Totals:** 92 numbered items became 112 entries.
- **Orphan:** Henry (1972) is listed but cited nowhere, in the current text or the base commit. It is kept and flagged (query X-2).
- **Approval:** No, except that the added entries use only metadata already in the notes.

### 5.4 Tooling

- **`research/analysis/check_book.py`:**
  - parses the new "References" list;
  - normalizes accented surnames before matching (G\'omez, Mois\'es);
  - adds `UNCITED_PENDING = {"Henry"}` until X-2 is decided.
- **Checks after each pass:**
  - full rebuild (147 pp, no undefined references, no overfull box above 10 pt);
  - `check_book.py` passes;
  - `verify_r3.py` reports `book_table_matches: true`.
