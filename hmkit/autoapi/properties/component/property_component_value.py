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
from .property_component import PropertyComponent
from enum import Enum, unique
from datetime import datetime, tzinfo, timezone
import struct
import codecs
from ..value.double_hm import DoubleHm
from .. import propertyvalue_object
from .. import DataUnit
import logging

log = logging.getLogger('hmkit.autoapi')

class PropertyComponentValue(PropertyComponent):
    """
    For internal usage of SDK

    """
    IDENTIFIER = 0x01

    def __init__(self, compbytes = bytearray(), value = None):

        if compbytes is not None:
            log.debug("Parsing ")
            super().__init__(compbytes)
        elif value is not None:
            log.debug("Constructing ")
            log.info("value: " + str(value) + " value type: " + str(type(value)))
            self.value = value
            super().__init__(None, PropertyComponentValue.IDENTIFIER, self.getbytes(value))
        return

    def getvalue_bytes(self):
        return super().getpayload_bytes()

    def getvalue(self):
        return self.value # what value ??

    def setvalue_obj(self, value_obj):
        return

    def getbytes(self, value, opt_valtype = None):

        log.info(" type: " + str(type(value)))
        #print("getbytes value: " + str(value) + " type:" + str(type(value)))

        if isinstance(value, bool):
            log.debug("bool instance(), int value : " + str(int(value)))
            outbytes = bytearray()
            outbytes.append(int(value))
        elif isinstance(value, int):
            log.debug("int instance()")
            outbytes = bytearray()
            outbytes.append(int(value))
        elif isinstance(value, list):
            log.debug("list instance()")
            outbytes = bytearray(value)
        elif isinstance(value, Enum):
            log.debug("Type  match Enum  value: " + str(value) + " value type: " + str(type(value)))
#            outbytes = value.getbyte(value)
            outbytes = bytearray()
            if isinstance(value.value, int):
                outbytes.append(value.value)
            elif isinstance(value.value, bytearray):
                outbytes += value.value
            else:
                log.debug("NOT IMPLEMENTED, Type: " + str(type(value.value)) )

            log.debug("value.value: " + str(value.value) )
            log.debug("outbytes: " + str(outbytes) )
        elif isinstance(value, tuple):
            log.debug("tuple instance()")
            outbytes = bytearray(value)
        elif isinstance(value, bytes): # TODO and Test
            log.debug("bytes instance()")
            print("bytes instance()")
            #b_string = codecs.encode(value, 'hex')
            outbytes = bytearray(value)
        elif isinstance(value, bytearray): # TODO and Test
            log.debug("bytearray instance()")
            print("bytearray instance()")
            #b_string = codecs.encode(value, 'hex')
            outbytes = value
        elif isinstance(value, str):
            log.debug("str instance()")
            outbytes = bytearray(value, 'utf-8')
        elif isinstance(value, float):
            log.debug("float instance()")
            outbytes = bytearray(struct.pack("!f", value)) # ! - big endian
        elif isinstance(value, DoubleHm): # Double
            log.debug("Double instance()")
            outbytes = bytearray(struct.pack("!d", value.getvalue())) # ! - big endian
            log.debug("Double bytes : " + str(outbytes))
        elif isinstance(value, datetime):
            log.debug("datetime instance()")
            # Timestamp local
            #timestamp = datetime.timestamp(value)
            # utc timestamp
            #timestamp = datetime.timestamp(value)
            timestamp = value.replace(tzinfo=timezone.utc).timestamp() * 1000
            log.debug("timestamp: " + str(timestamp) + " type: " + str(type(timestamp)))
            timestamp_int = int(timestamp)
            log.debug("timestamp int: " + str(timestamp_int) + " type: " + str(type(timestamp_int))) 
            outbytes = timestamp_int.to_bytes(8, byteorder='big')
            log.debug("timestamp bytes: " + str(outbytes) )
        elif isinstance(value, DataUnit):
            # value with measurement and unit codes
            log.debug("DataUnit bytes: " + str(outbytes) )
            outbytes = value.get_bytes()
        elif isinstance(value, propertyvalue_object.PropertyValueObject):
            log.debug("PropertyValueObject instance()")
            outbytes = value.get_valuebytes()

        log.info(" outbytes: " + str(outbytes))
        return outbytes
