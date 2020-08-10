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
from ..properties import DataMeasurementUnit
from ..properties.value import MeasurementType, CurrentType
from ..properties.value.unit_type import ElectricCurrentUnit
from enum import Enum, unique
import logging

log = logging.getLogger('hmkit.autoapi')

class SetHomeChargeCurrent(command_with_properties.CommandWithProperties):
    """
    Constructs HomeCharge SetCharge Current message bytes
    """
    CHARGE_CURRENT = 0x0e
    CURRENT_TYPE = 0x1b # TODO: update the fixed value

    def __init__(self, current, current_unit, current_type):
        """
        Constructs HomeCharge SetCharge Current message bytes and constructs Instance

        :param double current:
        :param float current_unit: Enum class:`properties.value.unit_type.ElectricCurrentUnit`
        :param enum current_type: Enum class:`properties.value.current_type.CurrentType`
        """
        log.debug(" ")
        self.msg_type = msg_type.MsgType(Identifiers.HOME_CHARGER, 0x01)
        super().__init__(None, self.msg_type)

        self.propcurr = None
        self.propcurrtype = None

        properties = []
        if current is not None and isinstance(current_unit, ElectricCurrentUnit):
            data_unit = DataMeasurementUnit(measurement_type=MeasurementType.ELECTRIC_CURRENT, unit_type=current_unit, data_value=current)
            self.propcurr = hmproperty.HmProperty(None, SetHomeChargeCurrent.CHARGE_CURRENT, data_unit, None, None)
            properties.append(self.propcurr)
        else:
            log.error("invalid argument type")

        if isinstance(current_type, CurrentType):
            self.propcurrtype = hmproperty.HmProperty(None, SetHomeChargeCurrent.CURRENT_TYPE, current_type, None, None)
            properties.append(self.propcurrtype)
        else:
            log.error("invalid argument type")

        super().create_bytes(properties)
        return
