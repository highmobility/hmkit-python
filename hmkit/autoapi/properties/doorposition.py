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
from . import hmproperty
from .propertyvalue_object import PropertyValueObject
from .value.location import Location
from .value.lock import Lock
from .value.position import Position
import logging

log = logging.getLogger('hmkit.autoapi')

class DoorPosition(PropertyValueObject):
    """
    Represents DoorPosition property which includes door position and location :class:`.value.position.Position` and :class:`.value.location.Location`
    """

    def __init__(self, propbytes):
        """
        Property bytes will be parsed to get internal data values

        :param bytearray propbytes: Property Component Bytes
        :rtype: None
        """
        log.debug("property " + " bytes Len:" + str(len(propbytes)) + " bytes: " + str(propbytes))
        super().__init__(propbytes)
        # parse the values in terms of value enums
        self.location = Location(propbytes[0])
        self.position = Position(propbytes[1])
        log.debug("property " + "location: " + str(self.location) + " ,position: " + str(self.position))
        return

    def get_position(self):
        """
        returns door position from the doorposition

        :return: Position
        :rtype: :class:`.value.position.Position`
        """
        return self.position

    def get_location(self):
        """
        returns door Location for the doorposition

        :return: Location
        :rtype: :class:`.value.location.Location`
        """
        return self.location


