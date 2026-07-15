import numpy as np
from rankine.expansion import PrandtlMeyer
from rankine.unsteady import ShockTube
from rankine.isentropic import IsentropicRelations
import time

M = np.linspace(0.1, 5.0, 1000)

start = time.time()
for _ in range(100):
    IsentropicRelations.calc_area_mach(M, gamma=1.4)
print("Isentropic area_mach:", time.time() - start)

ar = np.linspace(1.1, 10.0, 100)
start = time.time()
for _ in range(10):
    IsentropicRelations.calc_mach_area(ar, gamma=1.4, regime='subsonic')
print("Isentropic mach_area sub:", time.time() - start)

start = time.time()
for _ in range(10):
    IsentropicRelations.calc_mach_area(ar, gamma=1.4, regime='supersonic')
print("Isentropic mach_area sup:", time.time() - start)

start = time.time()
for _ in range(100):
    IsentropicRelations.calc_pressure_ratio(M, gamma=1.4)
print("Isentropic pressure_ratio:", time.time() - start)

nu = np.linspace(0.1, 1.0, 100)
start = time.time()
for _ in range(10):
    PrandtlMeyer.inverse_prandtl_meyer(nu, gamma=1.4)
print("PrandtlMeyer inverse:", time.time() - start)

driver = {'p': 1.0, 'rho': 1.0, 'u': 0.0}
driven = {'p': 0.1, 'rho': 0.125, 'u': 0.0}
tube = ShockTube(driver, driven, gamma=1.4)
start = time.time()
for _ in range(100):
    tube.solve_star_region()
print("ShockTube solve_star_region:", time.time() - start)
