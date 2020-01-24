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
from hmkit.autoapi.identifiers import Identifiers
import hmkit.autoapi.msg_type
from ..properties import hmproperty
from datetime import datetime
import logging

log = logging.getLogger('hmkit.autoapi')

class StartParking(command_with_properties.CommandWithProperties):
    """
    Constructs Start parking message
    """
    PARKING_STATUS_IDENTIFIER = 0x01
    OPERATOR_NAME_IDENTIFIER = 0x02
    OPERATOR_TICKET_ID_IDENTIFIER = 0x03
    TICKET_START_TIME_IDENTIFIER = 0x04
    TICKET_END_TIME_IDENTIFIER = 0x05

    def __init__(self, msgbytes, operator_name, operatorticket_id, start_time, end_time):
        """
        Constructs Start parking message and constructs an instance

        :param msgbytes : bytearray 
        :param operator_name : str
        :param operatorticket_id : str
        :param start_date :  datetime.datetime
        :param end_date :  datetime.datetime
        :rtype: None
        """
        print(" ")
        self.msg_type = msg_type.MsgType(Identifiers.PARKING_TICKET,0x01)

        super().__init__(None, self.msg_type)
 
        self.status = None
        self.operator_name = None
        self.ticket_id = None
        self.start_time = None
        self.end_time = None

        # Message Construction Case
        if msgbytes is None:
            properties = []

	    # Parking Status. Constant Value 0x01 (Started)
            self.status = hmproperty.HmProperty(None, StartParking.PARKING_STATUS_IDENTIFIER, 0x01, None, None)
            log.debug("status: " + str(self.status))
            properties.append(self.status)

            # construct case
            if isinstance(operator_name, str):
                # create a property
                # TODO, get timestamp and failure from arg
                log.debug("operator_name: " + str(operator_name))
                self.operator_name = hmproperty.HmProperty(None, StartParking.OPERATOR_NAME_IDENTIFIER, operator_name, None, None)
                properties.append(self.operator_name)
            else:
                log.debug("wrong parameter type for operator_name Expected Str but : " + str(type(operator_name)))

            if isinstance(operatorticket_id, str):
                # create a property
                # TODO, get timestamp and failure from arg
                log.debug("ticket_id: " + str(operatorticket_id))
                self.ticket_id = hmproperty.HmProperty(None, StartParking.OPERATOR_TICKET_ID_IDENTIFIER, operatorticket_id, None, None)
                #super().create_bytes(self.parkbrakestate)
                properties.append(self.ticket_id)
            else:
                log.debug("wrong parameter type for ticket_id Expected Str but : " + str(type(ticket_id)))

            if isinstance(start_time, datetime):
                # create a property
                # TODO, get timestamp and failure from arg
                log.debug("start_time: " + str(start_time))
                self.start_time = hmproperty.HmProperty(None, StartParking.TICKET_START_TIME_IDENTIFIER, start_time, None, None)
                #super().create_bytes(self.parkbrakestate)
                properties.append(self.start_time)
            else:
                log.debug("wrong parameter type for start_time Expected datetime but : " + str(type(start_time)))

            if isinstance(end_time, datetime):
                # create a property
                # TODO, get timestamp and failure from arg
                log.debug("end_time: " + str(end_time))
                self.end_time = hmproperty.HmProperty(None, StartParking.TICKET_END_TIME_IDENTIFIER, end_time, None, None)
                #super().create_bytes(self.parkbrakestate)
                properties.append(self.end_time)
            else:
                log.debug("wrong parameter type for end_time Expected datetime but : " + str(type(end_time)))
    
            super().create_bytes(properties)

        else:
            log.debug("parsing case not required for link device ")

        return


    def getOperatorName(self):
        """
        < For internal use >
        Get Operator Name

        :param None:
        :rtype: hmproperty.HmProperty str
        """
        log.debug(str(self.operator_name))
        return self.operator_name


    def getOperatorTicketId(self):
        """
        < For internal use >
        Get Operator TicketID

        :param None:
        :rtype: hmproperty.HmProperty str
        """
        log.debug( str(self.ticket_id))
        return self.ticket_id


    def getTicketStartDate(self):
        """
        < For internal use >
        Get Ticket Start Date

        :param None:
        :rtype: hmproperty.HmProperty (datetime.datetime)
        """
        log.debug(str(self.start_time))
        return self.start_time


    def getTicketEndDate(self):
        """
        < For internal use >
        Get Ticket End Date

        :param None:
        :rtype: hmproperty.HmProperty (datetime.datetime)
        """
        log.debug(str(self.end_time))
        return self.end_time

