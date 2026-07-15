import numpy as np
from rankine.shocks import ObliqueShock
import time

M_2d = np.linspace(1.5, 5.0, 50)[np.newaxis, :]
mu = np.arcsin(1.0 / M_2d)
t = np.linspace(0, 1, 500)[:, np.newaxis]
betas_2d = mu + t * (np.pi / 2 - mu)

start = time.time()
for _ in range(100):
    ObliqueShock.theta_beta_m(betas_2d, M_2d, gamma=1.4)
print("theta_beta_m:", time.time() - start)
