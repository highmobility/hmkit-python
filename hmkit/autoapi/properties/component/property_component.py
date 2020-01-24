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

class PropertyComponent(bytearray):
    """
    For internal usage of SDK
    """
    def __init__(self, compbytes = bytearray(), id = None, valbytes = None):

        if compbytes is not None:
            log.debug(" Parsing ")
            self.identifier = compbytes[0]
            # component payload part(data, timestamp, failure)
            self.valuebytes = compbytes[3:]
            # whole component block bytes
            self.compbytes = compbytes
        else:
            log.info(" Constructing. valuebytes: " + str(valbytes) + " id: " + str(id))
            self.valuebytes = valbytes
            self.identifier = id
            self.bytes = bytearray()
            self.bytes.append(id)
            log.debug(" bytes with id: " + str(self.bytes))
            #self.bytes.append(len(self.valuebytes))
            length = len(self.valuebytes)
            self.bytes += length.to_bytes(2, byteorder='big')
            log.debug(" bytes with len: " + str(self.bytes))
            self.bytes += self.valuebytes
            log.debug(" Bytes constrt: " + str(self.bytes))
            log.debug(" len field: " + str(len(self.valuebytes)) + " total length: " + str(len(self.bytes)) )
        return

    def getpayload_bytes(self):
        """
        # get the component payload part(value)
        """
        return self.valuebytes

    def getcomponent_bytes(self):
        """
        # get the component bytes(full)
        """
        return self.bytes

    def get_identifier(self):
        """
        # get the component ID
        """
        return self.identifier

    def getlength(self):
        """
        # get the component whole bytes length
        """
        return len(self.bytes)

    # TODO: construction code
