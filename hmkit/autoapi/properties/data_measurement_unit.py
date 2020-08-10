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

import sys
import codecs
import traceback
import struct
import logging
#from .commands import *

#from . import identifiers
from .value.unit_type import *
from .value.measurement_type import MeasurementType

log = logging.getLogger('hmkit.autoapi')

class DataMeasurementUnit(object):
    """
    parses the data bytes and 
    """
    # Lookup table (Dictionary) that links measurement type to unit type enums
    Measurement_Unit_map = { MeasurementType.ACCELERATION.value:AccelerationUnit,
    MeasurementType.ANGLE.value:AngleUnit,
    MeasurementType.ANGULAR_VELOCITY.value:AngularVelocityUnit,
    MeasurementType.DURATION.value:DurationUnit,
    MeasurementType.ELECTRIC_CURRENT.value:ElectricCurrentUnit,
    MeasurementType.ELECTRIC_POTENTIAL_DIFFERENCE.value:ElectricPotentialDifferenceUnit,
    MeasurementType.ENERGY.value:EnergyUnit,
    MeasurementType.ENERGY_EFFICIENCY.value:EnergyEfficiencyUnit,
    MeasurementType.FREQUENCY.value:FrequencyUnit,
    MeasurementType.FUEL_EFFICIENCY.value:FuelEfficiencyUnit,
    MeasurementType.ILLUMINANCE.value:IlluminanceUnit,
    MeasurementType.LENGTH.value:LengthUnit,
    MeasurementType.POWER.value:PowerUnit,
    MeasurementType.PRESSURE.value:PressureUnit,
    MeasurementType.SPEED.value:SpeedUnit,
    MeasurementType.TEMPERATURE.value:TemperatureUnit,
    MeasurementType.TORQUE.value:TorqueUnit,
    MeasurementType.VOLUME.value:VolumeUnit }

    def __init__(self, value_compbytes=None, measurement_type=None, unit_type=None, data_value=None):
        """
        parses the data bytes and returns the 

        :param  bytearray value_compbytes: autoapi data bytes
        :return: Autoapi class object with super type :class:` `
        :rtype: :class:` ` 
        """
        if value_compbytes is not None: # Parsing

            self.value_compbytes = value_compbytes
            self.parse_bytes()
            
            #self.charge_limit = DoubleHm(charge_limit[0])
            log.debug("DataUnit ,measurement_type: " + str(self.measurement_type) + " ,unit_type: "  + str(self.unit_type) + " ,value_compbytes: " + str(self.value_compbytes))

        else: # Construct

            self.measurement_type = measurement_type
            self.unit_type = unit_type
            self.data_value = data_value  #double

            self.create_bytes()
            log.debug("DataUnit ,measurement_type: " + str(self.measurement_type) + " ,unit_type: "  + str(self.unit_type) + " ,value_compbytes: " + str(self.value_compbytes))
        return

    def parse_bytes(self):
        #self.measurement_type = MeasurementType(codecs.encode(value_compbytes[0], 'hex'))
        self.measurement_type = MeasurementType(self.value_compbytes[0])

        # get the List for the identifier which contain ID String and Msg Type list
        unit_type_enum = DataMeasurementUnit.Measurement_Unit_map.get(self.measurement_type)
        #self.unit_type = unit_type_enum(codecs.encode(value_compbytes[1], 'hex'))
        self.unit_type = unit_type_enum(self.value_compbytes[1])

        value_bytes = self.value_compbytes[2:10] # 8 bytes
        self.data_value = struct.unpack('!d', value_bytes) #double value and big endian
        return

    def create_bytes(self):

        data_unit_bytes = bytearray()
        data_unit_bytes.append(self.measurement_type.value) # Enum
        data_unit_bytes.append(self.unit_type.value) # Enum
        data_unit_bytes += bytearray(struct.pack("!d", self.data_value)) # ! - big endian
        self.value_compbytes = data_unit_bytes
        return

    def get_bytes(self):
        return self.value_compbytes

    def get_measurement_type(self):
        return self.measurement_type

    def get_unit_type(self):
        return self.unit_type

    def get_data_value(self):
        return self.data_value
