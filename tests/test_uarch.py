import random
from uarch.cache import Cache, matmul_trace
from uarch.branch import Static, Bimodal, GShare, accuracy, loop_trace

def test_sequential_miss_rate_is_one_per_block():
    c = Cache(size=4096, block=64, ways=4)
    for a in range(0, 64 * 1000, 8): c.access(a)
    assert abs(c.miss_rate - 1 / 8) < 1e-9

def test_lru_working_set_fits():
    c = Cache(size=4096, block=64, ways=4)
    for _ in range(10):
        for a in range(0, 4096, 64): c.access(a)
    assert c.misses == 64

def test_lru_vs_fifo_differ_on_reuse():
    trace = [0, 2048, 0, 4096, 0, 6144, 0]  # same set (32 sets x 64B), block 0 reused
    l, f = Cache(4096, 64, 2, "lru"), Cache(4096, 64, 2, "fifo")
    for a in trace: l.access(a); f.access(a)
    assert l.hits > f.hits

def test_loop_order_changes_locality():
    r = {}
    for o in ("ijk", "ikj"):
        c = Cache(size=8192, block=64, ways=4)
        for a in matmul_trace(32, o): c.access(a)
        r[o] = c.miss_rate
    assert r["ikj"] < r["ijk"]

def test_predictors():
    t = loop_trace(200, 4)
    assert accuracy(GShare(), t) > 0.95 > accuracy(Bimodal(), t)
    rnd = random.Random(0); t2 = [(0x10, rnd.random() < 0.9) for _ in range(5000)]
    assert accuracy(Bimodal(), t2) > 0.85
    assert abs(accuracy(Static(), t2) - sum(x for _, x in t2) / 5000) < 1e-12
