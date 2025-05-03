
import pytest
from serial import Serial, SerialException
from unittest import mock
import RFXtrx


def test_open():
    serial_mock: mock.Mock | Serial = mock.Mock(spec=Serial)
    transport =  RFXtrx.PySerialTransport(0, serial_mock)
    transport.connect()
    assert serial_mock.open.call_count == 1


def test_reset(frozen_sleep):
    serial_mock: mock.Mock | Serial = mock.Mock(spec=Serial)
    transport =  RFXtrx.PySerialTransport(0, serial_mock)
    transport.connect()
    assert serial_mock.open.call_count == 1
    transport.reset()
    serial_mock.write.assert_called_with(b'\r\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    assert serial_mock.close.call_count == 1
    assert serial_mock.open.call_count == 2


def test_reset_retry(frozen_sleep):
    """Verify that we retry """
    serial_mock: mock.Mock | Serial = mock.Mock(spec=Serial)
    serial_mock.open.side_effect = [None, SerialException(), None]
    transport =  RFXtrx.PySerialTransport(0, serial_mock)
    transport.CONNECTION_RESET_TIMEOUT  = 2
    transport.CONNECTION_RETRY_INTERVAL = 1

    transport.connect()
    assert serial_mock.open.call_count == 1
    transport.reset()
    serial_mock.write.assert_called_with(b'\r\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    assert serial_mock.close.call_count == 1
    assert serial_mock.open.call_count == 3


def test_reset_retry_timeout(frozen_sleep):
    """Verify that we retry """
    serial_mock: mock.Mock | Serial = mock.Mock(spec=Serial)
    serial_mock.open.side_effect = [None, SerialException(), SerialException()]
    transport = RFXtrx.PySerialTransport(0, serial_mock)
    transport.CONNECTION_RESET_TIMEOUT  = 2
    transport.CONNECTION_RETRY_INTERVAL = 1

    transport.connect()
    with pytest.raises(RFXtrx.RFXtrxTransportError):
        transport.reset()

