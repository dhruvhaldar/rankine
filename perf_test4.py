import numpy as np
from rankine.aerodynamics import Aerodynamics
import time

M = np.linspace(5.0, 20.0, 100000)
theta = np.radians(10.0)

start = time.time()
for _ in range(100):
    Aerodynamics.newtonian_cp(M, theta, gamma=1.4)
print("newtonian_cp array:", time.time() - start)
