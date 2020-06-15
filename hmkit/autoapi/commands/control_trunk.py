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
from .. import identifiers
from .. import msg_type, property_enumeration, command_with_properties
import hmkit.autoapi
from hmkit.autoapi.identifiers import Identifiers
import hmkit.autoapi.msg_type
from ..properties import hmproperty
from enum import Enum, unique
from ..properties.value.lock import Lock
from ..properties.value.position import Position
import logging

log = logging.getLogger('hmkit.autoapi')

class ControlTrunk(command_with_properties.CommandWithProperties):
    """
    Constructs Control Trunk message bytes
    """
    TRUNK_LOCK = 0x01
    TRUNK_POS = 0x02

    def __init__(self, lock, pos):
        """
        Constructs Control Trunk message bytes and constructs Instance

        :param enum lock: :Enum class:`properties.value.lock.Lock`
        :param enum pos: :Enum class:`properties.value.position.Position`
        """
        log.debug(" ")
        self.msg_type = msg_type.MsgType(Identifiers.TRUNK_ACCESS, 0x01)
        super().__init__(None, self.msg_type)
        self.propblocks = []

        if isinstance(lock, Lock) and isinstance(pos, Position):
            propblock = hmproperty.HmProperty(None, ControlTrunk.TRUNK_LOCK, lock, None, None)
            self.propblocks.append(propblock)

            propblock = hmproperty.HmProperty(None, ControlTrunk.TRUNK_POS, pos, None, None)
            self.propblocks.append(propblock)

            super().create_bytes(self.propblocks)
        else:
            log.error("invalid argument type")

        return


