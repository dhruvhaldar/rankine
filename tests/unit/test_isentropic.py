
import pytest
import numpy as np
from rankine.isentropic import IsentropicRelations, CDNozzle

def test_area_mach_relation():
    # Test M=1 -> A/A* = 1
    assert abs(IsentropicRelations.calc_area_mach(1.0) - 1.0) < 1e-6
    # Test M=2, gamma=1.4 -> A/A* approx 1.6875 (Anderson Table A.1)
    # Anderson Table: M=2.0 -> A/A* = 1.6875
    val = IsentropicRelations.calc_area_mach(2.0, gamma=1.4)
    assert abs(val - 1.6875) < 1e-3

def test_mach_area_relation():
    # Test inverse of above
    m = IsentropicRelations.calc_mach_area(1.6875, gamma=1.4, regime='supersonic')
    assert abs(m - 2.0) < 1e-3

    # Subsonic branch
    # M=0.5 -> A/A* = 1.3398
    m_sub = IsentropicRelations.calc_mach_area(1.3398, gamma=1.4, regime='subsonic')
    assert abs(m_sub - 0.5) < 1e-3

def test_nozzle_solve_subsonic():
    # Subsonic flow
    nozzle = CDNozzle(A_throat=1.0, A_exit=2.0)
    # High back pressure -> Subsonic
    res = nozzle.solve(P0=100000, T0=300, back_pressure=98000)
    # Max Mach should be < 1
    assert np.max(res.M) < 1.0
    # Pressure should drop then recover (Venturi)
    assert abs(res.P[-1] - 98000) < 1e-4

def test_nozzle_solve_choked_supersonic():
    # Design condition
    nozzle = CDNozzle(A_throat=1.0, A_exit=1.6875) # Corresponds to M=2
    # P_exit should be approx P0 * 0.1278 (M=2)
    P0 = 100000
    P_design = P0 * IsentropicRelations.calc_pressure_ratio(2.0, 1.4)

    res = nozzle.solve(P0=P0, T0=300, back_pressure=P_design)

    # Throat Mach should be 1
    idx_throat = np.argmin(res.A)
    assert abs(res.M[idx_throat] - 1.0) < 0.05 # Grid resolution might affect exact peak

    # Exit Mach should be approx 2
    assert abs(res.M[-1] - 2.0) < 0.1

def test_nozzle_solve_shock_in_nozzle():
    # Back pressure between subsonic limit and supersonic design
    nozzle = CDNozzle(A_throat=1.0, A_exit=2.0)
    P0 = 100000

    # M=2.2 (approx) -> A/A* = 2.0
    M_design = IsentropicRelations.calc_mach_area(2.0, 1.4, 'supersonic')
    P_design = P0 * IsentropicRelations.calc_pressure_ratio(M_design, 1.4)

    # M_sub (approx) -> A/A* = 2.0
    M_sub = IsentropicRelations.calc_mach_area(2.0, 1.4, 'subsonic')
    P_sub = P0 * IsentropicRelations.calc_pressure_ratio(M_sub, 1.4)

    # Pick a pressure in between
    back_pressure = (P_design + P_sub) / 2.0

    res = nozzle.solve(P0=P0, T0=300, back_pressure=back_pressure)

    # Check that we have a shock jump (M goes from >1 to <1)
    # Find index where M crosses 1 downwards
    # Since it starts subsonic, goes sonic, goes supersonic, then shock to subsonic.

    # Supersonic region exists
    assert np.any(res.M > 1.0)
    # Exit is subsonic
    assert res.M[-1] < 1.0
