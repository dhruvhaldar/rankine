
import matplotlib.pyplot as plt
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rankine.shocks import ObliqueShock

def main():
    fig = ObliqueShock.plot_polar(mach_numbers=[2.0, 3.0, 5.0], gamma=1.4)
    fig.savefig('shock_polar.png')
    print("Generated shock_polar.png")

if __name__ == '__main__':
    main()
