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
import logging
#from .commands import *
from .commands import getlockstate, lockstate, lockunlockdoors, failure
from .commands import get_parkingbrake_state, parkingbrake_state, set_parkingbrake_state
from .commands import get_parkingticket, parkingticket, start_parking, end_parking
from .commands import capabilities, get_capability, get_capabilities
from .commands import ignition_state
#from .commands import get_homecharger_state, homecharger_state, set_charger_current, set_price_tariffs 
#from .commands import activate_deact_solar_charging, authenticate_expire_home_charger, enable_disable_wifi_hotspot
from .commands import get_charge_state, charge_state, start_stop_charging, set_charge_limit
from .commands import open_close_charge_port, set_charge_mode, set_charging_timers, setreduction_chargingcurrent_times
from .commands import notification, notification_action, clear_notification, notifications_state
from .commands import VehicleStatus
from .commands import get_homecharger_state, HomeCharger_State
from .commands import GasFlapState
from .commands import DriverFatigueState
from .commands import VehicleTime, GetVehicleTime
from .commands import GetTrunkState, TrunkState


#from . import identifiers
from .identifiers import Identifiers
from . import msg_type
from . import property_enumeration

log = logging.getLogger('hmkit.autoapi')

class CommandResolver(object):
    """
    parses the data bytes and finds out the corresponding Auto API class
    """
    # Lookup Dictionaries
    # Dictionary for each Message ID
    # Dictionary { Message Type Hex as Key : a List as Value }. List contains a string
    # and class
    # String represents the message type(used for debugging) and class type links to the
    # corresponding class implementation of the specific message  If the class type is
    # empty then it is not implemented yet.
    diagnostics = {  0x00:["GetDiagnosticsState"],  0x01:["DiagnosticsState"]}
    vehicle_status = {0x00:["GetVehicleStatus"],  0x01:["VehicleStatus", VehicleStatus]}
    historical = { 0x00:["GetHistoricalStates"],  0x01:["HistoricalStates"]}
    multicommand = { 0x02:["MultiCommand"], 0x01:["MultiState"]}
    doorlocks = { 0x00:["GetLockState",getlockstate.GetLockState],  0x01:["LockState",lockstate.LockState]}
    theft_alarm = { 0x00:["GetTheftAlarmState"], 0x01:["TheftAlarmState"], 0x12:["SetTheftAlarm"]}
    failure = { 0x01:["Failure", failure.Failure]}
    capabilities = {0x00:["GetCapabilities", get_capabilities.GetCapabilities],0x01:["Capabilities", capabilities.Capabilities]}
    trunk_access = { 0x00:["GetTrunkState", GetTrunkState], 0x01:["TrunkState", TrunkState]}
    hood = { 0x00:["GetHoodState"], 0x01:["HoodState"]}
    charging = { 0x00:["GetChargeState", get_charge_state.GetChargeState], 0x01:["ChargeState", charge_state.ChargeState]}
    climate = { 0x00:["GetClimateState"], 0x01:["ClimateState"]}
    rooftop = {0x00:["GetRooftopState"], 0x01:["RooftopState"]}
    honkflash = { 0x00:["GetFlashersState"], 0x01:["FlashersState"]}
    remote_control = { 0x00:["GetControlMode"], 0x04:["ControlCommand"], 0x01:["ControlMode"]}
    valet_mode = { 0x00:["GetValetMode"], 0x01:["ValetMode"]}
    vehicle_location = { 0x00:["GetVehicleLocation"], 0x01:["VehicleLocation"]}
    vehicle_time = { 0x00:["GetVehicleTime", GetVehicleTime], 0x01:["VehicleTime", VehicleTime]}
    navi_destination = { 0x00:["GetNaviDestination"], 0x01:["NaviDestination"]}
    maintenance = {  0x00:["GetMaintenanceState"], 0x01:["MaintenanceState"]}
    engine = { 0x00:["GetIgnitionState"], 0x01:["IgnitionState", ignition_state.IgnitionState]}
    lights = { 0x00:["GetLightsState"], 0x01:["LightsState"]}
    messaging = { 0x00:["MessageReceived"], 0x01:["SendMessage"]}
    notifications = { 0x00:["Notification", notification.Notification], 0x01:["NotificationState", notifications_state.NotificationsState]}
    windows = { 0x00:["GetWindowsState"], 0x01:["WindowsState"]}
    windscreen = { 0x00:["GetWindscreenState"], 0x01:["WindscreenState"]}
    fueling = { 0x00:["GetGasFlapState"], 0x01:["GasFlapState", GasFlapState], 0x12:["ControlGasFlap"]}
    parking_ticket = { 0x00:["GetParkingTicket", get_parkingticket.GetParkingTicket], 0x01:["ParkingTicket", parkingticket.ParkingTicket]}
    keyfob_position = { 0x00:["GetKeyfobPosition"], 0x01:["KeyFobPosition"]}
    firmware_version = { 0x00:["GetFirmwareVersion"], 0x01:["FirmwareVersion"]}
    race = { 0x00:["GetRaceState"], 0x01:["RaceState"]}
    off_road = { 0x00:["GetOffroadState"], 0x01:["OffroadState"]}
    chassis_settings = { 0x00:["GetChassisSettings"],  0x01:["ChassisSettings"]}
    seats = { 0x00:["GetSeatsState"], 0x01:["SeatsState"], }
    parking_brake = { 0x00:["GetParkingBrakeState", get_parkingbrake_state.GetParkingBrakeState], 0x01:["ParkingBrakeState",parkingbrake_state.ParkingBrakeState]}
    light_conditions = { 0x00:["GetLightConditions"], 0x01:["LightConditions"]}
    weather_conditions = { 0x00:["GetWeatherConditions"], 0x01:["WeatherConditions"]}
    wifi = { 0x00:["GetWifiState"], 0x01:["WifiState"]}
    home_charger = { 0x00:["GetHomeChargerState"], 0x01:["HomeChargerState", HomeCharger_State]}
    dashboard_lights = { 0x00:["GetDashboardLights"], 0x01:["DashboardLights"]}
    start_stop = { 0x00:["GetStartStopState"], 0x01:["StartStopState"]}
    cruise_control = { 0x00:["GetCruiseControlState"], 0x01:["CruiseControlState"]}
    power_take_off = { 0x00:["GetPowerTakeOffState"], 0x01:["PowerTakeOffState"]}
    tachograph = {0x00:["GetTachographState"],  0x01:["TachographState"]}
    mobile = { 0x00:["GetMobileState"], 0x01:["MobileState"]}
    usage = { 0x00:["GetUsage"],  0x01:["Usage"]}
    wakeup =  { 0x02:["WakeUp"]}
    video_handover = {0x00:["VideoHandover"]}
    browser = {0x00:["LoadUrl"]}
    graphics =  {0x00:["DisplayImage"]}
    text_input = {0x00:["TextInput"]}
    driver_fatigue_detected =  {0x01:["DriverFatigueDetected", DriverFatigueState]}
    heart_rate = { 0x01:["SendHeartRate"]}

    #MsgId_Str_Typ = { Identifiers.FAILURE.value:["FAILURE",failure],
    #Identifiers.FIRMWARE_VERSION.value:["FIRMWARE_VERSION",firmware_version]}

    # Lookup table (Dictionary) that links msg Identifier to the Message Type Lookup table
    MsgId_Str_Typ = { Identifiers.FAILURE.value:["FAILURE",failure],
    Identifiers.FIRMWARE_VERSION.value:["FIRMWARE_VERSION",firmware_version],
    Identifiers.CAPABILITIES.value:["CAPABILITIES",capabilities],
    Identifiers.VEHICLE_STATUS.value:["VEHICLE_STATUS",vehicle_status],
    Identifiers.HISTORICAL.value:["HISTORICAL",historical],
    Identifiers.MULTI_COMMAND.value:["MULTI_COMMAND",multicommand],
    Identifiers.DOOR_LOCKS.value:["DOOR_LOCKS",doorlocks],
    Identifiers.TRUNK_ACCESS.value:["TRUNK_ACCESS",trunk_access],
    Identifiers.WAKE_UP.value:["WAKE_UP",wakeup],
    Identifiers.CHARGING.value:["CHARGING",charging],
    Identifiers.CLIMATE.value:["CLIMATE",climate],
    Identifiers.ROOFTOP.value:["ROOFTOP",rooftop],
    Identifiers.HONK_FLASH.value:["HONK_FLASH",honkflash],
    Identifiers.REMOTE_CONTROL.value:["REMOTE_CONTROL",remote_control],
    Identifiers.VALET_MODE.value:["VALET_MODE",valet_mode],
    Identifiers.HEART_RATE.value:["HEART_RATE",heart_rate],
    Identifiers.VEHICLE_LOCATION.value:["VEHICLE_LOCATION",vehicle_location],
    Identifiers.NAVI_DESTINATION.value:["NAVI_DESTINATION",navi_destination],
    Identifiers.DIAGNOSTICS.value:["DIAGNOSTICS",diagnostics],
    Identifiers.MAINTENANCE.value:["MAINTENANCE",maintenance],
    Identifiers.ENGINE.value:["ENGINE",engine],
    Identifiers.LIGHTS.value:["LIGHTS",lights],
    Identifiers.MESSAGING.value:["MESSAGING",messaging],
    Identifiers.NOTIFICATIONS.value:["NOTIFICATIONS",notifications],
    Identifiers.FUELING.value:["FUELING",fueling],
    Identifiers.DRIVER_FATIGUE.value:["DRIVER_FATIGUE",driver_fatigue_detected],
    Identifiers.WINDSCREEN.value:["WINDSCREEN",windscreen],
    Identifiers.VIDEO_HANDOVER.value:["VIDEO_HANDOVER",video_handover],
    Identifiers.TEXT_INPUT.value:["TEXT_INPUT",text_input],
    Identifiers.WINDOWS.value:["WINDOWS",windows],
    Identifiers.THEFT_ALARM.value:["THEFT_ALARM",theft_alarm],
    Identifiers.PARKING_TICKET.value:["PARKING_TICKET",parking_ticket],
    Identifiers.KEYFOB_POSITION.value:["KEYFOB_POSITION",keyfob_position],
    Identifiers.BROWSER.value:["BROWSER",browser],
    Identifiers.VEHICLE_TIME.value:["VEHICLE_TIME",vehicle_time],
    Identifiers.GRAPHICS.value:["GRAPHICS",graphics],
    Identifiers.OFF_ROAD.value:["OFF_ROAD",off_road],
    Identifiers.CHASSIS_SETTINGS.value:["CHASSIS_SETTINGS",chassis_settings],
    Identifiers.LIGHT_CONDITIONS.value:["LIGHT_CONDITIONS",light_conditions],
    Identifiers.WEATHER_CONDITIONS.value:["WEATHER_CONDITIONS",weather_conditions],
    Identifiers.SEATS.value:["SEATS",seats],
    Identifiers.RACE.value:["RACE",race],
    Identifiers.PARKING_BRAKE.value:["PARKING_BRAKE",parking_brake],
    Identifiers.WIFI.value:["WIFI",wifi],
    Identifiers.HOME_CHARGER.value:["HOME_CHARGER",home_charger],
    Identifiers.DASHBOARD_LIGHTS.value:["DASHBOARD_LIGHTS",dashboard_lights],
    Identifiers.CRUISE_CONTROL.value:["CRUISE_CONTROL",cruise_control],
    Identifiers.START_STOP.value:["START_STOP",start_stop],
    Identifiers.TACHOGRAPH.value:["TACHOGRAPH",tachograph],
    Identifiers.POWER_TAKE_OFF.value:["POWER_TAKE_OFF",power_take_off],
    Identifiers.MOBILE.value:["MOBILE",mobile],
    Identifiers.HOOD.value:["HOOD",hood],
    Identifiers.USAGE.value:["USAGE",usage] }

    @classmethod
    def resolve(self, msgbytes):
        """
        parses the data bytes and returns the corresponding Auto API class object

        :param  bytearray msgbytes: autoapi data bytes
        :return: Autoapi class object with super type :class:`CommandWithProperties`
        :rtype: :class:`CommandWithProperties` 
        """
        version = msgbytes[0]
        msg_id = msgbytes[1:3]
        msgtyp = msgbytes[3]

        hex_id = codecs.encode(msg_id, 'hex')
        # get the List for the identifier which contain ID String and Msg Type list
        id_node_list = CommandResolver.MsgId_Str_Typ.get(hex_id)

        log.debug("resolve id_node_list: " + str(id_node_list))
        #print("resolve id_node_list: " + str(id_node_list))

        # get the type dictionary array list
        typ_dict_array = id_node_list[1]

        # from dictionary get the corresponsing type node
        typ_node = typ_dict_array.get(msgtyp)

        log.info("Type: " + str(type(typ_node)) + " LEN: " + str(len(typ_node)))
        #print("Type: " + str(type(typ_node)) + " LEN: " + str(len(typ_node)))

        if (len(typ_node) > 1) is not True:
            log.warning(">>>>> " + id_node_list[0] + " parsing is not implemented yet <<<<<<<")
            return None

        # get the command class from the Type node(list)
        cmd_object = typ_node[1](msgbytes[1:])

        log.info("Resolved Command Obj: " + str(type(cmd_object)) )

        return cmd_object
