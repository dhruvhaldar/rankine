
import numpy as np
from rankine.shocks import NormalShock
from rankine.isentropic import IsentropicRelations

class Aerodynamics:
    """
    Aerodynamic theories for compressible flow.
    """

    @staticmethod
    def prandtl_glauert_cp(cp0, M):
        """
        Prandtl-Glauert correction for subsonic compressible flow.
        cp0: Incompressible pressure coefficient.
        M: Freestream Mach number (M < 1).
        """
        if M >= 1.0:
            raise ValueError("Prandtl-Glauert is valid only for subsonic flow (M < 1).")
        return cp0 / np.sqrt(1.0 - M**2)

    @staticmethod
    def ackeret_cp(M, theta):
        """
        Ackeret's Linear Theory for supersonic flow.
        Returns the pressure coefficient Cp on a surface inclined by angle theta.
        M: Freestream Mach number (M > 1).
        theta: Surface inclination angle (radians). Positive for compression (facing flow), negative for expansion.
        """
        if M <= 1.0:
            raise ValueError("Ackeret's theory is valid only for supersonic flow (M > 1).")

        beta = np.sqrt(M**2 - 1.0)
        return 2.0 * theta / beta

    @staticmethod
    def newtonian_cp(M, theta, gamma=1.4):
        """
        Newtonian impact theory for hypersonic flow.
        Returns Cp.
        M: Freestream Mach number (M >> 1).
        theta: Surface inclination angle (radians). Must be positive (facing flow).
        """
        if theta < 0:
            return 0.0 # Shadow region

        # Modified Newtonian
        # Cp_max = (P02 - P_inf) / q_inf
        # q_inf = 0.5 * gamma * P_inf * M^2
        # Cp_max = 2 / (gamma * M^2) * (P02/P_inf - 1)

        # Calculate P02/P_inf using NormalShock and IsentropicRelations
        # P02/P_inf = (P02/P01) * (P01/P_inf)

        # P01/P_inf
        P01_P_inf = IsentropicRelations.calc_pressure_ratio(M, gamma)**(-1) # Since function returns P/P0

        # P02/P01
        ns = NormalShock(M, gamma)
        P02_P01 = ns.P02_P01

        P02_P_inf = P02_P01 * P01_P_inf

        Cp_max = (2.0 / (gamma * M**2)) * (P02_P_inf - 1.0)

        return Cp_max * np.sin(theta)**2
