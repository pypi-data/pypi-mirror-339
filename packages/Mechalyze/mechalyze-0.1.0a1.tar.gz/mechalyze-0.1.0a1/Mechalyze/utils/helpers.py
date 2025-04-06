import math

#unit coversions
def mm_to_m(mm):
    return mm / 1000

def m_to_mm(m):
    return m * 1000

def cm_to_m(cm):
    return cm / 100

def m_to_cm(m):
    return m * 100

def km_to_m(km):
    return km * 1000

def m_to_km(m):
    return m / 1000

def inches_to_meters(inches):
    return inches * 0.0254

def meters_to_inches(meters):
    return meters / 0.0254

def feet_to_meters(feet):
    return feet * 0.3048

def meters_to_feet(meters):
    return meters / 0.3048

#area conversion
def sq_mm_to_sq_m(sq_mm):
    return sq_mm / 1e6

def sq_m_to_sq_mm(sq_m):
    return sq_m * 1e6

def sq_cm_to_sq_m(sq_cm):
    return sq_cm / 1e4

def sq_m_to_sq_cm(sq_m):
    return sq_m * 1e4

def sq_km_to_sq_m(sq_km):
    return sq_km * 1e6

def sq_m_to_sq_km(sq_m):
    return sq_m / 1e6

def acres_to_sq_m(acres):
    return acres * 4046.86

def sq_m_to_acres(sq_m):
    return sq_m / 4046.86

def hectares_to_sq_m(hectares):
    return hectares * 1e4

def sq_m_to_hectares(sq_m):
    return sq_m / 1e4

#volume conversion
def ml_to_l(ml):
    return ml / 1000

def l_to_ml(l):
    return l * 1000

def cubic_cm_to_cubic_m(cubic_cm):
    return cubic_cm / 1e6

def cubic_m_to_cubic_cm(cubic_m):
    return cubic_m * 1e6

def cubic_inch_to_cubic_m(cubic_inch):
    return cubic_inch * 1.63871e-5

def cubic_m_to_cubic_inch(cubic_m):
    return cubic_m / 1.63871e-5

def gallons_to_l(gallons):
    return gallons * 3.78541

def l_to_gallons(l):
    return l / 3.78541

#mass conversion
def kg_to_g(kg):
    return kg * 1000

def g_to_kg(g):
    return g / 1000

def tons_to_kg(tons):
    return tons * 1000

def kg_to_tons(kg):
    return kg / 1000

def lb_to_kg(lb):
    return lb * 0.453592

def kg_to_lb(kg):
    return kg / 0.453592

#temperature conversion
def celsius_to_kelvin(celsius):
    return celsius + 273.15

def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5/9

#energy conversion
def joules_to_kilojoules(joules):
    return joules / 1000

def kilojoules_to_joules(kilojoules):
    return kilojoules * 1000

def joules_to_calories(joules):
    return joules / 4.184

def calories_to_joules(calories):
    return calories * 4.184

def joules_to_kilowatt_hours(joules):
    return joules / 3.6e6

def kilowatt_hours_to_joules(kwh):
    return kwh * 3.6e6

#power conversion
def watts_to_kilowatts(watts):
    return watts / 1000

def kilowatts_to_watts(kilowatts):
    return kilowatts * 1000

def watts_to_horsepower(watts):
    return watts / 746

def horsepower_to_watts(hp):
    return hp * 746

#pressure conversion
def pa_to_kpa(pa):
    return pa / 1000

def kpa_to_pa(kpa):
    return kpa * 1000

def atm_to_pa(atm):
    return atm * 101325

def pa_to_atm(pa):
    return pa / 101325

def bar_to_pa(bar):
    return bar * 1e5

def pa_to_bar(pa):
    return pa / 1e5


#rounding off

def round_to(value, decimal_places):
    """Round a value to the specified number of decimal places."""
    return round(value, decimal_places)

def radians(degrees):
    """Convert degrees to radians."""
    return math.radians(degrees)

def degrees(radians):
    """Convert radians to degrees."""
    return math.degrees(radians)



def format_float(value, decimal_places=2):
    """Format a float value to a string with specified decimal places."""
    return f"{value:.{decimal_places}f}"

def pad_string(value, length, char=" "):
    """Pad a string to a specific length with a given character."""
    return str(value).ljust(length, char)

#validating numbers and handling errors
def validate_positive_number(value):
    """Ensure a number is positive; raise ValueError otherwise."""
    if value < 0:
        raise ValueError("Value must be positive.")
    return value

def check_zero_division(divisor):
    """Ensure divisor is not zero."""
    if divisor == 0:
        raise ZeroDivisionError("Cannot divide by zero.")




def flatten_list(nested_list):
    """Flatten a nested list."""
    return [item for sublist in nested_list for item in sublist]

def find_max_index(array):
    """Find the index of the maximum value in an array."""
    return array.index(max(array))

#validating angle and temperature
def is_valid_angle(angle):
    """Check if the angle is between 0 and 360 degrees."""
    return 0 <= angle <= 360

def is_valid_temperature(temp):
    """Check if the temperature is within a realistic range."""
    return -273.15 <= temp <= 1e6  # Temperature range (-273.15°C to arbitrary upper limit)

#scientific notation
def scientific_notation(number, exponent):
    """
    Represent a number in scientific notation with a custom exponential power.
    :param number: The number to format.
    :param exponent: The desired exponential power (base 10).
    :return: String representation of the number in scientific notation.
    """
    if not isinstance(number, (int, float)):
        raise ValueError("The number must be an integer or float.")
    if not isinstance(exponent, int):
        raise ValueError("The exponent must be an integer.")

    # Adjust the number to the desired exponent
    base = number / (10 ** exponent)
    return f"{base}e{exponent}"