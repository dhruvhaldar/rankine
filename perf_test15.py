import numpy as np
import time

M = np.linspace(0.1, 5.0, 10000)
gamma = 1.4

start = time.time()
for _ in range(100):
    term = 1.0 + (gamma - 1.0) / 2.0 * (M * M)
    res1 = 1.0 / (term ** (gamma / (gamma - 1.0)))
print("Power array:", time.time() - start)

start = time.time()
for _ in range(100):
    term = 1.0 + (gamma - 1.0) / 2.0 * (M * M)
    res2 = 1.0 / (term * term * term * np.sqrt(term))
print("Bypass array:", time.time() - start)

print(np.allclose(res1, res2))
