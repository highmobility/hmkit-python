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
from ..properties.value.parking_ticketstate import ParkingTicketState
from datetime import datetime
import logging

log = logging.getLogger('hmkit.autoapi')

class ParkingTicket(command_with_properties.CommandWithProperties):
    """
    Parses Parking Ticket message bytes and provides get APIs for the internal parameters
    """

    TICKET_STATE_IDENTIFIER = 0x01
    OPERATOR_NAME_IDENTIFIER = 0x02
    OPERATOR_TICKET_ID_IDENTIFIER = 0x03
    TICKET_START_TIME_IDENTIFIER = 0x04
    TICKET_END_TIME_IDENTIFIER = 0x05

    def __init__(self, msgbytes):
        """
        Parses Parking Ticket Messsage and construct the object

        :param bytes msgbytes: Parking Ticket message bytes
        :rtype: None
        """
        # Construction of ParkingTicket is only required from Car side
        # Hence only parsing is implemented.
        log.debug(" ")
        super().__init__(msgbytes)
        log.debug(" after")

        self.ticket_state = None
        self.operator_name = None
        self.ticket_id = None
        self.start_time = None
        self.end_time = None

        props = super().getProperties()
        prop_itr = self.properties_iterator
 
        print("********************* Parking Ticket Received *************************")
        while self.properties_iterator.has_next() == True:
            hmprop = self.properties_iterator.next()

            # TODO  
            if hmprop.getproperty_identifier() == ParkingTicket.TICKET_STATE_IDENTIFIER:
                log.debug("ParkingTicket TICKET_STATE_IDENTIFIER")
                if hmprop.getcomponent_valuebytes() is not None:
                    ticketstate = int.from_bytes(hmprop.getcomponent_valuebytes(), byteorder='big', signed=False)
                    self.ticket_state = ParkingTicketState(ticketstate)
                    log.debug("parking_ticketstate: " + str(self.ticket_state))
                    print("parking_ticketstate: " + str(self.ticket_state))

            elif hmprop.getproperty_identifier() == ParkingTicket.OPERATOR_NAME_IDENTIFIER:
                log.debug("ParkingTicket OPERATOR_NAME_IDENTIFIER")
                if hmprop.getcomponent_valuebytes() is not None:
                    self.operator_name = hmprop.getcomponent_valuebytes().decode("utf-8") # get the string equivalent of hex bytes
                    log.debug("operator_name: " + str(self.operator_name))
                    print("operator_name: " + str(self.operator_name))

            elif hmprop.getproperty_identifier() == ParkingTicket.OPERATOR_TICKET_ID_IDENTIFIER:
                log.debug("ParkingTicket OPERATOR_TICKET_ID_IDENTIFIER")
                if hmprop.getcomponent_valuebytes() is not None:
                    self.ticket_id  = hmprop.getcomponent_valuebytes().decode("utf-8") # get the string equivalent of hex bytes
                    log.debug("ticket_id: " + str(self.ticket_id))
                    print("ticket_id: " + str(self.ticket_id))

            elif hmprop.getproperty_identifier() == ParkingTicket.TICKET_START_TIME_IDENTIFIER:
                log.debug("ParkingTicket TICKET_START_TIME_IDENTIFIER")
                if hmprop.getcomponent_valuebytes() is not None:
                    self.start_time = hmprop.getvalue_frombytes(hmprop.getcomponent_valuebytes(), datetime)
                    #self.start_time = hmprop.getvalue_frombytes(hmprop.getcomponent_valuebytes(), type(datetime))
                    log.debug("ParkingTicket Start-Time: " + str(self.start_time))
                    print("ParkingTicket Start-Time: " + str(self.start_time.strftime("%m/%d/%Y, %H:%M:%S")))
            elif hmprop.getproperty_identifier() == ParkingTicket.TICKET_END_TIME_IDENTIFIER:
                log.debug("ParkingTicket TICKET_END_TIME_IDENTIFIER")
                if hmprop.getcomponent_valuebytes() is not None:
                    self.end_time = hmprop.getvalue_frombytes(hmprop.getcomponent_valuebytes(), datetime)
                    log.debug("ParkingTicket End-Time: " + str(self.end_time))
                    print("ParkingTicket End-Time: " + str(self.end_time.strftime("%m/%d/%Y, %H:%M:%S")))
        print("**************************************************************")

        return


    def get_state(self):
        """
        Get the Parking Ticket State

        :param None:
        :rtype: properties.value.parking_ticketstate.ParkingTicketState
        """
        log.debug(" " + str(self.ticket_state))
        return self.ticket_state

    def get_operator_name(self):
        """
        Get the Operator Name (Parking Ticket)

        :param None:
        :rtype: str
        """
        log.debug(str(self.operator_name))
        return self.operator_name

    def get_operator_ticketId(self):
        """
        Get the Operator Ticket ID(Parking Ticket)

        :param None:
        :rtype: str
        """
        log.debug(str(self.ticket_id))
        return self.ticket_id


    def get_ticket_startdate(self):
        """
        Get the Start Date of Parking Ticket

        :param None:
        :rtype: datetime.datetime
        """
        log.debug(str(self.start_time))
        return self.start_time


    def get_ticket_enddate(self):
        """
        Get the End Date of Parking Ticket

        :param None:
        :rtype: datetime.datetime
        """
        log.debug(str(self.end_time))
        return self.end_time
