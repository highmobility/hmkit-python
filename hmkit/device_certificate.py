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
import base64
import logging

log = logging.getLogger('hmkit')

class DeviceCertificate():
    """
    Class handles device certificate parsing and provides getters for various parameters
    """

    # Positions of different Fields in Device Certificate
    ISSUER_START = 0
    ISSUER_END = 3
    APPID_START = 4
    APPID_END = 15
    SER_START = 16
    SER_END = 25
    PUBKEY_START = 25
    PUBKEY_END = 88
    SIGN_START = 89
    SIGN_END = 152

    devCertf = bytearray()

    def update_devcertf(self, devcert):
        """
        Takes the decoded device certificate and parses it.

        :param  bytearray devcert: decoded device certificate from the copied snippet from high-mobility server
        :rtype: None
        """
        ##log.debug("** type: " + str(type(devcert))) 
        self.devCertf = devcert
        ##log.debug(str(self.devCertf))
        # return

    def get_devSerialNum(self):
        """
        parses the device serial number from device certificate

        :return: serial number
        :rtype: bytearray
        """
        serial = bytes(self.devCertf[DeviceCertificate.SER_START:DeviceCertificate.SER_END])
        ##log.debug(str(serial) + ", type: " + str(type(serial)))
        return serial;

    def get_issuer_pubkey(self):
        """
        parses the issuer public key from device certificate

        :return: issuer public key
        :rtype: bytearray
        """
        #issuerpubkey = base64.b64decode(self.devCertf[ISSUER_START:ISSUER_END])
        issuerpubkey = self.devCertf[DeviceCertificate.ISSUER_START:DeviceCertificate.ISSUER_END]
        ##log.debug(str(issuerpubkey))
        return issuerpubkey;

    def get_app_identifier(self):
        """
        parses the appllication id from device certificate

        :return: application id
        :rtype: bytearray
        """

        # TODO
        return;

    def __init__(self, hmkit):
        #log.debug(" ")
        pass

