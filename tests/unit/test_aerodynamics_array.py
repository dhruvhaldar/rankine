import pytest
import numpy as np
from rankine.aerodynamics import Aerodynamics

def test_prandtl_glauert_array():
    # Array inputs should not raise ValueError
    M = np.array([0.1, 0.5, 0.8])
    cp0 = np.array([1.0, 1.0, 1.0])

    cp = Aerodynamics.prandtl_glauert_cp(cp0, M)

    assert len(cp) == 3
    assert abs(cp[1] - 1.1547) < 1e-4

def test_ackeret_array():
    M = np.array([1.5, 2.0, 3.0])
    theta = np.array([0.1, 0.1, 0.1])

    cp = Aerodynamics.ackeret_cp(M, theta)

    assert len(cp) == 3
    # M=2.0 -> beta = sqrt(3) = 1.732. Cp = 2 * 0.1 / 1.732 = 0.11547
    assert abs(cp[1] - 0.11547) < 1e-4

def test_newtonian_array():
    M = np.array([5.0, 10.0])
    theta = np.array([0.0, np.pi/2])

    cp = Aerodynamics.newtonian_cp(M, theta)

    assert len(cp) == 2
    assert cp[0] == 0.0

    # Check value roughly. M=10, theta=90. Cp_max ~ 1.839
    assert abs(cp[1] - 1.839) < 0.1
