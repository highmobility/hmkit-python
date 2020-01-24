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
import logging
import datetime
import pytz
from . import  access_certificate

log = logging.getLogger('hmkit')

class Storage():
    """
    Class handles access certificate Storage
    """

    def store_access_certificate(self, accesscertf, ser_num):
        """
        <Internal Use> Store access ceritifcate in the database

        :param  bytearray accesscertf: device_access_certificate element present in the downloaded access certificate  
        :rtype: None
        """
        print("\n PY: Storage: store_access_certificate \n")
        signature = self.hmkit.hm_pyc.store_certificate(accesscertf, ser_num)

    def get_access_certificate(self, ser_num):
        """

        :return: accesscertificate
        :rtype: bytearray
        """
        print("\n PY: Storage: get_access_certificate \n")
        access_cert = self.hmkit.hm_pyc.get_certificate(ser_num)
        return access_cert

    def delete_access_certificate(self, ser_num):
        """
        parses the gaining serial number from access certificate

        :return:
        :rtype: 
        """
        print("\n PY: Storage: delete_certificate \n")
        log.debug(str(ser_num))
        ret = self.hmkit.hm_pyc.delete_certificate(ser_num)
        return

    def __init__(self, hmkit):
        print("\n PY: Storage Manager \n")
        self.hmkit = hmkit
