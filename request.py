import re
import socket
from selectors import EVENT_WRITE, EVENT_READ

from response import Response
from future import Future, Task
from loop import selector


class Request:
    def __init__(self):
        self.url = None
        self.protocol = None
        self.host = None
        self.port = None
        self.path = None
        self.response = None

        self.sock = None

    @Task.coroutine
    def get(self, url):
        self.url = url
        if not re.match(r'^(https?://)', self.url):
            self.url = 'http://' + self.url
        url_segs = [seg for seg in re.split('(https?)://|/{1}', self.url, 2) if seg]
        if len(url_segs) == 2:
            url_segs.append('/')
        self.protocol, self.host, self.path = url_segs
        self.port = 80 if self.protocol == 'http' else 443

        self.sock = socket.socket()
        self.sock.setblocking(False)
        try:
            self.sock.connect((self.host, self.port))
        except BlockingIOError:
            pass

        f = Future()

        def on_connected(key, mask):
            f.set_result(None)

        selector.register(self.sock.fileno(), EVENT_WRITE, on_connected)
        yield from f
        selector.unregister(self.sock.fileno())

        request = 'GET {} HTTP/1.0\r\nHost: {}\r\n\r\n'.format(self.url, self.host)
        self.sock.send(request.encode('ascii'))

        def read(sock):
            f = Future()

            def on_readable(key, mask):
                f.set_result(sock.recv(4096))

            selector.register(self.sock.fileno(), EVENT_READ, on_readable)

            chunk = yield from f
            selector.unregister(self.sock.fileno())
            return chunk

        def read_all(sock):
            response = []
            chunk = yield from read(sock)
            while chunk:
                response.append(chunk)
                chunk = yield from read(sock)
            return b''.join(response)

        self.response = yield from read_all(self.sock)
        self.response = Response(self)
        print(self.response.header.status_human)
        return self.response
