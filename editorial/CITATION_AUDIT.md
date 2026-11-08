# Citation Audit

**State audited:** `book/dpep_book.tex` on branch `editorial`, after Phase 5 (author–date). Base commit `c578ba8`.
**Date:** November 8, 2026.
**System:** CMOS author–date. Citations appear in the text and in the notes; the reference list is titled "References" and has 112 entries.

## 1. Automated checks

| Check | Result |
|---|---|
| Every reference-list entry is cited in the text or notes (`check_book.py` [2]) | Pass. One exception, held pending: Henry 1972 (X-2) |
| Every "Surname (Year)" citation in the text resolves (`check_book.py` [3]) | Pass (64 citations) |
| Every author–date citation in the notes matches a surname-and-year pair in References (script run on November 8, 2026) | Pass. All remaining flags were false positives (first names, place names, prose mentions such as "Albert and Hahnel's 1991 design") |
| Cross-references (`\ref`) | 118 labels, 91 references; none missing or duplicated |
| LaTeX build | 147 pp; no undefined references or citations |

## 2. Unresolved references (author action)

| # | Entry | Location | Problem | Recommendation |
|---|---|---|---|---|
| X-2 | Henry, Claude. 1972. | References | Listed but never cited. The base commit had no citation either; the checker had matched it only on Henry Corrigan-Gibbs's first name. | Cite it where planning procedures are discussed (§4.4), or delete it. |
| X-3 | O'Neill 2024a/2024b | §8.2 (L2529, 2545), Ch. 10 (L2714), Ch. 12 (L2902), reader's guide (L362) | The two 2024 articles were one combined entry. In-text "O'Neill (2024)" was assigned to 2024a ("Pluralism, Ecology and Planning") on the evidence of the context. | Confirm, or change any passage that draws on the 2024b response. |
| C-9 | Not confirmed in `research/SOURCE_AUDIT.md` | References | Hahnel 2022; Sandström 2023; Participatory Economy Project 2023; Heal 1973; Leval 1971; Mintz 2013; O'Connor et al. 2020 (BLAKE3); NIST 2024a–c; Buchman, Kwon, and Milosevic 2018; Kornai 1980; Corrigan-Gibbs and Boneh 2017; Crites and Stewart 2025 | Check the publisher, DOI or URL. The metadata is unchanged from the base text and nothing was invented. |
| C-9 | Partly confirmed | References | Sandström 2025 (Crossref dates the online edition 2026; subtitle unconfirmed); Hurwicz 1973; Hayek 1945; Devine 1988; Leval 1975; Peirats 1974; Marx 1871; Freeman 1972 (two venues listed); Casanova 2005 (Crossref 2004) | Confirm the edition used. For Casanova and Sandström, decide which date to cite. |
| X-6 | Added entries with thin metadata | References | Bookchin 1974 ("Introductory Essay" in Dolgoff; page range of the essay unknown, xxvii–xxx cited); Moisés 2023 (no URL in the source note); Yin et al. 2019 (author list given as "et al." in the source note) | Supply the essay pages, the Enlace Zapatista URL and the full HotStuff author list, or accept "et al." |
| X-7 | Freeman 1972 | References | Two venues are given (*The Second Wave* 2 (1); *Berkeley Journal of Sociology* 17: 151–164). CMOS wants the version that was consulted. | Name the version consulted and give the other as "Reprinted in …" |
| X-8 | Lessig 2000, Madison 1788, Hume 1741 | References | No page numbers or URLs for Lessig 2000 and Hume 1741 | Acceptable for well-known texts. Add a URL or a modern edition if one was used. |

## 3. Conventions applied

- **Locators:** "chap.", "chaps.", "sec.", page numbers without "pp."; "n" for a note (for example 58n3).
- **Same author and year:** distinguished with a, b, c (Albert and Hahnel 1991a and 1991b; O'Neill 2024a and 2024b; NIST 2024a–c).
- **Reprints:** original date in parentheses, for example Castoriadis (1957) 1972.
- **DOIs:** given as `https://doi.org/…` URLs.
- **Web sources:** cited in the notes with "checked [date]", and not listed in References. CMOS permits this for web documentation, release pages and news.
- **Access remarks:** "Cited at bibliographic level", "read in full" and "abstract consulted" are kept in the notes and entries (query P-4).
- **Short titles in tables:** PEPE, LF, DEP and PLAC are kept as defined abbreviations, and each abbreviation-list entry gives its author–date key (query X-4).
- **Epigraph source lines:** left in author-and-title form, which is CMOS practice for epigraphs.
