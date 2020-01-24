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
from .. import identifiers, msg_type, property_enumeration, command_with_properties
from ..properties import hmproperty
import logging

log = logging.getLogger('hmkit.autoapi')

class IgnitionState(command_with_properties.CommandWithProperties):
    """
    Handle Ignition State
    """
    ENGINE_IGNITION_IDENTIFIER = 0x01
    ACCESSORIES_IGNITION_IDENTIFIER = 0x02

    def __init__(self, msgbytes):
        """
        Parse the IgnitionState messagebytes and construct the instance

        :param bytes msgbytes: Ignition message in bytes
        """
        # Construction of IgnitionState is only required from Car side
        # Hence only parsing is implemented.
        log.debug(" ")
        super().__init__(msgbytes)

        self.engine_ignition = None
        self.accessories_ignition = None

        props = super().getProperties()
        prop_itr = self.properties_iterator 

        while self.properties_iterator.has_next() == True:
            hmprop = self.properties_iterator.next()

            # TODO
            if hmprop.getproperty_identifier() == IgnitionState.ENGINE_IGNITION_IDENTIFIER:
                log.debug(" ENGINE_IGNITION_IDENTIFIER")
                print(" ENGINE_IGNITION_IDENTIFIER: val bytes" + str(hmprop.getcomponent_valuebytes()) )
                if hmprop.getcomponent_valuebytes() is not None:
                    self.engine_ignition = bool(int.from_bytes(hmprop.getcomponent_valuebytes(), byteorder='big', signed=False))

            elif hmprop.getproperty_identifier() == IgnitionState.ACCESSORIES_IGNITION_IDENTIFIER:
                log.debug(" ACCESSORIES_IGNITION_IDENTIFIER")
                print(" ACCESSORIES_IGNITION_IDENTIFIER: val bytes" + str(hmprop.getcomponent_valuebytes()) )
                if hmprop.getcomponent_valuebytes() is not None:
                    self.accessories_ignition = bool(int.from_bytes(hmprop.getcomponent_valuebytes(), byteorder='big', signed=False))

        return

    def get_engine_ignition(self):
        """
        Get engine ignition

        :param None:
        :rtype: bool
        """
        return self.engine_ignition

    def get_accessories_ignition(self):
        """
        Get Accessories Ignition

        :param None:
        :rtype: bool
        """
        return self.accessories_ignition
