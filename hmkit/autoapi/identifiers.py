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
import traceback
from . import msg_type
#from .msg_type import MsgType
from enum import Enum
import logging

log = logging.getLogger('hmkit.autoapi')

class Identifiers(Enum):

    # Identifier Enums
    FAILURE = b'0002'
    FIRMWARE_VERSION = b'0003'
    CAPABILITIES = b'0010'
    VEHICLE_STATUS = b'0011'
    HISTORICAL = b'0012'
    MULTI_COMMAND = b'0013'
    DOOR_LOCKS = b'0020'
    TRUNK_ACCESS = b'0021'
    WAKE_UP = b'0022'
    CHARGING = b'0023'
    CLIMATE = b'0024'
    ROOFTOP = b'0025'
    HONK_FLASH = b'0026'
    REMOTE_CONTROL = b'0027'
    VALET_MODE = b'0028'
    HEART_RATE = b'0029'
    VEHICLE_LOCATION = b'0030'
    NAVI_DESTINATION = b'0031'
    DIAGNOSTICS = b'0033'
    MAINTENANCE = b'0034'
    ENGINE = b'0035'
    LIGHTS = b'0036'
    MESSAGING = b'0037'
    NOTIFICATIONS = b'0038'
    FUELING = b'0040'
    DRIVER_FATIGUE = b'0041'
    WINDSCREEN = b'0042'
    VIDEO_HANDOVER = b'0043'
    TEXT_INPUT = b'0044'
    WINDOWS = b'0045'
    THEFT_ALARM = b'0046'
    PARKING_TICKET = b'0047'
    KEYFOB_POSITION = b'0048'
    BROWSER = b'0049'
    VEHICLE_TIME = b'0050'
    GRAPHICS = b'0051'
    OFF_ROAD = b'0052'
    CHASSIS_SETTINGS = b'0053'
    LIGHT_CONDITIONS = b'0054'
    WEATHER_CONDITIONS = b'0055'
    SEATS = b'0056'
    RACE = b'0057'
    PARKING_BRAKE = b'0058'
    WIFI = b'0059'
    HOME_CHARGER = b'0060'
    DASHBOARD_LIGHTS = b'0061'
    CRUISE_CONTROL = b'0062'
    START_STOP = b'0063'
    TACHOGRAPH = b'0064'
    POWER_TAKE_OFF = b'0065'
    MOBILE = b'0066'
    HOOD = b'0067'
    USAGE = b'0068'

    DOOR_LOCKS_HEX = [0x00, 0x20]

    def __init__(self, identifier):
        """
        :param bytes identifier: Identifier bytes
        :rtype: None
        :raises: None
        """
        log.debug("Identifiers, __init__() ")
        self.identifier = identifier
        return


    def get_bytes(self):
        """
        :param bytes __:
        :rtype: None
        :raises: None
        """
        return self.identifier


