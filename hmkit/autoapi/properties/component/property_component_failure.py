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

from enum import Enum, unique
from .property_component import PropertyComponent
import logging

log = logging.getLogger('hmkit.autoapi')

class PropertyComponentFailure(PropertyComponent):
    """
    For internal usage of SDK
    """
    def __init__(self, compbytes  = bytearray(), fail_reason = None, fail_description = None):

        if compbytes is not None:
            log.debug("Parsing ")
            super().__init__(compbytes)
            component_payload = super().getpayload_bytes()
            self.reason = FailureReason(component_payload[0])
            descriptionsize = component_payload[1]
            #descriptionsize = int.from_bytes(descriptionsize_bytes, byteorder='big')
            self.description = str(component_payload[2 : 2+ descriptionsize])
            #print("PropertyComponentFailure reason: " + str(self.reason) + " Descrp: " + str(self.description))
        else:
            log.debug("Construction ")
            self.reason = fail_reason
            self.description = fail_description
        return

    def getvalue_bytes(self):
        return super().getpayload_bytes()

    def getfailure_description(self):
        return self.description

    def getfailure_reason(self):
        return self.reason


@unique
class FailureReason(Enum):

    RATE_LIMIT = 0x00  # Property rate limit has been exceeded
    EXECUTION_TIMEOUT = 0x01    # Failed to retrieve property in time
    FORMAT_ERROR = 0x02 # Could not interpret property 
    UNAUTHORISED = 0x03 # Insufficient permissions to get the property
    UNKNOWN = 0x04 # Property failed for unknown reason
    PENDING = 0x05 # Property is being refreshed
