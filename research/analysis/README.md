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

# Fourth refinement (technology stack): signature suites, phone traffic, Layer-1
# checkpoint sizes, archive sizes, S7 costs, K=2/3 upload, post-quantum anchoring
# options (S8); reproduces reference
# Test S first -> signature_suites_results.json
python3 research/analysis/verify_signature_suites.py

# Light-client sync committee sizes and capture probabilities -> sync_committee_results.json
python3 research/analysis/verify_sync_committee.py

# Signature-verification benchmark (Rust; about 30 s): Ed25519 (single and batch),
# ML-DSA-65, hybrid, aggregated BLS12-381 of 86 signers
cargo run --release --manifest-path research/analysis/bench_signatures/Cargo.toml \
  > research/analysis/bench_signatures/results_<machine>.json

# Prio3SumVec benchmark (Rust; about 1 minute at ITERS=30)
cargo run --release --manifest-path research/analysis/bench_prio3/Cargo.toml \
  > research/analysis/bench_prio3/results_<machine>.jsonl
```

`verify_security_and_scoring.py` still contains n=64 figures and is not quoted by the book. `verify_r2.py`'s architecture-sensitivity block uses the second-pass Table 6.1 cells and is superseded by `verify_r3.py` section C.

## Expected output (fourth refinement, 7 November 2026)

`verify_signature_suites.py`, section S1 (reference Test S, constants inline) reproduces the book as it stood before correction: hybrid block 700,142 B / 297.6 MB per year; Ed25519 415,568 B / 176.6 MB; aggregated BLS 410,176 B / 174.3 MB; coarse archives 237.5 / 787.4 MB and dense 909.5 / 1,459.4 MB (hybrid at 3,437 B per signer) against 102.6 / 112.8 / 774.6 / 784.8 MB (Ed25519).

Section S2 uses `parameters.py` with the corrected hybrid size (3,373 B = 3,309 + 64, RFC 10073):

| Quantity | Hybrid | Ed25519 | Aggregated BLS |
|---|---|---|---|
| Quorum signatures per checkpoint | 290,078 B | 5,504 B | 112 B |
| Checkpoint block | 700,142 B | 415,568 B | 410,176 B |
| Layer 1 per year (425 blocks) | 297.6 MB | 176.6 MB | 174.3 MB |
| Coarse archive, 1 / 5 signers | 234.9 / 774.6 MB | 102.6 / 112.8 MB | — |
| Dense archive, 1 / 5 signers | 906.9 / 1,446.6 MB | 774.6 / 784.8 MB | — |

Phone traffic per round (S3; price deltas 15–40 kB, 512 B inclusion path, plus a 55,120 B report at milestones): hybrid full check 305.6–330.6 / 360.7–385.7 kB (automated / milestone); Ed25519 full check 21.0–46.0 / 76.1–101.1 kB; aggregated BLS 15.6–40.6 / 70.7–95.7 kB; witnessed log with 11 Ed25519 cosignatures 16.4–41.4 / 71.5–96.5 kB, with ML-DSA-44 cosignatures 45.6–70.6 / 100.8–125.8 kB.

Section S8 (post-quantum history anchoring; SLH-DSA-SHA2-192s 16,224 B, ML-DSA-44 2,420 B + 12 B signed-note framing; 425 blocks a year):

| Option | Per anchor | Per year |
|---|---|---|
| Single federation SLH-DSA key (rejected) | 16,224 B | 6.90 MB |
| 3-of-5 federation SLH-DSA (proposed, BFT) | 48,673 B | 20.69 MB |
| 4-of-7 federation SLH-DSA | 64,897 B | 27.58 MB |
| 11-of-16 ML-DSA-44 witness cosignatures (proposed, log) | 26,752 B | 11.37 MB |
| Annual 3-of-5 SLH-DSA backstop (log) | 48,673 B | 0.05 MB |

Phones in the log design check only the Ed25519 cosignatures (11 × 76 = 836 B).

`verify_r3.py` section H (Table 6.1 with D under the tiered policy and D-log): baseline A 3.095, B 3.585, C 2.535, D 4.070, D-log 4.100; equal weights D 4.036, D-log 4.107; 70% on criteria 4/11/12: A 4.084, D 3.920, D-log 4.146; A overtakes D at 0.63 and D-log at 0.74; harsher cells D 3.79, D-log 3.745; perturbation wins D 44.4%, D-log 55.5%, B 0.08%. Budget: programme \$726k–\$1,553k; formal model \$20k–\$45k; K = 3 add-on \$40k–\$95k. `book_table_matches: true`.

`verify_sync_committee.py`: 24 members, quorum 16: 53,968 B hybrid (1,024 B Ed25519), capture probability 0.000172 at f = 42.

`bench_signatures` (Apple M4 Pro, 14 threads; rustc/cargo 1.98.1; ed25519-dalek 3.0.0, blst 0.3.17, libcrux-ml-dsa 0.0.11; run 7 November 2026): Ed25519 17.27 µs single, 8.71 µs batched (64); ML-DSA-65 32.19 µs, signature 3,309 B; hybrid 49.46 µs; 200,000 signatures on one core: Ed25519 batched 1.74 s, ML-DSA 6.44 s (extrapolated), hybrid 9.89 s (extrapolated); ML-DSA 200,000 on all cores 0.66 s; aggregated BLS of 86 signers 0.45 ms, single BLS 0.43 ms. Results in `bench_signatures/results_m4pro.json`. Desktop numbers only.

## Expected output (third refinement)

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
