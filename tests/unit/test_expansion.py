
import pytest
import numpy as np
from rankine.expansion import PrandtlMeyer

def test_prandtl_meyer_M1():
    # nu(1) = 0
    nu = PrandtlMeyer.prandtl_meyer_function(1.0)
    assert abs(nu) < 1e-6

def test_prandtl_meyer_inverse():
    # M=2.0 -> nu approx 26.38 deg
    nu_ref = 26.3797 * np.pi / 180.0
    nu = PrandtlMeyer.prandtl_meyer_function(2.0, gamma=1.4)
    assert abs(nu - nu_ref) < 1e-3

    # Inverse
    M_calc = PrandtlMeyer.inverse_prandtl_meyer(nu, gamma=1.4)
    assert abs(M_calc - 2.0) < 1e-3

def test_expansion_fan():
    # M1=2.0, theta=10 deg
    # nu1 = 26.38 deg
    # nu2 = 36.38 deg
    # M2 should correspond to nu2

    M1 = 2.0
    theta_deg = 10.0
    theta_rad = np.radians(theta_deg)

    M2, mu1, mu2_rel = PrandtlMeyer.expansion_fan(M1, theta_rad, gamma=1.4)

    # Check M2 > M1
    assert M2 > M1

    nu2 = PrandtlMeyer.prandtl_meyer_function(M2, gamma=1.4)
    nu1 = PrandtlMeyer.prandtl_meyer_function(M1, gamma=1.4)

    assert abs(nu2 - (nu1 + theta_rad)) < 1e-4

def test_plot_fan():
    fig = PrandtlMeyer.plot_fan(2.0, 10.0)
    assert fig is not None
