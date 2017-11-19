from unittest import TestCase

import RFXtrx


class RfxMeterTestCase(TestCase):

    def setUp(self):
        #A 71 0 1F 21 D1 0 20 1F A4 60
        self.data = bytearray(b'\x0A\x71\x00\x1F\x21\xD1\x00\x20'
                              b'\x1F\xA4\x60')
        self.parser = RFXtrx.lowlevel.RfxMeter()

    def test_parse_bytes(self):
        rfxmeterpacket = RFXtrx.lowlevel.parse(self.data)
        self.assertEquals(RFXtrx.lowlevel.RfxMeter, type(rfxmeterpacket))
        self.assertEquals(rfxmeterpacket.type_string, 'RFXMeter Count')
        self.assertEquals(rfxmeterpacket.id_string, '21')
        self.assertEquals(rfxmeterpacket.value3, 0x20)
        self.assertEquals(rfxmeterpacket.value2, 0x1F)
        self.assertEquals(rfxmeterpacket.value1, 0xA4)
        self.assertEquals(rfxmeterpacket.value, 2105252)

    def test_validate_bytes_short(self):
        data = self.data[:1]
        rfxmeterpacket = RFXtrx.lowlevel.parse(data)
        self.assertEquals(rfxmeterpacket, None)

    def test_validate_unkown_packet_type(self):

        self.data[1] = 0xFF
        rfxmeterpacket = RFXtrx.lowlevel.parse(self.data)
        self.assertEquals(rfxmeterpacket, None)

    def test_validate_unknown_sub_type(self):

        self.data[2] = 0xEE
        rfxmeterpacket = RFXtrx.lowlevel.parse(self.data)
        self.assertEquals(rfxmeterpacket.type_string, 'Unknown type (0x71/0xee)')

    def test_equal(self):
        rfxmeterpacket = RFXtrx.lowlevel.parse(self.data)
        self.data = bytearray(b'\x0A\x71\x00\x1F\x21\xD1\x00\x20'
                              b'\x1F\xA4\x60')
        rfxmeterpacket2 = RFXtrx.lowlevel.parse(self.data)
        self.assertTrue(rfxmeterpacket == rfxmeterpacket2)
        self.assertFalse(rfxmeterpacket == None)
