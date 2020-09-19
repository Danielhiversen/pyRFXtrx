from unittest import TestCase

import RFXtrx


class RfyTestCase(TestCase):
    def test_parse_bytes(self):

        rfy = RFXtrx.lowlevel.parse(bytearray(b'\x08\x1A\x00\x00\x0A\x00\x01\x01\x03'))
        self.assertEqual(rfy.__repr__(), "Rfy [subtype=0, seqnbr=0, id=0a0001:1, cmnd=Down]")
        self.assertEqual(rfy.packetlength, 8)
        self.assertEqual(rfy.subtype, 0)
        self.assertEqual(rfy.type_string, "Rfy")
        self.assertEqual(rfy.seqnbr, 0)
        self.assertEqual(rfy.id_string, "0a0001:1")
        self.assertEqual(rfy.cmnd, 3)
        self.assertEqual(rfy.cmnd_string, "Down")

        rfy = RFXtrx.lowlevel.Rfy()
        rfy.set_transmit(0, 0, 0x0a0001, 1, 3)
        self.assertEqual(rfy.__repr__(), "Rfy [subtype=0, seqnbr=0, id=0a0001:1, cmnd=Down]")
        self.assertEqual(rfy.packetlength, 8)
        self.assertEqual(rfy.subtype, 0)
        self.assertEqual(rfy.type_string, "Rfy")
        self.assertEqual(rfy.seqnbr, 0)
        self.assertEqual(rfy.id_string, "0a0001:1")
        self.assertEqual(rfy.cmnd, 3)
        self.assertEqual(rfy.cmnd_string, "Down")

        rfy = RFXtrx.lowlevel.Rfy()
        rfy.parse_id(0, "0a0001:2")
        self.assertEqual(rfy.unitcode, 2)
        self.assertRaises(ValueError, rfy.parse_id, 0, "AA")

        rfy = RFXtrx.get_device(0x1A, 0, "0a0001:1")
        self.assertEqual(rfy.__str__(), "<class 'RFXtrx.RfyDevice'> type='Rfy' id='0a0001:1'")
        self.assertEqual(rfy.unitcode, 1)

        rfy = RFXtrx.lowlevel.parse(bytearray(b'\x08\x1A\x01\x00\x0A\x00\x01\x01\x05'))
        self.assertEqual(rfy.cmnd_string, "Unknown command (0x05)")
        self.assertEqual(rfy.type_string, "Rfy Extended")

        rfy = RFXtrx.lowlevel.parse(bytearray(b'\x08\x1A\x02\x00\x0A\x00\x01\x01\x05'))
        self.assertEqual(rfy.cmnd_string, "Unknown command (0x05)")
        self.assertEqual(rfy.type_string, "Unknown type (0x1a/0x02)")
        
        rfy = RFXtrx.get_device(0x1A,3,'0a0001:2')
        self.assertEqual(rfy.subtype, 3)
        self.assertEqual(rfy.__str__(), "<class 'RFXtrx.RfyDevice'> type='ASA' id='0a0001:2'")
        
