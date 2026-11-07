#!/usr/bin/env python3
"""Signature-suite sizing and the costs that depend on it (fourth refinement).

    python3 research/analysis/verify_signature_suites.py

Sections
  S1  Reference Test S as supplied with the external review (constants inline), to show
      that its hybrid rows reproduce the book as it stood: 700,142 B block; 237.5 / 787.4 /
      909.5 / 1,459.4 MB archives. Those rows use 3,437 B per council signer.
  S2  The same quantities from parameters.py with the corrected hybrid size (3,373 B =
      3,309 B ML-DSA-65 + 64 B Ed25519, RFC 10073 concatenation), for three suites:
      all-hybrid, Ed25519, aggregated BLS12-381 (checkpoints only).
  S3  Per-round phone traffic for each light-client option and signature policy.
  S4  Witnessed-log checkpoints (C2SP signed-note cosignatures, Ed25519 or ML-DSA-44).
  S5  Server verification load per round, from bench_signatures/results_m4pro.json.
  S6  Intra-year fulfilment (S7): per-person daily signature and byte cost by option.
  S7  Household aggregation with two or three aggregators: upload size.
  S8  Post-quantum history anchoring: one SLH-DSA key, k-of-n SLH-DSA by federations,
      ML-DSA-44 witness cosignatures; bytes per anchored block and per year.

Writes signature_suites_results.json. Standard library only. SI units (1 kB = 1,000 B).
"""
from __future__ import annotations

import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import parameters as P  # noqa: E402

N_VAL = P.N_VALIDATORS
Q = P.QUORUM_CEIL_2N3                       # 86
G = P.G_CATALOGUE                           # 10,000
BLOCKS_PER_YEAR = P.CHECKPOINT_BLOCKS_PER_YEAR  # 425
N_WC = N_CC = P.M_COUNCILS_AT_1E6 // 2      # 20,000 each
WC_ITEMS, CC_COARSE, CC_DENSE = 150, P.G_COARSE, P.G_PRIV


# ---------------------------------------------------------------------------
def s1_reference_test_s() -> dict:
    """Reference Test S, verbatim constants (reproduces the pre-correction book)."""
    from math import ceil
    q = ceil(2 * 128 / 3)
    arrays = 5 * 10_000 * 8
    bitmap, roots = 10_000, 2 * 32
    hdr, item = 400, 12
    sig = {"hybrid_checkpoint": 3_373, "hybrid_council": 3_437, "ed25519": 64}
    bls_agg, val_bitmap = 96, 128 // 8

    def block(sb):
        return arrays + sb + bitmap + roots

    quorum = {"hybrid": q * sig["hybrid_checkpoint"], "ed25519": q * sig["ed25519"], "bls_agg": bls_agg + val_bitmap}
    out = {"quorum": {k: {"sig_bytes": v, "block_bytes": block(v), "year_MB": round(block(v) * 425 / 1e6, 1)} for k, v in quorum.items()}}

    def prop(items, signers, s):
        return hdr + items * item + signers * s

    arch = {}
    for cc, label in [(200, "coarse"), (3_000, "dense")]:
        for signers in (1, 5):
            hyb = 20_000 * (prop(150, signers, sig["hybrid_council"]) + prop(cc, signers, sig["hybrid_council"]))
            ed = 20_000 * (prop(150, signers, 64) + prop(cc, signers, 64))
            arch[f"{label}_{signers}"] = {"hybrid_MB": round(hyb / 1e6, 1), "ed25519_MB": round(ed / 1e6, 1), "ratio": round(hyb / ed, 2)}
    out["archive"] = arch
    return out


# ---------------------------------------------------------------------------
SUITES = {
    "hybrid": P.HYBRID_SIG_BYTES,           # 3,373
    "ed25519": P.ED25519_SIG_BYTES,         # 64
}


def round_archive(cc_items: int, signers: int, sig: int) -> int:
    return N_WC * P.proposal_bytes(WC_ITEMS, signers, sig) + N_CC * P.proposal_bytes(cc_items, signers, sig)


def s2_corrected() -> dict:
    quorum = {
        "hybrid": Q * P.HYBRID_SIG_BYTES,
        "ed25519": Q * P.ED25519_SIG_BYTES,
        "bls_agg_minpk": P.BLS_MINPK_SIG_BYTES + N_VAL // 8,
        "bls_agg_minsig": P.BLS_MINSIG_SIG_BYTES + N_VAL // 8,
    }
    checkpoints = {}
    for k, v in quorum.items():
        b = P.layer1_block_bytes(sigs=v)["total_bytes"]
        checkpoints[k] = {"quorum_sig_bytes": v, "block_bytes": b, "year_MB": round(b * BLOCKS_PER_YEAR / 1e6, 1)}
    proposals = {}
    for name, sig in SUITES.items():
        for label, items in [("wc150", WC_ITEMS), ("cc200", CC_COARSE), ("cc3000", CC_DENSE)]:
            for signers in (1, 5):
                proposals[f"{name}_{label}_{signers}"] = P.proposal_bytes(items, signers, sig)
    archives = {}
    for label, cc in [("coarse", CC_COARSE), ("dense", CC_DENSE)]:
        for signers in (1, 5):
            row = {}
            for name, sig in SUITES.items():
                a = round_archive(cc, signers, sig)
                row[f"{name}_MB_per_round"] = round(a / 1e6, 1)
                row[f"{name}_GB_per_year"] = round(10 * a / 1e9, 2)
            row["ratio_hybrid_over_ed25519"] = round(row["hybrid_MB_per_round"] / row["ed25519_MB_per_round"], 2)
            row["signature_verifications"] = (N_WC + N_CC) * signers
            archives[f"{label}_{signers}_signer"] = row
    # Table 9.3 rows (coarse, single key) by population scale
    scales = {100: (24, 30, 20), 1_000: (51, 80, 40), 10_000: (430, 500, 400), 100_000: (4_120, 2_000, 4_000), 1_000_000: (40_600, 10_000, 40_000)}
    t93 = {}
    for n, (m, g, props) in scales.items():
        row = {}
        for name, sig in SUITES.items():
            avg = (P.proposal_bytes(WC_ITEMS, 1, sig) + P.proposal_bytes(CC_COARSE, 1, sig)) / 2
            row[f"{name}_leaf_round_kB"] = round(props * avg / 1e3, 1)
            row[f"{name}_leaf_year_MB"] = round(10 * props * avg / 1e6, 2)
        for name, qs in [("hybrid", Q * P.HYBRID_SIG_BYTES), ("ed25519", Q * P.ED25519_SIG_BYTES), ("bls", P.BLS_MINPK_SIG_BYTES + N_VAL // 8)]:
            blk = 5 * g * 8 + qs + math.ceil(m * 2 / 8) + 2 * P.BLAKE3_DIGEST_BYTES
            row[f"{name}_L1_year_MB"] = round(BLOCKS_PER_YEAR * blk / 1e6, 1)
        t93[str(n)] = row
    return {"checkpoints": checkpoints, "proposals": proposals, "archives": archives, "table93": t93,
            "hybrid_sig_bytes": P.HYBRID_SIG_BYTES, "ml_dsa_65_sig_bytes": P.ML_DSA_65_SIG_BYTES,
            "double_counted_per_signer": P.HYBRID_SIG_BYTES_DOUBLE_COUNTED}


# ---------------------------------------------------------------------------
PRICE_DELTAS = (15_000, 40_000)    # book assumption: compressed price deltas per round
INCLUSION = 16 * 32                 # 512-B Merkle path
REPORT_K3 = P.prio3_report_bytes(P.G_COARSE, P.HRU_BITS, shares=3)["client_upload_bytes"]
REPORT_K2 = P.prio3_report_bytes(P.G_COARSE, P.HRU_BITS, shares=2)["client_upload_bytes"]
WITNESSES, WITNESS_QUORUM = 16, 11  # illustrative sortitioned witness set, 2/3 quorum


def s3_phone_traffic() -> dict:
    """Bytes per round for a phone: prices, inclusion path, checkpoint check, report at milestones."""
    checks = {
        "hybrid_full_86": Q * P.HYBRID_SIG_BYTES,
        "hybrid_coordinator_attestation": P.HYBRID_SIG_BYTES,
        "hybrid_sync_committee_24_q16": 16 * P.HYBRID_SIG_BYTES,
        "ed25519_full_86": Q * P.ED25519_SIG_BYTES,
        "bls_aggregate": P.BLS_MINPK_SIG_BYTES + N_VAL // 8,
        "log_ed25519_cosigs": WITNESS_QUORUM * P.COSIG_LINE_ED25519_BYTES + P.ED25519_SIG_BYTES,
        "log_mldsa44_cosigs": WITNESS_QUORUM * (P.ML_DSA_44_SIG_BYTES + 12) + P.HYBRID_SIG_BYTES,
    }
    out = {"check_bytes": checks}
    for k, c in checks.items():
        lo = PRICE_DELTAS[0] + INCLUSION + c
        hi = PRICE_DELTAS[1] + INCLUSION + c
        out[k] = {"automated_round_kB": [round(lo / 1e3, 1), round(hi / 1e3, 1)],
                  "milestone_round_kB": [round((lo + REPORT_K3) / 1e3, 1), round((hi + REPORT_K3) / 1e3, 1)]}
    return out


def s4_witnessed_log() -> dict:
    ckpt_body = 200  # origin line, tree size, root hash, extension lines (signed-note text, estimate)
    return {
        "witnesses": WITNESSES, "quorum": WITNESS_QUORUM,
        "checkpoint_plus_ed25519_cosigs_bytes": ckpt_body + P.ED25519_SIG_BYTES + WITNESS_QUORUM * P.COSIG_LINE_ED25519_BYTES,
        "checkpoint_plus_mldsa44_cosigs_bytes": ckpt_body + P.HYBRID_SIG_BYTES + WITNESS_QUORUM * (P.ML_DSA_44_SIG_BYTES + 12),
        "note": "Arrays (prices, totals) are served separately and bound by the totals root; a phone fetches deltas, not the full block.",
    }


def s5_verification_load() -> dict:
    path = os.path.join(HERE, "bench_signatures", "results_m4pro.json")
    if not os.path.exists(path):
        return {"error": "run bench_signatures first"}
    b = json.load(open(path))
    out = {"machine": "Apple M4 Pro, 14 threads (10P+4E)", "bench": b}
    for n in (40_000, 200_000):
        out[f"{n}"] = {
            "hybrid_single_core_s": round(n * b["hybrid_verify_us"] / 1e6, 2),
            "mldsa65_single_core_s": round(n * b["mldsa65_verify_us"] / 1e6, 2),
            "ed25519_single_core_s": round(n * b["ed25519_single_us"] / 1e6, 2),
            "ed25519_batch_single_core_s": round(n * b["ed25519_batch64_us"] / 1e6, 2),
        }
    return out


def s6_fulfilment() -> dict:
    """S7 per-person daily cost, two pickups a day (illustrative)."""
    pickups = 2
    payload = 120  # depot id, category, quantity, period, nonce (estimate)
    opts = {
        "a_attributed_receipts_ed25519": pickups * (payload + 2 * P.ED25519_SIG_BYTES),
        "a_attributed_receipts_hybrid": pickups * (payload + 2 * P.HYBRID_SIG_BYTES),
        "b_blind_tokens_bls": pickups * (32 + P.BLS_MINSIG_SIG_BYTES + payload),
        "b_blind_tokens_rsa2048": pickups * (32 + 256 + payload),
        "c_council_allocation_staples": 0,
    }
    return {"pickups_per_day": pickups, "bytes_per_person_per_day": opts,
            "per_year_MB_attributed_ed25519": round(365 * opts["a_attributed_receipts_ed25519"] / 1e6, 2),
            "per_year_MB_attributed_hybrid": round(365 * opts["a_attributed_receipts_hybrid"] / 1e6, 2)}


def s7_aggregators() -> dict:
    return {"coarse_upload_K3_bytes": REPORT_K3, "coarse_upload_K2_bytes": REPORT_K2}


def s8_anchoring() -> dict:
    """Bytes added per anchored Layer-1 block (425 a year) by each anchoring option."""
    slh = P.SLH_DSA_SHA2_192S_SIG_BYTES                 # 16,224 B
    mldsa44_line = P.ML_DSA_44_SIG_BYTES + 12           # signed-note cosignature: 4-B key hash + 8-B timestamp
    opts = {
        "single_federation_slh_dsa": 1 * slh,
        "slh_dsa_3_of_5_federations": 3 * slh + 1,       # + 1-byte signer bitmap
        "slh_dsa_4_of_7_federations": 4 * slh + 1,
        "mldsa44_cosigs_11_of_16": WITNESS_QUORUM * mldsa44_line,
        "annual_slh_dsa_3_of_5_backstop": 3 * slh + 1,   # once a year over the year's log root
    }
    out = {}
    for k, b in opts.items():
        per_year = b if k.startswith("annual") else b * BLOCKS_PER_YEAR
        out[k] = {"bytes_per_anchor": b, "kB_per_anchor": round(b / 1e3, 1), "MB_per_year": round(per_year / 1e6, 2)}
    # Phone cost: under the log design phones check only the Ed25519 cosignatures.
    out["phone_bytes_log_ed25519_cosigs"] = WITNESS_QUORUM * P.COSIG_LINE_ED25519_BYTES
    return out


def main():
    out = {
        "S1_reference_test_s": s1_reference_test_s(),
        "S2_corrected": s2_corrected(),
        "S3_phone_traffic": s3_phone_traffic(),
        "S4_witnessed_log": s4_witnessed_log(),
        "S5_verification_load": s5_verification_load(),
        "S6_fulfilment": s6_fulfilment(),
        "S7_aggregators": s7_aggregators(),
        "S8_anchoring": s8_anchoring(),
    }
    dest = os.path.join(HERE, "signature_suites_results.json")
    json.dump(out, open(dest, "w"), indent=2)
    print(json.dumps(out, indent=2))
    print(f"\nWrote {dest}", file=sys.stderr)


if __name__ == "__main__":
    main()
