# This file is part of pyRFXtrx, a Python library to communicate with
# the RFXtrx family of devices from http://www.rfxcom.com/
# See https://github.com/woudt/pyRFXtrx for the latest version.
#
# Copyright (C) 2012  Edwin Woudt <edwin@woudt.nl>
#
# pyRFXtrx is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyRFXtrx is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with pyRFXtrx.  See the file COPYING.txt in the distribution.
# If not, see <http://www.gnu.org/licenses/>.

import logging
import sys
sys.path.append("../")

from RFXtrx import PySerialTransport, PyNetworkTransport
from RFXtrx import FanDevice
from time import sleep

logging.basicConfig(level=logging.DEBUG)

transport = PySerialTransport('/dev/cu.usbserial-05VN8GHS')
transport = PyNetworkTransport(('192.168.2.247', 10001))
transport.reset()

transport.send(b'\x0D\x00\x00\x01\x02\x00\x00'
               b'\x00\x00\x00\x00\x00\x00\x00')
event = transport.receive_blocking()
print(event)

#transport.send(b'\x0D\x00\x00\x03\x07\x00\x00'
#               b'\x00\x00\x00\x00\x00\x00\x00')
#event = transport.receive_blocking()
#print(event)

while True:
    event = transport.receive_blocking()
    print(event)
    if hasattr(event, 'device') and isinstance(event.device, FanDevice):
        sleep(5)
        print(f"Sending high command")
        event.device.send_high(transport)

#        transport.close()

