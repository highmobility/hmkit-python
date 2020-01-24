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
from ..properties.value.charging.charge_timer import ChargingTimer
import logging

log = logging.getLogger('hmkit.autoapi')

class SetChargingTimers(command_with_properties.CommandWithProperties):
    """
    Constructs Set Charging Timers message
    """
    charge_timer_prop_id = 0x15

    def __init__(self, msgbytes, charge_timers):
        """
        Construct Set Charging Timers message bytes and Construct an instance

        :param  bytearray msgbytes: only required for Parse case else pass None
        :param  list of ChargingTimer:  list of :class:`properties.value.charging.charge_timer.ChargingTimer`
        """
        log.debug(" ")
        self.msg_type = msg_type.MsgType(Identifiers.CHARGING,0x01)

        if isinstance(charge_timers, list) and isinstance(charge_timers[0], ChargingTimer):
            # construct message bytes case
            super().__init__(None, self.msg_type)
            # create a property
            # TODO, get timestamp and failure from arg  
            log.info("arg: " + str(charge_timers))
            self.set_chargingtimers = []

            for charge_timer in charge_timers:
                set_chargingtimer = hmproperty.HmProperty(None, SetChargingTimers.charge_timer_prop_id, charge_timer, None, None)
                self.set_chargingtimers.append(set_chargingtimer)

            super().create_bytes(self.set_chargingtimers)

        elif msgbytes is not None:
            # message bytes parsing
            super().__init__(msgbytes)
            self.charging_timers = []

            props = super().getProperties()
            prop_itr = self.properties_iterator 
 
            while self.properties_iterator.has_next() == True:
                hmprop = self.properties_iterator.next()

                # TODO  
                if hmprop.getproperty_identifier() == charge_timer_prop_id:
                    log.debug("Charge Timer")
                    if hmprop.getcomponent_valuebytes() is not None:
                        chargetimer = charge_timer.ChargingTimer(hmprop.getcomponent_valuebytes(), None, None)
                        self.charging_timers.append(chargetimer)
        else:
            log.error("invalid argument type")
        return


    def get_chargingtimers(self):
        """
        < Internal Use >
        Get ChargingTimers of  :class:`autoapi.properties.value.charging.charge_timer.ChargingTimer`

        :param  None:
        :rtype:  list of hmproperty.HmProperty :class:`autoapi.properties.value.charging.charge_timer.ChargingTimer`
        """
        return self.set_charging_timers

