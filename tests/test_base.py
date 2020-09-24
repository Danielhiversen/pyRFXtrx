from unittest import TestCase
import time

import RFXtrx

num_calbacks = 0
def _callback(*args, **kwargs):
    global num_calbacks
    num_calbacks = num_calbacks + 1


class CoreTestCase(TestCase):

    def setUp(self):
        self.path = '/dev/serial/...'
        global num_calbacks
        num_calbacks = 0
        self.maxDiff = 1000

    def test_constructor(self):
        global num_calbacks
        core = RFXtrx.Core(self.path, event_callback=_callback, transport_protocol=RFXtrx.DummyTransport2)
        while num_calbacks < 6:
            time.sleep(0.1)

        self.assertEqual(len(core.sensors()),2)
        self.assertTrue(core._thread.is_alive())
        core.close_connection()
        self.assertFalse(core._thread.is_alive())

    def test_format_packet(self):
        # Lighting1
        core = RFXtrx.Connect(self.path, event_callback=_callback, transport_protocol=RFXtrx.DummyTransport)
        bytes_array = bytearray([0x07, 0x10, 0x00, 0x2a, 0x45, 0x05, 0x01, 0x70])
        event = core.transport.parse(bytes_array)
        self.assertEqual(RFXtrx.ControlEvent, type(event))
        self.assertEqual(event.device.type_string,'X10 lighting')
        self.assertEqual(event.device.id_string,'E5')
        self.assertEqual(event.values['Command'],'On')
        self.assertEqual(event.values['Rssi numeric'],7)
        event.device.send_on(core.transport)
        event.device.send_off(core.transport)
        self.assertRaises(ValueError,event.device.send_dim,core.transport,50)

        # Lighting2
        bytes_array =[0x0b, 0x11, 0x00, 0x2a, 0x01, 0x23, 0x45, 0x67, 0x05, 0x02, 0x07, 0x70]
        event = core.transport.parse(bytes_array)
        event.device.send_on(core.transport)
        event.device.send_off(core.transport)
        self.assertRaises(ValueError,event.device.send_dim,core.transport,150)
        self.assertRaises(ValueError,event.device.send_dim,core.transport,-1)
        event.device.send_dim(core.transport,50)
        event.device.send_dim(core.transport,0)

        # Lighting3
        bytes_array = [0x08, 0x12, 0x00, 0x2a, 0x01, 0x34, 0x02, 0x15, 0x79]
        event = core.transport.parse(bytes_array)
        event.device.send_on(core.transport)
        event.device.send_off(core.transport)
        self.assertRaises(ValueError,event.device.send_dim,core.transport,150)
        self.assertRaises(ValueError,event.device.send_dim,core.transport,-1)
        event.device.send_dim(core.transport,50)
        event.device.send_dim(core.transport,0)

        # Lighting4
        bytes_array = [0x09, 0x13, 0x00, 0x2a, 0x12, 0x34, 0x56, 0x01, 0x5e, 0x70]
        event = core.transport.parse(bytes_array)
        self.assertEqual(RFXtrx.ControlEvent, type(event))
        self.assertEqual(RFXtrx.LightingDevice, type(event.device))
        event.device.send_on(core.transport)
        event.device.send_off(core.transport)
        self.assertRaises(ValueError,event.device.send_dim,core.transport,50)

        # Lighting5, subtype0
        bytes_array = bytearray(b'\x0A\x14\x00\xAD\xF3\x94\xAB\x01\x10\x00\x60')
        event = core.transport.parse(bytes_array)
        event.device.send_on(core.transport)
        event.device.send_off(core.transport)
        event.device.send_open(core.transport)
        event.device.send_close(core.transport)
        event.device.send_stop(core.transport)
        self.assertRaises(ValueError,event.device.send_openclosestop,core.transport,0x0c)
        self.assertRaises(ValueError,event.device.send_dim,core.transport,150)
        self.assertRaises(ValueError,event.device.send_dim,core.transport,-1)
        event.device.send_dim(core.transport,50)
        event.device.send_dim(core.transport,0)

        # Lighting5, subtype0, rollershutter
        bytes_array = bytearray(b'\x0A\x14\x00\xAD\xF3\x94\xAB\x01\x0D\x00\x60')
        event = core.transport.parse(bytes_array)
        event.device.send_open(core.transport)
        event.device.send_close(core.transport)
        event.device.send_stop(core.transport)

        # Lighting5, subtype1
        bytes_array = bytearray(b'\x0A\x14\x01\xAD\xF3\x94\xAB\x01\x10\x00\x60')
        event = core.transport.parse(bytes_array)
        event.device.send_on(core.transport)
        event.device.send_off(core.transport)
        self.assertRaises(ValueError,event.device.send_dim,core.transport,150)
        self.assertRaises(ValueError,event.device.send_dim,core.transport,-1)
        event.device.send_dim(core.transport,50)
        event.device.send_dim(core.transport,0)


        # Lighting5, subtype2
        bytes_array = bytearray(b'\x0A\x14\x02\xAD\xF3\x94\xAB\x01\x10\x00\x60')
        event = core.transport.parse(bytes_array)
        event.device.send_on(core.transport)
        event.device.send_off(core.transport)
        self.assertRaises(ValueError,event.device.send_dim,core.transport,150)
        self.assertRaises(ValueError,event.device.send_dim,core.transport,-1)
        event.device.send_dim(core.transport,50)
        event.device.send_dim(core.transport,0)


        # Lighting5, subtype3
        bytes_array = bytearray(b'\x0A\x14\x03\xAD\xF3\x94\xAB\x01\x10\x00\x60')
        event = core.transport.parse(bytes_array)
        event.device.send_on(core.transport)
        event.device.send_off(core.transport)
        self.assertRaises(ValueError,event.device.send_dim,core.transport,150)
        self.assertRaises(ValueError,event.device.send_dim,core.transport,-1)
        event.device.send_dim(core.transport,50)
        event.device.send_dim(core.transport,0)


        # Lighting5, subtype4
        bytes_array = bytearray(b'\x0A\x14\x04\xAD\xF3\x94\xAB\x01\x10\x00\x60')
        event = core.transport.parse(bytes_array)
        event.device.send_on(core.transport)
        event.device.send_off(core.transport)
        self.assertRaises(ValueError,event.device.send_dim,core.transport,150)
        self.assertRaises(ValueError,event.device.send_dim,core.transport,-1)
        event.device.send_dim(core.transport,50)
        event.device.send_dim(core.transport,0)

        # Lighting5, subtype5
        bytes_array = bytearray(b'\x0A\x14\x05\xAD\xF3\x94\xAB\x01\x10\x00\x60')
        event = core.transport.parse(bytes_array)
        event.device.send_on(core.transport)
        event.device.send_off(core.transport)
        self.assertRaises(ValueError,event.device.send_dim,core.transport,150)
        self.assertRaises(ValueError,event.device.send_dim,core.transport,-1)
        event.device.send_dim(core.transport,50)
        event.device.send_dim(core.transport,0)

        # Lighting5, subtype6 . unknown
        bytes_array = bytearray(b'\x0A\x14\x06\xAD\xF3\x94\xAB\x01\x10\x00\x60')
        event = core.transport.parse(bytes_array)
        event.device.send_on(core.transport)
        event.device.send_off(core.transport)
        self.assertRaises(ValueError,event.device.send_dim,core.transport,150)
        self.assertRaises(ValueError,event.device.send_dim,core.transport,-1)
        event.device.send_dim(core.transport,50)
        event.device.send_dim(core.transport,0)

        #Lighting 6
        bytes_array = [0x0b, 0x15, 0x00, 0x2a, 0x12, 0x34, 0x41, 0x05, 0x03, 0x01, 0x00, 0x70]
        event = core.transport.parse(bytes_array)
        event.device.send_on(core.transport)
        event.device.send_off(core.transport)
        self.assertRaises(ValueError,event.device.send_dim,core.transport,50)

        #rain
        bytes_array = [0x0b, 0x55, 0x02, 0x03, 0x12, 0x34, 0x02, 0x50, 0x01, 0x23, 0x45, 0x57]
        event = core.transport.parse(bytes_array)
        self.assertEqual(RFXtrx.SensorEvent, type(event))
        self.assertEqual(event.__str__(),"<class 'RFXtrx.SensorEvent'> device=[<class 'RFXtrx.RFXtrxDevice'> type='PCR800' id='12:34'] values=[('Battery numeric', 7), ('Rain rate', 5.92), ('Rain total', 7456.5), ('Rssi numeric', 5)]")

        #bbq
        bytes_array = [0x0a, 0x4e, 0x01, 0x06, 0xfc, 0xd8, 0x00, 0x13, 0x00, 0x13, 0x79]
        event = core.transport.parse(bytes_array)
        self.assertEqual(RFXtrx.SensorEvent, type(event))
        self.assertEqual(event.__str__(),"<class 'RFXtrx.SensorEvent'> device=[<class 'RFXtrx.RFXtrxDevice'> type='BBQ1 - Maverick ET-732' id='fcd800:78'] values=[('Battery numeric', 9), ('Rssi numeric', 7), ('Temperature', 19), ('Temperature2', 19)]")
        
        #baro
        bytes_array = [0x09, 0x53, 0x01, 0x2a, 0x96, 0x03, 0x04, 0x06, 0x00, 0x79]
        event = core.transport.parse(bytes_array)
        self.assertEqual(RFXtrx.SensorEvent, type(event))
        self.assertEqual(event.__str__(),"<class 'RFXtrx.SensorEvent'> device=[<class 'RFXtrx.RFXtrxDevice'> type='Unknown type (0x53/0x01)' id='96:03'] values=[('Barometer', 1030), ('Battery numeric', 9), ('Forecast', 'no forecast available'), ('Forecast numeric', 0), ('Rssi numeric', 7)]")

        #wind
        bytes_array = [0x10, 0x56, 0x01, 0x03, 0x2F, 0x00, 0x00, 0xF7, 0x00, 0x20, 0x00, 0x24, 0x81, 0x60, 0x82, 0x50, 0x59]
        event = core.transport.parse(bytes_array)
        self.assertEqual(RFXtrx.SensorEvent, type(event))
        self.assertEqual(event.__str__(),"<class 'RFXtrx.SensorEvent'> device=[<class 'RFXtrx.RFXtrxDevice'> type='WTGR800' id='2f:00'] values=[('Battery numeric', 9), ('Rssi numeric', 5), ('Wind average speed', 3.2), ('Wind direction', 247), ('Wind gust', 3.6)]")

        #uv
        bytes_array = [0x09, 0x57, 0x02, 0x02, 0x64, 0x00, 0x20, 0x02, 0x3c, 0x69]
        event = core.transport.parse(bytes_array)
        self.assertEqual(RFXtrx.SensorEvent, type(event))
        self.assertEqual(event.__str__(),"<class 'RFXtrx.SensorEvent'> device=[<class 'RFXtrx.RFXtrxDevice'> type='UVN800' id='64:00'] values=[('Battery numeric', 9), ('Rssi numeric', 6), ('UV', 3.2)]")

        #Elec4
        bytes_array = [0x13, 0x5b, 0x01, 0x04, 0x2e, 0xB2, 0x01, 0x11, 0x12, 0x14, 0x15, 0x17, 0x18, 0x17, 0x18, 0x19, 0x20, 0x21, 0x22, 0x69]
        event = core.transport.parse(bytes_array)
        self.assertEqual(RFXtrx.SensorEvent, type(event))
        self.assertEqual(event.__str__(),"<class 'RFXtrx.SensorEvent'> device=[<class 'RFXtrx.RFXtrxDevice'> type='ELEC4, CM180i' id='2e:b2'] values=[('Battery numeric', 9), ('Count', 1), ('Current Ch. 1', 437.0), ('Current Ch. 2', 514.1), ('Current Ch. 3', 591.2), ('Rssi numeric', 6), ('Total usage', 113527617921.3023)]")

        #Lighting5
        bytes_array = bytearray(b'\x0A\x14\x00\xAD\xF3\x94\xAB'
                                b'\x01\x01\x00\x60')
        event= core.transport.receive(bytes_array)
        self.assertEqual(RFXtrx.ControlEvent, type(event))
        self.assertEqual(event.__str__(),"<class 'RFXtrx.ControlEvent'> device=[<class 'RFXtrx.LightingDevice'> type='LightwaveRF, Siemens' id='f394ab:1'] values=[('Command', 'On'), ('Rssi numeric', 6)]")

        #RollerTrol
        bytes_array = bytearray(b'\x09\x19\x00\x00\x00\x9b\xa8\x01\x01\x00')
        event= core.transport.receive(bytes_array)
        self.assertEqual(RFXtrx.ControlEvent, type(event))
        self.assertEqual(event.__str__(),"<class 'RFXtrx.ControlEvent'> device=[<class 'RFXtrx.RollerTrolDevice'> type='RollerTrol' id='009ba8:1'] values=[('Command', 'Down'), ('Rssi numeric', 0)]")
        event.device.send_open(core.transport)
        event.device.send_close(core.transport)
        event.device.send_stop(core.transport)

        #Rfy
        bytes_array = bytearray(b'\x08\x1A\x00\x00\x0A\x00\x01\x01\x03')
        event= core.transport.receive(bytes_array)
        self.assertEqual(RFXtrx.ControlEvent, type(event))
        self.assertEqual(event.__str__(),"<class 'RFXtrx.ControlEvent'> device=[<class 'RFXtrx.RfyDevice'> type='Rfy' id='0a0001:1'] values=[('Command', 'Down')]")
        event.device.send_open(core.transport)
        event.device.send_close(core.transport)
        event.device.send_stop(core.transport)

        #temphumid
        bytes_array = [0x0a, 0x52, 0x01, 0x2a, 0x96, 0x03, 0x81, 0x41, 0x60, 0x03, 0x79]
        event = core.transport.parse(bytes_array)
        self.assertEqual(RFXtrx.SensorEvent, type(event))
        self.assertEqual(event.__str__(),"<class 'RFXtrx.SensorEvent'> device=[<class 'RFXtrx.RFXtrxDevice'> type='THGN122/123, THGN132, THGR122/228/238/268' id='96:03'] values=[('Battery numeric', 9), ('Humidity', 96), ('Humidity status', 'wet'), ('Humidity status numeric', 3), ('Rssi numeric', 7), ('Temperature', -32.1)]")

        #Chime
        bytes_array = [0x0a, 0x16, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        event = core.transport.parse(bytes_array)
        self.assertEqual(RFXtrx.ControlEvent, type(event))
        self.assertEqual(event.__str__(),"<class 'RFXtrx.ControlEvent'> device=[<class 'RFXtrx.ChimeDevice'> type='Byron SX' id='00:00'] values=[('Command', 'Chime'), ('Rssi numeric', 0), ('Sound', 0)]")
        event.device.send_chime(core.transport, 1)

        #security1
        bytes_array = [0x0a, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        event = core.transport.parse(bytes_array)
        self.assertEqual(RFXtrx.SensorEvent, type(event))
        self.assertEqual(event.__str__(),"<class 'RFXtrx.SensorEvent'> device=[<class 'RFXtrx.RFXtrxDevice'> type='X10 Security' id='000000:32'] values=[('Battery numeric', 0), ('Rssi numeric', 0), ('Sensor Status', 'Normal')]")

        #temp
        bytes_array = [0x0a, 0x50, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        event = core.transport.parse(bytes_array)
        self.assertEqual(RFXtrx.SensorEvent, type(event))
        self.assertEqual(event.__str__(),"<class 'RFXtrx.SensorEvent'> device=[<class 'RFXtrx.RFXtrxDevice'> type='THR128/138, THC138' id='00:00'] values=[('Battery numeric', 0), ('Rssi numeric', 0), ('Temperature', 0.0)]")

        #humid
        bytes_array = [0x0a, 0x51, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        event = core.transport.parse(bytes_array)
        self.assertEqual(RFXtrx.SensorEvent, type(event))
        self.assertEqual(event.__str__(),"<class 'RFXtrx.SensorEvent'> device=[<class 'RFXtrx.RFXtrxDevice'> type='LaCrosse TX3' id='00:00'] values=[('Battery numeric', 0), ('Humidity', 0), ('Humidity status', 'dry'), ('Humidity status numeric', 0), ('Rssi numeric', 0)]")

        #temphumidBaro
        bytes_array = [0x10, 0x54, 0x01, 0x03, 0x2F, 0x00, 0x00, 0xF7, 0x00, 0x20, 0x00, 0x24, 0x81, 0x60, 0x82, 0x50, 0x59]
        event = core.transport.parse(bytes_array)
        self.assertEqual(RFXtrx.SensorEvent, type(event))
        self.assertEqual(event.__str__(),"<class 'RFXtrx.SensorEvent'> device=[<class 'RFXtrx.RFXtrxDevice'> type='BTHR918' id='2f:00'] values=[('Barometer', 36), ('Battery numeric', 0), ('Forecast', 'unknown forecast'), ('Forecast numeric', 129), ('Humidity', 0), ('Humidity status', 'unknown humidity'), ('Humidity status numeric', 32), ('Rssi numeric', 6), ('Temperature', 24.7)]")

        #rfxmeter
        # A 71 0 1F 21 D1 0 20 1F A4 60
        bytes_array = [0x0A, 0x71, 0x00, 0x1F, 0x21, 0xD1, 0x00, 0x20, 0x1F, 0xA4, 0x60]
        event = core.transport.parse(bytes_array)
        self.assertEqual(RFXtrx.SensorEvent, type(event))
        self.assertEqual(event.device.subtype, 0x00)
        self.assertEqual(event.device.type_string, 'RFXMeter Count')
        self.assertEqual(event.device.id_string, '21')
        self.assertEqual(event.values['Counter value'], 2105252)

        #temphumidBaro, too short package length
        bytes_array = [0x10, 0x54, 0x01, 0x03, 0x2F, 0x00, 0x00, 0xF7, 0x00, 0x20, 0x00, 0x24, 0x81, 0x60, 0x82, 0x50]
        event = core.transport.parse(bytes_array)
        self.assertEqual(None, event)

        #temprain
        bytes_array = [0x0a, 0x4f, 0x01, 0x06, 0xee, 0x09, 0x00, 0x65, 0x00, 0x03, 0x69]
        event = core.transport.parse(bytes_array)
        self.assertEqual(RFXtrx.SensorEvent, type(event))
        self.assertEqual(event.__str__(),"<class 'RFXtrx.SensorEvent'> device=[<class 'RFXtrx.RFXtrxDevice'> type='TR1 - WS1200' id='ee:09'] values=[('Battery numeric', 9), ('Rain total', 0.3), ('Rssi numeric', 6), ('Temperature', 10.1)]")
       

        core.close_connection()


    def test_equal_check(self):
        data1 = bytearray(b'\x11\x5A\x01\x00\x2E\xB2\x03\x00\x00'
                          b'\x02\xB4\x00\x00\x0C\x46\xA8\x11\x69')
        energy = RFXtrx.lowlevel.parse(data1)


        data2 = bytearray(b'\x0A\x14\x00\xAD\xF3\x94\xAB'
                          b'\x01\x01\x00\x60')
        light = RFXtrx.lowlevel.parse(data2)
        light2 = RFXtrx.lowlevel.parse(data2)

        data3 = bytearray(b'\x0A\x52\x02\x11\x70\x02\x00\xA7'
                          b'\x2D\x00\x89')
        temphum = RFXtrx.lowlevel.parse(data3)

        self.assertTrue(light==light2)
        self.assertFalse(light==energy)
        self.assertFalse(temphum==energy)

    def test_equal_device_check(self):
        core = RFXtrx.Connect(self.path, event_callback=_callback, transport_protocol=RFXtrx.DummyTransport)
        data1 = bytearray(b'\x11\x5A\x01\x00\x2E\xB2\x03\x00\x00'
                          b'\x02\xB4\x00\x00\x0C\x46\xA8\x11\x69')
        energy = core.transport.receive(data1)


        data2 = bytearray(b'\x0A\x14\x00\xAD\xF3\x94\xAB'
                          b'\x01\x01\x00\x60')
        light = core.transport.receive(data2)
        light2 = core.transport.receive(data2)

        data3 = bytearray(b'\x0A\x52\x02\x11\x70\x02\x00\xA7'
                         b'\x2D\x00\x89')
        temphum = core.transport.receive(data3)

        bytes_array = bytearray(b'\x0A\x14\x00\xAD\xF3\x94\xAB\x01\x10\x00\x60')
        lighting5_subtype0 = core.transport.receive(bytes_array)

        bytes_array = bytearray(b'\x0A\x14\x01\xAD\xF3\x94\xAB\x01\x10\x00\x60')
        lighting5_subtype1 = core.transport.receive(bytes_array)

        self.assertFalse(light==light2)
        self.assertFalse(light==energy)
        self.assertFalse(temphum==energy)

        self.assertTrue(light.device==light2.device)
        self.assertFalse(light.device==energy.device)
        self.assertFalse(temphum.device==energy.device)

        self.assertFalse(lighting5_subtype0.device==lighting5_subtype1.device)
        core.close_connection()

    def test_get_device(self):
        core = RFXtrx.Connect(self.path, event_callback=_callback, transport_protocol=RFXtrx.DummyTransport)
        # Lighting1
        bytes_array = bytearray([0x07, 0x10, 0x00, 0x2a, 0x45, 0x05, 0x01, 0x70])
        event = core.transport.parse(bytes_array)
        device = RFXtrx.get_device(event.device.packettype, event.device.subtype, event.device.id_string)
        self.assertTrue(device==event.device)

        # Lighting2
        bytes_array =[0x0b, 0x11, 0x00, 0x2a, 0x01, 0x23, 0x45, 0x67, 0x05, 0x02, 0x07, 0x70]
        event = core.transport.parse(bytes_array)
        device = RFXtrx.get_device(event.device.packettype, event.device.subtype, event.device.id_string)
        self.assertTrue(device==event.device)

        # Lighting3
        bytes_array = [0x08, 0x12, 0x00, 0x2a, 0x01, 0x34, 0x02, 0x15, 0x79]
        event = core.transport.parse(bytes_array)
        device = RFXtrx.get_device(event.device.packettype, event.device.subtype, event.device.id_string)
        self.assertTrue(device==event.device)

        # Lighting4
        bytes_array = [0x09, 0x13, 0x00, 0x2a, 0x12, 0x34, 0x56, 0x01, 0x5e, 0x70]
        event = core.transport.parse(bytes_array)
        device = RFXtrx.get_device(event.device.packettype, event.device.subtype, event.device.id_string)
        self.assertTrue(device==event.device)

        # Lighting5
        bytes_array = bytearray(b'\x0A\x14\x00\xAD\xF3\x94\xAB'
                              b'\x01\x01\x00\x60')
        event = core.transport.parse(bytes_array)
        device = RFXtrx.get_device(event.device.packettype, event.device.subtype, event.device.id_string)
        self.assertTrue(device==event.device)

        #Lighting 6
        bytes_array = [0x0b, 0x15, 0x00, 0x2a, 0x12, 0x34, 0x41, 0x05, 0x03, 0x01, 0x00, 0x70]
        event = core.transport.parse(bytes_array)
        device = RFXtrx.get_device(event.device.packettype, event.device.subtype, event.device.id_string)
        self.assertTrue(device==event.device)

        #energy sensor
        bytes_array = bytearray(b'\x11\x5A\x01\x00\x2E\xB2\x03\x00\x00'
                          b'\x02\xB4\x00\x00\x0C\x46\xA8\x11\x69')
        event = core.transport.parse(bytes_array)
        self.assertRaises(ValueError, RFXtrx.get_device,event.device.packettype, event.device.subtype, event.device.id_string)
        core.close_connection()

    def test_set_recmodes(self):
        core = RFXtrx.Connect(self.path, event_callback=_callback, 
                              transport_protocol=RFXtrx.DummyTransport)
        time.sleep(0.2)
        self.assertEqual(None, core._modes)

        modes = ['ac', 'arc', 'hideki', 'homeeasy', 'keeloq', 'lacrosse', 'oregon', 'rsl', 'x10']
        bytes_array = bytearray(b'\x0D\x01\x00\x01\x02\x53\x45'
                          b'\x10' # msg3: rsl
                          b'\x0C' # msg4: hideki lacrosse
                          b'\x2F' # msg5: x10 arc ac homeeasy oregon
                          b'\x01' # msg6: keeloq
                          b'\x01\x00\x00' # unused
                         )
        core._status = core.transport.receive(bytes_array)
        core.set_recmodes(modes)
        self.assertEqual(modes, core._modes)

        # set an unknown mode
        with self.assertRaises(ValueError):
          core.set_recmodes(['arc', 'oregon', 'unknown-mode'])

    def test_receive(self):
        core = RFXtrx.Connect(self.path, event_callback=_callback, transport_protocol=RFXtrx.DummyTransport)
        time.sleep(0.2)
        # Lighting1
        bytes_array = bytearray([0x07, 0x10, 0x00, 0x2a, 0x45, 0x05, 0x01, 0x70])
        event= core.transport.receive(bytes_array)
        self.assertEqual(RFXtrx.ControlEvent, type(event))

        self.assertEqual(event.__str__(),"<class 'RFXtrx.ControlEvent'> device=[<class 'RFXtrx.LightingDevice'> type='X10 lighting' id='E5'] values=[('Command', 'On'), ('Rssi numeric', 7)]")

        #status
        bytes_array = bytearray(b'\x0D\x01\x00\x01\x02\x53\x45'
                                b'\x10' # msg3: rsl
                                b'\x0C' # msg4: hideki lacrosse
                                b'\x2F' # msg5: x10 arc ac homeeasy oregon
                                b'\x01' # msg6: keeloq
                                b'\x01\x00\x00' # unused
                               )
        event= core.transport.receive(bytes_array)
        self.assertEqual(RFXtrx.StatusEvent, type(event))
        self.assertEqual(event.__str__(),"<class 'RFXtrx.StatusEvent'> device=[Status [subtype=433.92MHz, firmware=69, output_power=0, devices=['ac', 'arc', 'hideki', 'homeeasy', 'keeloq', 'lacrosse', 'oregon', 'rsl', 'x10']]]")
        core.close_connection()
