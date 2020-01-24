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

from hmkit.autoapi.command_resolver import CommandResolver
from hmkit.autoapi.commands import *

from hmkit.autoapi.commands import get_parkingbrake_state
from hmkit.autoapi.commands import parkingbrake_state
from hmkit.autoapi.commands import set_parkingbrake_state

class TestGetParkingBrakeState(unittest.TestCase):

    def setUp(self):
       print("TestGetParkingBrakeState: setUp")

    def test_bytesconstruction(self):
        getparking_brakestate = bytearray([0x00, 0x58, 0x00])
        constructed_bytes = get_parkingbrake_state.GetParkingBrakeState().get_bytearray()
        self.assertEqual(constructed_bytes, getparking_brakestate, 'GetParkingBrakeState wrong bytes')


class TestParkingBrakeState(unittest.TestCase):

    def setUp(self):
       print("TestParkingBrakeState: setUp")

    def test_bytesparsing(self):

        # All locked, position closed
        ACTIVE_STATE = b'00580101000f010001010200080000016b63efa908'
        ACTIVE_STATE_decoded = ACTIVE_STATE.decode()
        active_state_hx = bytearray.fromhex(ACTIVE_STATE_decoded)

        # All unlocked, position closed
        INACTIVE_STATE = b'00580101000f010001000200080000016b8d475ba0'
        INACTIVE_STATE_decoded = INACTIVE_STATE.decode()
        inactive_state_hx = bytearray.fromhex(INACTIVE_STATE_decoded)

        cmd_obj = CommandResolver.resolve(active_state_hx)
        print("\n App: command_incoming, cmd_obj: ", str(cmd_obj))
        with self.subTest(i=1):
            #print(" isinstance of LockState: " + str(isinstance(cmd_obj, lockstate.LockState)))
            self.assertIsInstance(cmd_obj, parkingbrake_state.ParkingBrakeState, 'ParkingBrake: Active wrong parsing')

        cmd_obj = CommandResolver.resolve(inactive_state_hx)
        print("\n test_bytesparsing: cmd_obj: ", str(cmd_obj))
        with self.subTest(i=2):
            #print("\n test_bytesparsing: " + str(isinstance(cmd_obj, lockstate.LockState)))
            self.assertIsInstance(cmd_obj, parkingbrake_state.ParkingBrakeState, 'ParkingBrake: inActive wrong parsing')


class TestSetParkingBrakeState(unittest.TestCase):

    def setUp(self):
       print("TestSetParkingBrakeState: setUp")

    def test_bytesconstruction(self):
        # Active
        setparking_active_brakestate = bytearray([0x0,  0x58,  0x12,  0x01,  0x00,  0x04,  0x01,  0x00,  0x01,  0x01])
        constructed_bytes = set_parkingbrake_state.SetParkingBrakeState(True).get_bytearray()
        with self.subTest(i=1):
            self.assertEqual(constructed_bytes, setparking_active_brakestate, 'SetParkingBrakeState Active wrong bytes')

        # InActive
        setparking_inactive_brakestate = bytearray([0x0,  0x58,  0x12,  0x01,  0x00,  0x04,  0x01,  0x00,  0x01,  0x00])
        constructed_bytes = set_parkingbrake_state.SetParkingBrakeState(False).get_bytearray()
        with self.subTest(i=2):
            self.assertEqual(constructed_bytes, setparking_inactive_brakestate, 'SetParkingBrakeState inActive wrong bytes')

