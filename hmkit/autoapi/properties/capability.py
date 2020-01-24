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
from . import propertyvalue_object
from ..msg_type import MsgType
from ..identifiers import Identifiers
import codecs
import logging

log = logging.getLogger('hmkit.autoapi')

class Capability(propertyvalue_object.PropertyValueObject):
    """
    Capability property which includes identifier and supported msg types(int)
    """

    def __init__(self, comp_valuebytes):
        """
        Property bytes will be parsed to get internal data values

        :param bytearray propbytes: Property Component Bytes
        """
        self.prop_ids = []
        log.debug("Capability property " + " bytes Len:" + str(len(comp_valuebytes)) + " bytes: " + str(comp_valuebytes))
        #print("Capability property " + " bytes Len:" + str(len(comp_valuebytes)) + " bytes: " + str(comp_valuebytes))

        super().__init__(comp_valuebytes)

        msg_id_bytes = comp_valuebytes[:2]
 
        msg_id = codecs.encode(msg_id_bytes, 'hex') # considers the input as hex (two digits per byte) and convert to bytes

       # print("Capability: msg_id: " + str(msg_id) + " len: " + str(len(msg_id)) + " type: " + str(type(msg_id)))

        self.identifier = Identifiers(msg_id)
        prop_ids_size_bytes = comp_valuebytes[2:4]
        prop_ids_size = int.from_bytes(prop_ids_size_bytes, byteorder='big', signed=False)
        prop_ids_bytes = comp_valuebytes[4:4+prop_ids_size]

        for prop_id in prop_ids_bytes:
            self.prop_ids.append(prop_id)

        log.debug("Capability  property " + "identifier: " + str(self.identifier) + " , prop_ids[]: " + str(self.prop_ids))

        return

    def get_property_ids(self):
        """
        returns Property IDs included in this Capability

        :return: Types
        :rtype: list of Property IDs
        """
        return self.prop_ids

    def get_identifier(self):
        """
        returns the Identifier this Capability belongs to

        :return: Identifiers
        :rtype: identifiers.Identifiers
        """
        return self.identifier

    def is_supported(self, prop_id):
        """
        returns whether the message type in supported in this capability

        :param  int prop_id:
        :return: True / False
        :rtype: bool
        """
        #print("capability: is_supported() , prop_id val: " + str(prop_id) )
        #print("capability: is_supported() identifier " + str(self.get_identifier()) )

        for property_id in self.prop_ids:
            #print("capability: is_supported() loop: prop_id " + str(prop_id))
            if prop_id == property_id:
                return True

        return False
