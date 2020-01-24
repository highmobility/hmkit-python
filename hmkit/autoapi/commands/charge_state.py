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
import datetime
import struct
from .. import identifiers, msg_type, property_enumeration, command_with_properties
from ..properties import doorlockstate, doorposition
from ..properties.value.charging.charge_mode import ChargeMode
from ..properties.value.charging.charge_timer import ChargingTimer
from ..properties.value.charging.charge_port_state import ChargePortState
from ..properties.value.charging.charging_state import ChargingState
from ..properties.value.charging.departure_time import DepartureTime
from ..properties.value.charging.plug_type import PlugType
from ..properties.value.charging.reduction_time import ReductionTime
from ..properties.value.double_hm import DoubleHm

import logging

log = logging.getLogger('hmkit.autoapi')

class ChargeState(command_with_properties.CommandWithProperties):
    """
    Handle Charge State
    """

    ESTIMATED_RANGE = 0x02 # Integer 2 bytes
    BATTERY_LEVEL = 0x03 # Double 8 bytes
    BATTERY_CURRENT_AC = 0x04 # float 4 bytes
    BATTERY_CURRENT_DC = 0x05 # float 4 bytes
    CHARGER_VOLTAGE_AC = 0X06 # float 4 bytes
    CHARGER_VOLTAGE_DC = 0x07 # float 4 bytes
    CHARGE_LIMIT = 0x08 # Double 8 bytes
    TIME_TO_COMPLETE_CHARGE = 0x09 # Integer 2 bytes
    CHARGING_RATE_KW = 0x0A # float 4 bytes
    CHARGE_PORT_STATE = 0x0B # Enum 1 byte
    CHARGE_MODE = 0x0C # Enum 1 byte
    MAXIMUM_CHARGING_CURRENT = 0x0E # float 4 bytes
    PLUG_TYPE = 0x0F # Enum 1 byte
    CHARGING_WINDOW_CHOSEN = 0x10 # Enum 1 byte Choosen/NotChoosen
    DEPARTURE_TIMES = 0x11 # Enum 1 byte(Active State) + Integer 1 byte(Hour) + Integer 1 byte(Min)
    REDUCTION_OF_CHARGING_CURRENT_TIMES = 0x13 # Enum 1 byte(StartStop State) + Integer 1 byte(Hour) + Integer 1 byte(Min)
    BATTERY_TEMPERATURE = 0x14 # float 4 bytes
    TIMERS = 0x015  # Enum 1 byte(Timer Type) +  # Integer 8 bytes (ms since unix Epoch)
    PLUGGED_IN = 0x16 # Enum 1 byte
    CHARGING_STATE = 0x17  # Enum 1 byte

    def __init__(self, msgbytes):
        """
        Parse the Lock State messagebytes and construct the instance

        :param bytes msgbytes: Lock State message in bytes
        """

        # Construction of Lockstate is only required from Car side
        # Hence only parsing is implemented.
        log.debug(" ")
        super().__init__(msgbytes)

        self.estimated_range = None # Integer 2 bytes
        self.battery_level = None  # Double 8 bytes
        self.battery_current_ac = None # float 4 bytes
        self.battery_current_dc = None # float 4 bytes
        self.charger_voltage_ac = None # float 4 bytes
        self.charger_voltage_dc = None # float 4 bytes
        self.charge_limit = None  # Double 8 bytes
        self.time_to_complete_charge = None  # Integer 2 bytes
        self.charging_rate_kw = None # float 4 bytes
        self.charge_port_state = None  # Enum 1 byte
        self.charge_mode = None # Enum 1 byte
        self.maximum_charging_current = None  # float 4 bytes
        self.plug_type = None  # Enum 1 byte
        self.charging_window_chosen = None  # Enum 1 byte
        self.departure_times = None # Enum 1 byte(Active State) + Integer 1 byte(Hour) + Integer 1 byte(Min)
        self.reduction_of_charging_current_times = None  # Enum 1 byte(StartStop State) + Integer 1 byte(Hour) + Integer 1 byte(Min)
        self.battery_temperature = None  # float 4 bytes
        self.charging_timers = None   # Enum 1 byte(Timer Type) +  # Integer 8 bytes (ms since unix Epoch)
        self.plugged_in = None  # Enum 1 byte
        self.charging_state = None  # Enum 1 byte

        props = super().getProperties()
        prop_itr = self.properties_iterator

        i = 0
        while self.properties_iterator.has_next() == True:
            hmprop = self.properties_iterator.next()

            log.debug(" ChargeState props interation: " + str(i))
            i += i

            # TODO
            if hmprop.getproperty_identifier() == ChargeState.ESTIMATED_RANGE:
                log.debug(" ChargeState.ESTIMATED_RANGE")
                 # Integer 2 bytes
                if hmprop.getcomponent_valuebytes() is not None:
                    self.estimated_range = int.from_bytes(hmprop.getcomponent_valuebytes(), byteorder='big', signed=False)
                    log.debug("ChargeState.ESTIMATED_RANGE: " + str(self.estimated_range))

            elif hmprop.getproperty_identifier() == ChargeState.BATTERY_LEVEL:
                 # Double 8 bytes
                log.debug("ChargeState BATTERY_LEVEL")
                if hmprop.getcomponent_valuebytes() is not None:
                    battery_level = struct.unpack('!d',hmprop.getcomponent_valuebytes())
                    self.battery_level = DoubleHm(battery_level[0])
                    log.debug("ChargeState BATTERY_LEVEL: " + str(self.battery_level))

            elif hmprop.getproperty_identifier() == ChargeState.BATTERY_CURRENT_AC:
                 # float 4 bytes
                log.debug("ChargeState BATTERY_CURRENT_AC")
                if hmprop.getcomponent_valuebytes() is not None:
                    battery_current_ac = struct.unpack('!f',hmprop.getcomponent_valuebytes())
                    self.battery_current_ac = battery_current_ac[0]
                    log.debug("ChargeState BATTERY_CURRENT_AC: " + str(self.battery_current_ac))

            elif hmprop.getproperty_identifier() == ChargeState.BATTERY_CURRENT_DC:
                 # float 4 bytes
                log.debug("ChargeState BATTERY_CURRENT_DC")
                if hmprop.getcomponent_valuebytes() is not None:
                    battery_current_dc = struct.unpack('!f',hmprop.getcomponent_valuebytes())
                    self.battery_current_dc = battery_current_dc[0]
                    log.debug("ChargeState BATTERY_CURRENT_DC: " + str(self.battery_current_dc))

            elif hmprop.getproperty_identifier() == ChargeState.CHARGER_VOLTAGE_AC:
                 # float 4 bytes
                log.debug("ChargeState CHARGER_VOLTAGE_AC")
                if hmprop.getcomponent_valuebytes() is not None:
                    charger_voltage_ac = struct.unpack('!f',hmprop.getcomponent_valuebytes())
                    self.charger_voltage_ac = charger_voltage_ac[0]
                    log.debug("ChargeState CHARGER_VOLTAGE_AC: " + str(self.charger_voltage_ac))

            elif hmprop.getproperty_identifier() == ChargeState.CHARGER_VOLTAGE_DC:
                 # float 4 bytes
                log.debug("ChargeState CHARGER_VOLTAGE_DC")
                if hmprop.getcomponent_valuebytes() is not None:
                    charger_voltage_dc = struct.unpack('!f',hmprop.getcomponent_valuebytes())
                    self.charger_voltage_dc = charger_voltage_dc[0]
                    log.debug("ChargeState CHARGER_VOLTAGE_DC: " + str(self.charger_voltage_dc))

            elif hmprop.getproperty_identifier() == ChargeState.CHARGE_LIMIT:
                 # Double 8 bytes
                log.debug("ChargeState CHARGE_LIMIT")
                if hmprop.getcomponent_valuebytes() is not None:
                    charge_limit = struct.unpack('!d', hmprop.getcomponent_valuebytes())
                    self.charge_limit = DoubleHm(charge_limit[0])
                    log.debug("ChargeState CHARGE_LIMIT: " + str(self.charge_limit))

            elif hmprop.getproperty_identifier() == ChargeState.TIME_TO_COMPLETE_CHARGE:
                # Integer 2 bytes
                log.debug(" ChargeState.TIME_TO_COMPLETE_CHARGE")
                if hmprop.getcomponent_valuebytes() is not None:
                    self.time_to_complete_charge = int.from_bytes(hmprop.getcomponent_valuebytes(), byteorder='big', signed=False)
                    log.debug("ChargeState.TIME_TO_COMPLETE_CHARGE: " + str(self.time_to_complete_charge))

            elif hmprop.getproperty_identifier() == ChargeState.CHARGING_RATE_KW:
                # float 4 bytes
                log.debug("ChargeState CHARGING_RATE_KW")
                if hmprop.getcomponent_valuebytes() is not None:
                    charging_rate_kw = struct.unpack('!f',hmprop.getcomponent_valuebytes())
                    self.charging_rate_kw = charging_rate_kw[0]
                    log.debug("ChargeState CHARGING_RATE_KW: " + str(self.charging_rate_kw))

            elif hmprop.getproperty_identifier() == ChargeState.CHARGE_PORT_STATE:
                 # Enum 1 byte
                log.debug("ChargeState CHARGE_PORT_STATE")
                if hmprop.getcomponent_valuebytes() is not None:
                    charge_port_state = int.from_bytes(hmprop.getcomponent_valuebytes(), byteorder='big', signed=False)
                    self.charge_port_state = ChargePortState(charge_port_state)
                    log.debug("ChargeState CHARGE_PORT_STATE: " + str(self.charge_port_state))

            elif hmprop.getproperty_identifier() == ChargeState.CHARGE_MODE:
                # Enum 1 byte
                log.debug("ChargeState CHARGE_MODE")
                if hmprop.getcomponent_valuebytes() is not None:
                    charge_mode = int.from_bytes(hmprop.getcomponent_valuebytes(), byteorder='big', signed=False)
                    self.charge_mode = ChargeMode(charge_mode)
                    log.debug("ChargeState CHARGE_MODE: " + str(self.charge_mode))

            elif hmprop.getproperty_identifier() == ChargeState.MAXIMUM_CHARGING_CURRENT:
                 # float 4 bytes
                log.debug("ChargeState MAXIMUM_CHARGING_CURRENT")
                if hmprop.getcomponent_valuebytes() is not None:
                    maximum_charging_current = struct.unpack('!f',hmprop.getcomponent_valuebytes())
                    self.maximum_charging_current = maximum_charging_current[0]
                    log.debug("ChargeState MAXIMUM_CHARGING_CURRENT: " + str(self.maximum_charging_current))

            elif hmprop.getproperty_identifier() == ChargeState.PLUG_TYPE:
                 # Enum 1 byte
                log.debug("ChargeState PLUG_TYPE")
                if hmprop.getcomponent_valuebytes() is not None:
                    plug_type = int.from_bytes(hmprop.getcomponent_valuebytes(), byteorder='big', signed=False)
                    self.plug_type = PlugType(plug_type)
                    log.debug("ChargeState PLUG_TYPE: " + str(self.plug_type))

            elif hmprop.getproperty_identifier() == ChargeState.CHARGING_WINDOW_CHOSEN:
                 # Enum 1 byte (bool)
                log.debug(" ChargeState.CHARGING_WINDOW_CHOSEN")
                if hmprop.getcomponent_valuebytes() is not None:
                    self.charging_window_chosen = bool(int.from_bytes(hmprop.getcomponent_valuebytes(), byteorder='big', signed=False))
                    log.debug("CHARGING_WINDOW_CHOSEN bool: " + str(self.charging_window_chosen))

            elif hmprop.getproperty_identifier() == ChargeState.DEPARTURE_TIMES:
                # Enum 1 byte(Active State) + Integer 1 byte(Hour) + Integer 1 byte(Min)
                log.debug("ChargeState DEPARTURE_TIMES")
                if hmprop.getcomponent_valuebytes() is not None:
                    self.departure_time = DepartureTime(hmprop.getcomponent_valuebytes())
                    log.debug("ChargeState DEPARTURE_TIMES: " + str(self.departure_time))

            elif hmprop.getproperty_identifier() == ChargeState.REDUCTION_OF_CHARGING_CURRENT_TIMES:
                # Enum 1 byte(StartStop State) + Integer 1 byte(Hour) + Integer 1 byte(Min)
                log.debug("ChargeState REDUCTION_OF_CHARGING_CURRENT_TIMES")
                if hmprop.getcomponent_valuebytes() is not None:
                    self.reduction_time = ReductionTime(hmprop.getcomponent_valuebytes(), None, None)
                    log.debug("ChargeState REDUCTION_OF_CHARGING_CURRENT_TIMES: " + str(self.reduction_time))

            elif hmprop.getproperty_identifier() == ChargeState.BATTERY_TEMPERATURE:
                 # float 4 bytes
                log.debug("ChargeState BATTERY_TEMPERATURE")
                if hmprop.getcomponent_valuebytes() is not None:
                    battery_temperature = struct.unpack('!f',hmprop.getcomponent_valuebytes())
                    self.battery_temperature = battery_temperature[0]
                    log.debug("ChargeState BATTERY_TEMPERATURE: " + str(self.battery_temperature))

            elif hmprop.getproperty_identifier() == ChargeState.TIMERS:
                 # Enum 1 byte(Timer Type) +  Integer 8 bytes (ms since unix Epoch)
                log.debug("ChargeState TIMERS")
                if hmprop.getcomponent_valuebytes() is not None:
                    self.charging_timers = ChargingTimer(hmprop.getcomponent_valuebytes(), None, None)
                    log.debug("ChargeState TIMERS: " + str(self.charging_timers))

            elif hmprop.getproperty_identifier() == ChargeState.PLUGGED_IN:
                # Enum 1 byte (bool)
                log.debug(" ChargeState.PLUGGED_IN")
                if hmprop.getcomponent_valuebytes() is not None:
                    self.plugged_in = bool(int.from_bytes(hmprop.getcomponent_valuebytes(), byteorder='big', signed=False))
                    log.debug("Plugged_In bool: " + str(self.plugged_in))

            elif hmprop.getproperty_identifier() == ChargeState.CHARGING_STATE:
                 # Enum 1 byte
                log.debug("ChargeState CHARGING_STATE")
                if hmprop.getcomponent_valuebytes() is not None:
                    charging_state = int.from_bytes(hmprop.getcomponent_valuebytes(), byteorder='big', signed=False)
                    self.charging_state = ChargingState(charging_state)
                    log.debug("CHARGING_STATE: " + str(self.charging_state))

        return


    def get_estimated_range(self):
        """
        Get Estimated Range

        :param None:
        :rtype: int
        """
        return self.estimated_range


    def get_battery_level(self):
        """
        Get Battery Level

        :param None:
        :rtype: float 8 bytes(DoubleHm)
        """
        return self.battery_level

    def get_battery_current_ac(self):
        """
        Get Battery Current AC

        :param None:
        :rtype: float
        """
        return self.battery_current_ac

    def get_battery_current_dc(self):
        """
        Get Battery Current DC

        :param None:
        :rtype: float
        """
        return self.battery_current_dc

    def get_charger_voltage_ac(self):
        """
        Get Charger Voltage AC

        :param None:
        :rtype: float
        """
        return self.charger_voltage_ac

    def get_charger_voltage_dc(self):
        """
        Get Charger Voltage DC

        :param None:
        :rtype: float
        """
        return self.charger_voltage_dc


    def get_charge_limit(self):
        """
        Get Charge Limit

        :param None:
        :rtype: float 8 bytes(DoubleHm)
        """
        return self.charge_limit

    def get_time_to_complete_charge(self):
        """
        Get Time To Complete Charge

        :param None:
        :rtype: integer in (mins)
        """
        return self.time_to_complete_charge

    def get_charging_rate(self):
        """
        Get Charging Rate

        :param None:
        :rtype: float
        """
        return self.charging_rate_kw

    def get_charge_port_state(self):
        """
        Get Charge Port State

        :param None:
        :rtype: properties.value.charging.charge_port_state.ChargePortState
        """
        return self.charge_port_state

    def get_charge_mode(self):
        """
        Get Charge Mode

        :param None:
        :rtype: properties.value.charging.charge_mode.ChargeMode
        """
        return self.charge_mode

    def get_maxcharging_current(self):
        """
        Get Max Charging Current

        :param None:
        :rtype: float
        """
        return self.maximum_charging_current

    def get_plug_type(self):
        """
        Get Plug Type

        :param None:
        :rtype: properties.value.charging.plug_type.PlugType
        """
        return self.plug_type

    def get_charging_window_chosen(self):
        """
        Get Charging Window Chosen

        :param None:
        :rtype: bool
        """
        return self.charging_window_chosen

    def get_reduction_of_charging_currenttimes(self):
        """
        Get Reduction Of Charging Current Times

        :param None:
        :rtype:  properties.value.charging.reduction_time.ReductionTime
        """
        return self.reduction_of_charging_current_times

    def get_departure_times(self):
        """
        Get Departure Times

        :param None:
        :rtype:  properties.value.charging.departure_time.DepartureTime
        """
        return self.departure_times

    def get_battery_temperature(self):
        """
        Get Battery Temperature

        :param None:
        :rtype: float
        """
        return self.battery_temperature

    def get_timers(self):
        """
        Get Charging Timers

        :param None:
        :rtype: properties.value.charging.charge_timer.ChargingTimer
        """
        return self.timers

    def get_timer(self, timer_type):
        """
        Get Charging Timer

        :param timer_type:
        :rtype: properties.value.charging.charge_timer.ChargingTimer
        """
        for timer in self.timers:
            if timer.get_timertype() == timer_type:
                return timer


    def get_pluggedin(self):
        """
        Get Pluggedin

        :param None:
        :rtype: bool
        """
        return self.plugged_in

    def get_active_state(self):
        """
        Get Active State

        :param None:
        :rtype:  properties.value.charging.charging_state.ChargingState
        """
        return self.charging_state
