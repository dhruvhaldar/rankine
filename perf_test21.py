import numpy as np
from rankine.isentropic import IsentropicRelations
import time

M = np.linspace(0.1, 5.0, 100)

start = time.time()
for _ in range(100):
    IsentropicRelations.calc_pressure_ratio(M, gamma=1.4)
print("Isentropic pressure_ratio:", time.time() - start)
