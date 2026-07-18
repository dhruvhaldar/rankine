import time
import numpy as np
from rankine.shocks import NormalShock

# Test scalar
t0 = time.time()
for _ in range(100000):
    shock = NormalShock(2.0)
t1 = time.time()
print(f"Scalar time: {t1 - t0:.5f}s")

# Test array
M_array = np.linspace(1.1, 5.0, 100000)
t0 = time.time()
shock_array = NormalShock(M_array)
t1 = time.time()
print(f"Array time: {t1 - t0:.5f}s")
