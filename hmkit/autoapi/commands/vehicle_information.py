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

import  base64
import  json
import  codecs
import struct
from hmkit.autoapi.commands import ignition_state, lockstate, parkingbrake_state, charge_state
from .. import identifiers, msg_type, property_enumeration, command_with_properties, command_resolver
import logging
from ..properties import DataMeasurementUnit
from ..properties.value import MeasurementType, CurrentType, PowerTrainType
from ..properties.value.unit_type import *
from ..properties.value.values_with_unit import *

log = logging.getLogger('hmkit.autoapi')

class VehicleInformation(command_with_properties.CommandWithProperties):
    """
    Handle Vehicle Status
    """
    VIN_IDENTIFIER = 0x01
    POWER_TRAIN_IDENTIFIER = 0x02
    MODEL_NAME_IDENTIFIER = 0x03
    NAME_IDENTIFIER = 0x04
    LICENSE_PLATE_IDENTIFIER = 0x05
    SALES_DESIGNATION_IDENTIFIER = 0x06
    MODEL_YEAR_IDENTIFIER = 0x07
    COLOR_IDENTIFIER = 0x08
    POWER_IDENTIFIER = 0x13
    NUMBER_OF_DOORS_IDENTIFIER = 0x0A
    NUMBER_OF_SEATS_IDENTIFIER = 0x0B

    ENGINE_VOLUME_IDENTIFIER = 0x0C
    MAX_TORQUE_IDENTIFIER = 0x0D
    GEARBOX_IDENTIFIER = 0x0E

    DISPLAY_UNIT_IDENTIFIER = 0x0F
    DRIVER_SEAT_LOCATION_IDENTIFIER = 0x10
    EQUIPMENTS_IDENTIFIER = 0x11

    BRAND_IDENTIFIER = 0x12

    def __init__(self, msgbytes):
        """
        Parse the Vehicle Information messagebytes and construct the instance

        :param bytes msgbytes: Vehicle Information message in bytes
        """

        # Construction of Vehicle Information is only required from Car side
        # Hence only parsing is implemented here.
        log.debug(" ")
        super().__init__(msgbytes)

        self.equipments = []
        self.vin = None
        self.powerTrain = None
        self.model_name = None
        self.name =  None
        self.license_plate = None
        self.sales_designation = None
        self.model_year = None
        self.color = None
        self.power = None # properties.value.values_with_unit.Power
        self.number_of_doors = None
        self.number_of_seats = None
        self.engine_volume = None # properties.value.values_with_unit.Volume
        self.max_torque = None # properties.value.values_with_unit.Torque
        self.gearBox = None
        self.displayUnit = None
        self.driverSeatLocation = None
        self.equipments = []
        self.brand = None
 
        while self.properties_iterator.has_next() == True:
            hmprop = self.properties_iterator.next()

            # TODO  
            if hmprop.getproperty_identifier() == VehicleInformation.VIN_IDENTIFIER:
                if hmprop.getcomponent_valuebytes() is not None:
                    self.vin = hmprop.getcomponent_valuebytes().decode("utf-8")
                    log.debug("VIN_IDENTIFIER: vin: " + str(self.vin) )

            elif hmprop.getproperty_identifier() == VehicleInformation.POWER_TRAIN_IDENTIFIER:
                if hmprop.getcomponent_valuebytes() is not None:
                    self.powerTrain = PowerTrainType(hmprop.getcomponent_valuebytes(), None, None)
                    log.debug("POWER_TRAIN_IDENTIFIER powerTrain: " + str(self.powerTrain) )

            elif hmprop.getproperty_identifier() == VehicleInformation.MODEL_NAME_IDENTIFIER:
                if hmprop.getcomponent_valuebytes() is not None:
                    self.model_name = hmprop.getcomponent_valuebytes().decode("utf-8")
                    log.debug("MODEL_NAME_IDENTIFIER:= modelName: " + str(self.model_name) )

            elif hmprop.getproperty_identifier() == VehicleInformation.NAME_IDENTIFIER:
                if hmprop.getcomponent_valuebytes() is not None:
                    self.name = hmprop.getcomponent_valuebytes().decode("utf-8")
                    log.debug("NAME_IDENTIFIER name: " + self.name )

            elif hmprop.getproperty_identifier() == VehicleInformation.LICENSE_PLATE_IDENTIFIER:
                log.debug(" LICENSE_PLATE_IDENTIFIER")
                if hmprop.getcomponent_valuebytes() is not None:
                    self.license_plate = hmprop.getcomponent_valuebytes().decode("utf-8")
                    log.debug("LICENSE_PLATE_IDENTIFIER, licensePlate: " + self.license_plate)

            elif hmprop.getproperty_identifier() == VehicleInformation.SALES_DESIGNATION_IDENTIFIER:
                if hmprop.getcomponent_valuebytes() is not None:
                    self.sales_designation = hmprop.getcomponent_valuebytes().decode("utf-8")
                    log.debug("SALES_DESIGNATION_IDENTIFIER, salesDesignation: " + self.sales_designation )

            elif hmprop.getproperty_identifier() == VehicleInformation.MODEL_YEAR_IDENTIFIER:
                if hmprop.getcomponent_valuebytes() is not None:
                    self.model_year = int.from_bytes(hmprop.getcomponent_valuebytes(), byteorder='big', signed=False)
                    log.debug("MODEL_YEAR_IDENTIFIER, modelYear: " + str(self.model_year))

            elif hmprop.getproperty_identifier() == VehicleInformation.COLOR_IDENTIFIER:
                if hmprop.getcomponent_valuebytes() is not None:
                    self.color = hmprop.getcomponent_valuebytes().decode("utf-8")
                    log.debug("COLOR_IDENTIFIER, color: " + self.color )

            elif hmprop.getproperty_identifier() == VehicleInformation.POWER_IDENTIFIER:
                if hmprop.getcomponent_valuebytes() is not None:
                    data_unit = DataMeasurementUnit(value_compbytes=hmprop.getcomponent_valuebytes())
                    self.power = Power(data_unit.get_data_value(), data_unit.get_unit_type())
                    log.debug("POWER_IDENTIFIER power: " + str(data_unit.get_data_value()) + " ,Unit: " + str(data_unit.get_unit_type()))

            elif hmprop.getproperty_identifier() == VehicleInformation.NUMBER_OF_DOORS_IDENTIFIER:
                if hmprop.getcomponent_valuebytes() is not None:
                    self.number_of_doors = int.from_bytes(hmprop.getcomponent_valuebytes(), byteorder='big', signed=False)
                    log.debug("NUMBER_OF_DOORS_IDENTIFIER, numberOfDoors: " + str(self.number_of_doors ) )

            elif hmprop.getproperty_identifier() == VehicleInformation.NUMBER_OF_SEATS_IDENTIFIER:
                if hmprop.getcomponent_valuebytes() is not None:
                    self.number_of_seats = int.from_bytes(hmprop.getcomponent_valuebytes(), byteorder='big', signed=False)
                    log.debug("NUMBER_OF_SEATS_IDENTIFIER, numberOfSeats: " + str(self.number_of_seats ) )

            elif hmprop.getproperty_identifier() == VehicleInformation.ENGINE_VOLUME_IDENTIFIER:
                if hmprop.getcomponent_valuebytes() is not None:
                    data_unit = DataMeasurementUnit(value_compbytes=hmprop.getcomponent_valuebytes())
                    self.engine_volume = Volume(data_unit.get_data_value(), data_unit.get_unit_type())
                    log.debug("ENGINE_VOLUME_IDENTIFIER engine_volume: " + str(data_unit.get_data_value()) + " ,Unit: " + str(data_unit.get_unit_type()))

            elif hmprop.getproperty_identifier() == VehicleInformation.MAX_TORQUE_IDENTIFIER:
                if hmprop.getcomponent_valuebytes() is not None:
                    data_unit = DataMeasurementUnit(value_compbytes=hmprop.getcomponent_valuebytes())
                    self.max_torque = Torque(data_unit.get_data_value(), data_unit.get_unit_type())
                    log.debug("MAX_TORQUE_IDENTIFIER max_torque: " + str(data_unit.get_data_value()) + " ,Unit: " + str(data_unit.get_unit_type()))

            elif hmprop.getproperty_identifier() == VehicleInformation.GEARBOX_IDENTIFIER:
                log.debug(" GEARBOX_IDENTIFIER")
                if hmprop.getcomponent_valuebytes() is not None:
                    #self.gearBox
                    log.debug("GEARBOX_IDENTIFIER val bytes: " + str(hmprop.getcomponent_valuebytes()) )

            elif hmprop.getproperty_identifier() == VehicleInformation.DISPLAY_UNIT_IDENTIFIER:
                log.debug(" DISPLAY_UNIT_IDENTIFIER")
                if hmprop.getcomponent_valuebytes() is not None:
                    #self.displayUnit
                    log.debug("DISPLAY_UNIT_IDENTIFIER val bytes: " + str(hmprop.getcomponent_valuebytes()) )

            elif hmprop.getproperty_identifier() == VehicleInformation.DRIVER_SEAT_LOCATION_IDENTIFIER:
                log.debug(" DRIVER_SEAT_LOCATION_IDENTIFIER")
                if hmprop.getcomponent_valuebytes() is not None:
                    #self.driverSeatLocation
                    log.debug("DRIVER_SEAT_LOCATION_IDENTIFIER val bytes: " + str(hmprop.getcomponent_valuebytes()) )

            elif hmprop.getproperty_identifier() == VehicleInformation.EQUIPMENTS_IDENTIFIER:
                log.debug(" EQUIPMENTS_IDENTIFIER")
                if hmprop.getcomponent_valuebytes() is not None:
                    # List of Str
                    equipment = hmprop.getcomponent_valuebytes().decode("utf-8")
                    self.equipments.append(equipment)
                    log.debug("EQUIPMENTS_IDENTIFIER equipment: " + equipment )

            elif hmprop.getproperty_identifier() == VehicleInformation.BRAND_IDENTIFIER:
                log.debug(" BRAND_IDENTIFIER")
                if hmprop.getcomponent_valuebytes() is not None:
                    self.brand = hmprop.getcomponent_valuebytes().decode("utf-8")
                    log.debug("BRAND_IDENTIFIER brand: " + self.brand )

        return

    def get_vin(self):
        """
        Get vehicle identifier

        :param None:
        :rtype: str
        """
        return self.vin

    def get_power_train(self):
        """
        Get Power Train

        :param None:
        :rtype: properties.value.power_train_type.PowerTrainType
        """
        return self.powerTrain

    def get_licenseplate(self):
        """
        Get license plate details

        :param None:
        :rtype: str
        """
        return self.license_plate

    def get_power(self):
        """
        Get Power

        :param None:
        :rtype: class: `properties.value.values_with_unit.Power`
        """
        return self.power

    def get_engine_volume(self):
        """
        Get Engine Volume

        :param None:
        :rtype: class: `properties.value.values_with_unit.Volume`
        """
        return self.engine_volume

    def get_max_torque(self):
        """
        Get Max Torque

        :param None:
        :rtype: class: `properties.value.values_with_unit.Torque`
        """
        return self.max_torque

