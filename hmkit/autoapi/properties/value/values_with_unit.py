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

from .current_type import CurrentType
from .unit_type import * 
import logging

log = logging.getLogger('hmkit.autoapi')


class ValueWithUnit(object):
    """
    Represents data with Units
    """

    def __init__(self, value, unit):
        """
        Object to hold data with Units

        :param double value: 
        :param Enum unit: class:`.value.unit_type.*`
        :rtype: None
        """
        # parse the values in terms of value enums
        self.value = value
        self.unit = unit
        log.debug("ValueUnit: value: " + str(self.value) + " ,unit: " + str(self.unit))
        return

    def get_value(self):
        """
        Get value
        :return: value
        :rtype: double
        """
        return self.value

    def get_unit(self):
        """
        Get Unit
        :return: unit
        :rtype: Enum unit: class:`.value.unit_type.*`
        """
        return self.unit


class Current(ValueWithUnit):
    """
    Represents Current property which includes electric current value and :class:`.value.unit_type.ElectricCurrentUnit`
    """

    def __init__(self, value, unit):
        """
        Object to hold the Electric Current value and its Type(AC/DC)

        :param double value: Electric Current
        :param Enum unit: class:`.value.unit_type.ElectricCurrentUnit`
        :rtype: None
        """
        # parse the values in terms of value enums
        super.__init__(value, unit)
        #log.debug("property " + " ,current_value: " + str(self.value) + " ,current_unit: " + str(self.unit))
        return

    def get_current_value(self):
        """
        Get current value
        :return: current value
        :rtype: double
        """
        return self.value

    def get_current_unit(self):
        """
        Get current value
        :return: current unit
        :rtype: Enum unit: class:`.value.current_type.ElectricCurrentUnit`
        """
        return self.unit


class Voltage(ValueWithUnit):
    """
    Represents Voltage property which includes electric voltage value and :class:`.value.unit_type.ElectricPotentialDifferenceUnit`
    """

    def __init__(self, value, unit):
        """
        Object to hold the Electric Voltage value and its Type(AC/DC)
        :param double value: Electric Voltage
        :param Enum unit: class:`.value.unit_type.ElectricPotentialDifferenceUnit`
        :rtype: None
        """
        # parse the values in terms of value enums
        super.__init__(value, unit)
        log.debug("property " + "voltage_value: " + str(self.value) + " ,volt_unit: " + str(self.unit) )
        return

    def get_voltage_value(self):
        """
        Get voltage value
        :return: voltage value
        :rtype: double
        """
        return self.value

    def get_voltage_unit(self):
        """
        Get voltage value
        :return: voltage unit
        :rtype: Enum unit: class:`.value.unit_type.ElectricPotentialDifferenceUnit`
        """
        return self.unit

class Power(ValueWithUnit):
    """
    Represents Power property which includes electric power and :class:`.value.unit_type.PowerUnit`
    """

    def __init__(self, value, unit):
        """
        Object to hold the Electric Power value and its Unit
        :param double value: Electric Power
        :param Enum unit: class:`.value.unit_type.PowerUnit`
        :rtype: None
        """
        # parse the values in terms of value enums
        super.__init__(value, unit)
        log.debug("property " + " ,power_value: " + str(self.value) + " ,power_unit: " + str(self.unit) )
        return

    def get_power_value(self):
        """
        Get Electric Power value
        :return: Electric Power value
        :rtype: double
        """
        return self.value

    def get_power_unit(self):
        """
        Get Electric Power Unit
        :return: Electric Power Unit
        :rtype: Enum unit: class:`.value.unit_type.ElectricPotentialDifferenceUnit`
        """
        return self.unit


class Length(ValueWithUnit):
    """
    Represents Length property which includes length value and :class:`.value.unit_type.LengthUnit`
    """

    def __init__(self, value, unit):
        """
        Object to hold the Length value and its Unit
        :param double value:
        :param Enum length_unit: class:`.value.unit_type.LengthUnit`
        :rtype: None
        """
        # parse the values in terms of value enums
        super.__init__(value, unit)
        log.debug("property " + "length_value: " + str(self.value) + " ,length_unit: " + str(self.unit))
        return

    def get_length_value(self):
        """
        Get Length value
        :return: Length value
        :rtype: double
        """
        return self.value

    def get_unit(self):
        """
        Get Length Unit
        :return: Length unit
        :rtype: class:`.value.unit_type.LengthUnit`
        """
        return self.unit


class Frequency(ValueWithUnit):
    """
    Represents Frequency property which includes frequency value and :class:`.value.unit_type.FrequencyUnit`
    """

    def __init__(self, frequency, freq_unit):
        """
        Object to hold the frequency value and its Unit
        :param double frequency:
        :param Enum freq_unit: class:`.value.unit_type.FrequencyUnit`
        :rtype: None
        """
        # parse the values in terms of value enums
        super.__init__(frequency, freq_unit)
        log.debug("property " + "freq_value: " + str(self.value) + " ,freq_unit: " + str(self.unit))
        return

    def get_freq_value(self):
        """
        Get freq value
        :return: freq value
        :rtype: double
        """
        return self.value

    def get_unit(self):
        """
        Get Freq Unit
        :return: Length unit
        :rtype: class:`.value.unit_type.FrequencyUnit`
        """
        return self.unit

class Duration(ValueWithUnit):
    """
    Represents Duration property which includes duration value and :class:`.value.unit_type.DurationUnit`
    """

    def __init__(self, duration, unit):
        """
        Object to hold the duration value and its Unit
        :param double duration:
        :param Enum freq_unit: class:`.value.unit_type.DurationUnit`
        :rtype: None
        """
        # parse the values in terms of value enums
        super.__init__(duration, unit)
        log.debug("property " + "duration_value: " + str(self.value) + " ,unit: " + str(self.unit))
        return

    def get_duration_value(self):
        """
        Get Duration value
        :return: Duration value
        :rtype: double
        """
        return self.value

    def get_unit(self):
        """
        Get Duration Unit
        :return: Duration unit
        :rtype: class:`.value.unit_type.DurationUnit`
        """
        return self.unit

class Temperature(ValueWithUnit):
    """
    Represents Temperature property which includes temperature value and :class:`.value.unit_type.TemperatureUnit`
    """

    def __init__(self, temperature, unit):
        """
        Object to hold the temperature value and its Unit
        :param double temperature:
        :param Enum unit: class:`.value.unit_type.TemperatureUnit`
        :rtype: None
        """
        # parse the values in terms of value enums
        super.__init__(temperature, unit)
        log.debug("Temperature: value: " + str(self.value) + " ,unit: " + str(self.unit))
        return

    def get_temperature_value(self):
        """
        Get Temperature value
        :return: Temperature value
        :rtype: double
        """
        return self.value

    def get_unit(self):
        """
        Get Temperature Unit
        :return: Temperature unit
        :rtype: class:`.value.unit_type.TemperatureUnit`
        """
        return self.unit

class Volume(ValueWithUnit):
    """
    Represents Volume property which includes volume value and :class:`.value.unit_type.VolumeUnit`
    """

    def __init__(self, volume, unit):
        """
        Object to hold the Volume value and its Unit
        :param double Volume:
        :param Enum unit: class:`.value.unit_type.VolumeUnit`
        :rtype: None
        """
        # parse the values in terms of value enums
        super.__init__(volume, unit)
        log.debug("Volume: value: " + str(self.value) + " ,unit: " + str(self.unit))
        return

    def get_volume_value(self):
        """
        Get Volume value
        :return: Volume value
        :rtype: double
        """
        return self.value

    def get_unit(self):
        """
        Get Volume Unit
        :return: Volume unit
        :rtype: class:`.value.unit_type.VolumeUnit`
        """
        return self.unit

class Torque(ValueWithUnit):
    """
    Represents Torque property which includes volume value and :class:`.value.unit_type.VolumeUnit`
    """

    def __init__(self, torque, unit):
        """
        Object to hold the Torque value and its Unit
        :param double torque:
        :param Enum unit: class:`.value.unit_type.TorqueUnit`
        :rtype: None
        """
        # parse the values in terms of value enums
        super.__init__(torque, unit)
        log.debug("Torque: value: " + str(self.value) + " ,unit: " + str(self.unit))
        return

    def get_torque_value(self):
        """
        Get Torque value
        :return: Torque value
        :rtype: double
        """
        return self.value

    def get_unit(self):
        """
        Get Torque Unit
        :return: Torque unit
        :rtype: class:`.value.unit_type.TorqueUnit`
        """
        return self.unit


#---------------------------- Inherited Classed ---------------------------------------

class HeartRate(Frequency):
    """
    Represents Frequency property which includes frequency value and :class:`.value.unit_type.FrequencyUnit`
    """

    def __init__(self, rate, frequency_unit):
        """
        Object to hold the frequency value and its Unit
        :param double rate:
        :param Enum freq_unit: class:`.value.unit_type.FrequencyUnit`
        :rtype: None
        """
        super().__init__(rate, frequency_unit)
        log.debug("property " + "freq_value: " + str(self.value) + " ,freq_unit: " + str(self.unit))
        return

    def get_heartrate(self):
        """
        Get heartrate value
        :return: heartrate value
        :rtype: double
        """
        return self.value

    def get_unit(self):
        """
        Get heartrat Unit
        :return: heartrate unit
        :rtype: class:`.value.unit_type.FrequencyUnit`
        """
        return self.unit


class EstimatedRange(Length):
    """
    Represents EstimatedRange property which includes estimated distance and unit :class:`.value.unit_type.LengthUnit`
    """

    def __init__(self, value, unit):
        """
        Object to hold the Estimated Distance value and its Unit
        :param double value:
        :param Enum length_unit: class:`.value.unit_type.LengthUnit`
        :rtype: None
        """
        # parse the values in terms of value enums
        super.__init__(value, unit)
        log.debug("property " + "Estimated distance: " + str(self.value) + " ,unit: " + str(self.unit))
        return

    def get_estimated_value(self):
        """
        Get estimated value
        :return: estimated value
        :rtype: double
        """
        return self.value

    def get_unit(self):
        """
        Get estimated Unit
        :return: estimated unit
        :rtype: class:`.value.unit_type.LengthUnit`
        """
        return self.unit
