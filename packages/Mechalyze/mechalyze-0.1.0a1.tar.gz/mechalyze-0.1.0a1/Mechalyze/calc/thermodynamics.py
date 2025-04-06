

def boyles_law(initial_pressure, initial_volume, final_volume):
    """
    Calculate final pressure using Boyle's Law: P1 * V1 = P2 * V2.
    :param initial_pressure: Initial pressure (Pa)
    :param initial_volume: Initial volume (m³)
    :param final_volume: Final volume (m³)
    :return: Final pressure (Pa)
    """
    return (initial_pressure * initial_volume) / final_volume

def internal_energy_change(heat_added, work_done):
    """
    Calculate the change in internal energy using ΔU = Q - W.
    :param heat_added: Heat added to the system (J)
    :param work_done: Work done by the system (J)
    :return: Change in internal energy (J)
    """
    return heat_added - work_done

def heat_transfer(mass, specific_heat, temperature_change):
    """
    Calculate heat transfer using Q = mcΔT.
    :param mass: Mass of the substance (kg)
    :param specific_heat: Specific heat capacity (J/kg·K)
    :param temperature_change: Change in temperature (K)
    :return: Heat transferred (J)
    """
    return mass * specific_heat * temperature_change

def heat_engine_efficiency(heat_absorbed, heat_rejected):
    """
    Calculate the efficiency of a heat engine using η = 1 - Qc / Qh.
    :param heat_absorbed: Heat absorbed by the engine (J)
    :param heat_rejected: Heat rejected by the engine (J)
    :return: Efficiency (dimensionless, between 0 and 1)
    """
    return 1 - (heat_rejected / heat_absorbed)

def carnot_efficiency(temperature_hot, temperature_cold):
    """
    Calculate Carnot efficiency using η = 1 - Tc / Th.
    :param temperature_hot: Temperature of the hot reservoir (K)
    :param temperature_cold: Temperature of the cold reservoir (K)
    :return: Carnot efficiency (dimensionless, between 0 and 1)
    """
    return 1 - (temperature_cold / temperature_hot)

def ideal_gas_pressure(moles, temperature, volume, gas_constant=8.314):
    """
    Calculate pressure using the ideal gas law: PV = nRT.
    :param moles: Number of moles of gas (mol)
    :param temperature: Temperature (K)
    :param volume: Volume (m³)
    :param gas_constant: Universal gas constant (J/(mol·K))
    :return: Pressure (Pa)
    """
    return (moles * gas_constant * temperature) / volume

def thermal_expansion(initial_length, expansion_coefficient, temperature_change):
    """
    Calculate thermal expansion using ΔL = αL0ΔT.
    :param initial_length: Initial length of the material (m)
    :param expansion_coefficient: Coefficient of linear thermal expansion (1/K)
    :param temperature_change: Change in temperature (K)
    :return: Change in length (m)
    """
    return initial_length * expansion_coefficient * temperature_change

import math

def isothermal_work(moles, temperature, initial_volume, final_volume, gas_constant=8.314):
    """
    Calculate work done during an isothermal process: W = nRT ln(Vf / Vi).
    :param moles: Number of moles of gas (mol)
    :param temperature: Temperature (K)
    :param initial_volume: Initial volume (m³)
    :param final_volume: Final volume (m³)
    :param gas_constant: Universal gas constant (J/(mol·K))
    :return: Work done (J)
    """
    return moles * gas_constant * temperature * math.log(final_volume / initial_volume)

def adiabatic_pressure_volume(initial_pressure, initial_volume, final_volume, heat_capacity_ratio):
    """
    Calculate final pressure in an adiabatic process using P1 * V1^γ = P2 * V2^γ.
    :param initial_pressure: Initial pressure (Pa)
    :param initial_volume: Initial volume (m³)
    :param final_volume: Final volume (m³)
    :param heat_capacity_ratio: Ratio of specific heats (γ = Cp/Cv)
    :return: Final pressure (Pa)
    """
    return initial_pressure * (initial_volume / final_volume) ** heat_capacity_ratio