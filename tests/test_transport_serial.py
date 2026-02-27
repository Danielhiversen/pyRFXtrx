"""Tests for PySerialTransport error handling."""

from unittest.mock import MagicMock

import pytest

import RFXtrx


def test_typeerror_during_receive_raises_transport_error():
    """TypeError from serial.read (fd=None on shutdown) is caught."""
    transport = RFXtrx.PySerialTransport("/dev/null")
    transport.serial = MagicMock()
    transport.serial.read.side_effect = TypeError(
        "an integer is required (got type NoneType)"
    )

    with pytest.raises(RFXtrx.RFXtrxTransportError, match="receive failed"):
        transport.receive_blocking()


def test_typeerror_during_send_raises_transport_error():
    """TypeError from serial.write (fd=None on shutdown) is caught."""
    transport = RFXtrx.PySerialTransport("/dev/null")
    transport.serial = MagicMock()
    transport.serial.write.side_effect = TypeError(
        "an integer is required (got type NoneType)"
    )

    with pytest.raises(RFXtrx.RFXtrxTransportError, match="send failed"):
        transport.send(b"\x00")
