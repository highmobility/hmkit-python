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
import logging
from .. import identifiers, msg_type, property_enumeration, command_with_properties
import hmkit.autoapi
from hmkit.autoapi.identifiers import Identifiers
import hmkit.autoapi.msg_type
from ..properties.value.failure_reason import FailureReason
from ..properties import hmproperty
from ..msg_type import MsgType

log = logging.getLogger('hmkit.autoapi')

class Failure(command_with_properties.CommandWithProperties):
    """
    Handle Failure Message
    """

    COMMAND_ID_IDENTIFIER = 0x01
    COMMAND_TYPE_IDENTIFIER = 0x02
    FAILURE_REASON_IDENTIFIER = 0x03
    FAILURE_DESCRIP_IDENTIFIER = 0x04

    def __init__(self, msgbytes):
        """
        Parse the Failure messagebytes

        :param bytes msgbytes: Failure message in bytes
        """

        # Construction of Failure is only required from Car side
        # Hence only parsing is implemented.
        log.debug(" ")
        super().__init__(msgbytes)

        self.failed_identifier = None
        self.failed_type_byte = None
        self.failure_reason = None # Enum
        self.failure_descrip = None

        props = super().getProperties()
        prop_itr = self.properties_iterator 
 
        while self.properties_iterator.has_next() == True:
            hmprop = self.properties_iterator.next()

            # TODO  
            if hmprop.getproperty_identifier() == Failure.COMMAND_ID_IDENTIFIER:
                log.debug(" COMMAND_ID_IDENTIFIER")
                if hmprop.getcomponent_valuebytes() is not None:
                    msg_id_bytes = hmprop.getcomponent_valuebytes()
                    msg_id = codecs.encode(msg_id_bytes, 'hex')
                    self.failed_identifier = Identifiers(msg_id)
                    log.debug("COMMAND_ID_IDENTIFIER: ID: " + str(self.failed_identifier) + " value: " + str(self.failed_identifier.value) )

            elif hmprop.getproperty_identifier() == Failure.COMMAND_TYPE_IDENTIFIER:
                log.debug(" COMMAND_TYPE_IDENTIFIER")
                if hmprop.getcomponent_valuebytes() is not None:
                    msgtype = int.from_bytes(hmprop.getcomponent_valuebytes(), byteorder='big', signed=False)
                    self.failed_type = MsgType(self.failed_identifier, msgtype)
                    log.debug("COMMAND_TYPE_IDENTIFIER: " + str(self.failed_type) )

            elif hmprop.getproperty_identifier() == Failure.FAILURE_REASON_IDENTIFIER:
                log.debug(" FAILURE_REASON_IDENTIFIER")
                if hmprop.getcomponent_valuebytes() is not None:
                    reason_id = int.from_bytes(hmprop.getcomponent_valuebytes(), byteorder='big', signed=False)
                    self.failure_reason = FailureReason(reason_id)
                    log.debug("FAILURE_REASON_IDENTIFIER: ID: " + str(self.failure_reason) + " value: " + str(self.failure_reason.value) )
    
            elif hmprop.getproperty_identifier() == Failure.FAILURE_DESCRIP_IDENTIFIER:
                log.debug(" FAILURE_DESCRIP_IDENTIFIER")
                if hmprop.getcomponent_valuebytes() is not None:
                    self.failure_descrip = hmprop.getcomponent_valuebytes()
                    log.debug("FAILURE_DESCRIP_IDENTIFIER: Descp: " + str(self.failure_descrip) + " Type: " + str(type(self.failure_descrip)) )

        return

    def get_failed_identifier(self):
        """
        Get Failed Identifier

        :param None:
        :rtype: identifiers.Identifiers
        """
        return self.failed_identifier

    def get_failed_type(self):
        """
        Get Failed Type

        :param None:
        :rtype: hmkit.autoapi.msg_type.MsgType
        """
        return self.failed_type

    def get_failure_reason(self):
        """
        Get Failure Reason

        :param None:
        :rtype: Enum properties.value.failure_reason.FailureReason
        """
        return self.failure_reason

    def get_failure_description(self):
        """
        Get Failure Description

        :param None:
        :rtype: byte array (UTF-8)
        """
        return self.failure_descrip
