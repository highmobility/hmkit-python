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
from ..properties import hmproperty
import hmkit.autoapi
from hmkit.autoapi.identifiers import Identifiers
import hmkit.autoapi.msg_type
import logging

log = logging.getLogger('hmkit.autoapi')

class ClearNotification(command_with_properties.CommandWithProperties):

    CLEAR_NOTIFICATION = 0x04

    """
    Constructs Clear Notification
    """
    def __init__(self):
        """
        Constructs Clear Notification message

        :param None:
        """
        log.debug(" ")
        self.msg_type = msg_type.MsgType(Identifiers.NOTIFICATIONS,0x01)
        super().__init__(None, self.msg_type)

        self.propblocks = []
        propblock = hmproperty.HmProperty(None, ClearNotification.CLEAR_NOTIFICATION, 0x00, None, None)
        self.propblocks.append(propblock)

        super().create_bytes(self.propblocks)

        return
