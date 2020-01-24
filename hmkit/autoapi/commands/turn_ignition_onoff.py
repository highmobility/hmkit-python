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
import hmkit.autoapi
from .. import msg_type, property_enumeration, command_with_properties
from hmkit.autoapi.identifiers import Identifiers
import hmkit.autoapi.msg_type
from ..properties import hmproperty
import logging

log = logging.getLogger('hmkit.autoapi')

class TurnIgnitionOnOff(command_with_properties.CommandWithProperties):
    """
    Constructs TurnIgnitionOnOff message bytes 
    """

    IGNITION_IDENTIFIER = 0x01

    def __init__(self, ignition_on, msgbytes=None):
        """
        Constructs TurnIgnitionOnOff message bytes and constructs a Instance

        :param bool: 
        """
        log.debug(" ")

        self.msg_type = msg_type.MsgType(Identifiers.ENGINE,0x01)

        if ignition_on is not None:
            # construct case
            super().__init__(None, self.msg_type)
            # create a property
            # TODO, get timestamp and failure from arg  
            log.debug("__init__ ignition_on: " + str(ignition_on))
            propblock = hmproperty.HmProperty(None, TurnIgnitionOnOff.IGNITION_IDENTIFIER, ignition_on, None, None)
            super().create_bytes(propblock)
        elif isinstance(msgbytes, (bytes, bytearray)):
            # NOTE: parsing case NOT needed for link device
            super().__init__(msgbytes)
            log.info("__init__ parsing not implemented for link device")
        else:
            log.error("invalid argument type")
        return

