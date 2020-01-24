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

class StartStopCharging(command_with_properties.CommandWithProperties):
    """
    Constructs StartStopCharging message
    """

    charging_state_prop_id = 0x17

    def __init__(self, arg):
        """
        Constructs Start Stop Charging and constructs an instance

        :param arg : bool 
        :rtype: None
        """
        log.debug(" ")
        self.msg_type = msg_type.MsgType(Identifiers.CHARGING,0x01)

        if isinstance(arg, bool):
            # construct case
            super().__init__(None, self.msg_type)
            # create a property
            # TODO, get timestamp and failure from arg  
            log.debug("arg: " + str(arg))
            self.charging_state = hmproperty.HmProperty(None, StartStopCharging.charging_state_prop_id, arg, None, None)
            super().create_bytes(self.charging_state)
        elif isinstance(arg, (bytes, bytearray)):
            # NOTE: parsing case NOT needed for link device
            super().__init__(arg)
            log.debug("StartStopCharging parse case not required in Link and not implemented")
        else:
            log.debug("invalid argument type")
        return


    def get_chargingstate(self):
        """
        < For internal use >
        Get Charging State

        :param None:
        :rtype: HmProperty (charging_state)
        """
        return self.charging_state

