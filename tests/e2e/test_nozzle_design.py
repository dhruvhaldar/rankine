
import pytest
import numpy as np
from rankine.isentropic import CDNozzle

def test_mass_conservation_nozzle():
    # Mass flow rate should be constant at inlet, throat, and exit
    # This assumes isentropic flow everywhere (solve_isentropic helper)

    nozzle = CDNozzle(A_throat=1.0, A_exit=2.0, A_inlet=3.0)

    # Inlet Mach 0.1 (Subsonic, consistent with geometry)
    # A_throat=1.0. A_inlet=3.0.
    # If M=0.3, A/A* ~ 2.035 -> A* = 1.47. A_throat < A*, impossible.
    # If M=0.1, A/A* ~ 5.82 -> A* = 0.51. A_throat > A*, valid.
    res = nozzle.solve_isentropic(M_inlet=0.1)

    # mdot = rho * u * A
    mdot = res.rho * res.u * res.A

    # Check consistency
    mdot_in = mdot[0]
    mdot_throat = mdot[np.argmin(res.A)]
    mdot_ex = mdot[-1]

    # Should be constant within numerical precision
    # Using relative error
    assert abs((mdot_in - mdot_ex)/mdot_in) < 1e-4
    assert abs((mdot_in - mdot_throat)/mdot_in) < 1e-4

    # Also check standard solve with back pressure
    # Choked flow
    res_choked = nozzle.solve(P0=100000, T0=300, back_pressure=10000)
    mdot_choked = res_choked.rho * res_choked.u * res_choked.A

    # Check if constant
    # Note: Across a shock, mass flow is conserved.
    # So even if there is a shock, mdot is constant.

    # Check range of variation
    mdot_mean = np.mean(mdot_choked)
    max_dev = np.max(np.abs(mdot_choked - mdot_mean))

    assert max_dev / mdot_mean < 1e-4
