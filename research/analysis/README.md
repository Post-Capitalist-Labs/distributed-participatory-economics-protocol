# Analysis scripts

Every figure the monograph attributes to a script comes from this directory. `parameters.py` is the single source of derived constants. All Python scripts use the standard library only and run from the repository root.

## Inputs

- `pequod-cljs` at `8bd46b5c233f0e48c767ad6d5069b9437a67c38b`. Twenty `dep1ex*.clj` generators (`dep1ex51`, `dep1ex60–78`) are Git LFS objects of about 160 MB each. Without `git-lfs`, fetch them from the media endpoint and check each against the SHA-256 in its pointer:

  ```bash
  git clone https://github.com/msszczep/pequod-cljs && cd pequod-cljs
  git checkout 8bd46b5c233f0e48c767ad6d5069b9437a67c38b
  cd src/clj/pequod_cljs
  for f in dep1ex51.clj dep1ex6{0..9}.clj dep1ex7{0..8}.clj; do
    oid=$(grep oid "$f" | cut -d: -f2)
    curl -sSL -o "$f.tmp" "https://media.githubusercontent.com/media/msszczep/pequod-cljs/8bd46b5c233f0e48c767ad6d5069b9437a67c38b/src/clj/pequod_cljs/$f"
    [ "$(shasum -a 256 "$f.tmp" | cut -d' ' -f1)" = "$oid" ] && mv "$f.tmp" "$f" || echo "retry $f"
  done
  ```

- Network access only for `audit_bibliography.py` (Crossref API) and for building `bench_prio3`.

## Commands

```bash
# Reviewer's reference tests A-C, verbatim (seconds)
python3 research/analysis/reference_tests_r3.py

# Third-pass checks: success measures, Algorithm 3b vs Deng Alg. 4, Table 6.1
# rescoring and perturbation, Prio3 sizes (checked against the benchmark),
# proposal sizes, Layer-1 units, budget per FTE-year -> r3_verification_results.json
python3 research/analysis/verify_r3.py

# Second-pass checks still cited by the book (Shapley-Folkman sweep, committee
# binomials, pequod CSV subsets) -> r2_verification_results.json
PEQUOD_DIR=/path/to/pequod-cljs/src/clj/pequod_cljs python3 research/analysis/verify_r2.py

# Scarf, single plant, numeraire -> econ_verification_results.json
python3 research/analysis/verify_economics.py

# Toothache exponents over all 70 generators, CSV statistics -> pequod_dataset_audit.json
PEQUOD_DIR=/path/to/pequod-cljs python3 research/analysis/verify_pequod_datasets.py

# Book consistency: labels/refs, bibliography <-> citations, reviewer-voice
# phrases, script figures present in the book (exit 1 on failure)
python3 research/analysis/check_book.py

# Bibliography identity check against Crossref (about 7 minutes; network)
python3 research/analysis/audit_bibliography.py > bibliography_audit.txt

# Prio3SumVec benchmark (Rust; about 1 minute at ITERS=30)
cargo run --release --manifest-path research/analysis/bench_prio3/Cargo.toml \
  > research/analysis/bench_prio3/results_<machine>.jsonl
```

`verify_security_and_scoring.py` still contains n=64 figures and is not quoted by the book. `verify_r2.py`'s architecture-sensitivity block uses the second-pass Table 6.1 cells and is superseded by `verify_r3.py` section C.

## Expected output (this pass)

`reference_tests_r3.py`:

```text
Test A: first D<=S at round 3: p=11.52 S=100 D=58.48, unused 42%
Test B as_printed linear: max|resid|=0.9998, lambda 0.000..2.000
Test B with_resid linear: max|resid|=0.0000, lambda 1.000..1.000
Test B as_printed log   : max|resid|=0.0000, lambda 0.667..0.667
Test B with_resid log   : max|resid|=0.0000, lambda 0.667..0.667
Test C baseline: A=3.10 B=3.58 C=2.54 D=4.32
Test C A beats D on criteria: [11, 13]
Test C 70% weighting: A=4.08 B=3.75 C=2.30 D=4.32
Test C harsher D: A=3.10 B=3.58 C=2.54 D=3.92
```

Test C uses the second-pass Table 6.1 cells. (B's exact score is 3.585, which the book rounds to 3.59 and Python prints as 3.58.)

Key `verify_r3.py` results:

| Check | Result |
|---|---|
| Single plant: first feasible round, unused share, ever cleared? | 3, 41.5%, never |
| K=20 staggered: first feasible, first cleared, share of rounds cleared | 3 (8.4% unused), 5, 56.8% |
| Scarf: share of rounds feasible | 0% |
| Deng Alg. 4 with slack, linear welfare (tau=2.01, N=3) | violation 0, price 1.0 |
| Table 6.1 as printed (rescored D) baseline | A 3.095, B 3.585, C 2.535, D 4.065 |
| A overtakes D at weight on criteria 4/11/12 of | 0.63 (at 0.70: A 4.084, D 3.918) |
| Harsher D (rescored) | 3.82 |
| U(-1,1) perturbation, D first | 99.2%; median lead 0.498, 5th pct 0.151 |
| Prio3 leader share 3000x20 / 200x16 | 975,760 B / 54,896 B (upload 55,120 B) |
| Predicted vs libprio sizes (9 configs) | all match byte-for-byte |
| Layer-1 block / year at 425 blocks | 700,142 B / 297.6 MB (283.8 MiB) |
| Proposal sizes (WC 150 items, CC 200, CC 3000; 1 signer) | 5,637 / 6,237 / 39,837 B |
| Round archive at 10^6 (coarse 1 signer ... dense 5 signers) | 237.5 MB ... 1,459 MB |
| Budget reconciliation, programme total | $621k–$1,358k |

`verify_r2.py` (unchanged figures): Shapley–Folkman K=20, a=70: min 0.396%, last-100 max 8.38%; sweep median 6.01%, worst 9.47%, 24.4% of cases ≤5%. Committee n=128, p=0.20/0.25/0.30: 0.022% / 1.82% / 21.3%. `dep1ex61–100`: 11.85 / 19.20 / 6.575; `dep1ex01–50` Y1: 11.18.

`verify_pequod_datasets.py`: 70 generators, 750,000 worker-council records; baseline Σb + c/k ∈ [0.7696, 0.8781]; with the toothache increment, [1.0696, 1.6652].

## Benchmark (bench_prio3)

`prio` 0.18.1 (crates.io, 25 September 2026), which implements `draft-irtf-cfrg-vdaf-18` per its README. Results: `bench_prio3/results_m4pro.jsonl`, measured on an Apple M4 Pro (macOS 26.6.2), rustc and cargo 1.98.1, release profile with thin LTO, one core, 30 iterations, medians. `chunk_length` from `prio::vdaf::prio3::optimal_chunk_length`. These are desktop numbers; phones and Raspberry Pi boards will be slower by an unmeasured factor.

## Versions

- Python 3.9 (macOS Command Line Tools), standard library only. PyMuPDF and Pillow were used only to render PDF pages for inspection, not by these scripts.
- `pequod-cljs` `8bd46b5c`; Clojure/Leiningen not run.
- VDAF: `draft-irtf-cfrg-vdaf-22` text (14 August 2026); libprio implements draft 18.
- TeX: `tectonic` (Homebrew) for `book/dpep_book.tex`.
