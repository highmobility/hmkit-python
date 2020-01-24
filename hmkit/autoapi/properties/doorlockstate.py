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

from . import *
from . import propertyvalue_object
from .value import location
from .value import lock
#from . import properties.value.position
import logging

log = logging.getLogger('hmkit.autoapi')

class DoorLockSate(propertyvalue_object.PropertyValueObject):
    """
    Doorlockstate property which includes door lock and location :class:`.value.lock.Lock` and :class:`.value.lock.Location`
    """

    def __init__(self, propbytes):
        """
        Property bytes will be parsed to get internal data values

        :param bytearray propbytes: Property Component Bytes
        :rtype: None
        """
        log.debug("DoorLockSate property " + " bytes Len:" + str(len(propbytes)) + " bytes: " + str(propbytes))
        super().__init__(propbytes)
        self.location = location.Location(propbytes[0])
        self.doorlock = lock.Lock(propbytes[1])
        log.debug("DoorLockState  property " + "location: " + str(self.location) + " ,lock: " + str(self.doorlock))
        return
    # TODO: need to handle construct with a methods instead of _init_
 
    def get_lock(self):
        """
        returns door lock from the doorlockstate

        :return: Lock
        :rtype: :class:`.value.lock.Lock`
        """
        return self.doorlock

    def get_location(self):
        """
        returns door location from the doorlockstate

        :return: Location
        :rtype: :class:`.value.lock.Location`
        """
        return self.location
