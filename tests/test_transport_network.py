
import pytest
import RFXtrx

import socket
import dataclasses
import threading
from typing import Tuple, List


@pytest.fixture(name="server_socket")
def fixture_server_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 0))
    sock.settimeout(1)
    sock.listen(1)
    try:
        yield sock
    finally:
        sock.close()


@dataclasses.dataclass
class Server:
    address: Tuple
    connections: List[socket.socket]
    event = threading.Event()


@pytest.fixture(name="server")
def fixture_server(server_socket: socket.socket):

    server = Server(address=server_socket.getsockname(), connections=[])

    def runner():
        while True:
            try:
                connection, address = server_socket.accept()
                server.connections.append(connection)
                server.event.set()
            except socket.timeout:
                continue
            except socket.error:
                return
    thread = threading.Thread(target=runner, daemon=True)
    thread.start()
    try:
        yield server
    finally:
        server_socket.close()
        for connection in server.connections:
            connection.close()
        thread.join()


def connected_transport(server: Server):
    server.event.clear()
    transport = RFXtrx.PyNetworkTransport(server.address)
    transport.sock.settimeout(10)
    transport.connect()
    assert server.event.wait(10)
    return transport, server.connections[-1]


def test_transport_shutdown_between_packet(server: Server):
    transport, connection = connected_transport(server)
    connection.sendall(bytes([0x09, 0x03, 0x01, 0x04, 0x28,
                              0x0a, 0xb7, 0x66, 0x04, 0x70]))
    connection.shutdown(socket.SHUT_RDWR)

    pkt = transport.receive_blocking()
    assert isinstance(pkt, RFXtrx.SensorEvent)
    with pytest.raises(RFXtrx.RFXtrxTransportError):
        transport.receive_blocking()


def test_transport_shutdown_mid_packet(server: Server):
    transport, connection = connected_transport(server)
    connection.sendall(bytes([0x09, 0x03, 0x01, 0x04]))
    connection.shutdown(socket.SHUT_RDWR)

    with pytest.raises(RFXtrx.RFXtrxTransportError):
        transport.receive_blocking()


def test_transport_close_mid_packet(server: Server):
    transport, connection = connected_transport(server)
    connection.sendall(bytes([0x09, 0x03, 0x01, 0x04]))
    connection.close()

    with pytest.raises(RFXtrx.RFXtrxTransportError):
        transport.receive_blocking()


def test_transport_empty_packet(server: Server):
    transport, connection = connected_transport(server)
    connection.sendall(bytes([0x00]))

    assert transport.receive_blocking() is None
