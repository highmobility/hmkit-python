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

log = logging.getLogger('hmkit.autoapi')

class VehicleStatus(command_with_properties.CommandWithProperties):
    """
    Handle Vehicle Status
    """

    STATE_IDENTIFIER = 0x99;

    def __init__(self, msgbytes):
        """
        Parse the Vehicle Status messagebytes and construct the instance

        :param bytes msgbytes: Vehicle Status message in bytes
        """

        # Construction of VehicleStatus is only required from Car side
        # Hence only parsing is implemented here.
        log.debug(" ")
        super().__init__(msgbytes)

        self.states = []
        self.equipments = []
        self.state_ignition = None
        self.state_parkingbreak = None
        self.state_charging = None
        self.state_doorlocks = None
 
        while self.properties_iterator.has_next() == True:
            hmprop = self.properties_iterator.next()

            if hmprop.getproperty_identifier() == VehicleStatus.STATE_IDENTIFIER:
                log.debug(" STATE_IDENTIFIER")
                if hmprop.getcomponent_valuebytes() is not None:
                    log.debug("STATE_IDENTIFIER: val bytes: " + str(hmprop.getcomponent_valuebytes()) )
                    self.proccess_states(hmprop.getcomponent_valuebytes())
            else:
                log.info("Wrong Property ID: " + str(hmprop.getproperty_identifier()))

        return

    def proccess_states(self, comp_bytes):
        """
        Process the different states received

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
