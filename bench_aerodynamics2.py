import numpy as np
import time
from rankine.aerodynamics import Aerodynamics

cp0 = -0.5
M = np.linspace(0.1, 0.9, 1000000)

start = time.time()
cp = Aerodynamics.prandtl_glauert_cp(cp0, M)
pg_time = time.time() - start
print(f"pg_time: {pg_time:.4f}s")

start = time.time()
cp = cp0 / np.sqrt(1.0 - M**2)
np_time = time.time() - start
print(f"np_time: {np_time:.4f}s")

def optimized_pg(cp0, M):
    M_arr = np.asarray(M)
    # The condition `np.any(M_arr >= 1.0)` has to evaluate the entire array just to see if one is >= 1.0
    # Let's see if we can do `np.max(M_arr) >= 1.0` which is sometimes faster in numpy
    if np.max(M_arr) >= 1.0:
        raise ValueError("Prandtl-Glauert is valid only for subsonic flow (M < 1).")
    return cp0 / np.sqrt(1.0 - M_arr**2)

start = time.time()
cp = optimized_pg(cp0, M)
opt_time = time.time() - start
print(f"opt_time: {opt_time:.4f}s")
