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
import logging

log = logging.getLogger('hmkit.autoapi')

@unique
class FailureReason(Enum):
    """
    Enum Class for Failure Reason
    """
    UNSUPPORTED_CAPABILITY = 0x00
    UNAUTHORISED = 0x01
    INCORRECT_STATE = 0x02
    EXECUTION_TIMEOUT = 0x03
    VEHICLE_ASLEEP = 0x04
    INVALID_COMMAND = 0x05
    PENDING = 0x06
    RATE_LIMIT = 0x07

'''
    def __init__(self, value):
        print("PY: Init value Lock")
        self.valuebyte = value
        return

    def getByte(self):
        return self.valuebyte
'''

    #TODO: fromByte() which should return ENUM to be stores in Property
