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
from ..properties import doorlockstate, doorposition
from ..properties.value.lock import Lock
from ..properties.value.position import Position
import logging

log = logging.getLogger('hmkit.autoapi')

class LockState(command_with_properties.CommandWithProperties):
    """
    Handle Door Lock States
    """
    # Doors Position - Open, Close
    # Doors Lock Inside - Lock, Unlock
    # Doors Lock Outside - Lock, Unlock

    INSIDE_LOCKS_IDENTIFIER = 0x02
    OUTSIDE_LOCKS_IDENTIFIER = 0x03
    POSITION_IDENTIFIER = 0x04
    INSIDE_LOCKS_STATE_IDENTIFIER = 0x05 # whole car
    LOCKS_STATE_IDENTIFIER = 0x06 # whole car

    def __init__(self, msgbytes):
        """
        Parse the Lock State messagebytes and construct the instance

        :param bytes msgbytes: Lock State message in bytes
        """

        # Construction of Lockstate is only required from Car side
        # Hence only parsing is implemented.
        log.debug(" ")
        super().__init__(msgbytes)

        self.inside_locks = []
        self.outside_locks = []
        self.position_states = []

        props = super().getProperties()
        prop_itr = self.properties_iterator 
 
        while self.properties_iterator.has_next() == True:
            hmprop = self.properties_iterator.next()

            # TODO  
            if hmprop.getproperty_identifier() == LockState.INSIDE_LOCKS_IDENTIFIER:
                log.debug(" INSIDE_LOCKS_IDENTIFIER")
                if hmprop.getcomponent_valuebytes() is not None:
                    doorlockst = doorlockstate.DoorLockSate(hmprop.getcomponent_valuebytes())
                    self.inside_locks.append(doorlockst)
                    log.debug(" INSIDE_LOCKS_IDENTIFIER: " + str(doorlockst))

            elif hmprop.getproperty_identifier() == LockState.OUTSIDE_LOCKS_IDENTIFIER:
                log.debug(" OUTSIDE_LOCKS_IDENTIFIER")
                if hmprop.getcomponent_valuebytes() is not None:
                    doorlockst = doorlockstate.DoorLockSate(hmprop.getcomponent_valuebytes())
                    self.outside_locks.append(doorlockst)
                    log.debug(" OUTSIDE_LOCKS_IDENTIFIER: " + str(doorlockst))

            elif hmprop.getproperty_identifier() == LockState.POSITION_IDENTIFIER:
                log.debug(" POSITION_IDENTIFIER")
                if hmprop.getcomponent_valuebytes() is not None:
                    doorpos = doorposition.DoorPosition(hmprop.getcomponent_valuebytes())
                    self.position_states.append(doorpos)
                    log.debug(" POSITION_IDENTIFIER: " + str(doorpos))

            elif hmprop.getproperty_identifier() == LockState.INSIDE_LOCKS_STATE_IDENTIFIER:
                log.debug(" INSIDE_LOCKS_STATE_IDENTIFIER")
                if hmprop.getcomponent_valuebytes() is not None:
                    lock_bytes = hmprop.getcomponent_valuebytes()
                    self.inside_locks_state = Lock(int(lock_bytes[0]))
                    log.debug(" INSIDE_LOCKS_STATE_IDENTIFIER: " + str(lock_bytes))

            elif hmprop.getproperty_identifier() == LockState.LOCKS_STATE_IDENTIFIER:
                log.debug(" LOCKS_STATE_IDENTIFIER")
                if hmprop.getcomponent_valuebytes() is not None:
                    lock_bytes = hmprop.getcomponent_valuebytes()
                    self.locks_state = Lock(int(lock_bytes[0]))
                    log.debug(" LOCKS_STATE_IDENTIFIER: " + str(lock_bytes))

        return


    def getoutside_locks(self):
        """
        Get all outside locks

        :param None:
        :rtype: List of properties.doorlockstate.DoorLockSate
        """
        return self.outside_locks


    def getoutside_lock(self, doorlocation):
        """
        Get all outside lock

        :param Enum doorlocation: :class:`.value.location.Location`
        :rtype: properties.doorlockstate.DoorLockSate
        """
        for outsidelock in self.outside_locks:
            if outsidelock.get_location() == doorlocation:
                return outsidelock

        # not found ?
        return None

    def getinside_locks(self):
        """
        Get all inside locks

        :param None:
        :rtype: List of properties.doorlockstate.DoorLockSate
        """
        return self.inside_locks

    def getinside_locks_state(self):
        """
        Get inside locks state for whole car

        :param None:
        :rtype: properties.value.lock.Lock
        """
        return self.inside_locks_state

    def get_locks_state(self):
        """
        Get locks state for whole car

        :param None:
        :rtype: properties.value.lock.Lock
        """
        return self.locks_state


    def getinside_lock(self, doorlocation):
        """
        Get inside lock for the location specified by doorlocation parameter

        :param Enum doorlocation: :class:`.value.location.Location`
        :rtype: properties.doorlockstate.DoorLockSate
        """
        for insidelock in self.inside_locks:
            if insidelock.get_location() == doorlocation:
                return insidelock

        return None


    def getpositions(self):
        """
        Get all doors positions

        :param None:
        :rtype: List of properties.doorposition.DoorPosition
        """
        return self.position_states


    def getposition(self, doorlocation):
        """
        Get door position for the location specified by doorlocation parameter

        :param Enum doorlocation: :class:`.value.location.Location`
        :rtype: properties.doorposition.DoorPosition
        """
        for door_position in self.position_states:
            if door_position.get_location() == doorlocation:
                return door_position

    # Whether all of the outside door locks are locked
    def islocked(self):
        """
        is all Doors Locked. return False even if a single door is UnLocked

        :param None:
        :rtype: True/False
        """
        for outsidelock in self.outside_locks:
            if outsidelock.get_lock() == Lock.UNLOCKED:
                return False

        return True


    def json_dump(self):
        """

        :param None:
        :rtype: None
        """
        # TODO: failure and timestamp
        dicobj_inside_locks = {"insidelocks":{"value":[]}}
        for lock in self.inside_locks:
            location_tmp = lock.get_location()
            lock_tmp = lock.get_lock()
            dicobj_inside_locks["insidelocks"]["value"].append({"doorLocation": location_tmp.name, "lockState": lock_tmp.name})

        dicobj_locks = {"locks":{"value":[]}}
        for lock in self.outside_locks:
            #index = self.outside_locks.index(lock)
            location_tmp = lock.get_location()
            lock_tmp = lock.get_lock()
            dicobj_locks["locks"]["value"].append({"doorLocation": location_tmp.name, "lockState": lock_tmp.name})


        dicobj_pos = {"positions":{"value":[]}}
        for position in self.position_states:
            location_tmp = position.get_location()
            pos_tmp = position.get_position()
            #dicobj_pos["positions"]["value"] = {"doorLocation": location_tmp.name, "position":  pos_tmp.name}
            dicobj_pos["positions"]["value"].append({"doorLocation": location_tmp.name, "position":  pos_tmp.name})


        result_dict = dicobj_inside_locks
        result_dict.update(dicobj_locks)
        result_dict.update(dicobj_pos)

        diclockst = {"lockstate":result_dict}

        print(diclockst)
        #print("**final: " + resDic)
        json_out = json.dumps(diclockst, indent=4)
        print(json_out)

        return json_out

