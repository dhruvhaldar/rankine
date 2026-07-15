import numpy as np
from rankine.expansion import PrandtlMeyer
import time

M = np.linspace(1.5, 5.0, 10000)
start = time.time()
for _ in range(100):
    PrandtlMeyer.prandtl_meyer_function(M, gamma=1.4)
print("prandtl_meyer_function array:", time.time() - start)

nu = np.linspace(0.1, 1.0, 100)
start = time.time()
for _ in range(10):
    PrandtlMeyer.inverse_prandtl_meyer(nu, gamma=1.4)
print("inverse_prandtl_meyer array:", time.time() - start)
