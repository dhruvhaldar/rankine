import numpy as np
from rankine.isentropic import CDNozzle
import time

nozzle = CDNozzle(A_throat=1.0, A_exit=2.0)
P0 = 100000
back_pressure = 98000

start = time.time()
for _ in range(100):
    nozzle.solve(P0=P0, T0=300, back_pressure=back_pressure)
print("CDNozzle.solve subsonic:", time.time() - start)
