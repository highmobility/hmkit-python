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
from struct import *
from .. import identifiers
from .. import msg_type, property_enumeration, command_with_properties
import hmkit.autoapi
from hmkit.autoapi.identifiers import Identifiers
import hmkit.autoapi.msg_type
from ..properties import hmproperty
from ..properties.value.double_hm import DoubleHm
from ..properties.value.pricing_type import PricingType
from ..properties.homecharge_tariff import HomeChargeTariff
import logging

log = logging.getLogger('hmkit.autoapi')

class SetHomeChargerPriceTariff(command_with_properties.CommandWithProperties):
    """
    Constructs Set Home Charger Price Tariff message bytes
    """
    PRICE_TARIFF_PROP_ID = 0x12

    def __init__(self, msgbytes, pricetariffs):
        """
        Constructs Set HomeCharger Price Tariff message bytes and construct instance.

        :param HomeChargeTariff pricetariff:
        """
        log.debug(" ")
        self.msg_type = msg_type.MsgType(Identifiers.HOME_CHARGER,0x01)

        if msgbytes is None: # Construction

            # construct case
            super().__init__(None, self.msg_type)

            self.propblocks = []

            if isinstance(pricetariffs, list) and isinstance(pricetariffs[0], HomeChargeTariff):

                for pricetariff in pricetariffs:
                    prop_pricetariff = hmproperty.HmProperty(None, SetHomeChargerPriceTariff.PRICE_TARIFF_PROP_ID, pricetariff.get_valuebytes(), None, None)
                    self.propblocks.append(prop_pricetariff)

            elif isinstance(pricetariffs, HomeChargeTariff):
                prop_pricetariff = hmproperty.HmProperty(None, SetHomeChargerPriceTariff.PRICE_TARIFF_PROP_ID, pricetariffs.get_valuebytes(), None, None)
                self.propblocks.append(prop_pricetariff)

            super().create_bytes(self.propblocks)

        else:
            log.error("invalid argument type")
        return
