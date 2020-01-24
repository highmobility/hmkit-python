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

from .. import identifiers, msg_type, property_enumeration, command_with_properties
from ..msg_type import MsgType
from ..properties.capability import Capability

import logging

log = logging.getLogger('hmkit.autoapi')

class Capabilities(command_with_properties.CommandWithProperties):
    """
    Parses Capabilities message bytes and provides get APIs for the internal parameters
    """

    CAPABILITY_IDENTIFIER = 0x01

    def __init__(self, msgbytes):
        """
        Parses Capabilities message bytes and construct the object

        :param bytes msgbytes: Capabilities message bytes
        """
        # Construction of Capabilities is required only from Car side
        # Hence only parsing is implemented for Link device
        log.debug(" ")
        #print("Capabilities: msg bytes " + str(msgbytes) )
        super().__init__(msgbytes)

        self.capabilities_bytes = msgbytes
        self.capabilities = []

        props = super().getProperties()
        prop_itr = self.properties_iterator

        while self.properties_iterator.has_next() == True:
            hmprop = self.properties_iterator.next()

            if hmprop.getproperty_identifier() == Capabilities.CAPABILITY_IDENTIFIER:
                log.debug("Capabilities CAPABILITY_IDENTIFIER")
                #print("Capabilities: val bytes: " + str(hmprop.getcomponent_valuebytes()) )
                if hmprop.getcomponent_valuebytes() is not None:
                    capability = Capability(hmprop.getcomponent_valuebytes())
                    self.capabilities.append(capability)
                    log.debug("capability: " + str(capability))

        return

    def get_capabilities(self):
        """
        Get  Capabilities

        :param None:
        :return: list of properties.capability.Capability
        :rtype: list
        """

        return self.capabilities

    def get_capability(self, identifier):
        """
        Get the capability

        :param MsgType msgtype: msg_type.MsgType
        :rtype: hmkit.autoapi.properties.capability.Capability
        """

        for capability_obj in self.capabilities:
            if capability_obj.get_identifier() == identifier:
                #print("get_capability: matched " + " ID:" + str(identifier))
                #msgtype.get_identifier()
                #capability_obj.is_supported(msgtype)
                return capability_obj
