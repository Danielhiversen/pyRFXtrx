from unittest import TestCase

import RFXtrx


class WindTestCase(TestCase):

    def test_parse_bytes_5(self):
        data = [0x10, 0x56, 0x07, 0x05, 0x2c, 0x01, 0x00, 0x87, 0x00, 0x04, 0x00, 0x08, 0x68, 0x74, 0x20, 0x52, 0x69]
        packet = RFXtrx.lowlevel.parse(data)
        self.assertEquals(RFXtrx.lowlevel.Wind, type(packet))
        self.assertEquals(packet.type_string,'Alecto WS4500')
        self.assertEquals(packet.id_string,'2c:01')
        self.assertEquals(packet.direction, 135)
        self.assertEquals(packet.average_speed, 0.4)
        self.assertEquals(packet.gust, 0.8)
        self.assertEquals(packet.temperature, None)
        self.assertEquals(packet.chill, None)
        self.assertEquals(packet.battery, 9)
        self.assertEquals(packet.rssi, 6)


    def test_parse_bytes_6(self):
        data = [0x10, 0x56, 0x06, 0x8f, 0x4c, 0x00, 0x00, 0x43, 0x00, 0x00, 0x00, 0xf0, 0x68, 0x74, 0x20, 0x52, 0x69]
        packet = RFXtrx.lowlevel.parse(data)
        self.assertEquals(RFXtrx.lowlevel.Wind, type(packet))
        self.assertEquals(packet.type_string,'WS2300')
        self.assertEquals(packet.id_string,'4c:00')
        self.assertEquals(packet.direction, 67)
        self.assertEquals(packet.average_speed, 0.0)
        self.assertEquals(packet.gust, 24.0)
        self.assertEquals(packet.temperature, None)
        self.assertEquals(packet.chill, None)
        self.assertEquals(packet.battery, 9)
        self.assertEquals(packet.rssi, 6)
