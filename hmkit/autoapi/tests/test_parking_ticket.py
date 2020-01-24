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

from hmkit.autoapi.properties.value.parking_ticketstate import ParkingTicketState

from hmkit.autoapi.commands import get_parkingticket
from hmkit.autoapi.commands import parkingticket
from hmkit.autoapi.commands import start_parking
from hmkit.autoapi.commands import end_parking

from datetime import datetime

class TestGetParkingTicket(unittest.TestCase):

    def setUp(self):
       print("TestGetParkingTicket: setUp")

    def test_bytesconstruction(self):
        getparking_ticket = bytearray([0x00, 0x47, 0x00])
        constructed_bytes = get_parkingticket.GetParkingTicket().get_bytearray()
        self.assertEqual(constructed_bytes, getparking_ticket, 'GetParkingTicket construct wrong bytes')


class TestParkingTicket(unittest.TestCase):

    def setUp(self):
        print("TestParkingTicket: setUp")

    def test_bytesparsing(self):

        # All locked, position closed
        # STARTED, Berlin Parking, 76543
        # Start Time: 2019-06-26 06:30:00.000000,(01:00:00) 1561510800000
        # EndTime: 2019-06-27 07:30:00.000000,(02:00:00) 1561600800000
        ParkingTicket = b'00470101000f010001010200080000016b8dfaa53c02001c01000e4265726c696e205061726b696e670200080000016b8dfaa54503001301000537363534330200080000016b8dfaa5470400160100080000016b914bea800200080000016b8dfaa5490500160100080000016b96a935000200080000016b935e5c92'
        ParkingTicket_decoded = ParkingTicket.decode()
        parking_ticket_hx = bytearray.fromhex(ParkingTicket_decoded)

        cmd_obj = CommandResolver.resolve(parking_ticket_hx)
        #print("\n App: command_incoming, cmd_obj: ", str(cmd_obj))
        self.assertIsInstance(cmd_obj, parkingticket.ParkingTicket, 'ParkingTicket: locked wrong parsing')

        #print(" getState: " + str(cmd_obj.getState()) + " type: " + str(type(cmd_obj.getState())))
        self.assertEqual(cmd_obj.getState(), ParkingTicketState.STARTED, 'ParkingTicket wrong State')

        #print(" getOperatorName: " + str(cmd_obj.getOperatorName()) + " type: " + str(type(cmd_obj.getOperatorName())))
        self.assertEqual(cmd_obj.getOperatorName(), "Berlin Parking", 'ParkingTicket Operator Name wrong')

        #print(" getOperatorTicketId: " + str(cmd_obj.getOperatorTicketId()) + " type: " + str(type(cmd_obj.getOperatorTicketId())))
        self.assertEqual(cmd_obj.getOperatorTicketId(), "76543", 'Parking Operator ID wrong ')

        datetime_str = '2019-06-26 01:00:00'
        endtime_str = '2019-06-27 02:00:00'
        startdatetime = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
        enddatetime = datetime.strptime(endtime_str, '%Y-%m-%d %H:%M:%S')
 
        self.assertEqual(cmd_obj.getTicketStartDate(), startdatetime, 'ParkingTicket: wrong start date')
        self.assertEqual(cmd_obj.getTicketEndDate(), enddatetime, 'ParkingTicket: wrong end date')


class TestStartParking(unittest.TestCase):

    def setUp(self):
        print("TestStartParking: setUp")

    def test_bytesconstruction(self):

        datetime_str = '06/26/19 01:00:00'
        endtime_str = '06/27/19 00:59:00'
        startdatetime = datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')
        enddatetime = datetime.strptime(endtime_str, '%m/%d/%y %H:%M:%S')
        constructed_bytes = start_parking.StartParking(None,"Berlin Parking","76543",startdatetime, enddatetime ).get_bytearray()
        print("TestStartParking: final bytes : " + str(constructed_bytes))

        startparking_ticket = bytearray([0x0,  0x47,  0x2,  0x1,  0x0,  0x11,  0x1,  0x0,  0xe,  0x42,  0x65,  0x72,  0x6c,  0x69,  0x6e,  0x20,  0x50,  0x61,  0x72,  0x6b,  0x69,  0x6e,  0x67,  0x2,  0x0,  0x8,  0x1,  0x0,  0x5,  0x37,  0x36,  0x35,  0x34,  0x33,  0x3,  0x0,  0xb,  0x1,  0x0,  0x8,  0x0,  0x0,  0x1,  0x6b,  0x91,  0x4b,  0xea,  0x80,  0x4,  0x0,  0xb,  0x1,  0x0,  0x8,  0x0,  0x0,  0x1,  0x6b,  0x96,  0x71,  0x5c,  0x20])
        with self.subTest(i=1):
            self.assertEqual(constructed_bytes, startparking_ticket, 'StartParking: construct wrong bytes')

class TestEndParking(unittest.TestCase):

    def setUp(self):
        print("TestEndParking: setUp")

    def test_bytesconstruction(self):

        endparking = bytearray([0x00, 0x47, 0x03])
        constructed_bytes = end_parking.EndParking().get_bytearray()
        self.assertEqual(constructed_bytes, endparking, 'TestEndParking: wrong bytes')


