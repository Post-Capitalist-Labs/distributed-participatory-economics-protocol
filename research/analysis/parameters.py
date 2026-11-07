"""
Single source of derived DPEP working-draft figures.

Every byte-count, committee, archive, and Prio3-size figure cited in the
monograph should be generated from these constants (or from a function below)
so a change such as n_validators = 64 -> 128 updates everywhere.
"""
from __future__ import annotations
import math

# ---------------------------------------------------------------------------
# Population / catalogue
# ---------------------------------------------------------------------------
N_PARTICIPANTS = 1_000_000
G_CATALOGUE = 10_000          # |Omega| priced categories at national scale
G_PRIV = 3_000                # private-consumption categories in household reports
S_ACTIVE_ITEMS = 50           # typical non-zero household items (sparse support)
M_COUNCILS_AT_1E6 = 40_000    # worker + consumer councils at N=10^6
PROPOSAL_BYTES_RAW = 5_200    # canonical CBOR sparse council proposal
PROPOSAL_BYTES_ZSTD = 1_500   # ~60 MB / 40k ≈ 1.5 KB compressed (book: 60 MB)

# ---------------------------------------------------------------------------
# Cryptography
# ---------------------------------------------------------------------------
ED25519_SIG_BYTES = 64
ML_DSA_65_SIG_BYTES = 3_309      # FIPS 204 Table 2 (confirmed: libcrux-ml-dsa 0.0.11 emits 3,309 B)
# Hybrid Ed25519 + ML-DSA-65: RFC 10073 composite = mldsaSig || tradSig (concatenation).
HYBRID_SIG_BYTES = ML_DSA_65_SIG_BYTES + ED25519_SIG_BYTES   # 3,373
# Until the fourth refinement, proposals used 3,437 B per signer: the 3,373-B hybrid
# plus a second Ed25519 signature (double count). Kept only to reproduce old tables.
HYBRID_SIG_BYTES_DOUBLE_COUNTED = HYBRID_SIG_BYTES + ED25519_SIG_BYTES  # 3,437
ML_DSA_44_SIG_BYTES = 2_420      # FIPS 204 Table 2; C2SP tlog-cosignature recommends ML-DSA-44
SLH_DSA_SHA2_192S_SIG_BYTES = 16_224
BLS_MINPK_SIG_BYTES = 96         # BLS12-381 min-pk: signature in G2 (blst; bench_signatures)
BLS_MINSIG_SIG_BYTES = 48        # BLS12-381 min-sig: signature in G1 (CometBFT bls12381 key type)
COSIG_LINE_ED25519_BYTES = 4 + 8 + 64   # C2SP signed-note cosignature: key hash + timestamp + Ed25519
ML_KEM_768_CT_BYTES = 1_120
BLAKE3_DIGEST_BYTES = 32
FIELD128_ENCODED_SIZE = 16    # VDAF-22 Table 4
XOF_SEED_SIZE = 32            # XofTurboShake128 in VDAF-22
PRIO3_SHARES = 3
PRIO3_PROOFS = 1
BITS_PER_ITEM = 20            # ceil(log2(max_measurement)); 2^20 micro-units ≈ 1.05 units
# 64-bit micro-units actually need 64 bits; BITS_PER_ITEM=20 is a lower bound used
# by the reviewer. We report both.

# ---------------------------------------------------------------------------
# Consensus / checkpoints
# ---------------------------------------------------------------------------
N_VALIDATORS = 128
F_BFT = (N_VALIDATORS - 1) // 3          # 42
QUORUM = 2 * F_BFT + 1                   # 85  (2f+1)
# Reviewer used 86 = ceil(2n/3). We report both 2f+1 and ceil(2n/3).
QUORUM_CEIL_2N3 = math.ceil(2 * N_VALIDATORS / 3)  # 86
PLANNING_ROUNDS_TABLE = 10               # tables 1.1 / 9.2 illustrative 10-round plan
PLANNING_ROUNDS_COST_FOOTNOTE = 20       # earlier cost footnote; do not mix
PLANNING_ROUNDS_KILL_GATE = 25           # Kill Gate 1 upper bound
DAILY_OPS_BLOCKS = 365
REPLAN_BLOCKS = 50
CHECKPOINT_BLOCKS_PER_YEAR = PLANNING_ROUNDS_TABLE + DAILY_OPS_BLOCKS + REPLAN_BLOCKS  # 425 at 10 rounds; 435 at 20

# ---------------------------------------------------------------------------
# Privacy / aggregation
# ---------------------------------------------------------------------------
M_MIN_BATCH = 30
M_WARD_RARE_GOODS = 250       # book previously mixed 250 and 500; canonical: 250
K_FEDERATED_AGGREGATORS = 3

# ---------------------------------------------------------------------------
# Derived helpers
# ---------------------------------------------------------------------------
def next_power_of_2(n: int) -> int:
    p = 1
    while p < n:
        p <<= 1
    return p


def optimal_chunk_length(meas_len: int) -> int:
    """Port of `prio::vdaf::prio3::optimal_chunk_length` (prio 0.18.1).

    Chooses chunk_length to minimise PROOF_LEN = 2*chunk + 2*(next_pow2(1+calls)-1)
    over gadget_calls of the form 2^k - 1. VDAF-22 Sec. 7.4.3 only RECOMMENDS a
    value "near the square root of length * bits"; libprio's choice is used here so
    predicted sizes can be checked byte-for-byte against bench_prio3.
    """
    if meas_len <= 1:
        return 1
    best = None
    max_log2 = (meas_len + 1).bit_length() - 1
    for log2 in range(max_log2, 0, -1):
        calls = (1 << log2) - 1
        chunk = -(-meas_len // calls)
        cost = 2 * chunk + 2 * (next_power_of_2(1 + calls) - 1)
        if best is None or cost < best[0]:
            best = (cost, chunk)
    return best[1]


def prio3_sumvec_proof_len(length: int, bits: int, chunk_length: int | None = None) -> int:
    """PROOF_LEN for Prio3SumVec (VDAF-22 Sec. 7.3 / 7.4.3, ParallelSum(Mul)).

    ParallelSum(Mul, chunk_length) has ARITY = 2*chunk_length and DEGREE = 2, so
    PROOF_LEN = 2*chunk_length + 2*(next_pow2(1 + calls) - 1) + 1.
    (The second-refinement version used ARITY = 2, which understated report sizes
    by about 1%; corrected in the third pass and checked against libprio.)
    """
    meas_len = length * bits
    if chunk_length is None:
        chunk_length = optimal_chunk_length(meas_len)
    gadget_calls = -(-meas_len // chunk_length)
    arity, degree = 2 * chunk_length, 2
    wire = next_power_of_2(1 + gadget_calls)
    gadget_poly = degree * (wire - 1) + 1
    return arity + gadget_poly


def prio3_report_bytes(length: int, bits: int = BITS_PER_ITEM, shares: int = PRIO3_SHARES,
                       chunk_length: int | None = None) -> dict:
    """
    Uncompressed Prio3SumVec report sizes from VDAF-22 Sec. 7.2.7.

    Leader (aggregator 0) receives the full measurement share + proof share.
    Helpers receive XOF seeds (plus joint-randomness blinds).
    Matches the encoded sizes measured with libprio 0.18.1 in bench_prio3/.
    """
    meas_len = length * bits
    proof_len = prio3_sumvec_proof_len(length, bits, chunk_length)
    F = FIELD128_ENCODED_SIZE
    S = XOF_SEED_SIZE
    leader_inner = F * meas_len + F * proof_len * PRIO3_PROOFS
    leader_share = leader_inner + S  # + blind (joint randomness)
    helper_share = S + S             # seed + blind
    public_share = S * shares        # joint_rand_parts
    helpers = shares - 1
    client_upload = public_share + leader_share + helpers * helper_share
    return {
        "length": length,
        "bits": bits,
        "meas_len": meas_len,
        "proof_len": proof_len,
        "leader_share_bytes": leader_share,
        "helper_share_bytes": helper_share,
        "public_share_bytes": public_share,
        "client_upload_bytes": client_upload,
        "leader_share_kib": round(leader_share / 1024, 1),
        "client_upload_kib": round(client_upload / 1024, 1),
        "client_upload_mib": round(client_upload / (1024 * 1024), 3),
    }


def quorum_sig_bytes(n: int = N_VALIDATORS, sig: int = HYBRID_SIG_BYTES) -> dict:
    f = (n - 1) // 3
    q_2f1 = 2 * f + 1
    q_ceil = math.ceil(2 * n / 3)
    return {
        "n": n,
        "f": f,
        "quorum_2f1": q_2f1,
        "quorum_ceil_2n3": q_ceil,
        "bytes_2f1": q_2f1 * sig,
        "bytes_ceil_2n3": q_ceil * sig,
        "kib_2f1": round(q_2f1 * sig / 1024, 1),
        "kib_ceil_2n3": round(q_ceil * sig / 1024, 1),
    }


def layer1_block_bytes(n: int = N_VALIDATORS, g: int = G_CATALOGUE, sigs: int | None = None) -> dict:
    """Layer-1 block: 5 FixedDecimal arrays + quorum signatures + 2-bit bitmap + two roots.

    `sigs` overrides the quorum-signature bytes (e.g. 86 x 64 for Ed25519, 96 + 16 for an
    aggregated BLS signature plus a 128-bit signer bitmap). Default: 86 hybrid signatures.
    """
    arrays = 5 * g * 8                         # 5 FixedDecimal arrays
    if sigs is None:
        sigs = quorum_sig_bytes(n)["bytes_ceil_2n3"]
    bitmap = math.ceil(M_COUNCILS_AT_1E6 * 2 / 8)  # 2 bits/council
    total = arrays + sigs + bitmap + 2 * BLAKE3_DIGEST_BYTES
    return {
        "arrays_bytes": arrays,
        "sigs_bytes": sigs,
        "bitmap_bytes": bitmap,
        "total_bytes": total,
        "kib": round(total / 1024, 1),
    }


# ---------------------------------------------------------------------------
# Third refinement: household reporting unit, coarse baseline, proposals, budget
# ---------------------------------------------------------------------------
PROTOCOL_SCALE = 1_000_000            # FixedDecimal micro-units per protocol unit
# With bits b at the fixed 10^-6 scale the largest reportable quantity is
# (2^b - 1) / 10^6 protocol units: b = 20 gives 1.048575 units, i.e. useless.
# Household reports therefore use a per-category Household Reporting Unit (HRU):
#   q_{u,g} in {0, ..., 2^HRU_BITS - 1},   total_micro_g = s_g * sum_u q_{u,g}
# where s_g (an integer number of micro-units per HRU) is fixed in the catalogue.
HRU_BITS = 16                          # 0 .. 65,535 HRU per category per report
G_COARSE = 200                         # proposed coarse household-report catalogue
G_COARSE_RANGE = (100, 250)
ROUNDS_FRESH_REPORT = 3                # milestone rounds with fresh household reports

# Proposal sizes (canonical CBOR). A sparse item = 4-B id + 8-B quantity = 12 B.
SPARSE_ITEM_BYTES = 12
PROPOSAL_HEADER_BYTES = 400            # ids, round, totals, transcript root, bitmap (estimate)


def proposal_bytes(items: int, signers: int = 1, sig: int = HYBRID_SIG_BYTES,
                   header: int = PROPOSAL_HEADER_BYTES) -> int:
    """Raw canonical-CBOR proposal size: header + sparse items + one sig per signer."""
    return header + SPARSE_ITEM_BYTES * items + signers * sig


def hru_rounding(n_households: int, s_g_micro: int) -> dict:
    """Rounding loss from converting a real quantity to whole HRUs (round-half-even).

    Worst case per household is half an HRU; the aggregate worst case is
    N * s_g / 2 micro-units, and for independent uniform errors the standard
    deviation is s_g * sqrt(N / 12). The HRU -> micro-unit step itself is exact.
    """
    return {
        "worst_case_micro": n_households * s_g_micro // 2,
        "sd_micro": s_g_micro * math.sqrt(n_households / 12),
    }


# Budget table (Table 1.2) as printed, for per-FTE-year reconciliation.
BUDGET_ROWS = {
    # name: (fte_lo, fte_hi, months_lo, months_hi, labour_lo, labour_hi, non_labour_lo, non_labour_hi)
    "Phase 1 + 1H": (2.0, 2.0, 2, 3, 25_000, 45_000, 50, 200),
    "Phase 2": (2.0, 3.0, 3, 4, 150_000, 280_000, 1_500, 3_000),
    # Printed total $250k-$950k includes hosting $10k-$40k and audit $50k-$150k,
    # so implied labour is $190k-$760k.
    "Phase 3": (4.0, 8.0, 6, 12, 190_000, 760_000, 60_000, 190_000),
}


def binomial_tail(n: int, k_fail: int, p: float) -> float:
    return sum(math.comb(n, k) * (p ** k) * ((1 - p) ** (n - k)) for k in range(k_fail, n + 1))
