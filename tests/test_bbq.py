from unittest import TestCase

import RFXtrx


class BbqTestCase(TestCase):

    def setUp(self):
        self.parser = RFXtrx.lowlevel.Bbq()

    def test_parse_bytes(self):
        self.data = bytearray([0x0a, 0x4e, 0x01, 0x06, 0xfc, 0xd8, 0x00, 0x13, 0x00, 0x13, 0x79])
        bbq = RFXtrx.lowlevel.parse(self.data)
        self.assertEqual(RFXtrx.lowlevel.Bbq, type(bbq))
        self.assertEqual(bbq.temp1,19)
        self.assertEqual(bbq.temp2,19)
        self.assertEqual(bbq.type_string,'BBQ1 - Maverick ET-732')
        self.assertEqual(bbq.id_string,'fcd800:78')

        self.data = bytearray([0x0a, 0x4e, 0x01, 0x01, 0x6f, 0xe1, 0x00, 0x13, 0x00, 0x20, 0x79])
        bbq = RFXtrx.lowlevel.parse(self.data)
        self.assertEqual(RFXtrx.lowlevel.Bbq, type(bbq))
        self.assertEqual(bbq.temp1,19)
        self.assertEqual(bbq.temp2,32)
        self.assertEqual(bbq.type_string,'BBQ1 - Maverick ET-732')
        self.assertEqual(bbq.id_string,'6fe100:78')

        self.data = bytearray([0x0a, 0x4e, 0x01, 0x11, 0x6f, 0xe1, 0x00, 0x1c, 0x00, 0x1a, 0x79])
        bbq = RFXtrx.lowlevel.parse(self.data)
        self.assertEqual(RFXtrx.lowlevel.Bbq, type(bbq))
        self.assertEqual(bbq.temp1,28)
        self.assertEqual(bbq.temp2,26)
        self.assertEqual(bbq.type_string,'BBQ1 - Maverick ET-732')
        self.assertEqual(bbq.id_string,'6fe100:78')

        self.data = bytearray([0x0a, 0x4e, 0x01, 0x15, 0x6f, 0xe1, 0x00, 0x1a, 0x00, 0x1e, 0x79])
        bbq = RFXtrx.lowlevel.parse(self.data)
        self.assertEqual(RFXtrx.lowlevel.Bbq, type(bbq))
        self.assertEqual(bbq.temp1,26)
        self.assertEqual(bbq.temp2,30)
        self.assertEqual(bbq.type_string,'BBQ1 - Maverick ET-732')
        self.assertEqual(bbq.id_string,'6fe100:78')

        self.data = bytearray([0x0a, 0x4e, 0x01, 0x1f, 0x6f, 0xe1, 0x00, 0x18, 0x00, 0x1f, 0x79])
        bbq = RFXtrx.lowlevel.parse(self.data)
        self.assertEqual(RFXtrx.lowlevel.Bbq, type(bbq))
        self.assertEqual(bbq.temp1,24)
        self.assertEqual(bbq.temp2,31)
        self.assertEqual(bbq.type_string,'BBQ1 - Maverick ET-732')
        self.assertEqual(bbq.id_string,'6fe100:78')
