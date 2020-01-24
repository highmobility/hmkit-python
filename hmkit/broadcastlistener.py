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
import codecs
from . import link
#from abc import ABCMeta, abstractmethod
from abc import ABC, abstractmethod
import logging

log = logging.getLogger('hmkit')

class BroadcastListener(ABC):
    """
    Abstract base class for broadcastlistener. Defines the blue print for broadcastlistening.
    Class and methods to be implemented by the app as defined here.
    """
#    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def connected(self, link):
        """
        Callback for bluetooth connection.

        :param link Link: :class:`Link` object
        :rtype: None
        """
        #link.set_listener(self)
        pass

    @abstractmethod
    def disconnected(self, link):
        """
        Callback for bluetooth disconnection.

        :param link Link: :class:`Link` object
        :rtype: None
        """
        pass

    @abstractmethod
    def state_changed(self, state):
        """
        Place holder api. Callback for bluetooth connection changes (TODO)

        :param state state:
        :rtype: None
        """
        #def state_changed(self, state, old_state):
        # code
        pass
