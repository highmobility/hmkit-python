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
import logging
import datetime
from ... import propertyvalue_object
from ..start_stop import StartStop

log = logging.getLogger('hmkit.autoapi')

class ReductionTime(propertyvalue_object.PropertyValueObject):
    """
    ReductionTime property which includes ActiveState(bool) and Time(hour and min) 
    """

    def __init__(self, valbytes, startstop, time):
        """
        Supports both construction and parsing of ReductionTime.
        Parsing - valbytes will be parsed to get internal data values.
        Construction - pass startstop and time values. make valbytes as None

        :param bytearray valbytes: None if not parsing. Property Component date value Bytes.
        :param StartStop startstop: properties.value.start_stop.StartStop
        :param datetime.time time: datetime.time, fill hour and mins
        """

        if valbytes is not None:
            log.debug("DepartureTime property " + " bytes Len:" + str(len(valbytes)) + " bytes: " + str(valbytes))
            super().__init__(valbytes)
            self.start_stop = StartStop(valbytes[0])
            hour = valbytes[1]
            min = valbytes[2]
            self.datetime_time = datetime.time(hour, min)
            log.debug("DepartureTime  property " + "Active_State: " + str(self.start_stop) + " ,time: " + str(self.datetime_time))
        else:
            log.info("StartStop: " + str(startstop) + " datetime.time: " + str(time) )
            self.start_stop = startstop
            self.datetime_time = time

            self.valbytes = bytearray()
            self.valbytes.append(self.start_stop.value)
            self.valbytes.append(time.hour)
            self.valbytes.append(time.minute)
            #self.valbytes += PropertyComponentValue(None, None).getbytes(self.date_time, None)

            super().__init__(self.valbytes)
            log.info("valbytes: " + str(valbytes))
        return
 
    def get_start_stop(self):
        """
        returns start stop

        :return: active_state
        :rtype: properties.value.start_stop.StartStop
        """
        return self.start_stop

    def get_time(self):
        """
        returns time hour and mins

        :return: time - hour and mins
        :rtype: datetime.time
        """
        return self.datetime_time
