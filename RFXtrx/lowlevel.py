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
This module provides low level packet parsing and generation code for the
RFXtrx.
"""
# pylint: disable=C0302,R0902,R0903,R0911,R0913
# pylint: disable= too-many-lines, too-many-statements


def parse(data):
    # pylint: disable=too-many-branches
    """ Parse a packet from a bytearray """
    if data[0] == 0 or len(data) < 2:
        # null length packet - sometimes happens on initialization
        return None

    expected_length = data[0] + 1
    if len(data) != expected_length:
        return None

    if data[1] == 0x01:
        pkt = Status()
    elif data[1] == 0x10:
        pkt = Lighting1()
    elif data[1] == 0x11:
        pkt = Lighting2()
    elif data[1] == 0x12:
        pkt = Lighting3()
    elif data[1] == 0x13:
        pkt = Lighting4()
    elif data[1] == 0x14:
        pkt = Lighting5()
    elif data[1] == 0x15:
        pkt = Lighting6()
    elif data[1] == 0x16:
        pkt = Chime()
    elif data[1] == 0x19:
        pkt = RollerTrol()
    elif data[1] == 0x1A:
        pkt = Rfy()
    elif data[1] == 0x20:
        pkt = Security1()
    elif data[1] == 0x50:
        pkt = Temp()
    elif data[1] == 0x4E:
        pkt = Bbq()
    elif data[1] == 0x4F:
        pkt = TempRain()
    elif data[1] == 0x51:
        pkt = Humid()
    elif data[1] == 0x52:
        pkt = TempHumid()
    elif data[1] == 0x53:
        pkt = Baro()
    elif data[1] == 0x54:
        pkt = TempHumidBaro()
    elif data[1] == 0x55:
        pkt = Rain()
    elif data[1] == 0x56:
        pkt = Wind()
    elif data[1] == 0x57:
        pkt = UV()
    elif data[1] == 0x59:
        pkt = Energy1()
    elif data[1] == 0x5A:
        pkt = Energy()
    elif data[1] == 0x5B:
        pkt = Energy4()
    elif data[1] == 0x5C:
        pkt = Energy5()
    elif data[1] == 0x71:
        pkt = RfxMeter()
    else:
        return None

    pkt.load_receive(data)
    return pkt


###############################################################################
# Packet class
###############################################################################

class Packet():
    """ Abstract superclass for all low level packets """

    _UNKNOWN_TYPE = "Unknown type ({0:#04x}/{1:#04x})"
    _UNKNOWN_CMND = "Unknown command ({0:#04x})"

    def __init__(self):
        """Constructor"""
        self.data = None
        self.packetlength = None
        self.packettype = None
        self.subtype = None
        self.seqnbr = None
        self.rssi = None
        self.rssi_byte = None
        self.type_string = None
        self.id_string = None

    def has_value(self, datatype):
        """Return True if the sensor supports the given data type.
        sensor.has_value(RFXCOM_TEMPERATURE) is identical to calling
        sensor.has_temperature().
        """
        return hasattr(self, datatype)

    def value(self, datatype):
        """Return the :class:`SensorValue` for the given data type.
        sensor.value(RFXCOM_TEMPERATURE) is identical to calling
        sensor.temperature().
        """
        return getattr(self, datatype, None)

    def __getattr__(self, name):
        typename = name.replace("has_", "", 1)
        if not name == typename:
            return lambda: self.has_value(typename)
        raise AttributeError(name)

    def __eq__(self, other):
        if not isinstance(other, Packet):
            return False
        return self.id_string == other.id_string

    def __str__(self):
        return "Packet [id_string={0}]".format(self.id_string)

    def __repr__(self):
        return self.__str__()


###############################################################################
# Status class
###############################################################################

class Status(Packet):
    """
    Data class for the Status packet type
    """

    TYPES = {
        0x50: '310MHz',
        0x51: '315MHz',
        0x53: '433.92MHz',
        0x55: '868.00MHz',
        0x56: '868.00MHz FSK',
        0x57: '868.30MHz',
        0x58: '868.30MHz FSK',
        0x59: '868.35MHz',
        0x5A: '868.35MHz FSK',
        0x5B: '868.95MHz',
        0x5C: '868.30MHz FSK PKT',
        0x5D: '868.35MHz FSK PKT',
        0x5E: '868.40MHz FSK PKT'
    }

    """
    Receiving modes names. DO NOT alter their order.
    """
    RECMODES = [
        [
            "aeblyss",
            "rubicson",
            "fineoffset",
            "lighting4",
            "rsl",
            "byronsx",
            "imagintronix",
            "undecoded"
        ],
        [
            "mertik",
            "adlightwave",
            "hideki",
            "lacrosse",
            "fs20",
            "proguard",
            "blindst0",
            "blindst1234"
        ],
        [
            "x10",
            "arc",
            "ac",
            "homeeasy",
            "meiantech",
            "oregon",
            "ati",
            "visonic"
        ],
        [
            "keeloq",
            "homeconfort"
        ]
    ]
    """
    Mapping of numeric subtype values to strings, used in type_string
    """

    def __str__(self):
        return ("Status [subtype={0}, firmware={1}, output_power={2}, "
                "devices={3}]").format(self.type_string,
                                       self.firmware_version,
                                       self.output_power,
                                       self.devices)

    def __init__(self):
        """Constructor"""
        super().__init__()
        self.tranceiver_type = None
        self.firmware_version = None
        self.output_power = None
        self.devices = None

    def _decode_recmodes(self, data, index):
        res = set()

        for i in range(0, len(self.RECMODES[index])):
            if (data & (1 << i)) != 0:
                res.add(self.RECMODES[index][i])
        return res

    def load_receive(self, data):
        """Load data from a bytearray"""
        self.data = data
        self.packetlength = data[0]
        self.packettype = data[1]

        self.tranceiver_type = data[5]
        self.firmware_version = data[6]
        self.output_power = data[13]

        devs = set()
        devs.update(self._decode_recmodes(data[7], 0))
        devs.update(self._decode_recmodes(data[8], 1))
        devs.update(self._decode_recmodes(data[9], 2))
        devs.update(self._decode_recmodes(data[10], 3))
        self.devices = sorted(devs)

        self._set_strings()

    def _set_strings(self):
        """Translate loaded numeric values into convenience strings"""
        if self.tranceiver_type in self.TYPES:
            self.type_string = self.TYPES[self.tranceiver_type]
        else:
            # Degrade nicely for yet unknown subtypes
            self.type_string = 'Unknown'


def get_recmode_tuple(mode_name):
    """
    Look for a receiving mode in the RECMODES lists from a name.
    Return a tuple (listno, sublistno), or (None, None) if
    not found.
    """
    for i in range(0, len(Status.RECMODES)):
        if mode_name in Status.RECMODES[i]:
            return (i, Status.RECMODES[i].index(mode_name))
    return (None, None)


###############################################################################
# Lighting1 class
###############################################################################

class Lighting1(Packet):
    """
    Data class for the Lighting1 packet type
    """

    TYPES = {0x00: 'X10 lighting',
             0x01: 'ARC',
             0x02: 'ELRO AB400D',
             0x03: 'Waveman',
             0x04: 'Chacon EMW200',
             0x05: 'IMPULS',
             0x06: 'RisingSun',
             0x07: 'Philips SBC',
             0x08: 'Energenie',
             0x09: 'Energenie5',
             0x0A: 'GDR2',
             0x0B: 'HQ'}
    """
    Mapping of numeric subtype values to strings, used in type_string
    """

    ALIAS_TYPES = {'KlikAanKlikUit code wheel': 0x01,
                   'NEXA code wheel': 0x01,
                   'CHACON code wheel': 0x01,
                   'HomeEasy code wheel': 0x01,
                   'Proove': 0x01,
                   'DomiaLite': 0x01,
                   'InterTechno': 0x01,
                   'AB600': 0x01}
    """
    Mapping of subtype aliases to the corresponding subtype value
    """

    HOUSECODES = {0x41: 'A', 0x42: 'B', 0x43: 'C', 0x44: 'D',
                  0x45: 'E', 0x46: 'F', 0x47: 'G', 0x48: 'H',
                  0x49: 'I', 0x4A: 'J', 0x4B: 'K', 0x4C: 'L',
                  0x4D: 'M', 0x4E: 'N', 0x4F: 'O', 0x50: 'P'}
    """
    Mapping of housecode numeric values to strings, used in id_string
    """

    COMMANDS = {0x00: 'Off',
                0x01: 'On',
                0x02: 'Dim',
                0x03: 'Bright',
                0x05: 'All/group Off',
                0x06: 'All/group On',
                0x07: 'Chime',
                0xFF: 'Illegal command'}
    """
    Mapping of command numeric values to strings, used for cmnd_string
    """

    def __str__(self):
        return ("Lighting1 [subtype={0}, seqnbr={1}, id={2}, cmnd={3}, " +
                "rssi={4}]") \
            .format(self.type_string, self.seqnbr, self.id_string,
                    self.cmnd_string, self.rssi)

    def __init__(self):
        """Constructor"""
        super().__init__()
        self.housecode = None
        self.unitcode = None
        self.cmnd = None
        self.cmnd_string = None

    def parse_id(self, subtype, id_string):
        """Parse a string id into individual components"""
        try:
            self.packettype = 0x10
            self.subtype = subtype
            hcode = id_string[0:1]
            for hcode_num in self.HOUSECODES:
                if self.HOUSECODES[hcode_num] == hcode:
                    self.housecode = hcode_num
            self.unitcode = int(id_string[1:])
            self._set_strings()
        except ValueError as exc:
            raise ValueError("Invalid id_string") from exc
        if self.id_string != id_string:
            raise ValueError("Invalid id_string")

    def load_receive(self, data):
        """Load data from a bytearray"""
        self.data = data
        self.packetlength = data[0]
        self.packettype = data[1]
        self.subtype = data[2]
        self.seqnbr = data[3]
        self.housecode = data[4]
        self.unitcode = data[5]
        self.cmnd = data[6]
        self.rssi_byte = data[7]
        self.rssi = self.rssi_byte >> 4
        self._set_strings()

    def set_transmit(self, subtype, seqnbr, housecode, unitcode, cmnd):
        """Load data from individual data fields"""
        self.packetlength = 7
        self.packettype = 0x10
        self.subtype = subtype
        self.seqnbr = seqnbr
        self.housecode = housecode
        self.unitcode = unitcode
        self.cmnd = cmnd
        self.rssi_byte = 0
        self.rssi = 0
        self.data = bytearray([self.packetlength, self.packettype,
                               self.subtype, self.seqnbr, self.housecode,
                               self.unitcode, self.cmnd, self.rssi_byte])
        self._set_strings()

    def _set_strings(self):
        """Translate loaded numeric values into convenience strings"""
        self.id_string = self.HOUSECODES[self.housecode] + str(self.unitcode)
        if self.subtype in self.TYPES:
            self.type_string = self.TYPES[self.subtype]
        else:
            # Degrade nicely for yet unknown subtypes
            self.type_string = self._UNKNOWN_TYPE.format(self.packettype,
                                                         self.subtype)
        if self.cmnd is not None:
            if self.cmnd in self.COMMANDS:
                self.cmnd_string = self.COMMANDS[self.cmnd]
            else:
                self.cmnd_string = self._UNKNOWN_CMND.format(self.cmnd)


###############################################################################
# Lighting2 class
###############################################################################

class Lighting2(Packet):
    """
    Data class for the Lighting2 packet type
    """

    TYPES = {0x00: 'AC',
             0x01: 'HomeEasy EU',
             0x02: 'ANSLUT',
             0x03: 'Kambrook'}
    """
    Mapping of numeric subtype values to strings, used in type_string
    """

    ALIAS_TYPES = {'KlikAanKlikUit automatic': 0x00,
                   'NEXA automatic': 0x00,
                   'CHACON autometic': 0x00,
                   'HomeEasy UK': 0x00}
    """
    Mapping of subtype aliases to the corresponding subtype value
    """

    COMMANDS = {0x00: 'Off',
                0x01: 'On',
                0x02: 'Set level',
                0x03: 'Group off',
                0x04: 'Group on',
                0x05: 'Set group level'}
    """
    Mapping of command numeric values to strings, used for cmnd_string
    """

    def __str__(self):
        return ("Lighting2 [subtype={0}, seqnbr={1}, id={2}, cmnd={3}, " +
                "level={4}, rssi={5}]") \
            .format(self.type_string, self.seqnbr, self.id_string,
                    self.cmnd_string, self.level, self.rssi)

    def __repr__(self):
        return self.__str__()

    def __init__(self):
        """Constructor"""
        super().__init__()
        self.id1 = None
        self.id2 = None
        self.id3 = None
        self.id4 = None
        self.id_combined = None
        self.unitcode = None
        self.cmnd = None
        self.level = None
        self.cmnd_string = None

    def parse_id(self, subtype, id_string):
        """Parse a string id into individual components"""
        try:
            self.packettype = 0x11
            self.subtype = subtype
            self.id_combined = int(id_string[:7], 16)
            self.id1 = self.id_combined >> 24
            self.id2 = self.id_combined >> 16 & 0xff
            self.id3 = self.id_combined >> 8 & 0xff
            self.id4 = self.id_combined & 0xff
            self.unitcode = int(id_string[8:])
            self._set_strings()
        except ValueError as exc:
            raise ValueError("Invalid id_string") from exc
        if self.id_string != id_string:
            raise ValueError("Invalid id_string")

    def load_receive(self, data):
        """Load data from a bytearray"""
        self.data = data
        self.packetlength = data[0]
        self.packettype = data[1]
        self.subtype = data[2]
        self.seqnbr = data[3]
        self.id1 = data[4]
        self.id2 = data[5]
        self.id3 = data[6]
        self.id4 = data[7]
        self.id_combined = (self.id1 << 24) + (self.id2 << 16) \
            + (self.id3 << 8) + self.id4
        self.unitcode = data[8]
        self.cmnd = data[9]
        self.level = data[10]
        self.rssi_byte = data[11]
        self.rssi = self.rssi_byte >> 4
        self._set_strings()

    def set_transmit(self, subtype, seqnbr, id_combined, unitcode, cmnd,
                     level):
        """Load data from individual data fields"""
        self.packetlength = 0x0b
        self.packettype = 0x11
        self.subtype = subtype
        self.seqnbr = seqnbr
        self.id_combined = id_combined
        self.id1 = id_combined >> 24
        self.id2 = id_combined >> 16 & 0xff
        self.id3 = id_combined >> 8 & 0xff
        self.id4 = id_combined & 0xff
        self.unitcode = unitcode
        self.cmnd = cmnd
        self.level = level
        self.rssi_byte = 0
        self.rssi = 0
        self.data = bytearray([self.packetlength, self.packettype,
                               self.subtype, self.seqnbr, self.id1, self.id2,
                               self.id3, self.id4, self.unitcode, self.cmnd,
                               self.level, self.rssi_byte])
        self._set_strings()

    def _set_strings(self):
        """Translate loaded numeric values into convenience strings"""
        self.id_string = "{0:07x}:{1}".format(self.id_combined, self.unitcode)
        if self.subtype in self.TYPES:
            self.type_string = self.TYPES[self.subtype]
        else:
            # Degrade nicely for yet unknown subtypes
            self.type_string = self._UNKNOWN_TYPE.format(self.packettype,
                                                         self.subtype)
        if self.cmnd is not None:
            if self.cmnd in self.COMMANDS:
                self.cmnd_string = self.COMMANDS[self.cmnd]
            else:
                self.cmnd_string = self._UNKNOWN_CMND.format(self.cmnd)


###############################################################################
# Lighting3 class
###############################################################################

class Lighting3(Packet):
    """
    Data class for the Lighting3 packet type
    """

    TYPES = {0x00: 'Ikea Koppla'}
    """
    Mapping of numeric subtype values to strings, used in type_string
    """

    COMMANDS = {0x00: 'Bright',
                0x08: 'Dim',
                0x10: 'On',
                0x11: 'Level 1',
                0x12: 'Level 2',
                0x13: 'Level 3',
                0x14: 'Level 4',
                0x15: 'Level 5',
                0x16: 'Level 6',
                0x17: 'Level 7',
                0x18: 'Level 8',
                0x19: 'Level 9',
                0x1a: 'Off',
                0x1c: 'Program'}
    """
    Mapping of command numeric values to strings, used for cmnd_string
    """

    def __str__(self):
        return ("Lighting3 [subtype={0}, seqnbr={1}, id={2}, cmnd={3}, " +
                "battery={4}, rssi={5}]") \
            .format(self.type_string, self.seqnbr, self.id_string,
                    self.cmnd_string, self.battery, self.rssi)

    def __init__(self):
        """Constructor"""
        super().__init__()
        self.system = None
        self.channel1 = None
        self.channel2 = None
        self.channel = None
        self.cmnd = None
        self.battery = None
        self.cmnd_string = None

    def parse_id(self, subtype, id_string):
        """Parse a string id into individual components"""
        try:
            self.packettype = 0x12
            self.subtype = subtype
            self.system = int(id_string[:1], 16)
            self.channel = int(id_string[2:], 16)
            self.channel1 = self.channel & 0xff
            self.channel2 = self.channel >> 8
            self._set_strings()
        except ValueError as exc:
            raise ValueError("Invalid id_string") from exc
        if self.id_string != id_string:
            raise ValueError("Invalid id_string")

    def load_receive(self, data):
        """Load data from a bytearray"""
        self.data = data
        self.packetlength = data[0]
        self.packettype = data[1]
        self.subtype = data[2]
        self.seqnbr = data[3]
        self.system = data[4]
        self.channel1 = data[5]
        self.channel2 = data[6]
        self.channel = (self.channel2 << 8) + self.channel1
        self.cmnd = data[7]
        self.rssi_byte = data[8]
        self.battery = self.rssi_byte & 0x0f
        self.rssi = self.rssi_byte >> 4
        self._set_strings()

    def set_transmit(self, subtype, seqnbr, system, channel, cmnd):
        """Load data from individual data fields"""
        self.packetlength = 0x08
        self.packettype = 0x12
        self.subtype = subtype
        self.seqnbr = seqnbr
        self.system = system
        self.channel = channel
        self.channel1 = channel & 0xff
        self.channel2 = channel >> 8
        self.cmnd = cmnd
        self.rssi_byte = 0
        self.battery = 0
        self.rssi = 0
        self.data = bytearray([self.packetlength, self.packettype,
                               self.subtype, self.seqnbr, self.system,
                               self.channel1, self.channel2, self.cmnd,
                               self.rssi_byte])
        self._set_strings()

    def _set_strings(self):
        """Translate loaded numeric values into convenience strings"""
        self.id_string = "{0:1x}:{1:03x}".format(self.system, self.channel)
        if self.subtype in self.TYPES:
            self.type_string = self.TYPES[self.subtype]
        else:
            # Degrade nicely for yet unknown subtypes
            self.type_string = self._UNKNOWN_TYPE.format(self.packettype,
                                                         self.subtype)
        if self.cmnd is not None:
            if self.cmnd in self.COMMANDS:
                self.cmnd_string = self.COMMANDS[self.cmnd]
            else:
                self.cmnd_string = self._UNKNOWN_CMND.format(self.cmnd)


###############################################################################
# Lighting4 class
###############################################################################

class Lighting4(Packet):
    """
    Data class for the Lighting4 packet type
    """

    TYPES = {0x00: 'PT2262'}
    """
    Mapping of numeric subtype values to strings, used in type_string
    """
    COMMANDS = {0x00: 'Off',
                0x01: 'On',
                0x02: 'Off',
                0x03: 'On',
                0x04: 'Off',
                0x05: 'On',
                0x07: 'On',
                0x09: 'On',
                0x0c: 'On'}
    """
    Mapping of command numeric values to strings, used for cmnd_string
    """

    def __str__(self):
        return ("Lighting4 [subtype={0}, seqnbr={1}, cmd={2}, pulse={3}, " +
                "rssi={4}]") \
            .format(self.type_string, self.seqnbr, self.id_string,
                    self.pulse, self.rssi)

    def __init__(self):
        """Constructor"""
        super().__init__()
        self.cmd1 = None
        self.cmd2 = None
        self.cmd3 = None
        self.cmd = None
        self.pulsehigh = None
        self.pulselow = None
        self.pulse = None
        self.cmnd_string = ""

    def parse_id(self, subtype, id_string):
        """Parse a string id into individual components"""
        try:
            self.packettype = 0x13
            self.subtype = subtype
            self.cmd = int(id_string, 16)
            self.cmd1 = self.cmd >> 16
            self.cmd2 = (self.cmd >> 8) & 0xff
            self.cmd3 = self.cmd & 0xff
            self._set_strings()
        except ValueError as exc:
            raise ValueError("Invalid id_string") from exc
        if self.id_string != id_string:
            raise ValueError("Invalid id_string")

    def load_receive(self, data):
        """Load data from a bytearray"""
        self.data = data
        self.packetlength = data[0]
        self.packettype = data[1]
        self.subtype = data[2]
        self.seqnbr = data[3]
        self.cmd1 = data[4]
        self.cmd2 = data[5]
        self.cmd3 = data[6]
        self.cmd = (self.cmd1 << 16) + (self.cmd2 << 8) + self.cmd3
        self.pulsehigh = data[7]
        self.pulselow = data[8]
        self.pulse = (self.pulsehigh << 8) + self.pulselow
        self.rssi_byte = data[9]
        self.rssi = self.rssi_byte >> 4
        self._set_strings()

    def set_transmit(self, subtype, seqnbr, cmd, pulse):
        """Load data from individual data fields"""
        self.packetlength = 0x09
        self.packettype = 0x13
        self.subtype = subtype
        self.seqnbr = seqnbr
        self.cmd = cmd
        self.cmd1 = self.cmd >> 16
        self.cmd2 = (self.cmd >> 8) & 0xff
        self.cmd3 = self.cmd & 0xff
        self.pulse = pulse
        self.pulsehigh = self.pulse >> 8
        self.pulselow = self.pulse & 0xff
        self.rssi_byte = 0
        self.rssi = 0
        self.data = bytearray([self.packetlength, self.packettype,
                               self.subtype, self.seqnbr,
                               self.cmd1, self.cmd2, self.cmd3,
                               self.pulsehigh, self.pulselow, self.rssi_byte])
        self._set_strings()

    def _set_strings(self):
        """Translate loaded numeric values into convenience strings"""
        self.id_string = "{0:06x}".format(self.cmd)
        if self.subtype in self.TYPES:
            self.type_string = self.TYPES[self.subtype]
        else:
            # Degrade nicely for yet unknown subtypes
            self.type_string = self._UNKNOWN_TYPE.format(self.packettype,
                                                         self.subtype)
        if self.cmd is not None:
            if self.cmd2 in self.COMMANDS:
                self.cmnd_string = self.COMMANDS[self.cmd2]
            else:
                self.cmnd_string = self._UNKNOWN_CMND.format(self.cmd)


###############################################################################
# Lighting5 class
###############################################################################

class Lighting5(Packet):
    """
    Data class for the Lighting5 packet type
    """

    TYPES = {0x00: 'LightwaveRF, Siemens',
             0x01: 'EMW100 GAO/Everflourish',
             0x02: 'BBSB new types',
             0x03: 'MDREMOTE LED dimmer',
             0x04: 'Conrad RSL2',
             0x05: 'Livolo',
             0x06: 'TRC02',
             0x07: 'Aoke',
             0x08: 'TRC02_2',
             0x09: 'Eurodomest',
             0x0A: 'Livolo appliance',
             0x0B: 'RGB432W',
             0x0C: 'MDREMOTE 107',
             0x0D: 'Legrand CAD',
             0x0E: 'Avantek',
             0x0F: 'ProMax/IT',
             0x10: 'MDREMOTE 108',
             0x11: 'Kangtai'}
    """
    Mapping of numeric subtype values to strings, used in type_string
    """

    ALIAS_TYPES = {'LightwaveRF': 0x00,
                   'Siemens': 0x00,
                   'EMW100 GAO': 0x01,
                   'Everflourish': 0x01,
                   'ProMax': 0x0f,
                   'IT': 0x0f}
    """
    Mapping of subtype aliases to the corresponding subtype value
    """

    COMMANDS_00 = {0x00: 'Off',
                   0x01: 'On',
                   0x02: 'Group off',
                   0x03: 'Mood1',
                   0x04: 'Mood2',
                   0x05: 'Mood3',
                   0x06: 'Mood4',
                   0x07: 'Mood5',
                   0x0a: 'Unlock',
                   0x0b: 'Lock',
                   0x0c: 'All lock',
                   0x0d: 'Close (inline relay)',
                   0x0e: 'Stop (inline relay)',
                   0x0f: 'Open (inline relay)',
                   0x10: 'Set level'}
    """
    Mapping of command numeric values to strings, used for cmnd_string
    """

    COMMANDS_01 = {0x00: 'Off',
                   0x01: 'On',
                   0x02: 'Learn'}
    """
    Mapping of command numeric values to strings, used for cmnd_string
    """

    COMMANDS_02_04_0F = {0x00: 'Off',
                         0x01: 'On',
                         0x02: 'Group off',
                         0x03: 'Group on'}
    """
    Mapping of command numeric values to strings, used for cmnd_string
    """

    COMMANDS_03 = {0x00: 'Power',
                   0x01: 'Light',
                   0x02: 'Bright',
                   0x03: 'Dim',
                   0x04: '100%',
                   0x05: '50%',
                   0x06: '25%',
                   0x07: 'Mode+',
                   0x08: 'Speed-',
                   0x09: 'Speed+',
                   0x0a: 'Mode-'}

    """
    Mapping of command numeric values to strings, used for cmnd_string
    """

    COMMANDS_XX = {0x00: 'Off',
                   0x01: 'On'}
    """
    Mapping of command numeric values to strings, used for cmnd_string
    """

    def __str__(self):
        return ("Lighting5 [subtype={0}, seqnbr={1}, id={2}, cmnd={3}, " +
                "level={4}, rssi={5}]") \
            .format(self.type_string, self.seqnbr, self.id_string,
                    self.cmnd_string, self.level, self.rssi)

    def __init__(self):
        """Constructor"""
        super().__init__()
        self.id1 = None
        self.id2 = None
        self.id3 = None
        self.id_combined = None
        self.unitcode = None
        self.cmnd = None
        self.level = None
        self.cmnd_string = None

    def parse_id(self, subtype, id_string):
        """( a string id into individual components"""
        try:
            self.packettype = 0x14
            self.subtype = subtype
            self.id_combined = int(id_string[:6], 16)
            self.id1 = self.id_combined >> 16
            self.id2 = self.id_combined >> 8 & 0xff
            self.id3 = self.id_combined & 0xff
            self.unitcode = int(id_string[7:])
            self._set_strings()
        except ValueError as exc:
            raise ValueError("Invalid id_string") from exc
        if self.id_string != id_string:
            raise ValueError("Invalid id_string")

    def load_receive(self, data):
        """Load data from a bytearray"""
        self.data = data
        self.packetlength = data[0]
        self.packettype = data[1]
        self.subtype = data[2]
        self.seqnbr = data[3]
        self.id1 = data[4]
        self.id2 = data[5]
        self.id3 = data[6]
        self.id_combined = (self.id1 << 16) + (self.id2 << 8) + self.id3
        self.unitcode = data[7]
        self.cmnd = data[8]
        self.level = data[9]
        self.rssi_byte = data[10]
        self.rssi = self.rssi_byte >> 4
        self._set_strings()

    def set_transmit(self, subtype, seqnbr, id_combined, unitcode, cmnd,
                     level):
        """Load data from individual data fields"""
        self.packetlength = 0x0a
        self.packettype = 0x14
        self.subtype = subtype
        self.seqnbr = seqnbr
        self.id_combined = id_combined
        self.id1 = id_combined >> 16
        self.id2 = id_combined >> 8 & 0xff
        self.id3 = id_combined & 0xff
        self.unitcode = unitcode
        self.cmnd = cmnd
        self.level = level
        self.rssi_byte = 0
        self.rssi = 0
        self.data = bytearray([self.packetlength, self.packettype,
                               self.subtype, self.seqnbr, self.id1, self.id2,
                               self.id3, self.unitcode, self.cmnd,
                               self.level, self.rssi_byte])
        self._set_strings()

    def _set_strings(self):
        """Translate loaded numeric values into convenience strings"""
        # pylint: disable=too-many-branches
        self.id_string = "{0:06x}:{1}".format(self.id_combined, self.unitcode)
        if self.subtype in self.TYPES:
            self.type_string = self.TYPES[self.subtype]
        else:
            # Degrade nicely for yet unknown subtypes
            self.type_string = self._UNKNOWN_TYPE.format(self.packettype,
                                                         self.subtype)
        if self.cmnd is not None:
            if self.subtype == 0x00 and self.cmnd in self.COMMANDS_00:
                self.cmnd_string = self.COMMANDS_00[self.cmnd]
            elif self.subtype == 0x01 and self.cmnd in self.COMMANDS_01:
                self.cmnd_string = self.COMMANDS_01[self.cmnd]
            elif self.subtype == 0x02 and self.cmnd in self.COMMANDS_02_04_0F:
                self.cmnd_string = self.COMMANDS_02_04_0F[self.cmnd]
            elif self.subtype == 0x03 and self.cmnd in self.COMMANDS_03:
                self.cmnd_string = self.COMMANDS_03[self.cmnd]
            elif self.subtype == 0x04 and self.cmnd in self.COMMANDS_02_04_0F:
                self.cmnd_string = self.COMMANDS_02_04_0F[self.cmnd]
            elif self.subtype >= 0x05 and self.cmnd in self.COMMANDS_XX:
                self.cmnd_string = self.COMMANDS_XX[self.cmnd]
            elif self.subtype >= 0x0f and self.cmnd in self.COMMANDS_02_04_0F:
                self.cmnd_string = self.COMMANDS_02_04_0F[self.cmnd]
            else:
                self.cmnd_string = self._UNKNOWN_CMND.format(self.cmnd)

###############################################################################
# Lighting6 class
###############################################################################


class Lighting6(Packet):
    """
    Data class for the Lighting6 packet type
    """

    TYPES = {0x00: 'Blyss'}
    """
    Mapping of numeric subtype values to strings, used in type_string
    """

    COMMANDS = {0x00: 'On',
                0x01: 'Off',
                0x02: 'Group on',
                0x03: 'Group off'}
    """
    Mapping of command numeric values to strings, used for cmnd_string
    """

    def __str__(self):
        return ("Lighting6 [subtype={0}, seqnbr={1}, id={2}, cmnd={3}, " +
                "cmndseqnbr={4}, rssi={5}]") \
            .format(self.type_string, self.seqnbr, self.id_string,
                    self.cmnd_string, self.cmndseqnbr, self.rssi)

    def __init__(self):
        """Constructor"""
        super().__init__()
        self.id1 = None
        self.id2 = None
        self.id_combined = None
        self.groupcode = None
        self.unitcode = None
        self.cmnd = None
        self.cmndseqnbr = None
        self.rfu = None
        self.level = None
        self.cmnd_string = None

    def parse_id(self, subtype, id_string):
        """Parse a string id into individual components"""
        try:
            self.packettype = 0x15
            self.subtype = subtype
            self.id_combined = int(id_string[:4], 16)
            self.id1 = self.id_combined >> 8 & 0xff
            self.id2 = self.id_combined & 0xff
            self.groupcode = ord(id_string[5])
            self.unitcode = int(id_string[6:])
            self._set_strings()
        except ValueError as exc:
            raise ValueError("Invalid id_string") from exc
        if self.id_string != id_string:
            raise ValueError("Invalid id_string")

    def load_receive(self, data):
        """Load data from a bytearray"""
        self.data = data
        self.packetlength = data[0]
        self.packettype = data[1]
        self.subtype = data[2]
        self.seqnbr = data[3]
        self.id1 = data[4]
        self.id2 = data[5]
        self.id_combined = (self.id1 << 8) + self.id2
        self.groupcode = data[6]
        self.unitcode = data[7]
        self.cmnd = data[8]
        self.cmndseqnbr = data[9]
        self.rfu = data[10]
        self.rssi_byte = data[11]
        self.rssi = self.rssi_byte >> 4
        self._set_strings()

    def set_transmit(self, subtype, seqnbr, id_combined, groupcode, unitcode,
                     cmnd, cmndseqnbr):
        """Load data from individual data fields"""
        self.packetlength = 0x0b
        self.packettype = 0x15
        self.subtype = subtype
        self.seqnbr = seqnbr
        self.id_combined = id_combined
        self.id1 = id_combined >> 8 & 0xff
        self.id2 = id_combined & 0xff
        self.groupcode = groupcode
        self.unitcode = unitcode
        self.cmnd = cmnd
        self.cmndseqnbr = cmndseqnbr
        self.rfu = 0
        self.rssi_byte = 0
        self.rssi = 0
        self.data = bytearray([self.packetlength, self.packettype,
                               self.subtype, self.seqnbr, self.id1, self.id2,
                               self.groupcode, self.unitcode, self.cmnd,
                               self.cmndseqnbr, self.rfu, self.rssi_byte])
        self._set_strings()

    def _set_strings(self):
        """Translate loaded numeric values into convenience strings"""
        self.id_string = "{0:04x}:{1}{2}".format(self.id_combined,
                                                 chr(self.groupcode),
                                                 self.unitcode)
        if self.subtype in self.TYPES:
            self.type_string = self.TYPES[self.subtype]
        else:
            # Degrade nicely for yet unknown subtypes
            self.type_string = self._UNKNOWN_TYPE.format(self.packettype,
                                                         self.subtype)
        if self.cmnd is not None:
            if self.cmnd in self.COMMANDS:
                self.cmnd_string = self.COMMANDS[self.cmnd]
            else:
                self.cmnd_string = self._UNKNOWN_CMND.format(self.cmnd)


###############################################################################
# SensorPacket class
###############################################################################

class SensorPacket(Packet):
    """
    Abstract superclass for all sensor related packets
    """

    HUMIDITY_TYPES = {0x00: 'dry',
                      0x01: 'comfort',
                      0x02: 'normal',
                      0x03: 'wet',
                      -1: 'unknown humidity'}
    """
    Mapping of humidity types to string
    """

    FORECAST_TYPES = {0x00: 'no forecast available',
                      0x01: 'sunny',
                      0x02: 'partly cloudy',
                      0x03: 'cloudy',
                      0x04: 'rain',
                      -1: 'unknown forecast'}
    """
    Mapping of forecast types to string
    """


###############################################################################
# Temp class
###############################################################################

class Temp(SensorPacket):
    """
    Data class for the Temp1 packet type
    """

    TYPES = {0x01: 'THR128/138, THC138',
             0x02: 'THC238/268,THN132,THWR288,THRN122,THN122,AW129/131',
             0x03: 'THWR800',
             0x04: 'RTHN318',
             0x05: 'La Crosse TX2, TX3, TX4, TX17',
             0x06: 'TS15C',
             0x07: 'Viking 02811',
             0x08: 'La Crosse WS2300',
             0x09: 'RUBiCSON',
             0x0A: 'TFA 30.3133',
             0x0B: 'WT0122'}
    """
    Mapping of numeric subtype values to strings, used in type_string
    """

    def __str__(self):
        return ("Temp [subtype={0}, seqnbr={1}, id={2}, temp={3}, " +
                "battery={4}, rssi={5}]") \
            .format(self.type_string, self.seqnbr, self.id_string,
                    self.temp, self.battery, self.rssi)

    def __init__(self):
        """Constructor"""
        super().__init__()
        self.id1 = None
        self.id2 = None
        self.temphigh = None
        self.templow = None
        self.temp = None
        self.battery = None

    def load_receive(self, data):
        """Load data from a bytearray"""
        self.data = data
        self.packetlength = data[0]
        self.packettype = data[1]
        self.subtype = data[2]
        self.seqnbr = data[3]
        self.id1 = data[4]
        self.id2 = data[5]
        self.temphigh = data[6]
        self.templow = data[7]
        self.temp = float(((self.temphigh & 0x7f) << 8) + self.templow) / 10
        if self.temphigh >= 0x80:
            self.temp = -1 * self.temp
        self.rssi_byte = data[8]
        self.battery = self.rssi_byte & 0x0f
        self.rssi = self.rssi_byte >> 4
        self._set_strings()

    def _set_strings(self):
        """Translate loaded numeric values into convenience strings"""
        self.id_string = "{0:02x}:{1:02x}".format(self.id1, self.id2)
        if self.subtype in self.TYPES:
            self.type_string = self.TYPES[self.subtype]
        else:
            # Degrade nicely for yet unknown subtypes
            self.type_string = self._UNKNOWN_TYPE.format(self.packettype,
                                                         self.subtype)


###############################################################################
# Bbq class
###############################################################################

class Bbq(SensorPacket):
    """
    Data class for the Temp1 packet type
    """

    TYPES = {0x01: 'BBQ1 - Maverick ET-732'}
    """
    Mapping of numeric subtype values to strings, used in type_string
    """

    def __str__(self):
        return ("Bbq [subtype={0}, seqnbr={1}, id={2}, temp1={3}, " +
                "temp2={4}, battery={5}, rssi={6}]") \
            .format(self.type_string, self.seqnbr, self.id_string,
                    self.temp1, self.temp2, self.battery, self.rssi)

    def __init__(self):
        """Constructor"""
        super().__init__()
        self.id1 = None
        self.id2 = None
        self.id3 = None
        self.id_combined = None
        self.temp1 = None
        self.temp2 = None
        self.battery = None

    def load_receive(self, data):
        """Load data from a bytearray"""
        self.data = data
        self.packetlength = data[0]
        self.packettype = data[1]
        self.subtype = data[2]
        self.seqnbr = data[3]
        self.id1 = data[4]
        self.id2 = data[5]
        self.id3 = data[6]
        self.id_combined = (self.id1 << 16) + (self.id2 << 8) + self.id3
        self.temp1 = data[7]
        self.temp2 = data[9]
        self.rssi_byte = data[10]
        self.battery = self.rssi_byte & 0x0f
        self.rssi = self.rssi_byte >> 4
        self._set_strings()

    def _set_strings(self):
        """Translate loaded numeric values into convenience strings"""
        self.id_string = "{0:06x}:{1}".format(self.id_combined,
                                              self.packettype)
        if self.subtype in self.TYPES:
            self.type_string = self.TYPES[self.subtype]
        else:
            # Degrade nicely for yet unknown subtypes
            self.type_string = self._UNKNOWN_TYPE.format(self.packettype,
                                                         self.subtype)


###############################################################################
# Humid class
###############################################################################

class Humid(SensorPacket):
    """
    Data class for the Humid packet type
    """

    TYPES = {0x01: 'LaCrosse TX3',
             0x02: 'LaCrosse WS2300',
             0x03: 'Inovalley S80'}
    """
    Mapping of numeric subtype values to strings, used in type_string
    """

    def __str__(self):
        return ("Humid [subtype={0}, seqnbr={1}, id={2}, " +
                "humidity={3}, humidity_status={4}, battery={5}, rssi={6}]") \
            .format(self.type_string, self.seqnbr, self.id_string,
                    self.humidity, self.humidity_status,
                    self.battery, self.rssi)

    def __init__(self):
        """Constructor"""
        super().__init__()
        self.id1 = None
        self.id2 = None
        self.humidity = None
        self.humidity_status = None
        self.humidity_status_string = None
        self.battery = None

    def load_receive(self, data):
        """Load data from a bytearray"""
        self.data = data
        self.packetlength = data[0]
        self.packettype = data[1]
        self.subtype = data[2]
        self.seqnbr = data[3]
        self.id1 = data[4]
        self.id2 = data[5]
        self.humidity = data[6]
        self.humidity_status = data[7]
        self.rssi_byte = data[8]
        self.battery = self.rssi_byte & 0x0f
        self.rssi = self.rssi_byte >> 4
        self._set_strings()

    def _set_strings(self):
        """Translate loaded numeric values into convenience strings"""
        self.id_string = "{0:02x}:{1:02x}".format(self.id1, self.id2)
        if self.subtype in self.TYPES:
            self.type_string = self.TYPES[self.subtype]
        else:
            # Degrade nicely for yet unknown subtypes
            self.type_string = self._UNKNOWN_TYPE.format(self.packettype,
                                                         self.subtype)
        if self.humidity_status in self.HUMIDITY_TYPES:
            self.humidity_status_string = \
                self.HUMIDITY_TYPES[self.humidity_status]
        else:
            self.humidity_status_string = self.HUMIDITY_TYPES[-1]


###############################################################################
# TempHumid class
###############################################################################

class TempHumid(SensorPacket):
    """
    Data class for the TempHumid packet type
    """

    TYPES = {0x01: 'THGN122/123, THGN132, THGR122/228/238/268',
             0x02: 'THGR810, THGN800',
             0x03: 'RTGR328',
             0x04: 'THGR328',
             0x05: 'WTGR800',
             0x06: 'THGR918/928, THGRN228, THGN500',
             0x07: 'TFA TS34C, Cresta',
             0x08: 'WT260,WT260H,WT440H,WT450,WT450H',
             0x09: 'Viking 02035,02038',
             0x0A: 'Rubicson',
             0x0B: 'EW109',
             0x0C: 'Imagintronix',
             0x0D: 'Alecto WS1700',
             0x0E: 'Alecto'}
    """
    Mapping of numeric subtype values to strings, used in type_string
    """

    def __str__(self):
        return ("TempHumid [subtype={0}, seqnbr={1}, id={2}, temp={3}, " +
                "humidity={4}, humidity_status={5}, battery={6}, rssi={7}]") \
            .format(self.type_string, self.seqnbr, self.id_string,
                    self.temp, self.humidity, self.humidity_status,
                    self.battery, self.rssi)

    def __init__(self):
        """Constructor"""
        super().__init__()
        self.id1 = None
        self.id2 = None
        self.temphigh = None
        self.templow = None
        self.temp = None
        self.humidity = None
        self.humidity_status = None
        self.humidity_status_string = None
        self.battery = None

    def load_receive(self, data):
        """Load data from a bytearray"""
        self.data = data
        self.packetlength = data[0]
        self.packettype = data[1]
        self.subtype = data[2]
        self.seqnbr = data[3]
        self.id1 = data[4]
        self.id2 = data[5]
        self.temphigh = data[6]
        self.templow = data[7]
        self.temp = float(((self.temphigh & 0x7f) << 8) + self.templow) / 10
        if self.temphigh >= 0x80:
            self.temp = -1 * self.temp
        self.humidity = data[8]
        self.humidity_status = data[9]
        self.rssi_byte = data[10]
        self.battery = self.rssi_byte & 0x0f
        self.rssi = self.rssi_byte >> 4
        self._set_strings()

    def _set_strings(self):
        """Translate loaded numeric values into convenience strings"""
        self.id_string = "{0:02x}:{1:02x}".format(self.id1, self.id2)
        if self.subtype in self.TYPES:
            self.type_string = self.TYPES[self.subtype]
        else:
            # Degrade nicely for yet unknown subtypes
            self.type_string = self._UNKNOWN_TYPE.format(self.packettype,
                                                         self.subtype)
        if self.humidity_status in self.HUMIDITY_TYPES:
            self.humidity_status_string = \
                self.HUMIDITY_TYPES[self.humidity_status]
        else:
            self.humidity_status_string = self.HUMIDITY_TYPES[-1]


###############################################################################
# Baro class
###############################################################################

class Baro(SensorPacket):
    """
    Data class for the Baro packet type
    """

    TYPES = {}
    """
    Mapping of numeric subtype values to strings, used in type_string
    """

    def __str__(self):
        return ("Baro [subtype={0}, seqnbr={1}, id={2}, baro={3}, " +
                "forecast={4}, battery={5}, rssi={6}]") \
            .format(self.type_string, self.seqnbr, self.id_string, self.baro,
                    self.forecast, self.battery, self.rssi)

    def __init__(self):
        """Constructor"""
        super().__init__()
        self.id1 = None
        self.id2 = None
        self.baro1 = None
        self.baro2 = None
        self.baro = None
        self.forecast = None
        self.forecast_string = None
        self.battery = None

    def load_receive(self, data):
        """Load data from a bytearray"""
        self.data = data
        self.packetlength = data[0]
        self.packettype = data[1]
        self.subtype = data[2]
        self.seqnbr = data[3]
        self.id1 = data[4]
        self.id2 = data[5]
        self.baro1 = data[6]
        self.baro2 = data[7]
        self.baro = (self.baro1 << 8) + self.baro2
        self.forecast = data[8]
        self.rssi_byte = data[9]
        self.battery = self.rssi_byte & 0x0f
        self.rssi = self.rssi_byte >> 4
        self._set_strings()

    def _set_strings(self):
        """Translate loaded numeric values into convenience strings"""
        self.id_string = "{0:02x}:{1:02x}".format(self.id1, self.id2)
        if self.subtype in self.TYPES:
            self.type_string = self.TYPES[self.subtype]
        else:
            # Degrade nicely for yet unknown subtypes
            self.type_string = self._UNKNOWN_TYPE.format(self.packettype,
                                                         self.subtype)
        if self.forecast in self.FORECAST_TYPES:
            self.forecast_string = self.FORECAST_TYPES[self.forecast]
        else:
            self.forecast_string = self.FORECAST_TYPES[-1]


###############################################################################
# RFXMeter class
###############################################################################

class RfxMeter(SensorPacket):
    """
    Data class for the RFXMeter packet type
    """

    TYPES = {0x00: 'RFXMeter Count',
             0x01: 'RFXMeter Interval',
             0x02: 'RFXMeter Calibration',
             0x03: 'RFXMeter Address',
             0x04: 'RFXMeter Counter reset',
             0x0B: 'RFXMeter Counter set',
             0x0C: 'RFXMeter Set interval',
             0x0D: 'RFXMeter Set calibration',
             0x0E: 'RFXMeter Set Address',
             0x0F: 'RFXMeter Ident'}

    """
    Mapping of numeric subtype values to strings, used in type_string
    """

    def __str__(self):
        return ("RFXMeter [subtype={0}, seqnbr={1}, id={2}, value3={3}, " +
                "value2={4}, value1={5}, value={6}, rssi={7}]") \
            .format(self.type_string, self.seqnbr, self.id_string,
                    self.value3, self.value2,
                    self.value1, self.value, self.rssi)

    def __init__(self):
        """Constructor"""
        super().__init__()
        self.idbyte = None
        self.value = None
        self.value3 = None
        self.value2 = None
        self.value1 = None
        self.type_string = None

    def load_receive(self, data):
        """Load data from a bytearray"""
        self.data = data
        self.packetlength = data[0]
        self.packettype = data[1]
        self.subtype = data[2]
        self.seqnbr = data[3]
        self.idbyte = data[4]
        self.value3 = data[7]
        self.value2 = data[8]
        self.value1 = data[9]
        self.value = (self.value3 << 16) + (self.value2 << 8) + self.value1
        self.rssi_byte = data[10]
        self.rssi = self.rssi_byte >> 4
        self._set_strings()

    def _set_strings(self):
        """Translate loaded numeric values into convenience strings"""
        self.id_string = "{0:02x}".format(self.idbyte)
        if self.subtype in self.TYPES:
            self.type_string = self.TYPES[self.subtype]
        else:
            # Degrade nicely for yet unknown subtypes
            self.type_string = self._UNKNOWN_TYPE.format(self.packettype,
                                                         self.subtype)


###############################################################################
# TempHumidBaro class
###############################################################################

class TempHumidBaro(SensorPacket):
    """
    Data class for the TempHumidBaro packet type
    """

    TYPES = {0x01: 'BTHR918',
             0x02: 'BTHR918N, BTHR968'}
    """
    Mapping of numeric subtype values to strings, used in type_string
    """

    def __str__(self):
        return ("TempHumidBaro [subtype={0}, seqnbr={1}, id={2}, temp={3}, " +
                "humidity={4}, humidity_status={5}, baro={6}, forecast={7}, " +
                "battery={8}, rssi={9}]") \
            .format(self.type_string, self.seqnbr, self.id_string, self.temp,
                    self.humidity, self.humidity_status, self.baro,
                    self.forecast, self.battery, self.rssi)

    def __init__(self):
        """Constructor"""
        super().__init__()
        self.id1 = None
        self.id2 = None
        self.temphigh = None
        self.templow = None
        self.temp = None
        self.humidity = None
        self.humidity_status = None
        self.humidity_status_string = None
        self.baro1 = None
        self.baro2 = None
        self.baro = None
        self.forecast = None
        self.forecast_string = None
        self.battery = None

    def load_receive(self, data):
        """Load data from a bytearray"""
        self.data = data
        self.packetlength = data[0]
        self.packettype = data[1]
        self.subtype = data[2]
        self.seqnbr = data[3]
        self.id1 = data[4]
        self.id2 = data[5]
        self.temphigh = data[6]
        self.templow = data[7]
        self.temp = float(((self.temphigh & 0x7f) << 8) + self.templow) / 10
        if self.temphigh >= 0x80:
            self.temp = -1 * self.temp
        self.humidity = data[8]
        self.humidity_status = data[9]
        self.baro1 = data[10]
        self.baro2 = data[11]
        self.baro = (self.baro1 << 8) + self.baro2
        self.forecast = data[12]
        self.rssi_byte = data[13]
        self.battery = self.rssi_byte & 0x0f
        self.rssi = self.rssi_byte >> 4
        self._set_strings()

    def _set_strings(self):
        """Translate loaded numeric values into convenience strings"""
        self.id_string = "{0:02x}:{1:02x}".format(self.id1, self.id2)
        if self.subtype in self.TYPES:
            self.type_string = self.TYPES[self.subtype]
        else:
            # Degrade nicely for yet unknown subtypes
            self.type_string = self._UNKNOWN_TYPE.format(self.packettype,
                                                         self.subtype)
        if self.humidity_status in self.HUMIDITY_TYPES:
            self.humidity_status_string = \
                self.HUMIDITY_TYPES[self.humidity_status]
        else:
            self.humidity_status_string = self.HUMIDITY_TYPES[-1]
        if self.forecast in self.FORECAST_TYPES:
            self.forecast_string = self.FORECAST_TYPES[self.forecast]
        else:
            self.forecast_string = self.FORECAST_TYPES[-1]


###############################################################################
# Rain class
###############################################################################

class Rain(SensorPacket):
    """
    Data class for the rain packet type
    """
    TYPES = {
        0x01: 'RGR126/682/918',
        0x02: 'PCR800',
        0x03: 'TFA',
        0x04: 'UPM RG700',
        0x05: 'WS2300',
        0x06: 'La Crosse TX5',
        0x07: 'Alecto'}

    def __str__(self):
        return ("Rain [subtype={0}, seqnbr={1}, id={2}, rainrate={3}, " +
                "raintotal={4}, battery={5}, rssi={6}]") \
            .format(self.type_string, self.seqnbr, self.id_string,
                    self.rainrate, self.raintotal, self.battery, self.rssi)

    def __init__(self):
        """Constructor"""
        super().__init__()
        self.id1 = None
        self.id2 = None
        self.rainrate1 = None
        self.rainrate2 = None
        self.rainrate = None
        self.raintotal1 = None
        self.raintotal2 = None
        self.raintotal3 = None
        self.raintotal = None
        self.battery = None

    def load_receive(self, data):
        """Load data from a bytearray"""
        self.data = data
        self.packetlength = data[0]
        self.packettype = data[1]
        self.subtype = data[2]
        self.seqnbr = data[3]
        self.id1 = data[4]
        self.id2 = data[5]
        self.rainrate1 = data[6]
        self.rainrate2 = data[7]
        self.rainrate = (self.rainrate1 << 8) + self.rainrate2
        if self.subtype == 2:
            self.rainrate = float(self.rainrate) / 100
        self.raintotal1 = data[8]
        self.raintotal2 = data[9]
        self.raintotal3 = data[10]
        self.raintotal = float((self.raintotal1 << 16) +
                               (self.raintotal2 << 8) +
                               self.raintotal3) / 10
        self.rssi_byte = data[11]
        self.battery = self.rssi_byte & 0x0f
        self.rssi = self.rssi_byte >> 4
        self._set_strings()

    def _set_strings(self):
        """Translate loaded numeric values into convenience strings"""
        self.id_string = "{0:02x}:{1:02x}".format(self.id1, self.id2)
        if self.subtype in self.TYPES:
            self.type_string = self.TYPES[self.subtype]
        else:
            # Degrade nicely for yet unknown subtypes
            self.type_string = self._UNKNOWN_TYPE.format(self.packettype,
                                                         self.subtype)


###############################################################################
# TempRain class
###############################################################################

class TempRain(SensorPacket):
    """
    Data class for the TempRain packet type
    """

    TYPES = {0x01: 'TR1 - WS1200'}
    """
    Mapping of numeric subtype values to strings, used in type_string
    """

    def __str__(self):
        return ("TempRain [subtype={0}, seqnbr={1}, id={2}, temp={3}, " +
                "totalrain={4}, battery={5}, rssi={6}]") \
            .format(self.type_string, self.seqnbr, self.id_string,
                    self.temp, self.totalrain,
                    self.battery, self.rssi)

    def __init__(self):
        """Constructor"""
        super().__init__()
        self.id1 = None
        self.id2 = None
        self.temphigh = None
        self.templow = None
        self.temp = None
        self.raintotal = None
        self.battery = None

    def load_receive(self, data):
        """Load data from a bytearray"""
        self.data = data
        self.packetlength = data[0]
        self.packettype = data[1]
        self.subtype = data[2]
        self.seqnbr = data[3]
        self.id1 = data[4]
        self.id2 = data[5]
        self.temphigh = data[6]
        self.templow = data[7]
        self.temp = float(((self.temphigh & 0x7f) << 8) + self.templow) / 10
        if self.temphigh >= 0x80:
            self.temp = -1 * self.temp
        self.raintotal = float(((data[8] & 0x7f) << 8) + data[9]) / 10
        self.rssi_byte = data[10]
        self.battery = self.rssi_byte & 0x0f
        self.rssi = self.rssi_byte >> 4
        self._set_strings()

    def _set_strings(self):
        """Translate loaded numeric values into convenience strings"""
        self.id_string = "{0:02x}:{1:02x}".format(self.id1, self.id2)
        if self.subtype in self.TYPES:
            self.type_string = self.TYPES[self.subtype]
        else:
            # Degrade nicely for yet unknown subtypes
            self.type_string = self._UNKNOWN_TYPE.format(self.packettype,
                                                         self.subtype)


###############################################################################
# Wind class
###############################################################################


class Wind(SensorPacket):
    """
    Data class for the Wind packet type
    """

    TYPES = {0x01: 'WTGR800',
             0x02: 'WGR800',
             0x03: 'STR918, WGR918, WGR928',
             0x04: 'TFA',
             0x05: 'UPM WDS500',
             0x06: 'WS2300',
             0x07: 'Alecto WS4500'}
    """
    Mapping of numeric subtype values to strings, used in type_string
    """

    def __str__(self):
        return ("Wind [subtype={0}, seqnbr={1}, id={2}, direction={3}, " +
                "average_speed={4}, gust={5}, temperature={6}, chill={7}, " +
                "battery={8}, rssi={9}]") \
            .format(self.type_string, self.seqnbr, self.id_string,
                    self.direction, self.average_speed, self.gust,
                    self.temperature, self.chill, self.battery, self.rssi)

    def __init__(self):
        """Constructor"""
        super().__init__()
        self.id1 = None
        self.id2 = None
        self.direction = None
        self.average_speed = None
        self.gust = None
        self.temperature = None
        self.temphigh = None
        self.templow = None
        self.chill = None
        self.chillhigh = None
        self.chilllow = None
        self.battery = None
        self.rssi = None

    def load_receive(self, data):
        """Load data from a bytearray"""
        self.data = data
        self.packetlength = data[0]
        self.packettype = data[1]
        self.subtype = data[2]
        self.seqnbr = data[3]
        self.id1 = data[4]
        self.id2 = data[5]
        self.direction = data[6] * 256 + data[7]
        self.average_speed = (data[8] * 256.0 + data[9]) / 10.0
        self.gust = (data[10] * 256.0 + data[11]) / 10.0
        if self.subtype not in (0x06, 0x07):
            self.temphigh = data[12]
            self.templow = data[13]
            self.temperature = float(((self.temphigh & 0x7f) << 8) +
                                     self.templow) / 10
            if self.temphigh >= 0x80:
                self.temperature = -1 * self.temperature
            self.chillhigh = data[14]
            self.chilllow = data[15]
            self.chill = float(((self.chillhigh & 0x7f) << 8) +
                               self.chilllow) / 10
            if self.chillhigh >= 0x80:
                self.chill = -1 * self.chill
        if self.subtype == 0x03:
            self.battery = data[16] + 1 * 10
        else:
            self.rssi_byte = data[16]
            self.battery = self.rssi_byte & 0x0f
            self.rssi = self.rssi_byte >> 4
        self._set_strings()

    def _set_strings(self):
        """Translate loaded numeric values into convenience strings"""
        self.id_string = "{0:02x}:{1:02x}".format(self.id1, self.id2)
        if self.subtype in self.TYPES:
            self.type_string = self.TYPES[self.subtype]
        else:
            # Degrade nicely for yet unknown subtypes
            self.type_string = self._UNKNOWN_TYPE.format(self.packettype,
                                                         self.subtype)


###############################################################################
# UV class
###############################################################################

class UV(SensorPacket):
    """
    Data class for the uv packet type
    """
    TYPES = {0x01: 'UVN128, UV138',
             0x02: 'UVN800',
             0x03: 'TFA'}

    def __str__(self):
        return ("UV [subtype={0}, seqnbr={1}, id={2}, uv={3}," +
                " battery={5}, rssi={6}]") \
            .format(self.type_string, self.seqnbr, self.id_string,
                    self.uvi, self.battery, self.rssi)

    def __init__(self):
        """Constructor"""
        super().__init__()
        self.id1 = None
        self.id2 = None
        self.uvi = None
        self.battery = None

    def load_receive(self, data):
        """Load data from a bytearray"""
        self.data = data
        self.packetlength = data[0]
        self.packettype = data[1]
        self.subtype = data[2]
        self.seqnbr = data[3]
        self.id1 = data[4]
        self.id2 = data[5]
        self.uvi = float(data[6]) / 10
        self.rssi_byte = data[9]
        self.battery = self.rssi_byte & 0x0f
        self.rssi = self.rssi_byte >> 4
        self._set_strings()

    def _set_strings(self):
        """Translate loaded numeric values into convenience strings"""
        self.id_string = "{0:02x}:{1:02x}".format(self.id1, self.id2)
        if self.subtype in self.TYPES:
            self.type_string = self.TYPES[self.subtype]
        else:
            # Degrade nicely for yet unknown subtypes
            self.type_string = self._UNKNOWN_TYPE.format(self.packettype,
                                                         self.subtype)


###############################################################################
# Energy1 class
###############################################################################


class Energy1(SensorPacket):
    """
    Data class for the Energy "ELEC1" packet type
    """

    TYPES = {0x01: 'ELEC1, Electrisave'}

    def __str__(self):
        return ("Energy1 [subtype={0}, seqnbr={1}, id={2}, count={3}, " +
                "current_amps1={4}, current_amps2={5}, current_amps3={6}, " +
                "battery={7}, rssi={8}]") \
            .format(self.type_string, self.seqnbr, self.id_string,
                    self.count, self.currentamps1, self.currentamps2,
                    self.currentamps3, self.battery, self.rssi)

    def __init__(self):
        """Constructor"""
        super().__init__()
        self.id1 = None
        self.id2 = None
        self.count = None
        self.currentamps1 = None
        self.currentamps2 = None
        self.currentamps3 = None
        self.battery = None
        self.rssi = None

    def load_receive(self, data):
        """Load data from a bytearray"""
        self.data = data
        self.packetlength = data[0]
        self.packettype = data[1]
        self.subtype = data[2]
        self.seqnbr = data[3]
        self.id1 = data[4]
        self.id2 = data[5]
        self.count = data[6]
        self.currentamps1 = float((data[7] << 8) + data[8]) / 10
        self.currentamps2 = float((data[9] << 8) + data[10]) / 10
        self.currentamps3 = float((data[11] << 8) + data[12]) / 10
        self.rssi_byte = data[13]
        self.battery = self.rssi_byte & 0x0f
        self.rssi = self.rssi_byte >> 4
        self._set_strings()

    def _set_strings(self):
        """Translate loaded numeric values into convenience strings"""
        self.id_string = "{0:02x}:{1:02x}".format(self.id1, self.id2)
        if self.subtype in self.TYPES:
            self.type_string = self.TYPES[self.subtype]
        else:
            # Degrade nicely for yet unknown subtypes
            self.type_string = self._UNKNOWN_TYPE.format(self.packettype,
                                                         self.subtype)


###############################################################################
# Energy class
###############################################################################


class Energy(SensorPacket):
    """
    Data class for the Energy packet type
    """

    TYPES = {0x01: 'ELEC2, CM119/160',
             0x02: 'ELEC3, CM180'}
    """
    Mapping of numeric subtype values to strings, used in type_string
    """

    def __str__(self):
        return ("Energy [subtype={0}, seqnbr={1}, id={2}, count={3}, " +
                "current_watts={4}, total_watts={5}" +
                "battery={6}, rssi={7}]") \
            .format(self.type_string, self.seqnbr, self.id_string,
                    self.count, self.currentwatt, self.totalwatts,
                    self.battery, self.rssi)

    def __init__(self):
        """Constructor"""
        super().__init__()
        self.id1 = None
        self.id2 = None
        self.count = None
        self.currentwatt = None
        self.totalwatts = None
        self.battery = None
        self.rssi = None

    def load_receive(self, data):
        """Load data from a bytearray"""
        self.data = data
        self.packetlength = data[0]
        self.packettype = data[1]
        self.subtype = data[2]
        self.seqnbr = data[3]
        self.id1 = data[4]
        self.id2 = data[5]
        self.count = data[6]
        self.currentwatt = ((data[7] * pow(2, 24)) + (data[8] << 16) +
                            (data[9] << 8) + data[10])
        self.totalwatts = ((data[11] * pow(2, 40)) + (data[12] * pow(2, 32)) +
                           (data[13] * pow(2, 24)) + (data[14] << 16) +
                           (data[15] << 8) + data[16]) / 223.666

        if self.subtype == 0x03:
            self.battery = data[17] + 1 * 10
        else:
            self.rssi_byte = data[17]
            self.battery = self.rssi_byte & 0x0f
            self.rssi = self.rssi_byte >> 4
        self._set_strings()

    def _set_strings(self):
        """Translate loaded numeric values into convenience strings"""
        self.id_string = "{0:02x}:{1:02x}".format(self.id1, self.id2)
        if self.subtype in self.TYPES:
            self.type_string = self.TYPES[self.subtype]
        else:
            # Degrade nicely for yet unknown subtypes
            self.type_string = self._UNKNOWN_TYPE.format(self.packettype,
                                                         self.subtype)


###############################################################################
# Energy4 class
###############################################################################


class Energy4(SensorPacket):
    """
    Data class for the Energy "ELEC4" packet type
    """

    TYPES = {0x01: 'ELEC4, CM180i'}
    """
    Mapping of numeric subtype values to strings, used in type_string
    """

    def __str__(self):
        return ("Energy4 [subtype={0}, seqnbr={1}, id={2}, count={3}, " +
                "current_amps1={4}, current_amps2={5}, current_amps3={6}, " +
                "total_watts={7}, battery={8}, rssi={9}]") \
            .format(self.type_string, self.seqnbr, self.id_string,
                    self.count, self.currentamps1, self.currentamps2,
                    self.currentamps3, self.totalwatthours, self.battery,
                    self.rssi)

    def __init__(self):
        """Constructor"""
        super().__init__()
        self.id1 = None
        self.id2 = None
        self.count = None
        self.currentamps1 = None
        self.currentamps2 = None
        self.currentamps3 = None
        self.totalwatthours = None
        self.battery = None
        self.rssi = None

    def load_receive(self, data):
        """Load data from a bytearray"""
        self.data = data
        self.packetlength = data[0]
        self.packettype = data[1]
        self.subtype = data[2]
        self.seqnbr = data[3]
        self.id1 = data[4]
        self.id2 = data[5]
        self.count = data[6]
        self.currentamps1 = float((data[7] << 8) + data[8]) / 10
        self.currentamps2 = float((data[9] << 8) + data[10]) / 10
        self.currentamps3 = float((data[11] << 8) + data[12]) / 10
        self.totalwatthours = ((data[13] * pow(2, 40)) +
                               (data[14] * pow(2, 32)) +
                               (data[15] * pow(2, 24)) + (data[16] << 16) +
                               (data[17] << 8) + data[18]) / 223.666
        self.rssi_byte = data[19]
        self.battery = self.rssi_byte & 0x0f
        self.rssi = self.rssi_byte >> 4
        self._set_strings()

    def _set_strings(self):
        """Translate loaded numeric values into convenience strings"""
        self.id_string = "{0:02x}:{1:02x}".format(self.id1, self.id2)
        if self.subtype in self.TYPES:
            self.type_string = self.TYPES[self.subtype]
        else:
            # Degrade nicely for yet unknown subtypes
            self.type_string = self._UNKNOWN_TYPE.format(self.packettype,
                                                         self.subtype)


###############################################################################
# Energy5 class
###############################################################################


class Energy5(SensorPacket):
    """
    Data class for the Energy "ELEC5" packet type
    """

    TYPES = {0x01: 'ELEC5, Revolt'}
    """
    Mapping of numeric subtype values to strings, used in type_string
    """

    def __str__(self):
        return ("Energy5 [subtype={0}, seqnbr={1}, id={2}, voltage={3}, " +
                "current_amps={4}, current_watts={5}, total_watts={6}, " +
                "powerfactor={7}, frequency={8}, rssi={9}]") \
            .format(self.type_string, self.seqnbr, self.id_string,
                    self.voltage, self.currentamps, self.currentwatt,
                    self.totalwatthours, self.powerfactor, self.frequency,
                    self.rssi)

    def __init__(self):
        """Constructor"""
        super().__init__()
        self.id1 = None
        self.id2 = None
        self.voltage = None
        self.currentamps = None
        self.currentwatt = None
        self.totalwatthours = None
        self.powerfactor = None
        self.frequency = None
        self.rssi = None

    def load_receive(self, data):
        """Load data from a bytearray"""
        self.data = data
        self.packetlength = data[0]
        self.packettype = data[1]
        self.subtype = data[2]
        self.seqnbr = data[3]
        self.id1 = data[4]
        self.id2 = data[5]
        self.voltage = data[6]
        self.currentamps = float((data[7] << 8) + data[8]) / 100
        self.currentwatt = float((data[9] << 8) + data[10]) / 10
        self.totalwatthours = float((data[11] << 8) + data[12]) * 10
        self.powerfactor = float(data[13]) / 100
        self.frequency = float(data[14])
        self.rssi_byte = data[15]
        self.rssi = self.rssi_byte >> 4
        self._set_strings()

    def _set_strings(self):
        """Translate loaded numeric values into convenience strings"""
        self.id_string = "{0:02x}:{1:02x}".format(self.id1, self.id2)
        if self.subtype in self.TYPES:
            self.type_string = self.TYPES[self.subtype]
        else:
            # Degrade nicely for yet unknown subtypes
            self.type_string = self._UNKNOWN_TYPE.format(self.packettype,
                                                         self.subtype)


###############################################################################
# Chime class
###############################################################################


class Chime(Packet):
    """
    Data class for the Chime packet type
    """

    TYPES = {0x00: 'Byron SX',
             0x01: 'Byron MP001',
             0x02: 'Select Plus',
             0x03: 'Select Plus 3',
             0x04: 'Envivo'}
    """
    Mapping of numeric subtype values to strings, used in type_string
    """

    def __str__(self):
        return ("Chime [subtype={0}, seqnbr={1}, id={2}, sound={3}, " +
                "battery={6}, rssi={7}]") \
            .format(self.type_string, self.seqnbr, self.id_string,
                    self.sound, self.battery, self.rssi)

    def __init__(self):
        """Constructor"""
        super().__init__()
        self.id1 = None
        self.id2 = None
        self.sound = None
        self.battery = None
        self.rssi = None
        self.cmnd = None
        self.cmnd_string = None

    def parse_id(self, subtype, id_string):
        """Parse a string id into individual components"""
        try:
            self.packettype = 0x16
            self.subtype = subtype
            self.id1 = int(id_string[:2], 16)
            self.id2 = int(id_string[3:5], 16)
            self._set_strings()
        except ValueError as exc:
            raise ValueError("Invalid id_string") from exc
        if self.id_string != id_string:
            raise ValueError("Invalid id_string")

    def load_receive(self, data):
        """Load data from a bytearray"""
        self.data = data
        self.packetlength = data[0]
        self.packettype = data[1]
        self.subtype = data[2]
        self.seqnbr = data[3]
        self.id1 = data[4]
        self.id2 = data[5]
        self.sound = data[6]
        self.rssi_byte = data[7]
        self.battery = self.rssi_byte & 0x0f
        self.rssi = self.rssi_byte >> 4
        self._set_strings()

    def set_transmit(self, subtype, seqnbr, id1, id2, sound):
        """Load data from individual data fields"""
        self.packetlength = 0x07
        self.packettype = 0x16
        self.subtype = subtype
        self.seqnbr = seqnbr
        self.id1 = id1
        self.id2 = id2
        self.sound = sound
        self.battery = 0
        self.rssi = 0
        self.rssi_byte = (self.rssi << 4) | self.battery
        self.data = bytearray([self.packetlength, self.packettype,
                               self.subtype, self.seqnbr,
                               self.id1, self.id2, self.sound,
                               self.rssi_byte])

    def _set_strings(self):
        """Translate loaded numeric values into convenience strings"""
        self.id_string = "{0:02x}:{1:02x}".format(self.id1, self.id2)
        if self.subtype in self.TYPES:
            self.type_string = self.TYPES[self.subtype]
        else:
            # Degrade nicely for yet unknown subtypes
            self.type_string = self._UNKNOWN_TYPE.format(self.packettype,
                                                         self.subtype)
        self.cmnd_string = "Chime"

###############################################################################
# Security1 class
###############################################################################


class Security1(SensorPacket):
    """
    Data class for the Security1 packet type
    """

    TYPES = {0x00: 'X10 Security',
             0x01: 'X10 Security Motion Detector',
             0x02: 'X10 Security Remote',
             0x03: 'KD101 Smoke Detector',
             0x04: 'Visonic Powercode Door/Window Sensor Primary Contact',
             0x05: 'Visonic Powercode Motion Detector',
             0x06: 'Visonic Codesecure',
             0x07: 'Visonic Powercode Door/Window Sensor Auxilary Contact',
             0x08: 'Meiantech',
             0x09: 'Alecto SA30 Smoke Detector',
             0x0A: 'RM174RF Smoke Detector'}
    """
    Mapping of numeric subtype values to strings, used in type_string
    """
    STATUS = {0x00: 'Normal',
              0x01: 'Normal Delayed',
              0x02: 'Alarm',
              0x03: 'Alarm Delayed',
              0x04: 'Motion',
              0x05: 'No Motion',
              0x06: 'Panic',
              0x07: 'End Panic',
              0x08: 'IR',
              0x09: 'Arm Away',
              0x0A: 'Arm Away Delayed',
              0x0B: 'Arm Home',
              0x0C: 'Arm Home Delayed',
              0x0D: 'Disarm',
              0x10: 'Light 1 Off',
              0x11: 'Light 1 On',
              0x12: 'Light 2 Off',
              0x13: 'Light 2 On',
              0x14: 'Dark Detected',
              0x15: 'Light Detected',
              0x16: 'Battery low',
              0x17: 'Pairing KD101',
              0x80: 'Normal Tamper',
              0x81: 'Normal Delayed Tamper',
              0x82: 'Alarm Tamper',
              0x83: 'Alarm Delayed Tamper',
              0x84: 'Motion Tamper',
              0x85: 'No Motion Tamper'}
    """
    Mapping of numeric status values to strings, used in type_string
    """

    def __str__(self):
        return ("Security1 [subtype={0}, seqnbr={1}, id={2}, status={3}, " +
                "battery={4}, rssi={5}]") \
            .format(self.type_string, self.seqnbr, self.id_string,
                    self.security1_status_string, self.battery, self.rssi)

    def __init__(self):
        """Constructor"""
        super().__init__()
        self.id1 = None
        self.id2 = None
        self.id3 = None
        self.id_combined = None
        self.security1_status = None
        self.battery = None
        self.rssi = None
        self.security1_status_string = 'unknown'

    def load_receive(self, data):
        """Load data from a bytearray"""
        self.data = data
        self.packetlength = data[0]
        self.packettype = data[1]
        self.subtype = data[2]
        self.seqnbr = data[3]
        self.id1 = data[4]
        self.id2 = data[5]
        self.id3 = data[6]
        self.id_combined = (self.id1 << 16) + (self.id2 << 8) + self.id3
        self.security1_status = data[7]
        self.rssi_byte = data[8]
        self.battery = self.rssi_byte & 0x0f
        self.rssi = self.rssi_byte >> 4
        self._set_strings()

    def _set_strings(self):
        """Translate loaded numeric values into convenience strings"""
        self.id_string = "{0:06x}:{1}".format(self.id_combined,
                                              self.packettype)
        if self.subtype in self.TYPES:
            self.type_string = self.TYPES[self.subtype]
        else:
            # Degrade nicely for yet unknown subtypes
            self.type_string = self._UNKNOWN_TYPE.format(self.packettype,
                                                         self.subtype)
        if self.security1_status in self.STATUS:
            self.security1_status_string = self.STATUS[self.security1_status]

###############################################################################
# Rfy class
###############################################################################


class Rfy(Packet):
    """
    Data class for the Rfy packet type
    """
    TYPES = {0x00: 'Rfy',
             0x01: 'Rfy Extended',
             0x03: 'ASA'}
    """
    Mapping of numeric subtype values to strings, used in type_string
    """

    COMMANDS = {0x00: 'Stop',
                0x01: 'Up',
                0x03: 'Down',
                0x0F: '0.5 Seconds Up',
                0x10: '0.5 Seconds Down',
                0x11: '2 Seconds Up',
                0x12: '2 Seconds Down',
                0x13: 'Enable sun automation',
                0x14: 'Disable sun automation'}
    """
    Mapping of command numeric values to strings, used for cmnd_string
    """

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "Rfy [subtype={0}, seqnbr={1}, id={2}, cmnd={3}]" \
            .format(
                self.subtype,
                self.seqnbr,
                self.id_string,
                self.cmnd_string
            )

    def __init__(self):
        """Constructor"""
        super().__init__()
        self.id1 = None
        self.id2 = None
        self.id3 = None
        self.id_combined = None
        self.unitcode = None
        self.cmnd = None
        self.cmnd_string = None

    def parse_id(self, subtype, id_string):
        """( a string id into individual components"""
        try:
            self.packettype = 0x1a
            self.subtype = subtype
            self.id_combined = int(id_string[:6], 16)
            self.id1 = self.id_combined >> 16
            self.id2 = self.id_combined >> 8 & 0xff
            self.id3 = self.id_combined & 0xff
            self.unitcode = int(id_string[7:])
            self._set_strings()
        except ValueError as exc:
            raise ValueError("Invalid id_string") from exc
        if self.id_string != id_string:
            raise ValueError("Invalid id_string")

    def load_receive(self, data):
        """Load data from a bytearray"""
        self.data = data
        self.packetlength = data[0]
        self.packettype = data[1]
        self.subtype = data[2]
        self.seqnbr = data[3]
        self.id1 = data[4]
        self.id2 = data[5]
        self.id3 = data[6]
        self.unitcode = data[7]
        if self.packetlength > 7:
            self.cmnd = data[8]

        self.id_combined = (self.id1 << 16) + (self.id2 << 8) + self.id3
        self._set_strings()

    def set_transmit(self, subtype, seqnbr, id_combined, unitcode, cmnd):
        """Load data from individual data fields"""
        self.packetlength = 0x08
        self.packettype = 0x1a
        self.subtype = subtype
        self.seqnbr = seqnbr
        self.id_combined = id_combined
        self.id1 = id_combined >> 16
        self.id2 = id_combined >> 8 & 0xff
        self.id3 = id_combined & 0xff
        self.unitcode = unitcode
        self.cmnd = cmnd
        self.data = bytearray([self.packetlength, self.packettype,
                               self.subtype, self.seqnbr,
                               self.id1, self.id2, self.id3, self.unitcode,
                               self.cmnd])

        self._set_strings()

    def _set_strings(self):
        """Translate loaded numeric values into convenience strings"""
        self.id_string = "{0:06x}:{1}".format(self.id_combined,
                                              self.unitcode)

        if self.subtype in self.TYPES:
            self.type_string = self.TYPES[self.subtype]
        else:
            # Degrade nicely for yet unknown subtypes
            self.type_string = self._UNKNOWN_TYPE.format(self.packettype,
                                                         self.subtype)

        if self.cmnd is not None:
            if self.cmnd in self.COMMANDS:
                self.cmnd_string = self.COMMANDS[self.cmnd]
            else:
                self.cmnd_string = self._UNKNOWN_CMND.format(self.cmnd)

###############################################################################
# RollerTrol class
###############################################################################


class RollerTrol(Packet):
    """
    Data class for the RollerTrol packet type
    """
    TYPES = {0x00: 'RollerTrol'}
    """
    Mapping of numeric subtype values to strings, used in type_string
    """

    COMMANDS = {0x02: 'Stop',
                0x00: 'Up',
                0x01: 'Down'}
    """
    Mapping of command numeric values to strings, used for cmnd_string
    """

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return ("RollerTrol [subtype={0}, seqnbr={1}, id={2}, cmnd={3}, " +
                "rssi={4}]") \
            .format(
                self.subtype,
                self.seqnbr,
                self.id_string,
                self.cmnd_string,
                self.rssi
            )

    def __init__(self):
        """Constructor"""
        super().__init__()
        self.id1 = None
        self.id2 = None
        self.id3 = None
        self.id_combined = None
        self.unitcode = None
        self.cmnd = None
        self.cmnd_string = None

    def parse_id(self, subtype, id_string):
        """( a string id into individual components"""
        try:
            self.packettype = 0x19
            self.subtype = subtype
            self.id_combined = int(id_string[:6], 16)
            self.id1 = self.id_combined >> 16
            self.id2 = self.id_combined >> 8 & 0xff
            self.id3 = self.id_combined & 0xff
            self.unitcode = int(id_string[7:])
            self._set_strings()
        except ValueError as exc:
            raise ValueError("Invalid id_string") from exc
        if self.id_string != id_string:
            raise ValueError("Invalid id_string")

    def load_receive(self, data):
        """Load data from a bytearray"""
        self.data = data
        self.packetlength = data[0]
        self.packettype = data[1]
        self.subtype = data[2]
        self.seqnbr = data[3]
        self.id1 = data[4]
        self.id2 = data[5]
        self.id3 = data[6]
        self.id_combined = (self.id1 << 16) + (self.id2 << 8) + self.id3
        self.unitcode = data[7]
        self.cmnd = data[8]
        self.rssi_byte = data[9]
        self.rssi = self.rssi_byte >> 4
        self._set_strings()

    def set_transmit(self, subtype, seqnbr, id_combined, unitcode, cmnd):
        """Load data from individual data fields"""
        self.packetlength = 0x09
        self.packettype = 0x19
        self.subtype = subtype
        self.seqnbr = seqnbr
        self.id_combined = id_combined
        self.id1 = id_combined >> 16
        self.id2 = id_combined >> 8 & 0xff
        self.id3 = id_combined & 0xff
        self.unitcode = unitcode
        self.cmnd = cmnd
        self.rssi_byte = 0
        self.rssi = self.rssi_byte >> 4
        self.data = bytearray([self.packetlength, self.packettype,
                               self.subtype, self.seqnbr,
                               self.id1, self.id2, self.id3, self.unitcode,
                               self.cmnd, self.rssi])

        self._set_strings()

    def _set_strings(self):
        """Translate loaded numeric values into convenience strings"""
        self.id_string = "{0:06x}:{1}".format(self.id_combined,
                                              self.unitcode)

        if self.subtype in self.TYPES:
            self.type_string = self.TYPES[self.subtype]
        else:
            # Degrade nicely for yet unknown subtypes
            self.type_string = self._UNKNOWN_TYPE.format(self.packettype,
                                                         self.subtype)

        if self.cmnd is not None:
            if self.cmnd in self.COMMANDS:
                self.cmnd_string = self.COMMANDS[self.cmnd]
            else:
                self.cmnd_string = self._UNKNOWN_CMND.format(self.cmnd)
