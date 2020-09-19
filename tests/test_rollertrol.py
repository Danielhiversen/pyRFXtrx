from unittest import TestCase

import RFXtrx


class RollerTrolTestCase(TestCase):
    def test_parse_bytes(self):

        rollertrol = RFXtrx.lowlevel.parse(bytearray(b'\x09\x19\x00\x00\x00\x9b\xa8\x01\x01\x00'))
        self.assertEqual(rollertrol.__repr__(), "RollerTrol [subtype=0, seqnbr=0, id=009ba8:1, cmnd=Down, rssi=0]")
        self.assertEqual(rollertrol.packetlength, 9)
        self.assertEqual(rollertrol.subtype, 0)
        self.assertEqual(rollertrol.type_string, "RollerTrol")
        self.assertEqual(rollertrol.seqnbr, 0)
        self.assertEqual(rollertrol.id_string, "009ba8:1")
        self.assertEqual(rollertrol.cmnd, 1)
        self.assertEqual(rollertrol.cmnd_string, "Down")
        self.assertEqual(rollertrol.rssi_byte, 0)
        self.assertEqual(rollertrol.rssi, 0)

        rollertrol = RFXtrx.lowlevel.RollerTrol()
        rollertrol.set_transmit(0, 0, 0x009ba8, 1, 1)
        self.assertEqual(rollertrol.__repr__(), "RollerTrol [subtype=0, seqnbr=0, id=009ba8:1, cmnd=Down, rssi=0]")
        self.assertEqual(rollertrol.packetlength, 9)
        self.assertEqual(rollertrol.subtype, 0)
        self.assertEqual(rollertrol.type_string, "RollerTrol")
        self.assertEqual(rollertrol.seqnbr, 0)
        self.assertEqual(rollertrol.id_string, "009ba8:1")
        self.assertEqual(rollertrol.cmnd, 1)
        self.assertEqual(rollertrol.cmnd_string, "Down")
        self.assertEqual(rollertrol.rssi_byte, 0)
        self.assertEqual(rollertrol.rssi, 0)

        rollertrol = RFXtrx.lowlevel.RollerTrol()
        rollertrol.parse_id(0, "009ba8:2")
        self.assertEqual(rollertrol.unitcode, 2)
        self.assertRaises(ValueError, rollertrol.parse_id, 0, "AA")

        rollertrol = RFXtrx.get_device(0x19, 0, "009ba8:1")
        self.assertEqual(rollertrol.__str__(), "<class 'RFXtrx.RollerTrolDevice'> type='RollerTrol' id='009ba8:1'")
        self.assertEqual(rollertrol.unitcode, 1)

        rollertrol = RFXtrx.lowlevel.parse(bytearray(b'\x09\x19\x02\x00\x00\x9b\xa8\x01\x05\x00'))
        self.assertEqual(rollertrol.cmnd_string, "Unknown command (0x05)")
        self.assertEqual(rollertrol.type_string, "Unknown type (0x19/0x02)")
        
