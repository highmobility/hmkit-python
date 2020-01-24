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
from ..properties import hmproperty
import logging

log = logging.getLogger('hmkit.autoapi')

class SetParkingBrakeState(command_with_properties.CommandWithProperties):
    """
    Constructs Set Parking Brake State message
    """
    parkingbrake_state_prop_id = 0x01

    def __init__(self, arg):
        """
        Construct Set Parking Brake State message bytes and Construct an instance

        :param bool arg: True - Activate, False - Inactivate
        """
        log.debug("  ")
        self.msg_type = msg_type.MsgType(Identifiers.PARKING_BRAKE,0x01)

        if isinstance(arg, bool):
            # construct case
            super().__init__(None, self.msg_type)
            # create a property
            # TODO, get timestamp and failure from arg  
            log.info("arg: " + str(arg))
            self.parkbrakestate = hmproperty.HmProperty(None, SetParkingBrakeState.parkingbrake_state_prop_id, arg, None, None)
            super().create_bytes(self.parkbrakestate)
        elif isinstance(arg, (bytes, bytearray)):
            # NOTE: parsing case NOT needed for link device
            super().__init__(arg)
            log.info("parse case not required in Link and not implemented")
        else:
            log.error("invalid argument type")
        return

    def get_parkbrakestate(self):
        """
        < Internal Use >

        :param None:
        :rtype: hmproperty.HmProperty
        """
        return self.parkbrakestate
