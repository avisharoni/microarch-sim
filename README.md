# microarch-sim

![tests](https://github.com/avisharoni/microarch-sim/actions/workflows/tests.yml/badge.svg)

**Area:** Computer Architecture

Trace-driven simulators for two classic microarchitecture components.

- `cache.py`: set-associative cache with LRU or FIFO replacement, plus an address-trace generator for naive matrix multiply in `ijk` vs `ikj` loop order.
- `branch.py`: static always-taken, bimodal 2-bit saturating counters, and gshare (global history XOR PC).

Tests cover the expected sequential miss rate (1 per block), working-set fit, a case where LRU beats FIFO, a loop-order locality effect, and predictor behavior on loop and biased traces.

## Run

```bash
pip install -r requirements.txt
python -m pytest -q
PYTHONPATH=. python bench/bench.py
```

## Results (measured on my machine, Oct 2026)

```
matmul n=64, 32KiB 8-way 64B L1:
  order=ijk policy=lru: miss rate 5.34%
  order=ijk policy=fifo: miss rate 5.66%
  order=ikj policy=lru: miss rate 1.21%
  order=ikj policy=fifo: miss rate 0.84%
loop trip=4        Static=75.0%  Bimodal=75.0%  GShare=100.0%
loop trip=16       Static=93.8%  Bimodal=93.8%  GShare=93.8%
biased 90% taken   Static=90.1%  Bimodal=89.1%  GShare=89.0%
```

## Limitations

Note: FIFO beat LRU on the ikj trace here, which is a reminder that LRU isn't always best. With an 8-bit history, gshare can't capture a 16-trip loop. These are simulated numbers, not hardware measurements.

MIT licensed.
