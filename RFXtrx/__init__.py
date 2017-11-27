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
# pylint: disable=R0903
from __future__ import print_function

from time import sleep
import threading
import serial
from . import lowlevel


###############################################################################
# RFXtrxDevice class
###############################################################################


class RFXtrxDevice(object):
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
        super(RollerTrolDevice, self).__init__(pkt)
        if isinstance(pkt, lowlevel.RollerTrol):
            self.known_to_be_rollershutter = True
            self.id_combined = pkt.id_combined
            self.unitcode = pkt.unitcode
            self.cmndseqnbr = 0

    def send_close(self, transport):
        """ Send a 'Close' command using the given transport """
        pkt = lowlevel.RollerTrol()
        pkt.set_transmit(
            self.subtype,
            self.cmndseqnbr,
            self.id_combined,
            self.unitcode,
            0x01
        )
        self.cmndseqnbr = (self.cmndseqnbr + 1) % 5
        transport.send(pkt.data)

    def send_open(self, transport):
        """ Send an 'Open' command using the given transport """
        pkt = lowlevel.RollerTrol()
        pkt.set_transmit(
            self.subtype,
            self.cmndseqnbr,
            self.id_combined,
            self.unitcode,
            0x00
        )
        self.cmndseqnbr = (self.cmndseqnbr + 1) % 5
        transport.send(pkt.data)

    def send_stop(self, transport):
        """ Send a 'Stop' command using the given transport """
        pkt = lowlevel.RollerTrol()
        pkt.set_transmit(
            self.subtype,
            self.cmndseqnbr,
            self.id_combined,
            self.unitcode,
            0x02
        )
        self.cmndseqnbr = (self.cmndseqnbr + 1) % 5
        transport.send(pkt.data)


class RfyDevice(RFXtrxDevice):
    """ Concrete class for a roller device """
    def __init__(self, pkt):
        super(RfyDevice, self).__init__(pkt)
        if isinstance(pkt, lowlevel.Rfy):
            self.known_to_be_rollershutter = True
            self.id_combined = pkt.id_combined
            self.unitcode = pkt.unitcode
            self.cmndseqnbr = 0

    def send_close(self, transport):
        """ Send a 'Close' command using the given transport """
        pkt = lowlevel.Rfy()
        pkt.set_transmit(
            self.subtype,
            self.cmndseqnbr,
            self.id_combined,
            self.unitcode,
            0x03
        )
        self.cmndseqnbr = (self.cmndseqnbr + 1) % 5
        transport.send(pkt.data)

    def send_open(self, transport):
        """ Send an 'Open' command using the given transport """
        pkt = lowlevel.Rfy()
        pkt.set_transmit(
            self.subtype,
            self.cmndseqnbr,
            self.id_combined,
            self.unitcode,
            0x01
        )
        self.cmndseqnbr = (self.cmndseqnbr + 1) % 5
        transport.send(pkt.data)

    def send_stop(self, transport):
        """ Send a 'Stop' command using the given transport """
        pkt = lowlevel.Rfy()
        pkt.set_transmit(
            self.subtype,
            self.cmndseqnbr,
            self.id_combined,
            self.unitcode,
            0x00
        )
        self.cmndseqnbr = (self.cmndseqnbr + 1) % 5
        transport.send(pkt.data)


class LightingDevice(RFXtrxDevice):
    """ Concrete class for a control device """

    # pylint: disable=too-many-instance-attributes
    def __init__(self, pkt):
        super(LightingDevice, self).__init__(pkt)
        if isinstance(pkt, lowlevel.Lighting1):
            self.housecode = pkt.housecode
            self.unitcode = pkt.unitcode
        if isinstance(pkt, lowlevel.Lighting2):
            self.id_combined = pkt.id_combined
            self.unitcode = pkt.unitcode
        if isinstance(pkt, lowlevel.Lighting3):
            self.system = pkt.system
            self.channel = pkt.channel
        if isinstance(pkt, lowlevel.Lighting4):
            self.cmd = pkt.cmd
            self.pulse = pkt.pulse
        if isinstance(pkt, lowlevel.Lighting5):
            self.id_combined = pkt.id_combined
            self.unitcode = pkt.unitcode
        if isinstance(pkt, lowlevel.Lighting6):
            self.id_combined = pkt.id_combined
            self.groupcode = pkt.groupcode
            self.unitcode = pkt.unitcode
            self.cmndseqnbr = 0

    def send_onoff(self, transport, turn_on):
        """ Send an 'On' or 'Off' command using the given transport """
        if self.packettype == 0x10:  # Lighting1
            pkt = lowlevel.Lighting1()
            pkt.set_transmit(self.subtype, 0, self.housecode, self.unitcode,
                             turn_on and 0x01 or 0x00)
            transport.send(pkt.data)
        elif self.packettype == 0x11:  # Lighting2
            pkt = lowlevel.Lighting2()
            pkt.set_transmit(self.subtype, 0, self.id_combined, self.unitcode,
                             turn_on and 0x01 or 0x00, 0x00)
            transport.send(pkt.data)
        elif self.packettype == 0x12:  # Lighting3
            pkt = lowlevel.Lighting3()
            pkt.set_transmit(self.subtype, 0, self.system, self.channel,
                             turn_on and 0x10 or 0x1a)
            transport.send(pkt.data)
        elif self.packettype == 0x13:  # Lighting4
            pkt = lowlevel.Lighting4()
            code = self.cmd & ~1
            code |= 0x1 if turn_on else 0x0
            pkt.set_transmit(self.subtype, 0, code, self.pulse)
            transport.send(pkt.data)
        elif self.packettype == 0x14:  # Lighting5
            pkt = lowlevel.Lighting5()
            pkt.set_transmit(self.subtype, 0, self.id_combined, self.unitcode,
                             turn_on and 0x01 or 0x00, 0x00)
            transport.send(pkt.data)
        elif self.packettype == 0x15:  # Lighting6
            pkt = lowlevel.Lighting6()
            pkt.set_transmit(self.subtype, 0, self.id_combined, self.groupcode,
                             self.unitcode,
                             not turn_on and 0x01 or 0x00, self.cmndseqnbr)
            self.cmndseqnbr = (self.cmndseqnbr + 1) % 5
            transport.send(pkt.data)
        else:
            return

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
            pkt = lowlevel.Lighting5()
            pkt.set_transmit(self.subtype, 0, self.id_combined, self.unitcode,
                             command, 0x00)
            transport.send(pkt.data)
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
        if level < 0 or level > 100:
            raise ValueError("Dim level must be between 0 and 100")

        if self.packettype == 0x10:  # Lighting1
            raise ValueError("Dim level unsupported for Lighting1")
            # Supporting a dim level for X10 directly is not possible because
            # RFXtrx does not support sending extended commands
        elif self.packettype == 0x11:  # Lighting2
            if level == 0:
                self.send_off(transport)
            else:
                pkt = lowlevel.Lighting2()
                pkt.set_transmit(self.subtype, 0, self.id_combined,
                                 self.unitcode, 0x02,
                                 ((level + 6) * 16 // 100) - 1)
                transport.send(pkt.data)
        elif self.packettype == 0x12:  # Lighting3
            raise ValueError("Dim level unsupported for Lighting3")
            # Should not be too hard to add dim level support for Lighting3
            # (Ikea Koppla) due to the availability of the level 1 .. level 9
            # commands. I just need someone to help me with defining a mapping
            # between a percentage and a level
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
        else:
            raise ValueError("Unsupported packettype")


###############################################################################
# get_devide method
###############################################################################


def get_device(packettype, subtype, id_string):
    """ Return a device base on its identifying values """
    # pylint: disable=too-many-return-statements
    if packettype == 0x10:  # Lighting1
        pkt = lowlevel.Lighting1()
        pkt.parse_id(subtype, id_string)
        return LightingDevice(pkt)
    elif packettype == 0x11:  # Lighting2
        pkt = lowlevel.Lighting2()
        pkt.parse_id(subtype, id_string)
        return LightingDevice(pkt)
    elif packettype == 0x12:  # Lighting3
        pkt = lowlevel.Lighting3()
        pkt.parse_id(subtype, id_string)
        return LightingDevice(pkt)
    elif packettype == 0x13:  # Lighting4
        pkt = lowlevel.Lighting4()
        pkt.parse_id(subtype, id_string)
        return LightingDevice(pkt)
    elif packettype == 0x14:  # Lighting5
        pkt = lowlevel.Lighting5()
        pkt.parse_id(subtype, id_string)
        return LightingDevice(pkt)
    elif packettype == 0x15:  # Lighting6
        pkt = lowlevel.Lighting6()
        pkt.parse_id(subtype, id_string)
        return LightingDevice(pkt)
    elif packettype == 0x19:  # RollerTrol
        pkt = lowlevel.RollerTrol()
        pkt.parse_id(subtype, id_string)
        return RollerTrolDevice(pkt)
    elif packettype == 0x1A:  # Rfy
        pkt = lowlevel.Rfy()
        pkt.parse_id(subtype, id_string)
        return RfyDevice(pkt)
    else:
        raise ValueError("Unsupported packettype")


###############################################################################
# RFXtrxEvent class
###############################################################################

class RFXtrxEvent(object):
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
        device = RFXtrxDevice(pkt)
        super(SensorEvent, self).__init__(device)

        self.values = {}
        self.pkt = pkt
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
            self.values['Temperature'] = pkt.temperature
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
        if isinstance(pkt, lowlevel.Chime):
            self.values['Sound'] = pkt.sound
        if isinstance(pkt, lowlevel.Security1):
            self.values['Sensor Status'] = pkt.security1_status_string
        if not isinstance(pkt, (lowlevel.Energy5, lowlevel.RfxMeter)):
            self.values['Battery numeric'] = pkt.battery
        self.values['Rssi numeric'] = pkt.rssi

    def __str__(self):
        return "{0} device=[{1}] values={2}".format(
            type(self), self.device, sorted(self.values.items()))


###############################################################################
# ControlEvent class
###############################################################################

class ControlEvent(RFXtrxEvent):
    """ Concrete class for control events """

    def __init__(self, pkt):
        # pylint: disable=too-many-boolean-expressions
        if isinstance(pkt, (lowlevel.Lighting1, lowlevel.Lighting2,
                            lowlevel.Lighting3, lowlevel.Lighting4,
                            lowlevel.Lighting5, lowlevel.Lighting6)):
            device = LightingDevice(pkt)
        elif isinstance(pkt, lowlevel.RollerTrol):
            device = RollerTrolDevice(pkt)
        elif isinstance(pkt, lowlevel.Rfy):
            device = RfyDevice(pkt)
        else:
            device = RFXtrxDevice(pkt)
        super(ControlEvent, self).__init__(device)

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

        if pkt.rssi is not None:
            self.values['Rssi numeric'] = pkt.rssi

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

###############################################################################
# DummySerila class
###############################################################################


class _dummySerial(object):
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

    def write(self, *args, **kwargs):
        """ Dummy function for writing"""
        pass

    # pylint: disable=invalid-name
    def flushInput(self, *args, **kwargs):
        """ Called by PySerialTransport"""
        pass

    def read(self, data=None):
        """ Dummy function for reading"""
        if data is not None or self._read_num >= len(self._data):
            return []
        res = self._data[self._read_num]
        self._read_num = self._read_num + 1
        return res

    def close(self):
        """ close connection to rfxtrx device """
        pass


###############################################################################
# RFXtrxTransport class
###############################################################################

class RFXtrxTransport(object):
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

    def reset(self):
        """ reset the rfxtrx device """
        pass

    def close(self):
        """ close connection to rfxtrx device """
        pass

###############################################################################
# PySerialTransport class
###############################################################################


class PySerialTransport(RFXtrxTransport):
    """ Implementation of a transport using PySerial """

    def __init__(self, port, debug=False):
        self.debug = debug
        self.port = port
        self.serial = None
        self._run_event = threading.Event()
        self._run_event.set()
        self.connect()

    def connect(self):
        """ Open a serial connexion """
        try:
            self.serial = serial.Serial(self.port, 38400, timeout=0.1)
        except serial.serialutil.SerialException:
            import glob
            port = glob.glob('/dev/serial/by-id/usb-RFXCOM_*-port0')[0]
            self.serial = serial.Serial(port, 38400, timeout=0.1)

    def receive_blocking(self):
        """ Wait until a packet is received and return with an RFXtrxEvent """
        data = None
        while self._run_event.is_set():
            try:
                data = self.serial.read()
            except TypeError:
                continue
            except serial.serialutil.SerialException:
                import time
                try:
                    self.connect()
                except serial.serialutil.SerialException:
                    time.sleep(5)
                    continue
            if not data or data == '\x00':
                continue
            pkt = bytearray(data)
            data = self.serial.read(pkt[0])
            pkt.extend(bytearray(data))
            if self.debug:
                print("RFXTRX: Recv: " +
                      " ".join("0x{0:02x}".format(x) for x in pkt))
            return self.parse(pkt)

    def send(self, data):
        """ Send the given packet """
        if isinstance(data, bytearray):
            pkt = data
        elif isinstance(data, (bytes, str)):
            pkt = bytearray(data)
        else:
            raise ValueError("Invalid type")
        if self.debug:
            print("RFXTRX: Send: " +
                  " ".join("0x{0:02x}".format(x) for x in pkt))
        self.serial.write(pkt)

    def reset(self):
        """ Reset the RFXtrx """
        self.send(b'\x0D\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        sleep(0.3)  # Should work with 0.05, but not for me
        self.serial.flushInput()

    def close(self):
        """ close connection to rfxtrx device """
        self._run_event.clear()
        self.serial.close()


class DummyTransport(RFXtrxTransport):
    """ Dummy transport for testing purposes """

    def __init__(self, device="", debug=True):
        self.device = device
        self.debug = debug

    def receive(self, data=None):
        """ Emulate a receive by parsing the given data """
        if data is None:
            return None
        pkt = bytearray(data)
        if self.debug:
            print("RFXTRX: Recv: " +
                  " ".join("0x{0:02x}".format(x) for x in pkt))
        return self.parse(pkt)

    def receive_blocking(self, data=None):
        """ Emulate a receive by parsing the given data """
        return self.receive(data)

    def send(self, data):
        """ Emulate a send by doing nothing (except printing debug info if
            requested) """
        pkt = bytearray(data)
        if self.debug:
            print("RFXTRX: Send: " +
                  " ".join("0x{0:02x}".format(x) for x in pkt))


class DummyTransport2(PySerialTransport):
    """ Dummy transport for testing purposes """
    #  pylint: disable=super-init-not-called
    def __init__(self, device="", debug=True):
        self.serial = _dummySerial(device, 38400, timeout=0.1)
        self.debug = debug
        self._run_event = threading.Event()
        self._run_event.set()


class Connect(object):
    """ The main class for rfxcom-py.
    Has methods for sensors.
    """
    #  pylint: disable=too-many-instance-attributes, too-many-arguments
    def __init__(self, device, event_callback=None, debug=False,
                 transport_protocol=PySerialTransport,
                 modes=None):
        self._run_event = threading.Event()
        self._run_event.set()
        self._sensors = {}
        self._status = None
        self._modes = modes
        self._debug = debug
        self.event_callback = event_callback

        self.transport = transport_protocol(device, debug)
        self._thread = threading.Thread(target=self._connect)
        self._thread.setDaemon(True)
        self._thread.start()

    def _connect(self):
        """Connect """
        self.transport.reset()
        self._status = self.send_get_status()

        if self._modes is not None:
            self.set_recmodes(self._modes)
            self._status = self.send_get_status()

        if self._debug:
            print("RFXTRX: ", self._status.device)

        self.send_start()

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
