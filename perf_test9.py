import numpy as np
from rankine.expansion import PrandtlMeyer
import time

nu = np.linspace(0.1, 1.0, 1000)

def residual_arr(M_guess, gamma, target_nu):
    c1 = np.sqrt((gamma + 1.0) / (gamma - 1.0))
    c2 = (gamma - 1.0) / (gamma + 1.0)
    c2_sqrt = np.sqrt(c2)
    M_safe = np.maximum(M_guess, 1.0 + 1e-9)
    s = np.sqrt(M_safe * M_safe - 1.0)
    return c1 * np.arctan(c2_sqrt * s) - np.arctan(s) - target_nu

def residual_arr_fprime(M_guess, gamma, target_nu):
    c3 = 0.5 * (gamma - 1.0)
    M_safe = np.maximum(M_guess, 1.0 + 1e-9)
    M_sq = M_safe * M_safe
    return np.sqrt(M_sq - 1.0) / (1.0 + c3 * M_sq) / M_safe

M_guess = np.linspace(1.5, 5.0, 1000)

start = time.time()
for _ in range(100):
    residual_arr(M_guess, 1.4, nu)
print("residual_arr:", time.time() - start)

start = time.time()
for _ in range(100):
    residual_arr_fprime(M_guess, 1.4, nu)
print("residual_arr_fprime:", time.time() - start)
