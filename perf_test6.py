import numpy as np
from rankine.isentropic import IsentropicRelations
import time

M = np.linspace(0.1, 5.0, 100000)
start = time.time()
for _ in range(10):
    IsentropicRelations.calc_area_mach(M, gamma=1.4)
print("calc_area_mach array:", time.time() - start)

ar = np.linspace(1.1, 10.0, 100)
start = time.time()
for _ in range(10):
    IsentropicRelations.calc_mach_area(ar, gamma=1.4, regime='subsonic')
print("calc_mach_area subsonic array:", time.time() - start)

start = time.time()
for _ in range(10):
    IsentropicRelations.calc_mach_area(ar, gamma=1.4, regime='supersonic')
print("calc_mach_area supersonic array:", time.time() - start)
