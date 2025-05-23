# This file is part of pyRFXtrx, a Python library to communicate with
# the RFXtrx family of devices from http://www.rfxcom.com/
# See https://github.com/Danielhiversen/pyRFXtrx for the latest version.
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
"""
This module provides the base implementation for pyRFXtrx
"""
# pylint: disable=R0903, invalid-name
# pylint: disable= too-many-lines

import functools
import glob
import socket
import threading
import logging
from contextlib import suppress

from time import sleep

import serial

from . import lowlevel

_LOGGER = logging.getLogger(__name__)


###############################################################################
# RFXtrxDevice class
###############################################################################

class RFXtrxDevice:
    """ Superclass for all devices """

    def __init__(self, pkt):
        self.packettype = pkt.packettype
        self.subtype = pkt.subtype
        self.type_string = pkt.type_string
        self.id_string = pkt.id_string
        self.known_to_be_dimmable = False
        self.known_to_be_rollershutter = False

    def __eq__(self, other):
        if self.packettype != other.packettype:
            return False
        if self.subtype != other.subtype:
            return False
        return self.id_string == other.id_string

    def __str__(self):
        return "{0} type='{1}' id='{2}'".format(
            type(self), self.type_string, self.id_string)


###############################################################################
# SwitchDevice class
###############################################################################

class RollerTrolDevice(RFXtrxDevice):
    """ Concrete class for a roller device """
    def __init__(self, pkt):
        super().__init__(pkt)
        if isinstance(pkt, lowlevel.RollerTrol):
            self.known_to_be_rollershutter = True
            self.id_combined = pkt.id_combined
            self.unitcode = pkt.unitcode
            self.cmndseqnbr = 0
            self.COMMANDS = lowlevel.RollerTrol.COMMANDS

    def send_command(self, transport, command):
        """ Send a command using the given transport """
        pkt = lowlevel.RollerTrol()
        pkt.set_transmit(
            self.subtype,
            self.cmndseqnbr,
            self.id_combined,
            self.unitcode,
            command
        )
        self.cmndseqnbr = (self.cmndseqnbr + 1) % 5
        transport.send(pkt.data)

    def send_close(self, transport):
        """ Send a 'Close' command using the given transport """
        self.send_command(transport, 0x01)

    def send_open(self, transport):
        """ Send an 'Open' command using the given transport """
        self.send_command(transport, 0x00)

    def send_stop(self, transport):
        """ Send a 'Stop' command using the given transport """
        self.send_command(transport, 0x02)


class DDxxxxDevice(RFXtrxDevice):
    """ Concrete class for a DDxxxx device """
    def __init__(self, pkt):
        super().__init__(pkt)
        if isinstance(pkt, lowlevel.DDxxxx):
            self.known_to_be_rollershutter = True
            self.id_combined = pkt.id_combined
            self.unitcode = pkt.unitcode
            self.cmndseqnbr = 0
            self.COMMANDS = lowlevel.DDxxxx.COMMANDS

    def send_command(
            self,
            transport,
            command,
            percent: int = 0,
            angle: int = 0):
        """ Send a command using the given transport """
        pkt = lowlevel.DDxxxx()
        pkt.set_transmit(
            self.subtype,
            self.cmndseqnbr,
            self.id_combined,
            self.unitcode,
            command,
            percent,
            angle
        )
        self.cmndseqnbr = (self.cmndseqnbr + 1) % 5
        transport.send(pkt.data)

    def send_up(self, transport):
        """ Send an 'Open' command using the given transport """
        self.send_command(transport, lowlevel.DDxxxx.CMD_UP)

    def send_down(self, transport):
        """ Send a 'Close' command using the given transport """
        self.send_command(transport, lowlevel.DDxxxx.CMD_DOWN)

    def send_stop(self, transport):
        """ Send a 'Stop' command using the given transport """
        self.send_command(transport, lowlevel.DDxxxx.CMD_STOP)

    def send_p2(self, transport):
        """ Send a 'P2' command using the given transport """
        self.send_command(transport, lowlevel.DDxxxx.CMD_P2)

    def send_percent(self, transport, percent: int):
        """ Send a 'Percent' command using the given transport """
        self.send_command(
            transport,
            lowlevel.DDxxxx.CMD_PERCENT,
            percent=percent
        )

    def send_angle(self, transport, angle: int):
        """ Send a 'Angle' command using the given transport """
        self.send_command(transport, lowlevel.DDxxxx.CMD_ANGLE, angle=angle)

    def send_percent_angle(self, transport, percent: int, angle: int):
        """ Send a 'Angle' command using the given transport """
        self.send_command(
            transport,
            lowlevel.DDxxxx.CMD_PERCENT_ANGLE,
            percent=percent,
            angle=angle
        )


class RfyDevice(RFXtrxDevice):
    """ Concrete class for a roller device """
    def __init__(self, pkt):
        super().__init__(pkt)
        if isinstance(pkt, lowlevel.Rfy):
            self.known_to_be_rollershutter = True
            self.id_combined = pkt.id_combined
            self.unitcode = pkt.unitcode
            self.cmndseqnbr = 0
            self.COMMANDS = lowlevel.Rfy.COMMANDS

    def send_command(self, transport, command):
        """ Send a command using the given transport """
        pkt = lowlevel.Rfy()
        pkt.set_transmit(
            self.subtype,
            self.cmndseqnbr,
            self.id_combined,
            self.unitcode,
            command
        )
        self.cmndseqnbr = (self.cmndseqnbr + 1) % 5
        transport.send(pkt.data)

    def send_close(self, transport):
        """ Send a 'Close' command using the given transport """
        self.send_command(transport, 0x03)

    def send_open(self, transport):
        """ Send an 'Open' command using the given transport """
        self.send_command(transport, 0x01)

    def send_stop(self, transport):
        """ Send a 'Stop' command using the given transport """
        self.send_command(transport, 0x00)

    def send_on(self, transport):
        """ Send an 'Enable Sun Automation' command """
        self.send_command(transport, 0x13)

    def send_off(self, transport):
        """ Send an 'Disable Sun Automation' command """
        self.send_command(transport, 0x14)

    def send_up05sec(self, transport):
        """ Send a '0.5 Seconds Up' command """
        self.send_command(transport, 0x0F)

    def send_down05sec(self, transport):
        """ Send a '0.5 Seconds Down' command """
        self.send_command(transport, 0x10)

    def send_up2sec(self, transport):
        """ Send a '2 Seconds Up' command """
        self.send_command(transport, 0x11)

    def send_down2sec(self, transport):
        """ Send a '2 Seconds Down' command """
        self.send_command(transport, 0x12)


class FunkDevice(RFXtrxDevice):
    """ Concrete class for a control device """

    def __init__(self, pkt):
        super().__init__(pkt)
        if isinstance(pkt, lowlevel.Funkbus):
            self.id_combined = pkt.id_combined
            self.groupcode = pkt.groupcode
            self.target = pkt.target
            self.COMMANDS = lowlevel.Funkbus.COMMANDS

    def send_command(self, transport, command, param, duration):
        """ Send a command using the given transport """
        pkt = lowlevel.Funkbus()
        pkt.set_transmit(self.subtype,
                         0,
                         self.id_combined,
                         self.groupcode,
                         param if command in [0x00, 0x01, 0x04] else 0x00,
                         command,
                         duration)
        transport.send(pkt.data)

    def send_onoff(self, transport, turn_on):
        """ Send on 'On' or 'Off' command using the given transport """
        self.send_command(transport,
                          0x01 if turn_on else 0x00,
                          self.target,
                          0x00)

    def send_on(self, transport):
        """ Send an 'On' command using the given transport """
        self.send_onoff(transport, True)

    def send_off(self, transport):
        """ Send an 'Off' command using the given transport """
        self.send_onoff(transport, False)

    def send_dim(self, transport, duration):
        """ Send a 'Dim' command using the given transport """
        self.send_command(transport,
                          0x00,
                          self.target,
                          duration + 1)

    def send_bright(self, transport, duration):
        """ Send a 'Bright' command using the given transport """
        self.send_command(transport,
                          0x01,
                          self.target,
                          duration + 1)

    def send_alloff(self, transport):
        """ Send an 'All OFF' command using the given transport """
        self.send_command(transport,
                          0x02,
                          0x00,
                          0x03)

    def send_allon(self, transport):
        """ Send a 'All ON' command using the given transport """
        self.send_command(transport,
                          0x03,
                          0x00,
                          0x03)

    def send_setscene(self, transport, scene):
        """ Send a 'Scene' command using the given transport """
        self.send_command(transport,
                          0x04,
                          scene,
                          0x01)

    def send_masterdim(self, transport, duration):
        """ Send a 'Master Dim' command using the given transport """
        self.send_command(transport,
                          0x05,
                          0x00,
                          duration + 1)

    def send_masterbright(self, transport, duration):
        """ Send a 'Bright' command using the given transport """
        self.send_command(transport,
                          0x06,
                          0x00,
                          duration + 1)


class LightingDevice(RFXtrxDevice):
    """ Concrete class for a control device """

    # pylint: disable=too-many-instance-attributes
    def __init__(self, pkt):
        super().__init__(pkt)
        if isinstance(pkt, lowlevel.Lighting1):
            self.housecode = pkt.housecode
            self.unitcode = pkt.unitcode
            self.COMMANDS = lowlevel.Lighting1.COMMANDS
        if isinstance(pkt, lowlevel.Lighting2):
            self.id_combined = pkt.id_combined
            self.unitcode = pkt.unitcode
            self.COMMANDS = lowlevel.Lighting2.COMMANDS
        if isinstance(pkt, lowlevel.Lighting3):
            self.system = pkt.system
            self.channel = pkt.channel
            self.COMMANDS = lowlevel.Lighting3.COMMANDS
        if isinstance(pkt, lowlevel.Lighting4):
            self.cmd = pkt.cmd
            self.pulse = pkt.pulse
            self.COMMANDS = lowlevel.Lighting4.COMMANDS
        if isinstance(pkt, lowlevel.Lighting5):
            self.id_combined = pkt.id_combined
            self.unitcode = pkt.unitcode
            if self.subtype == 0x00:
                self.COMMANDS = lowlevel.Lighting5.COMMANDS_00
            elif self.subtype == 0x01:
                self.COMMANDS = lowlevel.Lighting5.COMMANDS_01
            elif self.subtype in (0x02, 0x04, 0x0F):
                self.COMMANDS = lowlevel.Lighting5.COMMANDS_02_04_0F
            elif self.subtype == 0x03:
                self.COMMANDS = lowlevel.Lighting5.COMMANDS_03
            else:
                self.COMMANDS = lowlevel.Lighting5.COMMANDS_XX
        if isinstance(pkt, lowlevel.Lighting6):
            self.id_combined = pkt.id_combined
            self.groupcode = pkt.groupcode
            self.unitcode = pkt.unitcode
            self.cmndseqnbr = 0
            self.COMMANDS = lowlevel.Lighting6.COMMANDS

    def send_command(self, transport, command):
        """ Send an ommand using the given transport """
        if self.packettype == 0x10:  # Lighting1
            pkt = lowlevel.Lighting1()
            pkt.set_transmit(self.subtype, 0, self.housecode, self.unitcode,
                             command)
            transport.send(pkt.data)
        elif self.packettype == 0x11:  # Lighting2
            pkt = lowlevel.Lighting2()
            pkt.set_transmit(self.subtype, 0, self.id_combined, self.unitcode,
                             command, 0x00)
            transport.send(pkt.data)
        elif self.packettype == 0x12:  # Lighting3
            pkt = lowlevel.Lighting3()
            pkt.set_transmit(self.subtype, 0, self.system, self.channel,
                             command)
            transport.send(pkt.data)
        elif self.packettype == 0x13:  # Lighting4
            pkt = lowlevel.Lighting4()
            code = self.cmd & ~1
            code |= command
            pkt.set_transmit(self.subtype, 0, code, self.pulse)
            transport.send(pkt.data)
        elif self.packettype == 0x14:  # Lighting5
            pkt = lowlevel.Lighting5()
            pkt.set_transmit(self.subtype, 0, self.id_combined, self.unitcode,
                             command, 0x00)
            transport.send(pkt.data)
        elif self.packettype == 0x15:  # Lighting6
            pkt = lowlevel.Lighting6()
            pkt.set_transmit(self.subtype, 0, self.id_combined, self.groupcode,
                             self.unitcode,
                             command, self.cmndseqnbr)
            self.cmndseqnbr = (self.cmndseqnbr + 1) % 5
            transport.send(pkt.data)

    def send_onoff(self, transport, turn_on):
        """ Send an 'On' or 'Off' command using the given transport """
        if self.packettype == 0x10:  # Lighting1
            self.send_command(transport, turn_on and 0x01 or 0x00)
        elif self.packettype == 0x11:  # Lighting2
            self.send_command(transport, turn_on and 0x01 or 0x00)
        elif self.packettype == 0x12:  # Lighting3
            self.send_command(transport, turn_on and 0x10 or 0x1a)
        elif self.packettype == 0x13:  # Lighting4
            self.send_command(transport, 0x1 if turn_on else 0x0)
        elif self.packettype == 0x14:  # Lighting5
            self.send_command(transport, turn_on and 0x01 or 0x00)
        elif self.packettype == 0x15:  # Lighting6
            self.send_command(transport, not turn_on and 0x01 or 0x00)

    def send_on(self, transport):
        """ Send an 'On' command using the given transport """
        self.send_onoff(transport, True)

    def send_off(self, transport):
        """ Send an 'Off' command using the given transport """
        self.send_onoff(transport, False)

    def send_openclosestop(self, transport, command):
        """ Send an 'Open' or a 'Close' or a 'Stop' command
            using the given transport """
        if self.packettype == 0x14:  # Lighting5
            if command not in [0x0d, 0x0e, 0x0f]:
                raise ValueError(command, "is not a relay packet in Lighting5")
            self.send_command(transport, command)
        else:
            raise ValueError("Unsupported packettype")

    def send_open(self, transport):
        """ Send an 'Open' command using the given transport """
        self.send_openclosestop(transport, 0x0f)

    def send_close(self, transport):
        """ Send an 'Close' command using the given transport """
        self.send_openclosestop(transport, 0x0d)

    def send_stop(self, transport):
        """ Send an 'Stop' command using the given transport """
        self.send_openclosestop(transport, 0x0e)

    def send_dim(self, transport, level):
        """ Send a 'Dim' command with the given level using the given
            transport
        """
        #  pylint: disable=too-many-branches
        if level < 0 or level > 100:
            raise ValueError("Dim level must be between 0 and 100")

        if self.packettype == 0x10:  # Lighting1
            raise ValueError("Dim level unsupported for Lighting1")
            # Supporting a dim level for X10 directly is not possible because
            # RFXtrx does not support sending extended commands
        if self.packettype == 0x11:  # Lighting2
            if level == 0:
                self.send_off(transport)
            else:
                pkt = lowlevel.Lighting2()
                pkt.set_transmit(self.subtype, 0, self.id_combined,
                                 self.unitcode, 0x02,
                                 ((level + 6) * 16 // 100) - 1)
                transport.send(pkt.data)
        elif self.packettype == 0x12:  # Lighting3
            if level == 0:
                self.send_off(transport)
            elif level == 100:
                self.send_on(transport)
            else:
                pkt = lowlevel.Lighting3()
                pkt.set_transmit(self.subtype, 0, self.system, self.channel,
                                 (level * 9 // 100) + 17)
                transport.send(pkt.data)
        elif self.packettype == 0x14:  # Lighting5
            if level == 0:
                self.send_off(transport)
            else:
                pkt = lowlevel.Lighting5()
                pkt.set_transmit(self.subtype, 0, self.id_combined,
                                 self.unitcode, 0x10,
                                 ((level + 3) * 32 // 100) - 1)
                transport.send(pkt.data)
        elif self.packettype == 0x15:  # Lighting6
            raise ValueError("Dim level unsupported for Lighting6")
        elif self.packettype == 0x1e:  # Funkbus
            raise ValueError("Dim level unsupported for Funkbus")
        else:
            raise ValueError("Unsupported packettype")


class ChimeDevice(RFXtrxDevice):
    """ Concrete class for a control device """
    def __init__(self, pkt):
        super().__init__(pkt)
        self.id1 = pkt.id1
        self.id2 = pkt.id2
        self.COMMANDS = lowlevel.Chime.COMMANDS

    def send_command(self, transport, sound):
        """Trigger a chime sound on device."""
        pkt = lowlevel.Chime()
        pkt.set_transmit(self.subtype, 0, self.id1, self.id2, sound)
        transport.send(pkt.data)

###############################################################################
# get_device_from_pkt method
###############################################################################


def get_device_from_pkt(pkt):
    """Construct a device object from a packet."""
    # pylint: disable=too-many-boolean-expressions
    if isinstance(pkt, (lowlevel.Lighting1, lowlevel.Lighting2,
                        lowlevel.Lighting3, lowlevel.Lighting4,
                        lowlevel.Lighting5, lowlevel.Lighting6)):
        device = LightingDevice(pkt)
    elif isinstance(pkt, lowlevel.RollerTrol):
        device = RollerTrolDevice(pkt)
    elif isinstance(pkt, lowlevel.DDxxxx):
        device = DDxxxxDevice(pkt)
    elif isinstance(pkt, lowlevel.Rfy):
        device = RfyDevice(pkt)
    elif isinstance(pkt, lowlevel.Chime):
        device = ChimeDevice(pkt)
    elif isinstance(pkt, lowlevel.Security1):
        device = SecurityDevice(pkt)
    elif isinstance(pkt, lowlevel.Funkbus):
        device = FunkDevice(pkt)
    else:
        device = RFXtrxDevice(pkt)
    return device


class SecurityDevice(RFXtrxDevice):
    """ Concrete class for a control device """

    def __init__(self, pkt):
        super().__init__(pkt)
        self.id_combined = pkt.id_combined
        self.cmndseqnbr = 0
        self.STATUS = lowlevel.Security1.STATUS

    def send_status(self, transport, status):
        """Trigger a status message on device."""
        pkt = lowlevel.Security1()
        pkt.set_transmit(
            self.subtype,
            self.cmndseqnbr,
            self.id_combined,
            status
        )
        self.cmndseqnbr = (self.cmndseqnbr + 1) % 5
        transport.send(pkt.data)


###############################################################################
# get_device method
###############################################################################


def get_device(packettype, subtype, id_string):
    """ Return a device base on its identifying values """
    pkt = lowlevel.get_packet_with_id(packettype, subtype, id_string)
    if pkt is None:
        raise ValueError("Unsupported packettype")
    return get_device_from_pkt(pkt)


###############################################################################
# RFXtrxEvent class
###############################################################################

class RFXtrxEvent:
    """ Abstract superclass for all events """

    def __init__(self, device):
        self.device = device


###############################################################################
# SensorEvent class
###############################################################################

class SensorEvent(RFXtrxEvent):
    """ Concrete class for sensor events """

    def __init__(self, pkt):
        #  pylint: disable=too-many-branches, too-many-statements
        device = get_device_from_pkt(pkt)
        super().__init__(device)

        self.values = {}
        self.pkt = pkt
        if isinstance(pkt, lowlevel.Undecoded):
            self.values['Payload'] = pkt.payload.hex()
        if isinstance(pkt, lowlevel.RfxMeter):
            self.values['Counter value'] = pkt.value
        if isinstance(pkt, (lowlevel.Temp, lowlevel.TempHumid,
                            lowlevel.TempHumidBaro, lowlevel.TempRain)):
            self.values['Temperature'] = pkt.temp
        if isinstance(pkt, lowlevel.Bbq):
            self.values['Temperature'] = pkt.temp1
            self.values['Temperature2'] = pkt.temp2
        if isinstance(pkt, (lowlevel.Humid, lowlevel.TempHumid,
                            lowlevel.TempHumidBaro)):
            self.values['Humidity'] = pkt.humidity
            self.values['Humidity status'] = pkt.humidity_status_string
            self.values['Humidity status numeric'] = pkt.humidity_status
        if isinstance(pkt, (lowlevel.Baro, lowlevel.TempHumidBaro)):
            self.values['Barometer'] = pkt.baro
            self.values['Forecast'] = pkt.forecast_string
            self.values['Forecast numeric'] = pkt.forecast
        if isinstance(pkt, lowlevel.Rain):
            self.values['Rain rate'] = pkt.rainrate
            self.values['Rain total'] = pkt.raintotal
        if isinstance(pkt, lowlevel.TempRain):
            self.values['Rain total'] = pkt.raintotal
        if isinstance(pkt, lowlevel.Wind):
            self.values['Wind direction'] = pkt.direction
            self.values['Wind average speed'] = pkt.average_speed
            self.values['Wind gust'] = pkt.gust
            if pkt.temperature is not None:
                self.values['Temperature'] = pkt.temperature
            if pkt.chill is not None:
                self.values['Chill'] = pkt.chill
        if isinstance(pkt, lowlevel.UV):
            self.values['UV'] = pkt.uvi
        if isinstance(pkt, lowlevel.Energy):
            self.values['Energy usage'] = pkt.currentwatt
            self.values['Total usage'] = pkt.totalwatts
            self.values['Count'] = pkt.count
        if isinstance(pkt, lowlevel.Energy1):
            self.values['Current Ch. 1'] = pkt.currentamps1
            self.values['Current Ch. 2'] = pkt.currentamps2
            self.values['Current Ch. 3'] = pkt.currentamps3
            # CM113/ELEC1 doesn't have a 'total usage' counter, so provide an
            # aggregated virtual value
            self.values['Total usage'] = (pkt.currentamps1 + pkt.currentamps2
                                          + pkt.currentamps3)
            self.values['Count'] = pkt.count
        if isinstance(pkt, lowlevel.Energy4):
            self.values['Current Ch. 1'] = pkt.currentamps1
            self.values['Current Ch. 2'] = pkt.currentamps2
            self.values['Current Ch. 3'] = pkt.currentamps3
            self.values['Total usage'] = pkt.totalwatthours
            self.values['Count'] = pkt.count
        if isinstance(pkt, lowlevel.Energy5):
            self.values['Voltage'] = pkt.voltage
            self.values['Current'] = pkt.currentamps
            self.values['Energy usage'] = pkt.currentwatt
            self.values['Total usage'] = pkt.totalwatthours
        if isinstance(pkt, lowlevel.Cartelectronic):
            if pkt.type_string == 'CARTELECTRONIC_ENCODER':
                self.values['Counter value'] = pkt.counter1
                self.values['Count'] = pkt.counter2
            elif pkt.type_string == 'CARTELECTRONIC_LINKY':
                # Index for current tarif if consummer
                self.values['Total usage'] = pkt.conswatthours
                # Index for current tarif if production
                self.values['Count'] = pkt.prodwatthours
                # Index of current tarif
                self.values['Counter value'] = pkt.tarif_num
                self.values['Voltage'] = pkt.voltage
                self.values['Energy usage'] = pkt.currentwatt
                self.values['Sensor Status'] = pkt.teleinfo_ok
            elif pkt.type_string == 'CARTELECTRONIC_TIC':
                self.values['Counter value'] = pkt.counter1
                self.values['Count'] = pkt.counter2
                self.values['Energy usage'] = pkt.currentwatt
                self.values['Sensor Status'] = pkt.teleinfo_ok
                self.values['Contract type'] = pkt.contract_type
        if isinstance(pkt, lowlevel.Security1):
            self.values['Sensor Status'] = pkt.security1_status_string
        if not isinstance(pkt, (lowlevel.Energy5,
                                lowlevel.RfxMeter,
                                lowlevel.Undecoded)):
            self.values['Battery numeric'] = pkt.battery
        if not isinstance(pkt, lowlevel.Undecoded):
            self.values["Rssi numeric"] = pkt.rssi

    def __str__(self):
        return "{0} device=[{1}] values={2}".format(
            type(self), self.device, sorted(self.values.items()))


###############################################################################
# ControlEvent class
###############################################################################

class ControlEvent(RFXtrxEvent):
    """ Concrete class for control events """

    def __init__(self, pkt):
        device = get_device_from_pkt(pkt)
        super().__init__(device)

        self.values = {}
        self.values['Command'] = pkt.value('cmnd_string')
        if isinstance(pkt, lowlevel.Lighting2) and pkt.cmnd in [2, 5]:
            dimmable = True
            self.values['Dim level'] = (pkt.level + 1) * 100 // 16
        elif isinstance(pkt, lowlevel.Lighting5) and pkt.cmnd in [0x10]:
            dimmable = True
            self.values['Dim level'] = (pkt.level + 1) * 100 // 32
        else:
            dimmable = False
        self.device.known_to_be_dimmable = dimmable

        if isinstance(pkt, lowlevel.Lighting5) \
                and pkt.cmnd in [0x0d, 0x0e, 0x0f]:
            self.device.known_to_be_rollershutter = True

        if isinstance(pkt, lowlevel.Chime):
            self.values['Sound'] = pkt.sound

        if pkt.rssi is not None:
            self.values['Rssi numeric'] = pkt.rssi

        if isinstance(pkt, lowlevel.Funkbus):
            self.values['Keypress'] = pkt.value('time_string')

    def __str__(self):
        return "{0} device=[{1}] values={2}".format(
            type(self), self.device, sorted(self.values.items()))

###############################################################################
# Status class
###############################################################################


class StatusEvent(RFXtrxEvent):
    """ Concrete class for status """
    def __str__(self):
        return "{0} device=[{1}]".format(
            type(self), self.device)


class ConnectionEvent(RFXtrxEvent):
    """ Connection event """
    def __init__(self):
        super().__init__(None)


class ConnectionLost(ConnectionEvent):
    """ Connection lost """


class ConnectionDone(ConnectionEvent):
    """ Connection lost """


###############################################################################
# DummySerial class
###############################################################################


class _dummySerial:
    """ Dummy class for testing"""
    # pylint: disable=unused-argument
    def __init__(self, *args, **kwargs):
        self._read_num = 0
        self._data = {}
        self._data[0] = [0x0D, 0x01, 0x00, 0x01, 0x02, 0x53, 0x45,  # status
                         0x10,  # msg3: rsl
                         0x0C,  # msg4: hideki lacrosse
                         0x2F,  # msg5: x10 arc ac homeeasy oregon
                         0x01,  # msg6: keeloq
                         0x01, 0x00, 0x00]
        self._data[1] = [0x00, 0x00, 0x00, 0x00, 0x00,  # response to start
                         0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        self._data[2] = [0x0b, 0x15, 0x00, 0x2a, 0x12,
                         0x34, 0x41, 0x05, 0x03, 0x01, 0x00, 0x70]  # light
        self._data[3] = [0x0b, 0x15, 0x00, 0x2a, 0x12,
                         0x34, 0x41, 0x05, 0x03, 0x01, 0x00, 0x70]  # light
        self._data[4] = [0x0a, 0x51, 0x01, 0x00, 0x00,
                         0x00, 0x00, 0x00, 0x00, 0x00, 0x00]  # sensor1
        self._data[5] = [0x0b, 0x15, 0x00, 0x2a, 0x12,
                         0x34, 0x41, 0x05, 0x03, 0x01, 0x00, 0x70]  # light
        self._data[6] = [0x0a, 0x51, 0x01, 0x00, 0x00,
                         0x00, 0x00, 0x00, 0x00, 0x00, 0x00]  # sensor1
        self._data[7] = [0x0a, 0x20, 0x00, 0x00, 0x00,
                         0x00, 0x00, 0x00, 0x00, 0x00, 0x00]  # sensor2
        self._data[8] = [0x09, 0x03, 0x01, 0x1e,
                         0x28, 0x0a, 0xb7, 0x66, 0x04, 0x74]  # undecoded
        self._close_event = threading.Event()

    def write(self, *args, **kwargs):
        """ Dummy function for writing"""

    # pylint: disable=invalid-name
    def flushInput(self, *args, **kwargs):
        """ Called by PySerialTransport"""

    def read(self, data=None):
        """ Dummy function for reading"""
        if data is not None or self._read_num >= len(self._data):
            self._close_event.wait(0.1)
            return [0x00]
        res = self._data[self._read_num]
        self._read_num = self._read_num + 1
        return res

    def close(self):
        """ close connection to rfxtrx device """
        self._close_event.set()


###############################################################################
# RFXtrxTransportError class
###############################################################################


class RFXtrxTransportError(Exception):
    """ Connection error """

###############################################################################
# RFXtrxTransport class
###############################################################################


class RFXtrxTransport:
    """ Abstract superclass for all transport mechanisms """

    # pylint: disable=attribute-defined-outside-init
    @staticmethod
    def parse(data):
        """ Parse the given data and return an RFXtrxEvent """
        if data is None:
            return None
        pkt = lowlevel.parse(data)
        if pkt is not None:
            if isinstance(pkt, lowlevel.SensorPacket):
                obj = SensorEvent(pkt)
            elif isinstance(pkt, lowlevel.Status):
                obj = StatusEvent(pkt)
            else:
                obj = ControlEvent(pkt)

            # Store the latest RF signal data
            obj.data = data
            return obj
        return None

    def connect(self, timeout=None):
        """ connect to device """

    def reset(self):
        """ reset the rfxtrx device """

    def close(self):
        """ close connection to rfxtrx device """

    def receive_blocking(self):
        """ Wait until a packet is received and return with an RFXtrxEvent """

    def send(self, data):
        """ Send the given packet """


def transport_errors(message):
    """ Decorator to wrap low level errors in known error. """
    def _errors(func):
        @functools.wraps(func)
        def __errors(instance: RFXtrxTransport, *args, **kargs):
            try:
                return func(instance, *args, **kargs)
            except (socket.error,
                    serial.SerialException,
                    OSError) as exception:
                _LOGGER.debug("%s failed: %s", message,
                              str(exception), exc_info=True)
                raise RFXtrxTransportError(
                    "{0} failed: {1}".format(message, exception)
                ) from exception
        return __errors
    return _errors

###############################################################################
# PySerialTransport class
###############################################################################


class PySerialTransport(RFXtrxTransport):
    """ Implementation of a transport using PySerial """

    def __init__(self, port):
        self.port = port
        self.serial = None

    @transport_errors("connect")
    def connect(self, timeout=None):
        """ Open a serial connexion """
        try:
            self.serial = serial.Serial(self.port, 38400)
        except serial.SerialException:
            port = glob.glob('/dev/serial/by-id/usb-RFXCOM_*-port0')
            if len(port) < 1:
                raise
            _LOGGER.debug("Attempting connection by name %s", port)
            self.serial = serial.Serial(port[0], 38400)

    @transport_errors("receive")
    def receive_blocking(self):
        return self._receive_packet()

    def _receive_packet(self):
        """ Wait until a packet is received and return with an RFXtrxEvent """
        data = self.serial.read()
        if data == '\x00':
            return None
        pkt = bytearray(data)
        while len(pkt) < pkt[0]+1:
            data = self.serial.read(pkt[0]+1 - len(pkt))
            pkt.extend(bytearray(data))
        _LOGGER.debug(
            "Recv: %s",
            " ".join("0x{0:02x}".format(x) for x in pkt)
        )
        return self.parse(pkt)

    @transport_errors("send")
    def send(self, data):
        """ Send the given packet """
        if isinstance(data, bytearray):
            pkt = data
        elif isinstance(data, (bytes, str)):
            pkt = bytearray(data)
        else:
            raise ValueError("Invalid type")
        _LOGGER.debug(
            "Send: %s",
            " ".join("0x{0:02x}".format(x) for x in pkt)
        )
        self.serial.write(pkt)

    @transport_errors("reset")
    def reset(self):
        """ Reset the RFXtrx """
        self.send(b'\x0D\x00\x00\x00\x00\x00\x00'
                  b'\x00\x00\x00\x00\x00\x00\x00')
        sleep(0.3)  # Should work with 0.05, but not for me
        self.serial.flushInput()

    @transport_errors("close")
    def close(self):
        """ close connection to rfxtrx device """
        with suppress(serial.SerialException):
            self.serial.close()

###############################################################################
# PyNetworkTransport class
###############################################################################


class PyNetworkTransport(RFXtrxTransport):
    """ Implementation of a transport using sockets """

    def __init__(self, hostport):
        self.hostport = hostport    # must be a (host, port) tuple
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    @transport_errors("connect")
    def connect(self, timeout=None):
        """ Open a socket connection """
        self.sock.settimeout(timeout)
        self.sock.connect(self.hostport)
        self.sock.settimeout(None)
        _LOGGER.debug("Connected to network socket")

    @transport_errors("receive")
    def receive_blocking(self):
        """ Wait until a packet is received and return with an RFXtrxEvent """
        return self._receive_packet()

    def _receive_packet(self):
        """ Wait until a packet is received and return with an RFXtrxEvent """
        data = self.sock.recv(1)
        if data == b'':
            raise RFXtrxTransportError("Server was shutdown")
        if data == '\x00':
            return None
        pkt = bytearray(data)
        while len(pkt) < pkt[0]+1:
            data = self.sock.recv(pkt[0]+1 - len(pkt))
            if data == b'':
                raise RFXtrxTransportError("Server was shutdown")
            pkt.extend(bytearray(data))
        _LOGGER.debug(
            "Recv: %s",
            " ".join("0x{0:02x}".format(x) for x in pkt)
        )
        return self.parse(pkt)

    @transport_errors("send")
    def send(self, data):
        """ Send the given packet """
        if isinstance(data, bytearray):
            pkt = data
        elif isinstance(data, (bytes, str)):
            pkt = bytearray(data)
        else:
            raise ValueError("Invalid type")
        _LOGGER.debug(
            "Send: %s",
            " ".join("0x{0:02x}".format(x) for x in pkt)
        )
        self.sock.send(pkt)

    @transport_errors("reset")
    def reset(self):
        """ Reset the RFXtrx """
        try:
            self.send(b'\x0D\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00\x00\x00')
            sleep(0.3)
            self.sock.sendall(b'')
        except socket.error as exception:
            raise RFXtrxTransportError(
                "Reset failed: {0}".format(exception)) from exception

    @transport_errors("close")
    def close(self):
        """ close connection to rfxtrx device """
        with suppress(socket.error):
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()


class DummyTransport(RFXtrxTransport):
    """ Dummy transport for testing purposes """

    def __init__(self, device=""):
        self.device = device
        self._close_event = threading.Event()

    def connect(self, timeout=None):
        pass

    def receive(self, data=None):
        """ Emulate a receive by parsing the given data """
        if data is None:
            self._close_event.wait(0.1)
            return None
        pkt = bytearray(data)
        _LOGGER.debug(
            "Recv: %s",
            " ".join("0x{0:02x}".format(x) for x in pkt)
        )
        return self.parse(pkt)

    def receive_blocking(self, data=None):
        """ Emulate a receive by parsing the given data """
        return self.receive(data)

    def send(self, data):
        """ Emulate a send by doing nothing (except printing debug info if
            requested) """
        pkt = bytearray(data)
        _LOGGER.debug(
            "Send: %s",
            " ".join("0x{0:02x}".format(x) for x in pkt)
        )

    def close(self):
        """Close."""
        self._close_event.set()


class DummyTransport2(PySerialTransport):
    """ Dummy transport for testing purposes """
    #  pylint: disable=super-init-not-called
    def __init__(self, device=""):
        self.serial = _dummySerial(device, 38400, timeout=0.1)
        self._run_event = threading.Event()

    def connect(self, timeout=None):
        self._run_event.set()


class Connect:
    """ The main class for rfxcom-py.
    Has methods for sensors.
    """
    #  pylint: disable=too-many-instance-attributes, too-many-arguments
    def __init__(self, transport, event_callback=None,
                 modes=None):
        self._run_event = threading.Event()
        self._sensors = {}
        self._status = None
        self._modes = modes
        self._thread = threading.Thread(target=self._connect, daemon=True)
        self.event_callback = event_callback
        self.transport: RFXtrxTransport = transport

    def connect(self, timeout=None):
        """Connect to device."""
        self.transport.connect(timeout)
        self._thread.start()
        if not self._run_event.wait(timeout):
            self.close_connection()
            raise TimeoutError()

    def _connect(self):
        try:
            self._connect_internal()
        except RFXtrxTransportError as exception:
            _LOGGER.info("Connection lost %s", exception)
        finally:
            if self.event_callback and self._run_event.is_set():
                self.event_callback(ConnectionLost())

    def _connect_internal(self):
        """Connect """
        self.transport.reset()
        self._status = self.send_get_status()

        if self._modes is not None:
            self.set_recmodes(self._modes)
            self._status = self.send_get_status()

        if self._status:
            _LOGGER.debug(
                "Status: %s", self._status.device
            )

        self.send_start()

        self._run_event.set()
        if self.event_callback:
            self.event_callback(ConnectionDone())

        while self._run_event.is_set():
            event = self.transport.receive_blocking()
            if isinstance(event, RFXtrxEvent):
                if self.event_callback:
                    self.event_callback(event)
                if isinstance(event, SensorEvent):
                    self._sensors[event.device.id_string] = event.device

    def sensors(self):
        """ Return all found sensors.
        :return: dict of :class:`Sensor` instances.
        """
        return self._sensors

    def close_connection(self):
        """ Close connection to rfxtrx device """
        self._run_event.clear()
        self.transport.close()
        self._thread.join()

    def set_recmodes(self, modenames):
        """ Sets the device modes (which protocols to decode) """
        data = bytearray([0x0D, 0x00, 0x00, 0x00, 0x03, 0x00, 0x00,
                          0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

        # Keep the values read during init.
        data[5] = self._status.device.tranceiver_type
        data[6] = self._status.device.output_power

        # Build the mode data bytes from the mode names
        for mode in modenames:
            byteno, bitno = lowlevel.get_recmode_tuple(mode)
            if byteno is None:
                raise ValueError('Unknown mode name '+mode)

            data[7 + byteno] |= 1 << bitno

        self.transport.send(data)
        self._modes = modenames
        return self.transport.receive_blocking()

    def send_start(self):
        """ Sends the Start RFXtrx transceiver command """
        self.transport.send(b'\x0D\x00\x00\x03\x07\x00\x00'
                            b'\x00\x00\x00\x00\x00\x00\x00')
        return self.transport.receive_blocking()

    def send_get_status(self):
        """ Sends the Get Status command """
        self.transport.send(b'\x0D\x00\x00\x01\x02\x00\x00'
                            b'\x00\x00\x00\x00\x00\x00\x00')
        return self.transport.receive_blocking()


class Core(Connect):
    """ The main class for rfxcom-py. Has changed name to Connect """
