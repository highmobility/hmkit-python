import  base64
import  json
import  codecs
from .. import identifiers
from .. import msg_type, property_enumeration, command_with_properties
import hmkit.autoapi
from hmkit.autoapi.identifiers import Identifiers
import hmkit.autoapi.msg_type
from ..properties import hmproperty

import logging

log = logging.getLogger('hmkit.autoapi')

class GetCapability(command_with_properties.CommandWithProperties):
    """
    Constructs Get Capability message
    """
    getcapability_prop_id = 0x01

    def __init__(self, identifier):
        """
        Constructs Get Capability message

        :param identifier: hmkit.autoapi.identifiers.Identifiers
        """
        log.debug(" ")
        self.msg_type = msg_type.MsgType(Identifiers.CAPABILITIES,0x02)
        super().__init__(None, self.msg_type)

        if identifier is not None:
            print("GetCapability() identifier.value: " + str(identifier.value))

            identifier_bytes = identifier.value

            #print("GetCapability() id bytes: " + str(identifier_bytes))
            self.getcap = hmproperty.HmProperty(None, GetCapability.getcapability_prop_id, identifier_bytes, None, None)

        super().create_bytes(self.getcap)

        return
