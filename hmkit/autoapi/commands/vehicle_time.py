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
from .. import identifiers, msg_type, property_enumeration, command_with_properties
from ..properties import hmproperty
import logging

log = logging.getLogger('hmkit.autoapi')

class VehicleTime(command_with_properties.CommandWithProperties):
    """
    Handle Vehicle Time
    """
    VEHICLE_TIME_IDENTIFIER = 0x01

    def __init__(self, msgbytes):
        """
        Parse the VehicleTime messagebytes and construct the instance

        :param bytes msgbytes: VehicleTime message in bytes
        """
        # Construction of VehicleTime is only required from Car side
        # Hence only parsing is implemented.
        log.debug(" ")
        super().__init__(msgbytes)

        self.hour = None
        self.min = None

        props = super().getProperties()
        prop_itr = self.properties_iterator 

        hmprop = self.properties_iterator.next()

        # TODO
        if hmprop.getproperty_identifier() == VehicleTime.VEHICLE_TIME_IDENTIFIER:
            log.debug(" VEHICLE_TIME_IDENTIFIER")
            if hmprop.getcomponent_valuebytes() is not None:
                valbytes = hmprop.getcomponent_valuebytes()
                self.hour = valbytes[0]
                self.min = valbytes[1]
                print(" VEHICLE_TIME_IDENTIFIER, HOURS: ", self.hour, " Mins: ", self.min)
                #self.engine_ignition = bool(int.from_bytes(hmprop.getcomponent_valuebytes(), byteorder='big', signed=False))

        return

    def get_vehicle_time(self):
        """
        Get Vehicle Time

        :param None:
        :rtype: dict
        """
        vehicle_time = {}
        vehicle_time["hour"] = self.hour
        vehicle_time["mins"] = self.min

        return self.vehicle_time

