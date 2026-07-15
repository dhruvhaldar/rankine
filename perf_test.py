import numpy as np
from rankine.shocks import ObliqueShock
import time

M = np.linspace(1.5, 5.0, 1000)
theta = np.radians(10.0)
start = time.time()
for m in M:
    ObliqueShock.solve_beta(M=m, theta=theta, gamma=1.4, weak=True)
print("solve_beta:", time.time() - start)
