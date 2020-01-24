#!/usr/bin/env python
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
import sys, os
import logging
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
import HtmlTestRunner
from test_door_locks import TestGetLockState, TestLockState, TestLockUnlockDoors
from test_parking_brake import TestGetParkingBrakeState, TestParkingBrakeState, TestSetParkingBrakeState
from test_parking_ticket import TestGetParkingTicket, TestParkingTicket, TestStartParking, TestEndParking
from test_charging import TestGetChargeState, TestStartStopCharging, TestSetChargeLimit, TestSetChargeMode, TestSetChargingTimers

html_report_dir = './html_report'

#-------- Logging Config ------------
"""
logging.basicConfig(filename='hm_py.log',level=logging.DEBUG)
hmlog = logging.getLogger('hmkit')
autoapilog = logging.getLogger('hmkit.autoapi')
"""
LOG_FILE = "hm_py_test.log"
logger = logging.getLogger('hmkit')
logger.setLevel(logging.DEBUG)
# define file handler and set formatter
file_handler = logging.FileHandler('hm_testlog_{:%Y-%m-%d-%H-%M-%S}.log'.format(datetime.now()))
#file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
formatter   = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(module)s:%(funcName)s():%(lineno)d : %(message)s')
#formatter  = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(funcName)s:%(lineno)d : %(message)s')
file_handler.setFormatter(formatter)
# add file handler to logger
logger.addHandler(file_handler)
log = logger


def test_suite():

    suites = unittest.TestSuite()

    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestGetLockState))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestLockState))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestLockUnlockDoors))
    suites.addTest(suite)

    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestGetParkingBrakeState))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestParkingBrakeState))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestSetParkingBrakeState))
    suites.addTest(suite)

    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestGetParkingTicket))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestStartParking))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestEndParking))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestParkingTicket))
    suites.addTest(suite)

    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestGetChargeState))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestStartStopCharging))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestSetChargeLimit))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestSetChargeMode))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestSetChargingTimers))
    suites.addTest(suite)


    return suites
      
def run_test_suite_generate_html_report(test_suite):

    # Create HtmlTestRunner object and run the test suite.
    test_runner = HtmlTestRunner.HTMLTestRunner(output=html_report_dir)
    test_runner.run(test_suite)
    return


if __name__ == "__main__":

    suite = test_suite()

    #run_test_suite_generate_html_report(suite)
    result = unittest.TextTestRunner(stream=sys.stdout, verbosity=2).run(unittest.TestSuite(suite))
    if result.failures != 0:
        sys.exit(1)
