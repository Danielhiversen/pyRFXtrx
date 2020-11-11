from unittest import TestCase

import RFXtrx

class Elec1TestCase(TestCase):

    def setUp(self):
        self.data = bytearray(b'\x0D\x59\x01\xA7\x56\x00\x0A'
                              b'\x00\x07\x00\x00\x0B\x07\x69')
        self.parser = RFXtrx.lowlevel.Energy1()

    def test_parse_bytes(self):

        energy = RFXtrx.lowlevel.parse(self.data)
        print(energy)
        self.assertEqual(energy.type_string,"ELEC1, Electrisave")
        self.assertEqual(energy.seqnbr,167)
        self.assertEqual(energy.id_string,"56:00")
        self.assertEqual(energy.count,10)
        self.assertEqual(energy.currentamps1,0.7)
        self.assertEqual(energy.currentamps2,0)
        self.assertEqual(energy.currentamps3,282.3)
        self.assertEqual(energy.rssi,6)
        self.assertEqual(energy.battery,9)
        
class Elec2TestCase(TestCase):

    def setUp(self):

        self.data = bytearray(b'\x11\x5A\x01\x00\x2E\xB2\x03\x00\x00'
                              b'\x02\xB4\x00\x00\x0C\x46\xA8\x11\x69')
        self.parser = RFXtrx.lowlevel.Energy()

    def test_parse_bytes(self):

        energy = RFXtrx.lowlevel.parse(self.data)
        self.assertEqual(energy.type_string,"ELEC2, CM119/160")
        self.assertEqual(energy.seqnbr,0)
        self.assertEqual(energy.id_string,"2e:b2")
        self.assertEqual(energy.count,3)
        self.assertEqual(energy.currentwatt,692)
        self.assertEqual(energy.totalwatts,920824.5195961836)

class Elec4TestCase(TestCase):

    def setUp(self):

        self.data = bytearray(b'\x13\x5b\x01\x04'
                              b'\x2e\xB2'
                              b'\x01'
                              b'\x11\x12'
                              b'\x14\x15'
                              b'\x17\x18'
                              b'\x17\x18\x19\x20\x21\x22'
                              b'\x69')
        self.parser = RFXtrx.lowlevel.Energy4()

    def test_parse_bytes(self):

        energy = RFXtrx.lowlevel.parse(self.data)
        self.assertEqual(energy.type_string,"ELEC4, CM180i")
        self.assertEqual(energy.seqnbr,4)
        self.assertEqual(energy.id_string,"2e:b2")
        self.assertEqual(energy.count,1)
        self.assertEqual(energy.currentamps1,437)
        self.assertEqual(energy.currentamps2,514.1)
        self.assertEqual(energy.currentamps3,591.2)
        self.assertEqual(energy.totalwatthours,113527617921.3023)

class Elec5TestCase(TestCase):

    def setUp(self):

        self.data = bytearray(b'\x0f\x5c\x01\x05'
                              b'\x23\x95'
                              b'\xb2'
                              b'\x04\x48'
                              b'\x20\xce'
                              b'\x00\x76'
                              b'\x00'
                              b'\x32'
                              b'\x80')
        self.parser = RFXtrx.lowlevel.Energy5()

    def test_parse_bytes(self):

        energy = RFXtrx.lowlevel.parse(self.data)
        self.assertEqual(energy.type_string,"ELEC5, Revolt")
        self.assertEqual(energy.seqnbr,5)
        self.assertEqual(energy.id_string,"23:95")
        self.assertEqual(energy.voltage,178)
        self.assertEqual(energy.currentamps,10.96)
        self.assertEqual(energy.currentwatt,839.8)
        self.assertEqual(energy.totalwatthours,1180)
        self.assertEqual(energy.powerfactor,0)
        self.assertEqual(energy.frequency,50)
        

class CartelectronicTestCase(TestCase):

    def setUp(self):
        
        self.data = ""
        self.parser = RFXtrx.lowlevel.Cartelectronic()
        
    def test_parse_bytes(self):
        
        # Encoder
        self.data = bytearray(b'\x11\x60\x02\xb3\x3f\xfe\x61\xa3'
                              b'\x00\x00\x3c\x01'
                              b'\x00\x00\x00\x00'
                              b'\x00\x69')
        energy = RFXtrx.lowlevel.parse(self.data)
        self.assertEqual(energy.type_string, "CARTELECTRONIC_ENCODER")
        self.assertEqual(energy.seqnbr, 179)
        self.assertEqual(energy.id_string, "3ffe61a3")
        self.assertEqual(energy.counter1, 15361)
        self.assertEqual(energy.counter2, 0)
        # Linky
        self.data = bytearray(b'\x15\x60\x03\xb0\x2a\x29\xf2\x75'
                              b'\x00\x17\x9d\x74'
                              b'\x00\x00\x00\x00'
                              b'\x00'
                              b'\x23'
                              b'\x02\xae'
                              b'\x00\x69')
        energy = RFXtrx.lowlevel.parse(self.data)
        self.assertEqual(energy.type_string, "CARTELECTRONIC_LINKY")
        self.assertEqual(energy.seqnbr, 176)
        self.assertEqual(energy.id_string, "2a29f275")
        self.assertEqual(energy.conswatthours, 1547636)
        self.assertEqual(energy.prodwatthours, 0)
        self.assertEqual(energy.tarif_num, 0)
        self.assertEqual(energy.voltage, 235)
        self.assertEqual(energy.currentwatt, 686)
        self.assertEqual(energy.teleinfo_ok, True)
