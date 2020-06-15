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

class TrunkState(command_with_properties.CommandWithProperties):
    """
    Handle Trunk State
    """
    # Trunk Position - Open, Close
    # Trunk Lock  - Lock, Unlock

    LOCK_IDENTIFIER = 0x01
    POSITION_IDENTIFIER = 0x02

    def __init__(self, msgbytes):
        """
        Parse the Trunk State messagebytes and construct the instance

        :param bytes msgbytes: Trunk State message in bytes
        """

        # Construction of TrunkState is only required from Car side
        # Hence only parsing is implemented.
        log.debug(" ")
        super().__init__(msgbytes)

        self.lock_state = None
        self.position = None

        props = super().getProperties()

        while self.properties_iterator.has_next() == True:
            hmprop = self.properties_iterator.next()

            if hmprop.getproperty_identifier() == TrunkState.LOCK_IDENTIFIER:
                log.debug(" LOCKS_STATE_IDENTIFIER")
                lock_bytes = hmprop.getcomponent_valuebytes()
                if lock_bytes is not None:
                    self.lock_state = Lock(int(lock_bytes[0]))
                    log.debug(" TRUNK LOCKS_STATE: " + str(self.lock_state))
                    print(" TRUNK LOCKS_STATE: " + str(self.lock_state))

            elif hmprop.getproperty_identifier() == TrunkState.POSITION_IDENTIFIER:
                log.debug(" POSITION_IDENTIFIER ")
                pos_bytes = hmprop.getcomponent_valuebytes()
                if pos_bytes is not None:
                    self.position = Position(int(pos_bytes[0]))
                    log.debug(" TRUNK POS: " + str(self.position))
                    print(" TRUNK POS: " + str(self.position))

        return


    def get_lock(self):
        """
        Get lock state

        :param None:
        :rtype: `properties.value.lock.Lock`
        """
        return self.lock_state


    def get_position(self):
        """
        Get Trunk position

        :param None:
        :rtype: `properties.value.position.Position`
        """
        return self.position


