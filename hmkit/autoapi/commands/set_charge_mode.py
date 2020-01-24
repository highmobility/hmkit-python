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
from enum import Enum, unique
from ..properties.value.charging.charge_mode import ChargeMode
import logging

log = logging.getLogger('hmkit.autoapi')

class SetChargeMode(command_with_properties.CommandWithProperties):
    """
    Constructs Set Charge Mode message bytes
    """
    charge_mode_prop_id = 0x0c

    def __init__(self, arg):
        """
        Constructs Set Charge Mode message bytes and constructs Instance

        :param enum arg: :Enum class:`..properties.value.charge_mode.ChargeMode`
        """
        log.debug(" ")
        self.msg_type = msg_type.MsgType(Identifiers.CHARGING,0x01)

        if isinstance(arg, Enum):
            # construct case
            super().__init__(None, self.msg_type)
            # create a property
            # TODO, get timestamp and failure from arg  
            log.info("arg: " + str(arg))
            self.charge_mode = hmproperty.HmProperty(None, SetChargeMode.charge_mode_prop_id, arg, None, None)
            super().create_bytes(self.charge_mode)
        elif isinstance(arg, (bytes, bytearray)):
            # NOTE: parsing case NOT needed for link device
            super().__init__(arg)
            log.info("parse case not required in Link device and not implemented")
        else:
            log.error("invalid argument type")
        return

    def get_chargemode(self):
        """
        < For internal use >
        Get the ChargeMode value class:`..properties.value.charge_mode.ChargeMode`

        :param  None:
        :rtype: None
        """
        return self.charge_mode

