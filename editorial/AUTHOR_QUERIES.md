# Author Queries

**Status:** open. Raised during Phases 1–3 (audit). Nothing in the manuscript has been changed.
**Line numbers (L…)** refer to `book/dpep_book.tex` at `c578ba8`.

**Query prefixes:**
- **P**: publisher and house style; answers needed before Phase 4.
- **Q**: quotations and attribution.
- **D**: editorial decisions (same numbering as `INITIAL_AUDIT.md`).
- **AI**: disclosure of AI use.

**Answer first:** P-1 to P-3, then the Critical quotation queries Q-1 to Q-4.

---

## P. Publisher and house style

### P-1. Publisher status *(blocking)*
1. **Location:** whole manuscript; `STYLE_GUIDE.md` §1.
2. **Issue:** Your instructions put Bloomsbury rules above CMOS, but say not to apply them until you confirm the contract position.
3. **Problem:** Bloomsbury's current house style could not be retrieved. Its site refuses automated access, and the only copy found is dated 2015, refers to CMOS 15 and asks for submission on CD. The University of Chicago Press accepts LaTeX only after consulting the editor. Bloomsbury's position on LaTeX is unknown.
4. **Questions:**
   - Is there a contract or a commissioning editor?
   - Which imprint or list is it?
   - Is there a current house-style sheet and an author guide?
   - Will Bloomsbury accept LaTeX with PDF, or do they require Word?
5. **Recommendation:** ask the commissioning editor for the current *Author Guidelines* and *House Style* PDFs, and for their policy on LaTeX and on AI. Until then I work to CMOS 18 with British spelling.

### P-2. Conventions that differ between CMOS and British house style
1. **Location:** throughout (`STYLE_GUIDE.md` §2).
2. **Issue:**
   - quotation marks (now double);
   - commas and full stops at a closing quotation mark (now mostly inside, US style);
   - the serial comma (now mixed);
   - dashes (now mixed spaced and unspaced em dashes).
3. **Problem:** the manuscript has British spelling with US punctuation. A British publisher will probably want single quotation marks, logical punctuation, no serial comma and spaced en dashes.
4. **Recommendation:** apply the CMOS forms now (double quotation marks, serial comma, unspaced em dash) only where the text is currently inconsistent. Leave punctuation at quotation marks until P-1 is answered. All four are mechanical in LaTeX and can be switched later.
5. **Alternative:** if you expect a UK publisher, adopt British forms now: single quotation marks, logical punctuation, no serial comma, spaced en dashes.

### P-3. Citation system *(blocking for Phase 5)*
1. **Location:** all notes; about 75 author–date citations in the text; the bibliography (L3047–3144).
2. **Issue:** the book mixes a notes system (full citations in footnotes) with author–date (in-text "Albert and Hahnel (1991a, Ch.~5)" and a reference list in author–date form).
3. **Problem:** CMOS, the University of Chicago Press and Bloomsbury (2015) all require one system.
4. **Recommendation:** **Option A, author–date.**
   - Alphabetise the reference list, unnumbered, in CMOS form.
   - Turn note citations into "(Author Year, page)".
   - Keep footnotes for discussion and for remarks on how a source was accessed.
   - Reasoning: the reference list is already in this form, and the interdisciplinary and technical readership suits it.
5. **Alternative:** **Option B, notes and bibliography.**
   - Keep footnotes as the citation vehicle.
   - Turn the in-text citations into notes.
   - Restyle the bibliography in CMOS notes-and-bibliography form.
   - Reasoning: more usual in history and political theory, and closer to Bloomsbury's "short-title" option.

### P-4. Remarks on source access
1. **Location:**
   - copyright page, source-access tiers (L345);
   - bibliography remarks ("Full text analyzed via ZNetwork", "Print TOC/pagination scan preserved at research/sources/…", "Abstract consulted", "Bibliographic record only");
   - notes ("cited at bibliographic level" 12 times; "not read in full").
2. **Issue:** these state honestly how each source was used. That is good practice, but unusual in bibliography entries and on a copyright page.
3. **Recommendation:**
   - keep the remarks in the notes;
   - move the tier statement and the bibliography remarks into a one-page "Note on Sources" in the front matter;
   - leave repository file paths (`research/sources/…`) out of the printed bibliography, since they are in `research/SOURCE_AUDIT.md`.
4. **Alternative:** keep everything as it is and explain the practice in a preface.

### P-5. Branding: "Post-Capitalist Labs Imprint · Working Draft Monograph"
1. **Location:**
   - cover (L190–301);
   - imprint page with the "About Post-Capitalist Labs" panel (L306–334);
   - running footer on every page (preamble);
   - closing banner (L3146–3157);
   - `pdfauthor` and the "Cite as" line.
2. **Issue:** imprint branding, a mission statement, GitHub URLs and the "Working Draft" label.
3. **Problem:** a publisher supplies its own imprint and design. The Post-Capitalist Labs material would not appear in a Bloomsbury book, except perhaps as an author affiliation or in the acknowledgements.
4. **Recommendation:** add a LaTeX switch (for example `\submissiontrue`) that replaces the cover and imprint panels with a plain title page and removes the footer and banner in the submission build, while keeping the public GitHub draft as it is. *Needs your approval.*
5. **Alternative:** keep the branding in the public draft and strip it only at submission.

### P-6. CC BY-SA 4.0 licence and prior publication *(Critical C-6)*
1. **Location:** copyright page (L340ff.).
2. **Issue:** the text and figures are licensed CC BY-SA 4.0 and published openly.
3. **Problem:** a standard contract takes exclusive rights. The ShareAlike grant already made cannot be withdrawn, and Bloomsbury will want to know about the prior public versions.
4. **Recommendation:** raise this with the commissioning editor before submission, for example as an open-access edition under a CC licence or a print licence alongside the open version. Do not change the licence notice without legal or publisher advice.

---

## Q. Quotations and attribution

### Q-1. Quotations made British *(Critical C-1, C-2)*
1. **Location:**
   - Ch. 1 epigraph (L560), "decentralised";
   - Ch. 8 epigraph (L2478), "programmes";
   - Ch. 9 epigraph (L2543), "behaviours".
2. **Problem:** these quote American editions (*Looking Forward*; *PEPE*, Princeton). The Ch. 1 source reads "decentralized" (confirmed 7 November 2026). The other two could not be checked because ZNetwork blocked access, but they are very probably "programs" and "behaviors". CMOS requires quotations to keep their source's spelling.
3. **Recommendation:** restore the source spelling in all three, and let me check every quotation from an American source the same way in Phase 5. The style guide already forbids making quotations British.
4. **Your action:** confirm "programs" and "behaviors" against a print copy, or approve the restoration on the strength of the first confirmed case.

### Q-2. Nove quotation: interpolated word *(Critical C-3)*
1. **Location:** §1.2 block quotation (L580–581).
2. **Text:** "… binding instructions from planning offices [i.e., command planning]. There is no third way."
3. **Problem:** `research/SOURCE_AUDIT.md` §2 records the verified text as "[i.e., central planning]".
4. **Questions:**
   - Which wording is in your source?
   - Are the bracketed glosses Albert and Hahnel's (in *PEPE*) or added in this book?
5. **Recommendation:** match the source exactly. If the glosses are yours, keep them in square brackets and say so in the note ("brackets added").

### Q-3. Ch. 3 epigraph is jacket copy *(Critical C-4)*
1. **Location:** L980.
2. **Text:** "Until now, however, descriptions of alternatives have been unconvincing. Here Michael Albert and Robin Hahnel support the libertarian socialist tradition …"
3. **Problem:** this is Princeton University Press's promotional copy (front flap and JSTOR abstract), which refers to the authors in the third person, but it is attributed to Albert and Hahnel.
4. **Recommendation:** replace it with a sentence from the authors' own text.
5. **Alternative:** keep it, attributed as "Jacket copy, *The Political Economy of Participatory Economics* (Princeton University Press, 1991)", and seek permission from the press.

### Q-4. Ch. 9 epigraph is spliced *(Critical C-5)*
1. **Location:** L2543.
2. **Issue:** sentences from p. 108 and p. 129 of *PEPE* are joined by an ellipsis.
3. **Problem:** a reader would take it as one passage.
4. **Recommendation:** use only one of the two passages, preferably p. 129, which also opens Chapter 10's epigraph source.
5. **Alternative:** keep both, with the splice made explicit.

### Q-5. Brinton block quotation
1. **Location:** L936–938.
2. **Issues:**
   - "*Meaningful action*" is set with `\emph` inside an all-italic quotation, so it comes out roman, reversing the original emphasis.
   - "[,]" is an editorial insertion.
3. **Recommendation:**
   - set block quotations in roman, without enclosing quotation marks (CMOS treatment of block quotations; this applies to all three);
   - keep the italic for "Meaningful action" if it is in the original, adding "emphasis in original" to the note;
   - confirm that the original lacks the comma, which the bracketed "[,]" implies.

### Q-6. Second-hand quotations
1. **Location:** Ch. 4 epigraph (Buchanan, quoted from *PEPE*, L1062); Nove (Q-2).
2. **Issue:** both are quoted from Albert and Hahnel rather than from the originals.
3. **Recommendation:** keep the "quoted in" attribution, which is correct CMOS practice. No change unless you have checked the originals.

### Q-7. Sources cited in notes but missing from the bibliography *(Critical C-8)*
1. **Location:** Bookchin (L768), Souchy (L777), Moisés (L824), Radio Dabanga (L851), McGranaghan (L1483), Zawirski (L1725), WICG and Chromium (L1794), Cosmos SDK documentation (L2102), Apple (L2426), Eckstein (L2485).
2. **Recommendation:**
   - add the scholarly sources: Bookchin and Souchy as chapters in Dolgoff 1974; McGranaghan; Zawirski; Eckstein;
   - leave web documentation and news items to the notes only, which CMOS permits.
   - Your choice.

---

## D. Editorial decisions

Details are in `INITIAL_AUDIT.md` §3, "Editorial decisions".

| ID | Question | Recommendation |
|---|---|---|
| D-1 | Bold emphasis in running prose (about 980 instances) | Remove it from running prose; keep bold for column heads and run-in labels; use italics for a term's defining first use |
| D-2 | "Rigorous" and the 25-word subtitle | Drop "Rigorous", for example "*A Source-Grounded Feasibility Study and Post-Quantum Architecture for Democratic Planning*". Your wording. |
| D-3 | Long chapter titles in report style | Keep for now. Revisit with the publisher. |
| D-4 | "Why We Reject a Global Blockchain" in a single-author book | Keep if "we" means you plus Post-Capitalist Labs (D-5) |
| D-5 | "We" versus "I" (about 23 instances of "we/our"; "this book" 19×) | Decide on one voice. If the book is sole-authored, use "I" in the front matter and "this book" elsewhere. |
| D-6 | Chapter 1 as "Executive Summary" | Consider "Introduction" (content unchanged). |
| D-7 | "How to Read This Book" audience boxes and the cover's audience badges | Keep the reading guide as a short plain-text preface section; drop the badges with the cover (P-5) |
| D-8 | Verification remarks in notes ("cited at bibliographic level") | Keep them (see P-4) |
| D-9 | Figures depend on colour and use 5–7 pt type (`INITIAL_AUDIT.md` M-4) | Ask the publisher about colour. Otherwise add pattern or label cues and raise the type size to 7 pt or more. Production work, after approval. |
| D-10 | Missing acknowledgements, preface, list of figures and list of tables | You write the acknowledgements. I can add the lists automatically. |

---

## AI. Disclosure of AI assistance

### AI-1. Bloomsbury policy and draft statement
1. **Location:** not yet in the book. To be placed in the acknowledgements, a preface note, or wherever the publisher directs.
2. **Policy check (7 November 2026):** I could not find a public Bloomsbury Academic policy on generative AI for book authors. Bloomsbury's site refused automated access, and web searches returned no Bloomsbury page. What the search did show, as general practice, not as Bloomsbury rules:
   - AI tools cannot be authors;
   - use should be disclosed, naming the tool, where it was used and how much;
   - light language editing is often treated differently from substantive generation;
   - the author remains responsible for the content.
   - About a third of academic publishers had public policies in a 2025 audit.
   
   Ask the commissioning editor for Bloomsbury's current policy, and check the contract for AI warranties.
3. **Accuracy note:** your instructions describe the work as done with "Claude in Cursor". This editorial pass, and the recorded refinement passes, ran in **Claude Code** (Anthropic), in the terminal and VS Code. Please name the tool or tools you actually used, and the period. The draft below leaves them in brackets.
4. **Draft statement, for your approval and not inserted in the book:**

   > **Use of generative AI.** In preparing this book I used Claude, a large language model made by Anthropic, through [Claude Code / Cursor], between [month year] and [month year]. I used it to [write and run the analysis and benchmark scripts that check the book's calculations; check bibliographic details against Crossref, publishers' pages and standards bodies; compare drafts against review findings; propose revisions to wording, which I accepted, changed or rejected; and copyedit the manuscript]. The arguments, interpretations and conclusions are mine. I reviewed every change and am responsible for the content, including any errors. Claude is not an author of this book. The analysis scripts and a record of revisions are in the project repository [URL].

5. **Recommendation:** fill in the brackets so they describe your use accurately. Keep the last three sentences. Place the statement in the acknowledgements unless Bloomsbury specifies otherwise.

---

## Status after the author's answers (November 7, 2026)

| Query | Status |
|---|---|
| P-1 | **Resolved:** self-published; no contract. CMOS 18 governs. |
| P-2 | **Resolved:** CMOS forms applied (double quotation marks, commas and periods inside, serial comma, unspaced em dash). US spelling throughout. |
| P-3 | **Resolved:** author–date applied (CHANGELOG 5.1–5.3). |
| P-4 | **Open:** source-access remarks are kept in the notes and references for now. |
| P-5 | **Deferred** by the author (branding). |
| P-6 | **Open:** licence (relevant to any later publisher or distributor). |
| Q-1 | **Resolved:** "decentralized", "programs" and "behaviors" restored. |
| Q-2 | **Resolved:** Nove quotation kept; the brackets are Albert and Hahnel's. **Note:** `research/SOURCE_AUDIT.md` §2 still records the bracket as "central planning" and should be corrected to match. |
| Q-3 | **Open:** the Ch. 3 epigraph is still the Princeton University Press jacket copy. |
| Q-4 | **Open:** the Ch. 9 epigraph is still spliced (pp. 108, 129). |
| Q-5 | **Partly resolved:** block quotations are now roman with no enclosing quotation marks, and "*Meaningful action*" prints in italic. Still to confirm: whether the italic is in the original ("emphasis in original"), and the "[,]" insertion. |
| D-1 | **Deferred** (bold emphasis). |
| AI-1 | **Open:** the disclosure text needs your tool name and period. |

## New queries from Phases 4–5

### X-1. Broken reference: "ephemeral shares … Section 11.2"
1. **Location:** §7.4.3 (L2360): "that bounded retention is what ``ephemeral shares'' means in Section~11.2."
2. **Problem:** "ephemeral shares" occurs nowhere else in the book, and §11.2 (Theory of Transition) does not use the phrase. The target was probably renumbered or removed in an earlier pass.
3. **Recommendation:** say where the phrase is meant to point. If no target exists, delete "means in Section~11.2" and end the sentence "…is what we mean by ``ephemeral shares.''"

### X-2. Orphan reference: Henry (1972)
Henry (1972) is listed in References but cited nowhere. Cite it (for example in §4.4 alongside Heal 1973) or delete it. `check_book.py` holds it in `UNCITED_PENDING` until you decide.

### X-3. O'Neill 2024a vs. 2024b
In-text "O'Neill (2024)" now points to 2024a ("Pluralism, Ecology and Planning"). Confirm, or tell me which passages draw on 2024b (the response to Hahnel).

### X-4. Short titles in tables
PEPE, LF, DEP and PLAC remain as compact source pointers in dense tables (for example "PEPE Ch.~2, p.~26"), and each abbreviation entry now gives its author–date key. **Alternative:** convert every table pointer to full author–date form ("Albert and Hahnel 1991a, chap.~2, 26"), which would lengthen cells in Tables 2.2 and 3.1.

### X-5. Citation key for Isaac with Franke (2002)
Cited as "Isaac 2002" (CMOS practice for a "with" co-author). The alternative is "Isaac and Franke 2002".

### X-6 to X-8. Reference metadata
See `CITATION_AUDIT.md` §2: thin metadata on three added entries; Freeman's two venues; missing URLs.

### X-9. The adjectival date in §2.11 was reworded
"the SDF--Damascus integration agreement of January 30, 2026" replaces "the 30 January 2026 SDF--Damascus integration agreement". Approve or revert.

### X-10. Wording of the Table 2.1 caption
The caption was changed to sentence style and reordered: "institutions actually implemented vs.\ proposals and extrapolations". Approve or revert.
