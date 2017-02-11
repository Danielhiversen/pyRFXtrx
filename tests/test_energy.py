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
        self.assertEquals(energy.type_string,"ELEC1")
        self.assertEquals(energy.seqnbr,167)
        self.assertEquals(energy.id_string,"56:00")
        self.assertEquals(energy.count,10)
        self.assertEquals(energy.currentamps1,0.7)
        self.assertEquals(energy.currentamps2,0)
        self.assertEquals(energy.currentamps3,282.3)
        self.assertEquals(energy.rssi,6)
        self.assertEquals(energy.battery,9)
        
class Elec2TestCase(TestCase):

    def setUp(self):

        self.data = bytearray(b'\x11\x5A\x01\x00\x2E\xB2\x03\x00\x00'
                              b'\x02\xB4\x00\x00\x0C\x46\xA8\x11\x69')
        self.parser = RFXtrx.lowlevel.Energy()

    def test_parse_bytes(self):

        energy = RFXtrx.lowlevel.parse(self.data)
        self.assertEquals(energy.type_string,"CM119/160")
        self.assertEquals(energy.seqnbr,0)
        self.assertEquals(energy.id_string,"2e:b2")
        self.assertEquals(energy.count,3)
        self.assertEquals(energy.currentwatt,692)
        self.assertEquals(energy.totalwatts,920824.5195961836)

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
        self.assertEquals(energy.type_string,"CM180i")
        self.assertEquals(energy.seqnbr,4)
        self.assertEquals(energy.id_string,"2e:b2")
        self.assertEquals(energy.count,1)
        self.assertEquals(energy.currentamps1,437)
        self.assertEquals(energy.currentamps2,514.1)
        self.assertEquals(energy.currentamps3,591.2)
        self.assertEquals(energy.totalwatthours,113527617921.3023)

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
        self.assertEquals(energy.type_string,"ELEC5")
        self.assertEquals(energy.seqnbr,5)
        self.assertEquals(energy.id_string,"23:95")
        self.assertEquals(energy.voltage,178)
        self.assertEquals(energy.currentamps,10.96)
        self.assertEquals(energy.currentwatt,839.8)
        self.assertEquals(energy.totalwatthours,1180)
        self.assertEquals(energy.powerfactor,0)
        self.assertEquals(energy.frequency,50)
        
