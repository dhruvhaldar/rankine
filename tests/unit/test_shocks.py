
import pytest
import numpy as np
from rankine.shocks import NormalShock, ObliqueShock

def test_normal_shock_mach():
    # Known data: M1 = 2.0, Gamma = 1.4 -> M2 should be 0.5774
    ns = NormalShock(M1=2.0, gamma=1.4)
    assert abs(ns.M2 - 0.57735) < 1e-4

def test_normal_shock_pressure():
    # M1 = 2.0, Gamma = 1.4 -> P2/P1 = 4.5
    ns = NormalShock(M1=2.0, gamma=1.4)
    assert abs(ns.P2_P1 - 4.5) < 1e-4

def test_oblique_shock_beta():
    # For a given M and theta, check beta.
    # M=2.0, theta=10 degrees. Beta approx 39.3 deg (Weak)
    theta = np.radians(10.0)
    beta = ObliqueShock.solve_beta(M=2.0, theta=theta, gamma=1.4, weak=True)
    assert abs(np.degrees(beta) - 39.3) < 0.2

def test_oblique_shock_polar():
    # Plotting should not crash
    fig = ObliqueShock.plot_polar(mach_numbers=[2.0, 3.0], gamma=1.4)
    assert fig is not None
