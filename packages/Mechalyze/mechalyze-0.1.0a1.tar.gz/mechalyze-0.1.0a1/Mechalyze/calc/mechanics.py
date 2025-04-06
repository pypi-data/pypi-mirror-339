
import math

def horizontal_equilibrium(forces):
    """Check if the sum of horizontal forces equals zero."""
    return sum(forces) == 0

def vertical_equilibrium(forces):
    """Check if the sum of vertical forces equals zero."""
    return sum(forces) == 0

def moment_equilibrium(moments):
    """Check if the sum of moments equals zero."""
    return sum(moments) == 0

def moment(force, distance):
    """
    Calculate the moment of a force.
    :param force: Force (N)
    :param distance: Perpendicular distance to the axis (m)
    :return: Moment (N·m)
    """
    return force * distance


def normal_force(mass, angle):
    """
    Calculate the normal force on an inclined plane.
    :param mass: Mass of the object (kg)
    :param angle: Angle of inclination (degrees)
    :return: Normal force (N)
    """
    g = 9.81  # Acceleration due to gravity (m/s²)
    return mass * g * math.cos(math.radians(angle))

def frictional_force(normal_force, coefficient_of_friction):
    """
    Calculate the frictional force.
    :param normal_force: Normal force (N)
    :param coefficient_of_friction: Coefficient of friction (dimensionless)
    :return: Frictional force (N)
    """
    return normal_force * coefficient_of_friction

def center_of_mass(masses, positions):
    """
    Calculate the center of mass.
    :param masses: List of masses (kg)
    :param positions: List of positions corresponding to the masses (m)
    :return: Center of mass position (m)
    """
    total_mass = sum(masses)
    weighted_positions = sum(m * x for m, x in zip(masses, positions))
    return weighted_positions / total_mass

def shear_force(total_load, distance):
    """
    Calculate the shear force at a section of a beam.
    :param total_load: Total load applied (N)
    :param distance: Distance from the start of the beam (m)
    :return: Shear force (N)
    """
    return total_load * distance

def bending_moment(shear_force, distance):
    """
    Calculate the bending moment at a section of a beam.
    :param shear_force: Shear force (N)
    :param distance: Distance from the start of the beam (m)
    :return: Bending moment (N·m)
    """
    return shear_force * distance

def stress(force, area):
    """
    Calculate the stress on a material.
    :param force: Force (N)
    :param area: Cross-sectional area (m²)
    :return: Stress (Pa)
    """
    return force / area

def strain(change_in_length, original_length):
    """
    Calculate the strain on a material.
    :param change_in_length: Change in length (m)
    :param original_length: Original length (m)
    :return: Strain (dimensionless)
    """
    return change_in_length / original_length

def safety_factor(yield_stress, applied_stress):
    """
    Calculate the safety factor.
    :param yield_stress: Yield stress of the material (Pa)
    :param applied_stress: Applied stress (Pa)
    :return: Safety factor (dimensionless)
    """
    return yield_stress / applied_stress

def acceleration(final_velocity, initial_velocity, time):
    """
    Calculate acceleration using a = (v - u) / t.
    :param final_velocity: Final velocity (m/s)
    :param initial_velocity: Initial velocity (m/s)
    :param time: Time taken (s)
    :return: Acceleration (m/s²)
    """
    return (final_velocity - initial_velocity) / time

def final_velocity(initial_velocity, acceleration, time):
    """
    Calculate final velocity using v = u + at.
    :param initial_velocity: Initial velocity (m/s)
    :param acceleration: Acceleration (m/s²)
    :param time: Time (s)
    :return: Final velocity (m/s)
    """
    return initial_velocity + acceleration * time

def distance(initial_velocity, acceleration, time):
    """
    Calculate distance using s = ut + 0.5 * a * t².
    :param initial_velocity: Initial velocity (m/s)
    :param acceleration: Acceleration (m/s²)
    :param time: Time (s)
    :return: Distance (m)
    """
    return (initial_velocity * time) + (0.5 * acceleration * time ** 2)

def force(mass, acceleration):
    """
    Calculate force using F = ma.
    :param mass: Mass (kg)
    :param acceleration: Acceleration (m/s²)
    :return: Force (N)
    """
    return mass * acceleration

import math

def work(force, displacement, angle):
    """
    Calculate work using W = F * d * cos(θ).
    :param force: Force (N)
    :param displacement: Displacement (m)
    :param angle: Angle between force and displacement (degrees)
    :return: Work (J)
    """
    return force * displacement * math.cos(math.radians(angle))

def kinetic_energy(mass, velocity):
    """
    Calculate kinetic energy using KE = 0.5 * m * v².
    :param mass: Mass (kg)
    :param velocity: Velocity (m/s)
    :return: Kinetic Energy (J)
    """
    return 0.5 * mass * velocity ** 2

def potential_energy(mass, height):
    """
    Calculate potential energy using PE = mgh.
    :param mass: Mass (kg)
    :param height: Height (m)
    :return: Potential Energy (J)
    """
    g = 9.81  # Acceleration due to gravity (m/s²)
    return mass * g * height

def momentum(mass, velocity):
    """
    Calculate momentum using p = mv.
    :param mass: Mass (kg)
    :param velocity: Velocity (m/s)
    :return: Momentum (kg·m/s)
    """
    return mass * velocity

def impulse(force, time):
    """
    Calculate impulse using I = F * t.
    :param force: Force (N)
    :param time: Time (s)
    :return: Impulse (N·s)
    """
    return force * time

def power(work, time):
    """
    Calculate power using P = W / t.
    :param work: Work done (J)
    :param time: Time (s)
    :return: Power (W)
    """
    return work / time
