from pyquidnuncd import Client

import SocketServer
import threading


class MockServer(object):
    class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
        allow_reuse_address = True

    def __init__(self, host='localhost', port=3230):
        self.host = host
        self.port = port

    def start(self):
        self.server = MockServer.ThreadedTCPServer((self.host, self.port), SocketServer.BaseRequestHandler)
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.setDaemon(True)
        self.thread.start()

    def stop(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()


def test_client():
    server = MockServer(port=12345)
    server.start()

    c = Client(port=12345)
    assert c._socket
    assert c._fd
    c.close()

    server.stop()
