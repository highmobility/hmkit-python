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
from . import msg_type
from . import property_enumeration
from . import identifiers
from . import command_resolver
from .identifiers import Identifiers
import logging

log = logging.getLogger('hmkit.autoapi')

class autoapi_dump():
    """
    Prints out the Internals of the passed message. Like ID, Type, Properties etc
    Will be useful for debugging
    """
    def bytes2int(self, strid):
        # For internal usage
         return int(strid.encode('hex'), 16)

    def  message_dump(self, msg):
        """
        parses the data bytes and prints(log.debug level) the internals of the received msg

        :param  bytearray msg: autoapi data bytes
        :rtype: None
        """
        api_version = msg[0]
        msg_id = msg[1:3]
        msgtyp = msg[3]
        ##print("---- MSG ID: " + str(msg_id) + " MSG TYPE: " + str(msgtyp))
        ##print("----- MSG Length: " + str(len(msg)))
        ##print("---- MSG ID type: " + str(type(msg_id)) )
        ##print("----- MSG ID: identifiers Type: " + str(type(identifiers)))
#       print("----- MSG ID: identifiers.MsgId_Str Type: " + str(type(identifiers.MsgId_Str)))
        ##print("----- MSG ID: identifiers.Identifiers.MsgId_Str Type: " + str(type(identifiers.Identifiers.MsgId_Str)))
        #print("----- MSG ID: identifiers.Identifiers.MsgId_Str: " + str(identifiers.Identifiers.MsgId_Str.get(0x0010)))
        #hex_id = self.bytes2int(msg_id)
        log.debug("---- MSG ID before hex encode: " + str(msg_id[0]) + " nxt: " + str(msg_id[1]) + " type: " + str(type(msg_id)) + " len: " + str(len(msg_id)))
        hex_id = codecs.encode(msg_id, 'hex')
        log.debug("---- MSG ID hex: " + str(hex_id) )
        #print("---- Identifiers.DOOR_LOCKS: " + str(identifiers.Identifiers.DOOR_LOCKS.value) )
        Id_list = command_resolver.CommandResolver.MsgId_Str_Typ.get(hex_id)
        log.debug("----- Id_list: " + str(Id_list) + " type: " + str(type(Id_list)))
        #log.debug("----- MSG ID: " + str(Id_list[0]))
        #print("----- hex_typ " + str(msgtyp))
        typ_dict_array = Id_list[1]
        #print("----- Type(Typ_list) " + str(type(Typ_list)))
        #print("----- Type Typ_list.get(hex_typ): " + str(type(Typ_list.get(msgtyp))))
        log.debug("----- MSG Type: " + str(typ_dict_array.get(msgtyp)))
        typ_node = typ_dict_array.get(msgtyp)
        log.debug("----- Type List: " + str(typ_node))

        if (typ_node is not None) and (len(typ_node) > 1) is True:
           log.debug("----- Type List 1: " + str(typ_node[1]))
           log.debug("----- Type List 1 type: " + str(type(typ_node[1])))
        #element = typ[1]
        #print("----- element: " + str(element) + ", Type element: " + str(type(element)))
        #element1 = typ[1]()
        #print("----- element1: " + str(element1) + ",Type element1: " + str(type(element1)))
        #lckst = lockstate.LockState()
        #print("lckst :" + str(lckst) + "  ,type: " + str(type(lckst)))
        #self.properties_dump(msg[3:])

    def properties_dump(self, startbytes):
        # For internal usage
        ##print("---- properties_dump: startbytes type:" + str(type(startbytes)) + " len: " + str(len(startbytes)))
        prop_enumeration = property_enumeration.PropertyEnumeration(startbytes)
        while(prop_enumeration.has_more_elements() == True):
            element = prop_enumeration.next_element()
            prop_enumeration.dump_property(element)
            
        return 0

    def component_dump(self, startbytes):
        # For internal usage
        return 0

    def __init__(self):
        #print("PY: Init **** autoapi_dump ***")

        return


