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
from hmkit.autoapi.identifiers import Identifiers
import hmkit.autoapi.msg_type
from ..properties import hmproperty
from enum import Enum, unique
from ..properties import DataMeasurementUnit
from ..properties.value import MeasurementType
from ..properties.value.unit_type import FrequencyUnit
from ..properties.values_with_unit import HeartRate
import logging

log = logging.getLogger('hmkit.autoapi')

class SendHeartRate(command_with_properties.CommandWithProperties):
    """
    Constructs Send Heart Rate message bytes
    """
    HEART_RATE = 0x01

    def __init__(self, heartrate):
        """
        Constructs Send Heart Rate message bytes and constructs Instance

        :param heartrate: Enum HeartRate:`properties.values_with_unit.HeartRate`
        """
        log.debug(" ")
        self.msg_type = msg_type.MsgType(Identifiers.HEART_RATE, 0x01)
        super().__init__(None, self.msg_type)

        if isinstance(heartrate, HeartRate):
            data_unit = DataMeasurementUnit(measurement_type=MeasurementType.FREQUENCY, unit_type=heartrate.get_unit(), data_value=heartrate.get_heartrate())
            self.prop_heartrate = hmproperty.HmProperty(None, SendHeartRate.HEART_RATE, data_unit, None, None)

            super().create_bytes(self.prop_heartrate)
        else:
            log.error("invalid argument type")

        return
