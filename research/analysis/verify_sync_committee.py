#!/usr/bin/env python3
"""Light-client sync-committee option (book Table 7.8): size and capture probability.

    python3 research/analysis/verify_sync_committee.py

A committee of m members is drawn uniformly without replacement from the n=128
validators, of whom f are faulty. A phone accepts a checkpoint signed by at least
q = ceil(2m/3) committee members. The committee can mislead phones only if at
least q of its m members are faulty (hypergeometric tail). Writes
sync_committee_results.json next to this script. Standard library only.
"""
import json, math, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import parameters as P  # noqa: E402

HYBRID_SIG = P.HYBRID_SIG_BYTES   # 3,373 B (RFC 10073 concatenation); was 3,437 before the fourth refinement
ED25519_SIG = P.ED25519_SIG_BYTES

def tail(n, f, m, q):
    tot = math.comb(n, m)
    return sum(math.comb(f, k) * math.comb(n - f, m - k) for k in range(q, m + 1)) / tot

out = {}
for m in (8, 16, 24, 32):
    q = math.ceil(2 * m / 3)
    out[str(m)] = {
        "quorum": q,
        "sig_bytes": q * HYBRID_SIG,
        "sig_bytes_ed25519": q * ED25519_SIG,
        "capture_prob_f42": tail(128, 42, m, q),
        "capture_prob_f32": tail(128, 32, m, q),
    }
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sync_committee_results.json")
json.dump(out, open(path, "w"), indent=2)
for m, r in out.items():
    print(m, r)
