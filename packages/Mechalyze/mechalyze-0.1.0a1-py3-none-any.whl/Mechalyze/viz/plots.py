


import numpy as np
import matplotlib.pyplot as plt
from Mechalyze.calc.mechanics import (
    shear_force, bending_moment, stress, strain, kinetic_energy, potential_energy
)


def plot_shear_force(total_load, distances):
    shear_forces = [shear_force(total_load, d) for d in distances]

    plt.figure()
    plt.plot(distances, shear_forces, label="Shear Force (N)", color="blue")
    plt.xlabel("Distance (m)")
    plt.ylabel("Shear Force (N)")
    plt.title("Shear Force vs. Distance")
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_bending_moment(total_load, distances):
    shear_forces = [shear_force(total_load, d) for d in distances]
    bending_moments = [bending_moment(sf, d) for sf, d in zip(shear_forces, distances)]

    plt.figure()
    plt.plot(distances, bending_moments, label="Bending Moment (N·m)", color="red")
    plt.xlabel("Distance (m)")
    plt.ylabel("Bending Moment (N·m)")
    plt.title("Bending Moment vs. Distance")
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_stress_force(forces, area):
    stresses = [stress(f, area) for f in forces]

    plt.figure()
    plt.plot(forces, stresses, label="Stress (Pa)", color="green")
    plt.xlabel("Force (N)")
    plt.ylabel("Stress (Pa)")
    plt.title("Stress vs. Force")
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_strain_length(change_lengths, original_length):
    strains = [strain(dl, original_length) for dl in change_lengths]

    plt.figure()
    plt.plot(change_lengths, strains, label="Strain", color="purple")
    plt.xlabel("Change in Length (m)")
    plt.ylabel("Strain")
    plt.title("Strain vs. Change in Length")
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_kinetic_energy(masses, velocity_range):
    ke_values = [kinetic_energy(masses, v) for v in velocity_range]

    plt.figure()
    plt.plot(velocity_range, ke_values, label="Kinetic Energy (J)", color="orange")
    plt.xlabel("Velocity (m/s)")
    plt.ylabel("Kinetic Energy (J)")
    plt.title("Kinetic Energy vs. Velocity")
    plt.legend()
    plt.grid(True)
    plt.show()


print(plot_shear_force(8,[2,4,5]))