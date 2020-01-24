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

from datetime import datetime
import struct
from .property_component import PropertyComponent
import logging

log = logging.getLogger('hmkit.autoapi')

class PropertyComponentTimestamp(PropertyComponent):
    """
    For internal usage of SDK
    """
    def __init__(self, compbytes  = bytearray(), datetimeutc  = None):

        if compbytes is not None:
            # Parsing case
            log.debug("Parsing ")
            super().__init__(compbytes)
            # Timestamp since UTC in millisecs
            self.timestamp_bytes = super().getpayload_bytes()
            self.datetime_utc = self.get_datetime()
        else: # Construction case
            log.debug("Construction ")
            self.datetime_utc = datetimeutc
            try:
                timestamp_ms_utc = datetime.timestamp(self.datetime_utc) * 1000

            except OverflowError as e:
                log.exception("Exception: ", e.data)

            self.timestamp_bytes = bytearray(timestamp_ms_utc)
            #timestamp = value.replace(tzinfo=timezone.utc).timestamp()
        return

    def getvalue_bytes(self):
        """
        returns the component payload(timestamp) bytes

        """
        return self.timestamp_bytes

    def get_timestamp_integer(self):
        """
        returns timestamp miliseconds as integer

        """
        timestamp_ms = int.from_bytes(self.timestamp_bytes, byteorder='big', signed=False)
        #ts = struct.unpack("Q", bytes(self.timestamp_bytes))
        log.debug( str(timestamp_ms))
        return timestamp_ms

    def get_datetime(self):
        """
        returns datetime.datetime object

        """
        try:
            # param: convert the integer timestamp to secs
            datetimeutc = datetime.utcfromtimestamp(self.get_timestamp_integer()/1000)

        except (OverflowError, OSError)  as e:
            log.exception("Exception: ", e.data)
        else:
            log.debug("get_datetime(): " + datetimeutc.strftime('%Y-%m-%d %H:%M:%S.%f'))
            log.debug("year: " + str(datetimeutc.year))
            log.debug("month: " + str(datetimeutc.month))
            log.debug("day: " + str(datetimeutc.day))
            log.debug("hour: " + str(datetimeutc.hour))
            log.debug("min: " + str(datetimeutc.minute))
            log.debug("sec: " + str(datetimeutc.second))
            log.debug("ms: " + str(datetimeutc.microsecond/1000))

        return datetimeutc
