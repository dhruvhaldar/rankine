import numpy as np
import time
import math

M = np.linspace(0.1, 5.0, 10)
gamma = 1.4

start = time.time()
for _ in range(100000):
    term = 1.0 + (gamma - 1.0) / 2.0 * (M * M)
    try:
        res = 1.0 / (term * term * term * math.sqrt(term))
    except TypeError:
        res = 1.0 / (term * term * term * np.sqrt(term))
print("try/except:", time.time() - start)

start = time.time()
for _ in range(100000):
    term = 1.0 + (gamma - 1.0) / 2.0 * (M * M)
    res = 1.0 / (term * term * term * np.sqrt(term))
print("np.sqrt:", time.time() - start)
