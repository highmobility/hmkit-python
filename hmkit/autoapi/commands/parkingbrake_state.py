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
from .. import identifiers
from .. import msg_type, property_enumeration, command_with_properties
import hmkit.autoapi
from hmkit.autoapi.identifiers import Identifiers
import hmkit.autoapi.msg_type
import logging

log = logging.getLogger('hmkit.autoapi')

class ParkingBrakeState(command_with_properties.CommandWithProperties):
    """
    Parses Parking Break State Message
    """

    PARKING_BRAKE_IDENTIFIER = 0x01

    def __init__(self, msgbytes):
        """
        Parses Parking Break State Message and constructs Instance

        :param bytes msgbytes: Parking Break State message bytes
        """

        # Construction of ParkingBrakeState is required only in Car side
        # Hence only parsing is implemented for device
        log.debug(" ")
        super().__init__(msgbytes)

        self.parking_brake_state = bool() #bool

        props = super().getProperties()
        prop_itr = self.properties_iterator

        while self.properties_iterator.has_next() == True:
            hmprop = self.properties_iterator.next()

            # TODO
            if hmprop.getproperty_identifier() == ParkingBrakeState.PARKING_BRAKE_IDENTIFIER:
                log.debug("PARKING_BRAKE_IDENTIFIER")
                if hmprop.getcomponent_valuebytes() is not None:                 
                    log.debug("State: " + str(hmprop.getcomponent_valuebytes()))
                    log.debug("int State: " + str(bool(int.from_bytes(hmprop.getcomponent_valuebytes(), byteorder='big', signed=False))))               
                    self.parking_brake_state = bool(int.from_bytes(hmprop.getcomponent_valuebytes(), byteorder='big', signed=False))
                    log.debug("State bool: " + str(self.parking_brake_state))
        return


    def is_active(self):
        """
        Returns the Brake Active state

        :param None:
        :rtype: bool
        """
        return self.parking_brake_state

