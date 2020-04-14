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
from ..properties.value import FatigueLevel
import logging

log = logging.getLogger('hmkit.autoapi')

class DriverFatigueState(command_with_properties.CommandWithProperties):
    """
    Handle Driver Fatigue States
    """

    ### TODO  ### : not tested yet
    DETECTED_FATIGUE_LEVEL = 0x01

    def __init__(self, msgbytes):
        """
        Parse the Detected fatique level messagebytes and construct the instance

        :param bytes msgbytes: Driver Fatigue State in bytes
        """

        # Construction of DriverFatigueState is only required from Car side
        # Hence only parsing is implemented for Link.
        log.debug(" ")
        super().__init__(msgbytes)

        self.fatigue_level = None
 
        while self.properties_iterator.has_next() == True:
            hmprop = self.properties_iterator.next()
 
            if hmprop.getproperty_identifier() == DriverFatigueState.DETECTED_FATIGUE_LEVEL:
                log.debug(" DETECTED_FATIGUE_LEVEL")
                if hmprop.getcomponent_valuebytes() is not None:
                    fatiguelevel_bytes = int.from_bytes(hmprop.getcomponent_valuebytes(), byteorder='big', signed=False)
                    self.fatigue_level = FatigueLevel(fatiguelevel_bytes)
                    log.debug(" DETECTED_FATIGUE_LEVEL: " + str(self.fatigue_level))

        return

    def getfatigue_level(self):
        """
        Get Driver Fatigue Level

        :rtype: enum: `properties.value.fatigue_level.FatigueLevel`
        """

        return self.fatigue_level
