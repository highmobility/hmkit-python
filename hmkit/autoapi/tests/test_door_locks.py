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
from hmkit.autoapi.commands.lockunlockdoors import LockUnlockDoors
from hmkit.autoapi.properties.value.lock import Lock

from hmkit.autoapi.commands import getlockstate
from hmkit.autoapi.commands import lockstate
from hmkit.autoapi.commands import lockunlockdoors

#from ..commands import getlockstate
#from ..commands import lockstate
#from ..commands import lockunlockdoors

class TestGetLockState(unittest.TestCase):

    def setUp(self):
       print("TestGetLockState: setUp")

    def test_bytesconstruction(self):
        getlock_state = bytearray([0x00, 0x20, 0x00])
        constructed_bytes = getlockstate.GetLockState().get_bytearray()
        self.assertEqual(constructed_bytes, getlock_state, 'GetLockState wrong bytes')


class TestLockState(unittest.TestCase):

    def setUp(self):
        print("TestLockState: setUp")

    def test_bytesparsing(self):
        # All locked, position closed
        LOCKED_STATE = b'00200103001001000200010200080000016b7a3c88ac03001001000201010200080000016b7a3c88b403001001000202010200080000016b7a3c88b803001001000203010200080000016b7a3c88b904001001000200000200080000016a7810e89104001001000201000200080000016b4177a38304001001000202000200080000016a7810e89104001001000203000200080000016b4177d264'
        LOCKED_STATE_decoded = LOCKED_STATE.decode()
        locked_state_hx = bytearray.fromhex(LOCKED_STATE_decoded)

        # All unlocked, position closed
        UNLOCKED_STATE = b'00200103001001000200000200080000016b7a3e506103001001000201000200080000016b7a3e506a03001001000202000200080000016b7a3e506d03001001000203000200080000016b7a3e506e04001001000200000200080000016a7810e89104001001000201000200080000016b4177a38304001001000202000200080000016a7810e89104001001000203000200080000016b4177d264'
        UNLOCKED_STATE_decoded = UNLOCKED_STATE.decode()
        unlocked_state_hx = bytearray.fromhex(UNLOCKED_STATE_decoded)

        cmd_obj = CommandResolver.resolve(locked_state_hx)
        print("\n App: command_incoming, cmd_obj: ", str(cmd_obj))
        with self.subTest(i=1):
            #print(" isinstance of LockState: " + str(isinstance(cmd_obj, lockstate.LockState)))
            self.assertIsInstance(cmd_obj, lockstate.LockState, 'LockState: locked wrong parsing')

        cmd_obj = CommandResolver.resolve(unlocked_state_hx)
        print("\n test_bytesparsing: cmd_obj: ", str(cmd_obj))
        with self.subTest(i=2):
            #print("\n test_bytesparsing: " + str(isinstance(cmd_obj, lockstate.LockState)))
            self.assertIsInstance(cmd_obj, lockstate.LockState, 'LockState: unlocked wrong parsing')


class TestLockUnlockDoors(unittest.TestCase):

    def setUp(self):
        print("TestLockState: setUp")

    def test_bytesconstruction(self):

        locked = bytearray([0x00, 0x20, 0x12, 0x01, 0x00, 0x04, 0x01, 0x00, 0x01, 0x01])
        # Lock, b'\x00 \x12\x01\x00\x04\x01\x00\x01\x01'
        constructed_bytes = lockunlockdoors.LockUnlockDoors(Lock.LOCKED).get_bytearray()
        with self.subTest(i=1):
            self.assertEqual(constructed_bytes, locked, 'LockUnlockDoors: locked wrong bytes')

        unlocked = bytearray([0x00, 0x20, 0x12, 0x01, 0x00, 0x04, 0x01, 0x00, 0x01, 0x00])
        # UNLocked, b'\x00 \x12\x01\x00\x04\x01\x00\x01\x00'
        constructed_bytes = lockunlockdoors.LockUnlockDoors(Lock.UNLOCKED).get_bytearray()
        with self.subTest(i=2):
            self.assertEqual(constructed_bytes, unlocked, 'LockUnlockDoors: unlocked wrong bytes')
