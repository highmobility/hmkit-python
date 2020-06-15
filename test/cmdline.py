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
import datetime
import time
from hmkit import hmkit, linklistener, broadcastlistener, autoapi
import hmkit.autoapi as hm_autoapi
#from hmkit.autoapi import autoapi_dump
from hmkit.autoapi import CommandResolver
from hmkit.autoapi.commands import *
from hmkit.autoapi.commands import LockUnlockDoors
from hmkit.autoapi.commands import Notification, SendHeartRate, GetVehicleTime, VehicleTime
from hmkit.autoapi.commands import get_ignition_state, turn_ignition_onoff, get_vehiclestatus
from hmkit.autoapi.commands import GetDriverFatigueState, WakeUp, GetGasFlapState, ControlGasFlap
from hmkit.autoapi.commands import GetHomeChargerState, SetHomeChargerPriceTariff, AuthenticateHomeCharger
from hmkit.autoapi.commands import SetHomeChargeCurrent, ActivateHomeChargerSolar, EnableHomeChargerWifiHotSpot
from hmkit.autoapi.commands import GetTrunkState, TrunkState, ControlTrunk
from hmkit.autoapi.properties.value.lock import Lock
from hmkit.autoapi.properties.value.position import Position
from hmkit.autoapi.properties.value.charging import ChargeMode
from hmkit.autoapi.properties.value.charging import ChargingTimer, TimerType
from hmkit.autoapi.properties.value.charging import ChargePortState
from hmkit.autoapi.properties.value.charging import ReductionTime
from hmkit.autoapi.properties.value import ActionItem
from hmkit.autoapi.properties.value import StartStop
from hmkit.autoapi.properties.value import PricingType
from hmkit.autoapi.commands import SetReductionChargingCurrentTimes
from hmkit.autoapi.properties import PermissionLocation, PermissionType
from hmkit.autoapi.properties import Permissions
from hmkit.autoapi.properties import BitLocation
from hmkit.autoapi.properties import HomeChargeTariff
from hmkit.autoapi import Identifiers
from hmkit.autoapi import msg_type


import logging

log = logging.getLogger('hmkit')


# MERCEDES-BENZ EQC
# https://high-mobility.com/orgs/dGQg/emulators/E674453A685D7C0390#/


class Link_Listener(hmkit.linklistener.LinkListener):

    def __init__(self):
        pass

    def command_incoming(self, link, cmd):
        """
        Callback for incoming commands received from bluetooth link.
        Change in States will be received in this callback

        :param link Link: :class:`link` object
        :param bytearray cmd: data received
        :rtype: None
        """

        log.info("Len: " + str(len(cmd)))
        #log.debug("\n App: Cmd :", cmd)
        b_string = codecs.encode(cmd, 'hex')
        log.debug("*** Hex:* " + str(b_string) + " + Type: " + str(type(b_string)))
        #print("*** Hex:* " + str(b_string) + " + Type: " + str(type(b_string)))

        hmkit_inst = hmkit.get_instance()
        hmkit_inst.autoapi_dump.message_dump(cmd)

        cmd_obj = CommandResolver.resolve(cmd)
        log.debug("cmd_obj: " + str(cmd_obj))
        #log.debug(" isinstance of LockState: " + str(isinstance(cmd_obj, lockstate.LockState)))

        if isinstance(cmd_obj, capabilities.Capabilities):
            #print("App: Capabilities received ")

            # Example: Capability Checks
            doorlock_capability = cmd_obj.get_capability(Identifiers.DOOR_LOCKS) 
            is_sup = doorlock_capability.is_supported(msg_type.MsgType(Identifiers.DOOR_LOCKS,0x00))
            #print("App: get doorlocks() is_sup: " + str(is_sup))

            diags_capability = cmd_obj.get_capability(Identifiers.DIAGNOSTICS) 
            is_sup = diags_capability.is_supported(msg_type.MsgType(Identifiers.DIAGNOSTICS,0x00))
            #print("App: diags get() is_sup: " + str(is_sup))

            vehsts_capability = cmd_obj.get_capability(Identifiers.VEHICLE_STATUS)
            if vehsts_capability is not None:
                is_sup = vehsts_capability.is_supported(msg_type.MsgType(Identifiers.VEHICLE_STATUS,0x00))
                #print("App: is_sup: " + str(is_sup))
            #else:
                #print("Vehicle Status Capability not present")

            # Example: Permissions Check
            # Test Permission for VehicleStatus READ
            vehsts_permission_bitlocation = PermissionLocation.locationfor(Identifiers.VEHICLE_STATUS, PermissionType.READ)
            # get access_certificate, get permissions, serial mocked
            access_cert = hmkit_inst.get_certificate(None)
            permissions = access_cert.get_permissions()
            # check is_allowed from permissions.
            isallowed = permissions.is_allowed(vehsts_permission_bitlocation)
            #print("Permission check for Vehicle Status. isAllowed: ", isallowed)

        return 1

    def command_response(self, link, cmd):
        """
        Callback for command response received from bluetooth link
        Usually Acknowledgements

        :param link Link: :class:`link` object
        :param bytearray cmd: data received
        :rtype: None
        """

        log.info(" *** Msg: " + str(cmd) + " Len: " + str(len(cmd)))
        #print("\n LinkListener: App, Response Msg :", cmd)
        #b_string = codecs.encode(cmd, 'hex')
        #print("Response Hex: ", b_string, ", Type: ", type(b_string))
        #hmkit_inst = hmkit.hmkit.get_instance()
        #hmkit_inst.autoapi_dump.message_dump(cmd)
        return 1


class Broadcast_Listener(hmkit.broadcastlistener.BroadcastListener):

    def __init__(self):
        #print(" hm_app BroadcastListener(), __init__() ")
        self.bt_connected = 0;

    def connected(self, Link):
        log.info("App: Link connected")
        #print("App: Link connected")
        self.bt_connected = 1;
        #return 1

    def disconnected(self, Link):
        log.info("App: Link disconnected")
        #print("App: Link disconnected")
        self.bt_connected = 0;
        return 1

    def state_changed(self, state, old_state):
        # code: place holder api
        log.info("state_changed")
        print("state_changed")


# -----------------------------------------------------------------------------
# =============== Command Line processing for Sample App demo =================
# -----------------------------------------------------------------------------

class cmdline():

    commands = ("1 - doorlock","2 - doorunlock","3 - getlock","4 - getparkingticket",
    "5 - startparking","6 - endparking","7 - getparkingbreak","8 - setparkingbreak",
    "9 - getchargestate","10 - openchargeport", "11 - closechargeport","12 - setchargelimit",
    "13 - setchargemode","14 - setchargetimer","15 - setreductionchargecurr", "16 - startbroadcast", "17 - stopbroadcast",
    "18 - getcapabilities","19 - notification", "20 - clear notification",
    "21 - getignitionstate", "22 - turnIgnitionOn", "23 - getVehicleStatus", "24 - Level11 Sample",
    "25 - getdriverfatiguestate", "26 - wakeUp", "27 - getgasflap", "28 - controlgasflap", "29 - sendheartrate",
    "30 - gethomechargerstate", "31 - sethomechargerpricetariff", "32 - SetHomeChargeCurrent", "33 - ActivateHomeChargerSolar",
    "34 - EnableHomeChargerWifiHotSpot", "35 - AuthenticateHomeCharger", "36 - GetVehicleTime", "37 - GetTrunkState",
    "38 - ControlTrunk")

    def __init__(self):
        #print(" test_hm, __init__() ")
        pass

    def process_keys(self, input):
        i = 0
        valid = 1
        constructed_bytes = None

        if input == "exit":
            valid = 0
            log.critical("@@@@@@@@@@ Quiting Application @@@@@@@@@@")
            print("@@@@@@@@@@ Quiting Application @@@@@@@@@@")
            self.hmkit.hmkit_exit()
            print("@@@@@@@@@@ Exit @@@@@@@@@@")
            exit(0)
        elif input == "help":
            print("======= List of Commands =======")
            print("Keys: " + str(cmdline.commands))
            print("==== Enter the number selection: ")
            return

        if input.isdigit() == False:
            print("---- InValid Key---- ")
            return

        inp = int(input)

        if inp == 1:
            # Test Permission for Doorlock write
            doorlock_permission_bitlocation = PermissionLocation.locationfor(Identifiers.DOOR_LOCKS, PermissionType.WRITE)
            # get access_certificate, get permissions, serial mocked
            access_cert = self.hmkit.get_certificate(None)
            permissions = access_cert.get_permissions()
            # check is_allowed from permissions.
            isallowed = permissions.is_allowed(doorlock_permission_bitlocation)
            print("Permission check for DoorLocks. isAllowed: ", isallowed)

            constructed_bytes = lockunlockdoors.LockUnlockDoors(Lock.LOCKED).get_bytearray()
        elif inp == 2:
            constructed_bytes = lockunlockdoors.LockUnlockDoors(Lock.UNLOCKED).get_bytearray()
        elif inp == 3:
            constructed_bytes = getlockstate.GetLockState().get_bytearray()
        elif inp == 4:
            constructed_bytes = get_parkingticket.GetParkingTicket().get_bytearray()
        elif inp == 5:
            #datetime_str = '10/26/19 01:00:00'
            #endtime_str = '10/27/19 00:59:00'
            #startdatetime = datetime.datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')
            #enddatetime = datetime.datetime.strptime(endtime_str, '%m/%d/%y %H:%M:%S')
            #constructed_bytes = start_parking.StartParking(None,"Berlin Parking","76543",startdatetime, enddatetime ).get_bytearray()
            #print("ParkingMachine: send_start_parking")
            startdatetime = datetime.datetime.now()
            enddatetime = startdatetime + datetime.timedelta(days=1)
            constructed_bytes = start_parking.StartParking(None,"Berlin Parking","76543",startdatetime, enddatetime ).get_bytearray()
        elif inp == 6:
            constructed_bytes = end_parking.EndParking().get_bytearray()
        elif inp == 7:
            constructed_bytes = get_parkingbrake_state.GetParkingBrakeState().get_bytearray()
        elif inp == 8:
            constructed_bytes = set_parkingbrake_state.SetParkingBrakeState(False).get_bytearray()
        elif inp == 9:
            constructed_bytes = get_charge_state.GetChargeState().get_bytearray()
        elif inp == 10:
            constructed_bytes = open_close_charge_port.OpenCloseChargePort(ChargePortState.PORT_OPEN).get_bytearray()
        elif inp == 11:
            constructed_bytes = open_close_charge_port.OpenCloseChargePort(ChargePortState.PORT_CLOSE).get_bytearray()
        elif inp == 12:
            constructed_bytes = set_charge_limit.SetChargeLimit(0.6).get_bytearray()
        elif inp == 13:
            constructed_bytes = set_charge_mode.SetChargeMode(ChargeMode.INDUCTIVE).get_bytearray()
        elif inp == 14:
            datetime_str = '10/15/19 15:29:00'
            datetime_st = datetime.datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')
            chargingtimes = []
            chargingtimes.append(ChargingTimer(None, TimerType.PREFERRED_START_TIME, datetime_st))
            constructed_bytes = set_charging_timers.SetChargingTimers(None, chargingtimes).get_bytearray()
        elif inp == 15:
            datetime_time = datetime.time(11, 30)
            reductiontimes = []
            reductiontimes.append(ReductionTime(None, StartStop.STOP, datetime_time))
            constructed_bytes = SetReductionChargingCurrentTimes(None, reductiontimes).get_bytearray()
        elif inp == 16:
            hmkit.bluetooth.startBroadcasting()
        elif inp == 17:
            hmkit.bluetooth.stopBroadcasting()
        elif inp == 18:
            constructed_bytes = get_capabilities.GetCapabilities().get_bytearray()
        elif inp == 19:
            action_no = ActionItem(0, "No")
            action_yes = ActionItem(1, "Yes")
            actionitems = []
            actionitems.append(action_no)
            actionitems.append(action_yes)
            constructed_bytes = Notification("Would you like to Park", actionitems).get_bytearray()
        elif inp == 20:
            constructed_bytes = clear_notification.ClearNotification().get_bytearray()
        elif inp == 21:
            constructed_bytes = get_ignition_state.GetIgnitionState().get_bytearray()
        elif inp == 22:
            constructed_bytes = turn_ignition_onoff.TurnIgnitionOnOff(True).get_bytearray()
        elif inp == 23:
            constructed_bytes = get_vehiclestatus.GetVehicleStatus().get_bytearray()
        elif inp == 24:
            constructed_bytes = [0x0b, 0x00, 0x23, 0x00];
        elif inp == 25:
            constructed_bytes = GetDriverFatigueState().get_bytearray()
        elif inp == 26:
            constructed_bytes = WakeUp().get_bytearray()
        elif inp == 27:
            constructed_bytes = GetGasFlapState().get_bytearray()
        elif inp == 28:
            constructed_bytes = ControlGasFlap(Lock.UNLOCKED, Position.OPEN).get_bytearray()
        elif inp == 29:
            constructed_bytes = SendHeartRate(90).get_bytearray()
        elif inp == 30:
            constructed_bytes = GetHomeChargerState().get_bytearray()
        elif inp == 31:
            tariffs = []
            tariffs.append(HomeChargeTariff(PricingType.PER_MINUTE, 1.2, "$"))
            tariffs.append(HomeChargeTariff(PricingType.PER_KWH, 2.2, "$"))
            constructed_bytes = SetHomeChargerPriceTariff(None, tariffs).get_bytearray()
        elif inp == 32:
            constructed_bytes = SetHomeChargeCurrent(11.9).get_bytearray()
        elif inp == 33:
            constructed_bytes = ActivateHomeChargerSolar(True).get_bytearray()
        elif inp == 34:
            constructed_bytes = EnableHomeChargerWifiHotSpot(True).get_bytearray()
        elif inp == 35:
            constructed_bytes = AuthenticateHomeCharger(True).get_bytearray()
        elif inp == 36:
            constructed_bytes = GetVehicleTime().get_bytearray()
        elif inp == 37:
            constructed_bytes = GetTrunkState().get_bytearray()
        elif inp == 38:
            constructed_bytes = ControlTrunk(Lock.UNLOCKED, Position.OPEN).get_bytearray()
        else:
            print("InValid Key: " + str(inp))
            return

        if constructed_bytes is not None:
            if self.hmkit.bluetooth.broadcaster.is_connected() == False:
                print("---- PY: Device is not connected through Bluetooth. Cannot send commands ----")
                return;
            log.debug("*** final bytes : " + str(constructed_bytes))
            print("*** final bytes : " + str(constructed_bytes))
            log.debug(" after obj creation")
            self.hmkit.bluetooth.link.sendcommand(constructed_bytes)

        return;

    def listening_loop(self):

        #print("PY: test_loop() Entered py_main")
        print("======== List of Commands ========")
        print("Keys: " + str(cmdline.commands))

        print("==== Enter the number selection: ")
        print("'exit' for termination, 'help' for list of commands\n")
        while True:
            try:
                line = sys.stdin.readline()
            except KeyboardInterrupt:
                print("###### PY: test_loop() KeyboardInterrupt py_main ####")
                break

            if line:
                line = line[:-1]
                print("input: ", line)
                self.process_keys(line)

        print("###### PY: test_loop() END py_main ########")
        return;

    def start(self, hmkit):
        self.hmkit = hmkit
        self.listening_loop()
        return;

# -----------------------------------------------------------------------

if __name__== "__main__":

    # Initialise with HMKit class with a Device Certificate and private key. To start with
    # this can accept Base64 strings straight from the Developer Center

    hmkit = hmkit.HmKit(["dGVzdEUTEM0a92kpgEW5Yvfq8VEQmf2f8IFEgAQ34X7TPZjG6P4IGPyqorpJD8rXyK3aLejImdLZHaHT6jrPPdxpm+JzEjIGlwux3TZknv64nAAbejubKmAO8ua0MRs7lrzJ0r8CqMAUSY3+abRmmzRhHp6bQE0Q2pWMb0kqvGCsAbq92YuNkbvNSsSzeKo0vya7wrb8RoYs",
    "bXVCzrYtwwehRNYhJ2+wWj3iJBS1BvPYL9P8MofMBDI=",
    "5jAC31ddtR4RKeF2O10fuSNkYtCtzTW9uUWu+K4PfVZ1ZEO5L6so+zFpvykVxYdfEOqhX2Eba3gdjrEDvX144Q=="], logging.DEBUG)

    # Download Access Certificate with the token
    try:
        hmkit.get_instance().download_access_certificate(b"b063d69b-a069-4abc-ad02-d2ae99deffe4")

    except Exception as e:
        # Handle the error
        log.critical("Error in Access certicate download " + str(e.args[0]))
        print("Error in Access certicate download " + str(e.args[0]))
        hmkit.hmkit_exit()

    # local LinkListener object of sampleapp
    linkListener = Link_Listener()

    # local BroadcastListener object of sampleapp
    broadcastListener = Broadcast_Listener()

    # set link listener for BLE link device events
    hmkit.bluetooth.link.set_listener(linkListener)

    # set Broadcast listener for BT broadcast events
    hmkit.bluetooth.broadcaster.set_listener(broadcastListener)

    # Set BLE Device Name, it must be 8 chars
    hmkit.bluetooth.setBleDeviceName("parkhere")

    # Start BLE broadcasting/advertising, hmkit-core does it during init
    hmkit.bluetooth.startBroadcasting()

    #hmkit.bluetooth.stopBroadcasting()

    # for App Testing, Command Interface
    cmdline = cmdline()

    # Start command line based test loop
    cmdline.start(hmkit)
