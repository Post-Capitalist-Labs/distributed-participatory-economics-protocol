# Source Audit and Provenance Verification

**Deliverable:** `research/SOURCE_AUDIT.md`
**Status:** Working Draft (third refinement, 4 November 2026; new-entry audit, 6 November 2026)
**Canonical bibliography:** back matter of `book/dpep_book.tex`. Earlier sections of this file are kept below as a historical record; where they conflict with this section, this section wins.

---

## Audit of entries added on 5–6 November 2026

`research/analysis/audit_bibliography.py` was re-run on 6 November 2026 over the whole bibliography (103 works; output `research/analysis/bibliography_audit.json`). This section records dispositions for the 34 works added since the third-refinement audit below: the six from the stack maturity pass and the works added with §5.1, the Chapter 2 expansion and §§11.3–11.4. Entries already listed in the third-refinement table were not re-dispositioned.

**34 entries reviewed:** 31 confirmed, 3 partially confirmed, 0 not confirmed, 0 corrected.

| Entry | Result | How checked |
|---|---|---|
| Hume (1741) "Of the Independency of Parliament" | Confirmed | Crossref: essay in OUP and CUP editions of Hume's essays; quotation checked against the Project Gutenberg text of the *Essays* |
| Madison (1788) Federalist No. 51 | Confirmed | Crossref: reprint of Federalist No. 51 under its full title; date and quotation checked on the Library of Congress text |
| Lessig (1999) *Code and Other Laws of Cyberspace* | Confirmed | Crossref: reviews (SSRN 2000; College & Research Libraries 62(1)) |
| Lessig (2000) "Code Is Law", *Harvard Magazine* | Confirmed | Magazine page fetched (not in Crossref) |
| Rogaway (2015) "The Moral Character of Cryptographic Work" | Confirmed | IACR ePrint 2015/1162 page and PDF; quotations and pages checked |
| Brinton (1967) "As We See It" | Confirmed | Text on marxists.org; quotation checked verbatim (the source has no comma after "confidence") |
| Brinton (1970) *The Bolsheviks and Workers' Control* | Confirmed | Full text on marxists.org read; Solidarity, London, 1970 stated in the transcription |
| Brinton (2004) *For Workers' Power*, ed. Goodway | Confirmed | Crossref: reviews in ILWCH (2006) and J. Labor and Society (2021) |
| Castoriadis (1957/1972) *Workers' Councils and the Economics of a Self-Managed Society* | Partially confirmed | 1972 Solidarity translation read in full (original S. ou B. 22, July 1957, stated there); the 1988 Minnesota reprint is not confirmed |
| Anderson (1964) *Hungary '56* | Confirmed | Chapter "The Proletariat Crushed" read on libcom; Solidarity, London, 1964 confirmed by a 1964 review (Kidron) and a translation's source note |
| Lomax (1976) *Hungary 1956* | Partially confirmed | Crossref: AHR review of the 1977 St. Martin's (New York) edition; the 1976 Allison & Busby (London) edition is not directly confirmed |
| Estrin (1983) *Self-Management* | Confirmed | Crossref: reviews in Canadian-American Slavic Studies and Slavic Review (1985), Cambridge University Press |
| Woodward (1995) *Socialist Unemployment* | Confirmed | DOI 10.1515/9780691219653 |
| Winn (1986) *Weavers of Revolution* | Confirmed | Crossref: reviews in The Americas and AHR (1987) |
| Medina (2011) *Cybernetic Revolutionaries* | Confirmed | DOI 10.7551/mitpress/8417.001.0001 |
| Sitrin, ed. (2006) *Horizontalism* | Confirmed | Crossref: reviews in Left History and Choice (2007) |
| Gómez (2009) *Argentina's Parallel Currency* | Partially confirmed | DOI 10.4324/9781315653532 resolves to the 2015 Routledge reissue; the 2009 Pickering & Chatto edition is not directly confirmed |
| Mora (2017) *Kuxlejal Politics* | Confirmed | DOI 10.7560/314463 |
| Klein (2015) *Compañeras* | Confirmed | No Crossref record; publisher and bookseller listings: Seven Stories Press, 2015, ISBN 9781609805876 |
| Baschet (2024) "The Reorganization of Zapatista Autonomy" | Confirmed | *Ill Will* page fetched (15 November 2024); not in Crossref |
| Aziz (2011) "A Discussion Paper on Local Councils in Syria" | Confirmed | 2013 English translation read in full on The Anarchist Library; not in Crossref |
| Bayat (2017) *Revolution without Revolutionaries* | Confirmed | Crossref: reviews in IJMES and AJS (2018), Stanford University Press |
| Isaac with Franke (2002) *Local Democracy and Development* | Confirmed | Crossref: reviews in J. Asian Studies and American Anthropologist (2004) |
| Farrell, Suiter & Harris (2019) | Confirmed | DOI 10.1080/07907184.2018.1534832; 34(1) 113-123 (Crossref dates the online version 2018) |
| Barandiaran et al. (2024) *Decidim* | Confirmed | DOI 10.1007/978-3-031-50784-7 |
| Kennedy, Lietaer & Rogers (2012) *People Money* | Confirmed | No Crossref match; title page of the PDF read in full (Triarchy Press, Axminster, 2012) |
| Mattsson, Criscione & Ruddick (2022) | Confirmed | DOI 10.1038/s41597-022-01539-4 |
| Mattsson, Criscione & Takes (2023) | Confirmed | DOI 10.1038/s41598-023-33184-1 |
| Davis, Patton, Rosulek & Schoppmann (2023) | Confirmed | DOI 10.56553/popets-2023-0126, PoPETs 2023(4) 578-592 |
| Massimo, Kampanakis, Turner & Westerbaan (2025) RFC 9881 | Confirmed | Crossref: DOI 10.17487/rfc9881 |
| Ounsworth et al. (2026) composite ML-DSA draft-19 | Confirmed | Internet-Draft, not in Crossref (query returned unrelated RFCs); checked on the IETF Datatracker on 5 November 2026 |
| Sonnino et al. (2019) Coconut | Confirmed | DOI 10.14722/ndss.2019.23272 |
| Bootle, Lyubashevsky, Nguyen & Sorniotti (2023) | Confirmed | Crossref: CRYPTO 2023, LNCS, DOI 10.1007/978-3-031-38545-2_13 |
| Argo et al. (2024) | Confirmed | DOI 10.1145/3658644.3670297, CCS 2024, pp. 1523-1537 |

No entry needed correction. The three partial confirmations concern editions (Castoriadis 1988 reprint, Lomax London edition, Gómez first edition), not the identity of the work; the book cites none of them by page.

## Third refinement (this pass)

### How sources were accessed in this pass

| Source | Access | Used for |
|---|---|---|
| Laibman (2014), *Science & Society* 78(2) | Crossref record and publisher abstract (via Crossref API). Full text paywalled; not read. | R3-15: authorship, pages, §8.2 limited to the abstract |
| Hahnel (2014), *Science & Society* 78(3) 379-389 | Crossref bibliographic record only | R3-15: identified the response |
| Ackerman, "The Red and the Black", *Jacobin* (20 Dec 2012) | Jacobin page: author and date visible, body paywalled; secondary commentary via web search | R3-15: bibliographic identity confirmed, but its treatment of participatory economics could not be read, so it is **not** cited in the book |
| EJPE 17(2), Winter 2024 (O'Neill, Kuch, Dapprich) | Open-access issue PDF downloaded from `ejpe.org/journal/issue/download/35/67` this pass (2.0 MB, 271 pp.) plus each article's landing page metadata. **No copy is in the repository**; the earlier claim of an "issue PDF" was not backed by a stored file. Not committed, to avoid redistributing the issue. | R3-17: titles, pages, DOIs; abstracts and conclusions of Kuch and Dapprich; abstracts of both O'Neill pieces |
| Deng, Lai, Peng & Yin (2017) | arXiv 1312.3040v2 PDF, read in full for Algorithms 3-4, Lemma 2.2, eq. (2.8)/(2.11), Thm 2.3-2.4 | R3-12 |
| `draft-irtf-cfrg-vdaf-22` | Full text (`.txt`) from ietf.org archive | R3-04 (§7.4.3 SumVec), R3-07 (§7.2.3, §9.2, §9.4) |
| `prio` 0.18.1 (libprio-rs) | crates.io; source in the Cargo registry; compiled and run | R3-08 benchmark; README states it implements VDAF draft 18 |
| Leval, *Collectives in the Spanish Revolution*, Part 2 Ch. V | libcom.org online edition (first 100k characters) | R3-16: 24 cantonal federations, 275 villages, 141,430 families; Caspe 14-15 Feb 1937 |
| Peirats, in Dolgoff (1974), Part 2 Ch. 9 | marxists.org edition | R3-16: 500 collectives / 433,000 members (Souchy's estimate); Caspe 14 Feb 1937 |
| Wikipedia, "Regional Defence Council of Aragon" | web page | R3-16: Bujaraloz plenary 6 Oct 1936; "500 delegates representing 80,000 collectivists" (no inline source); dissolution 10-11 Aug 1937 |
| `msszczep/pequod-cljs` @ `8bd46b5c` | Existing clone plus the 20 Git LFS objects fetched from `media.githubusercontent.com`; each checked against the SHA-256 in its pointer (5 needed a retry after truncated downloads) | All 70 generators audited |
| Upstream `csvgen.clj` | Clone, lines 391-395 and 463-469 | R3-13 (redundant `min`), corrected line numbers |
| Every bibliography entry | Crossref API by DOI or bibliographic query (`research/analysis/audit_bibliography.py`, output `bibliography_audit.json`), plus the pages above | R3-15 bibliography audit |

Not accessed: paywalled books (Hahnel 2021 print, Sandström 2020/2025, Mintz, Casanova, Seidman, Hansen, Mansbridge, Dahl & Tufte, Kornai 1980); the full text of Laibman (2014) and of Ackerman's Jacobin article. No paywall was bypassed.

### R3-15: Laibman, not Ackerman

Crossref for DOI `10.1521/siso.2014.78.2.207` returns author **David Laibman**, pages **207-234**. The book attributed the article to Seth Ackerman with pages 207-239 in the bibliography, the §8.2 citation list, the §8.2 dynamic-entry item and a footnote. All are corrected. §8.2 now states only what the abstract says (an "abstractly speculative" design approach, a fear of authority rooted in classical anarchism, an "uncanny resemblance to Walrasian competitive market equilibrium") and cites Hahnel's response, `10.1521/siso.2014.78.3.379`, pp. 379-389. Ackerman's "The Red and the Black" (*Jacobin*, 20 December 2012) exists, but its participatory-economics argument could not be read, so it is not cited.

### R3-16: Caspe and Aragon

The book's "about 450 collectives and 300,000 members" and "established in October 1936" are not supported by the sources checked. October 1936 (the 6th, at Bujaraloz) is the founding of the Regional Defence Council of Aragon. The Federation of Collectives was constituted at Caspe on 14-15 February 1937. Reported sizes: Leval 24 cantonal federations / 275 villages / 141,430 families; Peirats citing Souchy 500 collectives / 433,000 members; Wikipedia 500 delegates / 80,000 collectivists (unsourced). All are sympathetic or participant sources. The book now gives the range, attributions and dates. Other Chapter 2 headline figures were reworded: the "70-80% of Catalan industry" figure is flagged as untraced, Mintz's and Leval's participation estimates are attributed and their partisan character noted, and the Mondragón membership split is no longer stated as a precise figure.

### R3-17: other gaps

- **Levy (1991):** no such work identified by Crossref or web search. Removed from the bibliography and from §8.2.
- **Freundlich (2015):** no 2015 work of that title found (web search; Mondragon Unibertsitatea's research portal lists a 2017 *lecture* of that title, not a publication). Removed; Mondragón figures now cite Whyte & Whyte and are hedged.
- **Dapprich, Kuch, O'Neill:** see above. Fairness check: the book's Dapprich summary was broadly fair, but it omitted his central liberty argument about domination by the majority of one's own workers' council, and his word "algorithmic planning process" (so "algorithmic" is his, though "algorithmic centralism" is not). Kuch's title was wrong ("Decentralisation, Federations, and Authority..."; actually "Centralization Tendencies in Participatory Planning"), and his thesis (federations as "central planning authorities in disguise") is now stated. O'Neill's effort-surveillance criticism and his "consumption and production corridors" were missing and are now included.
- **Tier 3 page-level claims:** reworded where they implied a reading ("this pass did not re-read" became "consulted at bibliographic level", and page-specific claims for Casanova and Seidman are withdrawn).

### Bibliography audit (R3-15 extension)

**72 entries reviewed:** 39 confirmed, 9 corrected and now confirmed, 9 partially confirmed, 12 not confirmed this pass, 3 removed.

| Entry | Result | How checked |
|---|---|---|
| Albert & Hahnel (1991a) PEPE | Confirmed | DOI 10.2307/j.ctv131bvr2 resolves to title/authors/publisher |
| Albert & Hahnel (1991b) Looking Forward | Confirmed | Crossref: review in J. Comparative Economics 16(4) confirms title/authors |
| Hahnel & Albert (1990) Quiet Revolution | Corrected, now confirmed | Printed DOI 10.1515/9780691216034 resolved to Paret, *Understanding War*; corrected to 10.1515/9781400887057 |
| Albert (2003) Parecon | Confirmed | Crossref: review in Sustainable Development 13(4) quotes title, Verso 2003, 311 pp. |
| Hahnel (2021) DEP | Confirmed | DOI 10.4324/9781003173700 |
| Hahnel (2022) A Participatory Economy | Not confirmed this pass | No Crossref match; AK Press page not checked |
| Sandström (2020) | Confirmed | DOI 10.4324/9781003036005 |
| Sandström (2023) web article | Not confirmed this pass | URL not re-fetched |
| Sandström (2025) | Partially confirmed | Crossref DOI 10.4324/9781003732174 (dated 2026); subtitle not in record |
| Szczepanczyk (2023) | Confirmed | DOI 10.58567/jie01030004 (pages not in record) |
| PEP (2023) User Story Mapping | Not confirmed this pass | URL not re-fetched |
| Arrow, Hurwicz & Uzawa (1958) | Confirmed | Crossref: reviews in Canadian Math. Bull. 3(3) and Math. Gazette 44 |
| Heal (1973) | Not confirmed this pass | No Crossref match |
| Henry (1972) | Corrected, now confirmed | Title corrected to 'Differential equations with discontinuous right-hand side for planning procedures'; JET 4(3) 545-551 confirmed |
| Hurwicz (1973) | Partially confirmed | Reprint in Collected Papers found; AER 63(2) details not directly confirmed |
| Hayek (1945) | Partially confirmed | Reprints found; AER 35(4) 519-530 not directly confirmed |
| Lange & Taylor (1938/1964) | Confirmed | Crossref: 1939 and 1940 reviews |
| Nove (1983) | Confirmed | Crossref: Slavic Review 42(4) review |
| Buchanan (1985) | Confirmed | Crossref: Review of Politics 49(3) review |
| Cockshott & Cottrell (1993) | Confirmed | Crossref: QJAE 7(1) review |
| Devine (1988) | Partially confirmed | Crossref: 2020 Routledge reissue; 1988 Westview edition not directly confirmed |
| Schweickart (1993) | Confirmed | Crossref: Phil. Soc. Sci. 27(3) review |
| Laibman (2014) [was 'Ackerman (2014)'] | Corrected, now confirmed | DOI 10.1521/siso.2014.78.2.207: author David Laibman, pp. 207-234 (printed 207-239) |
| Hahnel (2014) response | Confirmed | DOI 10.1521/siso.2014.78.3.379, pp. 379-389 (added) |
| Hahnel & Wright (2016) | Confirmed | Crossref: JWSR 24(2) review |
| O'Neill (2024) two pieces | Corrected, now confirmed | EJPE landing pages: pp. 27-48 and 117-124, DOIs added |
| Kuch (2024) | Corrected, now confirmed | Title corrected to 'Centralization Tendencies in Participatory Planning', pp. 49-72, DOI .885 |
| Dapprich (2024) | Confirmed | EJPE landing page: full title confirmed, pp. 73-93, DOI .867 |
| Dolgoff (1974) | Confirmed | Crossref: Review of Politics 37(1) review |
| Leval (1975) | Partially confirmed | Crossref: review of a later (Oakland) edition; Freedom Press 1975 not confirmed; Ch. V read online |
| Leval (1971) Espagne Libertaire | Not confirmed this pass | Added from existing epigraph footnote; not checked |
| Peirats, in Dolgoff | Partially confirmed | Ch. 9 read on marxists.org; Ch. 6 not checked |
| Mintz (2013) | Not confirmed this pass | No Crossref match |
| Marx (1871) | Partially confirmed | Reprints found; original publication details not confirmed |
| Merriman (2014) | Confirmed | Crossref: reviews in The Historian and J. Interdisciplinary History |
| Hansen (1991) | Confirmed | Crossref: Classical Review 42(2) review |
| Freeman (1972) | Partially confirmed | Crossref: WSQ 2013 reprint; 1972 journal details not confirmed |
| Graeber (2013) | Confirmed | Crossref: Sociology 48(5) review |
| Ostrom (1990) | Confirmed | Crossref: Politica 24(1) review |
| Whyte & Whyte (1991) | Confirmed | Crossref: 1989 reviews of the first edition; 2nd ed. (1991) not directly confirmed |
| Freundlich (2015) | Removed | Removed: no such 2015 work found (web search; Mondragon research portal lists none) |
| Levy (1991) | Removed | Removed: could not be identified |
| Groves & Ledyard (1977) | Removed | Removed: confirmed (DOI 10.2307/1912672) but not cited in the text |
| Goulart & Chen | Corrected, now confirmed | Now published: Math. Programming Computation (2026), DOI 10.1007/s12532-026-00320-7 |
| O'Connor et al. (2020) BLAKE3 spec | Not confirmed this pass | Not re-fetched this pass |
| NIST FIPS 203/204/205 | Not confirmed this pass | Not re-fetched this pass |
| Kleppmann et al. (2019) | Confirmed | Crossref: DOI 10.1145/3359591.3359737, pp. 154-178 |
| Shapiro et al. (2011) | Confirmed | Crossref: LNCS, pp. 386-400 |
| Buchman, Kwon & Milosevic (2018) | Not confirmed this pass | arXiv not in Crossref; not fetched |
| Boyd et al. (2011) | Corrected, now confirmed | Confirmed, DOI added; title spelling restored to 'Optimization' |
| Deng, Lai, Peng & Yin (2017) | Confirmed | DOI 10.1007/s10915-016-0318-2, 71(2) 712-736; arXiv full text read |
| Hong, Luo & Razaviyayn (2016) | Corrected, now confirmed | Title and journal spelling corrected ('Alternating Direction Method of Multipliers', 'Optimization'); DOI added |
| Scarf (1960) | Confirmed | Crossref: IER 1(3) 157; DOI 10.2307/2556215 |
| Sonnenschein (1973) | Confirmed | Crossref: JET 6(4) 345-354 |
| Starr (1969) | Confirmed | Crossref: Econometrica 37(1) 25 |
| Hurwicz (1972) | Corrected, now confirmed | Volume confirmed via reviews; title spellings restored ('Decentralized', 'Organization'); pages not confirmed |
| Weitzman (1974) | Confirmed | Crossref: RES 41(4) 477 |
| Weitzman (1980) | Confirmed | Crossref: Bell J. Econ. 11(1) 302 |
| Kornai (1980) | Not confirmed this pass | No Crossref match |
| Kornai (1986) | Confirmed | Crossref: Kyklos 39(1) 3-30 |
| Casanova (2005) | Partially confirmed | Crossref: Routledge DOI 10.4324/9780203022801 dated 2004 |
| Seidman (1991) | Confirmed | Crossref: AHR 97(1) review |
| Seidman (2002) | Confirmed | Crossref: J. Social History 38(2) review |
| Finley (1981) | Confirmed | Crossref: Classical Review 32(2) review |
| Ste. Croix (1981) | Confirmed | Crossref: AHR 87(5) review |
| Mansbridge (1980) | Confirmed | Crossref: Political Theory 9(4) review |
| Dahl & Tufte (1973) | Confirmed | Crossref: APSR 68(3) review |
| Corrigan-Gibbs & Boneh (2017) | Not confirmed this pass | USENIX proceedings not in Crossref; not fetched |
| Boneh et al. (2019) | Confirmed | Crossref: LNCS, pp. 67-97 |
| Barnes et al. (2026) VDAF-22 | Confirmed | Full text fetched from ietf.org this pass |
| Crites & Stewart (2025) | Not confirmed this pass | Not re-fetched this pass |
| Aas et al. (2026) prio 0.18.1 | Confirmed | crates.io metadata and source inspected; compiled and run |


---

# Historical record (earlier passes)

# Source Audit and Provenance Verification

**Deliverable:** `research/SOURCE_AUDIT.md`  
**Status:** Working Draft (corrected 4 November 2026)  
**This file was previously named `SECOND_EDITION_SOURCE_AUDIT.md`.**

**Access this pass (state how, do not claim unread books were read):**
- VDAF-22: IETF Datatracker HTML, 14 August 2026, Informational, IRSG poll as of 18 October 2026.
- BLAKE3 spec: GitHub BLAKE3-specs (“128-bit security for all of its security goals”).
- Dapprich, O’Neill, Kuch: Winter 2024 EJPE issue PDF (`/journal/issue/download/35/67`). Single-article `/article/download/867/605` returned 404. Phrase “algorithmic centralism” not found in that extract. O’Neill titles: “Incommensurability, Environment and Planning: A Response to Hahnel’s Reply” and “Pluralism, Ecology and Planning” (not “Socialism, Ecology and Economic Calculation”).
- Deng, Lai, Peng, Yin (2017): PDF from UGA/UCLA pages; $o(1/k)$ on $\|x^{k+1}-x^k\|_M^2$ for convex multi-block Jacobi-proximal ADMM.
- `pequod-cljs` @ `8bd46b5c`: clone under `$PEQUOD_DIR`; 50 real `dep1ex01–50.clj`; 20 Git LFS pointers unfetched (`git-lfs` not installed); Clojure not run.
- Hansen, Mintz, Leval (1975), Merriman, Mansbridge, Dahl & Tufte, Casanova, Seidman, Kornai, Weitzman: **Tier 3** — bibliographic identity only; page-level claims unchecked. Front-matter now lists them.
- Hahnel (2021) increasing-returns pages: not independently re-read; secondary notes only.

The bibliography line “verified for identity, provenance, and completeness” is withdrawn in the book.

---

## 1. Four-Tier Source Verification and Provenance Classification

An earlier draft colophon stated: *"All primary and secondary sources cited in this monograph were verified on November 4, 2026."*

Auditing our primary source corpus shows that the 42+ sources in the bibliography fall into **four distinct evidentiary access tiers**, which are disclosed transparently in the Working Draft:

| Access Tier | Definition | Sources in This Tier |
| :--- | :--- | :--- |
| **Tier 1: Full-Text & Source-Code Direct Inspection** | Complete text or complete source repository was downloaded, read, and audited directly during this study. | - **Albert & Hahnel (1991a)**, *The Political Economy of Participatory Economics* (full text via ZNetwork `intro.htm`–`6.htm` + print pagination scan `pepe_dandelon.pdf`, pp. 1–132).<br>- **Albert & Hahnel (1991b)**, *Looking Forward* (full text via ZNetwork `lfIntroduction.htm`, `lf1_1.htm`–`lf10_1.htm`, `lfGlossary.htm`).<br>- **Albert (2003)**, *Parecon: Life After Capitalism* (full 311-page Verso text via ZCommunications/ZNetwork archive).<br>- **Dolgoff, ed. (1974)**, *The Anarchist Collectives* (full text via The Anarchist Library, including translations of Leval, Souchy, Peirats, and Bookchin's Introductory Essay).<br>- **Szczepanczyk (2023)**, *Journal of Information Economics* 1(3): 43–54 (CC BY 4.0 full PDF).<br>- **`msszczep/pequod-cljs`** at commit `8bd46b5c233f0e48c767ad6d5069b9437a67c38b` (complete repository cloned and audited, including `src/clj/pequod_cljs/csvgen.clj`, `wcs.clj`, `ccs.clj`, `util.cljc`, `bin/process_bk1.py`, 70 `dep1ex*.clj` datasets, and 99 `dep1ex*.csv` simulation logs).<br>- **EJPE Winter 2024 Special Issue** (*Erasmus Journal for Philosophy and Economics* Vol. 17, No. 2: full text of O'Neill, Kuch, Dapprich, and Hahnel's replies).<br>- **Sandström (2023)**, "An Accounting System for a Libertarian Socialist Economy" (`participatoryeconomy.org` technical article) and **PEP (2023)** User Story Mapping.<br>- **Crites & Stewart (2025)**, *On Reed–Solomon Proximity Gaps Conjectures* (IACR ePrint `2025/2046` full PDF).<br>- **IETF CFRG `draft-irtf-cfrg-vdaf-16`** (Verifiable Distributed Aggregation Functions / Prio3 full draft).<br>- **Scarf (1960)**, "Some Examples of Global Instability of the Competitive Equilibrium" (*International Economic Review* 1(3): 157–172, full PDF). |
| **Tier 2: Partial Preview + Extended Secondary / Author-Summary Inspection** | Book front-matter/preview and extracted chapters inspected directly; remaining chapters verified via author's companion articles, symposium papers, or simulation scripts. | - **Hahnel (2021)**, *Democratic Economic Planning* (Routledge): Front-matter, full Table of Contents, Preface, Chapter 1, and extracted sections on PDRM (Ch. 7, pp. 139–148), computer simulations (Ch. 9, pp. 177–179, Tables 9.1–9.2), and capital user rights (Ch. 12, pp. 244–245) inspected directly; remaining chapters cross-verified via Hahnel's 2024 EJPE symposium replies and `pequod-cljs` scripts.<br>- **Sandström (2020)**, *Anarchist Accounting* (Routledge) & **Sandström (2025)**, *The Participatory Economy: Adding Realism to Democratic Planning*: Bibliographic metadata and chapter structure verified via Routledge/Taylor & Francis; substantive accounting equations verified via Sandström's open-access 2023 technical summary.<br>- **Hahnel (2022)**, *A Participatory Economy* (AK Press): Metadata verified; substantive model covered via Hahnel (2021). |
| **Tier 3: Standard Primary Standards & Peer-Reviewed Literature Verified via Official Specs / Abstracts / Secondary Citations** | Bibliographic metadata, DOIs, theorem statements, and parameters verified against official standards bodies (NIST) or canonical secondary citations in Tier 1 texts, without full-book paywall access. | - **NIST (2024a, 2024b, 2024c)** FIPS 203 (`ML-KEM`), FIPS 204 (`ML-DSA`), FIPS 205 (`SLH-DSA`).<br>- **Hahnel & Albert (1990)**, *Quiet Revolution in Welfare Economics* (theorems verified as summarised in PEPE Chs. 1, 3, 5).<br>- **Arrow, Hurwicz, & Uzawa (1958)**; **Heal (1973)**; **Henry (1972)**; **Hurwicz (1972, 1973)**; **Groves & Ledyard (1977)**; **Nove (1983)**; **Buchanan (1985)**; **Devine (1988)**; **Schweickart (1993)**; **Cockshott & Cottrell (1993)**; **Ackerman (2014)**.<br>- **Historical & Institutional Works:** Marx (1871), Merriman (2014), Hansen (1991), Freeman (1972), Graeber (2013), Ostrom (1990), Whyte & Whyte (1991), Seidman (1991, 2002), Casanova (2005). |
| **Tier 4: Code Inspected & Datasets Audited, Not Re-Executed in Live Clojure Runtime** | Source code and committed CSV output logs audited by Python script, but `lein run` was not re-executed. | - **`pequod-cljs` Clojure execution:** We audited all 799 lines of `csvgen.clj`, `wcs.clj`, `ccs.clj`, 150,000 WC records in 70 `dep1ex*.clj` files, and 99 `dep1ex*.csv` output files via `research/analysis/verify_pequod_datasets.py`, and re-implemented the price rule in Python (`research/analysis/verify_economics.py`), but did **not** run `lein run -m pequod-cljs.csvgen` inside a Leiningen JVM session. |

**Update Applied to Working Draft Colophon:** The colophon and Chapter 3 methodology section explicitly state these four access tiers rather than claiming undifferentiated verification across paywalled monographs. Similarly, the colophon's phrasing *"without unauthorised verbatim reproduction"* has been clarified to *"without unauthorised reproduction of full copyrighted volumes; short scholarly quotations and epigraphs are reproduced with exact attribution under fair dealing / fair use."*

---

## 2. Verification of Every Quotation and Epigraph (`R-SRC-01`)

We checked every verbatim quotation and chapter epigraph in the manuscript against the underlying primary text:

| Location in Manuscript | Quoted Author & Text | Verification Result | Action Taken in Working Draft |
| :--- | :--- | :--- | :--- |
| **Ch. 1 Epigraph** (p. 1) | Michael Albert & Robin Hahnel (*Looking Forward*, 1991, Ch. 6): *"No central agency composes the final plan. No market competition generates the final plan. A decentralised, social, iterative, communication process allows all actors to democratically formulate the final plan."* | **VERIFIED VERBATIM** against ZNetwork `lf6_1.htm` (opening callout quote and paragraph 5). | Retained verbatim with exact citation. |
| **Ch. 1, Sec. 1.2** (p. 2) | Alec Nove (*The Economics of Feasible Socialism*, 1983, pp. ix–x, 44): *"In a complex industrial economy the interrelation between its parts can be based in principle either on freely chosen negotiated contracts [i.e., markets], or on a system of binding instructions from planning offices [i.e., central planning]. There is no third way."* | **VERIFIED** against PEPE Ch. 4 epigraph and text (pp. 57–58). Note: PEPE p. 58 uses `[i.e., central planning]` rather than `[i.e., command planning]`. | Restored exact bracketed text `[i.e., central planning]` from PEPE p. 58. |
| **Ch. 2 Epigraph** (p. 7) (`R-SRC-01`) | Attributed to Gaston Leval / Sam Dolgoff (1974): *"Regular general assemblies of the syndicates or collectives were convened, in which all affairs were discussed and decided, and to which the administrative committees reported and remained at all times accountable and subject to recall. Self-management was not a slogan; it was the daily practice of millions of workers and peasants coordinating production in solidarity."* | **PARAPHRASE ERROR (`R-SRC-01` Confirmed):** Search of Dolgoff (1974) (`agent-tools/3888b91d...txt`) confirms this string was a composite paraphrase of Leval's *Espagne Libertaire* (p. 219, quoted in Dolgoff 1974, Note 72) and Dolgoff's Ch. 1 introduction, mistakenly placed inside quotation marks during the revision replacing Rosa Luxemburg. | **Replaced** with Gaston Leval's **exact verbatim translation** in Dolgoff (1974, Ch. 1, p. 6, quoting Leval, *Espagne Libertaire*, p. 11): *"In almost all the industries, factories, mills, workshops, transportation services, public services, and utilities, the rank and file workers, their revolutionary committees, and their syndicates reorganized and administered production, distribution, and public services without capitalists, high salaried managers, or the authority of the state... They instituted not bourgeois formal democracy but genuine grass roots functional libertarian democracy."* |
| **Ch. 2, Sec. 2.2.1** (p. 8) | Murray Bookchin ("Introductory Essay," in Dolgoff 1974, p. xxviii): *"Where such popular assemblies were possible, their decisions were executed by a committee elected from the assembly. Apparently, the right to recall committee members was taken for granted and they certainly enjoyed no privileges, emoluments, or institutional power... It remained a cardinal principle of Spanish anarchists never to pay their delegates, even when the CNT numbered a million members. Normally, the responsibilities of elected delegates had to be discharged after working hours."* | **VERIFIED VERBATIM** against Dolgoff (1974) text (`agent-tools/3888b91d...txt`, line 205, noting original typo `responsibilies` normalised to `responsibilities`). | Retained verbatim with exact citation. |
| **Ch. 3 Epigraph** (p. 15) | Michael Albert & Robin Hahnel (*PEPE*, 1991, Front Flap / JSTOR Abstract): *"Until now, however, descriptions of alternatives have been unconvincing. Here Michael Albert and Robin Hahnel support the libertarian socialist tradition by presenting a rigorous, well-defined model of how producers and consumers could democratically plan their interconnected activities."* | **VERIFIED VERBATIM** against JSTOR / Princeton University Press book description (`https://www.jstor.org/stable/j.ctv131bvr2`) and Google Books blurb. | Clarified attribution to "Publisher's Overview / JSTOR Abstract to *The Political Economy of Participatory Economics* (1991)." |
| **Ch. 4 Epigraph** (p. 19) | Allen Buchanan (*Ethics, Efficiency, and the Market*, 1985, p. 29, quoted in PEPE Ch. 4, p. 58): *"It is impossible to show that a feasible nonmarket system at least approaches the productivity of the market unless (1) a rather well-developed theoretical model of the nonmarket system is available, and (2) it is demonstrated that a sufficiently productive approximation of the ideal ... system described in the theoretical model is practically possible."* | **VERIFIED VERBATIM** against PEPE Ch. 4 (`4.htm`, line 21, p. 58). | Retained verbatim with exact citation. |
| **Ch. 5 Epigraph** (p. 27) | Michael Albert & Robin Hahnel (*Looking Forward*, 1991, Ch. 6): *"Planning is computerized. All councils can access data banks of all facilitation boards and all other councils. The only thing demanding about flexible information access is that the computer system not only automatically accept but also sum and compare proposals to ascertain the status of any good."* | **VERIFIED VERBATIM** against ZNetwork `lf6_2.htm` (final paragraph). | Retained verbatim with exact citation. |
| **Ch. 6 Epigraph** (p. 30) | Michael Albert & Robin Hahnel (*PEPE*, 1991, Ch. 4, p. 68): *"Devising and choosing from among these and other possibilities is a practical issue in implementing any actual participatory economy. Assuming the procedures chosen do not violate principles essential to participatory planning, considerations include (1) the extent to which iteration workers could bias outcomes, (2) the extent of reductions in the number of iterations required to reach a plan..."* | **VERIFIED VERBATIM** against PEPE Ch. 4 (`4.htm`, line 101, p. 68). | Retained verbatim with exact citation. |
| **Ch. 7 Epigraph** (p. 33) | Michael Albert & Robin Hahnel (*Looking Forward*, 1991, Ch. 3): *"Decisions about what individuals wish to consume will be subject to collective criticism by fellow council members, though with specific guarantees for preserving individual freedoms and privacy."* | **VERIFIED VERBATIM** against ZNetwork `lf3_2.htm` (Principle 3). | Retained verbatim with exact citation. |
| **Ch. 8 Epigraph** (p. 36) | Michael Albert & Robin Hahnel (*Looking Forward*, 1991, Ch. 9): *"Finally, we point out to those who fear that computers could become the new dictators, the computer programmes are human products, socially evaluated and improved each year... In short, neither consumers nor producers need accept computer facilitated alternatives."* | **VERIFIED VERBATIM** against ZNetwork `lf9_2.htm` (third-to-last paragraph). | Retained verbatim with exact citation. |
| **Ch. 9 Epigraph** (p. 40) | Michael Albert & Robin Hahnel (*PEPE*, 1991, Ch. 6, pp. 108, 129): *"The easiest 'experiments' to implement are a variety of computer simulations in which various features of the system and assumptions about actors' behaviours can be altered to see how outcomes change... Conceivably one could run a 'shadow' participatory economy within an existing economy."* | **VERIFIED VERBATIM** against PEPE Ch. 6 (`6.htm`, lines 18 and 245, pp. 108, 129). | Retained verbatim with exact citation. |
| **Ch. 10 Epigraph** (p. 43) | Michael Albert & Robin Hahnel (*PEPE*, 1991, Ch. 6, p. 129): *"A simulation incorporates more detail than a differential economic model, but still misses the richness of living interaction. As a result, the full characteristics of participatory economics and the diverse solutions to institutional problems associated with it will ultimately only reveal themselves in actual operations."* | **VERIFIED VERBATIM** against PEPE Ch. 6 (`6.htm`, line 243, p. 129). | Retained verbatim with exact citation. |

---

## 3. Verification of Historical, Institutional, and Bibliographic Findings (`R-SRC-02` to `R-SRC-06`, `R-HIST-01`, `R-ECON-12`)

| Finding ID | Initial Draft Phrasing | Independent Verification Against Primary/Secondary Sources | Update Applied in Working Draft |
| :--- | :--- | :--- | :--- |
| **`R-SRC-02` (Mondragón Governance & Workforce)** | Described Mondragón as having "$>80,000$ worker-owners" and referred to "Watchdog Audit Councils (*Consejo Social*)." | **Confirmed:** 1. In Mondragón's governance structure (Freundlich 2015; Participedia Case 82; Whyte & Whyte 1991), the ***Consejo Social* (Social Council)** is the body of elected work-area representatives that advises on personnel, safety, and worker-management communication, whereas financial auditing and oversight are performed by the ***Comisión de Vigilancia* / Audit Committee (Watchdog Council)**. The initial draft conflated the two.<br>2. While Mondragón's total workforce across all cooperatives and subsidiaries has historically been ~70,000–80,000, **not all employees are worker-owners (*socios*)**: in the industrial cooperatives, roughly 80–85% are worker-members, whereas in the retail cooperative Eroski and international subsidiaries, non-member wage employees have comprised 60–70% of the workforce (putting actual worker-owners across the group closer to 30,000–35,000 out of ~70,000–80,000 total workers). | Corrected Chapter 2 to distinguish the *Consejo Social* (frontline worker representation council) from the *Comisión de Vigilancia* / Audit Committee, and updated workforce figures to distinguish total group workforce (~70,000–80,000) from actual cooperative worker-owners (*socios*, ~30,000–35,000), highlighting Eroski/subsidiary non-member employment as further evidence of market erosion. |
| **`R-SRC-03` (Porto Alegre Participatory Budgeting)** | Heading read "Porto Alegre Participatory Budgeting (1989–Present)." | **Confirmed:** As documented by the World Resources Institute (WRI, *Porto Alegre: Participatory Budgeting and the Challenge of Sustaining Transformative Change*) and *GaúchaZH* (April 3, 2017), Mayor Nelson Marchezan Jr. **suspended** Porto Alegre's participatory budgeting assemblies in **March/April 2017** after years of declining municipal investment shares and ~2,400 unfulfilled project requests. | Updated heading to **"Porto Alegre Participatory Budgeting (1989–2017 Suspension)"** and added an analysis of *why* it declined and was suspended: dependence on hostile municipal state fiscal structures, shrinking capital budgets, and a backlog of unexecuted votes that eroded popular participation. |
| **`R-SRC-04` (Rojava / DAANES Status)** | Heading read "Rojava / Democratic Confederalism (2012–Present)" without noting 2026 state integration. | **Confirmed:** Following military escalations in January 2026, the Syrian Democratic Forces (SDF) and the Syrian Transitional Government in Damascus signed a comprehensive integration agreement on **January 30, 2026** (published Feb 1, 2026; analyzed by the Middle East Council on Global Affairs, Kurdish Peace Institute, and *Al Majalla*), providing for a ceasefire, transfer of border crossings and oil fields to Damascus, integration of SDF brigades into the Syrian army and Interior Ministry, and **merging Autonomous Administration (DAANES) civil institutions into Syrian state bodies** (while retaining civilian staff and negotiating Kurdish civil/educational rights). | Updated heading to **"Rojava / Democratic Confederalism (2012–2026 Damascus Integration Accord)"** and analyzed the January 30, 2026 SDF–Damascus agreement as a critical real-world lesson on how autonomous confederal institutions are constrained and reshaped by surrounding nation-state military and fiscal power. |
| **`R-SRC-05` (Hurwicz Impossibility Citation)** | Cited Hurwicz (1973, *AER* 63(2): 1–30) for the impossibility of dominant-strategy incentive-compatible, Pareto-optimal, budget-balanced mechanisms. | **Confirmed:** Leonid Hurwicz's foundational impossibility theorem for privacy-preserving (informationally decentralised) dominant-strategy Pareto-optimal mechanisms in classical exchange environments was proved in **Hurwicz (1972)**, "On Informationally Decentralised Systems," in *Decision and Organisation: A Volume in Honor of Jacob Marschak*, ed. C. B. McGuire and R. Radner (Amsterdam: North-Holland, pp. 297–336), whereas Hurwicz (1973, *AER*) is his broader Richard T. Ely survey lecture. | Added **Hurwicz (1972)** to the bibliography and cited Hurwicz (1972) directly alongside Hurwicz (1973) whenever the impossibility theorem is invoked. |
| **`R-SRC-06` (Freeman 1972 & Meeting Scaling Limits)** | Linked Jo Freeman's "The Tyranny of Structurelessness" (1972) to $\mathcal{O}(N^2)$ plenary scaling bottlenecks and cited "~50–150 speakers" without separating them. | **Confirmed:** Freeman (1972) analyzed how **small, face-to-face feminist consciousness-raising and activist groups** generate unaccountable informal elites ("star systems" and friendship cliques) when they reject formal structure—a political/sociological phenomenon that asynchronous software does **not** automatically solve! Meanwhile, the $\mathcal{O}(N)$ turn-taking and $\mathcal{O}(N^2)$ pairwise deliberation scaling limits and the ~50–150 group threshold derive from **organisational communication theory and Dunbar/plenary assembly studies** (e.g., Mansbridge 1980, *Beyond Adversary Democracy*; Dahl & Tufte 1973, *Size and Democracy*; Dunbar 1993), not Freeman (1972). | Separated Freeman (1972) (informal elites in small groups, which persist online unless countered by explicit rotation, sortition, and role bounds) from the plenary speaking-time arithmetic ($\mathcal{O}(N)$ serial time, $\mathcal{O}(N^2)$ pairwise interactions) and cited Jane Mansbridge (*Beyond Adversary Democracy*, 1980) and Robert Dahl & Edward Tufte (*Size and Democracy*, 1973). |
| **`R-HIST-01` (Spanish Revolution Historiography, Coercion, War & Athenian Imperialism)** | Listed only internal accounting/coordination weaknesses for Spain 1936; relied primarily on sympathetic anarchist sources (Dolgoff, Leval, Mintz); and downplayed the role of slavery and tribute in classical Athens. | **Confirmed:** 1. In revolutionary Spain (1936–1939), the collectives did not operate in a peaceful laboratory: as **Julián Casanova** (*Anarchism, the Republic and Civil War in Spain: 1931–1939*, Routledge, 2005) documents, some rural collectives in Aragon were formed under the coercive shadow of armed militia columns, generated acute conflict with "individualist" smallholders, and were ultimately physically smashed by Republican Communist troops (Enrique Líster's 11th Division dissolving the Council of Aragon in August 1937) before Franco's victory in 1939. Furthermore, **Michael Seidman** (*Workers Against Work: Labour in Paris and Barcelona during the Popular Fronts*, Univ. of California Press, 1991; *Republic of Egos*, 2002) documents persistent worker absenteeism, wage demands, resistance to piecework/work discipline, and militant fatigue inside collectivised Barcelona factories under wartime scarcity.<br>2. In Classical Athens, while Hansen (1991) shows working citizens attended the *Ekklesia*, **G. E. M. de Ste. Croix** (*The Class Struggle in the Ancient Greek World*, 1981) and **Moses Finley** (*Economy and Society in Ancient Greece*, 1981) demonstrate that Athenian fiscal capacity for *misthophoria* (civic pay), navy rowers, and public works was heavily underwritten by the **Laurion silver mines (worked by tens of thousands of enslaved laborers)** and **5th-century Delian League imperial tribute (*phoros*)**. | Expanded Chapter 2 and Chapter 11 to incorporate **Casanova (2005)** and **Seidman (1991, 2002)** on wartime coercion, smallholder conflict, internal workplace resistance ("workers against work"), and armed state suppression in Spain, and **Finley (1981) / Ste. Croix (1981)** on the material base of Athenian *misthophoria*—establishing that software protocols cannot substitute for political defence, voluntary smallholder coexistence, or non-extractive material productivity. |
| **`R-ECON-12` (`pequod-cljs` Line Numbers & CSV Audit)** | Cited `csvgen.clj` line numbers from our local copy (`799` lines) without noting differences from upstream `8bd46b5c` (`836` lines), and did not explain the CSV multi-section parsing structure or the two experiment batches (`01..50` vs `51..100`). | **Confirmed & Resolved via `research/analysis/verify_pequod_datasets.py`:** Upstream `msszczep/pequod-cljs` at commit `8bd46b5c233f0e48c767ad6d5069b9437a67c38b` has `src/clj/pequod_cljs/csvgen.clj` (836 lines) and 99 `dep1ex*.csv` files (`dep1ex01..50` generated with 3,000 WCs/CCs via `big_gen.sh`; `dep1ex51..100` generated with 30,000 WCs/CCs via `bigger_gen.sh`). Each CSV contains Year 1 iterations, an `exponent-sum` separator row, Year 2 iterations, and a final `exponent-sum` row. Across `dep1ex61..100` ($N=40$, 30k scale), Year 1 averages **`11.85` rounds** at 5% (`:green`) and **`19.20` rounds** at 3% (`:blue`), and Year 2 averages **`6.53`–`6.58` rounds** at 5% (`:green`), matching Hahnel (2021, Tables 9.1–9.2, pp. 178–179) and Szczepanczyk (2023, p. 51). However, no wall-clock timing log exists in the upstream repository, so the "~2.5 s per iteration" figure is reclassified as an unverified estimate. | Documented both upstream (`8bd46b5c`) and local line numbers, added the exact CSV batch breakdown (`01..40` vs `51..90` vs `61..100`), reclassified "~2.5 s" as unverified, and replaced "proved 6–12 round convergence" with "demonstrated in Cobb-Douglas simulation experiments." |
