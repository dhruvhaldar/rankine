import numpy as np
import time
import math

M = 2.0
gamma = 1.4

start = time.time()
for _ in range(1000000):
    term = 1.0 + (gamma - 1.0) / 2.0 * (M * M)
    res = 1.0 / (term * term * term * term**0.5)
print("**0.5 scalar:", time.time() - start)

M = np.linspace(0.1, 5.0, 100)

start = time.time()
for _ in range(100000):
    term = 1.0 + (gamma - 1.0) / 2.0 * (M * M)
    res = 1.0 / (term * term * term * term**0.5)
print("**0.5 array:", time.time() - start)
