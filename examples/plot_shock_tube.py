
import matplotlib.pyplot as plt
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rankine.unsteady import ShockTube

def main():
    driver_gas = {'p': 1.0, 'rho': 1.0, 'u': 0.0}
    driven_gas = {'p': 0.1, 'rho': 0.125, 'u': 0.0}

    tube = ShockTube(driver_gas, driven_gas, gamma=1.4)
    tube.solve(time=0.25)

    fig = tube.plot_properties()
    fig.savefig('shock_tube.png')
    print("Generated shock_tube.png")

if __name__ == '__main__':
    main()
