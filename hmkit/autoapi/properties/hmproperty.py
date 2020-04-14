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

import sys
import codecs
import traceback
import logging
from . import *
from enum import Enum
from datetime import datetime
#from . import properties.value.lock
#from . import properties.value.position
from .component.property_component_value import PropertyComponentValue
from .component.property_component_timestamp import PropertyComponentTimestamp

log = logging.getLogger('hmkit.autoapi')

class HmProperty(bytearray):
    """
    Represents property block which can include value, timestamp and failure Components.
    components are represented by  :class:`.component.property_component_value.PropertyComponentValue`, 
    :class:`.component.property_component_timestamp.PropertyComponentTimestamp` and  :class:`.component.property_component_failure.PropertyComponentFailure`
    """

    def __init__(self, propbytes = None, id = None, value = None, timestamp = None, failure = None):
        """
        Initialize HmProperty object

        :param bytearray propbytes: message bytes of the property block
        :param integer id: Property ID
        :param value: possibly a object from .value. or any python data type
        :param timestamp: datetime.utc type
        :param failure:
        :rtype: None
        """
        # propbytes is complete property bytes from ID till the data end
        log.debug(" ")

        if propbytes is not None:
            # Parsing case
            log.debug("propbytes: " + str(propbytes))
            # input Byte array. Message parsing case
            self.prop_bytes = propbytes
            self.findcomponents()
        else:
            # Construction
            log.info("Id type: " + str(type(id)))
            log.info("Id: " + str(id) + " value: " + str(value) + " timestamp: " + str(timestamp) + " failure: " + str(failure))
            self.id = id
            self.timestamp = None
            self.data_obj = None
            self.failure = None
            self.update(id, value, timestamp, failure)
        return

    def update(self, identifier, value = None, timestamp = None, failure = None):
        """
        AutoApi construction. update the passed components fields.
        [for internal usage]
        """
        # Construction case
        if value is not None:
            self.data_obj = PropertyComponentValue(None, value)
            log.debug(" update data")

        if timestamp is not None:
            self.timestamp = PropertyComponentTimestamp(None, timestamp)
            log.debug(" update timestamp")

        if failure is not None:
            self.failure = PropertyComponentFailure(None, failure)
            log.debug(" update timestamp")

        self.create_bytes_from_components(identifier)

        return

    def create_bytes_from_components(self, identifier):
        """
        constructs property bytes from different components.
        [for internal usage]
        """
        # Construct Auto Api binary bytes
        #self.prop_bytes, self.data_obj, self.timestamp, self.failure
        self.prop_bytes = bytearray()
        #self.prop_bytes +=  bytearray(identifier)
        #self.prop_bytes +=  identifier.to_bytes(1, byteorder='big')
        self.prop_bytes.append(identifier)

        log.debug("Prop Bytes ID: " + str(self.prop_bytes))
        log.debug("ID: " + str(identifier) + " ID Type: " + str(type(identifier)))

        # Property Length
        if self.data_obj is not None:
            length =  self.data_obj.getlength()

        if self.timestamp is not None:
            length +=  self.timestamp.getlength()

        if self.failure is not None:
            length +=  self.failure.getlength()

        self.prop_bytes +=  length.to_bytes(2, byteorder='big')

        log.debug("Prop Bytes ID + Len: " + str(self.prop_bytes))

        # Include the components
        if self.data_obj is not None:
            self.prop_bytes +=  self.data_obj.getcomponent_bytes()

        if self.timestamp is not None:
            self.prop_bytes +=  self.timestamp.getcomponent_bytes()

        if self.failure is not None:
            self.prop_bytes +=  self.failure.getcomponent_bytes()

        log.debug("Prop Bytes: " + str(self.prop_bytes))
        return

    def get_propvalue_bytes(self):
        """
        returns the property value component bytes
        [for internal usage]
        """
        propertybytes = self.prop_bytes[2:]
        return propertybytes

    def get_propvalue_length(self):
        """
        returns the property value component length
        [for internal usage]
        """
        propertylen_bytes = self.prop_bytes[1:3]
        propertylen = int.from_bytes(propertylen_bytes, byteorder='big')
        return propertylen

    def getproperty_identifier(self):
        """
        returns the property Identifier
        [for internal usage]
        """
        return self.prop_bytes[0]

    def getproperty_bytes(self):
        """
        returns the property bytes (all the components)
        [for internal usage]
        """
        return self.prop_bytes

    def getcomponent_valuebytes(self):
        """
        returns the component value bytes
        [for internal usage]
        """
        return self.data_obj.getvalue_bytes()

    def getdata_component(self):
        """
        returns the component value class object for PropertyComponentValue
        [for internal usage]
        """
        '''if self.data_obj != None
            val = self.data_obj.getvalue()
        else
            val = None'''
        return self.data_obj

    def gettimestamp_component(self):
        """
        returns the component timestamp class object
        [for internal usage]
        """
        return self.timestamp

    def gettimestamp(self):
        """ retuns datetime stamp value"""
        return self.timestamp.get_datetime()

    def getfailure_component(self):
        return self.failure

    def findcomponents(self):

        count = 3
        log.debug(" ")
        self.data_obj = None
        self.timestamp = None
        self.failure = None

        while count < len(self.prop_bytes):
            compIdentifier = self.prop_bytes[count]
            compsize_bytes = self.prop_bytes[count+1 : count+3]
            compsize = int.from_bytes(compsize_bytes, byteorder='big')

            #compbytes is the complete component block bytes(start to end)
            compbytes = self.prop_bytes[count:count+3+compsize]        

            if compIdentifier == 0x01: # Data
                self.data_obj = PropertyComponentValue(compbytes)
                log.debug("data")

            elif compIdentifier == 0x02: # Timestamp
                self.timestamp = PropertyComponentTimestamp(compbytes)
                log.debug("timestamp")
 
            elif compIdentifier == 0x03: # Failure
                self.failure = PropertyComponentFailure(compbytes)
                log.debug("failure")

            count += 3 + compsize
 
        return


    def getunsigned_int(self, compbytes, size):


        return

    @staticmethod 
    def getvalue_frombytes(valuebytes, valuetype):

        value = None
        log.debug("valuetype: " + str(valuetype) + " ,valuebytes: " + str(valuebytes))
        log.debug("valuetype type: " + str(type(valuetype)))

        if valuetype is int:
            value = int.from_bytes(valuebytes, byteorder='big')
            log.debug("int: " + str(timestamp_ms))
        #elif valuetype is type(datetime):
        elif valuetype is datetime:
            timestamp_ms = int.from_bytes(valuebytes, byteorder='big', signed=False)
            #ts = struct.unpack("Q", bytes(self.timestamp_bytes))
            log.debug("timestamp: " + str(timestamp_ms))
            try:
                # param: convert the integer timestamp to secs
                value = datetimeutc = datetime.utcfromtimestamp(timestamp_ms/1000)
                #value = datetimeutc = datetime.fromtimestamp(timestamp_ms/1000)

            except (OverflowError, OSError)  as e:
                log.exception("get_datetime() Exception: ", e.data)
            else:
                log.debug("get_datetime(): " + datetimeutc.strftime('%Y-%m-%d %H:%M:%S.%f'))
                log.debug("year: " + str(datetimeutc.year))
                log.debug("month: " + str(datetimeutc.month))
                log.debug("day: " + str(datetimeutc.day))
                log.debug("hour: " + str(datetimeutc.hour))
                log.debug("min: " + str(datetimeutc.minute))
                log.debug("sec: " + str(datetimeutc.second))
                log.debug("ms: " + str(datetimeutc.microsecond/1000))
        elif valuetype is list:
            log.debug("TODO: list" )
        elif valuetype is Enum:
            log.debug("TODO: Enum" )
        elif valuetype is tuple:
            log.debug("TODO: tuple" )
        elif valuetype is str:
            value = str(valuebytes)
        elif valuetype is bool:
            value = bool(int.from_bytes(valuebytes, byteorder='big', signed=False))
        elif valuetype is float:
            value = struct.unpack('!f', valuebytes)
 
        log.info("value: " + str(value))

        return value

    # need set Apis
    # setIdentifier
    # setValueBytes
    # 
