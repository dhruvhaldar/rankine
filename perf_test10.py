import numpy as np
from rankine.unsteady import ShockTube
import time

driver = {'p': 1.0, 'rho': 1.0, 'u': 0.0}
driven = {'p': 0.1, 'rho': 0.125, 'u': 0.0}
tube = ShockTube(driver, driven, gamma=1.4)

start = time.time()
for _ in range(100):
    tube.solve_star_region()
print("solve_star_region:", time.time() - start)
