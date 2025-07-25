from unittest import TestCase

import RFXtrx


class SecurityTestCase(TestCase):

    def test_parse(self):
        data = [0x08, 0x20, 0x00, 0x4D, 0xD3, 0xDC, 0x54, 0x00, 0x89]
        packet = RFXtrx.lowlevel.parse(data)

        self.assertEqual(RFXtrx.lowlevel.Security1, type(packet))
        self.assertEqual(packet.packetlength, 8)
        self.assertEqual(packet.packettype, 32)
        self.assertEqual(packet.subtype, 0)
        self.assertEqual(packet.seqnbr, 77)
        self.assertEqual(packet.type_string, 'X10 Security')
        self.assertEqual(packet.id_string, 'd3dc54:32')
        self.assertEqual(packet.battery, 9)
        self.assertEqual(packet.rssi, 8)
        self.assertEqual(packet.security1_status, 0)
        self.assertEqual(packet.security1_status_string, 'Normal')
        self.assertEqual(packet.tamper, False)

    def test_set_transmit(self):
        packet = RFXtrx.lowlevel.Security1()
        packet.set_transmit(0x00, 77, 13884500, 0x00)

        self.assertEqual(packet.packetlength, 8)
        self.assertEqual(packet.packettype, 32)
        self.assertEqual(packet.subtype, 0)
        self.assertEqual(packet.seqnbr, 77)
        self.assertEqual(packet.type_string, 'X10 Security')
        self.assertEqual(packet.id_string, 'd3dc54:32')
        self.assertEqual(packet.battery, 0)
        self.assertEqual(packet.rssi, 0)
        self.assertEqual(packet.security1_status, 0)
        self.assertEqual(packet.security1_status_string, 'Normal')
        self.assertEqual(packet.tamper, False)
        self.assertEqual(packet.data.hex(), "0820004dd3dc540000")

    def test_parse_id(self):
        packet = RFXtrx.lowlevel.Security1()
        packet.parse_id(0, "d3dc54:32")

        self.assertEqual(packet.id1, 211)
        self.assertEqual(packet.id2, 220)
        self.assertEqual(packet.id3, 84)

        self.assertRaisesRegex(ValueError, "Invalid id_string", packet.parse_id, 0, "G:234")
        self.assertRaisesRegex(ValueError, "Invalid id_string", packet.parse_id, 0, "10234")
        self.assertRaisesRegex(ValueError, "Invalid id_string", packet.parse_id, 0, "1:23X")

class SecurityTestCase2(TestCase):

    def test_parse(self):
        data = [0x08, 0x20, 0x08, 0xce, 0x06, 0x80, 0x00, 0x88, 0x69]
        packet = RFXtrx.lowlevel.parse(data)

        self.assertEqual(RFXtrx.lowlevel.Security1, type(packet))
        self.assertEqual(packet.packetlength, 8)
        self.assertEqual(packet.packettype, 32)
        self.assertEqual(packet.subtype, 8)
        self.assertEqual(packet.seqnbr, 206)
        self.assertEqual(packet.type_string, 'Meiantech')
        self.assertEqual(packet.id_string, '068000:32')
        self.assertEqual(packet.id_combined, 425984)
        self.assertEqual(packet.battery, 9)
        self.assertEqual(packet.rssi, 6)
        self.assertEqual(packet.security1_status, 8)
        self.assertEqual(packet.security1_status_string, 'IR')
        self.assertEqual(packet.tamper, True)

    def test_set_transmit(self):
        packet = RFXtrx.lowlevel.Security1()
        packet.set_transmit(0x08, 206, 425984, 0x08, True)

        self.assertEqual(packet.packetlength, 8)
        self.assertEqual(packet.packettype, 32)
        self.assertEqual(packet.subtype, 8)
        self.assertEqual(packet.seqnbr, 206)
        self.assertEqual(packet.type_string, 'Meiantech')
        self.assertEqual(packet.id_string, '068000:32')
        self.assertEqual(packet.id_combined, 425984)
        self.assertEqual(packet.battery, 0)
        self.assertEqual(packet.rssi, 0)
        self.assertEqual(packet.security1_status, 8)
        self.assertEqual(packet.security1_status_string, 'IR')
        self.assertEqual(packet.tamper, True)

