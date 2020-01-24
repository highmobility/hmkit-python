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

log = logging.getLogger('hmkit.autoapi')

class PropertyEnumeration(object):

    def __init__(self, msg_bytes):
        #log.debug(" ")
        self.cursor = 0
        self.bytes = msg_bytes

    def has_more_elements(self):
        #log.debug(" ")
        if self.cursor + 3 <= len(self.bytes):
            return True
        else:
            return False

    def next_element(self):
        #log.debug(" ")
        propertyIdentifier = self.bytes[self.cursor]
        propertyStart = self.cursor + 3
        propertySize_bytes = self.bytes[self.cursor+1 : self.cursor+3]
        propertySize = int.from_bytes(propertySize_bytes, byteorder='big')
        self.cursor += 3 + propertySize
        #log.debug("next_element: Prop ID: "+ str(propertyIdentifier) + " Prop size: " + str(propertySize))
        return self.EnumeratedProperty(propertyIdentifier, propertySize, propertyStart)

    def dump_property(self, enumeratedproperty): 
        log.info(" Property: " + " ID: " + str(enumeratedproperty.identifier) + " , Size: " + str(enumeratedproperty.size) + ", Data: " + str(self.bytes[enumeratedproperty.value_start:enumeratedproperty.value_start+enumeratedproperty.size] ))

    class EnumeratedProperty():

        def __init__(self, identifier, size, valuestart):
            self.identifier = identifier
            self.size = size
            self.value_start = valuestart

