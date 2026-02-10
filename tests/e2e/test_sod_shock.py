
import pytest
import numpy as np
from rankine.unsteady import ShockTube

def test_sod_shock_tube():
    # Standard Sod Shock Tube problem
    # Left: P=1.0, rho=1.0, u=0
    # Right: P=0.1, rho=0.125, u=0
    # Gamma = 1.4
    # t = 0.25

    driver = {'p': 1.0, 'rho': 1.0, 'u': 0.0}
    driven = {'p': 0.1, 'rho': 0.125, 'u': 0.0}

    tube = ShockTube(driver, driven, gamma=1.4, length=1.0, diaphragm=0.5)

    res = tube.solve(time=0.25, n_points=100)

    # Check regions
    # 1. Driver region (x=0) -> Should be initial driver state
    assert abs(res['P'][0] - 1.0) < 1e-4
    assert abs(res['rho'][0] - 1.0) < 1e-4

    # 2. Driven region (x=1) -> Should be initial driven state
    assert abs(res['P'][-1] - 0.1) < 1e-4
    assert abs(res['rho'][-1] - 0.125) < 1e-4

    # 3. Star Region (Middle) -> P_star approx 0.30313
    # Find middle index where flow is non-zero
    # Or just check if P_star exists in the solution array.

    # P_star theoretical is approx 0.30313
    p_star_theory = 0.30313

    # Check if we have values close to p_star_theory
    # Filter out initial states
    middle_p = res['P'][(res['x'] > 0.4) & (res['x'] < 0.8)]

    # There should be a constant region of P_star
    # Find the most frequent value? Or just check if any value is close.
    assert np.any(np.abs(middle_p - p_star_theory) < 0.01)

    # Check velocity in star region. u_star approx 0.927
    u_star_theory = 0.927
    middle_u = res['u'][(res['x'] > 0.4) & (res['x'] < 0.6)]
    assert np.any(np.abs(middle_u - u_star_theory) < 0.01)

def test_shock_tube_plot():
    driver = {'p': 1.0, 'rho': 1.0, 'u': 0.0}
    driven = {'p': 0.1, 'rho': 0.125, 'u': 0.0}
    tube = ShockTube(driver, driven, gamma=1.4)
    tube.solve(time=0.25)
    fig = tube.plot_properties()
    assert fig is not None
