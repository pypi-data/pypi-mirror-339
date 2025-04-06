

def density(mass, volume):
    """
    Calculate density using ρ = m / V.
    :param mass: Mass of the fluid (kg)
    :param volume: Volume of the fluid (m³)
    :return: Density (kg/m³)
    """
    return mass / volume

def pressure(force, area):
    """
    Calculate pressure using P = F / A.
    :param force: Force applied (N)
    :param area: Area over which the force is applied (m²)
    :return: Pressure (Pa)
    """
    return force / area


def hydrostatic_pressure(density, gravity, depth):
    """
    Calculate hydrostatic pressure using P = ρ * g * h.
    :param density: Density of the fluid (kg/m³)
    :param gravity: Acceleration due to gravity (m/s²)
    :param depth: Depth of the fluid (m)
    :return: Hydrostatic pressure (Pa)
    """
    return density * gravity * depth

def buoyant_force(density, volume, gravity):
    """
    Calculate buoyant force using F_b = ρ * V * g.
    :param density: Density of the fluid (kg/m³)
    :param volume: Volume of the displaced fluid (m³)
    :param gravity: Acceleration due to gravity (m/s²)
    :return: Buoyant force (N)
    """
    return density * volume * gravity

def bernoulli(p1, v1, h1, p2, v2, h2, density, gravity):
    """
    Check if Bernoulli's equation holds true.
    :param p1: Initial pressure (Pa)
    :param v1: Initial velocity (m/s)
    :param h1: Initial height (m)
    :param p2: Final pressure (Pa)
    :param v2: Final velocity (m/s)
    :param h2: Final height (m)
    :param density: Fluid density (kg/m³)
    :param gravity: Acceleration due to gravity (m/s²)
    :return: True if Bernoulli's principle is satisfied, False otherwise
    """
    lhs = p1 + 0.5 * density * v1 ** 2 + density * gravity * h1
    rhs = p2 + 0.5 * density * v2 ** 2 + density * gravity * h2
    return lhs == rhs

def volumetric_flow_rate(area, velocity):
    """
    Calculate volumetric flow rate using Q = A * v.
    :param area: Cross-sectional area (m²)
    :param velocity: Fluid velocity (m/s)
    :return: Volumetric flow rate (m³/s)
    """
    return area * velocity

def reynolds_number(density, velocity, diameter, viscosity):
    """
    Calculate Reynolds number using Re = (ρ * v * D) / μ.
    :param density: Density of the fluid (kg/m³)
    :param velocity: Velocity of the fluid (m/s)
    :param diameter: Characteristic length (e.g., pipe diameter) (m)
    :param viscosity: Dynamic viscosity of the fluid (Pa·s)
    :return: Reynolds number (dimensionless)
    """
    return (density * velocity * diameter) / viscosity

def continuity(area1, velocity1, area2):
    """
    Calculate the velocity at the second section using the continuity equation.
    :param area1: Cross-sectional area at the first section (m²)
    :param velocity1: Velocity at the first section (m/s)
    :param area2: Cross-sectional area at the second section (m²)
    :return: Velocity at the second section (m/s)
    """
    return (area1 * velocity1) / area2

def drag_force(drag_coefficient, density, velocity, area):
    """
    Calculate drag force using F_d = 0.5 * C_d * ρ * v² * A.
    :param drag_coefficient: Coefficient of drag (dimensionless)
    :param density: Density of the fluid (kg/m³)
    :param velocity: Velocity of the object (m/s)
    :param area: Cross-sectional area of the object (m²)
    :return: Drag force (N)
    """
    return 0.5 * drag_coefficient * density * velocity ** 2 * area

