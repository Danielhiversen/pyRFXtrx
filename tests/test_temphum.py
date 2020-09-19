from unittest import TestCase

import RFXtrx


class TempHumidityTestCase(TestCase):

    def setUp(self):

        self.data = bytearray(b'\x0A\x52\x02\x11\x70\x02\x00\xA7'
                              b'\x2D\x00\x89')
        self.parser = RFXtrx.lowlevel.TempHumid()

    def test_parse_bytes(self):
        temphum = RFXtrx.lowlevel.parse(self.data)
        self.assertEqual(RFXtrx.lowlevel.TempHumid, type(temphum))
        self.assertEqual(temphum.temp,16.7)
        self.assertEqual(temphum.humidity,45)
        self.assertEqual(temphum.type_string,'THGR810, THGN800')
        self.assertEqual(temphum.id_string,'70:02')                


    def test_negative_temp(self):
        self.data = bytearray(b'\x0A\x52\x02\x11\x70\x02\x80\xA7'
                              b'\x2D\x00\x89')

        temphum = RFXtrx.lowlevel.parse(self.data)
        self.assertEqual(RFXtrx.lowlevel.TempHumid, type(temphum))
        self.assertEqual(temphum.temp,-16.7)

    def test_validate_bytes_short(self):
        data = self.data[:1]
        temphum = RFXtrx.lowlevel.parse(data)
        self.assertEqual(temphum, None)

    def test_validate_unkown_packet_type(self):

        self.data[1] = 0xFF
        temphum = RFXtrx.lowlevel.parse(self.data)
        self.assertEqual(temphum, None)

    def test_validate_unknown_sub_type(self):

        self.data[2] = 0xEE
        temphum = RFXtrx.lowlevel.parse(self.data)
        self.assertEqual(temphum.type_string,'Unknown type (0x52/0xee)')
        
    def test_equal(self):
        temphum = RFXtrx.lowlevel.parse(self.data)
        self.data = bytearray(b'\x0A\x52\x02\x11\x70\x02\x80\xA7'
                              b'\x2D\x00\x89')

        temphum2 = RFXtrx.lowlevel.parse(self.data)
        self.assertTrue(temphum==temphum2)
        self.assertFalse(temphum==None)