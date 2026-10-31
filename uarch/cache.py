"""Set-associative cache simulator with LRU or FIFO replacement."""
from collections import OrderedDict

class Cache:
    def __init__(self, size=32 * 1024, block=64, ways=8, policy="lru"):
        assert size % (block * ways) == 0
        self.block, self.ways, self.policy = block, ways, policy
        self.nsets = size // (block * ways)
        self.sets = [OrderedDict() for _ in range(self.nsets)]
        self.hits = self.misses = 0

    def access(self, addr):
        line = addr // self.block
        s = self.sets[line % self.nsets]; tag = line // self.nsets
        if tag in s:
            self.hits += 1
            if self.policy == "lru": s.move_to_end(tag)
            return True
        self.misses += 1
        if len(s) >= self.ways: s.popitem(last=False)
        s[tag] = True
        return False

    @property
    def miss_rate(self):
        return self.misses / max(1, self.hits + self.misses)

def matmul_trace(n, order="ijk", elem=8):
    """Address trace for C=A@B on n x n row-major doubles."""
    A, B, C = 0, n * n * elem, 2 * n * n * elem
    idx = {"ijk": lambda i, j, k: (i, j, k), "ikj": lambda i, k, j: (i, j, k)}[order]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                i, j, k = idx(a, b, c)
                yield A + (i * n + k) * elem
                yield B + (k * n + j) * elem
                yield C + (i * n + j) * elem
