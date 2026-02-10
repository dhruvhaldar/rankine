
import matplotlib.pyplot as plt
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rankine.isentropic import CDNozzle

def main():
    # Define nozzle: Inlet (stagnation), Throat Area, Exit Area
    nozzle = CDNozzle(gamma=1.4, A_throat=0.05, A_exit=0.1)

    # Example 1: Subsonic (Venturi)
    res_sub = nozzle.solve(P0=101325, T0=300, back_pressure=98000)
    fig_sub = res_sub.plot_distribution()
    fig_sub.savefig('nozzle_subsonic.png')

    # Example 2: Design Condition (Supersonic)
    # P_exit approx P0 * 0.1278 (M=2)
    # A_exit/A_throat = 2.0 -> M=2.2 (approx)
    # Let's find design pressure automatically by solving with very low back pressure
    res_design = nozzle.solve(P0=101325, T0=300, back_pressure=1000)
    fig_design = res_design.plot_distribution()
    fig_design.savefig('nozzle_supersonic.png')

    # Example 3: Shock in Nozzle
    # Back pressure between subsonic limit and design
    res_shock = nozzle.solve(P0=101325, T0=300, back_pressure=60000)
    fig_shock = res_shock.plot_distribution()
    fig_shock.savefig('nozzle_shock.png')

    print("Generated nozzle_subsonic.png, nozzle_supersonic.png, nozzle_shock.png")

if __name__ == '__main__':
    main()
