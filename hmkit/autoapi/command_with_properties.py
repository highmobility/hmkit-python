#!/usr/bin/env python
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
from . import identifiers, msg_type, property_enumeration
#from .msg_type import Type
from .properties import *
from .properties import hmproperty
import logging

log = logging.getLogger('hmkit.autoapi')

class CommandWithProperties(object):

    def __init__(self, msgbytes = None, *args):

        log.debug("CommandWithProperties __init__: ")
        self.hmproperties = []
        # Version 11(0x0b)
        self.type_version = [0x0b]

        # Command parsing case, bytearray received as input
        if msgbytes is not None:
            log.debug("CommandWithProperties: __init__() Parsing ")
            self.msgbytes = msgbytes

            self.prop_enumr = property_enumeration.PropertyEnumeration(msgbytes[3:])

            #print("CommandWithProperties; msgbytes: " + str(msgbytes))

            while self.prop_enumr.has_more_elements() == True:
                enum_prop  = self.prop_enumr.next_element()
                # create hmproperty for every enumerated prop
                #print("CommandWithProperties; prop_enumr bytes: " + str(type(self.prop_enumr.bytes[enum_prop.value_start-3 : enum_prop.value_start+enum_prop.size])))

                hmprop = hmproperty.HmProperty(self.prop_enumr.bytes[enum_prop.value_start-3 : enum_prop.value_start+enum_prop.size])
                self.hmproperties.append(hmprop)

            #self.enum_prop.identifier
            #self.enum_prop.size
            #str(self.prop_enumr.bytes[enum_prop.value_start:enum_prop.value_start+enum_prop.size] )

            # TODO: find universal properties(Timestamp, Failure etc)
            self.properties_iterator = CommandWithProperties.PropertiesIterator(self)

        else: # command construction case
            log.debug("Constructing ")

            for arg in args:
                if isinstance(arg, msg_type.MsgType):
                    self.msg_type = arg
                elif isinstance(arg, hmproperty.HmProperty):
                    # individual properties
                    self.hmproperties.append(arg)
        return None

    def settype_andbytes(self, msgbytes):
        self.msg_type = msg_type.MsgType(msgbytes[0:2],msgbytes[2])
        return None

    def getProperties(self):
        return self.hmproperties

    # Note: Use only for the cases where there wont be multiple
    # same properties ID's in a command
    def getProperty(self, ID):

        for prop in self.hmproperties:
            if prop.getproperty_identifier() == ID:
                return prop

        return None

    def create_bytes(self, props):
        """

        :param HmProperty prop: HmProperty object for the property block

        :rtype: None
        """
        self.id_and_type = self.msg_type.get_identifier_and_type()
        self.prop_bytes = bytearray()

        if isinstance(props, hmproperty.HmProperty):
            # individual properties
            self.prop_bytes = props.getproperty_bytes()
        elif isinstance(props, list) and isinstance(props[0], hmproperty.HmProperty):
            #list of properties
            for prop_elem in props:
                self.prop_bytes.extend(prop_elem.getproperty_bytes())
        elif props is None:
            self.prop_bytes = None

        log.debug("id_and_type Type: " + str(type(self.id_and_type)))
        log.debug("prop_bytes: " + str(self.prop_bytes))
        if props is not None:
            self.msgbytes = bytearray(self.type_version) + self.id_and_type + self.prop_bytes
        else:
            self.msgbytes = bytearray(self.type_version) + self.id_and_type

        log.info("full bytes: " + str(self.msgbytes))
        return None

    def get_bytearray(self):
        return self.msgbytes

    # will be needed for construct properties
    class Builder(object):

        def __init__(self, cmd_prop):

            self.properties = []
            return None

        def addProperty(self):

            return

        def getProperties(self):

            return


    class PropertiesIterator(object):

        def __init__(self, cmd_props):
            self.currentIndex = 0
            self.cmd_props = cmd_props
            self.currentSize = len(cmd_props.hmproperties)
            log.debug("properties count: " + str(self.currentSize))
            return None


        def has_next(self):
            return (self.currentIndex < self.currentSize)


        def next(self):
            curr_prop = self.cmd_props.hmproperties[self.currentIndex]
            self.currentIndex += 1
            return curr_prop


        def parseNext():

            return

