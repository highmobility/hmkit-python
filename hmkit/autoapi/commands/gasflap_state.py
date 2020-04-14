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
from .. import identifiers, msg_type, property_enumeration, command_with_properties
from ..properties.value.lock import Lock
from ..properties.value.position import Position
import logging

log = logging.getLogger('hmkit.autoapi')

class GasFlapState(command_with_properties.CommandWithProperties):
    """
    Handle Gas Flap States
    """
    # Gas Flap Position - Open, Close
    # Gas Flap Lock - Lock, Unlock

    GAS_FLAP_LOCK = 0x02
    GAS_FLAP_POS = 0x03

    def __init__(self, msgbytes):
        """
        Parse the Gas Flap State messagebytes and construct the instance

        :param bytes msgbytes: Gas Flap State in bytes
        """

        # Construction of GasFlapState is only required from Car side
        # Hence only parsing is implemented for Link.
        log.debug(" ")
        super().__init__(msgbytes)

        self.flap_lock = None
        self.flap_pos = None

        props = super().getProperties()
        prop_itr = self.properties_iterator 
 
        while self.properties_iterator.has_next() == True:
            hmprop = self.properties_iterator.next()
 
            if hmprop.getproperty_identifier() == GasFlapState.GAS_FLAP_LOCK:
                log.debug(" GAS_FLAP_LOCK")
                lock_bytes = hmprop.getcomponent_valuebytes()
                if lock_bytes is not None:
                    self.flap_lock = Lock(int(lock_bytes[0]))
                    log.debug(" GAS_FLAP_LOCK: " + str(self.flap_lock))

            elif hmprop.getproperty_identifier() == GasFlapState.GAS_FLAP_POS:
                log.debug(" GAS_FLAP_POS ")
                pos_bytes = hmprop.getcomponent_valuebytes()
                if pos_bytes is not None:
                    self.flap_pos = Position(int(pos_bytes[0]))
                    log.debug(" GAS_FLAP_POS: " + str(self.flap_pos))

        return

    def getlock(self):
        """
        Get Gas Flap lock

        :rtype: `properties.value.lock.Lock`
        """

        return self.flap_lock

    def getposition(self):
        """
        Get Gas Flap position

        :rtype: `properties.value.position.Position` 
        """

        return self.flap_pos

    def islocked(self):
        """
        is all Gas Flap Locked

        :param None:
        :rtype: True/False
        """
        if self.flap_lock == Lock.UNLOCKED:
            return False

        return True