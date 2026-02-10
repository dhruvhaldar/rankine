
# rankine/utils.py

# Physical Constants
R_UNIVERSAL = 8314.462618  # J/(kmol·K)
M_AIR = 28.9647            # kg/kmol
R_AIR = R_UNIVERSAL / M_AIR  # J/(kg·K) ≈ 287.05
GAMMA_AIR = 1.4

def c_to_k(celsius):
    """Convert Celsius to Kelvin."""
    return celsius + 273.15

def k_to_c(kelvin):
    """Convert Kelvin to Celsius."""
    return kelvin - 273.15

def pa_to_atm(pa):
    """Convert Pascals to Atmospheres."""
    return pa / 101325.0

def atm_to_pa(atm):
    """Convert Atmospheres to Pascals."""
    return atm * 101325.0
