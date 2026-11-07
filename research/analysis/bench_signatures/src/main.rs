//! Signature-verification benchmark for the DPEP monograph (signature policy, Kill Gate 2).
//!
//! Measures on the local machine:
//!   * Ed25519 single verification and batch verification (ed25519-dalek 3.0.0, `batch`);
//!   * ML-DSA-65 verification (libcrux-ml-dsa 0.0.11), and the hybrid Ed25519 + ML-DSA-65 cost;
//!   * BLS12-381 (min-pk: 48 B public keys, 96 B signatures; blst 0.3.17): verification of
//!     one aggregate signature from 86 validators on the same checkpoint digest.
//! and the wall-clock time to verify 40,000 and 200,000 council signatures per round on one
//! core and on all cores (rayon).
//!
//! Keys are derived deterministically from byte seeds; messages are 32-byte digests, as a
//! signer would sign the hash of a canonical-CBOR object. Desktop numbers only.
//!
//! Run from the repository root:
//!   cargo run --release --manifest-path research/analysis/bench_signatures/Cargo.toml
//! Output: one JSON object on stdout.

use ed25519_dalek::{Signature, Signer, SigningKey, Verifier, VerifyingKey};
use rayon::prelude::*;
use std::time::Instant;

fn seed(i: u64, tag: u8) -> [u8; 32] {
    // SplitMix64-style expansion; deterministic, not cryptographic.
    let mut out = [0u8; 32];
    let mut x = i.wrapping_mul(0x9E37_79B9_7F4A_7C15) ^ (tag as u64) << 56;
    for chunk in out.chunks_mut(8) {
        x = x.wrapping_add(0x9E37_79B9_7F4A_7C15);
        let mut z = x;
        z = (z ^ (z >> 30)).wrapping_mul(0xBF58_476D_1CE4_E5B9);
        z = (z ^ (z >> 27)).wrapping_mul(0x94D0_49BB_1331_11EB);
        z ^= z >> 31;
        chunk.copy_from_slice(&z.to_le_bytes());
    }
    out
}

fn secs<F: FnOnce()>(f: F) -> f64 {
    let t = Instant::now();
    f();
    t.elapsed().as_secs_f64()
}

fn main() {
    let threads = rayon::current_num_threads();
    const N: usize = 200_000;
    const POOL: usize = 2_000; // distinct keys; signatures cycle over them

    // ---------------- Ed25519 ----------------
    let ed_keys: Vec<SigningKey> = (0..POOL as u64).map(|i| SigningKey::from_bytes(&seed(i, 1))).collect();
    let ed_vks: Vec<VerifyingKey> = ed_keys.iter().map(|k| k.verifying_key()).collect();
    let msgs: Vec<[u8; 32]> = (0..N as u64).map(|i| seed(i, 2)).collect();
    let ed_sigs: Vec<Signature> = (0..N).map(|i| ed_keys[i % POOL].sign(&msgs[i])).collect();

    let ed_single_1c = secs(|| {
        for i in 0..N {
            ed_vks[i % POOL].verify(&msgs[i], &ed_sigs[i]).unwrap();
        }
    });
    let batch = 64;
    let ed_batch_1c = secs(|| {
        for c in (0..N).step_by(batch) {
            let e = (c + batch).min(N);
            let m: Vec<&[u8]> = (c..e).map(|i| &msgs[i][..]).collect();
            let s: Vec<Signature> = ed_sigs[c..e].to_vec();
            let k: Vec<VerifyingKey> = (c..e).map(|i| ed_vks[i % POOL]).collect();
            ed25519_dalek::verify_batch(&m, &s, &k).unwrap();
        }
    });
    let ed_batch_all = secs(|| {
        (0..N).into_par_iter().step_by(batch).for_each(|c| {
            let e = (c + batch).min(N);
            let m: Vec<&[u8]> = (c..e).map(|i| &msgs[i][..]).collect();
            let s: Vec<Signature> = ed_sigs[c..e].to_vec();
            let k: Vec<VerifyingKey> = (c..e).map(|i| ed_vks[i % POOL]).collect();
            ed25519_dalek::verify_batch(&m, &s, &k).unwrap();
        });
    });

    // ---------------- ML-DSA-65 ----------------
    use libcrux_ml_dsa::ml_dsa_65 as mldsa;
    let md_pool = 256usize;
    let md_keys: Vec<_> = (0..md_pool as u64).map(|i| mldsa::generate_key_pair(seed(i, 3))).collect();
    let md_n = 20_000usize; // measured sample; 200k extrapolated and also run on all cores
    let md_sigs: Vec<_> = (0..md_n)
        .map(|i| mldsa::sign(&md_keys[i % md_pool].signing_key, &msgs[i], b"", seed(i as u64, 4)).unwrap())
        .collect();
    let md_sig_len = md_sigs[0].as_slice().len();
    let md_1c = secs(|| {
        for i in 0..md_n {
            mldsa::verify(&md_keys[i % md_pool].verification_key, &msgs[i], b"", &md_sigs[i]).unwrap();
        }
    });
    let md_all_200k = secs(|| {
        (0..N).into_par_iter().for_each(|i| {
            let j = i % md_n;
            mldsa::verify(&md_keys[j % md_pool].verification_key, &msgs[j], b"", &md_sigs[j]).unwrap();
        });
    });

    // ---------------- BLS12-381 (min-pk) ----------------
    use blst::min_pk::{AggregatePublicKey, AggregateSignature, PublicKey as BPk, SecretKey as BSk, Signature as BSig};
    const DST: &[u8] = b"BLS_SIG_BLS12381G2_XMD:SHA-256_SSWU_RO_POP_DPEP-WD-v0-CHECKPOINT";
    let q = 86usize;
    let bsks: Vec<BSk> = (0..128u64).map(|i| BSk::key_gen(&seed(i, 5), &[]).unwrap()).collect();
    let bpks: Vec<BPk> = bsks.iter().map(|k| k.sk_to_pk()).collect();
    let digest = seed(99, 6);
    let bsigs: Vec<BSig> = bsks[..q].iter().map(|k| k.sign(&digest, DST, &[])).collect();
    let agg_sig = AggregateSignature::aggregate(&bsigs.iter().collect::<Vec<_>>(), true).unwrap().to_signature();
    let reps = 200;
    let bls_agg_verify = secs(|| {
        for _ in 0..reps {
            // phone-side work: aggregate the 86 public keys named in the bitmap, then one pairing check
            let pk_refs: Vec<&BPk> = bpks[..q].iter().collect();
            let apk = AggregatePublicKey::aggregate(&pk_refs, false).unwrap().to_public_key();
            assert_eq!(agg_sig.verify(true, &digest, DST, &[], &apk, true), blst::BLST_ERROR::BLST_SUCCESS);
        }
    }) / reps as f64;
    let bls_single = secs(|| {
        for _ in 0..reps {
            assert_eq!(bsigs[0].verify(true, &digest, DST, &[], &bpks[0], true), blst::BLST_ERROR::BLST_SUCCESS);
        }
    }) / reps as f64;
    let bls_sig_len = agg_sig.to_bytes().len();

    // ---------------- report ----------------
    let ed_single_us = ed_single_1c / N as f64 * 1e6;
    let ed_batch_us = ed_batch_1c / N as f64 * 1e6;
    let md_us = md_1c / md_n as f64 * 1e6;
    println!(
        "{{\"threads\":{threads},\"n_signatures\":{N},\
\"ed25519_single_us\":{ed_single_us:.2},\"ed25519_batch64_us\":{ed_batch_us:.2},\
\"ed25519_200k_single_core_s\":{:.2},\"ed25519_200k_batch_single_core_s\":{ed_batch_1c:.2},\"ed25519_200k_batch_all_cores_s\":{ed_batch_all:.3},\
\"mldsa65_sig_bytes\":{md_sig_len},\"mldsa65_verify_us\":{md_us:.2},\
\"mldsa65_200k_single_core_s_extrapolated\":{:.2},\"mldsa65_200k_all_cores_s\":{md_all_200k:.2},\
\"hybrid_verify_us\":{:.2},\"hybrid_200k_single_core_s_extrapolated\":{:.2},\
\"bls_aggregate_sig_bytes\":{bls_sig_len},\"bls_verify_aggregate_of_86_ms\":{:.3},\"bls_verify_single_ms\":{:.3},\
\"ed25519_86_individual_ms\":{:.3},\"hybrid_86_individual_ms\":{:.3}}}",
        ed_single_us * N as f64 / 1e6,
        md_us * N as f64 / 1e6,
        ed_single_us + md_us,
        (ed_single_us + md_us) * N as f64 / 1e6,
        bls_agg_verify * 1e3,
        bls_single * 1e3,
        ed_single_us * 86.0 / 1e3,
        (ed_single_us + md_us) * 86.0 / 1e3,
    );
}
