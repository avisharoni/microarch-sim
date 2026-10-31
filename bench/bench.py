import random
from uarch.cache import Cache, matmul_trace
from uarch.branch import Static, Bimodal, GShare, accuracy, loop_trace
print("matmul n=64, 32KiB 8-way 64B L1:")
for o in ("ijk", "ikj"):
    for p in ("lru", "fifo"):
        c = Cache(policy=p)
        for a in matmul_trace(64, o): c.access(a)
        print(f"  order={o} policy={p}: miss rate {c.miss_rate*100:.2f}%")
rnd = random.Random(0)
traces = {"loop trip=4": loop_trace(2000, 4), "loop trip=16": loop_trace(500, 16),
          "biased 90% taken": [(0x10, rnd.random() < 0.9) for _ in range(8000)]}
for name, t in traces.items():
    print(f"{name:18s} " + "  ".join(f"{P.__name__}={accuracy(P(), t)*100:.1f}%" for P in (Static, Bimodal, GShare)))
