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
from ..properties.value.lock import Lock
from hmkit.autoapi.identifiers import Identifiers
#import hmkit.autoapi.identifiers as identifiers
import hmkit.autoapi.msg_type
#from ..msg_type import MsgType
from ..properties import hmproperty
#from .. import identifiers 
#from ..identifiers import Identifiers
#from ..identifiers import Identifiers
import logging

log = logging.getLogger('hmkit.autoapi')

class LockUnlockDoors(command_with_properties.CommandWithProperties):
    """
    Constructs LockUnlockDoor message bytes 
    """

    lockst_prop_id = 0x06

    def __init__(self, arg):
        """
        Constructs LockUnlockDoor message bytes and constructs a Instance

        :param properties.value.lock.Lock arg: :class:`properties.value.lock.Lock`
        """
        log.debug(" ")

        log.debug("Identifiers.DOOR_LOCKS " + str(Identifiers.DOOR_LOCKS) + " Type: " + str(type(Identifiers.DOOR_LOCKS)))
        log.debug("Identifiers.DOOR_LOCKS.value " + str(Identifiers.DOOR_LOCKS.value) )

        self.msg_type = msg_type.MsgType(Identifiers.DOOR_LOCKS,0x01)

        if isinstance(arg, Lock):
            # construct case
            super().__init__(None, self.msg_type)
            # create a property
            # TODO, get timestamp and failure from arg  
            log.debug("__init__ arg: " + str(arg))
            self.doorlock = hmproperty.HmProperty(None, LockUnlockDoors.lockst_prop_id, arg, None, None)
            super().create_bytes(self.doorlock)
        elif isinstance(arg, (bytes, bytearray)):
            # NOTE: parsing case NOT needed for link device
            super().__init__(arg)
            log.info("__init__ parsing not implemented for link device")
        else:
            log.error("invalid argument type")
        return

    def getdoorlock(self):
        """
        < For internal use >
        Get Door Lock from LockUnlockDoors Instance

        :param None:
        :rtype: HmProperty
        """
        return self.doorlock


