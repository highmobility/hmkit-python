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
from . import *
#from . import commands
#from autoapi.commands import *
#from autoapi.commands.properties import *
from .identifiers import Identifiers
import logging

log = logging.getLogger('hmkit.autoapi')

class MsgType():

    def __init__(self, identifier, msgtype):
        """
        :param bytes identifier: Msg identifier bytes
        :param int msgtype: message type integer value
        :rtype: None
        """
        #self.identifier_bytes = bytearray(codecs.encode(identifier.value, 'hex')) #codecs.encode(msg_id, 'hex')
        #print("MsgType __init__, identifier:  " + str(identifier.value) + "identifier typ: " + str(type(identifier.value))) 
        log.info("identifier:  " + str(identifier) + " identifier typ: " + str(type(identifier))) 
        log.info("identifier.value:  " + str(identifier.value) + " identifier typ: " + str(type(identifier.value))) 
        identifier_str = identifier.value.decode() # get the string equivalent of hex bytes
        #log.info("identifier_str:  " + str(identifier_str) + " Len: " + str(len(identifier_str)) + " type: " + str(type(identifier_str)))
        self.identifier_bytes = bytearray.fromhex(identifier_str)
        #self.identifier_bytes =  bytearray()
        #self.identifierbytes[0]
        #self.identifier_bytes += self.identifierbytes[1]

        self.type = msgtype

        #print("MsgType __init__ identifier_bytes :  " + str(self.identifier_bytes) +  " Len: " + str(len(self.identifier_bytes)) + " typ: " + str(type(self.identifier_bytes)))
        log.debug("identifier_bytes [0]:  " + str(self.identifier_bytes[0]) + " ,[1]:  " + str(self.identifier_bytes[1]))
        log.debug("identifier_bytes [0] type:  " + str(type(self.identifier_bytes[0])) )
        log.debug("identifier_bytes type:  " + str(type(self.identifier_bytes)) )

        #log.info("self.type:  " + str(self.type) + " type: " + str(type(self.type)))
        self.identifier_and_type =  self.identifier_bytes
        self.identifier_and_type.append(msgtype)
        log.debug("ID and Type: " + str(self.identifier_and_type) + " typ: " + str(type(self.identifier_and_type)))

    def get_identifier_and_type(self):
        """

        :rtype: None
        """

        return self.identifier_and_type


    def get_identifier_bytes(self):
        """
        get the identifier bytes

        :rtype: bytes
        """

        return self.identifier_bytes

    def get_identifier(self):
        """
        get the identifier object

        :rtype: identifiers.Identifiers
        """

        return  Identifiers(self.identifier_bytes)

    def get_type(self):
        """
        get the message type byte 

        :rtype: int
        """

        return self.type
