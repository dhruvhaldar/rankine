import numpy as np
import time
import math

M = 2.0
gamma = 1.4

start = time.time()
for _ in range(1000000):
    res1 = 1.0 / ((1.0 + (gamma - 1.0) / 2.0 * (M * M)) ** (gamma / (gamma - 1.0)))
print("Original calc_pressure_ratio scalar:", time.time() - start)

start = time.time()
for _ in range(1000000):
    term = 1.0 + (gamma - 1.0) / 2.0 * (M * M)
    res2 = 1.0 / (term * term * term * math.sqrt(term))
print("Optimized calc_pressure_ratio bypass scalar (no if):", time.time() - start)

print(np.allclose(res1, res2))
