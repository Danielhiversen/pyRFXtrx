from unittest import TestCase

import RFXtrx


class StatusTestCase(TestCase):

    def setUp(self):

        self.data = bytearray(b'\x0D\x01\x00\x01\x02\x53\x45\x00\x0C'
                              b'\x2F\x01\x01\x00\x00')
        self.parser = RFXtrx.lowlevel.Status()

    def test_parse_bytes(self):
        status = RFXtrx.lowlevel.parse(self.data)
        self.assertEqual(RFXtrx.lowlevel.Status, type(status))
        self.assertEqual(status.devices, ['ac', 'arc', 'hideki', 'homeeasy', 'keeloq', 'lacrosse', 'oregon', 'x10'])
        self.assertEqual(status.type_string,'433.92MHz')
        self.assertEqual(status.firmware_version,69)
        self.assertEqual(status.output_power,0)
        self.assertTrue(status.has_value('devices'))

    def test_validate_bytes_short(self):

        data = self.data[:1]
        status = RFXtrx.lowlevel.parse(data)
        self.assertEqual(status, None)
        
    def test_validate_unkown_packet_type(self):

        self.data[1] = 0xFF
        status = RFXtrx.lowlevel.parse(self.data)
        self.assertEqual(status, None)

        

