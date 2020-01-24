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
from . import hmkit
from . import hm_pyc
from . import linklistener
import logging

log = logging.getLogger('hmkit')

class Link(object):
    """
    Class handles data communication with the bluetooth connected link
    """

    def __init__(self, pyc):

        self.hm_pyc = pyc
        self.linklistener = None

    def set_listener(self, linklistener):
        """
        setter for :class:`LinkListener`. Data received from connected link are relayed to linklistener instance.

        :param linklistener linklistener: :class:`LinkListener` object
        :rtype: None
        """
        self.linklistener = linklistener

    def sendcommand(self, msg):
        """
        send the message to the bluetooth connected link

        :param bytearray msg: data bytearray to be sent through bluetooth
        :rtype: None
        """
        msgbytes = bytes(msg)
        log.info("PY: msgbytes: " + str(msgbytes) + " type: " + str(type(msgbytes)))
        ret = self.hm_pyc.sendcommand(msgbytes)

    def cb_command_incoming(self, cmd):
        """
        Callback, Incoming command Data received from the bluetooth connected link is forwarded here,
        That is again forwarded to the registered linklistener.

        :param bytearray cmd: Incoming command bytearray
        :rtype: None
        """
        ##log.debug("---------- Len: " + str(len(cmd)) + " ,Cmd : " + str(cmd))
        #b_string = codecs.encode(cmd, 'hex')
        #log.debug("Hex: " + str(b_string) + " ,Type: " + str(type(b_string)))
        if self.linklistener is not None:
            self.linklistener.command_incoming(self, cmd)
        return 1

    def cb_command_response(self, cmd):
        """
        Callback, Incoming response Data received from the bluetooth connected link is forwarded here,
        That is again forwarded to the registered linklistener.

        :param bytearray cmd: Incoming response bytearray
        :rtype: None
        """
        ##log.debug("------ Len: " + str(len(cmd)) + " ,Msg: " + str(cmd))
        #b_string = codecs.encode(cmd, 'hex')
        #log.debug("Hex: " + str(b_string) " ,Type: " + str(type(b_string)))
        if self.linklistener is not None:
            self.linklistener.command_response(self, cmd)
        return 1

    def state_changed(self, state):
        """
        [TODO] Callback, Incoming response Data received from the bluetooth connected link is forwarded here,
        That is again forwarded to the registered linklistener.

        :param  state: change in connected link state
        :rtype: None
        """
        # code
        #link.send_command([])
        #log.debug(" ")
        pass
