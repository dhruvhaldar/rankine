import math
import time
import numpy as np

M1 = np.linspace(1.5, 5.0, 1000)

gamma = 1.4
term_M1 = 1.0 + (gamma - 1.0) / 2.0 * M1**2

start = time.time()
for _ in range(100):
    res1 = (term_M1 ** (gamma / (gamma - 1.0)))
print("Power scalar:", time.time() - start)

start = time.time()
for _ in range(100):
    if abs(gamma - 1.4) < 1e-9:
        res2 = term_M1 * term_M1 * term_M1 * np.sqrt(term_M1)
    else:
        res2 = term_M1 ** (gamma / (gamma - 1.0))
print("Power array bypass:", time.time() - start)

print(np.allclose(res1, res2))
