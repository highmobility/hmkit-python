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

import unittest
from datetime import datetime
from hmkit.autoapi.commands import get_charge_state
from hmkit.autoapi.commands import charge_state
from hmkit.autoapi.commands import start_stop_charging
from hmkit.autoapi.commands import set_charge_limit
from hmkit.autoapi.commands import open_close_charge_port
from hmkit.autoapi.commands import set_charge_mode
from hmkit.autoapi.commands import set_charging_timers
#from hmkit.autoapi.commands import setreduction_chargingcurrent_times
from hmkit.autoapi.properties.value.charging.charge_mode import ChargeMode
from hmkit.autoapi.properties.value.charging.charge_timer import ChargingTimer, TimerType


class TestGetChargeState(unittest.TestCase):

    def setUp(self):
       print("TestGetChargeState: setUp")

    def test_bytesconstruction(self):
        getcharge_state = bytearray([0x00, 0x23, 0x00])
        constructed_bytes = get_charge_state.GetChargeState().get_bytearray()
        self.assertEqual(constructed_bytes, getcharge_state, 'GetChargeState construct wrong bytes')


class TestStartStopCharging(unittest.TestCase):

    def setUp(self):
       print("TestStartStopCharging: setUp")

    def test_bytesconstruction(self):
        stop_charging = bytearray([0x0,  0x23,  0x12,  0x1,  0x0,  0x4,  0x1,  0x0,  0x1,  0x0])
        constructed_bytes = start_stop_charging.StartStopCharging(False).get_bytearray()
        with self.subTest(i=1):
            self.assertEqual(constructed_bytes, stop_charging, 'StartStopCharging: stop charging wrong bytes')

        start_charging = bytearray([0x0,  0x23,  0x12,  0x1,  0x0,  0x4,  0x1,  0x0,  0x1,  0x1])
        constructed_bytes = start_stop_charging.StartStopCharging(True).get_bytearray()
        with self.subTest(i=2):
            self.assertEqual(constructed_bytes, start_charging, 'StartStopCharging: start charging wrong bytes')


class TestSetChargeLimit(unittest.TestCase):

    def setUp(self):
       print("TestSetChargeLimit: setUp")

    def test_bytesconstruction(self):
        chargelimit = bytearray([0x0,  0x23,  0x13,  0x1,  0x0,  0xb,  0x1,  0x0,  0x8,  0x3f,  0xe3,  0x33,  0x33,  0x33,  0x33,  0x33,  0x33])
        constructed_bytes = set_charge_limit.SetChargeLimit(0.6).get_bytearray()
        with self.subTest(i=1):
            self.assertEqual(constructed_bytes, chargelimit, 'SetChargeLimit: Charge Limit wrong bytes')


class TestSetChargeMode(unittest.TestCase):

    def setUp(self):
       print("TestSetChargeMode: setUp")

    def test_bytesconstruction(self):
        chargemode = bytearray([0x0,  0x23,  0x15,  0x1,  0x0,  0x4,  0x1,  0x0,  0x1,  0x2])
        constructed_bytes = set_charge_mode.SetChargeMode(ChargeMode.INDUCTIVE).get_bytearray()
        with self.subTest(i=1):
            self.assertEqual(constructed_bytes, chargemode, 'SetChargeMode: Inductive wrong bytes')


class TestSetChargingTimers(unittest.TestCase):

    def setUp(self):
       print("TestSetChargingTimers: setUp")

    def test_bytesconstruction(self):
        chargetimer = bytearray([0x0,  0x23,  0x16,  0xd,  0x0,  0xc,  0x1,  0x0,  0x9,  0x1,  0x0,  0x0,  0x1,  0x6b,  0x5c,  0x9d,  0x48,  0x60])

        datetime_str = '06/15/19 19:29:00'
        enddatetime = datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')
        endchargingtimer = ChargingTimer(None, TimerType.PREFERRED_END_TIME,  enddatetime)

        constructed_bytes = set_charging_timers.SetChargingTimers(None, endchargingtimer).get_bytearray()
 
        with self.subTest(i=1):
            self.assertEqual(constructed_bytes, chargetimer, 'Setchargetimer:  wrong bytes')
