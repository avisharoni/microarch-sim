"""Branch predictors: static, bimodal 2-bit, and gshare."""
class Static:
    def predict(self, pc): return True
    def update(self, pc, taken): pass

class Bimodal:
    def __init__(self, bits=10):
        self.mask = (1 << bits) - 1; self.t = [2] * (1 << bits)
    def predict(self, pc): return self.t[pc & self.mask] >= 2
    def update(self, pc, taken):
        i = pc & self.mask
        self.t[i] = min(3, self.t[i] + 1) if taken else max(0, self.t[i] - 1)

class GShare(Bimodal):
    def __init__(self, bits=10, hist=8):
        super().__init__(bits); self.h = 0; self.hm = (1 << hist) - 1
    def _i(self, pc): return (pc ^ self.h) & self.mask
    def predict(self, pc): return self.t[self._i(pc)] >= 2
    def update(self, pc, taken):
        i = self._i(pc)
        self.t[i] = min(3, self.t[i] + 1) if taken else max(0, self.t[i] - 1)
        self.h = ((self.h << 1) | int(taken)) & self.hm

def accuracy(pred, trace):
    ok = 0
    for pc, taken in trace:
        ok += pred.predict(pc) == taken; pred.update(pc, taken)
    return ok / len(trace)

def loop_trace(iters, trip):
    """Inner loop branch taken trip-1 times then not taken, repeated."""
    return [(0x40, i % trip != trip - 1) for i in range(iters * trip)]
