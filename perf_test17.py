import numpy as np
from rankine.expansion import PrandtlMeyer
from rankine.unsteady import ShockTube
from rankine.isentropic import IsentropicRelations
from rankine.aerodynamics import Aerodynamics
import time

theta = np.radians(10.0)

M = np.linspace(1.1, 5.0, 1000)

start = time.time()
for _ in range(100):
    Aerodynamics.ackeret_cp(M, theta)
print("Ackeret array:", time.time() - start)

start = time.time()
for _ in range(100):
    Aerodynamics.newtonian_cp(M, theta)
print("Newtonian array:", time.time() - start)

start = time.time()
for _ in range(100):
    Aerodynamics.prandtl_glauert_cp(0.1, np.linspace(0.1, 0.9, 1000))
print("Prandtl_Glauert array:", time.time() - start)

from rankine.shocks import ObliqueShock

start = time.time()
for _ in range(100):
    ObliqueShock.theta_beta_m(theta, M, gamma=1.4)
print("ObliqueShock theta_beta_m array:", time.time() - start)
