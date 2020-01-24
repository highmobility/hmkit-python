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

from . import *
from .bit_location import BitLocation

import logging

log = logging.getLogger('hmkit.autoapi')

class Permissions(object):

    def __init__(self, permission_bytes):
        """
        Permissions object that holds the permission bytearray

        :param bytearray permission_bytes:
        """
        log.debug(" ")
        self.permission_bytes = permission_bytes
        return

    @staticmethod
    def get_bit(byte_value, bit_location):
        """
        Utility function gets a specific bit value from a byte

        :param int byte_value:
        :param int bit_location:
        :rtype: int
        """
        return (byte_value >> bit_location) & 1

    def is_allowed(self, bitlocation):
        """
        returns whether the permission pointed by the bitlocation is allowed or not

        :param bit_location.BitLocation bitlocation:
        :rtype: bool
        """

        permissionbyte = self.permission_bytes[bitlocation.get_byte_location()]
        self.permission_bit = Permissions.get_bit(permissionbyte, bitlocation.get_bit_location())
        if self.permission_bit is 0:
            return False
        else:
            return True
