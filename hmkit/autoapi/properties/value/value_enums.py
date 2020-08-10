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

from enum import Enum, unique
import logging

log = logging.getLogger('hmkit.autoapi')

@unique
class StartStop(Enum):
    """
    Enum Class for Start, Stop
    """
    START = 0x00
    STOP = 0x01
    RESET = 0x02

@unique
class PricingType(Enum):
    """
    Enum Class for Home Charger Tariff PricingType
    """
    STARTING_FEE = 0x00
    PER_MINUTE = 0x01
    PER_KWH = 0x02

@unique
class PowerTrainType(Enum):
    """
    Enum Class for Power Train Type
    """
    UNKNOWN = 0x00
    ALL_ELECTRIC = 0x01
    COMBUSTION_ENGINE = 0x02
    PLUG_IN_HYBRID_EV = 0x03
    HYDROGEN = 0x04
    HYDROGEN_HYBRID = 0x05

@unique
class Position(Enum):
    """
    Enum Class for Position of Door

    """
    CLOSED = 0x00
    OPEN = 0x01
    INTERMEDIATE = 0x02

@unique
class ParkingTicketState(Enum):
    """
    Enum Class for Parking Ticket States

    """
    ENDED = 0x00
    STARTED = 0x01


@unique
class Lock(Enum):
    """
    Enum Class for Lock State of Door
    """
    UNLOCKED = 0x00
    LOCKED = 0x01

@unique
class Location(Enum):
    """
    Enum Class for Locations (of Doors)
    """
    FRONT_LEFT = 0x00
    FRONT_RIGHT = 0x01
    REAR_RIGHT = 0x02
    REAR_LEFT = 0x03
    HATCH = 0x04
    ALL = 0x05


@unique
class HomeChargerStatus(Enum):
    """
    Enum Class for Home Charger Status
    """
    DISCONNECTED = 0x00
    PLUGGED_IN = 0x01
    CHARGING   = 0x02

@unique
class HomeChargerAuthMechanism(Enum):
    """
    Enum Class for Home Charger Authentication Mechanism
    """
    PIN = 0x00
    APP = 0x01

@unique
class GearBoxType(Enum):
    """
    Enum Class for Gear Box Type
    """
    MANUAL = 0x00
    AUTOMATIC = 0x01
    SEMI_AUTOMATIC = 0x02

@unique
class FatigueLevel(Enum):
    """
    Enum Class for Fatigue Level
    """

    LIGHT = 0x00
    PAUSE_RECOMMENDED = 0x01
    ACTION_NEEDED = 0X02
    CAR_READY_TO_TAKE_OVER = 0X03

@unique
class FailureReason(Enum):
    """
    Enum Class for Failure Reason
    """
    UNSUPPORTED_CAPABILITY = 0x00
    UNAUTHORISED = 0x01
    INCORRECT_STATE = 0x02
    EXECUTION_TIMEOUT = 0x03
    VEHICLE_ASLEEP = 0x04
    INVALID_COMMAND = 0x05
    PENDING = 0x06
    RATE_LIMIT = 0x07

@unique
class CurrentType(Enum):
    """
    Enum Class for Current Type
    """
    AC = 0x00
    DC = 0x01

class ChargeMode(Enum):
    """
    Enum Class for Charge Mode values
    """
    IMMEDIATE = 0x00
    TIMER_BASED = 0x01
    INDUCTIVE   = 0x02

@unique
class ChargePortState(Enum):
    """
    Enum Class for Charge Mode values
    """
    PORT_CLOSE = 0x00
    PORT_OPEN = 0x01


@unique
class ChargingStatus(Enum):
    """
    Enum Class for Charging Status values
    """
    NOT_CHARGING = 0x00
    CHARGING = 0x01
    CHARGING_COMPLETE = 0x02
    INITIALISING = 0x03
    CHARGING_PAUSED = 0x04
    CHARGING_ERROR  = 0x05
    CABLE_UNPLUGGED  = 0x06
    SLOW_CHARGING = 0x07
    FAST_CHARGING = 0x08
    DISCHARGING = 0x09
    FOREIGN_OBJECT_DETECTED = 0x0A

@unique
class PlugType(Enum):
    """
    Enum Class for Charge Mode values
    """
    TYPE_1 = 0x00
    TYPE_2 = 0x01
    COMBINED_CHARGING_SYSTEM = 0x02
    CHA_DE_MO = 0x03

@unique
class WifiHotspotSecurity(Enum):
    """
    Enum Class for Wifi Hotspot security
    """
    NONE = 0x00
    WEP = 0x01
    WPA_WPA2 = 0x02
    WPA2 = 0x03

