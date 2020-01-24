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
from .. import identifiers, msg_type, property_enumeration, command_with_properties
from ..properties.value.action_item import ActionItem
import logging

log = logging.getLogger('hmkit.autoapi')

class NotificationAction(command_with_properties.CommandWithProperties):
    """
    Parses Notification Action and provided get Apis 
    """
    # Hack, work around for Emulator returned value
    IDENTIFIER_RECEIVED_ACTION = 0x03

    def __init__(self, msgbytes):
        """
        Parses  Notification Action Messsage and construct the object

        :param bytes msgbytes: Notification Action messsage bytes
        :rtype: None
        """
        # only parsing is implemented.
        log.debug(" ")
        super().__init__(msgbytes)
        log.debug(" msgbytes: " + str(msgbytes))

        props = super().getProperties()
        prop_itr = self.properties_iterator
 
        while self.properties_iterator.has_next() == True:
            hmprop = self.properties_iterator.next()

            log.debug(" has_next True, prop Id: " + str(hmprop.getproperty_identifier()))

            ### Bug in Emulator Data, reported ###
            # propbytes: b'\x01\x00\x01\x01' type: <class 'bytes'>
            # Hack it untill fixed
            #print(" NotificationAction, actionid: " + str(msgbytes[3]) + " type: " + str(type(msgbytes[3])))
            print(" NotificationAction, msgbytes: " + str(msgbytes) + " len: " + str(len(msgbytes)))

            #self.actionid = int.from_bytes(msgbytes[3], byteorder='big', signed=False)
            self.actionid = msgbytes[len(msgbytes)-1]
            print(" NotificationAction, actionid: " + str(self.actionid))

            '''
            # Only one Action ID will be there
            if hmprop.getproperty_identifier() == NotificationAction.IDENTIFIER_RECEIVED_ACTION:
                log.debug("NotificationAction IDENTIFIER_RECEIVED_ACTION")
                if hmprop.getcomponent_valuebytes() is not None:
                    self.actionid = int.from_bytes(hmprop.getcomponent_valuebytes(), byteorder='big', signed=False)
                    log.debug("Received ActionID: " + str(self.actionid))
            '''

        return


    def get_actionid(self):
        """
        Get the Action ID

        :param None:
        :rtype: int
        """
        log.debug("Action Id: " + str(self.actionid))
        return self.actionid
