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
from hmkit.autoapi.commands import *
from hmkit.autoapi.commands import ignition_state, lockstate, parkingbrake_state, charge_state
from .. import identifiers, msg_type, property_enumeration, command_with_properties, command_resolver
import logging

log = logging.getLogger('hmkit.autoapi')

class VehicleStatus(command_with_properties.CommandWithProperties):
    """
    Handle Vehicle Status
    """
    VIN_IDENTIFIER = 0x01;
    POWER_TRAIN_IDENTIFIER = 0x02;
    MODEL_NAME_IDENTIFIER = 0x03;
    NAME_IDENTIFIER = 0x04;
    LICENSE_PLATE_IDENTIFIER = 0x05;
    SALES_DESIGNATION_IDENTIFIER = 0x06;
    MODEL_YEAR_IDENTIFIER = 0x07;
    COLOR_IDENTIFIER = 0x08;
    POWER_IDENTIFIER = 0x09;
    NUMBER_OF_DOORS_IDENTIFIER = 0x0A;
    NUMBER_OF_SEATS_IDENTIFIER = 0x0B;

    ENGINE_VOLUME_IDENTIFIER = 0x0C;
    MAX_TORQUE_IDENTIFIER = 0x0D;
    GEARBOX_IDENTIFIER = 0x0E;

    DISPLAY_UNIT_IDENTIFIER = 0x0F;
    DRIVER_SEAT_LOCATION_IDENTIFIER = 0x10;
    EQUIPMENTS_IDENTIFIER = 0x11;

    BRAND_IDENTIFIER = 0x12;
    STATE_IDENTIFIER = 0x99;

    def __init__(self, msgbytes):
        """
        Parse the Vehicle Status messagebytes and construct the instance

        :param bytes msgbytes: Vehicle Status message in bytes
        """

        # Construction of Lockstate is only required from Car side
        # Hence only parsing is implemented.
        log.debug(" ")
        super().__init__(msgbytes)

        self.states = []
        self.equipments = []
        self.state_ignition = None
        self.state_parkingbreak = None
        self.state_charging = None
        self.state_doorlocks = None

        props = super().getProperties()
        prop_itr = self.properties_iterator 
 
        while self.properties_iterator.has_next() == True:
            hmprop = self.properties_iterator.next()

            # TODO  
            if hmprop.getproperty_identifier() == VehicleStatus.VIN_IDENTIFIER:
                log.debug(" VIN_IDENTIFIER")
                if hmprop.getcomponent_valuebytes() is not None:
                    self.vin = hmprop.getcomponent_valuebytes().decode("utf-8")
                    log.debug("VIN_IDENTIFIER: vin: " + str(self.vin) )

            elif hmprop.getproperty_identifier() == VehicleStatus.POWER_TRAIN_IDENTIFIER:
                log.debug(" POWER_TRAIN_IDENTIFIER")
                if hmprop.getcomponent_valuebytes() is not None:
                    # PowerTrain
                    #self.powerTrain
                    log.debug("POWER_TRAIN_IDENTIFIER: val bytes" + str(hmprop.getcomponent_valuebytes()) )

            elif hmprop.getproperty_identifier() == VehicleStatus.MODEL_NAME_IDENTIFIER:
                log.debug(" MODEL_NAME_IDENTIFIER")
                if hmprop.getcomponent_valuebytes() is not None:
                    self.model_name = hmprop.getcomponent_valuebytes().decode("utf-8")
                    log.debug("MODEL_NAME_IDENTIFIER:= modelName: " + str(self.model_name) )

            elif hmprop.getproperty_identifier() == VehicleStatus.NAME_IDENTIFIER:
                log.debug(" NAME_IDENTIFIER")
                if hmprop.getcomponent_valuebytes() is not None:
                    self.name = hmprop.getcomponent_valuebytes().decode("utf-8")
                    log.debug("NAME_IDENTIFIER name: " + self.name )

            elif hmprop.getproperty_identifier() == VehicleStatus.LICENSE_PLATE_IDENTIFIER:
                log.debug(" LICENSE_PLATE_IDENTIFIER")
                if hmprop.getcomponent_valuebytes() is not None:
                    self.license_plate = hmprop.getcomponent_valuebytes().decode("utf-8")
                    log.debug("LICENSE_PLATE_IDENTIFIER, licensePlate: " + self.license_plate)

            elif hmprop.getproperty_identifier() == VehicleStatus.SALES_DESIGNATION_IDENTIFIER:
                log.debug(" SALES_DESIGNATION_IDENTIFIER")
                if hmprop.getcomponent_valuebytes() is not None:
                    self.sales_designation = hmprop.getcomponent_valuebytes().decode("utf-8")
                    log.debug("SALES_DESIGNATION_IDENTIFIER, salesDesignation: " + self.sales_designation )

            elif hmprop.getproperty_identifier() == VehicleStatus.MODEL_YEAR_IDENTIFIER:
                log.debug(" MODEL_YEAR_IDENTIFIER")
                if hmprop.getcomponent_valuebytes() is not None:
                    self.model_year = int.from_bytes(hmprop.getcomponent_valuebytes(), byteorder='big', signed=False)
                    log.debug("MODEL_YEAR_IDENTIFIER, modelYear: " + str(self.model_year))

            elif hmprop.getproperty_identifier() == VehicleStatus.COLOR_IDENTIFIER:
                log.debug(" COLOR_IDENTIFIER")
                if hmprop.getcomponent_valuebytes() is not None:
                    self.color = hmprop.getcomponent_valuebytes().decode("utf-8")
                    log.debug("COLOR_IDENTIFIER, color: " + self.color )

            elif hmprop.getproperty_identifier() == VehicleStatus.POWER_IDENTIFIER:
                log.debug(" POWER_IDENTIFIER")
                if hmprop.getcomponent_valuebytes() is not None:
                    self.power = int.from_bytes(hmprop.getcomponent_valuebytes(), byteorder='big', signed=False)
                    log.debug("POWER_IDENTIFIER, power: " + str(self.power) )

            elif hmprop.getproperty_identifier() == VehicleStatus.NUMBER_OF_DOORS_IDENTIFIER:
                log.debug(" NUMBER_OF_DOORS_IDENTIFIER")
                if hmprop.getcomponent_valuebytes() is not None:
                    self.number_of_doors = int.from_bytes(hmprop.getcomponent_valuebytes(), byteorder='big', signed=False)
                    log.debug("NUMBER_OF_DOORS_IDENTIFIER, numberOfDoors: " + str(self.number_of_doors ) )

            elif hmprop.getproperty_identifier() == VehicleStatus.NUMBER_OF_SEATS_IDENTIFIER:
                log.debug(" NUMBER_OF_SEATS_IDENTIFIER")
                if hmprop.getcomponent_valuebytes() is not None:
                    self.number_of_seats = int.from_bytes(hmprop.getcomponent_valuebytes(), byteorder='big', signed=False)
                    log.debug("NUMBER_OF_SEATS_IDENTIFIER, numberOfSeats: " + str(self.number_of_seats ) )

            elif hmprop.getproperty_identifier() == VehicleStatus.ENGINE_VOLUME_IDENTIFIER:
                log.debug(" ENGINE_VOLUME_IDENTIFIER")
                if hmprop.getcomponent_valuebytes() is not None:
                    self.engine_volume = struct.unpack('!f',hmprop.getcomponent_valuebytes())
                    log.debug("ENGINE_VOLUME_IDENTIFIER engineVolume: " + str(self.engine_volume ) )

            elif hmprop.getproperty_identifier() == VehicleStatus.MAX_TORQUE_IDENTIFIER:
                log.debug(" MAX_TORQUE_IDENTIFIER")
                if hmprop.getcomponent_valuebytes() is not None:
                    self.max_torque = int.from_bytes(hmprop.getcomponent_valuebytes(), byteorder='big', signed=False)
                    log.debug("MAX_TORQUE_IDENTIFIER maxTorque: " + str(self.max_torque) )

            elif hmprop.getproperty_identifier() == VehicleStatus.GEARBOX_IDENTIFIER:
                log.debug(" GEARBOX_IDENTIFIER")
                if hmprop.getcomponent_valuebytes() is not None:
                    #self.gearBox
                    log.debug("GEARBOX_IDENTIFIER val bytes: " + str(hmprop.getcomponent_valuebytes()) )

            elif hmprop.getproperty_identifier() == VehicleStatus.DISPLAY_UNIT_IDENTIFIER:
                log.debug(" DISPLAY_UNIT_IDENTIFIER")
                if hmprop.getcomponent_valuebytes() is not None:
                    #self.displayUnit
                    log.debug("DISPLAY_UNIT_IDENTIFIER val bytes: " + str(hmprop.getcomponent_valuebytes()) )

            elif hmprop.getproperty_identifier() == VehicleStatus.DRIVER_SEAT_LOCATION_IDENTIFIER:
                log.debug(" DRIVER_SEAT_LOCATION_IDENTIFIER")
                if hmprop.getcomponent_valuebytes() is not None:
                    #self.driverSeatLocation
                    log.debug("DRIVER_SEAT_LOCATION_IDENTIFIER val bytes: " + str(hmprop.getcomponent_valuebytes()) )

            elif hmprop.getproperty_identifier() == VehicleStatus.EQUIPMENTS_IDENTIFIER:
                log.debug(" EQUIPMENTS_IDENTIFIER")
                if hmprop.getcomponent_valuebytes() is not None:
                    # List of Str
                    equipment = hmprop.getcomponent_valuebytes().decode("utf-8")
                    self.equipments.append(equipment)
                    log.debug("EQUIPMENTS_IDENTIFIER equipment: " + equipment )

            elif hmprop.getproperty_identifier() == VehicleStatus.BRAND_IDENTIFIER:
                log.debug(" BRAND_IDENTIFIER")
                if hmprop.getcomponent_valuebytes() is not None:
                    self.brand = hmprop.getcomponent_valuebytes().decode("utf-8")
                    log.debug("BRAND_IDENTIFIER brand: " + self.brand )

            elif hmprop.getproperty_identifier() == VehicleStatus.STATE_IDENTIFIER:
                log.debug(" STATE_IDENTIFIER")
                if hmprop.getcomponent_valuebytes() is not None:
                    log.debug("STATE_IDENTIFIER: val bytes: " + str(hmprop.getcomponent_valuebytes()) )
                    self.proccess_states(hmprop.getcomponent_valuebytes())
        return


    def proccess_states(self, comp_bytes):
        """
        Get vehicle identifier

        :param None:
        :rtyp
        """
        cmd_obj = command_resolver.CommandResolver.resolve(comp_bytes)
        if isinstance(cmd_obj, ignition_state.IgnitionState):
            log.debug("VS: State: IgnitionState")
            self.state_ignition = cmd_obj
            log.debug("VS: State: Ignition: " + str(self.state_ignition.get_engine_ignition()))
            print("VS: State: Ignition: " + str(self.state_ignition.get_engine_ignition()))
        elif isinstance(cmd_obj, lockstate.LockState):
            log.debug("VS: State: Door LockState")
            self.state_doorlocks = cmd_obj
            log.debug("VS: State: Outside Door[0] LockState: " + str(self.state_doorlocks.getoutside_locks()[0].get_lock()))
            print("VS: State: Outside Door[0] LockState: " + str(self.state_doorlocks.getoutside_locks()[0].get_lock()))
        elif isinstance(cmd_obj, charge_state.ChargeState):
            log.debug("VS: State: ChargeState")
            self.state_charging = cmd_obj
            log.debug("VS: State: Charging, Battery Level: " + str(self.state_charging.get_battery_level().getvalue()))
            print("VS: State: Charging, Battery Level: " + str(self.state_charging.get_battery_level().getvalue()))
        elif isinstance(cmd_obj, parkingbrake_state.ParkingBrakeState):
            log.debug("VS: State: ParkingBrakeState")
            self.state_parkingbreak = cmd_obj
            log.debug("VS: State: ParkingBrakeState: is_active: " + str(self.state_parkingbreak.is_active()))
            print("VS: State: ParkingBrakeState: is_active: " + str(self.state_parkingbreak.is_active()))

        else:
            log.debug("VS: State: Others")
        return

    def get_vin(self):
        """
        Get vehicle identifier

        :param None:
        :rtype: str
        """
        return self.vin


    def get_licenseplate(self):
        """
        Get license plate details

        :param None:
        :rtype: str
        """
        return self.license_plate


    def get_state_ignition(self):
        """
        Get Ignition State details

        :param None:
        :rtype: ignition_state.IgnitionState Object
        """
        return self.state_ignition

    def get_state_doorlocks(self):
        """
        Get DoorLock State details

        :param None:
        :rtype: lockstate.LockState Object
        """
        return self.state_doorlocks

    def get_state_chargestate(self):
        """
        Get ChargeState details

        :param None:
        :rtype: charge_state.ChargeState Object
        """
        return self.state_charging

    def get_state_parkingbrake(self):
        """
        Get ParkingBrakeState State details

        :param None:
        :rtype: parkingbrake_state.ParkingBrakeState Object
        """
        return self.state_parkingbreak
