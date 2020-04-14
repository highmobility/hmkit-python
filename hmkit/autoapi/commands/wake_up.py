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
from ..properties import hmproperty
from hmkit.autoapi.identifiers import Identifiers
import hmkit.autoapi.msg_type
import logging

log = logging.getLogger('hmkit.autoapi')

class WakeUp(command_with_properties.CommandWithProperties):

    WAKE_UP_PROP_ID = 0x01

    """
    Constructs Wake Up message
    """
    def __init__(self):
        """
        Constructs Wake Up message

        :param None:
        """
        log.debug(" ")
        self.msg_type = msg_type.MsgType(Identifiers.WAKE_UP, 0x01)
        super().__init__(None, self.msg_type)

        self.propblocks = []
        propblock = hmproperty.HmProperty(None, WakeUp.WAKE_UP_PROP_ID, 0x00, None, None)
        self.propblocks.append(propblock)

        super().create_bytes(self.propblocks)
        return
