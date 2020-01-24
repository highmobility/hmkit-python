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

import logging
from .bit_location import BitLocation

log = logging.getLogger('hmkit.autoapi')

class Permission(object):
    """
    Permission object(per permission) extracted from Access certificate

    """

    def __init__(self, bitlocation, allowed):
        """
        Permission object that holds the bit location and allowed status

        :param bit_location.BitLocation bitlocation:
        :param bool allowed:
        """
        self.bitlocation = bitlocation
        self.allowed = allowed
        return

    def get_bit_location(self):
        """
        Get the bit location

        :param None:
        :rtype: bit_location.BitLocation
        """
        return self.bitlocation

    def is_allowed(self):
        """
        Return whether the permission is allowed

        :param None:
        :rtype: bool
        """
        return self.allowed
