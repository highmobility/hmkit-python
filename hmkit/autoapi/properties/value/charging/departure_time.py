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
from ... import propertyvalue_object

log = logging.getLogger('hmkit.autoapi')

class DepartureTime(propertyvalue_object.PropertyValueObject):
    """
    DepartureTime property which includes ActiveState(bool) and Time(hour and min) 
    """

    def __init__(self, propbytes):
        """
        Property bytes will be parsed to get internal data values

        :param bytearray propbytes: Property Component Bytes
        :rtype: None
        """

        if propbytes is not None:
            log.debug("DepartureTime property " + " bytes Len:" + str(len(propbytes)) + " bytes: " + str(propbytes))
            super().__init__(propbytes)
            self.active_state = bool(propbytes[0])
            hour = propbytes[1]
            minutes = propbytes[2]
            self.datetime_time = datetime.time(hour, minutes)
            log.debug("DepartureTime  property " + "Active_State: " + str(self.active_state) + " ,time: " + str(self.datetime_time))
        return
    # need to handle construct with a methods instead of _init_
 
    def get_active_state(self):
        """
        returns active state

        :return: active_state
        :rtype: bool
        """
        return self.active_state

    def get_time(self):
        """
        returns time hour and mins

        :return: time - hour and mins
        :rtype: datetime.time
        """
        return self.datetime_time
