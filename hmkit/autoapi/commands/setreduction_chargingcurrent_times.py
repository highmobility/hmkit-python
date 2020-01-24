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
from struct import *
from .. import identifiers
from .. import msg_type, property_enumeration, command_with_properties
import hmkit.autoapi
from hmkit.autoapi.identifiers import Identifiers
import hmkit.autoapi.msg_type
from ..properties import hmproperty
from ..properties.value.double_hm import DoubleHm
from ..properties.value.charging.reduction_time import ReductionTime
import logging

log = logging.getLogger('hmkit.autoapi')

class SetReductionChargingCurrentTimes(command_with_properties.CommandWithProperties):
    """
    Constructs Set Reduction Charging Current Times message
    """
    reduction_time_prop_id = 0x13

    def __init__(self, msgbytes, reductiontimes):
        """
        Construct Set Reduction Charging Current Times Timers message bytes and Construct an instance

        :param  bytearray msgbytes: only required for Parse case. pass None
        :param  list of ReductionTime: list of :class:`properties.value.charging.reduction_time.ReductionTime`
        """
        log.debug(" ")
        self.msg_type = msg_type.MsgType(Identifiers.CHARGING,0x01)
        self.set_reduc_chargecurr = []

        if msgbytes is not None:
            # message bytes parsing
            log.debug("parsing case not required for link device ")
        elif isinstance(reductiontimes, list) and isinstance(reductiontimes[0], ReductionTime):
            # construct message bytes case
            super().__init__(None, self.msg_type)
            # create a property
            # TODO, get timestamp and failure from arg  
            log.info("arg: " + str(reductiontimes))

            for reductiontime in reductiontimes:
                setreduc_chargecurr = hmproperty.HmProperty(None, SetReductionChargingCurrentTimes.reduction_time_prop_id, reductiontime, None, None)
                self.set_reduc_chargecurr.append(setreduc_chargecurr)

            super().create_bytes(self.set_reduc_chargecurr)
        else:
            log.error("invalid argument type")
        return
