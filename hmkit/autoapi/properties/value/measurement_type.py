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

from enum import Enum, unique
import logging

log = logging.getLogger('hmkit.autoapi')

@unique
class MeasurementType(Enum):
    """
    Enum Class for Measurement Types to represent Data Component Values
    """
    ACCELERATION = 0x01
    ANGLE = 0x02
    ANGULAR_VELOCITY = 0x03
    DURATION = 0x07
    ELECTRIC_CURRENT = 0x09
    ELECTRIC_POTENTIAL_DIFFERENCE = 0x0a
    ENERGY = 0x0c
    ENERGY_EFFICIENCY = 0x0d
    FREQUENCY = 0x0e
    FUEL_EFFICIENCY = 0x0f
    ILLUMINANCE = 0x11
    LENGTH = 0x12
    POWER = 0x14
    PRESSURE = 0x15
    SPEED = 0x16
    TEMPERATURE = 0x17
    TORQUE = 0x18
    VOLUME = 0x19

