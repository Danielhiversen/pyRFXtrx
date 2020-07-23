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

import sys
import logging
sys.path.append("../")

import RFXtrx
import time

def print_callback(event):
    print(event)

def main():
    logging.basicConfig(level=logging.DEBUG)

    if len(sys.argv) >= 2:
        rfxcom_device = sys.argv[1]
    else:
        rfxcom_device = '/dev/serial/by-id/usb-RFXCOM_RFXtrx433_A1Y0NJGR-if00-port0'

    modes_list = sys.argv[2].split() if len(sys.argv) > 2 else None
    print ("modes: ", modes_list)
    core = RFXtrx.Core(rfxcom_device, print_callback, modes=modes_list)

    print (core)
    while True:
        print(core.sensors())
        time.sleep(2)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass