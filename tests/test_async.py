"""Test for async connections."""
import asyncio
import logging
from typing import List

import pytest

import RFXtrx

logging.basicConfig(level=logging.DEBUG)


EVENT_1_DATA = bytes([0x07, 0x10, 0x00, 0x2A, 0x45, 0x05, 0x01, 0x70])
EVENT_1_STR = "<class 'RFXtrx.ControlEvent'> device=[<class 'RFXtrx.LightingDevice'> type='X10 lighting' id='E5'] values=[('Command', 'On'), ('Rssi numeric', 7)]"

EVENT_2_DATA = bytes(
    [0x0B, 0x55, 0x02, 0x03, 0x12, 0x34, 0x02, 0x50, 0x01, 0x23, 0x45, 0x57]
)
EVENT_2_STR = "<class 'RFXtrx.SensorEvent'> device=[<class 'RFXtrx.RFXtrxDevice'> type='PCR800' id='12:34'] values=[('Battery numeric', 7), ('Rain rate', 5.92), ('Rain total', 7456.5), ('Rssi numeric', 5)]"

# Cut an event short
EVENT_SHORT_DATA = bytes([EVENT_2_DATA[0] - 1, *EVENT_2_DATA[1:-1]])
EVENT_SHORT_STR = "<class 'RFXtrx.ExceptionEvent'> ParseError('No packet for data: 0a 55 02 03 12 34 02 50 01 23 45')"


@pytest.mark.parametrize(
    ["data", "events"],
    [
        pytest.param([EVENT_1_DATA], [EVENT_1_STR], id="one_packet"),
        pytest.param(
            [EVENT_1_DATA[:1], EVENT_1_DATA[1:]], [EVENT_1_STR], id="split_packet"
        ),
        pytest.param(
            [EVENT_1_DATA[:1], EVENT_1_DATA[1:4], EVENT_1_DATA[4:], EVENT_2_DATA],
            [EVENT_1_STR, EVENT_2_STR],
            id="combined_packet",
        ),
        pytest.param([EVENT_SHORT_DATA], [], id="invalid_len"),
    ],
)
async def test_parse_segmented(data: List[bytes], events: List[str]):
    """Verify that split packets end up parsing correctly"""
    received_events = []

    def callback(event: RFXtrx.RFXtrxEvent):
        received_events.append(str(event))

    transport = asyncio.Transport()
    protocol: asyncio.Protocol = RFXtrx.AsyncConnect(callback)
    protocol.connection_made(transport)
    for x in data:
        protocol.data_received(x)
    protocol.connection_lost(None)

    assert received_events == events
