#!/usr/bin/env python3
"""Reference tests supplied with the third external review.

Test A: one-sided feasibility on the single-plant case (R3-02).
Test B: Algorithm 3b as printed vs. with the augmented residual term (R3-12).
Test C: Table 6.1 scores and weight sensitivity (R3-18).

Kept verbatim (apart from this docstring) so the reviewer's figures can be
reproduced exactly. `verify_r3.py` extends these tests and checks whether they
represent the book's equations fairly. Standard library only.

    python3 research/analysis/reference_tests_r3.py
"""


def price_step(s, d, pd, p):
    """Eq. 4.14-4.15 for one good; pd is min(0.25, previous rho)."""
    surplus = s - d
    denom = s + d
    rho = 2 * abs(surplus) / denom if denom > 0 else 0.0
    tilde = 1.05 - 0.5 ** rho
    delta = max(0.001, min(tilde, tilde * pd))
    if surplus > 0:
        p *= 1 - delta
    elif surplus < 0:
        p *= 1 + delta
    return p, min(0.25, rho), rho


def test_a():
    """Single plant: S = 100 if p >= 10, else 0; D = 70 - p; p0 = 8."""
    p, pd = 8.0, 0.25
    for t in range(1, 501):
        s = 100.0 if p >= 10 else 0.0
        d = max(0.0, 70 - p)
        if s >= d:
            print(f"Test A: first D<=S at round {t}: p={p:.2f} S={s:.0f} "
                  f"D={d:.2f}, unused {(s - d) / s:.0%}")
            return
        p, pd, _ = price_step(s, d, pd, p)


def test_b(kind, welfare, rounds=20000, rho=1.0):
    """Two councils, x1 + x2 <= 1, 0 <= x <= 10, P = rho*N + 0.001."""
    n, b = 2, 1.0
    prox = rho * n + 1e-3
    x, lam = [0.0, 0.0], 0.0
    tail = []
    for t in range(rounds):
        resid = sum(x) - b
        coef = lam if kind == "as_printed" else lam + rho * resid
        new = []
        for xi in x:
            if welfare == "linear":
                v = xi + (1.0 - coef) / prox
            else:  # log(1 + x), solved by bisection
                lo, hi = 0.0, 10.0
                for _ in range(60):
                    m = (lo + hi) / 2
                    if -1 / (1 + m) + coef + prox * (m - xi) > 0:
                        hi = m
                    else:
                        lo = m
                v = (lo + hi) / 2
            new.append(min(10.0, max(0.0, v)))
        x = new
        lam = max(0.0, lam + rho * (sum(x) - b))
        if t >= rounds - 2000:
            tail.append((abs(sum(x) - b), lam))
    print(f"Test B {kind:10s} {welfare:6s}: max|resid|="
          f"{max(a for a, _ in tail):.4f}, "
          f"lambda {min(c for _, c in tail):.3f}..{max(c for _, c in tail):.3f}")


def score(weights, scores):
    return sum(w * s for w, s in zip(weights, scores)) / sum(weights)


def test_c():
    """Table 6.1 as rescored. Check these values against the current table."""
    w = [9, 10, 8, 8, 7, 8, 9, 8, 9, 6, 6, 4, 4, 4]
    a = [2, 2, 2, 5, 4.5, 4.5, 1.5, 1, 2.5, 4, 5, 4, 4.5, 4]
    b = [5, 3, 4.5, 4, 2.5, 3.5, 5, 2.5, 2, 3.5, 3, 4.5, 4, 3.5]
    c = [3, 4.5, 4, 2, 1.5, 1.5, 1, 5, 1, 2, 2.5, 2, 2.5, 2]
    d = [4.5, 4, 4.5, 5, 4.5, 4.5, 5, 4, 4, 4, 3.5, 4.5, 4, 4]
    names = "ABCD"
    table = [a, b, c, d]
    show = lambda ws, rows=table: " ".join(
        f"{n}={score(ws, s):.2f}" for n, s in zip(names, rows))
    print("Test C baseline:", show(w))
    print("Test C A beats D on criteria:",
          [i + 1 for i in range(14) if a[i] > d[i]])
    # 70% of the weight on criteria 4, 11, 12; the rest proportional to baseline
    focus = {3, 10, 11}
    rest = sum(w[i] for i in range(14) if i not in focus)
    w70 = [0.7 / 3 if i in focus else 0.3 * w[i] / rest for i in range(14)]
    print("Test C 70% weighting:", show(w70))
    # Harsher D: trust 3.5, bandwidth 2.5, hardware 3, privacy 3
    harsh = d[:]
    harsh[1], harsh[4], harsh[5], harsh[8] = 3.5, 2.5, 3, 3
    print("Test C harsher D:", show(w, [a, b, c, harsh]))


if __name__ == "__main__":
    test_a()
    for welfare in ("linear", "log"):
        for kind in ("as_printed", "with_resid"):
            test_b(kind, welfare)
    test_c()
