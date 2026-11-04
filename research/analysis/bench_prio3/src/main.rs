//! Prio3SumVec size and timing benchmark for the DPEP monograph (Kill Gate 3).
//!
//! Measures, for 3 aggregators and each (length, bits) pair:
//!   * encoded public share, leader (aggregator 0) input share and helper input share;
//!   * client `shard` time;
//!   * `verify_init` time for the leader and for one helper;
//!   * the combine step (`verifier_shares_to_message`) and `verify_next` for one aggregator.
//!
//! Crate: `prio` 0.18.1 (implements draft-irtf-cfrg-vdaf-18, per its README).
//! Run (from the repository root):
//!   cargo run --release --manifest-path research/analysis/bench_prio3/Cargo.toml
//! Output: JSON lines on stdout. Desktop numbers are not phone or Raspberry Pi numbers.

use prio::codec::Encode;
use prio::vdaf::prio3::{optimal_chunk_length, Prio3SumVec};
use prio::vdaf::{Aggregator, Client, VerifyTransition};
use rand::Rng;
use std::time::Instant;

const CTX: &[u8] = b"DPEP-WD-v0 bench";

fn median(v: &mut [f64]) -> f64 {
    v.sort_by(|a, b| a.partial_cmp(b).unwrap());
    v[v.len() / 2]
}

fn bench(len: usize, bits: u32, iters: usize) {
    let max: u128 = if bits >= 128 { u128::MAX } else { (1u128 << bits) - 1 };
    let chunk = optimal_chunk_length(len * bits as usize);
    let vdaf = Prio3SumVec::new_sum_vec(3, max, len, chunk).expect("vdaf");
    let mut rng = rand::thread_rng();
    let verify_key: [u8; 32] = rng.gen();

    let (mut t_shard, mut t_vi_leader, mut t_vi_helper, mut t_combine, mut t_next) =
        (vec![], vec![], vec![], vec![], vec![]);
    let (mut pub_b, mut lead_b, mut help_b) = (0usize, 0usize, 0usize);

    for i in 0..iters {
        let meas: Vec<u128> = (0..len).map(|_| rng.gen_range(0..=max.min(1_000_000))).collect();
        let nonce: [u8; 16] = rng.gen();

        let t0 = Instant::now();
        let (public_share, input_shares) = vdaf.shard(CTX, &meas, &nonce).expect("shard");
        t_shard.push(t0.elapsed().as_secs_f64() * 1e3);

        if i == 0 {
            pub_b = public_share.get_encoded().unwrap().len();
            lead_b = input_shares[0].get_encoded().unwrap().len();
            help_b = input_shares[1].get_encoded().unwrap().len();
        }

        let mut states = vec![];
        let mut vshares = vec![];
        for (agg_id, share) in input_shares.iter().enumerate() {
            let t = Instant::now();
            let (st, vs) = vdaf
                .verify_init(&verify_key, CTX, agg_id, &(), &nonce, &public_share, share)
                .expect("verify_init");
            let ms = t.elapsed().as_secs_f64() * 1e3;
            match agg_id {
                0 => t_vi_leader.push(ms),
                1 => t_vi_helper.push(ms),
                _ => {}
            }
            states.push(st);
            vshares.push(vs);
        }
        let t = Instant::now();
        let msg = vdaf
            .verifier_shares_to_message(CTX, &(), vshares)
            .expect("combine");
        t_combine.push(t.elapsed().as_secs_f64() * 1e3);
        for (k, st) in states.into_iter().enumerate() {
            let t = Instant::now();
            let tr = vdaf.verify_next(CTX, st, msg.clone()).expect("verify_next");
            if k == 0 {
                t_next.push(t.elapsed().as_secs_f64() * 1e3);
            }
            assert!(matches!(tr, VerifyTransition::Finish(_)), "report rejected");
        }
    }
    println!(
        "{{\"length\":{len},\"bits\":{bits},\"chunk_length\":{chunk},\"iters\":{iters},\
\"public_share_bytes\":{pub_b},\"leader_input_share_bytes\":{lead_b},\"helper_input_share_bytes\":{help_b},\
\"client_upload_bytes\":{},\"shard_ms_median\":{:.3},\"verify_init_leader_ms_median\":{:.3},\
\"verify_init_helper_ms_median\":{:.3},\"combine_ms_median\":{:.4},\"verify_next_ms_median\":{:.4}}}",
        pub_b + lead_b + 2 * help_b,
        median(&mut t_shard),
        median(&mut t_vi_leader),
        median(&mut t_vi_helper),
        median(&mut t_combine),
        median(&mut t_next),
    );
}

fn main() {
    let iters: usize = std::env::var("ITERS").ok().and_then(|s| s.parse().ok()).unwrap_or(30);
    for &len in &[100usize, 230, 3000] {
        for &bits in &[20u32, 32, 64] {
            bench(len, bits, iters);
        }
    }
}
