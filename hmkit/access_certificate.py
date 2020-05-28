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
import  requests
import  json
import codecs
#from . import  access_certificate
from . import  storage
import logging
import datetime
import pytz
from hmkit.autoapi.properties.permissions import Permissions

log = logging.getLogger('hmkit')

class AccessCertificate():
    """
    Class handles access certificate download, parsing and get apis.
    """

    url = "https://sandbox.api.staging.high-mobility.net/v1/" # Staging
    #url = "https://sandbox.api.high-mobility.com/v1/" # Prod
    #url = "https://sandbox.api.develop.high-mobility.net/v1/" # Dev
    # Hack for testing with local emulator
    #url = "http://localhost:4443/hm_cloud/api/v1/"
    # Positions of different Fields in Device Certificate
    VERSION_POS = 0
    ISSUER_START = 1
    ISSUER_END = 4
    SER_PROVIDING_START = 5
    SER_PROVIDING_END = 13
    SER_GAINING_START = 14
    SER_GAINING_END = 22
    GAINING_PUBLIC_KEY_START = 23
    GAINING_PUBLIC_KEY_END = 86
    VALIDITY_START_DATE_START = 87
    VALIDITY_START_DATE_END = 91
    VALIDITY_END_DATE_START = 92
    VALIDITY_END_DATE_END = 96
    PERMISSION_SIZE_POS = 97
    PERMISSIONS_START = 98 # end decided by permissions length

    SIGNATURE_SIZE = 64

    def download_access_certificate(self, access_token):
        """
        Downloads access ceritifcate from the hmserver with the access token passed.

        :param  bytearray access_token: access token copied from high-mobility 
        :rtype: None
        """
        ##print("toke type " + str(type(access_token)))
        ac_url = self.url + "access_certificates"
        serial = self.hmkit.device_certificate.get_devSerialNum()
        # hy_pyc returns tuple
        signature = self.hmkit.hm_pyc.generate_signature(access_token)
        log.debug("sign type: " + str(type(signature[0])) + " length: " + str(len(signature[0])))
        log.debug("signature: " + str(signature[0]))
        signatureb64 = base64.b64encode(bytes(signature[0]))
        log.debug("sign base64 : " + str(signatureb64))
        log.debug("SerialNum : " + str(serial))
	## SerialNumber formating: bytes -> hex -> decode(utf-8) -> str -> upper
        serialtmp = codecs.encode(serial, 'hex')
        log.debug(" Paylod Types; serial: " + str(type(serialtmp)) + ", access_token: " + str(type(access_token)) + ", signature: " + str(type(signatureb64)))
        # signature of access token in base64 format
        payload  =  {'access_token' :  access_token.decode("utf-8"), 'serial_number' :  str(serialtmp.decode("utf-8")).upper(),  'signature' :  signatureb64.decode("utf-8") }

	#========== Works =============#
        log.debug("Payload: " + str(payload))
        ##log.debug("Payload: type: " + str(type(payload)))
        ##log.debug("Url: " + str(ac_url))
        # Download the Access certificate HTTP Post
        try:
            resp  =  requests.post(ac_url,  json=payload)
        except requests.exceptions.RequestException as e:
            # handle all the errors here
            log.critical("Access Certificate Download Error : " + str(e))
            print("Access Certificate Download Error : " + str(e))
            #raise

        #resp = {"vehicle_access_certificate": null, "device_access_certificate": "AXRtY3OGLI/H0qzNcbMa1OgKyECxUPYmjM3Ze3HwiV2x+CEsvpsYFJJs1XJ53Wab5yt0pDFCNYJ/+Yvpi3rIP3Lus7ZzBoEtFffOwsnnrcUDTEilGOW5EwoZCS4YChkJLhAQB//9/+//////HwAAAAAArLUfT3Wf0vea9xIzcGUERg5Trne/vXGW4Z4JJ8mUfSDRPGLSTdQq9nKZmr+ZGBKsphCW+PXWDZSP7UsLDFcYFQ=="}

	##log.debug("*** Received AC: type: " + str(type(resp)))
        ##log.debug(" *** Received AC: " + resp.text)
        log.debug(" resp: " + json.dumps(resp.json()))
        resp_data = resp.json()

        #if "errors" in resp_data:
        #    print(" errors in received response" + str(resp_data))
        #    log.error("Error in received response: " + str(resp_data))
        #    raise AttributeError(str(resp_data))

        dev_access_cert_raw = resp_data['device_access_certificate']
        ##log.debug("resp device_access_certificate : " + resp_data['device_access_certificate'])
        ##log.debug("device_access_certificate : " + dev_access_cert + ",  type: " + str(type(dev_access_cert)))

        ## Hack for testing with local emulator
        #dev_access_cert = "AXRtY3MX9XdGSNG2BFitipieMJEce0nBWf7CGlohR61K7yxUx1+cp8xVVDulzeferOdypO92YkdYpu508Xbd9MeymtZG5rs+ZJeASjvHv/jmHGkID54HEwIHDSkYAgcNKRAQB//9/+//////HwAAAAAArASACR9QMyxxasiJeTp5ZZUgA2417W6uId9UbIoNqokxYkRgzGUfpWOHOzDmZlPbA7KiMYmAvOJkN8/Jbn3M8Q=="
        #dev_access_cert_raw = "AXRtY3OGLI/H0qzNcbMa1OgKyECxUPYmjM3Ze3HwiV2x+CEsvpsYFJJs1XJ53Wab5yt0pDFCNYJ/+Yvpi3rIP3Lus7ZzBoEtFffOwsnnrcUDTEilGOW5EwoZCS4YChkJLhAQB//9/+//////HwAAAAAArLUfT3Wf0vea9xIzcGUERg5Trne/vXGW4Z4JJ8mUfSDRPGLSTdQq9nKZmr+ZGBKsphCW+PXWDZSP7UsLDFcYFQ=="

        self.accesscert = base64.b64decode(dev_access_cert_raw)
        ##log.debug("*** Decoded AC: " + str(self.accesscert) + ",  type: " + str(type(self.accesscert)) )
        accesscert_dec_hex = codecs.encode(self.accesscert, 'hex')
        ##log.debug("accesscert_dec_hex : " + str(accesscert_dec_hex))
        ##log.debug("*** Received AC: " + str(accesscertf_b64))

        self.parse_decoded_certiticate(self.accesscert)

        return


    def print_access_certificate(self, accesscertf):

        log.debug("AC gaining_serial: " + str(self.gaining_serial))
        log.debug("AC providing_serial: " + str(self.providing_serial))
        log.debug("AC version: " +  str(self.version))
        log.debug("AC issuer_name: " + str(self.issuer_name))
        log.debug("AC pubkey: " + str(self.pubkey))
        log.debug("AC startdatetime: " + str(self.startdatetime))
        log.debug("AC enddatetime: " + str(self.enddatetime))
        log.debug("AC permissions_len: " + str(self.permissions_len))
        log.debug("AC permissions: " + str(self.permissions))
        log.debug("AC signature: " + str(self.signature))

    def parse_decoded_certiticate(self, cert):
        # cert - base64 decoded

        self.version = cert[AccessCertificate.VERSION_POS]
        self.issuer_name =  cert[AccessCertificate.ISSUER_START : AccessCertificate.ISSUER_END+1]
        self.providing_serial = cert[AccessCertificate.SER_PROVIDING_START:AccessCertificate.SER_PROVIDING_END+1]
        self.gaining_serial = cert[AccessCertificate.SER_GAINING_START:AccessCertificate.SER_GAINING_END+1]
        self.pubkey =  cert[AccessCertificate.GAINING_PUBLIC_KEY_START:AccessCertificate.GAINING_PUBLIC_KEY_END+1]

        start_year =  cert[AccessCertificate.VALIDITY_START_DATE_START] + 2000
        start_month = cert[AccessCertificate.VALIDITY_START_DATE_START+1]
        start_day =  cert[AccessCertificate.VALIDITY_START_DATE_START+2]
        start_hour =  cert[AccessCertificate.VALIDITY_START_DATE_START+3]
        start_min =  cert[AccessCertificate.VALIDITY_START_DATE_START+4]

        #print("AC start_year: ", start_year, "start_month: ", start_month, "start_day ", start_day
        #, "start_hour ", start_hour, "start_min: ", start_min)

        # datetime(year, month, day, hour, minute, second, microsecond)
        self.startdatetime = datetime.datetime(start_year, start_month, start_day, start_hour, start_min, 0, 0,tzinfo=pytz.UTC)

        end_year =  cert[AccessCertificate.VALIDITY_END_DATE_START] + 2000
        end_month =  cert[AccessCertificate.VALIDITY_END_DATE_START+1]
        end_day = cert[AccessCertificate.VALIDITY_END_DATE_START+2]
        end_hour = cert[AccessCertificate.VALIDITY_END_DATE_START+3]
        end_min = cert[AccessCertificate.VALIDITY_END_DATE_START+4]
        self.enddatetime = datetime.datetime(end_year, end_month, end_day, end_hour, end_min, 0, 0, tzinfo=pytz.UTC)

        self.permissions_len = cert[AccessCertificate.PERMISSION_SIZE_POS]
        self.permissions_bytes = cert[AccessCertificate.PERMISSIONS_START : AccessCertificate.PERMISSIONS_START + self.permissions_len]

        #print("AC permissions_len: ", self.permissions_len, " Permissions: ", self.permissions_bytes)

        self.signature =  cert[AccessCertificate.PERMISSIONS_START + self.permissions_len : AccessCertificate.PERMISSIONS_START + self.permissions_len + AccessCertificate.SIGNATURE_SIZE]
        self.permissions = Permissions(self.permissions_bytes)

        #self.store_access_certificate(self.accesscert)

        self.print_access_certificate(cert)

    def get_raw_certiticate(self):
        """
        get the parsed and base64 decoded certificate

        :return: raw access certificate
        :rtype: bytearray
        """
        return self.accesscert

    def get_gaining_serial_number(self):
        """
        parses the gaining serial number from access certificate

        :return: serial number
        :rtype: bytearray
        """
        ##log.debug(str(self.gaining_serial))
        ##log.debug(str(len(self.gaining_serial)))
        return self.gaining_serial

    def get_providing_serial_number(self):
        """
        parses the providing serial number from access certificate

        :return: serial number
        :rtype: bytearray
        """
        ##log.debug(str(self.providing_serial))
        ##log.debug(str(len(self.providing_serial)))
        return self.providing_serial

    def get_version(self):
        """
        returns the certificate version from access certificate

        :return: certificate version number
        :rtype: integer
        """
        return self.version

    def get_issuer(self):
        """
        returns the Certificate Issuer name from access certificate

        :return: Certificate Issuer name 4 bytes
        :rtype: bytearray
        """
        return self.issuer_name

    def get_vehicle_pubkey(self):
        """
        returns the vehicle public key from access certificate

        :return: vehicle public key
        :rtype: bytearray
        """
        return self.pubkey;

    def get_start_date(self):
        """
        returns the start date of the access certificate

        :return: startdate
        :rtype: datetime.datetime
        """
        ##log.debug(str(self.startdatetime))
        return self.startdatetime

    def get_end_date(self):
        """
        returns the end date of the access certificate

        :return: enddate
        :rtype: datetime.datetime
        """
        ##log.debug(str(self.enddatetime))
        return self.enddatetime

    def is_expired(self):
        """
        Checks and returns expiry of the access certificate

        :return: Certificate date expiry status
        :rtype: True/False
        """

        now_datetime_utc = datetime.datetime.utcnow()
        # make it offset aware
        now_datetime_utc_aware = pytz.utc.localize(now_datetime_utc)

        time_delta = now_datetime_utc_aware - self.enddatetime
        if time_delta.total_seconds() > 1:
            log.debug("is_expired(): False")
            return False
        else:
            log.debug("is_expired(): True")
            return True

    def is_not_valid_yet(self):
        """
        Checks validity start of the access certificate. Raspberry device must be set with correct time.

        :return: bool indicates if the certificate is not valid yet, but will be in the future.
        :rtype: True/False
        """

        now_datetime_utc = datetime.datetime.utcnow()
        # make it offset aware
        now_datetime_utc_aware = pytz.utc.localize(now_datetime_utc)

        time_delta = now_datetime_utc_aware - self.startdatetime
        if time_delta.total_seconds() > 1:
            log.debug("is_not_valid_yet(): True")
            return True
        else:
            log.debug("is_not_valid_yet(): False")
            return False

    def get_permissions(self):
        """
        returns permissions from access certificate

        :return: capability permissions
        :rtype: hmkit.autoapi.properties.permissions.Permissions
        """
        return self.permissions;

    def __init__(self, hmkit, cert=None):
        ##print("\n PY: access_certificates_manager \n")
        self.hmkit = hmkit
        if cert is not None:
            self.accesscert = cert
            self.parse_decoded_certiticate(self.accesscert)
