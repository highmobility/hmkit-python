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
import struct
from . import *
from . import propertyvalue_object
from .value.pricing_type import PricingType

log = logging.getLogger('hmkit.autoapi')

class HomeChargeTariff(propertyvalue_object.PropertyValueObject):
    """

    """

    def __init__(self, pricetype, price, currency, propbytes=None):
        """
        Property bytes will be parsed to get internal data values

        :param enum pricetype:
        :param float price:
        :param string currency:
        :rtype: None
        """

        if propbytes is not None:
            super().__init__(propbytes)
            #self.valbytes = propbytes

            self.pricetype = PricingType(propbytes[0])
            log.debug("PRICE_TARIFF Type: " + str(self.pricetype))

            # float 4 bytes
            tariffprice = struct.unpack('!f',propbytes[1:5])
            self.price = tariffprice[0]
            log.debug("HomeCharger_State Tariff Price: " + str(self.price))

            # currency str len 2 bytes
            currency_str_len = int.from_bytes(propbytes[5:7], byteorder='big', signed=False)
            log.debug("Tariff Currency Len: " + str(currency_str_len))
            # currency str
            self.currency_str = str(propbytes[7:7+currency_str_len])
            log.debug("Tariff Currency : " + self.currency_str)

        else:
            self.pricetype = pricetype
            self.price = price
            self.currency_str_len = len(currency)
            self.currency_str = currency

            self.valbytes = bytearray()
            # how many bytes it will take ??
            self.valbytes.append(self.pricetype.value) # enum
            outbytes = bytearray(struct.pack("!f", self.price)) # ! - big endian
            self.valbytes += outbytes
            str_len_bytes = self.currency_str_len.to_bytes(2, byteorder='big')
            self.valbytes += str_len_bytes
            self.valbytes += self.currency_str.encode()
            super().__init__(self.valbytes)
            log.debug("valbytes: " + str(self.valbytes))
            print("valbytes: " + str(self.valbytes))
            log.debug("HomeChargeTariff  property " + "pricetype: " + str(self.pricetype) + " ,price: " + str(self.price) + " Currency_str: " + str(self.currency_str))
            print("***** HomeChargeTariff  property " + "pricetype: " + str(self.pricetype) + " ,price: " + str(self.price) + " Currency_str: " + str(self.currency_str))

        return

    def get_price_type(self):
        """
        returns home charger tariff pricetype

        :return enum pricetype:
        :rtype: enum
        """
        return self.pricetype

    def get_price(self):
        """
        returns home charger tariff price

        :return float price:
        :rtype: float
        """
        return self.price

    def get_currency_str(self):
        """
        returns home charger tariff currency type

        :return string currency:
        :rtype: string
        """
        return self.currency_str
