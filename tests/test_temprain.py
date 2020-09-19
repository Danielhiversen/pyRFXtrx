from unittest import TestCase

import RFXtrx


class TempRainTestCase(TestCase):
        
    def test_parse_bytes(self):
        data = [0x0a, 0x4f, 0x01, 0x06, 0xee, 0x09, 0x00, 0x65, 0x00, 0x03, 0x69]
        temprain = RFXtrx.lowlevel.parse(data)
        self.assertEqual(RFXtrx.lowlevel.TempRain, type(temprain))
        self.assertEqual(temprain.temp, 10.1)
        self.assertEqual(temprain.raintotal, 0.3)
        self.assertEqual(temprain.type_string,'TR1 - WS1200')
        self.assertEqual(temprain.id_string,'ee:09')

    def test_parse_bytes_negative_temp(self):
        data = [0x0a, 0x4f, 0x01, 0x05, 0xef, 0x09, 0x80, 0x50, 0x01, 0x06, 0x79]
        
        temprain = RFXtrx.lowlevel.parse(data)
        self.assertEqual(RFXtrx.lowlevel.TempRain, type(temprain))
        self.assertEqual(temprain.temp, -8.0)
        self.assertEqual(temprain.raintotal, 26.2)
        self.assertEqual(temprain.type_string,'TR1 - WS1200')
        self.assertEqual(temprain.id_string,'ef:09')