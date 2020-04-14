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
from ..properties.value.charging.plug_type import PlugType
from ..properties.value.double_hm import DoubleHm
from ..properties.value import HomeChargerStatus, HomeChargerAuthMechanism, WifiHotspotSecurity
from ..properties.value import PricingType
from ..properties import HomeChargeTariff

import logging

log = logging.getLogger('hmkit.autoapi')

class HomeCharger_State(command_with_properties.CommandWithProperties):
    """
    Handle Charge State
    """

    CHARGING_STATUS = 0x01 # float
    AUTHENTICATION_MECHANISM = 0x02 # enum
    CHARGER_PLUG_TYPE = 0x03 # enum
    CHARGING_POWER_KW = 0x04 # float, 4 bytes
    SOLAR_CHARGING = 0x05 # enum
    WIFI_HOTSPOT_ENABLE = 0x08 # enum
    WIFI_HOTSPOT_SSID = 0x09 # string, variable len
    WIFI_HOTSPOT_SECURITY = 0x0A # enum
    WIFI_HOTSPOT_PASSWD = 0x0b # string,  variable len
    AUTHENTICATION_STATE = 0x0d # enum
    CHARGE_CURRENT_DC = 0x0e # float, 4 bytes
    MAX_CHARGING_CURRENT = 0x0F  # float, 4 bytes
    MIN_CHARGING_CURRENT = 0x10  # float, 4 bytes
    COORDINATES = 0x11 # latitude(double) 8 bytes, longitude(double) 8 bytes
    PRICE_TARIFF = 0x12 # Pricing Type(enum), Price(float), Currency(string)

    def __init__(self, msgbytes):
        """
        Parse the Home charger state  messagebytes and construct the instance

        :param bytes msgbytes: Home Charger State message in bytes
        """
        # Construction of Home Charger is only required from Car side
        # Hence only parsing is implemented.
        log.debug(" ")
        super().__init__(msgbytes)

        self.charging_status = None # float
        self.authentication_mechanism = None # enum
        self.plug_type = None # enum
        self.charging_power_kw = None # float
        self.solar_charging = None # enum
        self.wifi_hotspot_enable = None # enum
        self.wifi_hotspot_ssid = None # string
        self.wifi_hotspot_security = None # enum
        self.wifi_hotspot_passwd = None # string
        self.authentication_state = None # enum
        self.charge_current_dc = None # float
        self.max_charging_current = None # float
        self.min_charging_current = None # float
        self.coordinates_latitude = None # Double
        self.coordinates_longitude = None # Double
        self.tariff_type = None # enum
        self.tariff_price = None # float
        self.tariff_currency = None # string

        props = super().getProperties()
        prop_itr = self.properties_iterator

        i = 0
        while self.properties_iterator.has_next() == True:
            hmprop = self.properties_iterator.next()

            log.debug(" ChargeState props interation: " + str(i))
            i += i

            if hmprop.getproperty_identifier() == HomeCharger_State.CHARGING_STATUS:
                # Enum 1 byte
                log.debug("HomeCharger_State CHARGING_STATUS")
                if hmprop.getcomponent_valuebytes() is not None:
                    charging_sts = int.from_bytes(hmprop.getcomponent_valuebytes(), byteorder='big', signed=False)
                    self.charging_status = HomeChargerStatus(charging_sts)
                    log.debug(" CHARGING_STATUS: " + str(self.charging_status))

            elif hmprop.getproperty_identifier() == HomeCharger_State.AUTHENTICATION_MECHANISM:
                # Enum 1 byte
                log.debug("HomeCharger_State AUTHENTICATION_MECHANISM")
                if hmprop.getcomponent_valuebytes() is not None:
                    authentication_mech = int.from_bytes(hmprop.getcomponent_valuebytes(), byteorder='big', signed=False)
                    self.authentication_mechanism = HomeChargerAuthMechanism(authentication_mech)
                    log.debug(" AUTHENTICATION_MECHANISM: " + str(self.authentication_mechanism))

            elif hmprop.getproperty_identifier() == HomeCharger_State.CHARGER_PLUG_TYPE:
                # Enum 1 byte
                log.debug("HomeCharger_State CHARGER_PLUG_TYPE")
                if hmprop.getcomponent_valuebytes() is not None:
                    plug_type = int.from_bytes(hmprop.getcomponent_valuebytes(), byteorder='big', signed=False)
                    self.plug_type = PlugType(plug_type)
                    log.debug(" CHARGER_PLUG_TYPE: " + str(self.plug_type))

            elif hmprop.getproperty_identifier() == HomeCharger_State.CHARGING_POWER_KW:
                 # float 4 bytes
                log.debug("HomeCharger_State CHARGING_POWER_KW")
                if hmprop.getcomponent_valuebytes() is not None:
                    charging_powerkw = struct.unpack('!f',hmprop.getcomponent_valuebytes())
                    self.charging_power_kw = charging_powerkw[0]
                    log.debug(" CHARGING_POWER_KW: " + str(self.charging_power_kw))

            elif hmprop.getproperty_identifier() == HomeCharger_State.SOLAR_CHARGING:
                # Enum 1 byte (bool)
                log.debug(" HomeCharger_State.SOLAR_CHARGING")
                if hmprop.getcomponent_valuebytes() is not None:
                    self.solar_charging = bool(int.from_bytes(hmprop.getcomponent_valuebytes(), byteorder='big', signed=False))
                    log.debug("SOLAR_CHARGING bool: " + str(self.solar_charging))

            elif hmprop.getproperty_identifier() == HomeCharger_State.WIFI_HOTSPOT_ENABLE:
                 # Enum 1 byte (bool)
                log.debug(" HomeCharger_State.WIFI_HOTSPOT_ENABLE")
                if hmprop.getcomponent_valuebytes() is not None:
                    self.wifi_hotspot_enable = bool(int.from_bytes(hmprop.getcomponent_valuebytes(), byteorder='big', signed=False))
                    log.debug("WIFI_HOTSPOT_ENABLE bool: " + str(self.wifi_hotspot_enable))

            elif hmprop.getproperty_identifier() == HomeCharger_State.WIFI_HOTSPOT_SSID:
                log.debug("HomeCharger_State.WIFI_HOTSPOT_SSID")
                if hmprop.getcomponent_valuebytes() is not None:
                    self.wifi_hotspot_ssid = str(hmprop.getcomponent_valuebytes())
                    log.debug("WIFI_HOTSPOT_SSID : " + self.wifi_hotspot_ssid)

            elif hmprop.getproperty_identifier() == HomeCharger_State.WIFI_HOTSPOT_SECURITY:
                # Enum 1 byte
                log.debug("HomeCharger_State WIFI_HOTSPOT_SECURITY")
                if hmprop.getcomponent_valuebytes() is not None:
                    wifi_hotspotsecurity = int.from_bytes(hmprop.getcomponent_valuebytes(), byteorder='big', signed=False)
                    self.wifi_hotspot_security = WifiHotspotSecurity(wifi_hotspotsecurity)
                    log.debug("ChargeState WIFI_HOTSPOT_SECURITY: " + str(self.wifi_hotspot_security))

            elif hmprop.getproperty_identifier() == HomeCharger_State.WIFI_HOTSPOT_PASSWD:
                log.debug("HomeCharger_State.WIFI_HOTSPOT_PASSWD")
                if hmprop.getcomponent_valuebytes() is not None:
                    self.wifi_hotspot_passwd = str(hmprop.getcomponent_valuebytes())
                    log.debug("WIFI_HOTSPOT_PASSWD : " + self.wifi_hotspot_passwd)

            elif hmprop.getproperty_identifier() == HomeCharger_State.AUTHENTICATION_STATE:
                # Enum 1 byte (bool)
                log.debug(" HomeCharger_State.AUTHENTICATION_STATE")
                if hmprop.getcomponent_valuebytes() is not None:
                    self.authentication_state = bool(int.from_bytes(hmprop.getcomponent_valuebytes(), byteorder='big', signed=False))
                    log.debug("AUTHENTICATION_STATE bool: " + str(self.authentication_state))

            elif hmprop.getproperty_identifier() == HomeCharger_State.CHARGE_CURRENT_DC:
                # float 4 bytes
                log.debug("HomeCharger_State CHARGE_CURRENT_DC")
                if hmprop.getcomponent_valuebytes() is not None:
                    charge_currentdc = struct.unpack('!f',hmprop.getcomponent_valuebytes())
                    self.charge_current_dc = charge_currentdc[0]
                    log.debug(" CHARGE_CURRENT_DC: " + str(self.charge_current_dc))

            elif hmprop.getproperty_identifier() == HomeCharger_State.MAX_CHARGING_CURRENT:
                # float 4 bytes
                log.debug("HomeCharger_State MAX_CHARGING_CURRENT")
                if hmprop.getcomponent_valuebytes() is not None:
                    maxcharging_current = struct.unpack('!f',hmprop.getcomponent_valuebytes())
                    self.max_charging_current = maxcharging_current[0]
                    log.debug(" MAX_CHARGING_CURRENT: " + str(self.max_charging_current))

            elif hmprop.getproperty_identifier() == HomeCharger_State.MIN_CHARGING_CURRENT:
                # float 4 bytes
                log.debug("HomeCharger_State MIN_CHARGING_CURRENT")
                if hmprop.getcomponent_valuebytes() is not None:
                    min_chargingcurrent = struct.unpack('!f',hmprop.getcomponent_valuebytes())
                    self.min_charging_current = min_chargingcurrent[0]
                    log.debug(" MIN_CHARGING_CURRENT: " + str(self.min_charging_current))

            elif hmprop.getproperty_identifier() == HomeCharger_State.COORDINATES:

                log.debug("HomeCharger_State COORDINATES")
                if hmprop.getcomponent_valuebytes() is not None:
                    comp_bytes = hmprop.getcomponent_valuebytes()
                    # Double 8 bytes
                    coordinateslatitude = struct.unpack('!d',comp_bytes[0:8])
                    self.coordinates_latitude = DoubleHm(coordinateslatitude[0])
                    log.debug("COORDINATES Latitude: " + str(self.coordinates_latitude))

                    # Double 8 bytes
                    coordinateslongitude = struct.unpack('!d',comp_bytes[8:16])
                    self.coordinates_longitude = DoubleHm(coordinateslongitude[0])
                    log.debug("COORDINATES Longitude: " + str(self.coordinates_longitude))

            elif hmprop.getproperty_identifier() == HomeCharger_State.PRICE_TARIFF:
                log.debug("HomeCharger_State PRICE_TARIFF")
                if hmprop.getcomponent_valuebytes() is not None:
                    comp_bytes = hmprop.getcomponent_valuebytes()
                    self.tariff = HomeChargeTariff(None, None, None, comp_bytes)

        return


    def get_charging_status(self):
        """
        Get Charging Status

        :param None:
        :rtype: enum: properties.value.HomeChargerStatus
        """
        return self.charging_status


    def get_authentication_mechanism(self):
        """
        Get Authentication Mechanism

        :param None:
        :rtype: enum: properties.value.HomeChargerAuthMechanism
        """
        return self.authentication_mechanism

    def get_plug_type(self):
        """
        Get Home Charger Plug Type

        :param None:
        :rtype: enum: properties.value.PlugType
        """
        return self.plug_type

    def get_charging_powerkw(self):
        """
        Get Charging Powerkw

        :param None:
        :rtype: float
        """
        return self.charging_power_kw

    def get_solar_charging(self):
        """
        Get Solar Charging

        :param None:
        :rtype: bool
        """
        return self.solar_charging
 
    def get_wifi_hotspot_enable(self):
        """
        Get Wifi HotSpot Enable status

        :param None:
        :rtype: bool
        """
        return self.wifi_hotspot_enable

    def get_wifi_hotspot_ssid(self):
        """
        Get Wifi HotSpot SSID

        :param None:
        :rtype: Str
        """
        return self.wifi_hotspot_ssid

    def get_wifi_hotspot_security(self):
        """
        Get Wifi Hotspot Security

        :param None:
        :rtype: enum: properties.value.WifiHotspotSecurity
        """
        return self.wifi_hotspot_security

    def get_wifi_hotspot_passwd(self):
        """
        Get Wifi HotSpot Password

        :param None:
        :rtype: str:
        """
        return self.wifi_hotspot_passwd

    def get_authentication_state(self):
        """
        Get Authentication State

        :param None:
        :rtype: bool
        """
        return self.authentication_state

    def get_charge_current_dc(self):
        """
        Get Charge Current DC
        :param None:
        :rtype: float
        """
        return self.charge_current_dc

    def get_max_charging_current(self):
        """
        Get Max Charging Current
        :param None:
        :rtype: float
        """
        return self.max_charging_current

    def get_min_charging_current(self):
        """
        Get Min Charging Current

        :param None:
        :rtype: float
        """
        return self.min_charging_current

    def get_coordinates_latitude(self):
        """
        Get Coordinates Latitude

        :param None:
        :rtype: double
        """
        return self.coordinates_latitude

    def get_coordinates_longitude(self):
        """
        Get Coordinates Longitude

        :param None:
        :rtype: double
        """
        return self.coordinates_longitude

    def get_tariff(self):
        """
        Get Tariff

        :param None:
        :rtype: HomeChargeTariff: properties.homecharge_tariff.HomeChargeTariff
        """
        return self.tariff
