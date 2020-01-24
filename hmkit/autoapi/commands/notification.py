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
from ..properties.value.action_item import ActionItem
import logging

log = logging.getLogger('hmkit.autoapi')

class Notification(command_with_properties.CommandWithProperties):
    """
    Constructs Notification message
    """
    IDENTIFIER_TEXT = 0x01
    IDENTIFIER_ACTION_ITEM = 0x02

    def __init__(self, text, actionitems, msgbytes=None):
        """
        Constructs Notification message

        :param None:
        """
        log.debug(" ")
        self.msg_type = msg_type.MsgType(Identifiers.NOTIFICATIONS,0x01)

        if text is not None:

            # construct message bytes case
            super().__init__(None, self.msg_type)
            # create a property
            # TODO, get timestamp and failure from arg  
            log.debug("__init__ text: " + text + " actionitems: " + str(actionitems))
            self.propblocks = []
            propblock = hmproperty.HmProperty(None, Notification.IDENTIFIER_TEXT, text, None, None)
            self.propblocks.append(propblock)

            if isinstance(actionitems, list) and isinstance(actionitems[0], ActionItem):

                for actionitem in actionitems:
                    set_chargingtimer = hmproperty.HmProperty(None, Notification.IDENTIFIER_ACTION_ITEM, actionitem, None, None)
                    self.propblocks.append(set_chargingtimer)

            super().create_bytes(self.propblocks)

        elif msgbytes is not None:
            # parsing case
            super().__init__(msgbytes)

            #log.info("__init__ parsing not implemented for link device")
        else:
            log.error("invalid argument type")
        return
