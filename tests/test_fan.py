from unittest import TestCase

import RFXtrx


class FanTestCase(TestCase):
        
    def test_parse_bytes(self):
        data = [0x08, 0x17, 0x0D, 0x00, 0x12, 0x34, 0x56, 0x01, 0x00]
        fan = RFXtrx.lowlevel.parse(data)
        self.assertEqual(RFXtrx.lowlevel.Fan, type(fan))
        self.assertEqual(fan.id1, 0x12)
        self.assertEqual(fan.id2, 0x34)
        self.assertEqual(fan.id3, 0x56)
        self.assertEqual(fan.id_string,'123456')
        self.assertEqual(fan.cmnd, 0x01)
        self.assertEqual(fan.cmnd_string, 'Low')
        self.assertEqual(str(fan), 'Fan [subtype=Itho HRU400, seqnbr=0, id=123456, cmnd=Low]')
