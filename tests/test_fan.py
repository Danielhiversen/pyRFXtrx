from unittest import TestCase

import RFXtrx
from RFXtrx.lowlevel import Fan

class packetTestCase(TestCase):
        
    def test_parse_bytes(self):
        data = [0x08, 0x17, 0x0D, 0x00, 0x12, 0x34, 0x56, 0x01, 0x00]
        packet = RFXtrx.lowlevel.parse(data)

        self.assertEqual(Fan, type(packet))
        self.assertEqual(packet.id1, 0x12)
        self.assertEqual(packet.id2, 0x34)
        self.assertEqual(packet.id3, 0x56)
        self.assertEqual(packet.id_string,'123456')
        self.assertEqual(packet.cmnd, 0x01)
        self.assertEqual(packet.cmnd_string, 'Low')
        self.assertEqual(str(packet), 'Fan [subtype=Itho HRU400, seqnbr=0, id=123456, cmnd=Low]')


    def test_set_transmit(self):
        packet = RFXtrx.lowlevel.Fan()
        packet.set_transmit(0x0D, 0x123456, Fan.Commands.MEDIUM.value)
        print(packet)

        self.assertEqual(packet.packetlength, 8)
        self.assertEqual(packet.packettype, 0x17)
        self.assertEqual(packet.subtype, 0x0D)
        self.assertEqual(packet.id_combined, 0x123456)
        self.assertEqual(packet.id1, 0x12)
        self.assertEqual(packet.id2, 0x34)
        self.assertEqual(packet.id3, 0x56)
        self.assertEqual(packet.cmnd, 0x02)
        self.assertEqual(packet.data, bytearray([0x08, 0x17, 0x0D, 0x00, 0x12, 0x34, 0x56, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]))
