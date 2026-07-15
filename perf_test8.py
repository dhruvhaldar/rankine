import numpy as np
from rankine.expansion import PrandtlMeyer
import time

M = np.linspace(1.5, 5.0, 100000)
start = time.time()
for _ in range(10):
    PrandtlMeyer.prandtl_meyer_function(M, gamma=1.4)
print("PM function:", time.time() - start)

nu = np.linspace(0.1, 1.0, 1000)
start = time.time()
for _ in range(10):
    PrandtlMeyer.inverse_prandtl_meyer(nu, gamma=1.4)
print("PM inverse:", time.time() - start)
