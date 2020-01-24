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
from .. import identifiers
from .. import msg_type, property_enumeration, command_with_properties
import hmkit.autoapi
from ..properties import hmproperty
from hmkit.autoapi.identifiers import Identifiers
import hmkit.autoapi.msg_type
from ..properties.value.action_item import ActionItem
import logging

log = logging.getLogger('hmkit.autoapi')

class NotificationsState(command_with_properties.CommandWithProperties):
    """
    Parse Notifications State message
    """
    IDENTIFIER_TEXT = 0x01
    IDENTIFIER_ACTION_ITEM = 0x02
    IDENTIFIER_ACTIVATED_ACTION = 0x03
    IDENTIFIER_CLEAR_NOTIFICATION = 0x04

    def __init__(self, msgbytes):
        """
        Parse Notifications State message

        :param bytes msgbytes: Lock State message in bytes
        """
        log.debug(" ")
        super().__init__(msgbytes)

        self.notification_text = None
        self.actionitems = []
        self.activated_action_id = None
        self.clean_notification = None

        props = super().getProperties()
        prop_itr = self.properties_iterator

        while self.properties_iterator.has_next() == True:
            hmprop = self.properties_iterator.next()

            if hmprop.getproperty_identifier() == NotificationsState.IDENTIFIER_TEXT:
                log.debug("NotificationsState.IDENTIFIER_TEXT")
                if hmprop.getcomponent_valuebytes() is not None:
                    self.notification_text = str(hmprop.getcomponent_valuebytes())
                    log.debug("NotificationsState.IDENTIFIER_TEXT : " + self.notification_text)

            elif hmprop.getproperty_identifier() == NotificationsState.IDENTIFIER_ACTION_ITEM:
                log.debug("NotificationsState.IDENTIFIER_ACTION_ITEM")
                if hmprop.getcomponent_valuebytes() is not None:
                    self.actionitems.append(ActionItem(None, None, hmprop.getcomponent_valuebytes()))
                    log.debug("NotificationsState.IDENTIFIER_ACTION_ITEM : " + str(self.actionitems))

            elif hmprop.getproperty_identifier() == NotificationsState.IDENTIFIER_ACTIVATED_ACTION:
                log.debug("NotificationsState.IDENTIFIER_ACTIVATED_ACTION")
                if hmprop.getcomponent_valuebytes() is not None:
                    self.activated_action_id = hmprop.getcomponent_valuebytes()
                    log.debug("NotificationsState.IDENTIFIER_ACTIVATED_ACTION_ID : " + str(self.activated_action_id))

            elif hmprop.getproperty_identifier() == NotificationsState.IDENTIFIER_CLEAR_NOTIFICATION:
                log.debug("NotificationsState.IDENTIFIER_CLEAR_NOTIFICATION")
                if hmprop.getcomponent_valuebytes() is not None:
                    self.clean_notification = hmprop.getcomponent_valuebytes()
                    log.debug("NotificationsState.IDENTIFIER_CLEAR_NOTIFICATION : " + str(self.clean_notification))

        return

    def get_notification_text(self):
        """
        get notification text

        :param None:
        :rtype: string
        """
        return self.notification_text

    def get_action_items(self):
        """
        get notification action items

        :param None:
        :rtype: ActionItem[]
        """
        return self.actionitems

    def get_activated_action_id(self):
        """
        get notification activated action id

        :param None:
        :rtype: int
        """
        return self.activated_action_id

    def get_clean_notificationi(self):
        """
        get clean notification value

        :param None:
        :rtype: int
        """
        return self.clean_notification
