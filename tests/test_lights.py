import unittest
from RFXtrx import lowlevel
import RFXtrx

class TestRFXTRlowlevel(unittest.TestCase):
    """
    Tests rfxtrx lowlewel
    """

    def test_Status(self):
        x = lowlevel.Status()
        self.assertIsNone(x.type_string)
        self.assertIsNone(x.firmware_version)
        self.assertIsNone(x.devices)
        
        x.load_receive(bytearray([0x0d, 0x01, 0x00, 0x01, 0x02, 0x53, 0x3e, 0x00, 0x0c, 0x2f, 0x01, 0x01, 0x00, 0x00]))
        self.assertEqual(x.type_string, "433.92MHz")
        self.assertEqual(x.firmware_version, 62)
        self.assertEqual(x.output_power, 0)
        self.assertEqual(x.devices, ['ac', 'arc', 'hideki', 'homeeasy', 'keeloq', 'lacrosse', 'oregon', 'x10'])

        self.assertEqual(list(x.data), [13, 1, 0, 1, 2, 83, 62, 0, 12, 47, 1, 1, 0, 0])
        self.assertEqual(x.packetlength, 13)
        self.assertEqual(x.packettype, 1)
        self.assertEqual(x.tranceiver_type, 83)

    def test_Lighting1(self):
        x = lowlevel.Lighting1()
        self.assertIsNone(x.subtype)
        self.assertIsNone(x.seqnbr)
        self.assertIsNone(x.id_string)
        self.assertIsNone(x.cmnd)
        self.assertIsNone(x.rssi)
 
        x.load_receive(bytearray([0x07, 0x10, 0x00, 0x2a, 0x45, 0x05, 0x01, 0x70]))
        self.assertEqual(x.seqnbr, 42)
        self.assertEqual(x.id_string,"E5")
        self.assertEqual(list(x.data), [7, 16, 0, 42, 69, 5, 1, 112])
        self.assertEqual(x.packetlength,7)
        self.assertEqual(x.packettype,16)
        self.assertEqual(x.subtype,0)
        self.assertEqual(x.type_string,"X10 lighting")
        self.assertEqual(x.seqnbr,42)
        self.assertEqual(x.housecode,69)
        self.assertEqual(x.unitcode,5)
        self.assertEqual(x.cmnd,1)
        self.assertEqual(x.cmnd_string,"On")
        self.assertEqual(x.rssi_byte,112)
        self.assertEqual(x.rssi,7)
        self.assertEqual(x.__str__(),'Lighting1 [subtype=X10 lighting, seqnbr=42, id=E5, cmnd=On, rssi=7]')

        self.assertTrue(x.has_type_string)

        x = lowlevel.Lighting1()
        x.set_transmit(0x00, 0x2a, 0x45, 0x05, 0x01)
        self.assertEqual(x.seqnbr, 42)
        self.assertEqual(x.id_string,"E5")
        self.assertEqual(list(x.data), [7, 16, 0, 42, 69, 5, 1, 0])
        self.assertEqual(x.packetlength,7)
        self.assertEqual(x.packettype,16)
        self.assertEqual(x.subtype,0)
        self.assertEqual(x.type_string,"X10 lighting")
        self.assertEqual(x.seqnbr,42)
        self.assertEqual(x.housecode,69)
        self.assertEqual(x.unitcode,5)
        self.assertEqual(x.cmnd,1)
        self.assertEqual(x.cmnd_string,"On")
        self.assertEqual(x.rssi_byte,0)
        self.assertEqual(x.rssi,0)
        
        x.parse_id(0, "E13")        
        self.assertEqual(x.housecode, 69)
        self.assertEqual(x.unitcode,13)
        
        self.assertRaises(ValueError, x.parse_id,0, "Q1")
        self.assertRaises(ValueError, x.parse_id,0, "AA")


    def test_Lighting2(self):
        x = lowlevel.Lighting2()
        self.assertIsNone(x.subtype)
        self.assertIsNone(x.seqnbr)
        self.assertIsNone(x.id_string)
        self.assertIsNone(x.cmnd)
        self.assertIsNone(x.rssi)
 
        x.load_receive(bytearray([0x0b, 0x11, 0x00, 0x2a, 0x01, 0x23, 0x45, 0x67, 0x05, 0x02, 0x08, 0x70]))
        self.assertEqual(x.seqnbr, 42)
        self.assertEqual(x.id_string,"1234567:5")
        self.assertEqual(list(x.data), [11, 17, 0, 42, 1, 35, 69, 103, 5, 2, 8, 112])
        self.assertEqual(x.packetlength,11)
        self.assertEqual(x.packettype,17)
        self.assertEqual(x.subtype,0)
        self.assertEqual(x.type_string,"AC")
        self.assertEqual(x.seqnbr,42)
        self.assertEqual(x.unitcode,5)
        self.assertEqual(x.id1,1)
        self.assertEqual(x.id2,35)
        self.assertEqual(x.id3,69)
        self.assertEqual(x.id4,103)
        self.assertEqual(x.id_combined,19088743)
        self.assertEqual(x.cmnd,2)
        self.assertEqual(x.cmnd_string,"Set level")
        self.assertEqual(x.rssi_byte,112)
        self.assertEqual(x.rssi,7)
        self.assertEqual(x.__str__(),'Lighting2 [subtype=AC, seqnbr=42, id=1234567:5, cmnd=Set level, level=8, rssi=7]')
 
        x = lowlevel.Lighting2()
        x.set_transmit(0x00, 0x2a, 0x1234567, 0x05, 0x02, 0x08)
        self.assertEqual(x.seqnbr, 42)
        self.assertEqual(list(x.data), [11, 17, 0, 42, 1, 35, 69, 103, 5, 2, 8, 0])
        self.assertEqual(x.packetlength,11)
        self.assertEqual(x.packettype,17)
        self.assertEqual(x.subtype,0)
        self.assertEqual(x.type_string,"AC")
        self.assertEqual(x.seqnbr,42)
        self.assertEqual(x.id1,1)
        self.assertEqual(x.id2,35)
        self.assertEqual(x.id3,69)
        self.assertEqual(x.id4,103)
        self.assertEqual(x.id_combined,19088743)
        self.assertEqual(x.unitcode,5)
        self.assertEqual(x.id_string,"1234567:5")
        self.assertEqual(x.cmnd,2)
        self.assertEqual(x.cmnd_string,"Set level")
        self.assertEqual(x.rssi_byte,0)
        self.assertEqual(x.rssi,0)

        x = lowlevel.Lighting2()
        x.parse_id(0, "1234567:5")
        self.assertEqual(x.id1,1)
        self.assertEqual(x.id2,35)
        self.assertEqual(x.id3,69)
        self.assertEqual(x.id4,103)
        self.assertEqual(x.id_combined,19088743)
        self.assertEqual(x.unitcode,5)

       
        self.assertRaises(ValueError, x.parse_id,0, "12345678:5")
        self.assertRaises(ValueError, x.parse_id,0, "123456:54")
        self.assertRaises(ValueError, x.parse_id,0, "123456785")


    def test_Lighting3(self):
        x = lowlevel.Lighting3()
        self.assertIsNone(x.subtype)
        self.assertIsNone(x.seqnbr)
        self.assertIsNone(x.id_string)
        self.assertIsNone(x.cmnd)
        self.assertIsNone(x.rssi)
 
        x.load_receive(bytearray([0x08, 0x12, 0x00, 0x2a, 0x01, 0x34, 0x02, 0x15, 0x79]))
        self.assertEqual(list(x.data), [8, 18, 0, 42, 1, 52, 2, 21, 121])
        self.assertEqual(x.packetlength,8)
        self.assertEqual(x.packettype,18)
        self.assertEqual(x.subtype,0)
        self.assertEqual(x.type_string,"Ikea Koppla")
        self.assertEqual(x.seqnbr,42)
        self.assertEqual(x.system,1)
        self.assertEqual(x.channel1,52)
        self.assertEqual(x.channel2,2)
        self.assertEqual(x.channel,564)
        self.assertEqual(x.id_string,"1:234")
        self.assertEqual(x.cmnd,21)
        self.assertEqual(x.cmnd_string,"Level 5")
        self.assertEqual(x.rssi_byte,121)
        self.assertEqual(x.rssi,7)
        self.assertEqual(x.battery,9)
        self.assertEqual(x.__str__(),'Lighting3 [subtype=Ikea Koppla, seqnbr=42, id=1:234, cmnd=Level 5, battery=9, rssi=7]')
         
        x = lowlevel.Lighting3()
        x.set_transmit(0x00, 0x2a, 0x1, 0x234, 0x15)
        self.assertEqual(list(x.data), [8, 18, 0, 42, 1, 52, 2, 21, 0])
        self.assertEqual(x.packetlength,8)
        self.assertEqual(x.packettype,18)
        self.assertEqual(x.subtype,0)
        self.assertEqual(x.type_string,"Ikea Koppla")
        self.assertEqual(x.seqnbr,42)
        self.assertEqual(x.system,1)
        self.assertEqual(x.channel1,52)
        self.assertEqual(x.channel2,2)
        self.assertEqual(x.channel,564)
        self.assertEqual(x.id_string,"1:234")
        self.assertEqual(x.cmnd,21)
        self.assertEqual(x.cmnd_string,"Level 5")
        self.assertEqual(x.rssi_byte,0)
        self.assertEqual(x.rssi,0)
        self.assertEqual(x.battery,0)

        x = lowlevel.Lighting3()
        x.parse_id(0, "1:234")
        self.assertEqual(x.channel1,52)
        self.assertEqual(x.channel2,2)
        self.assertEqual(x.channel,564)

       
        self.assertRaises(ValueError, x.parse_id,0, "G:234")
        self.assertRaises(ValueError, x.parse_id,0, "10234")
        self.assertRaises(ValueError, x.parse_id,0, "1:23X")



class test_Lighting3(unittest.TestCase):

    def setUp(self):

        self.data = bytearray(b'\x0A\x14\x00\xAD\xF3\x94\xAB'
                              b'\x01\x01\x00\x60')
        self.parser = RFXtrx.lowlevel.Lighting5()

    def test_parse_bytes(self):

        light = RFXtrx.lowlevel.parse(self.data)
        self.assertEqual(RFXtrx.lowlevel.Lighting5, type(light))
        self.assertEqual(light.type_string,"LightwaveRF, Siemens")
        self.assertEqual(light.seqnbr,173)
        self.assertEqual(light.id_string,"f394ab:1")
        self.assertEqual(light.cmnd_string,"On")
        self.assertEqual(light.cmnd,1)
        self.assertEqual(light.level,0)
