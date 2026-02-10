
import pytest
import numpy as np
from rankine.aerodynamics import Aerodynamics

def test_prandtl_glauert():
    # M=0.5, Cp0 = 1.0 -> Cp = 1.0 / sqrt(0.75) = 1.1547
    cp = Aerodynamics.prandtl_glauert_cp(1.0, 0.5)
    assert abs(cp - 1.1547) < 1e-4

def test_ackeret():
    # M=sqrt(2) approx 1.414. beta = 1.
    # Cp = 2 * theta / 1 = 2 * theta
    # theta = 0.1 rad
    cp = Aerodynamics.ackeret_cp(np.sqrt(2.0), 0.1)
    assert abs(cp - 0.2) < 1e-4

def test_newtonian():
    # Modified Newtonian
    # M=10, theta = 10 deg (0.1745 rad)
    # Cp_max approx 1.839 for gamma=1.4, M=infinity (Cp_max -> 1.839 = ((g+1)^2/4g)^(g/g-1) * ... limits)
    # Actually Cp_max -> 1.839 is Cp_max stagnation.
    # For M=10, Cp_max should be calculated.

    # Let's just check consistency.
    # theta = 0 -> Cp = 0
    assert Aerodynamics.newtonian_cp(5.0, 0.0) == 0.0

    # theta = 90 deg -> Cp = Cp_max
    cp_max = Aerodynamics.newtonian_cp(5.0, np.pi/2)

    # Check value roughly.
    # M=5. P02/Pinf approx 32.6 (Normal Shock Table)
    # q_inf = 0.7 * 25 = 17.5 * P_inf
    # Cp_max = (32.6 - 1) / 17.5 = 1.80
    assert abs(cp_max - 1.81) < 0.1
