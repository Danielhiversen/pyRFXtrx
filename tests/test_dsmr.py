from decimal import Decimal
from unittest import TestCase

from RFXtrx import lowlevel


class DsmrTestCase(TestCase):

    def test_parse(self):
        data = bytearray(b'\x05\x62\x01\x03\x0D\x0A')
        packet = lowlevel.parse(data)

        self.assertEqual(lowlevel.Dsmr, type(packet))
        self.assertEqual(packet.packetlength, 5)
        self.assertEqual(packet.packettype, 0x62)
        self.assertEqual(packet.subtype, 1)
        self.assertEqual(packet.type_string, "P1")
        self.assertEqual(packet.seqnbr, 3)
        self.assertEqual(packet.id_string, None)

    def test_header_data(self):
        data = bytearray(b'\x1A\x62\x01\x00'
                         b'\x2F\x58\x4D\x58\x35\x4C\x47\x42'
                         b'\x42\x4C\x41\x34\x34\x31\x35\x35'
                         b'\x37\x30\x30\x37\x38'
                         b'\x0D\x0A')
        packet = lowlevel.parse(data)

        self.assertEqual(packet.id_string, None)

    def test_version_data(self):
        data = bytearray(b'\x12\x62\x01\x02'
                         b'\x31\x2D\x33\x3A\x30\x2E\x32\x2E'
                         b'\x38\x28\x35\x30\x29'
                         b'\x0D\x0A')
        packet = lowlevel.parse(data)

        self.assertEqual(packet.id_string, None)

    def test_equipment_identifier(self):
        data = bytearray(b'\x33\x62\x01\x04'
                         b'\x30\x2D\x30\x3A\x39\x36\x2E\x31'
                         b'\x2E\x31\x28\x34\x35\x33\x30\x33'
                         b'\x30\x33\x34\x33\x36\x33\x30\x33'
                         b'\x30\x33\x34\x33\x32\x33\x31\x33'
                         b'\x38\x33\x33\x33\x32\x33\x39\x33'
                         b'\x35\x33\x31\x33\x38\x29'
                         b'\x0D\x0A')
        packet = lowlevel.parse(data)

        self.assertEqual(packet.id_string, None)

    def test_electricity_used_tariff_1(self):
        data = bytearray(b'\x1E\x62\x01\x05'
                         b'\x31\x2D\x30\x3A\x31\x2E\x38\x2E'
                         b'\x31\x28\x30\x30\x30\x33\x31\x34'
                         b'\x2E\x39\x38\x33\x2A\x6B\x57\x68\x29'
                         b'\x0D\x0A')
        packet = lowlevel.parse(data)

        self.assertEqual(packet.id_string, 'dsmr:1')
        self.assertEqual(packet.electricity_used_tariff_1, Decimal('314.983'))
        self.assertEqual(packet.electricity_used_tariff_1_unit, 'kWh')

    def test_electricity_used_tariff_2(self):
        data = bytearray(b'\x1E\x62\x01\x06'
                         b'\x31\x2D\x30\x3A\x31\x2E\x38\x2E'
                         b'\x32\x28\x30\x30\x30\x32\x33\x32'
                         b'\x2E\x36\x38\x36\x2A\x6B\x57\x68\x29'
                         b'\x0D\x0A')
        packet = lowlevel.parse(data)

        self.assertEqual(packet.id_string, 'dsmr:1')
        self.assertEqual(packet.electricity_used_tariff_2, Decimal('232.686'))
        self.assertEqual(packet.electricity_used_tariff_2_unit, 'kWh')

    def test_electricity_delivered_tariff_1(self):
        data = bytearray(b'\x1E\x62\x01\x07'
                         b'\x31\x2D\x30\x3A\x32\x2E\x38\x2E'
                         b'\x31\x28\x30\x30\x30\x31\x38\x31'
                         b'\x2E\x35\x38\x34\x2A\x6B\x57\x68\x29'
                         b'\x0D\x0A')
        packet = lowlevel.parse(data)

        self.assertEqual(packet.id_string, 'dsmr:1')
        self.assertEqual(packet.electricity_delivered_tariff_1,
                         Decimal('181.584'))
        self.assertEqual(packet.electricity_delivered_tariff_1_unit, 'kWh')

    def test_electricity_delivered_tariff_2(self):
        data = bytearray(b'\x1E\x62\x01\x08'
                         b'\x31\x2D\x30\x3A\x32\x2E\x38\x2E'
                         b'\x32\x28\x30\x30\x30\x34\x32\x33'
                         b'\x2E\x38\x34\x33\x2A\x6B\x57\x68\x29'
                         b'\x0D\x0A')
        packet = lowlevel.parse(data)

        self.assertEqual(packet.id_string, 'dsmr:1')
        self.assertEqual(packet.electricity_delivered_tariff_2,
                         Decimal('423.843'))
        self.assertEqual(packet.electricity_delivered_tariff_2_unit, 'kWh')

    def test_checksum_data(self):
        data = bytearray(b'\x0A\x62\x01\x25'
                         b'\x21\x44\x43\x44\x36'
                         b'\x0D\x0A')
        packet = lowlevel.parse(data)

        self.assertEqual(packet.id_string, None)
