from unittest import TestCase

import RFXtrx


class RfxMSensorTestCase(TestCase):

    def setUp(self):
        self.parser = RFXtrx.lowlevel.RfxMeter()

    def test_parse_temp(self):
        rfxmeterpacket = RFXtrx.lowlevel.parse(bytearray(b'\x07\x70\x00\x0E\x1B\x07\x08\x60'))
        self.assertEqual(RFXtrx.lowlevel.RfxSensor, type(rfxmeterpacket))
        self.assertEqual(rfxmeterpacket.type_string, 'RfxSensor Temperature')
        self.assertEqual(rfxmeterpacket.id_string, '1b')
        self.assertEqual(rfxmeterpacket.value, 18.0)
        self.assertEqual(rfxmeterpacket.field, "Temperature")

        rfxmeterpacket = RFXtrx.lowlevel.parse(bytearray(b'\x07\x70\x00\x0E\x1B\x87\x08\x60'))
        self.assertEqual(rfxmeterpacket.value, -18.0)

    def test_parse_AD(self):
        rfxmeterpacket = RFXtrx.lowlevel.parse(bytearray(b'\x07\x70\x01\x0E\x1B\x01\x28\x60'))
        self.assertEqual(RFXtrx.lowlevel.RfxSensor, type(rfxmeterpacket))
        self.assertEqual(rfxmeterpacket.type_string, 'RfxSensor A/D')
        self.assertEqual(rfxmeterpacket.id_string, '1b')
        self.assertEqual(rfxmeterpacket.value, 2960)
        self.assertEqual(rfxmeterpacket.field, "Analog")

    def test_parse_Voltage(self):
        rfxmeterpacket = RFXtrx.lowlevel.parse(bytearray(b'\x07\x70\x02\x0E\x1B\x02\x01\x60'))
        self.assertEqual(RFXtrx.lowlevel.RfxSensor, type(rfxmeterpacket))
        self.assertEqual(rfxmeterpacket.type_string, 'RfxSensor Voltage')
        self.assertEqual(rfxmeterpacket.id_string, '1b')
        self.assertEqual(rfxmeterpacket.value, 5130)
        self.assertEqual(rfxmeterpacket.field, "Voltage")

    def test_validate_unknown_sub_type(self):
        rfxmeterpacket = RFXtrx.lowlevel.parse(bytearray(b'\x07\x70\xEE\x0E\x1B\x07\x08\x60'))
        self.assertEqual(rfxmeterpacket.type_string, 'Unknown type (0x70/0xee)')

    def test_equal(self):
        rfxmeterpacket = RFXtrx.lowlevel.parse(bytearray(b'\x07\x70\x00\x0E\x1B\x07\x08\x60'))
        rfxmeterpacket2 = RFXtrx.lowlevel.parse(bytearray(b'\x07\x70\x00\x0E\x1B\x07\x08\x60'))
        self.assertTrue(rfxmeterpacket == rfxmeterpacket2)
        self.assertIsNotNone(rfxmeterpacket)
