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
from ... import hmproperty
from enum import Enum, unique
from ... component.property_component_value import PropertyComponentValue
from ... import propertyvalue_object
import logging


log = logging.getLogger('hmkit.autoapi')

class ChargingTimer(propertyvalue_object.PropertyValueObject):
    """
    Charging Timer Value Object(datetime and TimerType) and get api's are provided
    """
    def __init__(self, valbytes, timertype, date_time):
        """
        :param bytearray valbytes: Required only for parsing case otherwise pass None. bytes to parse and get TimerType and date_time
        :param autoapi.properties.value.charging.charge_timer.TimerType timertype:
        :param datetime.datetime datetime:
        :rtype: None
        """

        if valbytes is not None:
            log.info("valbytes")
            super().__init__(valbytes)
            self.valbytes = valbytes
            self.timertype = TimerType(valbytes[0])
            self.date_time = hmproperty.HmProperty.getvalue_frombytes(valbytes[1:], datetime.datetime)
        else:
            log.info("timertype: " + str(timertype) + " datetime: " + str(date_time) )
            self.timertype = timertype
            self.date_time = date_time

            self.valbytes = bytearray()
            self.valbytes.append(int(self.timertype.value))
            self.valbytes += PropertyComponentValue(None, None).getbytes(self.date_time, None)
            super().__init__(self.valbytes)
            log.info("valbytes: " + str(valbytes))
        return

    def get_timertype(self):
        """
        Get the TimerType value of type Enum class:`..properties.value.charge_timer.TimerType`

        :param  None:
        :rtype: None
        """
        return self.timertype

    def get_datetime(self):
        """
        Get the datetime value of type datetime.datetime 

        :param  None:
        :rtype: None
        """
        return self.date_time


@unique
class TimerType(Enum):
    """
    Enum Class for Timer Type values
    """
    PREFERRED_START_TIME = 0x00
    PREFERRED_END_TIME = 0x01
    DEPARTURE_TIME = 0x02

    #TODO: fromByte() which should return ENUM to be stores in Property
