"""
The MIT License

Copyright (c) 2014- High-Mobility GmbH (https://high-mobility.com)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

from enum import Enum, unique
import logging

log = logging.getLogger('hmkit.autoapi')

@unique
class AccelerationUnit(Enum):
    """
    Enum Class for Acceleration unit Type
    """
    METERS_PER_SECOND_SQUARED = 0x00
    GRAVITY = 0x01

@unique
class AngleUnit(Enum):
    """
    Enum Class for Angle unit Type
    """
    DEGREES = 0x00
    RADIANS = 0x03
    REVOLUTIONS = 0x05

@unique
class AngularVelocityUnit(Enum):
    """
    Enum Class for AngularVelocity unit Type
    """
    REVOLUTIONS_PER_MINUTE = 0x00
    DEGREES_PER_SECOND = 0x01
    RADIANS_PER_SECOND = 0x02

@unique
class DurationUnit(Enum):
    """
    Enum Class for Duration unit Type
    """
    SECONDS = 0x00
    MINUTES = 0x01
    HOURS = 0x02
    DAYS = 0x03
    WEEKS = 0x04
    MONTHS = 0x05

@unique
class ElectricCurrentUnit(Enum):
    """
    Enum Class for Electric Current unit Type
    """
    AMPERES = 0x00
    MILLIAMPERES = 0x01
    KILOAMPERES = 0x02

@unique
class ElectricPotentialDifferenceUnit(Enum):
    """
    Enum Class for Electric Potential Difference unit Type
    """
    VOLTS = 0x00
    MILLIVOLTS = 0x01
    KILOVOLTS = 0x02

@unique
class EnergyUnit(Enum):
    """
    Enum Class for Energy unit Type
    """
    JOULES = 0x00
    KILOJOULES = 0x01
    KILOWATTJOULES = 0x04

@unique
class EnergyEfficiencyUnit(Enum):
    """
    Enum Class for Energy Efficiency unit Type
    """
    KWH_PER_100_KILOMETERS = 0x00
    MILES_PER_KWH = 0x01

@unique
class FrequencyUnit(Enum):
    """
    Enum Class for Frequency unit Type
    """
    HERTZ = 0x00
    MILLIHERTZ = 0x01
    KILOHERTZ = 0x03
    MEGAHERTZ = 0x04
    GIGAHERTZ = 0x05
    BEATS_PER_MINUTE = 0x08

@unique
class FuelEfficiencyUnit(Enum):
    """
    Enum Class for Fuel Efficiency unit Type
    """
    LITERS_PER_100_KILOMETERS = 0x00
    MILES_PER_IMPERIAL_GALLON = 0x01
    MILES_PER_GALLON = 0x02

@unique
class IlluminanceUnit(Enum):
    """
    Enum Class for Illuminance unit Type
    """
    LUX = 0x00

@unique
class LengthUnit(Enum):
    """
    Enum Class for Length unit Type
    """
    METERS = 0x00
    MILLIMETERS = 0x01
    CENTIMETERS = 0x02
    DECIMETERS = 0x03
    KILOMETERS = 0x04
    MEGAMETERS = 0x05
    INCHES = 0x0b
    FEET = 0x0c
    YARDS = 0x0d
    MILES = 0x0e
    SCANDINAVIAN_MILES = 0x0f
    NAUTICAL_MILES = 0x11

@unique
class PowerUnit(Enum):
    """
    Enum Class for Power unit Type
    """
    WATTS = 0x00
    MILLIWATTS = 0x01
    KILOWATTS = 0x02
    MEGAWATTS = 0x03
    HORSEPOWER = 0x0a

@unique
class PressureUnit(Enum):
    """
    Enum Class for Pressure unit Type
    """
    NEWTONS_PER_METERS_SQUARED = 0x00
    KILOPASCALS = 0x03
    INCHES_OF_MERCURY = 0x05
    BARS = 0x06
    MILLIBARS = 0x07
    MILLIMETERS_OF_MERCURY = 0x08
    POUNDS_FORCE_PER_SQUARE_INCH = 0x09

@unique
class SpeedUnit(Enum):
    """
    Enum Class for Speed unit Type
    """
    METERS_PER_SECOND = 0x00
    KILOMETERS_PER_HOUR = 0x01
    MILES_PER_HOUR = 0x02
    KNOTS = 0x03

@unique
class TemperatureUnit(Enum):
    """
    Enum Class for Temperature unit Type
    """
    KELVIN = 0x00
    CELSIUS = 0x01
    FAHRENHEIT = 0x02

@unique
class TorqueUnit(Enum):
    """
    Enum Class for Torque unit Type
    """
    NEWTON_METERS = 0x00
    NEWTON_MILLIMETERS = 0x01
    POUND_FEET = 0x02

@unique
class VolumeUnit(Enum):
    """
    Enum Class for Volume unit Type
    """
    LITERS = 0x02
    MILLILITERS = 0x03
    CENTILITERS = 0x04
    DECILITERS = 0x05
    CUBIC_MILLIMETERS = 0x0a
    CUBIC_CENTIMETERS = 0x09
    CUBIC_DECIMETERS = 0x08
    CUBIC_METERS = 0x07
    CUBIC_INCHES = 0x0b
    CUBIC_FEET = 0x0c
    FLUID_OUNCES = 0x13
    GALLONS = 0x17
    IMPERIAL_FLUID_OUNCES = 0x1a
    IMPERIAL_GALLONS = 0x01d
