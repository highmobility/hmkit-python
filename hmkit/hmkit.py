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
import time
import os
import subprocess
import threading
import codecs
import base64
import logging
import socket
import sys
from datetime import datetime
from . import ( 
    access_certificate,
    device_certificate,
    storage,
    broadcaster,
    link,
    broadcastlistener,
    linklistener,
    autoapi,
    hm_pyc,
    bluetooth
)
from hmkit.autoapi import autoapi_dump
from hmkit.autoapi.identifiers import Identifiers

#-------- Logging Config ------------
logger = logging.getLogger('hmkit')
# define file handler and set formatter
file_handler = logging.FileHandler('hmlog_{:%Y-%m-%d-%H-%M-%S}.log'.format(datetime.now()))
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(module)s():%(funcName)s:%(lineno)d : %(message)s')
#formatter    = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
file_handler.setFormatter(formatter)
# add file handler to logger
logger.addHandler(file_handler)
log = logger


class HmKit():

    """
    Main class interface to initialize and access High mobility Python sdk hmkit

    """

    __instance = None

    @staticmethod 
    def get_instance():
        """
        get the HmKit instance

        :rtype: :class:`HmKit`. returns None if not created already.
        """
        return HmKit.__instance

    def set_logging_level(self, loglevel=logging.INFO):
        """
        set logging level for logger

        :param logging loglevel:  python logging level for hmkit logs. logging.DEBUG, 
            logging.INFO, logging.WARNING ,logging.ERROR, logging.CRITICAL
        :rtype: None
        """
        logger.setLevel(loglevel)

    def cmain_thread(self):
        """
        thread function dedicated to c thread operations

        """
        log.debug("PY: cmain_thread")
        ret = hm_pyc.cmain_thread()

    def hmkit_exit(self):
        """
        terminate hmkit. this terminates the cthreads

        """
        log.info("PY: ****** cthread_exit") 
        hm_pyc.cthread_exit()
        time.sleep(1)
        log.info("PY: return** cthread_exit") 

    def init_threads(self):
        """
        create a python thread. which will be deligated for c

        """
        ##log.debug("Entered init_threads")

        thread = threading.Thread(target=self.cmain_thread)
        thread.start()
        time.sleep(3)

    def certificate_update(self, snippet):
        """
        Parses and updates the certificate to  :class:`device_certificate` and  :class:`hm_pyc`

        :param bytearray snippet: device certificate snippet
        :rtype: None
        """
        devCerts_snippet = []
        devCerts_decoded = []

        devCerts_snippet = snippet
        ##log.debug("PY: type of dev certs:" + str(type(devCerts_snippet)))
        ##log.debug("DevCert: " + str(devCerts_snippet[0]))
        ##log.debug("DevPrv: " + str(devCerts_snippet[1]))
        ##log.debug("IssPub: " + str(devCerts_snippet[2]))

        devCerts_decoded.append(base64.b64decode(devCerts_snippet[0]))
        devCerts_decoded.append(base64.b64decode(devCerts_snippet[1]))
        devCerts_decoded.append(base64.b64decode(devCerts_snippet[2]))

        #------- Dev Cert ------
        ##log.debug("DevCert decoded, len: " + str(len(devCerts_decoded[0])) + " type: " + str(type(devCerts_decoded[0])) + " Array:  " + str(devCerts_decoded[0]))

        list_devCerts_decoded = list(devCerts_decoded[0])
        bytes_devCerts_decoded = bytes(list_devCerts_decoded)
        #log.debug("DevCert decoded List, len: " + str(len(list_devCerts_decoded)) + " type: " + str(type(list_devCerts_decoded)) + " Array:  " + str(list_devCerts_decoded))
        #log.debug("DevCert decoded Bytes, len: " + str(len(bytes_devCerts_decoded)) + " type: " + str(type(bytes_devCerts_decoded)) + " Array: " + str(bytes_devCerts_decoded))

        #-------- Prv -------
        #log.debug("Prv decoded, len: " + str(len(devCerts_decoded[1])) + " type: " + str(type(devCerts_decoded[1])) + " Array:  " + str(devCerts_decoded[1]))

        list_prv_decoded = list(devCerts_decoded[1])
        bytes_prv_decoded = bytes(list_prv_decoded)
        #log.debug("DevCert decoded List, len: " + str(len(list_prv_decoded)) + " type: " + str(type(list_prv_decoded)) + " Array: " + str(list_prv_decoded))
        #log.debug("Prv decoded Bytes, len: " + str(len(bytes_prv_decoded)) + " type: " + str(type(bytes_prv_decoded)) + " Array: " + str(bytes_prv_decoded))

        #---------- Pub -------
        #log.debug("Prv decoded, len: " + str(len(devCerts_decoded[2])) + " type: " + str(type(devCerts_decoded[2])) + " Array: " + str(devCerts_decoded[2]))

        list_pub_decoded = list(devCerts_decoded[2])
        bytes_pub_decoded = bytes(list_pub_decoded)
        #log.debug("Pub decoded List, len: " + str(len(list_pub_decoded)) + " type: " + str(type(list_pub_decoded)) + " Array: " + str(list_pub_decoded))
        #log.debug("Pub decoded Bytes, len: " + str(len(bytes_pub_decoded)) + " type: " + str(type(bytes_pub_decoded)) + " Array: " + str(bytes_pub_decoded))
        #print("DevPrv decoded, len: ",len(devCerts_decoded[1]) ," Array:  ", devCerts_decoded[1])
        h_string2 = codecs.encode(devCerts_decoded[1], 'hex')
        #print("Hex, len: ", len(h_string2), " Value: ", h_string2)

        #print("IssPub decoded, len: ",len(devCerts_decoded[2]) ," Array:  ", devCerts_decoded[2])
        h_string3 = codecs.encode(devCerts_decoded[2], 'hex')
        #print("Hex, len: ", len(h_string3), " Value: ", h_string3)

        self.device_certificate.update_devcertf(bytes_devCerts_decoded)

        ret = hm_pyc.set_certs(bytes_devCerts_decoded, bytes_prv_decoded, bytes_pub_decoded)

    def download_access_certificate(self, token):
        """
        Pass the Access token to :class:`access_certificate` to download Access Certificate

        :param bytearray token: Access Token for device
        :rtype: None
        """
        self.access_certificate.download_access_certificate(token)
        self.storage.store_access_certificate(self.access_certificate.get_raw_certiticate(), self.access_certificate.get_gaining_serial_number())

        ######## for Testing
        ac = self.storage.get_access_certificate(self.access_certificate.get_gaining_serial_number())
        #print("Received AC from Storage: " + str(ac))

        #ret = self.storage.delete_access_certificate(self.access_certificate.get_gaining_serial_number())
        #print("Deleted AC from Storage: ")
        ########

    def get_certificate(self, serial):
        """
        returns the Access Certificate

        :param bytearray serial: Serial Number
        :returns: AccessCertificate() object that contains the received Access certificate
        :rtype: access_certificate.AccessCertificate()
        """
        #print("HMKT: " + "get_certificate()")
        # TODO: get it from storage based on the serial number
        return self.access_certificate

    #-------------------------------------------------
    #--------------------- Init ----------------------
    #-------------------------------------------------

    def __init__(self, snippet, loglevel=logging.INFO):
        """
        Main :class: HmKit _init_ to initialize and access High mobility Python sdk hmkit

        :param bytearray snippet: Device certificate snippet downloaded from developer centre
        :param logging loglevel: python logging level for hmkit logs. logging.DEBUG, logging.INFO, logging.WARNING ,logging.ERROR, logging.CRITICAL
        :rtype: None
        """
        global listener
        ##print("PY: Init Function of HmKit")

        logger.setLevel(loglevel)

        # Virtually private constructor
        if HmKit.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            HmKit.__instance = self

        # access certificate and device certificate class objects
        self.access_certificate = access_certificate.AccessCertificate(self)
        self.device_certificate = device_certificate.DeviceCertificate(self)

        self.storage = storage.Storage(self)

        # update the received certificate snippet
        self.certificate_update(snippet)

        # Initialize Pyhton threads
        self.init_threads()

        # set python c interface module
        self.hm_pyc = hm_pyc
        # set bluetooth interface module
        self.bluetooth = bluetooth.Bluetooth(self.hm_pyc)
        # set autoapidump module
        self.autoapi_dump = autoapi_dump()

