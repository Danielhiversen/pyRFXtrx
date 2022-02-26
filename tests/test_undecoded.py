from unittest import TestCase

import RFXtrx


class UndecodedTestCase(TestCase):

    def setUp(self):
        self.parser = RFXtrx.lowlevel.Undecoded()

    def test_parse_bytes(self):
        self.data = bytearray([0x09, 0x03, 0x01, 0x04, 0x28, 0x0a, 0xb7, 0x66, 0x04, 0x70])
        undecoded = RFXtrx.lowlevel.parse(self.data)
        self.assertEqual(RFXtrx.lowlevel.Undecoded, type(undecoded))
        self.assertEqual(undecoded.subtype, 0x01)
        self.assertEqual(undecoded.type_string, 'arc')
        self.assertEqual(undecoded.payload, bytearray([0x28, 0x0a, 0xb7, 0x66, 0x04, 0x70]))
        self.assertEqual(undecoded.id_string,'Undecoded')
