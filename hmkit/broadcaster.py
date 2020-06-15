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
from . import link
import logging

log = logging.getLogger('hmkit')

class Broadcaster(object):
    """
    handles bluetooth connections and disconnections
    """

    def connected(self, msg):
        """
        gets called for bluetooth connection. Invokes connected method of :class:`BroadcastListener` 

        :param bytearray msg: received message
        :rtype: None
        """
        log.critical("\n--------- BLE Device Connected (broadcaster) ------")
        print("\n--------- BLE Device Connected ------")
        self.bt_connected = 1;
        if self.broadcastlistener is not None:
            self.broadcastlistener.connected(msg)

    def is_connected(self):

        if self.bt_connected == 1:
            isconnected = True
        else:
            isconnected = False

        return isconnected

    def disconnected(self, msg):
        """
        gets called for bluetooth disconnection. Invokes disconnected method of :class:`BroadcastListener` 

        :param bytearray msg: received message
        :rtype: None
        """
        log.critical("\n-------- BLE Device Disconnected (broadcaster) -------\n")
        print("\n-------- BLE Device Disconnected (broadcaster) -------\n")
        self.bt_connected = 0;
        if self.broadcastlistener is not None:
            self.broadcastlistener.disconnected(msg)

    def set_listener(self, broadcastlistener):
        """
        setter for :class:`BroadcastListener`. Connection Events received are relayed to broadcastlistener instance.

        :param broadcastlistener broadcastlistener: :class:`BroadcastListener` object
        :rtype: None
        """
        #log.debug("\n-------- broadcaster.set_listener -------")
        self.broadcastlistener = broadcastlistener

    def __init__(self):
        #log.debug("------- Init broadcaster -------")
        self.broadcastlistener = None
        self.bt_connected = 0;
        #TODO: create dynamically for mac, multiple possibility
        #self.link = link.Link(self)
