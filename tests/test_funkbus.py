from unittest import TestCase

import RFXtrx


class FunkbusTestCase(TestCase):
    def test_parse_bytes(self):


        funkbus = RFXtrx.lowlevel.parse(bytearray(b'\x09\x1E\x00\x00\x0A\x0B\x42\x01\x01\x01'))
        self.assertEqual(funkbus.__repr__(), "Funkbus [subtype=0, seqnbr=0, id=0a0b:4201, group=B, target=1, cmnd=Up, time=1 sec]")
        self.assertEqual(funkbus.packetlength, 9)
        self.assertEqual(funkbus.subtype, 0)
        self.assertEqual(funkbus.type_string, "Gira remote")
        self.assertEqual(funkbus.seqnbr, 0)
        self.assertEqual(funkbus.id_string, "0a0b:4201")
        self.assertEqual(funkbus.cmnd, 1)
        self.assertEqual(funkbus.cmnd_string, "Up")

        funkbus = RFXtrx.lowlevel.Funkbus()
        funkbus.set_transmit(0, 0, 0x0a0b, 0x41, 0x06, 0x00, 0x00)
        self.assertEqual(funkbus.__repr__(), "Funkbus [subtype=0, seqnbr=0, id=0a0b:4106, group=A, target=6, cmnd=Down, time=short]")
        self.assertEqual(funkbus.packetlength, 11)
        self.assertEqual(funkbus.subtype, 0)
        self.assertEqual(funkbus.type_string, "Gira remote")
        self.assertEqual(funkbus.seqnbr, 0)
        self.assertEqual(funkbus.id1, 10)
        self.assertEqual(funkbus.id2, 11)
        self.assertEqual(funkbus.id_combined, 2571)
        self.assertEqual(funkbus.id_string, "0a0b:4106")
        self.assertEqual(funkbus.cmnd, 0)
        self.assertEqual(funkbus.cmnd_string, "Down")
        self.assertEqual(funkbus.target, 6)
        self.assertEqual(funkbus.target_string, "6")
        self.assertEqual(funkbus.time, 0)
        self.assertEqual(funkbus.time_string, "short")


        funkbus = RFXtrx.lowlevel.Funkbus()
        funkbus.parse_id(0, "3fcc:4301")
        self.assertEqual(funkbus.id1, 63)
        self.assertRaises(ValueError, funkbus.parse_id, 0, "1E87")

        funkbus = RFXtrx.get_device(0x1E, 0, "3fcc:4102")
        self.assertEqual(funkbus.__str__(), "<class 'RFXtrx.FunkDevice'> type='Gira remote' id='3fcc:4102'")
        self.assertEqual(funkbus.groupcode, 65)
        self.assertEqual(funkbus.target, 2)

        funkbus = RFXtrx.lowlevel.parse(bytearray(b'\x09\x1E\x01\x00\x0A\x0B\x41\x09\x09\x00'))
        self.assertEqual(funkbus.cmnd_string, "Unknown command (0x09)")
        self.assertEqual(funkbus.type_string, "Insta remote")

        funkbus = RFXtrx.lowlevel.parse(bytearray(b'\x09\x1E\x05\x00\x0A\x0B\x41\x09\x07\x00'))
        self.assertEqual(funkbus.cmnd_string, "Unknown command (0x07)")
        self.assertEqual(funkbus.type_string, "Unknown type (0x1e/0x05)")