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

import sys
import time
import os
import subprocess
import threading
import codecs
import base64
import socket
import sys
from . import hm_pyc, link, broadcaster, bluetooth
import sys
import logging

log = logging.getLogger('hmkit')

class Bluetooth():
    """
    handles bluetooth advertisements control, callbacks registerations, connections
    """

    def startBroadcasting(self):
        """
        Start Bluetooth Advertisement to seek connection

        :rtype: None
        """
        log.info("\n")
        self.hm_pyc.ble_advertisement_start()


    def stopBroadcasting(self):
        """
        Stop Bluetooth Advertisement 

        :rtype: None
        """
        log.info("\n")
        self.hm_pyc.ble_advertisement_stop()


    def setBleDeviceName(self, name):
        """
        Set BLE Device Name

        :param string name: BLE Device name, must be 8 chars
        :rtype: int
        """
        log.info("\n")
        if len(name) != 8:
            log.error("BLE Device Name must be 8 characters, add some space ?")
            return 1

        self.hm_pyc.set_ble_device_name(name.encode())

    def py_cb_command_incoming(self, msg):
        """
        callback for bluetooh incoming command message. Callback forwarded to :class:`Link` 

        :param bytearray msg: received message
        :rtype: None
        """
        #log.debug("Len: " + str(len(msg)) + " Msg :" + str(msg))
        #b_string = codecs.encode(msg, 'hex')
        #log.debug("Hex: " + str(b_string) + ", Type: " + str(type(b_string)))

        self.link.cb_command_incoming(msg)

    def py_cb_command_response(self, msg):
        """
        callback for bluetooth received responses. Callback forwarded to :class:`Link` 

        :param bytearray msg: received message
        :rtype: None
        """
        ## log.debug("\n PY: bluetooth.py_cb_command_response\n")
        self.link.cb_command_response(msg)

    def py_cb_entered_proximity(self, msg):
        """
        callback for bluetooth connection. Callback forwarded to :class:`broadcaster` 

        :param bytearray msg: received message
        :rtype: None
        """
        log.info("\n cb_entered_proximity\n")
        self.broadcaster.connected(msg)

    def py_cb_exited_proximity(self, msg):
        """
        callback for bluetooth disconnection. Callback forwarded to :class:`broadcaster` 

        :param bytearray msg: received message
        :rtype: None
        """
        log.info("\n cb_exited_proximity\n")
        self.broadcaster.disconnected(msg)

    def reg_callbacks(self):
        """
        registers own callback methods to python-c interface module

        :rtype: None
        """
        ##print("PY: bluetooth.reg_callbacks")
        self.hm_pyc.register_cb("py_cb_command_response", self.py_cb_command_response)
        self.hm_pyc.register_cb("py_cb_entered_proximity", self.py_cb_entered_proximity)
        self.hm_pyc.register_cb("py_cb_exited_proximity", self.py_cb_exited_proximity)
        self.hm_pyc.register_cb("py_cb_command_incoming", self.py_cb_command_incoming)

    def __init__(self, pyc):
        """
        registers the own callback methods to python-c interface module

        :param module pyc: pythonc module
        :rtype: None
        """
        ##print("PY: Init bluetooth")
        self.hm_pyc = pyc
        self.broadcaster = broadcaster.Broadcaster()
        #TODO: create dynamically with mac, multiple possibility 
        self.link = link.Link(self.hm_pyc)
        self.reg_callbacks()
