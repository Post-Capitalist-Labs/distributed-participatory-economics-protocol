# Editorial Style Guide: *Distributed Participatory Economics Protocol*

**Status:** **approved with changes by the author, 7 November 2026.** The decisions immediately below override anything later in this guide.
**Prepared:** 7 November 2026, on branch `editorial`, from `book/dpep_book.tex` at commit `c578ba8`.
**Scope:** copyediting and preparing the manuscript for publication. This is not a rewrite.

## Author decisions of 7 November 2026 (these override §§1–9 where they conflict)

1. **Self-published.** There is no contract and no publisher, so Bloomsbury rules do not apply. **CMOS 18 governs**, under the repository rules (protected maths, code, identifiers and numbers; SI units).
2. **US spelling throughout:**
   - -ize spellings: *organize, optimization*;
   - *labor, behavior, neighborhood, center, defense, license, fulfillment, judgment, modeling, toward, program*.
   - This **replaces §3**.
   - Exceptions, never changed: quotations (they keep the spelling of their source), titles of published works, proper names (for example *Regional Defence Council of Aragon* as the title of a cited article), identifiers and code.
3. **CMOS punctuation now:**
   - double quotation marks, with single marks inside;
   - commas and periods inside closing quotation marks;
   - the serial comma;
   - unspaced em dashes;
   - en dashes for ranges;
   - a comma after *e.g.* and *i.e.*
4. **Dates:** month day, year ("March 18, 1871"), with a comma after the year when the sentence continues. This is the US form, chosen to match US spelling. CMOS also permits day–month–year; the author can reverse this choice.
5. **Block quotations and epigraphs:** CMOS treatment, with no enclosing quotation marks. Block quotations are set in roman type. Epigraphs keep their italic design.
6. **Citations:** author–date (STYLE_GUIDE §6, Option A). The reference list is alphabetized, unnumbered and titled "References". Footnotes are kept for discussion and for remarks on how a source was accessed.
7. **Quotations:**
   - restore the source spelling in the Ch. 1, Ch. 8 and Ch. 9 epigraphs;
   - Nove: keep the quotation as it is. The bracketed glosses were introduced by Albert and Hahnel to sharpen it.
8. **Branding and bold emphasis:** not changed in this pass.

---

## 1. Governing hierarchy and what is in force now

| Rank | Authority | Status |
|---|---|---|
| 1 | Instructions from a commissioning editor or contract | **None known.** Question P-1 in `AUTHOR_QUERIES.md` asks whether there is a contract or commissioning editor, and whether Bloomsbury accepts LaTeX. |
| 2 | Bloomsbury Academic house style | **Not applied yet** (repository rule). The only house-style text I could read is a 2015 copy that cites CMOS 15 and asks for submission on CD (see §8). It is evidence of Bloomsbury's British conventions, not a current rule. |
| 3 | *Chicago Manual of Style*, 18th ed. (2024) | **In force**, with British spelling. I had no subscription access to CMOS Online. Where a rule below cites CMOS, it reflects the edition's well-known provisions, and the paragraph number is given only where I am confident of it. Anything I could not check is marked *(unverified)*. |
| 4 | Scholarly conventions of the discipline | Political economy and history, with technical sections in cryptography and distributed systems. |
| 5 | The manuscript's own consistent and defensible conventions | Kept where they don't conflict with ranks 1–3. |

**Repository rules that override everything above** (from the author's instructions):

- The manuscript stays in LaTeX.
- Mathematics, code, schemas, and the names of standards, algorithms and software are protected. They may be queried but not edited.
- Every number and unit is protected. SI units and 1 kB = 1,000 B are kept, and numerals are used with units and in technical contexts.
- Technical, cryptographic and economic claims are not re-verified.
- Access dates ("checked …") are kept.

---

## 2. Decisions that depend on the publisher

These rules differ between CMOS (US) and British house styles, Bloomsbury's 2015 guide among them. The interim choice follows the manuscript's existing majority practice wherever that agrees with CMOS. Each item is also listed in `AUTHOR_QUERIES.md`, section P.

| Item | Manuscript now | CMOS 18 | Bloomsbury 2015 (British) | **Interim proposal** |
|---|---|---|---|---|
| Quotation marks | Double, with single inside (166 / 6) | Double, single inside | Single, double inside | **Keep double.** If Bloomsbury requires single, the swap is mechanical in LaTeX. |
| Comma and full stop at a closing quotation mark | Inside (76), outside (5) | Inside (US style) | Logical (outside unless part of the quotation) | **Defer.** British spelling with US punctuation is a hybrid. I recommend British logical punctuation if the book goes to a UK publisher. Nothing changes until P-1 is answered. |
| Serial comma | Mixed (≈121 with, ≈79 without) | Required | Omitted | **Apply the serial comma** (CMOS, and the majority use) unless the publisher says otherwise. |
| Parenthetical dash | Mixed: unspaced em dash (18), spaced em dash (15) | Unspaced em dash | Spaced en dash | **Unspaced em dash (`---`)** for now. Switch everything to spaced en dash if the publisher is British. |
| Dates | "7 November 2026" (42); "March 18, 1871" (8) | Either style, used consistently | "1 May 1975" | **Day–month–year everywhere**: 8 instances to fix, listed in the audit. |
| Percentages | `%` (85); "per cent" (0) | Numerals with % in scientific and technical contexts | "per cent" in text, % in tables | **Keep %** (technical book; protected-number rule). |
| *e.g.*, *i.e.* | Comma after them in 4 of 9 and 2 of 3 instances | Comma after | No comma | **Comma after**, roman type, inside parentheses where possible. |
| Notes and citation system | Blended: full footnote citations plus 53 in-text author–date references and an author–date reference list | One system, not a blend | Harvard or short-title, not both | **Author decision P-3** (see §6). |

---

## 3. Spelling and vocabulary

- **British spelling with -ise** (*organise, standardise, optimisation*). This is already the manuscript's dominant form, with about 120 -ise forms against about 45 -ize forms. Every -ize, -yze and American -or/-er form in the author's own prose will be made British, apart from the exceptions below. The locations are in `INITIAL_AUDIT.md`, Appendix A.
- **Exceptions, which are never changed:**
  - direct quotations and epigraphs;
  - titles of published works (*Decolonizing Research*, "On Informationally Decentralized Systems");
  - proper names;
  - identifiers and code (`catalog`, TikZ `align=center`, `\color`).
- **Specific words:**

  | Use | Not | Note |
  |---|---|---|
  | labour | labor | |
  | behaviour | behavior | |
  | neighbourhood | neighborhood | |
  | modelling | modeling | |
  | centre | center | |
  | colour | color | |
  | analyse | analyze | |
  | defence | defense | |
  | licence (noun), license (verb) | | |
  | towards | toward | |
  | fulfilment | fulfillment | |
  | judgement | judgment | |
  | programme (plan, schedule) | | |
  | program (computer software) | | British usage keeps "program" for software. |

- **Quotations keep their source's spelling**, as CMOS requires. American spellings inside quotations from American editions are correct and must not be made British. Spelling that an earlier pass made British inside a quotation must be restored after checking against the source (Critical query Q-1).

---

## 4. Punctuation and typography (LaTeX forms)

| Element | Rule | LaTeX |
|---|---|---|
| Em dash | Unspaced (interim; see §2) | `word---word` |
| En dash | Number and date ranges, and joint names (Arrow–Hurwicz) | `1917--1921`, `pp.~84--87` |
| Hyphen | Compounds only; never in a range | |
| Ellipsis | Three spaced dots, by LaTeX macro. No ellipsis at the start or end of a quotation unless the sense needs it. Square brackets only if the publisher requires them for omissions. | `\dots` |
| Interpolation in a quotation | Square brackets | `[i.e., markets]` |
| Apostrophe and possessive | *Marx's*, *Hahnel's*, *Walras's* in the author's prose (CMOS 7.17 *(unverified number)*). A title or quotation keeps its own form ("Walras' Identity"). | |
| Non-breaking space | Before references, page numbers, units and initials | `Section~\ref{}`, `p.~11`, `5~kB`, `C.~B.\ McGuire` |
| Italics | Titles of books and journals; foreign words not yet naturalised in English (*arrondissements*, *grama sabhas*); terms at their first, defining use. **Not** for emphasis in running prose except sparingly. | `\emph{}` |
| Bold | Headings and table column heads only. Bold used for emphasis in running prose (about 980 instances) is a production issue (see `INITIAL_AUDIT.md`, M-6) and is not removed without approval. | |
| Small capitals and colour | Design only. They do not carry meaning in the text, and a publisher's typesetter will strip them. | |
| Foreign names and institutions | Roman type (CNT, *Comisión de Vigilancia* italic only as a foreign phrase on first use) | |
| Abbreviations | Defined at first use in each chapter where the reader needs it. Listed in the List of Abbreviations. No full stops in capital-letter abbreviations (UK, CNT, NIST). | |
| *vs.* | "versus" in running prose; "vs." allowed in tables and captions | |

---

## 5. Numbers, dates and units

- **Protected.** No number, unit or table value is changed. Script-generated values are untouchable.
- **Prose:** in non-technical contexts, whole numbers from one to one hundred are spelled out (CMOS's general rule). The technical exception applies to quantities with units, statistics, money, percentages, version numbers and all technical material, which use numerals. In the historical chapters the existing mix (for example "72 days", "five federations") is left alone unless a single sentence is inconsistent. Then only that sentence is queried.
- **Thousands:** comma separator (`1,000`; in maths mode `1{,}000`). This is existing practice and is kept.
- **Dates:** day month year ("18 March 1871"); decades "1930s"; centuries spelled out ("fourth century BCE"); BCE/CE as now.
- **Ranges:** en dash, with numbers in full: `1917--1921`, `pp.~207--234`. CMOS's elision rules would allow "207–34", but full numbers are clearer for a technical readership and are the manuscript's existing practice.
- **Currency:** `\$40k--\$95k` style is kept in technical and budget passages (protected).

---

## 6. Citations, notes and bibliography

**What the manuscript does now:**

- (a) 152 footnotes, many giving full CMOS-style notes citations ("Karl Marx, *The Civil War in France* (London: …, 1871)"), with shortened forms later.
- (b) 53 narrative author–date citations in the text, such as "Albert and Hahnel (1991a, Ch.~5, pp.~84--87)", and 22 parenthetical ones, such as "(Casanova 2005)".
- (c) A numbered (`[1]`, `[2]` …) reference list in author–date form, grouped by topic rather than alphabetically, with ISBNs, page counts and notes on how each source was accessed.

**Problem.** That is a blend of the two systems. CMOS and the University of Chicago Press both say to use one. The Bloomsbury 2015 guide says the same.

**Proposal (author decision P-3), to be chosen before Phase 5:**

- **Option A, author–date (recommended).**
  - Keep the reference list, but alphabetise it, remove the numbering, and use CMOS author–date form ("Albert, Michael, and Robin Hahnel. 1991a. *Title*. Place: Publisher.").
  - Convert note citations to "(Author Year, page)" in the text.
  - Keep footnotes for discussion and for source-access remarks.
  - Why recommended: the reference list is already in this form, the in-text pattern already exists, and the technical and economics chapters suit author–date.
  - Cost: about 120 note citations to convert, and parentheses added to the running text.
- **Option B, notes and bibliography.**
  - Keep footnotes as the citation vehicle, with a full note at first citation in each chapter and shortened notes after.
  - Convert the 75 author–date citations into notes.
  - Reformat the bibliography in CMOS notes-and-bibliography form, alphabetised and unnumbered.
  - Why consider it: common in history and political theory.
  - Cost: about 75 conversions, and every bibliography entry restyled.
- **Either way:**
  - Use "chap." (CMOS) or keep "Ch." consistently. The manuscript uses "Ch." 172 times, and the interim rule is to keep it, since it is defensible and consistent.
  - DOIs as `https://doi.org/…` URLs (already done).
  - URLs keep the "checked [date]" access phrase (repository rule). Use one form: "(checked 7 November 2026)" where the day is known, otherwise "(checked November 2026)".
  - No *op. cit.*; *ibid.* only if the publisher wants it (it is not used now).
  - Every source cited in a note appears in the bibliography. About 13 do not; see the audit.
  - The bibliography is titled "Bibliography" (Option B) or "References" (Option A), not "Comprehensive Source Bibliography".
- **Source-access remarks** ("cited at bibliographic level", "not read in full", "Abstract consulted") are the author's deliberate statements of how each source was used. They are kept in the notes. Moving them out of the bibliography entries and into a short "Note on Sources" in the front matter is author decision P-4.

---

## 7. Headings, captions, tables and figures

- **Headings:** CMOS headline-style capitalisation, which is the existing majority practice. Lower case for articles, coordinating conjunctions and prepositions. The second element of a hyphenated compound is capitalised in headline style (CMOS 8.161 *(unverified number)*), which the manuscript already does ("Post-Quantum", "Two-Root"). No full stop after a heading.
- **Captions:** table and figure captions currently mix headline style ("Master Requirements Matrix Derived from …") with sentence style ("Enduring lessons and what they require of DPEP"). **Proposal: sentence style for every caption**, the more common form for long descriptive captions and already used by roughly half. Caption text is not otherwise changed.
- **Numbering:** double, by chapter (Table 2.1, Figure 5.3). This is already done, and it matches the press guidance.
- **Sources and notes:** table notes go below the table. Each table or figure drawn from another work ends with "Source:" or "Adapted from:" plus the citation. All 10 figures are TikZ drawings originated for this book. No source line is needed, but each is listed in the permissions log as "author-created".
- **Cross-references:** always by `\ref`, never "the table above". Hard-coded numbers ("Section 4.5", "Chapters 1--10") are replaced by `\ref` where that is unambiguous.

---

## 8. Sources consulted (7 November 2026)

| Source | What it gave | Notes |
|---|---|---|
| CMOS Online, "Manuscript Preparation" help page, <https://www.chicagomanualofstyle.org/help-tools/manuscript-prep.html> | Pointers only (art, tables, permissions), plus confirmation of the 18th edition (© 2024) | No rules on the page itself |
| University of Chicago Press, *Electronic Manuscript Guidelines*, <https://press.uchicago.edu/resource/emsguide.html> | Word preferred; LaTeX accepted after checking with the editor; one documentation system; double-numbered tables and figures; art in separate files; alt text for all images (≤150 characters); permissions documentation backing every credit line; title page, contents and full text required | Press guidance, not CMOS rules |
| Bloomsbury Academic, "A Guide to the Publishing Process", <https://www.bloomsbury.com/ca/discover/bloomsbury-academic/authors/a-guide-to-the-publishing-process/> | **Not retrieved**: the site refused automated access | Author or editor to supply |
| Bloomsbury Academic, *House Style Guidelines for Authors* (Yumpu copy dated 11 March 2015), <https://www.yumpu.com/en/document/view/48831998/bloomsbury-academic-house-style-guidelines-for-authors> | Single quotation marks; no serial comma; spaced dashes; "1 May 1975"; "per cent" in text; Harvard or short-title notes; notes numbered by chapter; tables numbered by chapter with "Source:" lines; author clears permissions; index by the author or at the author's cost | **Out of date**: refers to CMOS 15 and submission on CD. The guide itself says authors should get list-specific guidance from the commissioning editor. |
| Bloomsbury policy on generative AI | **Not found** in public sources (web search, 7 November 2026) | See `AUTHOR_QUERIES.md`, AI-1 |

---

## 9. Unresolved questions (also in `AUTHOR_QUERIES.md`)

- P-1: Is there a contract or commissioning editor? Will Bloomsbury accept LaTeX, and is there a current house style sheet?
- P-2: The interim choices in §2 (quotation marks, punctuation at quotation marks, serial comma, dashes).
- P-3: The citation system (Option A or B).
- P-4: Moving source-access remarks into a "Note on Sources".
- P-5: The "Post-Capitalist Labs Imprint · Working Draft Monograph" branding.
- P-6: The CC BY-SA 4.0 licence, given that the book is already published openly.
