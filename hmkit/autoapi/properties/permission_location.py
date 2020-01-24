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

from . import *
import logging
from enum import Enum, unique
from hmkit.autoapi.properties.bit_location import BitLocation
from ..identifiers import Identifiers

log = logging.getLogger('hmkit.autoapi')

@unique
class PermissionType(Enum):
    """
    Enum Class for Permission Type (Read, Write, limited)
    """
    READ = 0x00
    WRITE = 0x01
    LIMITED = 0x02

class PermissionLocation(object):
    """
    Represents PermissionLocation
    """
    # Dict with ID as key then inner dict with type as key
    # data in inner dict is tuple(byte_position, bit_position)
    #dict{Key-ID: dict{Key-Type.READ: tuple(byte_position, bit_position), Key-Type.READ: tuple(byte_position, bit_position)}}

    Id_Type_BitPosition = {
    Identifiers.CAPABILITIES: {PermissionType.READ: (2, 0)},
    Identifiers.VEHICLE_STATUS: {PermissionType.READ: (2, 1)},
    Identifiers.DOOR_LOCKS: {PermissionType.READ: (2, 3), PermissionType.WRITE: (2, 4)},
    Identifiers.TRUNK_ACCESS: {PermissionType.READ: (2, 7), PermissionType.WRITE: (3, 0)},
    Identifiers.WAKE_UP: {PermissionType.WRITE: (3, 2)},
    Identifiers.CHARGING: {PermissionType.READ: (3, 3), PermissionType.WRITE: (3, 4)},
    Identifiers.CLIMATE: {PermissionType.READ: (3, 5), PermissionType.WRITE: (3, 6)},
    Identifiers.ROOFTOP: {PermissionType.READ: (4, 2), PermissionType.WRITE: (4, 3)},
    Identifiers.HONK_FLASH: {PermissionType.READ: (7, 2), PermissionType.WRITE: (4, 6)},
    Identifiers.REMOTE_CONTROL: {PermissionType.READ: (5, 0), PermissionType.WRITE: (5, 1)},
    Identifiers.VALET_MODE: {PermissionType.READ: (5, 2), PermissionType.WRITE: (5, 3), PermissionType.LIMITED: (5, 4)},
    Identifiers.HEART_RATE: {PermissionType.WRITE: (5, 6)},
    Identifiers.VEHICLE_LOCATION: {PermissionType.READ: (6, 0)},
    Identifiers.NAVI_DESTINATION: {PermissionType.READ: (7, 3), PermissionType.WRITE: (6, 1)},
    Identifiers.DIAGNOSTICS: {PermissionType.READ: (2, 2) },
    #Identifiers.MAINTENANCE: {PermissionType.READ: , Type.WRITE: },
    Identifiers.ENGINE: {PermissionType.READ: (2, 5), PermissionType.WRITE: (2, 6)},
    Identifiers.LIGHTS: {PermissionType.READ: (3, 7), PermissionType.WRITE: (4, 0)},
    Identifiers.MESSAGING: {PermissionType.READ: (6, 7), PermissionType.WRITE: (4, 7)},
    Identifiers.NOTIFICATIONS: {PermissionType.READ: (6, 7), PermissionType.WRITE: (4, 7)},
    Identifiers.FUELING: {PermissionType.READ: (8, 5), PermissionType.WRITE: (5, 5)},
    Identifiers.DRIVER_FATIGUE: {PermissionType.READ: (5, 7)},
    Identifiers.WINDSCREEN: {PermissionType.READ: (4, 4), PermissionType.WRITE: (4, 5)},
    Identifiers.VIDEO_HANDOVER: {PermissionType.WRITE: (4, 7)},
    Identifiers.TEXT_INPUT: {PermissionType.WRITE: (4, 7)},
    Identifiers.WINDOWS: {PermissionType.READ: (7, 1), PermissionType.WRITE: (4, 1)},
    Identifiers.THEFT_ALARM: {PermissionType.READ: (6, 2)},
    Identifiers.PARKING_TICKET: {PermissionType.READ: (6, 4), PermissionType.WRITE: (6, 5)},
    Identifiers.KEYFOB_POSITION: {PermissionType.READ: (6, 6)},
    Identifiers.BROWSER: {PermissionType.WRITE: (4, 7)},
    Identifiers.VEHICLE_TIME: {PermissionType.READ: (7, 0)},
    Identifiers.GRAPHICS: {PermissionType.WRITE: (4, 7)},
    Identifiers.OFF_ROAD: {PermissionType.READ: (7, 5)},
    Identifiers.CHASSIS_SETTINGS: {PermissionType.READ: (7, 6), PermissionType.WRITE: (7, 7)},
    Identifiers.LIGHT_CONDITIONS: {PermissionType.READ: (8, 4)},
    Identifiers.WEATHER_CONDITIONS: {PermissionType.READ: (8, 4) },
    Identifiers.SEATS: {PermissionType.READ: (8, 0), PermissionType.WRITE: (8, 1)},
    Identifiers.RACE: {PermissionType.READ: (7, 4)},
    Identifiers.PARKING_BRAKE: {PermissionType.READ: (8, 2), PermissionType.WRITE: (8, 3)},
    Identifiers.WIFI: {PermissionType.READ: (8, 6), PermissionType.WRITE: (8, 7)},
    Identifiers.HOME_CHARGER: {PermissionType.READ: (9, 0), PermissionType.WRITE: (9, 1)},
    Identifiers.DASHBOARD_LIGHTS: {PermissionType.READ: (9, 2)},
    Identifiers.CRUISE_CONTROL: {PermissionType.READ: (9, 3), PermissionType.WRITE: (9, 4)},
    Identifiers.START_STOP: {PermissionType.READ: (9, 5), PermissionType.WRITE: (9, 6)},
    Identifiers.TACHOGRAPH: {PermissionType.READ: (9, 7)},
    Identifiers.POWER_TAKE_OFF: {PermissionType.READ: (10, 0), PermissionType.WRITE: (10, 1)},
    Identifiers.MOBILE: {PermissionType.READ: (10, 3)},
    Identifiers.HOOD: {PermissionType.READ: (10, 4)},
    Identifiers.USAGE: {PermissionType.READ: (10, 2)} }

    @staticmethod
    def locationfor(identifier, permission_type):
        """
        From the AutoApi Identifier and Permission Type. It finds and returns the corresponding bit location of permission 
        to be looked in the permission bytes  

        :param bytearray identifier: hmkit.autoapi.identifiers.Identifiers
        :param permission_location.PermissionType permission_type: Permission type(read, write, limited)
        :rtype: bit_location.BitLocation
        """

        bit_location = None
        type_dict = PermissionLocation.Id_Type_BitPosition.get(identifier)

        if type_dict is not None:
            permission_location = type_dict.get(permission_type)
            if permission_location is not None:
                bit_location = BitLocation(permission_location[0], permission_location[1])


        #print("locationfor: " + str(bit_location))
        return bit_location
