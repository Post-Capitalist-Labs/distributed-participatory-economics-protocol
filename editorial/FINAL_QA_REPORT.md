# Final QA Report

**Branch:** `editorial`, uncommitted. **Base:** `c578ba8`.
**Manuscript:** `book/dpep_book.tex` → 147-page PDF, copied to `reports/` and the repository root.
**Date:** November 8, 2026.

## 1. Work completed

| Phase | Done |
|---|---|
| 1–3: discovery, standards, audit | `STYLE_GUIDE.md`, `INITIAL_AUDIT.md`, `PERMISSIONS_LOG.md`, `AUTHOR_QUERIES.md` |
| Author decisions (Nov. 7) | Self-published; CMOS 18; US spelling; CMOS punctuation; author–date; three epigraphs restored; Nove kept; branding and bold deferred |
| 4: mechanical | US spelling (307), dates (50), dashes (12), punctuation at quotation marks (5), *e.g.*/*i.e.* (6), serial comma (145), cross-references (19, including 2 broken by the earlier Chapter 2 reorder), block quotation and epigraph treatment, sentence-style captions (12) |
| 5: apparatus | 115 notes converted to author–date; 14 in-text locators normalized; reference list rebuilt (92 numbered items → 112 alphabetized CMOS entries; 4 added, 1 orphan flagged); `CITATION_AUDIT.md`; alt text drafted (`ALT_TEXT.md`) |
| 6: editorial review | Substantive issues queried, not rewritten (`AUTHOR_QUERIES.md`, Q and X series) |
| 7: QA | This report |

The full record is in `CHANGELOG.md`.

## 2. Verification

- **Build:** clean full build; 147 pp; no undefined references or citations; no overfull box above 10 pt. One 30 pt overflow, caused by an unspaced em dash, was found and fixed.
- **`check_book.py`:** passes (parser updated for the new reference list; one pending orphan, X-2).
- **Clean-state run:** `parameters`, `verify_signature_suites`, `verify_r3` (`book_table_matches: true`), `verify_sync_committee`, `verify_economics`, `reference_tests_r3` and `verify_r2` all exit 0. Their output files are byte-identical to the committed versions.
- **Structure against the base:** chapters 14/14, sections 50/50, subsections 34/34, notes 153/153, captions 45/45, every float and maths environment count unchanged. Labels 100 → 116 (12 chapters and 4 sections added).
- **Protected content:** maths, code, TikZ paths, identifiers, labels and all numbers were masked during automated passes. The numeric tables are confirmed by `verify_r3` (`book_table_matches: true`) and by `check_book` figure checks [5].
- **Diff:** 555 insertions and 519 deletions in the `.tex`. The word-count drop (40,624 → 39,430) comes from full titles, places and publishers moving out of the notes into References, from ISBNs and page counts removed from the reference list, and from the spelling changes. No passage was removed.
- **Rendered checks in this pass:** References (first page); the Bookchin block quotation (roman, no enclosing marks); the Ch. 9 epigraph (no quotation marks, nested quotation marks now double); converted notes in §2.2 and §2.5. Other pages were not re-inspected visually. Their changes are character-level and the build reports no overflow above 10 pt.

## 3. Outstanding issues

**Critical (to resolve before release):**
- Q-3: the Ch. 3 epigraph is publisher's jacket copy attributed to Albert and Hahnel.
- Q-4: the Ch. 9 epigraph is spliced from pp. 108 and 129.
- X-1: broken pointer, "ephemeral shares … Section 11.2".
- Permissions (`PERMISSIONS_LOG.md`): 11 epigraphs and the Bookchin block quotation have no recorded permission. For a self-published book, decide which to keep, and seek permission or rely on fair use on advice.
- P-6: CC BY-SA 4.0 licence; matters only if a publisher or distributor is approached.

**Major:**
- Unconfirmed or partly confirmed reference metadata (`CITATION_AUDIT.md` §2, C-9; X-6 to X-8).
- Orphan reference Henry 1972 (X-2); O'Neill 2024a assignment (X-3).
- `research/SOURCE_AUDIT.md` still records the Nove bracket as "central planning" (Q-2 note).
- Figures depend on colour, use 5–7 pt type and have no embedded alt text (M-4, M-5; draft text ready).
- No acknowledgements, preface, or lists of figures and tables (M-9); no index or index plan.

**Deferred by the author:** bold emphasis (about 980 instances), branding and front-matter design, the AI disclosure text (AI-1).

**Editorial decisions open:** P-4 (source-access remarks), X-4 (table short titles), X-5 (Isaac key), X-9 and X-10 (two small rewordings), D-2 to D-8 (subtitle, chapter titles, voice, "Executive Summary").

## 4. Things a reader may notice

- **Reports out of step with the book.** The reports and research `.md` files still use British spelling and the old bibliography numbering. This pass covered only the book.
- **Changes needing a closer look.** Note citations are now short ("Hansen 1991, chap.~9, 230--245"), so readers find full details in References. Scan Chapter 2's notes to confirm you are happy with that density.

## 5. Readiness

The manuscript is **consistent in style and citation**: CMOS 18, US spelling, author–date, cross-references verified. It is **not ready to publish** while the Critical items in §3 remain. The epigraph attribution and the splice (Q-3, Q-4), the broken pointer (X-1) and the permissions decisions need your judgment. Nothing has been committed or pushed.
