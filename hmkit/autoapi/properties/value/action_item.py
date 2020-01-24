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

import datetime
import logging
from . import *
from .. import propertyvalue_object

log = logging.getLogger('hmkit.autoapi')

class ActionItem(propertyvalue_object.PropertyValueObject):
    """

    """

    def __init__(self, actionid, actiontext, propbytes=None):
        """
        Property bytes will be parsed to get internal data values

        :param bytearray propbytes: Property Component Bytes
        :rtype: None
        """

        self.text_len = 0x0000

        if propbytes is not None:
            super().__init__(propbytes)
            self.valbytes = propbytes
            self.id = int(propbytes[0])
            text_len_bytes = propbytes[1:3]
            self.text_len = int.from_bytes(text_len_bytes, byteorder='big', signed=False)
            self.text = propbytes[3:]
            log.debug("valbytes: " + str(self.valbytes))
            log.debug("ActionItem  property " + "ID: " + str(self.id) + " ,Text: " + str(self.text) + " Text Len: " + str(self.text_len))
            print("***** ActionItem  property " + "ID: " + str(self.id) + " ,Text: " + str(self.text) + " Text Len: " + str(self.text_len))
        else:
            self.id = actionid
            self.text = actiontext
            self.text_len = len(actiontext)
            self.valbytes = bytearray()
            # how many bytes it will take ??
            self.valbytes.append(self.id)
            text_len_bytes = self.text_len.to_bytes(2, byteorder='big')
            self.valbytes += text_len_bytes
            self.valbytes += self.text.encode()
            super().__init__(self.valbytes)
            log.debug("valbytes: " + str(self.valbytes))
            log.debug("ActionItem  property " + "ID: " + str(self.id) + " ,Text: " + str(self.text) + " Text Len: " + str(self.text_len))
            print("***** ActionItem  property " + "ID: " + str(self.id) + " ,Text: " + str(self.text) + " Text Len: " + str(self.text_len))
        return
        # need to handle construct with a methods instead of _init_

    def get_action_id(self):
        """
        returns action id

        :return: action id
        :rtype: int
        """
        return self.id

    def get_action_text(self):
        """
        returns action text

        :return: action text
        :rtype: str
        """
        return self.text
