import numpy as np
from rankine.isentropic import IsentropicRelations
import time
import math

M = np.linspace(0.1, 5.0, 1000000)
gamma = 1.4

start = time.time()
for _ in range(10):
    res1 = 1.0 / ((1.0 + (gamma - 1.0) / 2.0 * (M * M)) ** (gamma / (gamma - 1.0)))
print("Original calc_pressure_ratio:", time.time() - start)

start = time.time()
for _ in range(10):
    term = 1.0 + (gamma - 1.0) / 2.0 * (M * M)
    if abs(gamma - 1.4) < 1e-9:
        res2 = 1.0 / (term * term * term * np.sqrt(term))
    else:
        res2 = 1.0 / (term ** (gamma / (gamma - 1.0)))
print("Optimized calc_pressure_ratio bypass:", time.time() - start)

print(np.allclose(res1, res2))

start = time.time()
for _ in range(10):
    res3 = 1.0 / ((1.0 + (gamma - 1.0) / 2.0 * (M * M)) ** (1.0 / (gamma - 1.0)))
print("Original calc_density_ratio:", time.time() - start)

start = time.time()
for _ in range(10):
    term = 1.0 + (gamma - 1.0) / 2.0 * (M * M)
    if abs(gamma - 1.4) < 1e-9:
        res4 = 1.0 / (term * term * np.sqrt(term))
    else:
        res4 = 1.0 / (term ** (1.0 / (gamma - 1.0)))
print("Optimized calc_density_ratio bypass:", time.time() - start)

print(np.allclose(res3, res4))
