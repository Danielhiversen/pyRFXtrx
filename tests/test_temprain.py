from unittest import TestCase

import RFXtrx


class TempRainTestCase(TestCase):
        
    def test_parse_bytes(self):
        data = [0x0a, 0x4f, 0x01, 0x06, 0xee, 0x09, 0x00, 0x65, 0x00, 0x03, 0x69]
        temprain = RFXtrx.lowlevel.parse(data)
        self.assertEquals(RFXtrx.lowlevel.TempRain, type(temprain))
        self.assertEquals(temprain.temp, 10.1)
        self.assertEquals(temprain.raintotal, 0.3)
        self.assertEquals(temprain.type_string,'TR1 - WS1200')
        self.assertEquals(temprain.id_string,'ee:09')

    def test_parse_bytes_negative_temp(self):
        data = [0x0a, 0x4f, 0x01, 0x05, 0xef, 0x09, 0x80, 0x50, 0x01, 0x06, 0x79]
        
        temprain = RFXtrx.lowlevel.parse(data)
        self.assertEquals(RFXtrx.lowlevel.TempRain, type(temprain))
        self.assertEquals(temprain.temp, -8.0)
        self.assertEquals(temprain.raintotal, 26.2)
        self.assertEquals(temprain.type_string,'TR1 - WS1200')
        self.assertEquals(temprain.id_string,'ef:09')